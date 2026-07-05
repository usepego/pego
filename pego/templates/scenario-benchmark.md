# Scenario Benchmark

Use this template for public-safe synthetic benchmark results that compare
PEGO council governance against baselines such as generic assistant advice,
todo lists, or single-agent recommendations.

Structured implementations should emit:

```text
pego/schemas/scenario-benchmark.schema.json
```

## Date

Date.

## Benchmark Suite

Suite name and version.

## Summary

Scenario count, PEGO wins, baseline wins, ties, and public-safe status.

## Scenario Input

Synthetic scenario title, decision frame, context, assumptions, and source
recommendation count.

## Baseline Outputs

Baseline type, assumptions, output, score, and preserved failure modes.

## PEGO Output

Council outcome, proposed directive, next action, governance status, tradeoff
rationale, dissent, deferrals, evidence gaps, and score.

## Scoring Criteria

Criterion, weight, PEGO score, baseline scores, and rationale.

## Result

Winner, score totals, and comparison summary.

## Failure Modes

Failure modes for PEGO and baselines. Do not delete weak PEGO behavior from the
benchmark output.

## Public Export Review

Whether the benchmark artifact is safe for public use and which marker class
failed if it is not safe.
