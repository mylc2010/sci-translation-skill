#!/bin/bash
set -euo pipefail
skill_dir="$(cd "$(dirname "$0")/.." && pwd)"
if [[ $# -lt 2 || $# -gt 3 ]]; then
    printf 'Usage: bash %s source target [glossary.json]\nFor alignment and JSON output, use scripts/audit_translation.py directly.\n' "$0" >&2
    exit 2
fi
source_file="$1"
target_file="$2"
shift 2
if [[ $# -eq 1 ]]; then
    exec python3 "$skill_dir/scripts/audit_translation.py" "$source_file" "$target_file" --glossary "$1"
fi
exec python3 "$skill_dir/scripts/audit_translation.py" "$source_file" "$target_file"
