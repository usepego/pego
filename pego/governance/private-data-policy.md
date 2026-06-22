# Private Data Policy

PEGO separates reusable system design from the human's protected private operating state.

This is a product boundary first, not a source-control feature. The framework can be shared, reused, audited, or productized. The private instance is the subject's operating memory and must remain protected.

## Layers

### Framework Layer

The framework layer contains PEGO material that can safely become public or reusable:

- Agent protocols.
- Governance rules.
- Authority levels.
- Templates and schemas.
- Operating loops.
- Runners and verification tooling.
- Synthetic examples.
- Product documentation.

Framework files must not contain real subject facts.

### Private Instance Layer

The private instance contains the human's real operating state:

- Goals, values, constraints, and protected time.
- Current state, preferences, fears, concerns, and annoyances.
- Financial, health, work, relationship, household, and location context.
- Directives, outcomes, session logs, reviews, and private strategy.
- Private operating memory inferred from conversations and telemetry.
- Account data, exports, statements, balances, holdings, and credentials.

The private instance is not disposable. It needs durability, recovery, and backup, but ordinary framework publishing is not an acceptable backup mechanism.

### Local Derived State

Local derived state includes generated outputs, model runs, exports, caches, temporary files, and scenario results.

Derived state may still be sensitive because it can reveal private facts through summaries, filenames, or calculations. Treat derived state as protected unless it has been deliberately sanitized.

## Product Language

Use these terms in user-facing PEGO material:

- Protected private instance.
- Private operating memory.
- Protected local operating state.
- Framework layer.
- Synthetic example.
- Sanitized export.
- Encrypted backup.

Avoid describing privacy as an "ignored file" feature in user-facing docs. Git and GitHub mechanics belong in implementation, verification, and contributor guidance.

## Sharing Rules

PEGO must not disclose private subject information to public repositories, third-party tools, logs, prompts, screenshots, examples, or documentation unless the subject explicitly approves a sanitized export.

Sanitized exports must remove:

- Names and identifying facts.
- Exact account balances, net worth, holdings, salaries, and transactions.
- Health details.
- Relationship and household context.
- Employer, customer, and work details.
- Locations, routines, and calendar details.
- Secrets, credentials, tokens, and account identifiers.

## Durability

Protected private operating state should eventually have an encrypted backup and recovery policy.

Minimum requirements:

- Private data remains outside the reusable framework layer by default.
- Backups are encrypted before leaving the local machine.
- Recovery procedures are tested.
- Sensitive files are not copied into public issue trackers, shared prompts, analytics, or support channels.
- Any external storage provider is treated as a third party and reviewed under governance.

## Governance

Any operation that moves private instance content outside protected local storage is privacy-impacting and requires governance review.

Public framework work may define structures for private data, but must use templates or synthetic examples only.
