import assert from "node:assert/strict";
import { assetSql, isAsset, logHit } from "../harness/beacon/worker.js";

const assets = ["/favicon.ico", "/robots.txt", "/apple-touch-icon-180.png", "/app.css", "/font.woff2"];
const pages = ["/", "/privacy", "/go", "/offer.html"];
for (const path of assets) assert.equal(isAsset(path), true, `asset ${path} must be excluded`);
for (const path of pages) assert.equal(isAsset(path), false, `page ${path} must remain measurable`);

const sql = assetSql();
for (const token of ["/favicon.ico", "/robots.txt", "/apple-touch-icon%", "%.css", "%.woff2"])
  assert.ok(sql.includes(token), `stats predicate must retain ${token}`);

let stored = false;
const env = { DB: { prepare: () => { stored = true; return { bind: () => ({ run: async () => {} }) }; } } };
const req = new Request("https://example.test/", { headers: { "user-agent": "Mozilla/5.0", "accept-language": "en" } });
await logHit(env, { waitUntil: () => {} }, req, "/", "");
assert.equal(stored, false, "missing HASH_SALT must not store a hit");

console.log("beacon tests: asset parity and missing-salt fail-closed behavior pass");
