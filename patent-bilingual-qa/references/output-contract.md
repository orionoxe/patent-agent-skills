# Output Contract

## Severity

| Code | Meaning | Default handling |
|---|---|---|
| P0 | Likely scope, claim logic, disclosure, or filing-identity change | Reviewer decision required |
| P1 | Material terminology, ambiguity, omission, or inconsistency | Reviewer decision required |
| P2 | Grammar, typography, formatting, or style with no identified scope effect | May be applied to a working copy and logged |
| Q | Source ambiguity or strategy question | Owner and deadline required |

## Required package

1. translation-brief.md
2. segment-map.csv
3. termbase.csv
4. qa-issues.csv
5. bilingual-review.md
6. target-redline.docx or an equivalent side-by-side redline when DOCX is unavailable
7. target-clean-draft.docx only after the review status permits it

## Issue register columns

- issue_id
- severity
- segment_id
- category
- source_text
- target_text
- proposed_target
- rationale
- authority_or_termbase_id
- confidence
- owner
- decision
- status

Allowed status values: open, accepted, rejected, deferred, not-an-issue.

## Review summary

State:

- files and hashes reviewed;
- language pair and jurisdiction;
- segment count;
- P0, P1, P2, and Q counts;
- unresolved blockers;
- mechanical checker results;
- whether a clean draft was generated;
- the human approval still required.
