#!/usr/bin/env python3
"""OPERATOR-side fulfill web form (out-of-sandbox) -- the no-terminal surface for the queue.

The operator was expected to type `bin/actuate.py fulfill ACT-001 --minutes 14 --evidence "..."
--return-file cred.txt` in a terminal, on the facts-lane clone, with env vars set, under a deadline.
That is too much work for a human. This is the friendly surface: the operator opens a local web
page (from the notification link, on phone or laptop), reads the card, does the real action, pastes
any credential, and taps Submit. It measures the human-minutes itself.

What it does NOT change: the fulfillment is still SIGNED on the facts lane -- that signature is the
whole separation-of-duties wall. This server holds no new secret and signs nothing itself; it shells
out to `bin/actuate.py fulfill/decline`, which does the signing with the operator's key. It runs
ONLY on the operator's machine (like bin/actuate_notify.sh), binds localhost by default, and is in
the SoD blocklist so the agent cannot edit it. A pasted credential is written to a private temp file,
handed to fulfill (which encrypts it to the request's published key), and unlinked -- it never leaves
the machine except as ciphertext, and is never logged.

Run (on the operator's machine, facts-lane clone):
    AGENT_BRANCH=<run-branch> LEDGER_BRANCH=<facts-branch> MONEY_AGENT_STATE=~/.money-agent-operator \
      python3 bin/actuate_fulfill_server.py            # -> http://127.0.0.1:8765
Options: --host (default 127.0.0.1), --port (default 8765).
"""
from __future__ import annotations

import argparse
import html
import os
import subprocess
import sys
import tempfile
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "bin"))
import actuate  # noqa: E402  (operator-side; same repo)

# When the operator first OPENED each task's form -> used to measure hands-on human-minutes.
_OPENED: dict[str, float] = {}


def _minutes_since_open(task_id: str) -> float:
    """Hands-on operator time: form-open -> submit, floored at 0.1 min. Overridable in the form."""
    started = _OPENED.get(task_id)
    return round(max(0.1, (time.monotonic() - started) / 60.0), 1) if started else 1.0


def perform_fulfill(task_id: str, minutes: float, evidence: str, return_kind: str,
                    return_text: str | None = None, consent_ruling: str = "") -> tuple[bool, str]:
    """Run the SIGNED `actuate.py fulfill` for the operator (the web form's backend, and the test
    seam). Writes any pasted credential to a private temp file passed via --return-file, then
    unlinks it. Returns (ok, combined-output)."""
    cmd = ["python3", str(REPO / "bin" / "actuate.py"), "fulfill", task_id,
           "--minutes", str(minutes), "--evidence", evidence]
    tmp = None
    try:
        if return_kind == "credential":
            fd, tmp = tempfile.mkstemp(prefix="actuate-cred-")
            os.write(fd, (return_text or "").encode())
            os.close(fd)
            os.chmod(tmp, 0o600)
            cmd += ["--return-file", tmp]
        elif return_kind in ("value", "confirmation"):
            cmd += ["--return-value", return_text or ""]
        if consent_ruling.strip():
            cmd += ["--consent-ruling", consent_ruling.strip()]
        p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, timeout=180)
        return p.returncode == 0, (p.stdout + p.stderr).strip()
    finally:
        if tmp and os.path.exists(tmp):
            os.unlink(tmp)


def perform_decline(task_id: str, minutes: float, reason: str) -> tuple[bool, str]:
    """Run the SIGNED `actuate.py decline` for the operator. Returns (ok, combined-output)."""
    p = subprocess.run(["python3", str(REPO / "bin" / "actuate.py"), "decline", task_id,
                        "--minutes", str(minutes), "--reason", reason],
                       cwd=REPO, capture_output=True, text=True, timeout=120)
    return p.returncode == 0, (p.stdout + p.stderr).strip()


