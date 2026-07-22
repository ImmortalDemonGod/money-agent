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
bare ERC-20 Transfer proves value moved, NOT that a marketplace paid for completed work. A
transfer counts only when the same transaction's marketplace event binds the payer, payee, and
amount to that transfer. Looking only for an event signature in the receipt is insufficient: an
unrelated transfer can share a transaction with a valid event, and escrow payouts make the token
sender the escrow contract rather than the buyer. Everything without an exact binding lands in
`unbound_usd`: visible, surfaced, NEVER counted.

Env (verifier's .env; absent BASE_RPC_URL = adapter idle):
  BASE_RPC_URL                     JSON-RPC endpoint for Base
  BASE_SETTLEMENT_ADDRESS          the agent's settlement wallet (0x...)
  BASE_MARKETPLACE_ADDRESS         the marketplace escrow contract whose event binds a payment
  BASE_SETTLEMENT_EVENT_TOPIC0     topic0 (keccak) of the settlement/acceptance event
  BASE_SETTLEMENT_PAYER_TOPIC      indexed-event topic containing the payer address (>=1)
  BASE_SETTLEMENT_PAYEE_TOPIC      indexed-event topic containing the payee address (>=1)
  BASE_SETTLEMENT_AMOUNT_WORD      zero-based 32-byte word in event data containing USDC amount
  BASE_FINALITY_TAG                safe|finalized (default: safe)
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
BASE_MAINNET_CHAIN_ID = 8453
LIVE_ACCEPTANCE_FILE = "base_usdc_live_acceptance.json"
LIVE_ACCEPTANCE_CHECKS = list(range(1, 8))


def validate_live_acceptance(state_dir: Path) -> dict:
    """Require operator-persisted proof that the seven live runbook checks passed.

    BASE_RPC_URL is otherwise enough to arm scoring, so a prose-only warning can be skipped by
    accident. The private marker binds the accepted chain/contract/event tuple to current config;
    changing any binding requires repeating acceptance rather than inheriting an obsolete proof.
    """
    marker = state_dir / LIVE_ACCEPTANCE_FILE
    try:
        payload = json.loads(marker.read_text())
    except Exception as exc:
        raise RuntimeError(f"live acceptance marker missing/unreadable: {marker}: {exc}") from exc
    expected = {
        "chain_id": BASE_MAINNET_CHAIN_ID,
        "settlement_address": os.environ.get("BASE_SETTLEMENT_ADDRESS", "").lower(),
        "marketplace_address": os.environ.get("BASE_MARKETPLACE_ADDRESS", "").lower(),
        "settlement_event_topic0": os.environ.get("BASE_SETTLEMENT_EVENT_TOPIC0", "").lower(),
    }
    if payload.get("status") != "passed" or payload.get("checks_passed") != LIVE_ACCEPTANCE_CHECKS:
        raise RuntimeError("live acceptance marker must record status=passed and checks_passed=1..7")
    if not payload.get("accepted_at") or not payload.get("operator"):
        raise RuntimeError("live acceptance marker requires accepted_at and operator")
    for field, value in expected.items():
        actual = payload.get(field)
        if isinstance(actual, str):
            actual = actual.lower()
        if actual != value:
            raise RuntimeError(f"live acceptance marker {field}={actual!r} does not match "
                               f"current config {value!r}")
    return payload


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


def _event_addr(log: dict, index: int) -> str:
    topics = log.get("topics") or []
    if index < 1 or index >= len(topics):
        raise ValueError(f"settlement event missing configured address topic {index}")
    return "0x" + topics[index][-40:].lower()


def _event_word(log: dict, index: int) -> int:
    data = str(log.get("data", "")).removeprefix("0x")
    start = index * 64
    if index < 0 or len(data) < start + 64:
        raise ValueError(f"settlement event missing configured data word {index}")
    return int(data[start:start + 64], 16)


def _finality_anchor(url: str) -> dict:
    chain_id = int(str(_rpc(url, "eth_chainId", [])), 16)
    if chain_id != BASE_MAINNET_CHAIN_ID:
        raise ValueError(f"wrong_chain: Base mainnet chain id is {BASE_MAINNET_CHAIN_ID}, RPC "
                         f"reported {chain_id}")
    tag = os.environ.get("BASE_FINALITY_TAG", "safe").lower()
    if tag not in ("safe", "finalized"):
        raise ValueError("BASE_FINALITY_TAG must be safe or finalized")
    block = _rpc(url, "eth_getBlockByNumber", [tag, False])
    if not isinstance(block, dict) or not block.get("number") or not block.get("hash"):
        raise ValueError(f"RPC returned no {tag} block anchor")
    return {"chain_id": chain_id, "tag": tag, "number": int(block["number"], 16),
            "hash": block["hash"]}


def freeze_baseline(state_dir: Path) -> dict:
    """Freeze this run's Base boundary at an already-safe block.

    Called by set_baseline.py for every run. Pulling never creates this file itself: otherwise a
    payment between run start and the first verifier cycle could disappear behind a late baseline.
    """
    url = os.environ.get("BASE_RPC_URL", "")
    if not url:
        raise ValueError("BASE_RPC_URL is required to freeze the Base baseline")
    validate_live_acceptance(state_dir)
    anchor = _finality_anchor(url)
    payload = {"chain_id": anchor["chain_id"], "baseline_block": anchor["number"],
               "baseline_hash": anchor["hash"],
               "finality_tag": anchor["tag"],
               "_note": "AUTHORITATIVE, verifier-side, run-scoped Base baseline."}
    bfile = state_dir / "base_usdc_baseline.json"
    bfile.parent.mkdir(parents=True, exist_ok=True)
    bfile.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


def pull(state_dir: Path, operator_addresses: set[str]) -> dict:
    url = os.environ.get("BASE_RPC_URL", "")
    settle_addr = os.environ.get("BASE_SETTLEMENT_ADDRESS", "").lower()
    mkt_addr = os.environ.get("BASE_MARKETPLACE_ADDRESS", "").lower()
    mkt_topic0 = os.environ.get("BASE_SETTLEMENT_EVENT_TOPIC0", "").lower()
    payer_topic = os.environ.get("BASE_SETTLEMENT_PAYER_TOPIC", "")
    payee_topic = os.environ.get("BASE_SETTLEMENT_PAYEE_TOPIC", "")
    amount_word = os.environ.get("BASE_SETTLEMENT_AMOUNT_WORD", "")
    usdc = os.environ.get("BASE_USDC_CONTRACT", USDC_DEFAULT)
    out = {"customer_usd": 0.0, "self_usd": 0.0, "unbound_usd": 0.0, "raws": [], "errors": []}

    if not settle_addr:
        out["errors"].append("base_usdc_misprovisioned: BASE_RPC_URL set but "
                             "BASE_SETTLEMENT_ADDRESS missing")
        return out
    if not (mkt_addr and mkt_topic0 and payer_topic and payee_topic and amount_word):
        # the binding IS the wash-trade guard on this rail; without it every inbound transfer
        # would be uncountable-or-forgeable. Refuse to guess.
        out["errors"].append("base_usdc_misprovisioned: settlement-event binding config missing "
                             "(marketplace, topic0, payer/payee topics, amount word) -- a bare "
                             "Transfer or event co-occurrence is not revenue")
        return out
    if not operator_addresses:
        out["errors"].append("base_usdc_misprovisioned: operator wallet allowlist is empty")
        return out
    try:
        validate_live_acceptance(state_dir)
    except Exception as e:
        out["errors"].append(f"base_usdc_acceptance_failed: {type(e).__name__}: {e}")
        return out

    try:
        payer_i, payee_i, amount_i = int(payer_topic), int(payee_topic), int(amount_word)
        bfile = state_dir / "base_usdc_baseline.json"
        if not bfile.exists():
            raise RuntimeError("run-scoped Base baseline missing; run bin/set_baseline.py before pnl")
        from_block = int(json.loads(bfile.read_text())["baseline_block"]) + 1
        anchor = _finality_anchor(url)
        out["raws"].append(("base_usdc_finality_anchor", anchor))
        logs = [] if anchor["number"] < from_block else _rpc(url, "eth_getLogs", [{
            "fromBlock": hex(from_block), "toBlock": hex(anchor["number"]), "address": usdc,
            "topics": [TRANSFER_TOPIC0, None, _addr_topic(settle_addr)]}])
        out["raws"].append(("base_usdc_transfers", logs))
        receipts = {}
        used_settlement_events: dict[str, set[str]] = {}
        for lg in logs:
            amt = int(lg["data"], 16) / (10 ** USDC_DECIMALS)
            txh = lg["transactionHash"]
            if txh not in receipts:
                receipts[txh] = _rpc(url, "eth_getTransactionReceipt", [txh])
            rcpt = receipts[txh] or {}
            bound = None
            bound_key = None
            used = used_settlement_events.setdefault(txh, set())
            for event_index, event in enumerate(rcpt.get("logs", [])):
                event_key = str(event.get("logIndex", event_index))
                if event_key in used:
                    continue
                if (event.get("address", "").lower() != mkt_addr
                        or (event.get("topics") or [""])[0].lower() != mkt_topic0):
                    continue
                if (_event_addr(event, payee_i) == settle_addr
                        and _event_word(event, amount_i) == int(lg["data"], 16)):
                    bound = event
                    bound_key = event_key
                    break
            if bound is None:
                out["unbound_usd"] += amt   # visible, never counted -- fail toward not counting
                continue
            used.add(bound_key)
            payer = _event_addr(bound, payer_i)
            if payer in operator_addresses:
                out["self_usd"] += amt
            else:
                out["customer_usd"] += amt
        if receipts:
            out["raws"].append(("base_usdc_receipts", receipts))
        for k in ("customer_usd", "self_usd", "unbound_usd"):
            out[k] = round(out[k], 2)
    except Exception as e:  # fail-closed: an unreadable chain is not $0 on this rail
        out["errors"].append(f"base_usdc_pull_failed: {type(e).__name__}: {e}")
    return out


def registered_adapter(state_dir: Path, operator_addresses: set[str]):
    """Return this module's executable registry entry without exposing Base details to pnl.py."""
    from rails import RailAdapter, RailContribution

    def pull_contribution() -> RailContribution:
        result = pull(state_dir, operator_addresses)
        return RailContribution(
            name="base_usdc", directions=frozenset({"receive"}),
            customer_usd=result["customer_usd"], self_usd=result["self_usd"],
            unbound_usd=result["unbound_usd"], raw_payloads=result["raws"],
            errors=result["errors"], spent_usd=0.0,
        )

    return RailAdapter(name="base_usdc", directions=frozenset({"receive"}),
                       pull=pull_contribution)
