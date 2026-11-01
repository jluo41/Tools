# Task Work views

for: b17.j03.t03-s58:theme_work.work_workbench_pages.task_page @ task_ui_work

<!-- One card per question: ## QN · title, one short why, at most one ```text sketch``` or ![picture](f.png),
     **the question?**, then - [x] A · my pick and - [ ] B · another, then Why A: one line.
     collect.py check holds the limits; collect.py build renders the form. -->

A work Task's Work, verb do. Previews show an example fit Task, its Runs under their role (the Run contract); orange boxes mark differences. Full proposal: `s58-task-ui-work/result/views-proposal.md`.

## Q1 · Work's views

Today a Task's Work has one view, Progress: a row per Run, its status word, the Interaction button on a form. A draft Task's Work is its steps instead; the old page had Code and Runs.

**Which view buttons does a work Task's Work have?**

- [x] A · Runs: one view, what waits first, then each Run, then the agent.
  [preview](option-q1-a.html)
- [ ] B · Runs · Code: the worker, configs and code review get a view.
  [preview](option-q1-b.html)
- [ ] C · Plan · Build · Run · Check: the Task's steps, as a draft Task's.
  [preview](option-q1-c.html)

Why A: One screen to do the work; code is in Files, results in Report.

## Q2 · Runs or passes

A Run is redone in passes (`passes/pNN-<MMDD>/`): a retry of a ticket, or one more round of agent work. Timeline already lists every pass by date. This is s58's open point.

**A row per Run, or one per pass?**

- [x] A · One row per Run; its newest pass is its word: p02 · 10-29.
  [preview](option-q2-a.html)
- [ ] B · One row per pass, under its Run's name.
  [preview](option-q2-b.html)
- [ ] C · One row per Run, each pass a small button.
  [preview](option-q2-c.html)

Why A: You act on a Run; its passes are in Open and Timeline.

## Q3 · One Run row

A row shows one Run. Its card, `run.yaml`, also names its kind, type, role, agent and skill; its receipt says when it ran.

**What does one Run row show?**

- [x] A · Name, one line, state word, newest pass; Open and Result.
  [preview](option-q3-a.html)
- [ ] B · Also who runs it and its skill: claude · haipipe-task-for-fit.
  [preview](option-q3-b.html)
- [ ] C · Name and state word only, as today.
  [preview](option-q3-c.html)

Why A: Enough to choose a row; who and how are in Open.

## Q4 · What waits

What waits on you is orange and first, as you asked. A form waits for your answer. A built ticket whose card names you waits for you to press Run.

**What moves up into Waits for you?**

- [x] A · Forms to answer, and built tickets you press: Copy command.
  [preview](option-q4-a.html)
- [ ] B · Forms to answer only; built tickets stay in their place.
  [preview](option-q4-b.html)
- [ ] C · Forms, built tickets, and failed Runs.
  [preview](option-q4-c.html)

Why A: Only you press Run; fixing a failed Run starts with the agent.

## Q5 · Its result

Today a done Run's figure shows full width under its row, with its headline (`output_of`). s57, this Task's Report, shows its newest result.

**How does a done Run show its result in Work?**

- [x] A · Its picture small at the row's right; a click opens it.
  [preview](option-q5-a.html)
- [ ] B · Its figure full width under its row, as today.
  [preview](option-q5-b.html)
- [ ] C · One headline line; the figure only in Report.
  [preview](option-q5-c.html)

Why A: You see each result where its Run is, and rows stay short.

## Q6 · Ask the agent

The old page's Runs panel had a Prompt box and Copy. Here it is one notes box, then Copy prompt: plan, build, check (`run-plan-t01`, `run-build-t01`, `run-check-t01`).

**Where does Ask the agent sit in Work?**

- [x] A · At the foot of Runs, after every Run.
  [preview](option-q6-a.html)
- [ ] B · Second, right under Waits for you, as a draft step.
  [preview](option-q6-b.html)
- [ ] C · Nowhere in Work; this Task's Studio holds it.
  [preview](option-q6-c.html)

Why A: You read the Runs first, then ask for the next one.
