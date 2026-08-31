---
name: haipipe-board
description: >-
  Open and run a BOARD: one topic, one markdown page per decision (Q) or
  lifecycle stage (S), built into a browsable board/ site. Use to lay out and
  close a topic's open questions, or to share work with colleagues. Open
  BOARD_FOLDER means VIEW an existing board by rebuilding it and pushing
  board/index.html to VS Code, not create one. Trigger: board, open a board,
  add a question, close the board, 开板, 加一题, 关板, /haipipe-board.
metadata:
  version: "0.153.0"
  last_updated: "2026-08-31"
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

## 👪 The family: one door, one Page base, four contract catalogs

This skill is the DOOR: you invoke it to run a board.
The rest of this board family (`../`) is what other agents LOAD or CALL without opening the door, and this skill routes to them rather than restating them:

**The board's sub-skills**: which altitude each one works at.

```
haipipe-page       SPEC + ROUTER · the shared Page frame and the
                         Page Type × Page Phase composition
page-types/              the ONE variant this skill set owns; the others
                         live in the skill set that owns them (see below)
  haipipe-page-for-stage
                         TYPE · S-<Family>-<unit> lifecycle pages
page-workflows/
  haipipe-page-workflow
                         HEAD · the RUN router and its packet + receipt contract
  haipipe-page-draft
  haipipe-page-evidence
  haipipe-page-revise
  haipipe-page-check
                         PHASES · promise, inquiry, realization, judgment
haipipe-plugin     SPEC · every subfolder of a page's folder is a plugin:
                         storage · surface · writer · boundary; the roster in
                         its ref/roster.md is the single list of names
page-plugins/            the NINE per-plugin skills, each delta-only over that
                         contract: draw · slide · chat · latex · word · bibex ·
                         display · probe · skill (meeting · logging · _fixture
                         join when their rows go live)
ref/topic-entry-contract.md
                         LEGACY CHECKER COMPATIBILITY ONLY · validates archived
                         route/E-division Pages; current Page work uses pagex/
                         for existing Pages and Page-local probe/ for Task or
                         Discovery evidence. Never load it as a current contract.
haipipe-sentence   DOOR + SPEC · one sentence: comment, edit, card;
                         lanes, addresses, the archive-never-delete lifecycle
haipipe-board-routing    VERB · every write onto a board, at BOTH altitudes:
                         board.md's structure (propose · materialize · lanes ·
                         regroup) and one input → owning page → anchored write;
                         proposes, never creates; closes only answered rows
haipipe-page-creator-agent    AGENT · writes ONE page in a fresh context;
                         designed to fan out N of them, keep every shared write here
haipipe-board-reviewer-agent   AGENT · the read-only fresh-context reviewer
haipipe-page-auditor-agent
                         AGENT · runs one bounded Page loop, stores and audits
                         the receipt, never writes Page prose
```

`haipipe-board-index` was retired on 260802 (JL: "maybe merge, I will do B") and its whole altitude, including `lanes.py`, lives in `haipipe-board-routing`.
Three of its five verbs were other units' work written a second time, and the merge gave a group-altitude finding somewhere to land, which it had never had.
The `open` action below still describes proposing and materializing a board, on purpose: a person opening their first board should not have to load a second skill, and the two descriptions are corrected together.

