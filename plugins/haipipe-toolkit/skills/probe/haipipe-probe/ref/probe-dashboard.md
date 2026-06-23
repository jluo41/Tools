# Probe Dashboard

This defines the behavior of `/haipipe-probe` with no arguments and the panel
rendered by `/haipipe-probe <probe>`.

The dashboard is a derive-from-disk preflight. It orients the session before the
Probe Console or any lifecycle step acts.

## Golden Rule

```text
Never report a step as done because probe.yaml says so.
A step is done only when its expected artifact resolves on disk.
When stored status and disk disagree, disk wins and the gap is flagged DRIFT.
```

## Lifecycle Frontier

The dashboard uses the current probe lifecycle:

```text
Plan -> Gather -> Read -> Judge -> Deposit
```

The frontier is the first step whose disk predicate fails.

| Step | Done when | Next action if frontier |
|---|---|---|
| `Plan` | `probe.yaml` exists and has `claim` + `evidence_plan` | `/haipipe-probe plan ...` |
| `Gather` | required evidence refs/calls are present and linked/requested artifacts resolve or are explicitly pending | `/haipipe-probe gather <probe> ...` |
| `Read` | `evidence.md` exists and `probe.yaml.result` is present | `/haipipe-probe read <probe>` |
| `Judge` | `verdict.md` exists and `probe.yaml.verdict` is present | `/haipipe-probe judge <probe>` |
| `Deposit` | `deposit.md` exists and `probe.yaml.deposit` has a final status | `/haipipe-probe deposit <probe>` |

Glyphs:

```text
OK       done
ACTIVE   current frontier
TODO     not reached
DRIFT    stored state claims progress but disk predicate fails
BLOCKED  explicit blocker
```

## Shallow Check

For each active probe folder:

1. Read `probe.yaml`.
2. Extract path-like refs from `source`, `evidence_refs`, `calls`, `result`,
   `verdict`, and `return`.
3. Resolve refs against the project root.
4. Mark missing refs as drift if stored state depends on them.
5. Do not parse heavy artifacts or run integrity audits here.

Path-like refs include project-relative paths starting with:

```text
tasks/
discoveries/
insights/
probes/
paper/
applications/
```

## Render Skeleton

Same shape as the paper dashboard panel (header + one-line story + a lifecycle
progress bar), so paper and probe read consistently. probe's "story" is the claim.

The lifecycle strip (the `progress` line) is NOT hand-typed. Render it with the
deterministic helper so it can never be mis-ordered or mis-marked:

```sh
sh "$CLAUDE_SKILL_DIR/ref/stage-strip.sh" probes/<probe>
```

It prints 1-2 lines — the strip, plus a `← here` frontier reason — derived purely
from disk (the Golden Rule above): a step is ✅ only when its artifact resolves,
▶️ marks the first failing step, and `⚠ drift` appears when a linked ref no
longer resolves. Paste that output verbatim as the `progress` block in the skeletons
below; the glyph table describes exactly what the helper emits. For the no-arg
project view, run it once per probe folder.

### Single probe (Console / `/haipipe-probe <probe>`)

```text
📊 <P.id>  ·  <slug>

  Claim: <one plain sentence: what this probe claims + scope/caveat>

  progress  Plan ✅ ─ Gather ▶️ ─ Read ⬜ ─ Judge ⬜ ─ Deposit ⬜   ⚠ drift
        ← here Gather: <one-clause why this is the frontier>
```

(the `progress` and `← here` lines are pasted verbatim from `ref/stage-strip.sh`)

### Project level (no-arg `/haipipe-probe`)

The no-arg dashboard is a GLANCE, not a report. One summary line, one status
line per probe, and a single drift flag. No drift tables, no arm tables, no
evidence detail — those belong behind explicit `/haipipe-probe status <probe>`
or `/haipipe-probe gather <probe>`.

```text
📊 haipipe-probe  ·  <PROJECT>  ·  <DATE>  ·  <N> probes (<M> active)

  P.T0605  discretion-gradient     Gather ▶️  (2/6 refs resolved)
  P.D0622  trait-behavior-matrix   Read ▶️
  P.T0622  agreeableness-opioid-lbp  Judge ▶️
  P.T0623a per-arm-theory-fit      Deposit ✅

  ⚠ drift: P.T0605 (5 broken refs)

  Un-probed: 2 GAP (claim-bearing) → /haipipe-probe file ...
```

Each probe line is: `<ref>  <slug>  <frontier step> <frontier glyph>  (<brief why>)`
— derived from `ref/stage-strip.sh`. No claim text on the project view (save
that for the single-probe console). Drift is one aggregate line, not a per-arm
table. Un-probed evidence is a count, not a list.

Glyphs (derive-from-disk; first non-✅ rung = frontier):

```text
✅ done       the step's disk predicate passes
▶️ frontier   the first failing step; annotate "← here"
⬜ todo       not reached
⚠ drift      stored verdict claims progress but the disk predicate fails
```

Worked example (P.0605, derived from disk):

```text
📊 P.0605  ·  discretion-gradient

  Claim: Agreeableness raises opioid prescribing intensity, attenuating as clinical
         discretion falls; strong in low-back-pain (high discretion), near-zero in
         cancer (guideline-locked). (pending real data)

  progress  Plan ✅ ─ Gather ▶️ ─ Read ⬜ ─ Judge ⬜ ─ Deposit ⬜   ⚠ drift
        ← here Gather: 5/6 linked refs unresolved: R01_Regression_TraitOpioid
```

This is the literal output of `ref/stage-strip.sh probes/0605_discretion-gradient`.
Frontier = Gather: Plan is ✅ (probe.yaml has a claim), but 5 of the 6 arm-table
paths do not resolve on disk (the task folder was renamed
`R01_Regression_TraitOpioid` → `R01_Reg_TraitOpioid`), so Gather fails first.
⚠ drift because those linked refs are gone while the stored verdict still claims
mechanics=confirmed.

Keep the render concise. The dashboard is an orientation panel, not a report.
Detailed evidence belongs in `evidence.md`; claim verdicts belong in `verdict.md`.

## Writes

No-arg dashboard may write generated project-level orientation:

```text
probes/_index.md
```

Opening a specific console writes:

```text
.probe-console.yaml
probes/<probe>/status.md
```

Generated files should be overwritten from disk state. Do not treat them as
hand-authored source of truth.
