# haipipe-page-guide · outline v0.1
outline-version: v0.1
supersedes: none
date: 260912
approved: ⬜
arc: Page-owned sources allow independent delivery, which lets Board and workbenches share one workspace while bounded feedback preserves its decisions.

## C1 · Page ownership
### C1.P1 · Source and delivery
- B1 · [Scope] The Page Folder keeps its working materials together.
  Note: Source, code, figures, evidence, Runs, Results, and delivery outputs stay with the Page; Studio Chat and Studio Draw support human brainstorming. 🎯 A1.1
  Evidence: none · normative Page Folder scope.
  Draft: A Page Folder keeps everything needed to understand, change, and deliver one Page in one place. It can hold the Markdown source, code, figures, evidence, Runs and Results, and generated web, LaTeX, and Word files. Studio is where people brainstorm for the Page. Studio Chat keeps the conversation, while Studio Draw turns ideas into visual sketches.
- B2 · [Identity] The Markdown source shares the Page Folder's stem.
  Note: `haipipe-page-guide/` corresponds to `haipipe-page-guide.md`, which is this Page's source of truth. 🎯 A1.1
  Evidence: none · Page source naming rule.
  Draft: The Markdown source uses the same stem as the folder: haipipe-page-guide/ corresponds to haipipe-page-guide.md.
- B3 · [Projection] Delivery is generated from the Markdown source.
  Note: Web, LaTeX, and Word are outputs; this Page's earlier HTML draft is preserved material, not source authority. 🎯 A1.1
  Evidence: none · source-to-delivery rule.
  Draft: Each delivery file is generated from that Markdown source instead of maintained as a separate source. The earlier HTML draft is kept only as material and does not control this Page or its outputs.

## C2 · Board and workbenches
### C2.P2 · Shared content authority
- B1 · [Relationship] Board membership organizes the same Page Face.
  Note: The Page retains source ownership when membership changes. 🎯 A2.1
  Evidence: none · Board membership rule.
  Draft: Board supplies grouping, ordering, and navigation by registering the same Page Face. Removing that membership should leave the Page Folder and its content intact.
- B2 · [Mechanism] Workbenches present records through their declared writers.
  Note: Outline, Studio, Runs, Delivery, and Folder have distinct responsibilities. 🎯 A2.1
  Evidence: none · workbench architecture rule.
  Draft: Workbenches present the Page's planning records, conversations, runs, outputs, and files through their own declared writers.
- B3 · [Criterion] A visible label does not establish working integration.
  Note: Each advertised action needs an actual record path and supported writer. 🎯 A2.1
  Evidence: none · capability acceptance criterion.
  Draft: Putting a workbench's name on a folder or button is not enough; the workbench must actually open the Page's records and perform the actions it promises.

### C2.P3 · Two Run lanes
- B1 · [Definition] A Page Run uses a Page-local `rpNN` identity.
  Note: The sequence begins with fused Structure Run `rp-struct-01` and continues with concise typed paragraph Runs. 🎯 A2.1
  Evidence: none · Page Run definition.
  Draft: Each Page Run has a local identity and a Version that stores its feedback Steps.
- B2 · [Contrast] A Task Run returns delegated output to the Page.
  Note: Delegated paragraph writing and Discovery are Task Runs; their native identity, Ticket, and runtime remain with the owner. 🎯 A2.1
  Evidence: none · Task Run projection boundary.
  Draft: Task Runs keep their native identity and return delegated outputs, such as paragraph drafts or Discovery results, for the Page to use.
- B3 · [Independence] Page Run and Task Run counters remain independent.
  Note: `rp01` and native Task `r01` may coexist without collision or renumbering. 🎯 A2.1
  Evidence: none · namespace rule.
  Draft: The `rpNN` and Task `rNN` sequences are independent, so `rp01` and `r01` may coexist in one Page Folder.
- B4 · [Boundary] A Page workflow pass is not a Page Run.
  Note: Controller Run receipts remain under workflow/ and do not enter feedback history. 🎯 A2.1
  Evidence: none · workflow identity rule.
  Draft: An automated CONTEXT-to-CHECK controller invocation is a Page workflow pass, not another Page Run.

### C2.P4 · Proposing interaction
- B1 · [Proposal] The Runs function proposes bounded human-interaction goals.
  Note: The Page itself must need shaping, comparison, revision, or acceptance. 🎯 A2.1
  Evidence: none · proposal rule.
  Draft: The Page's Runs function proposes bounded interaction goals when a person needs to shape, compare, revise, or accept the Page itself.
