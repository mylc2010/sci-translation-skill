import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from check_glossary_gate import check_gate, fingerprint


ROOT = Path(__file__).resolve().parents[1]
SOURCE = "摘要、正文、图表和附录的完整文本。".encode("utf-8")


class GlossaryGateTests(unittest.TestCase):
    def glossary(self):
        glossary = json.loads((ROOT / "examples/terminology-glossary.sample.json").read_text(encoding="utf-8"))
        for term in glossary["terms"]:
            term["status"] = "author_confirmed"
            term["evidence"] = [{"kind": "author", "locator": "reviewed table row", "note": "Approved by author"}]
        glossary["approval"] = {
            "status": "approved",
            "glossary_version": glossary["version"],
            "author_reference": "author message confirming terminology-review.md",
            **fingerprint(glossary, SOURCE),
        }
        return glossary

    def test_approved_table_is_ready(self):
        self.assertEqual(check_gate(self.glossary(), SOURCE), [])

    def test_pending_review_blocks_translation(self):
        glossary = self.glossary()
        glossary["approval"]["status"] = "pending"
        self.assertTrue(check_gate(glossary, SOURCE))

    def test_unapproved_term_blocks_translation(self):
        glossary = self.glossary()
        glossary["terms"][0]["status"] = "provisional"
        glossary["approval"].update(fingerprint(glossary, SOURCE))
        self.assertTrue(any("Unapproved term" in issue for issue in check_gate(glossary, SOURCE)))

    def test_source_or_term_change_invalidates_lock(self):
        glossary = self.glossary()
        self.assertTrue(any("source_sha256" in issue for issue in check_gate(glossary, SOURCE + b"changed")))
        glossary["terms"][0]["canonical"] = "new name"
        self.assertTrue(any("terms_sha256" in issue for issue in check_gate(glossary, SOURCE)))

    def test_expansion_must_be_approved_and_unique(self):
        glossary = self.glossary()
        glossary["terms"][0].update({"abbreviation": "RAG", "full_form": "Retrieval-Augmented Generation", "allowed_forms": ["RAG", "Retrieval-Augmented Generation"]})
        glossary["terms"][1].update({"abbreviation": "RAG", "full_form": "Different Expansion", "allowed_forms": ["RAG", "Different Expansion"]})
        glossary["approval"].update(fingerprint(glossary, SOURCE))
        self.assertTrue(any("Conflicting expansion" in issue for issue in check_gate(glossary, SOURCE)))

    def test_incomplete_expansion_blocks_translation(self):
        glossary = self.glossary()
        glossary["terms"][0]["abbreviation"] = "RAG"
        glossary["approval"].update(fingerprint(glossary, SOURCE))
        self.assertTrue(any("Incomplete abbreviation" in issue for issue in check_gate(glossary, SOURCE)))

    def test_approval_needs_author_reference(self):
        glossary = self.glossary()
        glossary["approval"]["author_reference"] = ""
        self.assertTrue(any("author confirmation" in issue for issue in check_gate(glossary, SOURCE)))

    def test_cli_reports_ready_and_blocks_missing_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            source = folder / "source.txt"
            glossary_path = folder / "glossary.json"
            source.write_bytes(SOURCE)
            glossary = self.glossary()
            glossary_path.write_text(json.dumps(glossary), encoding="utf-8")
            command = [sys.executable, str(ROOT / "scripts/check_glossary_gate.py"), str(glossary_path), "--source", str(source)]
            ready = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(ready.returncode, 0)
            self.assertEqual(json.loads(ready.stdout)["status"], "ready")
            glossary["approval"]["status"] = "pending"
            glossary_path.write_text(json.dumps(glossary), encoding="utf-8")
            blocked = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(blocked.returncode, 1)
            self.assertEqual(json.loads(blocked.stdout)["issues"], ["Author review has not approved this glossary"])
            fingerprints = subprocess.run(command + ["--fingerprint"], capture_output=True, text=True)
            self.assertEqual(fingerprints.returncode, 0)
            self.assertEqual(json.loads(fingerprints.stdout), fingerprint(glossary, SOURCE))


if __name__ == "__main__":
    unittest.main(verbosity=2)
