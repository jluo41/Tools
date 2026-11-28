Discovery Workbench Table
=========================

Shape and check: `skills/0_utils/table-workbench/SKILL.md`. One Discovery Block is one
workbench (`/w/<block>`). Rows run input → process → output: Scope states the Block,
its Questions, its links and its drawings; Work finds and reads the papers, one Paper Run
each, and writes each Task's synthesis and the Questions' reports; Check reads every Run
receipt and which citations still need a person; Delivery holds the answered reports and
the Block's BibTeX. Folder is where the run writes: `Block ›` is the Block folder
(`discovery/bNN_<block>/`), `Tools ›` the workbench's server folder (retired to `servers/_old/workbench-discovery/`; the Spaces below are that retired page's); `none` writes no file,
only a verdict.

Agents are the Discovery family's own (`skills/2_work/discovery/agents/`): the orchestrator
routes, the creator writes Task Pages, Runs, Results and synthesis, the search worker
returns candidates only, and the reviewer judges what the creator made, never its own.
Reports are Pages: `hai-draft-writing-agent` writes, `hai-draft-check-agent` checks.

| Level | Space | View | Run type | Agent | Skill | Person signs | Folder |
|---|---|---|---|---|---|---|---|
| board | Guide | Description | none | none | none | none | none |
| board | Guide | Method | none | none | none | none | none |
| board | Guide | RoadMap Draw | none | none | none | none | none |
| board | Guide | Related Paper | Add a paper | hai-discovery-orchestrator-agent | hai-discovery | the source check | Tools › related/papers.md |
| board | Scope | Block | none | none | none | none | none |
| board | Scope | Questions | Ask a Question | hai-discovery-creator-agent | hai-report | the question | Block › board.md (Questions) · reports/qNN_<topic>/ |
| board | Scope | Questions | Review the questions | hai-discovery-reviewer-agent | hai-report | a change | none |
| board | Scope | Resources | Add a resource | hai-discovery-creator-agent | hai-report | none | Block › board.md (Related resources) |
| board | Scope | RoadMap Draw | Draw | hai-discovery-creator-agent | hai-studio | none | Block › studio/<name>.excalidraw |
| board | Work | Papers | Find papers | hai-discovery-search-worker-agent | hai-discovery-search | none | none |
| board | Work | Papers | Read a paper | hai-discovery-creator-agent | hai-discovery-review | none | Block › jNN_<job>/tNN_<task>/runs/rNN_<paper>/rNN_<paper>.sh · runs/rNN_<paper>/result/ |
| board | Work | Tasks | Synthesize a Task | hai-discovery-creator-agent | hai-discovery-synthesize | none | Block › jNN_<job>/tNN_<task>/summary.md |
| board | Work | Questions | Write the report | hai-draft-writing-agent | hai-draft-writing | none | Block › reports/qNN_<topic>/ |
| board | Check | Runs | Review a Run | hai-discovery-reviewer-agent | hai-discovery-review | none | none |
| board | Check | Citations | Verify a citation | hai-discovery-search-worker-agent | hai-discovery-search | the citation | Block › jNN_<job>/tNN_<task>/runs/rNN_<paper>/result/runtime.yaml (`bib.verification`; only a person sets `verified`) |
| board | Check | Reports | Check a report | hai-draft-check-agent | hai-draft-review | release or hold | none |
| board | Delivery | Reports | none | none | none | none | none |
| board | Delivery | BibTeX | none | none | none | none | none |
