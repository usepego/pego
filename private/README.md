# Private PEGO Instance

This directory is reserved for the real protected private PEGO instance.

The private instance is PEGO's protected local operating state: real goals, constraints, telemetry, directives, outcomes, and operating memory.

Do not commit actual goals, values, constraints, telemetry, directives, journals, health information, finances, relationship context, work context, or other personal material.

Keep reusable framework material under `pego/`. Keep real operating state in the protected private instance.

To create a local private skeleton, run:

```sh
python3 ops/private/bootstrap_private_instance.py
```
