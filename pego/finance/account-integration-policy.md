# Account Integration Policy

PEGO may use financial account integrations to understand holdings, balances, transactions, allocation, and risk.

The default posture is read-only visibility. Trading authority is a separate and higher-risk capability.

## Integration Stages

### Stage 0: Manual Export

Use CSV, XLSX, PDF, or manually entered summaries.

Allowed:

- Read exported account data.
- Summarize balances, holdings, and transactions.
- Update private financial-position files.

Not allowed:

- Login automation.
- API keys.
- Trading.

### Stage 1: Read-Only Aggregation

Use read-only data APIs or aggregators where possible.

Allowed:

- Balances.
- Holdings.
- Transactions.
- Security metadata.
- Account types.
- Cost basis where available.

Preferred permissions:

- Read-only.
- No transfer permission.
- No trading permission.
- No withdrawal permission.

### Stage 2: Analysis and Recommendations

PEGO may analyze allocation, risk, tax exposure, liquidity, and scenario impact.

Allowed:

- Rebalancing recommendations.
- Account-location recommendations.
- Tax-aware analysis.
- Retirement-account contribution analysis.
- Cash and runway analysis.

Not allowed:

- Placing trades.
- Moving money.
- Exercising options.
- Tax-triggering transactions.

### Stage 3: Prepared Trade Packets

PEGO may prepare explicit proposed trades or transfers for human review.

Required:

- Account.
- Asset.
- Action.
- Quantity or dollar amount.
- Rationale.
- Scenario impact.
- Tax considerations.
- Risks.
- Dissenting view.
- Reversibility.
- Waiting period if high impact.

The human executes manually unless Stage 4 has been explicitly approved.

### Stage 4: Execution

Default: not enabled.

Execution requires explicit approval, a scoped integration, and governance rules for each account type.

Never enable blanket trading authority across all accounts.

## Account Types

PEGO should track holdings by account type:

- 401(k)
- Traditional IRA
- Roth IRA
- HSA
- Taxable brokerage
- Checking
- Savings
- Crypto exchange
- Self-custody crypto wallet
- Private-company equity
- Real estate
- Business accounts

Account type matters because taxes, access, risk, contribution limits, and trading authority differ.

## Data PEGO Needs

For each account:

- Institution.
- Account nickname.
- Account type.
- Owner.
- Tax treatment.
- Balance.
- Holdings.
- Cash position.
- Cost basis if available.
- Contribution limits.
- Withdrawal constraints.
- Fees.
- Liquidity.
- Whether PEGO has read access.
- Whether PEGO has execution access.

## Credential Rules

- Do not commit credentials, API keys, tokens, recovery phrases, or account numbers.
- Store secrets only in local ignored files or a dedicated secret manager.
- Prefer read-only API scopes.
- Prefer separate API keys per institution and purpose.
- Disable withdrawals wherever possible.
- Use IP allowlists, passkeys, hardware keys, and MFA where available.
- Rotate keys after experiments.
- Keep a local register of what access exists.

## Disclosure Rules

- Do not disclose personal financial information publicly.
- Do not disclose personal financial information to third parties without explicit approval.
- Treat net worth, account balances, holdings, income, account institutions, projections, tax details, private-company equity, debt, and spending details as protected information.
- Do not place protected financial information in reusable framework files intended for public release.

## Trading Rules

Trading is Level 4 by default.

PEGO may not trade unless:

- The account is explicitly listed as execution-enabled.
- The asset class is explicitly approved.
- The maximum trade size is defined.
- The strategy is documented.
- Tax and liquidity consequences are modeled.
- Human confirmation is required for each trade or for a tightly bounded recurring rule.

## Retirement Account Rule

Retirement accounts require extra caution.

Before any retirement-account trade:

- Confirm account type.
- Confirm tax consequences.
- Confirm contribution/withdrawal rules.
- Confirm strategy and allocation target.
- Confirm whether the trade is rebalancing, risk reduction, or speculation.

## Crypto Rule

Crypto accounts require separate risk controls.

Before execution access:

- Disable withdrawals if possible.
- Keep separate read-only and trading keys.
- Define maximum position and trade size.
- Define custody policy.
- Define loss and theft response plan.

## Principle

PEGO should know what exists before deciding what to do. Past holdings matter because they reveal allocation, concentration, taxes, liquidity, behavior, and opportunity cost.
