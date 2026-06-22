# Cycle Ops

Local cycle runners for PEGO operating loops.

Cycle runners compose smaller local tools while preserving the same privacy rule: private content is written to ignored private files, and console output is limited to safe status and paths.

## Daily Cycle

Select the next directive and run preflight:

```sh
python3 ops/cycles/daily_cycle.py next --date YYYY-MM-DD --available 30 --energy medium --location computer
```

Record an outcome:

```sh
python3 ops/cycles/daily_cycle.py outcome --date YYYY-MM-DD --directive "Breakfast Anchor" --completion completed
```

Record a learning/context update:

```sh
python3 ops/cycles/daily_cycle.py learn --date YYYY-MM-DD --source Outcome --raw-observation "What was learned" --update-class Pattern --evidence-strength "Directive outcome" --stability "Current but changeable" --proposed-update "What should change"
```
