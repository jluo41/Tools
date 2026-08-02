# Convert a skill folder to a skill page
state: 🟡 PARTIAL
owner: JL
method: mirror `stage.py`: generate the page once, keep one managed block in sync, never touch what a human wrote

## Question
How should one independently versioned skill become a Board page that stays current and is still useful to discuss?

A bare link gives the reader nothing to assess, while a full copy starts drifting as soon as the skill changes.
The page must expose the live skill and its release history without surrendering its human-owned health judgment.
That makes skill activity visible beside the questions and decisions that affect it.
It succeeds when a resync updates every derived span and preserves every authored line byte for byte.


## Boundary
- ✅ Covered here
  **Turning a folder outside the board into a Q page**: what the generator derives, what it embeds, what it must never overwrite, when it re-runs, and how a stale generated page is detected.
- ↪ Covered elsewhere
  What a Q source file contains and which sections are recognized: `QAa0` and the QAa faces (QA2 merged into them 260729).
  How that page renders once it exists: `QAa0`.
  The `![[path]]` embed grammar itself: `ref/board-form.md` §5.
  How groups are proposed and named: `QA2`. Where the pages sit on disk: `QB1`.
  Whether the board should host skills at all, rather than how: that is this page's Question, and it is JL's.
  The skill pages this mechanism PRODUCES are the `Q-Skill` group; each is a roster row, not a ruling.

## Diagram

```
THE SOURCE (untouched, ships to other people)      THE PAGE (lives on a board)
skills/paper/0-enter/haipipe-paper-enter/          QA1-paper-enter.md
├── SKILL.md      name · version · summary  ──┐    ┌──────────────────────────┐
└── CHANGELOG.md  every version ever         │    │ # haipipe-paper-enter     │
                                              │    │ state: ✅ 0.6.6           │
                    ┌─── derived ─────────────┘    │ ## Question   what it owes│
                    │    (managed block,           │ ## Content               │
                    │     refreshed by sync)       │  <!-- managed:start -->  │
                    ▼                              │   version · tools · path │
              skillpage.py new                     │   ![[…/SKILL.md]]        │
              skillpage.py sync                    │   ![[…/CHANGELOG.md]]    │
              skillpage.py check                   │  <!-- managed:end -->    │
                                                   │ ## Items to Finish   ┐   │
  ZERO COPY: the embeds are read at BUILD time,    │ ## Where we are      │hand│
  so the page cannot go stale between syncs        │ ## Log               ┘   │
                                                   └──────────────────────────┘

── the precedent this follows, exactly ──
  stage.py new    writes the S page + its managed Stage Contract
  stage.py sync   replaces ONLY the marked span, never authored Content
  stage.py check  reports a stale contract-source-hash instead of rewriting

── the two ways to get this wrong ──
  copy too much  → 141 stale copies of skills that ship elsewhere
  copy too little → a bookmark: nothing to rank, comment on, or watch
```

## Content
### 1 · What the generator may derive
A skill's frontmatter already carries `name`, `metadata.version`, `metadata.last_updated`, `metadata.summary`, and `allowed-tools`, so those are facts, not judgments, and a script may write them.
The page title is the skill name and the `state:` line's readable suffix is its version, which makes the index row say `✅ 0.6.6` without anybody maintaining it.
Everything else the page shows is an embed rather than a copy: `![[…/SKILL.md]]` and `![[…/CHANGELOG.md]]` are read at build time, so between two syncs the page is still current.

### 2 · What the generator must never touch
`## Question`, `## Items to Finish`, `## Where we are`, `## Comments`, and `## Log` are written by people and are the only reason the page is worth more than an `ls`.
This is `stage.py`'s rule and it earned it: `replace_managed` rewrites only the span between its markers, and authored subsections have survived every sync since 260725.
A generator that reformats a human sentence once will not be trusted again, and the cost is not the sentence, it is that nobody writes the next one.

### 3 · The state line is a judgment, so a script may not set it
`state:` is the four-value machine token, and for a skill it means health: is this thing stable, in flux, unmaintained, or parked.
A version number cannot answer that, because a skill at `0.1.0` may be finished and one at `0.9.4` may be mid-rewrite.
So `new` seeds `🔴 OPEN` like every other page and a person changes it, while the version rides along as readable detail after the emoji.

