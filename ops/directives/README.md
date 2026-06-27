# Directive Ops

Local tools for producing PEGO directive packets.

Generated directives are written into the protected private instance under `private/directives/`.

## Generate Daily Directive

```sh
python3 ops/directives/generate_daily_directive.py
python3 pegoctl daily-directive
```

Optional date:

```sh
python3 ops/directives/generate_daily_directive.py --date 2026-06-22
python3 pegoctl daily-directive --date 2026-06-22
```

By default, the script will not overwrite an existing daily directive. Use `--force` only when intentionally regenerating a local private directive.
For installed or backed-up operation, pass `--private-root` to `pegoctl` or to
the direct script so generated daily directives stay inside the protected
private instance.

## Select Next Directive

```sh
python3 ops/directives/next_directive.py --date 2026-06-23 --available 30 --energy medium --location computer
```

With completed work:

```sh
python3 ops/directives/next_directive.py --date 2026-06-23 --done "Breakfast Anchor" --available 45 --energy medium --location computer
```

The runner reads protected private queue/register files and writes a protected command response under `private/directives/command-responses/`. It does not execute actions or grant additional authority.
