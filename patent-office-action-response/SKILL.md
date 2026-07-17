---
name: patent-office-action-response
description: Patent office-action response drafting for real CNIPA, USPTO, or EPO examination communications. Use when the user provides an examination opinion or Office Action and needs rejection inventory, cited-art mapping, claim-amendment options, original-disclosure basis, response arguments, interview planning, or a review-ready prosecution package.
---

# Patent Office Action Response

Build an auditable first-draft response to a real examination communication. Every objection is accounted for, every amendment has original-disclosure basis, and every factual or legal proposition is traceable.

## Steps

### 1. Open the matter record

Collect the office communication, application as filed, current claims, cited references, prosecution history, deadline exactly as stated, jurisdiction, procedural posture, commercial objective, and reviewer.

Preserve received files. If an input is PDF or DOCX, use the available document-reading capability and retain page or paragraph coordinates. For cross-language material, invoke patent-bilingual-qa before relying on translated passages.

Completion criterion: templates/matter-intake.md is complete; every input is listed with source, version, and hash; jurisdiction and procedural posture are confirmed.

### 2. Load the jurisdiction module

Read exactly one primary module:

- CN: references/jurisdictions/cn.md
- US: references/jurisdictions/us.md
- EP: references/jurisdictions/ep.md

If the communication is PCT, JP, KR, or another jurisdiction, stop the jurisdiction-specific drafting branch and create only a neutral issue inventory until a verified module is supplied.

Completion criterion: the record identifies the current official sources and retrieval date used for the run.

### 3. Inventory the entire communication

Create one row for every rejection, objection, requirement, formality, allowable-subject-matter indication, and procedural instruction. Record its category and whether its scope is claim-specific or communication-wide. Capture affected claims where applicable, authority, examiner reasoning, cited evidence, quoted pinpoint, and response deadline or requested action.

Completion criterion: every numbered heading and every claim mentioned in the communication maps to at least one inventory row; a second pass finds no unaccounted instruction.

### 4. Reconstruct the examiner's mappings

For novelty, inventive-step, and obviousness grounds, decompose each affected independent claim and relevant dependent limitation. Map each limitation to the exact passage relied upon by the examiner. Use claim-chart if available; otherwise use templates/claim-chart.md.

Record explicit disclosure, asserted inherent disclosure, combination rationale, common-general-knowledge assertion, disputed construction, and missing evidence separately.

Completion criterion: every limitation has a state and pinpoint; absence of a pinpoint is labeled [MISSING-EVIDENCE], not filled from memory.

### 5. Run claim and support checks

Check current and proposed claims for dependency, antecedent basis, clarity, terminology consistency, and specification support. Use patent-claims-analyzer if available, then verify its findings manually.

For each possible amendment, build an amendment-basis row before drafting the amendment. The basis must identify the as-filed document and pinpoint and explain why the combination is directly supported under the selected jurisdiction module.

Completion criterion: every proposed added or changed limitation has a basis row and scope-effect statement; unsupported amendments are excluded from the draft options and marked [NO-BASIS].

### 6. Build the strategy board

For each inventory row, select one or more strategies:

- traverse on fact or law;
- clarify without substantive amendment;
- amend with supported limitation;
- submit evidence or declaration;
- request interview, consultation, or oral proceedings;
- preserve an issue for appeal or another procedural route;
- obtain a client strategy decision.

Compare breadth lost, commercial coverage, downstream claim effects, inconsistency with prosecution history, admission risk, and procedural consequences. Use references/strategy-gates.md.

Completion criterion: every inventory row has an owner, chosen strategy, fallback, and disposition; every narrowing amendment has an explicit business and legal rationale.

### 7. Draft amendments and response

Draft amendments in the selected jurisdiction's required presentation. Then draft the response in the same order as the inventory:

1. examiner position stated neutrally;
2. applicant position;
3. claim or amendment relied upon;
4. source evidence and pinpoint;
5. legal authority verified from an official current source;
6. requested disposition.

Keep alternative strategies outside the filing draft in an internal strategy memo.

Completion criterion: every response section names the inventory row it resolves; every quote and citation has been checked against the source; no internal note appears in the filing draft.

### 8. Validate and hand off

Populate templates/package-manifest.json and run scripts/validate_package.py. Resolve every structural error. Its success status, `manifest-structure-valid`, confirms manifest completeness only. Critical flags and open inventory rows keep the package in not-ready status.

Produce the output package defined in references/output-contract.md. The responsible patent professional reviews deadlines, law, facts, amendments, admissions, and filing format before submission.

Completion criterion: validator exits successfully, the filing draft contains no placeholders, and the review checklist records a named human approver. This criterion means review-ready, not filing-authorized.

## Guardrails

- Deadline text is transcribed with source coordinates; deadline computation is a separate verified task.
- Confidential facts stay within user-authorized systems. External research uses official sources and abstracted queries.
- Source gaps remain visible as [MISSING], [VERIFY], [STRATEGY-DECISION], or [BLOCKER].
- The skill prepares drafts and decision records; it does not sign, file, send, or represent authorization to practice.

## References

- Read references/strategy-gates.md before selecting an amendment or procedural route.
- Read references/output-contract.md before generating files.
- Read references/official-sources.md when verifying law or current editions.
- Read the selected jurisdiction module in full; do not combine jurisdiction rules by analogy.
