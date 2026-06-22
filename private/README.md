# Private PEGO Instance

This directory is reserved for the real private PEGO instance.

Private instance files should remain local-only and ignored by Git.

Do not commit actual goals, values, constraints, telemetry, directives, journals, health information, finances, relationship context, work context, or other personal material.

Use local ignored files under `private/` for the private instance. Keep reusable framework material under `pego/`.

To create a local private skeleton, run:

```sh
python3 ops/private/bootstrap_private_instance.py
```
