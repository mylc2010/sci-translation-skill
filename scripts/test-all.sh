#!/bin/bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
bash "$root/skills/sci-translation/references/test-skill-integrity.sh"
PYTHONDONTWRITEBYTECODE=1 python3 "$root/skills/academic-humanizer/tests/test_skill_contract.py"
cmp "$root/shared/terminology-interchange.md" "$root/skills/sci-translation/references/glossary-interchange.md"
cmp "$root/shared/terminology-interchange.md" "$root/skills/academic-humanizer/references/glossary-interchange.md"
echo 'Both standalone skills and the terminology contract passed structural checks.'
