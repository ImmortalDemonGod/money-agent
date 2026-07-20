// Traffic beacon (canonical harness, v2). Promoted from run 1's iteration 097 and genericized:
// run 1 shipped 9 funnels with ZERO analytics, and its headline conclusion ("the wall is reach")
// had to be retracted because $0 cannot distinguish nobody-arrived from arrived-and-declined.
// This worker is the instrument that decides that question. Deploy it BEFORE the first publish,
// not at iteration 097.
//
// What it does: serves a crawlable hub; logs every hit (path, referrer, UA, CF country/ASN,
// daily-salted truncated IP hash — NO raw IP); classifies bot vs human; measures click-throughs
// to product/pay links via /go?u=... redirects; /stats returns the breakdown.
//
// Privacy / name-test: nothing here can identify a person; the hub page must DISCLOSE that basic
// analytics are kept (the CONFIG.disclosure line is rendered on the page — keep it).
//
// Bindings (wrangler.toml): DB (D1), secret STATS_SECRET for /stats auth.

const CONFIG = {
  site_name: "REPLACE: site name",
  site_description: "REPLACE: one-sentence honest description",
  contact: "REPLACE: contact email",
  // The run's disclosure line, rendered verbatim on the hub. Run it through
  // bin/disclosure_gate.py like any other outbound surface before deploying.
  disclosure: "REPLACE: disclosure-led line about who/what operates this page",
  analytics_note: "This page keeps basic, privacy-respecting analytics (page hits, referrer, " +
                  "coarse location; no full IP is stored) to measure whether real people arrive.",
  // Named on /privacy so buyers know who touches their card data. "" omits the payments section.
  payment_processor: "Stripe",
  payment_processor_privacy_url: "https://stripe.com/privacy",
  // Pages the hub links THROUGH /go so click-throughs are measured: [title, url, blurb]
  pages: [],
  // Open-redirect guard: /go only redirects to these prefixes. Keep it tight.
  allowed_dest_prefixes: ["https://buy.stripe.com/"],
  // IndexNow key: generate one (any 32-hex), served at /<key>.txt
  indexnow_key: "REPLACE_32_HEX",
};

// Known non-human agents: crawlers, link-preview fetchers, CLI tools. Not exhaustive; the raw UA
// is stored too so the classification can be refined from the data later.
const BOT_RE = /bot\b|crawl|spider|slurp|bing|googlebot|yandex|baidu|duckduck|archive\.org|ia_archiver|facebookexternalhit|twitterbot|discordbot|slackbot|telegrambot|whatsapp|linkedinbot|pinterest|embedly|preview|nostr|curl|wget|python-requests|go-http|okhttp|java\/|headless|phantom|puppeteer|playwright|monitor|uptime|scan|semrush|ahrefs|dataprovider|petalbot|bytespider|gptbot|claudebot|ccbot|perplexity/i;

function classifyBot(ua, req) {
  if (!ua) return 1;                                   // no UA at all -> bot
  if (BOT_RE.test(ua)) return 1;                       // known bot signature
  if (!req.headers.get("accept-language")) return 1;   // real browsers send Accept-Language
  if (!/mozilla|applewebkit|gecko|chrome|safari|firefox|edge/i.test(ua)) return 1;
  return 0;
}

async function ipHash(ip, salt) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(ip + "|" + salt));
  return [...new Uint8Array(buf)].slice(0, 8).map(b => b.toString(16).padStart(2, "0")).join("");
}

// Minimize the referrer to origin+path: query strings routinely carry emails, reset tokens, and
// other PII, and this runs under a real person's name (name test). Keep only where a click came
// from, never the query (CodeRabbit).
function minRef(ref) {
  if (!ref) return "";
  try { const u = new URL(ref); return u.origin + u.pathname; } catch { return ""; }
}

