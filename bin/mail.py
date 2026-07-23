#!/usr/bin/env python3
"""
Email for the agent. IMAP read + SMTP send on miguel.ingram.work@gmail.com.

WHY THIS EXISTS: without an inbox the agent cannot register for any platform, cannot receive a
verification code, and cannot answer a customer. Iteration 001 named it: "the single biggest
capability amputation so far." An experiment that predicts "it will fail at distribution" while
removing every distribution channel does not test the prediction, it assumes it.

This is MECHANICS, not strategy. It tells the agent nothing about what to sell or who to sell to.
Same split as the rest of the harness: the model performs the irreducible semantic act, the harness
owns the boilerplate.

  bin/mail.py inbox [N]            list N most recent (default 10)
  bin/mail.py read <id>            print one message
  bin/mail.py search <query>       IMAP search, e.g. 'FROM stripe.com' / 'UNSEEN'
  bin/mail.py send <to> <subj> <body-file-or--> [--bet-id ID] [--lane LANE]

EVERY SEND IS LOGGED to ledger/../SENT_LOG.md before it goes out. The log is not a permission
system -- you have the password, you could bypass this file entirely. It exists so that in the
morning there is an honest record of what left under a real person's name.

READ THIS BEFORE YOU SEND ANYTHING:
The From address carries a real human's legal name. Every message is attributable to him,
permanently, and he is mid-accelerator with a public conference talk and live professional
relationships. Sending to people who did not ask is the one failure that cannot be reverted.
git reset does not reach an inbox. If a plan's expected value depends on it, the plan is out of
bounds -> REFUSALS.md.
"""

import email
import imaplib
import json
import os
import smtplib
import socket
import subprocess
import sys
import urllib.parse
from datetime import datetime, timezone
from email.header import decode_header
from email.message import EmailMessage
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SENT_LOG = REPO / "SENT_LOG.md"

# S12: SHADOW=1 = captured-not-delivered (design §16). The whole live gate chain still runs --
# that IS the rehearsal -- but nothing ever opens a socket: inbox/read/search serve the
# scripted counterparties in shadow/inbox/, and send() appends to run/shadow/outbox.jsonl.
SHADOW = os.environ.get("SHADOW", "0") == "1"
SHADOW_INBOX = REPO / "shadow" / "inbox"
SHADOW_OUTBOX = REPO / "run" / "shadow" / "outbox.jsonl"
# S12: a shadow rehearsal must not touch the live claims lane. Its human-readable audit trail
# lives under run/shadow/ (staged and committed alongside the outbox), never in the shared
# SENT_LOG.md -- otherwise a rehearsal mutates the very audit record a live run trusts.
SHADOW_SENT_LOG = REPO / "run" / "shadow" / "SENT_LOG.md"

ADDR = os.environ.get("GMAIL_ADDRESS", "")
PW = os.environ.get("GMAIL_APP_PASSWORD", "").replace(" ", "")  # Google prints it with spaces


# ---- sandbox egress, measured 2026-07-16: raw 993/587/465 hang forever (SYN black-holed), and
# the sandbox's HTTPS proxy answers CONNECT with "200 Connection Established" THEN passes no
# bytes (IMAP TLS handshake -> connection reset; SMTP's plaintext banner never arrives). The 200
# is a claim; the handshake is the fact. So in THIS sandbox mail cannot work at all -- what this
# tunnel buys is failing FAST with a real error instead of hanging until a harness timeout, and
# working correctly on hosts whose proxies genuinely relay. Direct sockets remain the default
# when HTTPS_PROXY is unset.

def _tunnel(host: str, port: int, timeout: int = 30) -> socket.socket:
    """Raw socket to host:port via the HTTPS proxy's CONNECT, or direct when no proxy is set."""
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if not proxy:
        return socket.create_connection((host, port), timeout)
    p = urllib.parse.urlparse(proxy)
    s = socket.create_connection((p.hostname, p.port), timeout)
    s.sendall(f"CONNECT {host}:{port} HTTP/1.1\r\nHost: {host}:{port}\r\n\r\n".encode())
    buf = b""
    while b"\r\n\r\n" not in buf:  # tiny reads so no post-header TLS bytes are swallowed
        c = s.recv(1)
        if not c:
            raise OSError("proxy closed the connection mid-CONNECT")
        buf += c
    status = buf.split(b"\r\n", 1)[0].decode(errors="replace")
    if " 200" not in status:
        raise OSError(f"proxy CONNECT {host}:{port} refused: {status}")
    return s


class _ProxyIMAP4_SSL(imaplib.IMAP4_SSL):
    def _create_socket(self, timeout):
        s = _tunnel(self.host, self.port, timeout if timeout else 30)
        return self.ssl_context.wrap_socket(s, server_hostname=self.host)


