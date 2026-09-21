# Library pickup workflow walkthrough

This is a planning and presenter validation exercise. The real proposal is uncommissioned: eight Brief lines, eight registered items, zero Design Runs, zero ready items. No human release, live Board write, independent design review, distribution, or measurement happened. Records under `fixtures/` are manufactured examples with conspicuous synthetic actor names; their successful checks establish contract and presenter behavior only.

## Inspectable material

- Bounded Brief: [BRIEF.md](/tmp/design-workflow-validation-20260920/BRIEF.md).
- The canonical draft Brief and eight registers: [proposal Board](/tmp/design-workflow-validation-20260920/proposal/LibraryPickup-DesignBoard/board.md).
- Proposed portfolio: [Goal preview](/tmp/design-workflow-validation-20260920/previews/proposal-goal.html), [Design preview](/tmp/design-workflow-validation-20260920/previews/proposal-design.html), and [snapshot](/tmp/design-workflow-validation-20260920/checks/proposal-snapshot.json).
- Synthetic ready portfolio: [Goal preview](/tmp/design-workflow-validation-20260920/previews/portfolio-goal.html), [Run preview](/tmp/design-workflow-validation-20260920/previews/portfolio-run.html), [Delivery preview](/tmp/design-workflow-validation-20260920/previews/portfolio-delivery.html), [snapshot](/tmp/design-workflow-validation-20260920/checks/portfolio-snapshot.json), and [CSV](/tmp/design-workflow-validation-20260920/checks/portfolio-bundle.csv).
- Executed checks: [results](/tmp/design-workflow-validation-20260920/checks/executed-checks.json), [CLI audits](/tmp/design-workflow-validation-20260920/checks/cli-audits.json), and [construction/check script](/tmp/design-workflow-validation-20260920/validate.py).

The HTML files are local generated presenter documents, not hosted Board URLs. No Board server was started. They were inspected through snapshots and generated markup; browser visual review was not performed. A UI card or dashboard visual criterion would still need actual rendering and image inspection before a real review could pass.

## The eight item contracts

Each row is one audience × job × primary venue, with one requested design and one `ITEM01` in its own stable `2-Design/Design-NN-…` folder. Every item has `basis: brief-only`, `stance: generate`, `mode: compose`, `unit: {shape: single, count: 1}`, and a proposed iteration budget of two. Expected-effect and failure forecasts may remain null in compose mode. The following deliberately simple acceptance conditions are the only fixture criteria, compiled to one `contains` check each. They do not substitute for full venue quality review.

| Brief line / folder | Audience and job | Requirement | Acceptance condition | Selected venue guidance for real commissioning |
|---|---|---|---|---|
| R1 / Design-01 | Library members; collect held books | Name the library in the SMS | Message contains `Community Library` | SMS: one action, opt-out, available variables, preferably at most 160 characters. The 95-character fixture fits. |
| R2 / Design-02 | Library members; plan a pickup | Name the pickup job in the email subject | Artifact contains `Subject: Your library pickup` | Email: specific subject at most 60 characters, descriptive links, clear sections. The sample subject has 19 characters; the short fixture is not a complete 200–800-word email. |
| R3 / Design-03 | Library app users; open pickup details | Name the notification's tap action | Notification contains `View pickup details` | Push: title at most 50 characters, body at most 100, one specified destination. The sample title/body use 18/20; `{PICKUP_DETAIL_SCREEN}` remains a proposed binding. |
| R4 / Design-04 | Library members; remember pickup deadline | Make the reminder deadline explicit | Reminder contains `by {DATE}` | Reminder: supportive wording and at most 200 characters. The 84-character fixture is one example. Freeze the requested `unit.shape/count`; three to five variants is the rotating-set default, and a single example does not claim to complete a rotating set. |
| R5 / Design-05 | Library app users; view pickup instructions | Give the card a pickup action label | Card specification contains `View pickup details` | UI card: header → detail → action, named data bindings, actual script-free HTML screen and Result-local render for visual review. The text fixture is only a contract specimen. |
| R6 / Design-06 | Pickup desk staff; prepare pickup handoff | End the checklist with a completion check | Checklist contains `Confirm the handoff is complete` | Checklist: 5–12 action-led, completable entries in logical order. The fixture has five; the library must supply operational procedure before live use. |
| R7 / Design-07 | Library managers; review portfolio scope | State the absence of measured effectiveness evidence | Report contains `No measured effectiveness evidence is available.` | Report: scope, requirements, limitations, and next decision. Cite the mandate/Brief as the scope source, without inventing effectiveness studies, findings, or data plots. Set an explicit word budget before release. |
| R8 / Design-08 | Pickup desk staff; inspect sample pickup status | Label the dashboard data as synthetic | Dashboard specification contains `SAMPLE DATA` | Dashboard: summary → detail → action, panel jobs, source bindings, refresh and interaction notes. Use placeholders and a static synthetic source contract; do not imply real-time integration. |

Each folder's `outline/<stem>-design-items.md` contains the item goal and its acceptance rule. These registers contain no progress state. Synthetic examples are in the corresponding fixture's `results/rd02_generate_item01/content/<venue>.txt`; they are intentionally short record specimens, not eight production deliverables. The UI and dashboard files are specifications, not implemented interfaces.

