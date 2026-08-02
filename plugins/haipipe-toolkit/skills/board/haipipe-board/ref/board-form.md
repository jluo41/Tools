# Board form: full specification

SKILL.md is the shortest operating instructions; this file is where you look up the details.

## 1. Folders

**Where a board folder lives**: the two homes, by who owns the board.

```
<owner-unit>/diagram/<NN>-<topic>-<YYMMDD>/       # task / project / paper
<plugin>/skills/diagrams/<NN>-<topic>-<YYMMDD>/   # plugin skill-design Board
  board.md                  global: title · spine · close · Topic · Pipeline
                            · optional Board Map · Board Structure · Pages
  QA-<group-title-slug>/    one folder per group (default, JL 260726)
    QA1-<slug>.md           one file per question
    QA2-<slug>.md
  QB-<group-title-slug>/
    QB1-<slug>.md
    S-Seed-0-<slug>.md      named lifecycle page (write only when a lifecycle exists)
  board/                    generated, do not hand-edit
    index.html              Board-Webpage-Index
    QA.html                 one page for the QA group
    QA/QA1-<slug>.html      one page for each QA source page
    _assets/board.css       one shared assembled stylesheet
    _assets/board.js        one shared assembled script
  fig/                      screenshots
```

- **owner-unit** = who this board serves.
  Boards for a task, project, or paper default to their own `diagram/`; boards inside a plugin used to design a skill collect under that plugin's `skills/diagrams/`.
  A board is a work artifact, a skill is a delivery package, and the two never share one folder.
- **NN** orders boards within the same topic series; it does not assign a unique number across the whole collection.
  A new topic starts at `01`; only later boards on the same topic use `02`.
  So a shared `skills/diagrams/` can hold several different topics' `01-*` at once.
- **YYMMDD** is **the day the board was opened**, and it never changes afterward.