### 4 · Staleness has to be visible, not silent
`stage.py` stores a `contract-source-hash` and reports drift instead of rewriting, and the same applies here: if `SKILL.md`'s frontmatter changed since the last sync, `check` says so.
Without that, a page claiming `✅ 0.6.6` beside a skill that shipped `0.8.0` is worse than no page, because it is confidently wrong.

### 5 · Where each generated thing goes, and why there
(JL 260726: the tree and workflow in Diagram, the skill in Content, the changelog in Log)
The derived material lands in three separate spans, because it answers three different questions and one block cannot straddle three sections.
`## Diagram` carries the folder tree, drawn with every file's own one-line purpose beside it, and below it an AUTHORED workflow fence, because a folder can be read off disk and an intent cannot.
`## Content` carries the whole `SKILL.md` in its own bytes, then `### The other files`, which DESCRIBES them rather than reproducing them.
`## Log` carries the skill's `CHANGELOG.md` underneath the page's own hand-written lines, which is where change history belongs and which leaves the dashboard's update count reading the hand lines exactly as it does on every other page.

#### One generator, two kinds of shipped unit
(JL 260727: "and also the agent as well")
This family ships a skill, which is a folder whose definition is `SKILL.md`, and an agent, which is ONE `.md` file whose changelog belongs to its `agents/` folder and is shared with its siblings.
Both carry the same frontmatter (`name`, `metadata.version`, `last_updated`, `summary`), which is why one generator covers both instead of a second script that would drift from the first.
Only the folder tree differs, so a single-file unit emits that span empty rather than omitting it: `sync` replaces spans it can find, and a missing one would report as an older page needing repair on every run.

#### Scope is this family, not every skill in the plugin
(JL 260727: "you should just focus on the skills on Tools/plugins/haipipe-toolkit/skills/board")
The roster covers `skills/board/` and nothing else, which is the family this board was opened to design.
A page generated for `haipipe-probe` was produced as a proof and deleted for this reason: a roster that reaches past its board's subject makes the board a directory of the whole plugin, and no one owns that.
The 141-skill question stays open below as a scope item, and it is a different decision from whether the mechanism works.

#### A sub-sub section is an ITEM at ONE level, because items do not nest
(JL 260727: "2 · 🧭 Session attachment ... I still collapse this")
Every numbered section is an item, so all of them fold, and the number carries the depth.
The first attempt made the unit's `##` a `####` paragraph heading and only its `###` children items, which left section 2 with no fold at all because a `.ph` never folds and an indented `- ` inside an item body is absorbed as that item's text rather than becoming a nested item.
The board has exactly one folding level inside Content, so two nested folds were never available; QA4 had already ruled that depth is read off the numbering and refused a third heading level for this same reason.
Verified on both pages: 19 collapsible sections on the skill, 4 on the agent, and zero non-folding paragraph headings left.

#### A blank line closes an item, so an item body may not contain one
(the bug JL caught twice: `1 · 🗂 Shape`, whose heading was still Chinese at the time, folded down to its opening figure and dumped the rest of the section onto the page)
`body.py` calls `flush()` on a blank line, and `flush()` CLOSES the open item.
`SKILL.md` is written one sentence per line with blank lines between blocks, so the first blank line inside a converted section ended the fold and everything after it rendered as literal `- ` and `**bold**` text at 6-space indent.
A first fix guarded only the line immediately after the item head, which is why the symptom moved rather than went away: the fold now opened, and closed again at the next blank line.
Blank lines are dropped everywhere inside an item body and kept inside a fence, and the cost is nothing: the body is a list of rows and each row already renders on its own line.
The lesson generalizes past this page: the item form was designed for a hand-written explanation of a few lines, and feeding a whole document through it exposes every boundary condition at once.

#### Rendering a shipped file exposes the renderer, not the file
(two defects found this way, both older than this page and both on every board)
`inline()` held code spans out of the mark pass so `**` inside them would stay literal, and that same split cut every mark that SPANS a code span, so `**run `check.py` now**` rendered as literal asterisks.
It had been broken since the split was written and nobody had met it, because hand-written board prose rarely bolds a phrase containing a path.
`SKILL.md` does it constantly, so converting one file surfaced 13 instances immediately; code spans are now stashed behind a sentinel, the marks run over the whole string, and the spans go back afterwards.
The other one is the source's own wrapping: a long bold phrase legitimately spans two source lines, and one row per line leaves each half with an unclosed marker, so `join_wrapped` rejoins them rather than asking a shipped skill to be rewritten for a display.
Every board in the repo was rebuilt on the fix and none regressed.

