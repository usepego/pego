# PEGO User Journey

This document defines the intended user experience from first awareness through
first meaningful day-one operation.

The journey is not complete when PEGO is installed. It is complete when the
user receives, acts on, and reports the outcome of one governed directive that
clearly came from PEGO's agent and council model.

## Journey Principle

PEGO should feel like delegated executive governance becoming active.

The user should not feel that they are configuring a productivity app, filling
out a self-help workbook, or operating a developer tool. Setup exists only to
create enough trust, authority, and context for PEGO to govern safely.

## Stage 1: Awareness

### User State

The user has a felt problem:

- Too many life tradeoffs are being arbitrated manually.
- Goals, finances, health, work, relationships, and environment compete for
  attention.
- Existing tools capture information but do not decide what should happen next.
- The user wants stronger direction without giving up final authority.

### PEGO Message

PEGO is a Personal Executive Governance OS.

It turns goals, constraints, current state, and feedback into governed
directives: what to do next, what to defer, what to escalate, and what to
review.

### Surface

- Public site.
- Short demo.
- Synthetic directive examples.
- Architecture overview for technical users.

### Success

The user understands three things:

- PEGO is not a helper chatbot or dashboard.
- PEGO uses specialized agents and a council to choose directives.
- PEGO is constrained by privacy, authority, dissent, and review.

## Stage 2: Trust And Fit

### User Question

Before trying PEGO, the user needs to know:

- What will PEGO store?
- Where does private life data live?
- What authority does PEGO have?
- What will PEGO refuse to do?
- Can PEGO touch money, health, work, relationships, or private disclosure?

### PEGO Response

PEGO explains the boundary before asking for sensitive facts:

- Framework files are reusable and public-safe.
- The private instance contains real goals, constraints, telemetry, directives,
  and outcomes.
- High-impact actions require governance review.
- Default onboarding authority is Level 1: Recommend.
- The user can define stop rules and protected time before directives begin.

### Success

The user is willing to begin a protected private instance or hosted equivalent
because the authority and privacy boundary is clear.

## Stage 3: Start

### User Action

The user starts with a natural command:

```text
Start PEGO.
```

The user should not need to know the package manager, CLI command sequence,
repository structure, or adapter mechanics during normal operation.

### Adapter Responsibility

The adapter handles setup internally:

- Confirm private storage boundary.
- Load or create the private instance.
- Check readiness.
- Identify whether boundary onboarding is needed.
- Hide command output, file paths, diffs, and setup traces.

### User Sees

One of:

- A boundary question.
- A current-circumstance question.
- A domain-pressure question.
- A first directive.
- A governance stop condition.

### Success

The user experiences PEGO as an operating surface, not a developer console.

## Stage 4: Boundary Onboarding

### Goal

Create enough authority and privacy structure for PEGO to ask meaningful
questions without overreaching.

### PEGO Asks

```text
Before PEGO starts directing you, what is one thing PEGO must not disturb or
override?
```

Then, only if needed:

```text
What words or signal should pause PEGO immediately?
```

### PEGO Stores

- Initial privacy constraint.
- Stop rule.
- Default authority level.
- Protected-time boundary, if mentioned.

### Success

PEGO has permission to continue at Level 1 without creating authority confusion.

## Stage 5: Aim And Preservation

### Goal

Give the council a north star without forcing the user to design strategy.

### PEGO Asks

```text
What future state would make life clearly better, and what should PEGO preserve
even while pushing toward it?
```

If the answer is broad, PEGO should not ask for a complete plan. It should
extract aim, protected values, and candidate domains.

### PEGO Stores

- Desired state.
- Protected values.
- Initial happiness constraints.
- Candidate strategic domains.

### Success

Happiness, Governance, and Operations have enough context to reject directives
that optimize a proxy while harming the actual life objective.

## Stage 6: Current Circumstance

### Goal

Make the first directive fit the real day.

### PEGO Asks

```text
Where are you, how much time is available, what is your current energy, and
what is the next hard stop?
```

### PEGO Stores

- Location.
- Available time.
- Energy level.
- Next hard stop.
- Immediate constraints.

### Success

Operations can select only directives that fit the present moment.

## Stage 7: Domain Scan

### Goal

Expose the agent/council model early without overwhelming the user.

### PEGO Asks

```text
What is the main pressure PEGO should govern first: health/energy,
money/runway, career/work, venture creation, home, relationships, exploration,
or something else? Include what is true now and what must not be disturbed.
```

