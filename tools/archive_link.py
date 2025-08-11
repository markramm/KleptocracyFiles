#!/usr/bin/env python3
"""
archive_link.py — Extended with dedupe
Self-hosted archiver with two channels:
1) General links -> archives/<sha256>.<ext> (HTML, JSON, etc.)
2) Court orders/opinions -> casebook/<sha256>.pdf (and update court_meta)

- Dedupe: if a blob with the same sha256 already exists in the target dir (any extension),
  reuse that filename instead of writing a new one.
- Sidecar YAML stored next to blob for provenance.

CLI examples:
  # Single URL (auto-detect pdf -> casebook)
  python tools/archive_link.py --url https://example.com/page.html --out archives --casebook casebook

  # Walk timeline and update all missing
  python tools/archive_link.py --timeline timeline --out archives --casebook casebook --update

  # Court-only
  python tools/archive_link.py --timeline timeline --casebook casebook --update --court-only
"""
import argparse, os, sys, hashlib, time, datetime
from urllib.parse import urlparse
import yaml, requests

def sha256_bytes(b: bytes) -> str:
    h=hashlib.sha256(); h.update(b); return h.hexdigest()

def ext_from_ctype(ctype: str|None) -> str:
    if not ctype: return ''
    c = ctype.lower()
    if 'pdf' in c: return '.pdf'
    if 'html' in c or 'xml' in c: return '.html'
    if 'json' in c: return '.json'
    if 'text/plain' in c: return '.txt'
    return ''

def infer_ext(url: str, ctype: str|None) -> str:
    e = ext_from_ctype(ctype)
    if e: return e
    path = urlparse(url).path
    ext = os.path.splitext(path)[1].lower()
    if ext in ('.pdf','.html','.htm','.json','.txt','.csv'):
        return ext
    return '.bin'

def is_pdf_like(url: str, ctype: str|None) -> bool:
    if ctype and 'pdf' in ctype.lower(): return True
    path = urlparse(url).path.lower()
    return path.endswith(".pdf")

def fetch(url: str, timeout=30):
    ua = "DebuggingDemocracyArchiver/1.2 (+https://example.org)"
    r = requests.get(url, timeout=timeout, headers={"User-Agent": ua}, allow_redirects=True)
    data = r.content
    ctype = r.headers.get('content-type','').split(';')[0].strip().lower()
    return {
        "status_code": r.status_code,
        "final_url": r.url,
        "content_type": ctype,
        "content": data,
    }

def find_existing_by_sha(directory: str, sha: str):
    if not os.path.isdir(directory):
        return None
    for fn in os.listdir(directory):
        if fn.startswith(sha + ".") and not fn.endswith(".yaml"):
            return os.path.join(directory, fn)
    return None

