# Contributing

Issues and pull requests are welcome for workflow defects, deterministic checks, templates, documentation, and current official-source updates.

## Public-data rule

Use synthetic or fully de-identified examples. Public contributions must not contain unpublished inventions, client communications, personal data, credentials, filing identifiers, deadline data, or material you are not authorized to disclose.

## Before opening a pull request

1. Keep each behavioral rule in one authoritative location.
2. Preserve the visible human-review gates and jurisdiction boundaries.
3. Add or update a public-interface test for deterministic behavior.
4. Run `make test` and `make list`.
5. Explain the user-visible effect and any compatibility risk.

Legal or procedural rule changes must cite a current official WIPO, CNIPA, USPTO, EPO, or other relevant authority, record the retrieval date, and identify the exact skill step or reference affected. Secondary summaries are not enough.

## Pull request review

All checks must pass. Maintainers may request changes where a proposal broadens automatic legal conclusions, hides uncertainty, weakens original-disclosure checks, or introduces confidential examples.

## License of contributions

Every contribution intentionally submitted and accepted for inclusion in this repository is provided under the Apache License 2.0, consistent with Section 5 of that license. Contributions carrying conflicting or additional license terms will not be accepted. Submit only work you have the right to license.
