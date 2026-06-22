# Operator Ops

Local tools for running PEGO as an active operator.

These tools may read ignored private state and write ignored private operating artifacts. They should print only safe-derived status and file paths by default.

## Next Step

```sh
python3 ops/operator/next_step.py --date YYYY-MM-DD --available 30 --energy medium --location computer
```

With completed work:

```sh
python3 ops/operator/next_step.py --date YYYY-MM-DD --done "Breakfast Anchor" --available 45 --energy medium --location computer
```

The runner:

- Selects one next directive from the private queue/register.
- Writes an ignored command response.
- Runs governance preflight on the response.
- Writes an ignored preflight JSON record.
- Prints only paths and preflight outcome.
