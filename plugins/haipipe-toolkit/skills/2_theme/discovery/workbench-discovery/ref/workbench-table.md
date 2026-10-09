Discovery Workbench Table
=========================

Shape and check: `skills/0_utils/table-workbench/SKILL.md`. One Discovery Block is one
workbench (`/w/<block>`). Rows run input → process → output: Scope states the Block,
its Questions, its links and its drawings; Work finds and reads the papers, one Paper Run
each, and writes each Task's synthesis and the Questions' reports; Check reads every Run
receipt and which citations still need a person; Delivery holds the answered reports and
the Block's BibTeX. Folder is where the run writes: `Block ›` is the Block folder
(`discovery/bNN_<block>/`), `Tools ›` the workbench's server folder (`servers/workbench-discovery/`); `none` writes no file,
only a verdict.

Agents are the Discovery family's own (`skills/2_theme/discovery/agents/`): the orchestrator
routes, the creator writes Task Pages, Runs, Results and synthesis, the search worker
returns candidates only, and the reviewer judges what the creator made, never its own.
Reports are Pages: `haipipe-page-writing-agent` writes, `haipipe-page-check-agent` checks.

| Level | Space | View | Run type | Agent | Skill | Person signs | Folder |
|---|---|---|---|---|---|---|---|
| board | Guide | Description | none | none | none | none | none |
| board | Guide | Method | none | none | none | none | none |
| board | Guide | RoadMap Draw | none | none | none | none | none |
| board | Guide | Related Paper | Add a paper | haipipe-discovery-orchestrator-agent | haipipe-discovery | the source check | Tools › related/papers.md |
| board | Scope | Block | none | none | none | none | none |
| board | Scope | Questions | Ask a Question | haipipe-discovery-creator-agent | haipipe-question-asking | the question | Block › board.md (Questions) · reports/qNN_<topic>/ |
| board | Scope | Questions | Review the questions | haipipe-discovery-reviewer-agent | haipipe-question-review | a change | none |
| board | Scope | Resources | Add a resource | haipipe-discovery-creator-agent | haipipe-question | none | Block › board.md (Related resources) |
| board | Scope | RoadMap Draw | Draw | haipipe-discovery-creator-agent | workbench-studio | none | Block › studio/<name>.excalidraw |
| board | Work | Papers | Find papers | haipipe-discovery-search-worker-agent | haipipe-discovery-search | none | none |
| board | Work | Papers | Read a paper | haipipe-discovery-creator-agent | haipipe-discovery-review | none | Block › jNN_<job>/tNN_<task>/runs/rNN_<paper>.sh · results/rNN_<paper>/ |
| board | Work | Tasks | Synthesize a Task | haipipe-discovery-creator-agent | haipipe-discovery-synthesize | none | Block › jNN_<job>/tNN_<task>/summary.md |
| board | Work | Questions | Write the report | haipipe-page-writing-agent | haipipe-page-writing | none | Block › reports/qNN_<topic>/ |
| board | Check | Runs | Review a Run | haipipe-discovery-reviewer-agent | haipipe-discovery-review | none | none |
| board | Check | Citations | Verify a citation | haipipe-discovery-reviewer-agent | haipipe-discovery-search | the citation | Block › jNN_<job>/tNN_<task>/results/rNN_<paper>/rNN_<paper>.bib |
| board | Check | Reports | Check a report | haipipe-page-check-agent | haipipe-page-check | release or hold | none |
| board | Delivery | Reports | none | none | none | none | none |
| board | Delivery | BibTeX | none | none | none | none | none |
