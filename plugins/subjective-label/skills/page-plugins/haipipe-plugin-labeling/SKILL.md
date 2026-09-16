---
name: haipipe-plugin-labeling
description: >-
  The 🏷 Labeling lane and full Page-level surface available beside any real Page,
  including a standalone Page Folder: an optional page-local labeling/ holds the canonical subjective-label
  job, the full Labeling Space offers receipt-first Workflow, Data, Guideline,
  Human, Quality, and Runs workspaces; Studio Chat remains a sibling transport
  surface. Use
  when designing, opening, diagnosing, or implementing the labeling
  plugin/tab/folder, or /haipipe-plugin-labeling.
metadata:
  version: "0.11.0"
  last_updated: "2026-09-16"
---

# /haipipe-plugin-labeling · one job, one folder, one operated surface

**LOAD `haipipe-plugin` and `subjective-label` FIRST.** This is a LANE plugin:
it owns the `labeling/` roster row and its own surface. The family workflows
own semantic order and writes; this skill owns how that job lives beside and
appears beside one Page.

```text
one page folder
├── <stem>.md                    what the Page says
└── labeling/                    the job itself · canonical
    ├── config.yaml · corpus/ · policy/ · rounds/ · gold/ · handoff/
    ├── test/ · evaluation/ · production/ · audit/
    ├── gates/                      P0 contract + G0 receipts
    ├── runs/ · results/            Level-4 `rlNN` operation envelopes
    └── REPORT.md · .state.json  rendered/cache only; receipts win

🏷 Labeling Space · one full Page-level plugin surface
├── Workflow                 P0-P5 · G0-G6 · next action
├── Data                     corpus · embeddings · batches · D*
├── Guideline                meaning · regions · policy versions · handoff
├── Human                    authority · rounds · bounded human work · gold
├── Quality                  sealed Test · executors · Scan · Audit
└── Runs                     rlNN Tickets · safe Results · read-only

Studio remains a sibling Page plugin and opens on demand; it is not rendered
inside Labeling as a permanent bottom panel.
```

## 🧩 The four-part plugin contract

| part | contract |
|---|---|
| STORAGE | `<page>/labeling/`, exactly the job layout in `subjective-label/ref/ref-assets.md`; MIXED because canonical PRIMARY receipts and rendered views coexist |
| SURFACE | one optional `🏷 Labeling` right-pane tab on a real Page; it fills the plugin pane as one Labeling Space with six switchable Workspaces, while Studio Chat remains a sibling transport surface |
| WRITER | `subjective-label-workflow` dispatches the Building/Scanning ORDER machines; their Keeper, human event writer, runner, reconciler, and auditor own named artifacts |
| BOUNDARY | Board discovery never enters `labeling/`; the surface never renders protected item text or sealed ids and never treats an observed file as a validated gate |

The specialized `page-type: labeling` Job Page owns one corpus snapshot × one
target construct × one identified human semantic authority and uses the
labeling Page grammar. That Page type is not a
capability switch: a paper section, algorithm Page, or other Folder may open
the same plugin before a job exists and route P0 creation through Chat. The
control Page `S-Label-Dash` owns no job and therefore gets no Labeling lane or
tab.

## 🖼 Surface law

The surface follows Outline's category pattern: one Plugin owns one coherent
Labeling Space containing stable, noun-named Workspaces. Phases are state,
never navigation. Switching a Workspace hides but does not destroy the others,
and the last selected Workspace is remembered per Board source plus Page file.
The six Workspaces answer:

1. **Workflow** — which P0-P5 authority artifact is the frontier, which G0-G6
   assertion fails first, and what is the one next action?
2. **Data** — which corpus, embedding, calibration/production batches, and
   audited D* artifacts exist?
3. **Guideline** — what frozen or draft meaning, regions, policy components,
   versions, and handoff exist?
4. **Human** — who is the authority, which rounds and human-work operations
   exist, and which human-gold artifacts are owned by their Keepers?
5. **Quality** — what sealed-Test, executor, production-Scan, and final-Audit
   evidence exists? It names the active destination reservation custodian and
   labels any imported source custody as provenance only.
6. **Runs** — which `rlNN_<operation>_<target>` Tickets and safe Results exist,
   with their availability and next action, without creating or executing one.

These are projections over the one canonical `labeling/` tree, not six new
`*-space/` storage folders. They render safe metadata and artifact state only.

`GET /_board/labeling` re-reads disk on every open. For a v2 lane with a
`gates/p0-contract/receipt.json` or `gates/g0/receipt.json`, it delegates P0/G0
truth to the canonical subjective-label status evaluator, including checksum
and receipt validation. A historical lane with no canonical receipt may say
“observed”, but it must not silently promote that observation to a pass.
`REPORT.md`, `.state.json`, and the Page's prose are useful views, never the
source of the frontier.

On a Board host, Labeling fills its own plugin pane. A header action may open the
exact generated-Page `?pane=chat` document that Studio owns, including its
composer, sessions, quick actions, settings, GUI/TUI handoff, and optional Draw
controls; Labeling never embeds that document as a permanent lower panel and
never implements a second Chat. The Board-source `board.md` is only the source
resolver and must never receive `?pane=chat`; the current generated
`<page>.html` URL is carried separately and validated server-side. Chat may
prepare or dispatch work, but a semantic decision becomes real only when the
owning workflow writer lands its canonical event immediately under `labeling/`.