The Brief has its eight required fixed divisions. Its only table with all three header words `audience`, `job`, and `venue` is the final design list, so the parser selects the intended rows. It records mandate birth, not invented signed Wisdom. QD1 asks which operational fields and destinations are available; QK1 asks what evidence exists about effectiveness. Both remain neutral and unanswered. They block future operational use or empirical claims, not the permitted brief-only drafts.

## Workflow and file contracts

The Brief is a precondition, not a Design Run. Its draft has not passed its separate Page workflow or release. A real caller would first resolve/release the Brief under that workflow, then seek the named human's exact Commission decision. Preparing this packet does not supply either approval.

For each real item, the current route is:

```text
Commission: named human decides release or hold on exact frozen config
  release -> Generate: named agent produces and self-checks one bounded draft
  hold    -> stop; a person can release later through a new Commission
Generate records check passes -> Verify: genuinely fresh independent context
Verify complete/pass + clean records -> read-only Delivery of exact bytes
Verify complete/fail -> new Generate revise, then independent Verify
Verify invalid/unresolved -> failed Verify; queue a new review
```

No Delivery Run or second adoption gate is created. With no earlier holds, one completed ordinary item has `C=1, N=1, J=1`, or three current Design Runs. Eight ordinary items therefore have a planned minimum of 24. The proposal actually has zero. The separate synthetic portfolio contains 24 manufactured records, all paired and structurally valid. A held decision adds a Commission identity, and failed/blocked/superseded Runs remain in actual counts; attempts inside one Run and renderer calls do not add identities.

For one folder, the ordinary synthetic record paths are:

```text
outline/<stem>-design-items.md                 goal and rules
scripts/config/commission_item01.yaml          fixture's frozen Commission config
runs/rd01_commission_item01.yaml               human-decision Ticket specimen
results/rd01_commission_item01/decision.yaml    synthetic decision specimen
results/rd01_commission_item01/runtime.yaml     caller receipt specimen
runs/rd02_generate_item01.yaml                 worker Ticket
scripts/config/rd02_generate_item01.yaml        derived frozen config
results/rd02_generate_item01/result.yaml        exact artifact/check hashes
results/rd02_generate_item01/checks.yaml        one check per artifact × criterion
results/rd02_generate_item01/content/<venue>.txt
results/rd02_generate_item01/runtime.yaml
runs/rd03_verify_item01.yaml                   independent-review Ticket specimen
scripts/config/rd03_verify_item01.yaml          same design fields, independent review
results/rd03_verify_item01/result.yaml          exact target Result hash
results/rd03_verify_item01/checks.yaml
results/rd03_verify_item01/runtime.yaml
```

The production writer names its Commission config after the complete Run id; the fixture helper uses `commission_item01.yaml`. Both references resolve, and the current checker accepts the fixture convention. Ticket file stem and Result folder always share the exact `rdNN_*` identity.

A Commission pins config and item evidence files, not the Brief version, `reads:`, or venue packs. The caller must therefore compile acceptance rules before release. Downstream config copies preserve goal, intent, basis, unit, rules, and budget; only permitted operation mode and review mode differ. Evidence-informed work requires the exact approved source chain. Here the evidence list is empty because the explicit basis is brief-only; no measured effect is claimed.

The caller owns allocation, human authority and runtime. The worker owns only its paired Result, excluding runtime. Before real dispatch the caller names the actual worker with `name_worker`; afterwards `complete_run` records the actual records-check result and route. Merely changing an actor label never establishes independent review. Fixture reviewer labels are explicitly fictional.

Page and Design workflows share the folder but have separate identities, counters, Results, gates and receipts. Page explanation edits cannot release a Commission or verify a draft. Changes to the draft itself require a new Design Generate revise with frozen base and feedback. Design readiness alone does not release the Page. No Page Run was allocated by this validation.

## What the five Spaces show

| Space | Page level | Board level |
|---|---|---|
| Goal | One Brief promise and wanted/registered/ready counts | All eight Brief promises and aggregate counts |
| Design | One card per item, its goal, rule, draft, state and permitted actions | Every item with folder, state and who is awaited |
| Insight | Explicit basis and any supporting sources | Shared InsightBoards and source usage; here none are declared |
| Run | Actual Commission, Generate and Verify ids, actors, outcomes and receipts | Cross-folder waiting queue and unchanged Run identities |
| Delivery | Exact Verify-passed draft, read only | Ready items and the CSV projection; no distribution authority |

The proposal snapshot reports 8 wanted, 8 registered, 0 ready, and 0 Runs. The synthetic ordinary snapshot reports 8 wanted, 8 registered, 8 ready, and 24 Runs. Both report no records-check findings, and neither presenter mutated any source files. All eight venue strings survive the parser and CSV export. The static Board twin has no download link.

## Required recovery cases

### A person held a Commission and later releases it

