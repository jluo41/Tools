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
                              Paper / Application
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

The neutral spine is `skills/run/haipipe-run/SKILL.md`; Page evidence wiring is
owned by `skills/board/page-plugins/haipipe-plugin-outline/`.


Commands
--------

**Research axis:**

```
/haipipe-board        cross-cutting work surface — one topic, Q/S pages,
                      inline discussion, synchronization, and review

/haipipe-task         the internal executor — Plan → Build → Execute → Report
/haipipe-task run <task> [<run>]                 execute/reuse one Run/Result
                      Questions first reuse an exact Result; missing evidence
                      opens the shallowest new Run and returns its receipt.

/haipipe-discovery    the external executor — Search | Review | Synthesize
/haipipe-ideation     the semantic bridge — evidence bundle | ideas | Paper handoff
/haipipe-paper        thin academic router over Ideation, Story, Venue,
                      Section, and Round Pages (Roadmap/Narrative retired 260907)
/haipipe-application  the non-academic consumer — same model, venue-gated
```

Discovery work is addressed as discoveries → bNN Block → jNN Job → tNN Task
Page → rNN Run. Its 1_search, 2_review, and 3_synthesize folders are live
capability families, not additional levels: Search finds, Review inspects one
source, and Synthesize combines accepted Results. The D1 and Page 00–04
workflows are separate axes. See
`skills/discovery/haipipe-discovery/ref/bjtr-alignment.md`.

**Engineering axis:**

```
/haipipe-data         stages 1-4   SourceFn · RecordFn · CaseFn · TfmFn · SplitFn
/haipipe-nn           stage 5      algo → tuner → instance → modelset
/haipipe-end          stage 6      Fn-types · endpointset · deploy targets
/haipipe-individual   stages 0-2 per individual (inference-time data contract)
/haipipe-project      project container setup:  repo | new | feedback | digest
```

Every umbrella accepts positional args, flexible order, aliases, and free-form
natural language: `/haipipe-data "build a SourceFn for Dexcom"`.


How skills are organized
-------------------------

**The umbrella pattern.** You memorize the umbrellas. Specialists are real skills
with their own `SKILL.md`, but the umbrella parses your intent and dispatches to
them via `Skill()`. Only entry points get a slash-command; specialists are reached
through their umbrella.

The Paper family now follows a thin-door pattern: `/haipipe-paper` routes to six
current Page Types and the shared Page workflow. Archived stage skills are not a
second public surface.

**Folder names are organization only.** A skill is identified *solely* by the
`name:` field in its `SKILL.md` frontmatter. Moving a folder never renames a skill.

```
skills/
├── task/              ⚙️ internal execution + the engineering substrate
│   ├── haipipe-task/       the 4-stage lifecycle hub + Run/Result receipts
│   ├── 1_data/ 2_nn/ 3_end/ 4_individual/    the task-domain families
│   └── agents/             orchestrator · creator · reviewer
│
├── discovery/         🔍 external evidence — Search | Review | Synthesize + Run/Result
├── ideation/          💡 semantic research directions over Task + Discovery evidence
├── paper/             📄 academic composition over six Page Types
├── application/       📱 non-academic consumer — venue-gated
├── board/             🧭 Board + Page Type/Phase contracts + producer/reviewer/orchestrator
├── diagrams/          🗺 working design Boards; kept outside delivery skills
├── project/           📦 container setup
├── 0_utils/ 0_connect/   utilities and connectors
└── insight/           🪦 RETIRED 2026-07-12 — tombstone only
```

**There is no `_archive/` in this tree, and that is deliberate** (JL 260822:
"我既然把它变成 archive 了，意思就是说要把它们都删掉"). Retiring a skill means
DELETING it. Nine archive roots holding 487 files were removed on 260822; they are
recoverable from git at `438d1c87` and nowhere else. A retired skill that stays on
disk gets read, cited and followed — every archive root here had a live file
pointing into it when it was deleted.


Where to read next
------------------

```
skills/run/haipipe-run/SKILL.md  the neutral Level-4 Run/Result contract
skills/board/page-workflows/     the Page Context → Outline → Evidence → Content → Check loop
skills/STRUCTURE.md      the skill-tree mental model
skills/board/README.md   the first-class Board family and its reviewer
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