**The folder question (QC3, JL 260724)**: a Q file can also live inside the very folder it discusses, so a board can sit directly on top of an existing tree (the first consumer: a paper's `0-lifecycle/`):

```
0-lifecycle/                    ← the whole folder IS the board
  board.md
  QA1-frontier.md               top-level questions as usual
  0-seed/S-Seed-0-seed.md       lifecycle page lives in its own folder
  4-display/QD2-d01-….md        a question living in its own home
  5-section-edit/6-results/QE5-….md      any depth
  board/
    index.html
    QA/QA1-frontier.html
```

- Discovery rule: every `Q*.md` / `S*.md` / `Agent-<n>-*.md` anywhere in the board folder's whole tree, plus `Skill-<n>-*.md`; segments of the path starting with `_`/`.` (`_archive/`, `_preview/`, ...) and `fig/` do not count.
  The four prefixes are what `page_files()` in `src/common.py` actually globs, filtered by `PAGENAME`; the Skill and Agent kinds were added JL 260731 and neither is counted toward settled.
- Pages still lists only **filenames**; filenames are unique across the whole board, a duplicate warns on the command line and only the first one found is honored.
- Page write-back (comments, archiving) carries **a path relative to the board root**; archiving flattens a nested question into the board root's `_archive/`.
- A question newly added from a page **follows its own group** (QA1, JL 260726): `＋Q` looks at where that group's existing pages already live, and if they agree, writes into that folder.
  When the group has no page yet, it opens a new `Q<letter>-<slug>/` on the spot from `### Q<letter> · <title>`.
  Only when the group itself is already scattered across two places does it fall back to the board root (better to leave a scar than to guess blind).
- A Q file's own path references **stay relative to the board root** (exactly as in a flat layout), regardless of where the question itself lives.

**A page moves into a folder for only two reasons, and they are the same rule** (QA1 + QC3, JL 260726):

**Three folder meanings**: what a board folder can stand for.

```
GROUP folder     the folder IS this Q group                  a flat design board that grew up
SUBJECT folder   the folder IS what this question discusses  a board sitting on an existing tree
```

A page can live in only one place, so a board picks one.
**The two coincide on a paper's `0-lifecycle/`**: `1-work/`, `5-appendix/`, `6-submission/` are each both a subject folder and an S family, so that kind of board has had a group folder ever since 260724, without anyone deliberately giving it one.

Precisely because they coincide, the code recognizes no convention like "a folder named QA"; it recognizes only **where this group currently lives**: the same rule holds for both reasons.
Membership has been path-based, not registration-based, since 260722, and `## Pages` lists only bare filenames, so moving a page is a pure `mv` and board.md does not need a single character changed.

**JL ruled on 260726: the group folder is the default, from the very first page, on every board.**
The folder is named `Q<group-letter>-<group-title-slug>` (`QA-defining-a-board/`, `QD-working-on-the-board/`); **it must never be just `QA/`**, because that copies the id twice, and the group title is the half a reader cannot recover from the filename.

Only Board-level source and derived artifacts stay at the Board root: `board.md`, optional `board.excalidraw`, `fig/`, `_archive/`, and generated `board/`.
`## Pages` does not change a single character; it still lists only bare filenames.
A page's ＋Q writes into the folder its group already lives in; a new group with no page yet opens a named folder on the spot, from its first page's `### Q<letter> · <title>`.
To move a whole board, use `python3 <skill>/cli/regroup.py <board-dir> --apply` (omit `--apply` for a dry run, `--all <root>` scans the whole repo).

**Do not rename a board that is already split into folders under this rule.**
A paper's `0-lifecycle/` is exactly that case: `0-seed/`, `1-work/`, `3-display/` are each both a subject folder and an S family, so it already satisfies the one-folder-per-group rule, and its numbering additionally carries the lifecycle order, which letters cannot carry.
What must be satisfied is this rule, not a resemblance to a design board.
`regroup.py` therefore only touches pages sitting at the board root, and it skips outright a board with no page at its root.

**⚠️ `## Links` must be updated along with a move; `## Pages` does not need to be.**
Measured on 260726: after moving 154 pages, 17 declared Links broke, all of the cross-board kind, pointing at some page in another board's home (`../01-haipipe-paper-260725/QC0-….md`).
Pages lists bare filenames so it is unaffected; Links holds real paths, and it is exactly this moment that exposes the difference between the two sections.
The checker reports these as `dead-link` / `dead-href`, so `check.py` must run once after every move.

## 2. Numbering and kind

The filename prefix IS this question's id: `Q` + group letter + sequence number within the group.

**Ids carry the grouping**: the letter is the group, the number is the page.

```
QA1  QA2  QA3      group QA
QB1  QB2           group QB
QC1                group QC
```

Sort order is (letter, number).
With no grouping, it is simply `Q1 Q2 Q3`.
Adding a group means taking the next letter.
The **next number** within a group (the rule ＋Q on a page uses) = the maximum number of that group found across the whole tree on disk and in that group's entries under Pages, plus 1 (count the whole tree post-QC3, not just the board root).
`-<slug>` is only a short lowercase English tag for humans to recognize the file (`access`, `scheduling`); the parser ignores it, consistent with `board-example.md`.
A newly opened Q is always `state: 🔴 OPEN`.

A paper lifecycle's S page uses the full family name: `S-<Family>-<unit>-<slug>.md`.
Family is fixed to `Seed`, `Work`, `Venue`, `Display`, `Main`, `Appendix`, `Submission`; unit can be a number, or, in Appendix, a letter.
Examples: `S-Seed-1-literature.md`, `S-Main-4-theory.md`, `S-Appendix-B-validation.md`.
Q is a decision; S is a lifecycle page.
The two share the same section grammar, and the index page separately tallies `questions settled` and each S family's gate progress.
Old boards' `S0` / `SM0` / `SA0` naming still parses, but a new paper board no longer generates these abbreviations.

**S's `state:` uses the same set of four machine states as Q**, and the machine reads only the first emoji: `🔴` not started · `🟡` in progress · `✅` = **this stage's human gate has passed** (the `N/M` count the index shows for a family is exactly the ✅ count across that family's S pages) · `⏸️` explicitly on hold.
A human-readable note can follow the emoji, for example `✅ SETTLED`, `✅ PINNED · MISQ 2026`, `🟡 rendered · awaiting gate`; the suffix is not a fifth state, and it must not change what the first emoji means.
A newly opened S, like a newly opened Q, is always `🔴 OPEN`.
The only difference is **what earns the flip to ✅**: a Q needs every Aim met or explicitly held, while an S needs its own human gate to have passed.

**An S page in `## Pages` follows the same convention as a Q file**: one bare filename per line (`S-Main-2-introduction.md`), grouped under whichever `### ` heading it sits below.
An ordinary board's group title is free text; **a paper lifecycle board groups by named family by default**:

**A group block in board.md**: the heading plus its one-line intro.

```markdown
### QB · Work Group
Resources and claims become checkable lifecycle pages.
S-Work-0-resources.md
S-Work-1-claims.md
### QD · Display Group
The evidence-presentation layer serves both Main and Appendix.
S-Display-0-design.md
QD1-figure-order.md
QD2-table-scope.md
```

The seven groups' index order is fixed as `Seed → Work → Venue → Display → Main → Appendix → Submission`, but this is a stable ownership/navigation order, not a linear flow the executor derives automatically.
The real stage edges must be written in `## Pipeline`; one flow can enter Display after Narrative and then split into Main and Appendix.
Display is its own group because it owns the claim-to-display map, approved assets, captions, statistical labels, and placement; it is not an ordinary Work item.
In Seed, `S Seed → S Literature`; in Main, narrative control is followed by each manuscript section; in Appendix, control is followed by A/B/C; in Submission, reconcile → compile → review → submit.
After external review arrives, reopen the affected Work/Display/Main/Appendix pages and reuse that same set of Submission pages to record the next round; do not duplicate `S-Submission-R2-*` pages.
A given S's Q decision sits right after it.
The title still opens with one unique Q family (such as `QD`, `QBa`), so the page's ＋Q / archive controls have a stable writer key.
An unregistered one still displays, filed under the ⚠️ group.

## 3. board.md

**board.md's head**: the fields that define the board itself.

```markdown
# Board title: one sentence stating what this board is for
spine: The spine. What this board is solving, in one sentence. The topic must not drift until it is solved.
close: The close condition. When this board can be closed.
source: optional, where this board comes from (a meeting-notes path or similar)

## Topic
Written for someone with zero background: what project this is, who is who, what is being solved.
A zero-background review most often stalls on this section being missing.

## Pipeline
What relationship holds among these Qs: parallel? a pipeline? how many groups?

## Board Map
Optional, and it is the board's OWN MAP: how the groups connect, plus the cross-group page edges that really exist.
Write it as one ``` figure.
Every page id and group token inside a figure renders as a link (0.53.0), so an ASCII map is the only map a reader can travel on, it draws on a static host with no Excalidraw endpoint, and it survives with scripts off.

It renders FIRST on the index, above Topic, as a disclosure you can shut: a map you cannot close pushes the index off the first screen.

An ASCII `## Board Map` WINS over the `board-map:` share URL and over the local `board.excalidraw` scene.
Declare one source, not two.
A board with no `## Board Map` keeps the old iframe behaviour unchanged.

Not a second registry of pages: the index below lists every page, so a map that repeats the roster says the same thing twice.
Draw the CONNECTIONS.

## Board Structure
Optional. Write here whenever the board needs to show a zero-background reader its own shape, instead of opening a separate Q page for it.
It must split `Board-Folder` from `Board-Webpage`.
`Board-Folder` names the editable source (`board.md`, descriptive group folders, one Markdown file per page, `fig/`, `_archive/`) and the derived `board/` site.
`Board-Webpage` names the three reader routes: `board/index.html`, `board/<GROUP>.html`, and `board/<GROUP>/<page>.html`, plus the shared `_assets/` they load.
Since 0.78.0 this is source-only documentation in `board.md`; it does not render on the Index.

## Pages
### QA · group title
One sentence shown under the group header on the index (optional intro).
More plain lines: the click-to-expand body, what this group is for and why.
QA1-form.md
QA2-qtemplate.md
### QB · another group
QB1-skillmd.md
### QB · Seed Group
An S page lists only a bare filename, same as Q.
S-Seed-0-seed.md
S-Seed-1-literature.md
```

**Pages only handles ordering and grouping**; it never copies a title or body text, because a copy would go out of sync.

**The `doc:` line (formerly QF2, JL 260724; **retired 260726**, do not use it again)**: to display a file that lives elsewhere, use §5's `![[path]]` to embed it into a real page instead, which is equally zero-copy but the page then gets a state, a checklist count, and a place for comments.
The paragraph below is kept only for old boards, and the parser still recognizes it (no one in the whole SPACE uses it today): `doc: notes/readme.md` renders the listed source files **directly** as one page (id = the **folder** the first file sits in; a top-level file uses its filename stem instead, so `2b-pitch/PITCH_LOG.md`'s page is called `2b-pitch`, and two `README.md` files never collide; the title takes the first file's own `#`/setext heading, or the id if there is none).
There is no Q file wrapping it, so there is also no state, no checklist count, and no place for comments; a doc page is something to **look at**, not a **question**, and it does not count toward the settled tally or progress bar.
It is kept only for backward compatibility with old boards; a lifecycle stage that needs to take part in a checklist, a gate, and comments must be written as an S page instead.

**Group intro (QC2, 260724)**: plain lines between a `### ` heading and that group's first `.md` line are the group's intro.
Line 1 is always visible under the header on the index page; any further lines open on click (rendered as a native `<details>`, so the no-script invariant holds).
Intro lines must not end in `.md`.
The index page's ＋Q / ＋Group / 🗄 buttons write exactly this grammar through `POST /_board/structure` (`structure_op()` in `live/structure.py`, imported by the console): `add_question {group, title}` seeds a stub Q file and lists it under its group; `add_group {title, letter?, hook?, body?}` appends a `### QX · title` heading (letter auto-picked); `archive_question {q}` moves that file to `_archive/` inside the board folder (never deletes; since QC3 build.py DOES glob subfolders, so it is the `_` prefix that hides `_archive/` from discovery, and archived files leave the page for that reason); `archive_group {group}` removes a group only when it lists no questions.
Over HTTP the payload also carries `path` (the page's own location.pathname); called directly it is `structure_op(board_dir, payload)`, and importing serve.py is side-effect free (`serve_forever` sits behind `__main__`).

**Required**: `# title`, `spine:`, `close:`, `## Topic`, `## Pipeline`, `## Pages`.
All three of these sections must be written, so do not omit `## Pipeline`.
`## Board Structure`, `source:`, `## Related Folders`, and `## Links` are optional.
Board Structure is Board-level source documentation. It does not count toward a Q page, enter the settled count, occupy a page id, or render on the Index.

## 4. Q/S page

Section names correspond one-to-one with where they render on the page:

**Source field to rendered element**: which line becomes which part of the page.

```
# short title   → .h2         38px when focused, with the id hung in front
state:          → .pill       first token is ✅ / 🟡 / 🔴 / ⏸️; a human-readable note can follow
owner:          → status bar  JL shows 🧠 ruled, others show 🔧
method:         → status bar  one sentence on how it is done
requires:       → contract    explicit upstream S ids / paths, comma-separated (S only)
style-from:     → contract    explicit venue/style sources; rules materialize in Writing Style (S only)
provides:       → contract    a short delivery note this page gives downstream (S only)

## Opening         → .opening .ask + kind routing  the first question sentence lives in Opening; the explanatory paragraph is described below
## Stage Contract  → a collapsed row .csec.contract inside Opening  S's inherited inputs + Venue (folded into Opening, no longer its own visible section)
## Diagram         → .diagram-section > .dia  its own section, collapsed by default
                     splits into two sub-sections inside (JL 260726): `details.dsub.dsub-a` (▧ ASCII, `open`)
                     and `details.dsub.dsub-x` (✏️ Excalidraw, shut). **The source writes only one
                     `## Diagram`**; the split is computed by `page_question.split_diagram()` under the rule
                     "a whole line holding exactly one excalidraw URL"; a URL inside a fence does not count.
                     When there is no canvas, that section still renders (writing "No canvas attached yet"),
                     because the 🖌 attach-canvas button has to live somewhere.
## Content         → .content / .opening-context  required on S, optional on Q; see below
                     S carries only what this stage itself produces (JL 260725): Required Inputs and Venue
                     belong in `## Stage Contract`, prose rules in `## Writing Style`, settled corrections in `## States`, and
                     intended outcomes belong in `## Aims`. On S the section title displays the
                     stage's name (`📚 Content · Main 7 §6 Results`, derived from `# short title`, so when
                     the artifact's own numbering does not line up with the board index, title the page
                     `S Main 7 · §6 Results` to state both numbers at once), and it no longer counts
                     subsections; Q still shows a count.
                     Inside it there are **only two levels** (JL 260725): `###` = a block that has its own
                     content and can fold on its own (a division), `####` = one paragraph inside it, always
                     at this level. Depth is carried by numbering (`§6` vs `§6.1`), not by heading level: the
                     page folds only one layer deep, and one more level would compress the whole section into
                     a single box and lose per-division folding. A division is written out only when it
                     genuinely has content: a flat section writes one `### §1 Introduction` leading its
                     paragraphs, and a section with subsections starts directly at `### §6.1`, never opening a
                     box that is empty on click. The payoff is that it is checkable: the count of dotted `###`
                     headings IS the subsection count, checkable against the venue blueprint without reading
                     the prose.
## Aims           → .col.goal   green border, the column header derives `met/total` from States
## States         → .col.now    yellow border; one current emoji row per Aim
## Files           → .fls        which files this question touches, blue border (paths auto-become clickable links)
## Why here        → .folds      legacy only; collapsed when an old page still has it
## Discussion      → .folds      collapsed
## Law             → .folds      collapsed · the rules this question settled
## Lesson          → .folds      collapsed · the pitfalls this question hit
## Glossary        → .folds      collapsed
## Log             → .folds      collapsed
```

**Required on both kinds of page**: `# title`, `state:`, `owner:`, `## Opening`, `## Writing Style`, `## Aims`, `## States`.
S additionally requires `## Stage Contract` and `## Content`; Q deletes Stage Contract and may omit Content.
`## Files` is optional but **strongly recommended**; everything else (`method:`, `## Diagram`, and all the folded sections) is **optional**, so delete the whole section when it is not used.
There is no `## Boundary` section. Opening itself states the scope, and a page points at the neighbouring page that owns excluded work.
The order of the canonical folded sections is fixed by `build.py` (Discussion · Law · Lesson · Glossary · Log), independent of the order they were written in the file; a legacy Why here is collected ahead of them when an old page still has it.

**The on-stage order is fixed**:
Q is `Opening → Diagram → Content → Aims → States`;
S is the same: Stage Contract is folded inside Opening and no longer occupies its own section (JL 260725)
(Files follows after the state).
Opening is the question lead plus one paragraph stating what the question's own words mean, why that is hard, and what this page decides (JL 260801); the fixed sidebar already carries the page structure, so the drawer does not duplicate it. The optional Diagram is its own section, collapsed by default, and expands only when the section name is clicked.
Everything after `## Opening`'s FIRST BLANK LINE, on both Q and S, goes into the More details row of that page's own drawer (JL 260729; the row was labelled "Why this matters" until JL renamed it on 260801, and before 260729 a Q's explanatory paragraph automatically became Content's first subsection).
A stage has exactly one contract section and it is `## Stage Contract` (JL 260801). There is no Stage Record: an old page that still holds a direct `### Stage Record` under Content has it lifted into that contract verbatim, as its opening lines, and the remaining subsections stay in Content.
A Q's explicit Content can be omitted.
Intent comes first (what is being asked, the boundary, what counts as done), then the state (where things stand now).
An Aim is intent; its State is fact. The paired section labels are plural: `Aims` and `States`. A Plan, when needed, is optional text inside an Aim and never a third fixed top-level section.

**`## Why here` is retired.**
Its job (why this is hard, what happens if it stays unsettled) is merged into `## Opening` below its first blank line and rendered as "More details" (JL 260801, renamed from "Why this matters"): both Q and S put it in Opening's drawer, which is **shut until the visible paragraph is clicked** (JL 260729; before that Q put it in Content's first subsection) and then shows every row FLAT (JL 260725: one door, and nothing behind it folds a second time).
The old section on an old board is still collected into the folded area at the bottom.

**Every old section name is still recognized**, so an old board can be regenerated without being edited: `## Question` can also stand in for `## Opening` (`## Opening` is the canon, `## Question` the legacy alias, JL 260731), as can the Chinese names and the historical `## Done when` / `## Items to Finish` (= `## Aims`) and `## State` / `## Now` / `## Where we are` (= `## States`).

**The Q-consumer rule on an S page**: do not open a top-level `## Q-consumer`.
Each consumer is an Aim inside `## Aims`; its heading keeps both a stable Aim id and `Q-<Stage>-<n>`, while its detail keeps Description / Reason / Probe / Done when.
Mark it `✅` in `## States` only once the Answer has landed, been explained, and been woven back into Content; a deferred one closes only when a forward pointer has been written down.
`## States` only summarizes the stage; it does not restate each consumer answer.

**The Stage Contract rule on an S page**: dependencies are read from the top-level metadata only, never guessed from Pages order or from a number in a filename:

```markdown
requires: S-Work-1, S-Main-0, S-Display-0
style-from: S-Venue-1, STYLE.md
provides: reader-facing results section

## Writing Style
<!-- haipipe:style:start sha256=... -->
**Inherited requirements from `S-Venue-1`**: ...the resolved page prose rules...
<!-- haipipe:style:end -->

## Stage Contract
<!-- haipipe:contract:start sha256=... -->
### Required Inputs
...a short summary of the upstream `### Provides`, its path, and its gate state...
### Venue
...the explicit venue/style source; its prose rules are materialized in `## Writing Style`...
<!-- haipipe:contract:end -->

### Provides
The downstream delivery note this page's author owns; sync does not overwrite it.
```

`python3 <skill>/cli/stage.py new` creates the page, `stage.py sync` updates the marked Stage Contract and inherited block in `## Writing Style`, `stage.py sync --all` refreshes in the topological order of the explicit dependency graph (it does not look at Pages order), and `stage.py check` verifies the source hash.
`build.py` also puts a missing or stale contract into its warnings, but it never modifies the Markdown.
The upstream full text stays upstream; Stage Contract carries acceptance conditions and Venue links, while the page's own Writing Style carries the resolved prose rules.

## 4b. `## Links`: the wire between the board and its artifacts

What a board discusses usually does not live in the board's folder.
Declare it in `board.md`:

**A Links block**: how a board declares the paths its pages may cite.

```markdown
## Links
SKILL.md            ../../haipipe-board/SKILL.md
ref/page-template.md   ../../haipipe-board/ref/page-template.md
haipipe-board/      ../../haipipe-board/
```

The left side is how it is written in backticks in the body; the right side is the path relative to the Board source folder.
The split renderer adds the required hop from each generated page back to that folder, so one declaration works from the Index, group pages, and page pages.
After that, every `` `SKILL.md` `` becomes a clickable link.

- An undeclared path is still tried once automatically: it walks up level by level from the board's folder looking for the same path, and links it only when it is found and **really exists**.
  When nothing is found it stays a plain `<code>` and never turns into a dead link.
- A declared path is **not existence-checked**: write it wrong and it is a dead link, on you.
- Ordinary markdown links `[text](path)` are supported too.

## 5. Body syntax

| Written form | Effect |
|---|---|
| `### heading` (at the top level inside `## Content`) | **division**: a block of content that can fold on its own. Depth is carried by numbering (`§6` vs `§6.1`), not by heading level; write one only when it genuinely has content (see §4) |
| `#### heading` | **paragraph heading** (`.ph`): one paragraph inside a division, always at this level. It carries **no icon** and is one size smaller than a group title; it used to be flattened into `**…**`, which put the group title's 🔹 on it and made "one paragraph" claim to be "a sentence leading a run of items" (JL 260725) |
| a whole-line `(…)` directly after a `####` | **the job** this paragraph does (`.pj`): grey italic, left on stage as a scan hook, never folded (folded, it cannot be scanned). Only the line immediately after the heading is read this way, and per the venue template its length is about 80 to 120 characters |
| `**a whole bold line**` (alone on a line) | group title: slightly larger, leading a run of items below it. Start it with an emoji (`**🎨 Layout landed**`) and that emoji is used as its mark; without one the default 🔹 is used. **Use it only when it really does lead a run of items**; a single paragraph takes `####` |
| `- heading` plus an explanation line indented two spaces | item block: a ▸ bold heading plus a grey explanation |
| `- [ ]` / `- [x]` plus an indented explanation | a checklist for an explicit human decision or legacy page; canonical Aims use stable ids without checkboxes, and progress derives from their matching State rows |
| a ` ``` ` fence | verbatim `<pre>` output (ascii figures, code, folder trees). **Never draw two trees side by side**: the column boundary is whitespace, it disappears the moment anyone copies it, and the right column then reads as branches of the left one; a board exists to be pasted into chat and email. To compare, stack them vertically, one complete tree at a time |
| an **indented** ` ``` ` fence inside an item's explanation lines | goes into **that item's folded area** (it is not flushed out as a sibling block): dedented, then verbatim `<pre>`, and it can go wherever you put it (after the summary, between body paragraphs). A top-level fence is a sibling block as before (JL 260724, first used on the QC10 CABG board) |
| a line holding only `![[path]]` / `![[path#Section]]` / `![[path#Section\|source]]` | **embed** (QF1): pulls another file (whole, or one section) into this question by reference, read live at generation time. The path is relative to the board root, and when not found it is searched upward level by level (up to 8 levels); only `.md`/`.txt` are accepted; `#Section` recognizes a `##` heading **and** a setext (underlined) heading; a file that cannot be embedded, or a section that cannot be found, produces a red warning in place and never silently goes blank; an `![[…]]` written inside embedded content is not expanded (loop guard). A sentence comment is written only into the Markdown of the page carrying it; the embed source itself is not modified. A trailing `\|source` = the same file spread into a `<pre>` **byte for byte** (not rendered, no chip), for the kind of page that gives the source first and the rendered result after: both blocks are the same file read twice at generation time, so they cannot disagree. Any other mode is an in-place red error |
| an excalidraw share link alone on a line | embedded as an interactive canvas (iframe) plus a fallback "↗ open in Excalidraw" link |
| a bare `https://…` | becomes a clickable link automatically (a URL already inside an `href=` is not wrapped a second time) |
| `` `code` `` `**bold**`, plus the image form `!` `[` `]` `(fig/NAME.png)` and the same with `.pdf` | inline code / bold / image / readable PDF (with a fallback open link). The image form is spelled out here rather than written literally: the renderer resolves image syntax before inline code, so a literal example embeds a real (and dead) file. |
| `> Comment JL text · 260729 1502` | **sentence comment**: sits tight under the sentence above it, colored by signature; only when there is no preceding sentence is it an ordinary discussion line. `> Comment WHO` is the only form to write (JL 260802), because beside `> Citation:` and `> Value:` a bare pair of initials said nothing about what the row was; the older `> JL: text` still renders and `check.py` warns on it inside `## Content`. `## Discussion` is NOT affected and keeps `> JL:` with its nested `>>` replies, which is a thread and a different grammar |
| `> Card the words: what to show` | **span card** (JL 260802, QB5): the ONE record that does not render as a row under the sentence. It names a few words of the sentence above and turns them into a button whose panel carries the text, so the card is reached by clicking the WORDS while every other record is reached by clicking the LINE. The span travels in the record, never in the prose: the sentence gains no marker and no id, and the renderer finds the words by the same exact-text match `serve.py` already uses to find a sentence. Words that are not in the sentence render as a loud row in the drawer, never as silence. Written by hand, or by selecting the words and clicking 🪪 Card |
| `> ✎ The whole sentence with ~removed~ *added* words · JL · 260729 1502` | **edit record**: the sentence above has already been updated to its final text; this line repeats the whole sentence and marks only the removed and added words |
| `>> CC0723: text` | a reply |
| `> JL 「the quoted sentence」: text` | a discussion line, plus the sentence inside 「」 is highlighted in the body |
| `260723 1030 · text` | one Log line; the time can be omitted |

A signature is any 1 to 4 uppercase letters (`JL` `ZW` `CC0723`).
`JL`/`CC` have fixed colors; every colleague uses their own initials and is assigned a color automatically from the name.

Once the page is generated, render-local structure addresses are established inside `## Content` only.
Each `###` division is `Cn`; each `####` heading inside it is a terminal node `Cn.Hn`; a body paragraph sits at the same level as an H, and the sentence leaf is `Cn.Pn.S1`.
Therefore `QAb3.C1.H1` and `QAb3.C1.P1.S1` are legal, and `QAb3.C1.H1.P1.S1` is not.
One source line is currently one sentence, so every P has only `S1`.

When a pointer device hovers or focuses a Content sentence, it shows `Cn.Pn.S1 ＋ 💬`: `＋` opens a Comment under the sentence, and `💬` establishes a closable Sentence Focus at the top of the chat session this Q already has, showing the name of the Content division and of the nearest Heading.
Establishing the focus calls no model; only the next user message carries the position, the address, that sentence, and the apparatus directly adjacent to it.
A touch device collects Comment / Chat / Edit into an unobtrusive `⋯`.
These addresses are never written back into the Markdown; renumbering is allowed after Content nodes are inserted or moved, so they are focus addresses of the current render, not permanent ids.

## 6. Generating

`build.py` / `watch.py` both live in the skill folder's `cli/`, not in the board folder.
Call them with a path; do not `cd` into the board folder and run `build.py .`:

**Build once, or watch**: the two ways to regenerate the site.

```bash
python3 <skill>/cli/build.py <board-dir>     # generate once (<skill> = .../board/haipipe-board)
python3 <skill>/cli/watch.py <board-dir>     # watch it: any .md change regenerates automatically
```

**Do not hand-edit the generated `board/` tree**: the next generation overwrites it.
The md is the only source.

## 8. The generated Board-Webpage

One generated site has three URL kinds and no second deck:

- **Index**: `board/index.html` carries the spine, Board Map, Related Folders when declared, Section Matrix, page roster, and Activity.
- **Group**: `board/<GROUP>.html` carries that group's purpose, expandable explanation, progress, and page rows.
- **Page**: `board/<GROUP>/<page>.html` carries one permanently focused Q/S page, with the shared sidebar preserving navigation.

Internal links are ordinary HTML links when scripts are off. With scripts on, the router swaps the requested page into the current document so the attached chat or terminal session survives navigation.

**Board identity mark (QA4, JL 260726)**: the page title opens with the shared `assets/board-mark.svg`.
It is four pages overlapping each other, with a speech-shaped aperture cut out of the center; that cutout is transparent, so it works on a light or a dark background.
`build.py` inlines the SVG straight into the title and encodes the same source into a `<link rel="icon">`, so the mark adds no external dependency.
The geometry of the mark is maintained in the SVG only; the eight `--board-mark-*` tokens in `assets/css/00-base.css` control the gradient colors of the four faces.
The Index shows it at 42px and a focused page presses it down to 24px, so the title remains the primary information.

**What goes on stage and what is shut when focused** (settled by QA4):

- **On stage** (top to bottom): the title → `🧭 Opening` (this row does not fold, it is always there) → the lead sentence (always there, and **clickable**: open it, and in the drawer, More details / Writing Style plus S's Stage Contract (Required Inputs · venue), are all **flat**, seen in one go, with no second ▸ level nested inside.
  Every subheading in the drawer is **a bare word carrying no icon**: previously only 2 of 7 had an icon, and that is the inconsistency JL named, JL 260725) →
  `🖼 Diagram` (optional; only the section name is on stage, the content is collapsed by default; open it and ▧ ASCII is seen first, while ✏️ Excalidraw takes one more click, JL 260726) →
  `📚 Content` (only the subsections the author wrote explicitly; since 260729 a Q's explanatory paragraph also goes into Opening) →
  `🎯 Aims` → `📍 States` → `📁 Files`.
- **Three levels of hierarchy**: section heading (🧭/📚/🎯/📍, with a rule under it) > **group title** (a whole bold line → 🔹 by default, or the emoji it starts with, leading a run of items) > the item's name (`▸`).
- **Shut by default** (revealed by clicking the name, or the `expand all` to the right of the section heading): EVERY section and every Content division, including the first one (JL 260801, reversing the 260725 open-by-default rule now that the sidebar carries the map), the whole `## Diagram`, an item's explanation (collected into a native `<details>`), a sentence's own apparatus, and a code block in the body (collapsed into one line, `</> code · N lines`).
  Opening is the one section that does not fold from its heading, because a page whose first section can be shut can open showing nothing; its visible paragraph carries the fold instead.
  Diagram carries one more layer of ordering: open the section and ▧ ASCII is there while ✏️ Excalidraw is still shut, because a shut `<details>` is not displayed, so a `loading="lazy"` iframe inside it does not load, and a board with 28 canvases no longer starts 28 of them at load time.
- **Sunk into the folded area at the bottom**: Discussion · Law · Lesson · Glossary · Log; a legacy Why here is preserved ahead of them when present but is never authored on a new page.
- The first look at a screen = one clean column of section names and item names; Diagram is opened by hand, and `expand all` spreads out the items / code of the other sections in one click (pure enhancement: with the scripts stripped, every row still opens on its own).

**Other things that are fixed**: Aims and States are **stacked vertically**, not split into left and right columns (side by side, unequal lengths leave half a column empty); a long question **scrolls**, and is never truncated or split across screens; **no 16:9 lock**, the height follows the window (locking the aspect ratio belongs to a projection deck); a **real space** is left after the id in the big title, so copying it does not glue it into `QA4Single…`.

**Invariant: delete every `<script>` in the page, and every question and all of the body text is still there.**
`build.py` asserts this on every generation.
A script can only enhance (currently just the comment layer); it can never be the source of content.
