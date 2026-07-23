"""Focused regressions for PR-51's config-gated enforcement seams."""
# ruff: noqa: E402 -- bin/ is intentionally added to sys.path for script-module coverage.
from __future__ import annotations

import json
import datetime as dt
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
import truth


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


def obligation_auth(**updates):
    auth = {"enabled": True, "refund_authority": True, "max_open": 1,
            "max_single_usd": 25.0, "max_total_fraction": 1.0,
            "max_deadline_hours": 24.0}
    auth.update(updates)
    return auth


def test_obligation_authorization_requires_fresh_grounded_verifier_fact(monkeypatch):
    now = dt.datetime(2026, 7, 22, 12, tzinfo=dt.timezone.utc)
    monkeypatch.setattr(obligations, "_now", lambda: now)
    facts = {"verified": True, "computed_at": now.isoformat(),
             "authorization": obligation_auth()}
    monkeypatch.setattr(truth, "load", lambda _name="truth.json": (facts, "ledger-branch"))
    assert obligations._authorization()["max_open"] == 1

    monkeypatch.setattr(truth, "load",
                        lambda _name="truth.json": (facts, "working-tree-uncommitted"))
    with pytest.raises(RuntimeError, match="not verifier-grounded"):
        obligations._authorization()

    stale = {**facts, "computed_at": (now - dt.timedelta(hours=1)).isoformat()}
    monkeypatch.setattr(truth, "load", lambda _name="truth.json": (stale, "ledger-branch"))
    with pytest.raises(RuntimeError, match="stale"):
        obligations._authorization()


def test_obligation_watch_authorization_requires_every_safeguard(monkeypatch):
    monkeypatch.setenv("OBLIGATION_CLASS_ENABLE", "1")
    monkeypatch.setenv("EXPOSURE_MAX_OPEN", "2")
    monkeypatch.setenv("EXPOSURE_MAX_SINGLE_USD", "25")
    monkeypatch.setenv("EXPOSURE_MAX_TOTAL_FRACTION", "0.5")
    monkeypatch.setenv("OBLIGATION_MAX_DEADLINE_H", "48")
    assert obligation_watch._authorization("rk_refund")["enabled"] is True
    assert obligation_watch._authorization("")["enabled"] is False
    monkeypatch.setenv("EXPOSURE_MAX_SINGLE_USD", "nan")
    assert obligation_watch._authorization("rk_refund")["enabled"] is False


def test_obligation_watch_checks_open_records_without_agent_claim(monkeypatch, tmp_path):
    out = tmp_path / "ledger" / "obligations.json"
    obligation = {"id": "obl-001", "status": "open", "what": "hosted report",
                  "check": "delivery-url:https://example.test/report",
                  "deadline": "2099-01-01T00:00:00Z", "value_usd": 10.0,
                  "charge_id": "ch_1"}

    def run(args, **_kwargs):
        if args[1:3] == ["show", "origin/agent:run/obligations.json"]:
            return SimpleNamespace(returncode=0,
                                   stdout=json.dumps({"obligations": [obligation]}), stderr="")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setenv("AGENT_BRANCH", "agent")
    monkeypatch.setattr(obligation_watch, "REPO", tmp_path)
    monkeypatch.setattr(obligation_watch, "OUT", out)
    monkeypatch.setattr(obligation_watch.subprocess, "run", run)
    monkeypatch.setattr(obligation_watch, "_authorization",
                        lambda _key: obligation_auth())
    monkeypatch.setattr(obligation_watch, "_completion_oracle",
                        lambda _spec: (True, {"kind": "delivery-url", "rc": 0}))
    assert obligation_watch.main() == 0
    facts = json.loads(out.read_text())
    assert facts["open"] == 0
    assert facts["fulfilled"][0]["id"] == "obl-001"