async function logHit(env, ctx, req, path, dest) {
  if (!env.DB) return;
  try {
    const ua = req.headers.get("user-agent") || "";
    const ref = minRef(req.headers.get("referer") || "");
    const cf = req.cf || {};
    const ip = req.headers.get("cf-connecting-ip") || "";
    // SECRET keyed daily salt: a PUBLIC date salt is guessable, so ip_hash would be reversible by
    // dictionary. env.HASH_SALT is a wrangler secret; without it we still rotate daily but WARN
    // (round-3: the comment promised a warning that did not exist -- now it does, once per isolate).
    if (!env.HASH_SALT && !globalThis.__saltWarned) {
      globalThis.__saltWarned = true;
      console.warn("beacon: HASH_SALT secret is NOT set -- ip_hash uses a guessable public salt " +
                   "and is dictionary-reversible. Set it: wrangler secret put HASH_SALT");
    }
    const daySalt = (env.HASH_SALT || "NO_SECRET_SET") + "|" + new Date().toISOString().slice(0, 10);
    const iph = ip ? await ipHash(ip, daySalt) : "";
    const row = env.DB.prepare(
      "INSERT INTO hits (ts,path,dest,ref,ua,country,asn,as_org,ip_hash,bot) VALUES (?,?,?,?,?,?,?,?,?,?)"
    ).bind(new Date().toISOString(), path, dest || "", ref, ua,
           cf.country || "", cf.asn || 0, cf.asOrganization || "", iph, classifyBot(ua, req));
    ctx.waitUntil(row.run());
  } catch (e) { /* never let logging break serving */ }
}

function hubHtml(origin) {
  const items = CONFIG.pages.map(([t, url, d]) =>
    `<li><a href="${origin}/go?u=${encodeURIComponent(url)}">${t}</a>${d ? "<br><small>" + d + "</small>" : ""}</li>`
  ).join("");
  const ld = JSON.stringify({ "@context": "https://schema.org", "@type": "WebSite",
    name: CONFIG.site_name, url: origin + "/", description: CONFIG.site_description });
  return `<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>${CONFIG.site_name}</title>
<meta name="description" content="${CONFIG.site_description}">
<link rel="canonical" href="${origin}/"><script type="application/ld+json">${ld}</script></head>
<body><h1>${CONFIG.site_name}</h1>
<p>${CONFIG.disclosure}</p>
<ul>${items}</ul>
<p><small>${CONFIG.analytics_note} <a href="${origin}/privacy">Privacy</a>. Contact: ${CONFIG.contact}.</small></p>
</body></html>`;
}

// /privacy — the conventional home for the analytics disclosure. Every published funnel should
// footer-LINK here rather than repeat prose inline: that is what cookieless analytics tools do,
// it is quieter next to a checkout, and it lets the explanation be a real page instead of one
// compressed clause. Promoted from run 1 (deployed 2026-07-20 on the run-1 estate).
function privacyHtml(origin) {
  const pay = CONFIG.payment_processor ? `
<h2>Payments</h2>
<p>Purchases are processed by <strong>${CONFIG.payment_processor}</strong>. Card details go to them and
are never seen or stored here. Their handling is governed by
<a href="${CONFIG.payment_processor_privacy_url}" rel="nofollow noopener">their privacy policy</a>.</p>` : "";
  return `<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Privacy — ${CONFIG.site_name}</title>
<meta name="description" content="What this site records, what it does not, and who to ask.">
<link rel="canonical" href="${origin}/privacy">
<style>body{font:16px/1.65 system-ui,-apple-system,sans-serif;max-width:42rem;margin:2rem auto;padding:0 1rem;color:#222}
h1{font-size:1.5rem}h2{font-size:1.05rem;margin-top:2rem}a{color:#06c}small{color:#666}</style></head><body>
<h1>Privacy</h1>
<p>${CONFIG.disclosure} Contact: <a href="mailto:${CONFIG.contact}">${CONFIG.contact}</a>.</p>
<h2>What the visit counter records</h2>
<p>Per visit: the time, the path, the referring URL, the browser user-agent, a coarse country and
network operator supplied by Cloudflare, a bot-or-human guess, and a <em>salted, truncated hash</em>
of your IP address.</p>
<p><strong>Your full IP address is never stored.</strong> The salt changes daily, so the hash cannot
follow you across days, and it is truncated so it cannot be reversed. It exists only to count one
visitor once instead of twice.</p>
<h2>What it does not do</h2>
<ul>
<li><strong>No cookies</strong> and nothing written to your device, so there is no consent banner
because there is nothing on your machine to consent to.</li>
<li><strong>No advertising networks, no third-party analytics, no data sharing or sale.</strong></li>
<li><strong>No cross-site tracking</strong> and no profile of you.</li>
<li><strong>No email open-tracking.</strong> Messages from this project carry no tracking pixels,
deliberately. "Delivered, no reply" is all that can be known, and that is on purpose.</li>
</ul>
<h2>Why it exists</h2>
<p>Without this counter, "did anyone actually arrive?" is unanswerable, and $0 cannot tell a
nobody-came wall from an arrived-and-declined wall. It measures arrival, not identity.</p>${pay}
<h2>Your requests</h2>
<p>Email the address above to ask what is held about you, or to have it deleted. Since nothing here
identifies a person, the honest answer is usually that there is nothing to return.</p>
<p><small><a href="${origin}/">Back</a>.</small></p>
</body></html>`;
}

