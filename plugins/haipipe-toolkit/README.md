haipipe-toolkit
===============

A skill-set for **turning runs into trustworthy science**.

```text
⚙️ Engineering                         🔬 Research composition
data → nn → endpoint → individual      Task / Discovery ── QA bank
                                                  │
accepted Board Pages ── Probe/PageX ──┐           │ Probe/QA
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

The current research stack is Page-first. Task and Discovery execute work;
Probe routes evidence into the Page that consumes it; Paper composes accepted
Pages.

```
⚙️ EXECUTORS                         📄 CONSUMING PAGE
tasks/<leaf>/                        <page>/<page>.md
  results/                             outline/
  QA/<n>-<slug>.md                     pagex/   accepted-Page lane
discoveries/<leaf>/                    probe/   Task/Discovery QA lane
  sources.md · verdict.md              bibex/ · display/
  QA/<n>-<slug>.md                     latex/ · word/ derived

                         🃏 PROBE
                 source: page ──▶ PageX
       source: task|discovery ──▶ QA Probe
```

**The bank never learns that probes exist.** No `_ASK/`, no ids, no back-references.
It answers plain questions through its own `qa` verb, and the answer is a file.

**The wall is a dispatch rule plus separate Page-local records.** PageX binds
exact accepted Page files. QA Probe strips consumer stake before a neutral
question reaches Task or Discovery; the executor writes the bank answer.

Depth: `skills/probe/haipipe-probe/SKILL.md` is the constitution.
Design record + the rulings behind it: `Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/`.


Commands
--------

**Research axis:**

```
/haipipe-board        cross-cutting work surface — one topic, Q/S pages,
                      inline discussion, synchronization, and review

/haipipe-task         the internal executor — Plan → Build → Execute → Report
/haipipe-task qa "<question>" [<leaf>]          ← THE QUESTION DOOR
                      One question, GENERAL language (no paper ref, no stake).
                      ① QA scan → ② digest → ③ P-B-E-R → 🚫 refuse.
                      Returns tasks/<leaf>/QA/<n>-<slug>.md.
                      Three callers: a human exploring · the orchestrator
                      itself (self-directed) · a paper's probe DISPATCH.

/haipipe-discovery    the external executor — Search | Review | Idea
/haipipe-discovery qa "<question>" [<leaf>]     ← the symmetric door

/haipipe-probe        evidence router: PageX for accepted Pages; QA Probe for
                      Task/Discovery. The layer never runs bank work itself.

/haipipe-paper        thin academic router over Seed, Venue, Narrative,
                      Section, Round, and Dash Pages
/haipipe-application  the non-academic consumer — same model, venue-gated
```

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
│   ├── haipipe-task/       the 4-stage lifecycle hub + the `qa` verb
│   ├── 1_data/ 2_nn/ 3_end/ 4_individual/    the task-domain families
│   └── agents/             orchestrator · creator · reviewer
│
├── discovery/         🔍 external evidence — Search | Review | Idea + the `qa` verb
├── probe/             🃏 evidence router: PageX + Task/Discovery QA
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
ARCHITECTURE.md          the whole model — the two banks, the probe bridge, the layers
USAGE.md                 recipes: the commands, in the order you actually use them
Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/       the probe design record + every ruling behind it
skills/STRUCTURE.md      the skill-tree mental model
skills/board/README.md   the first-class Board family and its reviewer
skills/probe/haipipe-probe/SKILL.md    the probe constitution (read before touching probes)
```


Principles
----------

**The bank grows on its own.** An executor session runs Plan→Build→Execute→Report for
its own sake — no question pending, no ask. Most probe questions should therefore hit
an answer that *already exists*. Commissioning new work is the exception, not the norm.

**One file, one writer.** No file in this system has two writers. That is what lets a
paper session and a task session run weeks apart with zero coordination.

**Status is derived, never asserted.** Every state in the system is an `ls` or a `grep`.
No status is an agent's word for it — agents die, sessions end, files persist.

**Skill-first development.** Make a skill work standalone, then wire it into an umbrella's
keyword table. The `SKILL.md` prompt is the source of truth.
