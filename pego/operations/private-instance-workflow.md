# Private Instance Workflow

PEGO separates reusable framework material from private instance data.

## Repository Layer

Tracked by Git:

- `pego/`
- `ops/`
- `decisions/`
- `private/README.md`

Not tracked by Git:

- Actual private goals.
- Actual financial data.
- Actual health data.
- Directives.
- Journals.
- Telemetry.
- Writing samples, voice models, taste notes, drafts, and public-writing briefs.
- Local source files.

## Local Instance Layer

The local private instance lives under:

```text
private/
```

Everything under `private/` is protected private operating state except `private/README.md`, which only documents the boundary.

For installs or backed-up local operation, set:

```sh
export PEGO_PRIVATE_ROOT="/path/to/backed-up/PEGO/private"
```

or pass `--private-root` to setup and readiness commands. PEGO should redact
external private-root paths in routine reports unless explicit path reveal is
requested.

The private root should be covered by a real backup system. See
`pego/operations/private-storage-backup.md`.

## Bootstrap

Create or refresh the local skeleton:

```sh
python3 ops/private/bootstrap_private_instance.py
```

For an external backed-up private root:

```sh
python3 ops/private/bootstrap_private_instance.py --private-root "/path/to/backed-up/PEGO/private"
```

The bootstrap script does not overwrite existing files unless `--force` is passed.

## Readiness

Check whether the protected private instance has the minimum structure required
for USER mode operation:

```sh
python3 ops/private/check_readiness.py
```

The readiness checker must not print private contents. It may write a protected
private readiness report under `private/governance/preflight/`.

Check whether private storage is likely backed up:

```sh
python3 ops/private/check_storage.py
```

If PEGO cannot detect a backup/sync signal, the user may confirm backup coverage
explicitly, but that confirmation should be treated as infrastructure evidence,
not as a substitute for durable backup.

To persist that confirmation for future guide and readiness flows:

```sh
python3 pegoctl storage --confirm-backup
```

## Operating Rule

Agents may read and update local private files when operating on a private instance, but reusable framework files must not contain primary-subject details.

## Before Push

Run:

```sh
git ls-files private
```

Expected output:

```text
private/README.md
```
