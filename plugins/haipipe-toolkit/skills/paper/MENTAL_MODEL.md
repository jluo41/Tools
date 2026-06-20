# paper — the mental model: two cycles, one gate

For the full paper journey from seed idea to submission, revision, and
presentation, including file-change maps and loopback diagnosis, see
`LIFECYCLE.md`.

A paper is not a linear pipeline. It is **two loops that alternate until they
converge**, with a review gate deciding which loop you re-enter:

```
        ┌──────────── reopen: argument is broken ───────────┐
        ▼                                                   │
   ① PLAN cycle  ──contract──▶  ② EDIT cycle  ──draft──▶  [ REVIEW gate ]
   decide what                  realize the tex               │
   the paper says               (write + edit)                │ local fix
        ▲                                                     │ (edit again)
        └──────────────── another edit pass ◀─────────────────┘
                                                              │ clean
                                                              ▼
                                              submit → rebuttal → present
                                                   (terminal phases)
```

Run **① then ② then the gate**, and repeat. Each loop is itself iterative
(several passes). You stop when the gate says "submit."

> **Status:** this is the conceptual frame over the **existing** folders — nothing
> is renamed yet. The natural end state is `2-plan → 1-plan` and `4-edit → 2-edit`
> with the others folded in; until then, read the current folders through the
> roles below.

---

## ① PLAN cycle — decide *what the paper says*

Settles the argument before prose exists (or when prose has drifted from it):
one-minute paper pitch, narrative/story, core claim, **claim → evidence map**,
section architecture, outline, and the **figure inventory** (which figures, one
claim each).

**Output: a design contract** the edit cycle realizes.

The lightest artifact in this cycle is `0-pitch/PAPER_PITCH.md`: the current
one-minute story for this concrete manuscript. It can start from intuition, but
later pitch shifts should cite the source in `0-pitch/PITCH_LOG.md` and archive
semantic old versions under `0-pitch/archive/`.

Skills today: `1-narrative/narrative-report`, `2-plan/{paper-architecture,
paper-bootstrap, paper-incubator, paper-plan, paper-structure-diagram}`, and
**figure *planning*** (`3-figure/figure-planner`).

Re-entered when the gate finds a **structural** problem ("this section has no
job", "the claim isn't supported", "wrong story") — not a wording problem.

---

## ② EDIT cycle — realize & refine *the tex*

The heart of the workflow, already built in `4-edit/` as **five stages**:

```
(1) format-check → (2) annotate → (3) human-AI feedback → (4) improve → (5) clean + diff
```

comment-first (Stage 2 changes no prose; the human replies `========>`; Stage 4
applies only accepted comments), fanned out across the update **topics**
(content · values · citations · consistency · format · typeset).

Two things fold in here:

- **Write = the cold-start of editing.** A section's first pass (empty → draft)
  is just the edit cycle with nothing to format yet. `4-write/{paper-write,
  paper-compile, scientific-writing}` is the bootstrap of ②, not a separate stage.
- **Figure *making*** (`3-figure/{paper-figure, figure-spec, paper-illustration}`)
  is an asset ② produces and the prose consumes. Revision skills
  (`5-revise/{haipipe-paper-edit-optimizer, haipipe-paper-edit-results-revision, haipipe-paper-edit-weaving}`)
  are simply more edit passes.

Re-entered when the gate finds a **local** problem (a number, a cite, a clumsy
paragraph) — fixable without rethinking the plan.

---

## The REVIEW gate — *which loop do we re-enter?*

`6-review` is **not a third cycle**; it is the gate between cycles. Its
zero-context, fresh-model audits (`haipipe-paper-edit-claim-audit`, `citation-audit`,
`haipipe-paper-edit-manual-review-values/-citations`, `haipipe-paper-edit-proof-checker`, `haipipe-paper-edit-submission-audit`)
exist precisely to catch what the editing author is blind to. Its verdict routes:

| Gate finding | Route to |
|--------------|----------|
| Wording / number / cite / local prose | **② edit** again |
| Argument, evidence, or structure is wrong | **① plan** again |
| Clean | **submit** |

The edit cycle's own topic checks (②'s lightweight values/citations passes) are
the *fix-as-you-write* layer; the gate is the *adversarial pre-submission* layer.
Both exist on purpose.

---

## Figures live in both cycles (split)

- **Planning** a figure — what it claims, panel roles, main-vs-SI — is ① plan
  (`haipipe-paper-structure-figure-planner`).
- **Making** the figure — plotting, diagram, illustration — is ② edit
  (`haipipe-paper-structure-figure`, `haipipe-paper-structure-figure-spec`, `haipipe-paper-structure-illustration`).

Figures are the one shared asset that touches both loops; keep the *decision* in
plan and the *production* in edit.

---

## Terminal phases — outside the loop

After the gate says submit, the loop is over. What follows is lifecycle, not
authoring:

- **rebuttal** — `0-workflow/7-respond/{paper-rebuttal, rebuttal-response}`,
  `haipipe-paper-rebuttal` (a reviewer reply can, of course, kick off a fresh
  plan⇄edit loop for the revision).
- **present** — `0-workflow/8-present/{paper-poster, paper-slides}`.

The venue umbrellas (`haipipe-paper-conference/-journal/-is`) orchestrate the
whole arc: plan → edit → gate → submit → rebuttal → present.

---

## Iteration semantics (when to stop, which loop to reopen)

- **Within a cycle:** repeat passes until that cycle's own "done" holds — plan
  done = a stable contract; edit done = every section's topic cells applied
  (`4-edit/_shared/edit-cycle.md` grid).
- **Across cycles:** the gate decides. Local → edit; structural → plan; clean →
  submit. A `haipipe-paper-edit-diffpdf` at the end of each edit cycle shows co-authors what
  that cycle changed.
- **Convergence:** stop when a full edit cycle + gate produces no structural
  finding and only cosmetic edits — that's "ready to submit."

---

## Mapping: current folder → role in the model

| Folder today | Role | Cycle |
|--------------|------|-------|
| `0-pitch` | one-minute story + pitch provenance | ① plan |
| `1-narrative` | story / claim contract | ① plan |
| `2-plan` | architecture, outline, structure-diagram | ① plan |
| `3-figure` (figure-planner) | figure inventory | ① plan |
| `3-figure` (figure/spec/illustration) | figure production | ② edit |
| `4-write` | cold-start drafting | ② edit |
| `4-edit` | the 5-stage edit cycle | ② edit |
| `5-revise` | further edit passes | ② edit |
| `6-review` | the gate (route edit-again / plan-again / submit) | between |
| `0-workflow/7-respond` | rebuttal | terminal |
| `0-workflow/8-present` | poster / slides | terminal |
| `0-workflow/haipipe-paper-*` | venue orchestration of the whole arc | over all |
