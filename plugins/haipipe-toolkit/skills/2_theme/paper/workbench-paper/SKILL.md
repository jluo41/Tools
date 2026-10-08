---
name: workbench-paper
description: >-
  The paper theme of the shared workbench frame: a paper Board, each version and
  each Section open on the frame's tabs Guide · Block · Job ▾ · Task ▾, each with
  the six Spaces (Description · Idea Studio · Audience Report | Work Details |
  Runs · Delivery) and a Runs panel whose buttons are the paper's run cards by
  level and Space. Read-only: it shows the paper's Markdown and copies prompts.
  Trigger: Paper Workbench, paper workbench, paper theme, paper tab, version tab,
  Section tab, paper spaces, /workbench-paper.
metadata:
  version: "0.33.0"
  last_updated: "2026-10-07"
---

# /workbench-paper · the paper theme on the shared frame

**LOAD `workbench` FIRST.** It defines the common Workbench law: STORAGE, SURFACE, WRITER and BOUNDARY, and
the frame every theme shares (`servers/workbench/`, `servers/workbench/README.md`). This skill is the paper's
delta: which views each level's Spaces show, where they read, and which run cards their Runs panels list.

The design is drawn in `Tools/designs/b16_theme_paper/studio/`: s11 (the Board), s12 (a version), s13 (a
Section), s21 (the skills and Runs), s31 (the Guide by level). The paper's folders are
`haipipe-paper/ref/paper-ladder.md`. The four-Space page that came before (`/_board/paper-board`) is retired;
what it showed is kept in [`ref/old-page.md`](ref/old-page.md), since several views below still draw with its
renderers.

## 🔗 The link

```text
<DOMAIN>/_board/workbench?path=<Paper-…>                      the Board (Block tab)
<DOMAIN>/_board/workbench?path=<Paper-…>/<jNN_v<MMDD>_<desk>>  a version (Job tab)
<DOMAIN>/_board/workbench?path=<…>/<jNN_…>/<tNN_<title>>       a Section, the Abstract or a letter (Task tab)
   &space=<Space>&sub=<view>                                   open one Space and view
```

