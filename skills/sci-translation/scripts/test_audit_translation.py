import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from audit_translation import audit, validate_glossary

ROOT = Path(__file__).resolve().parents[1]


class AuditTests(unittest.TestCase):
    def glossary(self):
        return json.loads((ROOT / "examples/terminology-glossary.sample.json").read_text(encoding="utf-8"))

    def checks(self, source, target, **kwargs):
        return {item["check"] for item in audit(source, target, **kwargs)["findings"]}

    def test_numbers_change_is_detected(self):
        self.assertIn("numeric_sequence", self.checks(r"开销4.2\%", r"Overhead 42\%"))

    def test_inline_math_content_is_protected(self):
        self.assertIn("math_content", self.checks(r"满足 $x_i < 1$", r"Satisfies $X_j > 9$"))

    def test_display_math_content_is_protected(self):
        self.assertIn("math_content", self.checks(r"\begin{align}x=1\end{align}", r"\begin{align}y=1\end{align}"))

    def test_added_citation_is_detected(self):
        self.assertIn("protected_commands", self.checks(r"\cite{a}", r"\cite{a}\cite{b}"))

    def test_duplicate_citation_loss_is_detected(self):
        self.assertIn("protected_commands", self.checks(r"\cite{a}\cite{a}", r"\cite{a}"))

    def test_optional_citation_argument_is_protected(self):
        self.assertIn("protected_commands", self.checks(r"\citep[see][p.~2]{a}", r"\citep[see][p.~3]{a}"))

    def test_changed_reference_is_detected(self):
        self.assertIn("protected_commands", self.checks(r"\ref{fig:a}", r"\ref{fig:b}"))

    def test_custom_macro_loss_is_detected(self):
        self.assertIn("latex_command_counts", self.checks(r"\PARAG 系统", "PA-RAG system"))

    def test_empty_target_is_not_passed(self):
        self.assertIn("empty_target", self.checks("方法可能有效。", ""))

    def test_heading_loss_is_detected(self):
        self.assertIn("heading_sequence", self.checks("# 方法\n文字", "Text"))

    def test_deleted_latex_table_row_is_detected(self):
        source = r"\begin{tabular}{cc}甲 & 乙 \\ 丙 & 丁 \\ \end{tabular}"
        target = r"\begin{tabular}{cc}A & B \\ \end{tabular}"
        self.assertIn("table_shape", self.checks(source, target))

    def test_markdown_column_loss_is_detected(self):
        source = "|甲|乙|\n|---|---|\n|好|好|"
        target = "|A|\n|---|\n|good|"
        self.assertIn("table_shape", self.checks(source, target))

    def test_glossary_rejects_missing_canonical(self):
        data = self.glossary()
        del data["terms"][0]["canonical"]
        with self.assertRaises(ValueError):
            validate_glossary(data)

    def test_glossary_rejects_empty_terms(self):
        data = self.glossary()
        data["terms"] = []
        with self.assertRaises(ValueError):
            validate_glossary(data)

    def test_legacy_schema_requires_explicit_migration(self):
        with self.assertRaises(ValueError):
            validate_glossary({"terms": [{"term_en": "decapsulation"}]})

    def test_false_verified_entry_rejected_without_evidence(self):
        data = self.glossary()
        data["terms"][0]["status"] = "verified"
        with self.assertRaises(ValueError):
            validate_glossary(data)

    def test_scoped_term_allows_payload_decryption_in_same_sentence(self):
        source = "用户解封装数据密钥，然后进行载荷解密。"
        target = "The user decapsulates the data key and then performs payload decryption."
        alignment = {"segments": [{"id": "p1", "source": source, "target": target, "term_uses": [{"concept_id": "kem.decapsulation", "source_start": 2, "source_span": "解封装", "target_start": 9, "target_span": "decapsulates"}]}]}
        report = audit(source, target, self.glossary(), alignment)
        self.assertEqual(report["findings"], [])
        self.assertEqual(report["coverage"]["term_uses_checked"], 1)

    def test_unapproved_translation_detected_without_blacklist(self):
        source, target = "用户解封装。", "The user performs packet recovery."
        alignment = {"segments": [{"id": "p1", "source": source, "target": target, "term_uses": [{"concept_id": "kem.decapsulation", "source_start": 2, "source_span": "解封装", "target_start": 18, "target_span": "packet recovery"}]}]}
        self.assertIn("term_form_not_approved", self.checks(source, target, glossary=self.glossary(), alignment=alignment))

    def test_missing_alignment_is_not_terminology_success(self):
        report = audit("解封装", "packet recovery", self.glossary())
        self.assertEqual(report["coverage"]["term_uses_checked"], 0)
        self.assertTrue(any("NOT established" in item for item in report["warnings"]))

    def test_alignment_incomplete_is_detected(self):
        alignment = {"segments": [{"id": "p1", "source": "甲", "target": "A"}]}
        self.assertIn("alignment_coverage", self.checks("甲乙", "AB", alignment=alignment))

    def test_local_citation_swap_is_detected(self):
        source = r"甲\cite{a}。" + "\n" + r"乙\cite{b}。"
        target = r"A\cite{b}." + "\n" + r"B\cite{a}."
        alignment = {"segments": [
            {"id": "p1", "source": r"甲\cite{a}。", "target": r"A\cite{b}."},
            {"id": "p2", "source": r"乙\cite{b}。", "target": r"B\cite{a}."}
        ]}
        report = audit(source, target, alignment=alignment)
        self.assertTrue(any(item["check"] == "protected_commands" and item["location"] == "p1" for item in report["findings"]))

    def test_marker_requires_author_review(self):
        self.assertIn("unresolved_marker", self.checks("术语", "[?term]"))

    def test_semantic_blind_spot_is_explicit(self):
        report = audit("可能有效。", "It is guaranteed to work.")
        self.assertTrue(report["semantic_review_required"])
        self.assertNotIn("publication_ready", report)

    def test_cli_missing_glossary_is_invalid_input(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            (folder / "source.txt").write_text("原文", encoding="utf-8")
            (folder / "target.txt").write_text("Source", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/audit_translation.py"), str(folder / "source.txt"), str(folder / "target.txt"), "--glossary", str(folder / "missing.json")],
                capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["status"], "invalid_input")

    def test_cli_malformed_glossary_is_invalid_input(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            for filename, content in (("source.txt", "原文"), ("target.txt", "Source"), ("bad.json", "{")):
                (folder / filename).write_text(content, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/audit_translation.py"), str(folder / "source.txt"), str(folder / "target.txt"), "--glossary", str(folder / "bad.json")],
                capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 2)

    def test_null_cli_inputs_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            for filename, content in (("source.txt", "原文"), ("target.txt", "Source"), ("null.json", "null")):
                (folder / filename).write_text(content, encoding="utf-8")
            for option in ("--glossary", "--alignment"):
                result = subprocess.run(
                    [sys.executable, str(ROOT / "scripts/audit_translation.py"), str(folder / "source.txt"), str(folder / "target.txt"), option, str(folder / "null.json")],
                    capture_output=True, text=True
                )
                self.assertEqual(result.returncode, 2)

    def test_table_last_row_without_terminator_is_checked(self):
        source = r"\begin{tabular}{cc}甲 & 乙 \\ 丙 & 丁 \bottomrule\end{tabular}"
        target = r"\begin{tabular}{cc}A & B \\ \bottomrule\end{tabular}"
        self.assertIn("table_shape", self.checks(source, target))

    def test_table_trailing_rule_is_not_a_data_row(self):
        source = r"\begin{tabular}{cc}甲 & 乙 \\ 丙 & 丁 \\ \bottomrule\end{tabular}"
        target = r"\begin{tabular}{cc}A & B \\ C & D \bottomrule\end{tabular}"
        self.assertNotIn("table_shape", self.checks(source, target))

    def test_unicode_minus_cannot_be_lost(self):
        self.assertIn("numeric_sequence", self.checks("−5 °C", "5 °C"))
        self.assertNotIn("numeric_sequence", self.checks("−5 °C", "-5 °C"))

    def test_range_reference_second_endpoint_is_protected(self):
        self.assertIn("protected_commands", self.checks(r"\crefrange{fig:start}{fig:end}", r"\crefrange{fig:start}{fig:wrong}"))

    def test_range_reference_allows_inter_argument_whitespace(self):
        for whitespace in (" ", "\n"):
            source = r"\crefrange{fig:start}" + whitespace + "{fig:end}"
            for target in (r"\crefrange{fig:start}" + whitespace + "{fig:wrong}", r"\crefrange{fig:wrong}" + whitespace + "{fig:end}"):
                self.assertIn("protected_commands", self.checks(source, target))

    def test_reused_term_position_is_rejected(self):
        source, target = "解封装，再解封装。", "First, decapsulate; second, decrypt."
        uses = [
            {"concept_id": "kem.decapsulation", "source_start": 0, "source_span": "解封装", "target_start": 7, "target_span": "decapsulate"},
            {"concept_id": "kem.decapsulation", "source_start": 5, "source_span": "解封装", "target_start": 7, "target_span": "decapsulate"}
        ]
        report = audit(source, target, self.glossary(), {"segments": [{"id": "p1", "source": source, "target": target, "term_uses": uses}]})
        self.assertTrue(any(item["check"] == "term_span_reused" for item in report["findings"]))
        self.assertEqual(report["coverage"]["term_uses_checked"], 1)

    def test_term_substring_cannot_fake_approved_form(self):
        source, target = "文档分片", "chunking"
        uses = [{"concept_id": "rag.chunk", "source_start": 0, "source_span": source, "target_start": 0, "target_span": "chunk"}]
        self.assertIn("term_target_unanchored", self.checks(source, target, glossary=self.glossary(), alignment={"segments": [{"id": "p1", "source": source, "target": target, "term_uses": uses}]}))


if __name__ == "__main__":
    unittest.main(verbosity=2)
