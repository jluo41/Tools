haipipe-toolkit
===============

A skill-set for **turning runs into trustworthy science**.

```text
⚙️ Engineering                         🔬 Research composition
data → nn → endpoint → individual      Task / Discovery ── Run/Result
                                                  │
accepted Board Pages ── Evidence Workspace ── Supporting/Local Runs
                                     ▼           ▼
                              typed consumer Pages
                                     │
                              Paper / Insight / Design
```

If you are here to **build a model** → the engineering substrate (below).
If you are here to **write a paper** → the research lifecycle (below).
If you want the whole model → **`ARCHITECTURE.md`**. For recipes → **`USAGE.md`**.


The research lifecycle, in one screen
--------------------------------------

The current research stack is Page-first. Task and Discovery execute work as
paired Runs/Results; Evidence Workspaces connect immutable Supporting Runs to
consumer-owned Local Runs; Ideation turns accepted evidence into research
directions; Paper composes accepted Pages.

```
⚙️ EXECUTORS                         📄 CONSUMING PAGE
tasks/<leaf>/                        <page>/<page>.md
  results/                             outline/
  workflow/report.yaml                 outline/  Page Evidence Workspace
discoveries/<leaf>/                    runs/ + results/  paired evidence
  sources.md · verdict.md              bibex/ · display/
  workflow/ (optional)                 latex/ · word/ derived

                         🧷 EVIDENCE
                 source Run ──▶ Supporting Run
            focal Page item ──▶ Local Run/Result
```

**The bank never learns a consumer's stake.** It returns an immutable Run/Result
receipt. The consumer records that full Run id as Supporting evidence and owns
the Local Run/Result that makes its focal item ready.

**The wall is a dispatch rule plus separate Page-local records.** The Page
Evidence Workspace binds exact Supporting Run ids and Local Run/Result receipts;
Task and Discovery never write consumer prose.

The neutral spine is `skills/1_base/project/hai-run/SKILL.md`; its
[`Run catalogue`](skills/1_base/project/hai-run/ref/run-catalog.md) links current domain
profiles, and its references define identity/history and receipt/inventory
rules. Workflow agents, domain owners, workers and presenters use these rules.
Page evidence wiring is
owned by `skills/1_base/draft/workbench-task-draft/`.


Commands
--------

**Research axis:**

```
/hai-draft         a Page Folder, alone or in a Board; the Board checker and
                      the Run CLIs live here (the Board skill retired 261005)

/hai-task         the internal executor — Plan → Build → Execute → Report
/hai-task run <task> [<run>]                 execute/reuse one Run/Result
                      Questions first reuse an exact Result; missing evidence
                      opens the shallowest new Run and returns its receipt.

/hai-discovery    the external executor — Search | Review | Synthesize
/hai-ideation     direction Block → Idea Jobs → evaluation Tasks → linked Paper
/hai-paper        thin academic router over Ideation, Story, Venue,
                      Section, and Round Pages (Roadmap/Narrative retired 260907)
/hai-insight      the evidence side — bounded Runs, evidence dependencies, signed handoff
/hai-design       the creative side — Brief → Commission → Generate → Verify
```

Discovery work is addressed as discoveries → bNN Block → jNN Job → tNN Task
Page → rNN Run. Its Search, Review, and Synthesize skills sit at the family root and are
capabilities, not additional levels: Search finds, Review inspects one
source, and Synthesize combines accepted Results; the vendored originals are parts
(`hai-search/_parts/`, `hai-discovery/_parts/`). The D1 and Page 00–04
workflows are separate axes. See
`skills/2_work/discovery/hai-discovery/ref/bjtr-alignment.md`.

**Engineering axis:**

```
/hai-data         stages 1-4   SourceFn · RecordFn · CaseFn · TfmFn · SplitFn
/hai-nn           stage 5      algo → tuner → instance → modelset
/hai-end          stage 6      Fn-types · endpointset · deploy targets
/hai-individual   stages 0-2 per individual (inference-time data contract)
/hai-project      project container setup:  repo | new | feedback | digest
```

Every umbrella accepts positional args, flexible order, aliases, and free-form
natural language: `/hai-data "build a SourceFn for Dexcom"`.


How skills are organized
-------------------------

**The umbrella pattern.** You memorize the umbrellas. Specialists are real skills
with their own `SKILL.md`, but the umbrella parses your intent and dispatches to
them via `Skill()`. Only entry points get a slash-command; specialists are reached
through their umbrella.

The Paper family now follows a thin-door pattern: `/hai-paper` routes to six
current Page Types and the shared Page workflow. Archived stage skills are not a
second public surface.

**Layers organize skills; folder names identify installer links.** The
`name:` field in `SKILL.md` declares a skill's name, while both root installers
create links from the skill folder's basename. Keep those names aligned when
renaming a skill. Moving the folder between layers preserves its link name.

```
skills/
├── 0_utils/           generic helpers
├── 1_base/            shared foundations
│   ├── project/           Block, Job, Studio, and Run contracts
│   ├── task/              execution and the data → model → endpoint pipeline
│   ├── draft/             Page writing, review, and runtime
│   ├── workbench/         shared screen manuals
│   └── evidence/ display/ draw/ ideation/ search/
├── 2_work/            blueprint/ cowork/ discovery/ knowledge/ work/
└── 3_theme/           design/ insight/ labeling/ paper/
```

Beside `skills/`, the plugin carries its infrastructure at plugin level, none
of it a skill:

```
checks/                scoped validation; run.py calls small modules by responsibility,
                       reusing owning checks (see checks/README.md)
servers/               🌐 everything a browser is served by: _host/ (serve.py, auth,
│                         the `live` namespace), space-home/, workbench/ (including
│                         workbench-task-draft/ and its reader/), and one
│                         workbench-<name>/ per live tab; see servers/README.md
mcp-servers/           🔌 MCP servers (codex-image2)
agents/                🤖 plugin-level agent definitions
```

**Retired content is excluded from installation.** Both root installers skip
folders whose names start with `_`, including `_archive/`, `_old/`, and `_parts/`,
as well as `node_modules/`. Parking retired content there does not install it as
a skill. Deletion is a separate maintenance decision; check remaining references
and preserve existing work before removing anything.


Where to read next
------------------

```
skills/1_base/project/hai-run/SKILL.md  the neutral Level-4 Run/Result contract
skills/1_base/draft/hai-draft-workflow/  the Page workflow: the list of Runs and their routes
skills/README.md         the skill-tree mental model
skills/1_base/draft/hai-draft/agents/README.md   the Page agents, the Board reviewer among them
```


Principles
----------

**Results grow by bounded Runs.** An executor session runs
Plan→Build→Execute→Report (or Discovery Scope→Acquire→Synthesize→Close) and
publishes an immutable Result. Consumers reuse a complete Run by id whenever
possible; missing evidence opens the shallowest new Run.

**One file, one writer.** No file in this system has two writers. That is what lets a
paper session and a task session run weeks apart with zero coordination.

**Status is derived, never asserted.** Every state in the system is an `ls` or a `grep`.
No status is an agent's word for it — agents die, sessions end, files persist.

**Skill-first development.** Make a skill work standalone, then wire it into an umbrella's
keyword table. The `SKILL.md` prompt is the source of truth.
