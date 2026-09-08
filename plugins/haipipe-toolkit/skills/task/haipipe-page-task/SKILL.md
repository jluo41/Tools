---
name: haipipe-page-task
description: >-
  Reader-facing companion for executable Task Pages (folder-kind: task):
  turns run-backed results into an evidence-rich technical page with a
  deliberate mix of data tables, result figures, and method diagrams. Use
  when creating, outlining, writing, reviewing, or delivering a Task Page;
  not for P-B-E-R execution or raw-data analysis.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.1.1"
  last_updated: "2026-09-08"
  parent: haipipe-task
  scope: Task Page Face
---

# /haipipe-page-task · the executable Task Page as a small paper

This is the Page-side companion to haipipe-task. haipipe-task remains the
canonical owner of the Task Folder, Plan → Build → Execute → Report, Run
receipts, and Folder closure. This skill owns the reader-facing extension:
what a Task Page must show so a reader can inspect the evidence without
reconstructing the scripts.

Load this skill together with haipipe-page, haipipe-task,
haipipe-task/ref/task-page.md, the current Page workflow phase, and the
display contracts. It does not replace any of those authorities and it never
executes a producing Task merely to make a Page look complete.

## ⚡ Core ruling · a numeric Task Page is not prose-only

The user-facing rule is visual evidence density: Task Pages should show more
than paragraphs. A data-bearing or empirical Task Page must carry a DISPLAY
plan in SHAPE and normally include all three kinds of reader aid:

- one exact-audit table for inputs, counts, reconciliation, or status;
- one figure for a distribution, comparison, funnel, trajectory, or other
  relationship that is easier to see than to read in a sentence;
- one method, provenance, or decision-boundary diagram.

Each Data or Result division carries at least one substantive table or figure.
Each Method or boundary division carries a diagram when a process, ownership,
or gate is part of its argument. A multi-source or multi-stage Task Page
usually needs four or more distinct display units. Do not repeat one chart
under several headings to satisfy the count.

The only exception is a genuinely non-numeric page with no useful visual
encoding. The outline must record DISPLAY: none and the reason; lack of time,
missing authoring, or a preference for prose is not a valid reason. A fenced
ASCII flow line is a useful draft map, but it does not satisfy the final
display requirement by itself.

For a worklist or coverage Task, the normal display inventory is:

1. source and selection funnel;
2. source-tier or field-composition table/figure;
3. exact expected-versus-observed and terminal-status display;
4. provenance/matching/release-boundary diagram;
5. hash, duplicate, or residual table when those facts affect the reading.

The inventory is adapted to the Task's actual question and Results. It is
never permission to invent a count or to draw a decorative chart.

## 🧭 Display choice · match the visual to the reader move

Use a table when the reader must quote exact values, reconcile rows, inspect
nulls, or compare named categories. Use a figure when the reader must see
relative size, distribution, trend, funnel loss, or status composition. Use a
diagram when the reader must understand a sequence, provenance edge, inferred
join, ownership boundary, or release gate.

Every display has one reader job. Its caption states the finding or question,
scope, source Run, and the important caveat. Use grayscale-readable,
colorblind-safe encoding, with position, shape, labels, or weight carrying
the contrast. Do not bake a title into the asset; the caller owns caption,
label, and placement.

## 🧱 Plan first · DISPLAY is a typed Evidence Item

During SHAPE, inventory displays before writing the prose:

- create one typed E<NN>-DISPLAY-<slug> item per distinct table, figure, or
  diagram;
- give each item one owning C<n>.P<m>.B<k> Target, a concrete Need, an
  expected ready payload, and observable Acceptance checks;
- use Serves only for additional reader moves performed by the same placed
  display; those Bullets still keep their own evidence decisions;
- place the display next to the paragraph that interprets it and name its
  DisplayN id in that sentence so the Board can show an evidence chip.

The Outline table is a plan/evidence map, not a data display. A two-row
READING table is a ruling table, not a substitute for the Task's result
tables. The plan must make the substantive displays visible before CONTENT
claims that the Page is complete.

## 📦 Unit contract · one display is one inspectable folder

Every Page display unit lives at:

    <task>/outline/evidence/display/<stem>-Display<N>-<slug>/

Use the shared display-unit-output-contract and display-intake-contract. A new
unit normally contains:

    README.md
    intake/manifest.yaml
    intake/inputs/          small approved display-safe extracts
    recipe/                 renderer recipe or FigureSpec
    assets/                 winning table/figure/diagram asset
    float.tex
    preview.tex
    preview.pdf

