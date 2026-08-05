haipipe-toolkit
===============

A skill-set for **turning runs into trustworthy science**.

Two things live here, and they meet at one point:

```
   ⚙️ THE ENGINEERING SUBSTRATE                  🔬 THE RESEARCH LIFECYCLE
   "how data becomes a model and ships"          "how runs become a paper you can defend"

   1_data → 2_nn → 3_end → 4_individual          task · discovery   (the EXECUTORS — the bank)
   RawData → … → Endpoint stores                        ⇅
   /haipipe-data /haipipe-nn /haipipe-end          probe            (the Q/A map)
   /haipipe-individual /haipipe-project                 ⇅
                                                 paper · application  (the CONSUMERS)
                    │                                              │
                    └──────────────── a task run ──────────────────┘
                       run.sh emits metrics.json; the research layer
                       wraps it with QA digests, probe files, and claims
```

If you are here to **build a model** → the engineering substrate (below).
If you are here to **write a paper** → the research lifecycle (below).
If you want the whole model → **`ARCHITECTURE.md`**. For recipes → **`USAGE.md`**.


The research lifecycle, in one screen
--------------------------------------

Five layers. Two of them execute, two of them consume, and one maps between.

```
   ⚙️ EXECUTORS (the bank — grows on its own)     📄 CONSUMERS (ask the questions)
   ══════════════════════════════════════        ═══════════════════════════════════
   tasks/<leaf>/          code, runs             papers/<P>/         the manuscript
     workflow/plan.yaml   the question             0-lifecycle/      stages × DPRC
     results/             the raw answer           1-probes/         ← the probe files
     QA/<n>-<slug>.md     the READABLE answer      1-claims.md       ← claim status lives here
                                                 applications/<A>/   same model, non-academic
   discoveries/<leaf>/    literature, prior art
     sources.md · verdict.md · landscape.md
     QA/<n>-<slug>.md     the READABLE answer

                    ╲                          ╱
                     ╲   🌉 THE PROBE          ╱
                      ╲  a PAPER-LEVEL file:  ╱
                       papers/<P>/1-probes/PPNN_<topic>.md
                       one file per TOPIC · one SECTION per question
                       binds by PATH:  target: tasks/…/QA/1-cycle.md
```

**The bank never learns that probes exist.** No `_ASK/`, no ids, no back-references.
It answers plain questions through its own `qa` verb, and the answer is a file.

**The wall is a dispatch rule, not a file.** A consumer session never runs bank work
inline — it hands a paper-agnostic `commission:` to a clean-context executor agent,
and the *executor* writes the answer. The stake (`## Why`, H1/H2/C6) never crosses.

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

/haipipe-probe        the probe constitution (anatomy, binding, the two LAWS).
                      A bare question ROUTES to an executor's qa verb — this
                      layer never runs bank work itself.

/haipipe-paper        the academic consumer — stages × DPRC, owns 1-probes/
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

⚠️ The two consumer families are registered inconsistently today: `application`
follows the umbrella pattern strictly (4 slash-commands, 16 specialists dispatched
via `Skill()`), while `paper` exposes 43. Both work. The `paper` surface is simply
wider than the pattern intends.

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
├── probe/             🌉 the constitution + the claim JUDGE (G1/G2/G3)
├── paper/             📄 academic consumer — stages × DPRC
├── application/       📱 non-academic consumer — venue-gated
├── board/             🧭 Board + Page Type/Phase contracts + producer/reviewer/orchestrator
├── diagrams/          🗺 working design Boards; kept outside delivery skills
├── project/           📦 container setup
├── 0_utils/ 0_connect/   utilities and connectors
└── insight/           🪦 RETIRED 2026-07-12 — tombstone only
```

**`_archive/` is not live.** 39 archived `SKILL.md` files sit inside the tree
(mostly under `paper/_archive/`). They are unregistered and never loaded — but they
*do* show up in your greps. Exclude `_archive/` when searching.


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
