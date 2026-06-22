fn-diff: Per-file local↔remote diff for one asset
==================================================

Read-only verb. Runs both `--pull --dry-run` and `--push --dry-run`
for a single asset path; renders the bidirectional diff.

---

Step 1: Parse args
-------------------

Required: `<store>/<name>` (e.g. `1-SourceStore/WellDoc2025CVS`).

---

Step 2: Pre-flight
-------------------

```bash
source .venv/bin/activate && source env.sh
which hai-remote-sync >/dev/null || abort
```

---

Step 3: Two dry-runs
---------------------

```bash
hai-remote-sync --pull --path {store}/{name} --dry-run > /tmp/pull.log 2>&1
hai-remote-sync --push --path {store}/{name} --dry-run > /tmp/push.log 2>&1
```

---

Step 4: Render
---------------

Parse each dry-run log into per-file lines. Bucket them:

```
{store}/{name}  diff:

REMOTE -> LOCAL would copy ({N} files, {size}):
  {file}   {size}
  ...

LOCAL -> REMOTE would copy ({N} files, {size}):
  {file}   {size}
  ...

In sync: {M} files (not listed)
```

If both lists are empty: print "Asset is in sync." and return.

If a file appears in BOTH lists, it has drifted on both sides --
flag this prominently:

```
WARNING: divergent files (changed on both sides):
  {file}   local mtime / remote mtime  (manual reconciliation needed)
```

The user resolves divergent files manually -- the skill cannot pick
a winner.

---

Step 5: Return
---------------

```
status:        ok
operation:     diff
target:        {store}/{name}
remote_only:   {N} files
local_only:    {N} files
divergent:     {N} files     (out of sync on both sides)
in_sync:       {M} files
next:          "/haipipe-data-remote pull {store}/{name}   (fetch remote -> local)"
               "/haipipe-data-remote push {store}/{name}   (publish local -> remote)"
```

---

MUST NOT
---------

- Do NOT transfer anything (dry-run only).
- Do NOT call `aws s3 ls` / `gsutil ls` directly.
- Do NOT auto-resolve divergent files -- always require user action.
