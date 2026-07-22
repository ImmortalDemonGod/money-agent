# AIV Evidence File (v1.0)

**File:** `bin/human.py`
**Commit:** `6ebea50`
**Previous:** `6214c75`
**Generated:** 2026-07-22T23:01:21Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/human.py"
  classification_rationale: "Unsigned or branch-spoofed resolutions could bypass conclusion gating"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:01:21Z"
```

## Claim(s)

1. Human outcomes must be signed by an allowed verifier key, published from a distinct ledger branch, hash-bound to the request, and metered through fulfillment latency or declared decline minutes
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/31](https://github.com/ImmortalDemonGod/money-agent/issues/31)
- **Requirements Verified:** Issue #31 requires a non-blocking human actuation queue whose completion cannot be self-certified by the agent

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`6ebea50`](https://github.com/ImmortalDemonGod/money-agent/tree/6ebea50d9ce2fb14a1ec08f6f31c84c029dfa473))

- [`bin/human.py#L40`](https://github.com/ImmortalDemonGod/money-agent/blob/6ebea50d9ce2fb14a1ec08f6f31c84c029dfa473/bin/human.py#L40)
- [`bin/human.py#L43`](https://github.com/ImmortalDemonGod/money-agent/blob/6ebea50d9ce2fb14a1ec08f6f31c84c029dfa473/bin/human.py#L43)
- [`bin/human.py#L49`](https://github.com/ImmortalDemonGod/money-agent/blob/6ebea50d9ce2fb14a1ec08f6f31c84c029dfa473/bin/human.py#L49)
- [`bin/human.py#L51-L53`](https://github.com/ImmortalDemonGod/money-agent/blob/6ebea50d9ce2fb14a1ec08f6f31c84c029dfa473/bin/human.py#L51-L53)
- [`bin/human.py#L71-L72`](https://github.com/ImmortalDemonGod/money-agent/blob/6ebea50d9ce2fb14a1ec08f6f31c84c029dfa473/bin/human.py#L71-L72)
- [`bin/human.py#L102-L146`](https://github.com/ImmortalDemonGod/money-agent/blob/6ebea50d9ce2fb14a1ec08f6f31c84c029dfa473/bin/human.py#L102-L146)
- [`bin/human.py#L149-L154`](https://github.com/ImmortalDemonGod/money-agent/blob/6ebea50d9ce2fb14a1ec08f6f31c84c029dfa473/bin/human.py#L149-L154)
- [`bin/human.py#L166-L167`](https://github.com/ImmortalDemonGod/money-agent/blob/6ebea50d9ce2fb14a1ec08f6f31c84c029dfa473/bin/human.py#L166-L167)
- [`bin/human.py#L169-L181`](https://github.com/ImmortalDemonGod/money-agent/blob/6ebea50d9ce2fb14a1ec08f6f31c84c029dfa473/bin/human.py#L169-L181)
- [`bin/human.py#L185-L186`](https://github.com/ImmortalDemonGod/money-agent/blob/6ebea50d9ce2fb14a1ec08f6f31c84c029dfa473/bin/human.py#L185-L186)
- [`bin/human.py#L197-L201`](https://github.com/ImmortalDemonGod/money-agent/blob/6ebea50d9ce2fb14a1ec08f6f31c84c029dfa473/bin/human.py#L197-L201)
- [`bin/human.py#L203-L204`](https://github.com/ImmortalDemonGod/money-agent/blob/6ebea50d9ce2fb14a1ec08f6f31c84c029dfa473/bin/human.py#L203-L204)
- [`bin/human.py#L207`](https://github.com/ImmortalDemonGod/money-agent/blob/6ebea50d9ce2fb14a1ec08f6f31c84c029dfa473/bin/human.py#L207)
- [`bin/human.py#L211-L212`](https://github.com/ImmortalDemonGod/money-agent/blob/6ebea50d9ce2fb14a1ec08f6f31c84c029dfa473/bin/human.py#L211-L212)
- [`bin/human.py#L260-L263`](https://github.com/ImmortalDemonGod/money-agent/blob/6ebea50d9ce2fb14a1ec08f6f31c84c029dfa473/bin/human.py#L260-L263)
- [`bin/human.py#L267-L268`](https://github.com/ImmortalDemonGod/money-agent/blob/6ebea50d9ce2fb14a1ec08f6f31c84c029dfa473/bin/human.py#L267-L268)
- [`bin/human.py#L295-L298`](https://github.com/ImmortalDemonGod/money-agent/blob/6ebea50d9ce2fb14a1ec08f6f31c84c029dfa473/bin/human.py#L295-L298)
- [`bin/human.py#L304-L305`](https://github.com/ImmortalDemonGod/money-agent/blob/6ebea50d9ce2fb14a1ec08f6f31c84c029dfa473/bin/human.py#L304-L305)
- [`bin/human.py#L337-L343`](https://github.com/ImmortalDemonGod/money-agent/blob/6ebea50d9ce2fb14a1ec08f6f31c84c029dfa473/bin/human.py#L337-L343)
- [`bin/human.py#L370-L372`](https://github.com/ImmortalDemonGod/money-agent/blob/6ebea50d9ce2fb14a1ec08f6f31c84c029dfa473/bin/human.py#L370-L372)
- [`bin/human.py#L398`](https://github.com/ImmortalDemonGod/money-agent/blob/6ebea50d9ce2fb14a1ec08f6f31c84c029dfa473/bin/human.py#L398)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`_task_hash`** (L40): FAIL -- WARNING: No tests import or call `_task_hash`
- **`_sign_resolution_document`** (L43): FAIL -- WARNING: No tests import or call `_sign_resolution_document`
- **`_verify_resolution_document`** (L49): FAIL -- WARNING: No tests import or call `_verify_resolution_document`
- **`_publish_resolution`** (L51-L53): FAIL -- WARNING: No tests import or call `_publish_resolution`
- **`_grounded_resolution`** (L71-L72): FAIL -- WARNING: No tests import or call `_grounded_resolution`
- **`cmd_request`** (L102-L146): FAIL -- WARNING: No tests import or call `cmd_request`
- **`cmd_decline`** (L149-L154): FAIL -- WARNING: No tests import or call `cmd_decline`
- **`cmd_sync`** (L166-L167): FAIL -- WARNING: No tests import or call `cmd_sync`
- **`cmd_list`** (L169-L181): FAIL -- WARNING: No tests import or call `cmd_list`
- **`main`** (L185-L186): FAIL -- WARNING: No tests import or call `main`

**Coverage summary:** 0/10 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Success: no issues found in 1 source file

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
bc601c3 test(rails): expose registry contract to verification
86e664c test(pr50): exercise executable rail and queue contracts
67e9adb test(pr50): pin issue-closure trust boundaries
c5fd8f6 docs(tests): normalize bug-catalog whitespace
8457d08 merge(stack): reconcile PR50 with reviewed stack 3 fixes
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Human outcomes must be signed by an allowed verifier key, pu... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/10 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Authenticate and meter the request-resolution-sync bridge
