# q01_guide_method · draft v0.1
draft-version: v0.1
supersedes: none
date: 261003
approved: ⬜
status: working · written from the 2026-10-03 workbench changes in run-section
arc: One page per family, the steps as its spine, served by one renderer.

## 1 · Structure · Bullet Point Table

### Structure Overview

- C1 · Answer
- C1.P1 · One page, the steps as its spine
- C2 · Evidence
- C2.P2 · The rule, the renderer and the files
- C3 · Limits
- C3.P3 · What one renderer does not yet reach
- C4 · Next
- C4.P4 · What to do next

### C1.P1 · One page, the steps as its spine
- B1 · [Answer] One page, the steps as its spine.
  Note: Picture, steps, depth, why, reference.
  Evidence: none · reads the files linked under Evidence
- B2 · [Detail] The picture is drawn once, then edited full screen.
  Note: View only inside Guide.
  Evidence: none · reads the files linked under Evidence
- B3 · [Detail] The steps table says each step once.
  Note: What, methods, where, who signs.
  Evidence: none · reads the files linked under Evidence
- B4 · [Detail] Each in-depth section holds its cards and tests.
  Note: One made-up example; no file notes.
  Evidence: none · reads the files linked under Evidence
- B5 · [Owner] One shared renderer serves the families.
  Note: method_doc and method_drawing.
  Evidence: none · reads the files linked under Evidence

### C2.P2 · The rule, the renderer and the files
- B1 · [Evidence] The rule is in the servers README.
  Note: Adding a workbench.
  Evidence: none · reads the files linked under Evidence
- B2 · [Evidence] The renderer and the two method files.
  Note: Seven cards each, papers checked online.
  Evidence: none · reads the files linked under Evidence
- B3 · [Evidence] The shape took three rounds in one day.
  Note: A to E, steps as spine, folds.
  Evidence: none · reads the files linked under Evidence

### C3.P3 · What one renderer does not yet reach
- B1 · [Limit] Insight still renders its own page.
  Note: Not on the shared renderer.
  Evidence: none · reads the files linked under Evidence
- B2 · [Limit] A canvas does not follow its cards.
  Note: Drawn once, then the person's.
  Evidence: none · reads the files linked under Evidence

### C4.P4 · What to do next
- B1 · [Next] Move Insight and Design onto the renderer.
  Note: One change reaches every family.
  Evidence: none · reads the files linked under Evidence
- B2 · [Next] Check canvases against their cards.
  Note: After a card changes.
  Evidence: none · reads the files linked under Evidence

## 2 · Scratch · What to write here

### C1.P1 · One page, the steps as its spine

### C2.P2 · The rule, the renderer and the files

### C3.P3 · What one renderer does not yet reach

### C4.P4 · What to do next

## 3 · Draft · Reading and Revise

### C1.P1 · One page, the steps as its spine
- B1 · A family's Guide › Method is one page with its steps as the spine: the method in one picture, the steps in one table, a section for each step that needs depth, then why it works, then the reference, folded.
- B2 · The picture is the family's methods canvas, drawn first from the method file and then edited full screen; inside Guide it opens view only, so it never edits beside another canvas.
- B3 · The steps table gives each step what happens, its methods, where it happens in the workbench and who signs, so each step appears once.
- B4 · Each in-depth section holds the method cards of its steps and the tests those steps must pass; one made-up example runs through the page, and no file notes show on screen.
- B5 · One shared renderer, `method_page_html` in workbench-shared, serves any family that names `method_doc` and `method_drawing`; Paper, Page and Labeling use it, and Design's own page has the same shape.

### C2.P2 · The rule, the renderer and the files
- B1 · The rule is written in [servers/README.md](../../../../../plugins/haipipe-toolkit/servers/README.md), under Adding a workbench.
- B2 · The renderer is [workbench_guide.py](../../../../../plugins/haipipe-toolkit/servers/workbench-shared/workbench_guide.py); the method files are [page-method.md](../../../../../plugins/haipipe-toolkit/skills/page/haipipe-workbench-page/ref/page-method.md) and [paper-method.md](../../../../../plugins/haipipe-toolkit/skills/paper/haipipe-workbench-paper/ref/paper-method.md), each with seven method cards whose papers pass the online check.
- B3 · The shape went through three rounds on 2026-10-03: a page of parts A to E, then the steps as the spine, then every part as a fold, all closed at first.

### C3.P3 · What one renderer does not yet reach
- B1 · Insight's Method page still uses its own renderer, so a change to the shared page does not reach it.
- B2 · The methods canvas is drawn once from the method file; after a person edits it, a changed method card does not reach the drawing.

### C4.P4 · What to do next
- B1 · Move Insight's and Design's Method pages onto the shared renderer, so one change reaches every family.
- B2 · Check that each family's methods canvas still matches its cards after a card changes.
