#!/usr/bin/env python3
"""Live check of every official link in data/links.json.
Each URL must return HTTP 200 after redirects; HTML pages must contain the
expected phrase (case-insensitive) and any #anchor; PDFs must be real PDFs.
Usage: python3 scripts/check_links.py
"""
import html, json, os, re, sys, time, urllib.request
from urllib.parse import urldefrag
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "Mozilla/5.0 (event-planner link check)"}
links = json.load(open(os.path.join(ROOT, "data", "links.json")))["links"]

def get(url, tries=3):
    err = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.status, r.headers.get("Content-Type", ""), r.read()
        except Exception as e:
            err = e; time.sleep(3 * (i + 1))
    return getattr(err, "code", 0) or 0, "", b""

items = [(t, c, it) for t, v in links.items() for c, its in v.items() if c != "generic" for it in its]
cache, bad = {}, []
for n, (topic, country, it) in enumerate(items, 1):
    base, frag = urldefrag(it["url"])
    if base not in cache:
        cache[base] = get(base); time.sleep(0.5)
    status, ctype, body = cache[base]
    note = "ok"
    if status != 200:
        note = f"HTTP {status}"
    elif base.endswith(".pdf"):
        if not body.startswith(b"%PDF"): note = "not a PDF"
    else:
        page = body.decode("utf-8", "replace")
        text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", page)))).lower()
        if it["expect"] and it["expect"].lower().replace("’", "'") not in text.replace("’", "'"):
            note = f"phrase missing: {it['expect']!r}"
        if frag and f'id="{frag}"' not in page:
            note = f"anchor #{frag} missing"
    print(f"[{n}/{len(items)}] {status} {topic}/{country} {it['url']}  {note}", flush=True)
    if note != "ok": bad.append((it["url"], note))
print(f"\n{len(items)} links on {len(cache)} pages")
if bad:
    print(f"{len(bad)} PROBLEMS"); [print(" ", u, w) for u, w in bad]; sys.exit(1)
print("ALL LINKS OK: HTTP 200, expected phrase and anchors present, PDFs valid")
