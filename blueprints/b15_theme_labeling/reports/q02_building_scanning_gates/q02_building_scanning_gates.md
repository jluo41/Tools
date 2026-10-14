# Where do the two sides and the human gates show?
state: 🔴 OPEN
answers: Q02
answer-status: open

## Opening

Proposed (261014), waiting for JL: the two sides are two **Task types** of the Job, split at the
signed Label Handoff: 🏗 building (`task-type: labeling-building`) and 🔍 scanning
(`task-type: labeling-scanning`). Each gate sits on its side's Task: Confirm meaning (G0) and Freeze in
building, the test lock and Audit in scanning. The Handoff is the one crossing: building's Delivery
hands it on, scanning's Description reads it. Today's one labeling Page is both sides at once, and the
workbench shows its views in that order.

**Where this Page sits:** [Q02 · How do Building and Scanning, and the human gates between them (Confirm meaning, freeze, test lock, audit), appear in the six Spaces?](../../board.md).

**Why it matters:** the Task types (s13) and the gates decide where a person acts and where the frozen meaning crosses to the executors.

## Content

### Answer

```text
side        its Task              Work views (in order)                              gates            Delivery
🏗 building  labeling-building     Preparation · Embedding · Definition · Rounds ·    G0 · Freeze      Handoff
                                  Guideline
     ── 🔒 signed Label Handoff ──▶ (scanning's Description › Handoff reads it)
🔍 scanning  labeling-scanning     Test · Evaluation · Scan · Audit                   test lock ·      Final labels
                                                                                     Audit
(today)     labeling              both rows, building first                          all four         both
```

Scan moved from Delivery into Work: it is a scanning step, and Delivery keeps only what leaves the Task
(the Handoff, the final labels). A person works in a building Task's Rounds (its 🏷 Label button) and in
a scanning Task's Audit (🔍 Audit). A scanning Task with no labeling Page of its own reads the job whose
Page sits in the same Job.

### Evidence

- [labeling Task types](../../studio/s13-labeling-task/s13-labeling-task.excalidraw): building and
  scanning as two steps, the Handoff between them as the key point.
- Code: `Tools/plugins/haipipe-toolkit/servers/workbench-labeling/labeling_theme.py` (`BUILD_WORK`,
  `SCAN_WORK`, `_task_spaces`, `task_action`); test `test_a_scanning_task_carries_out_the_jobs_labeling_job`.

### Limits

1. **One lane per Page.** The engine keeps one `labeling/` lane per Page, so a separate scanning Task
   has no lane of its own yet; it links to the building Page's views (s13 Open 2).
2. **Where a gate shows.** Each gate is a view today (Definition for G0, Guideline for Freeze, Test,
   Audit); a gate chip on the Task's card in Job › Work is not built.

### Next

- JL: agree the split at the Handoff, or keep one Page with two rows (s13 Open 1).

