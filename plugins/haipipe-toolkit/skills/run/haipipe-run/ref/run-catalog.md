# Run catalogue and owner index

Read this to choose a Run profile, define an extension, or show the kinds of
work available. Load only the selected owner's full contract. This is the
shared catalogue entry point; domain sources own their detailed operations.

```text
Run Type → bounded Run Spec → allocated Run Instance → Result/receipt
```

Types, operation variants, identity kinds, planning templates and actual
instances have different counting grains. The domain groupings below are an
index, not a mandatory family enum or a sum of executed Runs.

## Current profiles

Native spellings are preserved. An `operation` can resolve a profile through
its owner even when its existing receipt has no separate `run_type` field.
A new Spec must bind an unambiguous registered key/profile; a new label alone
does not provide an allocator or acceptance gate.

| Domain / profile | Declared key or operation / kind | Native identity | Target and close rule | Authority |
|---|---|---|---|---|
| Task execution | `task.execute`; concrete family/operation from the Ticket | `rNN_<noun>_<qualifier>`, globally qualified by owner/BJTR | one frozen Task/config target; required Results and native receipt checks | [Task execution](../../../task/haipipe-task/fn/run.md), [receipt schema](../../../task/haipipe-task/ref/runtime-yaml-schema.md) |
| Discovery | `paper-analysis`, `source-analysis` | `rNN_<author><year>_<subject>` + owning Task | exactly one admitted Subject; required facts/source/Bib artifacts and checks | [Discovery profile](../../../discovery/haipipe-discovery/ref/paper-run-contract.md) |
| Page RP | `Page.interactive-writing`; `struct`, `scratch`, `sec`, `para`, `revise` | `rp-struct-NN`, `rp-scratch-NN_<target>`, `rp-sec-NN`, `rp-para-NN_Pxx[-Pyy]`, `rp-revise-NN_<target>` | one scoped session; explicit acceptance, or Finish Scratch with summary | [Page families](../../../page/haipipe-page/ref/page-run-families.md), [interaction](../../../page/haipipe-page-workflow/ref/interactive-writing-run.md) |
| Delegated paragraph | `Page.paragraph-writing` / `paragraph-writing` | `rNN_page-writing_cNN-pNN` | one commissioned paragraph; paragraph/trace and declared acceptance | [Paragraph profile](../../../page/workflow-runs/haipipe-page-writing/ref/paragraph-run.md) |
| Page post-run analysis | `page-run-analysis` profile; separately commissioned review | `rNN_page-run-analysis` | closed RP journal by hash; output-only report and receipt, recommendations remain candidates | [Analysis profile](../../../page/haipipe-page-workflow/ref/post-run-analysis.md) |
| Page RE | `evidence-item`; `value`, `display`, `cite` | `re-<kind>-NN_<slug>` or resolved native Ticket alias | one focal obligation; typed accepted Result and required verification | [Evidence owner](../../../page/workflow-runs/haipipe-page-evidence/SKILL.md), [Page families](../../../page/haipipe-page/ref/page-run-families.md) |
| Independent display | separately commissioned display unit | caller's declared native Run, e.g. `rNN_page-display_…` | one unit outside an RE commission; caller supplies Ticket/receipt and acceptance, renderer supplies output contract | [Display owner](../../../display/haipipe-display/SKILL.md), [unit contract](../../../display/ref/display-unit-output-contract.md) |
| Page RD | delivery target/version | `rdNN_<target>` and owner path | released source version × delivery lane; artifact/hash/build receipt | [Page families](../../../page/haipipe-page/ref/page-run-families.md), [Delivery owner](../../../page/haipipe-workbench-page/ref/delivery.md) |
| Insight RI | `insight / item` | `<instance>#riNN_<slug>@vNNN` execution | frozen base-R/data/question/target binding; accepted DIKW/RF requires independent review | [Insight item](../../../insight/haipipe-page-insight/ref/instance-items.md) |
| Design | `Design.commission`, `Design.generate`, `Design.verify` | `rdNN_<operation>_<slug>` + Design Folder | human release/hold decision; checked generation; independent verification verdict | [Design profile](../../../design/haipipe-design-workflow/references/run-profile.md) |
| Paper judgment | `paper.judgment.idea`, `.claim`, `.obligation`, `.narrative`; native `paper / judgment` | `ridea-`, `rclaim-`, `rtask-`, `rnarra-NN_<target>` | one fixed card/row discussion; scoped human judgment and durable closure | [Paper naming/closure](../../../paper/haipipe-paper/ref/run-naming.md), [Paper Specs](../../../paper/haipipe-paper-workflow/ref/run-workflow.md) |
| Paper compile | `paper.compile` | owner-local `rNN_compile-<slug>` | one frozen manuscript build; declared outputs and truthful manifest snapshot | [Paper Specs](../../../paper/haipipe-paper-workflow/ref/run-workflow.md), [assembler](../../../paper/haipipe-paper-assemble/SKILL.md) |
| Paper response | `paper.response` | `rresponse-NN_<batch>` | one response package; concern coverage, frozen build and human close | [Paper Specs](../../../paper/haipipe-paper-workflow/ref/run-workflow.md) |
| Labeling | 25 operation kinds under `labeling` | `rlNN_<operation>_<target>` | one operation target; canonical artifacts and operation-specific gate | [Labeling catalogue](../../../../../subjective-label/ref/ref-run.md) |

