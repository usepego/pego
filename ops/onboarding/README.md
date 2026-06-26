# Onboarding Ops

Local tools for creating PEGO onboarding intake packets.

First-run intake packets are protected private artifacts. They gather one phase of decision-grade facts at a time so onboarding does not become a giant questionnaire.

## Generate Intake Packet

```sh
python3 ops/onboarding/generate_intake.py --phase current-state
python3 pegoctl intake --phase current-state
```

Common phases:

- `boundary`
- `aim`
- `current-state`
- `environment`
- `strategy`
- `health`
- `finance-baseline`
- `career-baseline`
- `home-baseline`
- `relationships-baseline`
- `exploration-baseline`
- `communications-baseline`
- `happiness-baseline`
- `goal-reconciliation`
- `authority`

The runner writes under `private/onboarding/intake/` and prints only the output path.
For installed or backed-up operation, pass `--private-root` to `pegoctl` or to
the direct script so intake packets stay inside the protected private instance.

Baseline phases are for net-new users or domains without decision-grade private
state. They should collect rough but useful facts and unknowns, not force full
uploads, account links, quantified-self tracking, or complete life plans.

Run `goal-reconciliation` after enough domain baselines exist for Council to
decide cross-domain priority. It creates the priority model Council needs to
select the best directive rather than simply the most available one.