def save_archive(outdir: str, url: str, blob: dict):
    os.makedirs(outdir, exist_ok=True)
    sha = sha256_bytes(blob["content"])
    ext = infer_ext(url, blob.get("content_type"))
    existing = find_existing_by_sha(outdir, sha)
    if existing:
        fname = os.path.basename(existing)
    else:
        fname = f"{sha}{ext}"
        with open(os.path.join(outdir, fname), "wb") as f:
            f.write(blob["content"])
    meta = {
        "url": url,
        "final_url": blob.get("final_url"),
        "status_code": blob.get("status_code"),
        "content_type": blob.get("content_type"),
        "sha256": sha,
        "archived_at": datetime.datetime.utcnow().isoformat() + "Z",
        "file": os.path.join(os.path.basename(outdir), fname)
    }
    with open(os.path.join(outdir, fname) + ".yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(meta, f, sort_keys=False, allow_unicode=True)
    return meta

def save_casebook(casebook_dir: str, url: str, blob: dict, force=False):
    os.makedirs(casebook_dir, exist_ok=True)
    if not is_pdf_like(url, blob.get("content_type")) and not force:
        raise ValueError(f"Refusing to store non-PDF to casebook without --force-casebook (url: {url}, type: {blob.get('content_type')})")
    sha = sha256_bytes(blob["content"])
    existing = find_existing_by_sha(casebook_dir, sha)
    if existing:
        fname = os.path.basename(existing)
    else:
        fname = f"{sha}.pdf"
        with open(os.path.join(casebook_dir, fname), "wb") as f:
            f.write(blob["content"])
    meta = {
        "url": url,
        "final_url": blob.get("final_url"),
        "status_code": blob.get("status_code"),
        "content_type": blob.get("content_type"),
        "sha256": sha,
        "order_archived_at": datetime.datetime.utcnow().isoformat() + "Z",
        "file": os.path.join(os.path.basename(casebook_dir), fname)
    }
    with open(os.path.join(casebook_dir, fname) + ".yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(meta, f, sort_keys=False, allow_unicode=True)
    return meta

def update_links_in_yaml(ydata: dict, outdir: str, timeout=30, sleep=0.4, dry=False):
    links = ydata.get("links") or ydata.get("sources") or []
    new_links = []
    changed = False
    for item in links:
        obj = {"url": None}
        if isinstance(item, str):
            obj["url"] = item
        elif isinstance(item, dict):
            obj.update(item)
        else:
            new_links.append(item); continue
        url = obj.get("url")
        if not url or not url.lower().startswith(("http://","https://")):
            new_links.append(item); continue
        if obj.get("archive_file") and obj.get("archive_sha256"):
            new_links.append(obj); continue
        try:
            blob = fetch(url, timeout=timeout)
            meta = save_archive(outdir, url, blob) if not dry else {"file": None, "sha256": None, "archived_at": None}
            if not dry:
                obj["archive_file"] = meta["file"]
                obj["archive_sha256"] = meta["sha256"]
                obj["archived_at"] = meta["archived_at"]
                changed = True
        except Exception as e:
            obj.setdefault("archive_error", str(e))
        new_links.append(obj)
        if sleep: time.sleep(sleep)
    if changed and not dry:
        ydata["links"] = new_links
    return changed

def update_court_in_yaml(ydata: dict, casebook_dir: str, timeout=30, sleep=0.4, dry=False, force_casebook=False):
    cm = ydata.get("court_meta") or {}
    if not isinstance(cm, dict): 
        return False
    url = cm.get("order_url") or cm.get("opinion_url")
    if not url:
        return False
    if cm.get("order_file") and cm.get("sha256"):
        return False
    try:
        blob = fetch(url, timeout=timeout)
        meta = save_casebook(casebook_dir, url, blob, force=force_casebook) if not dry else {"file": None, "sha256": None, "order_archived_at": None}
        if not dry:
            cm["order_file"] = meta["file"]
            cm["sha256"] = meta["sha256"]
            cm["order_archived_at"] = meta["order_archived_at"]
            ydata["court_meta"] = cm
        changed = not dry
    except Exception as e:
        cm.setdefault("order_archive_error", str(e))
        ydata["court_meta"] = cm
        changed = False
    if sleep: time.sleep(sleep)
    return changed

def update_timeline_file(path: str, outdir: str, casebook_dir: str, court_only=False, timeout=30, sleep=0.4, dry=False, force_casebook=False):
    y = yaml.safe_load(open(path, "r", encoding="utf-8")) or {}
    changed = False
    if not court_only:
        changed = update_links_in_yaml(y, outdir, timeout=timeout, sleep=sleep, dry=dry) or changed
    changed = update_court_in_yaml(y, casebook_dir, timeout=timeout, sleep=sleep, dry=dry, force_casebook=force_casebook) or changed
    if changed and not dry:
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(y, f, sort_keys=False, allow_unicode=True)
    return changed

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", help="Single URL to archive (archives by default, PDFs -> casebook)")
    ap.add_argument("--out", default="archives", help="Output directory for general archives")
    ap.add_argument("--casebook", default="casebook", help="Output directory for court PDFs")
    ap.add_argument("--timeline", help="Timeline directory to walk")
    ap.add_argument("--update", action="store_true", help="Update timeline YAML files with archive info")
    ap.add_argument("--court-only", action="store_true", help="Only process court_meta order/opinion urls")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--sleep", type=float, default=0.4)
    ap.add_argument("--force-casebook", action="store_true", help="Allow non-PDF content to be stored in casebook")
    args = ap.parse_args()

    if args.url and not args.timeline:
        blob = fetch(args.url, timeout=args.timeout)
        try:
            if is_pdf_like(args.url, blob.get("content_type")):
                meta = save_casebook(args.casebook, args.url, blob, force=args.force_casebook) if not args.dry_run else {}
            else:
                meta = save_archive(args.out, args.url, blob) if not args.dry_run else {}
            print(yaml.safe_dump(meta, sort_keys=False))
            return 0
        except Exception as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            return 1

    if args.timeline and args.update:
        tdir = args.timeline
        files = [os.path.join(tdir, f) for f in os.listdir(tdir) if f.endswith(".yaml") and f!="timeline_index.yaml"]
        changed_any = False
        for p in sorted(files):
            try:
                changed = update_timeline_file(
                    p, args.out, args.casebook,
                    court_only=args.court_only, timeout=args.timeout, sleep=args.sleep,
                    dry=args.dry_run, force_casebook=args.force_casebook
                )
                if changed: print(f"Updated {os.path.basename(p)}")
                changed_any = changed_any or changed
            except Exception as e:
                print(f"[WARN] {p}: {e}", file=sys.stderr)
        print("Done. Changes:", changed_any)
        return 0

    print("Nothing to do. Use --url or --timeline --update.", file=sys.stderr)
    return 2

if __name__ == "__main__":
    raise SystemExit(main())