#### The version rides the TITLE, never the filename
(JL 260727: "could you add the version after haipipe-board as well?")
The title reads `haipipe-board · v0.41.0`, which is what the index row prints, so the shipped version is legible from the front page without opening anything.
An earlier pass put it after the `state:` emoji, and that was wrong for a reason worth keeping: `state:` holds a health judgment a person makes, so a derived value beside it makes a machine number and a human one compete for the same line.
The FILENAME never carries the version, because a name that changed on every release would break every link to the page, and links to a roster row are exactly what other pages will write.

#### A sub-sub section is an ITEM, because items fold and headings do not
(JL 260727: "for its subsubsection, could we make it collapse as well")
The skill's `##` stays a `####` paragraph heading, visible on stage, and its `###` becomes `- N.M · title` with an indented body, which is the board's item form and therefore a real `<details>`.
A `#####` heading renders as `.ph`, which never folds, so the previous shape gave eleven sub-sub sections no way to collapse.
One thing bit immediately and is worth recording: a blank line between an item and its body ENDS the item, so the first attempt silently flattened all eleven back into prose while the markdown still looked correct.
Numbering keeps carrying the depth either way, which is QA4's `§6` against `§6.1` rule.

#### The file is one subsection; the file's own sections are sub-sub sections
(JL 260727: "SKILL.md as a subsection in the Content, and the section in the SKILL.md will be sub-sub section")
`## Content` gets one `### SKILL.md` division, and every heading inside the skill moves two levels down inside it.
A first pass promoted the skill's own `##` straight to `###`, which scattered nine unrelated divisions across Content and lost the fact that they are all one file.
The board renders exactly two Content levels and `#{4,6}` all render identically, so depth cannot come from the heading level.
It comes from NUMBERING, which is the rule QA4 already fixed for manuscript sections (`§6` against `§6.1`) and the reason a third heading level was refused there: the skill's `##` becomes `#### N ·` and its `###` becomes `##### N.M ·`, the same size on the page and an unambiguous hierarchy in the text.
So a section reads as `3` and its eleven verbs read as `3.1` through `3.11`, which is the structure the skill actually has.
An embed was one opaque block with one fold, one copy button, no per-section anchor, and nothing a comment could be pinned to.
As real subsections the reader folds them individually, the Content heading counts them, and a remark can be pinned to a sentence of the skill exactly as on any hand-written page.
This is a COPY, which the board normally refuses, and it is safe for the same reason `stage.py`'s contract block is: it lives inside a managed span whose hash `check` verifies, so drift is reported rather than possible.
Fenced blocks pass through byte for byte, which is load-bearing here: `SKILL.md` contains a page-anatomy figure whose lines start with `## `, and demoting those would have rewritten 14 lines of a diagram into headings.

#### The skill file must not sit behind a fold
(JL 260726, reading the first page: "we cannot see the content of SKILL.md")
Three things hid it at once, and only the third was the real one.
The machine markers printed on the page as literal text, because `strip_notes` keeps `<!-- haipipe:… -->` on purpose so the scripts can find their spans; they are now dropped at RENDER, so the file keeps its markers and no reader ever meets one.
`.embed.src .emb` clamped the embed to `34em` with its own scrollbar, which turned a 517-line file into a peephole competing with the section fold the reader already controls.
The real cause was that a direct `###` inside `## Content` is a DIVISION and a division renders collapsed, so the one thing the page exists to show was the one thing behind a click.
The skill file now sits directly under `## Content` with no heading of its own, and `### The other files` stays a division because it is supporting material.
The general form is worth keeping: on a page whose subject is one artifact, that artifact is not a subsection of the page.

#### Described, not reproduced
(the first attempt embedded `ref/` in full and JL cut it back)
Only `SKILL.md` is the skill's content; every other file is named, sized, and given the purpose line the file itself states.
A page that reproduced the folder would be a slow mirror of something that already exists, and the reader would scroll past the skill instead of reading it.
The manifest sits in a fence rather than a bullet list, because its purpose lines are verbatim quotes carrying other files' punctuation, and "fixing" a quote to satisfy the prose checker falsifies it.

### 6 · The changelog is CONVERTED into Log lines, not embedded as a file
(JL 260727: "copy and convert the content of Changelog to the LOG as well")
Convert, not embed, and the difference is the whole point of the section it lands in.
`## Log` has a grammar the board already reads: `YYMMDD · what changed`, newest first, with indented continuation lines that `sort_log` carries along with their head line.
A CHANGELOG entry is the same fact in a different notation, so a `## [version] · date · title` heading plus its bullets becomes one dated Log line plus its indented detail.
Translating it makes the skill's history first-class board content instead of a foreign document parked inside a page.

