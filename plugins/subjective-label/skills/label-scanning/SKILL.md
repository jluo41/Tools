---
name: label-scanning
description: >-
  The Scanning-side door of the subjective-label family, and its LAW: what a
  frozen Label Handoff permits, what Test, Scan and Audit may and may not
  create, which decisions are human gates, which verbs exist, and what is
  forbidden. It begins from one signed handoff and ends at audited D*. The
  order of steps lives in label-scanning-workflow. Use for sealed evaluation,
  model qualification, production labeling, risk queues, corpus scanning, spot
  checks, repair, final audit, or /label-scanning.
metadata:
  version: "0.6.0"
  last_updated: "2026-09-01"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /label-scanning · the law of executing a frozen meaning

`subjective-label` is the family umbrella; `subjective-label-workflow` declares
the phase numbers and gates; `label-scanning-workflow` orders the steps. This
door owns the LAW of the Scanning side, symmetric to `/label-building`.

## Boundary

Scanning may choose and execute an implementation of `G*`; it may not redefine
the human construct. `G*`, `D_cal*`, the corpus snapshot, and the sealed-test
reservation are read-only inputs bound by the handoff checksum. A semantic
defect found here is preserved as evidence and returned to Building under a new
lineage; it is never patched inside a Scanning Run, and neither are wrappers,
thresholds, or routing.

## The three phases and what each may create

```text
P3 Test    blind human gold T* on the sealed test, then comparable scorecards,
           then ONE qualified route under the preregistered rule, or none
P4 Scan    one terminal disposition per in-scope item, provenance-tiered;
           a candidate corpus, NOT yet D*
P5 Audit   an immutable audit receipt and, on pass, D* with bounded claims
```

Public datasets may supply separately labeled external-validity evidence. They
never replace project-specific `T*` and never license production.

Scanning uses the independently closable operations in `../../ref/ref-run.md`:

```text
P3  test-gold-lock · executor-predict* · executor-score* · executor-select
P4  scan-preflight · scan-shard* · risk-route · human-review · reconcile
P5  audit-sample · audit-human-gold · audit-analyze · dstar-materialize
```

Test, Scan, and Audit are episodes that group these Runs and their phase gates;
they are not additional umbrella Runs.

## Laws of Scanning Runs

1. **Gold before prediction.** No `executor-predict` Run starts before
   `test-gold-lock` closes; no score Run starts while any registered prediction Run is open.
2. **Registry before release.** Candidates, wrappers, metrics, floors, and
   the selection rule are frozen before protected text is released; a
   registry edited afterwards invalidates the test.
3. **"Best among failures" is not qualified.** A route qualifies only by
   passing every required floor; otherwise the route is human-only or `HOLD`.
4. **A manifest is immutable.** A changed executor, wrapper, or threshold opens
   a new Production episode with a new preflight and downstream Runs.
5. **Human review overrides, never edits.** A human production decision
   overrides the machine's label for that item and changes no policy.
6. **Unresolved is never `NONE`.** Over-capacity or undecidable items keep the
   `accepted-unresolved` disposition.
7. **The auditor is blind.** The audit design is frozen, and the human judges
   the sample, before any production label is shown.

## Human gates

```text
test gold     the human judges T* blind to every executor prediction         (P3)
risk queue    the human decides every escalated production item              (P4)
audit gold    the human judges the audit sample blind to production labels   (P5)
limitation    the human explicitly accepts any bounded final limitation      (P5)
```

No model, ensemble, or confidence threshold may write these decisions.

## Verbs

```text
enter | status       resolve the Scanning frontier from the bound handoff
test | qualify       run or resume P3
scan | produce       run or resume P4
audit | spot-check   run or resume P5
repair               apply an audit-owned repair under a new audit folder
reopen-building      route a semantic failure to a new Building lineage
workflow | run       hand the frontier to label-scanning-workflow
```

## Forbidden

- starting from `policy/current`, a draft, or an invalidated handoff;
- panel majority, nearest-neighbor inheritance, or untracked batch output as
  a terminal label;
- a scorecard on a test whose gold was visible to the executor;
- `D*` claimed without the bound final audit receipt;
- editing `G*`, `D_cal*`, a checkpoint, or a Building artifact of any kind.

## Ends at audited D*

`D*` exists only after every in-scope item has one terminal disposition and the
final audit passes or records an explicitly accepted bounded limitation. When
the Test Custodian, a blind Session recorder, the Final Evaluator, the
Production Executor with its reconciler, or the Final Audit Keeper is absent,
return `HOLD`; never emulate the missing role.
