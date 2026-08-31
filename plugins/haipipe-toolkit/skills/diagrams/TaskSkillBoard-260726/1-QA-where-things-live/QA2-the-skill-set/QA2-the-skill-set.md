# ① The skill set: what ships
state: 🟡 PARTIAL
owner: JL
method: one router, nine execution domains, two Page Types, and no engine specifics above the specialist

## Opening
What is in the reusable package, and which surface does a human intend to use? The family now has two explicit surfaces: task-folder execution and a Task/Insights Board. On disk it contains 46 `SKILL.md` files: nine numbered execution domains, one task door, one workflow helper, and two Page Types (`task`, `insight`).

The number is still too large for a human to hold as a menu, so `/haipipe-task` remains the one door. It first distinguishes `execution` from `insight`; only the execution branch runs the scope and type inference needed to choose an engine specialist. The Insight branch creates or resumes a consumer-neutral D→I→K→W Page and never pretends to be a tenth execution engine.

What makes it hard is that the domains are not peers. `1_data`, `2_nn`, `3_end` and `4_individual` are whole skill families with their own routers, moved under `task/` because data, NN, endpoint and individual inference are all execution domains. `5_fit` through `9_agent` are a single specialist each. So one folder holds both a family and a leaf at the same level, and nothing in the naming says which is which.

**Covered elsewhere**: Which folder this is among the seven is `QA1`; the board that rules it is `QA3`; the group it writes into is `QA6`; the four phases it runs are the `QB` group; the acceptance test is `QE1`.

## Diagram
```
   one request, one direction, no second orchestrator

   user intent
        │
        ▼
   haipipe-task/           THE ROUTER. Decides WHICH, never HOW.
        │                 8-branch scope cascade + 4-level type cascade
        │                 owns ONLY the engine-agnostic invariants:
        │                 ref/hierarchy.md · ref/task-structure.md
        │                 ref/authoring-conventions.md
        │
        ├─▶ a FAMILY            each has its own router beneath this one
        │     1_data/      10 skills   haipipe-data + task-for-data/raw
        │     2_nn/         6 skills   haipipe-nn + task-for-algo
        │     3_end/       14 skills   haipipe-end + 12 deploy/develop leaves
        │     4_individual/ 5 skills   haipipe-individual + inference
        │
        ├─▶ a LEAF              one specialist, no family beneath
        │     5_fit/ 6_eval/ 7_display/ 8_stata/ 9_agent/    1 each
        │
        ├─▶ page-types/
        │     for-task     execution/design record
        │     for-insight  consumer-neutral D → I → K → W record
        │
        └─▶ agents/            the creator/reviewer/orchestrator triad  → QB6

   ⚠️ a family and a leaf sit at the SAME level with the SAME kind of
      name. 3_end holds 14 skills; 5_fit holds 1. Nothing says so.

   ── what the router may NOT keep ────────────────────────────
      engine specifics. Each /haipipe-task-for-<engine> child owns its
      OWN ref/ with templates and dialect. Stata is the clean case: on
      detection the router hands off WHOLESALE and the specialist owns
      its stage alphabet and its engine contract.

   ── what LEAVES this folder ──────────────────────────────
      execution ──▶ a scaffold, plan, code, report, QA digest
      Probe     ──▶ reads Task/Discovery sources inside an Insight Page
      PageX     ──▶ exports the settled Insight Page to Paper/Application
      runtime   ──▶ never reads design-board pages to execute a task
```

## Content
### The router decides which, never how
The one architectural rule the package states about itself is that `haipipe-task` owns only the
engine-agnostic invariants and every engine specific lives in the specialist's own `ref/`. That is
a good rule and it is why the router can carry nine domains without becoming nine routers.

The rule has one clean instance and it is worth naming as the model: Stata. On detecting
`engine = Stata`, the router hands off wholesale, and the specialist owns its own stage-letter
alphabet, its own templates and its own engine contract. Nothing about Stata appears above it.

### The roster is the part a human cannot hold
```
 1_data        10      2_nn      6      3_end     15
 4_individual   5      5_fit     1      6_eval     1
 7_display      1      8_stata   1      9_agent    2
 haipipe-task   1      haipipe-workflow 1      page-types 2
 agents         3 (not skills)
```
Nine folders, and the largest holds fourteen times what the smallest does. That is not
necessarily wrong, but it means the numbered prefix carries no information about weight, and a
reader looking for "where does deployment live" has to already know that `3_end` is a family.

### What the specialist owns that the router must not
A `haipipe-task-for-<type>` specialist owns the scaffold for its type: which config skeleton to
seed, where its results land, which parameters its `run.sh` injects. `ref/hierarchy.md` states the
split as four things the type decides, and the useful half of it is the last: the process is
invariant, only the contents change.

That is the sentence that keeps the package from forking into nine lifecycles. Every type runs
Plan, Build, Execute, Report; every type produces four sister files bound by one token; every type
writes light artifacts to `results/` and heavy ones to `_WorkSpace/`. A specialist that needed a
fifth phase would be a different skill family, not a new type.

## Aims
- [ ] 🧭 Rule whether a family and a leaf may share a naming level
      `3_end/` holds 14 skills and `5_fit/` holds 1, at the same depth with the same kind of name. Either that is fine and should be said out loud, or the families should be marked.
- [ ] ✂️ Rule how much thinking the door may do
      An 8-branch scope cascade plus a 4-level type cascade runs before any dispatch. Every branch is defensible; the total is the thing to judge, and nobody has judged it.
- [ ] 🚪 Add the board entry to the router
      Blocked on `QA4`'s door ruling. This is where it lands: a new branch, or a changed meaning for branch 4.
- [ ] 📏 State what the router is allowed to keep
      "Engine-agnostic invariants" names three ref files today. Whether that list is closed, and what a tenth domain would be allowed to add, is not written.
- [x] 💡 Separate execution from reusable insight
      `/haipipe-task insight` creates or resumes an Insight Page; Probe reads Task/Discovery evidence there, and PageX exports only the settled Page.

## Discussion

### From the retired States section (merged 260831)
The package runs and is in daily use across 67 groups. The routing rule is stated and Stata is a
clean instance of it. Nothing about the board entry exists.
- 260817 CC · 💡 The family now exposes two surfaces
      Execution keeps Plan → Build → Execute → Report. Insight uses the shared Page lifecycle and a fixed D→I→K→W contract; it is not another engine domain.
- 260817 CC · 📏 Recounted from disk
      46 `SKILL.md`: the prior 44 plus two Page Types; `3_end` now contains 15.

## Files
- `SKILL.md`
  The router: the scope cascade, the type-inference cascade, the specialist table.
- `DESIGN.md`
  The layering, and the 2026-06-21 decision that specialist names stay `haipipe-task-for-*` on purpose.
- `hierarchy.md`
  The three levels and the four things a task-type decides.

## Log
260817 · Added the Task/Insights Board surface, `insight` routing, the two Page Types, and the Probe-in/PageX-out boundary.
260726 · Created with the board.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0