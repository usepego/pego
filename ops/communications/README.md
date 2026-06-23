# Communications Ops

Local tools for producing protected PEGO public-writing briefs and communications directive candidates.

Public-writing briefs are private operating artifacts. They may use protected voice and taste context, but they do not approve publication.

## Generate Public-Writing Brief

```sh
python3 ops/communications/generate_public_writing_brief.py
python3 pegoctl public-writing
```

Default private input:

```text
private/person/voice-and-taste.md
```

Default outputs:

```text
private/writing/briefs/
private/directives/candidates/communications-candidates.md
```

For installed or backed-up operation, pass `--private-root` to `pegoctl` or to
the direct script so voice context, writing briefs, and communications candidates
stay inside the protected private instance.

Publishing remains Level 4 until governance review explicitly clears it.
