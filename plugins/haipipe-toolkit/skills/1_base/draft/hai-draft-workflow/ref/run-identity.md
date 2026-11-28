How the Page Run Workflow gives each Run its identity, its evidence layers, and its full address; moved from SKILL.md.

## 🧱 Workflow orchestration and Run identity

The Page Run Workflow Definition/Runtime is the orchestration authority. A
Level-4 Run is one independently closable Ticket → Result attempt. A Run Spec
is the planned node that gives that Run its bounded target, actor, gates, routes,
skill binding, and Result contract:

```text
CONTEXT      adapter dispatch; Run Specs resolve planning inputs
SHAPE        inside shared `run-structure-<slug>`; it defines Bullet and Evidence Item contracts
SURVEY       inside shared `run-structure-<slug>`; it inventories/references/reserves the graph
LAND         Runs exist: Supporting Execution/Discovery/Insight, then one Page RE per item
EMBED        no Run; it interprets ready Results into the plan
CONTENT      after the Page release barrier, adopts all agreed Writing Results and reruns the Delivery Runs
CHECK        no Run; it is a version gate
```

For interactive writing, `run-structure-<slug>` records the human exchange for the
closable Page map through both SHAPE and SURVEY; each sibling Page Run records
its own independently closable Section or paragraph-group goal. Planning or a
`fn/Runs` proposal alone still does not allocate a Run. A writing Version's
human closure is not the whole-Page CHECK/CLOSE verdict.

The two evidence layers are mandatory and named separately:

```text
Supporting Runs  0..N  Execution, Discovery, or accepted Insight item execution
                         ↓ Results
Local Input        1    one frozen envelope per Evidence Item
                         ↓
Page RE            1    Page · Evidence Item execution lineage
                         ↓
Typed Result       1    VALUE | CITE | DISPLAY
```

There is no active PageX binding layer. Cross-Folder evidence must enter
through a Supporting Run Result. A governed page-local static source may be
named and frozen in Local Input. Related Page links belong to Context
Workspace for navigation and constraints; they do not become evidence by
being linked.

## 🆔 Run references

Use full real addresses for reuse and rerun:

```text
global Supporting Run    b01j02t03r04
Task-local new-run plan  b01j02t03        parent until LAND allocates rNN
Task-local allocated     b01j02t03r05
Page Evidence lineage   `run-citation-<slug>` → owner-native Ticket/Result
Page Delivery Run       run-delivery-webpage | run-delivery-latex | run-delivery-word (fixed)
Other local Run plan     <owner-native parent or permitted reserved address> · plan
local Ticket filename    r05_page-evidence-item_e03-cite-prior-work
Delegated writing Task   r06_page-writing_c02-p01
Structure + Bullets      `run-structure-<slug>` or `run-structure-<slug>`
Section-level writing    `run-section-<slug>` or `run-section-<slug>`
Paragraph-level writing  `run-paragraph-<slug>` or `run-paragraph-<slug>`
```

SURVEY names the real owner/parent for every new local route. The Page's RE is
the stable Page-local lineage identity; any underlying owner-native
Ticket/Result keeps its own naming contract. A full address may be reserved
only when that owner contract permits it; the route remains `new-run` with no
Ticket. LAND allocates the owner-native Run id and records it under the RE
lineage. The interactive workflow creates
the structure/Bullet Run first, then a Section-level or paragraph-level Page Run
for each selected writing scope;
CONTENT consumes its accepted output.
Those allocations do not consume one another's counters: RP, RE, and Task
Run `rNN` sequences are independent; a Delivery Run has no counter. Task or Discovery identities are never
rewritten with an `rp`, `re`, or `rd` prefix.
The single-paragraph delegated profile remains available when explicitly selected.
