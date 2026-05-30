haipipe-toolkit — Mental Model
================================

How to think about the 4 layers (C / D / E / G) and how sessions
("applications") drive them. Read this before USAGE.md if anything in
the toolkit feels arbitrary — the rules in USAGE.md are consequences
of the model laid out here.


TL;DR — 4 layers, 4 roles
==========================

```
C_task         WORK       one run.sh + one results/<RUN>/
                          produces: D + I material (observations + patterns)
                          "看到了什么, 像什么样子"

D_probe        PROBE      arms[] + statistical contract + verdict
              (folder:    implemented today as D_experiment / experiments/)
                          produces: K + W material (claims + recommendations)
                          "朝哪个方向试探, 我们 claim 什么, 该怎么办"

E_insight      ARCHIVE    D/I/K/W markdown cards under insights/
                          does NOT produce — only files + cross-refs
                          "项目的永久 KB"

G_application  SESSIONS   one user intent → one closed case file
                          4 kinds share one session skeleton:
                            ask      research question (KB-writing)
                            message  patient / clinician (KB-readonly)
                            ui       designer / dev (KB-readonly)
                            report   stakeholder (KB-readonly)
                          "一次案件, 评估 + 编排 + 产物"
```

One assignment to remember:

```
D + I  ←  comes from  C_task        (observational / descriptive)
K + W  ←  comes from  D_probe       (normative / prescriptive)
          folder/skill compatibility name: D_experiment
E_insight     = archivist           (files cards into permanent KB)
G_application = case worker         (one session per intent; 4 kinds;
                                     ask is the only kind that can write KB)
```


The 4 layers, in detail
========================

C_task — the WORK layer
------------------------

```
unit:        one run.sh + one results/<RUN>/ directory
verb:        EXECUTE, OBSERVE, DISPLAY
asks:        "this run, did it produce its expected artifact?"
artifacts:   *.py, configs/<RUN>.yaml, runs/<RUN>.sh,
             results/<RUN>/runtime.yaml, results/<RUN>/metrics.json,
             results/<RUN>/<figures>.png
location:    examples/<project>/tasks/<G##_group>/<##_task>/

DIKW lens:   D (data observation) + I (information pattern)
             — observational / descriptive only.
             A task can carry both lenses at once: e.g. a regression
             task produces D ("the distribution") AND I ("the
             correlation pattern") AND maybe a candidate K hint.
             But K and W never *commit* here; they need a probe.

task-types:  data / algo / training / eval / display / individual / agent
             (see C_task/haipipe-task SKILL.md)
```

A task is **atomic on the compute side**: one bash invocation, one
output directory. Multiple tasks can be chained, but each is its own
unit of work.

A task CAN produce evidence for several DIKW cards at once. A
well-designed display or regression task often closes 3+ D/I cards in
one shot. That is the point — DIKW is a *lens*, not a *phase*.


D_probe — the PROBE / CLAIM layer
----------------------------------

```
unit:        one experiment.yaml (one claim-directed probe thread)
verb:        PROBE, COMPARE, CLAIM, RECOMMEND
asks:        "across these arms, with N seeds, does the hypothesis hold?
              what should we do next?"
artifacts:   experiment.yaml (hypothesis + arms[] + result + claim + caveats),
             review.md, CLAIMS_FROM_RESULTS.md, logs/<DATE>.md
location:    examples/<project>/experiments/<NN_slug>/

DIKW lens:   K (validated belief) + W (per-experiment recommendation)
             — normative / prescriptive.
             K appears in experiment.yaml.claim after result aggregation.
             W appears as the "next step" implied by claim + caveats
             (e.g. "param-matched re-test", "drop arm X").
```

D_probe is the conceptual name. `D_experiment`, `experiments/`, and
`/haipipe-experiment` remain the compatibility names in the current
folder and command layout.

A claim CANNOT exist without an experiment.
A pattern observed in a single task is at most I; promoting it to K
requires a controlled comparison (arms × seeds × statistical test).

This is the most important boundary in the toolkit:

```
   D + I       no comparison needed     → C_task is sufficient
   K + W       requires controlled      → D_probe mandatory
               comparison                  (no shortcut from I to K)
```

