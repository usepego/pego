# Operations

Scripts, integrations, automations, registry inspection, and local operating
machinery for PEGO.

Secrets and local credentials belong outside the reusable framework layer.

Useful tools:

- `pego_registry.py`: inspect the public PEGO system registry without reading private data.
- `pego_doctor.py`: verify repository hygiene and required framework files.
- `private/bootstrap_private_instance.py`: create a protected private instance skeleton.
- `cycles/daily_cycle.py`: run daily next/outcome/learn cycle commands.
- `cycles/weekly_cycle.py`: generate protected weekly operating plans.
- `operator/next_step.py`: select one next directive and run governance preflight.
- `context/record_context_update.py`: record protected context updates.
- `directives/generate_daily_directive.py`: create protected daily directive packets.
- `outcomes/record_outcome.py`: record protected directive outcomes.
- `governance/generate_compliance_review.py`: create protected compliance review packets.
- `finance/run_scenarios.py`: run private finance scenarios from local assumptions.
