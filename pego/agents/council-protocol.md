# Council Protocol

The PEGO Council reconciles domain-agent recommendations into a single directive or escalation.

The council is the default deliberation layer for meaningful PEGO decisions. It should make the tradeoffs explicit, preserve dissent, and produce one coherent next action or escalation packet.

## Required Inputs

- Constitution.
- Active goals.
- Current state.
- Protected time.
- Current constraints.
- Relevant telemetry.
- Recent directives and outcomes.
- New human concerns or objections.
- Domain-agent recommendations.
- Governance review outcomes, if any.

## Domain Agents

Initial council members:

- Health Agent
- Finance Agent
- Career Agent
- Venture Agent
- Home and Environment Agent
- Operations Agent
- Relationships Agent
- Exploration Agent
- Happiness Agent
- Governance Agent

See domain protocols:

- `finance-agent.md`
- `health-agent.md`
- `career-agent.md`
- `venture-agent.md`
- `home-environment-agent.md`
- `relationships-agent.md`
- `exploration-agent.md`
- `happiness-agent.md`
- `operations-agent.md`

## Agent Invocation Contract

When an agent is invoked, it should return:

- Agent name.
- Recommendation or dissent.
- Authority level.
- Relevant facts used.
- Assumptions.
- Evidence quality.
- Expected benefit.
- Key risks.
- Reversibility.
- Privacy impact.
- Required handoffs.
- Stop conditions.

Agents must distinguish facts from inference. If evidence is weak, they should say so directly and reduce confidence.

Use `pego/templates/agent-recommendation.md` as the default output shape for domain-agent recommendations and dissent.

Use `pego/templates/decision-packet.md` for Level 4 escalations and high-impact decisions.

Structured runtimes should preserve Level 4 escalation packets using `pego/schemas/decision-packet.schema.json`.

Use `pego/templates/council-decision.md` when multiple agent recommendations must be reconciled into one directive, revision request, information request, or escalation.

Structured runtimes should preserve council decisions using `pego/schemas/council-decision.schema.json`.

Use `pego/templates/directive-candidate.md` when a recommendation needs to be compared, prioritized, or scheduled against other directives.

## Deliberation Order

Default order:

1. Operations frames the concrete decision or directive needed.
2. Relevant domain agents make recommendations.
3. Operations classifies candidate directives by altitude using `pego/operations/directive-synthesis.md`.
4. Happiness checks whether the proposal serves the actual life objective.
5. Relationships checks protected stakeholder and household impact.
6. Finance checks capital, runway, and downside.
7. Governance checks authority, privacy, risk, evidence, and constraints.
8. Council produces a single directive, revision request, or escalation.

The order may change when the issue clearly belongs to a specific domain, but Governance should remain the final gate for high-impact actions.

## Output Shape

Each council decision should produce:

- Directive or escalation.
- Rationale.
- Expected benefit.
- Key risks.
- Dissenting views.
- Review date or success criteria.
- Governance review outcome.
- Authority level.
- Conditions or stop rules.
- Required next action.

The reference local council decision runner lives at:

```text
ops/council/synthesize_decision.py
```

It reads protected agent recommendations and writes protected council decisions under the private instance.

## Governance Gate

Council decisions do not become directives until they pass the required governance/compliance review for their authority level and risk class.

When domain agents disagree, use `pego/governance/conflict-resolution.md` before producing the final council output.

## Council Must Not

- Hide dissent to create false clarity.
- Treat confidence as evidence.
- Convert a Level 1 recommendation into execution authority.
- Use private facts in reusable public framework files.
- Optimize financial, career, health, or productivity proxies at the expense of happiness and protected relationships.
