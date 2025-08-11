#!/usr/bin/env python3
"""
validate_timeline.py
Validates timeline/*.yaml against a pragmatic schema and catches common issues.
Exit code 0 => OK, non-zero => problems found.
"""
import argparse, os, sys, re, yaml, hashlib, json
from urllib.parse import urlparse
from datetime import datetime

ALLOWED_STATUS = {
    "confirmed",
    "pending_verification",
    "announced/active",
    "litigation: active",
    "litigation: on appeal",
    "injunction: active",
    "oversight finding",
}

ID_RE = re.compile(r"^\d{4}-\d{2}-\d{2}_[a-z0-9][a-z0-9\-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

def is_url(s: str) -> bool:
    try:
        u = urlparse(s)
        return u.scheme in ("http","https") and bool(u.netloc)
    except Exception:
        return False

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeline", default="timeline", help="Path to timeline/ directory")
    ap.add_argument("--repo-root", default=".", help="Repo root (for casebook/ resolution)")
    ap.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    args = ap.parse_args()

    tdir = args.timeline
    root = os.path.abspath(args.repo_root)

    if not os.path.isdir(tdir):
        print(f"[ERROR] timeline directory not found: {tdir}", file=sys.stderr)
        return 2

    files = [f for f in os.listdir(tdir) if f.endswith(".yaml") and f != "timeline_index.yaml"]
    if not files:
        print("[ERROR] no timeline YAML files found.", file=sys.stderr)
        return 2

    ids = set()
    errors = []
    warnings = []

    for fn in sorted(files):
        path = os.path.join(tdir, fn)
        try:
            data = yaml.safe_load(open(path, "r", encoding="utf-8")) or {}
        except Exception as e:
            errors.append((fn, f"YAML parse error: {e}"))
            continue

        # Required keys
        for k in ("id","date","title","status"):
            if not data.get(k):
                errors.append((fn, f"missing required key: {k}"))

        _id = data.get("id","")
        if _id and not ID_RE.match(_id):
            errors.append((fn, f"bad id format '{_id}' (expected YYYY-MM-DD_slug-lowercase)"))

        _date = data.get("date","")
        if _date and not DATE_RE.match(_date):
            errors.append((fn, f"bad date format '{_date}' (expected YYYY-MM-DD)"))
        else:
            # extra: invalid calendar dates
            try:
                if _date:
                    datetime.strptime(_date, "%Y-%m-%d")
            except Exception:
                errors.append((fn, f"invalid calendar date '{_date}'"))

        _status = data.get("status")
        if _status and _status not in ALLOWED_STATUS:
            errors.append((fn, f"nonstandard status '{_status}' (allowed: {sorted(ALLOWED_STATUS)})"))

        # Uniqueness
        if _id:
            if _id in ids:
                errors.append((fn, f"duplicate id '{_id}'"))
            ids.add(_id)

        # Links validation
        for key in ("links","sources"):
            arr = data.get(key) or []
            if not isinstance(arr, list):
                errors.append((fn, f"{key} must be a list"))
            else:
                for i, item in enumerate(arr):
                    if isinstance(item, str):
                        if not is_url(item):
                            warnings.append((fn, f"{key}[{i}] not a valid URL: {item!r}"))
                    elif isinstance(item, dict):
                        url = item.get("url","")
                        if not url or not is_url(url):
                            warnings.append((fn, f"{key}[{i}].url missing or invalid: {url!r}"))
                    else:
                        errors.append((fn, f"{key}[{i}] must be string or object"))

        # court_meta checks
        cm = data.get("court_meta") or {}
        if cm and not isinstance(cm, dict):
            errors.append((fn, "court_meta must be an object"))
        if isinstance(cm, dict):
            od = cm.get("order_date")
            if od and not DATE_RE.match(str(od)):
                warnings.append((fn, f"court_meta.order_date not YYYY-MM-DD: {od!r}"))
            of = cm.get("order_file")
            sha = cm.get("sha256")
            if of:
                # resolve relative to repo root
                cf = os.path.join(root, of) if not os.path.isabs(of) else of
                if not os.path.isfile(cf):
                    warnings.append((fn, f"court_meta.order_file not found on disk: {of}"))
                else:
                    calc = sha256_file(cf)
                    if sha and calc != sha:
                        errors.append((fn, f"court_meta.sha256 mismatch (have {sha}, calc {calc})"))
                    elif not sha:
                        warnings.append((fn, f"court_meta.sha256 missing (calc {calc})"))

    # Report
    if errors:
        print("Timeline validation FAILED:\n", file=sys.stderr)
        for fn, msg in errors:
            print(f"[ERROR] {fn}: {msg}", file=sys.stderr)
        if warnings:
            print("\nWarnings:", file=sys.stderr)
            for fn, msg in warnings:
                print(f"[WARN ] {fn}: {msg}", file=sys.stderr)
        return 1

    # If strict, treat warnings as errors
    if args.strict and warnings:
        print("Timeline validation has warnings (strict mode):\n", file=sys.stderr)
        for fn, msg in warnings:
            print(f"[WARN ] {fn}: {msg}", file=sys.stderr)
        return 1

    # Success
    if warnings:
        print("Timeline validation OK with warnings:")
        for fn, msg in warnings:
            print(f"[WARN ] {fn}: {msg}")
    else:
        print("Timeline validation OK.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
