---
name: haipipe-page-evidence
description: >-
  The 02 EVIDENCE phase of a Board Page:
  LAND executes each typed Evidence Item graph (zero-to-many Execution/Discovery
  Supporting Runs, freezes one Local Input, then executes exactly one Page
  Evidence Run (`RE`) lineage per item) and EMBED
  folds the ready local Result into the next outline version. Never plans the outline,
  writes Content, or interprets evidence inside an upstream Run. Trigger: page
  evidence, EVIDENCE phase, land evidence items, make supporting runs, make the
  local run, embed the result, fold evidence, /haipipe-page-evidence.
metadata:
  version: "0.25.0"
  last_updated: "2026-09-14"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-evidence · LAND each item graph, then EMBED ready Results

EVIDENCE changes what a Page can safely know. It does not choose the outline
shape and does not write a sentence of `## Content`.

```text
Page planning and evidence loop
  SHAPE    outline    specify item identity + expected ready evidence  👤 approved:
  SURVEY   outline    inventory supports + input + local RE             👤 Decide
  LAND     this file  allocate planned Tickets, execute → local Result ⚙ ready
  EMBED    this file  bind Result into v<G>.<S>.<E+1>          ⚙ CONTENT when G≥1
```

Load contracts in this order:

```text
haipipe-page
  → haipipe-page-workflow
  → haipipe-page-evidence
  → the Folder-owning workflow or canonical family skill
  → the exact Page Face owner skill
  → the exact narrative/style policy, when it governs Page interpretation
  → haipipe-plugin-outline/ref/item-table.md
  → haipipe-page/ref/page-run-families.md
  → haipipe-plugin-outline/ref/plan-grammar.md (EMBED only)
  → haipipe-plugin-outline/ref/evidence/values.md | citations.md | displays.md
    (LAND only, select the item's exact type contract)
  → haipipe-run
  → the exact Supporting Run workers selected by SURVEY
  → the renderer craft selected by haipipe-plugin-outline for DISPLAY
```

The Page surface already installs `haipipe-plugin-outline` as the shared
presenter. The refs above are EVIDENCE's payload/material contracts, not a
second presenter invocation.

The `haipipe-page-context` PREPARE record must be fresh before this chain acts.
Do not load or route through a separate Task Page-Type layer. The Folder owner
and exact Page Face owner supply semantic policy; this skill owns only the Page
EVIDENCE cycles. For a Task Folder, `haipipe-task` fills both roles and is
loaded once, with `haipipe-page-task` as its reader-facing companion for Page
display and prose requirements, not another execution owner.

## ⚡ Phase card

```text
READS    target Page · checked v0 plan or approved G>=1 plan · current
         outline/<stem>-evidence-items.md contract · selected Run
         Tickets/receipts/Results · frozen Context · current Result manifests
WRITES   Supporting and local Run receipts/Results in their owner-governed
         Run and Result stores ·
         one local Page Evidence Item Result per make-item · Result pointers
         in the table · next-working-plan fold lines
NEVER    target prose · item identity/type/Target/Expected/Acceptance · outline
         order · a Decide · a typed Status · PHI or raw rows in Page artifacts
EXITS    LAND: every locally attainable make-item has valid Supporting Results,
         one frozen input, and one ready local Result that passes its authored
         Acceptance checks; every remaining server/person gate is named · EMBED: every
         ready item is folded; v0 returns to SHAPE, G>=1 refreshes CONTENT
HUMAN    owns Decide and any worker-specific verification gate; LAND and EMBED
         never synthesize those decisions
```

## ⚖️ The evidence boundary

Keep four objects distinct:

```text
Supporting Result   detailed reusable output from Execution or Discovery
Local Input         one frozen envelope of Supporting Results + governed local sources
Local Result        one typed, focal, ready-to-use Evidence Item Result
Page interpretation what this ready Result means for this bullet, written at EMBED
```

