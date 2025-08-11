#!/usr/bin/env python3
import argparse, sys, json
from pathlib import Path
import yaml
import urllib.request, urllib.error

REPO = Path(__file__).resolve().parents[1]
TIMELINE = REPO / "timeline"

def check_url(url, timeout=12):
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.getheader("Location")
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return None, str(e)

def main():
    ap = argparse.ArgumentParser(description="Check timeline citation URLs for reachability.")
    ap.add_argument("--limit", type=int, default=0, help="Limit number of files checked")
    ap.add_argument("--csv", default=None, help="Optional CSV output file")
    args = ap.parse_args()
    files = sorted([p for p in TIMELINE.glob("*.yml") if p.name != "_SCHEMA.json"])
    if args.limit:
        files = files[:args.limit]
    results = []
    for y in files:
        d = yaml.safe_load(y.read_text(encoding="utf-8")) or {}
        for url in d.get("citations") or []:
            status, info = check_url(url)
            results.append({"file": y.name, "url": url, "status": status, "info": info})
            print(json.dumps(results[-1]))
    if args.csv:
        import csv

        with open(args.csv, "w", newline="", encoding="utf-8") as fp:
            writer = csv.DictWriter(fp, fieldnames=["file", "url", "status", "info"])
            writer.writeheader()
            writer.writerows(results)
    # summary to stderr
    ok = sum(1 for r in results if r["status"] and 200 <= r["status"] < 400)
    bad = sum(1 for r in results if r["status"] and r["status"] >= 400)
    unk = sum(1 for r in results if r["status"] is None)
    print(f"# OK={ok} BAD={bad} UNKNOWN={unk}", file=sys.stderr)

if __name__ == "__main__":
    main()
