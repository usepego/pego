# Synthesis Ops

Local tools for converting directive candidates into an active PEGO queue.

Directive synthesis coordinates competing domains so PEGO does not ask the human to do multiple incompatible actions at once. The output is a protected private directive queue under `private/directives/queues/`.

## Synthesize Queue

```sh
python3 ops/synthesis/synthesize_queue.py --date YYYY-MM-DD --candidate private/directives/candidates/example.md
```

Multiple candidate files may be supplied:

```sh
python3 ops/synthesis/synthesize_queue.py \
  --date YYYY-MM-DD \
  --candidate private/directives/candidates/health.md \
  --candidate private/anticipation/scans/home.md
```

The runner writes a queue for the existing next-directive tools and prints only the output path.
