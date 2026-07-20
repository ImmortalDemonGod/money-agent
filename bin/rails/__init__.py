"""Receive-rail adapters (issue #30 Part 1 -- the P1 fact-source contract, made explicit).

pnl.py's Stripe+Privacy path implicitly defines what makes a payment rail SCOREABLE; a new rail
is legitimate only when it satisfies the same properties, so they are written down here as the
contract every adapter module must implement:

  1. PRIMARY-SOURCE ONLY: the adapter reads the rail's authoritative ledger (an API the verifier
     holds keys for, or a public chain) -- never the agent's self-report.
  2. AGENT-UNWRITABLE INPUTS: credentials / RPC endpoints / baselines live in the verifier's env
     and STATE_DIR, outside the sandbox.
  3. IMMUTABLE RAW PULLS: every pull is returned as (name, payload) for pnl.py to write into
     ledger/raw/ and fold into MANIFEST.sha256 -- same audit trail as Stripe.
  4. IDENTITY-CLASSIFIED: self-payments are excluded via the operator identity file (emails,
     card fingerprints, wallet addresses); received_usd means CUSTOMER revenue on every rail.
  5. FAIL-CLOSED: a failed or incomplete pull returns errors -> verified=false; unknown is never
     zero, and an unverifiable rail never silently contributes.

Adapter interface (duck-typed, stdlib-only):

    pull(state_dir: Path, operator_addresses: set[str]) -> dict with keys
        customer_usd: float    # counted into received_usd
        self_usd: float        # operator's own transfers, excluded + surfaced
        unbound_usd: float     # moved value that FAILED the settlement binding: visible, never counted
        raws: list[tuple[str, object]]   # (pull-name, payload) for ledger/raw/
        errors: list[str]      # non-empty => verified=false

Onboarding a new rail is a reviewed harness change (issue #11's promotion policy applies): a new
module here + its env provisioning + sim fixtures + sod_hook coverage. The agent cannot add one
to itself.
"""
