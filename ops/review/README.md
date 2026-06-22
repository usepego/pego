# Review Ops

Local tools for turning PEGO outcomes into learning decisions.

Outcome reviews read protected private outcome records and write protected review packets under `private/reviews/outcomes/`. They are the bridge between "what happened" and "what PEGO should change next."

## Review Outcome

```sh
python3 ops/review/review_outcome.py --outcome private/outcomes/directives/YYYY-MM-DD-directive.md
```

The output should feed weekly review, directive synthesis, and context update.
