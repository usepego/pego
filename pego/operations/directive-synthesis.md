# Directive Synthesis

Directive synthesis is the process that converts agent recommendations at different altitudes into a finite, scheduled operating plan.

PEGO must not treat all valid directives as simultaneously executable. A person cannot cook, weed the garden, build a business, exercise, work, and rest at the same time. The Operations Agent owns synthesis, but all agents must provide recommendations in a form that can be compared, scheduled, deferred, or escalated.

## Governance Altitudes

PEGO should classify work by altitude before scheduling it.

### Altitude 0: Constitution

Purpose, values, non-negotiables, authority grants, and stop conditions.

Cadence: amended rarely.

### Altitude 1: Life Strategy

Major outcomes, multi-year paths, financial freedom, health trajectory, career or venture direction, household strategy, and happiness model.

Cadence: monthly or when circumstances materially change.

### Altitude 2: Programs

Ongoing domains of work.

Examples:

- Build a business capable of producing target income.
- Lose weight sustainably.
- Preserve home serenity and garden quality.
- Build career capital.
- Support important relationships.

Cadence: weekly and monthly.

### Altitude 3: Projects

Finite projects that advance a program.

Examples:

- Define three venture theses.
- Build a first market test.
- Create a 7-day breakfast default.
- Clear weeds from one garden bed.

Cadence: weekly.

### Altitude 4: Directives

Concrete actions for a day or week.

Examples:

- Eat a protein/fiber breakfast tomorrow.
- Weed the front bed for 25 minutes before it becomes visually stressful.
- Spend 60 minutes on venture thesis selection.

Cadence: daily or weekly.

### Altitude 5: Scheduled Blocks

Time-boxed execution slots.

Examples:

- 8:15-8:35: walk.
- 12:15-12:40: garden maintenance.
- 14:00-15:00: venture research.

Cadence: daily.

## Directive Candidate Shape

Each agent recommendation that might become a directive should specify:

- Altitude.
- Domain.
- Proposed action.
- Target behavior.
- Environment design.
- Duration.
- Deadline or recurrence.
- Energy required.
- Location required.
- Dependencies.
- Protected-time impact.
- Expected happiness or goal benefit.
- Consequence of deferral.
- Lead time required to prevent scrambling.
- Authority level.
- Governance status.
- Stop condition.

Use `pego/templates/directive-candidate.md`.

PEGO should favor directives that alter future action conditions when direct instruction is likely to be weak. A directive can be strategically indirect: the named action may be "walk the block," while the intended behavioral effect is exposure to neighbors, daylight, movement, and a low-friction transition out of indoor inertia.

## Private Facts To Directives

Private facts are not passive profile data. They are operating material.

PEGO should convert private facts into directive candidates when they imply:

- A resource that can be used.
- A constraint that must be protected.
- A recurring annoyance that should be prevented.
- A missing fact that blocks a decision.
- A health, finance, venture, relationship, or home default that should be
  changed.
- A future event that needs lead-time preparation.

The conversion should preserve the chain:

```text
private fact -> inference -> agent recommendation -> council decision -> directive candidate -> queue -> command response -> outcome
```

Agents must distinguish known facts from inference at each step. If the private
fact is stale, uncertain, or missing, the correct output is often a targeted
question or evidence-gathering directive rather than a broad plan.

Examples:

- Current salary and runway imply that quitting a job is an escalation, while a
  venture evidence task is a low-risk directive.
- A desire to invest differently implies an investment policy or holdings review
  before trade execution.
- A weight-loss goal and known lunch friction imply a next-meal directive and a
  grocery-default directive.
- Visible home deterioration implies a maintenance directive before the
  environment becomes aversive.

Council decisions are not scheduled directly. A council decision must first be converted into a directive candidate so adoption, revision, information requests, and escalation all pass through the same prioritization and governance gates.

The conversion rule is:

- Adopted decisions become operations candidates for the proposed directive.
- Revision decisions become governance candidates to revise and rerun council synthesis.
- Information requests become governance candidates to answer the missing decision-grade question.
- Escalations stay escalated and should be deferred by queue synthesis until the required governance review or decision packet exists.

## Synthesis Rules

The Operations Agent should:

1. Collect candidate directives.
2. Reject or revise candidates that violate the constitution.
3. Split broad candidates into smaller actions.
4. Compare candidates by urgency, importance, reversibility, happiness impact, and consequence of deferral.
5. Protect sleep, meals, relationship time, and recovery first.
6. Reserve capacity for work and income protection unless strategy says otherwise.
7. Schedule only what fits the day.
8. Defer unscheduled candidates explicitly rather than silently dropping them.
9. Preserve dissent when an important candidate is deferred.
10. Preserve lead-time candidates when a small early action prevents a larger future interruption.
11. Prefer environmental setup over repeated exhortation when a person has already failed to act on a rational instruction.

## Prioritization Heuristic

Use this order unless the constitution or governance review says otherwise:

1. Non-negotiables, health/safety, privacy, and protected relationships.
2. Existing commitments and income protection.
3. Time-sensitive maintenance that prevents visible or emotional deterioration.
4. Compounding strategic work toward major goals.
5. Health defaults that are small enough to repeat.
6. Administrative tasks that unblock future work.
7. Exploration, comfort, and optional polish.

## Maintenance Matters

PEGO should treat environmental maintenance as legitimate life governance.

A small recurring directive can be more valuable than a delayed recovery project. If weeds, clutter, deferred repairs, poor food defaults, or missing supplies predictably degrade the operating environment, PEGO should schedule maintenance before the condition becomes aversive.

## Anticipation Matters

PEGO should treat future prep as a legitimate directive source.

Known events, seasonal changes, household needs, travel, meetings, dinners, deadlines, purchases, documents, reservations, and clothing requirements should be inspected before they become urgent. The result should be a targeted question or a small prep directive, not an open-ended reflection exercise.

## Scheduling Conflicts

When directives conflict:

- Prefer the smaller reversible action if evidence is weak.
- Prefer the action with the highest consequence of deferral.
- Prefer the action that protects the environment the person must live in.
- Prefer the action that preserves future optionality.
- Defer or shrink the lower-priority directive.
- Do not steal protected time without governance review.

Use `pego/governance/conflict-resolution.md` for meaningful conflicts.

## Output

Directive synthesis should produce:

- Selected directives.
- Scheduled or suggested time blocks.
- Deferred directives.
- Rationale for tradeoffs.
- Stop conditions.
- End-of-day review questions.

Use `pego/templates/synthesized-day-plan.md` when a directive set needs explicit scheduling.

Structured runtimes should preserve synthesized day plans and live directive queues using:

```text
pego/schemas/synthesized-day-plan.schema.json
pego/schemas/directive-queue.schema.json
```

## Local Runner

The reference queue synthesis runner lives at:

```text
ops/synthesis/synthesize_queue.py
```

It reads protected directive candidates and anticipation scans, then writes an active queue under:

```text
private/directives/queues/
```

The resulting queue is consumed by `ops/directives/next_directive.py` and `ops/operator/next_step.py`.

The reference council-decision bridge lives at:

```text
ops/council/decision_to_candidate.py
```

It reads protected council decisions and writes protected directive candidates under:

```text
private/directives/candidates/
```
