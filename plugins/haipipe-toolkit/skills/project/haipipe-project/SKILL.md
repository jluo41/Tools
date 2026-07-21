---
name: haipipe-project
description: "Quick project setup: create the container folders and stop. Two kinds by name: Project-* = repo-backed (gh repo under a user-chosen org, never assumed; submodule at examples/<name>; if the repo already exists, adopt and pull it) and ProjX-* = plain directory under examples/. Owns ONLY the container layout (tasks/ discoveries/ papers/ applications/ diagram/; probes/ retired 2026-07-05 and insights/ retired 2026-07-12 — a paper's evidence questions live in its own 1-probes/ PPNN probe files, and the bank answers them in <task-folder>/QA/<n>-<slug>.md); each subfolder's internals belong to its owning skill family. Task/run scaffolding lives in /haipipe-task. Trigger: new project, project scaffold, repo project, project submodule, /haipipe-project."
argument-hint: "[repo|new|feedback|digest] [Project-Name|args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "3.2.0"
  last_updated: "2026-07-14"
  summary: "Project SETUP only: Project-* repo-backed submodules + ProjX-* plain dirs. Everything else moved out or retired. v3.2 syncs the container contract to the probe v3 model (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/, JL 2026-07-14): a task/discovery LEAF may carry an OPTIONAL QA/ folder (QA/<n>-<slug>.md — the executor's readable digest, numbering IS the index, on BOTH banks); the scaffold NEVER mints _ASK/ or _ANS/ (the bank is PROBE-UNAWARE: no PP ids, no answers: field); a consumer's evidence questions live in papers|applications/<X>/1-probes/PPNN_<topic>/ (renamed from 1-probe-plans/), bound to the bank BY PATH."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-project (project setup)
=======================================

One job: **set up a well-formed project container, QUICKLY.** Setup = folders ready (plus README + .gitignore for the repo kind) and stop. No metadata questionnaire, no diagram authoring, no seed tasks -- those are on-request extras. The name decides the kind:

```
/haipipe-project repo <Project-Name> [--org <owner>]
                                         REPO-BACKED project (fn/repo-project.md)
                                           gh repo create <org>/<name> --private
                                           + submodule at examples/<name>
                                           + scaffold + push + workspace pointer bump
                                           papers inside are submodules OF THE PROJECT
                                           org resolved per invocation (flag or ask;
                                           NO default org -- skill serves many owners)

/haipipe-project new <ProjX-Name>        PLAIN-DIRECTORY project (fn/project.md)
                                           examples/<ProjX-Name>/ container folders (papers/ etc.)

/haipipe-project feedback "<text>"       capture skill feedback (merge-or-create)
/haipipe-project digest [session] [--dry-run]   harvest feedback from a transcript
/haipipe-project                         list projects under examples/ + the two setup paths
```

Not this skill's job (where it lives instead):

```
task-group / task-folder / run scaffolding   -> /haipipe-task   (task/)
eval status scanning (scan-status)           -> /haipipe-task   (task/)
workflow plan/report schema                  -> task/haipipe-workflow
paper folders inside a project               -> /haipipe-paper-lifecycle folder
project audits / reorganization              -> retired; originals in project/_archive
claims / evidence questions                  -> /haipipe-probe (a probe is a
                                                paper-level file, papers/<P>/1-probes/PPNN_<topic>/
                                                -- it owns NO folder in the execution tree)
asking the bank a question                   -> /haipipe-task qa · /haipipe-discovery qa
```

---

Container Layout + Structure Ownership
----------------------------------------

This skill owns ONLY the top-level container. Each subfolder's INTERNAL structure is owned by its skill family; when setup or a question needs the details, CONSULT (infer from) the owner listed below -- never restate its rules here.

```
📦 examples/<name>/   (this skill sets up the container)
   ├── ⚙️ tasks/          owner: /haipipe-task        two-level hierarchy, group letters, task-folder anatomy
   ├── 🔎 discoveries/    owner: /haipipe-discovery   one topic = one folder (Search / Review / Idea types)
   ├── 📄 papers/         owner: /haipipe-paper-*     paper-folder contract (paper wiki); each paper a submodule (legacy projects use singular paper/; do not migrate)
   ├── 📬 applications/   owner: /haipipe-application-*  non-academic deliverables
   └── 🗺️ diagram/        owner: this skill (via /diagram-ascii)  01-story, 02-boundary -- EMPTY at setup, authored on request
```

**The evidence contract, in the three lines this skill must not get wrong** (owner:
`/haipipe-probe`; full detail in `skills/probe/haipipe-probe/SKILL.md`):

