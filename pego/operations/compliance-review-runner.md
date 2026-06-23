# Compliance Review Runner

The compliance review runner is a local helper for creating private governance review packets.

## Purpose

It turns a protected private directive file into a protected private review packet under:

```text
private/governance/reviews/
```

That directory is part of the protected private instance.

## Command

```sh
python3 ops/governance/generate_compliance_review.py --directive private/directives/daily/YYYY-MM-DD.md
python3 pegoctl compliance-review --directive private/directives/daily/YYYY-MM-DD.md
```

## Privacy

The runner may inspect a private directive to infer authority level, but it does not print directive content to stdout and does not write private content into framework files.

## Authority

The generated review is a draft governance artifact. It does not grant execution authority by itself.

Level 2 or higher actions still require explicit adoption under the private constitution and the appropriate review level.
