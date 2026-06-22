# Governance Ops

Local tools for producing PEGO governance and compliance artifacts.

Generated reviews are written under `private/governance/reviews/`, which is ignored by Git.

## Directive Preflight

```sh
python3 ops/governance/directive_preflight.py --directive private/directives/command-responses/YYYY-MM-DD-next.md
```

Use preflight to classify a directive before adoption:

- `pass`: can remain a low-risk Level 1 recommendation if local constraints still fit.
- `needs_review`: run compliance review before adoption.
- `escalate`: create or update a decision packet before execution.

## Generate Compliance Review

```sh
python3 ops/governance/generate_compliance_review.py --directive private/directives/daily/2026-06-22.md
```

Optional date and slug:

```sh
python3 ops/governance/generate_compliance_review.py \
  --directive private/directives/daily/2026-06-22.md \
  --date 2026-06-22 \
  --slug daily-directive
```

By default, the script will not overwrite an existing review. Use `--force` only when intentionally regenerating a local private review.