A single probe can produce multiple K (a main claim + secondary
claims observed in the same run) and multiple W (different "next
steps" implied by different parts of the claim).


E_insight — the ARCHIVE layer
------------------------------

```
unit:        one D/I/K/W markdown card under insights/
verb:        FILE, CROSS-REFERENCE, INDEX
asks:        "what does the project KNOW, and where is each piece?"
artifacts:   insights/INDEX.md, insights/{D,I,K,W}_*/{D,I,K,W}##_<slug>.md
location:    examples/<project>/insights/

DIKW lens:   all 4 — but as labels on cards that were *produced
             elsewhere*. E does not compute, observe, or claim. It only
             archives material that C_task and D_probe have
             already produced, and maintains the cross-reference graph.
```

E_insight is the **librarian**. It writes no original content.

Folder name aligned to DIKW letters:

```
insights/D_data/            D## cards   ← filed from C_task results/
insights/I_information/     I## cards   ← filed from C_task results/
insights/K_knowledge/       K## cards   ← filed from D_probe claims
insights/W_wisdom/          W## cards   ← filed from D_probe recs
                                          AND from strategic synthesis
                                          (multiple K → 1 strategic W)
```

W has two flavors in the archive — same folder, distinguished by
`sources:`

```
per-experiment W:  sources: [E07]                 (1 experiment)
strategic     W:  sources: [K01, K03, K05]       (cross-experiment)
```

The K-commit "harsh" gate (must list all counter-evidence) is NOT in
E_insight — it lives in `D_experiment/-review` where the claim is
made. By the time material reaches E_insight, it has already been
vetted upstream. E_insight is a flat file-write.


G_application — the SESSION layer
----------------------------------

```
unit:        one session = one user intent = one case file
verb:        DESIGN, DISPATCH, EVALUATE
asks:        "given the KB so far, can we produce this artifact?
              if not, what to do?"
artifacts:   SESSION_STATE.json, plans/plan-vN.yaml, gates/##-G-<phase>.md,
             invocations.log, the kind's output artifact
location:    examples/<project>/applications/<kind>/<...>/

DIKW lens:   none. G does not produce DIKW content directly. It
             evaluates whether enough D+I+K+W exists in the KB to
             produce the artifact, and orchestrates more work
             (tasks / experiments / new KB cards) if not.
```

G_application is the **case worker**. There are 4 kinds of case file,
all sharing one session skeleton:

```
kind        artifact                                writes KB?    can trigger?
─────────────────────────────────────────────────────────────────────────────
ask         applications/ask/<NN_slug>/report.md    YES           D_experiment + C_task
                                                                  + haipipe-insight-{D,I,K,W}
message     applications/messages/<...>.md           no            (chains to ask if gap)
ui          applications/ui/<slug>/                  no            (chains to ask if gap)
report      applications/reports/<...>.md            no            (chains to ask if gap)
```

`ask` is the only kind authorized to mutate the KB or trigger
D_experiment / C_task. The external kinds delegate KB work to `ask`
and resume their own draft once `ask` returns.

A session does NOT accumulate content into the KB by itself (only the
`ask` kind does, via insight-{D,I,K,W} files). When a session ends,
the permanent residue lives in `tasks/`, `experiments/`, `insights/`.
The applications/<kind>/<...>/ folder itself is a closed case file —
the journey, not the destination.

The session skeleton (shared by all 4 kinds):

```
haipipe-application                orchestrator (verb-routes to kind)
haipipe-application-<kind>         kind specialist (per-phase work)
haipipe-application-plan           writes plan-v{N}.yaml
haipipe-application-gate           phase gate (persona + attendance)
haipipe-application-context        per-task context loader
ref/session-state-schema.md        SESSION_STATE.json fields
ref/gate-persona.md                4 preset reviewer voices
ref/attendance-modes.md            attended / timed / unattended
```


The DIKW lens assignment — why this works
==========================================

Three old confusions, resolved:

```
Old confusion 1:  "where does K come from?"
                  was: vaguely "synthesize across D entries"
                  now: K is born when an experiment validates a claim;
                       no experiment, no K.

Old confusion 2:  "D vs I — what's the cut?"
                  was: blurry; both observational
                  now: D = one task's own observation
                       I = pattern visible across tasks (still C_task
                           work, but cited from multiple D cards)

Old confusion 3:  "what does E_insight actually do?"
                  was: synthesize / re-compute
                  now: file. The compute already happened upstream.
                       E maintains cards, INDEX, cross-refs only.
```


The plan-vN.yaml — central artifact of a session
=================================================

A session's plan does NOT enumerate phases (D / I / K / W). It
enumerates two related batches, with a DAG between them:

```yaml
plan_version: 2
question: "Does FiLM hold on test-od?"

# Batch A — C_task work to gather D + I material
task_batch:
  - id: T1
    skill: /haipipe-task eval
    type: regression
    yields: [D01, I01]
    notes: "fit val/test-id/test-od; D = per-split stats, I = pattern across splits"
  - id: T2
    skill: /haipipe-task display
    type: display
    yields: [I02]
  - id: T3
    skill: /haipipe-task individual
    type: individual-query
    yields: [D02]

# Batch B — D_experiment work to produce K + W
experiment_batch:
  - id: E07
    skill: /haipipe-experiment design
    arms: [film_pm, baseline_pm]
    yields: [K01, W01]
    needs: [D01, I02]          # must finish before E07 starts
  - id: E08
    skill: /haipipe-experiment design
    arms: [film_subset_od, baseline_subset_od]
    yields: [K02]
    needs: [D02]

# Archive — what cards E_insight will file
insight_yield:
  D01: {layer: D, sources: [T1]}
  D02: {layer: D, sources: [T3]}
  I01: {layer: I, sources: [T1]}
  I02: {layer: I, sources: [T2], refs: [D01]}
  K01: {layer: K, sources: [E07], refs: [D01, I02]}
  K02: {layer: K, sources: [E08], refs: [D02]}
  W01: {layer: W, sources: [E07], refs: [K01]}

# DAG — what blocks what
dag:
  - T1, T2, T3 in parallel
  - E07 needs D01 + I02
  - E08 needs D02
  - All yields → G-report
```

Key properties:

- **N tasks ↔ M D/I cards** (many-to-many, not 1:1)
- **N tasks can collectively close 1 D card** (cross-task evidence)
- **1 task can close multiple D+I cards at once** (lens multiplicity)
- **K + W cards always have an experiment id in `sources`**
- **Strategic W cards have multiple K ids in `sources`**


Phases of one session — per kind
==================================

Every kind specialist runs phases through the same machinery
(plan / gate / context + SESSION_STATE.json), but the phase list
differs by kind. The 2-step shape per phase is uniform: `task` then
`gate`.

ask kind — research session (4 phases):

```
   ┌──────────────────────────────────────────────────────────┐
   │   Phase 1   design       /haipipe-application-plan       │
   │                          writes plan-v{N}.yaml           │
   │                          [G-design gate, SOFT]           │
   │                                                          │
   │   Phase 2   observe      dispatch task_batch:            │
   │                            /haipipe-task <type>          │
   │                          → C_task workers produce D + I  │
   │                          [G-observe gate, SOFT]          │
   │                          (skip if KB already has all D+I)│
   │                                                          │
   │   Phase 3   claim        dispatch experiment_batch:      │
   │                            /haipipe-experiment design    │
   │                            /haipipe-experiment bridge    │
   │                            /haipipe-experiment result    │
   │                          → D_experiment workers          │
   │                            produce K + W                 │
   │                          [G-claim gate; SOFT on G side,  │
   │                           HARSH gates inside D_experiment]│
   │                          (skip if no experiment needed)  │
   │                                                          │
   │   Phase 4   report       /haipipe-application-plan       │
   │                          + /haipipe-insight-{D,I,K,W}    │
   │                            files all cards into KB       │
   │                          writes session report.md        │
   │                          [G-report gate, HARSH]          │
   └──────────────────────────────────────────────────────────┘
                Every gate's `revise` outcome → back to Phase 1
                Plan is the SOLE router for non-forward motion
```

message / ui / report kinds — external creation (6 phases):

```
   Phase init   parse intent + audience
   Phase load   load K/W from insights/ (filter by tag)
                  [G-load SOFT — KB material sufficient?]
   Phase gap    if gap → chain /haipipe-application ask "<sub-Q>"
                  (ask runs its own 4-phase session inline)
                  resume external kind after ask returns
   Phase draft  produce artifact (kind-specific template)
   Phase review self-review against audience-requirements.md
                  [G-review SOFT]
   Phase write  atomic write to applications/<kind>/<...>.md
                  [G-write HARSH — final artifact correct?]
```

No phase=D / phase=I / phase=K / phase=W in either shape. DIKW is a
card-labeling scheme, not an execution stage.


Gate harshness — HARSH vs SOFT
===============================

Two gate styles in the toolkit, separated by stake and reversibility:

```
                stake                 reversibility    style
─────────────────────────────────────────────────────────────────
C_task CODE_REVIEW    GPU compute waste    can re-run        HARSH
                                           (3 bypass options)
                                           
D_experiment review   claim entering       retract is        HARSH
  (structural)        project record       expensive         (no bypass)
                                           
D_experiment claim    public commitment    very expensive    HARSH
  (Codex verdict)                                            (no bypass)

E_insight card write  filing a vetted      n/a (already      no gate
                      claim                vetted upstream)
                                           
G_application (ask kind)
  G-design            time spent           cheap             SOFT
  G-observe           D+I gap              cheap             SOFT
  G-claim             K+W validity         medium            ⚠ inherits
                                                              D_experiment
                                                              HARSH gates
  G-report            wrong user answer    hard to undo      HARSH

G_application (message / ui / report kinds)
  G-load              KB-material gap      cheap             SOFT
  G-review            audience misfit      cheap             SOFT
  G-write             external artifact    public-facing     HARSH
```

**HARSH gates** have no persona / attendance / MAX_REVISIONS toggle.
They block until met. They protect the project's permanent record.

**SOFT gates** have:
- 3-outcome vocabulary: `approve` / `revise [feedback]` / `done`
- 4-preset persona: `strict` / `balanced` / `creative` / `lenient`
  + `strictness(0-10)` + `ambition(0-10)`
- 3-mode attendance: `null` (attended) / `N` (timed) / `0` (unattended)
- `MAX_REVISIONS=3` force-approve audit
- Plan as sole router (all revise → plan)

SOFT gates protect *exploration efficiency*, not permanent record.
That is why they have knobs — explorations should adapt.

The G-claim gate is special: from G_application's side it looks SOFT
(it can `revise` and re-plan), but the work it gates (the experiment
itself) is governed by D_experiment's HARSH review gates upstream.
G-claim does not duplicate those gates; it only checks "did we get
the K+W we wanted from this experiment batch?"


One full session, lifecycle walk-through (ask kind)
=====================================================

This trace is the `ask` kind. The `message` / `ui` / `report` kinds
follow the 6-phase external-creation shape (init/load/[gap]/draft/
review/write); their lifecycle is shorter and KB-readonly except for
the optional inline-ask chain at gap-phase.

```
[t=0]  user: "Does FiLM beat baseline on test-od?"

[t=1]  /haipipe-application ask "..."
       → creates applications/ask/03_film_test_od_generalization/
       → SESSION_STATE.json initialized (kind: ask)

[t=2]  Phase 1 — design
       /haipipe-application-plan
       → scans insights/INDEX.md  (does KB already answer?)
       → KB has D01, I01 already — but no K with test-od scope
       → writes plan-v1.yaml:
            task_batch:     [T1 (individual-query OD samples)]
            experiment_batch: [E12 (FiLM vs baseline, OD eval)]
            insight_yield:  [D02, K03, W02]
       [G-design SOFT] → approve

[t=3]  Phase 2 — observe
       dispatch T1:
         /haipipe-task individual individual-query --od-samples ...
         → tasks/E01_individual_query/02_od_filmcase/results/...
       → returns D02 material
       [G-observe SOFT] → approve

[t=4]  Phase 3 — claim
       dispatch E12:
         /haipipe-experiment design new E12
         /haipipe-experiment bridge E12
           → scaffolds 6 task-folders (3 seeds × 2 arms)
           → invokes Run Script Reviewer (HARSH gate, C_task side)
           → bash runs/<RUN>.sh × 6
         /haipipe-experiment result aggregate E12
           → fills result block in experiment.yaml
         /haipipe-experiment review E12
           → HARSH structural QA + Codex verdict
       → returns K03 + W02 material
       [G-claim SOFT-on-G-side] → approve

[t=5]  Phase 4 — report
       /haipipe-insight-{data,information,knowledge,wisdom}
         each files the cards:
         insights/D_data/D02_*.md
         insights/K_knowledge/K03_*.md
         insights/W_wisdom/W02_*.md
         INDEX.md rebuilt
       /haipipe-application-plan compose final report
         → writes applications/ask/03_*/report.md
         → cites D02 + K03 + W02 with full provenance
       [G-report HARSH] → confirms report.md actually answers Q
       → SESSION_STATE.status = complete

[t=6]  return to user:
       answer + applications/ask/03_*/report.md
       residue in KB: D02 / K03 / W02 (cited next time)
```


Boundary FAQ
=============

**Q: I have a notebook that plots 5 training runs into one figure.
    Where does it go?**

A: tasks/ — specifically a `display`-type task. The figure is the
   product of an observation task. It yields one or more I cards.
   The notebook lives at `tasks/.../<task>/notebooks/<RUN>.ipynb`,
   the figure at `tasks/.../<task>/results/<RUN>/<name>.png`. The
   I card cites it.

**Q: A regression task produced what looks like a clean causal effect.
    Can I write a K card straight from it?**

A: No. K requires a controlled comparison — arms × seeds × test. A
   regression is observational; it can produce strong I, but not K.
   Promote by scaffolding an experiment that arm-matches the regressor.

**Q: One C_task run yields evidence for 3 D cards. How is that
    recorded in the plan?**

A: `task_batch[i].yields: [D01, D02, D03]`. The yields list is the
   contract — that many cards must be filed at Phase 4 or G-observe
   refuses to approve.

**Q: One D card needs evidence from 3 tasks. How?**

A: `insight_yield.D01.sources: [T1, T2, T5]`. The card cites all
   three task results. E_insight filing reads from each task's
   results/.

**Q: Can a session skip Phase 3 (claim)?**

A: Yes. If the KB already has all needed K+W, or if the question
   only needs D+I (e.g. "describe the data"), the plan's
   `experiment_batch` is empty and Phase 3 is a no-op.

**Q: Can a session skip Phase 2 (observe)?**

A: Yes. If the experiment_batch only depends on existing D/I in the
   KB, Phase 2 is a no-op and Phase 3 runs directly.

**Q: Multiple sessions cite the same K card. Does the card get
    duplicated?**

A: No. Cards are atomic. Sessions cite by ID. The card's `ref_by:`
   list grows.

**Q: A session's K card later turns out wrong (new experiment
    refutes it). What happens?**

