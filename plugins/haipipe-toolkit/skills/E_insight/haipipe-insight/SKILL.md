---
name: haipipe-insight
description: "Insight base orchestrator (the E_insight umbrella). Builds and maintains the project's cross-experiment knowledge base under examples/<project>/insights/ (D_observations / I_patterns / K_knowledge / W_wisdom). Reads CONFIRMED claims from D_experiment, never executes code. Routes intent to the right specialist (observations / patterns / knowledge / wisdom / session / plan / report / explore / gate / context). Trigger: insight, insights, knowledge base, what do we know, build insight, /haipipe-insight, ask a research question, synthesize across experiments."
argument-hint: [function] [args...]
allowed-tools: Bash, Read, Grep, Glob, Skill
---

Skill: haipipe-insight (orchestrator)
======================================

User-facing entry for the **Insight base** — the project's persistent
knowledge layer that synthesizes confirmed experiments into structured
markdown.

```
C_task          executes runs                            (code, GPU)
D_experiment    claims from runs (per-thread)            (yaml + verdicts)
E_insight       cross-experiment knowledge base   ← THIS SKILL FAMILY
F_paper         publication                              (final form)
```


Where the insight base lives (project-level)
---------------------------------------------

```
examples/Proj-X/
├── tasks/                                  (C_task)
├── experiments/                            (D_experiment)
└── insights/                               ← E_insight writes here
    ├── INDEX.md                            (auto: all entries + status)
    ├── sessions/                           (lightweight Q&A log; one .md per question)
    │   └── <YYYY-MM-DD>_<slug>.md
    │
    ├── D_observations/                     "what we observed"
    │   ├── O01_<slug>.md
    │   └── ...
    │
    ├── I_patterns/                         "what patterns emerged"
    │   ├── P01_<slug>.md
    │   └── ...
    │
    ├── K_knowledge/                        "what we now believe"
    │   ├── K01_<slug>.md
    │   └── ...
    │
    └── W_wisdom/                           "what we should do next"
        ├── W01_<slug>.md
        └── ...
```

**Hard rule:** NO code, no Python, no notebooks, no plots inside insights/.
That work belongs to C_task (code) or D_experiment (claim verdicts).
E_insight only synthesizes markdown.


Commands
--------

```
/haipipe-insight                                 dashboard (insight base overview)
/haipipe-insight ask <question>                  question-driven session (Phase 0–8)
/haipipe-insight session <question>              alias for ask
/haipipe-insight observations <exp-id>           D-level: write observation from one experiment
/haipipe-insight patterns [--scope <O*>]         I-level: synthesize cross-observation pattern
/haipipe-insight knowledge [--scope <P*>]        K-level: elevate pattern to validated belief
/haipipe-insight wisdom [--scope <K*>]           W-level: strategic recommendation
/haipipe-insight plan <question>                 plan a multi-phase synthesis
/haipipe-insight explore [project-path]          scan experiments/ for synthesis-ready threads
/haipipe-insight gate <phase>                    review proposed outcome of a phase
/haipipe-insight "<natural language>"            infer, dispatch
```


Specialists
-----------

```
haipipe-insight-session         WORKFLOW: question-driven; can call /haipipe-experiment
                                          to scaffold new arms if knowledge is missing
haipipe-insight-data    D-LEVEL:  read confirmed experiment → O*.md
haipipe-insight-information        I-LEVEL:  cross-observation patterns → P*.md
haipipe-insight-knowledge       K-LEVEL:  validated beliefs → K*.md
haipipe-insight-wisdom          W-LEVEL:  strategic recommendations → W*.md
haipipe-insight-plan            PLAN:     write plan-vN.yaml for a question
haipipe-insight-explore         READ:     coverage scan over experiments + insights
haipipe-insight-gate            REVIEW:   gate-outcome proposer between phases
haipipe-insight-context         LOAD:     per-phase context for the running specialist

(External-facing reports / messages / UI are NOT in E_insight — they
 live in G_application. E_insight's internal Q&A answer = the K/W
 entries written by the session + insights/sessions/<DATE>.md log.)
```


Function Verb Map
------------------

```
ask, question, /ask, "does X hold?", session    -> haipipe-insight-session
observations, observe, D-level, raw findings    -> haipipe-insight-data
patterns, I-level, cross-experiment trend       -> haipipe-insight-information
knowledge, K-level, validated belief, claim    -> haipipe-insight-knowledge
wisdom, W-level, recommendation, what next      -> haipipe-insight-wisdom
plan, plan-vN, design analysis                  -> haipipe-insight-plan
explore, coverage, scan, what can we synthesize -> haipipe-insight-explore
gate, review, approve/revise                    -> haipipe-insight-gate
context, load context                           -> haipipe-insight-context

(report / stakeholder doc / message → /haipipe-application; NOT E_insight)
```


Routing Logic
-------------

```
Step 1: Parse $ARGUMENTS.
Step 2: Resolve verb → specialist via verb map.
        - First positional is a verb → use it.
        - First positional is a question (has "?" or "does"/"is"/"why"
          opener) → default to /ask.
        - No args → dashboard (list current insights/).
Step 3: Validate project root (cwd-inferred or --project).
Step 4: Dispatch: Skill("haipipe-insight-<specialist>", args="<rest>").
Step 5: Surface specialist tail.
```


Boundary with D_experiment and C_task
---------------------------------------

The most-confused boundaries:

```
"this experiment confirmed X"             → D_experiment's claim
"5 experiments all show X"                → I-level pattern (E_insight)
"X is robust on val but not test-od"      → K-level knowledge (E_insight)
"we should re-test X with param-matched"  → W-level wisdom (E_insight)
"run param-matched re-test"               → triggers /haipipe-experiment
                                            (via /haipipe-insight-session)
```

**One-way dependencies:**

```
E_insight READS from D_experiment + C_task
E_insight CAN TRIGGER D_experiment (only via /haipipe-insight-session)
E_insight NEVER writes to tasks/ directly
D_experiment NEVER reads from insights/
```


Specialist Return Contract
---------------------------

```
status:    ok | blocked | failed | answered | budget
summary:   2-3 sentences
artifacts: [paths created / updated]
next:      suggested next command
```


Relation to other top-level skills
-----------------------------------

```
A_discover    feeds ideas → seeded questions for /haipipe-insight-session
B_project     project umbrella → owns the examples/Proj-X/ shape
C_task        provides runs → linked into experiments → into observations
D_experiment  provides claims → input to E_insight synthesis
F_paper       consumes K + W entries → academic publication
G_application consumes K + W entries → patient/clinician messages,
                                       UI sketches, stakeholder reports
                                       (external creation; never writes back)

E_insight is the cross-experiment synthesis hub: reads from D_experiment,
feeds F_paper + G_application. Source of "what does this project KNOW".
```


Files owned by this umbrella
-----------------------------

```
SKILL.md                              (this file)
ref/insight-md-schema.md              canonical entry schema (D/I/K/W)
ref/insight-context-loading.md        loading strategy for callers
ref/index-templates.md                INDEX.md / K-INDEX / W-INDEX templates
```


Schema authority
-----------------

Every insight entry under `examples/<project>/insights/` MUST conform
to `ref/insight-md-schema.md`. The 4 layer skills (data / information
/ knowledge / wisdom) all reference this single file as their entry
schema source.

When loading insight context for a query, follow `ref/insight-context-
loading.md` — layer-cascading + tag-filtering + INDEX-as-gateway.
