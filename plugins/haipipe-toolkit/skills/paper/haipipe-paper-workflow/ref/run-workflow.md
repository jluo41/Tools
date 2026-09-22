# Paper Runs: Specs, routing, and Runtime

Read this when planning, commissioning, resuming, or reporting Paper Runs.
Paper Runs are the Paper-scoped execution layer; they are not PageTypes or
Page controller steps.
The shared authorities are `haipipe-run`, `haipipe-page-workflow`, and
`haipipe-page/ref/page-run-families.md`. Paper specializes their targets and
dependencies; it does not introduce another lifecycle.

## Workflow = a list of Runs

A Workflow Definition lists bounded Run Specs, dependencies, Spec-owned routes,
and completion rules. A Workflow Runtime lists the actual owner-native Runs
materialized from those Specs. A Run Type supplies reusable defaults; a Spec
binds one goal/target; an Instance carries its Ticket, Result, and receipt.
Steps and Versions stay inside the Run. A Page, Folder, Space, Gate, or tool
call is not by itself a Run.

Use the following templates only for independently commissioned, independently
closable work. Resolve symbolic targets and selected owner contracts before
dispatch. Cardinality is 0..N selected targets, not one Run per Page or click.

| Spec template | Run Type / owner | Target and inputs | Actor / action | Entry → exit | Routes and internal Steps |
|---|---|---|---|---|---|
| `idea.<idea>` | `paper.judgment.idea` / Paper Ideation Page | one admitted Idea; exact Ideation card and test Results | hybrid / discuss one idea | card exists → bounded judgment recorded | unresolved source → support; accepted discussion → CLOSE; feedback → SELF/NEW_VERSION |
| `claim.<story>.<claim>` | `paper.judgment.claim` / Story | one C5 proposition and its evidence/limits | hybrid / judge claim support | frozen claim + available evidence → judgment and open limits recorded | missing evidence → support; settled → CLOSE; revision → SELF/NEW_VERSION |
| `obligation.<story>.<row>` | `paper.judgment.obligation` / Story | one C7 evidence obligation and candidate study plan | hybrid / review one obligation | row exists → bounded obligation judgment | research needed → support after G1; settled → CLOSE |
| `narrative.<story>.<section>` | `paper.judgment.narrative` / Story | one C8 row, current Venue contract, claim/evidence pointers | hybrid / review Section telling | row exists → reviewed narrative with risks | G3 release → selected structure/write; otherwise HOLD or CLOSE as proposal |
| `support.<target>` | selected Task/Discovery/Ideation worker's native Run Type | one missing computation, source inquiry, generation or test Result; frozen inputs and authorized scope | owner-selected / execute bounded work | owner entry + relevant G1 → accepted native Result | relevant G2 return → consumers; failure → owner retry or HOLD |
| `structure.<page>` | Page Structure RP / shared Page workflow + exact PageType | commissioned whole-Page structure, direction and evidence decisions | hybrid / SHAPE + SURVEY | Page owner resolved + applicable G3 → native structure acceptance | evidence/write as selected; feedback internal; changed goal → NEW_RUN |
| `write.<page>.<scope>` | Page Writing RP / shared Page workflow + exact PageType | one Section/paragraph goal; accepted structure and required evidence | hybrid / draft, review, diagnose, revise | native writing entry + applicable G3 → native writing acceptance | SELF, NEW_VERSION, CLOSE, NEW_RUN under Page owner |
| `evidence.<page>.<item>` | Page Evidence RE / Page evidence owner + selected worker | one VALUE/CITE/DISPLAY item; frozen Local Input and 0..N Supporting Results | agent or hybrid / make and verify typed Result | decided item + required inputs → accepted typed Result | EMBED control → dependent write/deliver; failure → repair or HOLD |
| `deliver.<page>.<format>` | Page Delivery RD / `haipipe-workbench-page` | one released Page version and delivery target | agent / render one target | native release barrier → artifact/hash/build receipt | Page CHECK control → compile dependency; failure → repair/HOLD |
| `compile.<paper>.<build>` | `paper.compile` / `haipipe-paper-assemble` | exact compile-order, Section fragments/bindings, config/profile | agent / assemble one manuscript build | valid safe config + explicit build request → truthful manifest and declared outputs or failure | G4 evaluates readiness; feedback → response; build outcome → CLOSE |
| `response.<round>` | `paper.response` / `haipipe-paper-round` | one frozen feedback batch/base build, ledger, checked returned versions | hybrid / compose one response package | named batch → covered concerns, frozen answer build and human response/close receipt | required repairs → affected owner Specs; incomplete → HOLD; G5 → CLOSE |

G0–G5 predicates are defined in the Workflow skill. Their human decisions keep
the same authority. A judgment may close with a documented concern or proposed
route; that does not release a Section, select an Idea, or commission a Task.
For `support`, bind the exact native Run Type, actor, entry/exit and retry rules
from its owner. Never create a Paper wrapper Run around an already counted
native Run. Existing current Results can satisfy dependencies without reruns.

