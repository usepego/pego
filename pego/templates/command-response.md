# Command Response Template

Use this template when the human asks for the next directive or reports an intra-day status update.

Structured runtimes should preserve the public schema at:

```text
pego/schemas/command-response.schema.json
```

## State Update

What changed since the prior directive?

## Next Directive

One directive only.

## Duration

Estimated time box.

## Start Condition

What must be true before starting?

## Why This Now

Operational reason for selecting this directive over the other candidates.

## Target Behavior

What behavior, state, or future choice this directive is trying to make more likely.

## Environment Design

What condition, default, friction change, exposure, timing, or social context this directive creates.

## Fallback

What to do if this directive is blocked.

## Deferred

What PEGO is intentionally not selecting now.

## Stop Condition

What should cause the human to stop or ask for resynthesis?

## Next Check-In

When to return to PEGO.
