# Finance Ops

Local finance scenario tools for PEGO.

These scripts may read private inputs and write generated outputs under ignored local directories. Raw financial source files and generated reports should not be committed unless intentionally summarized into private Markdown.

## Run Scenario Engine

```sh
python3 ops/finance/run_scenarios.py
```

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