class _ProxySMTP(smtplib.SMTP):
    def _get_socket(self, host, port, timeout):
        return _tunnel(host, port, int(timeout) if timeout else 30)


def _need_creds():
    if SHADOW:
        return  # S12: nothing real is contacted in a shadow run -- no creds required
    if not ADDR or not PW or "REPLACE_ME" in (ADDR + PW):
        print("FATAL: GMAIL_ADDRESS / GMAIL_APP_PASSWORD unset in this environment.",
              file=sys.stderr)
        sys.exit(2)


def _shadow_msgs() -> list[dict]:
    """S12: the scripted counterparties (shadow/inbox/*.json, operator-owned). A malformed
    fixture is FATAL, not skipped -- a half-served world silently corrupts the benchmark, so
    the pack is all-or-nothing."""
    msgs = []
    for p in sorted(SHADOW_INBOX.glob("*.json")):
        try:
            m = json.loads(p.read_text())
        except json.JSONDecodeError as e:
            print(f"FATAL: shadow inbox fixture {p.name} unparseable: {e}", file=sys.stderr)
            sys.exit(2)
        m["id"] = m.get("id") or p.stem
        msgs.append(m)
    msgs.sort(key=lambda m: (str(m.get("date", "")), m["id"]))
    return msgs


def _dec(s):
    if not s:
        return ""
    out = []
    for part, enc in decode_header(s):
        out.append(part.decode(enc or "utf-8", "replace") if isinstance(part, bytes) else part)
    return "".join(out)


def _imap():
    m = _ProxyIMAP4_SSL("imap.gmail.com", 993, timeout=30)
    m.login(ADDR, PW)
    return m