```
   ⚙️ THE BANK is PROBE-UNAWARE.  tasks/<task-group>/<task-folder>/ and discoveries/<discovery-group>/<discovery-folder>/ carry NO _ASK/,
      NO _ANS/, NO `answers:` field, NO PP id -- ever. THIS SKILL NEVER MINTS ONE.
      A leaf MAY carry an OPTIONAL QA/ folder: QA/<n>-<slug>.md, the executor's readable
      digest, written by the EXECUTOR at its Report stage. Numbering IS the index.
      Not scaffolded at setup -- it appears when the task-folder has something to say.

   📄 THE CONSUMER holds the questions.  papers|applications/<X>/1-probes/PPNN_<topic>/
      (renamed from 1-probe-plans/ on 2026-07-14). One file per TOPIC, one SECTION per
      question. Created by the consumer's own PROBE phase, never by this skill.

   🔗 THEY BIND BY PATH.  A section's `target:` names a QA file. No id crosses. Nothing
      to renumber, no ledger, no shared namespace.
```

Two refs live here: `ref/project-structure.md` (the top-level container contract only: naming, standard layout, the seven-worlds table + dependency map, project-level diagram/, structure-ownership pointers) and `ref/code-structure.md` (Track A layout + the paired-example rule: every new pipeline Fn or ML model stub gets a paired example task). The tasks/ internals (group folders, task naming, task-folder anatomy, run scripts) live at `task/haipipe-task/ref/task-structure.md`, moved there 2026-07-03.

---

Routing Logic
-------------

```
Step 1: Parse $ARGUMENTS.
Step 2: Resolve verb.
  - "feedback" first token -> fn/feedback.md (resolve BEFORE other parsing)
  - "digest" first token   -> fn/digest.md   (resolve BEFORE other parsing)
  - "repo" or a Project-*  name              -> fn/repo-project.md
  - "new" / "project" or a ProjX-* name      -> fn/project.md
  - task/task-group/task-folder/run verbs    -> tell the user: /haipipe-task
  - review/organize/inventory/overview verbs -> tell the user: retired
                                                (originals in project/_archive)
  - no args -> list examples/ projects (one line each) + the two setup commands
Step 3: Run the fn. Step 4: Present with the return contract tail.
```

Return contract:

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was done
artifacts: [paths created]
next:      suggested next command
```

---

## Feedback

`/haipipe-project feedback "<text>"` captures a complaint / confusion / wish about
the project SKILL, recorded in this skill's `feedback/` folder with the fn named
in the item (e.g. a repo-scaffold gripe -> tagged fn/repo-project); workflow items
route to `task/haipipe-workflow/feedback/`. There is no `skill:` field -- the
folder plus fn tag is the record. `feedback list` aggregates open items;
`feedback move <file> <skill>` re-routes a mis-filed item. Capture is
MERGE-OR-CREATE: a same-topic complaint updates the existing file (appends a
dated recurrence, preserves prior wording verbatim, reopens if fixed) so
inboxes stay self-limiting.

`/haipipe-project digest ["<session-name|id>"] [--dry-run]` is the bulk
harvester: scans a session transcript (CURRENT session, or a named/id'd past
one), distills discrete TOOL/SKILL feedback (dropping one-off instructions,
project-content talk, bare paths), dedups (within-batch + against inbox), and
after a MANDATORY confirm gate routes each item through the SAME capture
(merge-or-create, BATCH mode, no per-item re-confirm). It NEVER auto-files;
`--dry-run` presents the list and stops; global behavioral prefs are FLAGGED
for `/remember`, not filed. Full conventions: `fn/digest.md`.

Routing is CROSS-CUTTING-GUARD-FIRST: a complaint asserting a rule true across
all project operations, or naming a cross-cutting concern (three-level
hierarchy, group letters, paired-example rule, return-contract tail, routing to
/haipipe-task) -> this skill's own inbox, overriding any keyword. Feedback about
how this skill HANDS OFF to /haipipe-task is orchestrator-level, not task-layer.
Full conventions: `fn/feedback.md`; fallback inbox: `feedback/README.md`.

## Behavioral Preferences (portable)

ALWAYS read and honor `PREFERENCES.md` in this skill's own folder: git-tracked
global behavioral preferences (e.g. communicate via ASCII diagrams) that survive
a machine change, unlike the machine-local `~/.claude` auto-memory. Kept in sync
across orchestrators by digest's global-pref fan-out (merge-or-create).
