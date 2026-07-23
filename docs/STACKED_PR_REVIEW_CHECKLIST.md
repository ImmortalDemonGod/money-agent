# Per-PR Merge Checklist (v4) — for stacked PRs

A working checklist for reviewing and merging a stack of dependent PRs (bottom-up),
where CodeRabbit reviews, `aiv commit` evidence, and a `tests/sim.sh` matrix are in play.
Run it top to bottom **for each PR**.

Marker legend — each addition records the PR that *earned* it:
- `⊕`   added from the #49–#51 defect audit (code defect classes)
- `⊕⊕`  added from the #52 audit (process & topology)
- `⊕⊕⊕` added from the #53–#54 audit (limits of self-review; reconciliation hazards)

## Governing principle (read first)

**The checklist is a floor; independent review (CodeRabbit) is the ceiling.** Across #52–#54,
the review layer caught what disciplined self-review missed — input-masking, honesty overclaims,
and a false-audit-record I *introduced* during reconciliation. Corollary: **reconciliation
(conflict resolution) is the single highest-risk operation in the flow**, because it is the one
place you author novel code that neither CI nor either parent has reviewed. Never merge a PR
whose latest HEAD an independent reviewer has not seen.

---

## 1 · Scope & claims intake
- [ ] Read the PR body — record every **issue it claims to close** and every behavioral claim
      ("flags-off is byte-identical", "refund on every breach path").
