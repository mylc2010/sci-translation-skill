# sci-translation-skill

[![License: MIT](https://img.shields.io/badge/license-MIT-2ea44f)](#license)
[![Agent skill hosts](https://img.shields.io/badge/agents-Codex%20%7C%20Claude%20Code%20%7C%20OpenClaw%20%7C%20OpenCode%20%7C%20Hermes-20232a)](#supported-agents)
[![Skills: 1](https://img.shields.io/badge/skills-1-159bd3)](#key-files)
[![Language: 中文 | English](https://img.shields.io/badge/language-%E4%B8%AD%E6%96%87%20%7C%20English-2769c6)](#sci-translation-skill)

[English](README_EN.md) | [简体中文](README.md)

Version 1.60: a Chinese-to-English translation and review workflow for manuscripts in computer science, medicine, and other STEM fields.
It is not a new translation model. It combines instructions for a coding agent with terminology control, review procedures, and local deterministic checks.

The goal is to reduce terminology drift, technical misrepresentation, omissions, and formatting damage, producing a draft that authors can review before submission.

## Why not just ask for an "SCI-style polish"?

Fluency is not accuracy. Common risks include:
- Renaming the same concept across the abstract, body, and figure captions.
- Turning "may be effective" into "has been proven effective" while losing conditions or threat-model boundaries.
- Having the same pass both translate and approve its own work, with no independent check or post-edit review.
- Preserving a number but attaching it to the wrong metric, or preserving the number of equations while changing variables.
- Adding nominalizations, unsupported mechanisms, or stronger conclusions to sound more academic.

This skill aims for natural scholarly English while putting scientific meaning ahead of rhetoric.

## Workflow

1. Preserve a snapshot of the complete source, incorporate any existing author glossary, and scan the body, figures, tables, algorithms, and appendices for technical terms and important acronyms.
2. **Give the author an editable terminology review table first.** Resolve canonical English terms, acronym expansions, and disputed entries, then freeze an approved version. Formal translation does not begin before approval.
3. Translate a pilot or the full manuscript in chunks using the same glossary. The translator handles faithful expression and academic register together.
4. Independently review source-to-target fidelity, manuscript-wide terminology, data binding, and citations. Revise actual problems and recheck the changes.
5. Deliver the translation, approved glossary, necessary review record, and questions for the author.

For a new paper, translate a two- or three-paragraph Methods/Results pilot after the full-manuscript glossary has been approved. Then extend to the full paper and finalize the abstract last. For an isolated short passage, lock only its local terms; do not claim manuscript-wide consistency.

For terminology review, default to Markdown when one author reviews roughly 30 entries or fewer. Use an editable Excel workbook for larger tables or when multiple reviewers need comments, conflict filtering, or per-entry decision tracking. Collaboration complexity matters more than the count. Both formats must reflect the same machine-readable locked glossary; synchronize author edits before locking a new version.

## Core capabilities

| Capability | How it works | Boundary |
|---|---|---|
| Author-approved terminology | Full-manuscript extraction → editable review table → version/hash lock → one glossary for all agents | Do not translate before approval; an external lookup is not author approval |
| Multi-agent collaboration | Assign terminology research, translation, and independent review when callable tools exist | Otherwise use serial self-review and disclose it |
| Technical fidelity | Track negation, conditions, quantifiers, and evidence strength by passage | The author remains responsible for scientific correctness |
| Academic register | Apply transferable qualities of Nature-style prose: precision, concision, and direct statements; check colloquial filler, articles, units, and subject–verb relations | Do not impose arbitrary word limits or spelling rules, or inflate claims |
| Reader-oriented editing | Organize existing information by section, clarify actors and references, and reduce sentence load | Do not add meaning, move content across paragraphs, or enforce a sentence-length cap |
| Separate evaluation | Check fidelity as a gate, then assess readability using concrete examples | No detected errors does not automatically mean a perfect score |
| Format protection | Check necessary structural boundaries, equations/macros/citations, and table coordinates | Complex formatting still needs human or rendered inspection |
| Automated difference checks | Check numbers, protected fragments, citation counts, basic structure, alignment, and registered terms | Automation is not a semantic peer review |

"Multi-agent" means separate task contexts, not necessarily different models or human experts. The run record names the roles and versions actually used; it must not fabricate team activity. A separate language editor and multiple files per paragraph are not required by default.

## Fields

- Computer science, security, and AI: threat models, access control, KEM versus payload decryption, mathematical notation, and technical boundaries.
- Medicine and biology: study design, association versus causation, effect estimates and intervals, samples, doses, endpoints, and time points.
- Engineering and materials: experimental conditions, units and dimensions, measured versus simulated results, uncertainty, and scope.

These are additional review guidelines, not claims of extensive cross-domain validation. Medical manuscripts require final review by qualified specialists.

## Installation and runtime

Place the `sci-translation-skill` directory containing `SKILL.md` in a skill directory supported by your host. Do not add an extra nesting level.

If the host supports installing skills from a repository, you may provide this repository's address. Supplying a link is not itself proof that installation succeeded; installation depends on the host and its permissions.

For a manual installation, the locally used Codex path is `~/.codex/skills/sci-translation-skill/SKILL.md`.

Run this example from the repository root, backing up an existing installed version first:
```bash
mkdir -p ~/.codex/skills/sci-translation-skill
rsync -a --exclude '.git/' --exclude '.DS_Store' --exclude '__pycache__/' ./ ~/.codex/skills/sci-translation-skill/
```

Refresh the host's skill discovery or start a new session, then confirm that it can read `SKILL.md`. This README does not replace the host's current configuration documentation.

### Supported agents

The hosts below provide a way to load `SKILL.md` directories. **This is not end-to-end certification of this skill on every platform.** Only the local Codex installation has been used for this repository. Keep `references/`, `scripts/`, and `examples/` with `SKILL.md` when copying it.

| Agent | Skill directory or installation entry point | Status for this repository |
|---|---|---|
| Codex | `~/.codex/skills/sci-translation-skill/` | Used locally |
| [Claude Code](https://code.claude.com/docs/en/skills) | `~/.claude/skills/sci-translation-skill/` | Official loader available; not tested with this repository |
| [OpenClaw](https://docs.openclaw.ai/tools/skills) | Import with `openclaw skills install ./path/to/sci-translation-skill`, or use its skill directory | Official local-skill import available; not tested with this repository |
| [OpenCode](https://opencode.ai/docs/skills) | `~/.config/opencode/skills/sci-translation-skill/` | Official loader available; not tested with this repository |
| [Hermes Agent](https://hermes-agent.nousresearch.com/docs/guides/work-with-skills/) | `~/.hermes/skills/sci-translation-skill/` | Official loader available; not tested with this repository |

For Antigravity, Cursor, Windsurf, Aider, and similar hosts, check their skill or rule-loading interfaces before loading this entry point and its references. Dify, FastGPT, Coze, and custom harnesses require their own role nodes, dependencies, file transfer, and run records; adding this skill to a knowledge base alone does not create a multi-agent pipeline.

Do not claim every platform works out of the box merely because files can be copied. The skill does not require a fixed Sonnet/Opus model or alter host configuration. Its scripts use only the Python 3 standard library.

## Copy-ready prompts

First use: review terminology only; **do not translate in this turn**.
```text
Use $sci-translation-skill to lock terminology before translating this complete paper.
Field: [discipline]; target journal: [name or undecided]; format: [LaTeX/Word/plain text].
Read my existing glossary first, then scan the title, abstract, body, equation descriptions, figures, tables, algorithms, and appendices.
Give me an editable table with each concept, context/location, one canonical English term, acronym and full form, approved grammatical forms, and open questions.
List any unread or uncovered content. Deliver only the terminology table in this turn; wait for my approval before a pilot translation.
```

Second message, after approving the table:
```text
I have approved this glossary: [path/version]. My changes were: [row numbers or "none"].
Use $sci-translation-skill to validate the locked version, then translate a [two- or three-paragraph Methods/Results pilot] or continue the full manuscript.
All translators and reviewers must use the same glossary. Preserve numbers, qualifications, equations, citations, and LaTeX macros.
Use precise, concise scholarly English without colloquial filler. Ask me to approve any new technical term first.
```

For an existing Chinese–English draft:
```text
Use the review mode of $sci-translation-skill to compare the English against the Chinese passage by passage.
Check technical meaning, terms, claim strength, numbers/units, and citations before checking fluency.
Correct only evidenced problems. Separate preferences such as "uses→adopts" from substantive errors.
Identify actual reading obstacles before editing. Compare the initial translation and edited draft for changes in condition scope, causality, metric binding, and citations.
For each issue, list the source, current translation, revision, reason, and post-edit verification.
```

For a full manuscript:
```text
Use $sci-translation-skill to scan the whole manuscript and present a terminology review table first. If I have already explicitly approved this complete table, validate it and proceed directly to full translation.
Deliver into a new directory without overwriting the source. All chunks share the same glossary version and research context.
Cover the body, figure captions, tables, equation descriptions, algorithms, and appendices; finally check the scope of claims in the abstract.
Deliver the English draft, locked glossary, necessary alignment/review records, and unresolved questions. Do not create empty files merely to satisfy a template.
```

## Check tools

```bash
bash references/test-skill-integrity.sh
python3 scripts/check_glossary_gate.py terminology-glossary.json --source source-snapshot.txt
python3 scripts/audit_translation.py source.tex target.tex \
  --glossary terminology-glossary.json \
  --alignment alignment.json \
  --output qa-report.json
```

Glossary gate exit codes: 0 = the approval record matches the glossary and source snapshot; 1 = not cleared; 2 = invalid input. Translation audit exit codes: 0 = implemented checks found no differences; 1 = review needed; 2 = invalid input.
Exit code 0 **does not mean the manuscript is submission-ready**. Without alignment, do not claim passage-level coverage or term compliance. Legitimate number reordering or formatting changes may trigger differences and require documented human adjudication.

The original shell entry point remains available:
```bash
bash references/test-translation-structure.sh source.tex target.tex glossary.json
```

Neither shell test script detects "AI writing" or certifies domain accuracy.

## Key files

- [SKILL.md](SKILL.md): entry point and release gates.
- [Terminology approval contract](references/glossary-schema.md): review table, author-approval gate, JSON schema, and alignment format.
- [Glossary gate script](scripts/check_glossary_gate.py): validates version, entries, and source snapshot; it cannot replace genuine author approval.
- [Agent contracts](references/agent-contracts.md): callable tools and artifact ownership.
- [Language guide](references/academic-phraseology-guide.md): faithful, concise, natural expression.
- [Reader-oriented editing](references/reader-oriented-editing.md): section roles, sentence load, continuity, and post-edit fidelity checks.
- [Domain profiles](references/domain-profiles.md): field-specific review risks.
- [Behavioral evaluation](references/behavioral-evaluation.md): model-behavior acceptance plan.
- [Example glossary](examples/terminology-glossary.sample.json): a field example, not externally verified or automatically applicable.
- [Translation example](examples/translation-diff-sample.md): a constructed case, not evidence of published performance.

## Version 1.60 update

**Full-manuscript terminology gate:** the abstract, body, figures, tables, and appendices use one approved version; acronym expansions and allowed grammatical forms are reviewed together. New terms require incremental approval.
The workflow borrows structure and independent review from `translation-quality`, and reader flow, precision, concision, and academic-register checks from `nature-polishing`. It does not copy parallel translation before glossary approval or rigid sentence-length rules.
To reduce turnaround time, claim maps and structural inventories are created only where risk warrants them. Translators combine faithful translation with routine language editing; a separate language editor is optional. After scripted screening, the reviewer performs focused semantic checks across the manuscript.
Following `nature-polishing`'s section-aware approach, the existing final review now also checks whether Introduction promises match Results evidence, Abstract conclusions match the body, and Discussion limitations name the claims they qualify. Gaps in the source become author queries, not invented content or unauthorized restructuring.

## License

The README currently declares the MIT License.
