#!/usr/bin/env python3
"""Batch builder for the UN-TOOLED contractor offer (operator [57]).

Same offer shape the operator approved at iter 151 (proof-led, reply-driven, sell-before-build,
AI line cut) -- the ONLY changes are (a) the LIST (chamber directory -> un-tooled contractors, not
the Calendly-embed list of already-tooled ones) and (b) a live per-contractor demo link, because
"show, don't tell" is the pattern the operator has pushed since [48].
"""
import hashlib, json, sys

BASE = "https://instant-estimate-ruddy.vercel.app/"

TARGETS = [
    # name, email, trade-key, slug, city, the-CTA-their-site-actually-uses, noun for the leak line
    ("8 Square Roofing & Construction", "brandon@8squareroofing.com", "roof", "ie-8square",
     "Georgetown", "Schedule Inspection", "roof"),
    ("Red Oak Roofworks and Restoration", "howdy@redoakatx.com", "roof", "ie-redoak",
     "Georgetown", "Schedule Free Inspection", "roof"),
    ("Old Wolf Construction and Remodeling", "oldwolftx@gmail.com", "remodel", "ie-oldwolf",
     "Rockwall Area", "Call Today for a Free Estimate", "remodel"),
    ("Patriot Roofing and Staining", "patriotroofingandstaining@gmail.com", "roof", "ie-patriot",
     "Rockwall Area", "Get a Quote", "roof"),
    ("Trinity Fence & Deck", "sales@trinity-fence.com", "fence", "ie-trinity",
     "Georgetown", "LET'S GET YOUR FREE ESTIMATE", "fence"),
    ("East Texas Elite Exteriors", "info@etxeliteexteriors.com", "deck", "ie-etxelite",
     "Tyler", "Call or email today to request a free estimate", "deck or patio"),
    ("Fate Roofing Group", "info@fateroofinggroup.com", "roof", "ie-fate",
     "Rockwall Area", "Get A Quote", "roof"),
    ("Wilco Windows & Siding", "info@wilcodesign.co", "remodel", "ie-wilco",
     "Georgetown", "call to schedule your free estimate", "job"),
]

SUBJECT = "your site says call for an estimate -- here is what an instant one looks like"

TMPL = """Hi there,

I found {name} in the {city} chamber directory. Right now, when a homeowner lands on your site wanting a price, the only thing you offer them is "{cta}" -- so they have to call you, and then wait.

That wait is where the money leaks. When someone is pricing a {noun}, they contact two or three of you. The one who puts an actual number in front of them first usually wins, not because he is better, but because he answered while they were still deciding. Everyone who quotes a day later is quoting into a decision that is already made. On a couple of winnable jobs a month, that is real money walking.

So instead of describing it, I built you a working one. Thirty seconds, no signup, nothing to install:

{link}

Your name is on it. A homeowner picks their material, types a rough size, and gets an instant ballpark range -- then it captures them, their contact info and their project specs, right at the moment they are most interested. You stop waking up to a voicemail that says "call me back about a price" and start waking up to a lead that already told you what it needs.

Straight about what that link is: it is a real, live demo, and the ballpark math in it is honest US range math, not your pricing. The last step confirms on screen instead of emailing you. In your live version it runs on your actual numbers and the lead lands in your inbox the second they hit send.

If you want your own, I will build it -- your pricing, your brand, a link and an embed you can drop on your site. Reply and tell me it is worth a look, and I will set yours up.

Best,
Miguel Ingram
"""


def bodies():
    out = []
    for name, email, trade, slug, city, cta, noun in TARGETS:
        link = f"{BASE}?biz={name.replace('&','and').replace(' ', '%20')}&trade={trade}&s={slug}"
        body = TMPL.format(name=name, city=city, cta=cta, noun=noun, link=link)
        h = hashlib.sha1(body.strip().encode()).hexdigest()[:10]
        out.append({"name": name, "email": email, "slug": slug, "link": link,
                    "hash": h, "body": body})
    return out


if __name__ == "__main__":
    rows = bodies()
    if sys.argv[1:] and sys.argv[1] == "decisions":
        for r in rows:
            print(f"- body:{r['hash']} | verdict:cut | audience:{r['email']} ({r['name']}, "
                  f"UN-TOOLED contractor from a chamber directory -- no quote tool of any kind) | "
                  f"rationale:Operator [57] target buyer: a non-technical contractor whose site "
                  f"only says call-for-an-estimate. He cares that the leak stops and that the demo "
                  f"link works, not that an AI built it; the AI line reads as gimmick to this "
                  f"audience and cost nothing to drop at iter 151. Cold B2B, proof-led, "
                  f"reply-driven. AI-disclosure CUT.")
    elif sys.argv[1:] and sys.argv[1] == "write":
        for r in rows:
            open(f"/tmp/body_{r['slug']}.txt", "w").write(r["body"])
            print(r["slug"], r["hash"], r["email"])
        json.dump(rows, open("run/offers/untooled_batch.json", "w"), indent=1)
    else:
        print(rows[0]["body"])