The Labeling catalogue owns corpus-contract, discovery-search, guideline-seed,
test-reserve, embedding-build, round-prepare, weak-prelabel, human-calibration,
guideline-learn, round-measure, round-close, handoff-freeze, test-gold-lock,
executor-predict, executor-score, executor-select, scan-preflight, scan-shard,
risk-route, human-review, reconcile, audit-sample, audit-human-gold,
audit-analyze and dstar-materialize. Read that owner for operation definitions
and the current Workflow for selected cardinality; no fixed happy-path formula
is a shared Run rule.

### Variants, projections, and historical vocabulary

- Existing `page.interactive-writing.paragraph` Specs narrow the interactive RP
  profile to paragraph scope. Preserve their native spelling; do not conflate
  them with delegated `Page.paragraph-writing`.
- RP kind tokens, RE focal kinds, and RD output formats are profile variants.
  Tables/figures/algorithms are display subtypes; individual labels are not Runs.
- A renderer called within an RE is an internal worker. Independent display
  production needs its own commission, resolver and receipt; a renderer asset
  directory alone does not establish a Run.
- Page RE/RD lineage and its underlying native Ticket may name the same work.
  Index aliases together. Distinct supporting production plus a local evidence
  transformation can be two Runs when each has its own target and close rule.
- `Design.adopt` and compact Page/Paper forms are historical input only.
  Design Delivery is a projection; new Design work uses the three current types.
- Paper's former ten `paper.*` coordination labels are mapped to native Specs
  or control actions by its [Workflow reference](../../../paper/haipipe-paper-workflow/ref/run-workflow.md).
  Selection, routing, setup and CHECK do not automatically allocate Runs.
- A new profile listed here is not proof of UI support. Resolve the actual
  native writer/reader before claiming that an interface can operate it.

## Reusable Execution templates

These are reference vocabulary, not preallocated records or installed runners.
Bind a concrete owner, native resolver and Result gate before dispatch.

| Key | Actor mode | Bounded work | Successful close / output |
|---|---|---|---|
| `acquisition.scrape` | agent or automatic | source + requested scope | coverage settled; dataset + receipt |
| `transformation.build-data` | agent or automatic | reproducible input/output dataset build | output/manifest validate |
| `training.fit` | agent or automatic | model/config/data fitting commission | artifact loads; fit metrics and receipt exist |
| `evaluation.validate` | agent | artifact + evaluation set | required coverage and verdict recorded, including a negative verdict |
| `authoring.write-file` | agent or hybrid | bounded file/artifact change | requested checks and acceptance settled; candidate/diff + receipt |

Each template also permits a truthful failed/blocked outcome through its
resolved owner. `automatic` describes actor mode; a tool/API/script is the
execution mechanism, not an additional mode.

## Register a profile or resolve a Spec

A profile must supply these facts, directly or through a linked authoritative
source. A catalogue table need not duplicate the owner's complete schema.

| Fact | Required resolution |
|---|---|
| Type and owner | stable key or owner-qualified operation mapping; exact contract |
| Target / actor / action | bounded target grammar; named owner; allowed modes/actions |
| Ticket / identity / Result | deterministic resolver, allocation scope, concrete output grammar |
| Inputs / dependencies | authoritative versions/hashes when required; may be empty |
| Gates / routes | default-open or declared entry; mandatory close; terminal CLOSE or explicit next Spec |
| Acceptance / promotion | testable completion and separate admission/release authority |
| History | retry, reopen, new-commission and supersession rules |
| Receipt | durable outcome, lifecycle and recoverable attempts/history |
| Boundary | examples of work that stays internal or is a projection |

Gate/Route and actor modes are `human | automatic | agent | hybrid`. Each
concrete Spec supplies cardinality and internal Steps; Workspace Cells bind
skills and interactions when a Workflow declares those surfaces. Follow the
[Workflow schema](../../../task/haipipe-workflow/ref/plan-schema.md).

Audit that every selected Spec resolves its profile, actor, action, target,
exit gate, routes and receipt without contradiction. Unknown or incomplete
contracts are explicit gaps, not permission to invent an executable type.
Catalogue, planned Spec, allocated instance and projected UI card remain
separate views of the same declared work.
