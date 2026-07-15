HAI-Pipe Toolkit Skill Structure
================================

Status: draft (2026-06-20; probe layer rewritten to the v3 Q/A model 2026-07-14;
        insight layer RETIRED 2026-07-12)
Scope: top-level mental model for the skill folder. Read this before grepping the
       tree — 39 of its SKILL.md files are ARCHIVED, not live (see `_archive/` below).
Spec:  the probe layer's contract is `Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/` (approved 2026-07-14).


Core Stack
==========

The core execution model is a stacked sandwich:

```
paper /     delivery layer     decides what the project needs to say; each stage
application                    runs DPRC (Draft/Probe/Revise/Check)
probe       the paper's        a PAPER-LEVEL Q/A map: collects the questions DRAFT
            Q/A map            raised, matches them against the bank, commissions
                               what is missing, interprets what comes back
discovery   outside evidence   sources, notes, prior art, novelty, verdicts
task        inside execution   code, runs, metrics, reports
```

`discovery` and `task` are sibling EXECUTION layers — the two EXECUTORS. Same
shape, same rules. A probe may point at one or many of either, or a mix. The
probe does not contain them; it points at their artifacts by PATH.


The probe, in five lines
========================

```
A PROBE IS A PAPER-LEVEL DOCUMENT. Nothing else.
    papers/<P>/1-probes/PPNN_<topic>.md    ·    applications/<A>/1-probes/PPNN_<topic>.md
One file per TOPIC; each question is one SECTION: serves / target / state / commission / reading.
Plus one '## Why' per file — the STAKE. It NEVER leaves the file.
Binding is by PATH, never by id: `target:` points at a QA file in the bank.
```

The bank (`tasks/` + `discoveries/`) is **PROBE-UNAWARE**: no `_ASK/`, no `_ANS/`,
no `answers:` field, no PP id anywhere. It answers plain questions through its own
`qa` verb — `/haipipe-task qa`, `/haipipe-discovery qa` — which returns
`<leaf>/QA/<n>-<slug>.md`: the executor's READABLE digest, numbered so that
`ls QA/` IS the index.

**The probe CAUSES a QA file; the EXECUTOR AUTHORS it.** A consumer session never
executes bank work inline (LAW 1) — it hands the `commission` block, verbatim, to
`Agent(haipipe-task-orchestrator-agent)` or
`Agent(haipipe-discovery-orchestrator-agent)`, and their clean context is the wall.
There is NO probe gateway agent (retired 2026-07-14).

Statuses are DERIVED from disk (`planned | commissioned | answered | read |
answered-local | failed`), so the map survives agent death and spans sessions.

The DELIVERY layer (paper / application) is the outer sandwich and the control
envelope. Its stages raise the questions, hold the probe files, read the returned
QA files, and decide whether the story is ready to ship. Narrative is one of its
STAGES, not a layer of its own.

