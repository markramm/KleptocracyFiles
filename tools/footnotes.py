#!/usr/bin/env python3
"""
footnotes.py
Generate Google-Docs-style footnotes from timeline IDs.

Usage:
  python tools/footnotes.py --ids 2025-06-07-dod-support-dhs-memo-and-la-deployments 2025-06-12-breyer-ruling-and-ninth-circuit-stays > footnotes.md

Or pass a file of IDs (one per line):
  python tools/footnotes.py --file ids.txt > footnotes.md
"""
import os, sys, yaml, argparse, itertools, textwrap

BASE = os.path.dirname(os.path.dirname(__file__))
TIMELINE = os.path.join(BASE, "timeline")

def load_card(card_id):
    # find file by id
    for root, _, files in os.walk(TIMELINE):
        for fn in files:
            if not fn.endswith(".yaml"): continue
            path = os.path.join(root, fn)
            y = yaml.safe_load(open(path, "r", encoding="utf-8")) or {}
            if y.get("id") == card_id:
                return y
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", nargs="*", help="timeline IDs")
    ap.add_argument("--file", help="file containing IDs")
    args = ap.parse_args()

    ids = list(args.ids or [])
    if args.file:
        ids.extend([line.strip() for line in open(args.file, "r", encoding="utf-8") if line.strip()])
    ids = [i for i in ids if i]

    sources = []
    for cid in ids:
        card = load_card(cid)
        if not card:
            continue
        for src in card.get("sources", []):
            title = src.get("title") or ""
            url = src.get("url") or ""
            if not url:
                continue
            sources.append((title, url, cid))

    # de-duplicate by (title,url)
    seen = set()
    out = []
    for (title, url, cid) in sources:
        key = (title, url)
        if key in seen: 
            continue
        seen.add(key)
        out.append((title, url, cid))

    # Emit simple numeric list suitable for docs
    for i, (title, url, cid) in enumerate(out, 1):
        print(f"{i}. {title} — {url}  (ref: {cid})")

if __name__ == "__main__":
    main()