`path` is the folder, relative to the SPACE root; `/w/<paper-board-folder>` lands on the Block tab. `<DOMAIN>`
is the origin the reader uses (the host's `--public-url`); find the listening port before quoting a link, and
never hand a remote reader `127.0.0.1`. Follow the link and read one real value off the page before returning it.

## 🪜 Levels and Spaces

`servers/workbench-paper/paper_theme.py` exports `THEME`: `spaces(level, folder, root, sub)` returns each Space
of a level; anything it leaves out is the frame's vanilla Space. `level_patterns` reads both layouts: a
`jNN_` folder (or an older `Ba-`/`Bb-`/`Bc-` group) is a Job, a `tNN_` folder (or an older `S-…`, `RD<NN>`) a Task.

| Level › Space | Its third-row views | Reads |
|---|---|---|
| Block › Description | Scope · Venue · Resources · Related | `board.md`; `venues/*/call.md`; `## Related resources`; `related/related.md` as cards, each opening on its deep read's drawing |
| Block › Idea Studio | one row per topic | `studio/sNN-<topic>/` (the frame's studio rows) |
| Block › Audience Report | Ideation · Narrative · High-level logic + Low-level work · Related Questions | `board.md ## Questions` by `group:`, their `reports/qNN_`; the current telling's studio topic |
| Block › Work Details | Jobs · Main · Appendix · Evidence | the versions; every Section by part; the Evidence Items |
| Block › Runs · Delivery | (Delivery) LaTeX · Word · Cover letter · Rounds | the Board's `runs/`; the newest version's `delivery/` |
| Job › Description | Version · Venue rules | the version face; its venue's `call.md` |
| Job › Audience Report | Questions · Draft-Main · Draft-Appendix · Comments · Cover letter | the face's `## Questions` and the standing J1–J5; each Section as Question │ Work │ Report with its rendered draft beside its drawing; the comments reports' `## Review Items`; the letter by paragraph |
| Job › Work Details | All · Main · Appendix · Letters | its `t0N_` · `t2N_` · `t3N_` Tasks; the comments reports the letters answer |
| Job › Runs · Delivery | (Delivery) one card per kind: manuscript · letters · checks · sent | the version's `runs/` and `delivery/` |
| Task › every Space | the Page Task's own views (`servers/workbench/task-page`) | the Section folder; the paper adds the reader contract (Scope), its `SUB-*` rows (Requirement), Comments, and "ready for the build" apart from "done" (Delivery) |

**Markdown is the only truth source (JL 260918).** Every view is drawn from the paper's `.md` files (and
authored config, `paper-build.toml`; and receipts, `build-manifest.json`, `runtime.yaml`) on each open; a
Markdown edit is live on reload. The theme stores nothing: no `console/`, no `data.js`.

**Base styles only (JL 261007).** A view uses the classes the frame gives every theme (`servers/workbench/README.md`):
the folding `.topic` row, `.q-row`, `wf-table`, `.st-ok` · `.st-warn`, `.topic.missing`. A view still drawn by the
old page's renderer is wrapped in `pv()`, which scopes that page's stylesheet to it. The reading rules stay: base
type 16px, never under 12px, every table with cell edges, a closed card shows its whole headline.

## ✍️ Writer: the Runs panel

The theme is a read-only projection. **Its only engagement is the Runs panel** of each Space: the buttons are the
run cards of `haipipe-paper-workflow/ref/run-cards.md` whose Space field is that `<Level> › <Space>`, kept for the
open view (`paper_theme._run_cards(level, space, view)`); a Section's buttons are the Page workflow's cards. As
every button of the frame, it is named by the Run it makes (the card's `🏷 RUN` line, `run-<type>-<target>`), its
label in small under it (haipipe-run `ref/run-types-by-space.md`). A button shows its skill and copies its prompt, `{folder}` filled with the open folder; the person runs it in a
Claude or Codex session. Clicking never sends, starts, allocates or writes.

Every Run is `run-<type>-<target>` (no date): a Board's or a version's is a folder in its `runs/` (`run.yaml`, ticket,
`passes/`, the shared Run contract); a Section's is its Page engine ticket. The run types,
with each one's agent, skill and sign, are `ref/workbench-table.md`; `table-workbench --check --cards` keeps the
table and the cards equal.

## 🧭 The Guide

The Guide tab reads `servers/workbench-paper/guide/guide.yaml` (family `paper`): its description, the Workbench
Table (`ref/workbench-table.md`, this skill's), Method (`guide/method.md`, split by level, its cards in
`guide/methods/`, its canvas `guide/methods.excalidraw`, the canvas being the source), RoadMap Draw, and Related
Paper (`servers/workbench-paper/related/papers.md`, `table-papers`).

## 🚦 Gates

The theme shows each gate where it is signed; the named owner closes it, never the screen:

```text
Board    G0 the admitted idea · G1 release of Task work · G2 the claim state and the answer
version  G3 release of one Section (Draft-Main) · G4 submission readiness (Delivery › checks) ·
         G5 every response answered (Comments, the t32_response letter)
```

The theme never infers a human approval from a percentage, a folder's existence, a generated PDF or a
`recorded` row. Gates: `haipipe-paper-workflow`.

## 🚧 Boundary

The theme coordinates the paper; it never becomes the owner of Page prose, Evidence Results, Discovery records,
Task configurations or delivery wording, and no view copies an authority record to make a table easier to draw.
The frame (`servers/workbench/`, `servers/_host/`) belongs to its owner; ask before changing it.

## ✅ Completion checks

- `servers/workbench-paper/tests` and `servers/_host/tests` pass; every paper Board renders at every level.
- Every button of every level's Space is a run card; `render_workbench_table.py ref/workbench-table.md --check
  --cards ../haipipe-paper-workflow/ref/run-cards.md` says PASS.
- No view writes, and none reads a `console/`, `data.js` or other per-paper projection.
