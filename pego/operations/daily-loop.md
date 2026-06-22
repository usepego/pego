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
3. If health state could change food, movement, sleep, or recovery directives, generate a targeted health check-in using `pego/templates/health-check-in.md`.
4. If finance state could change finance/admin, career, venture, spending, runway, or governance directives, generate a targeted finance check-in using `pego/templates/finance-check-in.md`.
5. Normalize recommendations using `pego/templates/agent-recommendation.md`.
6. If recommendations conflict, carry dissent, or involve cross-domain tradeoffs, synthesize a council decision using `pego/templates/council-decision.md`.
7. Convert competing recommendations or council-approved next actions into directive candidates using `pego/templates/directive-candidate.md`.
8. Synthesize candidates using `pego/operations/directive-synthesis.md`.
9. Select the minimum useful set of directives.
10. Assign authority level and governance status.
11. Produce the daily directive packet using `pego/templates/daily-directive.md`.
12. Produce or update the live directive queue using `pego/templates/directive-queue.md`.
13. Use `pego/operations/intra-day-command-loop.md` when the human reports status or asks what is next.
14. Execute only approved low-risk actions.
15. Review outcomes at the end of the day using `pego/operations/outcome-review.md`.

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

If the next plausible directive is health-related and the current state is stale or ambiguous, PEGO should ask a targeted health check-in question before selecting the directive. The question must be tied to a decision such as meal default, movement intensity, recovery priority, stop condition, or escalation. Do not ask for new biomarker tracking unless the measurement would change a directive, risk classification, escalation, or strategy review.

If the next plausible directive is finance-related and the current state is stale or ambiguous, PEGO should ask a targeted finance check-in question before selecting the directive. The question must be tied to a decision such as assumption refresh, scenario rerun, runway protection, upcoming spending, tax/admin lead time, account-data recency, or governance escalation. Do not ask for balances, holdings, or transaction details unless the protected private destination and decision use are clear.

If agent recommendations disagree, require handoffs, or contain risk that changes authority, PEGO should produce a council decision before selecting the next directive. The council output should preserve dissent and either adopt, revise, request information, escalate, or block the proposed directive.

## Governance

Any directive that changes protected time, creates material financial impact, affects a spouse/partner or protected stakeholder, or has meaningful health/career/legal risk must pass the appropriate governance review before execution.

High-impact actions must be converted into a decision packet using `pego/templates/decision-packet.md`; they should not be hidden inside a daily directive.

## Local Runner

The reference daily directive generator lives at:

```text
ops/directives/generate_daily_directive.py
```

It writes generated daily packets into the protected private instance.

The reference daily cycle runner lives at:

```text
ops/cycles/daily_cycle.py
```

It composes the local `health-check-in`, `finance-check-in`, `council`, `synthesize`, `next`, `outcome`, `review`, and `learn` operations for active daily use.

To generate a targeted health check-in through the daily runner:

```sh
python3 ops/cycles/daily_cycle.py health-check-in
```

To generate a targeted finance check-in through the daily runner:

```sh
python3 ops/cycles/daily_cycle.py finance-check-in
```

To synthesize a council decision through the daily runner:

```sh
python3 ops/cycles/daily_cycle.py council --recommendation private/agents/recommendations/example.json
```
