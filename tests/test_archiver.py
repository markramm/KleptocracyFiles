import os, shutil, yaml, unittest, importlib.util, tempfile, hashlib

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TOOLS = os.path.join(REPO_ROOT, "tools")

def load_module():
    spec = importlib.util.spec_from_file_location("archive_link", os.path.join(TOOLS, "archive_link.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

class ArchiverDedupeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="archiver_test_")
        self.timeline = os.path.join(self.tmp, "timeline")
        self.archives = os.path.join(self.tmp, "archives")
        self.casebook = os.path.join(self.tmp, "casebook")
        os.makedirs(self.timeline, exist_ok=True)

        self.mod = load_module()

        # monkeypatch fetch
        def fake_fetch(url, timeout=30):
            if url.endswith(".pdf"):
                content = b"%PDF-1.4\\n%MINI PDF\\n%%EOF\\n"
                return {"status_code":200,"final_url":url,"content_type":"application/pdf","content":content}
            else:
                html = (b"<!doctype html><html><body>same content</body></html>")
                return {"status_code":200,"final_url":url,"content_type":"text/html","content":html}
        self.mod.fetch = fake_fetch

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write_event(self, id_, date, title, url=None, order_url=None):
        y = {"id": id_, "date": date, "title": title, "status":"confirmed"}
        if url:
            y["links"] = [{"title":"A","url":url}]
        if order_url:
            y["court_meta"] = {"docket":"1:25-cv-1","court":"D.D.C.","order_url":order_url}
        p = os.path.join(self.timeline, f"{id_}.yaml")
        with open(p, "w", encoding="utf-8") as f: yaml.safe_dump(y, f, sort_keys=False)
        return p

    def read_yaml(self, path):
        return yaml.safe_load(open(path, "r", encoding="utf-8"))

    def test_general_dedupe(self):
        p1 = self.write_event("2025-08-01_evt1","2025-08-01","E1",url="https://x/a.html")
        p2 = self.write_event("2025-08-02_evt2","2025-08-02","E2",url="https://y/b.html")

        # First run
        self.mod.update_timeline_file(p1, self.archives, self.casebook, court_only=False, sleep=0.0)
        y1 = self.read_yaml(p1)
        f1 = y1["links"][0]["archive_file"]
        sha1 = y1["links"][0]["archive_sha256"]

        # Second run, different URL but same content => should reuse same file
        self.mod.update_timeline_file(p2, self.archives, self.casebook, court_only=False, sleep=0.0)
        y2 = self.read_yaml(p2)
        f2 = y2["links"][0]["archive_file"]
        sha2 = y2["links"][0]["archive_sha256"]

        self.assertEqual(sha1, sha2)
        self.assertEqual(f1, f2)

        # Only one file in archives with that sha
        files = [fn for fn in os.listdir(self.archives) if fn.startswith(sha1)]
        self.assertEqual(len(files), 2, "Expect blob and sidecar YAML")  # content + metadata

    def test_court_dedupe(self):
        p1 = self.write_event("2025-08-03_evt3","2025-08-03","E3",order_url="https://x/order.pdf")
        p2 = self.write_event("2025-08-04_evt4","2025-08-04","E4",order_url="https://y/another.pdf")

        self.mod.update_timeline_file(p1, self.archives, self.casebook, court_only=True, sleep=0.0)
        y1 = self.read_yaml(p1)
        f1 = y1["court_meta"]["order_file"]
        sha1 = y1["court_meta"]["sha256"]

        self.mod.update_timeline_file(p2, self.archives, self.casebook, court_only=True, sleep=0.0)
        y2 = self.read_yaml(p2)
        f2 = y2["court_meta"]["order_file"]
        sha2 = y2["court_meta"]["sha256"]

        self.assertEqual(sha1, sha2)
        self.assertEqual(f1, f2)

        files = [fn for fn in os.listdir(self.casebook) if fn.startswith(sha1)]
        self.assertEqual(len(files), 2, "Expect PDF and sidecar YAML")

if __name__ == "__main__":
    unittest.main(verbosity=2)
