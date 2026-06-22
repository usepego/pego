# Finance Ops

Local finance scenario tools for PEGO.

These scripts may read private inputs and write generated outputs into protected local directories. Raw financial source files and generated reports must stay inside the private instance unless intentionally summarized into sanitized Markdown.

## Run Scenario Engine

```sh
python3 ops/finance/run_scenarios.py
```

By default, the runner writes private output files and prints only file paths. Use `--print` only when console output of private financial model results is intentional.

Default input:

```text
private/finance/scenarios.json
```

Default output:

```text
private/_local/finance/scenario-output.json
```

Summarize selected outputs into:

```text
private/finance/scenario-results.md
```

Generate a local private Markdown summary:

```sh
python3 ops/finance/run_scenarios.py --write-summary
```

Run smoke tests with synthetic data:

```sh
python3 ops/finance/test_run_scenarios.py
```
