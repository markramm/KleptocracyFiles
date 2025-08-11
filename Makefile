# Debugging Democracy — helper targets

PY := python

# Build footnotes for a date range:
# Usage: make footnotes START=2024-06-01 END=2024-06-30 OUT=posts/footnotes-june.md
footnotes:
	@if [ -z "$(START)" ] || [ -z "$(END)" ]; then echo "Usage: make footnotes START=YYYY-MM-DD END=YYYY-MM-DD OUT=posts/footnotes.md"; exit 1; fi
	$(PY) scripts/build_footnotes.py --start $(START) --end $(END) -o $(OUT)

# Link checker (HEAD requests). Example: make lint-links LIMIT=50 CSV=link-report.csv
lint-links:
	$(PY) scripts/link_check.py --limit $(LIMIT) --csv $(CSV)

# Render a post to PDF via pandoc (requires pandoc + wkhtmltopdf or equivalent installed locally)
# Usage: make pdf POST=posts/01-when-the-infrastructure-layer-gets-compromised.md OUT=out.pdf
pdf:
	@if [ -z "$(POST)" ] || [ -z "$(OUT)" ]; then echo "Usage: make pdf POST=posts/file.md OUT=out.pdf"; exit 1; fi
	pandoc $(POST) -o $(OUT) --from=gfm --pdf-engine=wkhtmltopdf --metadata title="Debugging Democracy"

.PHONY: footnotes lint-links pdf
