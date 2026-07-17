---
name: patent-bilingual-qa
description: Patent bilingual QA for translating or reviewing patent claims, specifications, office actions, and prosecution papers. Use for source-target alignment, patent terminology consistency, scope-changing omissions or additions, claim dependencies, reference numerals, numbers, units, formulas, and bilingual DOCX redlines.
---

# Patent Bilingual QA

Treat every translation as a scope-preservation review. The deliverable is an auditable bilingual record, not merely fluent target-language prose.

## Modes

- Translate + QA: create a target draft, then run the full review.
- Existing-translation QA: compare an existing target against the authoritative source.
- Terminology audit: review only defined terms and repeated technical concepts.

## Steps

### 1. Fix the translation brief

Record the source of truth, target language, filing jurisdiction, document type, application or matter identifier, confidentiality constraints, client style guide, approved glossary, and prior family translations.

If the authoritative source, target language, or document type is unknown, ask for it before substantive work. Treat a machine-readable copy as convenience evidence; page images or the filed document remain authoritative where OCR is uncertain.

Completion criterion: templates/translation-brief.md is complete and every input file is listed with a SHA-256 hash.

### 2. Build the segment map

Assign stable IDs before translating or reviewing:

- CLM-<claim>-<limitation> for claim limitations.
- SPEC-<section>-<paragraph> for specification paragraphs.
- FIG-<figure>-<item> for drawing text and reference numerals.
- OA-<ground>-<paragraph> for office-action passages.

Preserve one source segment per row. Split a segment only when the legal or technical relationship remains explicit. Never merge separate claim limitations into an untraceable target sentence.

Completion criterion: every source segment is represented exactly once in the segment map, including headings, tables, formulas, footnotes, and drawing labels.

### 3. Establish the termbase

Apply the precedence rules in references/terminology-policy.md. Record each selected term, source, status, subject field, and any forbidden alternatives.

Completion criterion: every defined term and every technical noun phrase repeated three or more times has a termbase entry or an explicit no-entry decision.

### 4. Translate or load the target

Preserve claim logic before naturalness: actors, objects, modifiers, conditions, alternatives, sequence, polarity, ranges, and open or closed transitions. Mark source ambiguity as [SOURCE-AMBIGUITY] rather than resolving it silently.

When reviewing an existing translation, keep the received file immutable. Make proposed edits in a copy with tracked changes or a side-by-side issue register.

Completion criterion: every target segment is linked to its source segment and all unresolved translation choices are marked.

### 5. Run the four-pass QA

Read references/qa-rules.md and apply all four passes:

1. Coverage and alignment.
2. Scope and logic.
3. Mechanical invariants.
4. Terminology and target-language quality.

Run scripts/check_invariants.py on text-exported source and target files. Its findings are candidates for human review, not automatic legal conclusions.

Completion criterion: each segment has a recorded status and every script finding is resolved, accepted with rationale, or left as an explicit blocker.

### 6. Classify and propose corrections

Use the issue severities and output contract in references/output-contract.md. Every issue must show source text, target text, proposed correction, rationale, confidence, and reviewer decision.

Apply P2 editorial corrections to a working copy when they do not affect meaning, and log them. Keep P0 scope-critical and P1 material corrections as proposals until a reviewer accepts them.

Completion criterion: no issue is missing an owner or disposition; no P0 issue is silently incorporated into the clean target.

### 7. Deliver the review package

Produce the files required by references/output-contract.md. If DOCX input is involved, use the available document-editing capability for tracked changes and comments. Preserve the original file.

Completion criterion: the package includes the authoritative-source hashes, segment map, termbase, issue register, review summary, and redline; a clean target is labeled draft until P0/P1 decisions are closed.

## Guardrails

- Confidential material stays within user-authorized systems. Public web searches use abstracted terminology, not unpublished invention details.
- A cited term or rule carries its source and retrieval date. Current official sources outrank remembered practice.
- Back translation is an anomaly detector only.
- Filing, certification, and final scope decisions remain with the responsible patent professional.

## References

- Read references/qa-rules.md for every full review.
- Read references/terminology-policy.md whenever terminology is selected or changed.
- Read references/output-contract.md before creating deliverables.
- Read references/official-sources.md when a term or jurisdiction rule needs external verification.
