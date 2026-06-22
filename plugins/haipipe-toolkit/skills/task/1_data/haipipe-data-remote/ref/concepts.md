haipipe-data-remote: Concepts
==============================

Cross-stage transport over the LOCAL_/REMOTE_ pair model. The skill
is a thin wrapper over `hai-remote-sync`; this doc explains the
underlying model so the wrapper's verbs make sense.

---

The LOCAL_/REMOTE_ Pair Model
==============================

Every store has paired env vars in env.sh:

```
LOCAL_RAW_STORE              REMOTE_RAWDATA_STORE   (note the name asymmetry)
LOCAL_SOURCE_STORE           REMOTE_SOURCE_STORE
LOCAL_RECORD_STORE           REMOTE_RECORD_STORE
LOCAL_CASE_STORE             REMOTE_CASE_STORE
LOCAL_AIDATA_STORE           REMOTE_AIDATA_STORE
LOCAL_MODELINSTANCE_STORE    REMOTE_MODELINSTANCE_STORE
LOCAL_ENDPOINT_STORE         REMOTE_ENDPOINT_STORE
LOCAL_AGENTWORKSPACE_STORE   REMOTE_AGENTWORKSPACE_STORE
LOCAL_EXTERNAL_STORE         REMOTE_EXTERNAL_STORE
LOCAL_REFERENCE_STORE        REMOTE_REFERENCE_STORE
```

`REMOTE_ROOT` is the prefix shared by all `REMOTE_*` paths. Default
in this repo:

```
s3://rxinform-analytics-personalization/000-RxInform-JHU-AI-Repo/workspace_local_dev
```

Each `REMOTE_*_STORE = ${REMOTE_ROOT}/<store-folder>/`.

The asset path under each store is `{name}/...` -- the same shape on
both sides. So pulling `1-SourceStore/WellDoc2025CVS` means transferring:

```
s3://.../1-SourceStore/WellDoc2025CVS/   <-->   _WorkSpace/1-SourceStore/WellDoc2025CVS/
```

---

Supported Backends
===================

The wrapped `hai-remote-sync` autodetects the backend from the
`REMOTE_ROOT` URL prefix and dispatches to the right CLI:

```
prefix         backend           tool
-------------- ----------------- -------------
s3://          AWS S3            aws
gs://          Google Cloud      gsutil
dbfs://        Databricks DBFS   databricks
gdrive:        Google Drive      rclone
<remote>:      Custom rclone     rclone
```

Tool availability is checked at first use; missing tools surface an
install URL.

---

Copy-Only Contract
===================

This skill ALWAYS uses copy semantics. Concretely:

  - `pull`: adds remote files to local; never deletes local files
            even if they no longer exist on remote.
  - `push`: adds local files to remote; never deletes remote files
            even if they no longer exist locally.
  - hai-remote-sync's `--sync` flag (mirror mode, deletes) is
    DISALLOWED. The skill never passes it.

If the user wants to delete out-of-band files on either side, they do
that themselves with full eyes-on context. The skill's `prune` verb
surfaces such asymmetries but never acts on them.

This is a deliberate safety choice. CLAUDE.md's "destructive
operations" rule applies hard here -- a one-character wrong flag can
wipe a remote.

---

Discovery via --dry-run (no aws s3 ls)
=======================================

`hai-remote-sync` has no `list` verb, but its `--dry-run` mode prints
every file the underlying tool *would* transfer. We use this for
discovery:

```
--pull --dry-run on local against remote   ->  remote-only OR remote-newer
--push --dry-run on local against remote   ->  local-only  OR local-newer
neither path lists the file                ->  in sync
```

Two dry-runs per store covers all four diff buckets. The skill
NEVER calls `aws s3 ls` / `gsutil ls` directly -- everything goes
through hai-remote-sync, which keeps the backend abstraction intact.

Cost: each dry-run hits the bucket. Always live (no caching). On a
large bucket this can take 10-30s per store.

---

How `hai-remote-sync` Is Invoked
=================================

The CLI accepts two modes; the skill uses both.

**Path mode** (any subpath of any store):

```bash
hai-remote-sync --push --path 1-SourceStore/WellDoc2025CVS
hai-remote-sync --pull --path 2-RecStore
hai-remote-sync --pull --path 1-SourceStore --dry-run
```

**Named-store mode** (typed convenience):

```bash
hai-remote-sync --pull --source --name WellDoc2025CVS
hai-remote-sync --push --record --name MyRecordSet
```

Store flags available:
`--rawdata --source --record --case --aidata --model --endpoint --external`

The skill prefers path mode for status / diff / plan because it's
unambiguous; named-store mode is fine for explicit pull / push.

---

Credentials
============

The default REMOTE_ROOT is on DrFirst's AWS account. Users authenticate
via SSO. When transfers fail with credential errors:

  - Source the relevant DrFirst SSO portal:
    https://d-90676d90da.awsapps.com/start/#/?tab=accounts
  - Refresh tokens; export `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`,
    `AWS_SESSION_TOKEN` per the SSO flow.
  - Re-source env.sh.

The skill does NOT actively check credentials. When a transfer fails
with an auth error, surface the SSO URL and exit cleanly.

---

What This Skill Adds Over Calling hai-remote-sync Directly
============================================================

  status   one-screen drift summary across all stores
  diff     per-asset preview (just dry-run shaped for one asset)
  plan     dependency-aware multi-pull (resolves cohort + externals
           + record/case dependencies in one go)
  prune    visibility into local-only / remote-only asymmetries
           that direct hai-remote-sync calls do not show

For one-shot single-asset pulls/pushes, calling hai-remote-sync
directly is fine and equivalent. The skill exists for the workflows
above where N+1 calls and parsing would otherwise be required.

---

MUST DO
========

1. Source env.sh before any hai-remote-sync invocation.
2. Always dry-run before a real push or pull.
3. Surface SSO URL on credential errors.
4. Honor `--version @{tag}` for ExternalStore where the user pinned.

---

MUST NOT
=========

1. NEVER pass `--sync` to hai-remote-sync.
2. NEVER call `aws s3 rm`, `aws s3 sync --delete`, or any direct
   deletion.
3. NEVER call `aws s3 ls` directly -- use `hai-remote-sync --dry-run`.
4. NEVER auto-execute prune's findings -- always print and stop.
5. NEVER modify env.sh.
