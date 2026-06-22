# Directive Queue Template

Use this template to maintain the live queue for a day or work session.

The queue is not a backlog. It is the active set of candidates that PEGO may select from during intra-day command cycles.

Structured runtimes should preserve the public schema at:

```text
pego/schemas/directive-queue.schema.json
```

## Date or Session

Date or session name.

## Operating Frame

Current daily thesis, weekly priority, or active operating mode.

## Protected Time

Time and commitments unavailable for directives.

## Current State

- Time:
- Location:
- Energy:
- Weather/environment:
- Active obligations:
- Known constraints:

## Completed

| Time | Directive | Outcome |
| --- | --- | --- |
| TBD | TBD | TBD |

## Active Candidates

| Rank | Candidate | Domain | Duration | Energy | Location | Deadline | Authority | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

## Deferred

| Candidate | Reason Deferred | Next Review |
| --- | --- | --- |
| TBD | TBD | TBD |

## Blocked

| Candidate | Blocker | Required Change |
| --- | --- | --- |
| TBD | TBD | TBD |

## Next Directive

The next directive selected by the intra-day command loop.

## Next Check-In

When PEGO should be asked again or when the queue should be reviewed.
