# Design Board workbench · Space ↔ file map at board grain

The folded Run Type guide is separate from current matching records. It uses
the Page-level Design descriptions (name/canonical Type, bounded work,
owner/worker Skills, actor, prerequisites); Board capability is
`Shown here · read-only`, with `Copy request → paste and send` for eligible
Generate/Verify work in Design Space. Matching records retain folder/item
scope, real id, status, outcome and actor. Goal covers Commission;
Design/Insight/Run cover all three current types; Delivery covers only the
Generate/Verify support for ready items.

Design Item rows explain the next eligible Run and link to **Open item
controls** in the owning Page's Design Space. Native gates remain there;
Board task/folder operations remain separate from Run allocation. Run Space
keeps its history/status ledger.

The per-item **Copy prompt to chat** action uses its Folder's Page snapshot
and the same eligibility/prompt builder as the Page workbench. A reviewable prompt
names the exact item, target, Type, Skills, prerequisites, Commission, matching
Run/receipt and next action. It instructs chat to reread state, reuse an existing
queued identity, preserve the human Commission and independent Verify gates,
and report one Run's id/receipt. Copying changes only the clipboard; pasting and
sending remain manual. Native controls stay on the owning Page. Commission,
running, stale, blocked, unresolved, invalid, ready, retired or static states,
folder audit findings and missing/blocked Insight bindings have no prompt.
Revisions require native queueing with feedback first. Run/Delivery have no copy.

| Space | Reads | Shows | Links down to |
| --- | --- | --- | --- |
| Goal Space | `0-BR-brief/*/BR00-brief.md` (the list of design tasks); `board.md` `reads:`; each folder's register and independent Verify results for the counts | one line per task, by its full name `<job> <venue> for <who>` (never its line id) · how many (wanted · registered · ready) · insight board · folder · status; folders the Brief does not list; the New design tasks form; the Insight board line | Page-level Goal Space of that folder |
| Design Space | every `2-Design/*/` folder's register and Runs | every Design Item with folder, item, its title with the design text in one line under it, state, and who is waited on | Page-level Design Space of that folder (`?item=`) |
| Insight Space | every Insight board named by `reads:` or by a Brief line; each signed page's `signed:` and Design Handoff `FINDING`; each folder's evidence lines | per board: insight (title, label under it) · signed · what it says · rules it implies · used by, grouped per folder (`Design-01 · 6 items`, linked to that folder's Insight Space); a second table "Other pages the designs use (not signed insights)"; a red line when no design rests on a signed insight | the Insight workbench (`live_url` of the board) |
| Run Space | every folder's `runs/`, `results/*/runtime.yaml`, `result.yaml`, `decision.yaml` | the next-action queue (person first, then agent); every Run newest first with folder, original Run ID, Run type, who, status, outcome; the records check across folders | Page-level Run Space of that folder (`?item=`) |
| Delivery Space | every folder's register and each item's exact Verify-passed draft; its Result-local render manifest (legacy Delivery manifest as fallback) | one table per folder: item (id · title) · design text, or a picture gallery for a folder of screens; declined items folded under "Declined, kept for the record"; the csv link | Page-level Delivery Space of that folder |

Header: one line, `Board level · N design tasks · N wanted · N registered ·
N ready · waiting on <person>: N · on agent: N`, below the board's title; a
red line is added only when the records check has findings.

## The list of design tasks

The first Markdown table in the Brief whose header names `audience`, `job`
and `venue` together:

```text
| line | audience | job | venue | designs | insight | folder |
|---|---|---|---|---|---|---|
| R1 | all patients | prescription review | sms | 10 |  | `Design-01-all-patients-prescription-review-sms` |
| R4 | young male, age 35 or under | prescription review | sms | 10 | `DesignWorkbench-Demo-260916-InsightBoard` | — |
```

Columns match by header word (`audience`, `job`, `venue`, `designs` or
`wanted` or `how many`, `insight`, `folder`; the line id is the column headed
`line`, `row`, `id`, `#`, or `page`). A Brief with no line-id column still
works: its rows are numbered R1, R2 … in order. The id is a key in the file,
never a name on screen. `—`, `-`, or an empty folder cell means "no folder
yet"; an empty insight cell means the board's `reads:`. Line status is
derived: `no folder yet`, `folder missing on disk`, the Page level's refusal
reason for a legacy folder, or a count of item states (`1 ready · 9
generated`).

## The two writes

`add-tasks` `{subgroups, job, venue, designs, insight, open}`: one new line
per subgroup, ids continuing `R<N>`; missing `designs` / `insight` / `folder`
columns are added to the table, and the section is created (`### What to
design`) when the Brief has no list; with `open` = yes each new line gets a
folder at once. Refused, and nothing written, without a subgroup, job, or
venue, with `designs` below 1, or when the Insight board named does not
resolve from this board (a sibling name, or a relative path as on `reads:`).
The form's picker offers only names that resolve to an Insight board, each
shown by its folder name.

`new-folder` `{row}`: `row` is the parsed Brief row's `id`, for example
`{"row":"R3"}`; never pass a display title or integer position. Creates
`2-Design/Design-NN-<audience-slug>-<job-slug>-<venue>/`
with a page that passes the board checker (`folder-kind: design`,
`state: 🔴 OPEN · no design registered yet`, `owner:` from board.md else the
Brief, an Opening question "Which N <job> <venue> designs should we make for
<audience>?") and an empty register, writes the folder name into the line's
`folder` cell, and lists the page in board.md `## Pages` under its Design
heading. Refused when the line already names a folder (so a second click
opens no duplicate) or is not in the Brief; a refusal names the task by its
full name, never `R3`.

Neither write exists on the static `board/design.html`.

## Routes

```text
GET  /_board/design-board?path=/…/board.md[&space=goal|design|insight|run|delivery]
GET  /_board/design-board?board=<folder name>          short link
GET  /_board/design-board                              bare link: the server's only DesignBoard (the root itself, or the single one under it); with several, a list of them (200)
GET  /_board/design?folder=<Design-NN-…>[&space=…]     short Page-level link; 302 to the full path= & file= link; several boards hold it: 404 page listing each, never a guess
GET  /_board/design-bundle?path=/…/board.md            csv, one row per independently verified ready item; no failed or unverified drafts; downstream owners decide sending
POST /_board/design-board       {path}                 -> the live URL (workbench menu)
POST /_board/design-board-act   {path, action, …}      -> add-tasks · new-folder
board/design.html                                       static twin, built with the Board site
```

`?space=` aliases: `brief, tasks, frame, plan → goal`; `intent, items → design`;
`signal, evidence, insights → insight`; `runs, queue, waiting, workflow → run`;
`ready, launch → delivery`. Default `goal`.
