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

## Architecture at a glance

| Index | Phase skill | Cycle(s) | Primary surface/plugin | Creates L4 Runs? |
|---:|---|---|---|---|
| `00` | `haipipe-page-context` | `PREPARE` | `haipipe-plugin-outline` → Context Workspace | No |
| `01` | `haipipe-page-outline` | `SHAPE`, `SURVEY` | `haipipe-plugin-outline` → Bullet + Evidence Workspaces | No; SURVEY designs them |
| `02` | `haipipe-page-evidence` | `LAND`, `EMBED` | `haipipe-plugin-outline` → Evidence + Bullet Workspaces | Yes in LAND; none in EMBED |
| `03` | `haipipe-page-content` | `WRITE` | Page Content + declared delivery surfaces | Yes: Division Writing Runs |
| `04` | `haipipe-page-check` | `CHECK` | read-only whole-Page review + receipt | No |

The shared plugin does not merge phase authority. CONTEXT may write the Context
record, OUTLINE may write the plan and Run design, and EVIDENCE may bind/fold
ready Results. All three are viewed together because they are three views of
one Page planning process.

## Full workflow

| Index | Page phase / cycle | Objective | Required input | Exact skill chain | Outline plugin workspace | L3 Folder/Page content modified | L4 Runs commissioned or consumed | Exit evidence | Normal next authority |
|---:|---|---|---|---|---|---|---|---|---|
| `00` | `CONTEXT / PREPARE` | Make the governing context explicit before planning or writing. | Page + Folder identity; Folder owner; Page Face owner; policy; requirements; feedback; discussion; Files/Log/Skills; bounded related Page fragments; current plan/evidence/run receipts. | `haipipe-page-context → <Folder-owner> → <Page-Face-owner> → haipipe-plugin-outline/ref/record-shape.md` | `Context Workspace` | Generates `outline/<stem>-context.md`; reads the other Outline records without merging or replacing them. | **None.** Collect, Resolve, Freeze are planning movements. | Identity resolved; required sources addressed and fresh; missing/conflicting rows explicit; Context record generated. | `OUTLINE / SHAPE`; repeat `CONTEXT / PREPARE` or `HOLD` on unresolved input. |
| `01A` | `OUTLINE / SHAPE` | Agree what the Page will say and what ready evidence each Bullet expects. | Frozen Context record; Page Face owner outline grammar; current Page; prior plan; applicable feedback/decisions. | `haipipe-page-outline → <Folder-owner> → <Page-Face-owner> → <narrative/style-policy> → haipipe-plugin-outline/ref/plan-grammar.md + ref/item-table.md` | `Bullet Workspace`; Evidence contracts visible in `Evidence Workspace`; context read from `Context Workspace`. | Writes `outline/<stem>-outline-v<N>.md`; writes item identity, type, readable name, Target, Label, Need, Expected, Acceptance in `outline/<stem>-evidence-items.md`; may write Discussion/Log. Never writes Page Content. | **None.** Evidence Items and proposed routes are plans, not Runs. | Plan checks pass; every owed item is named `E<NN>-<TYPE>-<slug>` with `TYPE = VALUE/CITE/DISPLAY`, expectation, and acceptance; in copilot a person approves, while auto may record the owed review and continue under the declared gate policy. | `OUTLINE / SURVEY` when evidence is owed; `CONTENT / WRITE` when no make-item remains and the evidence-aware plan may proceed under the declared gate policy. |
| `01B` | `OUTLINE / SURVEY` | Design the complete Run graph for every Evidence Item before execution. | Agreed or auto-forwarded Shape; Evidence Item contracts; actual Execution/Discovery Run inventories and Results; local static source inventory. | `haipipe-page-outline → <Folder-owner> → <Page-Face-owner> → haipipe-plugin-outline/ref/plan-grammar.md + ref/item-table.md → haipipe-run + <selected-worker-contracts>` | `Evidence Workspace`; Context Workspace supplies source boundaries. | Updates only the route fields in `outline/<stem>-evidence-items.md`: `Supporting Runs`, one `Local Input`, one owner-native `Local Run`, and human `Decide`. | **Creates no Runs.** Plans `0..N` Supporting Runs plus exactly `1` owner-native Page Evidence Item Run per make-item. Reuse/rerun/registered rows name full ids; Task `new-run` names parent `bNNjNNtNN`; Paper may reserve `pjNNtNNrNN`; another Folder-local owner names its stable Folder address. | Every route is honestly classified; Local Input contents named; exactly one local route per item; make/defer/drop is explicitly signed. Auto HOLDs on an unsigned `Decide` unless a prior durable owner policy supplies the choice. | `EVIDENCE / LAND`; back to `OUTLINE / SHAPE` if the item contract is wrong; `HOLD` on unresolved Decide. |
| `02A` | `EVIDENCE / LAND` | Finish both Run layers and make one focal typed Result ready for every make-item. | Decided Evidence Item table; Supporting Run Tickets/Results; local input plan; selected evidence worker contract. | `haipipe-page-evidence → <Folder-owner> → <Page-Face-owner> → haipipe-plugin-outline/ref/item-table.md → ref/evidence/{values,citations,displays}.md → haipipe-run + <Execution/Discovery/local-workers>` | `Evidence Workspace` for graph, paths, availability, and next actions. | Allocates/updates `runs/`; materializes paired `results/`; freezes Local Input; binds full Run/Result ids in `outline/<stem>-evidence-items.md`; presents CITE review and stores the person's `Verified` signature on its authored item row; generated evidence status may refresh. | Executes/reuses `0..N` Execution/Discovery Supporting Runs, then exactly `1` `Page · Evidence Item` local Run per make-item. | All Supporting Results validate; Local Input is frozen; local `VALUE`, `CITE`, or `DISPLAY` Result passes the item's Acceptance contract; CITE also has signed `Verified`. | `EVIDENCE / EMBED`; `OUTLINE / SURVEY` for incomplete graph; `OUTLINE / SHAPE` for invalid meaning; `HOLD` for truthful block or pending CITE verification. |
| `02B` | `EVIDENCE / EMBED` | Interpret each ready local Result inside the plan without changing the plan's structure. | Ready local Evidence Item Results; current approved plan; target Bullet addresses. | `haipipe-page-evidence → <Folder-owner> → <Page-Face-owner> → <narrative/style-policy> → haipipe-plugin-outline/ref/item-table.md + ref/plan-grammar.md` | `Bullet Workspace` joined to `Evidence Workspace`. | Writes `outline/<stem>-outline-v<N+1>.md` with appended `Answered:`, `Drawn:`, and `Routed:` bindings; sets `approved: ⬜`; does not edit Run Results. | **None.** Consumes ready Results; does not commission a new Run. | Every ready Result is folded at its target; contradictions become Discussion findings; the new plan is ready for re-agreement. | `OUTLINE / SHAPE`, always. |
| `03` | `CONTENT / WRITE` | Realize the approved evidence-aware plan as Page Content and current delivery artifacts. | Fresh Context; approved folded plan; ready Evidence Results; Page Face owner structure; narrative/style policy; current Page version. | `haipipe-page-content → <Folder-owner> → <Page-Face-owner> → haipipe-plugin-outline/ref/plan-grammar.md → <narrative/style-policy> → haipipe-run + <Division-Writing/delivery-workers>` | Reads all three Outline workspaces; Page Content and Delivery are the produced surfaces. | Writes/promotes `<page>.md` Content divisions; updates authorized Opening/Aims/Log; regenerates declared `delivery/` projections; records writing receipts. | Normally `1 Page · Division Writing Run × commissioned division`; internal Draft/Revise/Build/Pre-check movements are not extra Runs. | Each division Result passes trace/style checks and is promoted; delivery artifacts are current; fresh pre-check returns `ready`. | `CHECK`; loop `CONTENT`; route to `CONTEXT`, `OUTLINE`, or `EVIDENCE` by the broken authority. |
| `04` | `CHECK / CHECK` | Judge one exact built Page version and name the next authority; only this phase may close. | Immutable source/render identity; full Page; Context; approved plan; evidence trace; Page Face owner closing rule; CONTENT trail; human-gate facts. | `haipipe-page-check → <Folder-owner> → <Page-Face-owner> → <owner/family-checker>` | Reads Context/Bullet/Evidence workspaces; writes no Outline material in the judged version. | Writes only the Page workflow check receipt and findings/comments in the declared review surface. Never repairs the Page it judges. | **None.** CHECK is a gate, not a Level-4 Run. | Mechanical errors zero; semantic rubric passes; source/render identity unchanged; every required human gate has durable evidence. | `CLOSE`, or `CONTEXT / OUTLINE / EVIDENCE / CONTENT / HOLD`. |

