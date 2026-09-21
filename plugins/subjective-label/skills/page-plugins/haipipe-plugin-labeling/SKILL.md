---
name: haipipe-plugin-labeling
description: >-
  The 🏷 Labeling lane and Page-level surface beside any real Page, including a
  standalone Page Folder. An optional page-local labeling/ folder holds the
  canonical subjective-label job. Two levels: a Board-level view lists every
  labeling job on the Board (zoom out), and a click opens that Page's surface
  with five Spaces (Data, Labeling, Quality, Run, Delivery) and one write door,
  POST /_board/labeling/act, for exactly ten engine-checked actions (zoom in).
  Studio Chat opens separately. Use when designing, opening, diagnosing, or
  implementing the labeling plugin, tab, or folder, or /haipipe-plugin-labeling.
metadata:
  version: "0.18.0"
  last_updated: "2026-09-20"
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
    ├── cache/                      embeddings/ · reveal/ · derived, never authority
    └── REPORT.md · .state.json  rendered/cache only; receipts win

🏷 Board level · GET /_board/labeling-board?path=<board.md>
all jobs   one card per Page that owns labeling/ · jobs that wait for you first
           click a card → the Page level below · "← All labeling jobs" comes back

🏷 Page level · five Spaces, each with its views
Data       Contract · Schema · Embedding
Labeling   Label · Rounds · Guideline
Quality    Test · Evaluation · Audit
Run        Runs · Phases · Workflow map
Delivery   Handoff · Final labels

