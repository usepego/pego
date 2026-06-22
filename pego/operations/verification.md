# Verification

PEGO includes a local verifier for repository hygiene and required framework files.

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
git status --short --branch
```

Expected private tracking boundary:

```text
private/README.md
```
