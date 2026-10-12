#!/bin/bash
set -euo pipefail
skill_dir="$(cd "$(dirname "$0")/.." && pwd)"
python3 - "$skill_dir" <<'PY'
import json
from pathlib import Path
import re
import sys

root = Path(sys.argv[1])
required = ["SKILL.md", "README.md", "README_EN.md", "scripts/audit_translation.py", "scripts/test_audit_translation.py", "examples/terminology-glossary.sample.json"]
for name in required:
    if not (root / name).is_file():
        raise SystemExit(f"Missing resource: {name}")
for document in root.rglob("*.md"):
    for link in re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
        if "://" not in link and not link.startswith("#"):
            if not (document.parent / link.split("#")[0]).exists():
                raise SystemExit(f"Broken local link: {document.name}: {link}")
json.loads((root / "examples/terminology-glossary.sample.json").read_text(encoding="utf-8"))
print("Resource/link checks passed; this is not a translation quality verdict.")
PY
PYTHONDONTWRITEBYTECODE=1 python3 "$skill_dir/scripts/test_audit_translation.py"
