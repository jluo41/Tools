# Page workflow table · one control map for every Page skill set

This is the canonical Page workflow map. When InsightBoard, DesignBoard,
Labeling, Paper, or another family designs a Page-producing workflow, it fills
the Page Face owner and Folder-owner cells without changing this phase grammar.

Every row uses one dependency order. The table abbreviates the common prefix
and shows each phase's specific tail:

```text
haipipe-page
  → haipipe-page-workflow
  → current phase skill
  → Folder-owning workflow or canonical family skill
  → exact Page Face owner skill
  → phase references / narrative-style policy
  → haipipe-run + selected worker skills, only where Runs exist
```

For the first three phases, the exact phase references are
`haipipe-plugin-outline/ref/...` contracts. The Page surface installs the
shared presenter once; it is not an execution dependency appended to each row.

## Two paths through the same capabilities

**Interactive writing:** CONTEXT → [SHAPE Bullets ⇄ candidate prose ⇄ human
feedback] in one persistent Writing Run → human agreement → evidence
integration and CONTENT adoption → requested delivery → CHECK.
SURVEY/LAND may supply missing evidence alongside this loop. An evidence
contradiction returns to the affected human decision. See
`interactive-writing-run.md`; this is not a new linear phase stack.

**Delegated/formal lifecycle:** the phase controller below still governs
evidence execution, publication and whole-Page closure. Its receipts are not
human interaction Steps.

| Writing step | Input | Skill used | L3/current source change | L4/history outcome | Human-facing outcome |
|---|---|---|---|---|---|
| Start/resume | goal, current sources, effective decisions | `haipipe-page-workflow → haipipe-page-context` when context is stale | no unrelated rewrite; resolve current policy | one Run; open Version; saved initial input | Section Mermaid and selected review window |
| Shape + draft | rough intent or selected feedback; scoped Bullets/Evidence | `haipipe-page-outline → haipipe-writing` | working Shape + `<stem>-preview.md`; item requirements when needed | one Step with full output and reasons; no Run per paragraph | 1–3 full paragraphs beside their Bullets |
| Revise | original feedback items and reviewed output identity | `haipipe-writing`; `haipipe-page-outline` for dependent plan changes | only requested scope; accepted text protected | append Step; retain original comments and disposition | saved full passage, concise reasons, direct links |
| Agree/close | explicit scoped human acceptance and close | `haipipe-page-workflow` | no automatic whole-Page approval | seal Version with final passage and dependencies | writing-agreed, not necessarily publishable |
| Continue | same goal, explicit reopening | `haipipe-page-workflow` | reopen only named targets | next Version after closure; same Run across sessions | new review window with prior decisions retained |
| Adopt/deliver | agreed passage + ready evidence + approved Shape | `haipipe-page-content`, evidence/delivery workers as needed | exact accepted wording into Content; trace and exports | consume Writing Result, not a replacement writing Run | current delivery and independent CHECK when requested |

Routine edits use narrow read/save/check; exports and whole-Page audits are not
foreground prerequisites. Link/return rules live in
`../../../haipipe-page/ref/user-check-packet.md`.

## Architecture at a glance

| Index | Phase skill | Cycle(s) | Primary surface/plugin | Creates L4 Runs? |
|---:|---|---|---|---|
| `00` | `haipipe-page-context` | `PREPARE` | `haipipe-plugin-outline` → Context Workspace | No |
| `01` | `haipipe-page-outline` | `SHAPE`, `SURVEY` | `haipipe-plugin-outline` → Bullet + Evidence Workspaces | No; SURVEY designs them |
| `02` | `haipipe-page-evidence` | `LAND`, `EMBED` | `haipipe-plugin-outline` → Evidence + Bullet Workspaces | Yes in LAND; none in EMBED |
| `03` | `haipipe-page-content` | `WRITE` | Adopted Page Content + declared delivery | Consumes agreed Writing Results; optional independently commissioned delegated work |
| `04` | `haipipe-page-check` | `CHECK` | read-only whole-Page review + receipt | No |

The shared plugin does not merge phase authority. CONTEXT may write the Context
record, OUTLINE may write the plan and Run design, and EVIDENCE may bind/fold
ready Results. All three are viewed together because they are three views of
one Page planning process.

## Full workflow

