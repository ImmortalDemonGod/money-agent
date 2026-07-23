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

// Hosting/cloud networks. A "browser" arriving from one of these is a crawler or a link-preview
// fetcher wearing a browser UA, not a person on a laptop. Consumer ISPs (Comcast, AT&T, Telekom,
// Vodafone...) are deliberately NOT here. The raw as_org is still stored, so this can be refined
// without losing data.
const DATACENTER_RE = /google|amazon|aws\b|microsoft|azure|digitalocean|linode|akamai|fastly|hetzner|ovh|vultr|scaleway|contabo|leaseweb|choopa|equinix|oracle|alibaba|tencent|cloudflare|m247|datacamp|hostinger|namecheap|godaddy|blix/i;

// Some brands above ALSO run a consumer ISP on a different ASN (Google Fiber vs Google Cloud, etc.).
// A bare substring match on as_org flags those real humans as bots -- the mirror of the over-counting
// this fixes. Exclude known consumer arms first so DATACENTER_RE only fires on the hosting side.
const CONSUMER_ISP_RE = /\b(google fiber|starlink|t-mobile|at&t|comcast|xfinity|verizon|spectrum|charter|cox communications|centurylink|frontier|telekom|vodafone|orange|telefonica|movistar|virgin media|sky broadband)\b/i;

function isDatacenterOrg(org) {
  if (!org) return false;
  if (CONSUMER_ISP_RE.test(org)) return false;   // consumer traffic, even if the parent brand sells cloud
  return DATACENTER_RE.test(org);
}

// Browsers fetch these automatically alongside a page. Counting them as visits double-counts a
// real visitor and, worse, manufactures a "visit" out of a bare crawler asset fetch.
const ASSET_RE = /^\/(favicon\.ico|apple-touch-icon[^/]*|robots\.txt|sitemap\.xml|.*\.(png|jpe?g|gif|svg|webp|ico|css|js|mjs|map|woff2?|ttf))$/i;

function isAsset(path) { return ASSET_RE.test(path || ""); }

function classifyBot(ua, req, cf) {
  if (!ua) return 1;                                   // no UA at all → bot
  if (BOT_RE.test(ua)) return 1;                       // known bot signature
  if (!req.headers.get("accept-language")) return 1;   // real browsers send Accept-Language; most bots don't
  if (!/mozilla|applewebkit|gecko|chrome|safari|firefox|edge/i.test(ua)) return 1; // no browser engine token
  // Caught live 2026-07-20: two /favicon.ico fetches from Google LLC and a NO hosting network,
  // both wearing full browser UAs with Accept-Language, were being counted as HUMAN.
  if (cf && isDatacenterOrg(cf.asOrganization)) return 1;
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
           cf.country || "", cf.asn || 0, cf.asOrganization || "", iph, classifyBot(ua, req, cf));
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
<p>Full open-source record of the experiment, including the immutable ledger and every refusal: <a href="https://github.com/ImmortalDemonGod/money-agent">github.com/ImmortalDemonGod/money-agent</a>.</p>
<p><small>This page keeps basic, privacy-respecting analytics (page hits, referrer, coarse location; no full IP is stored) to measure whether real people arrive. Ask miguel.ingram.work@gmail.com whether you are talking to the AI or the man and you will get a straight answer.</small></p>
<script src="${origin}/beacon.js" data-site="hub"></script>
</body></html>`;
}

function privacyHtml(origin) {
  return `<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Privacy — the one-honest-dollar experiment</title>
