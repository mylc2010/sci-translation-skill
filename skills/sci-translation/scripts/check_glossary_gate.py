import argparse
import hashlib
import json
from pathlib import Path
import sys

from audit_translation import validate_glossary


def fingerprint(glossary, source_bytes):
    approved_content = {key: glossary[key] for key in ("project", "version", "terms")}
    serialized = json.dumps(approved_content, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "terms_sha256": hashlib.sha256(serialized.encode("utf-8")).hexdigest(),
        "approved_term_count": len(glossary["terms"]),
    }


def check_gate(glossary, source_bytes):
    validate_glossary(glossary)
    expected = fingerprint(glossary, source_bytes)
    approval = glossary.get("approval")
    issues = []
    approved = isinstance(approval, dict) and approval.get("status") == "approved"
    if not approved:
        issues.append("Author review has not approved this glossary")
    else:
        if approval.get("glossary_version") != glossary["version"]:
            issues.append("Approval does not match glossary version")
        for field, value in expected.items():
            if approval.get(field) != value:
                issues.append(f"Approval does not match {field}")
        if not isinstance(approval.get("author_reference"), str) or not approval["author_reference"].strip():
            issues.append("Approval needs an explicit author confirmation reference")

    abbreviations = {}
    for term in glossary["terms"]:
        concept_id = term["concept_id"]
        if term["status"] == "provisional":
            issues.append(f"Unapproved term: {concept_id}")
        short = term.get("abbreviation")
        full = term.get("full_form")
        if short is not None or full is not None:
            if not all(isinstance(value, str) and value.strip() for value in (short, full)):
                issues.append(f"Incomplete abbreviation/full form: {concept_id}")
                continue
            approved_forms = {term["canonical"], *term["allowed_forms"]}
            if short not in approved_forms or full not in approved_forms:
                issues.append(f"Abbreviation and full form must both be approved forms: {concept_id}")
            previous = abbreviations.setdefault(short.casefold(), full.casefold())
            if previous != full.casefold():
                issues.append(f"Conflicting expansion for abbreviation: {short}")
    return issues


def main():
    parser = argparse.ArgumentParser(description="Check author-approved, source-bound terminology before translation")
    parser.add_argument("glossary", type=Path)
    parser.add_argument("--source", required=True, type=Path, help="Complete reviewed source-text snapshot")
    parser.add_argument("--fingerprint", action="store_true", help="Print hashes for the author-approved lock record")
    args = parser.parse_args()
    try:
        glossary = json.loads(args.glossary.read_text(encoding="utf-8"))
        source_bytes = args.source.read_bytes()
        validate_glossary(glossary)
        result = fingerprint(glossary, source_bytes) if args.fingerprint else check_gate(glossary, source_bytes)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, KeyError) as error:
        print(json.dumps({"status": "invalid_input", "error": str(error)}, ensure_ascii=False))
        return 2
    if args.fingerprint:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    status = "ready" if not result else "blocked"
    print(json.dumps({"status": status, "issues": result}, ensure_ascii=False, indent=2))
    return 0 if status == "ready" else 1


if __name__ == "__main__":
    sys.exit(main())
