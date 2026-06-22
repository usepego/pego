# Anticipation Loop

The anticipation loop identifies future friction early enough for PEGO to prevent it.

PEGO should not wait until the human is already irritated, rushed, hungry, unprepared, or forced into a larger decision. It should inspect known goals, current environment, upcoming events, seasonal conditions, supplies, and prior annoyances, then ask concrete operational questions or issue prep directives.

## Purpose

The anticipation loop should determine:

- What upcoming event, condition, deadline, or seasonal change may create friction.
- What recurring annoyance is likely to return if not handled.
- What missing supply, skill, outfit, reservation, document, appointment, or decision would create scrambling later.
- Which agent should own the next small action.
- Whether the next action is safe to direct or needs governance review.

## Inputs

- Calendar or known upcoming events.
- Active goals and strategy.
- Current state.
- Recent outcomes.
- Known irritants and recurring annoyances.
- Protected time.
- Home, health, finance, career, relationship, and exploration context.
- Weather, seasonality, travel dates, deadlines, and supply status when available.

## Operating Cadence

Use anticipation at several horizons:

- Daily: inspect today and tomorrow for immediate conflicts, food defaults, supplies, weather, and schedule constraints.
- Weekly: inspect the next 7-14 days for events, errands, home maintenance, purchases, reservations, wardrobe, documents, and project dependencies.
- Monthly: inspect the next 30-90 days for larger goals, seasonal home work, travel, social obligations, financial decisions, health appointments, and venture milestones.
- Event-driven: run the loop when a new trip, dinner, meeting, household issue, deadline, purchase, or concern appears.

## Targeted Questions

Questions should be specific to the known environment. They should gather decision-grade facts, not invite self-help reflection.

Use questions like:

- Which visible part of the home or yard is most annoying right now?
- What upcoming event requires clothing, reservation, gift, transport, documents, or prep?
- What do you already own that could work for that event?
- What item would need to be purchased this week to avoid a last-day scramble?
- Which recurring household issue has started to return?
- Which food default is missing from the house?
- Which work or venture dependency will block progress if it is not handled this week?
- Which relationship or household constraint needs to be protected before scheduling work?

Avoid questions like:

- How do you feel about your life today?
- What are you grateful for?
- What intention do you want to set?
- What does your best self want?

## Anticipation Domains

### Environment

Identify visible irritants, seasonal maintenance, repairs, supplies, yard work, garden quality, comfort, and household serenity risks.

### Events

Identify clothing, grooming, reservations, transport, gifts, tickets, documents, timing, and spouse/partner impact.

### Food and Health

Identify missing default foods, meal timing, protein/fiber options, sleep constraints, movement opportunities, and known failure points.

### Strategy

Identify next dependencies for financial freedom, venture work, skill acquisition, network development, and career optionality.

### Finance and Admin

Identify bills, account reviews, tax items, insurance, renewals, subscriptions, scenario updates, and spending decisions that should not become urgent.

## Output

Use `pego/templates/anticipation-scan.md`.

The output should produce one of:

- A targeted question.
- A prep directive.
- A deferred candidate.
- A supply or purchase candidate.
- A governance escalation.
- A context update.

## Synthesis Rule

Anticipation does not add unlimited tasks. It creates candidates for directive synthesis.

The Operations Agent must compare anticipated work against daily capacity, protected time, current strategy, and competing directives. Low-effort prevention can be scheduled early; larger actions should become weekly priorities or decision packets.

## Stop Conditions

Pause or escalate if:

- The anticipated action affects a spouse/partner, protected time, privacy, health risk, legal risk, or material spending.
- The question asks for private information that is not needed for a decision.
- The scan produces a large backlog instead of a small number of prevention candidates.
- PEGO cannot distinguish a real upcoming constraint from speculation.
