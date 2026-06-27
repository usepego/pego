# Tool Contract: finance.scenario_model

## Tool

`finance.scenario_model`

## Purpose

Model financial trajectory scenarios from protected assumptions so the Finance
Agent can evaluate runway, target dates, downside, lifestyle burn, savings,
returns, inflation, and strategy tradeoffs.

## Owning Agents

Finance Agent, Career Agent, Venture Agent, Governance Agent, Council.

## Inputs

- Protected finance assumptions.
- Scenario names and parameters.
- Burn, income, savings, return, inflation, and target assumptions.
- Optional stress cases.

## Outputs

- Scenario results.
- Target capital estimate.
- Runway classification.
- Sensitivity and stress notes.
- Decision-grade questions.
- Governance notes for high-impact actions.

## Authority Required

Level 0 observe for reading assumptions.

Level 1 recommend for scenario analysis and planning recommendations.

## Operation Type

Recommend.

## Private Data Used

- Financial assumptions.
- Savings, income, burn, target, and account-class data when supplied.

## Third-Party Disclosure

Local only by default. External financial modeling services require explicit
approval.

## Write Locations

Protected private finance outputs, reviews, check-ins, and council evidence.

## Governance Review

Scenario output does not grant authority to trade, quit, move, borrow, spend, or
make tax/legal decisions. High-impact actions require decision packets and
review.

## Failure Mode

If assumptions are stale or incomplete, issue a targeted finance check-in rather
than inventing precision.

## Logging Rule

Log assumptions used, confidence, and model limitations inside the protected
private instance.

## Prohibited Uses

- Public disclosure of balances, net worth, income, account details, or target
  numbers.
- Trade, transfer, tax, debt, employment, or housing execution.
- Treating model output as professional financial advice.
