# Job Studio views

for: b17.j03.t02-s56:theme_work.work_workbench_pages.job_page @ job_ui_studio

A Job's Studio shows the topics it makes; every view is listed in s56's `result/views-proposal.md`. Previews use real names; orange marks what differs.

<!-- One card per question: ## QN · title, one short why, at most one ```text sketch``` or ![picture](f.png),
     **the question?**, then - [x] A · my pick and - [ ] B · another, then Why A: one line.
     collect.py check holds the limits; collect.py build renders the form.
     The previews are written by ../../scripts/build_r03_previews.py; rerun it, never edit them. -->

## Q1 · Made topic

j01 makes b17-s01, which sits at the Block: s01's render.yaml names j01's Runs. Today j01 has no Studio at all, so s01 shows only on the Block's Studio.

```text
b17_theme_work/s01-work-ladder/delivery/render.yaml
  by: j01_work_ladder_contract/t01_skill_section/runs/run-write-ladder-section
  by: j01_work_ladder_contract/t02_scaffold/runs/run-build-work-scaffold
  by: j01_work_ladder_contract/t03_demo_fixture/runs/run-check-demo-block
```

**Does a Job's Studio show the Block topic it makes?**

- [x] A · Yes: its full card, first, under the heading "This Job makes".
  [preview](option-q1-a.html)
- [ ] B · Yes, as one line that opens its card on the Block.
  [preview](option-q1-b.html)
- [ ] C · No: only its own and its Tasks' topics; j01 keeps no Studio.
  [preview](option-q1-c.html)

Why A: j01 exists to make s01, so its thinking belongs on j01's page.

## Q2 · View buttons

Your rule: Studio groups are its view buttons, from each face's Tags. On j03 that gives five, two holding only s04. Your b16 note: Studio may later take Work's buttons.

```text
A  Interface · Navigation · Block UI · Job UI · Task UI
B  This Job · Block
C  This Job makes · t01_block_page · t02_job_page · t03_task_page
```

**Which view buttons does a Job's Studio have?**

- [x] A · One per group, from Tags, in the Block's order; Other last.
  [preview](option-q2-a.html)
- [ ] B · This Job, then Block, which adds the Block's other topics.
  [preview](option-q2-b.html)
- [ ] C · This Job makes, then one per Task, as Work lists them.
  [preview](option-q2-c.html)

Why A: The same buttons as the Block's Studio; no new list to keep.

## Q3 · Inside a view

A view can hold the topic j03 makes and topics from several Tasks. A heading can name where each sits; without one, the card's address says it.

**How are the topics inside one view laid out?**

- [x] A · Under headings: This Job makes, then each Task by name.
  [preview](option-q3-a.html)
- [ ] B · One list, no headings; each address says where it sits.
  [preview](option-q3-b.html)

Why A: A heading names the Task in words; an address needs decoding.

## Q4 · What waits

You asked that what waits on you is orange and first. Today a waiting form shows only as the orange 🙋 Interaction button on its card.

**Where does a waiting form show in a Job's Studio?**

- [x] A · A line on top of the view: its title, its topic, Answer.
  [preview](option-q4-a.html)
- [ ] B · Only on its card: the orange 🙋 Interaction button.
  [preview](option-q4-b.html)

Why A: Orange and first, one click to the form, as at the top of Work.

## Q5 · No topic

A Job with no topic, such as j02_food, has no Studio on its rail today. You keep Interactions and Delivery on the rail even when empty.

**When a Job holds no topic, does Studio stay on the rail?**

- [x] A · Yes: Studio stays, with one line saying no topic yet.
  [preview](option-q5-a.html)
- [ ] B · No: Studio leaves the rail, as today.
  [preview](option-q5-b.html)

Why A: The rail reads the same on every Job page.
