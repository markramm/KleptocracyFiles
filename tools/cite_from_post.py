#!/usr/bin/env python3
"""
Generate footnotes for posts from timeline cards.

Usage:
  python tools/cite_from_post.py --post posts/post-03.md
  python tools/cite_from_post.py --all

It scans for tokens like {{cite:TIMELINE_ID}} or {{cite:ID1,ID2}} in the post
and emits a numbered footnote list with full URLs. If court_meta exists, it appends
judge, docket, and order info.

Outputs:
  - writes posts/_footnotes/<post-slug>.md
  - prints a summary to stdout
"""
import argparse, re, sys, os, glob, yaml, pathlib
from datetime import datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
TIMELINE = ROOT / "timeline"
FOOTDIR = ROOT / "posts" / "_footnotes"

CITE_RE = re.compile(r"\{\{cite:([A-Za-z0-9_\-., ]+)\}\}")

def load_card(card_path):
    with open(card_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def find_card(id_):
    # look for timeline/<id>.yaml, then in subfolders
    p = TIMELINE / f"{id_}.yaml"
    if p.exists():
        return p
    # try updates overlay
    for path in TIMELINE.rglob(f"{id_}.yaml"):
        return path
    return None

def build_footnote_entry(card):
    title = card.get("title","")
    date = card.get("date","")
    srcs = card.get("sources",[]) or card.get("links",[])
    first_url = ""
    if isinstance(srcs, list) and srcs:
        # choose the first http(s) url
        for s in srcs:
            if isinstance(s, dict) and s.get("url","").startswith("http"):
                first_url = s["url"]; break
            if isinstance(s, str) and s.startswith("http"):
                first_url = s; break
    court_meta = card.get("court_meta") or {}
    cm_bits = []
    if court_meta:
        if court_meta.get("court"): cm_bits.append(court_meta["court"])
        if court_meta.get("judge"): cm_bits.append(f"Judge {court_meta['judge']}")
        if court_meta.get("docket"): cm_bits.append(f"Docket {court_meta['docket']}")
        if court_meta.get("order_date") and court_meta.get("order_type"):
            cm_bits.append(f"{court_meta['order_type']} on {court_meta['order_date']}")
    cm = (" — " + "; ".join(cm_bits)) if cm_bits else ""
    return f"{title} ({date}){cm}. {first_url}".strip()

def extract_cites(text):
    ids = []
    for m in CITE_RE.finditer(text):
        chunk = m.group(1)
        for raw in chunk.split(","):
            id_ = raw.strip()
            if id_:
                ids.append(id_)
    # preserve order but dedupe
    seen = set(); ordered = []
    for i in ids:
        if i not in seen:
            ordered.append(i); seen.add(i)
    return ordered

def slugify(path):
    base = os.path.basename(path)
    return os.path.splitext(base)[0]

def process_post(post_path):
    with open(post_path, "r", encoding="utf-8") as f:
        text = f.read()
    ids = extract_cites(text)
    items = []
    missing = []
    for id_ in ids:
        p = find_card(id_)
        if not p:
            missing.append(id_); continue
        card = load_card(p)
        items.append((id_, build_footnote_entry(card)))
    # write footnotes file
    FOOTDIR.mkdir(parents=True, exist_ok=True)
    out = FOOTDIR / f"{slugify(post_path)}.md"
    with open(out, "w", encoding="utf-8") as f:
        for idx, (_id, line) in enumerate(items, start=1):
            f.write(f"[{idx}] {line}\n")
    return out, items, missing

def process_all():
    out_map = {}
    for path in glob.glob(str(ROOT / "posts" / "*.md")):
        out, items, missing = process_post(path)
        out_map[path] = {"footnotes": str(out), "count": len(items), "missing": missing}
    return out_map

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--post", help="Path to a single post .md")
    ap.add_argument("--all", action="store_true", help="Process all posts/*.md")
    args = ap.parse_args()
    if args.post:
        out, items, missing = process_post(args.post)
        print(f"Wrote {out} ({len(items)} cites). Missing: {missing}")
    else:
        data = process_all()
        for k,v in data.items():
            print(f"{k}: {v['count']} cites; footnotes -> {v['footnotes']}; missing={v['missing']}")

if __name__ == "__main__":
    main()
