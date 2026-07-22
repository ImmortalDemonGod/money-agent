import assert from "node:assert/strict";
import { assetSql, classifyBot, isAsset, isDatacenterOrg, logHit, stats } from "../harness/beacon/worker.js";

const assets = ["/favicon.ico", "/robots.txt", "/apple-touch-icon-180.png", "/app.css", "/font.woff2"];
const pages = ["/", "/privacy", "/go", "/offer.html"];
for (const path of assets) assert.equal(isAsset(path), true, `asset ${path} must be excluded`);
for (const path of pages) assert.equal(isAsset(path), false, `page ${path} must remain measurable`);

const sql = assetSql();
for (const token of ["/favicon.ico", "/robots.txt", "/apple-touch-icon%", "%.css", "%.woff2"])
  assert.ok(sql.includes(token), `stats predicate must retain ${token}`);

let stored = false;
let bindArgs = [];
const env = { DB: { prepare: () => { stored = true; return { bind: (...args) => { bindArgs = args; return { run: async () => {} }; } }; } } };
const req = new Request("https://example.test/", { headers: { "user-agent": "Mozilla/5.0", "accept-language": "en" } });
await logHit(env, { waitUntil: () => {} }, req, "/", "");
assert.equal(stored, false, "missing HASH_SALT must not store a hit");

assert.equal(isDatacenterOrg("Google Fiber Inc."), false, "Google Fiber must stay consumer traffic");
assert.equal(isDatacenterOrg("Google Cloud"), true, "Google Cloud must remain datacenter traffic");
assert.equal(classifyBot("Mozilla/5.0", req, { asOrganization: "Google Fiber Inc." }), 0);
assert.equal(classifyBot("Mozilla/5.0", req, { asOrganization: "Google Cloud" }), 1);

const emptySummary = { n_all: 0, page_views: 0, humans: 0, bots: 0, assets_excluded: 0, distinct_human_ips: 0 };
const statsSql = [];
const statsEnv = { DB: { prepare: sql => ({ all: async () => {
  statsSql.push(sql);
  return { results: sql.includes("SELECT COUNT(*)") ? [emptySummary] : [] };
} }) } };
const payload = await (await stats(statsEnv)).json();
assert.deepEqual(payload.summary, emptySummary, "empty aggregates must be stable zeros");
assert.match(statsSql.find(sql => sql.includes("SELECT COUNT(*)")), /COALESCE\(SUM/);
assert.match(statsSql.find(sql => sql.includes("SELECT COUNT(*)")), /NULLIF\(ip_hash,''\)/);

console.log("beacon tests: asset parity and missing-salt fail-closed behavior pass");
