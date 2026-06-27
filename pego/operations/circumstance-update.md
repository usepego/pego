# Circumstance Update Loop

Circumstance updates are short reports that the human's operating environment
has changed.

They are not requests for a general plan. They are triggers for immediate
directive resynthesis.

## Purpose

PEGO should treat location, time, energy, hunger, weather, companions, store
context, restaurant context, travel state, equipment access, and unexpected
constraints as directive-changing facts.

The goal is to shape the next likely action before the human must rely on
abstract willpower.

Examples:

- The human is at a grocery store.
- The human is near a restaurant.
- The human has 20 minutes before a meeting.
- The human is tired and not at home.
- The weather makes the planned outdoor directive impossible.
- The human is with another person whose preferences matter.
- The human entered a store, airport, hotel, office, gym, garden, vehicle, or
  other context with different action affordances.

## Input Shape

A circumstance update may be as small as:

```text
I am at a grocery store.
```

or:

```text
I have 35 minutes before dinner and I am hungry.
```

The adapter or runtime should extract:

- Current location or environment.
- Available time.
- Energy or fatigue.
- Hunger or meal timing, when relevant.
- Active companions or stakeholder constraints, when relevant.
- Temptation, friction, or hazard created by the environment.
- Active goal affected by the environment.
- Authority level required for any proposed action.

Do not ask for all fields by default. Ask only for the smallest missing fact
that would change the directive.

## Resynthesis Rule

When a circumstance update arrives, PEGO should:

1. Record the update in the protected intra-day session log.
2. Infer whether the update changes location, time, energy, food environment,
   social context, risk, or available tools.
3. Filter the active directive queue against the new circumstance.
4. Prefer an existing candidate if one fits.
5. If no candidate fits, issue one targeted question or a small guardrail
   directive that preserves the active goal without pretending to solve the
   whole day.
6. Preserve governance limits, protected time, and authority gates.
7. Return one directive only.

## Micro-Directives

Circumstance updates often require micro-directives: small, local actions that
shape the environment immediately.

Examples:

- Buy only the approved meal ingredients and leave the store.
- Choose the restaurant item that best matches the active health target and
  likely follow-through.
- Skip an aisle, shelf, app, route, or conversation that predicts goal drift.
- Start the small maintenance action while tools and location are already
  available.
- Defer a strategic work directive because the current environment cannot
  support it.

Micro-directives should be explicit about guardrails:

- What to do.
- What not to do.
- Why this environment creates risk or opportunity.
- What fallback to use if the first option is unavailable.
- When to stop and leave the environment.

## Behavior Loops

Repeated circumstance updates and outcomes should be inspected for loops:

```text
trigger -> routine -> reward or relief -> strategic effect
```

If a context repeatedly produces behavior that works against an active strategy,
PEGO should create a behavior-loop record and ask the Council to decide whether
to adopt a disruption directive.

The disruption should change the human's environment or frame before the loop
fires. It may route around a trigger, narrow the purchase/order/action set,
change timing, stage a replacement default, or move the human into a different
context.

Use `pego/templates/behavior-loop.md`.

## Environmental Guardrails

PEGO may use environmental guardrails when they are within granted authority:

- Purchase limits.
- Aisle or shelf avoidance.
- Restaurant ordering constraints.
- Route choice.
- Store exit timing.
- App, website, or media avoidance.
- Tool staging.
- Social or household boundary preservation.

Guardrails must not shame, moralize, or turn into self-help language. They are
operating constraints used to make the desired behavior more likely.

## Output Shape

Use `pego/templates/command-response.md`.

The response should preserve:

- State update.
- Next directive.
- Start condition.
- Target behavior.
- Environment design.
- Fallback.
- Stop condition.
- Next check-in.

Example:

```text
Directive: Buy the approved meal ingredients and leave the store.

Environment design: Use the store visit to improve tomorrow's food defaults
while avoiding the sections most likely to create snack inventory.

Stop condition: If the approved items are unavailable, buy the nearest
protein/fiber substitute and leave without adding dessert or snack inventory.
```

## Governance

Circumstance updates may reorder low-risk directives. They must not silently
grant execution authority for high-impact decisions.

Escalate or block if the update implies:

- Financial execution.
- Medical risk.
- Legal commitment.
- Relationship-impacting action.
- Privacy disclosure.
- Hard-to-reverse career, housing, or household action.
- Use of credentials, accounts, or third-party systems beyond granted authority.

## Local Adapter

The local USER-mode check-in adapter may infer broad location classes from
natural language, such as `grocery_store`, `restaurant`, `home`, `outside`,
`car`, `airport`, `office`, `phone`, or `computer`.

This inference is convenience only. Mature runtimes should use richer context
when available and should keep raw private location details in the protected
private instance.
