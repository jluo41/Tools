Project Container Structure (examples/)
========================================

Scope: /haipipe-project owns ONLY the top-level project container described here. Each subfolder's internal structure is owned by its skill family (see Structure Ownership at the bottom) and is consulted at the owner, never restated in this file.

The doc surface of a project is diagram/, not README.md (plain-dir projects; repo-backed Project-* projects do get a README.md). Diagram .txt sources are authored via /diagram-ascii (ASCII + emoji) and bundled into .excalidraw via /diagram-ascii-canvas. Both .txt and .excalidraw are committed: .txt is grep-able and LLM-readable; .excalidraw is the human-readable, annotatable canvas.

---

Naming
=======

Two project kinds, decided by name:

  ProjX-*     plain directory under examples/ (fn/project.md)
  Project-*   repo-backed: own GitHub repo + submodule at examples/<name> + scaffold + push + pointer bump (fn/repo-project.md)

Plain-dir naming:

  Proj{Series}-{Category}-{Num}-{Name}

  Series    single uppercase letter (A=misc, B=benchmarking, C=models, D=EHR)
  Category  short descriptor (Bench, Model, EHR, Pretrain)
  Num       sequential integer within Series-Category
  Name      CamelCase (FairGlucose, ScalingLaw, WeightPredict)

---

Standard Top-Level Layout
==========================

  examples/{PROJECT_ID}/
  ├── tasks/          MANDATORY  execution work (owner: /haipipe-task)
  ├── discoveries/    MANDATORY  external-evidence topics, one topic = one folder (owner: /haipipe-discovery)
  │                   (probes/ RETIRED 2026-07-05 — the probe owns no folder in the execution tree.
  │                    insights/ RETIRED 2026-07-12 — the insight layer is fully retired. Legacy
  │                    probes/ and insights/ folders in old projects are dead history: nothing reads
  │                    them, nothing writes them; do NOT delete, do NOT scaffold.)
  ├── diagram/        MANDATORY  project-level story, high-level only (owner: this skill)
  ├── papers/         OPTIONAL   manuscripts; each Paper-{Name}-{venue}/ often a git submodule (owner: /haipipe-paper-*)
  └── applications/   OPTIONAL   external deliverables: messages / ui / reports (owner: /haipipe-application-*)

papers/ is plural for all NEW scaffolds, matching its sibling collections; legacy projects (ProjA-D) use singular paper/; do not migrate them (submodule paths in .gitmodules). diagram/ stays singular (it is a doc surface, not a collection).

Forbidden at top level: configs/, results/, docs/, cc-archive/, _old/, and README.md for plain-dir ProjX-* projects (repo-backed Project-* projects DO get a README.md).

---