An upstream Result never becomes Page evidence just because it exists. The
local Run validates, normalizes, and packages the focal item. It still carries
no Page argument: EMBED owns the interpretation.

## 🗺 Phase × Run Map

| Cycle | Level-4 Run operations | Cardinality | Close |
|---|---|---:|---|
| SHAPE | none | 0 | typed item expectation checked; Content release approval is separate |
| SURVEY | inventory + classify only | 0 allocations, 0 executions | each route is existing Result, Ticket only, rerun, or new design + Decide |
| LAND · Supporting | allocate/scaffold planned Execution / Discovery routes, then execute or reuse | `sum(S_i)`, `S_i ≥ 0` | every declared Supporting Result valid |
| LAND · Local | allocate/scaffold, then execute one Page `RE` per Evidence Item | exactly `N_make` | one ready local Result/Card per make-item |
| EMBED | none | 0 | every ready Result folded into the next working version |

There is no umbrella Page-wide Evidence Run. Each Evidence Item gets one
current Page `RE` lineage. Supporting Runs remain owner-native Level-4 Runs;
calls, scripts, retries, render passes, and agent turns inside one RE do not
add Page Run identities. A current RE emits one Result, which the Outline may
show as one Evidence Card with many Labels.

### Run Profile · Page · Evidence Item

```text
ALLOWED      operation: evidence-item; item type: VALUE | CITE | DISPLAY
TARGET       exactly one E<NN>-<TYPE>-<slug>
PAGE RUN     one typed `re-value-NN_<slug>`, `re-display-NN_<slug>`, or
             `re-cite-NN_<slug>` identity for this item's Page lineage
TICKET       Folder dialect selected by haipipe-run; full owner-native Run id when execution is Task-backed
INPUTS       one frozen envelope: item contract + 0..N Supporting Result paths,
             Run ids, receipt hashes, and any governed page-local source pointers
WORKER       haipipe-plugin-outline owns VALUE/CITE/DISPLAY payload rules;
             DISPLAY may dispatch a renderer craft beneath that one plugin
RESULT       runtime receipt + typed evidence-item result + safe artifact pointers; bind the matching typed RE id
ACCEPT       every SHAPE acceptance check passes; provenance resolves; aggregate only
PROMOTION    LAND binds Result to item; EMBED binds it to the next outline version
REOPEN       changed support Result/hash or item contract makes the binding stale
```

Resolve every physical Result through the Ticket's governed store contract.
When a dialect declares `result_store:`, follow that value; when its launcher
resolves `RESULT_STORE`, record the resolved safe path in the receipt and item
binding. Never assume Results sit beside the Task, and never copy governed
outputs into the Page merely to obtain a local-looking path.

A conventional local Run name is
`r07_page-evidence-item_e01-value-adjusted-effect`; its runtime receipt records:

```yaml
family: page
operation: evidence-item
target: E01-VALUE-adjusted-effect
```

## 🛬 LAND · execute one dependency graph per item

Before declaring evidence missing, search the Folder owner's current Result
store, governed `_WorkSpace` stores, and explicit `old/` directories. A
recovered prior output is a **provisional Supporting Result binding**, not a
new action: record its exact path and hash, use it when it satisfies the
current contract, and mark it stale automatically when a newer canonical
Result for the same target lands.

For every item whose `Decide` is `☑ make`:

1. **Validate the plan.** Confirm type, Target, Expected, Acceptance, Supporting
   Runs, one Local Input, and exactly one Local Run. An invalid meaning routes to SHAPE; an
   incomplete graph routes to SURVEY.
2. **Resolve Supporting routes.** Work only the routes SURVEY selected:
   existing full Run ids classified `reuse`, `rerun`, or `registered`, plus
   bounded `new-run`, `new-task`, `new-job`, or `new-block` plans. Supporting families
   are Execution and Discovery; an accepted Insight instance/item Result may
   also be reused under `haipipe-plugin-outline/ref/item-table.md`'s qualified
   identity and owner contract. Keep its instance/version intact. Search the governed current and old
   Result stores before concluding that a selected support is unavailable.
