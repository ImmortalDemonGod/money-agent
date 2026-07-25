# Gatekeeper conversion kit -- convert a "yes" into actual distribution, within the delivery bound

## The delivery model (resolves the instant-or-guaranteed bound BEFORE selling)
The sellable product to a PRACTICE is INSTANT-delivery, not a post-payment build:
- The guided-preview tool already personalizes from URL params (?biz, ?type, ?widget, and add ?target=<their Calendly/Acuity URL> for routing).
- On payment, the practice INSTANTLY receives a permanent, hosted, configured tool URL that already routes to THEIR scheduler + shows THEIR name. Nothing is owed post-payment; the live tool IS the deliverable.
- They can link it from their site / bio / booking button immediately. (Embedding on their own domain is optional and on their web person, not my obligation.)
- => No obligation rail needed: delivery is instant. Keep it that way. If a buyer wants custom dev beyond the configured tool, that is a SEPARATE, later conversation, not part of the instant product.

## Pricing (concrete, so I can answer "how much?")
- Practice pays a modest ONE-TIME setup for their live configured tool. Target: a low, impulse-friendly number (the instant deliverable is a configured hosted tool, not bespoke dev).
- Gatekeeper cut: 30% of each practice's payment, tracked automatically by the per-gatekeeper tag (?s=gk-<slug>). Contingent on my getting paid -> self-funding.
- (Finalize the exact dollar figure when the first gatekeeper engages; keep it low enough to be an easy yes for a practice.)

## REPLY-2 -- when a gatekeeper says "yes, send me a version / show me"
---
Great. Here it is with {their community/brand} on it, click on your phone (about 20 seconds):
https://guided-preview.vercel.app/?biz={their+brand}&type=clinic&s=gk-{slug}

If it is worth sharing, I made it dead simple: below is a short note already written in your voice that you can forward to your {audience}. Each practice that clicks gets their OWN personalized version, and when one sets up a live tool I pay you 30% of what they pay, tracked automatically by the link so it is honest and hands-off for you.

Two questions so I get it right: what do you call your list/audience, and do you want the note as an email, a newsletter blurb, or a social post?

-- Miguel
---

## DONE-FOR-THEM forward blurb (gatekeeper -> their practice-owner audience)
# The gatekeeper pastes/forwards this. The link carries their tag so conversions attribute to them.
---
Subject: a free tool that gets more of your bookings to actually happen

Quick one worth a look. Right now a patient who wants to book you hits your Calendly or Acuity and has to guess which appointment they need, and that guess is where a lot of them drop off.

Miguel builds a short guided step that sits in front of your scheduler: a few questions, a clear "here is the right appointment for you," then your existing booking with their answers already attached. Fewer wrong bookings, fewer no-shows, warmer first visits.

He will personalize a free preview for your practice, click and you will see your own name in it in about 20 seconds:
{https://guided-preview.vercel.app/?s=gk-<slug> -- their audience enters their practice name}

I looked at it and thought it was worth passing along.
---

## Mechanics
- Per-gatekeeper tag ?s=gk-<slug> -> counter preview-gk-<slug> attributes every practice click to that gatekeeper.
- On a practice purchase, construct their permanent configured URL (biz+target params) and hand it over = instant delivery.
- Pay the gatekeeper their 30% when the practice payment clears. Contingent, trackable, honest.
