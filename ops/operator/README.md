# Operator Ops

Local tools for running PEGO as an active operator.

These tools may read the protected private instance and write protected private operating artifacts. They should print only safe-derived status and file paths by default.

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
- Writes a protected command response.
- Runs governance preflight on the response.
- Writes a protected preflight JSON record.
- Prints only paths and preflight outcome.
