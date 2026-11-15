# Questions lead progress

Part of the [Workbench base README](../README.md).

The primary reading is: **what is the question, what answer do we have, what
supports it, and what remains open?** Related execution is shown as Work.
Question progress can come from design reasoning, an Insight report, a paper
claim, evidence review or other records owned by that workflow.

Paper's existing folding layout is the reference:

```text
Question                                  closed: answer + remaining issue
└── Expanded question
    ├── Answer and reasoning               hypotheses / claims / evidence
    └── Related Work
        ├── Shared preparation             also for another question
        └── Expanded Work
            └── Block
                └── Job
                    ├── Task               expands its Runs
                    │   └── Run            receipt + Result
                    └── Another Task
```

Jobs, Tasks and Runs stay together in this hierarchy. The reader can open a
Question, then its Work, then a Task's Runs without switching between separate
execution tabs. Closed Questions lead with the current answer and open issue;
closed Work keeps its role and references visible.

- A Question can have reasoning or a Report before it has any BJTR work.
- Work can support several Questions. Its native owner is retained; other
  Questions refer to it.
- Work without a Question remains visible under Paper's existing
  **Not under a question** fold.
- A completed Run contributes an execution receipt. The question's answer,
  evidence and remaining review are read from the owning Question / Report.
- The answer states in the drawing are illustrative. Each family keeps its
  native marks and acceptance rules; this proposal introduces no universal
  question-status enum or question database.

## Family examples

| Family / Space / View | Proposed reading |
|---|---|
| Paper / Story / High-level logic + low-level work | Collapsible Questions. An open Question shows reasoning beside Work; BJTR is nested together inside that Work. |
| Insight / Insight / Questions | Keep the partition's Logic / Work / Report columns and DIKW folds. The Question and its answer lead; related Runs and Reports stay alongside it. |
| Task / Task / each group | Insight's partition table: one View per register `group:`, a row per Question with Logic / Work / Report columns. Report Pages live in `reports/`; the Block's drawings, the generated question map first, are Scope › RoadMap Draw (`studio/`). |
| Other family-owned working Views | Place goals, design questions, Studio, evidence and checks according to the family's native workflow. |

The components may be reused across families. The layout, question semantics,
source files, actions and Run Type skill declarations stay with their owners.
This design creates no copied ledger or required `goal/`, `design/` or
`checklist/` directories. A working Studio retains its existing owner contract
for drawing and chat.

All example questions, names, counts and states are illustrative.
