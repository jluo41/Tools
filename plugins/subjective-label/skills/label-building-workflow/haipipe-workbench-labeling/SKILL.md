---
name: haipipe-workbench-labeling
description: >-
  The 🏷 Labeling lane and Page-level surface in a canonical Page folder. An
  optional page-local labeling/ folder holds the
  canonical subjective-label job. An optional Board-level view lists every
  labeling job on the Board (zoom out); a direct Page-folder route also opens the Page
  with four Spaces (Data, Labeling, Quality, Delivery), each with its content on
  the left and a Runs panel on the right, and one write door,
  POST /_board/labeling/act, for exactly eleven engine-checked actions (zoom in).
  Use when designing, opening, diagnosing, or
  implementing the labeling Workbench, tab, or folder, or /haipipe-workbench-labeling.
metadata:
  version: "0.23.16"
  last_updated: "2026-09-29"
---

# /haipipe-workbench-labeling · one job, one folder, one operated surface

**LOAD `haipipe-workbench` and `subjective-label` FIRST.** This is a Workbench lane:
it owns the `labeling/` roster row and its own surface. The family workflows
own semantic order and writes; this skill owns how that job lives beside and
appears beside one Page.

```text
one page folder
├── <stem>.md                    what the Page says
├── labeling/                    the job itself · canonical
│   ├── config.yaml · corpus/ · policy/ · rounds/ · gold/ · handoff/
│   ├── test/ · evaluation/ · production/ · audit/
│   ├── gates/                      P0 contract + G0 receipts
│   ├── preparation-owner.yaml       source attachment, even before a job
│   ├── preparation-ref.yaml         accepted source package, before Contract
│   ├── cache/                      embeddings/ · reveal/ · derived, never authority
│   └── REPORT.md · .state.json  rendered/cache only; receipts win
├── runs/                        full `run-labeling-...` Tickets, beside labeling/
└── results/                     one folder per Ticket, same name

🏷 Board level · GET /_board/labeling-board?path=<board.md>
all jobs   one card per Page that owns labeling/ · jobs that wait for you first
           click a card → the Page level below · "← All labeling jobs" comes back
empty      S-Label-* Pages without a job appear under "Pages before Contract"
           and link to their Page-level Preparation View, without allocating a Run;
           flat Board sources first ask for a canonical Page folder

🏷 Page level · the title, the Space tabs, then one Space
Data       Preparation · Contract · Embedding
Labeling   Definition · Rounds · Guideline
Quality    Test · Evaluation · Audit
Delivery   Handoff · Scan · Final labels
Runs       the right side of every Space, at every width: the current view's Run types
           in step order · the selected Run (its Run Type's declared Skills, Resume/Rerun, ▸ Prompt +
           Copy, Running process, Results); ▸/◂ folds it to a strip
drawers    ?drawer=workflow (Phases · SOP · Workflow map) · ?drawer=allruns; no button
actions    POST /_board/labeling/act · confirm_meaning · release_round · open_item · first · final
           · build_embedding (catalog models only, runs in the background)
           · embedding_status, embedding_item, group_examples, embedding_item_text (reads)
           · item_page (Data → Preparation item table, reads)
```

## 🖥 Hosting · its own host, or one tab on a Board