3. **Allocate before execution.** An existing route keeps its registered
   owner-native full id (`bNNjNNtNNrNN` for Task-backed work). For a planned route, invoke the owning Execution or
   Discovery workflow now to allocate one real `rNN`, scaffold its Ticket and
   planned runtime receipt, and write that full id back to the item lineage.
   A rerun uses the same target, frozen inputs, and acceptance contract; a
   material change routes back to SURVEY for a new design with `supersedes`.
4. **Require valid Supporting Results.** Trust no claimed `complete` without
   the owning worker's Result gate and runtime receipt. Preserve truthful
   failed or blocked receipts; do not invent `none` or ask a `person` action.
   A recovered old Result may be bound provisionally with its hash when it
   passes the present acceptance contract; a later canonical Result with the
   same target supersedes that binding and reopens LAND or EMBED as needed.
5. **Freeze one Local Input.** Materialize the SURVEY plan as one immutable
   envelope containing exact Supporting Result pointers/hashes plus any named
   pre-existing governed page-local artifacts. Cross-Folder evidence must
   arrive through a Supporting Run Result; Related Pages in the off-stage Context record
   do not become evidence automatically. Zero supports is valid only when the
   planned local material or item contract is
   sufficient. Never smuggle a sibling Evidence Item's future local Result
   into this envelope; if two items need the same evidence, both name the same
   upstream Supporting Run.
6. **Allocate and execute exactly one Page `RE` lineage.** Reuse the real
   Ticket when SURVEY found one; otherwise allocate the next typed RE id:
   `re-value-NN_<slug>`, `re-display-NN_<slug>`, or `re-cite-NN_<slug>`, and
   scaffold its Page · Evidence Item Ticket from the bounded local declaration
   before execution.
   A Task declaration names parent `bNNjNNtNN` and LAND writes back the full
   `bNNjNNtNNrNN`; another Folder-local owner follows its current naming
   contract and Run Profile, preserving a reservation only when that owner
   permits one. The Page `RE` identity is the lineage join; it does not rename
   the owner-native Ticket or Result. It targets this Evidence Item and emits
   one typed Result. The RE may invoke several scripts or calls internally;
   its Result/Card may expose zero-to-many `$V_xxx$`, `\figure{D_xxx}`,
   `\table{D_xxx}`, and `\cite{C_xxx}` Labels. A label does not allocate a
   child Run; split only when the label needs independent provenance,
   acceptance, or lifecycle. Retries remain attempts in the same lineage
   because target and Result gate are shared.
7. **Bind the local Result and update its action.** Allocation changes
   `new-run` to `registered`. A Result that passes the authored Acceptance
   checks changes it to `reuse` and
   appends the allocated global id plus `→ <result path>`; a failed, invalid,
   smoke-only, or stale attempt changes it to `rerun`. The Run receipt preserves
   history; the item row states the current next action. Do not point the item
   directly at a raw Supporting Result.
8. **Apply the CITE verification gate.** For a CITE item, present the source
   identity, focal claim, and locator for human verification. Record a durable
   `Verified: ✅ <who> <timestamp>` on that item row. A machine never signs it,
   and the CITE item remains not-ready until it is signed.
