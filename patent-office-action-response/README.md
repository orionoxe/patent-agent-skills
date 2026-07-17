# patent-office-action-response

An installable Agent Skill for auditable first-draft responses to real CNIPA, USPTO, and EPO examination communications.

## Package contents

- SKILL.md: predictable end-to-end steps.
- references/jurisdictions/: CN, US, and EP rule modules.
- references/: strategy gates, outputs, and official sources.
- templates/: intake, inventory, claim chart, amendment basis, response, and manifest.
- scripts/validate_package.py: deterministic manifest-structure gate.
- tests/: valid and intentionally incomplete manifest fixtures.

## Install

From the repository root:

    npx skills add orionoxe/patent-agent-skills \
      --skill patent-office-action-response -g -y

## Validate the bundled gate

    python3 patent-office-action-response/scripts/validate_package.py \
      patent-office-action-response/tests/fixtures/valid-manifest.json

The validator checks the manifest structure required by `references/output-contract.md`. It does not determine package review-readiness or legal correctness.
