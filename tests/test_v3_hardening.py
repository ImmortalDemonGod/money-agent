"""Focused regressions for PR-51's config-gated enforcement seams."""
# ruff: noqa: E402 -- bin/ is intentionally added to sys.path for script-module coverage.
from __future__ import annotations

import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "bin"))

import bet_gate
import bets
import decision_gate
import disclosure_gate
import mail
import obligation_watch
import obligations
import spine


def typed_bet(**updates):
    bet = {
        "id": "bet-x",
        "type": "probe",
        "lane": "audience/offer",
        "status": "open",
        "success_condition": {
            "oracle_id": "deterministic",
            "metric": "observations",
            "comparator": ">=",
            "threshold": 1,
            "window_h": 24,
        },
        "authorizes": {"send": 1},
        "spent_usd": 0,
    }
    bet.update(updates)
    return bet


def test_bet_gate_rejects_nan_and_binds_lane(monkeypatch):
    invalid = typed_bet()
    invalid["success_condition"]["threshold"] = float("nan")
    assert any("finite" in error for error in bet_gate.validate_bet(invalid))

    monkeypatch.setenv("BET_GATE_ENFORCE", "1")
    monkeypatch.setattr(bets, "_load", lambda: [typed_bet()])
    assert not bet_gate.authorize("send", bet_id="bet-x", lane="other/lane")[0]
    assert not bet_gate.authorize("send")[0]


def test_bet_gate_enforces_cumulative_spend(monkeypatch):
    bet = typed_bet(authorizes={"spend": 2}, max_spend_usd=10)
    monkeypatch.setenv("BET_GATE_ENFORCE", "1")
    monkeypatch.setattr(bets, "_load", lambda: [bet])

    @contextmanager
    def transaction(_message):
        yield [bet]

    monkeypatch.setattr(bets, "_transaction", transaction)
    assert bet_gate.authorize("spend", True, bet_id="bet-x", amount_usd=6)[0]
    assert not bet_gate.authorize("spend", True, bet_id="bet-x", amount_usd=5)[0]


def test_bets_save_path_limits_commit(monkeypatch, tmp_path):
    calls = []
    monkeypatch.setattr(bets, "REPO", tmp_path)
    monkeypatch.setattr(bets, "BETS", tmp_path / "run" / "bets.json")
    monkeypatch.setattr(bets, "LOCK", tmp_path / "run" / "bets.lock")

    def fake_run(args, **_kwargs):
        calls.append(args)
        rc = 1 if args[1:4] == ["diff", "--cached", "--quiet"] else 0
        return SimpleNamespace(returncode=rc, stdout="branch", stderr="")

    monkeypatch.setattr(bets.subprocess, "run", fake_run)
    bets._save([], "test")
    commit = next(args for args in calls if "commit" in args)
    assert "--" in commit
    assert str(bets.BETS) in commit


def test_bet_gate_serializes_reservation_consumption(monkeypatch, tmp_path):
    registry = tmp_path / "run" / "bets.json"
    registry.parent.mkdir()
    registry.write_text(json.dumps({"bets": [typed_bet()]}) + "\n")
    monkeypatch.setenv("BET_GATE_ENFORCE", "1")
    monkeypatch.setattr(bets, "BETS", registry)
    monkeypatch.setattr(bets, "LOCK", registry.with_suffix(".lock"))

    def save(records, _message):
        time.sleep(0.05)  # widen the lost-update window; the shared lock must still admit one.
        registry.write_text(json.dumps({"bets": records}) + "\n")

    monkeypatch.setattr(bets, "_save_unlocked", save)
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: bet_gate.authorize("send", True, bet_id="bet-x"),
                                range(2)))
    assert [ok for ok, _why in results].count(True) == 1
    assert json.loads(registry.read_text())["bets"][0]["authorizes"]["send"] == 0


def test_mail_refusal_does_not_consume_reservation(monkeypatch):
    calls = []

    def authorize(_action, consume=False, **_binding):
        calls.append(consume)
        return True, "ok"

    monkeypatch.setenv("BET_GATE_ENFORCE", "1")
    monkeypatch.setattr(bet_gate, "authorize", authorize)
    with pytest.raises(SystemExit):
        mail.send("buyer@example.com", "subject", "bad—body",
                  bet_id="bet-x", lane="audience/offer")
    assert calls == [False]


def test_mail_audit_failure_rolls_back_consumed_reservation(monkeypatch, tmp_path):
    calls = []
    rollbacks = []
    monkeypatch.setenv("BET_GATE_ENFORCE", "1")
    monkeypatch.setattr(disclosure_gate, "check", lambda _body: (True, "ok"))
    monkeypatch.setattr(bet_gate, "authorize",
                        lambda _action, consume=False, **_binding:
                        (calls.append(consume) or (True, "ok")))
    monkeypatch.setattr(bet_gate, "rollback",
                        lambda action, **binding:
                        (rollbacks.append((action, binding)) or (True, "rolled back")))
    monkeypatch.setattr(mail, "SENT_LOG", tmp_path / "SENT_LOG.md")
    monkeypatch.setattr(mail.subprocess, "run",
                        lambda *_args, **_kwargs: (_ for _ in ()).throw(OSError("disk full")))
    with pytest.raises(SystemExit):
        mail.send("buyer@example.com", "subject", "plain body",
                  bet_id="bet-x", lane="audience/offer")
    assert calls == [False, True]
    assert rollbacks == [("send", {"bet_id": "bet-x", "lane": "audience/offer"})]


