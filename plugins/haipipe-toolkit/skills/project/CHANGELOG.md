## [3.2.0] — 2026-07-14 — container contract synced to the probe v3 Q/A model

Spec of record: `Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/` (APPROVED JL 2026-07-14, R1-R18); operative form
`../probe/haipipe-probe/SKILL.md` v8.0.0. `/haipipe-project` scaffolds no probe machinery — but it
is the thing that MINTS FOLDERS, so the prohibition is restated here as a scaffolding rule.

- **`SKILL.md` (3.1.0 → 3.2.0):** frontmatter `description` + `summary` rewritten off the v3 model.
  New "The evidence contract, in the three lines this skill must not get wrong" block in the
  Container Layout section: the bank is PROBE-UNAWARE; a leaf MAY carry an OPTIONAL `QA/` folder
  (`QA/<n>-<slug>.md`, executor-written at Report, numbering IS the index, on BOTH banks, NOT
  scaffolded at setup); the consumer's questions live in `1-probes/PPNN_<topic>.md`; they bind BY
  PATH. Not-this-skill's-job table: the stale "/haipipe-probe (gateway layer doc; folderless —
  _PROBE cards live consumer-side)" line replaced with the probe-constitution pointer + a new row
  routing "asking the bank a question" to `/haipipe-task qa` · `/haipipe-discovery qa`.
- **`ref/project-structure.md`:** new **Evidence Contract** section — the hard prohibition
  (**THIS SKILL NEVER MINTS `_ASK/`**, no `_ANS/`, no `answers:`, no PP id under `tasks/` or
  `discoveries/`) plus the leaf diagram showing the optional `QA/` folder on both banks. The
  one-way dependency map re-expressed as a PATH binding (`target: <leaf>/QA/<n>-<slug>.md`) rather
  than "the probe bridge / 1-probe-plans PPNN cards". The insights/-retirement note corrected: a K
  card's content now splits into the executor's QA file (the general FACT) and the paper's own
  `1-claims.md` (the paper-specific JUDGMENT) — not into a "PPNN card ## Verdict", which no longer
  exists.
- **DEAD, do not resurrect:** `_ASK/` · `_ANS/` · `answers:` · `1-probe-plans/` (→ `1-probes/`) ·
  the gateway agent · "card" as the name of a probe file · "Verdict"/"verdicted". ⚠️ A DISCOVERY's
  own `verdict.md` (Review-type terminal file) is a DIFFERENT thing and SURVIVES.


## [3.1.0] — 2026-07-12 — insights/ removed from the container layout

JL insight-retirement ruling. `/haipipe-project` no longer mints an `insights/` folder: the container is `tasks/ discoveries/ diagram/` (+ `papers/`, `applications/` optional).
- `ref/project-structure.md`: "The Seven Worlds" → "The Five Worlds"; the one-way dependency map rewritten around the probe bridge (papers/applications READ tasks+discoveries THROUGH the bridge); the insights/ ownership row deleted.
- Legacy `insights/` folders in existing projects are DEAD HISTORY — never read, never written, NEVER deleted.

project — Changelog
=====================

Layer-scoped changelog for the project (project umbrella) layer. Newest first.
Rollup lives in the plugin-level `CHANGELOG.md`.


## [Unreleased] - 2026-07-03

### Changed
- **`ref/project-structure.md` rewritten to the ownership principle** (583 -> ~115 lines). It now carries ONLY the top-level container: ProjX-*/Project-* naming, the standard layout (adds `discoveries/`; `papers/` plural for new scaffolds, legacy ProjA-D keep singular `paper/`), the seven-worlds table + one-way dependency map, the project-level `diagram/` contract, the `_WorkSpace` note, and a Structure Ownership pointer table.
- **tasks/ internals moved** to `task/haipipe-task/ref/task-structure.md`: group folders, task naming, task-folder contents, skill-runner exemption, group/task `diagram/` contracts, run script templates, the runs/results/notebooks/sbatch relationship, and the auto-example rule. Rules already covered by `task/haipipe-task/ref/authoring-conventions.md` (four-sister naming §1, heavy-artifact rule §3, notebook retention/commit policy §7) stay there as authority; task-structure.md only points at them.
- **Review Checklist archived** to `project/_archive/review-checklist.md` (it belonged to the retired review fn; originals in `_archive/haipipe-project-inspect/`).
- **probes/ / insights/ / applications/ / paper internals dropped** from project-structure.md; the ownership table points to each world's schema authority (probe-yaml-schema.md, insight-md-schema.md, application ref/, paper wiki + haipipe-paper-folder, discovery SKILL.md folder contract).


## [Unreleased] — 2026-05-31

### Changed
- **`ref/project-structure.md` notebooks/ rules** aligned with the new task notebook policy:
  - documented the `_meta.notebook: full | thin | off` retention knob (run.sh applies it; cross-ref to `task/haipipe-task/ref/authoring-conventions.md §7`);
  - commit policy now **defaults to gitignoring `notebooks/` and `_WorkSpace/`** (N×seeds×arms recorded notebooks bloat the repo); commit a rendered notebook only when collaborators benefit. The project scaffold should seed `.gitignore` with `notebooks/` and `_WorkSpace/`.
