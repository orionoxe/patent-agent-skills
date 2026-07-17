# Publishing checklist

The repository is prepared locally. The commands below intentionally create public GitHub state; run them only after reviewing the complete first commit.

## 1. Verify the local repository

```bash
git status --short
git show --stat --oneline HEAD
make test
make list
make package VERSION=v0.1.0
```

Inspect `dist/SHA256SUMS.txt` and the archive contents. The `dist/` directory is ignored because the tag workflow rebuilds the release artifacts.

## 2. Create the public repository

```bash
gh repo create orionoxe/patent-agent-skills \
  --public \
  --source=. \
  --remote=origin \
  --description="Open, auditable Agent Skills for patent translation QA and office-action response drafting" \
  --push
```

Configure discovery topics:

```bash
gh repo edit orionoxe/patent-agent-skills \
  --enable-issues \
  --add-topic agent-skills \
  --add-topic patent \
  --add-topic legaltech \
  --add-topic translation \
  --add-topic cnipa \
  --add-topic uspto \
  --add-topic epo \
  --add-topic codex
```

Enable private vulnerability reporting and verify the setting before advertising the security contact:

```bash
gh api --method PUT \
  -H "X-GitHub-Api-Version: 2026-03-10" \
  repos/orionoxe/patent-agent-skills/private-vulnerability-reporting

test "$(gh api \
  -H "X-GitHub-Api-Version: 2026-03-10" \
  repos/orionoxe/patent-agent-skills/private-vulnerability-reporting \
  --jq '.enabled')" = "true"
```

Wait for the `CI` workflow on `main` to pass before tagging.

## 3. Publish the first pre-release

```bash
git tag -a v0.1.0 -m "v0.1.0 public preview"
git push origin v0.1.0
```

The tag workflow validates the repository, builds reproducible archives, generates SHA-256 checksums, and creates a GitHub pre-release.

## 4. Verify public installation

```bash
npx skills add orionoxe/patent-agent-skills --list
npx skills add orionoxe/patent-agent-skills \
  --skill patent-bilingual-qa -g -y
```

Confirm that both skills appear in the listing and that the GitHub Release contains all four expected assets.
