# Tool Contract: calendar.availability

## Tool

`calendar.availability`

## Purpose

Identify existing commitments, protected time, travel buffers, and viable time
windows so Operations can synthesize directives that actually fit the day.

## Owning Agents

Operations Agent, Relationships Agent, Governance Agent.

## Inputs

- Date or date range.
- Time zone.
- Protected-time rules.
- Optional calendar source identifiers.
- Optional event categories to include or exclude.

## Outputs

- Busy windows.
- Protected windows.
- Candidate directive windows.
- Schedule conflicts.
- Confidence and data freshness.

## Authority Required

Level 0 observe for read-only calendar inspection.

Level 3 execute is required before creating, moving, or deleting calendar
events.

## Operation Type

Observe.

## Private Data Used

- Calendar event metadata.
- Protected time.
- Location or travel hints when available.

## Third-Party Disclosure

External service if the runtime connects to a hosted calendar provider.

## Write Locations

Protected private instance only, usually under private operating briefs,
directive queues, or session logs.

## Governance Review

Read-only inspection requires the private constitution to grant calendar access.
Writing calendar events requires explicit tool permission and review.

## Failure Mode

If unavailable or stale, PEGO should ask the smallest scheduling question needed
to select the next directive.

## Logging Rule

Log data freshness, source class, and any schedule constraints used. Do not log
full private calendar contents in public files.

## Prohibited Uses

- Publishing calendar details.
- Moving or deleting commitments without explicit execution authority.
- Inferring sensitive relationship, health, work, or location facts beyond the
  directive need.
