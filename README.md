# Kleptocracy Files

This repository houses research into the possibility of kleptocratic capture in the United States. It organizes public source material into a searchable timeline, narrative posts, and a casebook of primary documents.

## Repository layout
- `timeline/` – `.yaml` event files with metadata, tags, and source citations.
- `posts/` – Narrative essays and playbooks that expand on timeline events.
- `casebook/` – Tools and data for ingesting and cataloging primary source PDFs.
- `scripts/` – Maintenance scripts and quality-assurance reports.

## Getting Started
1. Browse the `timeline/` directory for chronological event files.
2. Read essays in `posts/` for thematic analysis.
3. Review `PROJECT_EVAL.md` for project status and open questions.

## Interactive timeline viewer
The static viewer in `viewer/` fetches `timeline/index.json`, which is generated during the GitHub Pages workflow and not stored in the repository. The workflow publishes the latest files so the timeline can be browsed at `https://<user>.github.io/KleptocracyFiles/viewer/` once Pages is enabled. To preview locally without CORS issues, run `python scripts/build_timeline_index.py` and serve the repository with a simple HTTP server such as `python -m http.server`, then open `http://localhost:8000/viewer/`.

## Changelog
- 2025-08-11: Added Posts #3 and #4
