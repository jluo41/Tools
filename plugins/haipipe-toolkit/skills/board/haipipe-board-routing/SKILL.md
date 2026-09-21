---
name: haipipe-board-routing
description: >-
  The WRITE verb of the board family: take one input — a decision, finding,
  correction, status change — and land it on the owning page and section. Also
  proposes and materializes a board's structure and page groups. Use when work
  happened and the board must record it. Trigger: route, write back, owning
  page, we decided, board structure, regroup, /haipipe-board-routing.
metadata:
  version: "0.11.1"
  last_updated: "2026-09-20"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board-routing · every write onto a board, at both altitudes

Resolve the owning Board, work object and field, then record the input there
in the same round. Board kind determines membership; the Folder/Page owner
determines the content contract. These routing steps are an operating
procedure, not independently commissioned Workflow Runs.

**The boundary:**

```
haipipe-board-routing            what it loads          what it never does
─────────────────────            ─────────────────      ─────────────────────
propose a board's structure      haipipe-page     render, serve, check
materialize it after approval    haipipe-sentence tick a human decision
find the owning location                                change a human page gate
append the anchored write                               create a page silently
keep each group's lane block                            materialize an
propose a page when none fits                             unapproved proposal
```

Digest (a session transcript, many inputs) is this verb FANNED OUT: it calls routing per input and never reimplements it.
Digest is not built yet; when it is, it runs in a fresh context for the same reason the cold read does.

## 🗂 Two altitudes, one verb

```
🗂 BOARD + GROUP altitude          board.md and nothing else
   propose · materialize          the structure, before any page exists
   lanes · regroup                each group's engine · pages · folder block

✍️ PAGE altitude                   one page's .md
   the five-step route            one input → one owning page → one write

   both write MARKDOWN ONLY. haipipe-board renders, serves and checks.
```

An authorized Page write records work that already happened. A proposed Board
structure needs agreement because it determines which objects will exist and
which group IDs future citations use. Reuse explicit agreement already given
in the session; a group rename requires a migration plan.

## 🏗 The board altitude: propose, then materialize

### `propose` · before any file exists

Talk first, write nothing.
From a topic, propose and show:

```
1. spine        one sentence: what is being pinned down
2. close        what must be true for the board to be done
3. groups       3-7 of them, each a responsibility, not a phase
4. pages        the questions each group owns, with ids
5. connections  which group depends on which, and why
6. skills       which skill this board may change (optional)
```

Obtain agreement on the concrete proposal before materializing it. An existing
approval for that structure already satisfies this requirement.

### `materialize` · after approval

Resolve the Board kind first. A generic Board uses `board.md` (title, spine,
close, `## Topic`, `## Pipeline`, `## Pages`), one descriptive folder per group
and one Page per approved question. `## Board Map` optionally shows relationships;
`## Board Structure` optionally explains source folders and generated web routes.
Use `haipipe-board/ref/board-form.md` and the canonical Page template it delegates
to through `haipipe-board/ref/operations.md`.

Task/Discovery Blocks use their native Job/Task tree. Design and Insight Boards
use their independent family owners. Resolve existing members before creating
any object, then record presentation order and hand off to `haipipe-board` to
build. Generic Q/S creation does not replace native members.

This is the same work `haipipe-board`'s `open` action describes to a person running a board by hand.
Keep this procedure and the Board door's selected operation consistent.

### `lanes` · refresh the per-group blocks

This helper projects explicit Page rows in `board.md ## Pages`; it does not
discover membership. Use it for a group whose Pages are explicitly listed.
A native Task/Discovery Board may list only Job headings, so an empty lane
table does not mean the Job has no Tasks. Keep its native projection instead
of duplicating the Task roster just to feed this helper.

```bash
python3 <this-skill>/src/lanes.py <board-dir>            # dry run: what would change
python3 <this-skill>/src/lanes.py <board-dir> --apply    # write board.md
```

It ROUND-TRIPS.
The page roster is generated from `## Pages` so it can never disagree with the index, but every cell a person typed is kept:

```
· a row whose page still exists   → engine · name · folder all KEPT
· a page with no row yet          → arrives with `?`, which is the to-do list
· a row whose page is gone        → DROPPED
```

The generator owns the table skeleton; existing cells remain with their author.
A page's `# ` title only SEEDS a new row's name; the column is 29 characters and a real title rarely fits it.

