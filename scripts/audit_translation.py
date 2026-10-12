import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys

SCHEMA_VERSION = "2.0"
PROTECTED = re.compile(
    r"\\[cC]refrange\*?\s*(?:\[[^\]]*\]\s*)*\{[^{}]*\}\s*\{[^{}]*\}"
    r"|\\(?:cite[a-zA-Z]*|[cC]ref|ref|eqref|autoref|pageref|label)\*?"
    r"(?:\[[^\]]*\])*\{[^{}]*\}"
)
MATH = re.compile(
    r"(?<!\\)\$\$[\s\S]*?(?<!\\)\$\$|(?<!\\)\$(?!\$)[\s\S]*?(?<!\\)\$"
    r"|\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\]"
    r"|\\begin\{(?P<env>equation\*?|align\*?|gather\*?|multline\*?|displaymath)\}"
    r"[\s\S]*?\\end\{(?P=env)\}"
)
NUMBER = re.compile(r"(?<![A-Za-z0-9_])[-+]?(?:\d+(?:\.\d+)?|\.\d+)(?:[eE][-+]?\d+)?")
COMMAND = re.compile(r"\\[A-Za-z]+")
ENVIRONMENT = re.compile(r"\\(?:begin|end)\{[^{}]+\}")
HEADING = re.compile(r"^#{1,6}(?=\s)|\\(?:subsubsection|subsection|section|chapter|part)\*?", re.M)
LIMITS = [
    "Heuristic text checks, not a full LaTeX/Word parser or semantic verifier.",
    "Human review is required for claims, hedging, units, metric binding, terminology coverage and table-cell meaning.",
    "No publication-readiness or compilation guarantee is inferred from exit code 0."
]


def require_strings(value, label, nonempty=False):
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise ValueError(f"{label} must be an array of nonempty strings")
    if nonempty and not value:
        raise ValueError(f"{label} must not be empty")


def validate_glossary(data):
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Glossary schema_version must be 2.0; migrate legacy fields explicitly")
    if not isinstance(data.get("version"), str) or not data["version"]:
        raise ValueError("Glossary version is required")
    if not isinstance(data.get("project"), str) or not data["project"]:
        raise ValueError("Glossary project is required")
    if not isinstance(data.get("terms"), list) or not data["terms"]:
        raise ValueError("An explicitly supplied glossary must contain at least one term")
    concepts = {}
    for term in data["terms"]:
        if not isinstance(term, dict):
            raise ValueError("Each term must be an object")
        for field in ("concept_id", "canonical", "context", "notes"):
            if not isinstance(term.get(field), str):
                raise ValueError(f"Missing or invalid term field: {field}")
        if not all(term[field].strip() for field in ("concept_id", "canonical", "context")):
            raise ValueError("Concept ID, canonical and context must be nonempty")
        if term["concept_id"] in concepts:
            raise ValueError(f"Duplicate concept_id: {term['concept_id']}")
        for field in ("source_forms", "allowed_forms", "forbidden_aliases"):
            require_strings(term.get(field), field, nonempty=field == "source_forms")
        if term.get("status") not in ("author_confirmed", "verified", "provisional"):
            raise ValueError("Invalid term status")
        if not isinstance(term.get("evidence"), list):
            raise ValueError("Term evidence must be an array")
        if term["status"] != "provisional" and not term["evidence"]:
            raise ValueError("Confirmed/verified terms require evidence records")
        for record in term["evidence"]:
            if not isinstance(record, dict) or record.get("kind") not in ("author", "source", "standard", "paper", "official"):
                raise ValueError("Invalid evidence kind")
            if not all(isinstance(record.get(field), str) and record[field].strip() for field in ("locator", "note")):
                raise ValueError("Evidence requires locator and note")
        concepts[term["concept_id"]] = term
    return concepts


def protected_tokens(text):
    return PROTECTED.findall(text)


def math_tokens(text):
    return [match.group(0) for match in MATH.finditer(text)]


def number_tokens(text):
    return NUMBER.findall(text.replace("−", "-"))


