---
name: haipipe-application
description: "Application layer orchestrator (the G_application umbrella). Routes creation requests for project external-facing artifacts (patient/clinician messages, UI sketches, stakeholder reports) to the right kind-specialist. Each kind-specialist is itself an outer-loop session: reads K/W from E_insight, can trigger /haipipe-insight ask (which may chain into /haipipe-experiment) when knowledge gaps surface, then produces the artifact under examples/<project>/applications/<kind>/. NEVER writes back to insights/. Trigger: design a message, write a report, sketch UI, /haipipe-application."
argument-hint: [kind] [intent...]
allowed-tools: Bash, Read, Grep, Glob, Skill
---

Skill: haipipe-application (orchestrator)
==========================================

User-facing entry for **external-facing creation** — patient messages,
UI mockups, stakeholder reports. The "application layer" of the
haipipe stack:

```
C_task          executes runs                            (code, GPU)
D_experiment    claims from runs                         (yaml + verdicts)
E_insight       cross-experiment knowledge base          (D/I/K/W markdown)
F_paper         academic publication                     (paper-*)
G_application   external creation                ← THIS SKILL FAMILY
```

Where application artifacts live (project-level)
-------------------------------------------------

```
examples/Proj-X/
├── tasks/                                  (C_task)
├── experiments/                            (D_experiment)
├── insights/                               (E_insight)
├── paper/                                  (F_paper)
└── applications/                           ← G_application writes here
    ├── messages/<YYYY-MM-DD>_<audience>_<slug>.md
    ├── ui/<slug>/                          (sketches + annotated mocks)
    └── reports/<YYYY-MM-DD>_<audience>_<slug>.md
```

**Hard rules:**
- One-way: applications/ READS from insights/, NEVER writes back.
- If a creation request surfaces a knowledge gap, the kind-specialist
  triggers `/haipipe-insight ask <Q>` (which may chain into
  `/haipipe-experiment`). New entries land in insights/, then the
  specialist resumes drafting.
- Application artifacts must cite the K/W entries they used.


Commands
--------

```
/haipipe-application                                dashboard (list current artifacts)
/haipipe-application message <intent>               write a patient/clinician message
/haipipe-application ui <intent>                    UI sketch / spec
/haipipe-application report <intent>                external stakeholder report
/haipipe-application "<natural language>"           infer kind, dispatch
```


Specialists
-----------

```
haipipe-application-message    SESSION: outer-loop message creation
                                        (audience: patient / clinician)
haipipe-application-ui         SESSION: UI sketch / spec creation
                                        (audience: designer / dev)
haipipe-application-report     SESSION: external stakeholder report
                                        (audience: regulator / executive / partner)
```

Each specialist runs a Phase 0-N session:

```
Phase 0  Parse intent + audience
Phase 1  Load relevant K/W from insights/ (tag-filter via INDEX.md)
Phase 2  Gap check ── 是否知识充足？
            ├── yes → Phase 5
            └── no  → Phase 3
Phase 3  Propose missing knowledge → /haipipe-insight ask "<Q>"
              (insight-session can chain → /haipipe-experiment)
Phase 4  Re-load K/W after insight-session completes → re-evaluate
Phase 5  Draft artifact using kind-specific template
Phase 6  Self-review against audience requirements (ref/audience-requirements.md)
Phase 7  Atomic write to applications/<kind>/<...>.md
Phase 8  Return artifact path + cited K/W ids + experiment ids triggered
```


Function Verb Map
------------------

```
message, msg, sms, patient message, clinician note   -> haipipe-application-message
ui, sketch, mockup, screen, layout, wireframe        -> haipipe-application-ui
report, stakeholder, briefing, summary doc, exec     -> haipipe-application-report
```


Routing Logic
-------------

```
Step 1: Parse $ARGUMENTS.
Step 2: Resolve kind → specialist via verb map.
        - First positional matches a kind keyword → use it.
        - No args → dashboard (list current applications/).
        - Natural language → infer kind from keywords; ASK if ambiguous.
Step 3: Validate project root (cwd-inferred or --project).
Step 4: Dispatch: Skill("haipipe-application-<kind>", args="<rest>").
Step 5: Surface specialist tail.
```


Boundary with E_insight
------------------------

```
E_insight                                   G_application
─────────────────────                       ─────────────────────
"what does the project KNOW?"               "what does the project DELIVER?"
internal epistemic state                    external-facing artifacts
D/I/K/W structured entries                  message / ui / report
written by inference + experiments          written by kind-session
                                            cites K/W; never modifies them
```

**One-way dependencies:**

```
G_application READS from E_insight
G_application CAN TRIGGER E_insight (only via /haipipe-insight ask)
G_application NEVER writes to insights/, tasks/, or experiments/ directly
E_insight NEVER reads from applications/
```


Specialist Return Contract
---------------------------

```
status:    ok | blocked | failed | gap_unresolved
summary:   2-3 sentences (what artifact + which K/W cited)
artifacts: [paths created]
next:      suggested follow-up (open the artifact, revise, etc.)
```


Files owned by this umbrella
-----------------------------

```
SKILL.md                                  (this file)
ref/audience-requirements.md              shared audience/tone/length schema
ref/application-input-contract.md         how to read K/W from E_insight
```

These ref files are SHARED across all 3 kind-specialists. Each
kind-specialist reads them in Phase 1 (input contract) and Phase 6
(audience self-review).


Relation to other top-level skills
-----------------------------------

```
A_discover    seeds ideas → may suggest application themes
B_project     project umbrella → owns examples/Proj-X/applications/
C_task        runs code → indirect (via E_insight)
D_experiment  claims → indirect (via E_insight)
E_insight     K/W → REQUIRED INPUT for every G application
F_paper       parallel external artifact (academic only)
```

G_application is the "creative output" hub: read K/W, produce
audience-tailored artifacts, cite back.
