# Where do the Story and Ideation live?
state: 🟡 DRAFT · decided by JL 2026-10-07; decisions carried into s05 on 2026-10-10; remaining migration work is separate
answers: Q04
answer-status: partial
results-read: 2026-10-07T22:46-04:00

## Opening

A paper Board takes b03's shape. Ideation and each telling of the paper are studio topics
(`studio/s01-ideation/`, `studio/sNN-story-<telling>/`), each research question is a Board
Question grouped by its topic with a report (`reports/qNN_<question>/`), and the Section Narrative
with its compile order moves to the version that tells it. The Story and Ideation skills stay,
called from the Idea Studio and the Audience Report.

**Where this Page sits:** [Q04 · Where do the Story and Ideation live?](../../board.md).

**Why it matters:** the paper's Audience Report has had no Questions of its own; its answers sat
inside one Story Page. On b03's shape each question gets a row (Question │ Work │ Report) and a
report that can be checked.

## Content

### 1 · Answer

Drawn in [s05, frame 9](../../studio/s05-board-job-task-boundary/s05-board-job-task-boundary.excalidraw). All five s04 decisions are preserved as s05-D06-D10, with their original ids. The full s04 record is frozen under `_archive/20261010/studio/`.

| the part | goes to | shows in |
|---|---|---|
| Ideation (all of it) | `studio/s01-ideation/` | Idea Studio · Audience Report › Ideation |
| §1 Identity · §2 Pitch · §4 Stakes | `studio/sNN-story-<telling>/` face | Description › Scope · Audience Report › Narrative |
| the Story's drawings | `studio/sNN-story-<telling>/` | Idea Studio |
| §3, one research question each | `board.md ## Questions` (group: its topic) + `reports/qNN_<question>/` | Audience Report › High-level logic + Low-level work |
| §5 · §6 · §7 | each report's Work | the Question's Work column |
| §8 + compile order | the version face's `## Narrative` | the version's Draft-Main · the build |
| related papers | `related/related.md` | Description › Related |

### 2 · Evidence

JL 261007: "the stories will be merged into the studio sNN and report qNN, all the questions will
be grouped as different topics"; "story and ideation can be called, in that view". b03 s04 sets the
two folders' jobs (the studio makes, the report shows) and gives every level both.

### 3 · Limits

- The 2026-10-07 record below predates the current Story/Ideation skill wording. Both now define
  topic faces and Board Question rows; migration of older paper Boards still needs its own checks.
- A telling's evidence, discovery and Task roadmaps (§5–§7) stay in its face; they are not yet split
  into each report's Work.
- The example Board's build finds every Section through the version face's order, but no Section has a
  LaTeX fragment under its new `tNN_` name until each one is exported again.

### 4 · Historical record (2026-10-07)

These are the checks recorded on that date, not checks rerun by the 2026-10-10 topic cleanup.

- Readers: `paper.collect` reads a telling topic as a Story: its face, its Questions' blocks from their
  reports (`feeds:`), and its version's `## Narrative`. Ideation comes from `studio/sNN-ideation/`; the
  build reads its order from the version face. Tests: a placeholder Board in this shape.
- Scripts: `haipipe-paper/scripts/topics_paper.py` (Story and Ideation into topics and reports) and
  `version_paper.py` (a version's Space folders; the next version from an earlier one; a review batch
  as a comments report), each with a dry run, a record and an exact rollback.
- One example Board moved: 6 studio topics, 6 reports, the Section Narrative in its sent version's face;
  the next version starts from the sent one's writing and answers the editor's decision. Every level
  opens (524 screens, 0 failures), every Page is found, no new broken link.

### 5 · Next

1. Check older Boards against the current topic and Question contracts before migrating them.
2. Split §5–§7 into each report's Work, as the reports are answered.
3. Export each Section again, so the build has its fragments under the new names.
