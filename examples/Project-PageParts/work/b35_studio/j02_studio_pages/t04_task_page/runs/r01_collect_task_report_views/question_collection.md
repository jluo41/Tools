# Task Report views

for: b35.j02.t04-s17

Previews show t02_block_page (three sNN, Runs planned); Results show t01_build_studio_pages, the Task with done Runs.

<!-- previews: build_previews.py in this Run folder writes every q<N>-<key>.html from the live 5623 page; rerun it, never edit them -->

## Q1 · View list

A Task's Report checks results and progress. Today: MindMap (Runs only, no sNN) · Status (sNN, then Runs). Nothing shows what a done Run found.

**Which buttons sit under the Task's title?**

- [ ] A · MindMap · Status, as today; the map adds its sNN.
  [preview](q1-a.html)
- [ ] B · MindMap · Results · Status: Results adds what each done Run found.
  [preview](q1-b.html)
- [x] C · MindMap · Results: states sit on the map's leaves; no Status.
  [preview](q1-c.html)
- [ ] D · MindMap · UI: one view per delivery type, as b17 s51-D01.
  [preview](q1-d.html)

Why C: The map already carries each state; Results is the one thing missing.

## Q2 · MindMap

The face's Rule 1: the Task, its sNN (at most 3), its Runs. Each collect Run's for: line names the sNN it serves (r01 serves s11).

**How does the Task's map branch?**

- [ ] A · Two branches: Studio (s11 to s13), then Runs; each leaf its state.
  [preview](q2-a.html)
- [x] B · One branch per sNN, with the Runs that serve it under it.
  [preview](q2-b.html)
- [ ] C · Runs only, as today; the sNN stay in Studio.
  [preview](q2-c.html)

Why B: Each Run sits under the topic it serves; you see what waits on what.

## Q3 · Results

Each done Run keeps its ask, its Summary and its changed files (run-build-*/passes/p01-1030/pass.md).

**What does one Results row show?**

- [x] A · Your ask in your words, then the Run's Summary.
  [preview](q3-a.html)
- [ ] B · The Run's Summary, then the files it changed.
  [preview](q3-b.html)
- [ ] C · Only the newest done Run, its pass in full.
  [preview](q3-c.html)

Why A: You check each result against your own words.

## Q4 · Nothing done

On t02_block_page all three Runs are planned, so Results has nothing yet.

**What shows before any Run is done?**

- [x] A · No Results button until a Run is done; the map shows planned Runs.
  [preview](q4-a.html)
- [ ] B · Results shows one line: no Run done yet, see Work.
  [preview](q4-b.html)
- [ ] C · Results lists the planned Runs, each ⬜ planned.
  [preview](q4-c.html)

Why A: An empty view is noise; the map already shows the planned Runs.

## Q5 · Clicks

s02-D05: a link to an sNN opens its card in its level's Studio. Shown: a click on s11 in the MindMap.

**What does a click on a map leaf do?**

- [x] A · Goes to its card in Studio, outlined; a Run goes to Work.
  [preview](q5-a.html)
- [ ] B · Opens its card in a pop-out; the Report stays behind.
  [preview](q5-b.html)
- [ ] C · Unfolds in place: its one line and its open question.
  [preview](q5-c.html)

Why A: s02-D05 already decided it: one place per thing.
