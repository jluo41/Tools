# Where do venues, related papers and the built paper live?
state: 🟡 DRAFT · built paper and related papers follow b10's rules (261011); the venue's home is open
answers: Q02
answer-status: partial

## Opening

Two of the three already have one home, set by b10 for every Block: the built paper goes to the
Board's `delivery/`, one folder per version, and related papers go to the Board's `related/`. Only
the venue is the paper's own question: whether its call and author kit stay in `venues/<venue>/` at
the Board or become rows of `related/`.

**Where this Page sits:** [Q02 · Where on disk and on screen do the venue folders, the related-papers table and the built paper (LaTeX, Word, cover letter) sit: at the Board, or in each version's Job?](../../board.md).

**Why it matters:** a version is one send to one venue, so it was natural to keep its build and its
venue in the version Job. b10 settled that a Block's outputs and inputs are kept once, at the Block,
and every level reads them from there; this Page applies that to the paper.

## Content

### 1 · Answer

| what | on disk | on screen | rule |
|---|---|---|---|
| built paper (LaTeX, Word, PDF, cover letter) | `delivery/jNN_<version>/` at the Board, one folder per version, its Sections under it (`tNN_<section>/`), `latex/`, `word/` | top row › Delivery; from a version, that version's part | b10 s09-D05, s01-D32, s03 (haipipe-delivery 0.2.0) |
| a send | one row of `delivery/delivery.md` (date · for · from · status); only a person writes `sent` | Delivery | b10 s03-D05 |
| related papers | `related/related.md`, one row each (kind paper), open-licensed PDFs in `related/papers/` | Studio › Related (folded under the topics, 261011), and Report › Related Papers, by question | b10 s01-D34, s04-D01..D04 |
| meetings, files and emails we were sent | `related/meetings/`, `related/files/`, `related/emails/` (an .eml as it came), one row each | Studio › Related, each subfolder its own group | b10 s04-D01, D08, D09; /haipipe-related |
| venue call and author kit | open: `venues/<venue>/call.md` and `kit/` at the Board (what the theme reads today), or rows of `related/` | today Description › Venue | b16 s04-paper-related, Open |

A version Job keeps none of these: its face names its venue (`venue:`) and tells which Board
questions it answers; its build lands in the Board's `delivery/jNN_<version>/`.

### 2 · Evidence

- [b10 s01 · Studio, Block, Job, Task, Delivery (was s09)](../../../b10_project_workbench/studio/s01-overall-tree-structure/s01-overall-tree-structure.md):
  Studio and Delivery are the Block's alone (D01, D05).
- [b10 s04 · Related](../../../b10_project_workbench/studio/s04-related-workbench-skill/s04-related-workbench-skill.md):
  one `related/` per Block, read only, its table's columns; s04-D05 folds it inside the Studio.
- [b16 s03-paper-delivery](../../studio/s03-paper-delivery/) and [b16 s04-paper-related](../../studio/s04-paper-related/):
  the paper's own points, venues among them.
- ScalingGlucose (`examples-2-nn/Proj11-CGM-FM/paper/Paper-ScalingGlucose-NatSeries2026`, read 261011):
  `delivery/j01_v1009_nmi/` already holds the build (latex, word, six Sections); it has no
  `related/` yet (its one meeting sits in `meeting/`, its related papers in the telling's table)
  and no `venues/`.
- Code: `servers/workbench/frame.py` `related_view`, `studio_related`; `servers/workbench-paper/paper_theme.py`
  `_related_space`, `_description` (Scope · Venue · Resources).

### 3 · Limits

The venue's home is not settled. Keeping `venues/<venue>/` at the Board matches today's reader and
the Check the rules button, which reads the call; making it a `related/` row fits "what came in from
outside" but needs a place for the author kit. Nothing on a real Board has moved: ScalingGlucose's
`meeting/` to `related/meetings/` and its `related/related.md` wait for JL.

### 4 · Next

JL picks the venue's home in s04-paper-related. Then, with JL's go, ScalingGlucose gets
`related/related.md` (its related papers and the 2026-07-11 meeting), and the paper skills
(haipipe-paper-venue, haipipe-paper-story) name the same homes.
