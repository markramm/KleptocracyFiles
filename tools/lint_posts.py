#!/usr/bin/env python3
"""
lint_posts.py
Checks posts/*.md for:
- filename pattern YYYY-W##-NN_slug.md
- front-matter keys present
- date ISO
- claims id pattern
- timeline_refs exist in timeline
- required section order (headings)
- heuristic 'factual sentences' without {{cite:...}} (warn)
Exit 0 if OK (or warnings only), 1 on errors (or warnings in --strict)
"""
import argparse, os, re, sys, yaml

FN_RE = re.compile(r"^\d{4}-W\d{2}-\d{2}_.+\.md$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CLAIM_RE = re.compile(r"^C-[A-Za-z0-9-]+$")
CITE_RE = re.compile(r"\{\{cite:([^}]+)\}\}")
HEADINGS_REQ = [
    "## What happened",
    "## Systems impact",
    "## Attack pattern",
    "## Cascade risk",
    "## Monitoring points",
]
ALLOWED_STATUS = {"published","draft","in-review","revised"}

def load_timeline_ids(tdir):
    ids=set()
    for fn in os.listdir(tdir):
        if fn.endswith(".yaml") and fn!="timeline_index.yaml":
            try:
                y = yaml.safe_load(open(os.path.join(tdir,fn), "r", encoding="utf-8")) or {}
                if "id" in y: ids.add(y["id"])
            except Exception:
                pass
    return ids

def has_number_or_date(line):
    if re.search(r"\d{4}-\d{2}-\d{2}", line): return True
    # any number with 2+ digits or $ amounts
    if re.search(r"\$?\b\d{2,}(?:[,\.]\d{3})*(?:\.\d+)?\b", line): return True
    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--posts-dir", default="posts")
    ap.add_argument("--timeline", default="timeline")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    tids = load_timeline_ids(args.timeline)
    errors = []
    warnings = []

    for fn in sorted(os.listdir(args.posts_dir)):
        if not fn.endswith(".md"): continue
        if not FN_RE.match(fn):
            warnings.append((fn, "filename should be YYYY-W##-NN_slug.md"))
        path = os.path.join(args.posts_dir, fn)
        text = open(path, "r", encoding="utf-8").read()

        # split front-matter
        fm = {}
        body = text
        if text.startswith("---"):
            end = text.find("\n---", 3)
            if end != -1:
                fm_txt = text[4:end]
                body = text[end+4:]
                try:
                    fm = yaml.safe_load(fm_txt) or {}
                except Exception as e:
                    errors.append((fn, f"front-matter YAML error: {e}"))
            else:
                errors.append((fn, "front-matter not closed with ---"))
        else:
            errors.append((fn, "missing front-matter"))

        # front-matter keys
        req = {"title","date","status","summary","claims","timeline_refs","risk_level"}
        miss = req - set(fm.keys())
        if miss:
            errors.append((fn, f"missing keys: {sorted(miss)}"))

        # date/status
        d = str(fm.get("date",""))
        if d and not DATE_RE.match(d):
            errors.append((fn, f"bad date format '{d}' (YYYY-MM-DD)"))
        st = fm.get("status")
        if st and st not in ALLOWED_STATUS:
            warnings.append((fn, f"nonstandard status '{st}' (use one of {sorted(ALLOWED_STATUS)})"))

        # claims format
        claims = fm.get("claims") or []
        if not isinstance(claims, list):
            errors.append((fn, "claims should be a list"))
        else:
            for i,c in enumerate(claims):
                if not isinstance(c, str) or not CLAIM_RE.match(c):
                    warnings.append((fn, f"claims[{i}] '{c}' not in C-… format"))

        # timeline refs exist
        trefs = fm.get("timeline_refs") or []
        for ref in trefs:
            if ref not in tids:
                errors.append((fn, f"timeline_refs contains unknown id '{ref}'"))

        # headings presence/order
        lines = body.splitlines()
        hlines = [l for l in lines if l.strip().startswith("## ")]
        # ensure each required heading appears and in order
        pos = -1
        for h in HEADINGS_REQ:
            try:
                i = lines.index(h)
            except ValueError:
                warnings.append((fn, f"missing section heading: {h}"))
                continue
            if i <= pos:
                warnings.append((fn, f"section out of order near: {h}"))
            pos = i

        # placeholder lint
        if re.search(r"TBD|%FACT%|\[citation needed\]|Citation Needed", text, re.I):
            errors.append((fn, "placeholder found (TBD/%FACT%/[citation needed])"))

        # heuristic: lines with numbers/dates but no cite on same line
        for i, l in enumerate(lines, 1):
            if has_number_or_date(l) and "{{cite:" not in l:
                # allow headings or footnotes section
                if l.strip().startswith("## ") or l.strip().startswith("[^"):
                    continue
                warnings.append((fn, f"line {i}: factual-looking line without cite"))

        # cite ids exist
        for cid in set(re.findall(r"\{\{cite:([^}]+)\}\}", text)):
            if cid not in tids:
                errors.append((fn, f"{{{{cite:{cid}}}}} not found in timeline"))

    if errors:
        print("Posts lint FAILED:\n", file=sys.stderr)
        for fn, msg in errors:
            print(f"[ERROR] {fn}: {msg}", file=sys.stderr)
        for fn, msg in warnings:
            print(f"[WARN ] {fn}: {msg}", file=sys.stderr)
        return 1
    if warnings and args.strict:
        print("Posts lint has warnings (strict mode):\n", file=sys.stderr)
        for fn, msg in warnings:
            print(f"[WARN ] {fn}: {msg}", file=sys.stderr)
        return 1
    if warnings:
        print("Posts lint OK with warnings:")
        for fn, msg in warnings:
            print(f"[WARN ] {fn}: {msg}")
    else:
        print("Posts lint OK.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
