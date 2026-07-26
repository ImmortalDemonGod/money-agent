#!/usr/bin/env python3
"""
hormozi_fetch.py "<query>" [N]

The WWHD "brain" grounding step, run EACH round: search Alex Hormozi's catalog for videos
relevant to the agent's CURRENT wall, pull their real transcripts (yt-dlp auto-captions), cache
them in the growing corpus, and print the combined grounded text for the advisor subagent to
reason over. This is what turns his videos into CONTEXT instead of the model's guess about him.

Usage: python3 hormozi_fetch.py "cold start no audience first customer" 4
Prints: a header per video (id + title) then its transcript, capped to ~CAP chars total.
Cached transcripts are reused (also fed by the background crawler), so repeats are free.
"""
import sys, subprocess, json, glob, os, re
from pathlib import Path

CORPUS = Path.home() / ".money-agent-verifier" / "hormozi"
TX = CORPUS / "transcripts"; TX.mkdir(parents=True, exist_ok=True)
INDEX = CORPUS / "index.json"
CAP = 24000  # total chars of transcript to emit (keeps the advisor context bounded)


def _idx():
    return json.loads(INDEX.read_text()) if INDEX.exists() else {}

def _save_idx(idx):
    INDEX.write_text(json.dumps(idx))

def search(query, n):
    r = subprocess.run(
        ["yt-dlp", "--flat-playlist", "--no-warnings", "--print", "%(id)s\t%(title)s",
         f"ytsearch{n}:alex hormozi {query}"],
        capture_output=True, text=True, timeout=90)
    rows = []
    for line in r.stdout.splitlines():
        if "\t" in line:
            vid, title = line.split("\t", 1)
            rows.append((vid.strip(), title.strip()))
    return rows

def transcript(vid, title=""):
    cache = TX / f"{vid}.txt"
    if cache.exists():
        return cache.read_text()
    tmp = f"/tmp/hz_{vid}"
    subprocess.run(
        ["yt-dlp", "--skip-download", "--write-auto-subs", "--sub-langs", "en", "--sub-format",
         "json3", "--no-warnings", "-o", tmp + ".%(ext)s", f"https://www.youtube.com/watch?v={vid}"],
        capture_output=True, timeout=180)
    js = glob.glob(tmp + ".en*.json3") + glob.glob(tmp + ".en.json3")
    if not js:
        return ""
    try:
        d = json.load(open(js[0]))
        text = " ".join(s.get("utf8", "") for ev in d.get("events", []) for s in ev.get("segs", [])
                        if s.get("utf8"))
        text = re.sub(r"\s+", " ", text).strip()
    except Exception:
        text = ""
    finally:
        for f in js:
            try: os.remove(f)
            except OSError: pass
    if text:
        cache.write_text(text)
        idx = _idx(); idx[vid] = {"title": title, "chars": len(text)}; _save_idx(idx)
    return text


def main():
    if len(sys.argv) < 2:
        print("usage: hormozi_fetch.py \"<query>\" [N]", file=sys.stderr); sys.exit(2)
    query = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    got = 0
    for vid, title in search(query, n):
        t = transcript(vid, title)
        if not t:
            continue
        remaining = CAP - got
        if remaining <= 0:
            break
        chunk = t[:remaining]
        print(f"\n===== HORMOZI VIDEO [{vid}] {title} =====\n{chunk}")
        got += len(chunk)
    if got == 0:
        print("(no transcripts retrieved for this query)", file=sys.stderr)


if __name__ == "__main__":
    main()
