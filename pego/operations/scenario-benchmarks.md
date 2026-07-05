# Scenario Benchmarks

Scenario benchmarks are public-safe synthetic evaluations of PEGO decision
quality.

They exist to make product claims inspectable. They do not use private
outcomes, private Speckit planning, private roadmap content, user data, or
maintainer personal data.

## Purpose

Benchmarks should compare PEGO against:

- Generic assistant advice.
- Todo-list planning.
- Single-agent recommendations.

The comparison should preserve:

- Scenario input.
- Baseline output and assumptions.
- PEGO output.
- Scoring criteria and weights.
- Result.
- Failure modes.
- Public export review.

## Public-Safe Rule

Benchmark fixtures must be synthetic. A runner must reject private fixture
paths and must stop if public output contains private planning or subject-data
markers.

The export guard is intentionally conservative. A benchmark artifact that
fails public-safe review should not be used as a public example until the
source text is fixed.

## Failure Preservation

Benchmark output must include weak PEGO behavior. A scenario where PEGO fails,
ties, asks too much, over-escalates, or has insufficient evidence is useful
research evidence.

Do not turn benchmark results into marketing copy without preserving
assumptions and failure modes.

## Local Runner

For local operation:

```sh
python3 ops/evaluation/run_scenario_benchmarks.py
```

The default runner uses built-in synthetic fixtures and writes:

```text
benchmarks/scenario-benchmark.md
benchmarks/scenario-benchmark.json
```

To use a public-safe fixture directory:

```sh
python3 ops/evaluation/run_scenario_benchmarks.py --fixture-dir benchmarks/fixtures
```

The runner must reject paths under `private/`.

Structured results should conform to:

```text
pego/schemas/scenario-benchmark.schema.json
```

Use:

```text
pego/templates/scenario-benchmark.md
```
