# Domain Baseline Bootstrap

Domain baseline bootstrap is the process PEGO uses when a net-new user or
under-modeled domain lacks enough private state for specialized agents to make
decision-grade recommendations.

Readiness means PEGO can operate safely. It does not mean PEGO has enough
context to govern well.

## Purpose

PEGO should be able to build useful baseline context through conversation when
the user has not uploaded spreadsheets, documents, telemetry, account data, or
other structured sources.

The goal is not complete data collection. The goal is enough state for agents
and council to choose better directives and better questions.

## Principle

Ask for rough decision-grade context before asking for precision.

PEGO may use:

- Rough estimates.
- Buckets.
- Unknown lists.
- Constraints.
- Non-negotiables.
- Recent examples.
- Current friction.

PEGO should not require:

- Full account linking.
- Complete spreadsheets.
- Continuous telemetry.
- Full inventories.
- Complete life plans.
- Exact financial, medical, or relationship details before the privacy and
  authority boundary is clear.

## Bootstrap Order

Default net-new sequence:

1. Boundary.
2. Aim.
3. Current state.
4. Happiness baseline.
5. Finance baseline.
6. Career baseline.
7. Health baseline.
8. Home baseline.
9. Relationships baseline.
10. Exploration baseline.
11. Communications baseline, if writing, public positioning, career, venture,
    or taste is active.
12. Goal reconciliation.
13. Authority.

The order may change when the user's immediate pressure requires it, but
Boundary must come first and Authority must be clear before execution.

## Domain Baseline Phases

Generate protected intake packets with:

```sh
python3 pegoctl intake --phase finance-baseline
python3 pegoctl intake --phase career-baseline
python3 pegoctl intake --phase home-baseline
python3 pegoctl intake --phase relationships-baseline
python3 pegoctl intake --phase exploration-baseline
python3 pegoctl intake --phase communications-baseline
python3 pegoctl intake --phase happiness-baseline
python3 pegoctl reconcile-goals
```

These are adapter mechanics. A normal USER-mode surface should ask one compact
question at a time and record answers under protected private state.

## Finance Baseline

Finance baseline should recreate the minimum useful structure that an uploaded
spreadsheet might have provided:

- Income sources and dependency.
- Rough take-home income.
- Rough monthly burn.
- Irregular annual expenses.
- Liquid savings and emergency runway.
- Retirement, taxable, crypto, real estate, private equity, and debt buckets.
- Major future costs.
- Goal lifestyle and downside backstop.
- Forbidden financial actions.
- Unknowns and confidence level.

Finance should not ask for credentials, exact account numbers, trades,
transfers, tax actions, or allocation instructions.

## Career Baseline

Career baseline should capture:

- Current role and compensation dependency.
- Responsibilities and current pressure.
- Skills, proof of work, network, reputation, and leverage.
- Dissatisfaction, risk, and constraints.
- Moves that require explicit approval.
- Employer-sensitive boundaries.

Career should not ask the user to decide whether to quit before PEGO has
modeled finance, household, health, and opportunity consequences.

## Health Baseline

Health baseline should capture:

- Current goal and current body/energy state if voluntarily known.
- Typical food defaults.
- Movement baseline and aversions.
- Sleep and recovery baseline.
- Medical constraints, injuries, and forbidden directives.
- Optional metrics already available and acceptable.
- Smallest movement or food action likely to happen.

Health should not require new biometric tracking unless the measurement would
change a directive, risk classification, escalation, or strategy review.

## Home Baseline

Home baseline should capture:

- What about the home or environment affects happiness most.
- Recurring irritants, maintenance risks, supply gaps, seasonal work, and pets.
- Household disturbance constraints.
- Major projects or purchases requiring governance review.

Home should not turn a maintenance scan into renovation planning.

## Relationships Baseline

Relationships baseline should capture:

- Protected people and stakeholders.
- Protected time.
- Recurring obligations.
- Disturbance, disclosure, and approval constraints.
- Stop conditions for relationship-impacting directives.

Relationships should not ask for private third-party detail unless needed for a
specific directive or governance review.

## Exploration Baseline

Exploration baseline should capture:

- Curiosity and renewal sources.
- Travel, games, sports, food, art, craft, places, learning, and experiences
  that make life richer.
- Exploration crowded out by other domains.
- Costs or constraints that require governance review.

Exploration should not become productivity homework.

## Communications Baseline

Communications baseline should capture:

- Voice and tone.
- Taste evidence.
- Public positioning goals.
- Opportunity goals.
- Topics, claims, and private material that require review.

Communications should not publish, post, or disclose without governance review.

## Happiness Baseline

Happiness baseline should capture:

- What creates peace, joy, pride, meaning, love, curiosity, beauty, competence,
  autonomy, and freedom.
- What creates regret, resentment, anxiety, shame, depletion, drift, or deadness.
- Proxy goals that could become traps.
- Discomfort worth choosing versus discomfort that should stop PEGO.

Happiness should prevent finance, productivity, health, career, or status from
becoming unexamined proxy objectives.

## Council Use

When a domain lacks baseline state, Council should decide whether to:

- Ask a baseline question now.
- Ask a narrower current-circumstance question.
- Infer cautiously and proceed.
- Defer the domain.
- Escalate or block.

Use `pego/templates/information-value-assessment.md` before asking the human
when the question could burden, stress, or interrupt them.

After enough domain baselines exist, Council should build or use
`pego/operations/goal-reconciliation.md` to turn separate goals into priority
rules. This is the dependency that lets Council select the best directive
across domains rather than simply selecting the clearest or most recent
candidate.

If the generated reconciliation reports missing baselines or a targeted
priority question, Council should ask that single highest-value question before
making high-impact tradeoffs.

## Completion Criteria

A domain baseline is usable when the domain agent can produce:

- One useful recommendation or dissent.
- One missing-fact question that would change a directive.
- One stop condition.
- One governance boundary.
- One outcome signal to review later.

The baseline is not required to be complete.

## USER-Mode Constraint

Do not show the user a checklist of all domains unless they ask for onboarding
status. In active operation, ask only the one question that changes the next
directive or materially improves future directive quality.
