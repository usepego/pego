# Context Update

Context update is how PEGO converts new information into durable operating memory.

New context may come from conversation, outcomes, telemetry, documents, external events, or repeated directive results. PEGO should update private state deliberately instead of letting important information disappear into chat history.

## Purpose

Context update should determine:

- What new fact, preference, constraint, goal, or pattern was learned.
- Which private file should change.
- Whether the update is stable or provisional.
- Which agents need to use the update.
- Whether governance review is needed.

## Inputs

- New human statement.
- Directive outcome.
- Session log.
- Telemetry.
- Financial model result.
- Agent observation.
- External professional input.
- Repeated pattern.

## Update Classes

### Fact

Stable or currently true information.

Examples:

- Current asset.
- Current role.
- Current constraint.
- Current tool.

### Preference

A practical preference that should affect directives.

Examples:

- Food preference.
- Communication preference.
- Work style.
- Exercise aversion.

### Constraint

A hard or soft limit.

Examples:

- Protected time.
- Budget.
- Household disruption limit.
- Energy limit.

### Goal

Desired outcome or domain objective.

### Strategy

Current thesis for reaching a goal.

### Pattern

Repeated outcome, behavior, friction, or success condition.

### Tone Rule

Communication style that improves or degrades operating performance.

### Voice Rule

Writing or speaking style rule that should affect PEGO drafts, directives, and public artifacts.

### Taste Signal

Object, work, place, tool, person, or idea that reveals judgment, aesthetics, or preferred sophistication.

### Influence

Something read, watched, listened to, built, learned, practiced, or experienced that should inform PEGO's model of the person.

### Public Positioning

How the person wants to be perceived by future employers, collaborators, customers, readers, investors, or peers.

### Governance Rule

Authority, privacy, escalation, or stop-condition update.

## Destination Files

Use private files for instance-specific updates:

- `private/person/profile.md`
- `private/person/preferences.md`
- `private/person/tone.md`
- `private/person/voice-and-taste.md`
- `private/writing/`
- `private/person/observations.md`
- `private/current-state/current-state.md`
- `private/goals/`
- `private/time/protected-time.md`
- `private/finance/`
- `private/health/`
- `private/career/`
- `private/home/`
- `private/venture/`
- `private/governance/`

Do not write private context into public framework files.

## Update Procedure

1. Capture the raw observation in a private inbox or update log.
2. Classify the update.
3. Identify destination file.
4. Decide whether the update is stable, provisional, or needs confirmation.
5. Update the destination file only if the evidence is strong enough.
6. Record source and date.
7. Identify affected agents.
8. Trigger governance review if the update changes authority, privacy, protected time, or high-impact strategy.

## Voice And Taste Updates

PEGO should treat writing style, humor, taste, influences, and public positioning as durable operating context when they affect directives or opportunity strategy.

Use voice and taste updates for:

- Writing samples.
- Draft feedback.
- Books, essays, films, talks, software, places, objects, or people that shaped taste.
- Words and registers that create resistance.
- Public positioning goals.
- Perceptions to avoid.
- Opportunity goals for public artifacts.

Voice updates should preserve evidence quality. One sample can create a provisional rule, but repeated samples or direct feedback are needed before PEGO treats it as stable.

Use `pego/templates/voice-and-taste-model.md` for the private model.

## Evidence Strength

Classify evidence:

- Direct statement.
- Repeated statement.
- Observed behavior.
- Directive outcome.
- Telemetry.
- Model output.
- Professional input.
- Agent inference.
- Speculation.

Speculation should not become durable profile memory without review.

## Output

Use `pego/templates/context-update.md`.

For local operation, the reference runner is:

```sh
python3 ops/context/record_context_update.py --source Outcome --raw-observation "What was learned" --update-class Pattern --evidence-strength "Directive outcome" --stability "Current but changeable" --proposed-update "What should change"
```

It writes protected private context-update records. It updates destination files only when explicitly run with `--apply`.

To promote context-update candidates from a USER-mode session review, use:

```sh
python3 pegoctl promote-context
```

This records protected context-update files from `private/reviews/sessions/`
without applying them into durable profile, goal, health, finance, or strategy
files. Durable application remains an explicit governance-sensitive step.

To review protected context updates for durable application, use:

```sh
python3 pegoctl apply-context
```

This writes a protected memory-application review. It does not change durable
private memory unless run with `--apply`; even then, only eligible updates are
applied. Structured memory-application reviews must conform to
`pego/schemas/memory-application-review.schema.json`.

## Stop Conditions

Do not update durable memory if:

- The source is ambiguous.
- The update is private but the destination is public.
- The update would expose a third party unnecessarily.
- The update changes authority without governance review.
- The update is a one-off mood or transient condition being mistaken for a stable trait.