The renderer is selected through haipipe-display:

- haipipe-display-table for exact typeset tables;
- haipipe-display-figure for numeric plots;
- haipipe-display-diagram for deterministic editable SVG diagrams;
- haipipe-display-tex for hand-authored TeX-native diagrams or equations.

Do not create a flat figures/ or tables/ folder and do not leave a loose PNG
or PDF as the Page's only display record. The unit README names its DISPLAY
item, serves target, caption job, source Result, and human accepted: decision.

## 🔒 Numeric provenance · a visual cannot become a second data store

Numbers in a table, figure, or counted diagram arrive through the Page's
approved Evidence graph:

    producing Task Result
      → haipipe-task-for-page page-service values.yaml
      → Evidence Item Local Input
      → display/intake/ snapshot
      → renderer recipe
      → assets/ and preview.pdf

The renderer reads only the frozen intake snapshot. It never searches raw
Results, chooses rows from an arbitrary CSV, or types a number into float.tex.
The intake manifest records the producing holder, full Run id, canonical
artifact, provenance, and matching hashes. A changed source reopens the
display and its acceptance; it never gets silently patched in place.

Concept diagrams may have no numeric input, but any real count printed inside
one still requires a values source. A visual that says “all” or “complete”
must bind to the same exact coverage Result that supports that word.

## 🔁 Page workflow

1. CONTEXT/PREPARE resolves the Task question, Results, target audience,
   display-safe boundary, and any related Page.
2. OUTLINE/SHAPE creates the display inventory and typed DISPLAY Items. It
   checks the table/figure/diagram baseline before prose is drafted.
3. OUTLINE/SURVEY plans the Supporting and local Run routes without executing
   them. EVIDENCE/LAND validates Supporting Results, freezes Local Input, and
   admits the local display Result; EVIDENCE/EMBED folds it into the plan.
   A unit may be rendered as a candidate while its human accepted: gate remains open.
4. CONTENT/WRITE places each display beside the paragraph that explains it,
   cites DisplayN, writes the caption, and keeps prose numbers aligned with
   the same Run and intake.
5. Build inside CONTENT/WRITE regenerates every declared preview.pdf and the one-Page PDF.
   The Page-level PDF must contain the winning floats, not only references to
   them.
6. CHECK inspects the rendered Board Displays segment, each preview, the
   Page-level PDF, source/Run trace, grayscale readability, and the human
   accepted: gate. Missing or stale display units route back to OUTLINE,
   EVIDENCE, or CONTENT; they do not become a silent warning.

The reader-facing completion packet therefore includes the verified Board
Page, one current preview.pdf for every declared display unit, and the
current Page-level PDF. If a display is declared but not rendered, the packet
names it as missing instead of returning an older preview.

## ✅ Definition of done

- the Page's SHAPE plan contains a display inventory, not only prose bullets;
- every Data/Result division has the table or figure its reader move needs;
- the Page has the method/provenance/boundary diagram its argument needs;
- every display has one DISPLAY Evidence Item and a resolvable Local Input or
  an explicit concept-only contract;
- every numeric element traces to a full Run and matching intake snapshot;
- every unit has a caption, label, recipe, winning asset, and current preview;
- the Board Displays segment shows the displays at the top of each card;
- the Page-level PDF embeds those displays and the prose cites them;
- no display is treated as a face-positive, duplicate-free, or release-ready
  claim unless the governing Result and acceptance checks say so.

## 🚧 Boundaries

- Do not execute, rerun, or repair the producing Task from this Page skill.
- Do not bypass haipipe-task-for-page for numeric Page evidence.
- Do not convert a VALUE Item into a DISPLAY Item by implication; create the
  typed DISPLAY contract and its own Result.
- Do not tick approved:, accepted:, Decide, or a human READING ruling.
- Do not claim NPI2Photo, canonical integration, or any other release state
  merely because a display rendered or a coverage table reconciled.

## 📂 Governing references

- haipipe-page/SKILL.md · shared Page Face and reader-facing packet
- haipipe-task/ref/task-page.md · Task Page grammar and READING closure
- haipipe-task/ref/task-page-template.md · new Task Page shape
- haipipe-plugin-outline/ref/plan-grammar.md · typed DISPLAY planning
- haipipe-plugin-outline/ref/item-table.md · DISPLAY Result envelope
- haipipe-plugin-outline/ref/evidence/displays.md · Page display lane and chip
- haipipe-display/SKILL.md · renderer routing
- display/ref/display-unit-output-contract.md · unit files and invariants
- display/ref/display-intake-contract.md · approved numeric intake