def test_obligation_watch_breaches_late_delivery_and_unknown_status_with_refund(monkeypatch,
                                                                                tmp_path):
    # A delivery that is reachable NOW but only after the promised deadline is a breach, not a
    # fulfilment; an unrecognized status is a breach; and BOTH must attempt the bound refund. A
    # breach that halts the run while leaving the customer un-refunded is the exact harm the rail
    # exists to prevent (pre-fix: the late URL read as fulfilled, and the unknown status refunded
    # nothing).
    out = tmp_path / "ledger" / "obligations.json"
    late = {"id": "obl-late", "status": "open", "what": "hosted report",
            "check": "delivery-url:https://example.test/report",
            "deadline": "2000-01-01T00:00:00Z", "value_usd": 10.0, "charge_id": "ch_late"}
    weird = {"id": "obl-weird", "status": "resolved", "what": "hosted report",
             "check": "delivery-url:https://example.test/report",
             "deadline": "2099-01-01T00:00:00Z", "value_usd": 10.0, "charge_id": "ch_weird"}
    refunded = []

    def run(args, **_kwargs):
        if args[1:3] == ["show", "origin/agent:run/obligations.json"]:
            return SimpleNamespace(returncode=0,
                                   stdout=json.dumps({"obligations": [late, weird]}), stderr="")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setenv("AGENT_BRANCH", "agent")
    monkeypatch.setenv("STRIPE_REFUND_KEY", "rk_test")
    monkeypatch.setattr(obligation_watch, "REPO", tmp_path)
    monkeypatch.setattr(obligation_watch, "OUT", out)
    monkeypatch.setattr(obligation_watch.subprocess, "run", run)
    monkeypatch.setattr(obligation_watch, "_authorization", lambda _key: obligation_auth())
    # the delivery URL is reachable now (oracle True); timeliness is what must decide the verdict
    monkeypatch.setattr(obligation_watch, "_completion_oracle",
                        lambda _spec: (True, {"kind": "delivery-url", "rc": 0}))
    monkeypatch.setattr(obligation_watch, "_refund",
                        lambda charge, key, oid: (refunded.append(charge) or (True, "refunded")))
    assert obligation_watch.main() == 0
    facts = json.loads(out.read_text())
    assert {b["id"] for b in facts["breached"]} == {"obl-late", "obl-weird"}
    assert not facts["fulfilled"]              # reachable-but-late is NOT a fulfilment
    assert set(refunded) == {"ch_late", "ch_weird"}   # every breached liability was refunded
    assert facts["open"] == 0                  # a breached record is not also counted as open


def test_obligation_registration_uses_verifier_caps_and_serializes(monkeypatch, tmp_path):
    registry = tmp_path / "run" / "obligations.json"
    registry.parent.mkdir()
    registry.write_text('{"obligations": []}\n')
    monkeypatch.setattr(obligations, "OBL", registry)
    monkeypatch.setattr(obligations, "LOCK", registry.with_suffix(".lock"))
    monkeypatch.setattr(obligations, "_authorization", lambda: obligation_auth())
    monkeypatch.setattr(truth, "load",
                        lambda _name="truth.json": ({"received_usd": 100}, "ledger-branch"))

    def save(records, _message):
        time.sleep(0.05)
        registry.write_text(json.dumps({"obligations": records}) + "\n")

    monkeypatch.setattr(obligations, "_save_unlocked", save)
    deadline = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=1)).isoformat()
    args = SimpleNamespace(value_usd=10.0, what="deliver hosted report",
                           check="delivery-url:https://example.test/report", deadline=deadline,
                           charge_id="ch_1")
    # Agent-local variables are deliberately irrelevant; the verifier fact above is authoritative.
    monkeypatch.setenv("EXPOSURE_MAX_OPEN", "999")
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: obligations.cmd_register(args), range(2)))
    assert results.count(0) == 1
    records = json.loads(registry.read_text())["obligations"]
    assert len(records) == 1


def test_obligation_deadline_cap_and_fulfillment_claim_are_not_self_certifying(monkeypatch,
                                                                                tmp_path):
    registry = tmp_path / "run" / "obligations.json"
    registry.parent.mkdir()
    registry.write_text('{"obligations": []}\n')
    monkeypatch.setattr(obligations, "OBL", registry)
    monkeypatch.setattr(obligations, "LOCK", registry.with_suffix(".lock"))
    monkeypatch.setattr(obligations, "_authorization",
                        lambda: obligation_auth(max_deadline_hours=1))
    monkeypatch.setattr(truth, "load",
                        lambda _name="truth.json": ({"received_usd": 100}, "ledger-branch"))
    monkeypatch.setattr(obligations, "_save_unlocked",
                        lambda records, _message: registry.write_text(
                            json.dumps({"obligations": records}) + "\n"))
    too_late = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=2)).isoformat()
    args = SimpleNamespace(value_usd=10.0, what="deliver hosted report",
                           check="delivery-url:https://example.test/report", deadline=too_late,
                           charge_id="ch_1")
    assert obligations.cmd_register(args) == 1

    soon = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=30)).isoformat()
    args.deadline = soon
    args.charge_id = ""
    assert obligations.cmd_register(args) == 1
    args.charge_id = "ch_1"
    assert obligations.cmd_register(args) == 0
    assert obligations.cmd_fulfill(SimpleNamespace(id="obl-001", evidence="report is at URL")) == 0
    record = json.loads(registry.read_text())["obligations"][0]
    assert record["status"] == "fulfillment-claimed"
    assert record["resolution"]["verified"] is False


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
