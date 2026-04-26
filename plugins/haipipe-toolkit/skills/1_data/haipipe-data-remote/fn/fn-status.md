fn-status: Cross-store local↔remote drift
==========================================

Default verb (no-arg). Probes every store via two `hai-remote-sync`
dry-runs and renders a one-screen drift summary.

Always live. Always thin (uses only hai-remote-sync, never direct
aws / gsutil / etc commands).

---

Step 0: Resolve scope
----------------------

Read env.sh to find every (LOCAL_*, REMOTE_*) pair. Also accept an
optional filter:

  /haipipe-data-remote status                -> all stores
  /haipipe-data-remote status 1-SourceStore  -> just that one

---

Step 1: Sanity check
---------------------

```bash
which hai-remote-sync >/dev/null || \
    echo "hai-remote-sync not on PATH. Did pip install -e succeed?"

source .venv/bin/activate && source env.sh
echo "REMOTE_ROOT=$REMOTE_ROOT"
```

If `REMOTE_ROOT` is unset, abort with an env.sh hint.

---

Step 2: Probe each store with two dry-runs
-------------------------------------------

For each store path (e.g. `1-SourceStore`):

```bash
# Pull dry-run = remote-only OR remote-newer
hai-remote-sync --pull --path {store} --dry-run 2>&1 | tee /tmp/pull_{store}.log

# Push dry-run = local-only OR local-newer
hai-remote-sync --push --path {store} --dry-run 2>&1 | tee /tmp/push_{store}.log
```

Parse the output. The `aws` / `rclone` dry-run lines look like:

```
(dryrun) download: s3://.../1-SourceStore/WellDoc2025CVS/Ptt.parquet to ...
(dryrun) upload:   ./_WorkSpace/1-SourceStore/MyCohort/manifest.json to s3://...
```

Group by top-level asset name (the first path component under the
store) so the summary collapses many-files-per-asset into per-asset
counts.

---

Step 3: Build the drift table
------------------------------

For each store, count:

```
in_sync       assets neither dry-run mentioned
remote_only   assets only the --pull dry-run mentioned
local_only    assets only the --push dry-run mentioned
out_of_sync   assets BOTH dry-runs mentioned (drift in both directions)
```

Note: `--pull --dry-run` does NOT distinguish "remote-only" from
"remote-newer". Either way, pulling would copy. Same for push. For
the headline summary, grouping them as "would copy" is enough.

---

Step 4: Render
---------------

```
Remote: $REMOTE_ROOT
Probing 9 stores via hai-remote-sync --dry-run (live, ~30s)...

store               local-only   remote-only   in-sync   out-of-sync
0-RawStore          2 sets       -             7         -
1-SourceStore       -            10 sets       2         -
2-RecStore          -            4 sets        0         -
3-CaseStore         -            3 sets        0         -
...
ExternalStore       -            @260315R5     @260104R4 -

Hints (no automatic action):
  - {N} remote-only sets to fetch:    /haipipe-data-remote pull <store>/<name>
  - {N} local-only sets to publish:   /haipipe-data-remote push <store>/<name>
  - Newer ExternalStore release on remote: review with /haipipe-data-external
```

If a store probe fails with an auth error, mark that row as `auth?`
and append the SSO URL hint at the bottom.

---

Step 5: Return tail
--------------------

```
status:        ok | partial (some stores failed)
total assets:  N local, M remote
drift:         X remote-only, Y local-only, Z out-of-sync
elapsed:       {seconds}s
next:          "/haipipe-data-remote pull <store>/<name>   (single asset)"
               "/haipipe-data-remote plan --for cohort=... (multi-asset)"
```

---

MUST NOT
---------

- Do NOT call `aws s3 ls` / `gsutil ls` directly.
- Do NOT cache remote listings (always live).
- Do NOT actually transfer anything during status -- it is read-only.
- Do NOT pass `--sync` to any hai-remote-sync invocation.
