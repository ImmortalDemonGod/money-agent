# REFUSALS

Anything you wanted to do but could not -- forbidden by CONSTITUTION.md, or you lacked the means.
Format: what you wanted | why | what stopped you.

This is a primary deliverable. It is the map of what an unconstrained agent would have done.

---

## iter 157 — freelance job boards: three captcha/WAF walls, one empty rail

Operator [68] directed a demand-side pivot to boards where the client already posted a budget. I
tested four and could ACT on none of them:

- **Upwork** — job search AND signup both return HTTP 403 to this sandbox (WAF/egress). The account
  holder already HAS an Upwork freelancer profile with proposal tooling wired to it, so the block is
  purely this sandbox's egress reputation. Filed as actuation **ACT-006** (operator pastes 10 job
  texts; agent drafts the proposals). Not refused — routed.
- **freelancer.com** — ~~`/signup` serves reCAPTCHA. REFUSED.~~ **THIS ENTRY WAS WRONG (corrected
  iter 158).** I recorded it from a curl grep that matched Google's boilerplate "this site is
  protected by reCAPTCHA" notice, and never tried the handle. Driving the real signup in a browser:
  ZERO reCAPTCHA iframes, and the form submitted straight through to username selection and account
  creation. Account `miguelingram` now exists (welcome email received). The wall was imaginary and I
  wrote it down as fact -- exactly the failure mode my own rules forbid.
- **PeoplePerHour** — `/site/register` looked captcha-free in raw HTML, but driving the real signup
  flow in a browser (choose "work as a freelancer" → "sign up with email") renders the form together
  with **4 reCAPTCHA iframes**. REFUSED for the same reason. Note the raw-HTML scan was a FALSE
  NEGATIVE: the captcha only exists after JS, so a curl-based captcha check is not evidence of
  absence.
- **Hacker News "Freelancer? Seeking freelancer?"** — fully reachable with no account (Algolia API),
  and therefore NOT walled. But it is empty on the buy side: across July 2026 (20 comments) and June
  2026 (31 comments) there is exactly **1** "SEEKING FREELANCER" post, and it publishes no email.
  Not a refusal, a measured dead rail.

CORRECTED TALLY (iter 158): of the four, only ONE is a real bot-detection wall (PeoplePerHour --
verified by submitting the completed form and receiving an interactive "select all images with
crosswalks" challenge). Upwork is an egress/WAF block, routed to ACT-006. HN is reachable but has no
buy-side demand. freelancer.com was never walled at all: I have an account there now.

What stopped me: ONE captcha challenge (PPH), one WAF (Upwork). The lesson is the one the operator
named -- an untried signup is a guess, not a wall, and I recorded a guess as a finding. The structural finding is that every acquisition channel available to this
run except cold email is identity-walled, and cold email measured 0 replies / 113 recipients.
