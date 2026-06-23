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
16. `templates/decision-packet.md`: the standard shape for high-impact escalations.
17. `templates/tool-contract.md`: the standard shape for capabilities agents may call.
18. `tools/README.md`: the reusable catalog of tools agents may call.
19. `templates/behavior-loop.md`: how PEGO records recurring environment-driven loops and disruption directives.
20. `templates/voice-and-taste-model.md`: the private model for style, taste, influences, and public positioning.
21. `templates/public-writing-brief.md`: the private brief for turning source material into public-safe artifacts.
22. `finance/portfolio-management-skill-policy.md`: how future portfolio analysis and trading skills are governed.
23. `health/food-environment-spec.md`: how PEGO evaluates home food, groceries, restaurants, menus, nutrition, cost, and friction for meal directives.
24. `governance/compliance-review.md`: the review gate before adoption or execution.
25. `operations/attention-governance.md`: how PEGO decides whether live events, media, rest, or highlights deserve attention.
26. `operations/daily-loop.md`: how approved strategy becomes daily directives.
27. `operations/weekly-loop.md`: how recent outcomes become weekly priorities.
28. `operations/monthly-loop.md`: how PEGO reviews strategy, assumptions, and constitutional fit.
29. `operations/directive-synthesis.md`: how competing directives are prioritized, scheduled, deferred, or escalated.
30. `operations/operator-interface.md`: how the human asks for briefs, next directives, resynthesis, and review.
31. `operations/collaboration-modes.md`: how PEGO separates Engineering, UX, and USER work.
32. `operations/runtime-agent-protocol.md`: how an AI agent selects the correct PEGO role during a session.
33. `operations/start-pego.md`: how a normal user starts PEGO through conversation while the adapter handles setup.
34. `operations/first-run.md`: how to start a PEGO operating session from the repository root.
35. `operations/local-adapter.md`: why the local command tools exist and why they are not the primary user experience.
36. `operations/operating-readiness.md`: how to verify PEGO is ready to issue directives.
37. `operations/private-storage-backup.md`: how private PEGO state is protected and backed up.
38. `operations/intra-day-command-loop.md`: how PEGO answers "what is next?" during the day.
39. `operations/circumstance-update.md`: how PEGO resynthesizes directives when location, environment, time, energy, or friction changes.
40. `operations/outcome-review.md`: how execution results become evidence for the next directive.
41. `operations/context-update.md`: how conversation, outcomes, and telemetry update private operating memory.
42. `operations/anticipation-loop.md`: how PEGO detects future friction and asks targeted operational questions early.
43. `templates/operating-register.md`: the durable inventory of events, annoyances, supply gaps, prep needs, and strategic dependencies.

## Non-Scope

- Real personal goals
- Real telemetry
- Real health, finance, relationship, or work details
- Secrets or credentials
- Private journals or directives

## Privacy Boundary

PEGO uses a reusable framework layer and a protected private instance. Framework files may define structures, protocols, and templates, but must not contain real subject facts.

See `pego/governance/private-data-policy.md`.
