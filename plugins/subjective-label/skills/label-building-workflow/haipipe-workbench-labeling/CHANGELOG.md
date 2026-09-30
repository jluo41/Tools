# haipipe-workbench-labeling · CHANGELOG

## 0.23.15 · 2026-09-29

- Bind the human-calibration copy request to the Board, Page, folder, Run Type,
  round target, declared Skills, G0/Card prerequisites, and actual Ticket state.

## 0.23.14 · 2026-09-29

- An unfilled label schema now leads to Definition discussion; the Confirm
  meaning button and G0 writer refuse blank class meanings.

## 0.23.13 · 2026-09-29

- Give a missing G0 receipt its own Definition repair path when an intact
  human meaning confirmation already predates the released round. Show the
  restore action in the Page, Board status, and Rounds guidance; route
  irreparable historical jobs to the read-only Definition warning. Their
  Labeling Run cards are records rather than executable prompts.

## 0.23.12 · 2026-09-29

- Hide G0 confirmation while a definition discussion is open, and show a
  historical warning instead of a confirmation button when a released round
  has no valid pre-release attestation. Historical unbuilt or blocked Run
  cards expose a read-only Record, not a copied execution Prompt.

## 0.23.11 · 2026-09-29

- Explain a legacy discussion left open after round release as blocked history
  instead of telling the reader to finish a Run that can no longer proceed.

## 0.23.10 · 2026-09-29

- Offer only the next unfinished Corpus Preparation Run Type while its source
  owner is attached; stop offering source Runs after a package or Contract is
  bound to the Page.
- Use an open Definition discussion's `Resume` instead of suggesting a second
  `+ New Run`; keep historical unbuilt Run Types review-only. Point G0-pending
  users through the discussion before confirmation.

## 0.23.9 · 2026-09-29

- Hide discussion prompts after round release; the round writer refuses an
  open discussion, preserving the G0 meaning bound to a frozen batch.

## 0.23.8 · 2026-09-29

- Keep an interrupted Result's `Finish Run` card in the Board's waiting list.
- Apply the no-judgment Definition gate to an already-open discussion's writer
  calls, matching the Workbench's prompt suppression.

## 0.23.7 · 2026-09-29

- Point the Page header and Board card at interrupted calibration Result
  finalization before guideline work. The copied ongoing-round prompt now
  calls `open_item` for an already-shown unfinished item and forbids replaying
  its recorded first answer.

## 0.23.6 · 2026-09-29

- Hide Definition discussion start/resume requests until the Contract is
  valid and the job is not on HOLD; suppress new or replayed discussion
  prompts once any item has been judged.

## 0.23.5 · 2026-09-29

- Offer a contextual `Resume` copy request to finish an interrupted
  human-calibration Result when every item has a final event but the runtime
  is still running. The request uses `calibration.py finalize` on the same
  Ticket and never asks for judgments again.

## 0.23.4 · 2026-09-29

- Hide `human-calibration` `+ New Run` after any calibration Ticket exists for
  the open round. A closed or unreadable runtime cannot be reused by the
  engine; the Workbench keeps its history visible without a misleading action.

## 0.23.3 · 2026-09-29

- Give a released round a contextual `human-calibration` `+ New Run` copy
  request before its first item; `Resume` appears after the first item opens.
  Hide that request without an open item or while the job is on HOLD. Embedding
  and round preparation use their checked view buttons instead of a generic
  Runs-panel start prompt.
- Suppress `Resume` on stale human-calibration Tickets and `Rerun` on finished
  batches. Point the copied JUDGE prompt to the Rounds view skill and describe
  optional reference observations accurately.

## 0.23.2 · 2026-09-29

- Make the Board-backed Studio Chat versus direct Page agent-conversation
  distinction explicit in the first-use path and surface summary.

## 0.23.1 · 2026-09-29

- Clarify that host commands need Python 3.10+, the direct Page route uses
  the current four-Space presenter, and Data → Contract has a copy request
  after an accepted preparation package is linked.

## 0.23.0 · 2026-09-29

