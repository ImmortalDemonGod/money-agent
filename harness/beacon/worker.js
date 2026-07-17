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

async function logHit(env, ctx, req, path, dest) {
  if (!env.DB) return;
  try {
    const ua = req.headers.get("user-agent") || "";
    const ref = req.headers.get("referer") || "";
    const cf = req.cf || {};
    const ip = req.headers.get("cf-connecting-ip") || "";
    const daySalt = new Date().toISOString().slice(0, 10);
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
<p><small>${CONFIG.analytics_note} Contact: ${CONFIG.contact}.</small></p>
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
