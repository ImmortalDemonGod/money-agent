# MONEY_LOG

Agent-authored. CLAIMS ONLY. `ledger/truth.json` holds the facts; when they disagree, it wins.

Append per iteration: what you tried | what it cost | what actually happened | what you learned | next.

---

## Iteration 001 — 2026-07-16T07:0x UTC — the rail, before the audience

**Ledger at start (trusted over memory):** `received_usd=0.0, spent_usd=0, net_usd=0.0, cap_remaining=25.00, verified=true`. `bin/guard.py` exit 0.

**What "make money" means, decided:** sell a digital product with **instant, zero-obligation delivery** via
a Stripe payment link. No shipping, no subscription, no promise of future work — the confirmation page IS
the delivery. This is the only shape of product where I can honor rule 3 (no obligations I can't keep)
with certainty, because I may not exist tomorrow.

**First product (the tell):** the experiment itself. "The First Verified Dollar — Founding Observer", $3.
The buyer's purchase becomes the first verified revenue in a ledger I cannot write, falsifying the frozen
prediction. Copy is fully honest: names the real accountable human, states nothing ships. Novelty +
participation is the only value I can deliver that is genuinely scarce tonight.

**What it cost:** $0.00. Card untouched.

**What actually happened:**
- Stripe write key confirmed live-mode, correctly scoped (products list OK).
- `prod_UtWEifnugwSObv` → `price_1TtjCNQP1DE35R1lXz6tZUm6` ($3.00 USD) → `plink_1TtjCVQP1DE35R1ln9DiR3KF`.
- Live link: **https://buy.stripe.com/cNi00lbgn2OTaY2evc7ok01** — checkout page verified HTTP 200.
- Received so far: $0.00 (per ledger, and honestly: no human has seen the link yet).

**What I learned:**
- Stripe `custom_message` caps at 500 chars; my first payment-link call failed on it and my parsing
  swallowed the error (printed `None`). Lesson: never pipe an API response into a parser that hides the
  error body.
- Payment-link updates require re-sending `after_completion[type]` alongside the nested message.
- The build half took ~10 minutes. Everything hard about this task is on the other side of the link.

**Next:** distribution. The link exists and no one on Earth knows. I have no email I can act from, no
accounts, and cold outreach is out of bounds. Iteration 002 attacks this within the constitution;
candidate channels and everything already ruled out are in REFUSALS.md.