header     Next: <one line> · Open Studio Chat (separate tab)
write      POST /_board/labeling/act · confirm_meaning · release_round · open_item · first · final
           · build_embedding (catalog models only, runs in the background) · embedding_status (read)
           · embedding_item (read: one item's group and nearest items, never text)
```

## 🧩 The four-part plugin contract

| part | contract |
|---|---|
| STORAGE | `<page>/labeling/`, exactly the job layout in `subjective-label/ref/ref-assets.md`; MIXED because canonical PRIMARY receipts and rendered views coexist |
| SURFACE | one optional `🏷 Labeling` right-pane tab on a real Page; it fills the plugin pane with five Spaces and their views. The current adapter keeps P0-P5 as compatibility capability tags in `Run → Phases` and the one-line `Next:` header; they are not Workflow nodes, Run owners, or Route authority. Studio Chat opens in its own tab |
| WRITER | `subjective-label-workflow` defines the Run Spec graph and Routes; the Building/Scanning guides document operation order. Their Keeper, human event writer, runner, reconciler, and auditor own named artifacts. In the browser the only writer is `POST /_board/labeling/act`, which calls `engine/job.py` and `engine/calibration.py` |
| BOUNDARY | Board discovery never enters `labeling/`; overview views never render item text, sealed ids, or private judgments in the page HTML (`Labeling → Rounds` lists the drawn item ids with their map group, never an item's text); an item waiting in a round batch shows its text only in its round's table in `Labeling → Rounds`, and only once the chat has shown it (its `show` event); `Data → Embedding` fetches the text of other development items only on request (a group's typical items, or a picked dot), and each fetch is appended to `labeling/exposure/group_examples.jsonl`; an observed file is never treated as a validated gate |

## 🔭 Two levels: Board and Page

| level | where it opens | what it shows | writes |
|---|---|---|---|
| Board | the Board index, and the `S-Label-Dash` control Page | one card per Page whose `labeling/` has a `config.yaml`: target, question, data, step badge, progress, next step; Pages with no job listed below | none |
| Page | any real job Page | the five Spaces; label definitions in `Labeling → Label`, round tables in `Labeling → Rounds` | only `POST /_board/labeling/act` |

A card links to `/_board/labeling?path=…&file=…&page=…`, so zooming in opens
the Page level in the same pane. The Page header's `← All labeling jobs` link
goes back to `/_board/labeling-board?path=<board.md>`. Cards sort by what waits
for the human: labeling in progress, then meaning confirmation, then a round to
start, then judged, repair, and read-only (HOLD) jobs. The Board level reads
each job through the same view model as the Page level (`_view_model`,
`_next_step`), so the two can never disagree, and it never stores a label.
Labels stay per Page because each target has its own human gate.

The registry offers the Board-level entry (`id: labeling-board`) only on the
Board index or on `S-Label-Dash`, and the Page-level entry (`id: labeling`)
only on job Pages, so one 🏷 entry is offered at a time. A Board whose job
Pages are not named `S-Label-*` is recognised after `POST
/_board/labeling-board` counts its `labeling/` lanes.

The specialized `page-type: labeling` Job Page owns one corpus snapshot × one
target construct × one identified human semantic authority and uses the
labeling Page grammar. That Page type is not a
capability switch: a paper section, algorithm Page, or other Folder may open
the same plugin before a job exists and route P0 creation through Chat. The
control Page `S-Label-Dash` owns no job, so it gets no Page-level lane; it
opens the Board-level view instead.

## 🖼 Surface law

The surface uses one location word: **Space**. In this plugin, "Space" and
"Workspace" are the same concept. There are five Spaces, in this order:
`Data`, `Labeling`, `Quality`, `Run`, `Delivery`. `Guideline` is a view inside
`Labeling`, not a Space of its own. The older Human tab is gone.
`Run → Workflow map` shows the SOP (the steps a job walks, who does each, and
where this job is) above the Workflow map (every Run type × Space), both
projected from `ref/ref-space-mapping.md`. The current adapter shows P0-P5 in
`Run → Phases` and the `Next:` header as compatibility capability tags. This
projection and the legacy Space choice do not own Runs or authorize allocation,
closure, or Workflow Routes.

The roster table (views, first question, canonical sources), the rule for
which Space opens first, and the item-text rule live in
`../../../ref/ref-space-mapping.md`. The current adapter uses the legacy tag to
choose a presentation Space (P0 opens `Data`, P1 opens `Labeling`); that is
not the Workflow Route. A `?space=&view=` URL wins, then the browser's saved
choice.

These Spaces are projections over the one canonical `labeling/` tree, not
separate storage folders. Data may show source-preserving imported label
counts, but no overview view renders protected item text, sealed identifiers,
or private judgments.

`GET /_board/labeling` re-reads disk on every open. For a v2 lane with a
`gates/p0-contract/receipt.json` or `gates/g0/receipt.json`, it delegates P0/G0
truth to the canonical status evaluator, `engine/job.py status()`. That call
never raises on a bad file: it reports each defect in `integrity_errors`, and it
reports `hold` and `hold_reason` from `authority_hold(config)`, the one HOLD
rule every host uses. If the surface still cannot derive status, it fails
closed at P0 with an integrity error. A historical lane with no canonical
receipt may say "observed", but it must not promote that observation to a
pass. `REPORT.md`, `.state.json`, and the Page's prose are useful views, never
the source of the Run Spec frontier. The existing status/Space adapter still
projects compatibility state from gate receipts; it is not the host Run graph
and cannot by itself authorize a later Run.

On a Board host, Labeling fills its own plugin pane. The header link
`Open Studio Chat` opens the exact generated-Page `?pane=chat` document that
Studio owns in a separate browser tab, including its composer, sessions, quick
actions, settings, GUI/TUI handoff, and optional Draw controls. Labeling never
embeds that document and never implements a second Chat. The Board-source
`board.md` is only the source resolver and must never receive `?pane=chat`;
the current generated `<page>.html` URL is carried separately and validated
server-side. Chat may prepare or dispatch work, but a semantic decision becomes
real only when the owning workflow writer lands its canonical event under
`labeling/`.

On a standalone host, `engine/page_plugin.py` is still the older read-only
presenter. It keeps its own older tab names, has no write door, and has not
moved to the five Spaces yet. It names the current Codex task as transport and
offers a copyable next-action prompt derived from canonical status. The Page
host keeps `labeling/` private from Source editing and static downloads.

The Labeling surface has no persistent upper/lower boundary or splitter.
Studio's own surface owns its layout. Labeling remembers the selected Space and
view in the browser, keyed by Board source plus Page file, so same-named Pages
in different Boards do not share a view. An unknown saved Space falls back to
the next-step Space; an unknown view falls back to that Space's first view.

At `HOLD`, this is a hard boundary: the server re-derives HOLD from canonical
artifacts and forces that Page's Chat into read-only scoped mode, independently
of the browser payload. The permission selector is disabled, a held writable
client cannot be reused, and write/run tools are disallowed. The same server
guard rejects TUI start/reuse/input/local-resume commands and model-generated
Draw writes; keeping Studio's controls does not create alternate execution
doors. `Labeling → Rounds` shows a read-only notice, and the engine refuses every
write-door action. Chat may inspect and discuss; it cannot cross the gate.

## ✍️ Write and authority law

- First judgment, immutable lock, reveal, and final judgment are separate
  append-only events. A transcript is never a substitute.
- The workflow assigns semantic authority to one human. The current CLI and
  local Board require a matching caller-supplied id and explicit attestation,
  but do not authenticate the caller; deployments needing identity assurance
  must add an authenticated principal before treating these receipts as proof
  of actor identity.
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

The browser is not purely read-only anymore. It has exactly one write door,
`POST /_board/labeling/act`, with exactly ten actions. Each action exists
because its writer and its authority check exist end to end:

| action | where it is pressed | engine call |
|---|---|---|
| `confirm_meaning` | `Data → Contract` · `Confirm meaning` | `job.confirm_meaning(..., attest_as_human=True, channel="board labeling screen")` |
| `release_round` | `Labeling → Rounds` · `Start round 1` | `calibration.release_round` |
| `open_item` | no page button since 260919; the chat calls the engine directly | `calibration.open_item` |
| `first` | no page button since 260919; the chat calls the engine directly | `calibration.record_first` |
| `final` | no page button since 260919; the chat calls the engine directly | `calibration.record_final` |
| `build_embedding` | `Data → Embedding` · `Run embedding` with model, text, instruction, groups, map, seed | `embedding_build.start_background_build` (catalog ids and checked settings only; one run per job at a time; records the human as `started_by`; a build never starts without this click or a named person) |
| `embedding_status` | `Data → Embedding`, polled while a build runs (read only) | `embedding_build.build_status` |
| `embedding_item` | `Data → Embedding` · click a dot on the map (read only) | `embedding_build.neighbors` (development items only, no text) |
| `group_examples` | `Data → Embedding` · `Show typical items` / `Show 3 more` on a group | `embedding_build.group_examples` (items nearest the group centre, with text; items waiting in a round left out; appends to `exposure/group_examples.jsonl`) |
| `embedding_item_text` | `Data → Embedding` · `Show its text` on a picked dot | `embedding_build.item_text` (refuses an item waiting in a round; appends to `exposure/group_examples.jsonl`) |

What each call writes, and the event order, is owned by
`../../label-building-workflow/SKILL.md` (§P0 Contract and §P1 Round).

The door refuses before any engine call when:

1. the `Origin` header names another host (HTTP 403, same-origin only);
2. the Page has no labeling lane (404), or the `page` field does not name the
   matching generated Page URL (400);
3. the request does not carry `attest: true` (400);
4. the lane has no canonical job, meaning no `gates/p0-contract/receipt.json`
   (409).

The request also carries the configured human id and a session id. The engine
checks that supplied id against the job configuration on every call; this is
not identity authentication. It also checks that the job is not on HOLD, G0
has passed (for the four P1 actions), the event order holds, and sealed
custody holds (a sealed item is never drawn, shown, or revealed). A refusal
returns HTTP 409 with the engine's reason; a malformed value returns HTTP 400.

There is still no approve, freeze, reveal-all, final-for-all, or run button.
A new action ships only when its writer and authority check exist end to end.

## ⚙️ Relationship to Runs

One Labeling job allocates Level-4 Runs for the bounded commissions in its
Workflow Run Spec list. Existing Tickets may retain a P0-P5 compatibility
tag. A Run is named `rlNN_<operation>_<target>` (`rl` = Run of Labeling). Its Ticket is
`labeling/runs/<run>.yaml` and its Result folder is `labeling/results/<run>/`
(`runtime.yaml`, then `result.yaml` when complete). Legacy `rNN_labeling-*`
envelopes remain readable without aliases. The 25 operation kinds and the
count law live in `../../../ref/ref-run.md`. Round, Test, Scan, and Audit are
episodes that group Runs; they add no row.

The browser allocates a Run only as a side effect of an engine call.
`release_round` writes a complete `rlNN_round-prepare_round-01`. The first
`open_item` writes a running `rlNN_human-calibration_round-01`, and the last
`final` completes it. `engine/job.py create` (not the browser) writes
`rl01_corpus-contract_job-v1`.

`Run → Runs` lists one row per Ticket with its runtime status and outcome.
`haipipe-plugin-runs` presents the same envelopes read-only under a `Labeling`
filter and creates no parallel status, Result, or control. A Run row may
deep-link here at the same Run address. There is never an approve, freeze,
reveal, final, or run button in Run Space.

## 🔁 Operate or implement

When opening or diagnosing a job or one of its Runs:

```text
resolve   the folded Page and its direct labeling/ lane
inspect   canonical receipts only; batch item text only in Labeling → Rounds, once shown
derive    compatibility tags and failed gate evidence for display; identify
          an eligible Run Spec from the shared Workflow graph and Run receipts
route     through /subjective-label to exactly one bounded action under that Spec
stop      at human gate, HOLD, invalidation, step limit, or completion
```

When implementing or changing the plugin, keep these pieces aligned:

```text
roster       haipipe-plugin/ref/roster.md · labeling/ row first
registry     assets/js/10-drawer/60-plugin-labeling.js · one tab registration
surface      Board `live/labeling.py` · five Spaces, Label definitions, Rounds tables, `LabelingMixin`
             standalone `engine/page_plugin.py` · older read-only presenter
routes       Board `cli/serve.py` · GET `/_board/labeling` (page)
             POST `/_board/labeling` (tab URL) · POST `/_board/labeling/act` (write door)
engine       `engine/job.py` · status, confirm_meaning
             `engine/embedding_build.py` · CATALOG, build (P0 embedding-build Run), builds,
             build_status, start_background_build
             `engine/calibration.py` · release_round, open_item, record_first,
             record_final, verify_events
skill        this file · storage/surface/writer/boundary law
tests        Board `tests/test_labeling.py` · LabelingSurfaceTest,
             LabelingWriteDoorTest, LabelingRegistrationTest
             `engine/test_calibration.py` · fence, confirm, round 1, chain, reveal
             `engine/test_embedding_build.py` · sealed left out, no-op rebuild, failed Run
             Board LabelingEmbeddingViewTest · recipe, example, map, groups
```

Historical `labeling/field-tests/<id>/run/` may be read with a visible
"migration owed" warning; new jobs and every authoritative write go directly
under `<page>/labeling/`. The write door refuses such a lane because it has no
canonical `gates/p0-contract/receipt.json` at the lane root.

An older Board may still render a flat `<group>/<stem>.md` copy while the task
side lives at `pages/<stem>/labeling/`. The presenter, the server-side Chat
guard, and the write door must resolve that exact folded sidecar, show the
bridge explicitly, and enforce its receipts. The flat copy never becomes a
second job root, and no write lands outside the folded lane.

## 📂 Files

- `../../../ref/ref-assets.md` · full job tree and canonical/rendered split
- `../../../ref/ref-run.md` · 25 Labeling Run operations, resolver, count law,
  gates, and safe presentation boundary
- `../../../ref/ref-space-mapping.md` · the five-Space roster, the opening
  Space, the item-text rule, and the write door in one page
- `../../../ref/ref-config.md` · meaning text, round 1, and reveal settings the
  surface reads
- `../../../ref/ref-label-handoff.md` · the only Building → Scanning crossing
- `../../label-building-workflow/SKILL.md` · P0 fence/create/confirm and P1
  CARD, PREPARE, JUDGE order, including the events file
- `../../subjective-label-workflow/SKILL.md` · P0-P5, G0-G6, receipt chain
- `../../page-types/haipipe-page-for-labeling/SKILL.md` · Job Page contract
- the Board-engine paths in the implementation list above
