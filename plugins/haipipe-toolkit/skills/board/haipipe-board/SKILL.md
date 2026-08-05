---
name: haipipe-board
description: >-
  Open and run a BOARD: one topic, one source folder tree, and one markdown page per decision (Q) or lifecycle stage (S), generated into a browsable board/ site with an Index, one page per group, one page per Q/S file, and shared assets. Use when a topic has several undecided questions or stages that need to be laid out and closed; when one Page must run through an automatic, auditable lifecycle; when a session must remain visibly attached to a Board, page group, or page; when sharing work with colleagues; or when the user says board, status strip, queue, open this board, open a board, add a question, run this page, audit this page, close the board, 打开这块板, 开板, 加一题, 关板, or /haipipe-board. "Open BOARD_FOLDER" means VIEW an existing board by rebuilding it and pushing board/index.html to the user's VS Code browser over the VS Code IPC socket. It does not mean creating a new board, opening a retired board.html, or using file://.
metadata:
  version: "0.123.0"
  last_updated: "2026-08-06"
  summary: "Probe entries are hidden SOURCE RECORDS, not board pages (JL ruling B, 260806): the probe QA (entry record) is named <n>-<slug>.md so the Q/S/Agent/Meeting page sweep never finds it, and points at the bank QA, the original; ref/topic-entry-contract.md states the record shape, the naming law, and the twin-QA vocabulary, and the checker finds records with its own probes/ glob."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board: one topic, one source tree, one generated Board site

**One board = one folder.**
Inside it, one decision or stage gets one `.md` page. `build.py` derives one `board/` site that anyone can open at `board/index.html`.
Q is a decision, S is a lifecycle stage (JL 260729: no longer called a ruling); the two share one layout but not one closing semantic.

It replaces `/haipipe-session` (that skill was only a working log the person doing the work read for themselves).

