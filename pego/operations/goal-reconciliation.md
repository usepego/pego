# Goal Reconciliation

Goal reconciliation turns separate domain goals into a council-usable priority
model.

Without reconciliation, PEGO may have many true goals but no governed way to
decide what wins when finance, health, career, home, relationships, exploration,
and happiness point in different directions.

Goal reconciliation is a dependency for Council directive selection. Council
cannot claim it selected the best directive across domains unless it has either
a current reconciliation model or a stated temporary assumption about goal
priority.

Council is responsible for trying to build the reconciliation, not merely
checking whether one already exists. If no current reconciliation exists, the
runtime should first inspect protected private state and generate a draft
reconciliation. Only after that attempt should it ask the human for missing
priority context.

## Purpose

Goal reconciliation should answer:

- Which goals are active now?
- Which goals are constitutional, strategic, tactical, or experimental?
- Which goals protect the downside?
- Which goals create upside?
- Which goals preserve happiness, relationships, health, and protected time?
- Which goals conflict?
- What tradeoffs may PEGO make without asking?
- What tradeoffs require a targeted question or governance review?
- Which goals should dominate daily directive selection?

## Inputs

- Constitution.
- Happiness model.
- Active domain goals.
- Goal strategy artifacts.
- Current state.
- Protected time.
- Financial, health, career, home, relationship, exploration, venture, and
  operations baselines.
- Recent outcomes.
- Human objections.
- Governance reviews.

## Output

Use:

```text
pego/templates/goal-reconciliation.md
```

Structured runtimes should preserve reconciliations using:

```text
pego/schemas/goal-reconciliation.schema.json
```

The local reference runner is:

```sh
python3 pegoctl reconcile-goals
```

It reads protected private state, writes:

```text
private/goals/goal-reconciliation.md
private/goals/goal-reconciliation.json
```

and records missing baselines, targeted questions, temporary assumptions, and
stop conditions when the source evidence is incomplete.

## Reconciliation Classes

### Constitutional

Goals or constraints that PEGO must preserve even when they slow other goals.

Examples:

- Protected relationships.
- Health and safety.
- Privacy.
- Agency and dignity.
- Sleep and recovery.

### Strategic

Long-range goals that define direction but usually require projects, evidence,
and tradeoff modeling before major action.

Examples:

- Financial freedom.
- Independent income.
- Home serenity.
- Health trajectory.

### Operational

Goals that should affect daily directive selection.

Examples:

- Next-meal default.
- Work focus block.
- Maintenance scan.
- Outcome capture.

### Experimental

Goals that PEGO should explore without overcommitting.

Examples:

- New venture thesis.
- Public writing direction.
- Skill acquisition.
- Exploration portfolio.

## Tradeoff Rules

For each meaningful conflict, define:

- Default priority.
- Why the priority exists.
- When the lower-priority goal may temporarily win.
- What evidence would change the priority.
- Whether human confirmation is required.
- Whether governance review is required.

Examples:

- Financial freedom may not override protected relationship time by default.
- Health recovery may override routine productivity.
- Career income protection may defer venture work until a safe window exists.
- Home serenity may deserve small recurring directives but not unreviewed major
  renovation spending.

## Council Use

Council should build or consult the goal reconciliation before selecting a
directive.

If no current goal reconciliation exists, Council must do one of:

- Build one from protected private state, then use it if it is adequate for the
  decision.
- Ask the smallest priority question that would change the directive.
- Use a conservative temporary priority assumption and state it in the council
  decision.
- Select only a low-risk information-gathering or baseline directive.
- Escalate or block if the tradeoff affects protected time, relationships,
  health, finance, career, privacy, housing, legal, tax, or other high-impact
  areas.

When agents disagree, Council should ask:

- Which active goal does each recommendation serve?
- Which protected goal could it harm?
- Is the conflict constitutional, strategic, operational, or experimental?
- Does the recommendation create evidence for a larger goal?
- Does it reduce future anxiety or merely avoid a hard decision?
- Would a targeted question change the priority?

The council output should still be one directive, one targeted question, one
deferral, or one escalation.

## Information Requests

If goals cannot be reconciled from existing state, PEGO should ask the smallest
question that changes priority.

Use:

```text
pego/templates/information-value-assessment.md
```

Question examples:

- Which is more important to preserve this week: income protection or venture
  evidence?
- Is the current health constraint strong enough to downgrade work intensity
  today?
- Is this home issue an annoyance, a safety problem, or a relationship
  disturbance?

Do not ask the human to rank the entire life. Ask only the missing tradeoff
needed for the next directive or strategy review.

## Review Cadence

Review goal reconciliation:

- During first-run onboarding after baseline phases.
- Monthly.
- After major outcomes or repeated directive failures.
- After new financial, health, career, relationship, housing, or privacy facts.
- Whenever the human objects that PEGO is optimizing the wrong thing.

## Failure Modes

Goal reconciliation is failing if:

- PEGO selects directives from one domain while ignoring repeated harm in
  another.
- Financial, career, health, or productivity proxies dominate happiness.
- Protected relationships or sleep become residual time.
- Council decisions do not explain deferrals.
- The human feels PEGO is adding anxiety by keeping too many goals active.
- Goals remain as separate wish lists rather than a governed priority model.
