# Compliance Review

Every meaningful PEGO directive should be evaluated for constitutional alignment, risk, evidence quality, constraints, privacy, reversibility, and goal fit.

The Governance Agent owns this review.

## Review Levels

### Light Review

Use for low-risk Level 1 and Level 2 recommendations.

Required checks:

- Aligns with constitution.
- Supports at least one active goal.
- Does not violate known constraints.
- Is feasible with current resources.
- Has a review point or success condition.

### Standard Review

Use for repeated directives, meaningful lifestyle changes, financial choices, health behavior changes, work strategy, and any recommendation involving another person.

Required checks:

- Constitutional alignment.
- Goal alignment.
- Constraint fit.
- Evidence quality.
- Risk assessment.
- Reversibility.
- Privacy impact.
- Dissenting view.
- Opportunity cost.
- Review cadence.

### Formal Review

Use for Level 4 escalations and high-impact actions.

Required checks:

- Full decision packet using `pego/templates/decision-packet.md`.
- Scenario analysis.
- Dissent from relevant agents.
- Waiting period recommendation.
- External professional review if legal, medical, tax, or financial-advice risk exists.
- Explicit human approval.
- Audit record.

## Compliance Questions

Before a directive is accepted, ask:

- Does this violate any non-negotiable?
- Does this protect the primary subject's privacy?
- Does this use the minimum required repository, app, OAuth, or API access?
- Does this protect spouse/partner, family, or other protected stakeholder happiness and lack of disturbance where relevant?
- Does this preserve protected time unless override conditions are met?
- Does this improve or reasonably serve the top-level aim?
- Which goals does it advance?
- Which goals might it harm?
- What evidence supports it?
- What assumptions are uncertain?
- What is the downside?
- Is the action reversible?
- What is the smallest useful version of the action?
- What should cause PEGO to stop, reverse, or revise?

## Evidence Quality

Classify evidence:

- Direct telemetry.
- Financial model output.
- Human report.
- Repeated observed pattern.
- Expert source.
- Agent inference.
- Speculation.

Low-quality evidence does not block all action, but it should reduce confidence, scope, and authority level.

## Risk Classes

Classify risks:

- Financial.
- Health.
- Relationship.
- Career.
- Legal.
- Tax.
- Privacy.
- Reputation.
- Time.
- Energy.
- Psychological.
- Opportunity cost.

## Outcome

Each review should produce one of:

- Approve.
- Approve with constraints.
- Request more information.
- Downgrade authority level.
- Escalate.
- Reject.

## Auditability

High-impact decisions should leave an audit trail:

- Date.
- Directive or decision.
- Agents involved.
- Evidence.
- Assumptions.
- Risks.
- Dissent.
- Approval status.
- Review date.

## Templates

- Agent recommendation: `pego/templates/agent-recommendation.md`
- Decision packet: `pego/templates/decision-packet.md`
- Compliance review: `pego/templates/compliance-review.md`

## Conflict Resolution

Use `pego/governance/conflict-resolution.md` when agents, goals, values, constraints, evidence, authority, stakeholders, or time horizons conflict.

## Local Runner

The reference local runner lives at:

```text
ops/governance/generate_compliance_review.py
```

It writes generated review packets to ignored local private files.
