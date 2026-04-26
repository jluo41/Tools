fn-push: Copy local -> remote for one asset
============================================

Wraps `hai-remote-sync --push` for a single asset path. Always
dry-runs first, then asks confirm, then runs. Copy-only.

---

Step 1: Parse args
-------------------

Required: `<store>/<name>` (e.g. `1-SourceStore/MyCohort`).

Resolve via `ref/store-map.md`:

  - which store flag
  - or `--path` if no flag

---

Step 2: Pre-flight
-------------------

```bash
source .venv/bin/activate && source env.sh
which hai-remote-sync >/dev/null || abort "hai-remote-sync not on PATH"

# Confirm the local asset actually exists
ls _WorkSpace/{store}/{name}/ 2>/dev/null || \
    abort "Local asset _WorkSpace/{store}/{name}/ not found"
```

---

Step 3: Dry-run
----------------

```bash
hai-remote-sync --push --path {store}/{name} --dry-run
```

Capture and display the proposed transfer.

If nothing would transfer: print and exit.

---

Step 4: Confirm
----------------

```
Will copy from LOCAL -> REMOTE:
  store:   {store}
  name:    {name}
  files:   {N}
  size:    {bytes}
  remote:  {REMOTE_ROOT}/{store}/{name}/

This is a COPY (additive). No remote files will be deleted even if
they no longer exist locally.

Proceed? (yes / cancel)
```

`yes` -> Step 5. Anything else -> exit, no transfer.

For push to a SHARED remote, this confirmation is especially
important -- a wrong --name uploads to a shared bucket.

---

Step 5: Real run
-----------------

```bash
hai-remote-sync --push --path {store}/{name}
```

Stream output. NEVER add `--sync`.

---

Step 6: Return
---------------

```
status:    ok | failed
operation: push
target:    {store}/{name}
files:     {N}
elapsed:   {seconds}s
next:      "Verify: /haipipe-data-remote diff {store}/{name}"
```

If failed with credential error: surface the SSO URL.

---

MUST NOT
---------

- Do NOT pass `--sync`.
- Do NOT skip the dry-run + confirm.
- Do NOT push without verifying the local asset exists.
- Do NOT delete any remote files at any step.
