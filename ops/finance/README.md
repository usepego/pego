# Finance Ops

Local finance scenario tools for PEGO.

These scripts may read private inputs and write generated outputs into protected local directories. Raw financial source files and generated reports must stay inside the private instance unless intentionally summarized into sanitized Markdown.

Public engine contract:

```text
pego/finance/engine-contract.md
```

Public schemas:

```text
pego/schemas/finance-scenario-input.schema.json
pego/schemas/finance-scenario-output.schema.json
```

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

Review scenario output into governance-ready finance guidance:

```sh
python3 ops/finance/review_scenarios.py
```

Run smoke tests with synthetic data:

```sh
python3 ops/finance/test_run_scenarios.py
python3 ops/finance/test_review_scenarios.py
```
