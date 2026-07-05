# Outcome Review

Outcome review is how PEGO learns from execution.

A directive that is not reviewed is only a suggestion with no feedback loop. PEGO should treat outcomes as operating evidence and use them to adjust future directives, priorities, authority levels, and strategy.

Use `pego/operations/operating-memory.md` before promoting outcome evidence
into durable private memory.

Use `pego/operations/recommendation-quality-loop.md` when the outcome should
evaluate whether agent recommendations, council synthesis, or human questions
improved the directive.

## Purpose

Outcome review should answer:

- Did the directive happen?
- If not, why not?
- Did it improve the target condition?
- Did the human report progress toward the intended outcome?
- Did it increase, reduce, or fail to affect contentment?
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
5. Identify outcome progress and contentment signal.
6. Identify cost.
7. Review decision quality: actionability, goal fit, constraint fit, burden,
   timeliness, risk control, explanation quality, follow-through probability,
   outcome quality, and learning value.
8. Determine whether the directive should repeat, change, stop, or escalate.
9. Review agent recommendations if the directive came from a domain-agent
   recommendation.
10. Review council synthesis if the directive came from a council decision or
   cross-domain deferral.
11. Review information-value assessments if PEGO asked the human a question.
12. Update directive candidates.
13. Feed relevant evidence into the weekly loop.

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

To emit a structured runtime-neutral review artifact as well:

```sh
python3 ops/review/review_outcome.py --outcome private/outcomes/directives/YYYY-MM-DD-directive.json --json-output private/reviews/outcomes/YYYY-MM-DD-directive-review.json
```

Structured review artifacts must conform to
`pego/schemas/outcome-review.schema.json`.

Outcome reviews include a nested decision quality review. The decision quality
review should conform to:

```text
pego/schemas/decision-quality-review.schema.json
```

Use:

```text
pego/templates/decision-quality-review.md
```

To attribute the outcome back to the council decision and source
recommendations, pass the protected source artifacts explicitly:

```sh
python3 ops/review/review_outcome.py \
  --outcome private/outcomes/directives/YYYY-MM-DD-directive.json \
  --council-decision private/council/decisions/council-decision.json \
  --recommendation private/recommendations/health.json \
  --json-output private/reviews/outcomes/YYYY-MM-DD-directive-review.json
```

When a council decision is supplied, the runner can also discover its
`source_recommendations` if those paths are available. Missing source artifacts
must not fail outcome review; they should produce missing-source review records
so repository hygiene can be fixed later.

To write bounded private agent calibration records from attribution:

```sh
python3 ops/review/review_outcome.py \
  --outcome private/outcomes/directives/YYYY-MM-DD-directive.json \
  --council-decision private/council/decisions/council-decision.json \
  --json-output private/reviews/outcomes/YYYY-MM-DD-directive-review.json \
  --write-calibration
```

Calibration records write under:

```text
private/agents/calibration/
```

Use `pego/templates/agent-calibration-record.md` and
`pego/schemas/agent-calibration-record.schema.json`. These records are private
operating memory. They should inform future council weighting, but they do not
authorize higher authority or public disclosure.

To close a USER-mode session into a session-level learning review, use:

```sh
python3 pegoctl close-session
```

It reads the protected intra-day session log and writes a protected session
review under `private/reviews/sessions/`. Structured session reviews must
conform to `pego/schemas/session-review.schema.json`.

If the session review contains context-update candidates, promote them into
protected context-update records with:

```sh
python3 pegoctl promote-context
```

Outcome records should feed:

- `pego/operations/recommendation-quality-loop.md`
- `pego/operations/daily-loop.md`
- `pego/operations/intra-day-command-loop.md`
- `pego/operations/weekly-loop.md`
- `pego/operations/monthly-loop.md`
- `pego/operations/context-update.md`
- `pego/operations/operating-memory.md`
- Relevant agent files and model specs.