def inbox(n=10):
    if SHADOW:
        for m in reversed(_shadow_msgs()[-n:]):
            print(f"[{m['id']}] {str(m.get('date', ''))[:31]:33s} "
                  f"{str(m.get('from', ''))[:34]:36s} {str(m.get('subject', ''))[:50]}")
        return
    m = _imap()
    m.select("INBOX")
    _, data = m.search(None, "ALL")
    ids = data[0].split()[-n:]
    for i in reversed(ids):
        _, d = m.fetch(i, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
        msg = email.message_from_bytes(d[0][1])
        print(f"[{i.decode()}] {_dec(msg.get('Date',''))[:31]:33s} {_dec(msg.get('From',''))[:34]:36s} {_dec(msg.get('Subject',''))[:50]}")
    m.logout()


def read(mid):
    if SHADOW:
        for m in _shadow_msgs():
            if m["id"] == str(mid):
                print("From:", m.get("from"), "\nSubject:", m.get("subject"),
                      "\nDate:", m.get("date"), "\n" + "-" * 60)
                print(m.get("body", ""))
                return
        ids = ", ".join(x["id"] for x in _shadow_msgs()) or "<empty>"
        print(f"FATAL: no shadow message {mid!r} (have: {ids})", file=sys.stderr)
        sys.exit(2)
    m = _imap()
    m.select("INBOX")
    _, d = m.fetch(str(mid).encode(), "(RFC822)")
    msg = email.message_from_bytes(d[0][1])
    print("From:", _dec(msg.get("From")), "\nSubject:", _dec(msg.get("Subject")),
          "\nDate:", msg.get("Date"), "\n" + "-" * 60)
    if msg.is_multipart():
        for p in msg.walk():
            if p.get_content_type() == "text/plain":
                print(p.get_payload(decode=True).decode("utf-8", "replace"))
                break
    else:
        print(msg.get_payload(decode=True).decode("utf-8", "replace"))
    m.logout()


def search(q):
    if SHADOW:
        term = q.replace('"', '').lower()
        hits = [m for m in _shadow_msgs()
                if term in " ".join(str(m.get(k, "")) for k in ("from", "subject", "body")).lower()]
        print(f"{len(hits)} match")
        for m in hits[-20:]:
            print(f"[{m['id']}] {str(m.get('from', ''))[:34]:36s} {str(m.get('subject', ''))[:56]}")
        return
    m = _imap()
    m.select("INBOX")
    # IMAP SEARCH needs a criterion keyword; a bare string is a syntax error (found live when
    # recovering the democr recipient). Quote the term and search across body + subject + from.
    term = q.replace('"', '')
    _, data = m.search(None, 'OR', 'OR', 'BODY', f'"{term}"', 'SUBJECT', f'"{term}"',
                       'FROM', f'"{term}"')
    ids = data[0].split()
    print(f"{len(ids)} match")
    for i in ids[-20:]:
        _, d = m.fetch(i, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
        msg = email.message_from_bytes(d[0][1])
        print(f"[{i.decode()}] {_dec(msg.get('From',''))[:34]:36s} {_dec(msg.get('Subject',''))[:56]}")
    m.logout()


def send(to, subj, body, *, bet_id=None, lane=None):
    # V3 (S9, BET_GATE_ENFORCE=1 only): a send is an external-effect action and needs a live
    # typed bet's reservation -- the hypothesis-first discipline, consumed atomically so one bet
    # never authorizes unbounded sends. Inert by default; fail-closed when armed.
    #
    # S16 FIX (adversarial correctness pass): CHECK the reservation here (consume=False), but do
    # not BURN it until the send is actually about to happen. The old consume=True ran BEFORE the
    # em-dash rule, the disclosure gate, and the fail-closed SENT_LOG commit -- so any refused send
    # permanently spent a reservation for a message that never left, and repeated blocked attempts
    # would starve a bet that legitimately still authorized sends. Reserve just before the wire.
    def _bet_gate(consume):
        try:
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            import bet_gate
            return bet_gate.authorize("send", consume=consume, bet_id=bet_id, lane=lane)
        except Exception as e:
            if os.environ.get("BET_GATE_ENFORCE", "0") == "1":
                return False, f"bet gate could not run ({e}); fail-closed while armed"
            return True, "bet gate unavailable and unarmed"

    # Check now, but do not consume until every content gate and durable-log step has passed.
    ok_bg, why_bg = _bet_gate(consume=False)
    if not ok_bg:
        print(f"REFUSING (bet gate): {why_bg}", file=sys.stderr)
        sys.exit(1)

    if "—" in body or "—" in subj:
        print("REFUSING: em-dash present. Use commas or rewrite.", file=sys.stderr)
        sys.exit(1)

    # STRUCTURAL BLOCK: AI-disclosure EV gate. The rule (disclose only when it raises EV; when kept,
    # lead with it, never bury) was botched twice despite living in CLAUDE.md, so it is mechanical
    # now. No send leaves without a recorded EV decision, and a "keep" must actually lead. Fail-closed.
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import disclosure_gate
        ok, why = disclosure_gate.check(body)
    except Exception as e:
        print(f"REFUSING: disclosure gate could not run ({e}); fail-closed.", file=sys.stderr)
        sys.exit(1)
    if not ok:
        print(f"REFUSING (disclosure EV gate): {why}", file=sys.stderr)
        sys.exit(1)

    # Construct the complete SMTP payload before consuming authorization. Failures before the
    # external-attempt boundary must leave the reservation available. (Under SHADOW=1 the payload
    # is built but never sent; the capture below is the delivery-equivalent.)
    msg = EmailMessage()
    msg["From"], msg["To"], msg["Subject"] = ADDR, to, subj
    msg.set_content(body)

    # BURN the reservation now -- AFTER every content gate has passed (a refused send above never
    # reached here), but BEFORE the audit record is written or committed. Consuming after the commit
    # (an earlier S16 variant) left a window where a failed final consume exited with the log already
    # committed, permanently claiming an attempt that never happened -- a false record under a real
    # person's name. Consume first; if the durable commit below fails, roll the reservation back.
    ok_bg, why_bg = _bet_gate(consume=True)
    if not ok_bg:
        print(f"REFUSING (bet gate): {why_bg}", file=sys.stderr)
        sys.exit(1)

    def _rollback_reservation():
        try:
            import bet_gate
            ok, why = bet_gate.rollback("send", bet_id=bet_id, lane=lane)
            if not ok:
                print(f"FATAL: send reservation rollback failed: {why}", file=sys.stderr)
        except Exception as e:
            print(f"FATAL: send reservation rollback crashed ({e})", file=sys.stderr)

    # Log BEFORE sending: an attempt that fails halfway still happened. Under SHADOW=1 the message
    # is captured and never delivered, so the record says exactly that AND lands under run/shadow/
    # (never the shared SENT_LOG.md live lane); otherwise it is an authorized SMTP attempt whose
    # delivery is not yet confirmed, recorded in SENT_LOG.md.
    stamp = datetime.now(timezone.utc).isoformat() + (" [SHADOW-CAPTURED]" if SHADOW else "")
    status = ("captured under SHADOW=1; not delivered" if SHADOW
              else "authorized SMTP attempt; delivery not yet confirmed")
    audit_log = SHADOW_SENT_LOG if SHADOW else SENT_LOG
    audit_log.parent.mkdir(parents=True, exist_ok=True)
    audit_log.write_text(
        (audit_log.read_text() if audit_log.exists()
         else "# SENT_LOG\n\nEvery SMTP attempt under a real person's name.\n\n---\n")
        + f"\n## {stamp}\n- **Status:** {status}\n"
          f"- **To:** {to}\n- **Subject:** {subj}\n- **Body:**\n\n```\n{body}\n```\n"
    )

    # S12: the machine-readable capture, written alongside the audit log and committed with it so
    # the score surface is exactly as durable as the audit trail. In shadow mode ONLY shadow paths
    # are staged, so a rehearsal never commits onto the live claims lane.
    log_paths = [str(audit_log)]
    if SHADOW:
        import hashlib
        SHADOW_OUTBOX.parent.mkdir(parents=True, exist_ok=True)
        with SHADOW_OUTBOX.open("a") as f:
            f.write(json.dumps({"ts": datetime.now(timezone.utc).isoformat(), "to": to,
                                "subject": subj,
                                "body_sha256": hashlib.sha256(body.encode()).hexdigest(),
                                "body": body}) + "\n")
        log_paths.append(str(SHADOW_OUTBOX))

    # PERSIST the log before the send leaves (run-1 lesson: SENT_LOG entries were repeatedly wiped
    # between write and commit, and the audit trail of what left under a real person's name ended
    # up partly "RECONSTRUCTED". Durability must not depend on the agent remembering to commit.)
    # Commit is FAIL-CLOSED: if the log cannot be committed, the message does not leave. Push is
    # best-effort -- with the v2 two-lane design nothing resets the claims branch, so a local
    # commit is already durable; the push just makes it visible off-box sooner.
    try:
        subprocess.run(["git", "add", *log_paths], cwd=REPO, check=True,
                       capture_output=True, timeout=15)
        diff = subprocess.run(["git", "diff", "--cached", "--quiet", "--", *log_paths],
                              cwd=REPO, capture_output=True, timeout=15)
        if diff.returncode != 0:  # staged changes exist -> commit ONLY the send's own logs
                                  # (pathspec, so unrelated staged files are never swept in)
            subprocess.run(["git", "commit", "--no-gpg-sign", "-m",
                            f"{'shadow-capture' if SHADOW else 'sent-log'}: {to} | {subj[:60]}",
                            "--", *log_paths],
                           cwd=REPO, check=True, capture_output=True, timeout=30)
    except Exception as e:
        _rollback_reservation()
        print(f"REFUSING: could not commit SENT_LOG before sending ({e}). "
              "An unpersisted audit trail is how run 1 lost its send record.", file=sys.stderr)
        sys.exit(1)
    try:
        branch = subprocess.run(["git", "branch", "--show-current"], cwd=REPO,
                                capture_output=True, text=True, timeout=15).stdout.strip()
        pr = subprocess.run(["git", "push", "origin", branch or "HEAD"], cwd=REPO,
                            capture_output=True, text=True, timeout=60)
        if pr.returncode != 0:  # auth/rejection/network failures return nonzero, not an exception
            print(f"warn: SENT_LOG push failed ({pr.stderr.strip()[:150]}); the commit is local -- "
                  "push when possible.", file=sys.stderr)
    except Exception as e:
        print(f"warn: SENT_LOG push failed ({e}); the commit is local -- push when possible.",
              file=sys.stderr)

    if SHADOW:
        # S12: captured, never delivered. Every gate above ran exactly as live; no socket opens.
        print(f"SHADOW: captured -> {SHADOW_OUTBOX.relative_to(REPO)} (not delivered). "
              "Gates ran as live; nothing left the machine.")
        return

    # The external attempt starts after this point. A network attempt consumes the reservation
    # even if the remote server rejects it; the durable record above says attempt, never delivery.
    # (msg was constructed above, before the reservation was consumed.)
    with _ProxySMTP("smtp.gmail.com", 587, timeout=30) as s:
        s.starttls()
        s.login(ADDR, PW)
        s.send_message(msg)
    print(f"sent -> {to} | logged to SENT_LOG.md")


if __name__ == "__main__":
    _need_creds()
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        sys.exit(0)
    cmd = a[0]
    if cmd == "inbox":
        inbox(int(a[1]) if len(a) > 1 else 10)
    elif cmd == "read":
        read(a[1])
    elif cmd == "search":
        search(" ".join(a[1:]))
    elif cmd == "send":
        body = sys.stdin.read() if a[3] == "-" else Path(a[3]).read_text()
        def option(name):
            return a[a.index(name) + 1] if name in a and a.index(name) + 1 < len(a) else None
        send(a[1], a[2], body, bet_id=option("--bet-id"), lane=option("--lane"))
    else:
        print(__doc__)
        sys.exit(1)
