# Operations

Scripts, integrations, automations, registry inspection, and local operating
machinery for PEGO.

Secrets and local credentials should remain outside Git.

Useful tools:

- `pego_registry.py`: inspect the public PEGO system registry without reading private data.
- `pego_doctor.py`: verify repository hygiene and required framework files.
- `private/bootstrap_private_instance.py`: create local-only private instance skeleton.
- `operator/next_step.py`: select one next directive and run governance preflight.
- `directives/generate_daily_directive.py`: create local-only daily directive packets.
- `governance/generate_compliance_review.py`: create local-only compliance review packets.
- `finance/run_scenarios.py`: run private finance scenarios from local assumptions.
