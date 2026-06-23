# Distribution And Installation

PEGO should be installable through normal developer and user tooling without making the framework depend on one Python runtime.

The package surface exists to make PEGO easy to start, verify, and operate locally. It is not the PEGO runtime. Agent contracts, schemas, governance rules, privacy boundaries, and operating protocols remain the core product.

## Package Shape

The public package name is `usepego`.

The installed command is:

```sh
pegoctl
```

`pegoctl` is a thin command wrapper around framework operations. It may dispatch into local scripts, future runtime adapters, or hosted services, but it must preserve the same governance and private-instance contracts.

The package should stay small:

- `pyproject.toml` defines package metadata and build configuration.
- `[project.scripts]` exposes `pegoctl` as the command-line entry point.
- `src/usepego/` contains the installable CLI adapter.
- `ops/` remains engineering infrastructure for checks, scaffolding, validation, migrations, and reference operation scripts.
- `pego/` remains runtime-neutral framework infrastructure.

## Tooling Direction

Use the least amount of Python packaging machinery needed to look serious and remain maintainable.

Preferred path:

```sh
uv tool install usepego
pegoctl --help
```

Acceptable fallback:

```sh
pipx install usepego
pegoctl --help
```

While private, PEGO should not be published to PyPI. The package metadata keeps the project in pre-alpha and uses the `Private :: Do Not Upload` classifier as a guardrail against accidental public upload.

## Release Posture

Before public package publication, PEGO should have:

- A public repository with no private subject data.
- A clear license.
- A security policy.
- A changelog.
- CI on pull requests and main.
- Secret scanning and dependency scanning.
- Signed release tags where practical.
- PyPI Trusted Publishing from GitHub Actions instead of long-lived PyPI tokens.
- PyPI digital attestations when publishing is enabled.

For native desktop applications later, platform signing and notarization may apply. For the Python CLI package, the credible trust layer is source transparency, CI, Trusted Publishing, provenance, and conservative dependencies.

## Private Instance Setup

The installer must make the private-data boundary obvious.

Future `pegoctl init` should:

1. Explain that framework files and private life files are separate.
2. Ask where the protected private instance should live.
3. Prefer a user-owned, naturally backed-up location such as iCloud Drive, Dropbox, OneDrive, Syncthing, or an encrypted local backup path.
4. Bootstrap the private instance.
5. Verify readiness.
6. Confirm that private subject data is not stored in the framework package or public repository.

The current source checkout uses `private/` as the protected local instance root. Future package installs may support an explicit private root through environment or config, but that root remains outside the reusable framework boundary.

## Site Requirements

The public site should prepare users without exposing any private instance:

- Explain PEGO as Personal Executive Governance OS, not a helper chatbot or quantified-self dashboard.
- Show synthetic examples only.
- Explain authority levels, governance review, privacy boundaries, and reversibility.
- Explain install paths for `uv` and `pipx`.
- Explain private storage and backup expectations.
- Link to package provenance and release notes once publishing begins.
