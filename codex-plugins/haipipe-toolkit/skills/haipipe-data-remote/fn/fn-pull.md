fn-pull: Copy remote -> local for one asset
============================================

Wraps `hai-remote-sync --pull` for a single asset path. Always
dry-runs first, then asks confirm, then runs. Copy-only.

---

Step 1: Parse args
-------------------

Required: `<store>/<name>` (e.g. `1-SourceStore/WellDoc2025CVS`).

Resolve via `ref/store-map.md`:

  - which store flag (`--source`, `--record`, ...)
  - or fall back to `--path` if the store has no flag

---

Step 2: Pre-flight
-------------------

```bash
source .venv/bin/activate && source env.sh
which hai-remote-sync >/dev/null || abort "hai-remote-sync not on PATH"
```

---

Step 3: Dry-run
----------------

```bash
hai-remote-sync --pull --path {store}/{name} --dry-run
```

Capture and display the proposed transfer (file list, total size).

If nothing would transfer ("Already in sync"): print and exit.

---

Step 4: Confirm
----------------

```
Will copy from REMOTE -> LOCAL:
  store:  {store}
  name:   {name}
  files:  {N}
  size:   {bytes}

This is a COPY (additive). No local files will be deleted even if
they no longer exist on remote.

Proceed? (yes / cancel)
```

`yes` -> Step 5. Anything else -> exit, no transfer.

---

Step 5: Real run
-----------------

```bash
hai-remote-sync --pull --path {store}/{name}
```

Stream output. NEVER add `--sync`.

---

Step 6: Verify and return
--------------------------

```bash
ls _WorkSpace/{store}/{name}/
```

```
status:    ok | failed
operation: pull
target:    {store}/{name}
files:     {N}
elapsed:   {seconds}s
next:      "Inspect: /haipipe-data-{stage} load   (or read manifest.json)"
```

If failed with credential error: surface the SSO URL.

---

MUST NOT
---------

- Do NOT pass `--sync`.
- Do NOT skip the dry-run + confirm.
- Do NOT delete any local files (rm, mv, etc.) at any step.
