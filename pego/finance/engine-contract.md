# Finance Engine Contract

The PEGO finance engine converts protected private financial assumptions into
scenario outputs, scenario reviews, governance triggers, and directive
candidates.

The engine is part of PEGO's analysis layer. It does not grant execution
authority. Trade, transfer, account, tax, job, housing, debt, and major spending
decisions remain governed actions.

## Runtime Neutrality

The finance engine may be implemented by a local script, spreadsheet importer,
LangGraph node, Vercel-hosted service, custom backend, or another runtime
adapter. The runtime must preserve the same input, output, privacy, and
governance semantics.

## Inputs

The protected private scenario input should include:

- `as_of`: date assumptions were current.
- `currency`.
- `current_position`: summary values needed for modeling.
- `global_assumptions`: age, target date, longevity, emergency runway, and
  shared modeling assumptions.
- `scenarios`: named scenario assumptions.

Public schema:

```text
pego/schemas/finance-scenario-input.schema.json
```

## Outputs

The protected private scenario output should include:

- Validation status.
- Scenario summary.
- Per-scenario burn, target number, runway, target date projection, surplus or
  gap, and risk flags.

Public schema:

```text
pego/schemas/finance-scenario-output.schema.json
```

## Required Scenarios

The finance engine should maintain at least:

- Conservative.
- Base.
- Upside.
- Stress.
- Lifestyle upgrade.

If required scenarios are missing, the finance engine may still produce output,
but governance should treat the result as incomplete.

## Privacy Rules

- Scenario inputs and outputs are protected private financial data.
- Do not commit scenario inputs or outputs.
- Do not print scenario outputs unless explicitly requested.
- Do not disclose net worth, account balances, income, holdings, tax details,
  spending, target numbers, runway, or projections to public files or third
  parties without explicit approval.
- Public framework files may contain schemas, formulas, risk rules, and synthetic
  examples only.

## Governance Rules

The finance engine can support Level 1 recommendations and Level 2 directives
for low-risk analysis work.

Level 4 escalation is required for:

- Trades or transfers.
- Account changes.
- Debt actions.
- Job changes.
- Housing decisions.
- Major purchases or renovations.
- Tax-impacting decisions.
- Actions based on speculative equity, aggressive return assumptions, or reduced
  runway.

## Required Risk Flags

Finance outputs should flag:

- Target not reached within model window.
- Target after target date.
- Negative gap at target date.
- Liquid runway below emergency target.
- Dependency on Social Security, pension, sale proceeds, private equity, or
  speculative upside.

## Agent Routing

Finance scenario reviews should route to:

- Finance for model interpretation.
- Governance for authority, risk, privacy, and execution boundaries.
- Career and Venture when income strategy is implicated.
- Operations when low-risk next actions should be scheduled.
- Happiness when lifestyle layers materially change the desired life.

## Local Reference Adapter

The current local reference implementation is:

```text
ops/finance/run_scenarios.py
ops/finance/review_scenarios.py
```

These scripts are local engineering/runtime adapters, not the PEGO architecture
itself.
