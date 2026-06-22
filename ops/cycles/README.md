# Cycle Ops

Local cycle runners for PEGO operating loops.

Cycle runners compose smaller local tools while preserving the same privacy rule: private content is written into the protected private instance, and console output is limited to safe status and paths.

## Daily Cycle

Synthesize current directive candidates into an active queue:

```sh
python3 ops/cycles/daily_cycle.py synthesize --date YYYY-MM-DD --candidate private/directives/candidates/example.md
```

Select the next directive and run preflight:

```sh
python3 ops/cycles/daily_cycle.py next --date YYYY-MM-DD --available 30 --energy medium --location computer
```

Record an outcome:

```sh
python3 ops/cycles/daily_cycle.py outcome --date YYYY-MM-DD --directive "Breakfast Anchor" --completion completed
```

Review an outcome into a learning decision:

```sh
python3 ops/cycles/daily_cycle.py review --date YYYY-MM-DD --outcome private/outcomes/directives/YYYY-MM-DD-directive.md
```

Record a learning/context update:

```sh
python3 ops/cycles/daily_cycle.py learn --date YYYY-MM-DD --source Outcome --raw-observation "What was learned" --update-class Pattern --evidence-strength "Directive outcome" --stability "Current but changeable" --proposed-update "What should change"
```

## Weekly Cycle

Generate a bounded weekly operating plan:

```sh
python3 ops/cycles/weekly_cycle.py --week YYYY-Www
```
