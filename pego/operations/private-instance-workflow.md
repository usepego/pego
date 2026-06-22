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
- Local source files.

## Local Instance Layer

The local private instance lives under:

```text
private/
```

Everything under `private/` is ignored by Git except `private/README.md`.

## Bootstrap

Create or refresh the local skeleton:

```sh
python3 ops/private/bootstrap_private_instance.py
```

The bootstrap script does not overwrite existing files unless `--force` is passed.

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
