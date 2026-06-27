# Health Ops

Local tools for converting protected health baseline state into low-risk directive candidates.

Health candidate generation is not medical advice. It creates conservative Level 1 food, movement, and sleep candidates that must still pass PEGO synthesis and governance rules.

## Generate Health Candidates

```sh
python3 ops/health/generate_candidates.py
python3 pegoctl health-candidates
```

Default input:

```text
private/health/baseline.json
```

Default output:

```text
private/directives/candidates/health-candidates.md
```

The output can be passed into:

```sh
python3 ops/cycles/daily_cycle.py synthesize --candidate private/directives/candidates/health-candidates.md
```

## Generate Health Check-In

```sh
python3 ops/health/generate_check_in.py
```

Default input:

```text
private/health/baseline.json
```

Default output:

```text
private/health/check-ins/health-check-in.md
```

The check-in asks only targeted questions needed to select or revise health
directives. It should not create broad reflection prompts or new biomarker
tracking unless the measurement changes a decision.

## Decide Meal

```sh
python3 ops/health/decide_meal.py --option private/health/food-options/options.json
python3 pegoctl meal --option private/health/food-options/options.json
```

Default output:

```text
private/health/meal-decisions/meal-decision.md
```

The meal decision runner compares protected food options and emits a meal
decision plus a health directive candidate. It supports multiple nutrition
strategies, including weight loss, weight gain, maintenance, muscle gain,
performance, metabolic stability, appetite recovery, and balanced eating.

Food option inputs should follow:

```text
pego/schemas/food-option.schema.json
```

For installed or backed-up operation, pass `--private-root` to `pegoctl` or to
the direct scripts so baseline files, food options, meal decisions, and
candidate outputs stay inside the protected private instance.
