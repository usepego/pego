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

## Executable Engine

The reference local scenario runner lives at:

```text
ops/finance/run_scenarios.py
```

It reads private scenario assumptions and writes generated outputs to ignored local files.

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
