import os, json, shutil, tempfile, unittest, importlib.util, hashlib, yaml

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS = os.path.join(REPO_ROOT, "scripts")


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TimelineIndexTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="index_")
        self.timeline = os.path.join(self.tmp, "timeline")
        os.makedirs(self.timeline, exist_ok=True)

        with open(os.path.join(self.timeline, "a.yaml"), "w", encoding="utf-8") as f:
            yaml.safe_dump({"id": "evt1", "date": "2025-01-01", "title": "A"}, f)
        with open(os.path.join(self.timeline, "b.yml"), "w", encoding="utf-8") as f:
            yaml.safe_dump({"id": "evt2", "date": "2025-01-02", "title": "B"}, f)
        with open(os.path.join(self.timeline, "c.yaml"), "w", encoding="utf-8") as f:
            yaml.safe_dump(
                {
                    "id": "evt3",
                    "date": "2025-01-03",
                    "title": "C",
                    "sources": [{"url": "https://example.com"}],
                },
                f,
            )

        self.mod = load_module("build_timeline_index", os.path.join(SCRIPTS, "build_timeline_index.py"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_build_index_with_yaml_safe_load(self):
        out_json = os.path.join(self.tmp, "index.json")
        self.mod.main(self.timeline, out_json)
        data = json.load(open(out_json, "r", encoding="utf-8"))
        files = sorted(e["_file"] for e in data["events"])
        self.assertEqual(files, ["a.yaml", "b.yml", "c.yaml"])
        hashes = {e["_file"]: e["_id_hash"] for e in data["events"]}
        self.assertEqual(hashes["a.yaml"], hashlib.sha256("evt1".encode("utf-8")).hexdigest())
        self.assertEqual(hashes["b.yml"], hashlib.sha256("evt2".encode("utf-8")).hexdigest())
        self.assertEqual(hashes["c.yaml"], hashlib.sha256("evt3".encode("utf-8")).hexdigest())
        c_event = next(e for e in data["events"] if e["_file"] == "c.yaml")
        self.assertEqual(c_event["citations"], [{"url": "https://example.com"}])
        for ev in data["events"]:
            self.assertIn("tags", ev)
            self.assertIsInstance(ev["tags"], list)

if __name__ == "__main__":
    unittest.main()
