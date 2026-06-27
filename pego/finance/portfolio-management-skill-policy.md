# Portfolio Management Skill Policy

This policy governs future PEGO skills, plugins, or runtime adapters that analyze
investment accounts, propose allocation changes, or execute trades.

PEGO may ultimately manage portfolios to improve long-term wealth outcomes, but
portfolio execution is a high-impact financial capability. It requires stronger
governance than ordinary directives.

## Capability Levels

### Level A: Read And Classify

The skill may:

- Read account, holdings, transaction, and balance data.
- Classify assets.
- Map accounts by tax treatment and purpose.
- Detect concentration, liquidity, fee, or drift issues.
- Produce private reports.

No trade proposals or execution.

### Level B: Recommend

The skill may:

- Draft an investment policy statement.
- Propose allocation targets.
- Propose rebalance candidates.
- Produce tax-aware questions.
- Produce decision packets.

No execution.

### Level C: Prepare Execution

The skill may:

- Prepare trade tickets.
- Estimate tax, liquidity, and allocation impact.
- Simulate execution.
- Queue trades for human approval.

No submission to broker, custodian, exchange, or on-chain venue.

### Level D: Execute With Approval

The skill may execute only specific approved actions after explicit human
approval and governance review.

Required:

- Trade packet.
- Account and asset identifiers.
- Amount or quantity.
- Expected allocation impact.
- Tax and liquidity review.
- Expiration time for approval.
- Audit log.
- Kill switch.

### Level E: Autonomous Execution

Autonomous execution is not allowed by default.

It may be considered only after a formal governance upgrade that defines:

- Investment mandate.
- Approved asset universe.
- Rebalancing algorithm.
- Risk budget.
- Position limits.
- Tax rules.
- Liquidity constraints.
- Drawdown limits.
- Maximum trade size.
- Human notification and override rules.
- Emergency stop process.
- Credential storage and rotation policy.
- Full audit trail.

## Required Governance Artifacts

Before any Level C, D, or E capability is enabled, PEGO must have:

- Private investment policy statement.
- Account integration register.
- Holdings baseline.
- Capital bucket map.
- Risk policy.
- Tax and account-location assumptions.
- Security review.
- Governance decision packet.
- Human authority grant.

## Credential And API Rules

Portfolio skills must:

- Use least-privilege credentials.
- Prefer read-only access until execution is explicitly approved.
- Keep credentials out of Git.
- Avoid broad OAuth scopes when account-specific or action-specific scopes are
  available.
- Separate analysis credentials from execution credentials when possible.
- Log every external read and write.
- Support revocation and emergency disablement.

## Execution Rules

Execution skills must not:

- Trade without authority.
- Treat model confidence as permission.
- Optimize expected return while ignoring downside survival.
- Trade employer securities or restricted assets without review.
- Create tax events without review.
- Use leverage, margin, derivatives, shorting, or illiquid assets unless
  specifically approved.
- Override household, runway, tax, or protected-capital constraints.

## Review Cadence

At minimum:

- Daily for active automated execution.
- Weekly for portfolio drift and risk.
- Monthly for strategy fit.
- Quarterly for mandate, tax, account, and risk review.
- Event-driven for major market moves, life changes, income changes, tax events,
  or governance objections.

## Success Measure

Portfolio management succeeds only if it improves the subject's life outcomes:

- Better retirement trajectory.
- Better autonomy.
- Better risk-adjusted resilience.
- Better household security.
- More contentment with the financial path.

Higher returns alone are not sufficient if they create unmanaged risk,
complexity, anxiety, tax harm, or household instability.
