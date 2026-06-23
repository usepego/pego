# Tool Contract: food.environment.lookup

## Tool

`food.environment.lookup`

## Purpose

Identify food options available in the current environment so the Health Agent
can issue a concrete meal or grocery directive.

## Owning Agents

Health Agent, Operations Agent, Happiness Agent, Governance Agent.

## Inputs

- Current location class or approved precise location.
- Food environment type: home, grocery, restaurant, delivery, travel, event.
- Active health goal.
- Allergies, contraindications, dietary constraints, and preferences.
- Budget, time, hunger, energy, and social context when relevant.

## Outputs

- Comparable food options.
- Nutrition estimates and confidence.
- Cost and time estimates.
- Friction and temptation risks.
- Recommended guardrails.
- Candidate meal directive.

## Authority Required

Level 0 observe for lookup.

Level 1 recommend for meal or grocery recommendation.

Level 2 direct if the constitution grants PEGO authority to issue meal
directives.

Level 3 execute is required before ordering food or purchasing groceries.

## Operation Type

Observe or recommend.

## Private Data Used

- Health goals.
- Dietary constraints.
- Preferences.
- Current location or environment.
- Recent food outcomes when relevant.

## Third-Party Disclosure

External service if using map, grocery, delivery, restaurant, or nutrition APIs.

## Write Locations

Protected private instance under food options, meal decisions, directive
candidates, or command responses.

## Governance Review

Routine low-risk meal directives may use lightweight review. Medical diets,
eating-disorder risk, medication interactions, allergies, or significant health
changes require escalation.

## Failure Mode

If lookup fails, use approved home defaults, known local defaults, or ask one
missing food-environment question.

## Logging Rule

Log source, confidence, and decision-relevant estimates. Do not publish private
location, health, or preference details.

## Prohibited Uses

- Medical advice.
- Shame or moral judgment.
- Ordering or purchasing without explicit execution authority.
- Sending precise location or health details to third parties unless approved.
