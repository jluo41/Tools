# haipipe-page-guide · outline v0.1
outline-version: v0.1
supersedes: none
date: 260912
approved: ⬜
arc: Page-owned sources allow independent delivery, which lets Board and plugins share one workspace while bounded feedback preserves its decisions.

## C1 · Page ownership
### C1.P1 · Source and delivery
- B1 · [Scope] The Page Folder keeps its working materials together.
  Note: Source, code, figures, evidence, Runs, Results, and delivery outputs stay with the Page; Studio Chat and Studio Draw support human brainstorming. 🎯 A1.1
  Evidence: none · normative Page Folder scope.
- B2 · [Identity] The Markdown source shares the Page Folder's stem.
  Note: `haipipe-page-guide/` corresponds to `haipipe-page-guide.md`, which is this Page's source of truth. 🎯 A1.1
  Evidence: none · Page source naming rule.
- B3 · [Projection] Delivery is generated from the Markdown source.
  Note: Web, LaTeX, and Word are outputs; this Page's earlier HTML draft is preserved material, not source authority. 🎯 A1.1
  Evidence: none · source-to-delivery rule.

## C2 · Board and plugins
### C2.P2 · Shared content authority
- B1 · [Relationship] Board membership organizes the same Page Face.
  Note: The Page retains source ownership when membership changes. 🎯 A2.1
  Evidence: none · Board membership rule.
- B2 · [Mechanism] Plugins present records through their declared writers.
  Note: Outline, Studio, Runs, Delivery, and Folder have distinct responsibilities. 🎯 A2.1
  Evidence: none · plugin architecture rule.
- B3 · [Criterion] A visible label does not establish working integration.
  Note: Each advertised action needs an actual record path and supported writer. 🎯 A2.1
  Evidence: none · capability acceptance criterion.

### C2.P3 · Two Run lanes
- B1 · [Definition] A Page Run uses a Page-local `rpNN` identity.
  Note: The sequence begins with `rp00_mermaid-structure` and continues with concise numbered paragraph Runs. 🎯 A2.1
  Evidence: none · Page Run definition.
- B2 · [Contrast] A Task Run returns delegated output to the Page.
  Note: Delegated paragraph writing and Discovery are Task Runs; their native identity, Ticket, and runtime remain with the owner. 🎯 A2.1
  Evidence: none · Task Run projection boundary.
- B3 · [Independence] Page Run and Task Run counters remain independent.
  Note: `rp01` and native Task `r01` may coexist without collision or renumbering. 🎯 A2.1
  Evidence: none · namespace rule.
- B4 · [Boundary] A Page workflow pass is not a Page Run.
  Note: Controller phase receipts remain under workflow/ and do not enter feedback history. 🎯 A2.1
  Evidence: none · workflow identity rule.

### C2.P4 · Proposing interaction
- B1 · [Proposal] The Runs function proposes bounded human-interaction goals.
  Note: The Page itself must need shaping, comparison, revision, or acceptance. 🎯 A2.1
  Evidence: none · proposal rule.
- B2 · [Allocation] A proposal has no allocated Page Run identity.
  Note: Selection or direct commission precedes `rpNN`, Ticket, Result, and inventory state. 🎯 A2.1
  Evidence: none · allocation rule.
- B3 · [Continuation] Selection resumes or starts one Page Run.
  Note: Resume a matching open goal; allocate the next `rpNN` only for independent work. 🎯 A2.1
  Evidence: none · resume rule.
- B4 · [Exclusion] Output-producing work remains a Task Run.
  Note: Code, search, data, rendering, build, and Discovery keep owner-native identities even when humans later review Results. 🎯 A2.1
  Evidence: none · Task routing rule.

### C2.P5 · Mermaid Structure then paragraphs
- B1 · [Sequence] `rp00_mermaid-structure` is always the first Page Run.
  Note: Human and agent iterate on the complete Mermaid Structure until explicit closure. 🎯 A2.1
  Evidence: none · first-Run ordering rule.
- B2 · [Gate] Mermaid Structure closure freezes a Page-global `P01..PN` index.
  Note: Every paragraph serial maps to its plan address in reading order. 🎯 A2.1
  Evidence: none · paragraph-index gate.
- B3 · [Scope] A closed paragraph index defines the Step scope for each Page Run.
  Note: Each Step scope covers one or more numbered paragraphs; no paragraph Page Run exists before the Mermaid Structure Run closes. 🎯 A2.1
  Evidence: none · paragraph Step-scope rule.
- B4 · [Identity] Every paragraph Run exposes its exact serial or range.
  Note: Use concise identities such as `rp01_p01` and `rp02_p02-p03`; put description in Goal. 🎯 A2.1
  Evidence: none · paragraph Run naming rule.
- B5 · [Scope] Human decision boundaries determine Step scope while output work stays Task-owned.
  Note: Different acceptance questions may use different Step scopes; keep code, Discovery, data, rendering, and build in Task Runs. 🎯 A2.1
  Evidence: none · Step-scope and ownership rule.

## C3 · Continuing work
### C3.P6 · Scope and acceptance
- B1 · [Scope] Each feedback request bounds the permitted edit.
  Note: An Opening edit does not authorize changes to adjacent Content. 🎯 A3.1
  Evidence: none · editing-scope rule.
- B2 · [Preview] Planned points pair with provisional candidate prose.
  Note: Unapproved wording remains a planning draft for discussion. 🎯 A3.1
  Evidence: none · planning-preview rule.
- B3 · [History] Writing history preserves scoped feedback and acceptance.
  Note: Version closure, Page acceptance, and browser execution are separate. 🎯 A3.1
  Evidence: none · acceptance-history rule.