<meta name="description" content="What this site collects, what it does not, and who to ask. No cookies, no full IP, no ad networks.">
<link rel="canonical" href="${origin}/privacy">
<style>body{font:16px/1.65 system-ui,-apple-system,sans-serif;max-width:42rem;margin:2rem auto;padding:0 1rem;color:#222}
h1{font-size:1.5rem}h2{font-size:1.05rem;margin-top:2rem}code{background:#f4f4f4;padding:.1rem .3rem;border-radius:3px}
small{color:#666}a{color:#06c}</style></head><body>
<h1>Privacy</h1>
<p>This site is run by <strong>Miguel Ingram</strong>, a real person, as a public experiment in
which a disclosed AI agent tries to earn one honest dollar. Contact:
<a href="mailto:miguel.ingram.work@gmail.com">miguel.ingram.work@gmail.com</a>. Ask whether you are
talking to the AI or the man and you will get a straight answer.</p>

<h2>What the visit counter records</h2>
<p>Every page here pings a counter I run myself. Per visit it stores: the time, the path, the
referring URL, the browser user-agent string, a coarse country and network operator supplied by
Cloudflare, a bot-or-human guess, and a <em>salted, truncated hash</em> of your IP address.</p>
<p><strong>Your full IP address is never stored.</strong> The hash uses a salt that changes daily, so
it cannot be used to follow you across days, and it is truncated so it cannot be reversed. It exists
only to count one visitor twice instead of once.</p>

<h2>What it does not do</h2>
<ul>
<li><strong>No cookies</strong> and nothing written to your device. There is no consent banner
because there is nothing on your machine to consent to.</li>
<li><strong>No advertising networks, no third-party analytics, no data sharing or sale.</strong></li>
<li><strong>No cross-site tracking</strong> and no profile of you.</li>
<li><strong>No email open-tracking.</strong> Messages from this project contain no tracking pixels,
deliberately. "Delivered, no reply" is all I can know, and that is on purpose.</li>
</ul>

<h2>Why it exists</h2>
<p>The whole question this experiment asks is whether a real person ever actually arrives, or whether
the audience is entirely crawlers. Without this counter that question is unanswerable, and the
honest answer to "did anyone come?" would be "I have no idea." It measures arrival, not identity.</p>

<h2>Payments</h2>
<p>Purchases are processed by <strong>Stripe</strong>. Card details go to Stripe and are never seen or
stored by me; I receive the payment record only. Stripe's handling is governed by
<a href="https://stripe.com/privacy" rel="nofollow noopener">Stripe's privacy policy</a>.</p>

<h2>Your requests</h2>
<p>Email the address above to ask what is held about you, or to have it deleted. Given that nothing
here identifies a person, the usual honest answer is that there is nothing to return.</p>
<p><small>Last updated 2026-07-20. <a href="${origin}/">Back to the experiment</a>.</small></p>
</body></html>`;
}

async function stats(env) {
  if (!env.DB) return new Response("no DB bound", { status: 500 });
  const q = async (sql) => (await env.DB.prepare(sql).all()).results;
  // est_human_sessions uses the industry-standard JS-execution gate: a hit counts as a session
  // only if a real browser ran the hub's beacon <script> and fired /px. Non-JS crawlers never
  // reach it. Then bot=0 drops the ones whose UA/ASN still looks automated. What remains is an
  // ESTIMATE, not a proof -- a headless real browser also runs JS (inflates it), a VPN/cloud-browser
  // human egresses from a datacenter ASN (deflates it). No request-layer signal proves humanity;
  // the only ground truth for "a real human who valued this" is received_usd in ledger/truth.json.
  const [tot] = await q(`SELECT
      COUNT(*) raw_hits_all_paths,
      COALESCE(SUM(CASE WHEN path='/px' THEN 1 ELSE 0 END),0) js_confirmed_hits,
      COALESCE(SUM(CASE WHEN path='/px' AND bot=0 THEN 1 ELSE 0 END),0) est_human_sessions,
      COALESCE(SUM(CASE WHEN path='/px' AND bot=1 THEN 1 ELSE 0 END),0) js_hits_flagged_bot,
      COUNT(DISTINCT CASE WHEN path='/px' AND bot=0 THEN NULLIF(ip_hash,'') END) est_human_ips,
      COALESCE(SUM(CASE WHEN bot=1 THEN 1 ELSE 0 END),0) server_hits_flagged_bot
    FROM hits`);
  // ASN breakdown of the est-human bucket, so a reader can judge the residual themselves:
  // datacenter/proxy ASNs appearing here are exactly what inflate the estimate.
  const estByAsn = await q(`SELECT as_org, country, COUNT(*) n, COUNT(DISTINCT ip_hash) ips
      FROM hits WHERE path='/px' AND bot=0 GROUP BY as_org ORDER BY n DESC LIMIT 20`);
  // Per-site breakdown: dest carries the beacon tag's data-site id. Shows which of the estate's
  // sites the est-human sessions actually reached -- the funnel-level signal run 1 never had.
  const bySite = await q(`SELECT COALESCE(NULLIF(dest,''),'(unattributed)') site, COUNT(*) n, COUNT(DISTINCT ip_hash) ips
      FROM hits WHERE path='/px' AND bot=0 GROUP BY site ORDER BY n DESC LIMIT 20`);
  const clicks = await q("SELECT dest, COUNT(*) n, COALESCE(SUM(CASE WHEN bot=0 THEN 1 ELSE 0 END),0) non_bot_clicks FROM hits WHERE path='/go' GROUP BY dest ORDER BY n DESC");
  const recent = await q("SELECT ts,path,dest,country,as_org,bot,substr(ua,1,60) ua FROM hits ORDER BY id DESC LIMIT 20");
  return Response.json({
    _method: "est_human_sessions = JS-beacon-confirmed (/px) AND not-flagged-bot. An ESTIMATE with a known, irremovable residual: headless real browsers inflate it; VPN/cloud-browser humans deflate it. No request-layer signal proves humanity. The only ground truth for a real valuing human is received_usd (ledger/truth.json), verified out of band -- currently 0.00.",
    summary: tot,
    est_human_sessions_by_asn: estByAsn,
    est_human_sessions_by_site: bySite,
    click_throughs: clicks,
    recent: recent
  });
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

    // Reusable analytics tag. Any site instruments itself with ONE line:
    //   <script src="https://<beacon-host>/beacon.js" data-site="<name>"></script>
    // On load it fires the JS-gated /px ping with its site id + referrer. Served here so a fix to
    // the beacon reaches every site at once -- the standard analytics-tag pattern (GA/Plausible).
    if (u.pathname === "/beacon.js") {
      const px = origin + "/px";
      const js = "(function(){try{" +
        "var s=document.currentScript,id=(s&&s.getAttribute('data-site'))||'';" +
        "var u=" + JSON.stringify(px) + "+'?site='+encodeURIComponent(id)+'&ref='+encodeURIComponent(document.referrer||'');" +
        "if(!(navigator.sendBeacon&&navigator.sendBeacon(u)))fetch(u,{keepalive:true,mode:'no-cors'});" +
        "}catch(e){}})();";
      return new Response(js, { headers: {
        "content-type": "application/javascript; charset=utf-8",
        "cache-control": "public, max-age=300",
        "access-control-allow-origin": "*" } });
    }

    // JS-execution beacon. Fires ONLY when a real browser runs a site's beacon tag (/beacon.js).
    // Crawlers that never execute JS never reach this path -- the standard, cheap bot filter raw
    // request logging lacks. The 'site' query attributes the hit to the page that fired it; these
    // /px rows are the only ones counted as sessions.
    if (u.pathname === "/px") {
      await logHit(env, ctx, req, "/px", u.searchParams.get("site") || "");
      return new Response(null, { status: 204, headers: { "access-control-allow-origin": "*" } });
    }

    if (u.pathname === "/privacy") {
      await logHit(env, ctx, req, "/privacy", "");
      return new Response(privacyHtml(origin), { headers: { "content-type": "text/html; charset=utf-8" } });
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