On a standalone host, the domain-owned presenter does not imitate Studio or
invent an HTTP chat backend. It names the current Codex task as transport and
offers a copyable next-action prompt derived from canonical status. The same
rule holds: conversation is transport; only the workflow writer may land a
semantic event. The Page host keeps `labeling/` private from Source editing and
static downloads.

The Labeling Space has no persistent upper/lower boundary or splitter. Studio's
own surface owns its layout. Labeling only remembers its selected Workspace,
keyed by Board source plus Page file; this prevents same-named Pages in
different Boards from sharing a misleading view.

At `HOLD`, this is a hard boundary: the server re-derives HOLD from canonical
artifacts and forces that Page's Chat into read-only scoped mode, independently
of the browser payload. The permission selector is disabled, a held writable
client cannot be reused, and write/run tools are disallowed. The same server
guard rejects TUI start/reuse/input/local-resume commands and model-generated
Draw writes; keeping Studio's controls does not create alternate execution
doors. Chat may inspect and discuss; it cannot cross the gate.

## ✍️ Write and authority law

- First judgment, immutable lock, reveal, and final judgment are separate
  append-only events. A transcript is never a substitute.
- Only the identified human creates semantic gold or signs STOP/FREEZE.
- Models may prelabel, retrieve, diagnose, draft, and execute a frozen policy;
  agreement or consensus never promotes gold.
- Missing Keeper, event writer, sealed-test custodian, reconciler, runner, or
  auditor produces `HOLD` naming the missing owner and preserved frontier.
- For sealed custody, the active owner is the non-placeholder
  `test/sealed/status.json:custodian` in the current job. An imported
  `source_fence_attestation.source_custodian` is provenance only: it neither
  replaces that active owner nor independently triggers `HOLD` once the
  destination reservation has a valid custodian and rehashes.
- A backward route appends invalidation and creates new lineage; no closed
  checkpoint, handoff, scorecard, production run, or audit is rewritten.

The browser surface itself is read-only. It offers no “approve,” “freeze,”
“reveal,” “final,” or arbitrary run button. Those actions ship only when their
workflow writer and authority check exist end-to-end.

## ⚙️ Relationship to Runs

This workbench is the operational surface for one Labeling job. Newly allocated
Runs use the native `rlNN_<operation>_<target>` namespace (`rl` = Run of
Labeling); legacy `rNN_labeling-*` envelopes remain readable without aliases.
It may allocate
and resume the 25 independently closable operation kinds declared in
`ref-run.md`; P0-P5 and their Round/Test/Scan/Audit episodes group those Runs
without adding umbrella rows. `⚙️ Runs` presents the same Tickets and safe
Result envelopes under a `Labeling` filter, but it is read-only and creates no
parallel status, Result, or control. A Run row may deep-link here at the same
Run address. There is never a second run, approve, freeze, reveal, or final
button in the Runs surface.

## 🔁 Operate or implement

When opening or diagnosing a job or one of its Runs:

```text
resolve   the folded Page and its direct labeling/ lane
inspect   canonical receipts only; never protected item text
derive    P0-P5 and the first failed G0-G6 assertion
route     through /subjective-label to exactly one bounded action
stop      at human gate, HOLD, invalidation, step limit, or completion
```

When implementing or changing the plugin, keep these pieces aligned:

```text
roster       haipipe-plugin/ref/roster.md · labeling/ row first
registry     assets/js/10-drawer/60-plugin-labeling.js · one tab registration
surface      Board `live/labeling.py` or domain `engine/page_plugin.py` · read-only
routes       Board `cli/serve.py` or standalone Page server · `/_board/labeling`
skill        this file · storage/surface/writer/boundary law
tests        receipt parsing, HOLD across GUI/TUI/Draw, protected-text non-rendering,
             availability on ordinary and labeling Pages, dashboard exclusion,
             exact Studio Chat Page URL
```

Historical `labeling/field-tests/<id>/run/` may be read with a visible
“migration owed” warning; new jobs and every authoritative write go directly
under `<page>/labeling/`.

An older Board may still render a flat `<group>/<stem>.md` copy while the task
side lives at `pages/<stem>/labeling/`. The presenter and server-side Chat guard
must resolve that exact folded sidecar, show the bridge explicitly, and enforce
its receipts. This compatibility bridge is read-only: it does not make the flat
copy a second job root or authorize new writes outside the folded lane.

## 📂 Files

- `../../../ref/ref-assets.md` · full job tree and canonical/rendered split
- `../../../ref/ref-run.md` · 25 Labeling Run operations, resolver, count law,
  gates, and safe presentation boundary
- `../../../ref/ref-label-handoff.md` · the only Building → Scanning crossing
- `../../subjective-label-workflow/SKILL.md` · P0-P5, G0-G6, receipt chain
- `../../page-types/haipipe-page-for-labeling/SKILL.md` · Job Page contract
- the Board-engine paths in the implementation list above
