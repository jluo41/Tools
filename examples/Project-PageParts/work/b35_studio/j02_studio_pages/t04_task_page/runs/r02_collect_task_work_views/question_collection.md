# Task Work views

for: b35.j02.t04-s18

A Task's Work lists its Runs. Each preview shows two real Tasks: t01 (soft Runs) left, t02 (collection Runs) right.

<!-- previews: build_previews.py in this Run folder writes every q*.html; rerun it, never edit them -->

## Q1 · View list

Today Work has one view, Progress, and each row shows only the Run's name and status. Every b35 Task holds one kind and one type of Run, so a split shows one button.

**Which buttons sit under the title?**

- [x] A · Runs: one view, every Run one row.
  [preview](q1-a.html)
- [ ] B · Hard · Soft: one view per kind of Run.
  [preview](q1-b.html)
- [ ] C · Runs · Results · Passes: one view per part of a Run folder.
  [preview](q1-c.html)
- [ ] D · One view per Run type, as Studio's groups: Build, Collect.
  [preview](q1-d.html)

Why A: A Task holds few Runs; one list shows all, splits show one button.

## Q2 · Runs view

The Runs view, top to bottom. Status marks are only the four words: 🙋 waiting, ⏳ running, ⬜ planned, ✅ done.

**How is the Runs list arranged?**

- [x] A · One list: a waiting form first, then by name.
  [preview](q2-a.html)
- [ ] B · Two headings: Waits on you, then Runs.
  [preview](q2-b.html)
- [ ] C · One heading per status: waiting, running, planned, done.
  [preview](q2-c.html)

Why A: Few rows; a heading repeats the status word each row already says.

## Q3 · A Run's row

The face's rule 1 says a row is its name, then status · agent · skill from run.yaml. Its Open asks whether a row names the sNN it serves.

**What does one Run's row show?**

- [ ] A · Name, then status · agent · skill, as rule 1 says.
  [preview](q3-a.html)
- [x] B · A, plus its latest pass's title and pass name.
  [preview](q3-b.html)
- [ ] C · B, plus what it wrote (writes:) or its result/ files.
  [preview](q3-c.html)
- [ ] D · B, plus the sNN it serves, from its target: line.
  [preview](q3-d.html)

Why B: The pass title says what the Run did, in its own words.

## Q4 · Clicks

A Run has no page of its own. Its folder holds run.yaml, the ticket, result/ and passes/.

**What does a click on a Run's name do?**

- [x] A · Pop-out: run.yaml, ticket, result/, passes, one after another.
  [preview](q4-a.html)
- [ ] B · Pop-out of its ticket only.
  [preview](q4-b.html)
- [ ] C · Nothing; buttons on the row: Ticket, Result, Passes.
  [preview](q4-c.html)

Why A: One click shows the whole Run; no buttons to add on each row.