The Five Worlds
================

  Folder          Role               One-liner
  --------------  -----------------  ------------------------------------------------------------------------
  tasks/          WORK               execution: code, configs, runs, metrics; one task-folder = one runnable unit
  discoveries/    EXTERNAL-EVIDENCE  Search / Review / Idea folders; one topic = one folder; consumer-unaware
  papers/         PUBLISH            academic manuscripts
  applications/   DELIVER            external artifacts for non-academic audiences
  diagram/        STORY              high-level project motivation / boundary / exploration

  tasks/ + discoveries/ are the two EXECUTORS — same shape, same rules. Together they are the
  project's evidence BANK. papers/ + applications/ are the CONSUMERS.

  (insights/ was a sixth world — the D/I/K/W knowledge base — RETIRED 2026-07-12. What a K card
   was meant to be is now split correctly in two: the general, reusable FACT is the executor's
   own QA/<n>-<slug>.md; the paper-specific JUDGMENT is that paper's own 1-claims.md entry.)

One-way dependency map (cross-cutting orientation; no single world owns it):

  papers/        READ tasks/ + discoveries/ BY PATH — a section in the paper's own
                 1-probes/PPNN_<topic>/ carries `target: <task-folder>/QA/<n>-<slug>.md`
  applications/  same model (applications/<A>/1-probes/); NEVER write back
  discoveries/   consumer-unaware (the consumer records the link on its own side)
  tasks/         NEVER read discoveries/ papers/ applications/

---

The Evidence Contract (this skill's ONE hard rule about the bank)
==================================================================

Owner: /haipipe-probe (skills/probe/haipipe-probe/SKILL.md). Restated here ONLY as a scaffolding
prohibition, because this skill is the thing that creates folders.

  ⚙️ THE BANK IS PROBE-UNAWARE. Nothing under tasks/ or discoveries/ may carry an _ASK/ folder,
     an _ANS/ folder, an `answers:` field, or a PP id. THIS SKILL NEVER MINTS ONE. (The _ASK/
     mailbox of the 2026-07-11 bridge design is DEAD — killed 2026-07-14.)

  ✅ WHAT A LEAF MAY CARRY, optionally:

       tasks/{G}{NN}_{group}/{NN}_{task}/          discoveries/{S|L|P}{NN}_{group}/{NN}_{topic}/
       ├── workflow/plan.yaml   Q  code            ├── discovery.yaml              Q  spec
       ├── results/             A  code            ├── sources.md · verdict.md ·
       └── QA/                  A  readable        │   landscape.md                A  raw
           ├── 1-<slug>.md                         └── QA/                  A  readable
           └── 2-<slug>.md                             └── 1-<slug>.md

     QA/<n>-<slug>.md — the executor's READABLE digest of a direction it has explored.
       · <n> = creation order. The NUMBERING IS THE INDEX; `ls QA/` IS the index. No INDEX file.
       · SLUG ONLY. A PP id in a bank filename is the contract broken.
       · WRITER: the EXECUTOR, at its Report stage. Write-once.
       · NOT SCAFFOLDED AT SETUP. It appears when the task-folder has something to say.
       · Applies to BOTH banks — task and discovery are both executors.

  📄 THE CONSUMER holds the questions: papers|applications/<X>/1-probes/PPNN_<topic>/
     (renamed from 1-probe-plans/ on 2026-07-14). Created by the consumer's own PROBE phase,
     never by this skill. Bound to the bank BY PATH — no id ever crosses.

---

Project-Level diagram/
=======================

The one subfolder whose internal structure this skill owns. EMPTY at setup (setup is quick); authored later on request via /diagram-ascii, bundled via /diagram-ascii-canvas (txt-to-canvas.py).

  examples/{PROJECT_ID}/diagram/
  ├── 01-story.txt          motivation, research question, expected impact
  ├── 02-boundary.txt       in-scope / out-of-scope / definitions / assumptions
  └── project.excalidraw    bundle (built by txt-to-canvas)

HIGH-LEVEL ONLY: research narrative, not an operational dashboard. Status tables, run metrics, and daily logs belong in group/task diagram/ (owner: /haipipe-task). Refresh on substantive narrative change; otherwise stable.

---

_WorkSpace Paths
=================

Heavy data stores (_WorkSpace/) are declared in env.sh and read by setup_workspace() in code/haipipe/base.py. NEVER inside the project folder.

---

Structure Ownership
====================

For anything below the top level, consult the owner; this file never restates their rules.

  World           Owner skill              Schema authority
  --------------  -----------------------  --------------------------------------------------------------------------
  tasks/          /haipipe-task            task/haipipe-task/ref/task-structure.md (layout), plus ref/hierarchy.md + ref/authoring-conventions.md
  discoveries/    /haipipe-discovery       discovery/haipipe-discovery/SKILL.md (folder contract: discovery.yaml + evidence files)
  papers/         /haipipe-paper-*         paper wiki (paper/wiki/) + paper/3-deliver/1-build/haipipe-paper-folder (paper-folder contract)
  applications/   /haipipe-application-*   application/_audience/audience-requirements.md + the venue playbooks under application/_venue/
  diagram/        this skill               this file (Project-Level diagram/ section above)
