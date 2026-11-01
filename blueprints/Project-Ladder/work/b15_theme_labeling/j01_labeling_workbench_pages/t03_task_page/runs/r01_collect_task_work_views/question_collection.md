# Task Work screens

for: b15.j01.t03-s58:theme_labeling.labeling_workbench_pages.task_page @ task_ui_work

<!-- One card per letter that passed the Design loop's drawing review (haipipe-ui, stage 1): its screen as option A's
     picture. Q5 to Q7 come from the flow simulation, runs/r02_simulate_task_workflow/result/flow-simulation.md (JL
     261101: "could you simulate to use it as well?"). Answers feed the build of the meaning and expression Task pages
     (labeling_focus.py), stage 2. -->

Four views passed review. A simulated run then found seven slips (fixed) and three choices for you, Q5 to Q7. Its record: runs/r02_simulate_task_workflow.

## Q1 · C1 Frame

Frame after its step ran: your filled prompt, then the agreed question and your three answers. Passed round 2 at 8.1. At the build, your sent Goal, Use cases and Constraints become plain rows.

**Build C1 Frame as drawn?**

- [x] A · Yes: build it as drawn, with the small fix above.
  ![A](option-q1-a.png)
- [ ] B · Not yet: change it first; my note says what.

Why A: It passed every rubric, and the fix undoes nothing.

## Q2 · C2 Report

Your five Results: the interaction report per loop, typical, hard and random cases, and the guideline rules as a mind map with versions. Passed round 1 at 8.1. At the build, report-03's questions show in its row.

**Build C2 Report as drawn?**

- [x] A · Yes: build it as drawn, with the small fix above.
  ![A](option-q2-a.png)
- [ ] B · Not yet: change it first; my note says what.

Why A: It passed every rubric, and the fix undoes nothing.

## Q3 · C3 Preferences

You answer report-03's cards, then copy the prompt that sends your answers and notes to the chat. Passed round 3 at 8.4; the simulation then tagged each card with its round report, e02.

**Build C3 Preferences as drawn?**

- [x] A · Yes: build it as drawn, changed only by Q5.
  ![A](option-q3-a.png)
- [ ] B · Not yet: change it first; my note says what.

Why A: It passed every rubric; Q5 settles its one open point.

## Q4 · D3 Evaluate

Expression's Evaluate: the round report first, sent to meaning with a link there, then the error counts and the models' table. Passed round 2 at 8.0; it since gained your prompt box.

**Build D3 Evaluate as drawn?**

- [x] A · Yes: build it as drawn, changed only by Q7.
  ![A](option-q4-a.png)
- [ ] B · Not yet: change it first; my note says what.

Why A: It passed every rubric; Q7 settles how a round starts.

## Q5 · One send

In the simulation, Preferences sent your answers twice: the card's Submit feedback, then the prompt box. Update could also start twice: from that prompt and from Update's own.

```text
now  answer → Submit feedback, paste → Copy prompt, paste → Update
A    answer → Copy prompt (answers + notes + start Update), paste
```

**One send in Preferences?**

- [x] A · Yes: the prompt box sends answers and notes, and starts Update.
- [ ] B · No: keep Submit feedback and the prompt box apart.

Why A: One paste instead of two; Update's own prompt stays for reruns.

## Q6 · Approve m03

The simulated user could not tell whether m03 was approved: Update has no approve control, yet expression's strip says "approved meaning". A sign in Update would make it explicit.

**Add an Approve m03 sign to Update?**

- [x] A · Yes: a sign in Update; expression starts only after it.
- [ ] B · No: your answers approve; Update only applies them.

Why A: Expression must never run on a meaning you have not seen.

## Q7 · One round prompt

An expression round needed three pastes, Rewrite, Run and Evaluate, though the round never asks you anything. One prompt could run all three and stop at the round report.

**Start a whole expression round from one prompt?**

- [x] A · Yes: Rewrite's prompt runs the round to its round report.
- [ ] B · No: one prompt per step, as the slides show.

Why A: Three pastes become one; Run and Evaluate keep prompts for reruns.