def word_boundary(text, start, span):
    end = start + len(span)
    left_ok = not (start > 0 and re.match(r"[A-Za-z0-9_]", text[start - 1]) and re.match(r"[A-Za-z0-9_]", span[0]))
    right_ok = not (end < len(text) and re.match(r"[A-Za-z0-9_]", text[end]) and re.match(r"[A-Za-z0-9_]", span[-1]))
    return left_ok and right_ok


def table_shapes(text):
    shapes = []
    table_lines = []
    for line in text.splitlines() + [""]:
        if line.strip().startswith("|") and line.strip().endswith("|"):
            table_lines.append(line)
        else:
            if any(re.fullmatch(r"\s*\|(?:\s*:?-+:?\s*\|)+\s*", item) for item in table_lines):
                shapes.append(("markdown", [len(re.split(r"(?<!\\)\|", item.strip())[1:-1]) for item in table_lines]))
            table_lines = []
    for match in re.finditer(r"\\begin\{tabular\}([\s\S]*?)\\end\{tabular\}", text):
        body = re.sub(r"^\s*(?:\[[^\]]*\])?\s*\{[^{}]*\}", "", match.group(1))
        body = re.sub(r"\\(?:hline|toprule|midrule|bottomrule)(?:\[[^\]]*\])?", "", body)
        body = re.sub(r"\\(?:cline|cmidrule)(?:\([^)]*\))?\{[^{}]*\}", "", body)
        rows = [row for row in re.split(r"\\\\(?:\[[^\]]*\])?", body) if row.strip()]
        shapes.append(("tabular", [len(re.findall(r"(?<!\\)&", row)) + 1 for row in rows]))
    return shapes


def compact(text):
    return re.sub(r"\s+", "", text)


