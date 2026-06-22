# Weekly Operating Loop

The weekly loop converts goals, recent outcomes, and agent recommendations into a bounded operating plan for the next seven days.

It is the main cadence for course correction. The daily loop decides what to do today; the weekly loop decides what the week is for.

## Inputs

- Constitution.
- Active goals.
- Current state.
- Protected time.
- Recent daily directives and outcomes.
- Agent recommendations.
- Governance reviews.
- Calendar or availability.
- New human concerns or objections.
- Anticipation scans for the next 7-14 days.
- Current operating register.

## Steps

1. Review the previous week's directives and outcomes using `pego/operations/outcome-review.md`.
2. Identify friction, missed directives, energy gains, and recurring failure modes.
3. Check whether active goals still fit the current state.
4. Run an anticipation scan using `pego/operations/anticipation-loop.md`.
5. Gather or request agent recommendations using `pego/templates/agent-recommendation.md`.
6. Convert recommendations into directive candidates using `pego/templates/directive-candidate.md`.
7. Synthesize candidates using `pego/operations/directive-synthesis.md`.
8. Select a small number of weekly priorities.
9. Assign authority levels and governance status.
10. Produce the weekly operating plan using `pego/templates/weekly-operating-plan.md`.
11. Convert the weekly plan into daily directive constraints.
12. Escalate high-impact or unresolved decisions into decision packets.

## Weekly Limits

Until PEGO has strong outcome data, weekly plans should stay bounded:

- 1 primary strategic priority.
- 1 health priority.
- 1 career or income priority.
- 0-1 finance/admin priority.
- 0-1 exploration or relationship priority.
- Protected time explicitly preserved.

The weekly plan should create focus, not a backlog.

## Review Questions

- What did PEGO direct last week?
- What happened?
- What failed repeatedly?
- What created energy, clarity, or progress?
- What created drag, anxiety, or avoidance?
- Which goal assumptions changed?
- Which agent needs better information?
- Which upcoming event, maintenance issue, supply gap, or deadline needs lead time?
- Which register entries should become directive candidates this week?
- What should be simplified this week?

## Governance

The weekly loop may shape priorities, but it does not itself grant execution authority.

Any weekly priority that changes protected time, creates material financial impact, affects a protected stakeholder, or carries meaningful health, career, legal, tax, privacy, or relationship risk must pass the appropriate governance review.

High-impact actions must be converted into a decision packet using `pego/templates/decision-packet.md`.