**Two things must hold (JL's rule):**

- Opening it tells you what you are doing.
  That rested on `spine` (rendered on the Index) and `## Topic` in board.md.
  As of 0.78.0 `## Topic` is source-only and no longer rendered on the Index, so orientation on the rendered page now comes from the Index's Board Map and Section Matrix rows instead.
- You know when you can stop.
  That rests on `close` (the closing condition) and each page's `## Aims` plus `## States`.

## 👪 The family: one door, one Page base, two contract catalogs

This skill is the DOOR: you invoke it to run a board.
The rest of this board family (`../`) is what other agents LOAD or CALL without opening the door, and this skill routes to them rather than restating them:

**The board's sub-skills**: which altitude each one works at.

```
haipipe-board-page       SPEC + ROUTER · the shared Page frame and the
                         Page Type × Page Phase composition
page-types/
  haipipe-board-page-for-stage
                         TYPE · S-<Family>-<unit> lifecycle pages
  haipipe-board-page-for-skill
                         TYPE · Skill-<n> and Agent-<n> mirror pages
  haipipe-board-page-for-venue
                         TYPE · QBv<n> venue pages
page-phases/
  haipipe-board-page-draft
  haipipe-board-page-probe
  haipipe-board-page-revise
  haipipe-board-page-check
                         PHASES · promise, inquiry, realization, judgment
ref/topic-entry-contract.md
                         LEGACY IMPLEMENTATION SPEC · the persisted Probe Page
                         shape used by the current topic checker; not another
                         Page Type or lifecycle phase
haipipe-board-sentence   DOOR + SPEC · one sentence: comment, edit, card;
                         lanes, addresses, the archive-never-delete lifecycle
haipipe-board-routing    VERB · every write onto a board, at BOTH altitudes:
                         board.md's structure (propose · materialize · lanes ·
                         regroup) and one input → owning page → anchored write;
                         proposes, never creates; closes only answered rows
haipipe-board-creator-agent    AGENT · writes ONE page in a fresh context;
                         designed to fan out N of them, keep every shared write here
haipipe-board-reviewer-agent   AGENT · the read-only fresh-context reviewer
haipipe-board-page-orchestrator-agent
                         AGENT · runs one bounded Page loop, stores and audits
                         the receipt, never writes Page prose
```

`haipipe-board-index` was retired on 260802 (JL: "maybe merge, I will do B") and its whole altitude, including `lanes.py`, lives in `haipipe-board-routing`.
Three of its five verbs were other units' work written a second time, and the merge gave a group-altitude finding somewhere to land, which it had never had.
The `open` action below still describes proposing and materializing a board, on purpose: a person opening their first board should not have to load a second skill, and the two descriptions are corrected together.

The specs cite this skill's `ref/` files as their authority and never fork them; the verbs load the specs.
`haipipe-board-digest` (a transcript fanned out through routing) is named on the roster and not yet shipped.
For a batch of page creations or Opening revisions, the caller dispatches
exactly one fresh `haipipe-board-creator-agent` per page. Waves are allowed when
concurrency is limited, but one writer never owns two pages in the batch. The
assignment packet carries page facts, paths, sources, and ownership context,
not a copied prose checklist: every creator loads `haipipe-board-page` itself.
An existing Opening uses the creator's `revise-opening` operation, which reads
the target page completely and edits only that section. The caller alone owns
shared writes, one rebuild, and one mechanical check after all pages land.
Writer self-checks are local evidence, never approval. A fresh
`haipipe-board-reviewer-agent` then judges each changed page and reads all
changed Openings consecutively in Board order; interchangeable or form-letter
prose fails even when every page is locally clear.
For an automatic one-Page lifecycle, dispatch
`haipipe-board-page-orchestrator-agent` instead. It invokes the Page Workflow,
which calls the same creator for exactly one DRAFT, PROBE, or REVISE authority,
then a mechanical builder/version snapshot, then the reviewer for CHECK. The
orchestrator stores the exact result under `_runs/page/` and audits it; it never
writes Page prose, and the reviewer never cures its own finding.
A Page Type variant ships WHERE THE BOARD FAMILY MAINTAINS IT (JL 260803).
The three `for-*` variants maintained here ship under `page-types/`; family-specific stage data, such as the paper door's `stages/` and craft files, stays with its family.
The earlier rule read "ships under its CONSUMER, never here", and it broke the day a second variant landed: venue pages are consumed by the paper family and maintained here, so they satisfied neither that rule nor its Skill-and-Agent exception.
Who maintains it is the line that held twice; who consumes it never did.

**The Page Types, and how each one is CREATED**: six filename shapes, two procedures.

```
type      filename                     created by
──────────────────────────────────────────────────────────────────────
Q         Q<group><n>-<slug>.md        copy ref/page-template.md
S         S-<Family>-<unit>-<slug>.md  copy, or cli/stage.py new
QBv       QBv<n>-<slug>.md             copy QBv1-misq.md as the shape
Skill     Skill-<n>-<slug>.md          cli/skillpage.py new   ← GENERATED
Agent     Agent-<n>-<slug>.md          cli/skillpage.py new   ← GENERATED
Meeting   Meeting-<n>-<slug>.md        cli/meetingpage.py     ← GENERATED
```

A GENERATED Page Type is never copied from the template: the generator writes it from its own stub, owns managed spans inside it, and registers it in `board.md` itself.
`Meeting-<n>` had an engine and no contract in any SKILL.md until 260803; it is listed here so the kind is discoverable, and a contract for it is still owed.

## 🗂 Shape

**Where a board folder lives**: the two homes, by who owns the board.

```
<owning-unit>/diagram/<NN>-<topic>-<YYMMDD>/       # task / project / paper
<plugin>/skills/diagrams/<NN>-<topic>-<YYMMDD>/    # plugin skill-design Board
  board.md                    title · spine · close · ## Topic · ## Pipeline
                              · optional ## Board Map · ## Board Structure
                              · ## Pages
  QA-<group-title-slug>/      ← one group, one folder (the default, JL 260726)
    QA1-<slug>.md             one question, one file
    QA2-<slug>.md
  QB-<group-title-slug>/
    QB1-<slug>.md
    S-Seed-0-<slug>.md        a named lifecycle page (only when there is a lifecycle)
    Skill-1-<slug>.md         a skill skill page
    Agent-1-<slug>.md         an agent skill page
  board/                      ← generated by build.py, never hand-edit
    index.html                Board-Webpage-Index
    QA.html                   one Board-Webpage-Group
    QA/QA1-<slug>.html        one Board-Webpage-Page per source page
    _assets/board.css         one shared assembled stylesheet
    _assets/board.js          one shared assembled script
  fig/
```

The descriptive source folder (`QA-<group-title-slug>/`) and the compact generated route (`board/QA/`) are deliberately different. The source folder explains itself on disk; the generated token keeps page URLs short and stable.

- **The group folder is the default (JL ruled 260726).**
  From the first page onward, one group gets one folder, named `Q<group-letter>-<group-title-slug>` (`QA-defining-a-board/`), **never a bare `QA/`**.
  Writing only `QA/` just copies the id a second time; the half a reader cannot recognize is precisely the title half.
  Membership has looked only at the path, not at a registry, since 260722, so moving pages into folders is a plain `mv`: `## Pages` still writes bare filenames only, board.md needs not one word changed, and the render is identical except for the path attribute used for write-back (verified across 30 pages).
  The ＋Q on the page writes into the folder its group already lives in; a newly opened group gets a named folder opened by its first page.
  To move a whole existing board: `python3 <skill>/cli/regroup.py <board-folder> --apply` (omit `--apply` for a dry run).
  **⚠️ Run `check.py` once after moving.**
  `## Pages` writing bare filenames is unaffected, but `## Links` writes real paths, and any that point across boards into someone else's page will break (moving 154 pages on 260726 broke 17 links; all were fixed).
  **Never re-fold a board that is already sorted into folders**, for example a paper's `0-lifecycle/`: `0-seed/ 1-work/ 3-display/` is already both a subject folder and an S family, so it already satisfies this rule, and the numbering additionally carries lifecycle order.

- **Owning unit** = whoever this board serves.
  Task, project, and paper boards default into their own `diagram/`; boards used to design a skill inside the same plugin collect in that plugin's `skills/diagrams/`.
  Both locations keep the board separate from the skill it describes: the board is a work product, the skill is the deliverable package.
- **NN only orders within the same topic series; it is never a global counter.**
  A new topic starts at `01`; only a later board on the same topic uses `02`.
  So the shared `skills/diagrams/` can hold several different topics all starting their own `01-*`.
- **The date is the day the board was opened, and it never changes afterward.**
  One folder, one topic; later discussion is appended into it, never split into a new one.
- **Membership on a board is decided by path.**
  Every `Q*`, `S*`, `Agent-*` and `Meeting-*` `.md` anywhere in the board folder's **whole tree** is a page of this board (except segments starting with `_` or `.`, and `fig/`). Those four prefixes are what `page_files()` in `src/common.py` globs; a `Skill-` page rides the `S` glob, which is why it is not a fifth prefix.
  `## Pages` only controls ordering and grouping (and still only writes filenames); an unregistered page still shows up (filed under the ⚠️ group) and the command line flags it.
  **Missing registration only makes it ugly, it never loses the question.**
- **A Q/S file can live inside the folder it is about.**
  `4-display/QD2-….md` and `3-display/QD2-….md` and `3-display/S-Display-0-design.md` will all be discovered.
  An existing tree (for example a paper's `0-lifecycle/`) can therefore serve directly as a board, with each question living right next to what it is about.
  Such a board **does not** follow the `diagram/<NN>-…-<YYMMDD>` naming: the tree keeps whatever name it already has, and the NN-plus-date rule only governs boards newly opened under `diagram/`.
- **`## Topic` and `## Pipeline` are board.md source-only sections.**
  Release 0.78.0 removed the three ctx disclosures (🦴 Topic · 🔄 Pipeline · 🧭 Board-Structure) from the rendered Index on JL's 260731 ruling, so the Index now reads spine → Board Map → Section Matrix → ALL PAGES → Activity.
  Keep writing all three: they are the board's own documentation, and board.md is where a reader or an agent goes to find them.
- **`![[path]]` / `![[path#some-section]]` on its own line** (QF1) means embedding another file's content into this question **by reference**: read fresh at generation time, zero copy and zero drift, and the board does not adopt the source file's dialect.
  If it cannot be embedded, it is flagged red in place.
  See `ref/board-form.md` §5 for the full spec.
- **Do not use the `doc:` line in Pages anymore** (formerly QF2, retired 260726).
  To display a file that lives elsewhere, use the `![[path]]` line above to embed it into a real page instead.
  It is the same zero-copy behavior, but the page then has state, has an item count, and has a place for comments to land, none of which a doc page has.
  The parser still recognizes `doc:` only so old boards do not break; no board in the whole SPACE uses it today.
- **A paper lifecycle board groups by named S family.**
  The fixed index order is `Seed → Work → Venue → Display → Main → Appendix → Submission`.
  Display is an independent evidence-presentation layer, not an ordinary item under Work.
  This is ownership/navigation order, and it is not automatically the execution order; the real dependency lives in `## Pipeline`, for example Narrative feeding into Display, which then splits out to Main/Appendix.
  Each S page inside a family is one concrete, CHECK-able page; the Q decision blocking it sits right after that S page.
  Seed usually holds `S Seed` and `S Literature`; Main uses numbered sections; Appendix uses `0, A, B...`; Submission covers at least reconcile, compile, review, and submit.
  The four Submission pages are reused every round; reviewer feedback reopens the affected Work/Display/Main/Appendix page and runs the same reconcile → compile → review → submit chain again, rather than duplicating a page set per round.
  A group title still starts with a single Q family so the page's write-in buttons keep working.
- **Group intro (QC2, 260724)**: in `## Pages`, plain lines between a `### ` heading and its first `.md` line introduce that group.
  Line 1 always shows under the group header on the index; further lines expand on click.
  The page's ＋Q / ＋Group / 🗄 buttons edit this structure through `POST /_board/structure` (`structure_op` in `live/structure.py`); archive moves Q files to `_archive/`, never deletes.

## 🧭 Session attachment and Closing Block

Once this skill is loaded for a Board, make the attachment visible.

**Direct Board session:** end every user-visible reply with the exact three-line Markdown block emitted by `status.py`; put no prose after it.
This includes progress updates, questions, blocked replies, and the final handoff.

**Composed session:** when an explicitly enclosing first-class skill calls `haipipe-board` and defines one canonical closing block for the combined session, the enclosing contract takes precedence.
Do not append a second Board strip.
The enclosing block MUST preserve the Board attachment with a deep `board:` link to the active page and must remain the only closing block.
`haipipe-paper` is the canonical composed case.
Calling Board still transfers no ownership of Board files, rendering, or write-back to the enclosing skill.

Resolve the attachment in this order:

1. the Board/page attachment injected by `serve.py`;
2. an explicit Board path, page path, page id, or group in the request;
3. the nearest `board.md` above the current working path;
4. the attachment already established earlier in this conversation.

If more than one Board remains plausible, do not guess: report a blocked attachment and ask which Board to use.

The strip uses a small closed vocabulary:

- `queue` = the page group declared by `board.md ## Pages`; a page derives its queue automatically, a group is its own queue, and whole-Board work is `board-level · cross-group`.
- `focus` = `board | group | page`.
- `mode` = `discussion | sourcing | implementation | review | status`.
- `status` = `ready | working | blocked | done`.

Sourcing never floats.
`mode=sourcing` must name a page or page group that owns the evidence; whole-Board sourcing without a queue is blocked.

**The mode also decides the shape of the reply's BODY (QA3 §6, JL 260802).**
`discussion` keeps the repo's own default, because working an idea out in the terminal before anything is written down is the one thing that surface is genuinely better at.
`implementation`, `review` and `sourcing` collapse the reply to the outcome, the routing footer and the strip. In those modes a drawing, a comparison, a section or a list of rows is a PAGE WRITE FIRST and a pointer second, because only the page carries an address, a state, and a place for a comment to land.
JL 260802: "some content we want to put them in the Page, and not the user read the claude code results in TUI."
The failure this prevents is one figure existing in a transcript and on no page, disagreeing with the board within the hour, in the copy nobody can correct.

Render the closing block immediately before replying:

**The status call**: what to run to print a board's closing block.

```bash
python3 <skill>/status.py <BOARD_FOLDER> \
  --focus <board|group:ID|PAGE_ID> \
  --mode <discussion|sourcing|implementation|review|status> \
  --status <ready|working|blocked|done> \
  --next "<one concrete next action>"
```

Its complete shape is deliberately only three lines:

**The closing block**: the three lines every reply ends on.

```markdown
🧭 BOARD · QUEUE/FOCUS (deep-link)
✅ done · implementation
→ one concrete next action
```

Do not repeat labels, the page title, source file, or raw URL.
The link wraps the attachment on line 1; queue and focus use their short ids.

The Board files remain the durable record.
Do **not** create a shared `STATUS.md`: concurrent sessions would overwrite one another and stale live state would look authoritative.
When discussion changes a decision, item, comment, or log, still run the normal `sync` action in the same round; the closing block does not replace write-back.

## 🗣 A decision lives on the page

Never ask for a ruling only in chat (JL 260802: "don't put the decision in the claude code session"). Write the row FIRST, in the owning page's `States › Decision Now`, then say in chat which page and which row. The chat line is a pointer; the page is the decision.

**Do not go looking for the page by hand.** `haipipe-board-routing` exists for exactly this: give it the decision and it reads `board.md`'s `## Pages` as the only registry, finds the owning page and section, and appends an anchored write. It proposes rather than creates when nothing fits, and it closes a Decision Now row only once you have answered it, recording which option and the words you used (JL 260802). A row you have not answered still waits for you, which is the line that keeps the ruling yours.

A decision left in a session cannot be seen by anyone else, carries no `Blocks:` and no `Default:` so it evaporates instead of resolving itself, and leaves no record of the options weighed, which is what the next person to reopen it needs.

The row's shape is QB4 §5.2: 🗣 the question as the row's title · 📍 `Part` · 🔔 `Why now` · the options with ⭐ on the recommended one · 🛑 `Blocks` · 🤖 `If nobody answers`. A row that blocks nothing MUST carry a default, so it resolves itself and the list stays short.

And the prior question: most proposed decisions do not belong there at all. The test is whether anything STOPS until it is answered. If you could decide it yourself, decide it and write it in `## Log`.

## 🔨 Actions

Offline (needs `cli/build.py`, plus `cli/stage.py` for `stage`): **view · open · add · stage · build · sync · link · close**
Live (needs `cli/serve.py` running): **serve · excalidraw · comment**
Routed to `haipipe-board-page`: **create a page · update a page · run one page lifecycle**
Routed to `haipipe-board-sentence`: **comment · edit · card**

That is 11 verbs here, plus six routed actions this skill does not run itself.

**One door** (JL 260802: "you can just say, haipipe-board update the page etc, it will route to the haipipe-board-page"). Anything about ONE PAGE routes to `haipipe-board-page`, which owns the page contract and drives that page end to end:

```
🚪 say it here                                    ▸ runs there
──────────────────────────────────────────────────────────────────
"create a new page on <topic>"                    ▸ haipipe-board-page
"update / fix / work on <page>"                   ▸ haipipe-board-page
"bring <page> up to the standard"                 ▸ haipipe-board-page
"why does <page> fail the checker"                ▸ haipipe-board-page
"run / audit the lifecycle of <page>"             ▸ haipipe-board-page

"comment on / edit <sentence>"                    ▸ haipipe-board-sentence
"put a card on <these words>"                     ▸ haipipe-board-sentence
"what may attach to a sentence"                   ▸ haipipe-board-sentence

anything about the BOARD: its groups, roster,     ▸ here
index, serving, the round trip
```

Route by SCOPE at every altitude: one sentence is the sentence skill's, one page is the page skill's, the board and its structure are this skill's.

Inside the one-Page route, `haipipe-board-page` resolves the stable Page Type and the current DRAFT, PROBE, REVISE, or CHECK authority.
The one-Page contract now owns `RUN`, backed by `ref/page-lifecycle.workflow.js`.
It is not `ADVANCE`: the router may repeat, branch, HOLD, or begin a new DRAFT round.
The non-interactive dispatch target is `haipipe-board-page-orchestrator-agent`; the Board door still owns no separate phase verb.

Route by SCOPE, not by wording: one page is the page skill's, the board and its structure are this skill's. When a request names a page id or a page path, it is the page skill's even if it sounds structural, because whoever asks is looking at one page.
`xcal.py` rebuilds the scene offline, but both the embedded canvas and the editable one go through `serve.py`, so `excalidraw` is counted as live.

> **"Open `<some board>`" = view (look at an existing one), not open (create a new one).**
> When the user gives an already-existing folder path, that is view; only creating a new one is open.

### view · open an existing board (the most common case)

When the user says "open `<board folder>`", do these three steps, and **do not just say "opened the Board"**:

1. **Rebuild it first**, so the page is not the stale one:
   `python3 <skill>/cli/build.py <board folder>`
2. **Push it to the user's VS Code browser** (the block below is the only thing that actually works, see ⚠️):

**Resolving a board URL in a shell**: how the deep link is built.

```bash
BD=<board folder path relative to the repo root>   # e.g. Tools/plugins/.../diagram/01-boardform-260722
BOARD_BASE_URL="${HAIPIPE_BOARD_URL:-$(sed -n 's/^[[:space:]]*export[[:space:]]*HAIPIPE_BOARD_URL=//p' env.sh | tail -1)}"
BOARD_BASE_URL="${BOARD_BASE_URL:-http://127.0.0.1:5599}"
S=$(ls -t "$TMPDIR"/vscode-ipc-*.sock 2>/dev/null | head -1)
B=$(ls -t ~/.vscode-server/cli/servers/*/server/bin/helpers/browser.sh 2>/dev/null | head -1)
VSCODE_IPC_HOOK_CLI="$S" "$B" "$BOARD_BASE_URL/$BD/board/index.html"
```

3. Report the board's status in passing: how many questions, how many unresolved comments, where it is stuck.

⚠️ **Why a server-side `open` and `file://` cannot be used**: on a Remote-SSH machine the **browser is on the user's laptop and the files are on the server**.
`open` only opens something on the server's desktop, where the user sees nothing; `file://` points at the user's own local disk, which holds none of these files.
You must go through the IPC above, handing the URL to the VS Code on the user's side.
**On a local machine** (not Remote-SSH: there those two globs find nothing) just run `open "$BOARD_BASE_URL/<board>/board/index.html"`: it goes over http (only then is the comment layer alive), and it still never touches `file://`.

`BOARD_BASE_URL` and the `status.py` at the end of every reply use the same reader-facing setting: the current environment's `HAIPIPE_BOARD_URL` wins, then only that one item read from the repo root `env.sh`, and only then the fallback `http://127.0.0.1:5599`.
Never write one machine's Tailscale IP into shared skill source.

This needs `serve.py` running on 5599 (start it first if it is not, see the serve section).
`#top` returns to the index, `#QA6` jumps straight to one question, `#all` expands everything.

### open · start a **new** board

1. Ask three things: **what this board has to solve** (→ `spine`), **when it counts as finished** (→ `close`), and **which pages there are** (how many Q decisions, plus how many S stages when there is a lifecycle).
   That page list needs the user's explicit OK before you go any further: this is the only place where you must stop and ask.
2. Pick a location and create the folder: task, project, and paper use `<owning-unit>/diagram/<NN>-<topic>-<YYMMDD>/`; a plugin skill-design Board uses `<plugin>/skills/diagrams/<NN>-<topic>-<YYMMDD>/`.
   NN increments within the same topic series, and different topics may each start at `01`.
3. Write `board.md`: the title, `spine:`, `close:`, `## Topic`, `## Pipeline`, `## Pages` (write all three sections).
   To give the reader a **map they can walk**, write `## Board Map`: one ``` figure drawing how the groups connect and the cross-group page edges that really exist.
   The page ids and group tokens inside the figure render as links (0.53.0), so the ASCII map is the only map you can click your way through, it draws on a static host, and it is still there with scripts turned off.
   It renders at the top of the index as a disclosure you **can close**, and it takes precedence over the `board-map:` share link and over a local `board.excalidraw` (declare one source, not two).
   **Do not copy the index's roster a second time**: the roster below already lists every page, and what the map has to draw is the **connections**.
   If this board has to show its own shape to a zero-background reader, write `## Board Structure` after Pipeline.
   Since 0.78.0 it is board.md source-only documentation rather than a block on the rendered Board Index, and it is never opened as a Q page; inside it, keep `Board-Folder` (the source and the generated output on disk) separate from `Board-Webpage` (`Board-Webpage-Index` and the pages you reach after opening).
   An old board without this section still generates normally.
4. A Q or S page copies `ref/page-template.md`, and the rename decides which kind it is (a Skill, Agent or Meeting page does NOT: see step 4b): a decision becomes `Q<group-letter><n>-<slug>.md`; a paper lifecycle page becomes `S-<Family>-<unit>-<slug>.md`, where Family is `Seed|Work|Venue|Display|Main|Appendix|Submission` (for example `S-Seed-1-literature.md`, `S-Main-3-theory.md`, `S-Appendix-A-prompts.md`).
   A skill skill page becomes `Skill-<n>-<slug>.md` and an agent skill page becomes `Agent-<n>-<slug>.md`: the S grammar minus the family, where the number orders the roster and the slug says which unit the page mirrors (`src/parse.py`, JL 260731: a skill is LOADED into a context, an agent is DISPATCHED into a fresh one).
   The `S0-<slug>.md` of a plain old board stays compatible.

4b. A `Skill-`, `Agent-` or `Meeting-` page is GENERATED, never copied. `cli/skillpage.py new` writes the first two from its own stub and `cli/meetingpage.py` writes the third, and each registers the page in `board.md` itself. Copying `ref/page-template.md` for one of these produces a page with no managed spans, which `skillpage.py check` then reports as `no managed block` forever. Load `haipipe-board-page-for-skill` before writing the authored half of a Skill or Agent page.
   `<slug>` uses short lowercase English (`access`, `scheduling`), matching `ref/board-example.md`.
   A newly opened page is always `state: 🔴 OPEN` (Q and S use the same set of four states, see "One page" below).
   Give the owner by nature: whatever needs a ruling or an authorization goes to JL, hands-on work goes to the responsible colleague's initials or to CC.
   An S must additionally carry an explicit `## Stage Contract` and `## Content` (a Q writes no Stage Contract, and its Content is optional).
   Do not guess the upstream from the order of Pages; write it explicitly at the top of the S: `requires: S-Work-1, S-Main-0`, `style-from: S-Venue-1`, `provides: ...`.
   Create it with `stage.py new`, or refresh the managed contract with `stage.py sync`; never hand-copy the upstream's full text.
   In Pages an S writes only its bare filename, exactly like a Q: the group title is free text, so opening a separate group for stages (`### S · this lifecycle`) or mixing them into a related group are both fine.
5. Generate: `build.py` lives in the **skill folder**, not in the board folder, so pass its path.
   `python3 <skill>/cli/build.py <board folder>` (`<skill>` = `Tools/plugins/haipipe-toolkit/skills/board/haipipe-board`).
   **Do not `cd` into the board folder and run `python3 build.py .`**: build.py is not there.
   Generation writes only into `board/` and never touches your `.md` (md is the only source).
6. **Push `board/index.html` to the user's VS Code browser as described in the view section**, and do not merely report a path.

### add · add a question

Copy `ref/page-template.md` → new filename → write it into `board.md`'s `## Pages` → rebuild.
That is the Q and S path. A `Skill-`, `Agent-` or `Meeting-` page is generated instead, by `cli/skillpage.py new` or `cli/meetingpage.py`, which register it themselves (step 4b above).
Forgetting to write it into Pages does not lose it; it only lands in the ⚠️ group.
A folder question (QC3): put the new file into the folder it is about; Pages still writes the filename only, and filenames must be unique across the whole board.
The ＋Q on the page always generates the file at the **board root**: if it should live in a folder, move it there yourself (the Pages line needs no edit).

### stage · create or refresh a lifecycle page

An S page's "what the previous stage requires" and inherited writing rules may only come from an explicit reference, never from guessing at adjacency in Pages.
`build.py` only ever reads Markdown; the thing that actually writes files is `stage.py`:

**Creating a stage page**: the one command that writes a new S page.

```bash
python3 <skill>/cli/stage.py new <board-dir> \
  --family Main --unit 7 --slug results --title "S Main 7 · Results" \
  --requires S-Work-1,S-Main-0,S-Display-0 \
  --style-from S-Venue-1 \
  --provides "reader-facing results section" \
  --directory 5-section-edit/6-results \
  --group "QE · Main Group"

python3 <skill>/cli/stage.py sync <board-dir> S-Main-7
python3 <skill>/cli/stage.py sync <board-dir> --all
python3 <skill>/cli/stage.py check <board-dir>
```

`new` generates the S file, adds it to the named Pages group, writes the managed `## Stage Contract`, and materializes inherited prose rules in `## Writing Style`.
`sync --all` runs a topological sync over the explicit `requires` / `style-from` dependency graph, not over the order of Pages.
`sync` replaces only the marked `haipipe:contract` and `haipipe:style` blocks, and never touches Content, Aims, States, the author's own Writing Style prose, or `### Provides`.
As soon as an upstream source file changes, build and check report `Stage Contract is stale`, and only an explicit sync clears it.
An upstream should ideally write a short `### Provides` in its own Stage Contract, and a writing source a short `## Writing Style`.
Without those, the generated page keeps the source links and says plainly that a contract is still owed; it never copies a whole Content in order to guess the answer.

### build · generate

`build.py` lives in the skill folder (not in the board folder).
Call it with its path, and do not cd into the board folder to run `build.py .`:

**Build once, or watch**: the two ways to regenerate the site.

```bash
python3 <skill>/cli/build.py <board folder>     # generate once (<skill> = .../board/haipipe-board)
python3 <skill>/cli/watch.py <board folder>     # watch it: regenerate automatically on any .md change
```

Generation uses the standard library only, so the system's own `python3` is enough (3.9 works too).
**Only `serve.py` needs the repo's `.venv`**: it runs `claude_agent_sdk`, which needs 3.10+.
Do not mix up the interpreters of the two commands.

**md is the only source.**
Never hand-edit any generated file under `board/`.

The Board's shared mark lives at `assets/board-mark.svg`.
`build.py` inlines it into each page title and encodes the same SVG as the browser favicon; do not copy the mark into each Board folder.
The default colors are the `--board-mark-*` tokens in `assets/css/00-base.css`, so a recolor changes only those tokens and never the shape of the SVG.

### the round trip and its unit

Markdown is the only source. A direct file edit or a browser write follows the same loop:

**The round trip**: how a reader's action gets back into the markdown.

```text
board.md + page.md ──build.py──▶ board/ site ──reader action──▶ live/write.py
        ▲                                                       │
        └──────── exact sentence or section-boundary write ─────┘
```

The unit is explicit at each hop:

| Hop | Unit |
|---|---|
| Source write | one Markdown file, anchored by sentence or section boundary |
| Rebuild | the changed page, its group page, and the Index when `--only` is available; otherwise the full derived tree |
| Generated output | one HTML file per page, one per group, one Index, two shared assets |
| Browser notification | four-second poll until the open SSE decision is settled |
| Browser swap | the requested page's `div.wrap`; the drawer and terminal remain attached outside it |

A browser write is complete only after the Markdown lands and the generated tree rebuilds. HTML never travels back into Markdown.

### serve · bring the board alive (the live layer)

One server handles every board: it serves the repo root, not one board.

**Serving a board**: the command that puts it on a URL.

```bash
.venv/bin/python <skill>/cli/serve.py --root <repo root> --port 5599
```

`HAIPIPE_BOARD_URL` decides only the domain handed to the reader; the listener is still controlled separately by `--host`.
If the reader URL is a Tailscale IP, you must pass the same `--host <tailscale-ip>` explicitly at startup.
The Board has no authentication and `/_term/` is a real shell, so the listener in shared source stays on loopback by default.

Once it is running, the board is not only readable: **comments land directly on disk** (the next section depends on it), you can **open a chat or a terminal on one question and work there**, and you can **attach an excalidraw canvas** to a question's 🖼 Diagram (what gets written into the md is the line the author typed by hand; `QB8` is still taking shape).
⚖️ One question, one session · one session, one window · N questions, N terminals.
The details are in the board's `QD1` `## Law`.

> The SDK chat version (`QD2`) and the TUI chat version, a real CLI (`QD3`), are **still taking shape in the QD group**, and the terminal's form on a phone or a desktop is `QD4`.
> They are not restricted versus unrestricted: `QD2` carries three permission tiers and defaults to the full one, so the split is a difference of FORM, a rebuilt chat box against the CLI itself.
> Treat those questions as the authority on how they are used, and do not take them as fixed rules (see "the board ↔ SKILL.md" at the end).

### excalidraw · one scene per board, one frame per question

**One board has exactly one `fig/board.excalidraw`, and every page occupies one frame inside it.**
Never split it into one file per question: only a single canvas can express the **relationships** between pages, and that is the one thing a drawing does better than ASCII (`QAa2`, formerly QA4a).

**Self-hosting the canvas**: what to run when Excalidraw is local.

```bash
docker run --rm -d -p 5610:80 excalidraw/excalidraw     # the editor, run it once
python3 <skill>/cli/xcal.py <board folder>                  # rebuild the scene from board.md
python3 <skill>/cli/xcal.py <board folder> --wire           # also write each frame's URL into that question's ## Diagram
```

`board.md` declares the editor address once: `excalidraw: http://127.0.0.1:5599/_excalidraw`.
The live layer proxies the container under that path so that it goes through **the one port that is actually forwarded** (see `QE6`).
The two URLs point at the same file: without `?frame=` it is the whole board, and **this is where you draw the relationships**; with `?frame=<question id>` it is that question's frame, computed live by `serve_frame()` in `live/xcal.py`, and that is what the page embeds.

**What you draw is saved back into the repository**, because the live layer injects `assets/xcal-boot.js` into the app it proxies (`live/xcal.py`).
Open-source Excalidraw has no "save to the server" at all: it reads from `#url=` and saves into the browser.
So that script simply takes over the browser's storage: on entry it feeds the scene in per file (which is why the **"Replace my content" prompt no longer appears**), and while you edit it POSTs the changes to `/_board/excalidraw-save` every 1.5 seconds.
A save that carries `frame=` **replaces only that one frame's slice** and leaves the other 27 exactly as they were: that is what lets "one scene per board" be edited from any page.

⚖️ **The canvas embedded in a page is read-only, and writing happens only in the ✏️ tab.**
One board has one iframe per page, all of them same-origin on the same storage key, so if they were editable that would be 28 editors overwriting each other.
Hence: the iframe uses in-memory storage (you can pan and zoom, nothing is stored); the new tab opened by "✏️ Edit this frame" is the only one that can write, and it takes a lock, so a second tab falls back to read-only automatically.

**Pasted images are saved too**, but they are not stuffed into the scene: the bytes are written to `fig/assets/<fileId>.<ext>` and the scene keeps only a pointer (JL proposed that folder on 260726).
Excalidraw itself puts base64 inside the document, so one screenshot is several MB, and after that every box you move makes git re-diff the whole thing; the repository cannot take it.
On read, `live/xcal.py` restores the dataURL, so **the scene fetched from the server is self-contained** and the editor never knows any of this happened.
⚠️ The price: **opening that file on disk directly with the VS Code or Obsidian plugin shows empty images** (pointers only).

⚠️ Two known edges: **edited seed text is overwritten again by the next `xcal.py` run** (anything drawn beside it is unaffected); **deleting an image element leaves its file in `fig/assets/`** (it is not deleted automatically, because deleting it could not be undone).

Every frame is **seeded with the first ``` ASCII figure in that question's `## Diagram`**: with an empty frame the reader cannot tell "nobody has drawn it yet" from "the feature is broken" (JL hit exactly this on 260726).
The seeding is **one-way**: md is always the only source, and an edit on the canvas never flows back.

Re-running it is safe, which is why it could be made a script at all: ids are stable (`frame-QAa2`), a frame a human moved keeps its position, hand-drawn content is carried over untouched, and **a frame whose page has retired is deleted**.
`--fresh` is the only mode that destroys anything (it re-lays out everything and drops hand-drawn content), so it is never the default.

### comment / edit / card · anything about ONE SENTENCE (routed)

Routed to `haipipe-board-sentence`, which owns the sentence contract and its three verbs the way `haipipe-board-page` owns the page. Say it here and it runs there:

```
💬 "comment on <sentence>"      a person's remark, written under that line
✎ "edit <sentence>"            one line replaced, one word-level record
🪪 "card on <words>"            a panel on a few words INSIDE the line
```

This skill keeps the machinery those verbs call, and nothing else: `src/body.py` renders both surfaces, `live/write.py` and `cli/serve.py` hold the four write routes, `assets/js/40-sentence/` holds the controls a reader touches, and `tests/drive_sentence.py` drives all of it in a real browser.

Two rules that bind the ENGINE rather than the contract, so they stay here:

- **A write needs `serve.py`**, because it has to find that sentence in the server's Markdown. With the service down the page keeps only a pending line or a copyable patch, and it never grows a comment area at the foot of the page.
- **A form CLOSES before it asks for the repaint.** The live swap refuses to run while a textarea inside `div.wrap` holds text, which is what stops a rebuild from eating a half-written comment; a save form is inside `div.wrap` and still holds what it just saved, so asking first asks for something that can only be refused (260802: the edit path wrote its `> ✎` record and the page sat unchanged until someone pressed reload).

The old page-bottom comment queue is dead: it is no longer read, displayed, or migrated.

### sync · when the work is done, write it back to that question in the same round

**The board and the product must move together, or the board is just a stale pretty thing.**

⚠️ **The trigger is "this round did substantive work", not "this round opened some page".**
Every piece of substantive work done anywhere in a /haipipe-board session belongs to some page, even when the work started from one sentence in chat and never once named a question id.
So the order is: **claim which question owns it first, then do the work, then write it back in the same round**.
A piece of work that belongs to no question at all is itself a new question that should be opened.

A real incident (JL 260726): the entire local excalidraw route of QA4a (today `QAa2`) was built and running that same day, while `QA4a` still said `state: 🔴 OPEN` and "Nothing is built and nothing is decided".
The work was right and the write-back was not done, so what the board said and what the machine ran were two different things: exactly the "stale pretty thing".
`check.py`'s `open-with-met-aims` / `partial-with-nothing-open` are what catch this, but they can only see Aim State and never judge the prose, so they are a backstop, not a substitute.

**"Done" means written back.**
Reporting completion to JL without writing back is reporting something that does not exist on the board.

After finishing any substantive work under a page (a file written, an experiment run, a conclusion reached), write it back **in the same round**:

| Write back where | What to write |
|---|---|
| `## Aims` | Durable target states, grouped under their owning Content division. Change these only when intent changes. |
| `## States` | One factual current State row per Aim: ⬜ not started, 🔨 being worked on now, 🧠 waiting on a person or on something outside this page, ✅ met with the evidence named, or ❄️ on ice. The old `🟡` / `🟠` / `⏸️` still parse (`src/common.py`), but nothing new is written with them. |
| `## Log` | One line for each state transition or material change: `YYMMDD HHMM · what changed`. |
| `state:` | On a Q page, every Aim met or explicitly held → starts with ✅; on an S page, only its human gate may produce ✅. Progress made → starts with 🟡; deliberately parked → starts with ⏸️. The standard labels are SETTLED / PARTIAL / ON HOLD, and a human-readable note may be appended after them. |
| the `> Comment WHO` / `> ✎` lines under a sentence | The sentence comments and edit records added, replied to, or confirmed this round |

Then run `python3 <skill>/cli/build.py <board folder>` (or let `watch.py` run it; the invocation is in the build section above).

**Also clear out the claims this round overturned.**
When the board changes, an old description elsewhere in the prose becomes a self-contradiction immediately.
Real examples: the layout had long since changed to stacked while the prose still said "side by side"; the comment layer already pulls in JS while another question still said "insist on zero scripts".
That is the first thing a zero-background reader picks out.

### link · connect the board to its products

What a board discusses (a SKILL.md, a script, another board) usually does not live in the board's folder.
Add a `## Links` section in `board.md` declaring which real path each backticked form maps to:

**A Links block**: how a board declares the paths its pages may cite.

```markdown
## Links
SKILL.md            ../../haipipe-board/SKILL.md
ref/page-template.md   ../../haipipe-board/ref/page-template.md
build.py            ../../haipipe-board/cli/build.py
```

After that, any `` `SKILL.md` `` in the prose becomes a clickable link, one step from the board to the real thing.
Ordinary markdown links written as `[form](path)` work too.
A declared path is never guessed at for existence: write it wrong and it is a dead link, and that is on you.

### close · close the board

A board closes only once every page's `state:` starts with ✅ or ⏸️ and `close:` is satisfied.
Q and S use the same set of states, but the evidence for flipping to ✅ differs: a Q needs every Aim met or explicitly held, while an S needs **its own human gate to pass** (⏸️ is instead an explicit hold).
The index counts the ✅ among S pages separately per named family.
The sentence in `close:` IS the closing condition, so write it so that it can be accepted, not as "close enough".

## 📐 One page

**A page's metadata head**: the four top lines, and what each renders into.

```markdown
# Short title (a phrase, not a sentence)
state: 🔴 OPEN     first token is ✅ / 🟡 / 🔴 / ⏸️; a readable note may follow
owner: CC          JL renders as 🧠 (rules on it), anyone else renders as 🔧
method: one line on how it gets done

## Opening         the lead question, then the visible paragraph, which ends      ┐ 🧭 Opening
                   at the FIRST BLANK LINE; everything after it → More details    ┘
## Stage Contract  required on S; upstream inputs + Venue, managed block          ┐
## Diagram         ascii figure (may be omitted); its own section, folded by      │
                   default                                                        │
## Content         required on S, optional on Q; `###` is a division that folds   │ fixed
                   on its own, `####` is one paragraph                            │
## Aims             durable targets linked to Content; header derives met/total   │
## States           one factual current State per Aim                             │
## Files           action map + scoped related Page context (optional, advised)   ┘
## Law          the rules this question ruled  ┐
## Lesson       the traps this question hit    │
## Glossary     this page's new words          ├ optional · folded, off stage
## Discussion   loose discussion               │  delete the whole section when unused
## Log          260723 1030 · what changed     ┘
```

**The order of what stands on stage is fixed**, and it is the same for Q and S:
`Opening → Diagram → Content → Aims → States` (Files follows the state sections).
Opening carries the visible paragraph, which ends at the FIRST BLANK LINE of `## Opening`; its drawer begins with the rendered “More details” row, which is everything after that blank line (JL 260801, renamed from “Why this matters”).
The optional Diagram is a section of its own, folded by default, and it expands only when the section name is clicked.
Everything after `## Opening`'s first blank line automatically becomes the "More details" row inside its drawer, identically for Q and S (JL 260729; the row was labelled "Why this matters" until JL renamed it on 260801, and before 260729 a Q put it in the first section of Content).
An S page's Opening also holds the whole `## Stage Contract`, which is the stage's ONE contract section (JL 260801 retired `### Stage Record`; a legacy one still under Content is lifted into the contract as its opening lines), and **all of those lines are folded by default** (JL 260725: only the question sentence stays on stage), so Stage Contract no longer occupies a section of its own.
The rest of an S's Content still lives in `📚 Content`, and the section title shows the stage name (`📚 Content · Main 7 §6 Results`) instead of counting subsections; a Q's explicit Content is optional and its title still shows the count.
That title is derived from `# Short title`, so when the artifact's own numbering does not line up with the board's index, write the title as `S Main 7 · §6 Results`, putting both numbers on display.
**An S's `## Content` holds only what this stage itself produces** (JL 260725): Required Inputs and Venue belong in `## Stage Contract`; prose rules belong in `## Writing Style`; a correction already decided belongs in `## States`; and the intended outcome belongs in `## Aims`.
A new board writes `## Opening`. The `## Question` written by old boards still PARSES, so no old page breaks, but it is retired: `check.py` reports it as `retired-section` and a page being worked on should be renamed.

**One layout, two workflows:**

- `Q*.md` = decision.
  Only after every Aim is met or explicitly held may it be `✅ SETTLED`.
- `S*.md` = lifecycle stage.
  `## Content` is the stage substance (required on S); former Q-consumer questions become recognizable Aims inside `## Aims`; stage closes only at its human gate, which is to say that an S's `✅` means the gate passed, and the index counts by family on that basis.
- An S's `## Stage Contract` is not part of Content.
  It carries the acceptance conditions of the explicit `requires` upstreams and the Venue references from `style-from`; `stage.py` writes the managed part and the author owns `### Provides`.
  The prose rules resolved from `style-from` are materialized in the page's own `## Writing Style`, inside a separate managed block.
  The order of Pages is never dependency inference.
- Both page kinds **share the same four machine states**, decided by the first emoji of `state:`: a new page is always 🔴, 🟡 is in progress, ⏸️ is an explicit hold, and the evidence for ✅ is whichever of the two rules above applies.
  A readable note may follow the emoji, for example `✅ SETTLED`, `✅ PINNED · MISQ 2026`, `🟡 rendered · awaiting gate`; these are not a fifth state.
  The first emoji may never be omitted or replaced, and the note after it may never change its meaning.
- A Q-consumer Aim reaches ✅ only after the answer landed, was interpreted, and was woven into Content.
  A deferred Aim closes only after its forward pointer is recorded.
- `## States` summarizes the actual stage state through one current State per Aim.
  It does not copy every consumer answer.

Inside `## Files`, `### 🔗 Related Board Pages` is the checked, selective context map for another Page. Its rows declare relation + Page Phase + Page id + `page`/`§n` scope + Board-root-relative source path. `haipipe-board-page` owns the row contract; `cli/pagecontext.py` materializes only the current phase's rows, one hop, and `cli/check.py` rejects malformed or dead references. This is Page context, not configuration inheritance and not inferred stage order.

Long content in the prose is always written as **`- heading` plus a two-space-indented explanation**, never as one loose sentence after another.
A whole line in bold `**…**` is a **group title** (it leads a run of items).

**Every page's `## Content` structure is its own** (JL 260729): the names of the divisions, their numbering, and how many there are is decided by that page's own topic, and the manuscript form numbered with `§` is only the default look, not a requirement.
There are only two mechanical constraints, and they never change: `###` is a division that can be folded on its own, and `####` is one paragraph inside it, always at that level.
A page folds one level only: one level deeper and the whole section is squashed into a single box.
A division is written only when it really has content of its own: a flat section writes one `### §1 Introduction` leading its paragraphs, and a section that has subsections starts straight at `### §6.1`.
The benefit is that you can verify it without reading the prose: the number of `###` headings carrying a dot is the number of subsections.
`####` **carries no icon**: 🔹 belongs to group titles, so do not write `**…**` as a paragraph title.
A whole line of `(…)` immediately after a `####` is that paragraph's job, kept on stage in grey italic as a scan hook.
Add a question by copying `ref/page-template.md` (every section is marked required or optional); the full syntax table is in `ref/board-form.md`.

> Old section names are all still recognized: `## Done when` / `## Items to Finish` = `## Aims`; `## State` / `## Now` / `## Where we are` = `## States`; the Chinese names likewise.
> `## Why here` is retired: its job merged into `## Opening`'s explanation paragraph and renders into Content.
> An old section still written on an old board is still collected into the fold at the bottom.

## ✍️ Writing (the part most often skipped)

**"If it is not easy to read, writing that much of it is all rubbish."**
See `ref/writing-rules.md`; the three deadliest:

1. **No coined words**: every term is either the source document's own wording, or it is explained in `## Glossary`.
2. **Stale statements must be cleared out**: once the board changes, an old statement in the prose is a self-contradiction, and a zero-background reader picks it out at first glance.
3. **After editing, cold-read it with a brand-new agent**: call `haipipe-board-reviewer-agent`.
   It runs `check.py` read-only, cold-reads against `ref/writing-rules.md`, and reports stale or contradictory statements, and it never edits on the author's behalf.
   Reading it yourself in the same conversation tests nothing, because you know far too much that was never written down.
   When more than one Opening changed, the same fresh review also reads those
   Openings consecutively in Board order and rejects repeated scaffolds or
   subject-swappable prose.

The page's `✅ Quality Check` is the quick iteration surface for the same contract.
It reads `haipipe-board-page`, resolves base, variant, page-local, Stage Contract, division, and paragraph-job requirements, then returns one evidence-bearing verdict per review unit.
It is read-only and never substitutes for the fresh reviewer at the final gate.

## 🚫 Never do this

- Hand-edit anything under the generated `board/` tree
- Give a board a new date
- Delete a `> Comment WHO` line (or a legacy `> JL:` one) or a `> ✎` line under a sentence (they are that sentence's comment and edit record)
- Make a page depend on JS to be readable: scripts may only enhance it.
  **The invariant: delete every `<script>` in the page and every question and all of the prose is still there.**
  `build.py` asserts this on every build.

## 📖 The board ↔ SKILL.md: how they stay in sync

This SKILL.md was not written out of thin air: it is **the crystallization of the settled questions** on a board (this skill's own `diagram/01-boardform-260722/`).

**Skill and board side by side**: what each holds, and where they meet.

```
   that board (each question: Opening/Aims/States/Law/Lesson/Log)  SKILL.md
   ┌─────────────────────────────────────────┐ a question ✅ ┌─────────────────────┐
   │ the full design record: why, how it got │ ──────────►   │ conclusions only,   │
   │ here, and what is still undecided       │               │ just follow them    │
   └─────────────────────────────────────────┘               └─────────────────────┘
        the working record (includes 🟡/🔴)          the distillation of what is settled
```

**The graduation mechanism**: the moment a Q reaches `✅ SETTLED`, copy the rules from its `## Law` into the matching place in the manual.
Operating rules go into SKILL.md's prose, and **specifications** such as display or syntax go into `ref/` (SKILL.md stays as short as possible, QB1's Law).

- An unsettled question (🟡/🔴) does **not** enter the manual, so that something written off the cuff never becomes iron law.
  (This really happened: `QD1`'s permission rule was first written off the cuff as "may only change this one file", and JL later overturned it into "the same as the CLI".)
- So SKILL.md always equals **the sum of the settled rules**, no more and no less.
  Before changing it, check whether that question is `✅`.
- Graduated so far: `QAa0` (Q and S share one source template → `ref/page-template.md`, formerly QA2, merged 260729; formerly QA4: Q and S share one page layout → `ref/board-form.md §8`, and display specifications are not stuffed in here) · `QA6` (comments land on disk) · `QA1` (where a board lives, formerly QC1, merged 260729) · `QC3` (a Q may live in its own folder) · `QB5` (the Python split per page into `src/`; note the SENTENCE page is also QB5 on the design board, whose five faces folded into it on 260802).
- The live layer's chat and terminal (`QD1`/`QD2`/`QD3`) are still 🟡, so only pointers to them are given above, never rules.
  The embed syntax (formerly `QF1`) is settled into `ref/board-form.md §5`; the QF1 page itself retired on 260725, see the note on the board's QF group.

## 📚 ref/

| File | What you read it for |
|---|---|
| `ref/page-template.md` | The file a Q or S page is copied from (renamed from `ref/q-template.md` on 260801). A Skill, Agent or Meeting page is generated from its own stub instead and never copies this |
| `ref/board-form.md` | The full specification: folders, numbering, section ↔ page correspondence, the syntax table, `## Links` |
| `ref/writing-rules.md` | How to write it in plain language, plus the zero-background review prompt and its convergence criteria |
| `ref/topic-entry-contract.md` | Optional generic contract for a topic page and its nested `probes/<topic>/` entry records (hidden `<n>-<slug>.md` source files, not pages) |
| `ref/board-example.md` | A minimal example board with two questions |
| `ref/page-lifecycle.workflow.js` | Bounded non-linear controller for one Page: producer → build/version snapshot → independent CHECK → route |

The scripts and packages in the skill root:

| File | What it does |
|---|---|
| **`cli/`** | **Every runnable script lives here (JL 260801: a skill folder should not open onto a pile of `.py`).** The top level is now `SKILL.md`, `CHANGELOG.md`, `status.py`, and folders. Each script sets `HERE` to the ENGINE dir (`__file__.parent.parent`), so `HERE / "ref"` and `HERE / "cli" / "build.py"` still mean what they always did |
| `cli/build.py` | Read the Board Markdown and generate the canonical `board/` site; standard library only |
| `cli/watch.py` | Watch the board folder and re-run `build.py` on any `.md` change |
| `cli/check.py` | The structural self-check (the machine half of `QA9`): sections, state, references, the rendered html, template coverage |
| `cli/pagecontext.py` | Materialize one Page Phase's typed Related Board Page scopes, one hop only |
| `cli/pageflow.py` | Audit one serialized Page RUN for legal routes, round changes, role separation, immutable CHECK versions, human gates, and terminal stops |
| `cli/serve.py` | The live server, 496 lines: argument parsing, the request router, and the shared setup; everything with a feature in it now lives in `live/` |
| `live/base.py` | 260 lines: the shared request base the other live modules mix in |
| `live/structure.py` | 270 lines: `structure_op`, behind `POST /_board/structure` (＋Q / ＋Group / 🗄) |
| `live/write.py` | 426 lines: the sentence write path, the comment and edit writes under an anchor sentence |
| `live/xcal.py` | 468 lines: `serve_frame()`, the `assets/xcal-boot.js` injection, and the image pointer ↔ dataURL restore |
| `live/activity.py` | 446 lines: focus-time spans and the aggregates behind the Activity component |
| `live/chat.py` | 1332 lines: the chat drawer, its sessions, and the `claude_agent_sdk` turn |
| `live/term.py` | 857 lines: the `/_term/` PTY, parking, and reattachment |
| `src/` | The build and audit code split by topic, including `page_context.py` for checked scoped Page reads and `page_lifecycle.py` for deterministic RUN receipt validation; `build.py` and `serve.py` stay thin entries (QB5) |
| `cli/stage.py` | Explicitly create and sync an S page's inherited requirements, Venue links, and page Writing Style inheritance |
| `cli/skillpage.py` | One skill folder → one `Skill-<n>-<slug>` page (`new` / `sync` / `check`); the same split as `stage.py`, the derived header only, never the authored sections |
| `status.py` | Derive the visible session status strip at the end of every reply from Board, page group, and page; read-only, writes no state file. **The one script still at the top level, deliberately**: the reply-footer automation invokes it by absolute path, so moving it into `cli/` would silently break every board attachment |
| `cli/regroup.py` | Move a board's root pages into one named folder per group; a dry run without `--apply` |
| `cli/refs.py` | Render a paper's real bibliography once into a cache the board can read; it is a separate command because running BibTeX writes |
| `cli/xcal.py` | One `fig/board.excalidraw` per board, one frame per question; `--wire` writes each URL back into that question |
| `cli/gate_live.py` | The response-identical gate for a live-layer refactor: record every response and every file for one fixed request script before and after, then diff them; a clean diff means the move was mechanical |
| `assets/board-mark.svg` | The Board's shared SVG mark; inlined into the title at build time and reused as the favicon |
| `assets/css/`, `assets/js/` | The page's real CSS and JS parts, assembled by `build.py` into `board/_assets/board.css` and `board/_assets/board.js` |
| `assets/xcal-boot.js` | The script `live/xcal.py` injects into the proxied Excalidraw so that drawings save back to the repository |
| `tests/` | The skill's own tests, including Page lifecycle happy paths, branch routes, and fault injection; `tests/conftest.py` puts the engine dir on `sys.path` |

The independent judge: `../agents/haipipe-board-reviewer-agent.md`.
It has no write tools; after the author has fixed things, start another new reviewer.
The bounded non-interactive runner: `../agents/haipipe-board-page-orchestrator-agent.md`.
It stores the Workflow result under `_runs/page/` and calls `cli/pageflow.py`; it never edits Page prose.

A live example: `Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/`, this skill's own board (the flat form).
A live example of the nested form (Q decisions + S stages): `examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle/`.
