# Runtime Adapter Lifecycle

This file defines the minimum lifecycle a PEGO runtime adapter must support.

PEGO core remains runtime-neutral. A runtime adapter may be a local CLI, Codex
session, LangGraph deployment, Vercel interface, mobile app, Slack bot, custom
service, or another execution surface. The adapter's job is to preserve PEGO's
governance semantics while providing a concrete user experience.

## Lifecycle States

### 1. Initialize

Load public framework files, private operating state, adapter configuration, and
available tools.

Required checks:

- Confirm private data boundary.
- Confirm current collaboration mode.
- Confirm whether the adapter is in Engineering, UX, or USER mode.
- Confirm whether the private operating brief is available.
- Confirm the adapter has no unnecessary third-party access.

### 2. Intake

Accept new human input, telemetry, event data, schedule data, or status updates.

The adapter should classify input as one or more of:

- Goal update.
- Constraint update.
- Status update.
- Outcome report.
- New concern.
- New opportunity.
- New telemetry.
- Direct command.
- Governance objection.

### 3. Context Update

Convert durable facts, preferences, constraints, events, or patterns into
protected private memory using the context-update protocol.

The adapter must not write private facts into public framework files.

### 4. Agent Work

Select the correct PEGO role:

- Operator for active next-step use.
- Domain Agent for a domain-specific recommendation.
- Council for multi-domain reconciliation.
- Governance for authority, risk, privacy, reversibility, or dissent.

Agent outputs should use public PEGO schemas where structured data is available.

### 5. Directive Candidate Generation

Convert recommendations into directive candidates with enough structure for
synthesis.

Directive candidates must preserve:

- Domain.
- Altitude.
- Duration.
- Timing.
- Energy requirement.
- Location requirement.
- Dependencies.
- Expected benefit.
- Consequence of deferral.
- Protected-time impact.
- Authority level.
- Governance status.
- Stop condition.

### 6. Synthesis

The adapter must not present all valid directives as simultaneously executable.

Synthesis should produce one of:

- One next directive.
- A small daily queue.
- A weekly operating plan.
- A decision packet or escalation.
- A stop/review directive when no safe action fits.

### 7. Governance Review

Before adoption or execution, the adapter must evaluate authority, privacy,
risk, reversibility, protected time, stakeholders, evidence quality, and dissent.

High-impact actions must become decision packets. They should not be hidden
inside routine daily directives.

### 8. Directive Issue

The adapter gives the human a clear directive or command response.

Default output should include:

- State update.
- Next directive.
- Time box.
- Start condition.
- Reason selected.
- Fallback.
- Next check-in or review point.

### 9. Outcome Capture

After a directive is attempted, the adapter records what happened as evidence.

Outcome capture should preserve:

- Completion status.
- What happened.
- Evidence type.
- Friction.
- Benefit.
- Cost.
- Protected-time impact.
- Stakeholder impact.
- Environment impact.
- Follow-up candidates.
- Governance notes.

### 10. Learning

Convert outcomes into updates to:

- Operating register.
- Context memory.
- Agent models.
- Goal strategy.
- Constraints.
- Future directive selection.

Learning should be conservative. A single outcome may create a provisional
pattern, but durable model changes should require stronger evidence unless the
outcome reveals a safety, privacy, or constitutional issue.

## Required Adapter Commands

A PEGO runtime adapter should expose these commands or equivalents:

- `brief`: summarize current operating frame and active queue.
- `next`: select one next directive.
- `resynthesize`: update the active queue after material change.
- `record_outcome`: capture result of a directive.
- `update_context`: record durable new context.
- `review_goals`: review goals, strategy, assumptions, and constraints.
- `governance_review`: review authority, privacy, risk, and alignment.
- `stop`: halt or downgrade when authority or context is insufficient.

## Adapter Invariants

- Public framework files remain free of private subject facts.
- Protected private files stay under the private instance boundary.
- Runtime convenience must not weaken authority levels.
- Governance review must precede high-impact action.
- Dissent must be preserved when tradeoffs are real.
- The adapter must be able to explain why a directive was selected.
- The adapter must be able to record outcomes and update future selection.
- Missing context should produce a targeted question only when it would change
  the directive.

## Failure Modes

An adapter should stop, downgrade, or escalate when:

- Authority is ambiguous.
- Private data may leak.
- Required context is stale or missing.
- A directive touches financial, medical, legal, tax, career, relationship,
  housing, privacy, or hard-to-reverse action.
- The adapter cannot preserve protected time.
- It cannot distinguish a recommendation from execution.
- It cannot record the outcome of an issued directive.