#### What conversion buys that an embed cannot
(58 releases became 58 updates the dashboard can see)
The ACTIVITY dashboard counts one update per dated `## Log` line, so an embedded changelog counts as zero and a converted one puts every release the skill ever shipped onto the fourteen-day strip and into the Board to Group to Page ranking.
Measured on the first page: QB6 went from 1 update to 59, and the board's total from 507 to 566.
This is the answer to the question that opened this page, and it only works because the conversion produces the board's own grammar rather than a quotation of somebody else's.

#### A generated span is not the board's prose
(79 style warnings in one pass, every one of them about a quote)
Converting the changelog immediately produced 65 em-dash and 14 CJK warnings, because older entries were written before those rulings and some are bilingual.
The board did not write that text and cannot fix it without falsifying a quote, so `check.py` now skips prose-style rules inside any `<!-- haipipe:… -->` span while keeping every structural check.
That exemption belongs to the mechanism rather than to this page: a stage's inherited contract is quoted material for exactly the same reason.

### 7 · What this buys, stated as a number
The ACTIVITY dashboard counts one update per dated `## Log` line per page, so a roster of skill pages ranks skills by how much they changed.
Today that question needs 141 changelogs read by hand; after this it is one strip and one ranked tree on an index.

## Items to Finish
### Rulings awaiting JL
- [ ] 🧠 JL rules whether the board hosts skills at all
      A board's pages have always been questions somebody owns, and a skill page is a different kind of thing: a roster row.
      This closes either way, including "no, a roster is not a board".
- [ ] 🗂 The grouping is decided before 35 files land in one folder
      A single flat group would mean 35 pages in one folder, which is the wall `QB1` just removed.
      The skill tree already has groups (`0-enter`, `1-lifecycle`, `2-phase`, `3-deliver`, …), so the likely answer is one board group per skill sub-family.
- [ ] 🎯 Scope: this family only, or every skill in the plugin
      Settled for THIS board on 260727: `Q-Skill` covers `skills/board/` and nothing else, because a roster that reaches past its board's subject makes the board a directory of the whole plugin.
      Still open: whether each other family gets the same group on its own design board (paper 35, task 44, application 23, discovery 15), or one roster board carries all 141.

### The generator, built and proven
- [x] 🏷 The generated pages get their own named family and group
      Ruled 260727: a skill page is `Q-Skill-<skill-name>.md` in a `Q-Skill/` group, not a numbered id.
      A numbered id says a skill page is the first of a queue; `Q-Skill-haipipe-board` says which skill it is, which is the only thing a reader wants from the id, and it stays greppable across the repo.
      This is the same shape as the named S families and closes for the same reason: a roster row is identified by WHAT IT IS, never by a position.
      `parse.py` now recognizes `Q-<Family>-<rest>` as a named Q page, so the id and the page title agree without a number in between.
- [x] 🔨 `skillpage.py` with `new` / `sync` / `check`
      Built 260726 and proven on `haipipe-board` itself as `QB6`, which is the right first subject: if the tool cannot describe the skill that generated it, it describes nothing.
      `new` seeds the page and lists it under its group, `sync` replaces only the marked span, `check` reports a stale derived hash with the exact command to fix it.
      Verified: the page carries one `### SKILL.md` division holding 9 numbered sections and 11 numbered sub-sections, sync is idempotent, a version bump is caught by `check` with `saved != current`, and the authored workflow fence plus the hand-written Log line both survive a sync that really rewrites all three spans.
      The managed marker carries the skill's folder as well as the hash, because `sync` used to recover the folder from the page's embed line and that line vanished the moment the skill file became real subsections: a machine span must not depend on rendered content to know its own source.
- [x] 📐 The managed/authored split is written down before any code
      Derived and owned by the script: name, version, last_updated, summary, allowed-tools, folder path, and the two embed lines, all inside `<!-- haipipe:skill:start <hash> -->`.
      Never touched: Question, Items to Finish, Where we are, Comments, Log.
      Proven rather than asserted: two sentinel lines were written into the authored sections, the skill's version was bumped so sync had real work, and both sentinels survived while the version changed.
      The marker only counts at the start of a line, because this very page quotes it in prose and a substring test reported the ruling page as a broken skill page.

