---
name: haipipe-narrative
description: "Story layer (N_narrative). Manages the project's LIVING narratives under examples/<project>/narratives/ — the right-hand side of the KB ⇄ Narrative double arrow. A narrative is a story line: an angle, the claims it needs (by reference to insights/K), an ignite-log, and a section decision-tree. Reads the KB (insights/K + W) to surface claim GAPs; never writes to probes/tasks/insights. Distinct from F_paper/1-narrative/narrative-report (that is a one-shot paper contract; THIS is the upstream living story). NO code, pure markdown. Trigger: narrative, story, story line, angle, ignite, am I ignited, what story, sell this, which claims do I need, narrative gap, /haipipe-narrative."
argument-hint: "[new|status|claims|ignite] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-05-31"
---

Skill: haipipe-narrative (story layer)
========================================

User-facing entry for the **Narrative layer** — the project's LIVING
stories. Each narrative selects a subset of the KB and argues "here is the
angle, here is why it matters, here is the claim I must defend, here is what
I still need".

```
C_task        executes runs                      (code, GPU)
D_probe       claims from runs                    (probe.yaml + verdicts)
E_insight     cross-probe knowledge base (KB)     (D/I/K/W cards)
N_narrative   the living story over the KB   ← THIS SKILL FAMILY
F_paper       publication (renders a ready story)
G_application delivery (paper / report / message / ui)
```

**The engine.** ARCHITECTURE.md's one rule: KB ⇄ Narrative is the only
double arrow. This skill owns the Narrative side.

```
   🧠 KB (facts)  ⇄[🔥 ignite]⇄  📖 N_narrative (story)
   probes/ tasks/                  narratives/<NN>_<slug>/
   insights (D/I/K/W)              story + claims + ignite-log + decision-tree
```

- KB → Narrative (induction): a probe's claim ignites a story angle.
- Narrative → KB (deduction): a story's GAP says which probe to crack next.


NOT to be confused with narrative-report
=========================================

`F_paper/1-narrative/narrative-report` already exists. It is DIFFERENT and
does NOT conflict — strictly upstream → downstream:

```
narratives/01_fairness/  ──(status: ready)──►  narrative-report  ──►  NARRATIVE_REPORT.md ──► /haipipe-paper
   (living story, mutates)                      (snapshots it now)        (frozen, per venue)
```

THIS skill owns the living story + ignite. narrative-report snapshots a
`ready` story into a paper contract. 1 narrative : N papers.


Where narratives live (project-level)
======================================

```
examples/<PROJECT_ID>/narratives/
├── INDEX.md                  (auto: all narratives + ignite status)
├── 01_<slug>/                folder-per-narrative (2-digit, no gap on create)
│   ├── story.md              angle + why-it-sells + one-sentence core claim
│   ├── claims.md             needed K cards (BY REFERENCE) + GAP/weak rows
│   ├── ignite-log.md         ③ append-only "am I ignited?" judgments
│   └── decision-tree.md      section paths A/B/C/D
└── 02_<slug>/
    └── ...
```

**Hard rules** (mirror E_insight discipline):
- NO code, no notebooks, no plots. Pure markdown.
- `claims.md` references K cards by ID (`needs: [K01, K03]`), never copies.
- NEVER writes to probes/ tasks/ insights/. Reads the KB; records story state.
- Does NOT trigger a probe directly (that is scope B, via G_application ask).
- 1 narrative : N papers. Papers back-ref via `papers:` in story.md frontmatter.


Commands
--------

```
/haipipe-narrative                          dashboard (list narratives + ignite state)
/haipipe-narrative new <slug>               scaffold narratives/<NN>_<slug>/ (4 files)
/haipipe-narrative status [<id>]            overview: all narratives, or one in detail
/haipipe-narrative claims <id>              read insights/K, mark each needed slot have/weak/GAP
/haipipe-narrative ignite <id>              append an ignite-log entry; maybe flip status
/haipipe-narrative "<natural language>"     infer, dispatch
```

Scope note: `claims` SURFACES gaps only — it does not auto-fire a probe.
Auto-firing (claims → /haipipe-probe design) is scope B, deferred.


