# A Task folder, on one page

Replaces the retired `haipipe-folder` skill (JL 261016: "it is too large, it is only for the haipipe-draft-folder,
please rethink about it"). It said every Folder has two faces and an owner skill with nine required sections; no owner
followed that, so only what the code and the people use is kept here.

## The parts, one writer each

Every Task folder follows one rule: a Task may hold a draft; a Task is not a Page (JL 261011).

```text
tNN_<task>/
├── tNN_<task>.md   the face: title, task-type (draft, evidence, …), what it answers, its state
├── draft/          haipipe-draft-writing   the plan, the scratch, the text
├── evidence/       haipipe-evidence        cards.yaml (CITE, WORK) · proposals.md
├── display/        haipipe-display         one unit per figure or table, built on evidence/
└── runs/           each Run's ticket and its result/, written by the Run's own skill
```

1. **One writer per folder**: a part is changed only by its skill; the others read it.
2. **One direction**: evidence → display → draft; nothing writes back up the chain.
3. **Delivery belongs to the Block**: built files go to `<block>/delivery/jNN_<job>/tNN_<task>/<lane>/`, never into the
   Task (JL 261010).
4. **A Task does not hold a Page Folder**: the parent `jNN_<job>/` is only the Job container.

## The face's header lines a server reads

A skill that owns a kind of folder (today the six insight folder kinds and Discovery) says so in its own SKILL.md
header, under `metadata:`. `src/folder_contract.py` reads these lines to pick the folder's screen and owner:

```yaml
metadata:
  workflow: haipipe-insight-workflow   # the *-workflow skill that runs it
  folder_kind: knowledge               # kebab-case; the face's `folder-kind:` line selects it
  primary_face: page                   # page or task: which face a reader opens first
  page_ruling: none                    # none, domain-gate or local
  legacy_page_type: knowledge          # optional: an old page-type that resolves to the same owner
```

A folder says which kind it is in `workflow/folder.yaml` (`current: {folder-kind: <kind>}`); when that file is absent,
its face's front matter may declare the kind, or an older `page-type:` resolves to the same owner. A present
`folder.yaml` that is malformed is an error, never a reason to fall back. Nothing else about a folder's or an owner's
sections is required.
