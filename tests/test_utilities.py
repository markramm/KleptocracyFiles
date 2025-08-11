import subprocess, sys, pathlib

sys.path.append(str(pathlib.Path("scripts").resolve()))
from link_check import check_url  # noqa: E402
from pathlib import Path


def test_build_footnotes_handles_archived_citations():
    out = subprocess.check_output(
        [sys.executable, "scripts/build_footnotes.py", "--ids", "2023-06-02-youtube-election-policy"],
        text=True,
    )
    assert "webcache.googleusercontent.com" in out or "web.archive.org" in out


def test_link_check_fallback_get():
    status, _ = check_url(
        "https://www.theverge.com/2023/3/27/23659351/elon-musk-twitter-for-you-verified-accounts-polls"
    )
    assert status == 200


def test_viewer_references_index():
    html = Path("viewer/index.html").read_text(encoding="utf-8")
    assert "timeline/index.json" in html
