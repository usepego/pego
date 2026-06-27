# Intra-Day Session Log Template

Use this template to record command-loop interactions during a day or work session.

The session log preserves state between check-ins so PEGO can select the next directive without restarting the day plan.

Structured runtimes should preserve the public schema at:

```text
pego/schemas/intra-day-session-log.schema.json
```

## Date or Session

Date or session name.

## Active Queue

Path to the directive queue.

## Operating Frame

Current daily directive, weekly priority, protected time, and governance limits.

## Session Events

| Time | Human Input | State Change | PEGO Response | Outcome |
| --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD |

## Completed Directives

| Time | Directive | Evidence | Notes |
| --- | --- | --- | --- |
| TBD | TBD | TBD | TBD |

## Partial, Blocked, or Canceled Directives

| Time | Directive | Status | Reason | Next Handling |
| --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD |

## Queue Adjustments

What changed in the directive queue?

## Deferrals

Which candidates were deferred and why?

## Governance Notes

Authority, privacy, protected-time, stakeholder, or escalation issues.

## End-of-Day Transfer

Facts that should move into the directive outcome record.
