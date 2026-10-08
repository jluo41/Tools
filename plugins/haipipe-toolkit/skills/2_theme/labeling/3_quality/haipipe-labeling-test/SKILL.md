---
name: haipipe-labeling-test
description: >-
  The Quality › Test view skill of the labeling theme: it
  owns the held-back test: re-drawing its frame when needed and locking the human's blind gold on it. Every Run in this view names this skill, and no other view uses it.
  Use for held-back test, sealed test, test-reserve, test-gold-lock, T*, blind test labels, or /haipipe-labeling-test.
metadata:
  version: "0.1.1"
  last_updated: "2026-09-29"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-labeling-test · Quality Space › Test

This skill owns the Runs of the labeling workbench's Quality › Test
view: every Run Type here declares it as its context Skill. Load
`haipipe-labeling` (the family door) and `haipipe-labeling-workflow` (the Run
graph) first. For `test-reserve`, load `haipipe-labeling-building` and
`haipipe-labeling-building`; for `test-gold-lock`, load `haipipe-labeling-scanning` and
`haipipe-labeling-scanning`. The [Run Type–Skill table](../../haipipe-labeling-building/ref/ref-space-mapping.md#run-type-skills)
is the source for these bindings. The Building or Scanning workflow gives the
Run's order.

## Runs in this view

```text
step  Run Type                     state
 2    test-reserve         not built · the first reservation happens inside corpus-contract
14    test-gold-lock       not built
```

A new Run uses `run-labeling-<operation>-<MMDD>-<target>` on disk and
on the page. Older short-named Tickets remain readable. Its Ticket is
`<Page>/runs/<run>.yaml`
and its Result `<Page>/results/<run>/`, beside `labeling/`.

`test-reserve` (not built yet) supersedes the sealed frame under custody,
only when separately commissioned. The first reservation is made before the
job exists, by `engine/fence_source.py`, and reaches the job inside
`corpus-contract`.

The human step is first and locks before any executor runs.

```text
GOLD
 1 bind       check the handoff; the Final Evaluator writes evaluation/registry.yaml
              with the fields ref-assets.md §8 lists (handoff version, candidates,
              wrappers, baseline, metrics, repeats, floors, selection rule)
                                                                  → evaluation/registry.yaml
 2 allocate   registry freezes; allocate test-gold-lock
 3 release    Test Custodian authorizes test text release, logs it → test/sealed/access_log.jsonl
 4 first      blind human record per test item, executor outputs hidden
                                                                  → test/final/human_first.jsonl
 5 consistency re-judge the declared repeat subset                → test/final/consistency.json
 6 lock       close test-gold-lock; T* gold locked                → test/final/human_gold.jsonl
                                                                    test/final/lock.json
```

A registry edited after step 3 invalidates the episode.

## Return

Return the Run address or `none`, the files written, and exactly one next
runnable Run or named human gate.
