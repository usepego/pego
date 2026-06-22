# Outcome Review

Outcome review is how PEGO learns from execution.

A directive that is not reviewed is only a suggestion with no feedback loop. PEGO should treat outcomes as operating evidence and use them to adjust future directives, priorities, authority levels, and strategy.

## Purpose

Outcome review should answer:

- Did the directive happen?
- If not, why not?
- Did it improve the target condition?
- What did it cost?
- What should change next?

## Inputs

- Source directive.
- Synthesized day plan, if any.
- Human report.
- Artifacts produced.
- Telemetry or direct evidence.
- Protected-time impact.
- Stakeholder impact.
- Agent observations.

## Steps

1. Record completion status.
2. Separate facts from interpretation.
3. Identify friction.
4. Identify benefit.
5. Identify cost.
6. Determine whether the directive should repeat, change, stop, or escalate.
7. Update directive candidates.
8. Feed relevant evidence into the weekly loop.

## Outcome Classes

### Completed

The directive happened as intended.

### Partially Completed

Some useful action happened, but the directive was too large, poorly scheduled, or interrupted.

### Not Completed

The directive did not happen.

This is evidence. Do not treat it as a moral failure.

### Blocked

The directive could not happen because a dependency, constraint, energy limit, weather, tool, stakeholder, or governance condition blocked it.

### Canceled

The directive was intentionally canceled because it no longer fit the day or strategy.

## Interpretation Rules

- Repeated failure means the directive design is wrong until proven otherwise.
- A directive that repeatedly expands past its time box should be reduced or split.
- A directive that protects the environment or health with low friction should be considered for recurrence.
- A directive that creates protected-time conflict should be revised before repetition.
- A strategic directive that produces an artifact should feed the relevant program or project file.

## Output

Use `pego/templates/directive-outcome.md`.

For local operation, the reference runner is:

```sh
python3 ops/outcomes/record_outcome.py --date YYYY-MM-DD --directive "Directive name" --completion completed
```

It writes protected private outcome records and can append protected session-log events.

To convert a recorded outcome into a learning decision, use:

```sh
python3 ops/review/review_outcome.py --outcome private/outcomes/directives/YYYY-MM-DD-directive.md
```

It writes protected private review packets under:

```text
private/reviews/outcomes/
```

Outcome records should feed:

- `pego/operations/daily-loop.md`
- `pego/operations/intra-day-command-loop.md`
- `pego/operations/weekly-loop.md`
- `pego/operations/monthly-loop.md`
- `pego/operations/context-update.md`
- Relevant agent files and model specs.