Every concrete Spec also records Workspace Cells: target Page/Story row,
owning skill, interaction surface, authority path and Result presentation.
Space mapping is a projection of these fields, not another authority.

## Control actions and compatibility

Setup preview/apply, I3 selection, G0–G5 evaluation, Story/Section routing,
Ideation sync, Page controller passes, release, CHECK and status reads are
control/resource actions unless a native contract commissions independently
closable work. They do not automatically allocate Runs. Idea generation and
testing load `haipipe-ideation` and its requested specialist; index only the
native Runs those owners actually allocate, not one Run per I1/I2/I3 label.

The old workbench vocabulary maps as follows:

| Existing label | Current meaning |
|---|---|
| `paper.setup` | setup control; commissioned implementation uses its selected native Spec |
| `paper.ideation.generate`, `paper.ideation.test` | Ideation capability routes; bounded execution uses `support.<target>`, discussion uses `idea.<idea>` |
| `paper.ideation.select` | the existing human I3 control, followed by G0 validation; no second selection |
| `paper.story.shape` | selected `structure.<page>` and writing Specs, when commissioned |
| `paper.story.review` | selected claim/obligation/narrative judgment Specs |
| `paper.story.route`, `paper.section.route` | dependency routing and G1/G3 controls; Section work uses its native Specs |
| `paper.compile` | `compile.<paper>.<build>` |
| `paper.round.respond` | `response.<round>`; ledger triage alone is a control action |

P0–P4 are legacy Run names. The four Paper PageType skills are direct
`paper/haipipe-paper-*` entrypoints; they do not define the `paper-runs` layer.
Shared serialized `Run/cycle/next_cycle` fields remain Run names,
neither Run Specs nor Steps. Do not bulk-rename historical receipts or frozen
builds.

## Native identities and Result storage

Page RP/RE/RD use the current shared grammar. Paper judgments use the declared
`ridea/rclaim/rtask/rnarra` profile and scoped human closure in
[Paper naming](../../haipipe-paper/ref/run-naming.md#judgment-result-and-close-rule).
Supporting Runs stay in Task/Discovery/other native stores. RE/RD lineage and
its native Ticket refer to the same work; index it once with aliases.

A commissioned compile uses the neutral folder-local executable dialect:
`<paper>/delivery/runs/<rNN_compile-slug>.sh` pairs with
`<paper>/delivery/results/<rNN_compile-slug>/`. Its Ticket freezes config hash,
source versions and engine/profile references, and invokes the existing
`delivery/build.py` wrapper. The Result records outcome and exact paths/hashes,
including a byte-for-byte snapshot of the build manifest. That snapshot is
historical evidence; `delivery/build-manifest.json` remains the sole current
delivery receipt. Recheck the frozen config/source hashes before execution;
if they changed, replan rather than silently compiling a different target.
The mechanical builder does not allocate a Run on its own. A legacy bare
build manifest is delivery evidence, not proof that a new Spec was executed.

A commissioned response uses the Paper human-session dialect:
`<Round>/runs/rresponse-NN_<batch>.md` pairs with
`<Round>/results/rresponse-NN_<batch>/`. Its journal records Versions/Steps,
concern pointers, response and frozen build references, and the final human
decision. It never copies revised Section prose into a second source store.
Routine ledger updates do not require this commission.

## Runtime and completion

Use the shared `haipipe.workflow-runtime/v1` envelope from
`task/haipipe-workflow/ref/workflow-runtime.md`. When an aggregate Runtime is
needed, keep `<paper>/workflow/paper/<workflow_runtime_id>/runtime.yaml` with
its immutable `definition-vNNN.yaml` revisions. This is an index/control store,
not a new Run bank. A direct single Run can rely on its native receipt.

Each frozen definition lists concrete Specs with `id`, `run_type`, `owner`,
`target`, `actor`, `action`, `inputs`, `depends_on`, `entry`, `exit`, `routes`,
`cardinality`, `internal_steps` and `cells`; the shared owner determines the
exact schema. Gate/Route mode is `human | automatic | agent | hybrid`.
Nonterminal routes name their next Spec or HOLD condition; terminal work
defaults to CLOSE. Preserve the previous definition when dependencies change.

Each actual `runs` entry binds `spec_id`, full owner path/native id,
Ticket/Result/receipt locations, frozen type/target, status and input hashes.
Mark reused accepted Results as `participation: reused`; resume existing work
as `managed`. Planned nodes stay in the definition/frontier without invented
instance ids. Control-only work may truthfully have `runs: []`.

Completion is scoped to the request: all commissioned Runs have accepted
terminal outcomes or explicit authorized dispositions, the applicable controls
are satisfied, and no required frontier/dependency is unresolved. A DRAFT
compile may complete its requested build without passing G4. A response cannot
claim closure while concerns or the required human close remain open.

Report current goal/owner, accepted Result/version, pending dependency or gate,
and the next required decision. Report parallel work together; do not infer a
single current position from the folder names.
