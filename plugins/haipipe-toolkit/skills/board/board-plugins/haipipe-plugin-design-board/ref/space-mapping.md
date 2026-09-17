# Design Board plugin · Space ↔ file map at board grain

| Space | Reads | Shows | Links down to |
| --- | --- | --- | --- |
| Goal Space | `0-BR-brief/*/BR00-brief.md` (the list of design tasks); `board.md` `reads:`; each folder's register and adopt decisions for the counts | one line per task: who · their job · venue · how many (wanted · registered · adopted) · insight board · folder · status; folders the Brief does not list; the New design tasks form; the Insight board line | Page-level Goal Space of that folder |
| Design Space | every `2-Design/*/` folder's register and Runs | every Design Item with folder, state, and who is waited on | Page-level Design Space of that folder (`?item=`) |
| Insight Space | every Insight board named by `reads:` or by a Brief line; each signed page's `signed:` and Design Handoff `FINDING`; each folder's evidence lines | per board: insight · signed · what it says · used by (folder · item) | the Insight plugin (`live_url` of the board) |
| Run Space | every folder's `runs/`, `results/*/runtime.yaml`, `result.yaml`, `decision.yaml` | the waiting queue (person first, then agent); every Run newest first with folder, step, who, status, outcome; the records check across folders | Page-level Run Space of that folder (`?item=`) |
| Delivery Space | every folder's adopt `decision.yaml` and the pinned draft | one card per adopted item; a line naming the items not adopted | Page-level Delivery Space of that folder |

Header: title · counts (design tasks, wanted, registered, adopted, waiting on
the person, on the agent) · the records check when it has findings.

## The list of design tasks

The first Markdown table in the Brief whose header contains `audience`:

```text
| line | audience | job | venue | designs | insight | folder |
|---|---|---|---|---|---|---|
| R1 | full SMSR2 population | prescription review | sms | 10 |  | `Design-01-patient-confirm-sms` |
| R4 | young male, age 35 or under | prescription review | sms | 10 | `DesignPlugin-Demo-260916-InsightBoard` | — |
```

Columns match by header word (`audience`, `job`, `venue`, `designs` or
`wanted`, `insight`, `folder`; the first column is the line id). `—`, `-`, or
an empty folder cell means "no folder yet"; an empty insight cell means the
board's `reads:`. Line status is derived: `no folder yet`, `folder missing on
disk`, the Page level's refusal reason for a legacy folder, or a count of item
states (`1 adopted · 1 verified`).

## The two writes

`add-tasks` `{subgroups, job, venue, designs, insight, open}`: one new line
per subgroup, ids continuing `R<N>`; missing `designs` / `insight` / `folder`
columns are added to the table, and the section is created when the Brief has
no list; with `open` = yes each new line gets a folder at once. Refused, and
nothing written, without a subgroup, job, or venue, with `designs` below 1,
or when the Insight board named is not beside this board.

`new-folder` `{row}`: creates `2-Design/Design-NN-<audience-slug>-<job-slug>-<venue>/`
with a `folder-kind: design` page and an empty register, then writes the
folder name into the line's `folder` cell. Refused when the line already
names a folder or is not in the Brief.

Neither write exists on the static `board/design.html`.

## Routes

```text
GET  /_board/design-board?path=/…/board.md[&space=goal|design|insight|run|delivery]
GET  /_board/design-board?board=<folder name>          short link
GET  /_board/design-board                              bare link: the server's only DesignBoard (the root itself, or the single one under it)
GET  /_board/design?folder=<Design-NN-…>[&space=…]     short Page-level link; 302 to the full path= & file= link
GET  /_board/design-bundle?path=/…/board.md            csv of every adopted draft (the send-system hand-off)
POST /_board/design-board       {path}                 -> the live URL (plugin menu)
POST /_board/design-board-act   {path, action, …}      -> add-tasks · new-folder
board/design.html                                       static twin, built with the Board site
```

`?space=` aliases: `brief, tasks, frame, plan → goal`; `intent, items → design`;
`signal, evidence, insights → insight`; `runs, queue, waiting, workflow → run`;
`adopted, launch → delivery`. Default `goal`.
