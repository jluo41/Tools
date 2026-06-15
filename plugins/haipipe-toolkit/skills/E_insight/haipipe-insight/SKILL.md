---
name: haipipe-insight
description: "Insight base orchestrator (the E_insight umbrella). The project's permanent knowledge base under examples/<project>/insights/ (D_data / I_information / K_knowledge / W_wisdom). Three jobs: (1) route filing requests to the right DIKW specialist, (2) post-file accumulation check — suggest promotion when enough cards accumulate, (3) dashboard — show KB state. Called by C_task Stage 5 (→D), D_probe convergence (→K), G_application Phase 4 (→any), or human directly. Owns I + W synthesis. Never executes code, never triggers probes."
argument-hint: "[verb] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "2.0.0"
  last_updated: "2026-06-11"
  summary: "Insight base orchestrator — file cards, check accumulation, suggest promotion."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
    - "2.0.0 (2026-06-11): DIKW producer partition; post-file accumulation check; 3-job design (route + check + dashboard); step-by-step protocol."
---

Skill: haipipe-insight (orchestrator)
======================================

The project's **permanent knowledge base** — accumulates observations from tasks, beliefs from probes, and synthesizes patterns and recommendations across them.

```
C_task       EXECUTES runs          → files 🟦 D cards (Stage 5)
D_probe      TESTS hypotheses       → files 🟨 K cards (convergence)
E_insight    ACCUMULATES + PROMOTES  ← THIS SKILL FAMILY
F_paper      PUBLISHES from K + W
```

Unlike C_task (which transforms ONE folder through linear stages), E_insight is an **accumulation + promotion funnel**: cards arrive one at a time, build up, and when enough accumulate at one level the next level becomes fileable.

```
🟦 D cards arrive (from tasks)     → accumulate → when ≥ 2 share a pattern → 🟩 I fileable
🟨 K cards arrive (from probes)    → accumulate → when K is actionable     → 🟧 W fileable
```


Where the insight base lives (project-level)
---------------------------------------------

```
examples/Proj-X/
├── tasks/                                  (C_task — execution)
├── probes/                            (D_probe — research)
└── insights/                               ← E_insight writes here
    ├── INDEX.md                            (auto: all entries + status)
    ├── sessions/                           (lightweight Q&A log)
    │   └── <YYYY-MM-DD>_<slug>.md
    │
    ├── D_data/                     "what we observed"        (one task/run)
    │   ├── D01_<slug>.md
    │   └── ...
    │
    ├── I_information/                         "what patterns emerged"     (cross-task)
    │   ├── I01_<slug>.md
    │   └── ...
    │
    ├── K_knowledge/                        "what we now believe"       (one probe claim)
    │   ├── K01_<slug>.md
    │   └── ...
    │
    └── W_wisdom/                           "what we should do next"    (cross-probe)
        ├── W01_<slug>.md
        └── ...
```

**Hard rule:** NO code, no Python, no notebooks, no plots inside insights/. That work belongs to C_task (code) or D_probe (claim verdicts). E_insight only synthesizes markdown.


Who produces what (the DIKW producer partition)
------------------------------------------------

Each DIKW level is partitioned by scope. Each scope has one natural producer. No layer files cards above its scope.

```
DIKW level     Producer           Trigger                          Scope
─────────────  ─────────────────  ───────────────────────────────  ──────────────
🟦 D data      C_task Stage 5     task lifecycle completes         one task/run
🟩 I info      E_insight          enough D cards accumulate        cross-task pattern
🟨 K knowledge D_probe loop       probe converges (confirmed)      one probe claim
🟧 W wisdom    E_insight / G_app  enough K cards accumulate        cross-probe action
```

