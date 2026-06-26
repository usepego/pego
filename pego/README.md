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
5. `architecture/runtime-roadmap.md`: near-term Codex runtime path, future MCP layer, and deferred Vercel AI SDK reference runtime.
6. `architecture/runtime-adapter-lifecycle.md`: the lifecycle every runtime adapter must preserve.
7. `architecture/distribution-installation.md`: how PEGO becomes installable without becoming runtime-specific.
8. `ux/first-run-experience.md`: how a new user first understands and adopts PEGO.
9. `ux/user-journey.md`: the awareness-to-day-one path from public promise to first meaningful directive.
10. `ux/example-first-use-walkthrough.md`: a concrete synthetic acceptance test from site discovery to first outcome.
11. `ux/user-mode-simulation.md`: how to test whether PEGO feels like a working governed agent system.
12. `ux/public-site-positioning.md`: how the public PEGO site should introduce the category.
13. `templates/constitution.md`: the local delegation contract.
14. `templates/active-operating-brief.md`: the current private operating entry point.
15. `governance/authority-levels.md`: what PEGO may observe, recommend, direct, execute, or escalate.
16. `agents/council-protocol.md`: how domain agents deliberate and preserve dissent.
17. `agents/communications-agent.md`: how PEGO governs voice, taste, public writing, and opportunity-oriented communication.
18. `schemas/README.md`: runtime-neutral artifact contracts for future adapters.
19. `templates/agent-recommendation.md`: the standard shape for agent outputs.
20. `templates/agent-recommendation-review.md`: how PEGO evaluates whether an agent recommendation improved outcomes.
21. `templates/agent-message.md`: the standard shape for agent-to-agent deliberation messages.
22. `templates/deliberation-thread.md`: how PEGO preserves multi-agent deliberation before Council synthesis.
23. `templates/decision-packet.md`: the standard shape for high-impact escalations.
24. `templates/tool-contract.md`: the standard shape for capabilities agents may call.
25. `tools/README.md`: the reusable catalog of tools agents may call.
26. `templates/behavior-loop.md`: how PEGO records recurring environment-driven loops and disruption directives.
27. `templates/voice-and-taste-model.md`: the private model for style, taste, influences, and public positioning.
28. `templates/public-writing-brief.md`: the private brief for turning source material into public-safe artifacts.
29. `finance/portfolio-management-skill-policy.md`: how future portfolio analysis and trading skills are governed.
30. `health/food-environment-spec.md`: how PEGO evaluates home food, groceries, restaurants, menus, nutrition, cost, and friction for meal directives.
31. `governance/compliance-review.md`: the review gate before adoption or execution.
32. `operations/attention-governance.md`: how PEGO decides whether live events, media, rest, or highlights deserve attention.
33. `operations/recommendation-adoption.md`: how observations, recommendations, council decisions, and tool outputs become directives without gaining accidental authority.
34. `operations/recommendation-quality-loop.md`: how PEGO evaluates agent recommendations, council synthesis, and human-question value against outcomes.
35. `operations/domain-baseline-bootstrap.md`: how PEGO gathers decision-grade domain baselines for net-new users without requiring uploads.
36. `operations/goal-reconciliation.md`: how PEGO reconciles separate domain goals into council priority rules.
37. `templates/goal-reconciliation.md`: the council dependency artifact for cross-domain directive priority.
38. `templates/council-synthesis-review.md`: how PEGO evaluates whether a council decision selected, deferred, escalated, or asked well.
39. `templates/information-value-assessment.md`: how PEGO decides whether asking the human a question is worth the interruption.
40. `operations/daily-loop.md`: how approved strategy becomes daily directives.
41. `operations/weekly-loop.md`: how recent outcomes become weekly priorities.
42. `operations/monthly-loop.md`: how PEGO reviews strategy, assumptions, and constitutional fit.
43. `operations/directive-synthesis.md`: how competing directives are prioritized, scheduled, deferred, or escalated.
44. `operations/operator-interface.md`: how the human asks for briefs, next directives, resynthesis, and review.
45. `operations/collaboration-modes.md`: how PEGO separates Engineering, UX, and USER work.
46. `operations/runtime-agent-protocol.md`: how an AI agent selects the correct PEGO role during a session.
47. `operations/start-pego.md`: how a normal user starts PEGO through conversation while the adapter handles setup.
48. `operations/first-run.md`: how to start a PEGO operating session from the repository root.
49. `operations/local-adapter.md`: why the local command tools exist and why they are not the primary user experience.
50. `operations/operating-readiness.md`: how to verify PEGO is ready to issue directives.
51. `operations/private-storage-backup.md`: how private PEGO state is protected and backed up.
52. `operations/intra-day-command-loop.md`: how PEGO answers "what is next?" during the day.
53. `operations/circumstance-update.md`: how PEGO resynthesizes directives when location, environment, time, energy, or friction changes.
54. `operations/outcome-review.md`: how execution results become evidence for the next directive.
55. `templates/decision-quality-review.md`: how PEGO evaluates whether a directive was a good decision, not only whether it was completed.
56. `operations/context-update.md`: how conversation, outcomes, and telemetry update private operating memory.
57. `operations/operating-memory.md`: how PEGO promotes, quarantines, expires, corrects, or rejects memory.
58. `operations/anticipation-loop.md`: how PEGO detects future friction and asks targeted operational questions early.
59. `templates/operating-register.md`: the durable inventory of events, annoyances, supply gaps, prep needs, and strategic dependencies.

## Non-Scope

- Real personal goals
- Real telemetry
- Real health, finance, relationship, or work details
- Secrets or credentials
- Private journals or directives

## Privacy Boundary

PEGO uses a reusable framework layer and a protected private instance. Framework files may define structures, protocols, and templates, but must not contain real subject facts.

See `pego/governance/private-data-policy.md`.
