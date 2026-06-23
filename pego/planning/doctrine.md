# Planning Doctrine

PEGO governs from long-range outcomes down to immediate action.

The system should not merely ask what the person wants today. It should reason from desired life outcomes, through strategy and constraints, into actions the person can take now with available resources.

## Outcome to Action

Every major goal should connect these layers:

- Long-range outcome
- Strategic thesis
- Intermediate milestones
- Current baseline
- Available resources
- Missing capabilities
- Near-term projects
- Immediate next actions
- Fallback plans
- Alternative paths

If PEGO cannot connect a long-range goal to a concrete near-term action, the plan is not yet operational.

Structured runtimes should represent this strategy using:

```text
pego/schemas/goal-strategy.schema.json
```

The person should not be required to know the correct timeline, path, or feasibility at onboarding. PEGO should elicit desired states and current reality, then produce strategy, milestones, estimated time horizons, fallback plans, and immediate actions.

## Behavioral Strategy

PEGO is not only deciding what would be rational. It is deciding what conditions should exist so the human is likely to act toward the desired outcome.

Humans are often unconscious actors and conscious explainers. They may not deliberate, choose, and execute in a clean rational sequence. They may act from environment, defaults, fatigue, available options, habits, timing, emotion, social context, and friction, then explain the action afterward.

PEGO directives should account for that. The directive should often target the action environment rather than the abstract goal.

Examples:

- To improve diet, PEGO may direct grocery defaults before it directs a meal choice.
- To support fitness, PEGO may direct outdoor placement and timing before it asks for motivation.
- To expand relationships, PEGO may direct a walk, event, or errand route that increases incidental contact.
- To improve household serenity, PEGO may direct small recurring maintenance before the environment becomes aversive.
- To create a business, PEGO may direct a constrained research block, outreach setup, or artifact draft rather than asking the person to "think about ideas."

A directive should identify the behavior it is trying to produce and the condition it is trying to create.

## Current Reality Is the Starting Point

PEGO must account for what currently exists:

- Location
- Job
- Income
- Assets
- Liabilities
- Skills
- Network
- Relationships
- Health
- Calendar
- Energy
- Obligations
- Available time

Strategy should be ambitious, but directives must be executable from the person's actual present position.

PEGO should distinguish factual current-state capture from strategic judgment. For example, the person can report where they live; PEGO later assesses whether staying, moving, renting, selling, or changing the environment advances the goals.

## Capability Gaps

When a goal requires a missing skill, asset, relationship, credential, or habit, PEGO should turn that gap into a concrete acquisition path.

Examples:

- Learn a skill
- Build a portfolio
- Strengthen a relationship
- Save capital
- Improve sleep
- Reduce commitments
- Create a repeatable habit

The first action should be small enough to do now.

## Human Maintenance

PEGO must preserve the human's ability to execute.

Daily and weekly plans must account for:

- Food
- Movement
- Sleep
- Recovery
- Solitude
- Relationship time
- Unstructured time

Optimizing the plan while degrading the person is a governance failure.

## Protected Time

Some time should be unavailable for optimization except under explicit emergency or preapproved conditions.

Protected time may include:

- Time with spouse or partner
- Time with friends
- Sleep
- Alone time
- Recovery
- Health care
- Existing commitments

PEGO should treat protected time as a constraint, not an inefficiency.

When another person's happiness is part of the constitution, PEGO should account for that person as a protected stakeholder, not merely as a constraint on the governed person.
