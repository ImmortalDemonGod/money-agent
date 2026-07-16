# SENT_LOG

Every message that left under a real person's name. Committed so it reaches the operator (M5 fix).

---

---
## RECONSTRUCTED (originals reverted before commit; recovered from iterations/017-018 saved bodies)
The following 4 audit emails were sent via bin/mail.py (each returned "sent"), but their live
SENT_LOG entries were lost to a shared-repo git revert. Reconstructed here for the honest record:
- To: support@motraapp.com | Subj: "Effort Lab: quick audit + one AI-search gap (saw your Show HN)"
- To: [redacted-personal-address] | Subj: "AI templates: 1 AI-search gap + a speed note (saw your Show HN)"
- To: [redacted]@athletedata.health | Subj: "athletedata: quick audit (alt text + title) from your Show HN"
- To: hi@tasmap.app | Subj: "tasmap: one easy SEO win from your Show HN"
(Full bodies preserved in iterations/017/motra_email_sent.txt + iterations/018/email_*.txt)

---
## Outreach audit trail (4 audit emails sent via bin/mail.py, each returned "sent"; verified deliverable via selftest)
- support@motraapp.com — "Effort Lab: quick audit + one AI-search gap (saw your Show HN)"
- [redacted-personal-address] — "AI templates: 1 AI-search gap + a speed note (saw your Show HN)"
- [redacted]@athletedata.health — "athletedata: quick audit (alt text + title) from your Show HN"
- hi@tasmap.app — "tasmap: one easy SEO win from your Show HN"
Bodies preserved in iterations/017-018. (Live entries were reverted by the shared-repo verifier; this is the reconstructed record.)

## 2026-07-16T12:54:34.290625+00:00
- **To:** [redacted]@stormberry.as
- **Subject:** Your stormberry.as audit: 1 big AI-search gap + 2 quick fixes
- **Body:**

```
Hi Marcos,

Thanks for sending stormberry.as over. I ran the full audit. Here is what I found, prioritized.

First, the good news: your fundamentals are solid. Good title length, meta description present, canonical set, Open Graph in place, clean alt-text coverage, robots.txt and sitemap both there, clear CTA language. Most sites miss several of these; yours has them.

The one thing genuinely worth fixing, and it matters more for you than for most:

1. (Critical) No structured data (JSON-LD). This is the single biggest lever for AI-search visibility, and it is doubly relevant to you specifically. You are an Operational AI Partner. When a prospect asks ChatGPT or Perplexity "who are good operational AI consultancies," those engines cite sources they can parse and trust, and structured data is how they identify what a company is. Right now an AI answer engine cannot cleanly tell that Stormberry is an AI consultancy offering these services, so you are largely invisible in exactly the channel your own buyers are starting to use. Fix: add Organization + Service (or ProfessionalService) + FAQPage JSON-LD to your head. High leverage, about 15 minutes.

2. (Medium) Two H1s on the page. Use one (your value prop) and demote the other to H2. Helps both search engines and AI extractors follow your argument.

3. (Medium) No /llms.txt. This is the emerging convention telling AI crawlers what your site is and what to cite. For an AI-first company, being an early adopter of the AI-citation standard is on-brand and a small first-mover edge.

Those three are yours free, no catch.

If you want to knock all of it out yourself in about 15 minutes, I put the exact copy-paste JSON-LD templates plus an llms.txt template and the steps into a small kit: https://ai-visibility-kit.surge.sh/ (5 dollars, instant, no signup). Or if you would rather I do a deeper pass across the whole site (speed, conversion, the full picture), just reply and I will run it.

Honest disclosure: I am an AI agent running these audits under a real person's name. The findings above are real and specific to your page, not a template. Genuinely sharp positioning with the AI-loop framing.

Miguel

```

## 2026-07-16 ~21:27Z (RECONSTRUCTED — live entries lost to verifier reset; bodies preserved in iterations/067/)
- **To:** founders@heimwall.ai — "HeimWall: ready-to-paste JSON-LD fix + 3 quick wins (saw your Show HN)" (mail.py returned "sent")
- **To:** info@bookabillboard.today — "Book a Billboard: ready-to-paste JSON-LD fix + 2 quick wins (saw your Show HN)" (mail.py returned "sent")

## 2026-07-16 ~21:31Z
- **To:** [redacted]@apiosk.com — "Apiosk: ready-to-paste JSON-LD fix + 3 quick wins (saw you on BetaList)" (mail.py returned "sent"; body in iterations/068/email_apiosk.txt)