### The fresh-reader test
- [ ] 🧪 One generated page is read by someone who did not generate it
      They must be able to say what the skill does, what version it is, and what it still owes, without opening the skill folder.

## Where we are
One page exists and the mechanism is proven; the ruling and the scope are not.
`QB6` is the skill page for `haipipe-board`, generated by `skillpage.py` and syncing from `skills/board/haipipe-board/`.
Four items remain and the first is still the one that decides the rest: whether a roster of shipped deliverables belongs on a board whose every other page is a question somebody owns.

- 260726 CC · 🧪 Proven on the skill that generated it
  `haipipe-board` was the first subject deliberately: a tool that cannot describe its own skill describes nothing, and the failure would have been immediate rather than discovered on skill 40.
  The page went from 4,132 rendered characters to 132,256 once the embeds resolved, and every one of those characters is read from the skill folder at build time.
- 260726 CC · 🪞 A skill page renders the skill's BYTES, because the first one executed its own documentation
  `haipipe-board`'s SKILL.md documents board syntax, so embedding it rendered that documentation AS board syntax: a markdown link written there to SHOW what a link looks like became a real link, and a permanent `dead-href` ERROR on the board.
  Switched both embeds to `![[…|source]]`, which `board-form.md` §5 already offers, and the ruling generalizes past this one skill: a `SKILL.md` is instructions to an agent, so its bytes are the artifact and a prettified render is a lossy view of it.
  It also removes a whole class of future surprise, because no skill's examples can ever be executed by the page that displays them.
  A board that ships with one permanent ERROR teaches people to ignore errors, which is the real reason this could not be left as cosmetic.
- 260726 CC · 🕳 The embed refuses `..`, and said so on the page
  The first generated page emitted `![[../../board/haipipe-board/SKILL.md]]` and rendered two `⚠ embed not found` blocks, because `page_stage._find` refuses `..` and absolute paths by design and walks up from the board folder instead.
  The right token is what an ancestor sees, `board/haipipe-board/SKILL.md`.
  This is the embed contract earning its keep: it never fails silently, so a wrong path was visible on screen in one build rather than shipping as an empty section.
  `sync` now resolves the token by walking the identical ladder, because a page that renders one file while sync reads another is a disagreement no test catches, since both halves work alone.

- 260726 JL · 🌱 Opened from the activity dashboard, not from the skills
  The question arrived because the dashboard now ranks pages by updates, and JL asked what it would take to rank SKILLS the same way.
  That order matters: the roster is wanted for an answer it enables, not because 141 folders felt untidy, which is the difference between a page that gets read and one that gets generated and abandoned.

### Decision Now
These are the calls only JL can make; CC ticks nothing here.

- [ ] 🧠 Rule whether the board hosts skills at all
      The page records that this closes either way, including "no, a roster is not a board".
      A tick here also closes the same row in Items to Finish.
- [ ] 🗂 Decide the grouping before 35 files land in one folder
      The page's stated likely answer is one board group per skill sub-family, mirroring the skill tree's own groups.
      A tick here also closes the same row in Items to Finish.
- [ ] 🎯 Settle the scope beyond this board
      The options the page records: each other family gets the same group on its own design board (paper 35, task 44, application 23, discovery 15), or one roster board carries all 141.
      A tick here also closes the same row in Items to Finish.

## Files
### The precedent to mirror
- `stage.py`
  The precedent: `new` / `sync` / `check`, `replace_managed`, and the source-hash staleness report. Read this before writing anything.
- `src/stage_contract.py`
  `managed_span` and `replace_managed`, the 98 lines that make "never touch what a human wrote" true rather than intended.

### Input files
- `ref/board-form.md`
  §5 for the `![[path]]` embed grammar this depends on; §4 for which sections are recognized.
- `Tools/plugins/haipipe-toolkit/skills/`
  The source: 141 `SKILL.md` files in 10 families, each already carrying name, version, last_updated, and summary.

## Glossary
managed block: a span between `<!-- haipipe:...:start -->` and `:end` that a generator owns; everything outside it belongs to whoever typed it.
roster page: a page whose subject exists independently of the board, unlike a ruling, which exists only as the question it asks.

## Log
260801 0140 · Full renumber QC5a -> QC3a (JL forced 260801)
260801 0130 · Reindexed QC5 -> QC5a under the new QC5 generator parent (JL 260801)
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
