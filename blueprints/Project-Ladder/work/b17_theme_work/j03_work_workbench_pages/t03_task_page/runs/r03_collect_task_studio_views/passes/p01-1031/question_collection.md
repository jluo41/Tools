# Task Studio views

for: b17.j03.t03-s59:theme_work.work_workbench_pages.task_page @ task_ui_studio

A Task's Studio, proposed: what it makes, its own topics, then Ask the agent. Every view and section is in s59's result/views-proposal.md. Orange marks what differs.

<!-- One card per question: ## QN · title, one short why, at most one ```text sketch``` or ![picture](f.png),
     **the question?**, then - [x] A · my pick and - [ ] B · another, then Why A: one line.
     collect.py check holds the limits; collect.py build renders the form. -->
<!-- previews: t03_task_page/scripts/build_r03_previews.py writes every option-q*.html here; rerun it, never edit them -->

## Q1 · Made topic

t01_skill_section holds no sNN, but it makes s01's piece ladder-section: s01's delivery/render.yaml names its Run. Today t01 has no Studio, so s01 shows only on the Block's.

```text
b17_theme_work/s01-work-ladder/delivery/render.yaml
  - code: "ladder-section: haipipe-work SKILL.md's The work ladder section"
    by: j01_work_ladder_contract/t01_skill_section/runs/run-write-ladder-section
```

**Does a Task's Studio show the Block topic it makes?**

- [x] A · Yes: its full card, first, under the heading "This Task makes".
  [preview](option-q1-a.html)
- [ ] B · Yes, as one line that opens its card on the Block.
  [preview](option-q1-b.html)
- [ ] C · No: only its own topics, as today.
  [preview](option-q1-c.html)

Why A: t01 exists to make that piece; its thinking belongs here, as s56 proposes for a Job.

## Q2 · No topic

A Task that holds no sNN and makes no piece, such as b35's t02_new_topic_for_line, has no Studio on its rail today. You keep Interactions and Delivery on the rail even when empty.

**When a Task holds no topic, does Studio stay on the rail?**

- [x] A · Yes: one line saying no topic yet, then Ask the agent to start one.
  [preview](option-q2-a.html)
- [ ] B · No: Studio leaves the rail, as today; section=studio opens Work.
  [preview](option-q2-b.html)

Why A: The rail reads the same on every Task; the empty Studio is where topics start.

## Q3 · One click

s59's open question. new_topic.py writes a topic: its face, its mind map, a number from its band; a Task holds three at most. b16 s40 asks the same.

**Can an sNN be started here with one click?**

- [x] A · No: Copy prompt; the agent runs new_topic.py and draws it with you.
  [preview](option-q3-a.html)
- [ ] B · Yes: New topic takes a title and writes sNN-<slug>/ in this Task.
  [preview](option-q3-b.html)

Why A: A button gives an empty face; the prompt gives face, drawing and mind map together.

## Q4 · Ask the agent

Studio's two prompts: talk and sketch (about its topics) and start a topic. Work keeps its own Ask the agent for its Runs (s58). Shown: t03_task_page, Studio beside Work.

**Where does the Studio's Ask the agent sit?**

- [x] A · Its last section: one notes box, then its two Copy prompt buttons.
  [preview](option-q4-a.html)
- [ ] B · Its first section, above the topics.
  [preview](option-q4-b.html)
- [ ] C · Not in Studio: Work's Ask the agent carries both prompts.
  [preview](option-q4-c.html)

Why A: Pictures first, as a Studio is; a prompt follows the topics it talks about.

## Q5 · Work tag

Today a card's Work tag opens its Job's whole Work: on t03_task_page, j03's three Tasks and every Run. Shown: s59's card and what its Work opens.

```text
t03_task_page/runs/run-design-task-page/run.yaml
  target: task-page
  writes: s57-task-ui-report/delivery/ui/ · s58-task-ui-work/delivery/ui/ · s59-task-ui-studio/delivery/ui/
```

**What does a card's Work tag open on a Task page?**

- [x] A · The Run that writes its delivery: run-design-task-page.
  [preview](option-q5-a.html)
- [ ] B · Its Job's whole Work, as today.
  [preview](option-q5-b.html)
- [ ] C · Nothing: no Work tag on a Task page.
  [preview](option-q5-c.html)

Why A: That Run makes the topic's delivery; one click shows it, with nothing else around.