- The dedicated Labeling host opens an existing canonical Page folder through
  `/workbench/labeling?file=<Page>/<Page>.md` without a Board or generated
  Page. The mixed Board host cannot use that route. The same action door
  checks origin and engine authority before accepting writes.
- Flat Board Markdown sources now ask for their own Page folder before Corpus
  Preparation or a new Contract. The Workbench no longer offers source-owned
  Run prompts that would write into a shared group lane.

## 0.22.1 · 2026-09-29

- The Runs panel now lists every Skill declared for the selected Run Type,
  including shared workflow, domain, procedure, and View context Skills.
- The 26-row Run Type table is the panel's Skill source. It describes guidance,
  not the Skills actually loaded by a historical Run.
- Point the prerequisite and roster reference at the current `haipipe-workbench`
  Skill name.

## 0.22.0 · 2026-09-26

- A labeling job's Runs sit in the Page folder, beside `labeling/`:
  `<Page>/runs/<run>.yaml` and `<Page>/results/<run>/`, the same lane every
  other Page uses. `labeling/` now holds only the job's own state.
- Receipt paths are relative to the Page, so job files read `labeling/...`.
- `engine/job.py` gains `page_root`, `runs_dir`, `results_dir` and `page_path`;
  the calibration, embedding, page plugin and presenter code read through them.
- S-Label-4's seven Runs moved up; all 45 receipt hashes still match.
- The surface matches the Page workbench (260927): four Spaces (Data, Labeling,
  Quality, Delivery), no Run Space, no page bar, no Focus. The page is the title,
  the Space tabs with Studio Chat at the end, then one Space: its content on the
  left and its Runs panel on the right at every width, sticky while scrolling;
  `▸/◂` folds the panel to a thin strip.
- A view lists only its own Run types, from the new `view` column of the Workflow
  map in `ref-space-mapping.md`; types not built yet stay in the map only. The
  selected Run shows its name, state, Resume or Rerun, a folded Prompt whose Copy
  works folded, Running process and Results. `+ New Run` shows an open prompt.
- Workflow (Phases, SOP, Workflow map) and All runs open only from
  `?drawer=workflow` and `?drawer=allruns`.
- Hints, notes, status chips and explanation sentences are cut from every view;
  the Discussion view keeps only its question and `Copy discussion brief` (the
  example cards and run plan are gone). The Embedding view lists only unfinished
  builds. `_RUN_WORDS` follows the ref again.
- Content and Runs pick each other, as the Page workbench's Card ↔ Runs: a build
  in Data › Embedding and its `embedding-build` Run, a round in Labeling › Rounds
  and its Runs, linked by the Run's `target`.
- A rerun on the same target is named `-2`, `-3` after the older Run; Runs sort
  by rlNN number (rl10 after rl03).
- The round's chat prompt lives only in the Runs panel (`Resume` on its
  `human-calibration` Run); Rounds no longer repeats it.
- No placeholders: `—` and `not implemented · HOLD` lines are left blank.
- New Run type `definition-discussion` (26 operation kinds; JL 260927, after
  finding S-Label-4's label wording was AI-written): the human settles each
  label's wording in chat through `engine/definition_discussion.py` (start, say,
  decide, close). A changed wording is one `job.revise_meanings` revision
  (`gates/meaning-revisions/<seq>.json`) that retires G0, so Confirm meaning is
  pressed again; `status` rebuilds the P0 anchor through the revision chain.
  Refused once any item is judged. SOP step 2; happy-path plan is 44 Runs.
- Views exist only where Runs live (JL 260928): Data = Contract (Schema merged)
  · Embedding; Labeling = Definition (Discussion + Label merged, with Confirm
  meaning) · Rounds · Guideline; Delivery gains Scan. Run names are
  `run-<operation>-<target>`; types sort by the Workflow map's new `step` column.
- One skill per view, never shared (JL 260929): eleven `subjective-label-<view>`
  skills; each Run card shows `Skill <name>` from the new View skills table.
- No hash wording (AGENTS.md rule 9); the engine checks content, not checksums.
- Labeling → Discussion shows each discussion's labels before and after; the
  Label view's ⧉ buttons and the Discussion view's Copy brief are gone, since
  their prompts are now this Run's `+ New Run` and `Resume`.
