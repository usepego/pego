# Verification

PEGO includes a local verifier for repository hygiene and required framework files.

Verification is engineering infrastructure. It may use Python and GitHub
Actions without making PEGO itself a Python runtime.

## Command

```sh
python3 ops/pego_doctor.py
```

## Checks

The verifier checks:

- Required framework files exist.
- Only `private/README.md` is tracked under `private/`.
- Private instance paths remain outside the reusable framework history.
- Tracked files do not contain configured private markers.
- Python operation scripts compile.
- The system registry references existing public framework files.
- Public PEGO schemas are valid JSON and expose required artifact contract
  fields.

`ops/pego_doctor.py` compiles every `ops/**/*.py` file so validation coverage
follows the local operations tree as it grows.

## Continuous Integration

The GitHub Actions workflow at `.github/workflows/pego-ci.yml` runs the
repository verifier, validates the system registry JSON, checks the protected
private tracking boundary, and executes the local smoke tests.

CI must not require private instance contents. It should only validate the
public reusable framework, protected boundary rules, and reference tooling.

## Optional Private Marker Scan

For sensitive terms that should stay in protected local state, create:

```text
private/_local/doctor-private-markers.txt
```

Add one marker per line. That file stays in the protected private instance.

## Before Push

Run the verifier before pushing framework changes:

```sh
python3 ops/pego_doctor.py
python3 -m json.tool pego/system/registry.json > /dev/null
git status --short --branch
```

Expected private tracking boundary:

```text
private/README.md
```
