# Casebook

This folder is meant to store primary-source PDFs (court orders, EOs, GAO opinions, agency memos) for events in `timeline/`.

## How to build locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r tools/requirements.txt
python tools/schema_migrate.py
python tools/build_casebook.py
```

The fetcher will:
- scan `timeline/*.yaml`
- try to download any `.pdf` sources or documents from known gov/legal hosts
- write files under `casebook/<event-id>/...`
- update timeline entries with `court_meta.order_file` when an “order/opinion” match is found
- produce `casebook/casebook_index.json` mapping event IDs to local files

## Footnotes for posts

Generate Google-Docs-style footnotes from a set of timeline IDs:

```bash
python tools/footnotes.py --ids 2025-06-07-dod-support-dhs-memo-and-la-deployments 2025-06-12-breyer-ruling-and-ninth-circuit-stays > posts/_includes/footnotes.md
```

Or, put IDs into `ids.txt` (one per line):

```bash
python tools/footnotes.py --file ids.txt > posts/_includes/footnotes.md
```
*Filed: 2025-08-11*
