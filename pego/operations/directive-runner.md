# Directive Runner

The directive runner is a local operational helper for creating private daily directive packets.

## Purpose

It turns the PEGO daily-loop protocol into a concrete local file under:

```text
private/directives/daily/
```

That directory is ignored by Git.

## Command

```sh
python3 ops/directives/generate_daily_directive.py
```

## Privacy

The runner may read local private files. It must write generated directives only to ignored local paths.

The runner must not:

- Print private file contents to stdout.
- Write private instance content to tracked framework files.
- Imply Level 2 or higher authority without explicit adoption.

## Authority

Generated daily directives are Level 1 recommendations by default.

They become stronger only if the private constitution grants that authority and governance review approves it.