# ---- HTML (self-contained, no external assets) ------------------------------------------
_PAGE = """<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>money-agent · fulfill</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#0b1020;color:#c8d2ea;
font-family:-apple-system,Segoe UI,Roboto,sans-serif;padding:18px;max-width:720px;margin:0 auto}}
h1{{font-size:17px;color:#fff}}a{{color:#7aa2ff;text-decoration:none}}
.card{{background:#12182b;border:1px solid #263154;border-radius:12px;padding:16px 18px;margin:14px 0}}
.k{{color:#7ee787}}.h2{{color:#7aa2ff;font-weight:700;text-transform:uppercase;font-size:11px;letter-spacing:.6px;margin:12px 0 4px}}
b{{color:#eaf0ff}}label{{display:block;margin:12px 0 4px;color:#9fb0d8;font-size:13px}}
input,textarea{{width:100%;background:#0c1226;border:1px solid #2b385f;border-radius:8px;color:#eaf0ff;
padding:10px;font-size:14px;font-family:inherit}}textarea{{min-height:70px;font-family:ui-monospace,monospace}}
button{{margin-top:14px;background:#2f6df0;color:#fff;border:0;border-radius:9px;padding:12px 18px;
font-size:15px;font-weight:600;cursor:pointer}}button.d{{background:#3a2233;color:#ffb4c4;margin-left:8px}}
.li{{display:block;padding:12px 14px;border:1px solid #263154;border-radius:10px;margin:8px 0;background:#12182b}}
.u{{color:#f0b429;font-weight:700;font-size:11px}}.muted{{color:#6f7ba0;font-size:12px}}
pre{{white-space:pre-wrap;font-family:ui-monospace,monospace;font-size:12.5px;color:#cdd8f0}}
.ok{{color:#7ee787}}.err{{color:#ff8b8b}}
</style>{body}"""


def _tid_ok(tid: str) -> bool:
    """Accept only the ACT-NNN id shape (no path traversal / injection into the CLI id arg)."""
    import re
    return bool(re.fullmatch(r"ACT-\d{1,6}", tid or ""))


