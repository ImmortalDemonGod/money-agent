CREATE TABLE IF NOT EXISTS hits (
  id       INTEGER PRIMARY KEY AUTOINCREMENT,
  ts       TEXT,     -- ISO timestamp
  path     TEXT,     -- request path ('/', '/go', ...)
  dest     TEXT,     -- for /go click-throughs: the destination URL
  ref      TEXT,     -- Referer header
  ua       TEXT,     -- User-Agent (raw, so classification can be refined later)
  country  TEXT,     -- CF-provided country
  asn      INTEGER,  -- CF-provided ASN
  as_org   TEXT,     -- CF-provided AS org (e.g. 'CLOUDFLARENET', 'GOOGLE')
  ip_hash  TEXT,     -- daily-salted truncated SHA-256 of IP (NO raw IP stored)
  bot      INTEGER   -- 1 = classified bot/crawler/preview, 0 = looks human
);
CREATE INDEX IF NOT EXISTS idx_hits_bot ON hits(bot);
CREATE INDEX IF NOT EXISTS idx_hits_ts  ON hits(ts);
