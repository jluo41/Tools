HAI-Pipe Toolkit Skill Structure
================================

Status: draft (2026-06-20; probe layer rewritten to the v3 Q/A model 2026-07-14;
        insight layer RETIRED 2026-07-12; Board promoted to a first-class family
        2026-07-26)
Scope: top-level mental model for the skill folder. Read this before grepping the
       tree — 39 of its SKILL.md files are ARCHIVED, not live (see `_archive/` below).
Spec:  the probe layer's contract is `Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/` (approved 2026-07-14).


Core Stack
==========

The core execution model is a stacked sandwich:

```
paper /     composition layer  selects typed Pages and assembles accepted outputs
application                    owns its own audience-specific artifacts
page        durable work       each Page runs OUTLINE/PROBE/EVIDENCE/DRAFT/REVISE/CHECK
probe       evidence router    PageX for accepted Pages; QA crossing for Task/Discovery
discovery   outside evidence   sources, notes, prior art, novelty, verdicts
task        inside execution   code, runs, metrics, reports
```

`discovery` and `task` are sibling EXECUTION layers — the two EXECUTORS. Same
shape, same rules. A probe may point at one or many of either, or a mix. The
probe does not contain them; it points at their artifacts by PATH.


The probe, in six lines
========================

```
Probe is the one evidence-acquisition family for a consuming Page.
Its PageX lane reads exact material from accepted Pages during OUTLINE.
Its QA lane reaches Task or Discovery QA banks during PROBE/EVIDENCE.
The consuming Page owns one local probe/PP<NN>-<slug>/ card per question.
Only the stripped Q-executor crosses; the stake remains consumer-side.
Binding is by PATH: target points at the bank-owned QA file.
```

The bank (`tasks/` + `discoveries/`) is **PROBE-UNAWARE**: no `_ASK/`, no `_ANS/`,
no `answers:` field, no PP id anywhere. It answers plain questions through its own
`qa` verb — `/haipipe-task qa`, `/haipipe-discovery qa` — which returns
`<task-folder>/QA/<n>-<slug>.md`: the executor's READABLE digest, numbered so that
`ls QA/` IS the index.

**The probe CAUSES a QA file; the EXECUTOR AUTHORS it.** A consumer never writes
bank work inline. The shared probe executor sends only Q-executor through the
Task or Discovery owner and returns the exact QA path. Its clean context is the
wall.

Statuses are DERIVED from disk (`planned | commissioned | answered | read |
answered-local | failed`), so the map survives agent death and spans sessions.

The consuming Page raises the question, owns the local card, and decides what
the returned answer means. Paper stays outside that exchange: it composes Pages
and does not own another probe ledger.

Dead words in this layer: **_ASK/ · _ANS/ · answers: · the `asks` verb ·
1-probe-plans/ · 1-probes/**.
(A DISCOVERY's own `verdict.md` — the Review-type terminal file — is a DIFFERENT
thing and it SURVIVES.)


Project Folder Contract
=======================

When the stack runs inside a project, the durable project shape should be:

```
examples/<PROJECT>/
|-- tasks/          inside execution   (owner /haipipe-task)        leaves may carry QA/
|-- discoveries/    outside evidence   (owner /haipipe-discovery)   leaves may carry QA/
|-- papers/         academic delivery  (owner /haipipe-paper)
|-- applications/   other delivery     (owner /haipipe-application-*)
`-- diagram/        project-level story
```

This is what `/haipipe-project` creates and what real projects hold on disk.
Each subfolder's internals belong to its owning skill family; the container owns
only the top level. The link from a consuming Page to the bank is its local
probe card's `target:` — a PATH into a QA file, and nothing else.
The scaffold NEVER mints an `_ASK/` folder. Full picture: `../ARCHITECTURE.md`.


Current Folders
===============

Current top-level folders are the working structure:

```
0_*          utilities and connectors
board        cross-cutting Board skill + read-only reviewer agent
diagrams     working design Boards, kept outside delivery skills
project      project container setup
task         inside-execution layer: lifecycle hub + task-domain families
discovery    outside-evidence layer: Search / Review / Idea
probe        Page evidence router: PageX lane + Task/Discovery QA lane
paper        academic composition over six current Page Types
application  report / message / UI deliverables
```

The `probe` bucket is the logical evidence-acquisition family. Its shared router
selects PageX for accepted Page files or QA Probe for Task/Discovery questions.
The two Page-local surfaces remain physically under `board/page-plugins/` so the
Board registry stays stable. The thin collector under `probe/agents/` serves
only the Task/Discovery QA branch.

The `board` bucket is a first-class cross-cutting family rather than a utility:
`board/haipipe-board/` owns the format, renderer, local service, write-back, and
checks; `board/agents/` owns the read-only fresh-context reviewer. The Board used
to design that package remains at `diagrams/BoardSkillBoard-260722/`, because working
design records and delivery skills have different lifecycles.

There is no top-level `narrative` bucket. Narrative is one Paper Page Type under
`paper/page-types/`; the top-level evidence executor bucket is `discovery`, not
`discover`.

There is no live `insight` bucket either — the insight layer (D/I/K/W cards) was
RETIRED 2026-07-12 (JL); its skills are archived under `insight/_archive/` and
de-registered. `skills/insight/` is a tombstone (README + CHANGELOG + `_archive/`).
Settled evidence now lives where it landed: the general fact in the executor's
`QA/<n>-<slug>.md`, and the consumer interpretation in the owning Page's local
Probe card.

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
`probe/agents/_archive`, `project/_archive`, `insight/_archive` (the whole
retired layer).

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