Resolve `TOOLS_ROOT` to the checkout containing `plugins/` (`.` from that
checkout, or a consuming workspace's `Tools` link) and `PYTHON_BIN` to that
workspace's Python 3.10+ interpreter before using these host commands. The
system `python3` may be too old; check `"$PYTHON_BIN" --version` first.

```text
own host    "$PYTHON_BIN" "$TOOLS_ROOT/plugins/subjective-label/servers/_host/serve.py" --root <folder>
            the shared haipipe host with --only labeling: own port, DOMAIN and auth
            file; terminal, chat and every Board write route answer 404
Board tab   "$PYTHON_BIN" "$TOOLS_ROOT/plugins/haipipe-toolkit/servers/_host/serve.py" --root <folder>
            🏷 is one tab among the others; same routes, same write door
addresses   <DOMAIN>/w/<board-slug>                    every labeling job on the Board
            <DOMAIN>/w/<board-slug>/<page-id>/labeling one job, four Spaces
            <DOMAIN>/workbench/labeling?file=<Page>/<Page>.md
                                                        a canonical Page folder without a Board
```

The separate host isolates the service and its settings. Its direct Page route
resolves an existing `<Page>/<Page>.md` relative to `--root`, without `board.md`
or a generated Page URL. It rejects flat sources, symlinks, traversal, and
requests on the mixed Board host. The direct Page has the same Spaces, Views,
Runs panel, and Labeling action door; it has no Board back link. Create a Page folder before attaching Corpus Preparation or creating a
new Contract.

`<DOMAIN>` is whichever origin the server printed at startup (loopback, the
Tailscale IP, or the configured `--public-url`); the link body is the same for
all of them. The short address redirects to the long route and the server
fills in `path=<board>/board.md`, `file=<page-rel>` and `page=<generated
html>` itself. The workbench code is `servers/workbench-labeling/labeling.py`,
a mixin of the shared host; it reads the Board's page list through one
adapter (`_board_pages`) and nothing else of the Board grammar, and the
`engine/` it calls imports nothing from haipipe-toolkit. See
`plugins/subjective-label/servers/README.md`.

## 🧩 The four-part Workbench contract

| part | contract |
|---|---|
| STORAGE | `<page>/labeling/`, exactly the job layout in `subjective-label/ref/ref-assets.md`; MIXED because canonical PRIMARY receipts and rendered views coexist |
| SURFACE | a Board-backed Page offers an optional `🏷 Labeling` right-pane tab; the direct Page-folder route opens the same four Spaces, each with Views on the left and a Runs panel on the right. The current adapter keeps P0-P5 as compatibility capability tags in the Workflow drawer's Phases card (`?drawer=workflow`); they are not Workflow nodes, Run owners, or Route authority |
| WRITER | `subjective-label-workflow` defines the Run Spec graph and Routes; the Building/Scanning guides document operation order. Their Keeper, human event writer, runner, reconciler, and auditor own named artifacts. In the browser the only writer is `POST /_board/labeling/act`, which calls `engine/job.py` and `engine/calibration.py` |
| BOUNDARY | Board discovery never enters `labeling/`; overview views never render item text, sealed ids, or private judgments in the page HTML (`Labeling → Rounds` lists the drawn item ids with their map group); an item waiting in a round batch shows its text only in its round's table in `Labeling → Rounds`, and only once the chat has shown it (its `show` event); `Data → Embedding` fetches the text of other development items only on request (a group's typical items, or a picked dot), and each fetch is appended to `labeling/exposure/group_examples.jsonl`; an observed file is never treated as a validated gate |

## 🔭 Two levels: Board and Page

