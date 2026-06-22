# Onboarding Ops

Local tools for creating PEGO onboarding intake packets.

First-run intake packets are protected private artifacts. They gather one phase of decision-grade facts at a time so onboarding does not become a giant questionnaire.

## Generate Intake Packet

```sh
python3 ops/onboarding/generate_intake.py --phase current-state
```

Common phases:

- `boundary`
- `aim`
- `current-state`
- `environment`
- `strategy`
- `health`
- `authority`

The runner writes under `private/onboarding/intake/` and prints only the output path.
