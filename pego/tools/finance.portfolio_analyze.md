# Tool Contract: finance.portfolio_analyze

## Tool

`finance.portfolio_analyze`

## Purpose

Analyze holdings, allocation, concentration, drift, fees, liquidity, tax
exposure, and risk so the Finance Agent can propose reviewed portfolio
recommendations.

## Owning Agents

Finance Agent, Governance Agent, Council.

## Inputs

- Account classes.
- Holdings.
- Balances.
- Contribution rules.
- Tax status or account location when supplied.
- Investment policy constraints.
- Time horizon and risk constraints.

## Outputs

- Allocation summary.
- Concentration and drift notes.
- Risk and liquidity concerns.
- Decision questions.
- Proposed policy changes.
- Trade candidates only when authority and policy allow proposal.

## Authority Required

Level 0 observe for read-only account data.

Level 1 recommend for analysis.

Level 4 escalation for any trade, transfer, liquidation, leverage, options,
crypto, tax-sensitive, or account-permission change unless the private
constitution grants a narrower reviewed authority.

## Operation Type

Observe or recommend.

## Private Data Used

- Account names or classes.
- Holdings and balances.
- Tax/account location.
- Investment policy and goals.

## Third-Party Disclosure

Local only by default. Broker, data aggregator, or market-data API use requires
explicit approval and least-privilege credentials.

## Write Locations

Protected private finance reviews, portfolio analysis, decision packets, and
council evidence.

## Governance Review

Follow `pego/finance/portfolio-management-skill-policy.md`.

Execution remains locked unless explicitly enabled by account, tool, action,
authority, review, and stop conditions.

## Failure Mode

If account data is stale, incomplete, or ambiguous, request an account and
holdings map refresh before recommending changes.

## Logging Rule

Log source, freshness, assumptions, and review status. Do not log account
credentials or private balances publicly.

## Prohibited Uses

- Autonomous trading by default.
- Credential collection in public artifacts.
- Sharing holdings, balances, net worth, or account identifiers publicly.
- Treating allocation analysis as professional investment advice.