Function verb map
-----------------

```
new, create, start, scaffold a story            -> new
status, list, dashboard, show narratives, where -> status
claims, needs, what do I need, gap, gaps        -> claims
ignite, ignited?, am I ignited, sellable?, fire -> ignite
question opener (does/is/why) or vague topic     -> suggest /haipipe-application ask
```


Routing logic
-------------

```
Step 1: Parse $ARGUMENTS.
Step 2: Resolve verb via the map.
        - First positional is a verb → use it.
        - No args → dashboard (list narratives/).
Step 3: Resolve project root (cwd-inferred, or --project).
Step 4: Execute the verb (this skill owns all four; no sub-specialists in scope A).
Step 5: Emit the tail.
```


Verb workflows
--------------

### new <slug>

```
1. Resolve project root; ensure narratives/ exists (create + INDEX.md if first).
2. NN = max existing narratives/<NN>_* + 1 (zero-padded, no gap).
3. Create narratives/<NN>_<slug>/ with the 4 files seeded from
   ref/narrative-schema.md skeletons. status defaults to `exploring`.
4. Append a line to narratives/INDEX.md.
5. Tail: suggest /haipipe-narrative claims <NN> once K cards exist.
```

### status [<id>]

```
No id  → table of all narratives: id | slug | status | #claims have/weak/GAP |
         last ignite verdict | papers[].
With id→ render that narrative's story.md summary + claims ledger counts +
         latest ignite-log entry.
Read-only. Never edits.
```

### claims <id>

```
1. Load narratives/<id>/claims.md `needs[]`.
2. Read insights/K_knowledge/*.md (and W_wisdom/*.md of type next_probe).
3. For each needed slot, mark:
     have  — a K card matches AND confidence is high/medium
     weak  — a K card matches BUT confidence low/contested
     GAP   — no K card matches
4. Rewrite claims.md ledger table + Gap summary (atomic write).
5. Tail: list the GAP/weak rows as "candidate next probes" (text only —
   do NOT scaffold a probe; that is scope B).
```

### ignite <id>

```
1. Load narratives/<id>/story.md + claims.md (current have/weak/GAP).
2. Interactive (AUTO: best-effort): ask
     - ignited? (yes/no)
     - why? (one or two sentences — honest; a "no" is valuable)
     - next? (what this implies: crack probe for slot Cx / re-scope / shelve)
3. Append a dated entry to ignite-log.md (append-only; never rewrite history).
4. Optionally flip story.md `status`:
     yes + all needed slots have   → ready
     yes + gaps remain             → igniting
     no  + spine claim is GAP/dead → exploring (re-scope) or shelved (user choice)
5. Tail: if status→ready, suggest /narrative-report to snapshot into a paper.
```


Interfaces to neighbours
========================

```
reads:   insights/K_knowledge/*.md    (fill claims have/weak/GAP)
         insights/W_wisdom/*.md         (type: next_probe = candidate gaps)
         probes/INDEX.md                (what's already been probed)
writes:  narratives/<NN>_<slug>/*       (only here) + narratives/INDEX.md
feeds:   F_paper/1-narrative/narrative-report  (when status=ready)
         G_application ask kind          (scope B: gap rows → ask sub-questions)
NEVER:   writes probes/ tasks/ insights/ ; triggers a probe directly
```


Schema authority
----------------

Every file under `narratives/` MUST conform to
`ref/narrative-schema.md` (the canonical schemas for story / claims /
ignite-log / decision-tree).


Specialist tail
---------------

```
status:    ok | blocked | failed
summary:   2-3 sentences (what narrative, what changed, ignite verdict if any)
artifacts: [paths created / updated]
next:      suggested next command
```


Relation to other top-level skills
-----------------------------------

```
E_insight     provides K + W cards → narrative reads them for claims/gaps
D_probe       a GAP becomes a candidate next probe (scope B auto-wires this)
F_paper       a `ready` narrative is snapshotted by narrative-report → paper
G_application reads K/W for delivery; ask kind can close narrative gaps (scope B)

N_narrative is the project's LIVING STORY. It does not run probes or file
KB cards; it selects, argues, and judges ignition over the KB.
```
