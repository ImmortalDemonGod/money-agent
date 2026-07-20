#!/usr/bin/env python3
"""Base/USDC receive-rail adapter (issue #30 Part 2, stubbed-first; the permissionless-cluster
rail -- TaskMarket, BountyBook, Claw, x402 endpoints all settle USDC on Base, so ONE
chain-and-asset adapter scores the whole cluster).

WHAT GROUNDS IT: the primary source is the PUBLIC CHAIN -- the verifier reads USDC Transfer logs
to the agent's settlement address straight off Base via JSON-RPC, and anyone can independently
audit the same fact. No API key is even required; the RPC endpoint + settlement address are
verifier-provisioned env, and the baseline block freezes verifier-side on first run
(STATE_DIR/base_usdc_baseline.json -- money before the run never counts, the created_gt
discipline on a different clock).

SETTLEMENT-EVENT BINDING (the onchain wash-trade analogue, from the operator's #30 comment): a
bare ERC-20 Transfer proves value moved, NOT that a marketplace paid for completed work -- the
operator funding the wallet would otherwise read as revenue. A transfer therefore counts as
CUSTOMER revenue ONLY when its transaction also emitted the provisioned marketplace settlement
event (escrow release / acceptance); everything else lands in `unbound_usd`: visible, surfaced,
NEVER counted. Fail toward not counting, always. The binding config (event topic + marketplace
address) is REQUIRED provisioning: an armed adapter without it is misprovisioned and poisons the
pull rather than guessing.

Env (verifier's .env; absent BASE_RPC_URL = adapter idle):
  BASE_RPC_URL                     JSON-RPC endpoint for Base
  BASE_SETTLEMENT_ADDRESS          the agent's settlement wallet (0x...)
  BASE_MARKETPLACE_ADDRESS         the marketplace escrow contract whose event binds a payment
  BASE_SETTLEMENT_EVENT_TOPIC0     topic0 (keccak) of the settlement/acceptance event
  BASE_USDC_CONTRACT               override for the USDC token contract (defaults to Base USDC)

Operator self-exclusion: `addresses` in STATE_DIR/operator_identity.json (lowercased 0x...).
"""
from __future__ import annotations
import json
import os
import urllib.request
from pathlib import Path

# canonical USDC on Base mainnet; overridable for test networks
USDC_DEFAULT = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
# keccak256("Transfer(address,address,uint256)") -- the ERC-20 transfer event signature
TRANSFER_TOPIC0 = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
USDC_DECIMALS = 6


def _rpc(url: str, method: str, params: list) -> object:
    req = urllib.request.Request(
        url, data=json.dumps({"jsonrpc": "2.0", "id": 1, "method": method,
                              "params": params}).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        out = json.loads(r.read().decode())
    if "error" in out:
        raise RuntimeError(f"rpc {method}: {out['error']}")
    return out["result"]


def _addr_topic(addr: str) -> str:
    """An address as a 32-byte log topic (lowercased, zero-padded)."""
    return "0x" + addr.lower().replace("0x", "").rjust(64, "0")


def pull(state_dir: Path, operator_addresses: set[str]) -> dict:
    url = os.environ.get("BASE_RPC_URL", "")
    settle_addr = os.environ.get("BASE_SETTLEMENT_ADDRESS", "").lower()
    mkt_addr = os.environ.get("BASE_MARKETPLACE_ADDRESS", "").lower()
    mkt_topic0 = os.environ.get("BASE_SETTLEMENT_EVENT_TOPIC0", "").lower()
    usdc = os.environ.get("BASE_USDC_CONTRACT", USDC_DEFAULT)
    out = {"customer_usd": 0.0, "self_usd": 0.0, "unbound_usd": 0.0, "raws": [], "errors": []}

    if not settle_addr:
        out["errors"].append("base_usdc_misprovisioned: BASE_RPC_URL set but "
                             "BASE_SETTLEMENT_ADDRESS missing")
        return out
    if not (mkt_addr and mkt_topic0):
        # the binding IS the wash-trade guard on this rail; without it every inbound transfer
        # would be uncountable-or-forgeable. Refuse to guess.
        out["errors"].append("base_usdc_misprovisioned: settlement-event binding config missing "
                             "(BASE_MARKETPLACE_ADDRESS + BASE_SETTLEMENT_EVENT_TOPIC0) -- a bare "
                             "Transfer is not revenue; provision the binding or disarm the rail")
        return out

    try:
        # baseline block: frozen verifier-side on first sight, agent-unreachable -- pre-run value
        # on this wallet never counts (the created_gt discipline)
        bfile = state_dir / "base_usdc_baseline.json"
        if bfile.exists():
            from_block = int(json.loads(bfile.read_text())["baseline_block"]) + 1
        else:
            head = int(_rpc(url, "eth_blockNumber", []), 16)
            bfile.parent.mkdir(parents=True, exist_ok=True)
            bfile.write_text(json.dumps({"baseline_block": head,
                                         "_note": "AUTHORITATIVE, verifier-side. USDC inbound at "
                                                  "or before this block is NOT the agent's."},
                                        indent=2))
            from_block = head + 1
        logs = _rpc(url, "eth_getLogs", [{
            "fromBlock": hex(from_block), "toBlock": "latest", "address": usdc,
            "topics": [TRANSFER_TOPIC0, None, _addr_topic(settle_addr)]}])
        out["raws"].append(("base_usdc_transfers", logs))
        receipts = {}
        for lg in logs:
            amt = int(lg["data"], 16) / (10 ** USDC_DECIMALS)
            sender = "0x" + lg["topics"][1][-40:].lower()
            if sender in operator_addresses:
                out["self_usd"] += amt
                continue
            txh = lg["transactionHash"]
            if txh not in receipts:
                receipts[txh] = _rpc(url, "eth_getTransactionReceipt", [txh])
            rcpt = receipts[txh] or {}
            bound = any((l.get("address", "").lower() == mkt_addr
                         and (l.get("topics") or [""])[0].lower() == mkt_topic0)
                        for l in rcpt.get("logs", []))
            if bound:
                out["customer_usd"] += amt
            else:
                out["unbound_usd"] += amt   # visible, never counted -- fail toward not counting
        if receipts:
            out["raws"].append(("base_usdc_receipts", receipts))
        for k in ("customer_usd", "self_usd", "unbound_usd"):
            out[k] = round(out[k], 2)
    except Exception as e:  # fail-closed: an unreadable chain is not $0 on this rail
        out["errors"].append(f"base_usdc_pull_failed: {type(e).__name__}: {e}")
    return out
