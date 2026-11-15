# Report-driven academic editing

## Extraction and coverage

Snapshot inputs; record paths, hashes, report generation/version if available, and explicit unknowns. Use the actual report: PDF annotation objects, drawn highlights, or scanned images/OCR as appropriate. Preserve geometry or page/column anchors and original flagged fragments. Do not assume all PDF highlights are annotations or that color implies a reliable mark. If the page classifier, OCR, a relevant page or a highlight is uncertain, list it for manual inspection; do not equate extracted line count with complete coverage.

Exclude display equations, figures and captions, tables and captions, algorithms, code, and references. A paragraph with inline math is in scope, but protect the inline expression and macros byte-for-byte. A caption interleaved with prose or a flag spanning a protected boundary must be inspected and split only with reliable evidence. Report excluded counts separately from unreadable/unresolved counts; never claim a complete inventory where counting is unreliable.

## Align full sentences

Use the corresponding editable manuscript and surrounding context. Locate flagged span, then expand to sentence boundaries without including the previous sentence's trailing acronym alone. Merge a sentence split across pages/columns into one record, listing all locations; multiple adjacent marks in the same sentence also form one record. Identical sentences at separate source positions are different records. Related adjacent sentences may form one unit only when required to preserve scope and reference.

Each unit has a stable ID, report locations, marked fragment(s), source version/hash and exact structural anchor, full source sentence(s), Chinese translation, proposed English, Chinese back-translation, rationale, status and author decision. Track raw mark IDs separately and map each exactly once to a unit, exclusion, or unresolved record. Ensure every review unit has all four language fields. When a unit needs an unavailable continuation, do not guess; show the unresolved fragment separately and do not claim full coverage or approve it for replacement.

## Fidelity and humanizer checks

Apply the 26 checks from the upstream framework in academic context. Preserve claims and evidentiary force, conditions and negations, subjects/objects, numerical bindings, formulas, abbreviations, citations, technical nomenclature and author-approved glossary. Do not remove scientifically meaningful limitations as defensive prose. Do not change a strong unsupported original to a weaker claim without an author decision: keep the original strength in the proposed wording and explain the concern separately. Do not introduce missing evidence or fact claims. Compare both the proposed English and its Chinese translation against the source; mark unresolved differences for the author.

## Review artifact and diffs

Use a Word document by default for side-by-side or stacked four-part units, with original edits highlighted light red and new/replacement text light green. Match the baseline and proposal at word/token level; whitespace-only changes need not be highlighted. Render and visually inspect examples and verify text extraction preserves the words. Large reorderings may produce many highlights; explain this. Do not claim Excel supports partial-word background shading: use font color/underline in optional Excel or a separate format that actually supports run highlighting. Use one canonical structured dataset for review formats, and identify the authoritative approved version.

## Apply after approval

Read actual returned decisions, not a prior template; preserve comments and resolve conflicts. Record accepted, rejected, unchanged and unresolved entries, including cross-page duplicates. Authorize no actions for blank decisions. Check original source is the same version, then match each accepted unit uniquely with context and structured anchors. Preserve raw source syntax (including TeX commands, math, escapes and citation keys); abort or skip if the mapping or protected-token checks fail. Keep the source unchanged and generate a separate working copy and per-ID ledger. Compile only after all requested replacements are accounted for, and report partial work if any remain blocked.
