# Design plugin · Space ↔ file map and the state fold

| Space | Reads | Shows | Writes through |
| --- | --- | --- | --- |
| Goal Space | the Brief line whose `folder` names this folder (`0-BR-brief/*/BR00-brief.md`, first table whose header says `audience`; columns `audience`, `job`, `venue`, `designs`, `folder` by header word); `board.md` `reads:` | one sentence (N venue designs for who, their job) · venue · who · their job · how many (wanted · registered · adopted) · from (Brief, line) · the Insight board and its signed count | `haipipe-design-brief` (the line), the owning board (`reads:`) |
| Design Space | `outline/<stem>-design-items.md`; every run record's `item:` | one card per item: id · title · state · waiting on · type · who · job · the latest or adopted draft · goal · why (plain words) · insight pointer · predict · rules · runs · buttons | `haipipe-design` (register), `haipipe-design-workflow` (Commission, Adopt) |
| Insight Space | the register's `evidence:` lines; the pages they name (`signed:`, the Design Handoff block's `FINDING` / `CONSEQUENCE`, else the first Opening line); run records' `inputs` for the pin; the Insight board's signed pages | per item: insight (role word · page) · signed (by whom, when) · what it says · pinned in the run record; "needs an insight" in red for an evidence-informed item with none; "Available, unused" for signed pages no item uses | the Insight plugin (signing), `haipipe-design` (evidence lines) |
| Run Space | `runs/rdNN_*.yaml`, `scripts/config/`, `results/*/runtime.yaml`, `result.yaml`, `checks.yaml`, `content/*`, `decision.yaml` | per item: run · step · who (human/agent) · when · status · outcome (verdict n/m) · next; folded checks and draft text; the records check | `haipipe-design-workflow` (Generate, Verify, Adopt) |
| Delivery Space | `results/rdNN_adopt_*/decision.yaml` (draft pin), the pinned `content/*`, `delivery/render/` | one card per adopted item: text · draft run · sha256 · verifier · preview · words · adopter · time | `fn/render.md`, `Design.adopt` |

Header (above the Spaces): `Page level · <folder> · ↑ Board level`. A red
line only for a legacy folder or an unsigned Insight page.

## Plain words

| in the files | on the screen |
|---|---|
| `roster` | the Brief, a line of the Brief |
| `handoff` | signed insight |
| Ticket | run record |
| candidate | draft |
| `check_unit` | records check |
| `intent` / `move` | goal |
| stance · basis · mode | follows the evidence / challenges the evidence / explores a new direction / new design from the brief · built on evidence / from the brief only · written fresh / revised from an earlier draft / written to test the evidence / many rough options / derived from a stated theory (contract words in parentheses) |

## State fold

Walk an item's Runs in `rdNN` order; the last row wins.

| Run seen | status / outcome | item state | waiting on |
|---|---|---|---|
| none | | not commissioned | person · commission |
| Commission | release | commissioned | agent · generate |
| Commission | hold | hold | owner · commission |
| Generate | complete | generated | agent · verify |
| Generate | failed | generate failed | agent · revise |
| Generate | planned | generate queued | agent · generate |
| Generate | running | generating | agent · running |
| Verify | complete · pass | verified | person · adopt |
| Verify | complete · fail | verify failed | agent · revise |
| Verify | failed (the review itself failed the gate) | verify invalid | agent · verify |
| Verify | planned | verify queued | agent · verify |
| Verify | running | verifying | agent · running |
| Adopt | adopt | adopted | — |
| Adopt | decline | declined | — |
| Adopt | revise | revise requested | agent · generate |
| Adopt | hold | hold | owner · adopt |
| any | blocked | hold | person · `failure:` |

"person" is the named human seen on this folder's decision Runs (for example
`JL`), never a role invented by the tab.

## Query aliases

`?space=` accepts `goal | design | insight | run | delivery` (default `goal`).
Old values still resolve: `frame, plan, brief, ask → goal`;
`intent, draft, items → design`; `signal, evidence, insights → insight`;
`runs, shape, workflow, runtime, create, review → run`;
`launch, commit → delivery`. `?item=ITEM02` highlights that item in Design
Space and narrows Insight Space and Run Space to it. The retired `?flow=`
parameter is ignored.
