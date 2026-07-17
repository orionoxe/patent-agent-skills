# Output Contract

Create one versioned matter directory containing:

1. 00-matter-intake.md
2. 01-action-inventory.md
3. 02-claim-chart.md
4. 03-amendment-basis.md
5. 04-internal-strategy.md
6. 05-response-draft.md
7. 06-interview-plan.md when applicable
8. 07-review-checklist.md
9. package-manifest.json

## Status vocabulary

- open: not substantively addressed.
- addressed: draft position exists with support.
- deferred: intentionally left for a named decision-maker and date.
- withdrawn-by-office: the communication or later record shows withdrawal.
- not-applicable: reason recorded.

Every inventory row records a category and scope. Use `claims` scope with one or more affected claim identifiers. Use `communication` scope with an empty claim list for claim-independent formalities or procedural instructions.

## Review-ready gate

A package is review-ready only when:

- every inventory row is addressed, withdrawn-by-office, or explicitly deferred;
- every cited passage has a pinpoint;
- every amendment has original-disclosure basis and scope effect;
- every changed claim is checked for dependencies and terminology;
- the filing draft has no placeholders or internal strategy notes;
- critical_flags is empty;
- the deterministic validator exits zero;
- a named patent professional is assigned final review.

Review-ready does not mean filed, legally approved, or deadline-verified.
The validator's success status is `manifest-structure-valid`; it is a structural prerequisite and never a legal-readiness conclusion by itself.