### Agent Interpretation

Each relevant agent converts the answer into a position:

- Health: energy, food, sleep, movement, recovery implications.
- Finance: runway, spending, risk, execution limits.
- Career: work leverage, reputation, autonomy, constraints.
- Venture: evidence, ownership, opportunity creation.
- Home: environment friction, maintenance, household serenity.
- Relationships: protected people, household impact, commitments.
- Exploration: curiosity, renewal, optionality.
- Happiness: whether the proposed direction serves the real objective.
- Governance: authority, privacy, reversibility, risk, dissent.
- Operations: what can be done next.

### Success

PEGO has enough information to produce either agent recommendations or one
more targeted missing-fact question.

## Stage 8: Council Synthesis

### Goal

Turn domain pressure into one governed next move.

### Internal Process

PEGO should:

1. Generate structured domain-agent recommendations.
2. Preserve dissent and uncertainty.
3. Check authority, risk, privacy, reversibility, and protected time.
4. Convert acceptable recommendations into directive candidates.
5. Select one next directive or one targeted question.

### User Sees

The user does not see the full council transcript by default. They see the
result:

```text
State update: PEGO has enough current state to begin.
Next directive: [one directive].
Time box: [duration].
Start condition: [when to start].
Do this: [concrete instruction].
Reason: [one-line reason].
Fallback: [blocked path].
Deferred: [what is intentionally not selected].
Next check-in: [what to report].
```

### Success

The directive feels selected, not suggested. It is small enough to execute and
governed enough to trust.

## Stage 9: Meaningful Day-One Objective

### Objective

By the end of day one, the user should complete one directive and report one
outcome that improves PEGO's future governance.

Day-one success is not "finish onboarding." Day-one success is:

```text
PEGO issued one governed directive.
The user attempted it.
The user reported completion, blockage, or objection.
PEGO recorded the outcome.
The next directive or next question became better because of that evidence.
```

### Good Day-One Directives

The first directive should be low-risk, concrete, and useful. Examples:

- Next meal: choose one clear protein plus one fiber item.
- Strategy: spend 25 minutes filling one evidence map for the active venture
  question.
- Home: clear one visible environmental friction for 20 minutes.
- Career: identify the next high-leverage work artifact and its blocker.
- Finance: list accounts, obligations, and unknowns without moving money.

The first directive should not require:

- Financial execution.
- Medical decisions.
- Career-risking action.
- Relationship confrontation.
- Public disclosure.
- Major purchases.
- Complex setup.

### Outcome Capture

After the directive, PEGO asks:

```text
Directive done, blocked, or objected? What happened, and how much time is
available now?
```

### Success

PEGO records:

- Completion status.
- Friction.
- Benefit or evidence.
- Follow-up candidate.
- Governance note, if needed.

## Stage 10: First Loop Closure

### Goal

Show that PEGO learns from execution.

### PEGO Responds

If completed:

```text
State update: [outcome captured].
Next directive: [next selected action or stop condition].
Reason: [one-line reason from the changed state].
```

If blocked:

```text
State update: blocker recorded.
Next directive: [fallback or resynthesis question].
Reason: the prior directive no longer fits the current constraints.
```

If objected:

```text
State update: objection recorded.
Next directive: pause or governance review.
Reason: PEGO should not push through an authority or fit objection.
```

### Success

The user sees that PEGO is not merely giving advice. It is governing a loop:

```text
state -> recommendation -> council -> directive -> outcome -> better state
```

## Day-One Acceptance Criteria

The first-use journey works when:

- The user understands PEGO's category before installation or start.
- Privacy and authority are clear before sensitive facts are requested.
- The user answers no more than one compact question at a time.
- The system asks about goals, circumstance, and domain pressure before trying
  to govern.
- Domain-agent recommendations and council synthesis exist behind the surface.
- The visible output remains one directive, one question, or one stop condition.
- The first directive is useful even if onboarding is incomplete.
- The user reports an outcome.
- PEGO updates the next interaction based on that outcome.

## Non-Goals For Day One

Day one should not require:

- A complete life plan.
- Complete financial data.
- Complete health telemetry.
- Calendar integration.
- Account linking.
- A polished mobile app.
- A full council transcript.
- Granting execution authority.

Day one should prove the governing loop, not collect everything PEGO may
eventually need.
