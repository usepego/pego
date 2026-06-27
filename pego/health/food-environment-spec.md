# Food Environment Spec

Food directives require an environment model, not only a nutrition target.

PEGO should decide what to eat by combining health goals, current hunger and energy, available food, nearby restaurants, grocery options, cost, travel friction, preparation time, taste preferences, social context, and happiness impact.

## Purpose

The food environment layer helps PEGO answer:

- What can the person realistically eat now?
- What is available at home?
- What groceries are nearby and worth buying?
- Which restaurants are nearby?
- What menu items are available?
- What do those items likely cost?
- What are the calories, protein, fiber, sugar, sodium, and other relevant nutrition estimates?
- How long would it take to obtain the food?
- Would the person actually be willing to eat it?
- Does the choice advance the health goal without damaging happiness or creating rebound behavior?

## Inputs

- Health baseline.
- Current food log.
- Current hunger, energy, schedule, and location.
- Protected time.
- Home inventory.
- Grocery store options.
- Restaurant options.
- Menu item options.
- Nutrition estimates.
- Cost estimates.
- Travel time or delivery friction.
- Preferences, aversions, sweet triggers, and acceptable defaults.
- Recent outcomes: compliance, satisfaction, hunger later, cravings, sleep, energy.

## Data Sources

PEGO may use multiple sources, but each source needs a confidence label.

Possible sources:

- Manual user report.
- Home inventory list.
- Receipt or order history.
- Grocery APIs or store websites.
- Restaurant websites.
- Menu APIs.
- Nutrition databases.
- Map services.
- Delivery apps.
- User-entered defaults.
- Agent estimates.

Source quality must be explicit. Restaurant and menu nutrition estimates are often incomplete or stale.

## Food Option Shape

Each food option should capture:

- Source.
- Location type: home, grocery, restaurant, delivery, workplace, travel.
- Item or meal name.
- Ingredients or components when known.
- Estimated calories.
- Protein.
- Fiber.
- Sugar.
- Sodium.
- Cost.
- Travel or preparation time.
- Availability window.
- Satiety estimate.
- Enjoyment estimate.
- Goal fit.
- Confidence.
- Stop condition.

Use `pego/templates/food-option.md`.

Structured implementations should preserve food options using `pego/schemas/food-option.schema.json`.

## Meal Decision Shape

A meal decision compares available options and selects one directive.

It should include:

- Current context.
- Candidate options.
- Selected directive.
- Rationale.
- Tradeoffs.
- Why better options were not selected.
- What to do next time.
- Review question.

Use `pego/templates/meal-decision.md`.

Structured implementations should preserve meal decisions using `pego/schemas/meal-decision.schema.json`.

## Decision Rules

The Health Agent should:

1. Prefer available home defaults when they fit and friction is low.
2. Apply the person's current nutrition strategy. Examples include weight loss, weight gain, maintenance, muscle gain, performance, metabolic stability, appetite recovery, or basic meal reliability.
3. Avoid turning one imperfect meal into punitive restriction later.
4. Use restaurant meals deliberately, not reactively.
5. Compare the full meal, not one item in isolation.
6. Account for enjoyment and satisfaction; unsatisfying food may increase later friction.
7. Account for time, travel, weather, obligations, and protected time.
8. Treat estimates as estimates.
9. Use small corrective next directives after a meal misses the current strategy: water, walk, lighter or larger next meal, protein/fiber anchor, grocery reset, tomorrow breakfast default, or no correction.
10. Escalate medical, disordered-eating, or clinically significant nutrition issues.

## Integration Boundaries

Map, grocery, menu, delivery, and nutrition services are adapters, not PEGO core.

Adapters should provide structured options with:

- Timestamp.
- Source.
- Query scope.
- Confidence.
- Terms or usage limits when relevant.
- Privacy risk.

The core PEGO decision layer should remain able to operate from manual inputs.

## Governance

Food directives are normally Level 1 recommendations.

Level 4 escalation required:

- Medical nutrition therapy.
- Diabetes or glucose-directed medical interpretation.
- Eating-disorder risk.
- Extreme restriction.
- Supplements or medications.
- Any directive conflicting with clinician advice.

## Review

Meal outcomes should record:

- What was eaten.
- Approximate portion.
- Hunger before and after.
- Satisfaction.
- Energy.
- Cravings later.
- Any friction.
- What PEGO should change next time.
