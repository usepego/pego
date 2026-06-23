# Operations

Reference scripts, integrations, automations, registry inspection, and local
operating machinery for PEGO.

These tools are local runtime adapters. They are not the PEGO architecture
itself. PEGO should remain defined by agent contracts, governance contracts,
directive schemas, privacy boundaries, and operating protocols that can later
run through LangGraph, Vercel AI SDK, a custom service, a mobile app, a Slack
bot, a local CLI, or another runtime.

Python is welcome here as engineering infrastructure: tests, CI checks,
repository validation, scaffolding, privacy scans, migrations, and local
developer utilities. That does not mean PEGO's product runtime is Python.

Secrets and local credentials belong outside the reusable framework layer.

Useful tools:

- `../pegoctl`: local root wrapper for common operation commands.
- `pego_registry.py`: inspect the public PEGO system registry without reading private data.
- `pego_doctor.py`: verify repository hygiene and required framework files.
- `private/bootstrap_private_instance.py`: create a protected private instance skeleton.
- `onboarding/generate_intake.py`: generate one protected first-run intake packet.
- `communications/generate_public_writing_brief.py`: generate a protected public-writing brief and communications directive candidate.
- `synthesis/synthesize_queue.py`: synthesize protected directive candidates into one active queue.
- `cycles/daily_cycle.py`: run daily next/outcome/learn cycle commands.
- `cycles/weekly_cycle.py`: generate protected weekly operating plans.
- `anticipation/generate_scan.py`: generate one protected anticipation scan from the operating register.
- `attention/decide_attention.py`: select a protected attention directive for live events, media, rest, or highlights later.
- `operator/generate_brief.py`: generate a protected operating brief from active private queue/session state.
- `operator/next_step.py`: select one next directive and run governance preflight.
- `operator/user_check_in.py`: record a USER-mode check-in, select one next directive, run preflight, and update the intra-day session log.
- `context/record_context_update.py`: record protected context updates.
- `directives/generate_daily_directive.py`: create protected daily directive packets.
- `outcomes/record_outcome.py`: record protected directive outcomes.
- `review/review_outcome.py`: convert directive outcomes into learning decisions.
- `governance/generate_compliance_review.py`: create protected compliance review packets.
- `finance/run_scenarios.py`: run private finance scenarios from local assumptions.
- `finance/review_scenarios.py`: convert scenario output into protected governance-ready finance review.
- `health/generate_candidates.py`: convert a protected health baseline into low-risk directive candidates.
- `health/decide_meal.py`: select a protected meal directive from structured food options.
- `home/generate_candidates.py`: convert operating-register home entries into environment directive candidates.
