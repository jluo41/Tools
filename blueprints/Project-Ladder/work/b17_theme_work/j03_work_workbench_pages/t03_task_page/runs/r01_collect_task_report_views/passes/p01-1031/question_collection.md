# Task Report views

for: b17.j03.t03-s57:theme_work.work_workbench_pages.task_page @ task_ui_report

Applied: MindMap first, one view per type, Status to Work, planned look, one version word. Hard Runs use placeholder names: b17 has none yet. Full proposal: s57 result/views-proposal.md.

<!-- One card per question: ## QN · title, one short why, at most one ```text sketch``` or ![picture](f.png),
     **the question?**, then - [x] A · my pick and - [ ] B · another, then Why A: one line.
     collect.py check holds the limits; collect.py build renders the form. The previews are written by
     ../../scripts/build_r01_previews.py; rerun it, never edit an option-q*.html by hand. -->

## Q1 · View list

Decided: MindMap, then one view per delivery type. A Task has one output contract, and a delivery is one thing of one type (JL 261030). Open: a figures Run's charts.

**Which buttons follow MindMap on a Task's Report?**

- [x] A · One: the Task's type, Data; charts and audits sit inside it.
  [preview](option-q1-a.html)
- [ ] B · One per type its Runs make: Data, then Display for charts.
  [preview](option-q1-b.html)

Why A: One output contract, one button; the charts check the same result.

## Q2 · Which Runs

The s57 face asks: the newest Run's result, or every Run's? A replaced Run is pruned, so each current Run is its own cut; the newest may be an audit.

```text
t01_fit_model (placeholder)
r01_smoke_fit       🧪 trial
r02_fit_fold00      🔨 make
r03_fit_fold01      🔨 make
r04_audit_folds     🔎 check
r05_figures_folds   📊 figures
```

**Which Runs' results does the Data view show?**

- [x] A · Every current Run, one row each, the make Runs first.
  [preview](option-q2-a.html)
- [ ] B · Only the newest make Run, whole; the others stay in Work.
  [preview](option-q2-b.html)
- [ ] C · The newest make Run whole; every other Run one line.
  [preview](option-q2-c.html)

Why A: Each current Run is its own cut, a fold or a window.

## Q3 · Hard Run row

A hard Run's result/ keeps RUN-REPORT.md, tables/ and runtime.yaml; the receipt goes to Work. In every option, tags under the row open the rest.

**What leads one hard Run's row?**

- [x] A · Its headline line and its first table, small.
  [preview](option-q3-a.html)
- [ ] B · Its RUN-REPORT.md whole, in place, then its tables.
  [preview](option-q3-b.html)
- [ ] C · Its headline line only.
  [preview](option-q3-c.html)

Why A: The number and its table at a glance; the long report one click away.

## Q4 · Soft Run row

A soft Run writes into another file and keeps passes/pNN-MMDD/. Shown: b35's run-write-skill-section, whose pass p01-1030 wrote a haipipe-studio SKILL.md section.

**What does a soft Run's row show?**

- [x] A · The section it wrote, as it reads now; p01-1030 opens its pass.
  [preview](option-q4-a.html)
- [ ] B · Its newest pass: what was asked, what changed.
  [preview](option-q4-b.html)
- [ ] C · Both: the section, then its newest pass below it.
  [preview](option-q4-c.html)

Why A: You check the thing itself; how it was made is Work's.

## Q5 · Task MindMap

The MindMap opens first. A draft Task's map is its paper content (b32 s42). A work Task's map could draw its Runs, or its result's content.

**What does a work Task's MindMap draw?**

- [x] A · Its Runs by role, each boxed with what it found.
  [preview](option-q5-a.html)
- [ ] B · Its result's content: each report's sections, boxed with their first sentence.
  [preview](option-q5-b.html)

Why A: One look shows every Run's finding; each report is one click away.
