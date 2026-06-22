# Governance Ops

Local tools for producing PEGO governance and compliance artifacts.

Generated reviews are written under `private/governance/reviews/`, which is ignored by Git.

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
