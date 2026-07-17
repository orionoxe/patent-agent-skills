# Patent Agent Skills

[简体中文](README.zh-CN.md)

[![CI](https://github.com/orionoxe/patent-agent-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/orionoxe/patent-agent-skills/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

Open, auditable Agent Skills for patent translation quality assurance and office-action response drafting.

> [!IMPORTANT]
> These skills prepare drafts and review records. They do not provide legal advice, calculate filing deadlines, or authorize filing. A qualified patent professional must review every substantive output.

## Included skills

| Skill | Purpose | Deterministic gate |
|---|---|---|
| `patent-bilingual-qa` | Patent translation, bilingual alignment, terminology control, and scope-preservation QA | Compares claim identifiers, reference numerals, numbers, units, and publication numbers |
| `patent-office-action-response` | CNIPA, USPTO, and EPO action inventory, claim mapping, amendment support, strategy, and response drafting | Validates that every inventory row, amendment basis, pinpoint, reviewer, and critical flag is accounted for |

Both skills preserve visible blockers and require human approval for scope, legal, deadline, and filing decisions.

## Install

Node.js 18 or later is required by the Skills CLI. The bundled deterministic checkers require Python 3.9 or later and use only the standard library.

List the skills before installing:

```bash
npx skills add orionoxe/patent-agent-skills --list
```

Install one skill globally:

```bash
npx skills add orionoxe/patent-agent-skills \
  --skill patent-bilingual-qa -g -y

npx skills add orionoxe/patent-agent-skills \
  --skill patent-office-action-response -g -y
```

Install both through the interactive selector:

```bash
npx skills add orionoxe/patent-agent-skills
```

## Use

Typical requests include:

```text
Compare this English patent application with its Chinese translation. Build a
segment map and termbase, then report P0/P1/P2 bilingual QA issues.
```

```text
Analyze this USPTO Office Action and the application as filed. Inventory every
rejection, map the examiner's evidence, and prepare supported response options.
```

Read each skill's `SKILL.md` for its full input requirements, completion criteria, and output contract.

## Compatibility

- Verified locally with Codex and the `skills` CLI.
- Uses the portable `SKILL.md` format and is expected to work with other agents supported by the CLI.
- Platforms not named as verified have not yet received end-to-end testing.

## Development

```bash
make test
make list
make package VERSION=v0.1.0
```

The test suite verifies positive and intentionally invalid fixtures, deterministic archives, checksums, and public-repository hygiene.

## Releases

Pushing a semantic version tag such as `v0.1.0` runs all checks and publishes:

- `patent-bilingual-qa-v0.1.0.zip`
- `patent-office-action-response-v0.1.0.zip`
- `patent-agent-skills-v0.1.0.zip`
- `SHA256SUMS.txt`

Tags beginning with `v0.` are published as pre-releases.

## Source policy

Jurisdiction rules change. The skills link to official WIPO, CNIPA, USPTO, and EPO sources and record retrieval dates. A rule update must cite a current official source and identify the affected workflow behavior.

Use only synthetic or fully de-identified examples in public issues and pull requests. Never post unpublished inventions, client communications, credentials, filing identifiers, or deadline information.

See [DISCLAIMER.md](DISCLAIMER.md), [SECURITY.md](SECURITY.md), and [CONTRIBUTING.md](CONTRIBUTING.md) before relying on or contributing to the project.

## License

Apache License 2.0. See [LICENSE](LICENSE).
