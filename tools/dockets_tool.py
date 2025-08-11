#!/usr/bin/env python3
"""
Dockets & judges updater for timeline cards.

Modes:
  export-missing  -> writes tools/dockets_to_fill.csv with rows needing judge/docket
  apply-updates   -> reads tools/dockets_updates.csv and patches matching timeline YAMLs

CSV format (dockets_updates.csv):
id,court,docket,judge,order_date,order_type,order_url,notes

The tool preserves existing fields and only fills when provided.
"""
import argparse, csv, pathlib, yaml, sys, os

ROOT = pathlib.Path(__file__).resolve().parents[1]
TIMELINE = ROOT / "timeline"
UPDATES = ROOT / "tools" / "dockets_updates.csv"
MISSING = ROOT / "tools" / "dockets_to_fill.csv"

def iter_cards():
    for p in TIMELINE.rglob("*.yaml"):
        if p.name == "timeline_index.yaml":
            continue
        yield p

def load(p): 
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def dump(p, data):
    with open(p, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)

def export_missing():
    rows = [["id","path","title","date","status","court","docket","judge"]]
    for p in iter_cards():
        card = load(p)
        raw_status = card.get("status")
        if isinstance(raw_status, str):
            status = raw_status
        elif isinstance(raw_status, list):
            status = ";".join(str(s) for s in raw_status)
        else:
            status = str(raw_status or "")
        cm = card.get("court_meta") or {}
        needs = False
        if "litigation" in status or "injunction" in status or cm:
            if not cm or not cm.get("docket") or not cm.get("judge"):
                needs = True
        if needs:
            rows.append([card.get("id") or p.stem, str(p), card.get("title",""), card.get("date",""), status, cm.get("court",""), cm.get("docket",""), cm.get("judge","")])
    with open(MISSING, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    print(f"Wrote {MISSING} ({len(rows)-1} rows)")

def apply_updates():
    if not UPDATES.exists():
        print(f"No updates file at {UPDATES}")
        sys.exit(1)
    with open(UPDATES, "r", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        updates = list(rdr)
    applied = 0
    for row in updates:
        id_ = row["id"].strip()
        if not id_:
            continue
        # find the card
        target = None
        for p in iter_cards():
            stem = p.stem
            # support both exact id or filename match
            card = load(p)
            if (card.get("id") == id_) or (stem == id_):
                target = p; data = card; break
        if not target:
            print(f"[warn] No card for id={id_}")
            continue
        cm = data.get("court_meta") or {}
        for k in ["court","docket","judge","order_date","order_type","order_url"]:
            if row.get(k):
                cm[k] = row[k]
        if cm:
            data["court_meta"] = cm
        # also push into links if order_url given
        if row.get("order_url"):
            links = data.get("links") or data.get("sources") or []
            if isinstance(links, list):
                if row["order_url"] not in [l if isinstance(l,str) else l.get("url","") for l in links]:
                    links.append(row["order_url"])
            data["links"] = links
        dump(target, data); applied += 1
        print(f"Updated {id_} at {target}")
    print(f"Applied {applied} update rows.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["export-missing","apply-updates"])
    args = ap.parse_args()
    if args.mode == "export-missing":
        export_missing()
    else:
        apply_updates()

if __name__ == "__main__":
    main()
