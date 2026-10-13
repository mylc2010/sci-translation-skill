# sci-translation-skill

[English](README_EN.md) | [简体中文](README.md)

Version 6.0.0. An evidence-preserving Chinese-to-English manuscript translation and review workflow for computing, medicine and other STEM disciplines.
This is an agent skill and local QA toolkit, not a new translation model or a publication guarantee.

## Workflow

1. Preserve the source; record paper type, section, audience and edit scope; map structure and scientific propositions.
2. Freeze a project glossary with concept IDs, context, approved forms and evidence.
3. Translate faithfully, then edit for explicit actors, manageable sentence load and paragraph cohesion without adding arguments.
4. Review source versus edited text in both directions, then check editing changes for newly introduced drift.
5. Revise tracked issues and recheck the final version.
6. Deliver the translation, glossary, review record and author queries.

Start a new project with a 2–3-paragraph Methods/Results pilot. For full papers, finalize the abstract after reviewing the body.

## Principles

Scientific meaning and evidence strength take precedence over terminology preferences and prose style.
Keep negation, modality, conditions, populations, units, mathematical content, citations and attribution.
Remove empty preambles, not meaningful uncertainty or limitations.
Prefer precise direct verbs over unnecessary nominalization; “adopts” is not universally better than “uses.”
Use context-specific concepts rather than global forbidden-word replacement.
For example, KEM decapsulation and payload decryption may legitimately coexist in one sentence.

## Actual multi-agent execution

Use independent translator and reviewer agents only when callable tools exist.
Use the requested or runtime-default model; do not hard-code model names.
Record actual agent IDs, known model identities, input scope and artifacts.
Separate agents may use the same model and are not equivalent to independent human experts.
If tools are unavailable, use serial self-review and label it honestly.
For complex papers, an optional language-editor can handle the reader-oriented pass. The final reviewer still checks the source independently; short passages do not need another agent solely to add a role.

No cross-platform runtime certification is implied.
Loading Markdown into an editor or knowledge base does not create an independent agent team.

## Domains

The skill includes review profiles for:
- Computing/security/AI: threat models, trust boundaries, cryptographic operations and formal notation.
- Medicine/biology: study design, association versus causation, endpoints, effect estimates, intervals and units.
- Engineering/materials: conditions, dimensions, measured versus simulated results and uncertainty.

These are review instructions, not validated performance claims across all disciplines.
Clinical meaning still requires qualified human review.
Do not upload unpublished manuscripts, identifiable patient data or confidential research to external services without authorization.

## Installation

Place the directory containing SKILL.md in the host's supported skill directory.
The local Codex installation used for this project is ~/.codex/skills/sci-translation-skill/SKILL.md.
Run this example from the repository root. Back up an existing installed version before updating it.

```bash
mkdir -p ~/.codex/skills/sci-translation-skill
rsync -a --exclude '.git/' --exclude '.DS_Store' --exclude '__pycache__/' ./ ~/.codex/skills/sci-translation-skill/
```

Refresh skill discovery or start a new session as required by the host.
For Claude Code, Antigravity, Cursor, Windsurf or Aider, verify current loading and tool interfaces.
Dify, FastGPT, Coze and custom harnesses need explicit role orchestration, dependency handling and artifact transfer.
This repository does not provide tested adapters for every platform.

## Example request

```text
Use $sci-translation-skill in pilot mode.
Field: [field]; target journal: [journal or undecided]; format: [format].
Build a glossary from the supplied manuscript and translate the selected Methods/Results paragraphs.
Preserve claims, uncertainty, numbers, units, mathematics and citations.
After the faithful draft, improve reader flow within paragraphs; do not enforce sentence-length quotas or supply missing arguments.
Use independent review if tools are available; otherwise disclose serial self-review.
Return the translation, locked terms, located review findings and author queries.
```


For an existing bilingual draft, request review mode and minimal evidence-based corrections.
For full papers, request a new output directory, a shared glossary version, chunk-seam review and final abstract checking.

## Deterministic checks

Python 3 standard library only:
```bash
bash references/test-skill-integrity.sh
python3 scripts/audit_translation.py source.tex target.tex \
  --glossary terminology-glossary.json \
  --alignment alignment.json --output qa-report.json
```

Exit 0: no differences found by implemented checks.
Exit 1: candidate differences need review.
Exit 2: invalid input or parsing failure.
Exit 0 never certifies publication readiness.

Checks cover visible numbers, common protected LaTeX fragments, citation multiplicities, basic structures and registered aligned term uses.
They are heuristic, not a full TeX/Word parser or semantic reviewer.
Without alignment, local coverage and terminology compliance are not established.
Scientific meaning, metric binding, complex tables and uncertainty require human/agent review.
The legacy shell entrypoint delegates to this checker.

## Documentation

- [Entry point](SKILL.md)
- [Glossary and alignment schema](references/glossary-schema.md)
- [Agent contracts](references/agent-contracts.md)
- [Evidence-preserving style](references/academic-phraseology-guide.md)
- [Reader-oriented editing](references/reader-oriented-editing.md)
- [Domain profiles](references/domain-profiles.md)
- [Behavioral evaluation](references/behavioral-evaluation.md)
- [Illustrative glossary](examples/terminology-glossary.sample.json)
- [Constructed translation example](examples/translation-diff-sample.md)

The example glossary has no asserted external verification. Examples are not benchmark results.
The workflow draws on translation-quality's structure inventory, role separation, bidirectional checks and final validation, while adding scientific fidelity and project-level terminology controls.

## What changed in v6

This local update moves directly from v4.0.0 to v6.0.0; it does not assert an intermediate v5 release.
Building on v4's safeguards, it adapts ideas from the inspected nature-polishing v6.1.0:
- Route by paper type, section, audience and authorized edit scope before sentence polishing.
- Diagnose missing argumentation separately from unclear expression; flag gaps rather than fill them.
- Clarify systems, mechanisms, evidence and boundaries, with explicit actors and cohesive information flow.
- Add an optional language-editor and recheck changes against the source after editing.
- Separate fidelity gates from evidence-anchored editorial ratings; no automatic perfect score for finding no errors.

It does not adopt rigid 10–30-word sentences, punctuation bans or mandatory abstract templates. It does not delete background, add significance or restructure the manuscript without authorization.
The new reference is self-contained and requires no other skill at runtime. Deterministic audit code is unchanged.
These are workflow improvements, not demonstrated superiority across manuscripts; matched-input, multi-sample blind evaluation is still needed.
Check the target journal's current author and AI-use policies before submission; the skill does not certify policy compliance.

## License

MIT License.
