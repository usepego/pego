# PEGO Framework

Reusable framework layer for PEGO: Personal Executive Governance OS.

This directory should contain only material that can safely become public, shared, or productized.

## Scope

- Concepts and principles
- Governance models
- Agent protocols
- Templates and schemas
- Synthetic examples
- Prompt patterns
- Documentation

## Framework Order

Start here:

1. `principles.md`: the operating philosophy.
2. `architecture/agent-infrastructure.md`: why PEGO is runtime-neutral agent infrastructure, not a Python app or chatbot.
3. `architecture/runtime-options.md`: how LangGraph, Vercel AI SDK, custom services, CLI, mobile, and other runtimes should be evaluated.
4. `ux/first-run-experience.md`: how a new user first understands and adopts PEGO.
5. `templates/constitution.md`: the local delegation contract.
6. `templates/active-operating-brief.md`: the current private operating entry point.
7. `governance/authority-levels.md`: what PEGO may observe, recommend, direct, execute, or escalate.
8. `agents/council-protocol.md`: how domain agents deliberate and preserve dissent.
9. `templates/agent-recommendation.md`: the standard shape for agent outputs.
10. `templates/decision-packet.md`: the standard shape for high-impact escalations.
11. `governance/compliance-review.md`: the review gate before adoption or execution.
12. `operations/daily-loop.md`: how approved strategy becomes daily directives.
13. `operations/weekly-loop.md`: how recent outcomes become weekly priorities.
14. `operations/monthly-loop.md`: how PEGO reviews strategy, assumptions, and constitutional fit.
15. `operations/directive-synthesis.md`: how competing directives are prioritized, scheduled, deferred, or escalated.
16. `operations/operator-interface.md`: how the human asks for briefs, next directives, resynthesis, and review.
17. `operations/collaboration-modes.md`: how PEGO separates Engineering, UX, and USER work.
18. `operations/runtime-agent-protocol.md`: how an AI agent selects the correct PEGO role during a session.
19. `operations/first-run.md`: how to start a PEGO operating session from the repository root.
20. `operations/operating-readiness.md`: how to verify PEGO is ready to issue directives.
21. `operations/intra-day-command-loop.md`: how PEGO answers "what is next?" during the day.
22. `operations/outcome-review.md`: how execution results become evidence for the next directive.
23. `operations/context-update.md`: how conversation, outcomes, and telemetry update private operating memory.
24. `operations/anticipation-loop.md`: how PEGO detects future friction and asks targeted operational questions early.
25. `templates/operating-register.md`: the durable inventory of events, annoyances, supply gaps, prep needs, and strategic dependencies.

## Non-Scope

- Real personal goals
- Real telemetry
- Real health, finance, relationship, or work details
- Secrets or credentials
- Private journals or directives

## Privacy Boundary

PEGO uses a reusable framework layer and a protected private instance. Framework files may define structures, protocols, and templates, but must not contain real subject facts.

See `pego/governance/private-data-policy.md`.
