#!/usr/bin/env python3
"""
lint_timeline.py (fixed)
Style & quality linter for timeline/*.yaml
- filename ↔ id consistency
- title/summary quality hints
- type/status normalization suggestions
- actors/geo types
- links: recommend archive_file + archive_sha256 if url present
- court_meta basic checks
Exit 0 if OK (or warnings only), 1 on errors (or warnings in --strict)
"""
import argparse, os, re, sys, yaml
from datetime import datetime

ID_RE = re.compile(r"^\d{4}-\d{2}-\d{2}_[a-z0-9][a-z0-9\-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FILENAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}_[a-z0-9][a-z0-9\-]*\.yaml$")
ALLOWED_STATUS = {
    "confirmed",
    "pending_verification",
    "announced/active",
    "litigation: active",
    "litigation: on appeal",
    "injunction: active",
    "oversight finding",
}
ALLOWED_TYPES = {
    "executive-order","policy-change","legislation","litigation","injunction","sanctions",
    "ethics","reporting","enforcement-policy","finance-deal","policy-business"
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeline", default="timeline")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    tdir = args.timeline
    if not os.path.isdir(tdir):
        print(f"[ERROR] timeline dir not found: {tdir}", file=sys.stderr)
        return 2

    warnings = []
    errors = []

    for fn in sorted(os.listdir(tdir)):
        if not fn.endswith(".yaml") or fn == "timeline_index.yaml":
            continue
        path = os.path.join(tdir, fn)
        try:
            data = yaml.safe_load(open(path, "r", encoding="utf-8")) or {}
        except Exception as e:
            errors.append((fn, f"YAML parse error: {e}"))
            continue

        # filename style
        if not FILENAME_RE.match(fn):
            warnings.append((fn, "filename should be YYYY-MM-DD_slug.yaml (lowercase, hyphens)"))

        # id ↔ filename stem
        stem = fn[:-5]
        _id = data.get("id")
        if _id and _id != stem:
            warnings.append((fn, f"id '{_id}' does not match filename stem '{stem}'"))

        # date ISO & plausible
        d = data.get("date")
        if d and not DATE_RE.match(str(d)):
            warnings.append((fn, f"non-ISO date '{d}' (expected YYYY-MM-DD)"))

        # title quality
        title = (data.get("title") or "").strip()
        if len(title) < 8:
            warnings.append((fn, "title is very short (<8 chars)"))
        if len(title) > 160:
            warnings.append((fn, "title is very long (>160 chars)"))
        if title and title[0].islower():
            warnings.append((fn, "title should be capitalized"))

        # type/status normalization
        t = data.get("type")
        if t and t not in ALLOWED_TYPES:
            warnings.append((fn, f"nonstandard type '{t}' (suggest one of {sorted(ALLOWED_TYPES)})"))
        s = data.get("status")
        if s and s not in ALLOWED_STATUS:
            warnings.append((fn, f"nonstandard status '{s}' (allowed {sorted(ALLOWED_STATUS)})"))

        # actors/geo shape
        actors = data.get("actors")
        if actors and not isinstance(actors, list):
            warnings.append((fn, "actors should be a list (['Agency', 'Person', ...])"))
        geo = data.get("geo") or data.get("jurisdictions")
        if geo and not isinstance(geo, list):
            warnings.append((fn, "geo/jurisdictions should be a list of strings"))

        # links advice (prefer archive_file + archive_sha256)
        links = data.get("links") or data.get("sources") or []
        if not isinstance(links, list):
            errors.append((fn, "links/sources must be a list"))
        else:
            for i, item in enumerate(links):
                if isinstance(item, dict):
                    url = item.get("url")
                    af = item.get("archive_file")
                    ash = item.get("archive_sha256")
                    if url and not (af and ash):
                        warnings.append((fn, f"links[{i}] consider archiving: missing archive_file/archive_sha256 for {url}"))
                    if af and not ash:
                        warnings.append((fn, f"links[{i}] archive_file present but archive_sha256 missing"))
                elif isinstance(item, str):
                    warnings.append((fn, f"links[{i}] is a raw URL string — consider expanding to object with title/url + archive_file"))

        # court_meta basic
        cm = data.get("court_meta") or {}
        if cm and not isinstance(cm, dict):
            warnings.append((fn, "court_meta should be an object"))
        elif isinstance(cm, dict):
            if cm.get("order_file") and not cm.get("sha256"):
                warnings.append((fn, "court_meta.order_file present but sha256 missing"))
            if cm.get("order_url") and not (cm.get("order_file") and cm.get("sha256")):
                warnings.append((fn, "court_meta.order_url present — consider running archiver to populate order_file/sha256"))

    if errors:
        print("Timeline lint FAILED:\n", file=sys.stderr)
        for fn, msg in errors:
            print(f"[ERROR] {fn}: {msg}", file=sys.stderr)
        if warnings:
            print("\nWarnings:", file=sys.stderr)
            for fn, msg in warnings:
                print(f"[WARN ] {fn}: {msg}", file=sys.stderr)
        return 1

    if args.strict and warnings:
        print("Timeline lint has warnings (strict mode):\n", file=sys.stderr)
        for fn, msg in warnings:
            print(f"[WARN ] {fn}: {msg}", file=sys.stderr)
        return 1

    if warnings:
        print("Timeline lint OK with warnings:")
        for fn, msg in warnings:
            print(f"[WARN ] {fn}: {msg}")
    else:
        print("Timeline lint OK.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