Dead words in this layer: **card · row · table · stub · _ASK/ · _ANS/ · answers: ·
the `asks` verb · Takeaways · Verdict · verdicted · 1-probe-plans/**.
(A DISCOVERY's own `verdict.md` — the Review-type terminal file — is a DIFFERENT
thing and it SURVIVES.)


Project Folder Contract
=======================

When the stack runs inside a project, the durable project shape should be:

```
examples/<PROJECT>/
|-- tasks/          inside execution   (owner /haipipe-task)        leaves may carry QA/
|-- discoveries/    outside evidence   (owner /haipipe-discovery)   leaves may carry QA/
|-- papers/         academic delivery  (owner /haipipe-paper-*)     each holds 1-probes/
|-- applications/   other delivery     (owner /haipipe-application-*) each holds 1-probes/
`-- diagram/        project-level story
```

This is what `/haipipe-project` creates and what real projects hold on disk.
Each subfolder's internals belong to its owning skill family; the container owns
only the top level. The link between the KB (tasks/ + discoveries/) and a delivery
folder is the probe file's `target:` — a PATH into a QA file, and nothing else.
The scaffold NEVER mints an `_ASK/` folder. Full picture: `../ARCHITECTURE.md`.


Current Folders
===============

Current top-level folders are the working structure:

```
0_*          utilities, connectors, venue playbooks
project      project container setup
task         inside-execution layer: lifecycle hub + task-domain families
discovery    outside-evidence layer: Search / Review / Idea
probe        the paper-side Q/A map: the constitution + the claim-judging skill
paper        academic deliverables (stages × DPRC phases)
application  report / message / UI deliverables
```

The `probe` bucket holds NO folder in the execution tree and no live gateway. It
holds two skills — `haipipe-probe` (the constitution: probe-file anatomy, path
binding, the QA/ contract, the qa verb, the five-step loop, the cost ladder, the
two LAWS, status derivation, the writer table) and `haipipe-probe-review` (the
G1/G2/G3 claim-judging rulebook) — plus one live agent,
`haipipe-probe-reviewer-agent`.

There is no `narrative` bucket — narrative is a paper STAGE
(`paper/1-lifecycle/3-narrative/`), not a layer. The bucket is `discovery`,
not `discover`.

There is no live `insight` bucket either — the insight layer (D/I/K/W cards) was
RETIRED 2026-07-12 (JL); its skills are archived under `insight/_archive/` and
de-registered. `skills/insight/` is a tombstone (README + CHANGELOG + `_archive/`).
Settled evidence now lives where it landed: the general FACT in the executor's
`QA/<n>-<slug>.md`, the paper-specific JUDGMENT in that paper's own `1-claims.md`.

`1_data`, `2_nn`, `3_end`, and `4_individual` live inside `task/` as
task-domain families. They are still independent user-facing umbrellas by
skill name, but their folder home now reflects that they are all execution
domains under the task layer.

```
task/1_data        data task family
task/2_nn          model/algorithm task family
task/3_end         endpoint/deployment task family
task/4_individual  individual/inference task family
```

Keep skill `name:` values stable. Folder movement changes paths only; commands
such as `/haipipe-data`, `/haipipe-nn`, `/haipipe-end`, and
`/haipipe-individual` remain unchanged.


`_archive/` — 39 dead SKILL.md files live INSIDE this tree
==========================================================

Not every `SKILL.md` under `skills/` is a skill. **155 are live; 39 are archived.**
An archived skill sits under an `_archive/` directory, is DE-REGISTERED (no plugin
entry, not invocable), and is kept only so a decision can be traced back.

```
skills/**/_archive/**/SKILL.md     💀 NOT a skill. History. Do not follow it,
                                      do not repair it, do not resurrect it.
                                   ⚠️ it DOES answer a grep — that is the trap.
```

Live archive roots: `application/_archive`, `paper/_archive`,
`paper/3-build-submit/haipipe-paper-folder/_archive`, `probe/agents/_archive`,
`project/_archive`, `insight/_archive` (the whole retired layer).

So: **exclude `_archive/` from every sweep** unless you are deliberately reading
history — `grep -r ... --exclude-dir=_archive`. A hit inside `_archive/` is never
a bug. The same courtesy applies to `CHANGELOG.md` files and dated `feedback/`
records: they are ALLOWED to name dead machinery, because naming what died is
their job.


Skill Identity And Refresh
==========================

Folder names are organization only. A skill is identified by the `name:` field
inside its `SKILL.md` frontmatter.

After a folder rename, an already-running Codex session may still show the old
path in its cached skill list. Start a fresh session or reload the plugin index
to see the new folder paths. Do not rename skill `name:` values just to match
folder names.


Where the whole picture lives
=============================

`../ARCHITECTURE.md` — the top-level model: the KB ⇄ delivery double arrow, the
probe as a paper-level Q/A map, the probe-unaware bank + its QA/ folders, the qa
verb, the two session modes, the two LAWS, the layer table, and the real project
layout on disk. Read it before making structural changes here.
`Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/` — the spec of record (rulings R1-R18, approved 2026-07-14).