9. **Promote the verified bibliography entry.** After a CITE item is signed,
   write its verified entry into the bibliography declared by the Page Face
   owner (the Page's register, or a Paper room when that owner requires it) under
   the same citation key. If that key already exists with a different body,
   report the conflict and do not overwrite either entry. A ready CITE Result
   is not complete for delivery while its verified key is absent from that
   bibliography.

Different item graphs may run in parallel because cross-item local-Result
dependencies are forbidden. Within one graph the local Run waits for every
declared Supporting Result to validate. This dependency is
the only required ordering. LAND exhausts every route runnable on the current
machine before returning. Only a secure-server requirement or an explicit
person gate may stop the pass; the receipt names which one stopped it, or says
`nothing left`.

### Actions are not families

| Action | LAND behavior |
|---|---|
| `reuse` | validate the named full Run id and accepted Result; execute nothing |
| `rerun` | execute the same registered Run contract and append its attempt trail |
| `registered` | execute the registered Ticket for the first time |

Discovery is handled as a Run family. A CITE item can therefore reuse or
commission Discovery work without a special citation route.

## 🧰 Typed local Results

The common Result envelope is `<resolved-result>/result.yaml`. It names item
id, type, local Run id, frozen input, Supporting Run ids, governed local-source
hashes, payload paths, acceptance checks, and provenance. Its sibling
`runtime.yaml` owns execution lifecycle facts. `haipipe-plugin-outline` owns
the exact common keys and typed payload extensions:

The same manifest may include root-level `labels:` entries for the current
Result/Card. Each entry joins one authored `$V_<slug>$`, `\table{D_<slug>}` /
`\figure{D_<slug>}` / `\algorithm{D_<slug>}`, or `\cite{C_<slug>}` token to `kind`, `target`,
`status`, and optional reader-facing `display`. One RE/Result/Card can expose
zero-to-many labels; a resolved `display` never erases its token, and the
reader-side disclosure preserves Item, RE, Result path, target, and provenance.
An unresolved label remains visible during draft review and is a release gate
only when the selected final export requires that evidence.

VALUE, CITE, and DISPLAY are Result types, not three sibling payload
directories. The Evidence Item contract is declared by the Outline plan and
its Result manifest; its Page-owned execution lineage is the `RE` ticket under
`runs/`. The authoritative payload from a real local Run lives at the Result
address resolved by its Folder dialect (`results/<RUNNAME>/` for Folder-local,
or `$OUTPUT_ROOT/results/<task>/<RUNNAME>/` for a Task), while an external
payload stays at its Supporting Run's own Result path. Never introduce
`outline/evidence/value/` as a second copy of a VALUE Result.

DISPLAY is the umbrella Result type for a table, figure, or algorithm block.
Conceptual diagrams and AI illustrations are cited as ordinary figures. LAND may render a concrete unit and mark the local Result
ready when the Evidence Item's `Acceptance` checks pass. The governed Result
envelope records the source local Run id, resolved Result path, unit pointer,
and hashes; it does not require an intermediate `outline/evidence/display/`
copy that is later moved into the Page. The lowercase human `accepted:`
decision on the display unit is separate and is administered later by CHECK;
it is not a LAND or EMBED prerequisite.

For a consumer-serving canonical Task, that PHI-safe admitted unit is the one
narrow Page-authority exception to the rule that generated output stays under
`$OUTPUT_ROOT`. The paired `result.yaml` and `runtime.yaml` remain in
`$OUTPUT_ROOT/results/<task>/<RUNNAME>/`; the unit does not become a second
Result store.

| Type | Local Result must make ready |
|---|---|
| VALUE | value(s), units, population/denominator, method label, uncertainty when expected, reproducible provenance |
| CITE | verified source identity, supported focal claim, locator, and provenance to Discovery/support Results; the CITE row's `Verified` gate is signed |
| DISPLAY | frozen intake, build recipe, selected artifact plus required image/PDF `preview`, caption claim, `display_kind`, and provenance |

No local Result may contain raw sensitive rows, credentials, or an argument
about what the Page should conclude.

## 📌 EMBED · interpret the ready Result for this Page

EMBED reads only ready local Evidence Item Results that pass their authored
Acceptance checks, not raw Supporting
Results. For each ready item:

- `VALUE` or `CITE`: append
  `Answered: <item id> · <page-specific reading> · <local Result path>` under
  its target bullet.
- `DISPLAY`: append
  `Drawn: <item id> · <artifact claim> · <local Result path>` under its target
  bullet.
- Preserve the item id, expectation, acceptance, bullet head, order, and
  structure. EMBED fills; it never restructures.

If a ready Result contradicts the outline, open a `D<nn>` thread and route to
SHAPE. Otherwise preserve the Shape exactly and write the next evidence
revision `v<G>.<S>.<E+1>`. The two-part source `v<G>.<S>` has implicit
`E=0`. Set `supersedes:` to the exact source version. For `G=0`, keep
`approved: ⬜` and return to SHAPE; CONTENT remains closed. For `G>=1`, add
`shape-base: v<G>.<S>`, transcribe `approved: ✅ inherited from v<G>.<S> · …`
from that approved Shape, and route to CONTENT so every changed evidence
binding refreshes its affected realizations. Do not request another Shape
approval for a pure fold. A changed Supporting or local Result after the fold
makes the binding `stale` and reopens LAND or EMBED as needed.

## 🔀 Routing

```text
LAND   item meaning/acceptance invalid                  → OUTLINE / SHAPE
LAND   governing Context is stale or conflicting       → CONTEXT / PREPARE
LAND   Run graph or Local Input incomplete             → OUTLINE / SURVEY
LAND   support/local Run truthfully failed or blocked  → EVIDENCE / LAND or HOLD, with Run id
LAND   every locally attainable item is ready; remaining server/person gates named → EVIDENCE / EMBED
EMBED  ready Result contradicts the outline            → OUTLINE / SHAPE with D<nn>
EMBED  every make-item Result folded under G=0         → OUTLINE / SHAPE with evidence revision
EMBED  every ready Result folded; remaining gates named and defer/drop signed under G>=1 → CONTENT / WRITE only for a pure evidence revision or an explicit CONTENT instruction
```

EVIDENCE routes directly to CONTENT only for a pure evidence revision or an
explicit CONTENT instruction under an already approved `G>=1` Shape, after all
remaining gates are named and defer/drop is signed. A contradiction or any
Shape change still returns to SHAPE. Generation zero never reaches CONTENT.

## 🧾 Receipt

```text
phase: EVIDENCE
cycle: LAND | EMBED
items: n make · n deferred · n dropped · n ready · n folded · n stale
item-status: grouped by VALUE/CITE/DISPLAY · item → decided · landed · folded · ready · attainability local/server/person
supporting-runs: Execution n · Discovery n · reused n · rerun n · registered n
evidence-runs: n planned · n running · n done · n failed/blocked
bindings: item id → typed RE id → owner-native Run id → Result path → Card/Labels
previews: DISPLAY item → rendered image/PDF viewer link
folded: item ids written into the next working outline version
limits: Run ids that did not complete and truthful reasons
stopped-by: server <what> | person <what> | nothing left
route: CONTEXT | OUTLINE | EVIDENCE | CONTENT | HOLD
next_cycle: PREPARE | SHAPE | SURVEY | LAND | EMBED | WRITE  # omit on HOLD
```

Legacy material under `outline/evidence/` and generated `*-evidence.md` files
are not read by LAND or EMBED. Before execution, move them to
`_archive/legacy-outline-evidence/`; an unmigrated Page is a migration blocker,
not a partially supported Page.
Resolve execution artifacts through the Folder owner's Run dialect: a
Folder-local owner uses sibling `runs/` and `results/`; a canonical Task keeps
its Ticket under the Task's `runs/` and its generated Result under the resolved
`$OUTPUT_ROOT/results/<task>/<RUNNAME>/`. No LAND step may copy a Result merely to make it
look local, create a new `outline/evidence/` lane, recreate a root
`<page>/evidence/` category, or create a standalone Evidence tab.

Read fully only the target Page, checked v0 plan or approved G>=1 plan, Evidence Item table, named Run
receipts, and Results required by the current item graph. Keep broad build logs
and unrelated sibling Pages out of context.
