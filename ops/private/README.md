# Private Instance Ops

Local tools for creating and maintaining a private PEGO instance.

These tools may write files under `private/`, which is ignored by Git except for `private/README.md`.

## Bootstrap Local Private Instance

```sh
python3 ops/private/bootstrap_private_instance.py
```

The script creates a local private folder structure and starter files from reusable PEGO templates.

By default, it does not overwrite existing files.

Use `--force` only if you intentionally want to replace local private starter files.
