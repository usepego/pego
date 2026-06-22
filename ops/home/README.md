# Home Ops

Local tools for converting the protected operating register into home and environment directive candidates.

Home candidates preserve physical environment quality: yard, garden, repairs, supplies, beauty, privacy, serenity, and recurring household friction.

## Generate Home Candidates

```sh
python3 ops/home/generate_candidates.py
```

Default input:

```text
private/operator/operating-register.md
```

Default output:

```text
private/directives/candidates/home-candidates.md
```

The output can be passed into daily synthesis:

```sh
python3 ops/cycles/daily_cycle.py synthesize --candidate private/directives/candidates/home-candidates.md
```
