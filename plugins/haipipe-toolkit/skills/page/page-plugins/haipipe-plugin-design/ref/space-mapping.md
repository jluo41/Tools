# Design plugin · Space ↔ file map and the state fold

Each Space includes a read-only Run Type guide, followed by a separate latest
matching-record list. Goal: Commission. Design/Insight/Run: Commission,
Generate, Verify. Delivery: Generate/Verify for ready items. Each type names
its canonical identity, bounded work, owner/worker Skills, actor and prerequisites.
Only eligible native item controls in live Design Space are labeled `Start here`;
eligible Generate/Verify items additionally offer `Copy request → paste and send`.
Other guidance is `Shown here · read-only`. Expanding guidance has no side effects.

Open item cards explain the next eligible Run (or current Run/repair wait),
the released Commission and latest draft, then the latest matching record.
This description reads the native action-state rules; it cannot authorize a
Run. Run Space keeps the full ledger, including canonical Type and target;
Delivery remains read-only. Static cards omit mutation forms and batch controls.

**Copy prompt to chat** appears only in live Design Space for an eligible new
Generate/Verify or a compatible planned Run. Its preview binds the Board,
Folder, Page, item, target, Type, Skills, prerequisites, Commission, actual
matching Run/receipt and next action. Copying only changes the clipboard.
The prompt rereads state, reuses the queued identity, stops if state changes,
keeps Commission human-only, requires a fresh independent Verify context,
and reports one Run's id/receipt. No Commission, running, stale, blocked,
unresolved, invalid, ready, retired or static state has a prompt. Folder audit
findings or missing/blocked Insight bindings also suppress it. Revisions must
first pin feedback/base through the native queue form. Run/Delivery offer no copy.

| Space | Reads | Shows | Writes through |
| --- | --- | --- | --- |
| Goal Space | the Brief line whose `folder` names this folder (`0-BR-brief/*/BR00-brief.md`, the first table whose header names `audience`, `job` and `venue` together; columns `audience`, `job`, `venue`, `designs`, `insight`, `folder` by header word); `board.md` `reads:` | one sentence (N venue designs for who, their job) · venue · who · their job · how many (wanted · registered · ready, and declined when > 0) · from (the Brief file · design tasks) · the Insight board and its signed count | `haipipe-plugin-design-board` (adds the line, writes the folder cell), `haipipe-design-brief` (the Brief's prose), the owning board (`reads:`) |
| Design Space | `outline/<stem>-design-items.md`; every run record's `item:`; the candidate Result's hash-bound `render_manifest` for a screen's picture | one fixed-height foldable row per item (id · title · the design in one line · state · waiting on); opened, the design on the left, kept in view, with the handoff shown under a ready design and a two-column table on the right: Why this design · From insight to design (Data → Information → Knowledge → Wisdom → Also read → This design) · The bet (only when the item has one) · Rules (✓/✗) · Runs; retired items are folded after the live ones | `haipipe-design` (register), `haipipe-design-workflow` (Commission, Generate, Verify) |
| Insight Space | the register's `evidence:` lines; the pages they name (`signed:`, the Design Handoff block's `FINDING` / `CONSEQUENCE`, else the first Opening line when it is not a question, else the title); run records' `inputs` for the pin; the Insight board's signed pages | per item: insight (label and title, with its role in plain words, e.g. signed insight) · signed (by whom, when) · what it says · rules it implies · pinned in the run record; "needs an insight" in red for an evidence-informed item with none; "Available, unused" for signed pages no item uses, or "none · every signed insight is used by an item" | the Insight plugin (signing), `haipipe-design` (evidence lines) |
| Run Space | `runs/rdNN_*.yaml`, `scripts/config/`, `results/*/runtime.yaml`, `result.yaml`, `checks.yaml`, `content/*`, Commission `decision.yaml`, `outline/feedback/<run>.md` | per item: run · Run type (`Generate · revise of rdNN` for a revise) · who (human/agent) · when · status · outcome (verdict n/m) · next; folded checks (each named by its rule in words), feedback, and draft text; failed runs and fail verdicts in red, superseded runs grey with their reason; the records check | `haipipe-design-workflow` (Generate, Verify) |
| Delivery Space | the register (id, title); the candidate whose independent Verify passed; the candidate Result's `render_manifest` (legacy Delivery manifest as fallback) | one table, one row per ready item: item (id · title) · design (the text as sent, with the SMS `link` mark); a folder of ready screens as a picture gallery; no status, hash, or receipt | — (read only) |

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
| stance | follows the evidence / challenges the evidence / explores a new direction / a new design |
| basis | built on evidence / from the brief only |
| mode | never on screen; it stays in the files |
| `FW01` (an insight page's file id) | its label and title, `full-W01 · Send salience` |
| `R1` (a Brief line id) | the task's full name, `<job> <venue> for <who>` |

The contract word never appears beside its plain word, in parentheses or
otherwise. The New Design Item form uses the same plain labels (approach,
built on, expected, wrong if, insights, rules); the contract words are only
the option values.

## State fold

Walk an item's Runs in `rdNN` order; the last row wins. A superseded run is
skipped.

| Run seen | status / outcome | item state | waiting on |
|---|---|---|---|
| none | | not commissioned | person · commission |
| Commission | no decision yet | commission open | person · release or hold |
| Commission | release | commissioned | person · queue the draft |
| Commission | hold | commission held (a new release decision is offered) | person · release or hold |
| Generate | planned | generate queued | agent · generate |
| Generate | planned, a pinned file changed since | queued run out of date | person · queue again |
| Generate | running | generating | agent · running |
| Generate | complete | generated | person · queue the review |
| Generate | failed (the draft failed the records check) | generate failed | person · queue a revise |
| Verify | planned | verify queued | agent · verify |
| Verify | planned, a pinned file changed since | queued run out of date | person · queue again |
| Verify | running | verifying | agent · running |
| Verify | complete · pass, exact Result pins still valid | ready | — |
| Verify | previously passed, candidate/review records changed | records invalid | person · inspect the named records; no handoff |
| Verify | complete · fail | verify failed | person · queue a revise |
| Verify | failed (the review itself failed the records check) | verify invalid | person · queue the review again |
| any | blocked | blocked | person · resolve `<Run id>`: `failure:` |

"person" is the named human seen on this folder's decision Runs (for example
`JL`), never a role invented by the tab. "agent" is waited on only while a run
is queued or running. A blocked Run shows its reason and repair owner, never
a Commission Release button. A worker hold diagnostic does not record a human
HOLD decision. Run Space retains all real ids, including explicitly labeled
historical Adopt records; it never invents a Delivery Run id.

## Query aliases

`?space=` accepts `goal | design | insight | run | delivery` (default `goal`).
Old values still resolve: `frame, plan, brief, ask → goal`;
`intent, draft, items → design`; `signal, evidence, insights → insight`;
`runs, shape, workflow, runtime, create, review → run`;
`launch, commit → delivery`. `?item=ITEM02` opens that item's card in Design
Space, marks its row with an accent bar, and scrolls to it; Insight Space and
Run Space narrow to it under a line "showing ITEM02 only · show every item".
After a click, every item button lands back on Design Space at that item; a
draft request lands on Goal Space. The retired
`?flow=` parameter is ignored.
