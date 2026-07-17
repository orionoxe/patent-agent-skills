# QA Rules

Apply these rules to every segment. The comparison is source-to-target; target-language elegance never overrides source scope.

## Pass 1: Coverage and alignment

- Account for headings, body text, claim labels, tables, formulas, footnotes, sequence listings, drawing labels, and handwritten or stamped text.
- Mark illegible source material as [OCR-VERIFY] with page and location.
- Detect omitted, duplicated, merged, or invented segments.
- Keep each claim limitation traceable to one or more explicit target spans.

## Pass 2: Scope and logic

Compare the following dimensions explicitly:

| Dimension | Questions |
|---|---|
| Actor | Is the same entity performing the action? |
| Object | Is the same component, data, material, or result affected? |
| Modifier | Does each modifier attach to the same noun or verb? |
| Condition | Are if, when, unless, only if, and threshold conditions preserved? |
| Sequence | Is an ordered sequence preserved, or has order been introduced? |
| Polarity | Are positive, negative, exception, and exclusion statements preserved? |
| Quantity | Are singular, plural, at least one, each, any, and respective preserved? |
| Alternative | Are and, or, either, one of, and at least one of preserved? |
| Range | Are endpoints, inclusivity, approximation, and units preserved? |
| Transition | Is an open, closed, or partially closed claim transition preserved? |
| Function | Is configured-to, adapted-to, capable-of, and result language handled consistently with context? |
| Dependency | Does every dependent claim retain the same parent relationship and added limitation? |

Classify any unresolved difference in these dimensions as P0 or P1.

## Pass 3: Mechanical invariants

Compare source and target for:

- claim identifiers and dependency references;
- Arabic numerals, decimal separators, percentages, signs, and ranges;
- measurement units and scientific notation;
- equations, variable names, chemical formulas, and sequence identifiers;
- reference numerals, figure numbers, table numbers, and paragraph numbers;
- patent and publication numbers, priority dates, and party names.

Run scripts/check_invariants.py. Review every difference against the page image because OCR and language-specific numbering can create false positives.

## Pass 4: Terminology and language

- Use one approved target term for one concept unless the termbase records a justified variant.
- Preserve expressly defined terms exactly.
- Treat near-synonyms as different until the source context and termbase show equivalence.
- Keep patent style controlled and unambiguous; prefer the shortest target phrasing that preserves every relationship.
- Flag grammar or punctuation that changes attachment, scope, or antecedent reference above ordinary style defects.
- Record source-language errors separately from translation errors.

## Confidence

- High: source and authoritative terminology support one clear correction.
- Medium: correction is likely but domain or claim-construction context matters.
- Low: source ambiguity or jurisdiction practice requires a patent professional.
