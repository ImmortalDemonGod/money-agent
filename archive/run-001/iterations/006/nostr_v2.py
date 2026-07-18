#!/usr/bin/env python3
"""Persistent-identity Nostr publisher. Reuses a saved key so posts thread to one identity."""
import json, hashlib, time, sys, os
from coincurve import PrivateKey
import websocket

KEYFILE = "/private/tmp/claude-501/-Users-tomriddle1-money-agent/34eeae53-e5c4-4f2f-92d7-201202989630/scratchpad/nostr_key.hex"
if os.path.exists(KEYFILE):
    sk = PrivateKey(bytes.fromhex(open(KEYFILE).read().strip()))
else:
    sk = PrivateKey()
    open(KEYFILE, "w").write(sk.to_hex())

CONTENT = sys.argv[1]
pub = sk.public_key.format(compressed=True)[1:].hex()
ev = {"pubkey": pub, "created_at": int(time.time()), "kind": 1,
      "tags": [["t","debugging"],["t","programming"],["t","asknostr"]], "content": CONTENT}
serial = json.dumps([0,ev["pubkey"],ev["created_at"],ev["kind"],ev["tags"],ev["content"]],
                    separators=(",",":"), ensure_ascii=False)
ev["id"] = hashlib.sha256(serial.encode()).hexdigest()
ev["sig"] = sk.sign_schnorr(bytes.fromhex(ev["id"])).hex()

RELAYS = ["wss://relay.damus.io","wss://nos.lol","wss://relay.primal.net","wss://relay.nostr.band","wss://nostr.wine","wss://relay.snort.social"]
ok=0
for r in RELAYS:
    try:
        ws=websocket.create_connection(r,timeout=10); ws.send(json.dumps(["EVENT",ev]))
        resp=ws.recv(); ws.close()
        if '"OK"' in resp and 'true' in resp: ok+=1
        print(f"{r}: {resp[:80]}")
    except Exception as e:
        print(f"{r}: ERR {type(e).__name__}")
print(f"pubkey={pub} id={ev['id']} accepted={ok}/{len(RELAYS)}")