class Handler(BaseHTTPRequestHandler):
    def _send(self, body: str, code: int = 200):
        b = _PAGE.format(body=body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def log_message(self, *a):  # keep the console quiet; never log form bodies
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ("/", ""):
            return self._list()
        if parsed.path.startswith("/task/"):
            return self._task(parsed.path[len("/task/"):])
        self._send("<h1>not found</h1><a href=/>&larr; queue</a>", 404)

    def _list(self):
        try:
            tasks = actuate._operator_open_tasks()
        except Exception as e:
            return self._send(f"<h1>money-agent · fulfill</h1><p class=err>Cannot read the queue: "
                              f"{html.escape(str(e))}</p><p class=muted>Set AGENT_BRANCH / "
                              "MONEY_AGENT_STATE and run from the facts-lane clone.</p>")
        if not tasks:
            body = "<h1>money-agent · fulfill</h1><p class=muted>No open requests. 🎉</p>"
        else:
            rows = []
            for t in tasks:
                tid = html.escape(t.get("id", ""))
                urg = "<span class=u>● </span>" if t.get("kind") in actuate.MONEY_MOVING_KINDS else ""
                rows.append(f'<a class=li href="/task/{tid}">{urg}<b>{tid}</b> — '
                            f'{html.escape(actuate._scrub(t.get("kind","")))}<br>'
                            f'<span class=muted>{html.escape(actuate._scrub(t.get("gate","")))[:90]} · '
                            f'deadline {html.escape(actuate._scrub(t.get("deadline","")))}</span></a>')
            body = "<h1>money-agent · open requests</h1>" + "".join(rows)
        self._send(body)

    def _task(self, tid: str):
        if not _tid_ok(tid):
            return self._send("<h1>bad id</h1><a href=/>&larr; queue</a>", 400)
        try:
            task = actuate._operator_task(tid)
        except Exception as e:
            return self._send(f"<h1>{html.escape(tid)}</h1><p class=err>{html.escape(str(e))}</p>"
                              "<a href=/>&larr; queue</a>", 404)
        _OPENED.setdefault(tid, time.monotonic())   # start the human-minutes clock
        rk = task.get("return_kind", "none")
        card = html.escape(_card_to_html_source(task))
        ret_field = ""
        if rk == "credential":
            ret_field = ('<label>Paste the credential the action produced (stays on this machine; '
                         'encrypted before it touches git)</label><textarea name=return_text '
                         'autocomplete=off></textarea>')
        elif rk in ("value", "confirmation"):
            ret_field = (f'<label>The {rk} to hand back</label>'
                         '<input name=return_text autocomplete=off>')
        p3 = ""
        if task.get("kind") in actuate.MONEY_MOVING_KINDS:
            p3 = ('<label>P3 name-test ruling (required for money-moving; ≥ 20 chars) — is this '
                  'transaction acceptable on the account holder’s statement?</label>'
                  '<textarea name=consent_ruling></textarea>')
        body = (f'<a href=/>&larr; queue</a><div class=card><pre>{card}</pre></div>'
                f'<form method=post action="/fulfill"><input type=hidden name=id value="{html.escape(tid)}">'
                f'<input type=hidden name=return_kind value="{html.escape(rk)}">'
                '<label>What you did (one line is fine)</label>'
                '<input name=evidence value="performed the action" autocomplete=off>'
                f'{ret_field}{p3}'
                '<label>Minutes it took (auto-measured; edit if needed)</label>'
                f'<input name=minutes value="{_minutes_since_open(tid)}">'
                '<button type=submit>Submit (sign &amp; publish)</button></form>'
                f'<form method=post action="/decline" style="margin-top:10px">'
                f'<input type=hidden name=id value="{html.escape(tid)}">'
                '<input name=reason placeholder="reason to decline" autocomplete=off>'
                '<button class=d type=submit>Decline</button></form>')
        self._send(body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0") or "0")
        data = urllib.parse.parse_qs(self.rfile.read(length).decode(), keep_blank_values=True)
        get = lambda k: (data.get(k, [""])[0])
        tid = get("id")
        if not _tid_ok(tid):
            return self._send("<h1>bad id</h1><a href=/>&larr; queue</a>", 400)
        try:
            minutes = float(get("minutes") or _minutes_since_open(tid))
        except ValueError:
            minutes = _minutes_since_open(tid)
        if urllib.parse.urlparse(self.path).path == "/decline":
            ok, msg = perform_decline(tid, minutes, get("reason") or "declined by operator")
            verb = "declined"
        else:
            ok, msg = perform_fulfill(tid, minutes, get("evidence") or "performed the action",
                                      get("return_kind") or "none", get("return_text"),
                                      get("consent_ruling"))
            verb = "fulfilled"
        _OPENED.pop(tid, None)
        cls = "ok" if ok else "err"
        head = (f"<span class={cls}>✓ {verb} — signed &amp; published</span>" if ok
                else f"<span class=err>✗ not {verb}</span>")
        self._send(f"<h1>{html.escape(tid)}</h1><p>{head}</p><pre>{html.escape(msg)}</pre>"
                   "<a href=/>&larr; back to the queue</a>")


def _card_to_html_source(task: dict) -> str:
    """The rendered operator card (reuses actuate._render_card for identical wording/scrubbing);
    the CLI recipe is omitted since the form itself provides the fulfill/decline controls."""
    return actuate._render_card(task, include_cli=False)


def main() -> int:
    """Serve the operator fulfill form on the operator's machine."""
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    a = ap.parse_args()
    if not os.environ.get("AGENT_BRANCH"):
        print("warn: AGENT_BRANCH is unset -- the queue will be empty until you set it (and "
              "LEDGER_BRANCH / MONEY_AGENT_STATE), from the facts-lane clone.", file=sys.stderr)
    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    print(f"operator fulfill form: http://{a.host}:{a.port}  (Ctrl-C to stop)", file=sys.stderr)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
