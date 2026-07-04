Review Checklist (ARCHIVED 2026-07-03)
=======================================

Archived from project/haipipe-project/ref/project-structure.md when that file was rewritten to the ownership principle (container-only). This checklist belonged to the retired review fn; the original review/organize skills are preserved in _archive/haipipe-project-inspect/. Kept verbatim for reference only; each world's owning skill now carries its own validation rules.

---

Review Checklist
=================

Project structure:
  [ ] Name matches Proj{Series}-{Category}-{Num}-{Name}
  [ ] tasks/ + probes/ + insights/ + diagram/ exist at project root
  [ ] applications/ exists if any external artifacts have been created
  [ ] No top-level configs/, results/, README.md, docs/, cc-archive/, _old/
  [ ] Tasks live under tasks/{G}{NN}_{group}/{NN}_{name}/
  [ ] Active probes live under probes/{MMDD}_{slug}/
  [ ] Inactive/completed/deprecated probes live under probes/{YYYY}-archive/{MMDD}_{slug}/ with original name preserved
  [ ] Insights live under insights/{D,I,K,W}_*/ with INDEX.md at root
  [ ] Applications (if present) live under applications/{messages,ui,reports}/
  [ ] {PROJECT}/diagram/ has 01-story, 02-boundary, 03-exploration, project.excalidraw (canvas fresher than .txt sources)

Per group:
  [ ] No README.md
  [ ] Group letter G matches its tasks' series
  [ ] sbatch/ exists for cross-task orchestration (env.sh + batchers)
  [ ] If cohesive: {group}/diagram/ has 01-overview, 02-tasks, 03-progress, 04-design, group.excalidraw

Per task (standard):
  [ ] >=1 *.py at task root, no README.md
  [ ] Either group/diagram/ or task/diagram/ covers this task
  [ ] configs/ has own YAMLs (no symlinks)
  [ ] runs/ scripts atomic (1 config = 1 script, no loops, no CLI args)
  [ ] runs/<run>.sh ↔ results/<run>/ name pairing holds
  [ ] sbatch/ scripts call runs/*.sh, never *.py
  [ ] No heavy files in results/ (heavy → _WorkSpace/)
  [ ] notebooks/ has <run>.ipynb per runs/<run>.sh; template <stem>.ipynb sits at task root next to <stem>.py
  [ ] runs/*.sh include the "Files-generated footer" (Template A) — every run prints local results + _WorkSpace writes on EXIT
  [ ] runs/*.sh consistently use Template A (tee log) OR Template B (papermill); never mix on same task
  [ ] Papermill-mode .py: # %% [parameters] cell as first cell; auto-detects TASK_DIR via __file__ → __vsc_ipynb_file__ → os.environ['TASK_DIR']

Per task (skill-runner exemption):
  [ ] No *.py / data/ required
  [ ] runs/<slug>.sh execs `claude` (interactive, not `-p`); no tee header; passes --session-id $(uuidgen) and copies session.jsonl to results/
  [ ] If ≥2 questions: configs/<slug>.yaml + runs/_run.sh shared launcher + runs/ask_<slug>.sh one-line wrappers (`_`-prefix = shared/template)

Per probe (if any probes/ folders exist):
  [ ] Folder name is {MMDD}_{slug} (MMDD = creation date: MM month, DD day; same-day collisions get a letter suffix, e.g. 0601b)
  [ ] probe.yaml exists; passes schema (probe/haipipe-probe/ref/probe-yaml-schema.md)
  [ ] No *.py / *.ipynb / *.png / *.pdf inside probe folder
  [ ] If result.status == confirmed: review.md + INTEGRITY_AUDIT.md + CLAIMS_FROM_RESULTS.md all present
  [ ] LOOP_LOG.md (if loop ever started) records all rounds + final status
  [ ] logs/ entries are date-named (YYYY-MM-DD.md), append-only
  [ ] All probe.yaml arms[*] run-paths exist under tasks/

Per insight base (if insights/ exists):
  [ ] Top-level insights/INDEX.md present and fresh
  [ ] D_data/, I_information/, K_knowledge/, W_wisdom/ folders exist
  [ ] K_knowledge/INDEX.md and W_wisdom/INDEX.md present (high-signal layers)
  [ ] Every entry has YAML frontmatter (id, layer, tags, status, created, updated, sources, ref_by) per insight/ref/insight-md-schema.md
  [ ] No *.py / *.ipynb inside insights/ (synthesis only, no code)
  [ ] sources / ref_by are consistent (if K cites P, P's ref_by lists the K)
  [ ] All K entries cite ≥ 1 P; all W entries cite ≥ 1 K
  [ ] Each entry ≤ 200 lines total (frontmatter ≤ 13 + body ≤ 200)
  [ ] No reports/ or external-facing synthesis docs (those moved to applications/; insights/ is internal epistemic state only)

Per application (if applications/ exists):
  [ ] applications/INDEX.md present and fresh
  [ ] Artifacts live under applications/{messages,ui,reports}/
  [ ] Each artifact has YAML frontmatter (kind, audience, intent, created, cited_K, cited_W, triggered, status) per application/haipipe-application/ref/ audience-requirements.md
  [ ] cited_K / cited_W populated for every load-bearing claim
  [ ] No K cited with status=superseded as if active
  [ ] Length within audience budget (patient ≤ 200w, clinician ≤ 400w, regulator ≤ 1500w, executive ≤ 600w, partner ≤ 800w, designer/dev kind=ui per spec)
  [ ] No *.py / *.ipynb / no edits to insights/ from this layer
  [ ] If status=draft: "## Open questions" section present listing unresolved gaps

Paper (if applicable):
  [ ] paper/Paper-*/diagram/ has 01-overview, 02-figure-plan
  [ ] paper.excalidraw fresher than .txt sources