The specs cite this skill's `ref/` files as their authority and never fork them; the verbs load the specs.
`haipipe-board-digest` (a transcript fanned out through routing) is named on the roster and not yet shipped.
For a batch of page creations or Opening revisions, the caller dispatches
exactly one fresh `haipipe-page-creator-agent` per page. Waves are allowed when
concurrency is limited, but one writer never owns two pages in the batch. The
assignment packet carries page facts, paths, sources, and ownership context,
not a copied prose checklist: every creator loads `haipipe-page` itself.
An existing Opening uses the creator's `revise-opening` operation, which reads
the target page completely and edits only that section. The caller alone owns
shared writes, one rebuild, and one mechanical check after all pages land.
Writer self-checks are local evidence, never approval. A fresh
`haipipe-board-reviewer-agent` then judges each changed page and reads all
changed Openings consecutively in Board order; interchangeable or form-letter
prose fails even when every page is locally clear.
For an automatic one-Page lifecycle, dispatch
`haipipe-page-auditor-agent` instead. It invokes the Page Workflow,
which calls the same creator for exactly one DRAFT, EVIDENCE, or REVISE authority,
then a mechanical builder/version snapshot, then the reviewer for CHECK. The
orchestrator stores the exact result under `_runs/page/` and audits it; it never
writes Page prose, and the reviewer never cures its own finding.
**A Page Type variant ships in the folder of the SKILL SET THAT OWNS IT (JL 260809; paper amended JL 260831).**
Most skill sets carry a `page-types/` folder, so the folder a variant sits in is what names its owner.
Paper is the exception: its types are 1:1 with journey phases, so they ship as six phase skills under `paper/workflow-phases/` (each still owning its `page-type:` key) plus the non-phase `paper/haipipe-paper-venue/`.
The live inventory with owners and counts is `cli/pagetypes.py` output, never a prose count.
(`for-slide` retired 260815: a deck is `slide/` plugin material, written by `/_board/autodeck` under the `haipipe-plugin` contract.)

```
board/page-types/         for-stage
paper/workflow-phases/    haipipe-paper-ideation · -seed · -roadmap ·
                          -narrative · -section · -round
paper/                    haipipe-paper-venue (library lane, not a phase)
task/page-types/          for-task
application/page-types/   for-brief · for-insight · for-intervention · for-artifact
subjective-label/…/       for-labeling
```

Application's names are intentionally unique across the global resolver: Brief does not reuse Paper Seed, and the user-facing Design Page retains the machine key `intervention` rather than colliding with another family's vocabulary.
`for-stage` stays here although only paper and legacy application runtimes have lifecycles, because a stage page is a BOARD mechanism (the chain, the managed contract span, the human gate) that more than one family can instantiate.
The five that left describe a paper's own artifacts, so they belong to the paper.
Two earlier rules failed here and are recorded so neither returns: "ships under its CONSUMER, never here" broke when venue pages turned out to be consumed by the paper family and maintained by this one, and "ships WHERE THE BOARD FAMILY MAINTAINS IT" (JL 260803) held only while one family owned every variant.
⚠️ Moving a variant does not move its installed symlink: re-run `install.sh --global` (repo root) afterwards, or the skill silently stops resolving.

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
  1-QA-<group-title-slug>/    ← one group, one folder (the default, JL 260726)
                              the 1- is its place in ## Pages (JL 260816)
    draw/group.excalidraw     the group's own scene + import manifest
    QA1-<slug>/               ← one page, one FOLDER it owns (JL 260815)
      QA1-<slug>.md           the page, the only discoverable file inside
      draw/ slide/ latex/ …   its plugins; every subfolder is one, and
                              haipipe-plugin owns the roster and the law
  2-QB-<group-title-slug>/
    S-Seed-0-<slug>/          a named lifecycle page (only with a lifecycle)
    Design-1-<slug>/          a unit design page, its unit's bytes in skill/
                              (the Skill-/Agent- mirror kinds retired 260815)
  board/                      ← generated by build.py, never hand-edit
    index.html                Board-Webpage-Index
    QA.html                   one Board-Webpage-Group
    QA/QA1-<slug>.html        one Board-Webpage-Page per source page
    _assets/board.css         one shared assembled stylesheet
    _assets/board.js          one shared assembled script
  fig/
