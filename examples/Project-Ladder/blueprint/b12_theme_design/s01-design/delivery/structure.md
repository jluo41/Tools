# Design Board

One application in one channel. Each Job pins one goal × one method version × one inputs version.

## Job / Task Organization

Drawn as b17's folder tree (`delivery/structure/build_organization.py`, trace 261127/1305): Structure and Draw
show the naming rules. Structure embeds the corresponding real Design-Example records beside each rule and includes the live Block. Four levels; the two groups are authored
organization, not types.

```text
Design Board
└── 〈Method family〉                         Job group · optional
    └── 〈goal〉 · 〈M0x mK〉 · 〈inputs-vM〉     Job name
        ├── Ideas      ─ reason ideas          Task group ─ Task name
        ├── Designs    ─ 〈design name〉 …
        └── Review     ─ review whole
```

**Job group:** the pinned method's family from the method registry (`family:` in
`hai-design-method/methods/M0x-*/method.md`): j01 and j02 pin M01 (Goal Only), j03 pins M02 (Internal).
Every Board Job holds the same folders whatever its method, so there is one kind of Job.

**Job name:** `jNN · 〈goal〉 · 〈M0x mK〉 · 〈inputs-vM〉`, the selector's label (`j03 · G01 · M02 m1 · inputs-v2`);
the folder keeps `jNN_〈goal〉_M0x-〈method〉-mK_inputs-vM`, the face's heading the goal and method in words.

**Task group:** Ideas (`t00_reason-ideas`), Designs (`tNN_dNN_〈design〉`), Review (`t99_review-whole`), fixed.
Generate, verify and revise are Runs inside a Design Task, not more Tasks.

**Task name:** `reason ideas`, the design's short name kept through revision, `review whole`. A new idea makes
a new Design Task; another draft stays in the same Task.

### Actual Folder

```text
Design-Example/
└── j03_confirm-by-reply_M02-overall-performance-m1_inputs-v2/
    ├── t00_reason-ideas/
    ├── t01_d01_reply-first-short/
    ├── t02_d02_reminder-one-ask/
    └── t99_review-whole/
```

These are existing directories. Structure and Draw describe them; neither renames them.
Existing Task faces carry `task-type: design-reason` for reason ideas, `design-item` for each design and `design-whole` for review whole. These types are distinct from the Ideas, Designs and Review groups. Job type is a contract role; no new field is added by the diagram.

## Main and a selected Task

The shared horizontal rows are Job topic → Job → Main or Task topic → Task.
Main hides the Task row. Selecting a Task keeps the owning Block title and route.

**Main design:** Overview / Tasks / Findings. Overview holds the goal, pinned method and inputs,
and the next required action. Tasks groups Ideas, Designs and Review. Findings holds the kept
designs, ranking, predictions, observed comparisons and release output when present. A review
control sits beside the content it signs. Empty material is omitted.

**Current example:** the embedded Main already gathers these records, with separate Brief,
Tasks, Kept designs, Ranking, Predicted vs observed, Review and approve or Delivery, Workflow
and Runs sections when populated. Consolidating them into the three bands above belongs to
the separate Job Main plan; this structure Studio does not claim that consolidation is live.

A selected Ideas Task shows its inputs and reasoning. A selected design Task shows its draft,
element rationale, verification, revision history and prediction. Review shows the whole-set
ranking. The existing step controls and Runs remain inside that Task's panel.

Hard Runs expose their immutable result after closing. Soft Runs keep passes. Job setup,
freeze and release Runs belong to the Job; generation, verification and revision belong to
their design Task. Block-wide input and observation Runs remain on the Block.

## Studio organization

Studio topics sit beside the Jobs or Tasks they serve: `sNN-〈topic〉/` at Block, Job or Task level.
Block topics belong to the Design Board; Job topics to a Board Job;
Task topics to the specific reasoning, design or whole-set review Task that uses their delivery.
Numbering is shared across the Block. A topic is discussion and design, never an execution Task.

This type's structure Studio has Structure, Draw and Skills on top. Each Structure entry includes its real example; the named example entry embeds the live Block.
Several entries in a view use the shared left tabs; one entry uses the full content width.
Skills is a view in this Studio. It does not introduce another Studio per skill.

Studio Band names and order are read from b17's s71–s79 definitions through its shared builder. Empty Bands on a real Block remain omitted by the shared page.

## Sources

- Contract: `plugins/haipipe-toolkit/skills/3_theme/design/hai-design/ref/design-ladder.md`, The tree and Runs.
- Grouping and embedded content: `plugins/haipipe-toolkit/servers/workbench-design/design_jobs.py`.
- Shared authored views: `plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_views.py`.
- Example 1: `examples/Project-Ladder/design/Design-Example/`, rendered live inside Structure.
- Historical decisions remain in this topic's face; its earlier drawings and Q01–Q03 references are retained.

### Evidence and unresolved schema

The four-item mapping is supported by `hai-design/ref/design-ladder.md:26–65`, its naming rule
at `:91–97`, `hai-design-unit/SKILL.md` (reason, generate, revise, verify and rank), and the
real Job and four Task faces in the Folder above. `design_jobs.py:25–48` supplies the current groups
and selector labels. The current contract and example agree on these roles.

There is no serialized Job group / Task group field in these faces. A future schema enum
needs an owning-contract decision; this diagram does not silently create one.

Recheck both Studios with `python delivery/structure/build_organization.py --check` from this blueprint Block.
