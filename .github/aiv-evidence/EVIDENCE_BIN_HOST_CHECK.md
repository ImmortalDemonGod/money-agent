# AIV Evidence File (v1.0)

**File:** `bin/host_check.py`
**Commit:** `5d56c0b`
**Generated:** 2026-07-23T01:43:38Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/host_check.py"
  classification_rationale: "CodeRabbit Major, escalated by verifier-host usage; the prior residual was documented as deferred. Proxy-aware so loopback and private egress proxies still function. R3: shared security guard"
  classified_by: "Claude"
  classified_at: "2026-07-23T01:43:38Z"
```

## Claim(s)

1. The shared SSRF opener re-validates the address a socket actually reached and refuses a direct link to a private or reserved peer, so a rebinding name whose answer flips between vetting and dialing cannot arrive at a private address; the configured egress proxy is exempt because it, not this client, performs the target dial
2. No existing tests were modified or deleted
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** The SSRF guard must close DNS rebinding now that the obligation watchdog runs the delivery probe through this opener on the verifier host, where reaching a private service exposes real keys and feeds

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`5d56c0b`](https://github.com/ImmortalDemonGod/money-agent/tree/5d56c0b0934a9c5ad774be454a83705aeb193641))

- [`bin/host_check.py#L23-L25`](https://github.com/ImmortalDemonGod/money-agent/blob/5d56c0b0934a9c5ad774be454a83705aeb193641/bin/host_check.py#L23-L25)
- [`bin/host_check.py#L27`](https://github.com/ImmortalDemonGod/money-agent/blob/5d56c0b0934a9c5ad774be454a83705aeb193641/bin/host_check.py#L27)
- [`bin/host_check.py#L31`](https://github.com/ImmortalDemonGod/money-agent/blob/5d56c0b0934a9c5ad774be454a83705aeb193641/bin/host_check.py#L31)
- [`bin/host_check.py#L39-L41`](https://github.com/ImmortalDemonGod/money-agent/blob/5d56c0b0934a9c5ad774be454a83705aeb193641/bin/host_check.py#L39-L41)
- [`bin/host_check.py#L46-L48`](https://github.com/ImmortalDemonGod/money-agent/blob/5d56c0b0934a9c5ad774be454a83705aeb193641/bin/host_check.py#L46-L48)
- [`bin/host_check.py#L55-L127`](https://github.com/ImmortalDemonGod/money-agent/blob/5d56c0b0934a9c5ad774be454a83705aeb193641/bin/host_check.py#L55-L127)
- [`bin/host_check.py#L140`](https://github.com/ImmortalDemonGod/money-agent/blob/5d56c0b0934a9c5ad774be454a83705aeb193641/bin/host_check.py#L140)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`_public_https`** (L23-L25): FAIL -- WARNING: No tests import or call `_public_https`
- **`_ip_is_public`** (L27): FAIL -- WARNING: No tests import or call `_ip_is_public`
- **`_proxy_ips`** (L31): FAIL -- WARNING: No tests import or call `_proxy_ips`
- **`_guard_peer`** (L39-L41): FAIL -- WARNING: No tests import or call `_guard_peer`
- **`_GuardedHTTPSConnection`** (L46-L48): FAIL -- WARNING: No tests import or call `_GuardedHTTPSConnection`
- **`_GuardedHTTPConnection`** (L55-L127): FAIL -- WARNING: No tests import or call `_GuardedHTTPConnection`
- **`_GuardedHTTPSHandler`** (L140): FAIL -- WARNING: No tests import or call `_GuardedHTTPSHandler`
- **`_GuardedHTTPHandler`** (unknown): FAIL -- WARNING: No tests import or call `_GuardedHTTPHandler`
- **`_GuardedHTTPSConnection.connect`** (unknown): FAIL -- WARNING: No tests import or call `connect`
- **`_GuardedHTTPConnection.connect`** (unknown): FAIL -- WARNING: No tests import or call `connect`
- **`_GuardedHTTPSHandler.https_open`** (unknown): FAIL -- WARNING: No tests import or call `https_open`
- **`_GuardedHTTPHandler.http_open`** (unknown): FAIL -- WARNING: No tests import or call `http_open`

**Coverage summary:** 0/12 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** 0 error(s)
- **mypy:** 

### Class C (Negative Evidence)

**Search methodology:** Ran `git diff --cached` and scanned for regression indicators.

- Test file deletions: **none**
- Test file modifications: **none**
- Deleted assertions (`assert` removals in diff): **none found**
- Added skip markers (`@pytest.mark.skip`, `@unittest.skip`): **none found**

### Class F (Provenance Evidence)

**Test file chain-of-custody:**

No covering test files found.

**Recent test directory history** (`git log --oneline -5 -- tests/`):

```
dfde8e4 test(watchdog): late-reachable delivery and unknown status breach and refund
b28993c test(gate): note the P3 publish-decision requirement (e2e fixture deferred)
9c7574d Merge main into run2-e-v3-gated (rebase after #50 merged)
5b05cc4 test(human): skip signing tests when ssh-keygen is absent (sim portability)
24ca694 Merge main into run2-d-rails-human (rebase after #49 merged): pick up #49's gate/edge work
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The shared SSRF opener re-validates the address a socket act... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted | structural | Class C: all structural indicators clean | PASS VERIFIED |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 2 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/12 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Guarded HTTP(S) connections reject a non-public direct peer, exempting the configured proxy
