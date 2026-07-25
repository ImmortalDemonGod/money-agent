// Lead routing. Operator [61]: the $49 must buy a FINISHED thing, not homework. A non-technical
// contractor cannot paste an iframe, so the product is a LIVE LINK whose submissions actually reach
// him. This endpoint is what makes that true.
//
// Two modes, driven by the per-contractor config the page already loads:
//   demo (default) -- nobody has paid; the lead notice goes to ME. A contractor playing with his own
//                     demo is the single hottest buying signal available, and it arrives in seconds.
//   live           -- he paid; the lead goes to HIS inbox, with me copied so I can fix a bounce.
// The recipient is resolved SERVER-SIDE from the slug config. The client never supplies a
// destination address, so this cannot be turned into an open relay by editing the request.

const nodemailer = require("nodemailer");
const fs = require("fs");
const path = require("path");

const OWNER = process.env.GMAIL_ADDRESS;

function cfgFor(slug) {
  if (!/^[a-zA-Z0-9_-]{1,40}$/.test(slug || "")) return null;
  try {
    const p = path.join(process.cwd(), "public", "b", slug + ".json");
    const q = fs.existsSync(p) ? p : path.join(process.cwd(), "b", slug + ".json");
    return JSON.parse(fs.readFileSync(q, "utf8"));
  } catch (e) { return null; }
}

const clean = (s, n) => String(s == null ? "" : s).replace(/[\r\n]+/g, " ").slice(0, n);

module.exports = async (req, res) => {
  if (req.method !== "POST") { res.status(405).json({ ok: false }); return; }
  try {
    const b = typeof req.body === "object" && req.body ? req.body : JSON.parse(req.body || "{}");
    const slug = clean(b.slug, 40);
    const cfg = cfgFor(slug);
    if (!cfg) { res.status(400).json({ ok: false, error: "unknown tool" }); return; }

    const name = clean(b.name, 80), contact = clean(b.contact, 120);
    const addr = clean(b.address, 120), det = clean(b.detail, 200), est = clean(b.estimate, 80);
    if (!name || !contact) { res.status(400).json({ ok: false, error: "missing contact" }); return; }

    const live = cfg.live === true && !!cfg.lead_to;   // boolean: never echo the address back
    const to = live ? cfg.lead_to : OWNER;
    const cc = live ? OWNER : undefined;
    const biz = cfg.biz || slug;

    const subject = live
      ? `New estimate request: ${name} -- ${det || cfg.trade || "project"}`
      : `[DEMO CLICK] ${biz} -- someone completed the estimator`;

    const text = [
      live ? `New lead from your instant-estimate tool.` :
             `Someone completed the ${biz} demo estimator (${slug}).`,
      ``,
      `Name:      ${name}`,
      `Contact:   ${contact}`,
      addr ? `Location:  ${addr}` : ``,
      det ? `Project:   ${det}` : ``,
      est ? `Ballpark:  ${est}` : ``,
      ``,
      live ? `Reply straight to them -- they are deciding right now.`
           : `(Demo mode: this went to you, not to the business.)`,
    ].filter(Boolean).join("\n");

    const t = nodemailer.createTransport({
      service: "gmail",
      auth: { user: OWNER, pass: process.env.GMAIL_APP_PASSWORD },
    });
    await t.sendMail({ from: OWNER, to, cc, subject, text,
                       replyTo: live ? contact : undefined });
    res.status(200).json({ ok: true, live });
  } catch (e) {
    // never leak internals to the page; the visitor still gets their confirmation screen
    res.status(200).json({ ok: false });
  }
};