```

The descriptive source folder (`1-QA-<group-title-slug>/`) and the compact generated route (`board/QA`) are deliberately different. The source folder explains itself on disk; the generated token keeps page URLs short and stable. The number belongs to the source folder only and is stripped before anything reads the letter.

- **The group folder is the default (JL ruled 260726).**
  From the first page onward, one group gets one folder, named `<N>-Q<group-letter>-<group-title-slug>` (`1-QA-defining-a-board/`), **never a bare `QA/`**.
  Writing only `QA/` just copies the id a second time; the half a reader cannot recognize is precisely the title half.
- **The number is the group's place in `## Pages` (JL ruled 260816).**
  Letters carry identity and cannot carry order: on the board that found this, `QC-engine/` sorted four rows above `QPs-page-structure/` while board.md read them the other way round, and a folder listing that contradicts the board it stores is one nobody trusts.
  `## Pages` stays the only authority on order and the number is DERIVED from it, so you change the order by moving a `###` block and then renaming the folder, never the reverse.
  `check.py` reports `group-number-order` when the two disagree, `group-number-missing` when only some folders carry a number, and one `groups-not-numbered` WARN for a board still on the pre-260816 shape.
  A board is numbered or it is not: `regroup.py` always numbers because it lays the whole set down at once, and ＋Q opening one new group follows whatever the board already does.
  A paper's `0-lifecycle/` is untouched by all of this — `0-seed/ 1-work/` are SUBJECT folders whose numbers carry lifecycle order, and the check only looks at folders whose name, minus the number, starts with a `Q<letter>` board.md declares.
  Membership has looked only at the path, not at a registry, since 260722, so moving pages into folders is a plain `mv`: `## Pages` still writes bare filenames only, board.md needs not one word changed, and the render is identical except for the path attribute used for write-back (verified across 30 pages).
  The ＋Q on the page writes into the folder its group already lives in; a newly opened group gets a named folder opened by its first page.
  To move a whole existing board: `python3 <skill>/cli/regroup.py <board-folder> --apply` (omit `--apply` for a dry run).
  To give every page on that board its own folder afterwards: `python3 <skill>/cli/refold.py <board-folder> --apply` (same dry run by default).
  The two are one migration in two steps, and each has its own command because they answer different questions: `regroup` decides which GROUP a page belongs to, `refold` gives the page a home of its own so its plugins have somewhere to live.
  `refold` moves the plugin material in with its page — the group had been holding it keyed by page name, `display/<page name>/` and `draw/<id>.excalidraw` — and preserves the inner path rather than flattening it, because a display unit is addressed by its own folder name and a QA-probe record names its page by the drawer it sits in.
  It then re-anchors every path that RESOLVES today, from the file or from the board root, and leaves an already-dead path exactly as it is: guessing at what a dead path meant is how it becomes a plausible wrong one.
  Run it against a copy first if the board is large; on the 73-page paper board it moved 83 things and rewrote 49 files.
  **⚠️ Run `check.py` once after moving.**
  `## Pages` writing bare filenames is unaffected, but `## Links` writes real paths, and any that point across boards into someone else's page will break (moving 154 pages on 260726 broke 17 links; all were fixed).
  **Never re-fold a board that is already sorted into folders**, for example a paper's `0-lifecycle/`: `0-seed/ 1-work/ 3-display/` is already both a subject folder and an S family, so it already satisfies this rule, and the numbering additionally carries lifecycle order.

- **Owning unit** = whoever this board serves.
  Task, project, and paper boards default into their own `diagram/`; boards used to design a skill inside the same plugin collect in that plugin's `skills/diagrams` folder.
  Both locations keep the board separate from the skill it describes: the board is a work product, the skill is the deliverable package.
- **NN only orders within the same topic series; it is never a global counter.**
  A new topic starts at `01`; only a later board on the same topic uses `02`.
  So the shared `skills/diagrams` folder can hold several different topics all starting their own `01-*`.
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

**Direct Board session:** end every user-visible reply with the exact Markdown block emitted by `status.py`; put no prose after it.
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

Then resolve the Board's **surrounding operating context** before changing it:

1. Read the Board folder's parent unit and the repository root, not only the one `board.md` file.
2. If the repository root contains `.server_config/`, make it the **primary hosting configuration**. Read `.server_config/README.md` for the shareable protocol and `.server_config/settings.env` only for non-secret `JJLUO_*` startup values such as bind host, port, public URL, SPACE name, and auth-file path. `serve.py` and `status.py` use these values when their corresponding CLI flags are omitted. Never print credential contents or edit `settings.env` implicitly.
3. Look for the shared SPACE registry at `spaces/registry.yaml` from a Tools root or `Tools/spaces/registry.yaml` from a SPACE root. The registry enumerates the neighboring `*-SPACE` repositories and identifies the one that owns the Board; it supplies ownership and fallback context and does not override an existing root `.server_config`.
4. When the Board is inside a registered SPACE but has no root `.server_config/`, read that SPACE's public configuration page, `<SPACE>/.server_config/README.md`. Machine-local values may also exist beside it in `settings.env`; never print, copy, or edit that local file unless the user explicitly asks for a machine setting.
5. If no registry entry matches the Board's repository root, say that it is an unmounted/local Board. Never infer an owner from a similar folder name.

