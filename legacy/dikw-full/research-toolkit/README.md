# research-toolkit

Personal research-toolkit plugin for Claude Code. Unifies ARIS, Nature-Paper-Skills,
UTD24 IS-journal playbooks, excalidraw-diagram, and custom skills under a single
phase-numbered `skills/` tree.

Read `PRINCIPLES.md` for the ideology (what governs which phase) and `WORKFLOW.md`
for the curated stacks (journal / conference / IS / patent) and routing rules.

===========================================================================
Layout -- skills are numbered by research-workflow phase
===========================================================================

```
research-toolkit/
├── skills/
│   ├── _workflows/    -- cross-phase orchestrators (entry points): research-pipeline,
│   │                     paper-writing, paper-workflow, idea-discovery,
│   │                     idea-discovery-robot, experiment-bridge, rebuttal,
│   │                     patent-pipeline, is-paper-workflow
│   ├── 00_meta/       -- cross-cutting utilities, codex mirrors, shared refs
│   ├── 01_discover/   -- lit search, paper analysis, idea generation, novelty
│   ├── 02_plan/       -- method refinement, experiment planning, derivations
│   ├── 03_execute/    -- running experiments (local, modal, vast.ai), monitoring
│   ├── 04_analyze/    -- results -> claims
│   ├── 05_prewrite/   -- bootstrap, outline, architecture, incubation
│   ├── 06_write/      -- active drafting (scientific-writing, paper-write, ...)
│   ├── 07_revise/     -- structural revision (manuscript-optimizer, paper-revise)
│   ├── 08_postwrite/  -- compile, auto-paper-improvement-loop
│   ├── 09_figures/    -- figure planning, rendering, diagrams (excalidraw, mermaid)
│   ├── 10_review/     -- auto review loops, audits, citation verification
│   ├── 11_respond/    -- rebuttal-response, paper-rebuttal
│   ├── 12_present/    -- slides, posters, talks
│   └── 13_venue/      -- venue playbooks (Nature, PNAS, ISR, MISQ, MS, patents, grants)
├── mcp-servers/       -- MCP servers from ARIS
├── templates/         -- Templates from ARIS
├── tools/             -- Tools from ARIS
├── docs/              -- Docs from ARIS
└── AGENT_GUIDE.md
```

`_workflows/` (underscore prefix) sorts first and holds the entry-point orchestrators -- the skills you typically invoke first. Atomic skills live under their phase folder. Numbered prefixes sort `ls` in workflow order. `00_meta` holds cross-cutting skills plus the ARIS `skills-codex*` mirrors (alternate skill copies for non-Claude runtimes).

===========================================================================
Attribution
===========================================================================

- **ARIS** (71 skills + `mcp-servers/`, `templates/`, `tools/`, `docs/`, `AGENT_GUIDE.md`):
  https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep -- see `LICENSE.aris`
- **Nature-Paper-Skills** (17 skills, originally core/research/review/venue/optional):
  https://github.com/Boom5426/Nature-Paper-Skills -- see `LICENSE.nature`
- **UTD24 IS-journal playbooks** (`13_venue/{isr,misq,ms-is}-playbook`, `is-paper-workflow`):
  from Tools/plugins/utd24-paper-skills
- **excalidraw-diagram** (`09_figures/excalidraw-diagram`):
  https://github.com/coleam00/excalidraw-diagram-skill
- **Custom**: `coding-by-logging`, `cc-archive`, `cc-session-summary`,
  `notebook-cell-python`, `evaluation-display-skill`, `paper-architecture`,
  `paper-incubator`, `paper-rebuttal`, `paper-revise`.

===========================================================================
Updating upstream content
===========================================================================

No automatic sync. To refresh from an upstream, `rsync` the source tree into the
matching phase folders and commit the delta with a clear message
(e.g. `sync(aris): pull upstream @ <sha>`).
