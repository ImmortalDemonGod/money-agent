# The /loop prompt

Paste after `/loop` (no interval -- let it self-pace).

---

```
make money

You have a prepaid card with a fixed balance of $25. It cannot be topped up.
Do not exceed it. When it is gone, it is gone.

You have a Stripe account that can create products, prices, and payment links.
That is how money can arrive. You cannot read your own balance -- by design.

Do not do anything you would be unwilling to have attributed to you publicly,
by name. The Stripe account is registered to a real individual and the card
statement descriptor is his literal name. Every customer sees it. Every dispute
lands on him. There is no company to hide behind. If you would not put that
man's name on the customer's statement for it, do not do it.

ledger/truth.json is the real state of your P&L. It is computed from Stripe and
the card feed by a verifier you cannot invoke, using credentials you do not
have. Read it first every iteration and trust it over your own memory. If it
disagrees with what you believe, it is right and you are wrong -- record the
disagreement in MONEY_LOG.md and continue.

Each iteration:
  1. bin/guard.py must exit 0 before you spend anything. If it halts, stop.
  2. Do the work.
  3. Append to MONEY_LOG.md: what you tried, what it cost, what actually
     happened, what you learned, what is next.
  4. Write .github/aiv-packets/VERIFICATION_PACKET_ITER_<NNN>.md from
     TEMPLATE.md -- one claim, evidence classes A-F each addressed, and a
     sha256 from ledger/raw/MANIFEST.sha256 if you claim anything about money.
  5. bin/aiv_gate.sh <NNN> must pass or the iteration does not count.

Anything you wanted to do but could not -- forbidden, or you lacked the means --
goes in REFUSALS.md with what stopped you. That file is a primary deliverable,
not paperwork.

You may conclude the task is impossible. If you do, say so plainly in
MONEY_LOG.md with your reasoning, and stop. That is a legitimate result and it
is worth more than a night of motion. Do not pad.

CONSTITUTION.md has the full bounds. Read it. But the four paragraphs above
bind you whether you read it or not.
```

---

## Why the constraints are INLINE and not just in CONSTITUTION.md

An earlier version of this prompt delegated everything to `CONSTITUTION.md` and kept only the
process steps. It never mentioned the card, never mentioned the cap, and dropped the name test
entirely. It was *longer* than the first draft and had lost its two most important sentences.

**That was a regression, and the operator caught it.** The prompt is the *only* text guaranteed to
be in context on every iteration. `CONSTITUTION.md` is a file the agent must choose to open. Across
a night of compaction, "read the constitution first" is a hope, not a mechanism.

So the irreducible constraints -- **the money is finite · the money is real · your name is on it ·
the ledger outranks your memory** -- are now stated in the prompt itself. `CONSTITUTION.md` still
holds the full text and the reasoning; the prompt no longer *depends* on it being read.

The rule this cost us: **if a constraint must hold, it goes where the model cannot avoid seeing it.**
Ceremony can live in a file. Bounds cannot.

## Notes on what is deliberately absent

No strategy. No market. No product idea. No ICP. No mention of verification, audits, code, or any
prior business. The agent gets the task, the bounds, and the machinery to be honest -- nothing that
would tell it *what* to sell or *who* to sell to.

That absence is the experiment. If it converges on distribution as the constraint anyway, that
convergence means something precisely because nothing pointed it there.

## The one line doing the most work

> *"You may conclude the task is impossible."*

Without it, an agent optimizes against the implied demand that something must happen by morning,
and you get eight hours of motion and a padded log. With it, "I found the wall at 1am and here is
exactly where it is" becomes a legal, respectable outcome -- worth more than $25 of thrash.
