# Command Response Template

Use this template when the human asks for the next directive or reports an intra-day status update.

Structured runtimes should preserve the public schema at:

```text
pego/schemas/command-response.schema.json
```

This is the only USER-mode surface after internal checks complete. Do not add
setup logs, diffs, command output, file-write summaries, or agent scratch
planning to a command response.

## State Update

What changed since the prior directive?

## Next Directive

One directive only.

## Time Box

Estimated time box.

## Start Condition

What must be true before starting?

## Do This

The concrete execution instruction. Say what to do in plain operational terms.
Use examples when they reduce choice friction.

## Reason

Operational reason for selecting this directive over the other candidates.
Default to one line. Save detailed rationale for an explanation request,
objection, review, or governance escalation.

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
