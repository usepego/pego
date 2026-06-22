# Repository Access Policy

PEGO repositories should use least-privilege access.

## Scope

Repository and automation credentials should be scoped only to the PEGO repository they need.

Default rule:

- One repository.
- Minimum required permissions.
- No organization access unless explicitly required.
- No unrelated personal or company repositories.
- No broad OAuth grants when a fine-grained token or narrower app installation is available.

## Personal Instance Repositories

For a private personal PEGO instance:

- Use a personal repository controlled by the primary subject.
- Do not grant access to employer organizations.
- Do not grant access to unrelated organizations.
- Do not install company workspace tools.
- Do not connect company code-review, CI, or productivity tools unless explicitly reviewed.

## Recommended GitHub Access

Preferred:

- Fine-grained personal access token.
- Limited to the PEGO repository.
- `Contents: Read and write` only.

Optional permissions should be added only when needed:

- Pull requests.
- Issues.
- Actions.

Avoid:

- Broad `repo` OAuth scope.
- Organization-wide access.
- Tokens with delete/admin permissions except for brief, audited maintenance.
- Third-party GitHub Apps installed across all repositories.

## Organization Boundary

PEGO should not request or retain access to employer GitHub organizations.

If an OAuth app or GitHub App has organization access unrelated to PEGO, revoke that access before using it for PEGO work.

## Temporary Elevated Access

Temporary elevated access may be used only for explicit maintenance tasks.

Rules:

- Grant the scope only for the task.
- Complete the task.
- Revoke the scope immediately.
- Record the reason if the event is security-relevant.

## Verification

Before pushing sensitive or personal PEGO work:

- Confirm the remote points to the intended repository.
- Confirm tracked files do not include private instance data.
- Confirm protected private instance files remain outside the reusable framework layer.
- Confirm OAuth or app access does not include unrelated organizations.

## Principle

PEGO should never ask for more repository access than it needs to govern the private instance.