- B2 · [Allocation] A proposal has no allocated Page Run identity.
  Note: Selection or direct commission precedes `rpNN`, Ticket, Result, and inventory state. 🎯 A2.1
  Evidence: none · allocation rule.
  Draft: A proposal is not yet a Run and receives no `rpNN` until the person selects or directly commissions it.
- B3 · [Continuation] Selection resumes or starts one Page Run.
  Note: Resume a matching open goal; allocate the next `rpNN` only for independent work. 🎯 A2.1
  Evidence: none · resume rule.
  Draft: A selected candidate resumes a matching open Page Run or allocates the next `rpNN` for an independent goal, and later feedback appends Steps to that Run's current Version.
- B4 · [Exclusion] Output-producing work remains a Task Run.
  Note: Code, search, data, rendering, build, and Discovery keep owner-native identities even when humans later review Results. 🎯 A2.1
  Evidence: none · Task routing rule.
  Draft: Code, search, data, rendering, build, Discovery, and other output-producing work remains a normal Task Run even when a later human gate reviews its Result.

### C2.P5 · Structure Run then paragraphs
- B1 · [Sequence] `rp-struct-01` is always the first Page Run.
  Note: Human and agent complete SHAPE and SURVEY in this one shared Structure Run until explicit closure. Multiple people may contribute Steps to it. 🎯 A2.1
  Evidence: none · first-Run ordering rule.
  Draft: The first Page Run is always `rp-struct-01`, one shared Structure Run where the person and agent complete SHAPE and SURVEY for the whole Page until the person explicitly closes it. Multiple people may contribute Steps to this same Run.
- B2 · [Gate] Structure closure freezes a Page-global `P01..PN` index.
  Note: Every paragraph serial maps to its plan address in reading order. 🎯 A2.1
  Evidence: none · paragraph-index gate.
  Draft: That Structure closure freezes the Page-global reading order as `P01`, `P02`, through `PN`, with every serial mapped to its plan address.
- B3 · [Scope] A closed paragraph index defines the Step scope for each Page Run.
  Note: Each Step scope covers one or more numbered paragraphs; no paragraph Page Run exists before the Structure Run closes. 🎯 A2.1
  Evidence: none · paragraph Step-scope rule.
  Draft: After the Structure closes, the Runs function creates Steps, each with a scope covering one or more of the `N` numbered paragraphs.
- B4 · [Identity] Every paragraph Run exposes its exact serial or range.
  Note: Use typed identities such as `rp-para-01_P01` and `rp-para-02_P02-P03`; put description in Goal. 🎯 A2.1
  Evidence: none · paragraph Run naming rule.
  Draft: Each selected paragraph Run uses a typed identity that exposes the exact serial or contiguous range, such as `rp-para-01_P01` or `rp-para-02_P02-P03`; its descriptive wording stays in Goal.
- B5 · [Scope] Human decision boundaries determine Step scope while output work stays Task-owned.
  Note: Different acceptance questions may use different Step scopes; keep code, Discovery, data, rendering, and build in Task Runs. 🎯 A2.1
  Evidence: none · Step-scope and ownership rule.
  Draft: Different human questions or acceptance boundaries call for different Step scopes, while code, Discovery, data, rendering, and build remain normal Task Runs.

## C3 · Continuing work
### C3.P6 · Scope and acceptance
- B1 · [Scope] Each feedback request bounds the permitted edit.
  Note: An Opening edit does not authorize changes to adjacent Content. 🎯 A3.1
  Evidence: none · editing-scope rule.
  Draft: A request to revise Opening sets the editing boundary; it does not authorize rewriting the rest of the Page.
- B2 · [Preview] Planned points pair with provisional candidate prose.
  Note: Unapproved wording remains a planning draft for discussion. 🎯 A3.1
  Evidence: none · planning-preview rule.
  Draft: During planning, the Outline workspace pairs each planned point with candidate prose for discussion.
- B3 · [History] Writing history preserves scoped feedback and acceptance.
  Note: Version closure, Page acceptance, and browser execution are separate. 🎯 A3.1
  Evidence: none · acceptance-history rule.
  Draft: A Writing Run preserves the goal and feedback history through Versions and Steps, while accepted wording is adopted into Content through the Page workflow. Those records do not imply that a browser button executes an agent, and accepting one passage does not accept the whole Page.
