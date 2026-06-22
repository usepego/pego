# Directive Ops

Local tools for producing PEGO directive packets.

Generated directives are written into the protected private instance under `private/directives/`.

## Generate Daily Directive

```sh
python3 ops/directives/generate_daily_directive.py
```

Optional date:

```sh
python3 ops/directives/generate_daily_directive.py --date 2026-06-22
```

By default, the script will not overwrite an existing daily directive. Use `--force` only when intentionally regenerating a local private directive.

## Select Next Directive

```sh
python3 ops/directives/next_directive.py --date 2026-06-23 --available 30 --energy medium --location computer
```

With completed work:

```sh
python3 ops/directives/next_directive.py --date 2026-06-23 --done "Breakfast Anchor" --available 45 --energy medium --location computer
```

The runner reads protected private queue/register files and writes a protected command response under `private/directives/command-responses/`. It does not execute actions or grant additional authority.
