# AIV Verification Packet (v2.2)

## Identification

| Field | Value |
|-------|-------|
| **Repository** | github.com/ImmortalDemonGod/aiv-protocol |
| **Change ID** | pr50-coderabbit-remediation |
| **Commits** | `d52a400`, `dfe3ff8`, `6c6c0b2`, `408857c`, `d076eab`, `a05b6d3`, `5b821c4`, `3d103b4`, `34146a3`, `a308fe3`, `5f37af2`, `d060b27`, `5303969`, `27bfab2`, `ebcfa10`, `f5d88d6`, `04cc825`, `85f08cb`, `4e3242d`, `8b34caa`, `b811e37`, `8723558`, `201c610`, `c0fcf19`, `3804cba`, `4a1c283`, `e442d64` |
| **Head SHA** | `e442d64` |
| **Base SHA** | `adfd48f` |
| **Created** | 2026-07-22T23:42:36Z |

## Classification

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: component
  classification_rationale: "TODO: Describe why this tier was chosen"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:42:36Z"
```

## Claims

1. Direct tests call RailContribution.validate for boolean receive and spend amounts in addition to registry-level fail-closed assertions
2. No existing tests were modified or deleted during this change.
3. Queue precedence assertions run with a matching live verifier process and the dead-precedence assertion terminates it deliberately
4. No test files other than `tests/sim.sh` were modified or deleted during this change.
5. RailContribution.validate rejects boolean receive and measured-spend amounts while every invalid adapter path returns a zeroed error contribution
6. Operator wallet addresses with or without a 0x prefix normalize to lowercase 20-byte hex and malformed addresses fail closed
7. Orphan scanning has an empty bet list when registry loading fails and never depends on an unrelated file-read helper
8. Concurrent operator resolutions share a verifier-private inter-process lock through read, duplicate check, write, signing, staging, commit, and push
9. Supervisor VERDICT escalates unreadable signed queue state and reports a dead verifier before live human queue work
10. Base scoring and baseline freezing require a verifier-private seven-check marker bound to chain, wallet, marketplace, and settlement event configuration
11. Verifier startup refuses an armed Base rail until the persisted acceptance marker matches current bindings
12. The runbook provides the exact seven-check marker schema bound to current Base settlement configuration
13. The verifier environment template states that BASE_RPC_URL also requires the bound private live-acceptance marker
14. The context-state evidence claims only SHA-pinned contents actually present in its scope inventory
15. Environment evidence uses labeled fences and retains manual-review and claim-specific-test limitations
16. The closure-packet sidecar narrows its claim and preserves stable claim identities and execution limitations
17. The trust-packet sidecar retains a manual-review verdict and stable exact claim identities
18. Registry evidence cites the direct validator test and consistently reports two of two changed symbols covered
19. The trust-map evidence matrix uses stable claim IDs without truncated identities
20. The verifier-preflight evidence matrix uses stable claim IDs without truncated identities
21. The ledger evidence matrix uses stable claim IDs without truncated identities
22. The prompt evidence matrix uses stable claim IDs without truncated identities
23. The setup evidence matrix uses stable claim IDs without truncated identities
24. The simulation sidecar states that tests sim changed and only other test files were preserved
25. The closure packet evidence table matches the referenced sidecar commit headers
26. The trust-boundary packet restores Claim 4 and keeps a truthful explicit test-change Claim 3

---

## Evidence References

| # | Evidence File | Commit SHA | Classes |
|---|---------------|------------|---------|
| 1 | EVIDENCE_TESTS_TEST_RAILS_REGISTRY.md | `d52a400` | A, B, C, E, F |
| 2 | EVIDENCE_TESTS_SIM.SH.md | `dfe3ff8` | A, B, C, E, F |
| 3 | EVIDENCE_BIN_RAILS___INIT__.md | `6c6c0b2` | A, B, C, E, F |
| 4 | EVIDENCE_BIN_PNL.md | `408857c` | A, B, C, E, F |
| 5 | EVIDENCE_BIN_CONCLUSION_GATE.md | `d076eab` | A, B, C, E, F |
| 6 | EVIDENCE_BIN_CONCLUSION_GATE.md | `a05b6d3` | A, B, C, E, F |
| 7 | EVIDENCE_BIN_HUMAN.md | `5b821c4` | A, B, C, E, F |
| 8 | EVIDENCE_BIN_SUPERVISE.SH.md | `3d103b4` | A, B, C, E, F |
| 9 | EVIDENCE_BIN_RAILS_BASE_USDC.md | `34146a3` | A, B, C, E, F |
| 10 | EVIDENCE_BIN_START_VERIFIER.SH.md | `a308fe3` | A, B, C, E, F |
| 11 | EVIDENCE_TESTS_SIM.SH.md | `5f37af2` | A, B, C, E, F |
| 12 | EVIDENCE_TESTS_TEST_RAILS_REGISTRY.md | `d060b27` | A, B, C, E, F |
| 13 | EVIDENCE_SETUP.MD.md | `5303969` | A, B, C, E, F |
| 14 | EVIDENCE_.ENV.EXAMPLE.md | `27bfab2` | A, B, C, E, F |
| 15 | EVIDENCE_.GITHUB_AIV_EVIDENCE_EVIDENCE_.AIV_CHANGE.JSON.MD.md | `ebcfa10` | A, B, C, E, F |
| 16 | EVIDENCE_.GITHUB_AIV_EVIDENCE_EVIDENCE_.ENV.EXAMPLE.MD.md | `f5d88d6` | A, B, C, E, F |
| 17 | EVIDENCE_.GITHUB_AIV_EVIDENCE_EVIDENCE_.GITHUB_AIV_PACKETS_PACKET_PR50_CLOSURE_INTEGRITY.MD.MD.md | `04cc825` | A, B, C, E, F |
| 18 | EVIDENCE_.GITHUB_AIV_EVIDENCE_EVIDENCE_.GITHUB_AIV_PACKETS_PACKET_PR50_TRUST_BOUNDARIES.MD.MD.md | `85f08cb` | A, B, C, E, F |
| 19 | EVIDENCE_.GITHUB_AIV_EVIDENCE_EVIDENCE_BIN_RAILS___INIT__.MD.md | `4e3242d` | A, B, C, E, F |
| 20 | EVIDENCE_.GITHUB_AIV_EVIDENCE_EVIDENCE_BIN_README.MD.MD.md | `8b34caa` | A, B, C, E, F |
| 21 | EVIDENCE_.GITHUB_AIV_EVIDENCE_EVIDENCE_BIN_START_VERIFIER.SH.MD.md | `b811e37` | A, B, C, E, F |
| 22 | EVIDENCE_.GITHUB_AIV_EVIDENCE_EVIDENCE_LEDGER_README.MD.MD.md | `8723558` | A, B, C, E, F |
| 23 | EVIDENCE_.GITHUB_AIV_EVIDENCE_EVIDENCE_PROMPT.MD.MD.md | `201c610` | A, B, C, E, F |
| 24 | EVIDENCE_.GITHUB_AIV_EVIDENCE_EVIDENCE_SETUP.MD.MD.md | `c0fcf19` | A, B, C, E, F |
| 25 | EVIDENCE_.GITHUB_AIV_EVIDENCE_EVIDENCE_TESTS_SIM.SH.MD.md | `3804cba` | A, B, C, E, F |
| 26 | EVIDENCE_.GITHUB_AIV_PACKETS_PACKET_PR50_CLOSURE_INTEGRITY.MD.md | `4a1c283` | A, B, C, E, F |
| 27 | EVIDENCE_.GITHUB_AIV_PACKETS_PACKET_PR50_TRUST_BOUNDARIES.MD.md | `e442d64` | A, B, C, E, F |



### Class B (Referential Evidence)

**Scope Inventory** (from 45 file references across evidence files)

- `tests/test_rails_registry.py#L116-L127`
- `tests/sim.sh#L251-L252`
- `tests/sim.sh#L257-L258`
- `tests/sim.sh#L261-L262`
- `tests/sim.sh#L300-L301`
- `bin/rails/__init__.py#L39-L40`
- `bin/rails/__init__.py#L44-L45`
- `bin/pnl.py#L178-L185`
- `bin/conclusion_gate.py#L222`
- `bin/human.py#L38`
- `bin/human.py#L55`
- `bin/human.py#L162-L200`
- `bin/supervise.sh#L146-L149`
- `bin/rails/base_usdc.py#L46-L79`
- `bin/rails/base_usdc.py#L138`
- `bin/rails/base_usdc.py#L175-L179`
- `bin/start_verifier.sh#L85-L96`
- `SETUP.md#L129`
- `SETUP.md#L237-L254`
- `.env.example#L51`
- `.github/aiv-evidence/EVIDENCE_.AIV_CHANGE.JSON.md#L25`
- `.github/aiv-evidence/EVIDENCE_.AIV_CHANGE.JSON.md#L40`
- `.github/aiv-evidence/EVIDENCE_.AIV_CHANGE.JSON.md#L56-L58`
- `.github/aiv-evidence/EVIDENCE_.ENV.EXAMPLE.md#L71`
- `.github/aiv-evidence/EVIDENCE_.ENV.EXAMPLE.md#L99-L100`
- `.github/aiv-evidence/EVIDENCE_.GITHUB_AIV_PACKETS_PACKET_PR50_CLOSURE_INTEGRITY.MD.md#L25`
- `.github/aiv-evidence/EVIDENCE_.GITHUB_AIV_PACKETS_PACKET_PR50_CLOSURE_INTEGRITY.MD.md#L75`
- `.github/aiv-evidence/EVIDENCE_.GITHUB_AIV_PACKETS_PACKET_PR50_CLOSURE_INTEGRITY.MD.md#L87-L88`
- `.github/aiv-evidence/EVIDENCE_.GITHUB_AIV_PACKETS_PACKET_PR50_CLOSURE_INTEGRITY.MD.md#L103-L104`
- `.github/aiv-evidence/EVIDENCE_.GITHUB_AIV_PACKETS_PACKET_PR50_TRUST_BOUNDARIES.MD.md#L25`
- `.github/aiv-evidence/EVIDENCE_.GITHUB_AIV_PACKETS_PACKET_PR50_TRUST_BOUNDARIES.MD.md#L64-L65`
- `.github/aiv-evidence/EVIDENCE_BIN_RAILS___INIT__.md#L56-L58`
- `.github/aiv-evidence/EVIDENCE_BIN_RAILS___INIT__.md#L60`
- `.github/aiv-evidence/EVIDENCE_BIN_RAILS___INIT__.md#L80`
- `.github/aiv-evidence/EVIDENCE_BIN_RAILS___INIT__.md#L96-L97`
- `.github/aiv-evidence/EVIDENCE_BIN_RAILS___INIT__.md#L105-L106`
- `.github/aiv-evidence/EVIDENCE_BIN_README.MD.md#L86-L87`
- `.github/aiv-evidence/EVIDENCE_BIN_START_VERIFIER.SH.md#L83-L84`
- `.github/aiv-evidence/EVIDENCE_LEDGER_README.MD.md#L85-L86`
- `.github/aiv-evidence/EVIDENCE_PROMPT.MD.md#L83-L84`
- `.github/aiv-evidence/EVIDENCE_SETUP.MD.md#L84-L85`
- `.github/aiv-evidence/EVIDENCE_TESTS_SIM.SH.md#L27`
- `.github/aiv-evidence/EVIDENCE_TESTS_SIM.SH.md#L86-L87`
- `.github/aiv-packets/PACKET_pr50_closure_integrity.md#L62-L64`
- `.github/aiv-packets/PACKET_pr50_trust_boundaries.md#L31-L32`

---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence was collected by `aiv commit` during the change lifecycle.
Packet generated by `aiv close`.

---

## Known Limitations

- Evidence references point to Layer 1 evidence files at specific commit SHAs.
  Use `git show <sha>:.github/aiv-evidence/<file>` to retrieve.

---

## Summary

Change 'pr50-coderabbit-remediation': 27 commit(s) across 24 file(s).
