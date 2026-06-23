# Private Storage And Backup

PEGO private instance data must be both protected and recoverable.

Git history is not the private backup system. The reusable framework can live in Git, but the private instance should live in a user-owned protected location that is naturally backed up.

## Storage Rule

Private subject data belongs in the protected private instance, not in the framework package or public repository.

Acceptable private roots include:

- A local `private/` directory that is excluded from Git and covered by a system backup.
- A `private/` symlink pointing to a backed-up private folder.
- A package-managed private root outside the framework checkout.
- A user-selected folder under iCloud Drive, Dropbox, OneDrive, Google Drive, Syncthing, Proton Drive, or another trusted backup system.
- An encrypted local path that the user confirms is covered by backup.

The system should never assume backup is present merely because files exist.

## Backup Readiness

Use:

```sh
python3 ops/private/check_storage.py
```

or:

```sh
python3 pegoctl storage
```

The checker may inspect paths and Git tracking status. It must not print private file contents.

To persist a manual backup confirmation under the protected private root:

```sh
python3 pegoctl storage --confirm-backup
```

This writes `private/governance/preflight/storage-confirmation.json` or the
equivalent path under the configured external private root. The confirmation is
private operating infrastructure, not framework content.

## Decision Values

Return one of:

- `backup_ready`: private root has a recognizable backup/sync signal.
- `backup_ready_manual`: the user explicitly confirmed backup coverage.
- `backup_not_confirmed`: private root exists but backup coverage is unknown.
- `missing_private_root`: private root does not exist.

## Install Flow

Future `pegoctl init` should ask where the private instance should live.

Default recommendation:

1. Choose a private user-owned folder already covered by backup.
2. Bootstrap PEGO private instance files there.
3. Link or configure PEGO to use that private root.
4. Run readiness and storage checks.
5. Confirm that private files are not tracked by Git.

Current local tools support:

```sh
export PEGO_PRIVATE_ROOT="/path/to/backed-up/PEGO/private"
python3 pegoctl bootstrap
python3 pegoctl storage --confirm-backup
python3 pegoctl readiness
```

or explicit one-command selection:

```sh
python3 pegoctl bootstrap --private-root "/path/to/backed-up/PEGO/private"
```

## Privacy Constraints

Storage checks must:

- Avoid printing private file contents.
- Avoid writing reports to tracked framework files.
- Avoid revealing absolute private paths unless the user explicitly asks for them.
- Avoid uploading private metadata to third-party services.
- Treat account balances, health records, relationship notes, writing samples, and telemetry as protected private data.
- Store manual backup confirmation only under the protected private root.

## Failure Handling

If backup readiness is not confirmed, PEGO may still operate, but it should surface this as an infrastructure risk before relying on private memory as the durable operating record.