This surrounding-folder read is bounded: the Board's parent unit, repository root, SPACE registry, and matched configuration page are context; recursively inventorying unrelated sibling projects is not.

There are **two registries with different jobs**. `board.md ## Pages` is the only registry of Pages on one Board. `spaces/registry.yaml` is the registry of SPACE ownership, domains, roots, ports, and configuration pages. The Board Home still discovers Boards by walking the owning SPACE for `board.md`; never add a hand-maintained Board list to the SPACE registry.

**Configuration sync is same-round, but only when the fact changed.** A change to a SPACE id/name, root, domain, port, public URL, short route, mount, or discovery policy updates the shared registry and the matched `.server_config/README.md` in the same round. A Page title, Page prose, or ordinary Board decision does not mutate SPACE configuration. When the corresponding configuration page is outside the writable repository, report the exact companion edit instead of silently pretending it landed.

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

Its complete shape is deliberately three lines, FOUR when the focus is one page:

**The closing block**: the three lines every reply ends on.

```markdown
🧭 BOARD · QUEUE/FOCUS (deep-link)
✅ done · implementation
⏱️ 📮 PROBE · 🧭✅ 📮⏳ 🃏⬜ ✏️⬜ 🖊⬜ 🔍⬜ · ✋4   ← page focus only
→ one concrete next action
```