Kept cells are collected GLOBALLY, keyed by page id across the whole file rather than per block, so a page that changes group carries its typed cells with it instead of resetting to `?`.
`dropped` is judged against the whole roster for the same reason: after a regroup a page has merely moved, and only a page in no group is gone.

### `regroup` · move pages into one folder per group

`haipipe-board/cli/regroup.py` folderizes generic Board root Pages whose
filenames match a current group key. It leaves nested Pages in place and
reports unmatched roots or existing destinations as skipped:

```bash
python3 <board-skill>/cli/regroup.py <board-dir>            # plan
python3 <board-skill>/cli/regroup.py <board-dir> --apply    # git mv
```

This script does not rename/split existing nested groups, declare aliases, or
rewrite references. A no-moves result does not complete such a migration.
For a group rename/split, plan the exact nested folder/file moves, preserve old
IDs as declared aliases, and update current references together. Preserve
historical records. Dry-run the affected moves and check aliases/references
afterward; do not apply generic folderization to a native subject tree.

### What the board altitude does NOT own

The two canvases the Index carries are content, not structure, so they follow the same approval rule as everything else here.
The board level shows how GROUPS connect and nothing else, because the index already lists every page below it; a board-level roster is the same information twice.
The per-page `⚙️ engine · 📋 page · 📂 folder` mapping lives one altitude down, in each group's own intro, which is what `lanes.py` writes.
A group anchors at `#group-<token>` and is not a page: the anchor scrolls the index, never opens a card, and never enters the settled count.
Rendering the index, checking a page, and checking a sentence all belong to `haipipe-board/cli/`.

## 🗺 The page altitude: the route, five steps

```
1  READ the input        what happened · what kind of record it deserves
                         (an Aim `Now:` fact · a D<nn> decision thread · an
                          outline log/files record · a lane reply); a derived view,
                          aggregated from state the pages already hold,
                          deserves NO write, because a copy drifts

2  RESOLVE the board     the session's attached board, or the nearest board.md
   + operating context   above the working path; inspect the parent unit and
                         repository root first. If root .server_config exists,
                         read its README.md and non-secret settings.env values
                         as the primary hosting contract. Then inspect
                         spaces/registry.yaml (or Tools/spaces/registry.yaml)
                         for ownership/fallback context; two plausible boards
                         or SPACE owners = ask, never guess

3  FIND the owner        read board-kind and resolve actual members with the
                         Board's discovery rules. The source tree supplies
                         membership; ## Pages supplies display groups/order.
                         Task/Discovery Job headings need not list every Task.
                         Resolve a unique existing Page and its Folder owner;
                         ## Links may resolve an older id. Never invent a path
                         from an id, or create a duplicate for an unlisted Page.

4  PICK the surface      load haipipe-page and the resolved Folder/domain
                         owner. Its Page contract says whether the input belongs in
                         Opening, Content, Aims, or a typed `outline/` record

5  WRITE anchored        edit the owning on-stage field or typed record while
                         preserving its schema and id; never synthesize a
                         retired `## States`, `## Files`, `## Discussion`, or
                         `## Log` section
```

`board.md ## Pages` remains the presentation registry, not the membership
authority. A discovered but unlisted generic Page needs registration, not
replacement. The shared SPACE registry is
not a second list of Boards: it owns neighboring SPACE repositories and their
delivery configuration, while Board Home discovers Boards by walking the
matched SPACE for `board.md`.

If the input changes a SPACE id/name, root, domain, port, public URL, short
route, mount, or discovery policy, the routed Board write and the companion
configuration edit are one round: update the shared registry and the matched
`.server_config/README.md`. When the Board repository already has a root
`.server_config`, its host, port, public URL, and auth-file path are the primary
startup inputs; explicit user or CLI values may override them, while registry
data does not. Ordinary Page prose, Page titles, and Board decisions do not
touch SPACE configuration. Never print credentials or edit machine-local
`settings.env` without an explicit request.

## ⚖️ The two write laws, inherited not invented

**Human decisions.**
Routing may update factual Aim `Now:` lines and append typed log records. When
it has inspected the evidence, it may move an Aim among the allowed statuses
and records the reason in `outline/<stem>-log.md`. It may never decide for the
person or change a page-level human gate. A proposal receives a Board-wide
`D<nn>` thread in `outline/<stem>-discussion.md`; when it blocks an Aim, that
Aim's `Now:` points to the thread and the live ask is mirrored under
`Aims › Decision Now` when that owner declares this native/legacy surface.
New generic Pages keep targets and decisions in the owner's backstage records;
do not add an Aims section to their reading surface. Routing closes the row only after the person answered,
recording the option, who, when, and their words. An unanswered row waits.

