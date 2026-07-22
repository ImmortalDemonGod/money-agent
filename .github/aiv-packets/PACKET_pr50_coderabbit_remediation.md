# AIV Verification Packet (v2.2)

## Identification

| Field | Value |
|-------|-------|
| **Repository** | github.com/ImmortalDemonGod/money-agent |
| **Change ID** | pr50-coderabbit-remediation |
| **Commits** | `d52a400`, `dfe3ff8`, `6c6c0b2`, `408857c`, `d076eab`, `a05b6d3`, `5b821c4`, `3d103b4`, `34146a3`, `a308fe3`, `5f37af2`, `d060b27`, `5303969`, `27bfab2`, `ebcfa10`, `f5d88d6`, `04cc825`, `85f08cb`, `4e3242d`, `8b34caa`, `b811e37`, `8723558`, `201c610`, `c0fcf19`, `3804cba`, `4a1c283`, `e442d64` |
| **Head SHA** | `e442d64` |
| **Base SHA** | `adfd48f` |
| **Created** | 2026-07-22T23:42:36Z |

## Classification

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: [payments, identity_classification, privilege_boundary, audit_logging, conclusion_authorization]
  blast_radius: component
  classification_rationale: "R3/S1: remediation changes verified payment classification, live-rail enablement, signed operator fact publication, supervisor health, and conclusion authorization. Independent natural-person review remains required."
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:42:36Z"
```

## Claims

1. Direct tests call RailContribution.validate for boolean receive and spend amounts in addition to registry-level fail-closed assertions
2. `tests/test_rails_registry.py` was intentionally extended with direct fail-closed cases; no test file was deleted.
3. Queue precedence assertions run with a matching live verifier process and the dead-precedence assertion terminates it deliberately
4. `tests/sim.sh` was intentionally extended with two-lane review regressions; no test file was deleted.
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
27. Existing tests were preserved: the SHA-pinned test diff shows additive registry and simulation coverage with no deleted test file, and the preceding PR-head CI run passed all repository checks

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

### Class A (Execution Evidence)

- `bash tests/sim.sh`: **73 PASS, 0 FAIL, 0 SKIP** on the committed remediation head.
- `bash tests/corpus.sh`: **11 PASS, 0 FAIL**; the historical corpus remained unchanged.
- `python3 -m unittest -q tests/test_rails_registry.py`: **8 PASS**.
- Beacon/reach checks, Python compilation, Bash syntax, shellcheck, and `git diff --check` passed.
- Four aggregate AIV packets validated successfully.

### Class C (Negative Evidence)

- Deleted `run/human_tasks.json`, branch spoofing, direct terminal-state edits, unreadable queue
  signatures, dead-verifier/queue overlap, absent live acceptance, wrong chain, reused settlement
  events, non-canonical operator wallets, boolean money, adapter exceptions, identity/direction
  mismatches, and invalid unmeasured spend all have committed fail-closed assertions.

### Class D (Differential Evidence)

| Surface | Before final review | Remediated head |
|---|---|---|
| Human resolution writes | concurrent read/modify/write could overwrite | verifier-private lock covers read through push |
| Conclusion orphan scan | skipped if task file absent | companion scan runs independently of file existence |
| Supervisor | queue could mask death; unreadable fell through | unreadable escalates; death precedes live queue work |
| Operator identity | lowercase only, prefix mismatch possible | strict lowercase `0x` + 40-hex canonical form |
| Registry money | Python booleans accepted as numbers | booleans rejected for receive and spend |
| Base activation | runbook-only live warning | bound seven-check marker enforced at preflight, baseline, and pull |
| Evidence | truncated/misaligned claims and SHAs | stable IDs, direct coverage, narrowed claims, aligned references |

### Class E (Intent Alignment)

- **Immutable intent:** [CodeRabbit final-head review](https://github.com/ImmortalDemonGod/money-agent/pull/50#pullrequestreview-4759622532).
- **Requirement:** verify every finding against current code, fix every still-valid production and
  evidence issue, retain honest limitations, and revalidate the full issue-closure story.

### Class F (Provenance Evidence)

**Claim 27: Existing historical regression tests were preserved.**

- Base SHA `adfd48f`; remediation commits `d52a400` through `e442d64` are enumerated above and
  each was created with `aiv commit` plus its sidecar.
- `tests/corpus.sh` is unchanged and passed 11/0. SHA-pinned corpus:
  [`tests/corpus.sh` at remediation head](https://github.com/ImmortalDemonGod/money-agent/blob/e442d64/tests/corpus.sh).
- Test changes are explicit rather than denied: registry tests and `tests/sim.sh` were extended;
  no test file was deleted.
- SHA-pinned preservation diff: [test changes from the reviewed base through the remediation head](https://github.com/ImmortalDemonGod/money-agent/compare/adfd48f...e442d64#files_bucket).
- CI provenance: [preceding PR-head CI run](https://github.com/ImmortalDemonGod/money-agent/actions/runs/29965736632) passed before the review remediation; the Class A commands above were rerun locally on `e442d64`, and post-push CI remains a required external check.



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
- Issue #30 remains open for real TaskMarket/Base volume, submission, funding, and the now-enforced
  seven-step live acceptance marker; simulation does not prove those external seams.
- R3/S1 automated evidence does not replace independent natural-person review before merge.

---

## Summary

Change 'pr50-coderabbit-remediation': 27 commit(s) across 24 file(s).
