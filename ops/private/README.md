# Private Instance Ops

Local tools for creating and maintaining a protected private PEGO instance.

These tools may write protected operating state under `private/`.

## Bootstrap Local Private Instance

```sh
python3 ops/private/bootstrap_private_instance.py
```

The script creates a protected private folder structure and starter files from reusable PEGO templates.

By default, it does not overwrite existing files.

Use `--force` only if you intentionally want to replace private starter files.

## Check Operating Readiness

```sh
python3 ops/private/check_readiness.py
```

The readiness checker reports only path presence and safe status. It does not
print private file contents.

Write a protected private readiness report:

```sh
python3 ops/private/check_readiness.py --output private/governance/preflight/readiness.json
```