- [ ] `get` the PR: base branch, `mergeable_state`, additions/deletions/changed_files, commit count.
- [ ] Pull the **linked issues themselves** (not the PR's paraphrase) — acceptance criteria live
      there and the summary drifts.
- [ ] Record every deferral the body makes ("deferred-with-record", "lands in stack N") as a
      promise to verify, not skip.
- [ ] **⊕⊕ Tag integration/lifecycle claims.** Any claim of the form "runs the full X" /
      "end-to-end" / "the whole chain works" / "no forge is possible" is marked for an
      **end-to-end demonstration** in §5 — it is *not* satisfied by unit coverage of the parts.

## 2 · Diff analysis
- [ ] `get_diff` — read it **in full**, not just the hunks CodeRabbit touched.
- [ ] For each changed file: *what behavior changed, and is it covered by a test that fails
      without it?*
- [ ] Flag anything in the diff **not** explained by the stated scope (creep or an unannounced fix).
- [ ] **⊕ Fail-direction audit** — for every touched error path, exception handler,
      unrecognized-input branch, and missing-import/ImportError branch: confirm it fails **closed**
      by default. (`delivery_check.py`, `iter.py` in #49.)
- [ ] **⊕⊕ Independent-input check.** When several inputs guard one gate, verify each is checked
      *independently* — an `or` fallback or string concatenation lets one benign value (placeholder,
      test key) mask a live one. (#52 guard.py: `WRITE_KEY or READ_KEY`, `PRIVACY_READ_KEY + CARD_NUM`.)
- [ ] **⊕⊕⊕ Read the auto-merged hunks too.** After a multi-file rebase, "sim passed" is not
      "I read them." §2 applies to the *whole resolved diff* — the files git auto-merged are
      unreviewed diff until you read them. (#54: I trusted C2/SoD/F4/F6 because sim passed.)

## 3 · Closure & Coherence Audit
- [ ] For **each issue the PR claims to close**: does the diff actually satisfy its acceptance
      criteria? (Caught the inert `decision_gate` on #51 — "enforcement" wired to nothing.)
- [ ] **Cross-file coherence** — does a bound in one file contradict another? (The
      PROMPT-forbids / CLAUDE-authorizes obligation gap on #51; PROMPT.md still asserting the
      convergence claim #10 retired, on #53.)
- [ ] **Claim-vs-code** — verify load-bearing claims against the code directly, not against the
      evidence packet. ("mechanically guaranteed refund" → confirm `charge_id` is mandatory at
      registration.)
- [ ] Any issue the PR does **not** fully close stays **open** — the merge must not auto-close it.
      (#30 after #50.)
- [ ] **⊕ Deferred-promise check** — if an earlier merged PR promised a fix "lands in stack N,"
      and this *is* stack N, verify it actually landed here. (#51's F2/F8/F9 → verified in #54.)
- [ ] **⊕⊕ Stacked-reversion check.** If the PR under this one merged during review, after
      rebasing onto the new base verify every file belonging to the already-merged layer is
      **byte-identical to base** (no merged fix reverted) and only this PR's own commits remain.
      *(The single most valuable check in this document: on #54 a naive rebase would have reverted
      the #51/#52 fixes across 12 files.)*
- [ ] **⊕⊕ Re-audit after rebase/conflict.** A non-trivial rebase or merge-conflict resolution
      changes the diff — re-run §2/§3/§5 on the **resolved** result; prior verification is stale.
- [ ] **⊕⊕⊕ Reconciliation is NEW code.** When a conflict resolution *chooses between designs*
      (not a mechanical merge), treat the result as new code and run the full §2/§3 audit on it —
      **its failure modes may be in neither parent.** (#54: adopting "consume-at-the-wire" over
      "consume-before-commit" created a false-audit-record window present in neither #51 nor #52.
      CodeRabbit caught it; my re-run of the gates did not.)

## 4 · CodeRabbit findings
- [ ] **⊕⊕ Confirm a review actually ran on the current HEAD.** A non-default base branch makes
      CodeRabbit skip — "no findings" then means "not reviewed," not "clean." Retarget to the
      default branch and trigger a review. (#52/#53/#54 were all skipped until retargeted to `main`.)
- [ ] Read **every** thread, resolved and unresolved — not just top-severity.
- [ ] Triage each: 🔴/🟠 code findings → fix. Evidence/packet/lint bookkeeping → classify as the
      deferred generator-level class **with a stated reason**, never silently.
- [ ] For each finding that *sounds* like bookkeeping, one check: *does it actually describe code
      behavior?* (#51 finding [9] sounded like doc-prose but pointed at the refund-conditionality
      boundary; #54's evidence "no tests modified" was a *false* claim about the diff — fix those.)
- [ ] **⊕⊕ Evidence-nit convergence.** Auto-generated evidence prose is self-regenerating — each
      fix commit is itself reviewable and can spawn a new nit. Fix the specific nits raised
      (especially any that **misstate what the code does**), but the merge bar is *code-clean +
      raised-nits-addressed*, not chasing generated prose to zero.
- [ ] **⊕⊕⊕ "Fixing it would require fabrication" is a valid deferral.** A fix that cannot be done
      without inventing data (URLs, timestamps, counts you do not have) is a legitimate
      deferral — recorded as such, not laziness — especially when fabricating would violate the
      artifact's own honesty rules. (#53 quote-provenance: backfilling per-quote URLs would have
      broken the records' honesty gates.)
- [ ] Nothing waved off without either a fix or a written reason.

## 5 · Fix & verify locally
- [ ] Apply fixes on the PR branch; **⊕⊕ commit via `aiv commit` — mandatory, not optional** (the
      pre-push hook rejects plain commits lacking range evidence; evidence is regenerated per change).
- [ ] **⊕⊕⊕ Keep a change and its test in ONE `aiv commit`.** Splitting a functional change from
      the test that asserts it makes the per-commit evidence true-but-PR-misleading ("no tests
      modified" while the PR modifies tests). (#54's final finding was exactly this.)
- [ ] Run the real gates: `tests/sim.sh` (**clones committed HEAD, not the worktree**), `pytest`,
      `py_compile`/`ruff`, `bash -n` on shell scripts. Record pass counts.
- [ ] **⊕ Bite test** — every new regression test must **fail on pre-fix HEAD** and pass after.
      A test green on both proves nothing and is rejected. (#51 `decision_gate` test deleted for this.)
- [ ] **⊕⊕⊕ Bite-proof methodology.** Because `sim.sh` clones **committed** HEAD, a bite proof
      against pre-fix code is only valid if you **commit the pre-fix downgrade in the clone** *or*
      **run the assertion directly** against the old code. A working-tree checkout (or `git stash`)
      is invisible to the clone and gives a false green. The mutation harness works precisely
      because it *commits* each mutation. (#54: I botched this twice on my own documented trap.)
- [ ] **⊕⊕ End-to-end demonstration.** For each integration/lifecycle claim tagged in §1, run a
      test that exercises the **whole chain** and asserts the claimed outcome — a bite test that
      fails if any link is broken. (#52: test-mode dollar → verified shadow `truth.json` →
      first-dollar stop fires under `SHADOW=1`.)
- [ ] **⊕ Happy-path preservation** — for any guard / egress / auth / network change, run the
      **legitimate path end-to-end**, not only the block case. (DNS-rebinding guard fail-closed
      correctly *and* killed proxied egress; CI green while real outbound was dead.)
- [ ] Environmental failure? Prove it on **pristine pre-change HEAD** before blaming the
      environment — and if it exposes a real portability gap, fix it. (#50 ssh-keygen skip-guard.)
- [ ] **⊕ Side-effect-free verification** — snapshot `git status` and the pushed ref **before and
      after** verification; the only delta is the intended fix. Discard tool-written local state
      (e.g. `.aiv/change.json`). (My `iter.py new` pushed iteration-001 artifacts onto the #49 PR.)

## 6 · CI gate
- [ ] `get_check_runs` on the **actual pushed head SHA** — all checks green (sim matrix,
      byte-compile, shellcheck, gitleaks; `readme` when CONTRIBUTING/README changed). Local green
      is not CI green.

## 7 · Merge decision
- [ ] Confirm `mergeable_state: clean` and base is current (rebased if the PR under it just merged).
- [ ] **⊕⊕ Review current to HEAD.** Confirm CodeRabbit's last review `commit_id == pushed HEAD`
      **and** all threads resolved — a review lagging behind the latest commits is not a clean
      review. Budget for it: each fix push triggers a re-review; wait for it. (#52 was 2 commits
      behind; #54's re-review found a real finding on the fix commit.)
- [ ] **If the PR changes core bounds** (CLAUDE / PROMPT / CONSTITUTION, or the money / delivery /
      first-dollar rails) → **stop and get operator sign-off.** Hard gate. (#51 delivery bound;
      #53 CLAUDE.md governance; #54 guard/obligations/pnl rails.)
- [ ] Otherwise merge with the stack convention (merge commit, bottom-up).
- [ ] After merge: linked issues that were genuinely satisfied close; deferrals carry forward into
      §1 of the next PR; move on.

---

## Version history

- **v2** (#49–51): defect-class detectors — fail-direction, bite-test, happy-path,
  deferred-promise, closure/coherence, side-effect-free verification.
- **v3** (#52): process & topology — integration-claim tagging + end-to-end demonstration,
  independent-input fail-direction, stacked-reversion + re-audit-after-rebase, review-exists +
  evidence-convergence, review-current-to-HEAD at the merge gate.
- **v4** (#53–54): limits of self-review & reconciliation hazards — read the auto-merged hunks
  (§2), reconciliation-is-new-code (§3), fabrication-is-a-valid-deferral (§4), one-aiv-commit-per
  change+test (§5), and the **bite-proof methodology** (§5, the sharpest lesson: sim clones
  committed HEAD, so a pre-fix bite proof must commit the downgrade or run direct). Governing
  principle added: the checklist is a floor, independent review is the ceiling, and reconciliation
  is the highest-risk operation.

### The two highest-value checks, by what they actually caught
1. **§3 stacked-reversion (⊕⊕)** — prevented reverting merged security fixes across 12 files on #54.
2. **§1→§5 integration-claim thread + its v4 bite-proof methodology (⊕⊕/⊕⊕⊕)** — the difference
   between "CI is green" and "I demonstrated the thing the PR promises."
