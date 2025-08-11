import os
import json
import shutil
import tempfile
import unittest
import importlib.util
import yaml
import pathlib
import io
import sys
from contextlib import redirect_stdout
from unittest import mock


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS = os.path.join(REPO_ROOT, "scripts")
TOOLS = os.path.join(REPO_ROOT, "tools")


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class YamlExtensionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="yaml_ext_")
        self.timeline = os.path.join(self.tmp, "timeline")
        os.makedirs(self.timeline, exist_ok=True)

        event = {
            "id": "evt",
            "date": "2025-01-01",
            "title": "Event",
            "citations": ["http://example.com"],
            "sources": [{"url": "http://example.com/doc.pdf", "title": "Doc"}],
        }
        with open(os.path.join(self.timeline, "a.yaml"), "w", encoding="utf-8") as f:
            yaml.safe_dump(event, f)
        with open(os.path.join(self.timeline, "b.yml"), "w", encoding="utf-8") as f:
            yaml.safe_dump(event, f)

        self.link_check = load_module("link_check", os.path.join(SCRIPTS, "link_check.py"))
        self.build_footnotes = load_module("build_footnotes", os.path.join(SCRIPTS, "build_footnotes.py"))
        self.build_casebook = load_module("build_casebook", os.path.join(TOOLS, "build_casebook.py"))

        self.link_check.TIMELINE = pathlib.Path(self.timeline)
        self.build_footnotes.TIMELINE = pathlib.Path(self.timeline)
        self.build_casebook.TIMELINE = self.timeline

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_build_footnotes_loads_all_extensions(self):
        events = self.build_footnotes.load_events()
        names = sorted(e["_file"] for e in events)
        self.assertEqual(names, ["a.yaml", "b.yml"])

    def test_link_check_processes_all_extensions(self):
        self.link_check.check_url = lambda url, timeout=12: (200, None)
        buf = io.StringIO()
        with redirect_stdout(buf):
            with mock.patch.object(sys, "argv", ["link_check"]):
                self.link_check.main()
        lines = [json.loads(l) for l in buf.getvalue().splitlines() if l.startswith("{")]
        files = sorted({l["file"] for l in lines})
        self.assertEqual(files, ["a.yaml", "b.yml"])

    def test_build_casebook_iterates_all_extensions(self):
        cards = list(self.build_casebook.iter_cards())
        names = sorted(os.path.basename(p) for p, _ in cards)
        self.assertEqual(names, ["a.yaml", "b.yml"])


if __name__ == "__main__":
    unittest.main()

