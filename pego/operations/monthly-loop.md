# Monthly Strategy Loop

The monthly strategy loop evaluates whether PEGO is still governing toward the right life.

Daily and weekly loops optimize execution. The monthly loop reviews strategy, goals, assumptions, agent performance, and constitutional fit.

## Inputs

- Constitution.
- Active goals and goal strategies.
- Current state.
- Monthly outcome summaries.
- Financial, health, career, relationship, exploration, happiness, and operations agent assessments.
- Governance reviews and escalations.
- New human concerns or objections.
- Significant life changes.
- Anticipation scans for the next 30-90 days.
- Current operating register.

## Steps

1. Review the prior month's outcomes.
2. Compare outcomes against active goals and leading indicators.
3. Identify where PEGO created progress, friction, drift, or harm.
4. Reassess goal strategy using `pego/templates/goal-strategy.md`.
5. Reconcile active goals using `pego/operations/goal-reconciliation.md`.
6. Reassess the happiness model and protected-time fit.
7. Review financial runway, health trend, career capital, relationship impact, and exploration portfolio.
8. Run a 30-90 day anticipation scan using `pego/operations/anticipation-loop.md`.
9. Update strategic priorities for the next month.
10. Identify decisions requiring formal review.
11. Propose amendments only if the constitution no longer fits reality.
12. Produce the monthly strategy review using `pego/templates/monthly-strategy-review.md`.

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