def test_mail_attempt_is_bound_consumed_and_honestly_logged(monkeypatch, tmp_path):
    calls = []
    monkeypatch.setenv("BET_GATE_ENFORCE", "1")
    monkeypatch.setattr(disclosure_gate, "check", lambda _body: (True, "ok"))
    monkeypatch.setattr(bet_gate, "authorize",
                        lambda _action, consume=False, **binding:
                        (calls.append((consume, binding)) or (True, "ok")))
    monkeypatch.setattr(mail, "SENT_LOG", tmp_path / "SENT_LOG.md")

    def run(args, **_kwargs):
        if args[1:4] == ["diff", "--cached", "--quiet"]:
            return SimpleNamespace(returncode=1, stdout="", stderr="")
        if args[1:3] == ["branch", "--show-current"]:
            return SimpleNamespace(returncode=0, stdout="branch\n", stderr="")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    class SMTP:
        def __init__(self, *_args, **_kwargs): pass
        def __enter__(self): return self
        def __exit__(self, *_args): return None
        def starttls(self): pass
        def login(self, *_args): pass
        def send_message(self, _message): pass

    monkeypatch.setattr(mail.subprocess, "run", run)
    monkeypatch.setattr(mail, "_ProxySMTP", SMTP)
    mail.send("buyer@example.com", "subject", "plain body",
              bet_id="bet-x", lane="audience/offer")
    assert calls == [(False, {"bet_id": "bet-x", "lane": "audience/offer"}),
                     (True, {"bet_id": "bet-x", "lane": "audience/offer"})]
    assert "delivery not yet confirmed" in mail.SENT_LOG.read_text()


def test_deferred_obligations_are_refused_and_recorded(monkeypatch):
    refusals = []
    monkeypatch.setattr(obligations, "_record_refusal", refusals.append)
    args = SimpleNamespace(value_usd=float("nan"), what="x", check="delivery-url:https://x.test",
                           deadline="2099-01-01T00:00:00Z", charge_id="")
    assert obligations.cmd_register(args) == 1
    assert refusals == ["x"]
    claim = SimpleNamespace(id="obl-x", evidence="delivered at URL")
    assert obligations.cmd_fulfill(claim) == 1


def test_obligation_watch_rejects_shell_and_idempotently_refunds(monkeypatch):
    assert not obligation_watch._completion_oracle("true")[0]
    seen = []

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

        def read(self):
            return json.dumps({"id": "re_1", "status": "succeeded"}).encode()

    monkeypatch.setattr(obligation_watch.urllib.request, "urlopen",
                        lambda request, timeout: (seen.append(request) or Response()))
    assert obligation_watch._refund("ch_1", "secret", "obl-007")[0]
    assert seen[0].headers["Idempotency-key"] == "money-agent-obligation-obl-007"


def test_closed_lane_cannot_reopen_past_active_cap(monkeypatch):
    monkeypatch.setenv("SPINE_ENFORCE", "1")

    def bet(lane, status="open"):
        return {"id": lane, "lane": lane, "type": "probe", "status": status,
                "last_checked": None, "poll_after_h": 1,
                "resolve_by": "2099-01-01T00:00:00Z", "resolution": None}

    records = [bet("a"), bet("b"), bet("c"), bet("closed", "lost")]
    assert any("lane cap" in error
               for error in spine.check_placement("probe", "closed", records))


def test_provenance_must_name_a_committed_blob(monkeypatch, tmp_path):
    body = "acquired payload"
    untracked = ROOT / "untracked-pr51-manifest.tmp"
    untracked.write_text("manifest")
    try:
        digest = __import__("hashlib").sha256(untracked.read_bytes()).hexdigest()
        log = tmp_path / "DECISION_LOG.md"
        log.write_text(f"- class:data-acquisition | body:{decision_gate.body_hash(body)} | "
                       "decision:acquire | rationale:reviewed source | "
                       f"manifest:{untracked.name} | provenance:{digest}\n")
        monkeypatch.setattr(decision_gate, "LOG", log)
        assert not decision_gate.check("data-acquisition", body)[0]
    finally:
        untracked.unlink(missing_ok=True)


def test_decision_gate_requires_exact_parsed_fields(monkeypatch, tmp_path):
    body = "public listing body"
    h = decision_gate.body_hash(body)
    log = tmp_path / "DECISION_LOG.md"
    log.write_text(f"- class:wrong | body:wrong | rationale:contains class:publish and body:{h} "
                   "as substrings | decision:ship\n")
    monkeypatch.setattr(decision_gate, "LOG", log)
    assert decision_gate._decision("publish", h) is None


def test_typed_resolution_evaluates_declared_metric(monkeypatch):
    record = typed_bet(check="printf '{\"observations\":1}'", oracle="judgment",
                       resolve_by="2099-01-01T00:00:00Z", clock="other", what="probe",
                       placed_at="2026-01-01T00:00:00Z", checks=[], last_checked=None,
                       poll_after_h=1, resolution=None)

    @contextmanager
    def transaction(_message):
        yield [record]

    monkeypatch.setattr(bets, "_transaction", transaction)
    import append_log
    monkeypatch.setattr(append_log, "append", lambda *_args, **_kwargs: None)
    args = SimpleNamespace(id="bet-x", outcome="won", evidence="observed metric",
                           downgrade_judgment=False)
    assert bets.cmd_resolve(args) == 0
    assert record["resolution"]["condition_result"]["success"] is True