- `_space_mapping_ref()` finds `skills/label-building/ref/ref-space-mapping.md`,
  so the SOP and Workflow map render again.
- Design: `servers/workbench-labeling/studio/labeling-workbench-design.excalidraw`.

## 0.21.0 · 2026-09-22

- Renamed from `haipipe-plugin-labeling` to `haipipe-workbench-labeling`, pairing
  by name with `servers/workbench-labeling/`.
- subjective-label has its own host, `servers/_host/serve.py`: the shared
  haipipe host run with `--only labeling` (own port, DOMAIN, auth file; no
  terminal, chat or Board write routes). Addresses: `<DOMAIN>/w/<board-slug>`
  and `<DOMAIN>/w/<board-slug>/<page-id>/labeling`; the server composes
  `path`, `file` and `page`.
- `labeling.py` reads the Board grammar through one adapter, `_board_pages()`.

## 0.20.0 · 2026-09-21

The 🏷 Labeling presenter now ships with this plugin: `live/labeling.py` and
`60-workbench-labeling.js` moved from the Board skill to
`plugins/subjective-label/servers/workbench-labeling/`, where the toolkit's
server host discovers them as `live.labeling` and as a drawer part. The
presenter reaches `engine/job.py` two folders up instead of walking for it.

## 0.19.0 · 2026-09-21

Make the first-use SOP stop at the supported round-1 frontier. Distinguish the
Run Type catalogue from actual Tickets and runtime status, mark unbuilt
operations without implying their results exist, and correct production
human-review and candidate-reconcile placement. Record the owner/worker Skill
and contextual-copy fields required by a future host map. Record that the
current round prompt is copy-only but lacks full Page/target/Ticket/gate
context, and that contract setup has no in-page copy affordance yet.

## 0.18.0 · 2026-09-20

Show P2-P5 as unimplemented and held instead of presenting them as future
steps in a completed lifecycle. Make the caller-supplied authority id and
attestation language explicit and disclose that the local Board does not
authenticate the actor.

## 0.17.0 · 2026-09-16

