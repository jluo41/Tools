fn-prune: Surface local-only / remote-only asymmetries
=======================================================

Read-only verb. Lists assets in one store that exist locally but not
remotely (or vice versa). NEVER deletes anything; outputs are advisory.

---

Step 1: Parse args
-------------------

Required: `<store>` (e.g. `1-SourceStore`).

---

Step 2: Pre-flight
-------------------

```bash
source .venv/bin/activate && source env.sh
```

---

Step 3: Run two dry-runs against the whole store
-------------------------------------------------

```bash
hai-remote-sync --pull --path {store} --dry-run > /tmp/pull.log 2>&1
hai-remote-sync --push --path {store} --dry-run > /tmp/push.log 2>&1
```

Group output lines by top-level asset name (first path component).

---

Step 4: Categorize
-------------------

```
remote-only assets   -- present in /tmp/pull.log only
                        candidates to PULL or to leave untouched
local-only assets    -- present in /tmp/push.log only
                        candidates to PUSH (publish) or DELETE locally
both-modified        -- present in BOTH logs
                        drifted on both sides; manual reconciliation
in-sync              -- in neither log
```

Within local-only, categorize further by mtime:

  - recent (< 30 days): probably WIP, leave alone
  - older (>= 30 days): possibly stale; suggest review

---

Step 5: Render
---------------

```
Prune review: {store}

local-only ({N} sets):
  {name}    mtime={date}   size={bytes}   age={days}d
  ...
  Hint: to publish:        /haipipe-data-remote push {store}/{name}
        to delete locally: rm -rf _WorkSpace/{store}/{name}/  (you, not me)

remote-only ({N} sets):
  {name}    last seen on remote {date if discoverable}
  ...
  Hint: to fetch:   /haipipe-data-remote pull {store}/{name}

both-modified ({N} sets):
  {name}    diverged -- run /haipipe-data-remote diff {store}/{name}
  ...

in-sync ({M} sets, not listed)

This skill never deletes anything. Run any rm commands yourself.
```

---

Step 6: Return
---------------

```
status:          ok
store:           {store}
local_only:      {N}
remote_only:     {N}
both_modified:   {N}
in_sync:         {M}
next:            "/haipipe-data-remote push|pull <store>/<name>   (act on a hint)"
                 "/haipipe-data-remote diff <store>/<name>        (inspect divergence)"
```

---

MUST NOT
---------

- Do NOT delete any file (local or remote) under any circumstance.
- Do NOT print rm commands as if the skill will run them -- always
  frame deletions as "you, the user, run this if you want to".
- Do NOT cache results.
