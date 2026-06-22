# Health Ops

Local tools for converting protected health baseline state into low-risk directive candidates.

Health candidate generation is not medical advice. It creates conservative Level 1 food, movement, and sleep candidates that must still pass PEGO synthesis and governance rules.

## Generate Health Candidates

```sh
python3 ops/health/generate_candidates.py
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
