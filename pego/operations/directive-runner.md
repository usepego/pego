# Directive Runner

The directive runner is a local operational helper for creating private daily directive packets.

## Purpose

It turns the PEGO daily-loop protocol into a concrete protected private file under:

```text
private/directives/daily/
```

That directory is part of the protected private instance.

The public framework template is:

```text
pego/templates/daily-directive.md
```

## Command

```sh
python3 ops/directives/generate_daily_directive.py
python3 pegoctl daily-directive
```

## Next Directive Command

Use this command when the human reports status or asks what is next:

```sh
python3 ops/directives/next_directive.py --date YYYY-MM-DD --available 30 --energy medium --location computer
```

The runner reads the protected private directive queue and operating register, then writes one protected command response under:

```text
private/directives/command-responses/
```

It may also accept completed work:

```sh
python3 ops/directives/next_directive.py --date YYYY-MM-DD --done "Breakfast Anchor" --available 45 --energy medium --location computer
```

## Privacy

The runner may read protected private files. It must write generated directives only to protected private-instance paths.

The runner must not:

- Print private file contents to stdout.
- Write private instance content to framework files.
- Imply Level 2 or higher authority without explicit adoption.
- Treat markdown queue parsing as a substitute for governance review.

## Authority

Generated daily directives are Level 1 recommendations by default.

They become stronger only if the private constitution grants that authority and governance review approves it.

High-impact recommendations should remain decision packets, not routine daily directives.
