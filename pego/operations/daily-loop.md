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
- Anticipation scan for today and tomorrow.
- Current operating register.

## Steps

1. Gather approved or draft recommendations.
2. Check protected time and hard constraints.
3. Normalize recommendations using `pego/templates/agent-recommendation.md`.
4. Convert competing recommendations into directive candidates using `pego/templates/directive-candidate.md`.
5. Synthesize candidates using `pego/operations/directive-synthesis.md`.
6. Select the minimum useful set of directives.
7. Assign authority level and governance status.
8. Produce the daily directive packet using `pego/templates/daily-directive.md`.
9. Produce or update the live directive queue using `pego/templates/directive-queue.md`.
10. Use `pego/operations/intra-day-command-loop.md` when the human reports status or asks what is next.
11. Execute only approved low-risk actions.
12. Review outcomes at the end of the day using `pego/operations/outcome-review.md`.

Before selecting directives, run a short anticipation scan using `pego/operations/anticipation-loop.md`.

The daily scan should look for immediate friction: missing food defaults, schedule conflicts, visible environmental irritants, weather-dependent maintenance, upcoming event prep, or tomorrow's first blocker.

If the scan identifies a future condition that should not be scheduled today, add or update an operating-register entry instead of expanding the daily plan.

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

Use `pego/templates/directive-outcome.md` for outcome records.

## Intra-Day Use

The daily directive is not the only interaction point.

During the day, PEGO may resynthesize the next directive when the human reports completed work, blocked work, available time, energy, location, or new constraints.

The output should be one next directive, not a full replanning exercise, unless the day has materially changed.

If the human asks what is next after reporting status, PEGO should consider whether the next useful directive is preventive rather than reactive. Example categories include preparing for a known event, buying a missing default food, or handling the most visible environmental irritant before it becomes a larger annoyance.

## Governance

Any directive that changes protected time, creates material financial impact, affects a spouse/partner or protected stakeholder, or has meaningful health/career/legal risk must pass the appropriate governance review before execution.

High-impact actions must be converted into a decision packet using `pego/templates/decision-packet.md`; they should not be hidden inside a daily directive.

## Local Runner

The reference local runner lives at:

```text
ops/directives/generate_daily_directive.py
```

It writes generated daily packets to ignored local private files.