| Index | Page phase / cycle | Objective | Required input | Exact skill chain | Outline plugin workspace | L3 Folder/Page content modified | L4 Runs commissioned or consumed | Exit evidence | Normal next authority |
|---:|---|---|---|---|---|---|---|---|---|
| `00` | `CONTEXT / PREPARE` | Make the governing context explicit before planning or writing. | Page + Folder identity; Folder owner; Page Face owner; policy; requirements; feedback; discussion; Files/Log/Skills; bounded related Page fragments; current plan/evidence/run receipts. | `haipipe-page-context → <Folder-owner> → <Page-Face-owner> → haipipe-plugin-outline/ref/record-shape.md` | `Context Workspace` | Generates `outline/<stem>-context.md`; reads the other Outline records without merging or replacing them. | **None.** Collect, Resolve, Freeze are planning movements. | Identity resolved; required sources addressed and fresh; missing/conflicting rows explicit; Context record generated. | `OUTLINE / SHAPE`; repeat `CONTEXT / PREPARE` or `HOLD` on unresolved input. |
| `01A` | `OUTLINE / SHAPE` | Agree what the Page will say and what ready evidence each Bullet expects. | Frozen Context record; Page Face owner outline grammar; current Page; prior plan; applicable feedback/decisions. | `haipipe-page-outline → <Folder-owner> → <Page-Face-owner> → <narrative/style-policy> → haipipe-plugin-outline/ref/plan-grammar.md + ref/item-table.md` | `Bullet Workspace`; Evidence contracts visible in `Evidence Workspace`; context read from `Context Workspace`. | Writes `outline/<stem>-outline-v<G>.<S>[.<E>].md`; writes item identity, type, readable name, Target, Label, Need, Expected, Acceptance in `outline/<stem>-evidence-items.md`; may write Discussion/Log. May co-revise candidate `outline/<stem>-preview.md`, never published Page Content. | **No standalone planning Run.** May execute within an interactive Writing Step; Evidence Items and routes remain plans. | Plan checks pass; every owed item is named `E<NN>-<TYPE>-<slug>` with `TYPE = VALUE/CITE/DISPLAY`, expectation, and acceptance. A checked `v0.*` plan may continue to evidence work before approval; Content release requires the first human approval to promote the selected state to `v1.0`. | `OUTLINE / SURVEY` while any `make` item is not folded; `CONTENT / WRITE` when every `make` item is folded, every `defer`/`drop` row is durably decided, and a `G>=1` plan has direct or inherited Shape approval. |
| `01B` | `OUTLINE / SURVEY` | Design the complete Run graph for every Evidence Item before execution. | Mechanically checked `v0.*` Shape, or directly/inherited human-approved `G>=1` Shape; Evidence Item contracts; actual Execution/Discovery Run inventories and Results; local static source inventory. | `haipipe-page-outline → <Folder-owner> → <Page-Face-owner> → haipipe-plugin-outline/ref/plan-grammar.md + ref/item-table.md → haipipe-run + <selected-worker-contracts>` | `Evidence Workspace`; Context Workspace supplies source boundaries. | Updates only the route fields in `outline/<stem>-evidence-items.md`: `Supporting Runs`, one `Local Input`, one owner-native `Local Run`, and human `Decide`. | **Creates no Runs.** Plans `0..N` Supporting Runs plus exactly `1` owner-native Page Evidence Item Run per make-item. Existing routes name full ids; Task `new-run` names parent `bNNjNNtNN`; another owner names its stable Folder address or a full reservation permitted by its current naming contract. | Every route is honestly classified; Local Input contents named; exactly one local route per item; make/defer/drop is explicitly signed. Auto HOLDs on an unsigned `Decide` unless a prior durable owner policy supplies the choice. | `EVIDENCE / LAND`; back to `OUTLINE / SHAPE` if the item contract is wrong; `HOLD` on unresolved Decide. |
| `02A` | `EVIDENCE / LAND` | Finish both Run layers and make one focal typed Result ready for every make-item. | Decided Evidence Item table; Supporting Run Tickets/Results; local input plan; selected evidence worker contract. | `haipipe-page-evidence → <Folder-owner> → <Page-Face-owner> → haipipe-plugin-outline/ref/item-table.md → ref/evidence/{values,citations,displays}.md → haipipe-run + <Execution/Discovery/local-workers>` | `Evidence Workspace` for graph, paths, availability, and next actions. | Allocates/updates `runs/`; materializes paired `results/`; freezes Local Input; binds full Run/Result ids in `outline/<stem>-evidence-items.md`; presents CITE review and stores the person's `Verified` signature on its authored item row; generated evidence status may refresh. | Executes/reuses `0..N` Execution/Discovery Supporting Runs, then exactly `1` `Page · Evidence Item` local Run per make-item. | All Supporting Results validate; Local Input is frozen; local `VALUE`, `CITE`, or `DISPLAY` Result passes the item's Acceptance contract; CITE also has signed `Verified`. | `EVIDENCE / EMBED`; `OUTLINE / SURVEY` for incomplete graph; `OUTLINE / SHAPE` for invalid meaning; `HOLD` for truthful block or pending CITE verification. |
| `02B` | `EVIDENCE / EMBED` | Interpret each ready local Result inside the plan without changing the plan's structure. | Ready local Evidence Item Results; checked `v0.*` plan or approved `G>=1` plan; target Bullet addresses. | `haipipe-page-evidence → <Folder-owner> → <Page-Face-owner> → <narrative/style-policy> → haipipe-plugin-outline/ref/item-table.md + ref/plan-grammar.md` | `Bullet Workspace` joined to `Evidence Workspace`. | Writes `outline/<stem>-outline-v<G>.<S>.<E+1>.md` with appended `Answered:`, `Drawn:`, and `Routed:` bindings; for G=0 it remains unapproved, while G>=1 declares `shape-base: v<G>.<S>` and inherits Shape approval; does not edit Run Results. | **None.** Consumes ready Results; does not commission a new Run. | Every ready Result is folded at its target; contradictions become Discussion findings; the new plan is ready for SHAPE when G=0 and routes to CONTENT when G>=1. | `OUTLINE / SHAPE` for G=0; `CONTENT / WRITE` for G>=1. |
| `03` | `CONTENT / WRITE` | Adopt agreed text without redrafting, integrate authorized evidence and deliver. | Accepted Writing Version/Step + exact paragraph text; current Context; approved Shape; ready bound Evidence Results; current Page hash; selected delivery policy. | `haipipe-page-content → <Folder-owner> → <Page-Face-owner> → haipipe-plugin-outline/ref/plan-grammar.md → <delivery-workers>`; use `haipipe-writing` only for explicitly reopened prose. | Reads the three Workspaces and accepted preview. | Scoped adoption into `<page>.md`; authorized citations/placeholders; adoption trace; declared delivery. | Consumes the interactive Writing Result. No new writing Run per adopted paragraph. Separately commissioned export/evidence attempts use their owning Run contracts. | Accepted wording preserved; evidence requirements pass; source/version consistent; requested artifacts current; formal pre-check ready. | `CHECK` at formal completion; return the affected question to the interactive Run if wording/meaning must change. |
| `04` | `CHECK / CHECK` | Judge one exact built Page version and name the next authority; only this phase may close. | Immutable source/render identity; full Page; Context; approved plan; evidence trace; Page Face owner closing rule; CONTENT trail; human-gate facts. | `haipipe-page-check → <Folder-owner> → <Page-Face-owner> → <owner/family-checker>` | Reads Context/Bullet/Evidence workspaces; writes no Outline material in the judged version. | Writes only the Page workflow check receipt and findings/comments in the declared review surface. Never repairs the Page it judges. | **None.** CHECK is a gate, not a Level-4 Run. | Mechanical errors zero; semantic rubric passes; source/render identity unchanged; every required human gate has durable evidence. | `CLOSE`, or `CONTEXT / OUTLINE / EVIDENCE / CONTENT / HOLD`. |

