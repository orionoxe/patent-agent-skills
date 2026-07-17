# Security Policy

## Supported versions

During the `0.x` preview period, only the latest tagged release and the default branch receive fixes.

## Report a vulnerability

Use GitHub's private vulnerability reporting for code execution, archive handling, path traversal, credential exposure, or other security defects:

https://github.com/orionoxe/patent-agent-skills/security/advisories/new

The maintainer enables and verifies this repository setting as part of `PUBLISHING.md`; the link becomes usable only after that step succeeds.

Do not open a public issue containing exploit details, credentials, unpublished patent material, client information, application identifiers, or deadlines.

For incorrect legal sources or workflow behavior without a security impact, use the official-source update issue template and include a public primary source.

## Data handling

The bundled Python scripts operate on local files and use only the standard library. They do not make network requests. Agent behavior outside these scripts depends on the host agent and tools selected by the user; review those systems' data-handling terms before using confidential material.
