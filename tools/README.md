# Tools

## cite_from_post.py
Scan posts for `{{cite:ID}}` tokens and generate a numbered footnotes block per post from timeline cards.

**Usage**
```bash
python tools/cite_from_post.py --all
# or
python tools/cite_from_post.py --post posts/post-03.md
```
Outputs to `posts/_footnotes/<post>.md`.

Token formats:
- `{{cite:2025-06-12_la_deployment_tro}}`
- `{{cite:2025-06-12_la_deployment_tro, 2025-02-21_treasury_doge_pi}}`

It prefers the first `links`/`sources` URL and appends `court_meta` if present.

## dockets_tool.py
Export a to-do of cards missing docket/judge, or apply updates from a CSV.

**Export missing**
```bash
python tools/dockets_tool.py export-missing
# writes tools/dockets_to_fill.csv
```

**Apply updates**
1) Edit `tools/dockets_updates.csv` (seeded with verified cases).
2) Run:
```bash
python tools/dockets_tool.py apply-updates
```

This patches `timeline/*.yaml` in-place (only the `court_meta` and `links` fields).
