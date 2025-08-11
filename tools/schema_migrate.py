#!/usr/bin/env python3
"""
schema_migrate.py
Adds optional metadata keys to timeline/*.yaml without overwriting existing content.
Heuristically fills a few fields (geo, program) when obvious.
"""
import os, yaml, re, sys, datetime, pathlib

BASE = os.path.dirname(os.path.dirname(__file__))
TIMELINE = os.path.join(BASE, "timeline")

OPTIONAL_KEYS = {
    "actors": list,       # [{"name": "...", "role": "..."}]
    "authority": (str, type(None)),
    "program": (str, type(None)),
    "contract": dict,     # {"piid":"", "vehicle":"", "amount":"", "period":""}
    "court_meta": dict,   # {"court":"", "docket":"", "judge":"", "stage":"", "order_url":"", "order_date":""}
    "geo": (str, type(None)),
    "status": (str, type(None)),
    "links": list         # [{"type":"follows"|"relates","id":"..."}]
}

def guess_geo(title, summary):
    t = f"{title} {summary}".lower()
    if "los angeles" in t or "la deployment" in t:
        return "US-CA-LosAngeles"
    if "washington, d.c." in t or "washington dc" in t or "d.c. surge" in t or "dc surge" in t:
        return "US-DC-Washington"
    if "everglades" in t or "dade-collier" in t or "big cypress" in t or "alligator alcatraz" in t:
        return "US-FL-Everglades"
    if "georgia" in t:
        return "US-GA"
    if "texas" in t:
        return "US-TX"
    if "arizona" in t:
        return "US-AZ"
    return None

def guess_program(title, summary):
    s = f"{title} {summary}".lower()
    if "bead" in s and "broadband" in s:
        return "BEAD"
    if "nssl" in s or "national security space launch" in s or "space force" in s:
        return "NSSL Phase 3 Lane 2"
    if "cdao" in s or "frontier ai" in s:
        return "DoD CDAO Frontier AI"
    if "privacy act" in s or "opm" in s or "treasury" in s:
        return None
    return None

def guess_status(title, summary):
    s = f"{title} {summary}".lower()
    if "preliminary injunction" in s or "tro" in s or "halt" in s or "pause" in s or "stay" in s:
        return "litigation: active"
    if "announces" in s or "issues order" in s or "establishes" in s or "opens" in s:
        return "announced/active"
    return None

def migrate_file(path):
    changed = False
    with open(path, "r", encoding="utf-8") as f:
        y = yaml.safe_load(f) or {}
    orig = dict(y)
    # Ensure optional keys
    for k, t in OPTIONAL_KEYS.items():
        if k not in y:
            if t is list:
                y[k] = []
            elif t is dict:
                y[k] = {}
            else:
                y[k] = None
            changed = True
    # Heuristics only if missing
    if not y.get("geo"):
        g = guess_geo(y.get("title",""), y.get("summary",""))
        if g:
            y["geo"] = g; changed = True
    if not y.get("program"):
        p = guess_program(y.get("title",""), y.get("summary",""))
        if p:
            y["program"] = p; changed = True
    if not y.get("status"):
        st = guess_status(y.get("title",""), y.get("summary",""))
        if st:
            y["status"] = st; changed = True
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(y, f, sort_keys=False, width=1000, allow_unicode=True)
    return changed

def main():
    count = 0
    for root, _, files in os.walk(TIMELINE):
        for fn in files:
            if not fn.endswith(".yaml"): continue
            path = os.path.join(root, fn)
            if migrate_file(path):
                count += 1
    print(f"Migrated {count} files at {datetime.datetime.utcnow().isoformat()}Z")

if __name__ == "__main__":
    main()
