# Changelog

## 0.4.0 · 2026-10-03

- Three working Spaces in the shared shell: Scope (Block · Questions · Resources), Task
  (Questions · Studio) and Check (Runs · Tasks · Reports), each Space's Views and content in
  one box, with the shared Runs panel on the right built from `ref/workbench-table.md`.
- The Workbench Table gains the full Task lifecycle (plan, review, build, code review, run,
  report) and report planning, after an independent review; planned skills marked `(new)`.
- `task` leaves the conformance test's RUNS_GAPS.
- The page uses the shared shell exactly as Insight, Design and Shared draw it: 📋 title with
  all boards · board index, the Block band, the Space row, `wtab` View tabs inside one box,
  Insight's colors and tab sizes; the bespoke heading, search and refresh controls are gone.
- Scope › Resources lists the _WorkSpace folders each Job declares and the Block's
  ProjectResult folder, read-only: data files named and sized, the rest in the pop-out.

## 0.3.0 · 2026-10-03

- Guide meets the shared workbench rules: a Description and a five-step Method in the
  `task` registry entry; the Workbench Table `ref/workbench-table.md` (Scope · Task ·
  Check); the Related Paper table `ref/task-papers.md` (14 papers, checked online); and a
  generated "Workbench design" drawing, `servers/workbench-task/studio/task-workbench-design.py`,
  replacing the earlier four-View design. `task` leaves the conformance test's GAPS.

## 0.2.2 · 2026-10-03

- Work follows Insight's Task Work: one light Block → Job → Task → Run tree per
  Question, each level once, Runs folded, no status.
- Report shows only the title and the Opening's first paragraph; the title opens
  the report in the same pop-out as a Run. Status stays in Progress.

## 0.2.1 · 2026-10-02

- Share Paper's Work row markup and CSS: type pill, short name, explanation,
  shared-Question tags and counts; reveal the indented native tree on expansion.
- Open a selected Run's exact Result in a pop-out. Preserve native store
  resolution, and keep Task navigation and audit details inside their fold.

## 0.2.0 · 2026-10-02

- Task Space now has Task, Roadmap Studio, Related Paper and Progress; each
  Question has side-by-side Logic / Work / Report columns.
- Reports are ordinary Block-owned Pages under `reports/`. The register and
  reports supply one snapshot for Question cards and Progress.
- Add freeform drawing rows, resource authoring, session context and source
  warnings while preserving native Task and Page ownership.

## 0.1.0 · 2026-10-02

- Introduce the read-only Task Block Workbench contract: Progress, Runs and
  Scope, using existing Job/Task folders and Ticket/Result records.