| level | where it opens | what it shows | writes |
|---|---|---|---|
| Board | the Board index, and the `S-Label-Dash` control Page | one card per Page with a linked preparation package or a `labeling/config.yaml` job: target, question, data, step badge, progress, next step; Pages with neither listed below | none |
| Page | any real job Page | the four Spaces and their Runs panels; label definitions and Confirm meaning in `Labeling → Definition`, round tables in `Labeling → Rounds` | only `POST /_board/labeling/act` |

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
"Workspace" are the same concept. There are four Spaces, in this order:
`Data`, `Labeling`, `Quality`, `Delivery`. `Guideline` is a view inside
`Labeling`, not a Space of its own. A view exists only because Runs live in it
(JL 260928): Schema merged into Contract, Discussion and Label into Definition,
and Delivery gained Scan, so each of the 26 job-local Run types sits in exactly
one view. Data → Preparation adds five upstream source-owned Run Types.
Once a job exists, Data → Preparation shows two cards. `Raw corpus` reads
`labeling/corpus/source.yaml` and shows the raw folder: each file with size,
rows, columns and items, what one row is, which raw column became which item
field, and the other column names (never their values, which hold other
people's labels). `Items to label` gives what one item is, the counts, word
counts, and an item table that loads 20 items at a time on `Show items`
(action `item_page`, logged as an exposure). Data → Contract keeps the counts.
Preparation is a Data view over source-owned Corpus Runs; it can appear before
`labeling/config.yaml` exists. `labeling/preparation-owner.yaml` attaches its
source early so each completed Run appears in the panel. Its accepted package
is later linked through `labeling/preparation-ref.yaml`, while private candidates and the protected
group frame remain with the source owner. There is no Run Space and no page bar
(v3, 260927, as the Page workbench): the page is its title, the Space tabs,
then one Space. Each Space is its content
on the left and its Runs panel on the right at every width; the panel stays in
view while the page scrolls. Two drawers have no button and open only from the
URL: `?drawer=workflow` shows the Phases card (P0-P5 as compatibility capability
tags), the SOP and the Workflow map, both projected from
`ref/ref-space-mapping.md`; `?drawer=allruns` lists every Ticket; Esc closes
them. This projection does not own Runs or authorize allocation, closure, or
Workflow Routes.

The page carries content and the controls that act on it, never hints, crumbs,
status chips or explanation sentences (JL 260927: "as concise as possible").
A Runs panel lists only the current view's Run types, from the Workflow map's
`view` column, in its `step` order, each with this job's count. Types the map marks `not built yet`
stay in the map only; a view with no type says `No runs yet.` Below the types
sits the selected Run: its full on-disk name (`run-labeling-human-calibration-0929-round-01`),
its state, a `Run Type skills` line naming the declared set (from
`## Run Type skills` in `ref/ref-space-mapping.md`), `Resume` (an open Run,
same Ticket) or `Rerun` (a closed one,
new full `run-...` name), a folded `▸ Prompt` whose `Copy` works while folded, Running process
and Results. `+ New Run` shows an open prompt for the selected type. Every button
only copies a prompt; none starts a Run. `▸/◂` folds the panel to a thin strip,
remembered per Space in this browser.

The content and its Runs pick each other (v4, as the Page workbench's Card ↔
Runs): showing a build in `Data → Embedding` selects that build's
`embedding-build` Run, and picking the Run shows the build; opening a round in
`Labeling → Rounds` selects its Run, and picking a round's Run opens and outlines
that round. The link is the Run's `target` (the build version, `round-01`). A
rerun on the same target keeps the older Run's plain name and counts up
(`run-labeling-embedding-build-0929-minilm`, then `run-labeling-embedding-build-0929-minilm-2`).
Older short-named Tickets remain readable. An empty slot stays blank: no `—`,
no `not implemented · HOLD` line.

Treat the map as the Run Type catalogue, not the job's Run inventory. Today it
shows the friendly operation name/type, where its action or result belongs,
the output path, and a per-type count. The Runs panels and `?drawer=allruns` are the actual inventory:
one row per allocated Ticket with its runtime status and outcome. Do not infer
a Run or status from the catalogue row or count. Each Run card names its
Run Type's declared Skills, which do not prove what a historical Run loaded;
the matrix does not render bounded target,
actor/prerequisites, or a link to a matching Ticket.

The supported first-use path for structured transcripts is: use
`/subjective-label-preparation` to attach the source owner to a Page, normalize the source, choose the unit,
materialize and check it, reserve whole source groups, then link the accepted
package to a real Page. Data → Preparation shows these source-owned Runs before
the job exists, and offers a new Run prompt only for the next unfinished step
while an owner is attached and the Page has no Contract. Copy the Data → Contract request and send it in your agent conversation
(Claude Code or Codex); name the target, semantic human, and
sealed-test custodian (the human may also be the custodian). Discuss and settle
the label meanings in Labeling → Definition, close that discussion, then confirm
meaning as the configured human. Optionally build an embedding,
release round 1, and label that round using its copied prompt in the same
conversation.
The current engine stops after round 1 is fully judged because
`guideline-learn`, `round-measure`, and `round-close` have no workers.
Round 2+, handoff, test evaluation, production scanning, audit, and D*
materialization are not operable. Keep the SOP limited to the supported path
and label these later Run Types `not built yet`.

The roster table (views, first question, canonical sources), the rule for
which Space opens first, and the item-text rule live in
`../../label-building/ref/ref-space-mapping.md`. The current adapter uses the legacy tag to
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

On a Board host, Labeling fills its own Workbench pane. It has no chat of its
own and no link to one (Studio Chat was removed 260930): every copied request
goes into your agent conversation. The Board-source `board.md` is only the
source resolver; the current generated `<page>.html` URL is carried separately
and validated server-side. A conversation may prepare or dispatch work, but a
semantic decision becomes
real only when the owning workflow writer lands its canonical event under
`labeling/`.

The dedicated Labeling host's `/workbench/labeling?file=...` route is the same
four-Space presenter, including its engine-checked action door, for a Page
folder without a Board. It uses the current agent conversation for copied Run
requests. The older `engine/page_plugin.py` remains a separate read-only
presenter with older tab names and a copyable status prompt; it is not this
Workbench route. The host keeps `labeling/` private from static downloads.

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
  destination reservation has a valid custodian and its protected manifest is
  present with the declared count.
- A backward route appends invalidation and creates new lineage; no closed
  checkpoint, handoff, scorecard, production run, or audit is rewritten.

The browser is not purely read-only anymore. It has exactly one write door,
`POST /_board/labeling/act`, with exactly eleven actions. Each action exists
because its writer and its authority check exist end to end:

| action | where it is pressed | engine call |
|---|---|---|
| `confirm_meaning` | `Labeling → Definition` · `Confirm meaning` | `job.confirm_meaning(..., attest_as_human=True, channel="board labeling screen")` |
| `release_round` | `Labeling → Rounds` · `Start round 1` | `calibration.release_round` |
| `open_item` | no page button since 260919; the chat calls the engine directly | `calibration.open_item` |
| `first` | no page button since 260919; the chat calls the engine directly | `calibration.record_first` |
| `final` | no page button since 260919; the chat calls the engine directly | `calibration.record_final` |
| `build_embedding` | `Data → Embedding` · `Run embedding` with model, text, instruction, groups, map, seed | `embedding_build.start_background_build` (catalog ids and checked settings only; one run per job at a time; records the human as `started_by`; a build never starts without this click or a named person) |
| `embedding_status` | `Data → Embedding`, polled while a build runs (read only) | `embedding_build.build_status` |
| `embedding_item` | `Data → Embedding` · click a dot on the map (read only) | `embedding_build.neighbors` (development items only, no text) |
| `group_examples` | `Data → Embedding` · `Show typical items` / `Show 3 more` on a group | `embedding_build.group_examples` (items nearest the group centre, with text; items waiting in a round left out; appends to `exposure/group_examples.jsonl`) |
| `embedding_item_text` | `Data → Embedding` · `Show its text` on a picked dot | `embedding_build.item_text` (refuses an item waiting in a round; appends to `exposure/group_examples.jsonl`) |
| `item_page` | `Data → Preparation` · `Show items` / `Show 20 more` in Items to label | `corpus_view.item_page` (20 development items at a time with context and text; held-back items never read; an item waiting in a round keeps its text for Rounds; appends to `exposure/group_examples.jsonl`; refuses on HOLD) |

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

There is still no approve, freeze, reveal-all, or final-for-all button, and no
generic run button: `Run embedding` and `Start round 1` are the only buttons that
start work, each through its own checked door action.
A new action ships only when its writer and authority check exist end to end.

Prompts live only in the Runs panels (v4): `+ New Run` and `Resume` of
`definition-discussion` (Labeling → Definition), plus `+ New Run` before the
first item of an open round and `Resume` afterward for `human-calibration`.
`+ New Run` opens a prompt with a separate `Copy` button; `Resume` copies an
updated prompt. Neither control writes a Run. The Definition discussion prompt
appears only with a valid Contract, no HOLD, no released round, and no other
open discussion. An open discussion has `Resume` on its own Ticket. Historical
Tickets for Run Types without a worker are review-only. Labeling → Definition shows the
definitions with no copy button, each discussion's labels before and after (a
changed wording in green, `kept` otherwise) with its open questions, and then
Confirm meaning; picking a discussion Run in the panel shows that one. The round prompt currently includes the job folder, question
and label names, round progress, pending first answers, the next items, and
the JUDGE-by-chat instructions. It does not start a Run or write a judgment;
the chat must call the permitted calibration actions. Offer a copy control
only when there is a concrete next interaction, such as continuing an open
round. A richer per-Run prompt should also bind the Board/Folder/Page, target,
Run Type, its declared Skills, prerequisite state, matching Ticket/status when
one exists, and the next allowed action.
An older discussion Ticket left running after round release remains visible as
history with a blocked explanation; it has no Resume request. The current
definitions may still be reviewed. G0 can be restored after release only from
an intact human confirmation that predates the round; otherwise the page stays
historical and a new job is needed for new labels. While a discussion is open,
the G0 confirmation button is hidden. If only `gates/g0/receipt.json` is missing
and the earlier meaning receipt is still valid, Labeling → Definition offers
`Restore G0 receipt`; this restores the existing semantic attestation and then
returns to the existing round. If no valid earlier attestation predates a
released round, Definition shows a read-only warning instead of a button.
Its historical Labeling Run cards show `Record` without executable Copy or
Resume, and a running Ticket is labeled `blocked history`.
If a Contract lists labels without meanings, Labeling → Definition shows
`Define label meanings first`, offers Definition discussion, and hides Confirm
meaning until all labels have nonblank wording.
The current round prompt now includes the Board, Page, folder, round target,
Run Type, declared Skills, G0 and released-Card prerequisites, and matching
Ticket id/status when there is one. After Corpus Preparation links an accepted package, Data → Contract
offers a contextual, clipboard-only setup request in the Runs panel. Paste it
into your agent conversation; copying does not create the Contract Run.

