# Directive Ops

Local tools for producing PEGO directive packets.

Generated directives are written under `private/directives/`, which is ignored by Git.

## Generate Daily Directive

```sh
python3 ops/directives/generate_daily_directive.py
```

Optional date:

```sh
python3 ops/directives/generate_daily_directive.py --date 2026-06-22
```

By default, the script will not overwrite an existing daily directive. Use `--force` only when intentionally regenerating a local private directive.
