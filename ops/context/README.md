# Context Ops

Local tools for recording PEGO context updates.

Context updates are ignored private artifacts. They may contain private facts, preferences, constraints, goals, or operating patterns and should not be committed.

## Record Context Update

```sh
python3 ops/context/record_context_update.py \
  --date YYYY-MM-DD \
  --source Outcome \
  --raw-observation "What was learned" \
  --update-class Pattern \
  --evidence-strength "Directive outcome" \
  --stability "Current but changeable" \
  --destination-file private/person/observations.md \
  --proposed-update "Add the new pattern"
```

Default action is `Record only`.

To append an approved update to a private destination file:

```sh
python3 ops/context/record_context_update.py ... --action "Update destination" --apply
```
