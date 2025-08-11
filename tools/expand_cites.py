#!/usr/bin/env python3
"""
expand_cites.py
Expands {{cite:EVENT_ID}} tokens in posts/*.md into footnotes,
using links/sources from timeline/*.yaml. Writes output to --out-dir.
Fails if any cite IDs are missing.
"""
import argparse, os, re, yaml, sys
from datetime import datetime

CITE_RE = re.compile(r"\{\{cite:([^}]+)\}\}")

def load_timeline(tdir):
    index = {}
    for fn in os.listdir(tdir):
        if not fn.endswith(".yaml") or fn == "timeline_index.yaml":
            continue
        y = yaml.safe_load(open(os.path.join(tdir, fn), "r", encoding="utf-8")) or {}
        _id = y.get("id")
        if _id:
            index[_id] = y
    return index

def footnote_label(ev):
    # Prefer title + date
    title = ev.get("title","(untitled)")
    date = ev.get("date","")
    if date:
        return f"{title} ({date})"
    return title

def extract_links(ev):
    links = []
    for key in ("links","sources"):
        arr = ev.get(key) or []
        for item in arr:
            if isinstance(item, str):
                links.append((None, item))
            elif isinstance(item, dict) and item.get("url"):
                links.append((item.get("title"), item["url"]))
    # de-dup by URL
    seen = set(); out = []
    for title, url in links:
        if url in seen: continue
        seen.add(url); out.append((title, url))
    return out

def expand_post(mp, index):
    # Split front-matter if present
    fm = {}
    body = mp
    if mp.startswith("---"):
        end = mp.find("\n---", 3)
        if end != -1:
            fm_txt = mp[4:end]
            body = mp[end+4:]
            try:
                fm = yaml.safe_load(fm_txt) or {}
            except Exception:
                fm = {}

    cites = []
    def sub_fn(m):
        _id = m.group(1).strip()
        cites.append(_id)
        # The numeric token will be assigned after we de-dup
        return f"[^{_id}]"

    replaced = CITE_RE.sub(sub_fn, body)

    # Build footnote map (unique in insertion order)
    unique = []
    seen = set()
    for c in cites:
        if c not in seen:
            seen.add(c)
            unique.append(c)

    # Validate all cite IDs exist
    missing = [c for c in unique if c not in index]
    if missing:
        return None, missing

    # Build footnotes text
    lines = []
    lines.append("\n\n## Sources & Footnotes\n")
    nmap = {}  # id -> number
    for i, cid in enumerate(unique, 1):
        nmap[cid] = i
        ev = index[cid]
        label = footnote_label(ev)
        links = extract_links(ev)
        lines.append(f"[^{i}]: {label}")
        if links:
            for title, url in links:
                if title:
                    lines.append(f"    - {title}: {url}")
                else:
                    lines.append(f"    - {url}")
        else:
            lines.append("    - (no links provided)")
        lines.append("")

    # Replace [^ID] with actual numbers
    def numberize(m):
        cid = m.group(1)
        return f"[^{nmap.get(cid, '?')}]"
    numbered = re.sub(r"\[\^([^\]]+)\]", numberize, replaced)

    out_text = ""
    if fm:
        out_text += "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n"
    out_text += numbered + "\n" + "\n".join(lines) + "\n"
    return out_text, []

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--posts-dir", default="posts", help="Directory with .md posts")
    ap.add_argument("--timeline", default="timeline", help="Timeline directory with .yaml")
    ap.add_argument("--out-dir", default="build/posts", help="Where to write expanded posts")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    index = load_timeline(args.timeline)
    failures = []

    for fn in sorted(os.listdir(args.posts_dir)):
        if not fn.endswith(".md"): continue
        path = os.path.join(args.posts_dir, fn)
        txt = open(path, "r", encoding="utf-8").read()
        out, missing = expand_post(txt, index)
        if missing:
            for cid in missing:
                failures.append((fn, cid))
            continue
        out_path = os.path.join(args.out_dir, fn)
        open(out_path, "w", encoding="utf-8").write(out)

    if failures:
        print("expand_cites FAILED — missing timeline IDs:", file=sys.stderr)
        for fn, cid in failures:
            print(f"  {fn} -> {cid}", file=sys.stderr)
        sys.exit(1)

    print(f"expand_cites OK — wrote to {args.out_dir}")
    sys.exit(0)

if __name__ == "__main__":
    main()
