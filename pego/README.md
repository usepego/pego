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
3. `architecture/tool-contracts.md`: how agents call bounded tools without making the tool implementation the PEGO runtime.
4. `architecture/runtime-options.md`: how LangGraph, Vercel AI SDK, custom services, CLI, mobile, and other runtimes should be evaluated.
5. `architecture/runtime-adapter-lifecycle.md`: the lifecycle every runtime adapter must preserve.
6. `architecture/distribution-installation.md`: how PEGO becomes installable without becoming runtime-specific.
7. `ux/first-run-experience.md`: how a new user first understands and adopts PEGO.
8. `ux/public-site-positioning.md`: how the public PEGO site should introduce the category.
9. `templates/constitution.md`: the local delegation contract.
10. `templates/active-operating-brief.md`: the current private operating entry point.
11. `governance/authority-levels.md`: what PEGO may observe, recommend, direct, execute, or escalate.
12. `agents/council-protocol.md`: how domain agents deliberate and preserve dissent.
13. `agents/communications-agent.md`: how PEGO governs voice, taste, public writing, and opportunity-oriented communication.
14. `schemas/README.md`: runtime-neutral artifact contracts for future adapters.
15. `templates/agent-recommendation.md`: the standard shape for agent outputs.
16. `templates/agent-message.md`: the standard shape for agent-to-agent deliberation messages.
17. `templates/deliberation-thread.md`: how PEGO preserves multi-agent deliberation before Council synthesis.
18. `templates/decision-packet.md`: the standard shape for high-impact escalations.
19. `templates/tool-contract.md`: the standard shape for capabilities agents may call.
20. `tools/README.md`: the reusable catalog of tools agents may call.
21. `templates/behavior-loop.md`: how PEGO records recurring environment-driven loops and disruption directives.
22. `templates/voice-and-taste-model.md`: the private model for style, taste, influences, and public positioning.
23. `templates/public-writing-brief.md`: the private brief for turning source material into public-safe artifacts.
24. `finance/portfolio-management-skill-policy.md`: how future portfolio analysis and trading skills are governed.
25. `health/food-environment-spec.md`: how PEGO evaluates home food, groceries, restaurants, menus, nutrition, cost, and friction for meal directives.
26. `governance/compliance-review.md`: the review gate before adoption or execution.
27. `operations/attention-governance.md`: how PEGO decides whether live events, media, rest, or highlights deserve attention.
28. `operations/recommendation-adoption.md`: how observations, recommendations, council decisions, and tool outputs become directives without gaining accidental authority.
29. `operations/daily-loop.md`: how approved strategy becomes daily directives.
30. `operations/weekly-loop.md`: how recent outcomes become weekly priorities.
31. `operations/monthly-loop.md`: how PEGO reviews strategy, assumptions, and constitutional fit.
32. `operations/directive-synthesis.md`: how competing directives are prioritized, scheduled, deferred, or escalated.
33. `operations/operator-interface.md`: how the human asks for briefs, next directives, resynthesis, and review.
34. `operations/collaboration-modes.md`: how PEGO separates Engineering, UX, and USER work.
35. `operations/runtime-agent-protocol.md`: how an AI agent selects the correct PEGO role during a session.
36. `operations/start-pego.md`: how a normal user starts PEGO through conversation while the adapter handles setup.
37. `operations/first-run.md`: how to start a PEGO operating session from the repository root.
38. `operations/local-adapter.md`: why the local command tools exist and why they are not the primary user experience.
39. `operations/operating-readiness.md`: how to verify PEGO is ready to issue directives.
40. `operations/private-storage-backup.md`: how private PEGO state is protected and backed up.
41. `operations/intra-day-command-loop.md`: how PEGO answers "what is next?" during the day.
42. `operations/circumstance-update.md`: how PEGO resynthesizes directives when location, environment, time, energy, or friction changes.
43. `operations/outcome-review.md`: how execution results become evidence for the next directive.
44. `operations/context-update.md`: how conversation, outcomes, and telemetry update private operating memory.
45. `operations/anticipation-loop.md`: how PEGO detects future friction and asks targeted operational questions early.
46. `templates/operating-register.md`: the durable inventory of events, annoyances, supply gaps, prep needs, and strategic dependencies.

## Non-Scope

- Real personal goals
- Real telemetry
- Real health, finance, relationship, or work details
- Secrets or credentials
- Private journals or directives

## Privacy Boundary

PEGO uses a reusable framework layer and a protected private instance. Framework files may define structures, protocols, and templates, but must not contain real subject facts.

See `pego/governance/private-data-policy.md`.
