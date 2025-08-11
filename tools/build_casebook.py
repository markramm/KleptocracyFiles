#!/usr/bin/env python3
"""
build_casebook.py
Attempts to download primary documents (PDF orders, memos) referenced in timeline sources to a local `casebook/` folder.
- Only downloads .pdf URLs or known gov/legal hosts.
- Writes casebook/casebook_index.json mapping timeline ID -> local files.
- Optionally updates timeline files to add court_meta.order_file when a matching doc is found.

NOTE: Requires internet; run locally. `pip install requests`
"""
import os, re, sys, json, yaml, pathlib, urllib.parse
from typing import List
try:
    import requests
except ImportError:
    print("Please install requests: pip install requests", file=sys.stderr); sys.exit(1)

BASE = os.path.dirname(os.path.dirname(__file__))
TIMELINE = os.path.join(BASE, "timeline")
CASEBOOK = os.path.join(BASE, "casebook")

PDF_HOST_HINTS = (
    "courtlistener.com", "supremecourt.gov", "ca9.uscourts.gov", "cand.uscourts.gov",
    "law.justia.com", "govinfo.gov", "eff.org", "gao.gov", "opm.gov", "whitehouse.gov",
    "epa.gov", "fcc.gov", "state.gov", "ssa.gov", "irs.gov", "opm.gov", "treasury.gov"
)

def should_fetch(url: str) -> bool:
    if url.lower().endswith(".pdf"):
        return True
    host = urllib.parse.urlparse(url).netloc.lower()
    return any(h in host for h in PDF_HOST_HINTS)

def sanitize_filename(s: str) -> str:
    return re.sub(r'[^A-Za-z0-9._-]+','_', s)[:140]

def iter_cards():
    for root, _, files in os.walk(TIMELINE):
        for fn in files:
            if not fn.endswith(".yaml"): continue
            path = os.path.join(root, fn)
            y = yaml.safe_load(open(path, "r", encoding="utf-8")) or {}
            yield path, y

def download(url: str, outdir: str) -> str:
    fn = sanitize_filename(os.path.basename(urllib.parse.urlparse(url).path) or "document.pdf")
    if not fn.lower().endswith(".pdf"):
        fn += ".pdf"
    out = os.path.join(outdir, fn)
    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        with open(out, "wb") as f:
            f.write(r.content)
        return out
    except Exception as e:
        print(f"Failed to fetch {url}: {e}", file=sys.stderr)
        return ""

def main():
    os.makedirs(CASEBOOK, exist_ok=True)
    index = {}
    for path, y in iter_cards():
        cid = y.get("id") or os.path.basename(path).replace(".yaml","")
        bucket = []
        for src in y.get("sources", []):
            url = src.get("url")
            if not url or not should_fetch(url):
                continue
            localdir = os.path.join(CASEBOOK, sanitize_filename(cid))
            os.makedirs(localdir, exist_ok=True)
            local = download(url, localdir)
            if local:
                bucket.append({"title": src.get("title"), "url": url, "file": os.path.relpath(local, CASEBOOK)})
        if bucket:
            index[cid] = bucket
            # If any looks like an order, stash into court_meta.order_file (non-destructive)
            for b in bucket:
                if re.search(r'(order|opinion|memorandum|injunction|ruling)', (b.get("title") or "").lower()):
                    y.setdefault("court_meta", {})
                    if not y["court_meta"].get("order_file"):
                        y["court_meta"]["order_file"] = f"casebook/{cid}/{os.path.basename(b['file'])}"
            with open(path, "w", encoding="utf-8") as f:
                yaml.safe_dump(y, f, sort_keys=False, width=1000, allow_unicode=True)

    with open(os.path.join(CASEBOOK, "casebook_index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(index)} case entries to casebook_index.json")

if __name__ == "__main__":
    main()
