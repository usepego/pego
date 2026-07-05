# Agent Calibration Record

Use this template to preserve private evidence about how a specialist agent
should be weighted after outcome review.

Structured implementations should emit:

```text
pego/schemas/agent-calibration-record.schema.json
```

## Date

Date.

## Agent

Agent name and domain.

## Source Reviews

Outcome review, agent recommendation review, council synthesis review, or
other protected review artifacts that created this calibration evidence.

## Recommendation Usefulness

Strong / Adequate / Weak / Missing / Not applicable / Unknown.

## Score Delta

Small bounded calibration movement, normally -1, 0, or +1 from one outcome.

## Calibration Action

Increase weight / Keep weight / Decrease weight / Quarantine / Escalate.

## Friction Prediction

How well the agent predicted execution friction, blockers, energy, timing, or
context constraints.

## Evidence Quality

Whether the agent's claimed evidence was supported, overstated, speculative, or
missing.

## Stress Impact

Reduced / Preserved / Increased / Unknown.

## Missed Risks

Friction, stress, fit, authority, privacy, protected time, or other risk
classes the agent missed.

## Cautions

Limits on how future councils should weight this agent until more evidence
exists.

## Council Summary

One compact line Council can read during future deliberation.

## Future Weighting Note

What should change in future recommendations or weighting.

## Next Review

When this calibration evidence should be revisited.
