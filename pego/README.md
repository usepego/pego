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
4. `architecture/runtime-options.md`: how graph orchestrators, hosted interfaces, custom services, CLI, mobile, and other runtimes should be evaluated.
5. `architecture/runtime-roadmap.md`: near-term local runtime path, future tool-server layer, and deferred hosted web reference runtime.
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
21. `templates/agent-calibration-record.md`: how PEGO preserves bounded private evidence for future agent weighting.
22. `templates/agent-message.md`: the standard shape for agent-to-agent deliberation messages.
23. `templates/deliberation-thread.md`: how PEGO preserves multi-agent deliberation before Council synthesis.
24. `templates/decision-packet.md`: the standard shape for high-impact escalations.
25. `templates/tool-contract.md`: the standard shape for capabilities agents may call.
26. `tools/README.md`: the reusable catalog of tools agents may call.
27. `templates/behavior-loop.md`: how PEGO records recurring environment-driven loops and disruption directives.
28. `templates/voice-and-taste-model.md`: the private model for style, taste, influences, and public positioning.
29. `templates/public-writing-brief.md`: the private brief for turning source material into public-safe artifacts.
30. `finance/portfolio-management-skill-policy.md`: how future portfolio analysis and trading skills are governed.
31. `health/food-environment-spec.md`: how PEGO evaluates home food, groceries, restaurants, menus, nutrition, cost, and friction for meal directives.
32. `governance/compliance-review.md`: the review gate before adoption or execution.
33. `operations/attention-governance.md`: how PEGO decides whether live events, media, rest, or highlights deserve attention.
34. `operations/recommendation-adoption.md`: how observations, recommendations, council decisions, and tool outputs become directives without gaining accidental authority.
35. `operations/recommendation-quality-loop.md`: how PEGO evaluates agent recommendations, council synthesis, and human-question value against outcomes.
36. `operations/scenario-benchmarks.md`: how PEGO evaluates public-safe synthetic scenarios against baselines and preserves failure modes.
37. `templates/scenario-benchmark.md`: the public-safe benchmark result template.
38. `operations/domain-baseline-bootstrap.md`: how PEGO gathers decision-grade domain baselines for net-new users without requiring uploads.
39. `operations/goal-reconciliation.md`: how PEGO reconciles separate domain goals into council priority rules.
40. `templates/goal-reconciliation.md`: the council dependency artifact for cross-domain directive priority.
41. `operations/state-inputs.md`: how text check-ins, outcomes, wearable activity, bank account activity, sensors, and adapters become protected state signals.
42. `templates/state-signal.md`: the normalized protected evidence artifact for human state and behavior inputs.
43. `templates/goal-progress.md`: the domain progress artifact for leading indicators, lagging indicators, trajectory, confidence, and directive attribution.
44. `templates/council-synthesis-review.md`: how PEGO evaluates whether a council decision selected, deferred, escalated, or asked well.
45. `templates/information-value-assessment.md`: how PEGO decides whether asking the human a question is worth the interruption.
46. `operations/daily-loop.md`: how approved strategy becomes daily directives.
47. `operations/weekly-loop.md`: how recent outcomes become weekly priorities.
48. `operations/monthly-loop.md`: how PEGO reviews strategy, assumptions, and constitutional fit.
49. `operations/directive-synthesis.md`: how competing directives are prioritized, scheduled, deferred, escalated, or shaped by behavior loops.
50. `operations/operator-interface.md`: how the human asks for briefs, next directives, resynthesis, and review.
51. `operations/collaboration-modes.md`: how PEGO separates Engineering, UX, and USER work.
52. `operations/runtime-agent-protocol.md`: how an AI agent selects the correct PEGO role during a session.
53. `operations/start-pego.md`: how a normal user starts PEGO through conversation while the adapter handles setup.
54. `operations/first-run.md`: how to start a PEGO operating session from the repository root.
55. `operations/local-adapter.md`: why the local command tools exist and why they are not the primary user experience.
56. `operations/operating-readiness.md`: how to verify PEGO is ready to issue directives.
57. `operations/private-storage-backup.md`: how private PEGO state is protected and backed up.
58. `operations/intra-day-command-loop.md`: how PEGO answers "what is next?" during the day.
59. `operations/circumstance-update.md`: how PEGO resynthesizes directives when location, environment, time, energy, or friction changes.
60. `operations/outcome-review.md`: how execution results become evidence for the next directive.
61. `templates/decision-quality-review.md`: how PEGO evaluates whether a directive was a good decision, not only whether it was completed.
62. `operations/context-update.md`: how conversation, outcomes, and telemetry update private operating memory.
63. `operations/operating-memory.md`: how PEGO promotes, quarantines, expires, corrects, or rejects memory.
64. `operations/anticipation-loop.md`: how PEGO detects future friction and asks targeted operational questions early.
65. `templates/operating-register.md`: the durable inventory of events, annoyances, supply gaps, prep needs, and strategic dependencies.

## Non-Scope

- Real personal goals
- Real telemetry
- Real health, finance, relationship, or work details
- Secrets or credentials
- Private journals or directives

## Privacy Boundary

PEGO uses a reusable framework layer and a protected private instance. Framework files may define structures, protocols, and templates, but must not contain real subject facts.

See `pego/governance/private-data-policy.md`.
