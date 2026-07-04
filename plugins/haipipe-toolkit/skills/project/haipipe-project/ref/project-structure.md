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
  ├── probes/         MANDATORY  claim-level evidence contracts (owner: /haipipe-probe)
  ├── discoveries/    MANDATORY  external-evidence topics, one topic = one folder (owner: /haipipe-discovery)
  ├── insights/       MANDATORY  D/I/K/W knowledge base (owner: /haipipe-insight)
  ├── diagram/        MANDATORY  project-level story, high-level only (owner: this skill)
  ├── papers/         OPTIONAL   manuscripts; each Paper-{Name}-{venue}/ often a git submodule (owner: /haipipe-paper-*)
  └── applications/   OPTIONAL   external deliverables: messages / ui / reports (owner: /haipipe-application-*)

papers/ is plural for all NEW scaffolds, matching its sibling collections; legacy projects (ProjA-D) use singular paper/; do not migrate them (submodule paths in .gitmodules). diagram/ stays singular (it is a doc surface, not a collection).

Forbidden at top level: configs/, results/, docs/, cc-archive/, _old/, and README.md for plain-dir ProjX-* projects (repo-backed Project-* projects DO get a README.md).

---

The Seven Worlds
=================

  Folder          Role               One-liner
  --------------  -----------------  ------------------------------------------------------------------------
  tasks/          WORK               execution: code, configs, runs, metrics; one task-folder = one runnable unit
  probes/         CLAIMS             hypothesis -> evidence -> verdict; one probe = one claim-level contract; no code
  discoveries/    EXTERNAL-EVIDENCE  Search / Review / Idea folders; one topic = one folder; probe-unaware (the calling probe records the link)
  insights/       KNOWLEDGE          cross-probe synthesis cards (D/I/K/W markdown); no code
  papers/         PUBLISH            academic manuscripts
  applications/   DELIVER            external artifacts for non-academic audiences; reads K/W, never writes back
  diagram/        STORY              high-level project motivation / boundary / exploration

One-way dependency map (cross-cutting orientation; no single world owns it):

  probes/        READS tasks/ + discoveries/   (links runs and external evidence via evidence:)
  insights/      READS probes/ + tasks/        (D/I/K/W synthesis)
  papers/        READS insights/K + W, plus probes/tasks as needed
  applications/  READS insights/K + W          (can TRIGGER /haipipe-insight ask to close gaps; NEVER writes back)
  discoveries/   NEVER read probes/ or insights/ (probe-unaware; the calling probe records the link on its own side)
  tasks/         NEVER read probes/ discoveries/ insights/ papers/ applications/
  probes/        NEVER read insights/

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
  probes/         /haipipe-probe           probe/haipipe-probe/ref/probe-yaml-schema.md
  discoveries/    /haipipe-discovery       discovery/haipipe-discovery/SKILL.md (folder contract: discovery.yaml + evidence files)
  insights/       /haipipe-insight         insight/ref/insight-md-schema.md (+ insight/ref/index-templates.md)
  papers/         /haipipe-paper-*         paper wiki (paper/wiki/) + paper/3-build-submit/haipipe-paper-folder (paper-folder contract)
  applications/   /haipipe-application-*   application/haipipe-application/ref/audience-requirements.md + application-input-contract.md
  diagram/        this skill               this file (Project-Level diagram/ section above)
