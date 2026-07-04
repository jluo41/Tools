haipipe-project
===============

Quick project setup: create the container folders and stop. Two kinds by name; everything else (task scaffolding, audits, summaries) moved out or retired.

---

Commands
--------

  /haipipe-project repo <Project-Name> [--org <owner>]
      REPO-BACKED project: gh repo under a user-chosen org (never assumed) +
      submodule at examples/<name> + scaffold + push + workspace pointer bump.
      If the repo already exists, ADOPT: skip create, submodule add pulls it.
      Recipe: fn/repo-project.md. Papers inside are submodules OF THE PROJECT.

  /haipipe-project new <ProjX-Name>
      PLAIN-DIRECTORY project under examples/. Recipe: fn/project.md.

  /haipipe-project feedback "<text>"       capture skill feedback (merge-or-create)
  /haipipe-project digest [session] [--dry-run]   harvest feedback from a transcript
  /haipipe-project                         list projects + the two setup paths

Setup is QUICK by default: folders ready (plus README + .gitignore for the repo kind), then stop. No metadata questionnaire, no diagram authoring, no seed tasks. Retired verbs (task/overview/review/summarize/organize) live in project/_archive/.

---

Container Layout
-----------------

  examples/<name>/
  +-- tasks/          owner: /haipipe-task
  +-- probes/         owner: /haipipe-probe
  +-- discoveries/    owner: /haipipe-discovery
  +-- insights/       owner: /haipipe-insight
  +-- papers/         owner: /haipipe-paper-*  (each paper a submodule; legacy projects use singular paper/)
  +-- diagram/        owner: this skill via /diagram-ascii (EMPTY at setup, authored on request)

Forbidden at top level: docs/, cc-archive/, _old/, configs/, results/ (plain-dir kind also forbids README.md).

---

Skill Files
------------

  SKILL.md                    Router and dispatch table
  fn/repo-project.md          Repo-backed setup (preflight, ADOPT mode, scaffold, double-bump)
  fn/project.md               Plain-directory setup (3 steps + on-request extras)
  fn/feedback.md, fn/digest.md  Feedback capture + session harvest
  ref/project-structure.md    Top-level container contract only (tasks/ internals: task/haipipe-task/ref/task-structure.md)
  ref/code-structure.md       Track A layout + paired-example rule
  CHANGELOG.md                Version history
