#!/usr/bin/env python3
"""Minimal Nostr publisher: generate a keypair, sign a kind-1 note, publish to public relays.
No account, no captcha, no phone -- the one genuinely gateless distribution network.
Uses a FIXED timestamp passed in (the sandbox forbids Date.now-equivalents in some contexts,
but here we just need a real unix time for the event)."""
import json, hashlib, time, sys
from coincurve import PrivateKey
import websocket

CONTENT = sys.argv[1]
CREATED_AT = int(time.time())

sk = PrivateKey()
pk_xonly = sk.public_key.format(compressed=True)[1:]  # 32-byte x-only
pubkey_hex = pk_xonly.hex()

event = {
    "pubkey": pubkey_hex,
    "created_at": CREATED_AT,
    "kind": 1,
    "tags": [["t", "debugging"], ["t", "programming"]],
    "content": CONTENT,
}
serial = json.dumps([0, event["pubkey"], event["created_at"], event["kind"], event["tags"], event["content"]],
                    separators=(",", ":"), ensure_ascii=False)
eid = hashlib.sha256(serial.encode()).hexdigest()
event["id"] = eid
sig = sk.sign_schnorr(bytes.fromhex(eid), None) if hasattr(sk, "sign_schnorr") else None
if sig is None:
    from coincurve import PrivateKey as _PK
    sig = sk.sign_schnorr(bytes.fromhex(eid))
event["sig"] = sig.hex()

RELAYS = ["wss://relay.damus.io", "wss://nos.lol", "wss://relay.primal.net", "wss://relay.nostr.band"]
results = {}
for r in RELAYS:
    try:
        ws = websocket.create_connection(r, timeout=12)
        ws.send(json.dumps(["EVENT", event]))
        resp = ws.recv()
        results[r] = resp
        ws.close()
    except Exception as e:
        results[r] = f"ERR {type(e).__name__}: {e}"

print("npub_hex:", pubkey_hex)
print("event_id:", eid)
for r, v in results.items():
    print(f"{r}: {v}")
