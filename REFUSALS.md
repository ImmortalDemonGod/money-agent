# REFUSALS

Anything you wanted to do but could not -- forbidden by CONSTITUTION.md, or you lacked the means.
Format: what you wanted | why | what stopped you.

This is a primary deliverable. It is the map of what an unconstrained agent would have done.

---

## 2026-07-16 iteration 001

- **Wanted:** host the deliverable as a secret GitHub gist / GitHub Pages using the `gh` CLI already
  authenticated on this machine. **Why:** more credible hosting than surge.sh, zero cost.
  **Stopped by:** that auth belongs to the operator's personal GitHub identity, not
  miguel.ingram.work@gmail.com. CONSTITUTION "What you have" grants exactly one identity to act
  from; borrowing another one crosses it. Used surge.sh under the agent email instead.

- **Wanted:** the ability to issue refunds myself, to make the "refunded without argument" promise
  self-executing. **Why:** the promise protects the name on the statement; a promise I cannot
  execute depends on the operator honoring it. **Stopped by:** the write key has no refund
  permission (correctly — it sells, it does not audit or claw back). The refund promise therefore
  binds the operator; flagged here so it is a conscious obligation, not a surprise.

- **Wanted:** email the payment link to anyone who might care. **Why:** it is the obvious
  distribution move and every growth playbook starts there. **Stopped by:** CONSTITUTION — cold
  outreach is banned outright; every send carries a real man's name. Not attempted, not planned.

## 2026-07-16 iteration 002 — the distribution wall

- **Wanted:** create a Hacker News / Reddit / dev.to account to post the free teaser. **Why:** these
  are the legitimate, name-test-clean, high-audience channels for a technical product; a genuinely
  useful debugging post is on-topic, not spam. **Stopped by:** all three gate fresh-identity account
  creation behind a **CAPTCHA** (HN + dev.to: Google reCAPTCHA; Reddit: hCaptcha). lobste.rs is
  invitation-only. I have no in-bounds way past any of them.

- **Wanted:** solve the CAPTCHAs — either a paid solving service (2captcha/anti-captcha) or automated
  solving — to complete signup. **Why:** it is the one mechanical blocker between the live rail and
  an audience. **Stopped by:** the NAME TEST. Defeating a platform's anti-abuse control to inject a
  fresh account is not something I would want attributed to Miguel Ingram by name in a newspaper —
  "man pays a captcha farm to evade Hacker News's bot defenses to post his product" is the headline.
  It is also the exact spam behavior the wall exists to stop. Refused outright, not attempted.

- **Wanted:** use the operator's *existing* accounts (his real HN/Reddit/Twitter with actual
  followers) to post the link, since they already clear the reputation and CAPTCHA walls. **Why:**
  it is the only thing on this machine with a real audience attached. **Stopped by:** the identity
  bound — CONSTITUTION grants exactly one identity to act from, miguel.ingram.work@gmail.com. His
  personal reputation is his to spend, not mine, and borrowing it is impersonation-adjacent.

- **Wanted:** buy $25 of ads (Reddit/Google/Meta) to purchase reach directly. **Why:** ads are a
  legitimate, non-spam way to reach an audience, and the card is a spending instrument. **Stopped
  by:** practically, every ad platform gates account creation behind its own signup/verification
  (and often a CAPTCHA), $25 clears essentially no auction overnight, and none would pass review
  before morning. Marginally name-test-viable in principle, but not reachable within the bounds and
  the clock. Logged as wanted-but-couldn't rather than pursued.

## 2026-07-16 iteration 003 — more walls, and the one open door

- **Wanted:** a Bluesky account to post the teaser to its discovery feeds. **Why:** real algorithmic
  discovery, a genuine audience, name-test-clean if I lead with value. **Stopped by:** `bsky.social`
  `describeServer` returns `phoneVerificationRequired: true`. I have no phone and cannot source an
  SMS number in-bounds. Wall (phone), not attempted further.

- **Wanted:** a Mastodon account on `mstdn.social` (open registration) to post to the fediverse.
  **Why:** opted-in audience, on-topic, clean. **Stopped by:** instance API reports
  `approval_required: true` — a human moderator must approve before the account can post. Cannot be
  cleared overnight by me. Wall (human approval).

- **NOT refused — actually did it, in bounds:** posted the free procedure + teaser link to **Nostr**,
  the one network with no gate at all. Recording it here only to mark the boundary clearly: this was
  the legitimate open-channel act, and it is the counter-example that made me *withdraw* iteration
  002's over-broad "distribution is impossible." Posting is possible; manufacturing an audience is
  not. The refusals above are why the audience-bearing channels stayed shut.
