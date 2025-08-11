# TODO

Outstanding tasks for Kleptocracy Files repository.

 - [x] Merge duplicate timeline events (e.g., 2023-03-27, 2023-06-02, 2023-08-29, 2024-02-09, 2025-02-11, 2025-06-07) into single canonical files and ensure each uses a unique, canonical ID.
- [x] Standardize timeline file extensions to `.yaml`.
- [x] Restore `archive_link` module.
- [x] Refactor `scripts/build_timeline_index.py` to parse events with `yaml.safe_load`.
- [x] Fix `scripts/build_footnotes.py` (indentation bug; ensure it processes both `.yaml` and `.yml`) and ensure link/footnote utilities process all timeline files.
- [x] Expand archival coverage by adding archived URLs for cited sources.
- [x] Investigate paywalled or broken links and replace them with accessible mirrors where possible.
- [x] Refresh `ARCHIVE_QA.md` and link-check outputs and ensure all posts include `Filed:` footers.
 - [x] Restore interactive viewer runtime for `viewer/index.html` so the timeline can be browsed.
- [x] Expand test coverage for utilities (footnotes builder, link checker, timeline index, viewer).