- A task does not produce K (no hypothesis testing — that's a probe).
- A probe does not produce I (no cross-probe view — that's synthesis).
- The atomic layers (D, K) are filed automatically by their producers.
- The synthesis layers (I, W) require enough accumulation or human judgment.

---

Three Jobs
-----------

This orchestrator has three jobs:

```
Job 1: ROUTE    dispatch filing requests to the right DIKW specialist
Job 2: CHECK    after every D or K card is filed, check accumulation thresholds
Job 3: DASHBOARD  show the KB state when called with no args
```

**Job 1 (Route)** is the verb dispatch that already exists — same as C_task routing by type.

**Job 2 (Check)** is what's new — the E_insight equivalent of C_task's stage transitions. But instead of "advance to the next stage," it's "suggest promotion to the next DIKW level when enough cards accumulate." This fires automatically after every successful file operation.

**Job 3 (Dashboard)** is the explore skill — shows what the KB has, what's promotable, what's missing.

---

Commands
--------

Two styles: **path-based** (give it a source path, auto-detect what to file) or **verb-based** (explicit DIKW level).

```
# Path-based (auto-detect source type → DIKW level)
/haipipe-insight <task-folder-path>              auto: task → 🟦 D card
/haipipe-insight <probe-folder-path>             auto: probe → 🟨 K card (+ optional 🟧 W)
/haipipe-insight <task-group-path>               auto: iterate each child task → 🟦 D cards

# Verb-based (explicit DIKW level)
/haipipe-insight data <source>                   D-level: file observation card + check accumulation
/haipipe-insight information [--scope <D*>]      I-level: synthesize pattern from ≥2 D cards
/haipipe-insight knowledge <probe-ref>           K-level: file belief from confirmed probe + check for W
/haipipe-insight wisdom [--scope <K*>]           W-level: synthesize recommendation from K cards

# Dashboard
/haipipe-insight                                 dashboard (KB state overview)
/haipipe-insight explore [project-path]          coverage scan + promotion suggestions

# Natural language
/haipipe-insight "<natural language>"            infer, dispatch

(For question-driven sessions: → /haipipe-application ask)
(For session machinery (plan / gate / context): → G_application/)
```

Path-based is the recommended entry — you don't need to remember the verb. Just hand it the source folder and it does the right thing. Same pattern as `/haipipe-task <path>` auto-detecting task type.

---

Specialists
-----------

```
haipipe-insight-data            D-LEVEL:  file observation card → D*.md  (called by C_task Stage 5)
haipipe-insight-information     I-LEVEL:  synthesize cross-D pattern → I*.md  (owned by E_insight)
haipipe-insight-knowledge       K-LEVEL:  file belief from probe → K*.md  (called by D_probe convergence)
haipipe-insight-wisdom          W-LEVEL:  synthesize recommendation → W*.md  (owned by E_insight)
haipipe-insight-explore         READ:     coverage scan + promotion readiness

(Session machinery — plan / gate / context — and the question-driven
 ask workflow live in G_application. E_insight only files cards into
 the permanent KB; it does NOT run sessions or hold per-question state.)
```

---

Agents
------

Two agent families in `E_insight/agents/`, per DIKW type:

```
E_insight/agents/
  creators/                                  the headless, agent-callable path
    card-creator-data-agent.md               🟦 called by C_task Stage 5
    card-creator-information-agent.md        🟩 called by G_application or human
    card-creator-knowledge-agent.md          🟨 called by D_probe convergence
    card-creator-wisdom-agent.md             🟧 called by G_application or human
  reviewers/                                 per-type quality gate
    card-reviewer-data-agent.md              🟦 accuracy + D boundary
    card-reviewer-information-agent.md       🟩 accuracy + I boundary
    card-reviewer-knowledge-agent.md         🟨 accuracy + K boundary + probe gate
    card-reviewer-wisdom-agent.md            🟧 accuracy + actionability
    index-integrity-auditor-agent.md         🔗 cross-layer: sources↔ref_by, INDEX↔files
```

Each creator calls the dual-mode haipipe-insight-<layer> skill headless. The creator is the fan-out-able subagent_type; the skill holds the filing logic. The reviewer enforces accuracy + style against `ref/dikw-boundaries.md`.

---

Function Verb Map
------------------

```
VERB-BASED:
data, observations, D-level, raw findings       -> haipipe-insight-data
information, patterns, I-level, trend           -> haipipe-insight-information
knowledge, K-level, validated belief, claim     -> haipipe-insight-knowledge
wisdom, W-level, recommendation, what next      -> haipipe-insight-wisdom
explore, coverage, scan, what can we synthesize -> haipipe-insight-explore

PATH-BASED (auto-detect source type → specialist):
tasks/<group>/<task>/  (has results/)           -> haipipe-insight-data       (→ D card)
tasks/<group>/         (has child task dirs)     -> iterate haipipe-insight-data (→ D cards)
probes/<MMDD>_<slug>/  (has probe.yaml)         -> haipipe-insight-knowledge  (→ K card + optional W)

(ask / question / session / plan / gate / context → /haipipe-application; NOT E_insight)
(report / stakeholder doc / message / ui         → /haipipe-application; NOT E_insight)
```

---

Step-by-Step Protocol
----------------------

Step 0: Read `ref/insight-md-schema.md` first. Every card MUST conform to this schema.

Step 1: Detect AUTO_MODE. Same contract as C_task: `--auto` in args, `CLAUDE_AUTO_HANDOFF=1`, or parent skill passed `--auto`. AUTO_MODE changes ASK steps into "accept best inference or return blocked."

Step 2: Resolve scope. Cascade (highest to lowest confidence):

  (1) EXPLICIT VERB — first positional is a verb (`data` / `information` / `knowledge` / `wisdom` / `explore`) → dispatch to that specialist.

  (2) PATH-BASED AUTO-DETECT — first positional is a filesystem path → detect source type via Step 2a.

  (3) QUESTION — first positional is a question ("?" / "does" / "is" / "why" opener) → redirect to `/haipipe-application ask`.

  (4) NO ARGS → Job 3 (dashboard): run explore to show KB state.

  (5) STILL AMBIGUOUS → AUTO: `status: blocked`. Interactive: ASK.


Step 2a: Source-type detection (path-based routing).

  Given a path, detect what kind of source it is and map to the right DIKW level:

  ```
  Source type    Path signal                                DIKW    Dispatch to
  ───────────    ──────────────────────────────────────     ─────   ───────────────────────
  task-folder    path under tasks/ + has results/<run>/     🟦 D    haipipe-insight-data
  task-group     path under tasks/ + has child task dirs    🟦 D    iterate: haipipe-insight-data per child
  probe-folder   path under probes/ + has probe.yaml       🟨 K    haipipe-insight-knowledge
  (future)       path under narrative/                      🟩🟧    (reserved for narrative synthesis)
  ```

  Detection rules:
    - `ls <path>/results/*/metrics.json` succeeds → task-folder → D card
    - `ls <path>/*/results/*/metrics.json` succeeds → task-group → iterate D cards
    - `ls <path>/probe.yaml` succeeds → probe-folder → K card
    - path contains `/probes/` → probe-folder → K card
    - path contains `/tasks/` and is a directory with child `{NN}_*/` dirs → task-group → iterate D cards
    - path contains `/tasks/` → task-folder → D card

  For task-group iteration: iterate each child task-folder, filing one D card per child that has results. Same pattern as `/haipipe-task <task-group-path>` iterating the lifecycle per child.

  For probe-folder: after filing K, optionally chain W if the K card is actionable (same as D_probe convergence behavior).


Step 3: Resolve project root.
  Infer from the source path (walk up to the `examples/Proj*/` ancestor) or from `--project` arg or from cwd.

Step 4: Dispatch to specialist:
  `Skill("haipipe-insight-<specialist>", args="<source-path> [--auto]")`

  For task-group iteration:
  ```
  for each child in <task-group-path>/{NN}_*/:
    if child has results/<run>/metrics.json:
      Skill("haipipe-insight-data", args="<child-path> [--auto]")
  ```

Step 5: Post-file accumulation check (Job 2). Runs ONLY after a successful file (status=ok):

  After filing a 🟦 D card:
    (1) Count D cards in insights/D_data/ that share the same task-group or tag theme.
    (2) If count >= 3 and no I card already covers this group:
        → emit in `next:`: suggest `/haipipe-insight information --scope D{NN}..D{MM}`
    (3) Update INDEX.md (add the new D card entry).

  After filing a 🟨 K card:
    (1) Check if this K card is actionable (has concrete scope + confidence > low).
    (2) If actionable and no W card already derives from this K:
        → emit in `next:`: suggest `/haipipe-insight wisdom --scope K{NN}`
    (3) Update INDEX.md (add the new K card entry).

  After filing a 🟩 I card:
    (1) Update INDEX.md.
    (2) Note: I does NOT auto-suggest K — K requires a probe (the I→K gate).

  After filing a 🟧 W card:
    (1) Update INDEX.md.

Step 6: Emit the structured tail:

```
status:    ok | blocked | failed
summary:   2-3 sentences (what was filed + accumulation check result)
artifacts: [paths created / updated]
next:      suggested next command (promotion suggestion if threshold met, else explore)
```

---

The Promotion Funnel
---------------------

E_insight's flow is a funnel, not a pipeline. Cards arrive at different rates from different producers. Promotion happens when enough cards accumulate at one level:

```
        C_task Stage 5                D_probe convergence
              │                              │
              ▼                              ▼
        ┌───────────┐                 ┌───────────┐
        │ 🟦 D_data │                 │ 🟨 K_know │
        └─────┬─────┘                 └─────┬─────┘
              │ accumulate                   │ accumulate
              ▼                              ▼
        count >= 2?                    actionable?
        same pattern?                  no W yet?
              │ yes                          │ yes
              ▼                              ▼
        ┌───────────┐                 ┌───────────┐
        │ 🟩 I_info │                 │ 🟧 W_wisd │
        └───────────┘                 └───────────┘
              │
              │ ★ I→K gate: REQUIRES a probe
              │ (I alone NEVER promotes to K)
              ▼
        only via D_probe
```

Key constraint: the I→K gate requires a controlled comparison (a probe). No amount of I-level patterns can be promoted to K without a probe confirming them. This is what makes K cards load-bearing for paper claims and W recommendations.

---

Boundary with D_probe and C_task
---------------------------------------

**Who produces what (the DIKW producer partition):**

```
🟦 D data      ← C_task Stage 5 files per-task observations (Skill("haipipe-insight-data"))
🟩 I info      ← E_insight synthesizes cross-task patterns (when ≥2 D cards accumulate)
🟨 K knowledge ← D_probe convergence files per-probe beliefs (card-creator-knowledge-agent)
🟧 W wisdom    ← E_insight synthesizes cross-probe actions (when K cards accumulate)
```

Each DIKW level is partitioned by scope. No layer files cards above its scope: a task does not produce K (no hypothesis testing), a probe does not produce I (no cross-probe view).

**Dependencies:**

```
E_insight is CALLED BY C_task (Stage 5 → D) and D_probe (convergence → K)
E_insight OWNS synthesis: I (cross-D patterns) and W (cross-K actions)
E_insight NEVER triggers D_probe (that's G_application's ask kind)
E_insight NEVER writes to tasks/ or probes/ directly
E_insight ONLY writes to insights/
D_probe NEVER reads from insights/
```

---

Relation to other top-level skills
-----------------------------------

```
A_discover    feeds ideas → seeded questions handled in G_application ask
B_project     project umbrella → owns the examples/Proj-X/ shape
C_task        CALLS E_insight: Stage 5 → Skill("haipipe-insight-data") → 🟦 D card
              (per-task observations, insight-worthy types only)
D_probe       CALLS E_insight: convergence → card-creator-knowledge-agent → 🟨 K card
              (per-probe beliefs from confirmed/refuted claims)
F_paper       READS K + W entries → academic publication
G_application CALLS E_insight: Phase 4 → files D/I/K/W cards
              drives sessions (ask / message / ui / report) that read K/W

E_insight is the project's PERMANENT KB. It does NOT run sessions or
own per-question state. It files cards and synthesizes cross-cutting
patterns (I) and recommendations (W). Source of "what does this project KNOW".
```

---

Files owned by this umbrella
-----------------------------

```
SKILL.md                              (this file)
ref/insight-md-schema.md              canonical entry schema (D/I/K/W)
ref/insight-context-loading.md        loading strategy for callers
ref/index-templates.md                INDEX.md / K-INDEX / W-INDEX templates
ref/dikw-boundaries.md                per-layer boundary + worked examples (in ../ref/)
ref/invocation-modes.md               dual-mode contract (in ../ref/)
```

---

Schema authority
-----------------

Every insight entry under `examples/<project>/insights/` MUST conform to `ref/insight-md-schema.md`. The 4 layer skills (data / information / knowledge / wisdom) all reference this single file as their entry schema source.

When loading insight context for a query, follow `ref/insight-context-loading.md` — layer-cascading + tag-filtering + INDEX-as-gateway.

---

Invocation examples
--------------------

```
# Path-based: give it a task folder → auto-detect → D card
/haipipe-insight examples/ProjA/tasks/B03_band4/01_eval_h24/

# Path-based: give it a task group → iterate all children → D cards
/haipipe-insight examples/ProjA/tasks/B03_band4/

# Path-based: give it a probe folder → auto-detect → K card
/haipipe-insight examples/ProjA/probes/0602_x_vs_baseline/

# Verb-based: explicit D card from a task
/haipipe-insight data examples/ProjA/tasks/B03_band4/01_eval_h24/

# Verb-based: synthesize I pattern from accumulated D cards
/haipipe-insight information --scope D01,D02,D03

# Verb-based: explicit K card from a probe
/haipipe-insight knowledge P.0602

# Verb-based: synthesize W recommendation from K cards
/haipipe-insight wisdom --scope K01

# Dashboard: show KB state
/haipipe-insight
/haipipe-insight explore
```

---

Risk Profile
-------------

CREATES files under `examples/<project>/insights/`. Never deletes cards — only adds new ones or updates INDEX.md. The post-file accumulation check is read-only (it suggests, never auto-files the next level).
