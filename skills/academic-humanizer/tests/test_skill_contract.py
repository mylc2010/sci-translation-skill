import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ContractTests(unittest.TestCase):
    def test_entrypoint_and_self_contained_references(self):
        entry = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        self.assertRegex(entry, r'(?m)^name: academic-humanizer$')
        for relative in re.findall(r'\]\(([^)]+)\)', entry):
            if not relative.startswith(('https://', 'http://', '#')):
                self.assertTrue((ROOT / relative).is_file(), relative)

    def test_complete_original_framework_and_license(self):
        framework = (ROOT / 'references/upstream-humanizer.md').read_text(encoding='utf-8')
        self.assertEqual([int(item) for item in re.findall(r'^### (\d+)\.', framework, re.M)], list(range(1, 27)))
        self.assertIn('Copyright (c) 2025 Siqi Chen', (ROOT / 'HUMANIZER-LICENSE').read_text(encoding='utf-8'))

    def test_report_scope_and_author_gate(self):
        entry = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        for expected in ['Stop for explicit author approval', 'never duplicate a sentence',
                         'figures, figure captions, tables, table captions',
                         'preserve every inline formula and macro exactly',
                         'Do not weaken or strengthen a claim', 'authoritative decision source',
                         'light red background', 'light green background', 'never fuzzy-replace ambiguous matches']:
            self.assertIn(expected, entry)

    def test_no_implicit_final_claim(self):
        entry = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('otherwise deliver a clearly labeled partial file', entry)
        self.assertIn('no detection outcome is guaranteed', entry)


if __name__ == '__main__':
    unittest.main()
