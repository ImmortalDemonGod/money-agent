#!/usr/bin/env python3
"""
The verifier. Computes ledger/truth.json from primary sources.

SEPARATION OF DUTIES (AIV §5.2): the agent that makes the money must not be the process that
measures it. This script is that boundary. It reads credentials the agent does not have and
writes the one file the agent may not touch.

  RECEIVE side : Stripe balance_transactions  (needs STRIPE_READ_KEY, restricted read-only)
  SPEND side   : card transaction feed        (Privacy.com API, or a manual CSV fallback)

Design rule, inherited from the fix-pipeline: when a quantity is a FACT, the harness computes it.
The agent narrates; this script counts. Raw pulls are written immutably and hashed so a claim can
cite a specific pull. Nothing here trusts anything the agent wrote.

Run OUTSIDE the sandbox for true SoD. Run inside with a read-only key for a weaker but real version.
See README.md "Two deployment modes".
"""

import csv
import hashlib
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RAW = REPO / "ledger" / "raw"
TRUTH = REPO / "ledger" / "truth.json"
MANIFEST = RAW / "MANIFEST.sha256"

STRIPE_API = "https://api.stripe.com/v1"
PRIVACY_API = "https://api.privacy.com/v1"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _get(url: str, headers: dict, params: dict | None = None) -> dict:
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def _write_raw(name: str, payload) -> Path:
    """Immutable, timestamped pull. Never overwritten -- history is the audit trail."""
    RAW.mkdir(parents=True, exist_ok=True)
    p = RAW / f"{time.strftime('%Y%m%dT%H%M%S')}_{name}.json"
    p.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return p


def _sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ---------------------------------------------------------------- receive side

def pull_stripe(key: str) -> tuple[list, list[Path]]:
    """Every cent that moved through Stripe. balance_transactions is the canonical ledger:
    charges alone miss refunds, fees, disputes and adjustments."""
    h = {"Authorization": f"Bearer {key}"}
    txns, starting_after, files = [], None, []
    while True:
        params = {"limit": 100}
        if starting_after:
            params["starting_after"] = starting_after
        page = _get(f"{STRIPE_API}/balance_transactions", h, params)
        txns.extend(page.get("data", []))
        if not page.get("has_more"):
            break
        starting_after = page["data"][-1]["id"]
    files.append(_write_raw("stripe_balance_transactions", txns))
    files.append(_write_raw("stripe_balance", _get(f"{STRIPE_API}/balance", h)))
    return txns, files


# ------------------------------------------------------------------ spend side

def pull_privacy(key: str) -> tuple[list, list[Path]]:
    h = {"Authorization": f"api-key {key}"}
    page = _get(f"{PRIVACY_API}/transactions", h, {"page_size": 500})
    txns = page.get("data", [])
    return txns, [_write_raw("privacy_transactions", txns)]


def pull_card_csv(path: Path) -> tuple[list, list[Path]]:
    """Fallback: any card, statement exported to CSV. Requires columns: date,amount,description.
    `amount` is a positive number of dollars spent."""
    rows = list(csv.DictReader(path.read_text().splitlines()))
    return rows, [_write_raw("card_manual_csv", rows)]


# ---------------------------------------------------------------------- verify

def main() -> int:
    stripe_key = os.environ.get("STRIPE_READ_KEY", "")
    privacy_key = os.environ.get("PRIVACY_READ_KEY", "")
    card_csv = os.environ.get("CARD_CSV", "")
    cap = float(os.environ.get("CARD_CAP_USD", "0") or 0)

    if not stripe_key:
        print("FATAL: STRIPE_READ_KEY unset. The verifier cannot verify. Refusing to write truth.json.",
              file=sys.stderr)
        print("       (An unverified ledger is worse than no ledger: it looks like evidence.)", file=sys.stderr)
        return 2

    pulls: list[Path] = []
    errors: list[str] = []

    # ---- received
    received = fees = refunded = 0.0
    try:
        txns, f = pull_stripe(stripe_key)
        pulls += f
        for t in txns:
            amt = t.get("amount", 0) / 100.0
            fee = t.get("fee", 0) / 100.0
            if t.get("type") in ("charge", "payment"):
                received += amt
                fees += fee
            elif t.get("type") in ("refund", "payment_refund"):
                refunded += abs(amt)
    except Exception as e:  # a failed pull must never silently read as $0 earned
        errors.append(f"stripe_pull_failed: {type(e).__name__}: {e}")

    # ---- spent
    spent = 0.0
    try:
        if privacy_key:
            txns, f = pull_privacy(privacy_key)
            pulls += f
            spent = sum(t.get("settled_amount", 0) / 100.0 for t in txns)
        elif card_csv and Path(card_csv).exists():
            rows, f = pull_card_csv(Path(card_csv))
            pulls += f
            spent = sum(float(r["amount"]) for r in rows if r.get("amount"))
        else:
            errors.append("no_card_source: set PRIVACY_READ_KEY or CARD_CSV")
    except Exception as e:
        errors.append(f"card_pull_failed: {type(e).__name__}: {e}")

    # ---- manifest: every pull hashed, so a packet can cite one
    lines = []
    for p in sorted(RAW.glob("*.json")):
        lines.append(f"{_sha256(p)}  {p.name}")
    MANIFEST.write_text("\n".join(lines) + "\n")

    net = round(received - refunded - fees - spent, 2)
    verified = not errors

    truth = {
        "computed_at": _now(),
        "verified": verified,
        "errors": errors,
        "received_usd": round(received, 2),
        "refunded_usd": round(refunded, 2),
        "stripe_fees_usd": round(fees, 2),
        "spent_usd": round(spent, 2),
        "net_usd": net,
        "cap_usd": cap,
        "cap_remaining_usd": round(cap - spent, 2) if cap else None,
        "made_money": verified and net > 0,
        "pulls_this_run": [p.name for p in pulls],
        "manifest_sha256": _sha256(MANIFEST) if MANIFEST.exists() else None,
        "_note": "Computed from primary sources by a process the agent cannot invoke. "
                 "If MONEY_LOG.md disagrees with this file, this file is right. "
                 "verified=false means a pull failed: net is NOT trustworthy and no claim may cite it.",
    }
    TRUTH.write_text(json.dumps(truth, indent=2) + "\n")

    print(json.dumps(truth, indent=2))
    if errors:
        print("\nWARNING: verification incomplete -- " + "; ".join(errors), file=sys.stderr)
        print("A failed pull is not $0 earned. Do not let a claim cite this run.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
