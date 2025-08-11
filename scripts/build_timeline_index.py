#!/usr/bin/env python3
import json, hashlib
from pathlib import Path

def sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def main(timeline_dir="timeline", out_json="timeline/index.json"):
    tdir = Path(timeline_dir)
    events = []
    for y in sorted(tdir.glob("*.yaml")):
        data = {}
        # simple YAML parse: rely on minimal fields; not robust, but enough for listing keys
        # Since we control the writer, we can parse in a naive way.
        key = None
        current = {}
        lines = y.read_text(encoding="utf-8").splitlines()
        i = 0
        while i < len(lines):
            ln = lines[i]
            if ": |" in ln:
                k = ln.split(":")[0].strip()
                i += 1
                buf = []
                while i < len(lines) and (lines[i].startswith("  ") or lines[i].strip()==""):
                    buf.append(lines[i][2:] if lines[i].startswith("  ") else "")
                    i += 1
                current[k] = "\n".join(buf).strip()
                continue
            elif ln.endswith(":") and not ln.strip().startswith("-"):
                k = ln[:-1].strip()
                # list to follow
                i += 1
                arr = []
                while i < len(lines) and lines[i].strip().startswith("- "):
                    arr.append(lines[i].strip()[2:])
                    i += 1
                current[k] = arr
                continue
            elif ":" in ln:
                k, v = ln.split(":", 1)
                current[k.strip()] = v.strip().strip('"')
            i += 1

        data = current
        data["_file"] = y.name
        data["_id_hash"] = sha256(data.get("id",""))
        events.append(data)
    Path(out_json).write_text(json.dumps({"events": events}, indent=2), encoding="utf-8")
    print(f"Wrote {out_json} with {len(events)} events")

if __name__ == "__main__":
    main()
