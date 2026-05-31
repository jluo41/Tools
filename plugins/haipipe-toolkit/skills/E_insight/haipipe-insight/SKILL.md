---
name: haipipe-insight
description: "Insight base orchestrator (the E_insight umbrella). Builds and maintains the project's cross-probe knowledge base under examples/<project>/insights/ (D_data / I_information / K_knowledge / W_wisdom). Reads CONFIRMED claims from D_probe/D_probe, never executes code. Routes intent to the right specialist (observations / patterns / knowledge / wisdom / session / plan / report / explore / gate / context). Trigger: insight, insights, knowledge base, what do we know, build insight, /haipipe-insight, ask a research question, synthesize across probes."
argument-hint: [function] [args...]
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-05-31"
  summary: "Insight base orchestrator (the E_insight umbrella)."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
---

Skill: haipipe-insight (orchestrator)
======================================

User-facing entry for the **Insight base** — the project's persistent
knowledge layer that synthesizes confirmed probes into structured
markdown.

```
C_task          executes runs                            (code, GPU)
D_probe         claims from runs (per-thread)            (yaml + verdicts)
                compatibility name: D_probe
E_insight       cross-probe knowledge base   ← THIS SKILL FAMILY
F_paper         publication                              (final form)
```


Where the insight base lives (project-level)
---------------------------------------------

```
examples/Proj-X/
├── tasks/                                  (C_task)
├── probes/                            (D_probe / D_probe)
└── insights/                               ← E_insight writes here
    ├── INDEX.md                            (auto: all entries + status)
    ├── sessions/                           (lightweight Q&A log; one .md per question)
    │   └── <YYYY-MM-DD>_<slug>.md
    │
    ├── D_data/                     "what we observed"
    │   ├── D01_<slug>.md
    │   └── ...
    │
    ├── I_information/                         "what patterns emerged"
    │   ├── I01_<slug>.md
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
That work belongs to C_task (code) or D_probe (claim verdicts).
E_insight only synthesizes markdown.


Commands
--------

```
/haipipe-insight                                 dashboard (insight base overview)
/haipipe-insight data <exp-id>                   D-level: file observation card from one probe
/haipipe-insight information [--scope <D*>]      I-level: synthesize cross-probe pattern
/haipipe-insight knowledge [--scope <I*>]        K-level: file validated belief (claim from probe)
/haipipe-insight wisdom [--scope <K*>]           W-level: strategic recommendation
/haipipe-insight explore [project-path]          scan probes/ for synthesis-ready threads
/haipipe-insight "<natural language>"            infer, dispatch

(For question-driven sessions: → /haipipe-application ask
 For session machinery (plan / gate / context): → G_application/)
```


Specialists
-----------

```
haipipe-insight-data            D-LEVEL:  file observation card from a task or probe → D*.md
haipipe-insight-information     I-LEVEL:  cross-probe patterns → I*.md
haipipe-insight-knowledge       K-LEVEL:  validated beliefs (from confirmed probes) → K*.md
haipipe-insight-wisdom          W-LEVEL:  strategic recommendations → W*.md
haipipe-insight-explore         READ:     coverage scan over probes + insights

(Session machinery — plan / gate / context — and the question-driven
 ask workflow live in G_application. E_insight only files cards into
 the permanent KB; it does NOT run sessions or hold per-question state.)
```


Function Verb Map
------------------

```
data, observations, D-level, raw findings       -> haipipe-insight-data
information, patterns, I-level, trend           -> haipipe-insight-information
knowledge, K-level, validated belief, claim     -> haipipe-insight-knowledge
wisdom, W-level, recommendation, what next      -> haipipe-insight-wisdom
explore, coverage, scan, what can we synthesize -> haipipe-insight-explore

(ask / question / session / plan / gate / context → /haipipe-application; NOT E_insight)
(report / stakeholder doc / message / ui         → /haipipe-application; NOT E_insight)
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


Boundary with D_probe and C_task
---------------------------------------

The most-confused boundaries:

```
"this probe confirmed X"                  → D_probe's claim
"5 probes all show X"                → I-level pattern (E_insight)
"X is robust on val but not test-od"      → K-level knowledge (E_insight)
"we should re-test X with param-matched"  → W-level wisdom (E_insight)
"run param-matched re-test"               → triggers /haipipe-probe
                                            (via /haipipe-application ask)
```

**One-way dependencies:**

```
E_insight READS from D_probe + C_task
E_insight NEVER triggers D_probe (that's G_application's ask kind)
E_insight NEVER writes to tasks/ or probes/ directly
E_insight ONLY files DIKW cards into insights/ from already-existing evidence
D_probe NEVER reads from insights/
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
A_discover    feeds ideas → seeded questions handled in G_application ask
B_project     project umbrella → owns the examples/Proj-X/ shape
C_task        provides D/I evidence → filed by haipipe-insight-data/-information
D_probe       provides K/W claims    → filed by haipipe-insight-knowledge/-wisdom
F_paper       consumes K + W entries → academic publication
G_application drives sessions (ask / message / ui / report) that read K/W
              and (ask kind only) trigger new tasks / probes / KB writes

E_insight is the project's PERMANENT KB. It does NOT run sessions or
own per-question state. It just files cards. Source of "what does
this project KNOW".
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
