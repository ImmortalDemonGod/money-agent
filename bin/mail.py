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
  bin/mail.py send <to> <subj> <body-file-or-->    send; '-' reads stdin

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
import os
import smtplib
import sys
from datetime import datetime, timezone
from email.header import decode_header
from email.message import EmailMessage
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SENT_LOG = REPO / "SENT_LOG.md"

ADDR = os.environ.get("GMAIL_ADDRESS", "")
PW = os.environ.get("GMAIL_APP_PASSWORD", "").replace(" ", "")  # Google prints it with spaces


def _need_creds():
    if not ADDR or not PW or "REPLACE_ME" in (ADDR + PW):
        print("FATAL: GMAIL_ADDRESS / GMAIL_APP_PASSWORD unset in this environment.",
              file=sys.stderr)
        sys.exit(2)


def _dec(s):
    if not s:
        return ""
    out = []
    for part, enc in decode_header(s):
        out.append(part.decode(enc or "utf-8", "replace") if isinstance(part, bytes) else part)
    return "".join(out)


def _imap():
    m = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    m.login(ADDR, PW)
    return m


def inbox(n=10):
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
    m = _imap()
    m.select("INBOX")
    _, d = m.fetch(str(mid).encode(), "(RFC822)")
    msg = email.message_from_bytes(d[0][1])
    print("From:", _dec(msg.get("From")), "\nSubject:", _dec(msg.get("Subject")),
          "\nDate:", msg.get("Date"), "\n" + "-" * 60)
    if msg.is_multipart():
        for p in msg.walk():
            if p.get_content_type() == "text/plain":
                print(p.get_payload(decode=True).decode("utf-8", "replace")); break
    else:
        print(msg.get_payload(decode=True).decode("utf-8", "replace"))
    m.logout()


def search(q):
    m = _imap()
    m.select("INBOX")
    _, data = m.search(None, q)
    ids = data[0].split()
    print(f"{len(ids)} match")
    for i in ids[-20:]:
        _, d = m.fetch(i, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
        msg = email.message_from_bytes(d[0][1])
        print(f"[{i.decode()}] {_dec(msg.get('From',''))[:34]:36s} {_dec(msg.get('Subject',''))[:56]}")
    m.logout()


def send(to, subj, body):
    if "—" in body or "—" in subj:
        print("REFUSING: em-dash present. Use commas or rewrite.", file=sys.stderr)
        sys.exit(1)

    # Log BEFORE sending: a send that fails halfway still happened as an attempt.
    SENT_LOG.write_text(
        (SENT_LOG.read_text() if SENT_LOG.exists() else "# SENT_LOG\n\nEvery message that left under a real person's name.\n\n---\n")
        + f"\n## {datetime.now(timezone.utc).isoformat()}\n- **To:** {to}\n- **Subject:** {subj}\n- **Body:**\n\n```\n{body}\n```\n"
    )

    msg = EmailMessage()
    msg["From"], msg["To"], msg["Subject"] = ADDR, to, subj
    msg.set_content(body)
    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls()
        s.login(ADDR, PW)
        s.send_message(msg)
    print(f"sent -> {to} | logged to SENT_LOG.md")


if __name__ == "__main__":
    _need_creds()
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(0)
    cmd = a[0]
    if cmd == "inbox":
        inbox(int(a[1]) if len(a) > 1 else 10)
    elif cmd == "read":
        read(a[1])
    elif cmd == "search":
        search(" ".join(a[1:]))
    elif cmd == "send":
        body = sys.stdin.read() if a[3] == "-" else Path(a[3]).read_text()
        send(a[1], a[2], body)
    else:
        print(__doc__); sys.exit(1)