## ⚙️ Relationship to Runs

One Labeling job allocates Level-4 Runs for the bounded commissions in its
Workflow Run Spec list. Existing Tickets may retain a P0-P5 compatibility
tag. A new Run is named `run-labeling-<operation>-<MMDD>-<target>` on disk and
in the panel. Its Ticket is
`<Page>/runs/<run>.yaml` and its Result folder is `<Page>/results/<run>/`
(`runtime.yaml`, then `result.yaml` when complete), beside `labeling/`, not
inside it. Receipt paths are relative to the Page, so a round input reads
`labeling/rounds/round_01/manifest.yaml`. Legacy `rNN_labeling-*`
envelopes remain readable without aliases. The 26 operation kinds and the
count law live in `../../label-building/ref/ref-run.md`. Round, Test, Scan, and Audit are
episodes that group Runs; they add no row.

The browser allocates a Run only as a side effect of an engine call.
`release_round` writes a complete `run-labeling-round-prepare-<MMDD>-round-01`. `+ New Run` for
`human-calibration` is available only when a round has an item left, has no
calibration Ticket yet, and is not on HOLD. A stale or completed
human-calibration Run has no `Resume`, `Rerun`, or replacement `+ New Run`
request. If all item final events exist but that Run's Result did not close,
`Resume` instead copies a request to verify events and finalize the same
Ticket without repeating judgments. The Page header and Board card identify
that incomplete Result as the next action. An ongoing round's copied prompt
calls `open_item` for the next unfinished item even if it was shown already;
after an interrupted first or lock, the writer recovers the reveal without
repeating the person's first answer. The first
`open_item` writes a running `run-labeling-human-calibration-<MMDD>-round-01`, and the last
`final` completes it. `engine/job.py create` (not the browser) writes
`run-labeling-corpus-contract-<MMDD>-job-v1`.

