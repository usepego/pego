# Local Adapter Operation

This document is for developers, maintainers, and early framework operators who
need to verify or exercise PEGO locally.

It is not the primary user experience.

A normal PEGO user should experience PEGO through delivered directives,
operating briefs, targeted questions, and outcome reviews. The local adapter
exists so the framework can be inspected, tested, and used before a polished
runtime surface exists.

## Use Cases

Use the local adapter when you need to:

- Verify repository hygiene.
- Confirm the private-instance boundary.
- Bootstrap local private skeleton files.
- Generate sample or private operating artifacts.
- Exercise directive, council, finance, health, governance, and review loops.
- Test runtime-neutral schemas and operation contracts.
- Develop future adapters without leaking private data.

## Reference Command Surface

The local reference command wrapper is `pegoctl`.

```sh
python3 pegoctl doctor
python3 pegoctl guide
python3 pegoctl readiness
python3 pegoctl storage --confirm-backup
python3 pegoctl intake --phase boundary
python3 pegoctl daily-directive
python3 pegoctl daily health-check-in
python3 pegoctl weekly
python3 pegoctl monthly
python3 pegoctl finance-run --write-summary
python3 pegoctl finance-review
python3 pegoctl health-candidates
python3 pegoctl meal --option private/health/food-options/options.json
python3 pegoctl home-candidates
python3 pegoctl anticipate --domain Environment
python3 pegoctl attention --option private/attention/options/options.json
python3 pegoctl compliance-review --directive private/directives/daily/YYYY-MM-DD.md
python3 pegoctl public-writing
python3 pegoctl brief
python3 pegoctl check-in "Done: breakfast. Available: 45 minutes. What's next?"
python3 pegoctl close-session
python3 pegoctl promote-context
python3 pegoctl apply-context
```

## First Local Verification

From a fresh checkout:

```sh
python3 pegoctl doctor
python3 pegoctl bootstrap
python3 pegoctl guide
```

What these prove:

- `doctor` passing means the reusable framework is structurally healthy.
- `bootstrap` creates missing private skeleton paths without overwriting
  existing private files unless `--force` is passed.
- `guide` reports safe operating status and the recommended next local adapter
  command without printing private contents or absolute private paths.

## External Private Root

For protected operation outside the framework checkout, set `PEGO_PRIVATE_ROOT`
or pass `--private-root` before the command:

```sh
python3 pegoctl --private-root ~/Documents/PEGO/private guide
python3 pegoctl --private-root ~/Documents/PEGO/private check-in "Done: lunch. Available: 30 minutes. What's next?"
```

## Runtime Boundary

`pegoctl` is a local adapter around checked-in operation scripts. It is not the
PEGO runtime.

Future interfaces may be CLI, chat, mobile, watch, messaging, web, email,
calendar, or another surface, but they should preserve the same agent contracts,
schemas, governance checks, and private-instance boundary.

## Python Tooling Boundary

The local Python scripts are maintenance, validation, reference, and adapter
tooling. They exist to keep the framework inspectable, testable, and usable
before a polished prompt-agent runtime exists.

They should not become the hidden product authority or the required core user
experience. PEGO's functional behavior should remain expressible as
prompt/protocol-based agent work: domain recommendations, council reasoning,
governance review, directive synthesis, outcome review, memory promotion, and
strategy review.

When a script implements reusable behavior, the same behavior should be
documented in public-safe protocols, templates, schemas, or tool contracts so a
future prompt-agent, mobile, chat, or service adapter can run PEGO without
depending on that script.
