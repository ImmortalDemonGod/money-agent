"""Focused regressions for PR-51's config-gated enforcement seams."""
# ruff: noqa: E402 -- bin/ is intentionally added to sys.path for script-module coverage.
from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "bin"))

import bet_gate
import bets
import decision_gate
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
    monkeypatch.setattr(bets, "_save", lambda *_: None)
    assert bet_gate.authorize("spend", True, bet_id="bet-x", amount_usd=6)[0]
    assert not bet_gate.authorize("spend", True, bet_id="bet-x", amount_usd=5)[0]


def test_bets_save_path_limits_commit(monkeypatch, tmp_path):
    calls = []
    monkeypatch.setattr(bets, "REPO", tmp_path)
    monkeypatch.setattr(bets, "BETS", tmp_path / "run" / "bets.json")

    def fake_run(args, **_kwargs):
        calls.append(args)
        rc = 1 if args[1:4] == ["diff", "--cached", "--quiet"] else 0
        return SimpleNamespace(returncode=rc, stdout="branch", stderr="")

    monkeypatch.setattr(bets.subprocess, "run", fake_run)
    bets._save([], "test")
    commit = next(args for args in calls if "commit" in args)
    assert "--" in commit
    assert str(bets.BETS) in commit


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


def test_obligation_values_and_fulfillment_are_fail_closed(monkeypatch):
    args = SimpleNamespace(value_usd=float("nan"), what="x", check="delivery-url:https://x.test",
                           deadline="2099-01-01T00:00:00Z", charge_id="")
    assert obligations.cmd_register(args) == 1

    record = {"id": "obl-x", "status": "open", "check": "delivery-url:https://x.test"}
    monkeypatch.setattr(obligations, "_load", lambda: [record])
    monkeypatch.setattr(obligations, "_save", lambda *_: None)
    claim = SimpleNamespace(id="obl-x", evidence="delivered at URL")
    assert obligations.cmd_fulfill(claim) == 0
    assert record["status"] == "fulfillment-claimed"


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