`?drawer=allruns` lists one row per Ticket with its runtime status and outcome; each Space's Runs panel shows the same Tickets by view and type.
`haipipe-workbench-page/ref/run-space.md` presents the same envelopes read-only under a `Labeling`
filter and creates no parallel status, Result, or control. A Run row may
deep-link here at the same Run address. There is never an approve, freeze,
reveal, final, or run button in a Runs panel; Resume, Rerun and Copy only copy a prompt.

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
roster       haipipe-workbench/ref/roster.md · labeling/ row first
registry     plugins/subjective-label/servers/workbench-labeling/assets/js/10-drawer/60-workbench-labeling.js · one tab registration
surface      Board `plugins/subjective-label/servers/workbench-labeling/labeling.py` · four Spaces + Runs panels, Label definitions, Rounds tables, `LabelingMixin`
             standalone `engine/page_plugin.py` · older read-only presenter
routes       Board `servers/_host/serve.py` · GET `/_board/labeling` (page)
             POST `/_board/labeling` (tab URL) · POST `/_board/labeling/act` (write door)
engine       `engine/job.py` · status, confirm_meaning, revise_meanings
             `engine/definition_discussion.py` · start, say, decide, close, state
             `engine/embedding_build.py` · CATALOG, build (P0 embedding-build Run), builds,
             build_status, start_background_build
             `engine/calibration.py` · release_round, open_item, record_first,
             record_final, verify_events
skill        this file · storage/surface/writer/boundary law
tests        Board `tests/test_labeling.py` · LabelingSurfaceTest,
             LabelingWriteDoorTest, LabelingRegistrationTest
             `engine/test_calibration.py` · fence, confirm, round 1, chain, reveal
             `engine/test_definition_discussion.py` · revision, re-confirm, judged refusal
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

- `../../label-building/ref/ref-assets.md` · full job tree and canonical/rendered split
- `../../label-building/ref/ref-run.md` · 26 Labeling Run operations, resolver, count law,
  gates, and safe presentation boundary
- `../../label-building/ref/ref-space-mapping.md` · the four-Space roster, the opening
  Space, the item-text rule, and the write door in one page
- `../../label-building/ref/ref-config.md` · meaning text, round 1, and reveal settings the
  surface reads
- `../../label-building/ref/ref-label-handoff.md` · the only Building → Scanning crossing
- `../../label-building-workflow/SKILL.md` · P0 fence/create/discuss/confirm and P1
  CARD, PREPARE, JUDGE order, including the events file
- `../../subjective-label-workflow/SKILL.md` · P0-P5, G0-G6, receipt chain
- the Board-engine paths in the implementation list above
