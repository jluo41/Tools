---
name: haipipe-design-brief
description: >-
  LEGACY, older boards only: owner of an older DesignBoard's one Brief Folder
  (0-BR-brief/): why the Application exists, for whom, the behavior/outcome and
  venue boundary, the insight needs it raises, and the list of designs it
  authorizes. On the design ladder the Block's goal list (haipipe-design-goal,
  board.md ## Goals) replaced it; never write a Brief on a ladder Block.
  Trigger: design brief, application brief, folder-kind brief,
  /haipipe-design-brief.
metadata:
  version: "0.4.0"
  last_updated: "2026-09-28"
  folder_owner: canonical
  folder_kind: brief
  primary_face: page
  page_ruling: none
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Opportunity → Audience Set and Behavior → Outcome and Kill Criteria → Venue Scope → Promise → Insight Needs Raised → Frozen Signed-W Inputs → What to design"
---

# /haipipe-design-brief · frame the Application (older boards only)

> **Legacy (261007).** This skill serves an older board (`B00_DesignBoard-<name>/` with `0-BR-brief/`)
> until it is carried over. On the design ladder (`haipipe-design/ref/design-ladder.md`) the Block's goal
> list replaced the Brief: one signed goal per entry in `board.md ## Goals`, written by
> `run-add-goal-<goal>` (`haipipe-design-goal`). A ladder Block has no Brief Folder.

## Version governance

Version governance: this Design skill stays at `0.4.0`. Only explicit user approval may authorize `1.0.0`.

This Design family remains pre-1.0. Only explicit user approval may authorize
`1.0.0` or any higher major version. Architecture size, clean breaks, and
field-test repairs do not independently authorize a major-version jump.

Load `haipipe-folder`, `haipipe-page`, and `haipipe-design`. A current Brief
uses `folder-kind: brief` and its own Page workflow.

## Position

The Brief lives at `0-BR-brief/BR00-brief/` and is the board's only authority
for scope, promise, needs raised, and the list of designs. It is a precondition for
Design Commissions, not a Design workflow phase.

## Folder Kind

Brief says what the Application is building and for whom. It does not inventory
data, perform DIKW, decide a design direction, write content, or field an
experiment.

## Input

Two births are legal: `born-of: mandate` records a person's program decision;
`born-of: <W id list>` resolves signed Wisdom handoffs on boards named by
`reads:`. Evidence-first text is drafted from the handoffs and remains subject
to a person's edit.

## Page Face

Use the eight fixed divisions declared in metadata. Every insight need has a
stable QD/QI/QK/QW id, neutral wording, affected partition/audience, target
level, derived Question Group, and blocked Aim. The list of designs is one line per
audience × behavior job × primary venue.

The list of designs is a table under the `What to design` heading, and it is
the only table in the Brief whose header holds `audience`, `job` and `venue`
together; the Design workbenches read the first such table as the list, so no
other Brief table (an audience table under Audience Set and Behavior, say)
may put all three in its header. Columns are matched by header word:

```text
| line | audience | job | venue | designs | insight | folder |
|---|---|---|---|---|---|---|
| R1 | <audience a> | <job> | sms | 10 |  | `Design-01-<audience-a>-<job>-sms` |
| R2 | <audience b> | <job> | sms | 10 |  | — |
```

On a board with method folders (`2-Design-M<NN>-<slug>/`, see
`haipipe-design/ref/legacy/method-folders.md`) a row is a task, and its folder cell names the task's
`Design-NN-…` folder, the same name under every method. The method is the folder's, so a
`method` column is not read there; it stays for boards with only `2-Design/`.

- `line` (or `row`, `id`, `#`): the line id. A Brief with no such column
  still works; its rows are numbered R1, R2 … in order. The id is a key in
  the file and never a name on screen: a line shows by its full name,
  `<job> <venue> for <who>` (`<Job> SMS for <audience a>`).
- `audience`: who receives it, in plain words (`<audience a>`), never a
  data partition's internal name.
- `job`: what the recipient is trying to do; supplied `venue` guides cover
  `sms`, `ui-card`, `email`, `push`, `reminder`, `checklist`, `report`, and `dashboard`.
- `designs` (or `wanted`, `how many`): how many designs the line asks for.
- `insight`: the Insight board the line draws from; empty means the
  DesignBoard's `reads:`.
- `folder`: the Design Folder that keeps the line's promise; `—` means none
  yet.

Two writers touch this table. This skill owns the Brief's prose, needs, and
signed inputs, and may add or change any line. The Board-level Design workbench,
`workbench-design/ref/design-board.md`, also adds lines (`add-tasks`, ids continuing
`R<N>`, creating the section when the Brief has none) and writes a line's
`folder` cell when it opens that line's folder (`new-folder`); those cells and
lines are the only Brief edits it makes.

## Task Face

Resolve `born-of:` and `reads:`; reconcile opportunity, audience, behavior,
outcome/kill, venue, and promise; raise unanswered needs; bind already accepted
core inputs; and release the list of designs. Do not answer a need locally.

## Workbenches

- exact signed-W path/Page-version/signature/GI6 receipt required
  for evidence-first birth or accepted core inputs; PageX is invalid;
- `outline` required;
- upstream execution forbidden: missing insight is raised to the InsightBoard;
- `code` forbidden: the Brief frames work.

## Gate and Closure

The Brief is releasable when birth resolves, scope and kill criteria are
explicit, every load-bearing premise is a bound input or neutral need, and
every line has one audience/job/venue. The Page workflow releases that
exact version. No source inventory or preferred answer remains.

## Handoff

A Brief line reaches design through the Design Folder its `folder` cell names
and the Design Items registered there. A Commission pins its item's config and
the item's evidence files; it does not pin the Brief version, the board's
`reads:`, or venue packs.

## Clean break

Do not resolve `page-type: brief`, D0/GD0 records, PageX, or D1 handoffs. They
are unsupported and cannot authorize a current Commission.

## Files

- Page: `0-BR-brief/BR00-brief/BR00-brief.md`
- Cross-board inputs: frozen records in the Brief's current Context/Evidence workspace
