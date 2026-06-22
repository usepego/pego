# Outcome Ops

Local tools for recording PEGO execution outcomes.

Outcome records are protected private artifacts. They may contain private context and must stay inside the private instance unless explicitly sanitized.

## Record Outcome

```sh
python3 ops/outcomes/record_outcome.py \
  --date YYYY-MM-DD \
  --directive "Breakfast Anchor" \
  --completion completed \
  --what-happened "Ate protein/fiber breakfast" \
  --evidence "Human report"
```

The runner writes a private outcome file under:

```text
private/outcomes/directives/
```

It can also append a session event:

```sh
python3 ops/outcomes/record_outcome.py --append-session ...
```