A: The refuting experiment yields a new K with `supersedes: [K-old]`.
   K-old's `status:` changes to `superseded` but the file remains
   for history. Both visible in K_knowledge/INDEX.md.

**Q: A W card was filed last month. Is it still actionable?**

A: Maybe. W cards decay. Check `status:` (active / stale). The
   application doing the re-check can mark a W stale if its trigger
   condition no longer holds.

**Q: Where do raw thinking notes / daily logs go?**

A: applications/ask/<NN_slug>/logs/<YYYY-MM-DD>.md (append-only,
   captain's-log style). Not in tasks/, not in experiments/.

**Q: What's the difference between `/haipipe-application ask` and
    just running `/haipipe-task` + `/haipipe-experiment` directly?**

A: The ask kind gives you the session machinery: SESSION_STATE.json
   for resume, plan-vN.yaml for design intent, gates for phase
   review, persona/attendance knobs. Running raw skills works too,
   but you lose the per-session log + the gate review at each step.

**Q: Can I make a patient message without a session?**

A: No. All G_application work goes through the session skeleton —
   even short jobs get a SESSION_STATE.json. The skeleton is what
   gives you resume + audit + revise.

**Q: I want to ask a question that the message kind chains to
    automatically. How do I know it'll find a good ask sub-Q?**

A: At Phase load, the external kind reads K/W on the relevant tags.
   If gap found, it composes a sub-Q (audience-aware) and pipes
   verbatim to `/haipipe-application ask`. You can override the
   composed sub-Q at the G-load gate via reply B.

**Q: Two sessions want to run the same experiment. Wasted compute?**

A: The second session's plan-v1.yaml.experiment_batch will scan
   existing experiments/ first. If E07 with the desired arms exists
   and is `confirmed`, the second session reuses it (no re-run).


One-line rules of thumb
========================

```
new D / I material  → C_task        (a task run produces it)
new K / W material  → D_experiment  (an experiment claims it)
file a vetted card  → E_insight     (just write the markdown)
any session-style intent → G_application (4 kinds: ask / message / ui / report)

no controlled comparison         → no K, only I
no experiment                    → no K, only I
no I / no K available            → /haipipe-application ask  (only kind that
                                    can schedule tasks / experiments)
strategic synthesis across K     → still W, sources = [K01, K03, …]
external artifact needed         → /haipipe-application {message|ui|report}
                                    (KB-readonly; chains to ask if gap)
session ends                     → residue in tasks/+experiments/+insights/
                                    session folder is the case file
```


Where to go from here
======================

```
Toolkit-wide usage flows:        USAGE.md
C_task design + worktree:        skills/C_task/DESIGN.md
D_experiment ↔ C_task boundary:  skills/D_experiment/MENTAL_MODEL.md
E_insight schema:                skills/E_insight/ref/insight-md-schema.md
G_application umbrella:          skills/G_application/haipipe-application/SKILL.md
G_application session state:     skills/G_application/haipipe-application/ref/session-state-schema.md
G_application gate persona:      skills/G_application/haipipe-application/ref/gate-persona.md
G_application attendance modes:  skills/G_application/haipipe-application/ref/attendance-modes.md
Top-level skills inventory:      README.md
```
