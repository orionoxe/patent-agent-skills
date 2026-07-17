# patent-bilingual-qa

An installable Agent Skill for auditable patent translation and bilingual quality assurance.

## Package contents

- SKILL.md: invocation and execution steps.
- references/: QA rules, terminology precedence, outputs, and official sources.
- templates/: translation brief, segment map, termbase, and issue register.
- scripts/check_invariants.py: deterministic checks for claims, numbers, units, and reference numerals.
- tests/: small fixtures for the deterministic checker.

## Install

From the repository root:

    npx skills add orionoxe/patent-agent-skills \
      --skill patent-bilingual-qa -g -y

Or copy the folder into the skills directory used by your agent.

## Validate the bundled checker

    python3 patent-bilingual-qa/scripts/check_invariants.py \
      --source patent-bilingual-qa/tests/fixtures/source.txt \
      --target patent-bilingual-qa/tests/fixtures/target-good.txt

The checker uses only the Python standard library. A non-zero exit code means candidate invariant differences were found.
