# How should a workbench's Guide explain its method?
state: 🟡 DRAFT · written from the 2026-10-03 workbench changes; CHECK pending
content: draft v0.1 · adopted 261003 2204
answers: Q01
answer-status: partial
results-read: 2026-10-03T22:05:19-04:00

## Opening

A family's Guide › Method is one page with its steps as the spine, served by one shared renderer; Paper, Page and Labeling use it and Design's page has the same shape, while Insight's still renders its own.

**Where this Page sits:** [Q01 · What should Guide › Method hold for a family, how is it drawn, and how do its methods connect to their papers?](../../board.md).

**Why it matters:** A Method page that explains the same steps three or four times, or opens on reference tables, is not read; one shape on every family lets a reader move between them.

## Content

### 1 · Answer

A family's Guide › Method is one page with its steps as the spine: the method in one picture, the steps in one table, a section for each step that needs depth, then why it works, then the reference, folded. <!-- realizes: C1.P1.B1 -->
The picture is the family's methods canvas, drawn first from the method file and then edited full screen; inside Guide it opens view only, so it never edits beside another canvas. <!-- realizes: C1.P1.B2 -->
The steps table gives each step what happens, its methods, where it happens in the workbench and who signs, so each step appears once. <!-- realizes: C1.P1.B3 -->
Each in-depth section holds the method cards of its steps and the tests those steps must pass; one made-up example runs through the page, and no file notes show on screen. <!-- realizes: C1.P1.B4 -->
One shared renderer, `method_page_html` in workbench-shared, serves any family that names `method_doc` and `method_drawing`; Paper, Page and Labeling use it, and Design's own page has the same shape. <!-- realizes: C1.P1.B5 -->

### 2 · Evidence

The rule is written in [servers/README.md](../../../../../plugins/haipipe-toolkit/servers/README.md), under Adding a workbench. <!-- realizes: C2.P2.B1 -->
The renderer is [workbench_guide.py](../../../../../plugins/haipipe-toolkit/servers/workbench-shared/workbench_guide.py); the method files are [page-method.md](../../../../../plugins/haipipe-toolkit/skills/page/haipipe-workbench-page/ref/page-method.md) and [paper-method.md](../../../../../plugins/haipipe-toolkit/skills/paper/haipipe-workbench-paper/ref/paper-method.md), each with seven method cards whose papers pass the online check. <!-- realizes: C2.P2.B2 -->
The shape went through three rounds on 2026-10-03: a page of parts A to E, then the steps as the spine, then every part as a fold, all closed at first. <!-- realizes: C2.P2.B3 -->

### 3 · Limits

Insight's Method page still uses its own renderer, so a change to the shared page does not reach it. <!-- realizes: C3.P3.B1 -->
The methods canvas is drawn once from the method file; after a person edits it, a changed method card does not reach the drawing. <!-- realizes: C3.P3.B2 -->

### 4 · Next

Move Insight's and Design's Method pages onto the shared renderer, so one change reaches every family. <!-- realizes: C4.P4.B1 -->
Check that each family's methods canvas still matches its cards after a card changes. <!-- realizes: C4.P4.B2 -->
