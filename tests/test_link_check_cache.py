import json
import sys
from datetime import datetime, UTC
from pathlib import Path
import importlib.util


spec = importlib.util.spec_from_file_location(
    "link_check", Path(__file__).resolve().parents[1] / "scripts" / "link_check.py"
)
lc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lc)


def test_link_check_uses_cache(monkeypatch, tmp_path, capsys):
    timeline = tmp_path / "timeline"
    timeline.mkdir()
    url = "https://example.com"
    (timeline / "e.yaml").write_text(f"citations:\n- {url}\n", encoding="utf-8")
    log_path = tmp_path / "link_status.json"
    log_data = {
        url: {
            "target": url,
            "status": 200,
            "info": None,
            "checked_at": datetime.now(UTC).isoformat(),
        }
    }
    log_path.write_text(json.dumps(log_data))

    monkeypatch.setattr(lc, "REPO", tmp_path)
    monkeypatch.setattr(lc, "TIMELINE", timeline)
    monkeypatch.setattr(lc, "STATUS_LOG", log_path)

    called = False

    def fake_check(url, timeout=12):
        nonlocal called
        called = True
        return 500, "fail"

    monkeypatch.setattr(lc, "check_url", fake_check)
    monkeypatch.setattr(sys, "argv", ["link_check.py"])
    lc.main()

    assert not called