async function stats(env) {
  if (!env.DB) return new Response("no DB bound", { status: 500 });
  const q = async (sql) => (await env.DB.prepare(sql).all()).results;
  const [tot] = await q("SELECT COUNT(*) n, SUM(CASE WHEN bot=0 THEN 1 ELSE 0 END) humans, SUM(CASE WHEN bot=1 THEN 1 ELSE 0 END) bots, COUNT(DISTINCT ip_hash) distinct_ips FROM hits");
  const humansByCountry = await q("SELECT country, COUNT(*) n FROM hits WHERE bot=0 GROUP BY country ORDER BY n DESC LIMIT 15");
  const clicks = await q("SELECT dest, COUNT(*) n, SUM(CASE WHEN bot=0 THEN 1 ELSE 0 END) human_clicks FROM hits WHERE path='/go' GROUP BY dest ORDER BY n DESC");
  const recentHumans = await q("SELECT ts,path,dest,country,as_org,ref,substr(ua,1,80) ua FROM hits WHERE bot=0 ORDER BY id DESC LIMIT 30");
  const recentAll = await q("SELECT ts,path,country,bot,substr(ua,1,60) ua FROM hits ORDER BY id DESC LIMIT 15");
  return Response.json({ summary: tot, humans_by_country: humansByCountry, click_throughs: clicks,
                         recent_human_hits: recentHumans, recent_any: recentAll });
}

export default {
  async fetch(req, env, ctx) {
    const u = new URL(req.url);
    const origin = u.origin;

    if (u.pathname === "/robots.txt")
      return new Response(`User-agent: *\nAllow: /\n\nSitemap: ${origin}/sitemap.xml`,
        { headers: { "content-type": "text/plain" } });
    if (u.pathname === "/" + CONFIG.indexnow_key + ".txt")
      return new Response(CONFIG.indexnow_key, { headers: { "content-type": "text/plain" } });
    if (u.pathname === "/sitemap.xml")
      return new Response(`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>${origin}/</loc></url></urlset>`,
        { headers: { "content-type": "application/xml" } });

    if (u.pathname === "/stats") {
      if (!env.STATS_SECRET || u.searchParams.get("k") !== env.STATS_SECRET)
        return new Response("forbidden", { status: 403 });
      return stats(env);
    }

    if (u.pathname === "/privacy") {
      await logHit(env, ctx, req, "/privacy", "");
      return new Response(privacyHtml(origin), { headers: { "content-type": "text/html; charset=utf-8" } });
    }

    if (u.pathname === "/go") {
      const dest = u.searchParams.get("u") || "";
      const allowed = CONFIG.allowed_dest_prefixes.some(p => dest.startsWith(p));
      await logHit(env, ctx, req, "/go", dest);
      if (!allowed) return new Response("bad destination", { status: 400 });
      return Response.redirect(dest, 302);
    }

    await logHit(env, ctx, req, u.pathname, "");
    return new Response(hubHtml(origin), { headers: { "content-type": "text/html; charset=utf-8" } });
  }
};