def audit(source, target, glossary=None, alignment=None):
    findings = []
    warnings = []
    concepts = validate_glossary(glossary) if glossary is not None else {}

    def flag(check, location, before, after):
        findings.append({"check": check, "location": location, "source": before, "target": after, "status": "needs_review"})

    def compare(location, source_unit, target_unit):
        for check, extractor in (
            ("protected_commands", protected_tokens),
            ("math_content", math_tokens),
            ("latex_command_counts", COMMAND.findall),
        ):
            source_values = Counter(extractor(source_unit))
            target_values = Counter(extractor(target_unit))
            if source_values != target_values:
                flag(check, location, dict(source_values), dict(target_values))
        for check, extractor in (
            ("numeric_sequence", number_tokens),
            ("environment_sequence", ENVIRONMENT.findall),
            ("heading_sequence", HEADING.findall),
            ("table_shape", table_shapes),
        ):
            source_values = extractor(source_unit)
            target_values = extractor(target_unit)
            if source_values != target_values:
                flag(check, location, source_values, target_values)

    if not source.strip():
        raise ValueError("Source is empty")
    if not target.strip():
        flag("empty_target", "document", "nonempty source", "empty target")
    compare("document", source, target)
    checked_segments = 0
    checked_term_uses = 0
    if alignment is None:
        warnings.append("No alignment supplied: segment coverage, local citation binding and term uses were not checked.")
    else:
        if not isinstance(alignment, dict) or not isinstance(alignment.get("segments"), list) or not alignment["segments"]:
            raise ValueError("Alignment must contain nonempty segments")
        segments = alignment["segments"]
        seen = set()
        for segment in segments:
            if not isinstance(segment, dict) or not all(isinstance(segment.get(field), str) for field in ("id", "source", "target")):
                raise ValueError("Every segment needs string id/source/target")
            if not segment["id"] or segment["id"] in seen:
                raise ValueError("Segment IDs must be unique and nonempty")
            seen.add(segment["id"])
            if not segment["source"].strip() or not segment["target"].strip():
                flag("empty_segment", segment["id"], segment["source"], segment["target"])
            compare(segment["id"], segment["source"], segment["target"])
            uses = segment.get("term_uses", [])
            if not isinstance(uses, list):
                raise ValueError("term_uses must be an array")
            seen_source_spans = set()
            seen_target_spans = set()
            for use in uses:
                if not isinstance(use, dict) or use.get("concept_id") not in concepts:
                    raise ValueError("term_uses requires a matching glossary concept_id")
                term = concepts[use["concept_id"]]
                span = use.get("target_span")
                if not isinstance(span, str) or not span.strip():
                    raise ValueError("target_span must be nonempty")
                source_span = use.get("source_span")
                if not isinstance(source_span, str) or not source_span.strip():
                    raise ValueError("source_span must be nonempty")
                if any(type(use.get(field)) is not int or use[field] < 0 for field in ("source_start", "target_start")):
                    raise ValueError("source_start and target_start must be nonnegative integer offsets")
                source_start, target_start = use["source_start"], use["target_start"]
                source_key = (term["concept_id"], source_start)
                target_key = (term["concept_id"], target_start)
                anchored = True
                if source_key in seen_source_spans or target_key in seen_target_spans:
                    flag("term_span_reused", segment["id"], source_key, target_key)
                    anchored = False
                seen_source_spans.add(source_key)
                seen_target_spans.add(target_key)
                if segment["target"][target_start:target_start + len(span)] != span or not word_boundary(segment["target"], target_start, span):
                    flag("term_target_unanchored", segment["id"], term["concept_id"], span)
                    anchored = False
                if source_span not in term["source_forms"] or segment["source"][source_start:source_start + len(source_span)] != source_span:
                    flag("term_source_unanchored", segment["id"], term["source_forms"], source_span)
                    anchored = False
                if span not in [term["canonical"]] + term["allowed_forms"]:
                    flag("term_form_not_approved", segment["id"], term["canonical"], span)
                if span in term["forbidden_aliases"]:
                    flag("forbidden_alias_in_concept", segment["id"], term["canonical"], span)
                if anchored:
                    checked_term_uses += 1
            checked_segments += 1
        for field, original in (("source", source), ("target", target)):
            assembled = "".join(segment[field] for segment in segments)
            if compact(assembled) != compact(original):
                flag("alignment_coverage", field, "Full ordered text coverage required", "Alignment differs from input file")
    if glossary is not None and checked_term_uses == 0:
        warnings.append("Glossary supplied but no term uses audited; terminology compliance is NOT established.")
    for term in concepts.values():
        if term["status"] == "provisional":
            warnings.append(f"Provisional term requires author review: {term['concept_id']}")
    if re.search(r"\[\?(?:[^\]]*)\]|\[TODO\]|【待(?:作者确认|补)】", target):
        flag("unresolved_marker", "document", "Author decision required", "Unresolved marker in translation")
    if re.search(r"\\(?:verb|input|include|newcommand)|\\begin\{(?:verbatim|longtable|tabularx)\}|\\(?:multirow|multicolumn)", source + target):
        warnings.append("Complex LaTeX detected: manual structural/protected-content inspection required.")
    return {
        "status": "differences_detected" if findings else "no_differences_detected",
        "semantic_review_required": True,
        "coverage": {"aligned_segments": checked_segments, "term_uses_checked": checked_term_uses},
        "findings": findings,
        "warnings": warnings,
        "limits": LIMITS
    }


def main():
    parser = argparse.ArgumentParser(description="Detect candidate translation differences; never certify publication readiness.")
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("--glossary", type=Path)
    parser.add_argument("--alignment", type=Path)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    try:
        glossary = json.loads(arguments.glossary.read_text(encoding="utf-8")) if arguments.glossary else None
        alignment = json.loads(arguments.alignment.read_text(encoding="utf-8")) if arguments.alignment else None
        if arguments.glossary and not isinstance(glossary, dict):
            raise ValueError("Explicit glossary input must be a JSON object")
        if arguments.alignment and not isinstance(alignment, dict):
            raise ValueError("Explicit alignment input must be a JSON object")
        report = audit(arguments.source.read_text(encoding="utf-8"), arguments.target.read_text(encoding="utf-8"), glossary, alignment)
        exit_code = 1 if report["findings"] else 0
    except (OSError, ValueError, TypeError) as error:
        report = {"status": "invalid_input", "error": str(error), "semantic_review_required": True}
        exit_code = 2
    serialized = json.dumps(report, ensure_ascii=False, indent=2)
    if arguments.output:
        try:
            arguments.output.write_text(serialized + "\n", encoding="utf-8")
        except OSError as error:
            print(f"Cannot write report: {error}", file=sys.stderr)
            return 2
    print(serialized)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