**The ⏱️ row, and why it exists** (JL 260820: "how to update this so I know
which phase of the page I am in?"). `🔥 working` says a session is busy and
never says WHERE in the ①-⑦ page workflow the page sits, so a page-focused
strip adds one row: the phase whose exit test fails first, then all six as a
bar, then the human ticks still owed. Each phase carries its OWN emoji from
haipipe-page-workflow §🔁 (🧭 outline · 📮 probe · 🃏 evidence · ✏️ draft ·
🖊 revise · 🔍 check), because circled digits render at a few pixels in a
terminal font and JL could not read them (260820). CHECK is the one
substitution: §🔁 draws it as ✅, which is also the DONE marker, so a bar
pairing them would read `✅✅`. It is computed from disk by
`src/page_phase.py`, the same module `cli/pagephase.py` prints in full, so the
one-row and full forms cannot drift. A board- or group-focused strip keeps
three rows: a phase belongs to ONE page, and averaged over a group it means
nothing.

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

Offline (needs `cli/build.py`, plus `cli/stage.py` for `stage`): **preview · view · open · add · stage · build · sync · link · close**
Live (needs `cli/serve.py` running): **serve · excalidraw · comment**
Routed to `haipipe-page`: **create a page · update a page · run one page lifecycle**
Routed to `haipipe-sentence`: **comment · edit · card**

That is 12 verbs here, plus six routed actions this skill does not run itself.

`preview` answers "what does this say" at every altitude with one tool,
`cli/preview.py <path>`, which resolves the grain from the path itself: a
board folder prints spine + Topic + one roster line per page (id, type,
state tally, title); a group folder prints its pages' roster lines; a page
prints the full page preview (`haipipe-page` owns that grain's contract).
It reads and never writes, and it is a gist, never a substitute for the
read a verb owes.

**One door** (JL 260802: "you can just say, haipipe-board update the page etc, it will route to the haipipe-page"). Anything about ONE PAGE routes to `haipipe-page`, which owns the page contract and drives that page end to end:

```
🚪 say it here                                    ▸ runs there
──────────────────────────────────────────────────────────────────
"create a new page on <topic>"                    ▸ haipipe-page
"update / fix / work on <page>"                   ▸ haipipe-page
"bring <page> up to the standard"                 ▸ haipipe-page
"why does <page> fail the checker"                ▸ haipipe-page
"run / audit the lifecycle of <page>"             ▸ haipipe-page

"attach / edit a drawing on <page>"                ▸ haipipe-plugin-draw
"compile <page> to pdf / rebuild the tex"         ▸ haipipe-plugin-latex

"comment on / edit <sentence>"                    ▸ haipipe-sentence
"put a card on <these words>"                     ▸ haipipe-sentence
"what may attach to a sentence"                   ▸ haipipe-sentence

anything about the BOARD: its groups, roster,     ▸ here
index, serving, the round trip
```

Route by SCOPE at every altitude: one sentence is the sentence skill's, one page is the page skill's, the board and its structure are this skill's.

Inside the one-Page route, `haipipe-page` resolves the stable Page Type and the current DRAFT, EVIDENCE, REVISE, or CHECK authority.
The one-Page contract now owns `RUN`, backed by `ref/page-lifecycle.workflow.js`.
It is not `ADVANCE`: the router may repeat, branch, HOLD, or begin a new DRAFT round.
The non-interactive dispatch target is `haipipe-page-auditor-agent`; the Board door still owns no separate phase verb.

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
ROOT=<repo root>
BD=<board folder path relative to the repo root>   # e.g. Tools/plugins/.../diagram/01-boardform-260722
BOARD_BASE_URL=""
if [ -f "$ROOT/.server_config/settings.env" ]; then
  BOARD_BASE_URL="$(sed -nE 's/^[[:space:]]*(export[[:space:]]+)?JJLUO_PUBLIC_URL[[:space:]]*=[[:space:]]*([^[:space:]#]+).*$/\2/p' "$ROOT/.server_config/settings.env" | tail -1 | sed -e 's/^"//' -e 's/"$//' -e "s/^'//" -e "s/'$//")"
  BOARD_BASE_URL="${BOARD_BASE_URL:-$(sed -nE 's/^[[:space:]]*(export[[:space:]]+)?JJLUO_TAILSCALE_URL[[:space:]]*=[[:space:]]*([^[:space:]#]+).*$/\2/p' "$ROOT/.server_config/settings.env" | tail -1 | sed -e 's/^"//' -e 's/"$//' -e "s/^'//" -e "s/'$//")}"
fi
BOARD_BASE_URL="${BOARD_BASE_URL:-${HAIPIPE_BOARD_URL:-$(sed -n 's/^[[:space:]]*export[[:space:]]*HAIPIPE_BOARD_URL=//p' "$ROOT/env.sh" | tail -1)}}"
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

`BOARD_BASE_URL` and the `status.py` at the end of every reply use the same reader-facing setting: an explicit CLI value wins, then `JJLUO_PUBLIC_URL` (or `JJLUO_TAILSCALE_URL`) in the repository root's `.server_config/settings.env`, then the current environment's `HAIPIPE_BOARD_URL`, then the one item read from the repo root `env.sh`, and only then the fallback `http://127.0.0.1:5599`. The root `.server_config` is the source of truth for the host, port, public URL, and auth-file path when startup flags are omitted.
Never write one machine's Tailscale IP into shared skill source.

This needs `serve.py` running on the configured port (or 5599 when no root `.server_config/settings.env` is present; start it first if it is not, see the serve section).
`#top` returns to the index, `#QA6` jumps straight to one question, `#all` expands everything.

### open · start a **new** board

1. Ask three things: **what this board has to solve** (→ `spine`), **when it counts as finished** (→ `close`), and **which pages there are** (how many Q decisions, plus how many S stages when there is a lifecycle).
   That page list needs the user's explicit OK before you go any further: this is the only place where you must stop and ask.
2. Pick a location and create the folder: task, project, and paper use `<owning-unit>/diagram/<NN>-<topic>-<YYMMDD>/`; a plugin skill-design Board uses `<plugin>/skills/diagrams/<NN>-<topic>-<YYMMDD>`.
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

4b. A `Skill-`, `Agent-` or `Meeting-` page is GENERATED, never copied. `cli/skillpage.py new` writes the first two from its own stub and `cli/meetingpage.py` writes the third, and each registers the page in `board.md` itself. Copying `ref/page-template.md` for one of these produces a page with no managed spans, which `skillpage.py check` then reports as `no managed block` forever. These filename kinds use the base Page plus their Skill or Meeting plugin; they are not Page Types.
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
.venv/bin/python <skill>/cli/serve.py --root <repo root>
```

When the repository root has `.server_config/settings.env`, this command uses its `JJLUO_BIND_HOST` or `JJLUO_TAILSCALE_ADDRESS`, `JJLUO_LOCAL_PORT` or `JJLUO_TAILSCALE_PORT`, `JJLUO_SPACE_NAME`, `JJLUO_PUBLIC_URL` (or `JJLUO_TAILSCALE_URL`), and `JJLUO_AUTH_FILE`. An explicit CLI flag wins over the matching config value; without a config file, the listener falls back to loopback on port 5599.
The Board may be protected with the configured auth file. A non-loopback listener normally requires authentication because `/_term/` is a real shell; `serve.py --no-auth` is an explicit exception for a trusted private network such as Tailscale, and exposes that shell to every reachable device. Keep credentials in the ignored machine-local config and never commit them.

Once it is running, the board is not only readable: **comments land directly on disk**, and every page's plugin surfaces come alive in the right pane, the tab rail leading with 📂 Folder.
⚖️ One question, one session · one session, one window · N questions, N terminals.
The chat forms are `haipipe-plugin-chat`'s to state and the canvas is `haipipe-plugin-draw`'s; the door only starts the server they ride on.

> The SDK chat version (`QD2`) and the TUI chat version, a real CLI (`QD3`), are **still taking shape in the QD group**, and the terminal's form on a phone or a desktop is `QD4`.
> They are not restricted versus unrestricted: `QD2` carries three permission tiers and defaults to the full one, so the split is a difference of FORM, a rebuilt chat box against the CLI itself.
> Treat those questions as the authority on how they are used, and do not take them as fixed rules (see "the board ↔ SKILL.md" at the end).

### excalidraw · anything about ONE PAGE'S DRAWING (routed)

Routed to `haipipe-plugin-draw` (page-plugins/), which owns the draw plugin whole: one scene per owner, the ownership rule, the two group-editor modes, and the split/sync/compose/verify commands.
The engine files stay here (`cli/draw.py`, `live/xcal.py`); the contract lives there.
Same routing for every material plugin: slide, chat, latex, word, bibex, probe, skill, and display each own a `haipipe-plugin-<name>` under `page-plugins/`, delta-only over `haipipe-plugin`; the roster in `haipipe-plugin/ref/roster.md` stays the single list.
The 📂 Folder tab (the rail's first, folded pages only) is `haipipe-plugin-folder`'s — the meta-surface over the folder itself, with no subfolder and no roster row.

### comment / edit / card · anything about ONE SENTENCE (routed)

Routed to `haipipe-sentence`, which owns the sentence contract and its three verbs the way `haipipe-page` owns the page. Say it here and it runs there:

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
| `## States` | ⛔ RETIRED 260819, merged into `## Aims`; a page that still carries one is reported `retired-section`. One Aim row now carries its tick, its `Done when:` test AND its `Now:` fact. |
| `## Log` | ⛔ Moved 260830 to `outline/<stem>-log.md` (`haipipe-plugin-outline` 0.16.1). Still `YYMMDD HHMM · what changed`, still 15-35 words, newest-first; only its home changed. The page's `## Files` keeps one row pointing at it. |
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

## 📐 One page (routed)

A page's whole anatomy — the metadata head, the fixed on-stage order Opening → Diagram → Content → Aims → States, Files, and the folded tail — is `haipipe-page`'s to state, with the kinds in each owner's variant folder (`page-types/`, or paper's `workflow-phases/`) and the workflow under `page-workflows/`.
The door keeps only the two facts its own verbs depend on:

- A NEW page is always `state: 🔴 OPEN`, and the first emoji of `state:` is the machine state (✅ · 🟡 · 🔴 · ⏸️ · 🗂 FOLDED); a readable note may follow, never replacing it.
- A Q closes when every Aim is met or explicitly held; an S closes only at its human gate, and the index counts S pages per family on that basis.

Old section names keep parsing forever (`## Question`, `## Done when`, `## Where we are`, the Chinese names); `check.py` reports retired ones on pages being worked.

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
It reads `haipipe-page`, resolves base, variant, page-local, Stage Contract, division, and paragraph-job requirements, then returns one evidence-bearing verdict per review unit.
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
| `ref/topic-entry-contract.md` | Optional generic contract for an evidence page (head `route:` key, `### E<n>` divisions, E0 queue) and its nested `probes/<topic>/` QA-probe records (hidden `<n>-<slug>.md` source files, not pages) |
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
| `live/xcal.py` | Serve both legacy scenes and linked Group/Page sources; compose Group views, enforce one save owner, externalize owner-scoped assets, and reject stale revisions |
| `live/activity.py` | 446 lines: focus-time spans and the aggregates behind the Activity component |
| `live/chat.py` | 1332 lines: the chat drawer, its sessions, and the `claude_agent_sdk` turn |
| `live/term.py` | 857 lines: the `/_term/` PTY, parking, and reattachment |
| `src/` | The build and audit code split by topic, including `page_context.py` for checked scoped Page reads, `page_lifecycle.py` for deterministic RUN receipt validation, and `server_config.py` for safe root `.server_config/settings.env` reads; `build.py` and `serve.py` stay thin entries (QB5) |
| `cli/stage.py` | Explicitly create and sync an S page's inherited requirements, Venue links, and page Writing Style inheritance |
| `cli/skillpage.py` | One skill folder → one `Skill-<n>-<slug>` page (`new` / `sync` / `check`); the same split as `stage.py`, the derived header only, never the authored sections |
| `status.py` | Derive the visible session status strip at the end of every reply from Board, page group, and page; read-only, writes no state file. **The one script still at the top level, deliberately**: the reply-footer automation invokes it by absolute path, so moving it into `cli/` would silently break every board attachment |
| `cli/regroup.py` | Move a board's root pages into one named folder per group; a dry run without `--apply` |
| `cli/refold.py` | Give every page its own folder (`<name>/<name>.md`, JL 260815), move the group's page-keyed plugin material in with it, and re-anchor every path that still resolves; a dry run without `--apply` |
| `cli/refs.py` | Render a paper's real bibliography once into a cache the board can read; it is a separate command because running BibTeX writes |
| `cli/draw.py` | Split a legacy scene into lowercase Group `draw/` folders without overwriting, add newly declared Pages with additive `sync`, compose linked Page sources with namespaced references, and verify an exact round trip |
| `cli/xcal.py` | Legacy one-scene seeder for old Boards; not the source contract for new linked drawing work |
| `cli/gate_live.py` | The response-identical gate for a live-layer refactor: record every response and every file for one fixed request script before and after, then diff them; a clean diff means the move was mechanical |
| `assets/board-mark.svg` | The Board's shared SVG mark; inlined into the title at build time and reused as the favicon |
| `assets/css/`, `assets/js/` | The page's real CSS and JS parts, assembled by `build.py` into the generated `board/` site's `_assets/board.css` and `_assets/board.js` |
| `assets/xcal-boot.js` | The script `live/xcal.py` injects into the proxied Excalidraw so that drawings save back to the repository |
| `checks/linked_drawings_browser.py` | Headless acceptance for Group layer, Arrange Instance, entering one Page source, and returning to the Group without writing a scene |
| `tests/` | The skill's own tests, including Page lifecycle happy paths, branch routes, and fault injection; `tests/conftest.py` puts the engine dir on `sys.path` |

The independent judge: `../agents/haipipe-board-reviewer-agent.md`.
It has no write tools; after the author has fixed things, start another new reviewer.
The bounded non-interactive runner: `../agents/haipipe-page-auditor-agent.md`.
It stores the Workflow result under `_runs/page/` and calls `cli/pageflow.py`; it never edits Page prose.

A live example: `Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/`, this skill's own board (the flat form).
A live example of the nested form (Q decisions + S stages): `examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle/`.
