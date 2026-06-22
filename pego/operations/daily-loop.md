# Daily Operating Loop

The daily loop converts PEGO's current understanding into a small set of executable directives.

## Inputs

- Constitution.
- Protected time.
- Current state.
- Active goals.
- Agent recommendations.
- Governance reviews.
- Calendar or availability.
- Recent outcomes.
- New concerns.

## Steps

1. Gather approved or draft recommendations.
2. Check protected time and hard constraints.
3. Normalize recommendations using `pego/templates/agent-recommendation.md`.
4. Convert competing recommendations into directive candidates using `pego/templates/directive-candidate.md`.
5. Synthesize candidates using `pego/operations/directive-synthesis.md`.
6. Select the minimum useful set of directives.
7. Assign authority level and governance status.
8. Produce the daily directive packet using `pego/templates/daily-directive.md`.
9. Execute only approved low-risk actions.
10. Review outcomes at the end of the day.

## Directive Limits

Until the system has real outcome data, daily packets should stay small:

- 1 primary work directive.
- 1 health movement directive.
- 1 food/default directive.
- 0-1 finance/admin directive.
- Protected time explicitly preserved.

## Review Questions

- What was completed?
- What failed?
- What created friction?
- What produced energy?
- What should PEGO change tomorrow?

## Governance

Any directive that changes protected time, creates material financial impact, affects a spouse/partner or protected stakeholder, or has meaningful health/career/legal risk must pass the appropriate governance review before execution.

High-impact actions must be converted into a decision packet using `pego/templates/decision-packet.md`; they should not be hidden inside a daily directive.

## Local Runner

The reference local runner lives at:

```text
ops/directives/generate_daily_directive.py
```

It writes generated daily packets to ignored local private files.