Preserve the completed hold decision. Record the later named human release as a new Commission Run for that same item; do not overwrite the first decision. The item may have several held decisions but at most one released Commission. The tested fixture goes from `rd01_commission_item01` hold to `rd02_commission_item01` release and changes `commission held` to `commissioned`; the original decision hash is unchanged. After release, a change to the registered goal/rules belongs to a new item and Commission. This packet does not authorize the future release.

See [before release](/tmp/design-workflow-validation-20260920/checks/held-before-release.json) and [after synthetic release](/tmp/design-workflow-validation-20260920/checks/held-snapshot.json). The current action code explicitly permits a new Commission action for a held Commission while refusing a second release.

### A worker cannot proceed because a source is missing

The worker names the missing source and writes no Result; its hold diagnostic is not a human HOLD decision. The caller resolves the operational source or raises a neutral Brief/Insight need rather than inventing data. An undispatched queued record stays queued or is replaced truthfully. A recorded blocked receipt remains blocked, names the Run and repair owner, and offers no Commission Release button. Repair is a caller responsibility. A changed queued pin must be superseded and replaced, never edited in place. Preserve terminal history when allocating any subsequent valid work.

The [blocked fixture](/tmp/design-workflow-validation-20260920/checks/blocked-snapshot.json) says `blocked`, identifies `rd02_generate_item01`, and names the missing pickup-hours source and caller. It contains no worker Result and passes the inventory audit. It tests the display of a declared diagnostic, not a live source failure. The skill gives no one-command UI resume for a terminal blocked Run; the caller must repair and allocate according to the workflow rather than click Release.

### A completed independent review rejects a draft

A fully performed review with complete coverage and verdict `fail` is a completed Verify Run. It routes to Generate and displays `verify failed`; the person queues a revise with concrete feedback. The next Generate pins the old draft as base and a new feedback file. It preserves the released design fields and completed Results. After revision, a genuinely fresh context reviews the new exact Result. Do not rerun a completed valid review of the same unchanged candidate.

The [rejected-review fixture](/tmp/design-workflow-validation-20260920/checks/rejected-review-snapshot.json) is structurally valid, has state `verify failed`, and has no Delivery candidate. In contrast, unresolved checks or invalid coverage make the review itself fail the records check: state `verify invalid`, route Verify. That distinction comes from the Unit contract and `design_actions.complete_run`, not a discretionary human HOLD.

### A supplied older folder contains Adopt records

First inspect for decisive unsupported markers. Current v2 `rdNN_adopt_*` records are the narrow historical exception. Keep their real ids, show `Adopt (historical)`, and treat them as retained audit/delivery evidence. Do not create an Adopt Run or make it a new gate. Historical adopted content still needs its exact passing Verify authority to appear in Delivery; a historical decline is excluded. A historical hold instructs the caller to register a new item before continuing.

The [historical Adopt fixture](/tmp/design-workflow-validation-20260920/checks/historical-adopt-snapshot.json) retains `rd04_adopt_item01`, labels it historical and shows ready. The [decline fixture](/tmp/design-workflow-validation-20260920/checks/historical-decline-snapshot.json) retains the same original operation identity and is excluded from ready Delivery.

An older folder with v1, `rNN_design_*`, `design/DU*/`, PageX, `2-DS-design/DS*`, or phase-shaped legacy content is refused; it is not silently migrated or continued. The [v1 specimen](/tmp/design-workflow-validation-20260920/checks/legacy-v1-snapshot.json) is refused before loading Runs. If the owner elects to retire such a folder, the Design guidance says to park it under the board's `_archive/` and remove its `## Pages` entry; this simulation moves nothing.

## Execution and limits

`PYTHONDONTWRITEBYTECODE=1 python3 /tmp/design-workflow-validation-20260920/validate.py` constructed the isolated fixtures and executed 20 named checks. The first run passed 19 and exposed one verified-artifact corruption issue. After the parent's repair, the same assertions pass 20/20; the changed specimen is excluded and all eight unchanged valid items remain ready. The initial failure and repaired behavior are preserved in [OBSERVATIONS.md](/tmp/design-workflow-validation-20260920/OBSERVATIONS.md). No contract helper was used to make an actual human decision, no action endpoint was called, and no worker was dispatched.

Four independent CLI inventory checks used `python3 -B <design-unit>/scripts/check_unit.py --folder <fixture>`: blocked, rejected-review and historical-adopt exited 0; tampered-ready exited 1 with the expected hash mismatch findings. The initial presenter incorrectly exported changed text with the original hash; that evidence is preserved under `checks/before-repair/`. The repaired presenter labels the item `records invalid`, provides the repair reason/owner, and emits no row for it. Current generated CSV and hashes are preserved under `checks/tampered-export.*` and `checks/repaired-behavior.json`.

The three explicit relative Markdown links in the selected Design skill/reference set resolve. Every selected venue directory and profile used for this walkthrough exists. These checks are narrow; they do not prove all prose-mentioned paths throughout the repository exist.

The repository had extensive pre-existing changes. Validation read applicable root guidance and relevant skills/code only, did not read evaluations, reports, implementation diffs, parent conversation, or the other validation folder, and wrote only under this isolated temporary directory. No repository edit, server, live Board operation, publication, or measured claim resulted.
