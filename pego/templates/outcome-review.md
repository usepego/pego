# Outcome Review Packet

Use this packet to convert a directive outcome into a learning decision.

Structured implementations should emit
`pego/schemas/outcome-review.schema.json`.

## Date

Date.

## Source Outcome

Path or reference.

## Directive

Directive reviewed.

## Completion Class

Completed / Partially completed / Not completed / Blocked / Canceled.

## Evidence Summary

Facts separated from interpretation.

## Friction Summary

What made execution harder?

## Benefit Summary

What improved?

## Outcome Progress

What intended outcome became more real or better understood?

## Contentment Signal

More contentment / Less contentment / No material change / Unknown.

## Cost Summary

What did it consume, disrupt, or delay?

## Learning Decision

Repeat / Reduce / Split / Reschedule / Stop / Escalate / Gather more information.

## Queue Implication

Keep active / Add follow-up candidate / Defer / Remove / Block pending dependency / Escalate to decision packet.

## Context Update Recommendation

No update / Record provisional pattern / Update durable preference / Update constraint / Update goal or strategy / Governance review.

## Agent Routing

Which agents should use this evidence?

## Governance Status

Authority, privacy, protected-time, stakeholder, and risk review status.

## Decision Quality Review

Use `pego/templates/decision-quality-review.md` to evaluate whether PEGO made a
good decision, not only whether the directive was completed.

Baseline comparison: unmanaged prioritization / generic assistant advice /
to-do list plan / single-domain recommendation / council without goal
reconciliation / council with goal reconciliation / unknown.

Minimum dimensions:

- Actionability.
- Goal fit.
- Constraint fit.
- Burden.
- Timeliness.
- Risk control.
- Explanation quality.
- Follow-through probability.
- Outcome quality.
- Learning value.

## Decision Quality Assessment

Improved decision quality / Mixed / Poor fit / Insufficient evidence.

## Human Burden

Questions asked, answer burden, and whether the information request was worth
the decision improvement it enabled.

## Next Architecture Adjustment

What should change in agent recommendations, council synthesis, goal
reconciliation, information requests, directive phrasing, or outcome capture?

## Decision Quality Notes

Facts and interpretation that explain the quality assessment.

## Council Synthesis Review

If the outcome came from a council decision, preserve whether Council selected,
deferred, escalated, blocked, or requested information well.

Minimum dimensions:

- Selection quality.
- Dissent handling.
- Information timing.
- Human burden.
- Governance fit.

## Agent Recommendation Reviews

If source agent recommendations are available, preserve one review per relevant
agent. Include fit assessment, friction prediction, information request
quality, stress impact, evidence quality, dissent quality, review outcome, and
future adjustment.

## Agent Calibration Records

If attribution is strong enough, generate bounded private calibration evidence
using `pego/templates/agent-calibration-record.md`. One outcome may move an
agent only slightly; durable weighting changes should require repeated evidence
unless safety, privacy, authority, or protected-time risk appears.

## Next Review

When this evidence should be reviewed again.