## Run cardinality

Let:

- `I` be Evidence Items decided `make`;
- `S_i` be Supporting Runs for Evidence Item `i`;
- `D` be Content divisions commissioned for writing.

Then the planned Level-4 Page-work cardinality is:

```text
Evidence work = Σ(i=1..I) S_i supporting attempts + I local Evidence Item Runs
Content work  = D Page Division Writing Runs
Total         = Σ S_i + I + D
```

Reuse references remain graph edges and do not create duplicate Run identity.
Actual inventory is counted only from allocated Tickets plus valid runtime
receipts, never from this formula.

## One Evidence Item from outline to prose

| Stage | Authored/derived fact | Example |
|---|---|---|
| SHAPE | typed identity and ready-evidence contract | `E01-VALUE-adjusted-effect` + Expected + Acceptance |
| SURVEY | Supporting routes + Local Input plan + owner-native Local Run plan | Task `new-run · b01j02t03`; Paper `pj01t01r01 plan` |
| LAND | valid Supporting Results + frozen input + ready local Result | Task `b01j02t03r05`; Paper `pj01t01r01` → governed Result |
| EMBED | Page interpretation bound to the target Bullet | `Answered: E01 … → <owner-native full Run id>` |
| CONTENT | division candidate uses that folded result | `r04_page-division-writing_c02` trace row names E01 Result |
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

The family may specialize cells. It may not rename the Page phases, turn a
planning movement into a Run, let CHECK repair its own finding, or create a
second planning/evidence Plugin beside `haipipe-plugin-outline`.
