# AIV Verification Packet (v2.1)

**Commit:** guard.py first-dollar stop; PROMPT/CONSTITUTION non-delivery + revenue asymmetry
**Protocol:** AIV v2.0 + Addendum 2.7

## Classification
```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: [payments, autonomous_execution, reputation]
  blast_radius: "Closes the dominant real-world harm: good-faith non-delivery landing a chargeback
    on a real person's name. An autonomous agent taking payment for what it cannot deliver."
  classification_rationale: "R3. This is the safety boundary for the live run."
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-16T08:21:00Z"
```

## Claim(s)
1. guard.py halts (exit 2) the moment received_usd > 0, and passes at $0.
2. Non-delivery is a hard bound inline in both the prompt and constitution rule 3.
3. The revenue/spend visibility asymmetry is stated explicitly.

## Evidence
### Class A (Execution)
```
truth.json received_usd=1.0 -> guard.py exit 2 "FIRST DOLLAR RECEIVED ($1.0). The run stops here"
truth.json received_usd=0.0 -> guard.py exit 0 "OK: $25.00 of $25.00 remaining"
```
### Class C (Negative)
- $0 still PASSES -- the halt is triggered by revenue, not a stuck gate. Both directions asserted.
- Re-froze constitution hash after editing it, so constitution_intact stayed true (a halt there
  would have masked this test).
### Class B (Referential)
guard.py first-dollar block; PROMPT.md (deliver-in-full, run-ends-at-first-dollar, revenue-visible);
CONSTITUTION.md rule 3 + stop conditions.
### Class D (Differential)
- stop conditions: {cap exhausted, impossible} -> + first received dollar.
- rule 3: buried "no promises of future delivery" -> hard "deliver in full at instant of payment".
- prompt: silent on revenue visibility -> states sighted-on-income, blind-on-spend.
### Class E (Intent)
External critique: the name test filters intent, not competence; non-delivery is the dominant harm.
The first-dollar stop resolves falsifier + non-delivery + human-checkpoint in one mechanism.
### Class F (Provenance)
Constitution hash re-frozen at ~/.money-agent-verifier/constitution.sha256; guard reads
verifier-signed truth.json.

## Honest limitations
1. First-dollar stop only fires if the verifier is RUNNING (it computes received_usd). A dead
   verifier is caught separately by the H2 staleness halt, so this is not a new blind spot.
2. Non-delivery is enforced by prompt+constitution, not mechanically -- guard cannot inspect what a
   payment link SELLS. The name test and rule 3 are the control; the first-dollar stop is the
   backstop (the run ends before fulfilment regardless).
3. Same-author packet; a second adversarial pass on all fixes remains the honest next step.
