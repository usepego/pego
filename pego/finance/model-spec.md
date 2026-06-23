# PEGO Finance Model Spec

Reusable specification for PEGO financial freedom modeling.

This file must not contain private account balances, holdings, income, or personal financial details.

## Purpose

The PEGO finance model estimates when a person can stop relying on regular salary employment while preserving the target lifestyle, downside protection, and strategic optionality.

## Inputs

### Current Position

- Income
- Tax and deduction assumptions
- Monthly essential expenses
- Monthly discretionary expenses
- Annual irregular expenses
- Liquid savings
- Retirement savings
- Taxable investments
- Debt
- Equity or private-company options
- Real estate value and obligations
- Insurance and health care assumptions

### Lifestyle Scenarios

- Essential lifestyle
- Current lifestyle
- Better-than-current lifestyle
- Travel-included lifestyle
- High-discretionary lifestyle
- Dream lifestyle
- Stress lifestyle

### Assumptions

- Inflation
- Average nominal investment return
- Real return
- Retirement age or target date
- Lifespan / time-to-live
- Tax rate
- Social Security or pension inclusion
- Health care cost inflation
- Major capital projects

## Outputs

- Monthly burn
- Annual burn
- Essentials versus discretionary split
- Minimum viable income
- Savings rate
- Liquid runway
- Total runway
- Target number with Social Security or pension
- Target number without Social Security or pension
- Projected target date
- Gap versus target date
- Scenario comparison
- Sensitivity analysis
- Scenario validation
- Risk flags and governance triggers

## Executable Engine

The finance engine contract lives at:

```text
pego/finance/engine-contract.md
```

The reference local scenario runner lives at:

```text
ops/finance/run_scenarios.py
```

It reads private scenario assumptions and writes generated outputs into protected local files.

The reference finance review runner lives at:

```text
ops/finance/review_scenarios.py
```

It converts scenario output into a protected finance scenario review packet for Finance, Governance, Career, Venture, Operations, and Happiness agents.

The local wrapper exposes these as:

```sh
python3 pegoctl finance-run --write-summary
python3 pegoctl finance-review
```

The reference finance check-in runner lives at:

```text
ops/finance/generate_check_in.py
```

It reads protected scenario assumptions and writes targeted questions about assumption freshness, spending changes, runway risk, account-data recency, upcoming decisions, and governance-relevant risks.

By default, finance runners should not print private financial results to stdout. Console output should be limited to file paths or safe-derived status unless an explicit print flag is used.

Finance check-ins must ask for private financial values only inside the protected private instance, and only when the answer changes a directive, scenario, governance gate, or strategy review.

## Required Scenario Set

PEGO should maintain at least:

- Conservative
- Base
- Upside
- Stress
- Lifestyle upgrade

## Calculation Principles

- Keep assumptions explicit and versioned.
- Separate recurring burn from major capital projects.
- Separate essential expenses from nice-to-have lifestyle costs.
- Model optional lifestyle layers separately so the person can see which dreams are worth their target-number impact.
- Model travel separately and allow it to be toggled into target lifestyle.
- Avoid treating average returns as certainty.
- Show both nominal and real-dollar interpretations where useful.
- Stress-test inflation, return, taxes, health care, and income loss.

## Agent Use

The Finance Agent should use this model before making directives involving:

- Job changes
- Business formation
- Investment allocation
- Major purchases
- Home renovation
- Property purchases
- Travel budget
- Retirement timing
- Emergency fund sizing

For high-impact decisions, the Finance Agent should produce an escalation packet with assumptions, scenarios, risks, dissent, and reversibility.

## Governance Triggers

Finance outputs should create governance flags when:

- The target is reached after the target date.
- The target date has a negative surplus/gap.
- Liquid runway is below the emergency target.
- The scenario depends on Social Security, pension, sale proceeds, private-company equity, or speculative upside.
- Stress scenarios materially contradict base-case confidence.
