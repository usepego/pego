# Monthly Strategy Loop

The monthly strategy loop evaluates whether PEGO is still governing toward the right life.

Daily and weekly loops optimize execution. The monthly loop reviews strategy, goals, assumptions, agent performance, and constitutional fit.

## Inputs

- Constitution.
- Active goals and goal strategies.
- Current state.
- Monthly outcome summaries.
- Outcome reviews and nested decision-quality reviews.
- Agent calibration records.
- Durable goal progress records.
- Behavior loop records and disruption candidates.
- Synthetic scenario benchmark summaries.
- Financial, health, career, venture, home/environment, relationship,
  exploration, communications, happiness, operations, and governance agent
  assessments.
- Governance reviews and escalations.
- New human concerns or objections.
- Significant life changes.
- Anticipation scans for the next 30-90 days.
- Current operating register.

## Steps

1. Review the prior month's outcomes.
2. Compare outcomes against active goals and leading indicators.
3. Summarize decision quality, council synthesis quality, and learning decisions.
4. Summarize agent calibration records and identify weighting cautions.
5. Compare goal progress records against active goals and leading indicators.
6. Review active behavior loops before increasing directive recurrence.
7. Review synthetic scenario benchmark results before expanding public or research-facing claims.
8. Identify where PEGO created progress, friction, drift, or harm.
9. Reassess goal strategy using `pego/templates/goal-strategy.md`.
10. Reconcile active goals using `pego/operations/goal-reconciliation.md`.
11. Reassess the happiness model and protected-time fit.
12. Review financial runway, health trend, career capital, relationship impact, and exploration portfolio.
13. Run a 30-90 day anticipation scan using `pego/operations/anticipation-loop.md`.
14. Update strategic priorities for the next month only when evidence supports the change.
15. If evidence is thin, produce targeted evidence-gathering directives instead of broad strategy changes.
16. Identify decisions requiring formal review.
17. Propose amendments only if the constitution no longer fits reality.
18. Produce the monthly strategy review using `pego/templates/monthly-strategy-review.md`.

Structured runtimes should preserve monthly strategy reviews using:

```text
pego/schemas/monthly-strategy-review.schema.json
```

## Monthly Strategy Questions

- Is PEGO moving current conditions toward the stated desired outcomes?
- Which goals advanced?
- Which goals stalled?
- Which assumptions were wrong?
- Which directives worked better than expected?
- Which directives created hidden costs?
- Did PEGO protect relationships, health, privacy, and protected time?
- Did PEGO underuse current resources?
- Did PEGO avoid a needed decision?
- Did PEGO anticipate events, seasonal needs, prep work, and recurring annoyances early enough?
- Which register entries reveal a strategy, goal, or constitution change?
- Which strategy should change next month?
- Which goal conflicts need explicit priority rules before Council selects
  cross-domain directives?
- Which agents should carry more or less weight after outcome evidence?
- Which behavior loops should be disrupted before repeating directives?
- Is evidence strong enough for a strategy change, or should PEGO gather
  targeted evidence first?
- Did synthetic benchmarks reveal a failure mode that should change council
  governance before public claims expand?

## Agent Review

Each agent should answer:

- What did this domain learn?
- What should continue?
- What should stop?
- What should change?
- What evidence is missing?
- What dissent should be preserved?

## Governance

The monthly loop may recommend strategy changes, but high-impact decisions still require formal review.

Constitutional amendments should be proposed only when repeated outcomes, new evidence, or changed circumstances show that the constitution no longer governs well.

Monthly governance review items should include authority, privacy,
protected-time, constitutional, calibration, behavior-loop, and benchmark
concerns that should affect next-month strategy or public claims.

## Local Runner

The reference monthly cycle runner lives at:

```text
ops/cycles/monthly_cycle.py
```

It writes protected private monthly strategy reviews and structured JSON under
`private/directives/monthly/` by default. For installed or backed-up operation,
pass `--private-root` or set `PEGO_PRIVATE_ROOT` so the review uses the
protected private instance instead of the framework checkout.

The local wrapper is:

```sh
python3 pegoctl monthly --month YYYY-MM
```