Match the built Board surface and engine. The surface now has five Spaces:
`Data` (Contract, Schema, Embedding), `Labeling` (Label, Rounds, Guideline), `Quality`
(Test, Evaluation, Audit), `Run` (Runs, Phases, Workflow map), and `Delivery` (Handoff,
Final labels). Guideline is a view inside Labeling; P0-P5 is phase state in `Run → Phases` and the `Next:` header. The page
opens on the Space that holds the next step. The browser gains one write door,
`POST /_board/labeling/act`, with exactly ten engine-checked actions
(`confirm_meaning`, `release_round`, `open_item`, `first`, `final`,
`build_embedding`, `embedding_status`, `embedding_item`, `group_examples`,
`embedding_item_text`). Runs are
documented as Tickets under `labeling/runs/` and Results under
`labeling/results/` in every phase. The implement list adds
`engine/calibration.py`, the act route, `LabelingWriteDoorTest`, and
`engine/test_calibration.py`, and names the standalone `engine/page_plugin.py`
as the older read-only presenter. Two levels: `GET /_board/labeling-board` lists every labeling job on the
Board (zoom out) and each card opens that Page's surface (zoom in); the Page
header links back with `← All labeling jobs`. `Data → Embedding` shows how an
item becomes a vector, read from the embedding manifest: the fields joined
(response first, then context), the word-piece limit and how many items were
cut, the model, mean pooling, length 1, and where each row is saved. A made-up
worked example shows real word pieces and the first 8 numbers. A map (t-SNE)
colors every development item by group or by the human's final label and rings
the items a round drew; a group list gives keywords, size, and round coverage.
`Contract → Data` gains an `embedding` row. The person picks the embedder: an
`Embedding model` card lists the open-weight catalog (Qwen3-Embedding 0.6B/4B/8B,
bge-m3, multilingual-e5-large-instruct, all-mpnet-base-v2, all-MiniLM-L6-v2)
with size, word-piece limit, license, and download size; `Build` starts a
background build through the write door (`build_embedding`, catalog ids only,
one build per job at a time), the page watches `embedding_status`, and each
built model gets its own pane and `Showing` chip. Contract cards now each take
the full row. `Labeling → Rounds` now shows each round's frozen draw: state,
who released it and when, the draw method, pool size and seed, each item's
selection probability, the policy version, both Runs, and a list of the drawn
item ids in draw order with their map group and their state. The embedding map is interactive:
click a dot to see its group, round state, word-piece count, and its 6 nearest
items by cosine similarity (lines drawn to them; click one to move on); click a
group or legend entry to light that group up; show only round items; zoom
with + and − or a pinch, and drag to pan (a finger swipe still scrolls the
page). A 3D view of the same items can be dragged to turn, set to Spin, zoomed,
and clicked like the 2D map. The person controls each run from a `Run a new
embedding` form: model, which text (reply + context, reply only, context
only), an optional instruction for Qwen3 and e5-instruct models, group count
(auto or 2-20), map method (t-SNE or PCA), and seed. Each setting combination
is its own folder and Run, named after the model plus one tag per non-default
setting; `Your runs` lists every run with its settings and state. Each group in
the Groups card has `Show typical items`: the items nearest the group centre, 3
at a time, with the last two conversation turns (earlier turns on request), the
reply, and the group keywords marked; a picked dot has `Show its text`. Items
waiting in a round are left out, so the first look at them stays on the Label
screen, and every item shown is appended to `labeling/exposure/group_examples.jsonl`
(who, when, which build, which items). The text is fetched through the write
door and is never in the page HTML. A click-through review at 1000, 1440, and
2000 px and on a phone fixed: the hidden 3D canvas showing as an empty box under
the 2D map (any `hidden` element now always hides); a map taller than the window
on wide screens (now at most 72% of the window height); the map note naming
t-SNE for a PCA build; the Build record's group line and rebuild command
ignoring the run settings; blank word-piece chips for a newline; and the
Guideline view showing raw markdown (now rendered). `group_examples` sends
`group_index`, never `group`: the Board server reads a POST field named `group` as a
group-level chat session before any route, so every group but G1 (index 0) dropped
the request ("Failed to fetch"); `serve.py` now treats only a text `group` that way.
An embedding runs only when a person asks: the `Run a new embedding` form is always
open and shows only the model (name, download size, one-line note) and its `Run embedding`
button; text, instruction, groups, map, and seed sit under a closed `More settings`,
label/value rows and tables are bordered cells with a shaded label column (the Paper
plugin's `.kv` look), the Groups card is one table (group, keywords, items, picked,
labeled) with `Show typical items` per row, the map toggle `Round items` is now
`Picked for labeling`, and the Contract's embedding row lists one build per line;
a readability review by a fresh subagent (25 findings, 1440 px and phone) led to plain
words throughout: chatbot turns read "AI"; the page title is the job's question; times
read "16 Sep 2026, 3:13 pm"; rounds read "round 1"; Phases is a step line with "waiting for"
in words; "held back" and "to label" replace "sealed" and "development" on screen; the
Embedding view opens on the Map and Groups, with "How the map is made" and "Technical
details" folded; builds have short names ("MiniLM · reply + context"); runs and groups are
tables; the Run Space names what ran in words; the Board list drops its duplicate progress row;
`Run → Workflow map` (like the Paper plugin's) projects the new `## Workflow map` table of
`ref/ref-space-mapping.md`: one row per Run type (all 25, grouped by step), one column per
Space (`start` / `shows`), who starts it (a button, Chat, setup, or "not built yet"), where it
writes, and how many Runs of that type the job has; above it, an SOP card projects the
new `## SOP` table (12 steps: what happens, what you do, what the chat or engine does,
where, which Run) and marks this job's state per step (done, running, not yet, not built
yet) with the current step as "now"; the Run Space's plain words come from
the same table's `in words` column;
`Labeling → Rounds` cards are collapsed to one line with a compact item table whose
columns are #, Item, Text (the reply once the item has been shown, conversation folded),
Group, State, and Feedback (notes from the chat, `calibration.add_feedback` →
`sessions/feedback.jsonl`), so the person reads the round while labeling by chat; the terminal hint is gone from the top card,
`Runs on this job` (was `Your runs`) and the Build record say who started each build
(the button, the terminal for a named person, or no request recorded), and the CLI
refuses a build without `--started-by`.
`Labeling → Label` now holds the label definitions: the question, the judge
and scope rules, who confirmed them and when, a table of labels with their
meanings, the in-between cases, and how-sure levels. A `Copy chat prompt`
button and one `⧉ chat` icon per label (and one for in-between cases) copy a
prompt for defining the labels better in a Claude chat; an agreed change is a
guideline patch for LEARN, never an edit to the confirmed `config.yaml`.
`Labeling → Rounds` holds the rounds: the open round's card starts expanded
with its own `Copy chat prompt` (job folder, question, labels, progress, items
waiting for a final, the next five items, and the JUDGE-by-chat rules); State
shows `first: <label>` after a first answer and the final label after a final.
The one-item keyboard screen is gone, so no view writes a `show` event any
more: the chat shows an item (`calibration.open_item`) and records the
person's stated answers (`record_first`, `record_final`, `add_feedback`). With
no round open, Rounds shows `Start round 1` or the round-done notice first.
Every copy button writes nothing.

