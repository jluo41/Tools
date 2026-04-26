---
name: haipipe-data-remote
description: "Cross-stage transport specialist. Pushes / pulls cohort assets between local _WorkSpace and the configured remote (S3 / GCS / Databricks / Google Drive). Wraps hai-remote-sync; never invokes destructive operations. Trigger: push, pull, sync, remote, S3, upload, download, fetch, hai-remote-sync."
argument-hint: [function] [args...]
allowed-tools: Bash, Read, Grep, Glob
---

Skill: haipipe-data-remote
==========================

Cross-stage transport specialist. Operates on every store
(0-RawStore, 1-SourceStore, 2-RecStore, 3-CaseStore, 4-AIDataStore,
5-ModelInstanceStore, 6-EndpointStore, 7-AgentWorkspace,
ExternalStore, ExternalStore/@inference). Wraps the
`hai-remote-sync` CLI; does not implement transfer logic itself.

  Function axis:  status | pull | push | diff | plan | prune

Rules baked in:

  - NEVER passes `--sync` (mirror mode) to hai-remote-sync. Copy-only.
  - NEVER issues `aws s3 rm`, `rm -rf`, or any deletion command.
  - All push / pull / plan operations dry-run first, then confirm.
  - All discovery (status, ls-equivalent) uses
    `hai-remote-sync --dry-run` -- no direct `aws s3 ls` calls.

---

Commands
--------

```
/haipipe-data-remote                              -> status (default)
/haipipe-data-remote status                       -> cross-store local↔remote drift
/haipipe-data-remote pull <store>/<name>          -> copy remote -> local (additive)
/haipipe-data-remote push <store>/<name>          -> copy local  -> remote (additive)
/haipipe-data-remote diff <store>/<name>          -> per-file local↔remote diff
/haipipe-data-remote plan --for cohort=<name>     -> dependency-aware multi-asset plan
                          [--through stage=N]
/haipipe-data-remote prune <store>                -> review local-only / remote-only;
                                                     SUGGESTS action; never deletes
```

Stores recognized:

```
0-RawStore           5-ModelInstanceStore
1-SourceStore        6-EndpointStore
2-RecStore           7-AgentWorkspace
3-CaseStore          ExternalStore
4-AIDataStore        ExternalStore/@inference
```

---

Dispatch Table
--------------

```
Invocation     This skill's ref                   fn doc
-------------  ---------------------------------  ----------------
status         ref/concepts.md + ref/store-map.md fn/fn-status.md
pull           ref/concepts.md + ref/store-map.md fn/fn-pull.md
push           ref/concepts.md + ref/store-map.md fn/fn-push.md
diff           ref/concepts.md + ref/store-map.md fn/fn-diff.md
plan           ref/concepts.md + ref/store-map.md fn/fn-plan.md
prune          ref/concepts.md + ref/store-map.md fn/fn-prune.md
(no fn arg)    same as status                     fn/fn-status.md
```

---

Step-by-Step Protocol
----------------------

Step 0: Read this skill's `ref/concepts.md` for the LOCAL_/REMOTE_
        pair model and copy-only contract. Mandatory.

Step 1: Read `ref/store-map.md` to resolve which env var corresponds
        to the requested store and the typical asset-name pattern.

Step 2: Parse args. Verbs require:
          status:  no required args (optional store filter)
          pull:    <store>/<name>
          push:    <store>/<name>
          diff:    <store>/<name>
          plan:    --for cohort=<name>  (--through stage=N optional)
          prune:   <store>

Step 3: Read the matching fn doc and execute.

Step 4: For verbs that mutate state (pull, push, plan execution):
          - Run hai-remote-sync with --dry-run FIRST
          - Show the user the proposed transfer
          - Wait for explicit confirm (yes / cancel)
          - Then run without --dry-run
        NEVER skip the dry-run step.

Step 5: Return the structured tail (status / artifacts / next).

---

What This Skill Does NOT Own
-----------------------------

  - Asset.push_to_remote() Python API     (haipipe core)
  - hai-remote-sync CLI implementation    (code/scripts/remote_sync.py)
  - env.sh                                (the user's responsibility)
  - Any deletion logic                    (intentionally absent)

The skill is pure orchestration over what already exists.

---

MUST DO / MUST NOT
-------------------

- ALWAYS read `ref/concepts.md` and `ref/store-map.md` before any verb.
- ALWAYS dry-run before a real push / pull.
- ALWAYS surface AWS SSO error hints (the DrFirst SSO URL is in
  env.sh comments) when transfers fail with credential errors.
- NEVER pass `--sync` to hai-remote-sync.
- NEVER call `aws s3 ls` / `aws s3 rm` directly. Use hai-remote-sync.
- NEVER auto-delete local-only or remote-only assets discovered by
  prune; always print and let the user act.
