# TODO

Outstanding tasks for Kleptocracy Files repository.

- [ ] Merge duplicate timeline events (e.g., 2023-03-27, 2023-06-02, 2023-08-29, 2024-02-09) into single canonical files and ensure each uses a unique, canonical ID.
- [x] Standardize timeline file extensions to `.yaml`.
- [x] Restore `archive_link` module.
- [ ] Refactor `scripts/build_timeline_index.py` to parse events with `yaml.safe_load`.
- [ ] Fix `scripts/build_footnotes.py` and ensure link/footnote utilities process all timeline files.
- [ ] Expand archival coverage by adding archived URLs for cited sources.
- [ ] Investigate paywalled or broken links and replace them with accessible mirrors where possible.
- [ ] Audit posts that cite sources directly without timeline events; create corresponding timeline entries and update posts to reference them.
- [ ] Refresh `ARCHIVE_QA.md` and link-check outputs and ensure all posts include `Filed:` footers.
- [ ] Expand test coverage for utilities (footnotes builder, link checker, timeline index).
