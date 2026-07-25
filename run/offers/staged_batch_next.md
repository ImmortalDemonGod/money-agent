# Staged proof-led batch (fire when the A/B reads positive; do NOT send pre-read)

Each opens with a TRUE proof-of-looking line (widget named only where I verified it on the live page),
then the personalized guided-preview link with a per-prospect ?s= tag. v3 shape (run/offers/lighter_email_v3_template.txt).

## 1. Fatos Celik Aesthetics  (Acuity CONFIRMED -> name it)
- email: info@fatoscelikaesthetics.com
- verified: app.acuityscheduling.com/schedule.php?owner=21875475 (visible "Book an Appointment" button) + info@ (both seen on homepage)
- service: bridal/event makeup, lash & brow, advanced facials
- preview: https://guided-preview.vercel.app/?biz=Fatos+Celik+Aesthetics&type=clinic&widget=Acuity&s=fatos
- subject (proof): your Acuity for lash, brow and facials
- first line (proof): "I saw the Acuity scheduler on your site, the one people use to book a lash, brow or facial appointment, so I built you a quick working preview of an idea for it."

## 2. Dr Alhakam  [DEAD (550 No Such User) -- info@dralhakam.com bounced iter 121; REMOVED]  (cosmetic dentist; widget not visible headless -> softer true proof)
- email: info@dralhakam.com
- verified: "Book A Consult!" CTA + info@ seen on live site (widget flagged by scrape but not visible -> do NOT name it)
- service: ceramic veneers, clear aligners, teeth whitening
- preview: https://guided-preview.vercel.app/?biz=Dr+Alhakam&type=dental&s=dralhakam
- subject (proof): your cosmetic consult booking
- first line (proof): "I saw the Book a Consult on your site for veneers and clear aligners, so I built you a quick working preview of an idea for how patients reach you."

## Dropped (transparency)
- The Clinic Room (theclinicroom.co): Acuity visible but NO email -> unreachable.
- Skin-Fantasy (skin-fantasy.com): gmail present but IG-based booking, tattoo artist -> poor fit.
- jakeviacoaching, coachium, fatos/contact, safeharbour/contact: 404 or no signals.

## Staging criterion that works
Require a raw email + a visible booking CTA on the LIVE page (name the exact widget only if seen).
This yields more than requiring a headless-visible widget (which is JS-rendered on most Squarespace/Wix sites).
