#!/usr/bin/env python3
"""P6 -- the substrate-probe registry (S11). host_check.py proved the rule: a claim about a layer
is false until the LAYER ITSELF is probed (run 1 shipped ~60 iterations of "published" product a
host silently hid). This registry makes the rule enumerable: every claim TYPE names the probe
that must PASS before the claim may be made, so "which probe do I owe?" has one answer.

  claim type    probe                                     gate that re-runs it
  published     bin/host_check.py <url>                   aiv_gate stage 2b (HOST_CHECK_URL)
  paid-offer    bin/delivery_check.py <url> [--payment-link <url>]
                                                          aiv_gate stage 2c (DELIVERY_CHECK_URL)
  mail-roundtrip  built-in: send-to-self + IMAP poll      operator acceptance / SETUP preflight

Usage:
    python3 bin/probes.py list
    python3 bin/probes.py run <type> <target...>   # dispatches; exit mirrors the probe's
The mail-roundtrip probe needs GMAIL creds in the environment (source .env.agent) and proves the
send->receive loop end-to-end -- the M5-era propagation test, made a named probe.
"""
from __future__ import annotations
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

REGISTRY = {
    "published": {"cmd": ["python3", "bin/host_check.py"], "args": "<url>",
                  "gate": "aiv_gate 2b re-runs it on HOST_CHECK_URL"},
    "paid-offer": {"cmd": ["python3", "bin/delivery_check.py"],
                   "args": "<delivery-url> [--payment-link <url>]",
                   "gate": "aiv_gate 2c re-runs it on DELIVERY_CHECK_URL"},
    "mail-roundtrip": {"cmd": None, "args": "(no target: sends to self, polls the inbox)",
                       "gate": "operator acceptance (SETUP preflight)"},
}


def _mail_roundtrip() -> int:
    addr = os.environ.get("GMAIL_ADDRESS", "")
    if not addr or "REPLACE_ME" in addr:
        print("FATAL: GMAIL_ADDRESS unset -- source .env.agent first (the two-env-files trap: a "
              "missing credential means you did not source it, not that mail is broken).",
              file=sys.stderr)
        return 2
    sys.path.insert(0, str(REPO / "bin"))
    import mail
    token = f"probe-{int(time.time())}"
    mail.send(addr, f"mail-roundtrip {token}", f"substrate probe {token}: delete me")
    for i in range(6):
        time.sleep(10)
        r = subprocess.run(["python3", str(REPO / "bin" / "mail.py"), "search", token],
                          capture_output=True, text=True, timeout=60)
        if token in r.stdout:
            print(f"\nPROBE: mail-roundtrip | token={token} | verdict=PASS")
            return 0
    print(f"\nPROBE: mail-roundtrip | token={token} | verdict=FAIL (sent but never arrived "
          "within 60s -- the send->receive loop is broken)", file=sys.stderr)
    return 1


def main() -> int:
    a = sys.argv[1:]
    if a and a[0] == "list":
        for t, spec in REGISTRY.items():
            print(f"{t:<15} {' '.join(spec['cmd']) if spec['cmd'] else '(built-in)'} "
                  f"{spec['args']}\n{'':<15}   -> {spec['gate']}")
        return 0
    if len(a) >= 2 and a[0] == "run" or (len(a) == 2 and a[0] == "run"):
        typ = a[1]
        if typ not in REGISTRY:
            print(f"FATAL: unknown claim type {typ!r} (known: {tuple(REGISTRY)}). A claim type "
                  "without a registered probe is a claim nothing can verify -- register the "
                  "probe first (reviewed harness change).", file=sys.stderr)
            return 2
        if typ == "mail-roundtrip":
            return _mail_roundtrip()
        spec = REGISTRY[typ]
        r = subprocess.run(spec["cmd"] + a[2:], cwd=REPO)
        print(f"\nPROBE: {typ} | verdict={'PASS' if r.returncode == 0 else 'FAIL'}")
        return r.returncode
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
