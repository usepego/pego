# Anticipation Ops

Local tools for creating PEGO anticipation scans.

Anticipation scans read the protected private operating register and write one protected scan packet under `private/anticipation/scans/`. They should surface one concrete question, prep candidate, supply candidate, or deferred directive candidate before friction becomes urgent.

## Generate Anticipation Scan

```sh
python3 ops/anticipation/generate_scan.py --horizon 14-days
python3 pegoctl anticipate --horizon 14-days
```

Optional domain focus:

```sh
python3 ops/anticipation/generate_scan.py --domain Environment --horizon 7-days
python3 pegoctl anticipate --domain Environment --horizon 7-days
```

The runner prints only the output path.

For installed or backed-up operation, pass `--private-root` to `pegoctl` or to
the direct script so the operating register and scan packet stay inside the
protected private instance.