## 0.16.0 · 2026-09-16

Reduce visual color and align the Space order with the Page/Outline roster:
`Data`, `Guideline`, `Labeling`, `Quality`, `Run`, `Delivery`. Run and Delivery
are now the final two top-level tabs. The Workflow map gains a Delivery column,
and Delivery Space presents final artifacts and handoff receipts without
creating another execution controller.

## 0.15.0 · 2026-09-16

Redo the live page with the Outline-plugin presentation grammar: five compact
Space tabs (`Data`, `Guideline`, `Labeling`, `Run`, `Quality`), nested view tabs
inside each Space, and a read-only Workflow map inside Run Space. Labeling now
exposes `Iterations`, `Current Run`, and `History`; the interactive
`rlNN_human-calibration` Run is shown there, while item interactions remain
Steps/Events inside that Run. The former giant global workflow rail and the
separate Human Space are removed.

## 0.14.0 · 2026-09-16

Collapse Space and Workspace into one location concept. The Labeling surface
now has one Space navigation rail—Data & Label, Guideline, Human, Run, and
Quality—plus a separate Workflow phase/state rail (P0 Contract → P5 Audit).
Workflow map, Building Runs, and Scanning Runs are sections inside Run Space
rather than a second navigation layer.

## 0.13.0 · 2026-09-16

Reshape the page-level surface into four top-level Spaces with inner
Workspaces: Data & Label, Guideline, Run, and Quality. `Data & Label Space →
Start here` is the default onboarding door; `Run Space → Workflow map` is a
read-only Run Spec × Space table, and concrete `rlNN` Tickets remain separate
from the map.

## 0.12.0 · 2026-09-16

Make `Data & Label` the first/default Workspace. The page now explains the
onboarding order—choose the corpus, inspect its safe schema, define label
meaning, then unlock Workflow after a valid human meaning confirmation—instead
of leading with P0/G0–G6 gate state.

## 0.11.0 · 2026-09-16

Make Labeling one full Page-level Space with six internal Workspaces, promote
Runs to a first-class read-only Workspace, and open Studio Chat separately
instead of embedding it as a permanent lower panel.

## 0.10.0 · 2026-09-13

Require Quality to show the active destination custodian and visibly classify
imported source custody as provenance only.

## 0.9.0 · 2026-09-13

Define current sealed-test custody against the destination reservation's
`custodian`; imported source-custodian text is provenance and cannot replace
or invalidate that active role by itself.

## 0.8.0 · 2026-09-13

Clarify the lower transport contract: Board hosts persistent Studio Chat;
standalone Page Folders point to the current Codex task and never imitate a
Studio or HTTP chat backend.

## 0.7.0 · 2026-09-13

Add the standalone Page Folder host, native `rlNN` Run projection, Page-private
`labeling/` boundary, and current-Codex-task transport.
