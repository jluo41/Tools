# Job Work views

for: b17.j03.t02-s55:theme_work.work_workbench_pages.job_page @ job_ui_work

<!-- One card per question: ## QN · title, one short why, at most one ```text sketch``` or ![picture](f.png),
     **the question?**, then - [x] A · my pick and - [ ] B · another, then Why A: one line.
     collect.py check holds the limits; collect.py build renders the form.
     The previews are written by ../../scripts/build_r02_previews.py from j03's own folders; rerun it, never edit them.
     The whole proposal, every view and subsection: ../../s55-job-ui-work/result/views-proposal.md -->

A Job's Work lists its Tasks. Samples are j03, the Job these forms sit in. Its view buttons: Tasks, plus Runs if Q1 B, Deliverables if Q2 B.

## Q1 · Runs

s55's open question. A Task holds hard Runs (rNN_, result/), soft Runs (run-…, passes/) and forms (rNN_collect_). Today a Job's Work shows none. s52 asks the same one level up.

**Where do a Task's Runs show on the Job page?**

- [x] A · Under its Task row, one line each: name, word, one verb.
  [preview](option-q1-a.html)
- [ ] B · On a Runs view of their own, Task by Task.
  [preview](option-q1-b.html)
- [ ] C · Only on each Task's own page; the row links there.
  [preview](option-q1-c.html)

Why A: Every Run shows where you look, like b16's five step words on a Section.

## Q2 · Hands over

Each sNN's `delivery/render.yaml` names the Run that makes each piece: s04's job-page by t02_job_page's run-design-job-page. Older Jobs keep a `## Deliverables` to-do list. s54 asks whether the Report lists them too.

**Where does what each Task hands over show?**

- [x] A · On its Task row: the piece it makes, with that Run's word.
  [preview](option-q2-a.html)
- [ ] B · A Deliverables view after Tasks, as today: the face's to-do list.
  [preview](option-q2-b.html)
- [ ] C · Only in the Job's Report, by delivery type (s54's cell).
  [preview](option-q2-c.html)

Why A: The row then says what the Task is for and where it stands.

## Q3 · What waits

You said what waits on you comes first, in orange. On j03 nine forms wait, three per Task; `collect.py bundle` joins them into one page. s52 asks the same for the Block.

**What sits first in a Job's Work?**

- [x] A · Interactions: each form, sign or Run waiting on you, with Answer all.
  [preview](option-q3-a.html)
- [ ] B · Nothing extra, as today: each Task row carries its orange Interaction.
  [preview](option-q3-b.html)
- [ ] C · One orange line with Answer all; forms stay on their rows.
  [preview](option-q3-c.html)

Why A: You see each thing that waits and answer it in one place.

## Q4 · Task word

A Task row carries one word for where it stands. Today it is the face's hand-written `state:` line; all three j03 Tasks say 🔴 OPEN.

**Which word says where a Task stands?**

- [x] A · One word from its Runs' cards: waits, running, failed, done, not run.
  [preview](option-q4-a.html)
- [ ] B · The face's `state:` line, as written today.
  [preview](option-q4-b.html)
- [ ] C · Five life words (haipipe-task): plan · build · run · read · close.
  [preview](option-q4-c.html)

Why A: Read from disk, so never stale; one word, like each delivery's version.