**Cross-board ownership.**
Mechanical writes carry no judgement and are always allowed.
Editorial writes are never ours on a board that is neither the skill set nor the board being worked: there, the output is a report addressed to that board's owner, not an edit.

## 🎯 Where a GROUP-altitude input lands

Some findings are about a whole group rather than any one page in it: a status readout across its pages, a gap between what the group promises and what its members cover, a rename that would make the set legible.

It lands in the group's intro prose in `board.md`'s `## Pages`, at the section
boundary. Refresh an existing explicit Page lane block with `lanes.py` when
that helper applies to this group.

```
a finding about ONE page      →  that page's owning section
a finding about A GROUP       →  the group's intro in board.md ## Pages
a finding about THE BOARD     →  ## Topic, ## Pipeline, or ## Board Map
```

A group finding stays whole in the group's introduction. Page-specific
consequences may link to it from their owning Page fields.

## 🚪 When nothing fits

After checking actual membership and ownership, work with no owning Page
becomes a proposal for the appropriate Board kind.
Routing therefore ends in one of exactly three states:

```
LANDED     the write is on the owning page, and the reply names it
PROPOSED   no page owns this: routing drafts the page id, title, and group
           it would open, and waits; it never creates silently. If an existing
           governance Page owns the proposal, route its D<nn> thread there;
           otherwise return the pending Board-altitude proposal for approval
REPORTED   the owner is another family's board: a report, not an edit
```

**The handoff before the reply.**
After a source write, five conditions define a truthful handoff. The first and
fourth are human/browser judgements; the second
and third are mechanical checks:

```
①  WRITTEN BACK   every change has a record on the page that owns it
②  REBUILT        board.html came from the .md as it stands now
③  CHECKED        0 errors, and no page this round touched gained a warning
④  REACHABLE      the tab the person opens can run what shipped
⑤  STATED         the reply names which of ①-④ ran, with ③'s numbers
```

Run the current mechanical path after the write:

```bash
python3 <board-skill>/cli/build.py <board>
python3 <board-skill>/cli/check.py <board>
```

Whole-page semantic judgement belongs to `/haipipe-page-check`. It is
read-only and writes the check receipt; it never repairs the version it judged.
③ compares affected Pages, since concurrent sessions may change the Board
total. A warning introduced by this round blocks handback; standing warnings
are reported separately.
① and ④ remain explicit human/browser checks, because whether a change was
substantive and whether the person's own tab has the new assets cannot be
proven by a command. A handoff that reports an untested condition as complete
is worse than one that names the remaining judgement.
A round that changed PROSE also owes a cold read by `haipipe-board-reviewer-agent`; a round that changed only mechanics does not, since there is nothing for a reader to judge.
A failed gate is reported, never hidden. "The checker is red and here is why" is worth more than "done" and wrong.

**The reply contract.**
Name the end state and each write as `page id · ## section`. For a proposal
or report with no source change, say `Writes: none`; build/check/browser
conditions are then `not run — no source change`, not claimed as passed.
Summarize each pending Decision Now row with its ask and recommended option;
the full rationale and choices remain on the Page.

End with `Next: <actor and one concrete action>`, or `Next: none` when finished.
Continue authorized agent work yourself. Ask the person only for a missing
decision or an action that needs them. For example:

```text
State: PROPOSED
Writes: none
Next: person — review the proposed Page list and grouping
```

## 📂 Files

```
haipipe-board-routing/
├── SKILL.md            this contract
├── CHANGELOG.md        version history, including haipipe-board-index's
└── src/lanes.py        the per-group lane block, round-tripped
```

The page altitude owns no script: it is executed by the agent that loads this contract plus the two specs.
The board altitude owns exactly one, `src/lanes.py`, which arrived with `haipipe-board-index` on 260802; `regroup` wraps `haipipe-board/cli/regroup.py` rather than reimplementing it.
Reads and writes `board.md` and page `.md` files only, never the generated `board/` site.
History of the merged Board and Page routing contracts is in `CHANGELOG.md`.
