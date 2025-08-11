# Kleptocracy Files – Agent Guide

## Generated artifacts
- `timeline/index.json` – built from individual YAML items via `scripts/build_timeline_index.py`.
- Footnote pages in `posts/` – build with `scripts/build_footnotes.py`.
- Link report – run `python scripts/link_check.py --csv link_check.csv`.

## Archiving citations
- Timeline YAML `citations` entries may specify `url` and optional `archived` fields.
- When a source 404s or is paywalled, add an accessible mirror in `archived` (e.g., Wayback).
- Use `tools/archive_link.py` to create new archives when needed.

## Development workflow
0. Before starting, sync with the latest main branch:
 - `git pull --ff-only origin main`
 - The repository uses LF line endings; configure your editor to preserve them to avoid whitespace-only merge conflicts. An `.editorconfig` file is provided to help enforce this.
1. Modify source files (`timeline/*.yaml`, `posts/*.md`, etc.).
2. Rebuild derived files (timeline index, footnotes) if relevant.
3. Run linters and tests:
   - `python scripts/check_whitespace.py`
   - `pytest -q`
   - `python scripts/link_check.py --csv link_check.csv`
4. Commit changes and open a PR summarizing updates.

