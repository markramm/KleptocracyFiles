# Kleptocracy Files – Agent Guide

## Generated artifacts
- Footnote pages in `posts/` – build with `scripts/build_footnotes.py`.
- Link report – run `python scripts/link_check.py --csv link_check.csv`.
  - The checker caches results in `link_status.json`; commit this file so repeated runs can skip recently verified URLs.
<!--
`timeline/index.json` is generated in the GitHub Pages workflow and is no longer committed.
Run `python scripts/build_timeline_index.py` locally if you need a fresh index for development.
-->

## Archiving citations
- Timeline YAML `citations` entries may specify `url` and optional `archived` fields.
- When a source 404s or is paywalled, add an accessible mirror in `archived` (e.g., Wayback).
- Use `tools/archive_link.py` to create new archives when needed.

## Development workflow
0. Before starting, sync with the latest main branch:
   - `git pull --ff-only origin main`
1. Modify source files (`timeline/*.yaml`, `posts/*.md`, etc.).
2. Rebuild derived files (footnotes) if relevant:
   - `python scripts/build_footnotes.py`
3. Run tests:
   - `pytest -q`
   - `python scripts/link_check.py --csv link_check.csv`
4. Commit changes and open a PR summarizing updates.

