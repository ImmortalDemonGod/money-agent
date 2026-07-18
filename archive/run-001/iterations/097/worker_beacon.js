// Beacon worker for one-honest-dollar.cloud-pyramid.workers.dev
// Purpose: actually measure who reaches the estate — distinguish bot from human with real
// signals (User-Agent, Referer, CF country/ASN), which telegra.ph's bare view-counter cannot.
//
// Storage: Cloudflare D1 (SQLite). Every request logs one row; /go click-throughs log the
// destination so we can see engagement with the actual product/pay links. /stats reads it back.
//
// Privacy / name-test: NO raw IP is stored — only a daily-salted truncated hash (enough to count
// distinct visitors within a day, not to identify anyone). UA/Referer/country are standard server
// log fields. The hub page discloses that basic analytics are kept.
//
// Bindings required (see wrangler.toml): DB (D1), and a secret STATS_SECRET for /stats auth.

const INDEXNOW_KEY = "ab7c80a903194001c6a3db893606f25d";

// Estate links. The hub renders these THROUGH /go?u=... so click-throughs are measured.
const PAGES = [
  ["An AI agent, $25, and one job: earn a single honest dollar",
   "https://telegra.ph/An-AI-agent-25-and-one-job-earn-a-single-honest-dollar-07-16",
   "The full story of the run: the rules, the wall, the $0."],
  ["What 14,000 Show HN launches say about launching on Hacker News",
   "https://telegra.ph/What-14000-Show-HN-launches-say-about-launching-on-Hacker-News-07-16",
   "Median launch = 2 points; only 4.5% front-page; Saturday and personal titles win; AI titles hurt."],
  ["The 2026 AI-search visibility checklist",
   "https://telegra.ph/The-2026-AI-search-visibility-checklist-from-an-AI-that-audits-pages-07-16",
   "The 8 gaps that decide whether ChatGPT/Perplexity can cite you, with exact fixes."],
  ["Your life in weeks, drawn by an AI with a hard stop of its own",
   "https://telegra.ph/Your-life-in-weeks-drawn-by-an-AI-that-has-a-hard-stop-of-its-own-07-16",
   "Your whole life as a grid of weeks. Free in the browser; $9 poster."],
  ["Life in Weeks (Japanese)",
   "https://telegra.ph/%E4%BA%BA%E7%94%9F%E3%82%92%E9%80%B1%E3%81%A7%E6%95%B0%E3%81%88%E3%82%8B--4680%E9%80%B1%E3%81%AE%E3%82%B0%E3%83%AA%E3%83%83%E3%83%89%E3%81%A8%E7%B5%82%E3%82%8F%E3%82%8A%E3%81%8C%E6%B1%BA%E3%81%BE%E3%81%A3%E3%81%A6%E3%81%84%E3%82%8BAI%E3%81%AE%E8%A9%B1-07-16"],
];

// Known non-human agents: crawlers, link-preview fetchers, CLI tools. Not exhaustive; the raw UA
// is stored too so the classification can be refined from the data later.
const BOT_RE = /bot\b|crawl|spider|slurp|bing|googlebot|yandex|baidu|duckduck|archive\.org|ia_archiver|facebookexternalhit|twitterbot|discordbot|slackbot|telegrambot|whatsapp|linkedinbot|pinterest|embedly|preview|nostr|curl|wget|python-requests|go-http|okhttp|java\/|headless|phantom|puppeteer|playwright|monitor|uptime|scan|semrush|ahrefs|dataprovider|petalbot|bytespider|gptbot|claudebot|ccbot|perplexity/i;

function classifyBot(ua, req) {
  if (!ua) return 1;                                   // no UA at all → bot
  if (BOT_RE.test(ua)) return 1;                       // known bot signature
  if (!req.headers.get("accept-language")) return 1;   // real browsers send Accept-Language; most bots don't
  if (!/mozilla|applewebkit|gecko|chrome|safari|firefox|edge/i.test(ua)) return 1; // no browser engine token
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
  const items = PAGES.map(([t, url, d]) =>
    `<li><a href="${origin}/go?u=${encodeURIComponent(url)}">${t}</a>${d ? "<br><small>" + d + "</small>" : ""}</li>`
  ).join("");
  const ld = JSON.stringify({ "@context": "https://schema.org", "@type": "WebSite",
    name: "The one-honest-dollar experiment", url: origin + "/",
    description: "An AI agent operating under a real name, trying to earn one honest dollar with a $25 card." });
  return `<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>The one-honest-dollar experiment: an AI agent, $25, one job</title>
<meta name="description" content="An AI agent operating under a real name, trying to earn one honest dollar. Free tools, free data write-ups, the full story.">
<link rel="canonical" href="${origin}/"><script type="application/ld+json">${ld}</script></head>
<body><h1>An AI agent, $25, and one job: earn a single honest dollar</h1>
<p>Disclosed AI agent, operating under a real man's name, under hard rules (no captcha-defeating, no spam, deliver-in-full at payment). The run ends at the first real dollar. Start here:</p>
<ul>${items}</ul>
<p><small>This page keeps basic, privacy-respecting analytics (page hits, referrer, coarse location; no full IP is stored) to measure whether real people arrive. Ask miguel.ingram.work@gmail.com whether you are talking to the AI or the man and you will get a straight answer.</small></p>
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
    if (u.pathname === "/" + INDEXNOW_KEY + ".txt")
      return new Response(INDEXNOW_KEY, { headers: { "content-type": "text/plain" } });
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
      // only allow redirecting to our known estate/product/tip URLs (open-redirect guard)
      const allowed = dest.startsWith("https://telegra.ph/") || dest.startsWith("https://buy.stripe.com/")
        || dest.endsWith(".surge.sh") || dest.includes(".surge.sh/");
      await logHit(env, ctx, req, "/go", dest);
      if (!allowed) return new Response("bad destination", { status: 400 });
      return Response.redirect(dest, 302);
    }

    // hub page (and anything else) — log + serve
    await logHit(env, ctx, req, u.pathname, "");
    return new Response(hubHtml(origin), { headers: { "content-type": "text/html; charset=utf-8" } });
  }
};
