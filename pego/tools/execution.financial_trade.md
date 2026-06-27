# Tool Contract: execution.financial_trade

## Tool

`execution.financial_trade`

## Purpose

Place financial trades only after PEGO has explicit private authority,
account-level permissions, reviewed investment policy, governance approval, and
validated stop conditions.

This is a future execution tool contract, not an enabled default capability.

## Owning Agents

Finance Agent, Governance Agent, Council.

## Inputs

- Approved account.
- Approved instrument.
- Approved action.
- Approved quantity or sizing rule.
- Investment policy reference.
- Governance review reference.
- Human confirmation when required.
- Stop conditions.

## Outputs

- Execution attempt record.
- Broker response or confirmation.
- Fill status.
- Errors or partial fills.
- Post-trade review requirement.

## Authority Required

Level 3 execute only if the constitution explicitly grants the tool and action.

Level 4 escalation is required before enabling or changing this tool.

## Operation Type

Execute.

## Private Data Used

- Account identifiers.
- Holdings.
- Trade instructions.
- Credentials or broker permissions managed by the runtime.

## Third-Party Disclosure

External service.

## Write Locations

Protected private finance execution logs, governance reviews, and outcome
records.

## Governance Review

Required before enablement, before strategy changes, and before any action not
covered by an existing reviewed policy.

## Failure Mode

If anything is stale, mismatched, blocked, or ambiguous, do not trade. Escalate
to Governance and require review.

## Logging Rule

Log the minimum execution record needed for audit. Never log credentials. Never
write private financial details to public files.

## Prohibited Uses

- Default autonomous trading.
- Trading without explicit account-level permission.
- Trading from public prompts or public files.
- Trading when account data, policy, or authority is stale.
- Tax-sensitive, leveraged, derivative, crypto, concentrated, or illiquid
  actions without formal review.
