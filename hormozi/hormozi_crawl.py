#!/usr/bin/env python3
"""
hormozi_crawl.py [max_per_run]

Background corpus builder: slowly download the transcript of every Alex Hormozi video into the
corpus, a few at a time, rate-limited so YouTube does not throttle. Run detached; over many runs it
accumulates his full catalog into ~/.money-agent-verifier/hormozi/transcripts/ so hormozi_fetch.py
(and future local semantic retrieval) can draw on everything, not just per-round search results.

Enumerates @AlexHormozi/videos (flat), skips already-cached ids, fetches up to max_per_run new
transcripts with a polite sleep between each. Safe to run repeatedly / on a schedule.
"""
import sys, subprocess, json, glob, os, re, time
from pathlib import Path

CORPUS = Path.home() / ".money-agent-verifier" / "hormozi"
TX = CORPUS / "transcripts"; TX.mkdir(parents=True, exist_ok=True)
INDEX = CORPUS / "index.json"
LOG = CORPUS / "crawl.log"
CHANNEL = "https://www.youtube.com/@AlexHormozi/videos"
SLEEP = 20  # seconds between transcript pulls (gentle)


def log(msg):
    with LOG.open("a") as f:
        f.write(msg + "\n")

def _idx():
    return json.loads(INDEX.read_text()) if INDEX.exists() else {}

def _save_idx(idx):
    INDEX.write_text(json.dumps(idx))

def all_ids():
    r = subprocess.run(["yt-dlp", "--flat-playlist", "--no-warnings", "--print",
                        "%(id)s\t%(title)s", CHANNEL], capture_output=True, text=True, timeout=600)
    out = []
    for line in r.stdout.splitlines():
        if "\t" in line:
            vid, title = line.split("\t", 1)
            out.append((vid.strip(), title.strip()))
    return out

def transcript(vid, title):
    cache = TX / f"{vid}.txt"
    if cache.exists():
        return True
    tmp = f"/tmp/hzc_{vid}"
    subprocess.run(["yt-dlp", "--skip-download", "--write-auto-subs", "--sub-langs", "en",
                    "--sub-format", "json3", "--no-warnings", "-o", tmp + ".%(ext)s",
                    f"https://www.youtube.com/watch?v={vid}"], capture_output=True, timeout=180)
    js = glob.glob(tmp + ".en*.json3")
    if not js:
        return False
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
    if not text:
        return False
    cache.write_text(text)
    idx = _idx(); idx[vid] = {"title": title, "chars": len(text)}; _save_idx(idx)
    return True


def main():
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    ids = all_ids()
    have = {p.stem for p in TX.glob("*.txt")}
    todo = [(v, t) for v, t in ids if v not in have]
    log(f"[{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}] catalog={len(ids)} cached={len(have)} todo={len(todo)} this_run_cap={cap}")
    done = 0
    for vid, title in todo:
        if done >= cap:
            break
        ok = transcript(vid, title)
        done += 1 if ok else 0
        log(f"  {'ok ' if ok else 'skip'} {vid} {title[:60]}")
        time.sleep(SLEEP)
    log(f"  run complete: +{done} transcripts, corpus now {len(list(TX.glob('*.txt')))}")


if __name__ == "__main__":
    main()
