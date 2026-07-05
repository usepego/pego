# Council Decision Packet

Use this packet when PEGO reconciles multiple agent recommendations into one directive, revision request, information request, or escalation.

Structured implementations should emit `pego/schemas/council-decision.schema.json`.

## Date

Date.

## Decision Frame

The concrete decision or directive being reconciled.

## Goal Reconciliation Status

Current goal reconciliation supplied / Temporary priority assumption / Missing goal reconciliation.

## Goal Reconciliation Sources

Which goal reconciliation artifacts were consulted, if any.

## Priority Assumption

The council priority model or temporary conservative assumption used when
selecting, deferring, escalating, or requesting information.

## Source Recommendations

Which agent recommendations were considered.

## Proposed Directive

The directive or decision PEGO should adopt next, if any.

## Council Outcome

Adopt / Revise / Request more information / Escalate / Block.

## Rationale

Why this outcome best fits goals, constraints, evidence, and authority.

## Expected Benefit

What improves if this outcome is followed.

## Key Risks

Financial / Health / Relationship / Career / Legal / Tax / Privacy / Reputation / Time / Energy / Psychological / Opportunity cost.

## Dissent

Preserve the strongest opposing agent views.

## Deliberation Summary

Claims, objections, concessions, evidence gaps, vetoes, and unresolved dissent.
Keep this compact enough for outcome review.

## Tradeoff Rationale

Why Council selected, revised, escalated, blocked, or requested information
instead of the other available recommendations.

## Tradeoff Scorecard

One deterministic row per source recommendation: agent, selection status,
directive, authority, risks, evidence quality, and calibration adjustment.

## Agent Calibration Context

Agent calibration records consulted for recommendation weighting, including
score deltas, calibration actions, cautions, and future weighting notes.

## Deferrals

Recommendations or benefits preserved for later review because Council selected
a different next action, requested information, escalated, revised, or blocked.

## Required Handoffs

Agents, governance reviews, decision packets, or context updates required before adoption.

## Governance Status

Authority, privacy, protected-time, stakeholder, reversibility, and evidence status.

## Stop Conditions

What should cause PEGO to stop, revise, or escalate.

## Next Action

The smallest safe next action.

## Review

When or how this council decision should be reviewed.
