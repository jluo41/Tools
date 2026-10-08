# What does each base family give the themes?
state: 🔴 OPEN
answers: Q01
answer-status: open

## Opening

A first answer, drawn from disk in [s02 base map](../../studio/s02-base-map/s02-base-map.excalidraw)
(counts are files that name a skill, not proven calls). Two base families are called by every
theme, two by most, and four by only one or two themes. One theme, discovery, is named by six of
the other seven themes, so it behaves like base.

**Where this Page sits:** [Q01 · For each base family, what does it provide (contract, engine, CLI, agents), and which themes and other base families call it?](../../board.md).

**Why it matters:** a base family only one theme calls is not base, and a theme every theme calls
may be. The answer tells Q03 what to move.

## Content

### What the map shows (2026-10-07)

```text
base family   themes calling it        which
page          7/7                      every theme
project       7/7                      every theme (haipipe-run, haipipe-project)
question      5/7                      cowork, discovery, insight, paper, work
task          5/7                      discovery, insight, labeling, paper, work
display       2/7                      paper, work
ideation      2/7                      discovery, paper
writing       2/7                      cowork, paper
search        1/7                      discovery
```

- Theme x theme should be empty; it is not. Discovery's skills are named by cowork (1), design (3),
  insight (2), labeling (2), paper (5) and work (1); paper's by discovery (5); design's by
  labeling (1).
- Base skills named by only one theme: six ideation skills (only paper) and five search skills
  (only discovery). 39 base skills are named by nobody outside their family, most of them the
  stage-pipeline specialists in task/ that a person calls directly.

### Proposed reading

- page, project, question and task are the base proper.
- search is discovery's (only discovery calls it); ideation and writing lean to paper; display is
  shared by paper and work. These go to Q03 as candidates, with their callers.
- Discovery is called like a base family (literature search, Paper Runs, citations). Either the
  part of discovery other themes call moves to base, or those cross-theme names are doc links
  that the layer rule allows; JL's call.

### Evidence

- [s02 base map](../../studio/s02-base-map/s02-base-map.excalidraw): base family x caller, theme x
  theme, single-caller and uncalled base skills, read from disk by `studio/s02-base-map/callmap.py`.
- [s01 base overview](../../studio/s01-base-overview/s01-base-overview.excalidraw): the families.

### Limits

- A count is a file that names a skill: a doc mention counts like a code call. Splitting code
  calls from doc mentions is the next refinement.
- History (CHANGELOGs, dated feedback, chat transcripts, drawings) is left out.