## Run cardinality

Let `I` be make-items, `S` the unique newly commissioned Supporting Runs,
`W` the bounded interactive writing goals, and `D` other independently
commissioned delegated attempts.

```text
New Runs = S + I local make-item Runs + W + D
```

Count actual allocations, not every reuse edge, paragraph, Step, Version, or
routine mechanical command. One interactive Run may cover P1/P2 or a whole
Section; a review window is not another Run. Historical or explicitly selected
single-paragraph delegated Results retain their existing contract at
`../../haipipe-page-content/ref/paragraph-run.md`. Their immutable-attempt
rules do not force a new interactive Run on every human comment.

## One Evidence Item from outline to prose

| Stage | Authored/derived fact | Example |
|---|---|---|
| SHAPE | typed identity and ready-evidence contract | `E01-VALUE-adjusted-effect` + Expected + Acceptance |
| SURVEY | Supporting routes + Local Input plan + owner-native Local Run plan | `new-run · b01j02t03` (Task example); other owners follow their own naming contract |
| LAND | valid Supporting Results + frozen input + ready local Result | `b01j02t03r05` → governed Result (Task example) |
| EMBED | Page interpretation bound to the target Bullet | `Answered: E01 … → <owner-native full Run id>` |
| CONTENT | adopts accepted wording and its authorized evidence realization | adoption trace names Writing Run + Version/Step and E01 Result |
| CHECK | exact built version proves the trace and closing rule | finding-free check receipt or a named backward route |

## Cross-family adoption rule

Every skill set that produces or changes a Page must publish a projection of
this table and answer these fields explicitly:

1. exact Folder-owning workflow or canonical family skill;
2. exact Page Face owner skill (load once when it is the same skill as row 1);
3. exact outline/narrative/style policy skill;
4. L3 files or authorities each row may change;
5. L4 Run families, targets, cardinality, workers, Results, and promotion;
6. gates and legal backward routes.

The family may specialize cells. It may not rename the Page phases, allocate a separate Run for every
planning movement, let CHECK repair its own finding, or create a
second planning/evidence Plugin beside `haipipe-plugin-outline`.
