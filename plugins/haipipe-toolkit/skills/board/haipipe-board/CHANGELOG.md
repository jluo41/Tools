
## Unreleased — 2026-08-16

The page lifecycle's phase token and the first check on built page artifacts.

- `src/page_lifecycle.py`: `PHASES`/`LEGAL_ROUTES` speak EVIDENCE; `phase_token()`
  normalizes the retired `PROBE` on every phase and route read, including
  `traversed_edges`, so receipts written before the rename audit identically.
- `src/page_context.py`: `Related Board Pages` rows parse `EVIDENCE` and `PROBE`
  and both resolve to the same phase.
- `assets/js/10-drawer/65-plugin-pageflow.js`: the stepper's second door is
  EVIDENCE, every phase read goes through `phaseId()`, and each door's job line
  now says what that phase DELIVERS.
- NEW `src/page_evidence.py`, wired into `cli/check.py`'s per-page pass: reports
  the gap between what a page promised and what it built. Seven findings across
  two independent axes plus `display-declared-no-claim`: VISIBILITY (declared-not-rendered, cited-not-embedded,
  rendered-not-cited) and PROVENANCE (intake-unfrozen, accept-stale), plus
  latex-untitled and projection-stale. Driving it against the two live CMS
  boards is what separated the axes and what taught it the second legal
  citation form (`<stem>-DisplayN`), which the first draft called uncited.
  Written from the QV2-lbp-regression-results failure, which passed every
  existing check while shipping three of five tables to nobody.
- The unit README parser reads all FOUR dialects on disk (`- claim:`,
  `claim:`, `**Claim**:`, `- **Kind:**`) and aliases `Reader job`/`Evidence` to
  the contract's `caption-job`/`intake`. Reading only the bullet form called 25
  correctly-documented units litter and hid every `accepted:` tick, one of which
  is genuinely stale. ⚠️ `live/plugview.py:122 _readme_rows` still has the
  bullet-only rule, so the 🖼 tab shows those units with no claim, kind, or
  acceptance state; left alone because that file is another session's open work,
  and the two should share one parser.
- NEW `tests/test_page_evidence.py` (18 cases) reproduces that failure as a
  fixture; `tests/test_page_lifecycle.py` gains EVIDENCE coverage and an
  alias-equivalence case. 204 pass.

haipipe-board — Changelog
=========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

**v0-series rule (JL, 2026-07-23):** this skill stays on `0.x.x` — **it never goes to 1.0.0 without JL's explicit say-so.** Everything here is provisional: the board form, the Q template, the generator's output. Ship `0.MINOR.PATCH` freely; `1.0.0` is a decision, not a milestone that arrives on its own.

## 0.140.1 - 2026-08-17

- Updated the cross-family Page Type roster to sixteen variants across six
  owners: Task adds Insight; Application adds Brief, Intervention, and Artifact.
- Recorded the global-key rule behind the names: Application does not reuse
  Paper Opening or Board Design.
- Extended `cli/check.py`'s executable Page Type registry with the previously
  omitted Paper `venue` plus `insight`, `brief`, `intervention`, and `artifact`,
  so declared Pages resolve through step ③ instead of silently falling back to
  filename inference.

## 0.140.0 - 2026-08-16

- 🗑 THE FOCUS TIMER IS DELETED (JL 260816: "remove all the things related to
  .haipipe-board, but still keep the activity tracker for the logs"). This
  closes QB2's standing Decision Now row on option A. Gone: the
  `activity_spans` and `activity_ticks` tables, `activity_conn`,
  `activity_num`, `activity_day_parts`, the `start`/`pulse`/`stop` ops, the
  282-line browser beacon in `assets/js/50-activity.js`, and the 576K
  `.haipipe-board/activity.sqlite3` itself. `live/activity.py` 446 → 283
  lines, the script 282 → 167.
  The evidence it was dead: every SELECT against those two tables was the
  timer reading its OWN rows to write the next one, and `activity_stats` was
  handed the connection on every request and never touched it. JL had ruled on
  260726 that the unit is UPDATES, not time, so it had been measuring the
  wrong thing and storing it for nobody for three weeks.
  `import sqlite3` then went from seven files — `serve.py`, `base.py`,
  `chat.py`, `structure.py`, `term.py`, `write.py`, `xcal.py` — where it was
  already unused in all seven, a leftover of the copied import header from the
  260731 serve.py split. SQLite had entered this codebase only for the timer
  and now leaves with it. `.haipipe-board/` keeps `sessions.json`, which is
  chat and terminal session history and has nothing to do with any of this.
- 🐛 THE READOUT WAS SHOWING 82% OF THE WORK, and the deletion is what found
  it. `LOG_LINE` matched `^(\d{6})` with no list marker allowed, so a
  `## Log` written `- 260806 2215 · [REVISE-CC] swept` did not count while
  `260803 · EXECUTED` did. Both shapes are written on live boards: 1260
  counted, 276 dropped across the five skill boards. Now `^[-*]?\s*`.
  Nothing caught it because all six tests on this route tested the timer.
  They are replaced by five that test what the panel prints: one dated line is
  one update, an undated line is not, a dated line outside `## Log` is prose,
  the route takes no op but `stats`, and no state is written anywhere. The
  last one is the guard that keeps `.haipipe-board/` from growing a database
  again.
  One coupling had to be undone first: the beacon was also what FETCHED the
  readout — every heartbeat returned the stats and the panel drew them — so
  the display was given a request of its own, one POST on load and one on
  `board:updated`.

## 0.139.2 - 2026-08-17

- Corrected the live Page Type roster to twelve variants across five owning
  skill sets: Board 4, Paper 5, Task 1, Subjective Label 1, and View 1.
- Added Paper Opening and the previously omitted Task type; removed the retired
  Paper display, literature, value, and per-family dash types from the roster.
- `cli/check.py` now recognizes `page-type: opening` and `page-type: task` rather
  than warning that those live contracts are unknown.

## 0.139.1 - 2026-08-16

- 🗑 THE VIEW BOARD IS RETIRED (JL 260816). `01-haipipe-view-260810` and its
  212 files are gone, and nothing replaces them: while the refold gave every
  other board a new name — `ApplicationSkillBoard-260802`,
  `PaperSkillBoard-260725`, `TaskSkillBoard-260726`,
  `SubjectiveLabelBoard-260722`, and `BoardSkillBoard-260722` renumbered in
  place — this one was not carried across. That is the decision, not an
  oversight, and it is written down here because a board that simply stops
  appearing in `diagrams/` otherwise looks like a board someone lost.
  The skill it documented is untouched and still ships at
  `skills/view/haipipe-view/`. To read the retired board, check out any commit
  up to `671847d6`.

## 0.139.0 - 2026-08-16

- 📁 `cli/refold.py`: ONE PAGE, ONE FOLDER, as a command. The shape was ruled on
  260815 and the engine has read it ever since (`_page_home()` is
  `<name>/<name>.md`, `_in_plugin()` keeps discovery out of every other
  subfolder, and `check.py` climbs to the board root so a folded page's
  board-relative Files rows still resolve). What was missing was the migration,
  so a board that wanted the shape had to be moved by hand, page by page, and
  the paper board's 73 pages were still flat a day later. `regroup.py` decides
  which GROUP a page belongs to; this decides that the page gets a home of its
  own, which is what gives its plugins somewhere to live.
  It moves the page-keyed material in with the page — the group had been
  holding it side by side, `display/<page>/`, `QA-probe/<page>/`,
  `draw/<id>.excalidraw` — and preserves the INNER path rather than flattening
  it, because a display unit is addressed by its own folder name and a QA-probe
  record names its evidence page by the drawer it sits in
  (`src/topic_entry_contract.py` reads `parts[-2]`). Re-parent, never rename:
  renaming belongs to whoever owns that contract.
  Then the paths. A page one level deeper is a page whose every relative path is
  one level short, so the rewrite is part of the command: a token is re-anchored
  when it RESOLVES today, from the file (broken by the move even when its target
  never moved) or from the board root (survives the move, breaks only when its
  target moved). A path that answers to neither anchor is already dead and is
  left exactly as it is, because guessing at what it meant is how a dead path
  becomes a plausible wrong one. That one test is also what keeps prose in
  backticks from being mistaken for a path: prose does not resolve.
  Run on the paper board: 83 moves, 49 files rewritten, same 73 pages
  discovered, no new error, and five `stray-scene` warnings gone because a
  page's drawing is now inside the page. Verified against a copy first, by
  diffing the check output before and after in the same location.

## 0.138.1 - 2026-08-16

- 🔡 `check.py`'s group-heading pattern reads a lowercase TAIL, not one
  lowercase letter. `### QCskill · Engine skills` on the paper board was read as
  key `QCs`, which matched no folder, so that group dropped out of the count and
  every folder after it was told it was numbered one too high
  (`8-QF-execute` "numbered 8 but QF is #7"). `regroup.py` had always accepted
  the wider key, so the two writers of the same rule disagreed; they now match.

## 0.138.0 - 2026-08-16

- 🔢 A GROUP FOLDER CARRIES ITS PLACE IN `## Pages` (JL 260816, on finding
  `QC-engine/` sitting four rows above `QPs-page-structure/` in a listing whose
  board.md read them the other way round). Letters carry identity and cannot
  carry order, so the folder is now `<N>-Q<letter>-<slug>`, `7-QC-engine/`.
  What was weighed and rejected first: renaming the LETTERS so ASCII sorts them
  (`QC→QT`, `QO→QU`) touches 1594 id mentions across 43 pages, needs 43 `##
  Links` rows to keep the old ids resolving, cannot order `QPs`/`QPf`/`QPw`
  without destroying the s/f/w mnemonic, and spends all of it on the one thing
  colleagues actually cite. Numbering touches 206 path strings and nothing
  cites a folder.
  `## Pages` stays the ONLY authority; the number is DERIVED from it. New in
  `src/common.py`: `group_stem()` strips the number before anything reads the
  letter (so an unnumbered board keeps working with no migration) and
  `board_is_numbered()` answers whether this board opted in. Four readers strip
  through it — `live/chat.py` `group_folder()` + the group session prefix,
  `live/term.py`'s group terminal title, `cli/sentencerun.py`'s page URL — and
  the generated route is unchanged, `7-QC-engine/` still renders to `board/QC/`.
  Two writers, one rule each: `cli/regroup.py` always numbers, because it lays
  the whole set down at once and `groups_of()` now carries each heading's
  reading-order position; `＋Q` in `live/structure.py` numbers only when the
  board already does, so a legacy board never grows one numbered folder among
  eight bare ones. A board is numbered or it is not, and no writer may
  manufacture the middle.
  `cli/check.py` `check_group_order()` holds board.md and disk together:
  `group-number-order` when a folder's number disagrees with `## Pages`,
  `group-number-missing` on partial numbering, one `groups-not-numbered` WARN
  for the pre-260816 shape. A paper's `0-lifecycle/` is exempt by construction:
  a folder counts as a GROUP folder only when its name minus the number starts
  with a `Q<letter>` board.md declares, so `0-seed/` and `1-work/`, whose
  numbers carry lifecycle order, answer to a different rule and are not read
  here. Verified on four fixtures (wrong number, partial, lifecycle, flat
  regroup) and against the four live design boards, which report the migration
  WARN and no errors. Recorded on the board as QPf1.

## 0.137.0 - 2026-08-16

- ↕ A BOTTOM PANEL CAN BE RESIZED (JL 260816: "我好像没有办法按照上下的幅度去
  change 这个 workflow split size"). The shell's columns each got a hairline
  grabber the day the split shipped; the bottom panels never did, so both
  opened at a fixed 58vh — too tall for a four-row index, too short for a long
  run trail. `07-panel-resize.js` gives one top-edge grip to both `#wfpanel`
  and `#pfpanel`, drag to size, height persisted per panel id the way the
  column widths already are, double-click to reset. One owner, both panels: a
  second copy of drag-and-persist is how the two would drift.

- 📄 Page phases PANEL: the 🪜 Workflow menu's second member arrives, the one
  the registry reserved the seat for. `65-plugin-pageflow.js` shows the
  DRAFT/PROBE/REVISE/CHECK loop with the INDEX on the LEFT and content on the
  RIGHT (JL 260816: "把 workflow 放在最左边…跟具体的内容分开" — the first cut
  put each phase's job sentence inside its strip cell and scrolled off the
  screen): the index holds ①–④ phase names only, marks ▲ here / · next, and a
  ×n visit count; the right column holds the selected phase's job + contract
  and the run record. Reads ONLY the RUN receipts under `_runs/page/` through
  the new `GET /_board/pageruns` (`live/pageruns.py`, matched by the receipt's
  own `page` field, never the folder name). No receipts is an answer, not an
  error: the panel states the run contract's entry rule (existing page →
  CHECK, new page → DRAFT). NO locks — the loop has none. v1 is read-only; its
  one action is the labeling stepper's smallest — the
  `/haipipe-page-workflow run …` command shown and copyable, never executed.
  `#pfpanel` wears the same wf-* frame as `#wfpanel`; the two bottom panels
  close each other (one bottom, one occupant). Tests: `test_pageruns.py`.

## 0.135.0 - 2026-08-16

- 🛠 Skill FLATTENED to a ranked list (JL: "maybe we don't need to have
  these concept … we just need to show these skills and the user can drag
  and rank them themselves"): the uses/designs relations, the aligned ✓
  with drift dates, and ↑ designs came out of `live/skillmap.py` whole.
  The store is now `- <name>` rows whose ORDER is the person's rank (top =
  most related); the index cards carry a ⠿ handle and drag-to-rank saves
  through the new `POST /_board/skill-order`; `/_board/skill-verify` is
  removed; the pen (`/_board/skill-entry`) now does add-at-top, ✕ remove
  (the ` · removed` tombstone a refresh never re-seeds), ↩ restore, and
  note. Old-grammar stores parse cleanly and migrate on the next write;
  all 15 live stores were migrated in place, preserving the designs-first
  order the person saw as the initial rank.

## 0.134.0 - 2026-08-15

- 🔍 Skill: the whole split, one skill, with ← → (JL: "open a new small tab,
  the whole split should be the skill, like the display split, with ← and →").
  The 🛠 workbench card's NAME now posts to the shell instead of expanding an
  inline iframe; the shell stages a 🔍 Skill pseudo-tab framing
  `/_board/skillview`, remembered per page and offered from ＋ once staged.
  `serve_skillview` gains `?map=<the page's store>` and renders a ← → bar
  walking the page's skills in card order (designs first, then uses), with
  arrow keys live, the way a deck walks its slides. A standalone workbench
  falls back to opening the view in a browser tab.

## 0.133.0 - 2026-08-15

- The WORD export reads paragraph per paragraph (JL: "it should not be the
  sentence per paragraph"): `--join-paragraphs` rides every board export,
  so the source's one-sentence-per-line grammar stops at the writer and a
  coauthor gets flowing prose. QPf7 carries the ruling as contract.

## 0.132.0 - 2026-08-15

- The WORD export cites from the page's own bib too (JL: "how about the
  word? will we have the reference as well?"): when `bibex/<stem>.bib` holds
  an entry, `cli/refs.py` compiles `.board-refs.bbl` in bibex/ (rebuilt when
  the bib is newer) and md2docx is pointed there — the .docx and its PDF
  twin gain the in-text "(Luo et al. 2026)" and a real References section,
  from the same store as the chip, the block, and the LaTeX PDF. The paper
  root stays the fallback for pages with no store.
- md2docx's .bbl parser now reads plainnat's bare `\bibitem[label]{key}` as
  well as misq's braced form — demanding the braces made every plainnat
  bibliography parse to nothing and cites print bare keys (fixed in the
  paper family's own script; the paper path benefits identically).

## 0.131.0 - 2026-08-15

- The LaTeX export cites from the PAGE'S OWN BIB (JL: "convert it to the
  latex and this one to be cited as well"): the master's bibliography now
  prefers `bibex/<stem>.bib` when it holds an entry, falling back to the
  paper's `0-*.bib`, then cite-less. QPf8's PDF proves it end to end:
  `\citep{luo2026eventglucose}` compiles to "[Luo et al., 2026]" inline
  with a bibtex References page, one store feeding chip, block, and PDF.
- Built pages gained a 📚 References block above the folds
  (`src/page_question.py` + `assets/css/64-refs.css`): one numbered entry
  per cited key, authors (year), title, venue, doi/link, resolved from the
  page's own bib and never invented. The inline chip + card stay body.py's;
  this is the other half of what a citing page owes its reader.

## 0.130.0 - 2026-08-15

- The BibEx ＋ box learned LINKS (JL: "could we paste the paper link"): a
  DOI (doi.org content negotiation), an arXiv link or bare id (arxiv.org's
  bibtex endpoint), Scholar's session-signed Cite → BibTeX link, or any
  paper URL (Semantic Scholar fallback). The bibtex is fetched WHOLE from
  the source — copying, never composing — and fills the box for the person
  to review; landing stays their second click. An unusable fetched key
  (doi.org's URL-as-key) is renamed surname+year, a local-handle repair.
- The un-cited chip now reads "in the bib, not cited in the page text yet"
  and carries 📋 copy \citep{key}, after "added but not synced" confusion.
- The whole raw .bib renders in a fold at the view's foot with its on-disk
  path — it is PRIMARY material and hand-editing it is legal.

## 0.129.0 - 2026-08-15

- BibEx became a CITATION WORKBENCH on a PAGE-OWNED bib (JL: "the bib for
  this page only"). `bibex/<stem>.bib` is now PRIMARY — the page's own store,
  seeded by copying entries whole from the paper's `0-*.bib`, which is read
  and never written — and a refresh only appends imports, never overwriting
  or deleting an entry a person may have edited.
- The card view gained the working surface: parsed title/author/year, 🔎 a
  Google Scholar link built from the title, 🔗 DOI and 📄 URL when carried,
  ✅/⬜ checked status with a ✓ button, an ✎ edit fold per entry, and a ＋
  paste box for new entries.
- Two new doors beside `/_board/bibex`: `bibex-verify` writes the human ✓ as
  a `verified = {WHO YYMMDD}` field INSIDE the entry (JL picked the field
  over a sidecar; undo strips it), and `bibex-entry` is the pen — it lands a
  person's pasted bibtex verbatim, validates shape only, guards duplicate
  keys behind an explicit replace, and composes nothing (citation-craft.md).
- The key scan strips code fences and backtick spans first: a cite in a
  figure or a rule's quotation is an illustration, not a citation.

## 0.128.0 - 2026-08-15

- The right pane's tabs became an OPEN SET, per page (haipipe-plugin):
  the strip renders from the set, a tab appears on an explicit click — the ＋
  menu lists what the page could open, with ● where material already exists —
  the active tab carries its own ✕ (out of the set, focus to the left
  neighbour, last one closes the pane), and the pane's `✕ close` keeps meaning
  the whole pane. The set persists per page in `board-split-tabs:<path>`.
- Registry entries may carry `tab: {url(page), write(page,cb,err)}` and the
  shell builds their tab from it, so plugin N+1 ships by registering; Draw and
  Slides keep their window hooks for now.
- Three DERIVED paper-facing plugins shipped through that spec
  (`82-plugin-exports.js` + `live/export.py`): `/_board/latex` (md2tex + a
  standalone xelatex master → `latex/<stem>.pdf`), `/_board/word` (md2docx +
  docx2pdf's PDF twin → `word/<stem>.docx` + view), `/_board/bibex`
  (extract-only subset of the paper's `0-*.bib` → `bibex/<stem>.bib` + cards;
  never invents an entry, per citation-craft.md). `--paper-root` is discovered
  by walking up for a `0-*.bib`; pages outside a paper export cite-less.
- The contract itself is the new `board/haipipe-plugin` skill
  (SKILL.md + ref/roster.md): a plugin is STORAGE + SURFACE + WRITER +
  BOUNDARY, named once in the roster.

## 0.126.0 - 2026-08-09

- The door's sub-skill roster now lists the FIVE Page Type variants this skill
  set owns and points at `paper/page-types/` and
  `subjective-label/skills/page-types/` for the other six. It had named three
  since the variants were introduced.
- Records the per-skill-set ownership rule (JL 260809) and both superseded
  rules, so neither returns.
- Adds the operational warning the move exposed: relocating a variant does not
  relocate its installed symlink, so `install.sh --global` (repo root) must be re-run
  or the skill silently stops resolving. Five skills were dead this way between
  the move and the reinstall.

## 0.124.0 - 2026-08-06

JL's final evidence-page design (ruled 260806) executed:

- "evidence page" is the collective name for the for-literature and for-value
  types; the type key is now ONE head line, `route: outward | inward`, right
  after `owner:`/`method:`, replacing the retired `### Q-consumer register`
  marker + register route line
- the page organizes Content BY EXECUTOR: one `### E<n> · <question>` division
  per Q-executor conversation (🔗 QA-probe pointer + `#### consumers` rows +
  `#### answer digest`), plus the standing `### E0 · incoming` collect queue;
  one E<n> division ↔ one QA-probe; many QA-probes ↔ one QA-bank
- `ref/topic-entry-contract.md` rewritten to that shape; word order finalized
  (QA-bank / QA-probe); the four slot words are CAPITALS everywhere including
  heading slots (`#### Q-executor`, `#### A-executor`; `consumer trace` and
  `bank binding` stay lowercase)
- `src/topic_entry_contract.py` re-keyed: topics detected by the head route:
  line; capital slot headings canonical with lowercase accepted as a
  `topic-entry-heading-case` WARN; new `topic-probe-division` ERROR enforces
  the 1:1 E<n>↔record link
- chips re-anchored (src/body.py EDIV_TITLE + page-scoped EVIDENCE flag,
  src/page_question.py, src/parse.py `route:` head key): binding tokens chip
  inside E divisions of evidence pages only; Log stays chip-free
- tests updated (test_register_chips, test_topic_entry_contract; 137 green)

## 0.123.0 - 2026-08-06

**Probe entries become hidden SOURCE RECORDS** (JL ruling B, 260806: "an entry is a source file the topic page points at, like a PDF; the board renders the topic page, never the entry"). `ref/topic-entry-contract.md` rewritten: an entry is a RECORD, not a Page. No page frame (no `state:` header, Opening, Aims, States, Log, or gate); just a `# title` line, a `requires:` line, and the four slots (`#### q-executor` · `#### consumer trace` · bank binding with `**route**`/`**bank**`/`**target**`/`**state**` · `#### a-executor`). The naming law is now stated with its mechanism: `<n>-<slug>.md`, digit first, `<n>` restarting at 1 per `probes/<topic>/` folder, hidden precisely because `page_files` in `src/common.py` sweeps only the `Q`/`S`/`Agent`/`Meeting` prefixes (the glob itself is unchanged). Naming addendum, same ruling: both files in the exchange are called QA, distinguished by location; one conversation, two QAs: the bank QA is the original, the probe QA is the paper's copy that points at it. The file-level names QA-executor and QA-consumer are retired as WRONG; consumer and executor name slots only. `src/topic_entry_contract.py` therefore finds records with its own `probes/*/*.md` glob instead of relying on the page registry, and its test fixture moved to the record shape and digit-first names. First live migration: the MISQ paper's 28 entries (10 S03 + 18 S04) renamed per drawer, every pointer repointed, board page count 87 to 59 with an unchanged ERROR set.

## 0.122.0 - 2026-08-06

**Register rows render as evidence cards** (JL 260806: literature/values are the first to test the card evidence). Inside a `### Q-consumer register` section, and only there, a backticked binding token becomes the same chip + popover chipcard the prose `\citep` markers get: a bibliography key (or key-shaped token, which renders broken when it does not resolve, suggestions included) opens the cite card with the .bib entry, source links and rendered reference; a `tasks/…` or `discoveries/…` provenance path opens a `val` card whose links are the QA file and its run folder, with the QA's own `state:` line quoted, and a path that is not on disk renders `owed` with the miss stated, never invented. `src/dialect_paper.py` gains `Paper.register_binding` / `Paper.bank_binding` (the dialect resolves, the board renders, QBc5); `src/body.py` gains the scoped `REGISTER` mode (a `body(register=True)` door plus its own `###` detector, save/restore so embeds cannot bleed it) and the `code_or_link` binding branch; `src/page_question.py` passes the flag from `render_aims` and `render_subsections`, whose division split had hidden the heading from body(). Log lines and discussion lanes stay chip-free through the existing NOTE wall, and non-register backticks everywhere render exactly as before. Companion data files shipped with the paper family: `paper/S03-literature/{template,entry-template}.md` and `paper/S04-value/{template,entry-template}.md`, the copyable topic-register and probe-entry skeletons those cards read from.

## 0.121.0 - 2026-08-06

**Chip-card PDF previews fold shut** (JL: "the evidence card doesn't work, I cannot click it", S-Main-1). Root cause verified by driving a real Chrome over CDP: an open display card stacked two 24em `<object>` PDF previews inside its 60vh scroll box, pushing the file links ~900px below the card's fold, and the PDF plugin swallowed the wheel, so the card could neither be scrolled nor clicked where it mattered. `src/body.py` now wraps each pdf preview in a closed `<details class="ccfold">` whose summary wears the figcaption's face; `assets/css/60-chips.css` styles the fold. A card opens compact (header, body, one summary line per preview, links visible); one click expands the PDF in place (verified expanding to 348px and collapsing again). Image, text, and reference previews are unchanged.

## 0.120.1 - 2026-08-05

One line reworded for thin-paper phase 2: family-specific stage data (the paper
door's stages/ and craft files) stays with its family; the retired
`haipipe-paper-stage` is no longer named. Test fixture path updated to
`paper/haipipe-paper` (create-page.py's new home).

## 0.119.0 - 2026-08-05

**`ref/topic-entry-contract.md` grows the two rules the topic types need**
(review fix; the ref carries no version of its own, so the change is recorded
here).

- Register route line: the register's first line is a REQUIRED
  `route: outward | inward`, the machine key that separates the two topic
  types (the base's type resolution step ②). A register with no `route:` line,
  or with any other value, leaves the page's type unresolvable.
- Register-row states: a row ends SUPPORTED/BOUND, DEFERRED with a reason, or
  WITHDRAWN; an unresolved row holds the topic open; the topic's human gate
  reads the register, not the entries. Moved here from the two route contracts
  so the shared close semantics are stated once.

## 0.120.0 - 2026-08-05

**Embed URLs carry the shell opt-out** (JL 260805: "they are always of the same
slide number").

- `src/body.py`: the html-embed iframe src and its open link get `plain`
  appended. serve.py's shell-vs-file fallback is the Accept header, and a
  browser's iframe request sends the same `Accept: text/html` a tab navigation
  does; over a tailnet address plain http never carries `Sec-Fetch-Dest`, so
  every embed came back as the three-pane shell with its query dropped, and all
  seven divisions showed the deck's cover. `plain` is the shell's own
  documented opt-out, and it holds on every browser and origin.
- The blind spot was verification through 127.0.0.1, where Chrome DOES send
  `Sec-Fetch-Dest` (localhost is a trustworthy origin) and the embeds happened
  to get the raw file. The reader's path was the tailnet IP, where it never
  arrives. Reproduced with a header-faithful request before fixing.

## 0.118.0 - 2026-08-05

**Live html embeds, for the slide page type** (JL: "you will embed the html in
the content division"; proven on the boardform board's QA4).

- `src/body.py`: `![alt](x.html)` renders as a live iframe (`.fightml`) with an
  always-visible open link as the no-JS path. `?preview=N` on an html-ppt deck
  embeds exactly slide N, so a slide page carries one deck file, per-division.
- `src/page_board.py`: the split-site reroot now tells authored html files from
  generated page links by EXISTENCE in the board source folder, so an embed's
  src gets the `../../` hop exactly like a png while group-index links stay
  sited. (The first cut keyed on the `../` prefix and broke every group index
  row; the existence test replaced it the same hour.)
- `cli/check.py`: a media embed (`![](…)`) satisfies the division-figure rule,
  since a rendered embed is a figure in the renderer's own vocabulary; the
  caption rule still applies.
- `assets/css/60-chips.css`: `.fightml` frame styles, slide-proportioned
  (16:9), scoped like `figpdf`.

## 0.117.0 - 2026-08-04

- Adds the typed `### 🔗 Related Board Pages` Files group for precise Page-to-Page
  context by relation, Page Phase, Page id, and `page`/`§n` scope.
- Adds `src/page_context.py` and `cli/pagecontext.py`. The reader filters rows for
  the current phase, closes a division over target identity + Opening + matching
  Aims/States, shares the target frame across several selected scopes, and stops
  after one hop.
- Extends `cli/check.py` with errors for malformed rows, unsafe or dead paths,
  undiscoverable targets, Page-id mismatches, self-links, and missing scopes;
  duplicates warn and context emits them once.
- Adds fault tests for dead path, wrong Page id, missing scope, path escape,
  malformed form, duplicates, phase filtering, and recursion boundaries.

## 0.116.0 - 2026-08-04

- Adds `ref/page-lifecycle.workflow.js`, the bounded dynamic router for one Page.
  A producer performs DRAFT/PROBE/REVISE, a separate builder snapshots source
  and render hashes, and the fresh reviewer performs CHECK and selects the next
  legal route.
- Adds `src/page_lifecycle.py`, `cli/pageflow.py`, and lifecycle tests covering
  happy paths, legal branches, self-approval, changed-after-CHECK, human gates,
  illegal routes, round changes, bounded stops, strict SHA version identities,
  independent source/render rehashing, packet/run matching, version continuity,
  and producer/builder/judge separation.
- Routes Page-level `RUN` through `haipipe-page` and registers the narrow
  non-interactive Page orchestrator. `RUN` replaces the deferred router need;
  `ADVANCE` remains absent because the lifecycle is not linear.

## 0.115.0 - 2026-08-04

- Updates the family map to the Page Type × Page Phase model adopted on QB9.
- Lists `page-types/` with the three `for-*` variants and `page-phases/` with the direct DRAFT, PROBE, REVISE, and CHECK contracts.
- Routes phase work through `haipipe-page` and deliberately adds no Board-level `ADVANCE` verb.
- Treats the existing topic-entry implementation as a persisted Probe Page adapter rather than another lifecycle concept.

## 0.114.0 - 2026-08-03

**Board bucket review, 260803** (JL: "go ahead to solve yourself, dont ask me"). Ledger: `skills/_console/260803-board-bucket-review.md`.

- **The door was telling everyone to create a page the wrong way.** Three places said every page copies `ref/page-template.md`, "whatever its kind". For `Skill-`, `Agent-` and `Meeting-` pages that produces a page with no managed spans, which the checker then reports as broken forever. A new step 4b names the generated kinds and their generators, and `add` and the `ref/` table say the same.
- **A whole page kind had an engine and no contract.** `Meeting-<n>` is globbed by `src/common.py`, generated by `cli/meetingpage.py`, and exempted by `check.py`, and appeared in no SKILL.md in the family. The page-kind table now lists all six kinds with how each is created; a contract for Meeting is still owed.
- **The variant rule is rewritten from CONSUMER to MAINTAINER** (JL 260803 ruling). "A variant ships under its consumer, never here" broke the day `haipipe-page-for-venue` landed: its consumer is the paper family and its maintainer is this one, so it satisfied neither the rule nor the Skill-and-Agent exception. Who maintains it held twice; who consumes it never did.
- The family block names `haipipe-page-for-venue`, which had shipped with no door pointing at it.
- Seven of eight line counts in the `ref/` table were wrong, several by ~2x, and are now measured: `serve.py` 398→496, `chat.py` 1064→1332, `term.py` 670→857, `write.py` 259→426, `activity.py` 408→446, `base.py` 154→260, `structure.py` 274→270.
- "all 11 tests" → 14. The whole-tree membership sentence named two prefixes where the code globs four.
- `## Question` is no longer called "permanently recognized": it still parses, and `check.py` reports it as `retired-section`.
- The status strip's spec follows the code (JL 260803 ruling): `status.py` emits a terminal-clickable link, and `SKILL.md` plus three tests asserted the older markdown form. Suite is green, 91 passing.

## 0.114.0 - 2026-08-03

**🔗 A generic board folder no longer claims the whole SPACE's URL.**

JL: "the lifecycle is not good, I prefer it to be misq-xxxx-lifecycle".

`board_slug` trimmed the `NN-` ordinal and stopped, so `0-lifecycle` became `lifecycle`. Every paper on this SPACE carries a `0-lifecycle/`, so the FIRST paper took `/b/lifecycle` and the second would have answered to the same route. That name says what KIND of board it is, not which one. Generic names are now qualified by the owning folder, with the `Paper-` and `Project-` prefixes dropped for the same reason the ordinal is: `personality2opioid-misq2026-lifecycle`. Every non-generic board keeps the slug it had, checked against all ten boards on this SPACE. The old bare route now 404s rather than redirecting, which is this file's own doctrine: a redirect to the wrong board is worse than a miss.

`configured_base_url` also looked for `env.sh` in exactly one directory, `--root`, which defaults to cwd, so running `status.py` from inside a board folder printed the loopback URL even with a tailnet address set at the SPACE root. It now walks up.

**This was never a serving defect.** One `serve.py --root <SPACE>` has always answered for every board on the same tailnet address and port, because a board is just a path under that root. Only the printed strip was wrong. Measured the same day while looking for a slowness that is not on this side: `ThreadingHTTPServer`, gzip already live through `try_gzip` (407 KB of HTML leaves as 62 KB), 6 ms total on the host, and the peer link is `direct`, not DERP-relayed. Noted because a `curl -sI` probe sends HEAD, `try_gzip` handles GET only, and the missing `Content-Encoding` header reads exactly like compression being off when it is not.

## 0.113.0 - 2026-08-02

**💬 A comment made on selected words now RECORDS those words.**

JL asked whether selecting a few words and commenting makes an evidence card, and whether the comment also lands in the lanes. Neither happened. The comment landed under the whole line as a lane, and the words he had selected were used for a temporary local highlight and then thrown away: `srvComment` posted `{file, who, sentence, text, when}` and never sent `quote`, which the client had been collecting all along. So a remark about three words in a forty-word sentence arrived saying nothing about which three.

The grammar already had a home for it. `render_apparatus` carried a `「…」` quoted form, but only on the bare-initials shape, and the canonical `> Comment WHO` branch runs first, so `> Comment JL 「words」: text` printed its brackets as prose.

- `src/body.py` — the `Comment` branch takes an OPTIONAL `「…」` span and renders it in `.qt` ahead of the text. The three older shapes are untouched.
- `live/write.py` — `add_comment` accepts `quote` and writes `> Comment WHO 「the words」: text`. It is kept only when the words really occur in that source line, so a selection crossing two sentences records nothing rather than something wrong, and it never blocks the comment itself: a remark must always land.
- `assets/js/10-drawer/10-comment/30-write.js` — sends the `quote` it was already holding.

**A card is still a different thing, on purpose.** A card answers what a phrase IS and holds one answer; a remark is a person talking about the line. 🪪 Card remains the button that makes the other one, and `QB5 §5.1` now says so where a reader meets the question.

**🖼 Also fixed: the excalidraw embed pointed at the wrong page's frame.** Yesterday's review repointed QB5's embed from the retired `frame=QAb0` to `frame=QB5`, which was correct in form and wrong in fact: `frame-QB5` had been seeded back when `QB5` meant the `src/` split page, so the page embedded a drawing about a different subject. `cli/xcal.py` reseeds from the current pages; it dropped 22 frames whose pages are gone (`QAb0`-`QAb4`, `QAa0`-`QAa7`, `QA6`, `QA9` and others) and `frame-QB5` now carries this page's own figure.

## 0.112.0 - 2026-08-02

**🔗 The `✎` record has one computation, and a test that keeps it one.**

JL asked how `haipipe-writing` wires in. The answer is one place, and it is the `> ✎` change record: this file and `haipipe-writing/cli/wdiff.py` both computed the word-level diff with difflib and agreed byte for byte on every case tried, which is agreement by luck. The next edit to either splits them, and the record is a review trail somebody reads months later.

- `live/write.py` — `_change_diff` now calls `wdiff(host="board")`. It is LOOKED UP BY PATH, not imported, because every unit in this family must stay deletable from every other; the local computation survives as the fallback for a checkout with no `haipipe-writing` beside it.
- `tests/test_change_diff.py` — compares the fallback against the shared function over ten pairs, including an empty side, a full replacement and an unchanged sentence. Drift is now a red test.

**🌐 `tests/drive_board.py`** — a second recorded drive, 16 checks, against the REAL board instead of a fixture, and it writes nothing so it is safe to point at a live one. It answers the question the sentence drive cannot: a sentence can work perfectly on a page nobody can reach.

Its first run produced three FALSE REDS, both worth naming. It read `innerText`, which reports only what is on screen while every section is folded shut, so a complete page looked empty. And its detail line printed "found <probe>" whether or not the probe was found, so a red row read like a green one. Both fixed; it reads `textContent` and reports which half failed.

## 0.111.0 - 2026-08-02

**🚪 The sentence verbs migrated to `haipipe-sentence`, on the `haipipe-page` precedent (JL 260802).**

JL: "if we want to put sentence things, we migrate that part from haipipe-board to haipipe-sentence, just like haipipe-page, right?" Yes, and the precedent is precise about WHAT migrates: `haipipe-page` owns the page contract and its two verbs and owns no scripts, calling this engine rather than containing it. The sentence half had been the other way round: the operating detail lived in this SKILL.md while `haipipe-sentence` was a 94-line spec with no verbs at all.

- `### comment / edit` (26 lines of gestures, addresses, the action bar and sentence chat) is now a ROUTE. What stays are the two rules that bind the engine rather than the contract: a write needs `serve.py`, and a form closes before it asks for the repaint.
- The one-door table gained three sentence rows, and now states the rule at every altitude: one sentence is the sentence skill's, one page is the page skill's, the board is this skill's.
- The family roster now reads `DOOR + SPEC` for the sentence unit rather than `SPEC`.

## 0.110.0 - 2026-08-02

**📄 The family gains a page-kind variant: `haipipe-page-for-skill`.**

JL asked whether a skill page is special enough to need its own contract that calls `haipipe-page` inside it. It is. A `Skill-<n>` or `Agent-<n>` page mirrors a unit that ships elsewhere and DECIDES NOTHING, so the base Opening shape, which ends in `what this page decides`, leaves it with no question to ask. Five skill and agent pages filled that empty slot with the same rhetorical question, and read consecutively they were one form letter with the nouns swapped.

The family block and its heading change back to `three specs` for a real third spec this time, rather than for a verb set filed as one.

## 0.110.0 - 2026-08-02

**🔍 Two write paths still needed a manual reload, and nothing had ever tested past the point where they could not fail.**

JL asked directly: when I add a comment, or I do an edit, does the page only update when I refresh it myself? The card and comment paths were fine. The other two were not.

**Editing a sentence** called `location.reload()` on save. It threw away the scroll position and shut every section the reader had opened to reach that sentence, to show one changed line. Replacing it with the swap then exposed a second, quieter defect: the swap refuses to run while any textarea inside `div.wrap` holds text, which is the rule that stops a rebuild from eating a half-written comment. The editor's own textarea is inside `div.wrap` and still held the sentence that had just been saved, so the repaint could only ever be refused. The `> ✎` record reached the markdown and the page sat unchanged until somebody pressed reload. The reload it replaced had never met that guard, which is why it had never shown.

**Adding a typed lane** never asked for a repaint at all. It printed "✔ saved", closed its form, and left the lane to arrive whenever the background poll noticed, which backs off to five seconds on a page nobody has touched.

- `assets/js/40-sentence/00-apparatus.js` — both forms now CLOSE first and then call `window.__boardRefresh()`. The rule this sets: a writer clears its own draft before it asks for the page back.

All four write paths now repaint in 0.4s and hold the reader's place: card 883→883, comment 1204→1204, edit 1925→1925 with 16 open sections before and after, typed lane unchanged across the save.

**🧪 `tests/drive_sentence.py` grew from 31 to 36 checks.** The old F3 was called "double-click opens the sentence editor" and checked exactly that, which is the half that cannot fail; both defects lived after it. Four new steps follow the edit and the lane through to the repainted row, including a window flag set before the save and read after it, which is how a swap is told apart from a reload. `tests/fixture_board.py` gained five more targets: a sentence carrying both surfaces, a card naming absent words, two cards on one sentence, a three-line card body, and a sentence to edit.

Two of the new steps were red for a while because of the harness, not the code, and both are worth naming: the lane form is reached from the `＋` in the hover rail rather than by double-click, which opens the editor; and its dropdown remembers what was used last and falls back to `JL`, which is a person's initials and renders as a comment row, so the step was counting a lane that was never going to appear.

## 0.109.0 - 2026-08-02

**👪 `haipipe-board-index` is retired, and the family is one door, two specs, one verb.**

JL ruled the merge on 260802 ("maybe merge, I will do B") after asking what the index was for. The audit that question forced found three of its five verbs were other units' work written a second time: `propose` and `materialize` are this skill's own `open` action, `regroup` wrapped `cli/regroup.py`, and `check` was a subset of `cli/check.py`. Only `src/lanes.py` was code the family held nowhere else, and it moved to `haipipe-board-routing/src/lanes.py`.

The family block and the section heading both change: `three specs` was already wrong before the merge, since index was a verb set rather than a contract, and it is now `two specs`.

`open` keeps its own description of proposing and materializing a board on purpose, and the file now says so. A person opening their first board should not have to load a second skill; the duplication is declared in both files rather than left to be rediscovered, and the two are corrected together.

## 0.108.1 - 2026-08-02

**📏 The Opening budget stopped charging a page for its own change records.**

`check.py`'s Opening rules measured the on-stage paragraph as every non-blank line above the first blank line. `page_question.py` does not: it hands every `>` line to `render_apparatus` and joins only the rest into the lead. So the two halves disagreed about the same fact, and the disagreement only appeared once a sentence apparatus landed on the lead.

Found on `QBv1-misq.md` (260802): one `> ✎` record under a 340-char lead reported the paragraph as 841 chars, and reported the record's own word-level diff as a stuffed sentence carrying 6 clauses. Both findings described a line no reader sees in the paragraph.

- `cli/check.py` — `onstage` and `prose` now skip `>` lines, which is exactly what the renderer does. A lane is somebody's signed record, not a clause the reader has to get through.

## 0.109.0 - 2026-08-02

**🗺 The sentence family folded from six pages to two, and `check.py` learned the `Card` lane.**

Board-content work rather than engine work, but the checker change ships here. `QB5`'s five faces were carved on 260729, when the model was one sentence with five attachments and a page for each. The 260802 card ruling replaced that with TWO surfaces, and the split stopped carrying it: `QB5a` ended up owning both while its own title still said "click a sentence", which is the lane gesture.

Same shape as `QB4`'s seven section faces on 260801, and the same answer:

    QB5a  evidence card      -> QB5 §3 (the card) + §4 (the lanes)   archived
    QB5b  comments           -> QB5 §5 (a person's remark)           archived
    QB5c  editing            -> QB5 §6 (changing a sentence)         archived
    QB5d  chat + addresses   -> QD8, in the working lane             moved
    QB5e  details lifecycle  -> unchanged, still its own page

`QB5d` moved rather than folded because a generated address is how a machine POINTS AT a location, not a thing attached to a sentence: nothing is written under the sentence and nothing enters the file at all. Its readers are the chat drawer and the routing verb, both of which live in `QD`.

- `cli/check.py` — `old-comment-form` now knows `Card`. Without it, `> Card SPAN of words: …` matched the bare-initials shape as author "C", so every span card on every board reported itself as a legacy comment.
- `ref/board-form.md` — the `> Card` row joined the syntax table.
- Board 54 pages to 51, zero errors, `QB5` and every page whose live prose pointed at a folded face repointed. Every retired id (`QB5a`-`QB5d`, `QAb1`-`QAb3`, `QA6`, `QA8`, `QA8a`) still resolves through `board.md`'s Links table, so nothing already written breaks.

## 0.108.0 - 2026-08-02

**🪪 A card on a SPAN of words, and saving stopped throwing the reader back to the top.**

JL asked for two things on the sentence and named them apart: a card reached by clicking the selected words, and lanes under the line taking a citation, a comment, or any other kind. The second already shipped. The first did not: a card existed only where a paper marker did, so nobody could attach one by hand.

JL delegated the ruling. The three options drafted on `QB5` were all wrong in the same way, because each one asked where to put a MARKER. Option D, ruled instead: the record names its own span.

    The pooled coefficient reached a stable value in the third quarter.
    > Card stable value: what should open when someone clicks those words

- `src/body.py` — `CARD_LANE`, `_split_cards`, `_wrap_span`, and a `head=` on `_chip`. Cards are pulled out of the apparatus BEFORE it renders, so a sentence carrying only cards keeps its plain `<p>` and never grows an empty drawer with a `⚑ 0` badge.
- `live/write.py` — `add_card` behind `POST /_board/card`, with three refusals: the sentence must be found exactly once, the words must really be in that source line, and the same card may not be written twice.
- `assets/js` — 🪪 Card beside 💬 Comment, offered only when the selected words are genuinely in the sentence, because a button that can only fail is worse than no button.
- `assets/css/60-chips.css` — the words stay PROSE. A `\citep{}` chip replaced a marker nobody wanted to read and may look like a control; a span card sits on words the author wrote, so it keeps the text's font, colour and weight and takes one dotted underline.
- `sentenceText` gained its one exception: it deletes every `button`, because a paper chip's label is not the source text. A span card's label IS the source text, so it is unwrapped instead. Without this every later write on that sentence would miss its anchor forever.
- `check.py` learned `Card`, which it had been reporting as a legacy `> C:` comment.

**🎯 The smoothness half** (JL: adding a comment and hitting save made the whole thing refresh).

- A pane used to `location.reload()` on every write. It now runs the same drawer-preserving swap the single-document path always had, and the writer asks for it immediately rather than waiting up to 800ms for the poll to notice.
- The swap's fold restore was keyed on summary TEXT, and `board.js` decorates summaries after each render, so the old key read `📚 Content C1 ⧉ 🤖` and the fetched one read `📚 Content`. They never matched. It only showed on the comment path, because the text fallback runs only when the drawer count changed, which happens exactly when a sentence gains its first record.
- Measured: a card save holds scroll 883 to 883 with 16 sections open before and after; a comment save holds 1229 to 1229. Both land in 0.4s.

**🧪 `tests/drive_sentence.py`** — a recorded Chrome drive, 14 of 14 green. It builds its own throwaway board (`tests/fixture_board.py`), serves it on a free port, moves the real mouse through every gesture, and writes one screenshot and one row per step into a `report.md`. The first version drove `QB5` itself and had to be thrown away: it left five cards on a page a person reads, and its second run could not tell a pass from a break.

## 0.107.0 - 2026-08-02

- A hidden `⧉` on every `Decision Now` row (JL: "could you give a hidden copy
  button so I can copy the decision easier?"). A decision row is the one block a
  person routinely moves OFF the board, into a chat or a message, and copying it
  by hand meant dragging across ten wrapped lines and collecting the checkbox
  glyph with them. `assets/js/45-decision-copy.js` + `.dcopy` in `10-focus.css`.
- Hidden at rest, revealed on `:hover` and `:focus-within` so the keyboard
  reaches it, and always visible on coarse pointers. Scoped to rows under a
  `Decision Now` summary; the board's other checkbox rows are legacy checklists
  nobody moves anywhere.
- Two defects found by CLICKING it, neither visible in the markup:
  the first version looked for the heading in `previousElementSibling`, but a
  `###` inside States renders as `details.csec > summary`, so nothing ever
  matched and no button appeared; and `rowText` used `innerText`, which reads
  LAID-OUT text, so with the rows inside shut `<details>` it returned '' and the
  button flashed ✓ while handing the clipboard an empty string. It now walks a
  detached clone with `textContent`. Verified over CDP: 1412 chars, 10 lines,
  checkbox stripped, 8/8 rows on QB2 and 5/5 on QA3 and QC1b.

## 0.106.0 - 2026-08-02

- The live `mode` now decides the shape of a reply's BODY (QA3 §6, JL 260802):
  `discussion` keeps the repo default; `implementation`, `review` and `sourcing`
  collapse the reply to outcome, routing footer and strip, and a drawing, table,
  section or row-list becomes a page write first and a pointer second.

## 0.105.0 - 2026-08-02

- A machine now CLOSES a `### Decision Now` row once the person has answered it,
  recording which option, who ruled, when, and the words they used (JL 260802:
  "I think you should close it automatically, please go ahead and do it").
  It still may not close a row nobody answered, and may not flip a page-level
  human gate; a machine's own recommendation is never an answer. Before this a
  row answered in chat and acted on within the hour still rendered as pending,
  so the page reported work as waiting that had already shipped.

## 0.104.2 - 2026-08-02

- **THE SWEEP THAT REPORTED AN EMPTY BOARD.** `cli/sentencerun.py` navigated to a page
  URL and evaluated `window.__boardSentenceText` in the top frame. The live shell answers
  a page URL with a three-pane frame whose real document loads in an iframe, so the run
  read the shell's window, found no reader, and printed
  `SKIP … this page has no __boardSentenceText` for all 55 pages of the design board.
  A run that reports nothing looks exactly like a run that found nothing.
  `tree_url` now appends `?pane=page`, which asks the server for the page rather than
  the shell around it.
- The first honest sweep after the fix: 55 pages, 5069 writable sentences, 0 unreadable,
  3067 unanchored, and not one of them the ①→② drift the run was built to catch. They
  split 2724 indented item explanations, 215 paragraphs joined from several source lines,
  68 generated placeholders, 56 markdown table rows and 4 duplicate sentences. Recorded on
  `QF5` with the two repairs it now asks for: stop offering a control that cannot succeed,
  and stop printing a correct refusal as `FAIL`.

## 0.104.1 - 2026-08-02

- The family heading cited `QC6 §8`. That page was reindexed to `QC1b` on 260801 and its
  Content was rebuilt into 8 parts on 260802, so the roster shape now lives at `QC1b §2`.

## 0.104.0 — 260802

- **THE SIX-LANE BUG.** `POST /_board/activity` never returned. Every board
  page posts `op=stats` to it as it loads, and `log_boards()` answered by
  running an unpruned `rglob` over the whole repository root: 366,951 entries
  to find ten `board.md` files, measured here at over 60 s with no response at
  all.

  A browser allows SIX connections per origin, SHARED ACROSS EVERY TAB, and a
  request that has not finished is still holding one. So a few open pages held
  every lane and the next CLICK never left Chrome's queue. Devtools reports
  that as "Provisional headers are shown" with "0 B transferred", and a reader
  experiences it as one to two minutes of a spinner. JL reported it for eight
  days as "why is it so slow"; every measurement taken in that time said the
  server answered in 20 to 70 ms, and every one of them was correct.

  `log_boards()` now prunes in place, the same fix `live/home.py` got that
  morning and this second copy did not, plus a two-second cache so ten tabs
  loading at once pay for one walk.

  | | before | after |
  |---|---|---|
  | `POST /_board/activity` | 60 s+, no reply | 43 ms |
  | ten concurrent | never finished | 0.88 s |
  | requests pending after a page settles | 1, forever | 0 of 8 |
  | click QB1 → QB2 | queued 1-2 min | 53 ms |
  | server threads | 178 | 12 |
  | ESTABLISHED from one laptop | 6 of 6 | 1 |

- **`checks/pending.mjs`** (new). Opens a page in headless Chrome and fails if
  ANYTHING is still pending once it settles, or if ten concurrent
  `/_board/activity` posts take over 5 s. Every existing check asked "did the
  page load" and every one passed throughout, because the page did load. The
  question that finds a held connection is "did everything finish", and it has
  to be asked of a real browser: a request Chrome never sent appears in no
  server log. Skips cleanly without Chrome or `ws`.

- Lessons recorded on `QD8-pagecost` (boardform board; opened as `QC5`, moved to the QD lane the same day on JL's call): a fast server plus a
  fast link is not a fast page, because the third term is whether a lane was
  free and `curl` cannot see it, since curl always gets its own connection;
  when a bad walk is fixed in one place, grep for its other sites the same
  hour; and a check that asks "did it work" will not find a resource leak.

## 0.101.0 - 2026-08-02

## 0.102.0 — 260802

- ONE DOOR (JL 260802: "you can just say, haipipe-board update the page etc,
  it will route to the haipipe-page"). `## Actions` now lists two routed
  verbs, `create a page` and `update a page`, with the routing table beside
  the eleven this skill runs itself. Route by SCOPE: one page is the page
  skill's, the board and its structure are this skill's, and a request naming
  a page id or path is the page skill's even when it sounds structural.
- The `## Actions` command paths were still pre-`cli/`.

Stale-statement sweep of `SKILL.md` and `ref/` against QB4's rewritten contract
(QB4 `## Law`, 260801-260802). No rule was invented here; every edit repairs a
sentence QB4 now contradicts.

- Aim status vocabulary corrected to `⬜ 🔨 🧠 ✅ ❄️` in `SKILL.md`'s sync
  table, `ref/page-template.md` (`## States` prose plus its two example rows)
  and `ref/writing-rules.md`. The old `🟡 🟠 ⏸️` are named as still parsing but
  no longer written. The page `state:` line keeps its own `✅ 🟡 🔴 ⏸️` set,
  which is a different vocabulary and was left untouched everywhere.
- Aims/States group ids are `A<n>`, carrying the Content part's number, name
  and emoji: `ref/page-template.md`'s two `### C1 ·` example groups and
  `ref/writing-rules.md`'s "an Aim for division C3".
- A sentence comment is `> Comment WHO …`: `ref/board-form.md` §5's syntax row,
  `ref/page-template.md`'s apparatus example, `ref/writing-rules.md`, and
  `SKILL.md`'s never-delete rule. `## Discussion` keeps its own `> JL:` /
  `>> CC0726:` thread grammar and is called out as unaffected.
- Dead CLI paths after the move into `cli/`: `SKILL.md`'s script table
  (`stage.py`, `skillpage.py`, `regroup.py`, `refs.py`, `xcal.py`,
  `gate_live.py`), `ref/board-form.md` §6's build/watch commands, its
  `regroup.py` and `stage.py new` invocations, and `structure_op()`, which
  lives in `live/structure.py` and not in `serve.py`.
- Content is numbered all the way down: the template's example divisions are
  `### 1 ·` / `### 2 ·`, its group title `**1.1 ·**`, its paragraph
  `#### 2.1 ·` (it was `#### P1.`).
- Everything starts SHUT: the template no longer says human comments and edit
  records open by default, and `ref/board-form.md` §8's shut-by-default list
  now names every section and every Content division, with Opening as the one
  section that folds from its lead instead of its heading.
- The Opening drawer is FLAT behind one click: the template's "EVERY one of
  those rows starts collapsed" and `ref/board-form.md`'s matching parenthetical
  contradicted the same file's own flat-drawer spec and `render_subsections(
  ..., flat=True)`.
- Files is the action map for "if I change a rule here, what do I touch?", and
  its groups are a MENU of actions: Engines · Contracts · Checks · Input files ·
  Output files (`ref/page-template.md`; the old text offered only the trio and
  cited two archived pages).
- Decision Now goes FIRST in States and carries the fixed row shape (📍 Part ·
  🔔 Why now · ⭐ on the recommended option · 🛑 Blocks · 🤖 If nobody answers);
  an answered decision LEAVES States, its ruling to `## Law` and its change to
  `## Log`. The template's dated-change-record example moved out of States for
  the same reason, and the `span.stmp` construct it was the fixture for is now
  exercised by a dated `## Law` ruling.
- `## Law` / `## Lesson` / `## Glossary` entries are `- ` rows opening with an
  emoji, and a Glossary term is bold (template and writing-rules).
- Dead page pointers repaired: `ref/writing-rules.md`'s worked example was
  `QA4-pagelayout.md`, which no longer exists; the template pointed at `QB4c`,
  `QB4a-QB4g`, `QB4f` and `QA2b`, all folded into QB4 or archived on 260801.
- `ref/page-template.md` is described by its own name in `SKILL.md`'s ref
  table; the note claiming a historical filename was kept predates the
  260801 rename from `ref/q-template.md`.

## 0.100.0 - 2026-08-02

## 0.58.0 — 260802

- `## Discussion` renders as a nested, collapsible THREAD (`render_thread` in
  `src/body.py`): avatar with initials, author bold on its own row, body
  aligned under the name, replies nested inside what they answer so the rail
  spans the subtree, and `⊖`/`⊕` collapse via `<details>`.
- The author is now OPTIONAL in a thread line. Five of QB4's 34 discussion
  lines had been falling through to raw text with their `>` markers visible,
  because a parenthetical before the colon or an unsigned thread opener did
  not match the old author-required pattern.
- `## Law`, `## Lesson` and `## Glossary` take an emoji per entry and a bold
  Glossary term; the renderer already lifts a leading emoji into the row icon.

## 0.57.0 — 260802

- `cli/check.py --summary` scores a board instead of listing it: findings per
  rule, the worst pages, and how many are clean. QB4 §9 says the findings ARE
  the measurement, and a 291-row list does not tell you whether the board is
  improving.
- Six new checks land the QB4 rules mechanically: `group-name-drift`,
  `two-canvases`, `division-no-figure`, `division-no-caption`,
  `old-comment-form`, `dead-file-path`, plus an on-stage paragraph ceiling
  replacing the old prose-line count.
- `haipipe-board-reviewer-agent` 0.4.1: its `check.py` path had gone stale when
  the CLI moved into `cli/`, it now also runs `--summary`, and it states that it
  LOADS `haipipe-page` rather than restating the contract, which is what
  keeps it from drifting a night behind the rules.

**The board can be OPERATED as three panes: index, page, chat, each refreshing on its own (QD5).** `live/shell.py` adds four routes and no dependency: `/_shell?p=<page or board folder>` serves one document holding three same-origin iframes; `<any board page>?pane=index|page|chat` serves the SAME static file with a `<style>`, a `window.__boardPane` marker and, for the index, `<base target="page">` injected at serve time, so strip the query and the byte-identical page is still there (QB2 intact). A rail click is now ordinary HTML — `target="page"` loads the sibling frame, `70-router.js` returns at its first line inside a pane, and links carry `?pane=page` out with them so a frame stays a frame. `/boards` cards gained a `⇱ Split` link, because nobody should have to type a route.

**The refresh mechanism was built three times, and each version was removed by the cost of the last.** First a server push: `/_events` streamed the path of every rewritten page and the shell reloaded the matching frame. It worked, and it holds one of the browser's six connections per origin for as long as the document lives — and a browser neither closes nor makes readable a connection belonging to a document it has replaced, so opening the split twice inside a few seconds wanted seven connections in six slots. That failure is silent by construction: the second shell's panes never loaded, its frames' `location.reload()` did nothing at all, and a queued request is indistinguishable from a slow one. Bounding the stream (a per-tab id retiring its own orphan, a 55s life, a 3s heartbeat) reduced it and could not remove it, because the terminal's WebSocket spends a second connection the same way. Second, a shell-side poll: it had to remember what it had already told a frame to do, and a reload dropped mid-navigation was then never retried, so a page could sit stale forever while the code believed it was fresh. Third, and shipped: **each pane asks about its own url** — a `HEAD` every 800 ms compared against `document.lastModified`, reload on difference, and the chat pane never asks at all. Nothing is held, nothing is remembered, and being still stale on the next tick IS the retry. Two engine fixes were needed for it and nothing else would have found them: `serve_pane` must send `Last-Modified` (the static handler gives it for free; a served pane did not, so the `HEAD` had nothing to compare), and the baseline must be `document.lastModified` rather than the first answer received (an edit landing between a frame's load and its first tick was otherwise adopted as current).

**And the gap suite found a bug that was never about the split.** `checks/splitgaps.py` runs 21 assertions on a throwaway fixture with its own server and Chrome, because unlike `splitshell.mjs` these WRITE: G1 proves an ORDINARY board page is unchanged by this session (the router still swaps `div.wrap`, `20-live-refresh.js` still lands an edit in place, neither reloads — the regression surface of every change here, previously untested), G2 that scroll and open sections survive a pane refresh, G3 that all three pane kinds still read with every `<script>` stripped, G4 that a comment posted to `/_board/comment` repaints the page pane and leaves the chat pane alone. G4 failed, and the cause was `live/base.py`: `rebuild()` still pointed at `HERE / "build.py"`, which 0.99.0 moved into `cli/`. So since that release EVERY write through the server — comment, sentence edit, resolve, chat, terminal — updated the Markdown and then silently failed to rebuild the html, answering 200 with the error text tucked into a `build` field nobody reads. `checks/run.py` carried the same two stale paths. Both fixed. Also recorded: a real reload loses scroll where the old `div.wrap` swap did not, so `80-restore.js` is now LOAD-BEARING in a pane rather than the deletable thing A2.3 predicted.

Verified by driving it, not by reading it: `checks/splitshell.mjs` (23 assertions in headless Chrome — three frames, a rail click that moves only the page frame, the address bar following it, a rebuild that repaints only the page frame while a real `claude` keeps running in the chat pane) plus `tests/test_shell.py` (11, no browser). Green twice from a fresh browser; run back-to-back in a tab that held a shell moments ago, the refresh still lands but takes ~10s while the previous terminal socket is collected, which is the residue QD5 C4 P6 names. **And the wire itself, which was the thing JL actually felt.** He asked why opening a page takes so long; the server answers in 2 to 6 ms, so it was never the machine. Nothing had ever been compressed: a page is 172 KB, the index 244 KB, the largest page 451 KB, and `board.js` + `board.css` another 350 KB, all crossing a VS Code or ssh forward at full price. `live/base.py try_gzip()` now sends static text gzipped (GET only, above 1 KB) and `_send_html` does the same for the panes and the shell, which the static handler never sees. Measured 5.6× on a page, 7.2× on the index, 3.6× on the largest: a cold page open went 521 KB → 140 KB, and the split's first open 937 KB → 206 KB. HEAD is left alone on purpose — the panes poll with it and read only `Last-Modified` — and revalidation still answers a 0-byte 304, and a `.md` link still arrives as text rather than a download. Recorded as QD5 C2 P5 and a new Aim A2.5.

**`/boards` took 95 seconds.** JL said he could not open it and I first read that as a network problem; it was `render_home()`. `rglob("board.md")` descends everywhere and the skip list was applied to the RESULTS, so the home page walked 366,951 entries — `.venv`, `node_modules`, `.git`, `_WorkSpace`, and the generated `board/` tree under every board — to find ten files. Warm 2.7 s, cold 95 s. Pruning `dirnames` in place during an `os.walk` leaves 11,670 entries and the page now answers in 0.12 s, measured three times in a row. Also this release: the split's url is now the PAGE's own url plus `?split` (JL: "why they don't share the same URL? It is very weird") with `/_shell?p=` kept as an alias; the shell carries a 30 px strip naming the board and the page, with 🏠, ☰ and 💬 — the same two gestures the one-document board has, where hiding a pane is a zero-width column and never an unloaded frame, so a terminal mid-command survives being put away; and the chat pane hides the drawer's own ✕ while keeping its `>_` / `←`, which is the GUI-to-TUI switch JL asked to keep. Refusing to mirror a frame that has not loaded also killed `/_shell?p=blank`, an address that named no board and 404'd on reload.

Recorded on QD5, whose States now read 10 of 13 Aims met — A2.2 and A3.2 are the honest gaps: A3.2's behaviour is there but the guard code it names (deferred swaps, asset-stamp deferral, PTY parking) is still in the tree: the index is loaded once per session because it is its own frame, but every page still SHIPS the 53 `sb-out` blocks and the pane only stops drawing them.

## 0.99.0 - 2026-08-01

**The skill folder stopped opening onto a pile of `.py`.** JL, browsing the new RELATED FOLDERS fold: "为什么有那么多 .py 文件是在最外面的?它不应该放到哪一个文件夹内部吗? ... 因为它本身是一个 skill folder,你这么多 Python 的文件放外面,感觉不对吧?" He was right, and the first answer here was a bad one: the top level was defended with a reference count (`serve.py` named 73 times, `build.py` 64), which turned out to be counting PROSE mentions on board pages. The number that decides a migration is how many places EXECUTE a path, and that was 15, in 6 SKILL.md files. Two moves followed. First the 11 `test_*.py` into `tests/`, then the 13 runnable scripts into `cli/`, leaving a top level of `SKILL.md`, `CHANGELOG.md`, `status.py`, and folders. Both moves ran against a before-and-after suite (50 passed → 50 passed) rather than inspection, which is what caught the silent part: `HERE` meant "the engine dir" in every script and every test, so a plain move re-pointed `HERE / "ref"`, `HERE / "cli" / "build.py"`, `HERE / "serve.py"` and `root.parents[1]` at the wrong folder. `tests/conftest.py` now puts both the engine dir and `cli/` on `sys.path`. `check.py` then caught the half no test could see: the board's `## Links` still named the old paths, so 96 rendered hrefs were dead; repointing them took it back to 0 error. `status.py` stays at the top on purpose, because the reply-footer automation invokes it by absolute path. Also this release: the Board Map is shut by default (JL: "默认的话就合起来", it pushed the roster off the first screen), and the RELATED FOLDERS fold became a real directory browser whose files are clickable links rather than inlined content. Recorded on QC2 and QB2.

## 0.97.0 - 2026-08-01

**Writing Style now has one owner.** Stage Contract carries Required Inputs and
Venue, while `stage.py` materializes `style-from` prose rules in a managed block
inside the page's own `## Writing Style`. Author-written page rules and
`### Provides` remain outside generated spans. A focused regression test locks
the ownership boundary.

## 0.96.0 - 2026-08-01

**Quality Check now evaluates the page section by section.** Requirements keep
one source in `haipipe-page`; the evaluator resolves the base contract,
consumer variant, page Writing Style, Stage Contract, local Content division,
and paragraph job before judging. The page action returns one evidence-bearing
`MEETS | NEEDS WORK | N/A | NOT VERIFIABLE` row per review unit, separates
mechanics, function, evidence, and readability, and reports requirement
conflicts instead of silently choosing one source. The fresh Board reviewer now
uses the same contract as the independent gate.

## 0.95.1 - 2026-08-01

**The paired record sections now use paired plural labels.** JL rejected the
visual asymmetry of `Aims / State`. The canonical headings and rendered labels
are now `Aims / States`: one Aim still maps to one State record, while each
section contains several records. `State`, `Where we are`, and `Now` remain
input aliases so old boards rebuild without migration.

## 0.95.0 - 2026-08-01

**A page now separates intent from fact.** JL ruled that the task-shaped `Items to Finish` and the catch-all `Where we are` made it hard to tell what a page wanted from what was merely true today. The canonical page sequence is now `Opening → Diagram → Content → Aims → State → Files`. An Aim is a durable target state linked to its Content division (`A3.1` under C3), with `P1` reserved for a genuine page-level target. Its optional `Done when` defines acceptance and its optional `Plan` records a temporary route. State mirrors those Aim ids and carries exactly one current emoji per Aim: ⬜ not started, 🟡 active, 🟠 waiting, ✅ met, or ⏸️ held. State transitions belong in Log.

**The model is executable, not only renamed.** The renderer derives Aim and group counts from State, the Section Matrix and JSON output use the same progress helper, the checker validates page-state alignment against Aim State, and the new-page, stage, skill, and meeting generators emit the canonical shape. `Aims` and `State` are aliases of the historical parser slots, so `Items to Finish`, `Done when`, `Where we are`, `Now`, and the Chinese headings continue to rebuild without migration. QB4 is the worked design page and the template/spec/writing rules carry the same contract.

**Page closure and quick actions follow the same boundary.** A Q may close from
met or explicitly held Aims; an S may close only at its human gate. Browser
quick actions now ask about open Aim States and never present the legacy
`Done when` checkbox shape as canonical.

## 0.94.0 - 2026-08-01

**The ⚑ badge was being posted as part of the sentence, so nothing could be written.** JL sent a screenshot: the edit form open on a sentence that carries one comment, and the server answering "this sentence is not in the source file, nothing written". It was not. `QC7`'s anchor is an EXACT match of the posted string against a source line, and the payload ended `…below the read.⚑ 1`, because the badge now lives INSIDE the `<p>` (it became a zero-width span in 0.88.0 so it could never wrap onto a line of its own) while all three writers still read `p.textContent` raw. Every edit, every added lane and every sentence-local comment on a sentence that already had apparatus therefore failed, and the server was right to refuse each one. There is now ONE reader, `window.__boardSentenceText`, stripping `.sbz/.sbadge` and the controls; the edit path, the add-a-lane path and the comment path all call it, and `40-sentence/10-address.js` dropped its own copy instead of keeping a second implementation of the same grammar. Proven in Chrome without writing anything: posting the stripped text now reaches the server's SECOND gate, "the sentence has not changed", which is only reachable once the line has been found.

**The edit form was one character wide.** Same screenshot. `.sedit` is a grid and the error message sat in a fifth column, so a message the length of a Chinese sentence took the row's width and left the textarea a sliver. The message spans its own row now and the textarea has a 12em floor: measured at 480px after a real double-click.

**Navigation stopped re-downloading a rail it throws away.** JL: "why I feel it will have a long time to navigate to different pages?" Measured: the server answers in 8ms and re-wiring a swapped page costs 4ms, so the fetch was the whole cost. Every page file carries the complete 112 KB rail and the router swaps only `div.wrap`, so 82% of a median 136 KB page is discarded on arrival, and both the fetch and the server said `no-store`, which re-downloaded it every visit. `no-store` was the wrong instrument for the guarantee it protected (JL 260726, "why now I cannot open them"): that requirement is never serve a page from before the last build, and it is spelled `no-cache`, meaning REVALIDATE BEFORE USE. Both sides now say it, a revisit costs 0.3 KB instead of 119 KB, and the staleness guarantee was re-tested by editing a page on disk and watching the next fetch come back full-size with the new bytes. The 112 KB duplicated into every page file is recorded as an open decision on QC4.

**Two smaller repairs.** The rail's drag handle is `position:fixed` and placed off `--sbw` alone, so with the rail collapsed it stood 238px into the page as a bar across the text (JL screenshot); it now carries the rail's own two visibility conditions and moved from `80-matrix.css` to `70-sidebar.css` beside what it resizes. And `check.py` called `fig/image copy.png` a dead link because it compared a URL-encoded `%20` against a filesystem path; it unquotes first. Recorded on QB5c, QC4 and QB2a.

## 0.93.0 - 2026-08-01

**One canonical generated shape.** A Board source folder now has one generated output: `board/index.html`, one `board/<GROUP>.html` per group, one `board/<GROUP>/<page>.html` per source page, and shared `board/_assets/`. `SKILL.md`, `ref/board-form.md`, the Index spec, `build.py`, `watch.py`, the live rebuild path, and the Paper Board's own structure description now name that same shape. The retired `board.html` remains only as a compatibility input or cleanup target, never as a new folder-build output.

**Split-page resources move as one set.** The renderer already rerooted page-body `href` values, but evidence-card panels sit outside that body and carried Board-root-relative `_fixture/...` URLs unchanged. Every split page therefore had broken source links, images, and PDF objects even though the page itself returned 200. `tree_reroot()` now moves `href`, `src`, and `data` together in page bodies and popover cards; `check.py` verifies all three attributes so the visible-media half cannot regress behind a clean link check.

**Split-page navigation is file navigation.** The shared question renderer still emitted monolith-era `#previous`, `#next`, and `#top` links inside an otherwise independent page file. The tree renderer now converts those fragments, plus Q/S references in group and Index prose, into real page routes before writing the site. `check.py` also rejects a rendered fragment whose id does not exist in that file, so scripts-off navigation cannot silently regress.

**One browser-side Board path.** Image paste, terminal paste, copied `claude --resume` commands, and Activity sample data still derived their folder from the open document's immediate parent. On a focused split page that parent is `board/<GROUP>/`, so paths and copied commands pointed below the editable Board. They now share `boardDirPath()`, derived from the same canonical `boardPath()` every write endpoint uses. The standing checks and live refactor gate also send `board/index.html` rather than naming the retired monolith.

**The page contract has one Opening rule again.** The current page spec and template ruled out a separate `## Boundary`, while the older board-form and live ＋Q stub still generated or recommended one. The authoritative files now agree: Opening states scope and why the question matters, and it names the neighbouring page that owns excluded work.

## 0.92.0 - 2026-08-01

**A group intro's figure renders as a figure on the group page.** `index_rows` and the group page built the same intro body two ways: the index turned a ``` fence into `<pre class="gidia">`, while the group page flattened every fence line into `<p>` prose, which is how a group's ladder arrived mangled inside "why this group exists" (JL 260801). Both paths now share `page_board._gi_body()`, and `.gwhy-b .gidia` joins the `.gib .gidia` CSS rule so the figure is styled there too. Board-side, on the design board: the QB group intro redrawn as the section-protocol ladder (one reader question per section), and the seven QB4a-QB4g faces each open with the five-row protocol (conveys · holds · source · rules · omit), master view on QB4 §0. JL ruled the graduation (option A) the same day: the template's How-to-use comment now carries the reader-question ladder + the misplaced-sentence rule, and `haipipe-page` 0.3.0 carries the five-row contract.

## 0.91.1 - 2026-08-01

**checks/ follows the QD3m→QD3 merge.** JL ruled the design board's QD3m (the myrlin smooth-view page) folds back into QD3 — its engine half had already shipped into QD3 as 0.64.0, and its open smooth-view work now rides QD2 M1 — so the page moved to the board's `_archive/`. `checks/pty_e2e.py`'s default spawn target pointed at the archived path and would have 400'd on the next full-tier run; it now defaults to `QPf-page-folder/QPf4c-chat-terminal/QPf4c-chat-terminal.md`. Board-side records on QD3 (Where we are + Log) and board.md's QD lane/map/Pages rows.

## 0.91.0 - 2026-07-31

**`Meeting-<n>` is a page kind, and a vault note becomes a board page.** JL: "the MEETING-page should be a special page like SKILL, but still fit the Basic page structure." It does, and the reason it fits is what reading `jluo41/echo-meeting` turned up: its summarizer's system prompt FIXES six headings, so the mapping is a lookup rather than an interpretation. `### TL;DR` becomes the Opening, `### Diagram` is already the emoji ASCII figure this board asks every page for, `### Key Points` and `### Decisions` and the `## Conversation` chapters become Content divisions, the transcript is the last division, and an Obsidian `> [!quote]-` callout becomes exactly this board's sentence apparatus, so clicking a chapter's summary line opens the words that produced it. Three managed spans (`head`, `diagram`, `body`) resync from the note; Items to Finish and Decision Now are SEEDED ONCE from `### Action Items` and `### Open Questions` and never touched again, because you tick those and a resync that rewrote them would eat your state. New `meetingpage.py` (`new` / `sync`); `src/common.py` and `src/parse.py` learned the prefix and a `meeting` kind that sorts after Agent; `check.py` learned the filename in `## Pages`. Generated `Meeting-1` from the real 260723 note: six base sections, 18 Content divisions, 15 sentence drawers, zero warnings. Recorded on QC10.

**A meeting page is exempt from English-only, deliberately.** The imported note is 8,573 Chinese words, and JL's 260724 rule is about the prose this team writes, not about a meeting held in the language it was held in; "fixing" a quotation falsifies the record. Managed spans were already skipped by `strip_fences(prose_only=True)`, but the two seeded lists sit outside them by design, so `check.py` now exempts `Meeting-<n>` pages from the CJK and em-dash rules: 26 warnings became 0.

**Two defects the first generated page exposed.** The Opening's LEAD is composed in `page_question.py`, outside `body()`'s marker filter, so a page whose Opening opens with a managed span printed `<!-- haipipe:meeting:head:start … -->` as its own lead sentence; the filter now applies in both places. And `check.py`'s `## Pages` scanner matched only `[QS]`/`Agent-`, so a correctly listed Meeting page was reported as not listed.

## 0.90.0 - 2026-07-31

**serve.py re-execs itself onto the venv, ending the 3.9 saga.** The checklist's very next run after shipping caught the live 5599 on system python 3.9 for the THIRD time in one day (pages 200, every 💬 turn dead) — three restarts by three hands, all hitting the same invisible trap that serve.py's docstring, a memory, and a QC8 log line all already warned about. A rule people keep forgetting belongs in code: `main()` now tries `import claude_agent_sdk` right after parse_args, and on failure `os.execv`s itself onto `<--root>/.venv/bin/python` when that exists. Loop-safe twice over (the venv python resolves equal to itself, and under the venv the import succeeds before the branch is reached); if the venv is also SDK-less it warns once and keeps serving rather than dying. Proven by starting serve.py under `/usr/bin/python3` (3.9) on a scratch port: `GET /_board/health` answered `python 3.13.14, sdk true` — the process traded itself in before binding. Shipped with the alignment lap JL asked for: `checks/run.py --full` re-run against SDK-Talk's latest code (assets split into 24 parts, router click queue, drawer restore fix) — full tier green (pty ①–⑦, CHATOK, termnav 12/12), the 0.86 follow() fix verified intact inside `assets/js/10-drawer/40-follow.js`, ledger 0.85→0.89 sequential with no collisions. Recorded on QC8.

## 0.89.0 - 2026-07-31

**The checklist becomes executable: `checks/`, two tiers, and a health probe.** JL: "checklist 就是 item to finish — 要时刻保证它们永远是被 check 的." Today proved why a tick alone is not that: `follow()` on the tree silently stopped enforcing QD1's one-window law and no checkbox moved. The one-off scratchpad batteries are now a checked-in standing checklist. **Smoke tier** (`checks/run.py`, seconds, read-only, against the LIVE server): the tree serves, `watch.py` is rebuilding, tree `_assets` match the assembled source, claude and node are present, and — through the new `GET /_board/health` — the server's OWN interpreter imports `claude_agent_sdk`. That last one cannot be checked from outside: ps shows the venv symlink RESOLVED to the bare interpreter, and re-running that binary loses the venv, which is exactly how the 3.9 restart (pages 200, every chat turn dead) slipped through twice. **Full tier** (`--full`, minutes, real turns): a THROWAWAY fixture board with its own server and Chrome runs `pty_e2e.py` ①–⑦ (a real CLI turn through the PTY), one scoped SDK chat turn (CHATOK), and `termnav.mjs` (⌨ follows the tree router, park-not-held, paste — 12 browser checks). A standing check must never touch a real board: the fixture excludes the sidecar registry, strips every page's `session:` header (or a spawn `--resume`s a session whose jsonl lives under the real repo — pty booted but the turn hung), and answers the fresh-cwd folder-trust dialog (same symptom, found by the battery's own second run). Both tiers green: smoke 6/6 on 5599, full = pty ①–⑦ + CHATOK + termnav 12/12. `navtest.mjs` (💬 follows the router) joins `checks/` once SDK-Talk's harness settles — copying an in-flight file would freeze a flaky version. Recorded on QC8 (home), QD3 and QD2 (anchors).

## 0.88.0 - 2026-07-31

**The ⚑ badge stops taking part in line breaking, and every heading gains an address.** JL: "why is it on another line? it should be at the end of the sentence." The 260731 repair had glued the badge to the last word inside a `nowrap` group, which stopped the badge from landing alone but dragged the word down with it, so the reader still met a short line carrying `row. ⚑3` and nothing else. The badge now sits in a zero-width inline block (`.sbz`), so the browser breaks the sentence exactly as it would with no badge present and the pill paints off the final character; the demonstration sentence went from three lines to two. Because a badge that costs no width can paint past the text column, the sentence's `summary` reserves a 52px flag gutter and the pill hangs inside it. Measured rather than eyeballed: 111 window widths from 360px to 1800px across three pages, zero cases of the badge leaving its sentence's last line, zero cases of it crossing the card edge. Recorded on QB5a.

**Heading focus (QB5d's last five items).** Every rendered `##` section and `###` subsection heading now carries a rail at its END, invisible until that heading is hovered, exactly the contract the sentence rail and the `C1` chips follow: the generated breadcrumb (`QB4e / Where we are / Decision Now`, built from the heading's own label with its emoji, its `1/7` count and its `· 6 sections` suffix stripped), `⧉` for a subsection's text, and `🤖` for chat. The chip copies the address plus the markdown source path so Claude Code can open the right file without guessing. `window.__boardHeadingChat` reuses the page's existing session and fills the same Focus card, which gained a `kind` so one card serves a sentence or a heading. `wireHeadingPaths` runs inside the rewire hook, so a live swap regenerates both address families together. Two decisions worth stating: the rail collapses to zero WIDTH rather than `opacity:0`, because a breadcrumb is long enough to reflow the heading it decorates if it keeps its box while invisible; and `⧉` on a `##` heading keeps copying the section's TEXT (JL 260725), so copying the ADDRESS moved onto the chip. Driven in Chrome, not read: chip, `⧉` and `🤖` each verified by a real click. Recorded on QB5d, whose 19 items are now all ticked; the state line waits on JL.

## 0.87.0 - 2026-07-31

**RELATED FOLDERS: a third Index fold that opens the folders a board touches.** JL, with a screenshot of the Board Map and Section Matrix folds: add a third fold, "related folders", so a reader can "click open this folder, and see ... the skill ... and what this board folder should look like", then "do the B level." B is the clickable browser, and it ships at BUILD by EMBEDDING each named file rather than fetching it live, so the fold opens with scripts stripped and on a static host — the same reason `## Board Map` is ASCII, and what keeps QE3's one-file Law intact. A new `## Related Folders` grammar in board.md declares the folders and the files each opens (`@ <path> | <label>`, then `- <file>` lines); `parse.py` reads it to `meta["related"]`, and `page_board.py`'s `related_folders()` resolves each path under the board dir, refuses anything outside the repo root, inlines only `.md`/`.txt` under 120 KB, and renders every failure as a visible box. The fold reuses the `.board-status` disclosure shell so it matches the Section Matrix and hides with the rest of the index when a page opens, and it is emitted by BOTH packagings — the single `board.html` and the `board/` tree, through the same `tree_relink` the Board Map uses. On this board it opens two folders (the shipping engine, and the board folder itself) with four files embedded, and the index rail gains a 🗂 Related Folders row. A live `serve.py` endpoint for folders too big to inline is deferred to QC8. Also fixed the Board Map header typo "placement is not one." → "placement is not." Recorded on QB2 (the fold), QA0 (the folder list), and QC8 (the deferred live endpoint).

## 0.86.0 - 2026-07-31

**The terminal follows the tree router too.** JL asked CLI-Talk to read SDK-Talk's session and find what was missed; the answer was ⌨. SDK-Talk's `follow()` fix and its navtest suite cover the chat drawer thoroughly but never open the terminal, and reading their tree branches against the terminal code found two gaps. First, the `docPage()`/`docGroup()` branches called `chatOpen()` directly with no terminal hand-over, so navigating the tree with ⌨ on switched the drawer's LABEL while the old page's claude kept the screen — typing went to the wrong session, and the old PTY was never parked. Both branches now run the same dance the hash branch always had: park the old scope's PTY, rebind, reopen on the new scope. Second, every `termRelease` call inside `follow()` dropped the group argument, so leaving a GROUP terminal parked the board scope instead and left the group's PTY held; all three call sites now pass it. Proven the way SDK-Talk's directive demands, in a real Chrome before JL touches it: `termnav.mjs` (same CDP harness shape as navtest.mjs) drives group ⌨ on a tree page → navigate to a page → back to the index, asserting the drawer follows, each new PTY paints, and each abandoned PTY is PARKED not held (server-side reopen answers `reused:true`); plus the image-paste proof re-anchored to a tree URL since board.html is being discarded. 12/12 checks, zero JS errors, all test PTYs killed and the pasted fixture image removed after. Recorded on QD3 and QD1.

## 0.86.0 - 2026-07-31

**The page yields exactly as much as the rail takes, in both packagings.** JL: "when I drag the left panel the body text does not follow; board.html does, can you unify them." The rail's width had become `--sbw` in 0.85.0, but the body's `padding-left` was still hard-coded at `238px`, so widening the rail slid it OVER the text instead of pushing the text along. Both now read the same variable, which is exactly what `--chatw` already does for the chat drawer and the body it displaces: one variable, two consumers, no way for them to disagree. Verified over CDP by dragging in a real browser, and the two packagings return the same three numbers: rail 238 to 460, content left edge 369 to 480, content width held at 1000, identically on a `board/` tree page and in `board.html`. Recorded on QB2a.

## 0.85.0 - 2026-07-31

**A tree page is a FOCUSED page, and the rail can be dragged.** JL sent a screenshot of `board.html` in focus mode: "this is the format I want, look how wide it is, no boundary." A page in the `board/` tree is alone in its document, so it is permanently the focused page, and rather than inventing a second look for it (which is how the tree drifted three times today) all 79 `:target` focus-mode rules are now mirrored onto `body.split`. The card's coloured left bar, the Opening's accent bar, and the 820px width are gone on tree pages for the same reason they are gone in focus mode, and the index keeps them because it is not focused. The naive mirror needed two corrections found in the browser: it produced `body.split .q:target`, which a tree page never matches, and a `body.split .q{display:none}` that hid every page.

**Rail drag (`--sbw`).** JL: "can the left panel be dragged, it feels fixed." One CSS variable, a handle that sets it, width remembered per machine: the same shape `--chatw` already uses for the chat drawer. Range 150px to 60% of the window, double-click the handle to reset. The handle had to become a FIXED strip OUTSIDE the nav, because the rail is `overflow-y:auto` and clipped an absolutely-positioned handle so thoroughly that `elementFromPoint` returned BODY. Verified by dragging it over CDP: 238 to 440, then 440 to 180, with 180 surviving a reload, a jump to another tree page, and the single-file board.

**Two reversals, both mine.** Reading "I do not want boundary" as the `## Boundary` SECTION, CC removed it from 47 pages; JL meant the coloured bar down the left of the card. 41 were restored from git HEAD; 6 pages born today have no committed version and their Boundary text is lost. CC also removed the left rail entirely on a second misreading, and put it back.

## 0.84.0 - 2026-07-31

**The tree index and rail stop being a second implementation.** JL: "the ASCII here has not become real ASCII", then "compare your configuration with the original .md one, there are big differences, look carefully." Both symptoms had one cause: `render_tree` hand-wrote the index listing and the sidebar instead of reusing what `render()` already built. That silently dropped every `.gi` group-intro block, every `.gib` body, and all six `.gidia` figures (the per-group lane diagrams), so the ASCII was not failing to render as monospace, it was not being emitted at all; the rail lost its per-page section outline the same way, 54 `.sb-out` blocks and 298 `.sb-s` rows. Fixed structurally: the index loop is now `index_rows(meta, qs, href_for, group_href)` and the rail loop `sidebar_rows(qs, href_for, group_href)`, each parameterised only by how a link is spelled, and both packagings call the same function. Verified by a class-by-class diff of the two indexes: the only remaining differences are the progress bar and the ALL PAGES hint (both deliberate under JL's "only Map, Matrix and Activity" ruling) and one rail row, because the tree's Index is its own document. `pre.gidia` confirmed in the browser as `ui-monospace` with `white-space: pre`. This is the third time in one day that this family's own "one grammar, never two implementations" law caught its author, which is the argument for the law. Recorded on QB2.

## 0.83.0 - 2026-07-31

**A group page stops being a bare list, and Boundary becomes genuinely optional.** JL: "index has a template, page has a template, should the page GROUP have one too? Opening a group shows only a list, can it say what the group is for?" The group's intro has lived in `board.md` under its `### ` heading since 260724 and the group page simply never read it. It now renders as a PURPOSE line, with any further intro lines behind a "why this group exists" drawer, plus the group's own settled count. What derivation cannot give is a group that holds a decision, an open item, or a `state:` that closes; that needs a source file and a parser slot, and is `QB2`'s new Decision Now row.

**Boundary.** JL: "I remember I said I do not want Boundary." CC searched every page before acting and found no such ruling: `## Boundary` was ADDED by CC on 260723, and the only JL ruling touching it is 260724's `✅ Covered here` / `↪ Covered elsewhere` pair, about its internal shape. So the ask was either never written down or folded into the 260729 "keep the headings simple" pass, and either way this family's own rule applies: a ruling not written into a page does not exist. Now recorded on `QB4a` and made real where it binds: `ref/q-template.md` says OPTIONAL and tells an author to delete the section when the Opening already makes the scope obvious, and `haipipe-page` carries the same sentence for agents that load the spec instead of the template. Existing pages were NOT stripped: mass-deleting 54 Boundaries would be the blind sweep this board keeps warning about.

## 0.82.0 - 2026-07-31

**The tree index gains the three board-level components JL asked for, and the Board Map header stops being ugly.** JL ruled "for the tree index, we only want the Map, section Matrix, and Activity board", so all three are now on the tree's `index.html`, REUSED from `render()` rather than rewritten (the index-rows lesson, one build ago) with their `#fragment` links rewritten to tree paths by `tree_href_map` / `tree_relink`; the Activity markup moved into a shared `ACTIVITY_HTML` so both packagings emit the same block. All 61 link targets and all 54 Section Matrix cell links verified to resolve on disk.

Then JL sent a screenshot: "make these two styles consistent." The Board Map header was a two-column flex with a large title left and its blurb stranded right, wrapping to two lines; the Section Matrix header was one compact line. The map now uses the matrix's shape exactly (one line, one triangle, same padding, weight, size), with the blurb dropped because the body already opens with the same sentence. **Two stray triangles**, both found in the browser rather than the source: the `<summary>` disclosure marker, which `list-style:none` does not remove because a summary is `display:list-item` and Chrome draws it via `::marker`; and a real `::before` whose suppression rule had the SAME specificity as the generic `details[open]>summary::before` further down the file and lost on order alone. Both beaten explicitly.

**Two more real defects.** The tree's linked `board.css`/`board.js` had **no cache-busting**, so a shipped CSS fix did not reach the page at all (caught when a verified-correct rule had no effect); both now carry `?v=<assets stamp>`. And deleting a page's `.md` left its `.html` in the tree forever, still linkable and looking real; the tree now prunes anything outside the expected set, computed from every page so it stays correct under `--only`. Recorded on QB2 and QC9.

## 0.81.0 - 2026-07-31

**The tree survives contact with a real browser.** JL asked twice whether CC tests its own work, so the `board/` tree was driven over CDP with real clicks instead of checked with curl, and that found four defects no status code could. (1) **Every write in the tree failed silently**: a write posts `location.pathname`, the server takes its PARENT as the board folder, and from `board/QC/page.html` it looked for `board.md` inside `board/QC/`; seven writers now share one file-scope `boardPath()` that collapses the tree tail back to the board root. (2) `serve.py`'s `rebuild()` did not pass `--split`, so a comment written from the page updated `board.html` and left the tree stale. (3) Deleting a page's `.md` left its `.html` in the tree forever, still linkable and still looking real; the tree now prunes anything outside the expected set, computed from every page so it is correct under `--only` too. (4) The first render pass **reimplemented** the index rows with invented class names instead of reusing them, so not one CSS rule matched and the index rendered as a wall of inline links, and the left rail and chip popovers were missing from the template entirely; rows now come from one shared builder and the rail is the real `.sidebar`.

**Smoothness, both halves JL named.** Open drawers now survive the swap, keyed by POSITION because position is identity when only text changed (a first attempt keyed on summary text and only 1 of 3 open sections survived, which the browser test caught). Submitting a discussion line no longer calls `__boardRefresh`: the row lands next to the box that wrote it, in exactly the markup the next build emits, with a brief tint. Measured live: 3 sections open before and after, scroll unchanged, and the page does not move on submit. With the chat drawer open and a half-typed question in it, an update left the drawer open, the draft intact, and the terminal alive.

**One page changes, three files move.** `watch.py` passes the changed filenames to `build.py --only`, which rewrites those pages plus the groups containing them plus the index: 3 files out of 61. Verified in the browser that sitting on `QB4` while `QC9` was rewritten leaves `QB4`'s DOM untouched, its sections open, and its scroll unmoved. Recorded on QC9 and QD4.

## 0.80.0 - 2026-07-31

**An emoji in a figure is not monospace, and that is why every figure looked bent.** JL, of `QB4f`'s head figure: "it is very hard to read. Why?" The drawing was not the problem. A figure is authored in a terminal, where every emoji occupies exactly TWO cells and the author aligns the columns against that; the browser breaks the contract, because `pre` asks for `ui-monospace` and each emoji falls back to the system colour-emoji font at its own ~1.4-1.6ch. So a column that is straight in the `.md` arrives ragged on the page, differently per emoji, and the reader blames the figure. `body.pad_emoji()` now wraps every emoji cluster in a figure and `pre .eu` pins it to `2ch`, restoring the width the author drew against. Matched set is Emoji_Presentation=Yes plus anything wearing U+FE0F, with skin tones and ZWJ joins, so a bare `▶` or `→` is deliberately left alone: it has text presentation and already measures one cell. Applied to figures only (`pre.asc`, the `## Diagram` figure, and `pre.ip` inside item folds), never to a language-tagged code listing, where an emoji inside a string is somebody else's source. The SOURCE is untouched, so a figure still survives being copied into chat or a mail, which is `QB4b` §0's rule. Verified in a real headless Chrome against the served board: the three-row group in QB4f's figure now lands on one column, where before `⚠️` and `✋` sat left of `📎` on the same indent. Ships with JL's Files ruling in `ref/q-template.md`: one shared taxonomy is the STANDARD shape (`Engines` / `Input files` / `Output files`, the toolkit's own Input-Process-Output applied to a page's file map), renaming is the exception, and which group a file goes in is decided by what you DO to it rather than by what it is. Recorded on QB4f, with the remaining taste half (how far a figure may stop looking like a terminal) opened as a Decision Now on QB2.

## 0.79.0 - 2026-07-31

**The family's contracts become English, all of them.** JL ruled the QC1 language row option A and widened it himself: "yes, do it. Apply to all." `SKILL.md` (581 lines, 59% Chinese), `ref/board-form.md` (411 lines, 65%), and `ref/board-example.md` (111 lines, 41%) are now English, joining the five sibling units that already were; the family's own `ref/writing-rules.md` had stated the English-only ruling (JL 260724) that these three contradicted. All 32 rules that existed only in Chinese survived, each verified by grep against the output, including the three load-bearing ones: the page list needs the user's explicit OK before `open` proceeds (the skill's only mandatory stop-and-ask), "done means written back" in the same round, and the no-auth `/_term/`-is-a-real-shell reason the shared listener stays on loopback. Two categories of Chinese are deliberately KEPT because they are data a machine matches on rather than prose a reader follows: the legacy section aliases in `board-form.md` §4 that `ALIAS` still resolves, and the frontmatter's Chinese trigger phrases, which a translating agent had removed and which were restored, since dropping them stops a Chinese-speaking user from reaching the skill at all. Source-code comments stay out of scope by the existing `scrub_cjk_comments()` ruling: the source keeps its comments, the output stays English. Shipped alongside the staleness repairs the three reviewers found: the `live/` package is documented with real line counts and the moved `structure_op` / `serve_frame` / write-path citations repointed, the 0.78.0 Index removal corrected in three places, `Skill-<n>` and `Agent-<n>` added to the page-kind list and to `board-form.md` §1's discovery rule, the creator-agent fan-out marked not-yet-wired, the verb roster synced to 11, and the `ref/` table extended to every script including `gate_live.py`. The board felt it at once: warnings fell 34 to 12, because the Skill mirror pages stopped carrying Chinese into an English-only board. Recorded on QC1.

## 0.78.0 - 2026-07-31

**The Index row unfolds, and the three ctx disclosures leave the Index.** Two JL rulings in one round. "For the left panel headings, what should be the index's section content? Please add them as well": the rail's `🗂 Index` row now carries the same chevron and outline as a page row, unfolding the Index's own components in on-page order, 🗺 Board Map, 🩺 Section Matrix (page × column count), 📄 All Pages (page count), 📈 Activity, each present only when the board has it, each scrolling the Index to that component, open by default at load since the Index is the open "page". And "🦴 Topic · 🔄 Pipeline · 🧭 Board-Structure — I want to just remove this": the renderer no longer emits the three ctx disclosures; board.md keeps the sections as source-only documentation, and the Index reads spine → Board Map → Section Matrix → ALL PAGES → Activity. Ledger repaired again: group-level chat renumbered 0.77.0. Recorded on QB2 and QB2a.

## 0.77.0 - 2026-07-31

**Group-level chat: the third altitude.** JL: "for each Question group, we can also add the chat icon for them, and then we can add the sdk or cli to discuss about this Question group." Every group heading on the index gains 💬 beside ＋Q and 🗄; it opens the drawer attached to the GROUP. The design move that made it cheap: a group's session identity is its FOLDER path (`QC-engine/`), so `term_key`, HOLD, parking, the sidecar registry, names, and the picker all work unchanged — `live/chat.py` and `live/term.py` only grew `is_dir()` branches (session_of reads the registry's newest entry since a folder has no header line; remember_session skips the header write; the picker prefix is the folder's letter). `group_folder()` maps a heading ("QC · Engine") to its folder; serve.py resolves a `group` param on the session routes in place of `target()`. Scope sits between board and page: a group session may edit any `.md` inside its folder, and `group_prime_context` orients it with the group's pages and their states. The client threads `group` through chat, term, sessions, session-name, release, and the pagehide beacon. Verified live: a scoped SDK turn on QC answered through the group session (auto-named `QC-group-chat-smoke`), the picker listed it with the letter prefix, and the ⌨ group terminal resumed the drawer's session — the same two-front-ends-one-session law as pages. Recorded on QD1.

## 0.76.0 - 2026-07-31

**The family gains a second agent: `haipipe-board-creator-agent`, one page each, N at once.** JL: "we should have a new agent named haipipe-board-creator-agent, it can be called to write the pages markdown in parallels, instead of haipipe-board to write each of them one by one." The agent (`agents/`, v0.1.0) writes exactly ONE page from an assignment packet rather than from the board, so opening an eight-page board costs the slowest page instead of the sum, and every page gets an equally fresh reader of the specs. Its parallel safety is structural, not advisory: no Bash tool so it cannot rebuild, no claim on `board.md` so the registry every writer would collide on stays with the caller, and no sibling page may be read so two agents cannot duplicate each other's judgment mid-flight. The packet's `siblings` field is what lets a page write an honest `## Boundary` without reading the board. The caller keeps every shared write: registration, `lanes.py`, one build, one check, then `haipipe-board-reviewer-agent` judges the batch, completing the creator/reviewer pair the task and discovery families already run. This entry registers it in the family block and README only; the caller's fan-out procedure is NOT shipped, so `open` and `add` still write pages one by one. Both agents were set to v0.1.0 at JL's direction, matching the family's v0-series rule. Recorded on QC6 and Agent-2.

## 0.75.0 - 2026-07-31

**The SECTION MATRIX: the board's status as one derived table.** JL: "We want to have a dashboard to show the status of the board. Each row is a page, each column is a subsection. the cell might be some status." `board_status()` in page_board.py renders a shut-by-default disclosure between the Board Map and ALL PAGES: one row per page, one column per section (🧭 🖼 📚 🎯 📍 📎 🗄), every cell computed at build from the same parses the pages render from. The vocabulary: 📚 `n÷·m🖼` is divisions and how many open with their face diagram (the QB4c retrofit watched from one column), 🎯 `done/total`, 📍 `DN·k` owed Decision Now ticks, 📎 `n·gg` files and groups, 🗄 `Ln` Log lines; amber = incomplete, accent = waiting on JL, muted = absent. Cells link: click one and the page opens scrolled to that section. Hidden in the focused page view like the other Index components. Ledger housekeeping again: the concurrent session's terminal-survival and session-name entries are renumbered 0.73.0 and 0.74.0.

## 0.74.0 - 2026-07-31

**Sessions have names: `<page-id>-<what-it-is-for>`.** JL: "for each session, we can give them the name? like Qxxx-what-is-this-for? ... and this should be shown as well." The sidecar registry (`.haipipe-board/sessions.json`) entries grew from bare ids to `{id, name}` (old lists migrate in place); a name can be given at birth — the picker's ＋ New session row turns into an inline "what is this session for?" input, and the name rides the next `/_board/chat` or `/_board/term` POST — or later, via ✎ on any picker row → `POST /_board/session-name`. The page-id prefix is derived server-side from the owning file, so the stored purpose is bare and the display reads `QD3m-fix-black-screen`; named rows render bold monospace in the picker and take over the 🗂 strip summary; unnamed history keeps the first-message-title fallback (myrlin's shape). Names live in the registry, never the page header (QD1: the board's md records outcomes only). Verified live: named at birth through the terminal POST, renamed an old session, prefix correct, full terminal e2e still ALL PASS. Recorded on QD1.

## 0.73.1 - 2026-07-31

**Shift+Enter inserts a newline in the ⌨ terminal instead of submitting.** JL: "I cannot the shift+enter to have a new line, it just submitted to llm now." In a raw terminal Shift+Enter and Enter are the same byte (`\r`), so claude cannot tell them apart — the native CLI needs `/terminal-setup` to teach VS Code/iTerm2 a distinguishable sequence. Our xterm owns the keyboard, so no setup: `attachCustomKeyEventHandler` catches Shift+Enter and sends claude's native continuation sequence instead. Both candidates were tested by driving real bytes through the WS and reading the repainted screen: ESC+CR SUBMITS (transcript showed `❯ line-one` and a turn ran), backslash+CR inserts the newline (two-line draft, no submission) — so backslash+CR it is. Recorded on QD3.

## 0.73.0 - 2026-07-31

**"It works, then after a while it quits": three causes, three fixes.** JL opened a terminal, and minutes later it was gone; the diagnosis chain ran through the page, the server, and the environment. ① The asset-stamp full reload: whenever a rebuild shipped new JS (three sessions did, all day), the open tab's 4s poll hit `location.reload()`, whose pagehide beacon killed the PTY. Now the reload DEFERS while a terminal is open (`body.termon` + a "will reload when the terminal closes" badge; the queued reload fires on toggle-off), and the beacon PARKS instead of kills. ② Parking is QD3's item ⑤ shipped: `/_board/release {park:true}` keeps the process and pump alive, closes the WS windows, frees HOLD, and stamps a 600s deadline; re-clicking ⌨ inside grace reattaches the SAME pid with the ring replaying the screen instantly; a sweeper reaps expired parks; the drawer's hold kills a parked PTY first (one jsonl, one process — QD1). Verified live: park → process alive → reattach `reused:true`, same pid. ③ The quiet corruption underneath: serve.py restarted from a Claude Code session's shell passes `CLAUDE_CODE_CHILD_SESSION` down, and every board terminal silently ran with TRANSCRIPT SAVING OFF (caught on the PTY screen during the park test) — resume, the picker, and QD1's "the conversation IS the jsonl" all break downstream. serve.py main and `spawn_pty` now scrub the session markers; verified: the warning is gone and a turn grew the jsonl 7KB→48KB. Plus the mid-typing guard for JL's "add discussion … and the things are gone": the swap defers while a `.wrap` editor is focused or any draft is non-empty (QD4's Decision Now rows on the banner and the morph stay open). Recorded on QD3, QD4, QD3m.

## 0.72.0 - 2026-07-31

**The face-diagram rule, and the rail's two-control click.** JL ruled it in QB4c's Discussion: "please add it as a rule that after the subsection name, add the diagram-ascii to explain in high level about this section's concept or content." The rule is positional, no new syntax: the first fenced ascii figure directly after a `###` division heading is that division's FACE DIAGRAM. It is stated in QB4c §1, taught by `ref/q-template.md`'s Content guide, and demonstrated by QB4c's own four divisions; renderer pin-and-rank and the retrofit over existing boards stay open on QB4c's Decision Now. The rail's click model split on JL's follow-up ("for the right end of the page, add a hiden > ... the normal click will show us to the top"): a page row always navigates and a re-click scrolls back to the page top, while a hidden `▸` chevron at the row's end (rotating to `▾`) toggles that page's outline, accordion preserved. Housekeeping: two concurrent sessions had both cut "0.69.0"; the drawer-defects entry is renumbered 0.71.0 and the ledger is descending again.

## 0.71.0 - 2026-07-31

**Eight defects from a review plus actually clicking it.** JL asked for a re-review; the standing rule is that wire-green is not UI-green, so Chrome was driven over CDP against the live board and screenshotted after each fix. **Read from the code:** the `catch` path called `busyEnd()` without `traceEnd()`, so an aborted turn orphaned an un-collapsed trace and the next turn lost the reference; `chatOpen` cleared `.bd` without stopping the 400ms ticker, leaking an interval that wrote to a detached node for the life of the tab; `traceEnd` counted `.tr, .tool` but not `.tk`, so a think-then-answer turn collapsed to "0 steps"; a `wait` stub and `setBubble` were left dead. **Seen only in the screenshot:** the answer bubble was re-rendering the same narration already listed in the trace — the duplication of 0.68.0 had moved rather than gone — so the concluding segment is now pulled out of the trace and rendered as the answer (which also makes a no-tool turn read as one plain reply, with an empty trace removed entirely). **Found only by clicking twice:** the second turn on a question hung indefinitely on "Thinking". Two causes, both from M1: a browser reload aborts the HTTP request but not the coroutine, which kept running on the host loop with the held client mid-turn so the next `query()` queued behind it forever; and `live.lock` was created but never acquired. An abandoned request now cancels its future and evicts the client (its state is no longer known), a second concurrent turn on the same question is refused with a readable message instead of queueing invisibly, and the lock is held for the turn so `reap()` can see it. Re-verified after each fix: a two-tool turn yields two trace rows, two tool cards and one answer; a no-tool turn yields one plain answer; zero JS errors in either. Recorded on QD2.

## 0.70.0 - 2026-07-31

**The three tail sections gain subsections, answering JL's three page discussions (QB4d/QB4e/QB4f).** Items to Finish: `###` topic headings group the boxes and each visible group badges its own `done/total` (`render_items()` in page_question.py); empty groups are omitted and the overall count is untouched. Files: JL's default trio from the QB4f discussion — `Engines` (the skill files implementing the page's subject), `Input files`, `Output files` (what the board renders) — is the recommended example set in the spec pages and template guide, deliberately matching the rail's lane vocabulary; contextual names stay allowed. Where we are: decided decisions group under context-named topics (`### Decisions taken` on QB4e is the worked example) beside the reserved `### Decision Now`. The rail unfolds all of it: 🎯 rows list the item groups with counts, 📎 rows list the file groups. And the active page's rail row is now a toggle (JL: "click that again, I collapse that page level content"): click folds the outline, click unfolds, fresh navigation always starts unfolded. Worked examples live on the three faces themselves: QB4d's own Items, QB4e's own Where we are, QB4f's own Files.

## 0.69.0 - 2026-07-31

**The ⌨ black screen's real root cause, found by clicking the board in a real browser.** JL asked "did you clicked it yourself?" — and the answer was no: every prior green was wire-level (a Python WS client speaking ttyd's protocol), which is exactly why the defect survived four ALL-PASS batteries. Driving a real Chrome (headed and headless, CDP, no libraries) through the actual gesture — fab → 💬 → ⌨ — reproduced JL's black pane deterministically, and the instrument trail (netlog: full 200 body downloaded; script-tag listeners: both assets LOAD; a MutationObserver on the toast) finally surfaced the swallowed exception: `You must set the allowProposedApi option to true to use proposed API`, thrown by `loadAddon(Unicode11Addon)` and eaten by `termOpen`'s catch into a 3-second toast. One line fixes it: `allowProposedApi: true` in the Terminal constructor. After the fix the same clicked run paints the full Claude Code TUI in the drawer (screenshot-verified), WS open, 45 buffer lines. Three more fixes from the same independent check of the QC8 split: `USE_TTYD` had stayed behind in serve.py while `terminal()` moved (every term open crashed `NameError`; the fix then hit `terminal()`'s local `base` string shadowing the module — aliased `_base`); `live/xcal.py` resolved `xcal-boot.js` against its new `__file__` (`live/assets/`, absent — every excalidraw scene 500'd; now `base.HERE`); and a rapid respawn after release races the dying claude for the same session (`kill_term` registers the pid in `DYING`, the next spawn waits up to 2s in `wait_dying`; three zero-spacing e2e runs pass). Lesson, in QD3's words: an exception after `termView(true)` IS a black pane — the wire can be perfect while the front end dies silently in a catch. Recorded on QD3, QD3m, and QC8.

## 0.68.0 - 2026-07-31

**Interim and final become two different things on screen, and a live working line.** JL's screenshot showed four assistant bubbles where each repeated all of the previous text plus a little more. That was a regression 0.67.0 introduced hours earlier: making a tool call start a new bubble (`cur = null`) without resetting the text accumulator, so every new bubble re-rendered the entire turn. The fix is the shape JL asked for in the same message — a turn now opens ONE `.trace` box (fixed height, scrollable, smaller type) holding every interim message with a per-kind icon (✻ working · 💭 thinking · ✍️ narration · ⚒ tool card), while the answer renders once beneath it at full size; narration is accumulated per SEGMENT and reset at each tool boundary, which removes the duplication at its cause. Once the answer lands the trace dims and collapses to a step-count label, so a finished turn reads answer-first. A second bug found by a static consistency check on the way: `done` still wrote the full answer into `cur` via `setBubble`, but `cur` is now a trace ROW, so that would have replaced the row's markup and destroyed the interim text — the `done` branch no longer touches `cur`. Also new: the live "still working" line JL asked for after comparing with the CLI ("check how claude code indicate that the claude is still working"), replacing a static `…thinking` bubble that the first event deleted — a pulsing glyph cycling ✻ ✽ ✳ ✢ ·, the current activity (Thinking, the tool name and its target, Responding), and elapsed seconds, honoring `prefers-reduced-motion` and removed when the answer arrives. Verified live with a deliberately two-tool turn: three separate short narration rows, two tool cards carrying their real outputs, one answer. Recorded on QD2.

## 0.67.0 - 2026-07-31

**Decision Now joins the sidebar outline, and `###` becomes a real heading everywhere.** JL: "ok, also unfold the Decision Now in the sidebar, go ahead." `structure_rows()`'s Where-we-are row now carries that section's `###` subsections; each renders as an indented rail row found by heading text (`data-t`), and a Decision Now row appends how many ticks it owes ("Decision Now · 3 to tick"). Shipping it exposed a rendering hole: `###` inside a non-Content section fell through body() as literal "### …" prose — twelve pages' Decision Now headings rendered that way. body() now renders them as `.sh` subsection headings (Content is untouched: its `###` lines are split into divisions before body() runs), which is also the anchor the rail scrolls to. Recorded on QB2a and QB4e.

## 0.67.0 - 2026-07-31

**The drawer shows the trace, not just the answer.** JL put the board's chat drawer and the VS Code plugin side by side and asked what differed, then named it: "make the thinking and tool calling to be out as well." The drawer had been discarding the trace on both sides of the wire: `live/chat.py` emitted `{"t":"tool","name":…}` with no input and never emitted a tool RESULT at all, and `board.js` wrote that bare name into the transient waiting line, which the next event overwrote — so a turn that ran ten tools left no evidence of any of them. Now `ToolUseBlock` carries `id`, `brief`, and a truncated input preview (Bash reads as its command, everything else as indented JSON), `UserMessage`'s `ToolResultBlock` is emitted as `t:"tool_result"` and matched to its card by `tool_use_id`, and the drawer renders one collapsible card per call in the plugin's shape: what ran, its input, then its output, with errors marking the card instead of vanishing. Cards are closed by default so a tool-heavy turn stays readable, and previews cap at 4000 chars because a card is a preview, not a log viewer. One visible bug fell out of the same screenshot comparison and is fixed here: `mdInline` handled code, bold, and italic but not `[text](url)`, so the status strip's own link printed as literal text with the full URL showing; links now render, restricted to http/https so an escaped `javascript:` cannot ride in. Verified live with a turn that forces a real Read (thinking streamed, the card carried the resolved path and the file's first lines); QC8's gate re-run green. One checker bug surfaced on the way and is fixed here: `check.py`'s dead-href scan read the whole file rather than the scripts-stripped `bare` it computes two lines above, so `board.js`'s own anchor builder was reported as a rendered link with an unresolvable href; a string inside inlined JavaScript is a program, not markup. Recorded on QD2.

## 0.66.0 - 2026-07-31

**The sidebar gains a per-page section outline, accordion enforced.** JL, pasting the Structure rows ("🎯 Items to Finish · 2 done · 1 open …"): should the sections be in the left panel too, "and make sure that everytime, only one pages's section and subsection can be opened". The Structure map's counting logic moved out of `render_structure()` into a shared `structure_rows()` (page_question.py), and the sidebar now renders those same rows — section emoji + name + meta, plus one indented row per Content division — under every page, hidden by `.sb-out` until that page is the open one; `mark()` collapses every other page's outline on navigation, so exactly one page's sections show at a time. Clicking an outline row navigates, then opens the target `<details>` and scrolls to it (division rows open Content first). Because drawer and rail read one source, they can never disagree. Owned by the new design-board face QB2a-sidebar/QB2a-sidebar.md, opened on JL's ask this round.

## 0.66.0 - 2026-07-31

**QD2 M1: the drawer holds one `claude` per question.** JL asked to continue into `live/chat.py` after the QC8 split. `SessionHost` runs one asyncio loop for the process's life and owns every live `ClaudeSDKClient`; the HTTP thread only submits to it, because the SDK forbids a client crossing async runtime contexts and `chat()` previously ran a fresh `anyio.run` per POST. Three things holding a client makes necessary, all built: a stable `can_use_tool` shim (a held client keeps its connect-time callback, so without indirection message two's permission prompt would be written into message one's dead socket), eviction when the ⌨ terminal takes the same question (QD1's one-window Law), and an idle reaper at 30 minutes plus `killall` teardown, since a held client is a live process. `--no-hold` is the fuse, in the `--ttyd` pattern. Measured on the design board at the scoped tier: first token 11.34s, then 2.27s, then 1.17s, with the stage line reporting "session already up" from turn two; verified again on the live 5599 board. **Two corrections the measurement forced**, both recorded on QD2: the first build showed no win at either tier because the fingerprint folded in the resumed session id, so every turn silently reconnected while still reporting success (only the stage line exposed it); and the "8.1s per message" figure this skill's own page claimed was wrong, because a resumed session plus a warm page cache already made turn two cheap without holding. The durable case for M1 is that `interrupt`, `set_model`, `set_permission_mode`, `get_context_usage`, and `rewind_files` exist only on a live client. QC8's gate re-run green (M1 on against M1 off, 18 responses and 54 files identical); `test_hold.py` added as the two-turn latency probe.

## 0.65.0 - 2026-07-31

**serve.py splits into `live/`.** JL: "could we separate them? ... I don't think it is good to put all the things in one." QC8 opened as QC3's deferred half (that page split `build.py` on 260724 and recorded that it left the live layer alone "while it is still forming"), and this ships it. `gate_live.py` came first, per QC3's Law that a refactor moves code under a gate and features never ride along: it starts a real server against a FROZEN throwaway copy of the design board, drives 18 requests covering every route including the error paths, and hashes all 54 written files, passing responses and file contents through one narrow `norm()` so a clock or uuid cannot fail it. The move itself is machine-made: every method body sliced by `ast` and copied byte for byte into a mixin, so no line was hand-retyped. `serve.py` goes 2933 → 361 lines (imports, the mixin assembly, `do_GET`/`do_HEAD`/`do_POST`, the daemon, and the console re-exports); `live/` carries base 154 · structure 274 · write 259 · xcal 465 · activity 408 · chat 702 · term 563. The gate earned itself on its first run by catching `@staticmethod` decorators being dropped (the slicer started at `def`, not at the decorator), which would have shipped eight silently broken methods; two gate defects found alongside it were fixed rather than tolerated. `from serve import structure_op` and the other console imports still resolve, so `boards_api.py` is untouched (QE3's Law). Ends green: 18 responses and 54 files identical, live 5599 restarted on the split code. Recorded on QC8.

## 0.64.0 - 2026-07-31

**serve.py owns the PTY; ttyd becomes the `--ttyd` fallback.** JL approved QD3m §8 ("ok, go ahead and implement it"): myrlin's method rewritten in stdlib Python, no AGPL code crossing. `spawn_pty` (pty.openpty + os.login_tty + TIOCSWINSZ), one reader thread per terminal feeding a 256KB ring buffer and every attached WebSocket client, with a UTF-8 tail guard so a multibyte codepoint is never split across frames (the per-message TextDecoder mojibake cousin of the QD3 smear). `/_term/<key>/ws` is now terminated by serve.py itself — RFC6455 handshake, masking, ping/pong, continuation — while keeping ttyd's wire protocol verbatim (auth/size JSON, '0' input, '1' resize, '0'-prefixed output), so board.js needed no wire changes. Reconnecting clients get the ring replayed instantly (myrlin's trick); a new client joining a running terminal sees the screen at once. Lifecycle carried over: HOLD, session picker parameter, killall, pagehide beacon; reaping now sweeps `<key>.pid` files whose ps command matches our claude spawn signature (pid-reuse safe). Terminal-side image paste landed with it: pasting over the ⌨ pane saves through `/_board/image` and types the repo-root-relative path into the PTY. Verified live: 7-step end-to-end in 24s (spawn → handshake → TUI boot → real PTYOK turn → resize → second-client ring replay → clean release), two questions coexisting, killall reaping both with zero orphans. ttyd stays behind `serve.py --ttyd` until JL's click-through, then the brew dependency can be deleted. Recorded on QD3m and QD3.

## 0.63.0 - 2026-07-31

**A stale tab can no longer eat a write: assets stamp + guarded rewire.** JL: "still hard to add the discussions … I just added one in QB4c" — and the server log shows NO discuss POST ever arrived: the text was lost client-side. Root cause is QD4's blind spot: the in-place swap keeps a tab's scripts alive forever, three sessions shipped 0.57→0.62 under an open tab, and the stale JS rewiring newer markup threw, leaving every ➕ button dead — clicks that post nothing. Two guards: `page_board.py` stamps `<meta name="board-assets">` (md5 of the inlined JS+CSS) and `tick()` does one full `location.reload()` when the fetched stamp differs (a poor tab's HMR, no toolchain); and `safewire()` runs every wire function in its own try/catch (console-visible) so one throw cannot kill the buttons after it. Tabs opened before this ship need one manual hard reload; later ships reload them automatically. Also answered JL's repeat Node/npm ask on QD4's Discussion: verdict stays no Node — the npm cure for this failure IS hot-module-reload, which the stamp now provides; the mature-stack direction lives on QE3 (haichat-board). Recorded on QD4.

## 0.62.0 - 2026-07-31

**One Q, many sessions: the session picker; plus a drag-resizable drawer.** JL amended QD1's Law ("one Q, multiple session. the chat session with the predefined prompt related to this Q") and asked to choose the chat history when the drawer opens, from the index or any page, with the picked session reaching the ⌨ terminal too. `serve.py`: every id it mints or adopts is now recorded per question in the gitignored sidecar `.haipipe-board/sessions.json`; the new `POST /_board/sessions` lists current + history with landed/mtime/size and a title read from the jsonl's first user message (myrlin's `discover()` shape, rewritten by design, no AGPL code crosses); `/_board/chat` and `/_board/term` accept `session: "<uuid>"|"new"`, where picking resumes that session and makes it current (the header follows), "new" mints fresh, and an explicitly picked session restarts a running ttyd. `board.js`/`board.css`: a 🗂 Session strip under the drawer header (current first, history by last write, ＋ New session; opens itself when there is a real choice), the drawer textarea takes pasted images through the existing `/_board/image` and inserts a repo-root-relative `fig/` path that claude can Read from the SPACE root, and the drawer's left edge is a drag handle driving the shared `--chatw` variable (drawer width and the page's yield together), persisted per machine. Verified against the live 5599: QD1's session listed with its title; an explicit resume of the current id left the header byte-identical; `session:"new"` minted into QD3m's header and the sidecar; the whole-board index session listed too. The myrlin reuse plan (copy ruled out by AGPL; run-beside or rewrite-by-design; phases P0-P3) is QD3m Content §7; this release is P1. Recorded on QD3m, QD1 (amended Law), and the QD lane.

## 0.61.0 - 2026-07-31

**A hideable pages sidebar.** JL: "I also think to added the sidebar so I can choose the pages more easier ... like the side bar, and then index, QA, QA1, QA2, etc ... and that sidebar can be hidden as well." `page_board.py` now renders a fixed left rail from the same listing as the index rows — `🗂 Index`, then each group heading, then each page as state emoji + id + title — so the rail exists with JavaScript off and never drifts from `## Pages`. It sits OUTSIDE `.wrap`, untouched by the `:target` show/hide rules, so it stays up in both the Index view and an open page; a group link re-targets `#group-…`, which also restores the Index. `board.js` adds the ☰ toggle (state persisted per board in localStorage), the active-row highlight on hashchange, and the narrow-screen behavior (overlay, closed by default, a jump closes it). CSS default with no saved choice: open at ≥1150px, hidden below; the rail is print-hidden. Recorded on the design board's QB2.

## 0.60.0 - 2026-07-31

**Screenshots paste into the comment and discussion boxes.** JL: "when I take the screenshot, can it be paste there?" A paste listener on the comment box and every discussion box catches a clipboard image, POSTs it as a data URL to the new `/_board/image`, which stores it under the board's `fig/` (sanitized stem + timestamp name, 8MB cap, png/jpeg/gif/webp only) and returns the relative path; the box gets `![image](fig/…)` inserted at the cursor, and the visible row still lands through the unchanged discuss/comment write — which is also why the upload itself never rebuilds. Rendering needed nothing: `note()` already ran markdown images inside `> WHO:` rows and the global `img{max-width:100%}` bounds them. Verified end to end against the live server: upload, sanitized filename, HTTP 200 serve, bad-base64 rejection. Recorded on QB4g and QB5b.

## 0.59.0 - 2026-07-31

**Fold prose takes sentence comments.** JL asked, on the design board's QB4g itself: "When I try to add the comments, it does work, why?" The refusal was frontend-only: three blanket `.folds` guards in `board.js` (the highlight scanner's `scan()`, the select-to-comment `containingSentence()`, and the double-click editor) excluded the whole drawer, while `serve.py`'s `_sentence_line` anchor rule already lands a `> WHO:` row under any plain source line regardless of section. The guards now exclude only what cannot anchor: `.cmt` rendered comments, `.sapp` apparatus, and the non-`<p>` Log/bullet rows that were never reachable anyway. On rebuild a fold comment renders as a `.cmt` row directly below its sentence, since fold bodies pass `apparatus=False`. Ruling recorded on QB4g §2.

## 0.58.0 - 2026-07-31

**Address chips move to the heading's end and reveal on hover.** JL read `C1` prepended to an authored `1 ·` heading as "C11 · Content: establish the substance" and asked for the sentence's contract: "make the C1 to be the end of the sentence, and only shown when we hover it, just like the sentence". `board.js` now appends `.caddr`/`.haddr` instead of prepending; `board.css` holds both at opacity 0 until their heading is hovered (chips therefore stay hidden on touch, like the sentence chip). Addresses, refs, and the chat packet are unchanged: this is display only. The per-division diagram ask from the same message is NOT shipped here; it waits as a Decision Now row on the design board's QB4c.

## 0.57.0 - 2026-07-31

**Decision Now reaches the template guide.** JL, same day, two rulings in one thread: "don't make the decision here ... Always go to the corresponding Q's Where we are's subsection of Decision Now", and the reply must name which page and section were updated. `ref/q-template.md`'s Where-we-are guidance now teaches the subsection (one `- [ ]` row per pending human decision: ask, options, recommendation; machine writes, human ticks; answered rows move into the dated record). The rule itself is OWNED by `haipipe-page` 0.2.0, and the reply footer by `haipipe-board-routing` 0.2.0; this entry is only the template catching up.

## 0.56.0 - 2026-07-31

- **`Agent-<unit>-<slug>` is a page kind below the skills** (JL 260731: "Should we separate the Agent from Skill? ... we will call it Agent-1 ... Below the skill").
  The reasoning is the morning's Q-Skill lesson applied once more: the label must say what the thing IS, and a skill is LOADED into a context while an agent is DISPATCHED into a fresh one.
  The reviewer is now `Agent-1`; it wears an AGENT badge, stays out of the settled count, sorts after the Skill rows, and `Skill-2` plus the old named id remain declared Links.
  `skillpage.py` discriminates by what it mirrors (a folder is a skill, a lone .md is an agent), mints `Agent-<n>` starting at 1, and `page_files`, `PAGENAME`, and the checker's listing scan all accept the prefix.
- **`Opening` is the ONE name of the lead section, on every page kind** (JL 260731: "just one single Opening, Remove all the Question things from the skills").
  The canon flipped in the renderer's own alias table, so every page ever written as `## Question` parses forever; the checker's required list, its construct probes, serve.py's ＋ button skeleton and rule strings, `ref/q-template.md`, and every reference doc now say `Opening`.
  A skill page is consistent with every page AT THE SECTION LEVEL and flexible below it: `### SKILL.md` is one Content subsection, which the managed body span already produced.
- The boardform restructure had silently broken three of the paper board's cross-board Links (the failure mode `ref/board-form.md` §1 documents); they are repointed and that board is back to 0 errors, 0 warnings.

## 0.55.0 - 2026-07-31

- **The family ships QC6 §8's shape: one door, three specs, one verb** (JL 260731:
  "make the haipipe-board thinner, and have other skills ... please creating them now").
  `haipipe-page` and `haipipe-sentence` are loadable SPECS, cut contract-first from the QB4* and QB5* faces: what a page and a sentence ARE, for a consumer with no board open.
  `haipipe-board-routing` is the unit VERB: one input, the owning page and section found through `## Pages` only, one anchored write, ending LANDED, PROPOSED, or REPORTED.
  Both write laws ride along with their provenance: propose a tick, never tick (QC6 §10), and mechanical-always, editorial-never on another family's board (QB1 §4).
- No code moved: the specs cite `ref/q-template.md` and `ref/board-form.md` §5 as their authority and must never fork them.
  The named next step is making `serve.py`'s two hand-rolled rule strings consumers of the specs, which kills the copy that already rotted once.
  `haipipe-board-digest` stays on the roster unshipped; a page-kind variant still ships under its consumer family.
- SKILL.md gains the family block so the door routes to the units, and the family README lists all six.

## 0.54.0 - 2026-07-31

- **Every page id now matches its group letter** (JL 260731: "I think you also need to align the Q name to the Q group as well").
  36 of 43 pages on `BoardSkillBoard-260722` were renamed: `QA1a → QA1`, `QAa5 → QB9`, `QB5 → QC3`, `QE1 → QD7`, `QA9 → QE1`, and so on.
  The rename is two-phase, because the map collides with itself: `QC3-folderq.md` must become `QB3-*` while `QB5-srcsplit.md` becomes `QC3-*`, so every file parks at a `__tmp__` name first and nothing ever lands on an occupied one.
  A NAMED family keeps its name: `Q-Skill-haipipe-board` is identified by which skill it mirrors, never by a position in a queue.
- **An alias travels like a real address.** The rename stranded every older id in the figures that cite it: `QAa5` was suddenly not a page, so it rendered as dead text even though `## Links` knew exactly where it went.
  `link_faces` now also links a declared Link whose target is a page on this board, showing the OLD id (what the author wrote, and what a reader is looking for) and pointing at the CURRENT page.
  45 such alias links now travel on this board, and no citation anywhere in the repo had to be rewritten, so a changelog entry that says `QB5` still means what it meant on the day it was written.
- **`## Board Map` opens with a folder lane** (JL 260731: "did you say what folders are used here? engine folder, output folder ... I think here we need to mention this as well").
  A reader who knows how the groups connect but not which folder holds the engine still cannot act, so the map now has three lanes: the folders this board works with, how its five groups connect, then the cross-group page edges.
  The section heading moved from `Pages and their relationships` to `Folders, pages, and how they connect`.
- `QA0 · Three folders: the skill family, its board, and what it renders` is the new first face, modelled on the paper family's `QA1-eight-folders`.
  A first draft numbered `haipipe-board`, `haipipe-board-index` and `agents/` as three peers, and JL corrected it: "I want 1 or 2 to be large folder like skill/board ... board folder, is the (2) ... subskills are the subskills in (1)".
  `skills/board/` is ONE folder on disk and one family in the roster, so it is one number, and a subskill is a unit inside it, a peer of the engine rather than of the board.
  That collapses seven numbers to three and makes the pair exact: `①` what ships, `②` what argues it, `③` what it renders.
  Its test is one line: delete `②` and every skill in `①` still runs.
- **A parent page carries its faces as sub-letters** (JL 260731: "could we have page QB5 to QB11 to QB4a to QB4b ... and QB12 to be QB5, and then we have QB5a, QB5b").
  QB4 is the page and QB4a-QB4g its seven section faces; QB5 is the sentence and QB5a-QB5e what attaches to it.
  The id grammar already allowed the trailing letter and sorts it after its parent, so this cost no parser change: 13 renames, two-phase, every old id kept as a declared Link.
- **The skill roster is its own page KIND** (JL 260731: "remove Q, from Q-Skill to be Skill ... Like Skill will be a special Page. Like Skill-0-xxx, Skill-1-xxx").
  `Skill-<unit>-<slug>.md` parses with id `Skill-<unit>`; it renders with a SKILL badge, leaves the settled count (`page_board.py` excludes the kind), and is exempt from the S-page stage sections in `check.py`.
  The old name was a standing contradiction: a `Q-Skill` row was counted as a question and declared not to be one.
  `skillpage.py` mints the new form, discovers pages through `page_files` so both eras sync, and `find_page` answers to `Skill-<unit>`.
  The named-family form `Q-Skill-<name>` still parses everywhere, so no other board moved.
- **QD split into QDa · Working and QDb · Sharing** (JL 260731: "should we separate the Working and Sharing ... You can have QDa and QDb").
  The 260730 merge had been mine, made to free the QE letter for Execute; JL's subgroup letters keep the letter free AND the two responsibilities separate, which is strictly better.
  QDa1-QDa6 working, QDb1-QDb6 sharing; 261 tokens repointed in one pass; every QD1-QD12 id stays a declared Link.
- **`QDa7 · Board-level agent` returned from the archive** (JL 260731: "QD5-boardagent.md should be in the Working").
  Archived 260725, its subject (one session whose scope is the whole board: adding pages, regrouping, batch rewrites) is working-layer machinery, the same serve.py session/HOLD stock as QDa1-QDa3.
  Its ids were repointed on restore and its five pre-rule em-dashes fixed; it returns 🔴 OPEN, and its collision with QDa1's one-session-per-question LAW is still the item that matters most.
- **The subgroup letters flattened the same day: QD · Working, QE · Sharing, QF · Execute** (JL 260731: "could we update it to QDa QDb QE to QD QE QF?").
  The QDa/QDb split had overloaded the lowercase-letter device: `QDa` was a group while `QB4a` is a face of page QB4.
  Flat letters restore one meaning per device, and Sharing returns to its ORIGINAL ids, `QE1-hosting` through `QE6-bindaddress`, which erases that token's era ambiguity outright.
  Execute now sits at QF, diverging from the paper board's QE; group letters were never aligned across boards, so nothing depends on the match.
  15 renames, 301 tokens repointed in one pass, QDa*/QDb* kept as declared Links, and two citations of the RETIRED QF2 ruling de-linked because that id now belongs to Execute's newcomer page.
- **A sequential rename map is a corruption engine, and it ran twice today.**
  Applying `QA1→QB1` then `QB1→QC1` as ordered replacements dragged tokens two steps, so board.md prose said `QC1 owns the words` where QA1 was meant; the same pass also rewrote `QA1@paper`, which names a page on ANOTHER board.
  The repair: rewrite as ONE regex alternation with a dict lookup, never in sequence; treat `@board` suffixed tokens as untouchable; and rewrite the affected prose sections wholesale where the claim itself had gone stale.
  286 prose tokens across 35 pages were then repointed the same one-pass way, because 17 short ids were RE-USED by the alignment and an alias cannot help a token that now names a different live page.
- Prose reflowed to ONE SENTENCE PER LINE across every file touched today (JL 260731: "why it is one sentence multiple line, instead of one sentence one line?").
  The rule is the board's own, stated at `check.py:255` and repeated in `ref/q-template.md:175`, and hard-wrapping violated it invisibly: `check.py:271` exempts lines starting with `-` or two spaces, which is exactly the shape of a dated entry.
  It was not cosmetic. A group intro joins its source lines with `<br>` and ctx prose emits one `<p>` per line, so a wrapped sentence rendered as `groups in the<br>first place.` on the live index.

## 0.53.0 - 2026-07-30

- **A figure is now a map you can travel on** (JL 260730: "make the ASCII canvas clickable").
  `link_faces` in `src/body.py` wraps every page and group id inside an ASCII figure as a link: fenced figures, indented-fence figures inside a bullet, and the group-intro figure on the index.
  The wrap happens AFTER `esc()` and adds no characters to the line, so monospace alignment is untouched; the href is a plain fragment, so travel works with scripts off and on a static host, exactly like an index row. 122 links across 25 of 61 figures on the boardform board, 262 on the paper board.
- `FACE_IDS` / `GROUP_IDS` are the authority, and `_face_pat` orders the alternation LONGEST FIRST, which is what keeps `QAa0` from being read as the group `QAa`, `QA6` from being read as `QA`, and `Q-Skill-haipipe-board-reviewer-agent` from being cut down to `Q-Skill-haipipe-board`.
  A token that is not a page or group on THIS board stays plain text, so a retired or renamed id reads as dead text in the figure and the canvas checks itself on every build.
- A group heading now carries `id="group-<token>"` (`bd.group_token`: `QA · Defining a board` → `QA`).
  A group is not a page: `#group-QA` scrolls the index, it does not open a card, and nothing about the settled count changes.
- Topic, Pipeline and Board Structure render with `fold_code=False`.
  They already sit behind a `<details class="ctx">`, so a long fence folding itself into `</> code · N lines` in there was the double fold the board's own Law forbids: a fold that works and cannot be seen.
  A board-level canvas is the content of its section, so it stays on stage at any length.
- **The two canvas altitudes** (JL 260730, correcting a first attempt that put the whole 41-page roster on the index): a page is a WORKING RECORD, not an undecided question, and the board level does not need the roster twice, because the index already lists every page below.
  So the board-level figure now shows what the index cannot, which is how the groups CONNECT (main line QA → QAa → QAb, QB shipping, QD/QE as parallel layers, Q-Skill declared) plus the handful of real cross-group page edges.
  Each GROUP intro then carries its own `⚙️ engine · 📋 pages · 📂 folder` lane block, one row per page: which engine file governs it, and which folder artifact it produces. 7 group figures, 41 links in them; the board canvas is 15.
- That per-group map needs no engine work: a group intro has accepted a ``` figure since QC2 (JL 260724) and `parse_dir` already collects it verbatim, so the lanes are board CONTENT.
  `?` in an engine cell means the mapping is not verified yet, which is the honest state and doubles as QAa7's to-do list.
- **This board's own groups restructured to the three-layer model** (JL 260730, after the same split was field-tested on the paper family's Skill-Board): seven groups became five.
  `QA · Design` what the Board system is · `QB · Delivery` what a reader gets, Board → Group → Page → Section → Sentence · `QC · Engine` how it is made and shipped · `QE · Execute` what actually ran, with evidence and a reopen path · `QD · Working and sharing` the live layer, absorbing the former QE Sharing.
  Execute is the layer that keeps "skill written, delivery defined" from passing as done.
- Every one of the 42 page ids survived, so no citation anywhere in the repo broke: QA1 now sits in Delivery, QB1 in Engine, QE1 in Working.
  A page's LETTER is the group it was OPENED under, never where it is listed now, and after two restructures most pages wear a letter older than their group.
  Five group folders replace seven (`QA-design/ QB-delivery/ QC-engine/ QD-working-and-sharing/ QE-execute/`), moved with `git mv`, and every `oldfolder/page.md` citation inside the board was rewritten.
- The Board-Structure canvas now draws those five groups and their edges, and every id in it travels, so the index's own map is the first thing that proves `link_faces` works.
- **`## Board Map` is a board.md section, and ASCII wins** (JL 260730: "what is the section for board map?
  I think I might need the ASCII version ... and make it collapsable").
  It holds one ``` figure and beats BOTH canvas sources, because a figure draws on a static host with no Excalidraw endpoint and no share URL, survives with scripts off, and has links in it, so it is the only map a reader can travel on.
  `board_map()` therefore takes three sources in priority order: `## Board Map` → `board-map:` share URL → the local `board.excalidraw` scene through the declared Excalidraw host.
  A board with no `## Board Map` renders exactly as before.
- It renders as `<details class="board-map board-map-ascii" open>` rather than a fixed 62vh block: a map you cannot shut pushes the index off the first screen.
  The whole map head is the handle and the caret rides the `BOARD MAP` kicker, so no second control appears.
  The figure keeps `pre.asc`'s own padding, so no new rule can disturb its alignment.
- On this board the map moved out of `## Board Structure` into its own `## Board Map`, and the now-dead `board-map:` URL was deleted, which closes the two-sources-of-truth hole the static-host workaround had opened.
  The shared canvas survives as a link inside the section.
  `## Board Structure` keeps the source-to-webpage line and its prose.

## 0.52.0 - 2026-07-30

- A Board may now carry `## Board Structure` in `board.md`. It renders as a native
  disclosure after Pipeline on the Board-Webpage-Index, remains readable without JavaScript,
  and does not become a Q/S page or enter the settled count.
- The design vocabulary separates `Board-Folder` from `Board-Webpage`, and the latter into
  `Board-Webpage-Index` and an opened `Board-Webpage-Page`. The former QA0 map page on the
  design Board was archived and its external Excalidraw map entry preserved in Board-Structure.
- The former QA10 page is now QA2b, `Board-Webpage Design`; legacy `QA10` remains a declared
  link alias. Parsing and rendering remain backward-compatible for Boards without the optional
  section.

## 0.51.0 - 2026-07-29

- Opening's drawer now opens with a generated `Structure` row (JL: "the Structure subsection
  just above Boundary"): `render_structure` in `src/page_question.py` maps the page from its
  parsed sections — one row per section that exists, Content division names under their count,
  item/entry/file tallies — so the map is render-only and can never go stale. `.pmap` styling
  in `assets/board.css`; drawer order is now Structure → Boundary → Why this matters → S rows.
- Specs updated in the same change (one face, both projections): `ref/q-template.md`,
  `ref/board-form.md` §8 (also repairing the stale "Q rationale becomes Content's first
  subsection" sentence), and SKILL.md's page section.
- Design faces: QAa1 §7 owns the Structure decision; QAa0's diagram and Law carry the new
  drawer order; QAa0 §1 records the base/variant model (a page kind redefines only Content and
  ships under its consumer family); the five sibling QAa faces are marked frame.

## 0.50.0 - 2026-07-29

- Reader-facing Board links now honor the machine-local `HAIPIPE_BOARD_URL` even when the
  calling shell did not source `env.sh`. `status.py` reads only that one assignment from the
  served root; an explicit `--base-url` and the live environment still take precedence.
- The documented view command uses the same setting instead of hardcoding loopback. Shared
  source retains `http://127.0.0.1:5599` only as the safe fallback, so this machine can hand
  readers its Tailscale URL without committing its personal IP as every clone's default.
- Reader URL and listener bind remain intentionally separate: `HAIPIPE_BOARD_URL` chooses the
  link, while `serve.py --host` chooses who can reach the unauthenticated write and terminal
  endpoints.

## 0.49.0 - 2026-07-29

- Content-aware addresses replace page-global `Pn.Sn`. Only `## Content` is indexed:
  `###` divisions receive `Cn`, terminal `####` headings receive `Cn.Hn`, and prose receives
  sibling `Cn.Pn.S1` leaves.
- `H` never parents prose. `QAb3.C1.H1` and `QAb3.C1.P1.S1` are valid;
  `QAb3.C1.H1.P1.S1` is invalid. Generated C/H chips make that hierarchy visible.
- Sentence Focus shows the Content and nearest Heading display names while keeping Heading out
  of the sentence address. The focus packet carries that display path with the existing sentence
  and apparatus context.

## 0.48.0 - 2026-07-29

- Pointer devices now expose one quiet sentence action rail: `Pn.Sn ＋ 💬`. Comment opens
  directly beneath the sentence, Chat establishes sentence focus, and double-click remains Edit.
- Sentence Chat now renders a clearable focus card in the existing Q drawer. Opening it spends no
  model turn; the next user message carries the address, sentence, and directly attached apparatus.
- Touch devices collapse the sentence actions into `⋯`, whose menu shows the full address and
  Comment / Chat / Edit. `Esc` closes the active sentence operation without taking over normal
  single-click text selection.

## 0.47.0 - 2026-07-29

- Sentence-specific chat now reuses the existing Q session. Eligible prose receives a
  render-local `Pn.Sn` address; hover/focus exposes the address and a compact chat button.
- Clicking the button opens that Q's drawer and sends an explicit focus packet containing the
  full page-qualified address, sentence text, and directly adjacent apparatus. No sentence
  sessions and no sentence ids are written to Markdown.
- The legacy page-bottom comment queue was removed. Human comments and tracked edits live
  directly beneath their sentence as `> WHO:` and `> ✎` rows.

## 0.46.0 - 2026-07-29

- Why this matters renders inside Opening's drawer for Q pages too, unifying Q with S (JL 260729,
  decided on the design board's QAa1): `src/page_question.py` drops the Q branch that inserted it
  as Content's first subsection; `check.py`'s template coverage asserts the drawer row instead;
  `ref/board-form.md`, `ref/q-template.md` and SKILL.md say the new placement.
- Content is per-page flexible (JL 260729, decided on QAa3): the `§`-numbered manuscript shape is
  the default, not a mandate; the only fixed mechanics remain the one fold level (`###` division,
  `####` paragraph). Rule text only; the renderer already accepted any division set.
- Vocabulary: a Q page settles a "decision", not a "ruling" (JL 260729), across SKILL.md,
  ref/board-form.md, ref/q-template.md and the reviewer agent.
- Pointer maintenance after the design board's 260729 restructure (QA4->QAa0, QA4a->QAa2,
  QA8->QAb1, QA8a->QAb3, QC1 merged into QA1, QA2 merged into the QAa faces): the graduated list
  and the excalidraw section's live ids follow the new names.

## [0.45.0] - 2026-07-28 - a variant tail is part of the unit's identity

- **`S-Display-<n><letter><tail>` now resolves**, e.g. `S-Display-4al2` and `S-Display-4al5`, the same claim under two specifications. Three places stopped at the letter and each failed differently: the chip pattern rendered NO card for either; `_short()` returned `S-Display-4a` for both so `by_short` kept whichever sorted first; and the face-id derivation gave both the anchor `S-Display-4A`, which exists on neither page, so both cards silently lost their owning-page link.
- All three now carry the tail. The legacy `display<NN><a>` form is untouched, and `S-Display-Dash` (a page, not a unit) and `S-Display-4A` (the uppercase page anchor) still do not chip, so the two identities never compete for one string.

## [0.44.0] - 2026-07-28 - a member may have variants, and both the parser and the minter had to learn it

- **`src/parse.py`, the unit pattern.** A page id was `\d+[a-z]?`, a number plus at most one letter, so `S-Display-4al2-main-regression.md` matched NOTHING. The failure mode was the bad one: the file parsed as no page at all, `board.md` reported "listed in Pages but no such file exists", and the page was invisible rather than rejected with a reason. The alternation now leads with `\d+[a-z][a-z0-9]+`, so a VARIANT id parses and `4a` still parses exactly as before.
- **`stage.py`, `resolve_filename`.** It accepted only a number or one uppercase letter, so the minter could not create `4a` either, and every block-plus-member page in the MISQ paper had been made by hand while this function's own docstring called it "the one place an S page's filename is composed". Widened to the same grammar, preserving case for a lowercase member id and still upper-casing a single appendix letter.
- **What a variant MEANS, so the tail does not become a free-for-all:** the same claim and the same job under a different specification of the exposure or method, INHERITING its parent's letter. That inheritance is the point. Letters are reading order, so a unit reading right after `4a` would otherwise have to become `4b` and shift `4b` and `4c` down, and the MISQ board measured that cascade twice on 2026-07-27 at roughly 750 rewritten lines across 105 files.
- **`4a-l2` is not available, on a mechanical ground.** The page-id regex stops at the first hyphen, so a hyphenated tail parses as `S-Display-4A` and collides with its own parent. The tail runs on: `4al2`.
- **Verified on the MISQ board:** 42 pages, the new page ordered between `S-Display-4A` and `S-Display-4B`, 0 stale-contract warnings, every other page id unchanged, and `build-displays.py` shipping 11 units.

## [0.44.0] - 2026-07-28 - measure the master the paper SHIPS

- **A paper may have two tex trees, and 0.43.0 measured the wrong one.** On the MISQ board `3-dist/tex/paper.tex` is the live deliverable, generated one-way from the S-Main pages by `md2tex.py`, while a root master over hand-written `sections/` still builds beside it. `_input_closure()` globbed the ROOT for `\begin{document}`, so it saw only the legacy tree and reported `??` for nine displays that were in the shipped PDF all along. It now prefers `3-dist/tex/paper.tex` when present.
- **An `\input` resolves against the file's own directory OR the paper root.** `md2tex.py` compiles with `TEXINPUTS=".:<paper root>:"`, which is how `\input{S-Main-3-theory}` and `\input{displays/S-Display-1a-hero-concept/float}` both work from inside `3-dist/tex/`. A walker trying only one base silently loses half the tree.
- **Net effect on that board:** one `\ref` chip still reports `??`, `fig:llm-measurement`, whose unit is deliberately folded. Verified by regenerating: `paper.pdf` at 47 pages, nine unit labels in `paper.aux`, zero undefined references.
- **The lesson worth keeping:** "a label exists on disk" (0.42.0), "a label reaches the master" (0.43.0), and "which master" (this one) are three different questions, and only the third makes the second mean anything.

## [0.43.0] - 2026-07-28 - a label on disk is not a label in the document

- **`Registry._input_closure()`.** The label index spans every `.tex` on purpose, so a section-local label still resolves. The cost was that "a `\label` exists somewhere" was reported as "this pointer works", and those are different questions: a float that no reachable section `\input`s declares its label in a file LaTeX never opens, so the `\ref` compiles to `??` while the chip painted green. `ref()` now resolves the master's real `\input`/`\include` closure once and downgrades any label declared outside it.
- **Measured on the MISQ board before the fix:** `tab:descriptives` read `ok` EIGHT times on one page and printed `??`; `tab:main_results` read `ok` while its only declaration sat in a retired `displays/_old/` file reached solely by an orphan section. After: all 22 display chips on that page match ground truth.
- **It downgrades the `\ref` CHIP, never the unit CARD.** A card answers "is this display built and agreed", which stays true of an unwired float; a `\ref` chip IS the claim that the pointer resolves. This is `_gate`'s worst-state-wins applied to a second thing disk cannot see, and it deliberately stops short of the cards for the same reason `[AMBER]` does not downgrade one: ambering the whole set would stop the distinction informing.
- **No master, no judgement.** `_prints()` returns True when no `\begin{document}` file is found, so a board whose paper-root has no master is not painted amber wholesale.

## [0.42.0] - 2026-07-27 - a display unit is named for the page that owns it

- **The unit-to-page join is a LOOKUP, not a guess.** `_sdisplay_read` used to derive an S-Display page name from the unit folder with `display0*(\d+)([a-z]?)` and rglob a stem. When either side was renamed the derivation still produced a face id, found no file, and returned an EMPTY state line, so the AGREED downgrade never fired and a `[RED]` blocked unit painted green on the board. Where a unit folder shares its name with its page, the page is now read directly. The derived branch is kept, and labelled as the fragile one, so a paper that has not migrated still builds.
- **Two layouts, detected not configured.** `Registry` prefers `0-lifecycle/3-display/workspace/S-Display-*/` when it exists and falls back to `displays/display*/`. The board always reads the SOURCE tree, because `candidates/`, `versions/` and `preview.png` exist only there and a card without them cannot be judged.
- **Both trees are excluded from the cite scan.** Under the workspace layout `displays/` holds a GENERATED copy of every float, so indexing it would declare each `\label{}` twice and report a collision against itself. `disp_parts` replaces the single `disp_rel in p.parts` test at both sites.
- **`_short()` replaces `id.split("-", 1)[0]`.** That split was correct only while every id began with `display`; on `S-Display-4a-main-regression` the first hyphen belongs to the prefix, so every unit would have keyed on `S` and the whole set would have collapsed onto whichever sorted first.
- **ALWAYS A CARD (JL 2026-07-27).** A unit name in prose renders as the evidence card, never as a bare page link: the card already carries the owning page's anchor and its state line, so it is a strict superset of the link. MARKER group 6 now accepts `S-Display-<n><letter>[-slug]` alongside the legacy form. The page ANCHOR keeps the uppercase short id (`S-Display-4A`), which the new alternative does not match, so the two identities never compete for one string. `S-Display-Dash`, a page and not a unit, does not match either.

## [0.41.9] — 2026-07-27 — a Display exposes its alternatives without selecting one

- Every allocated paper Display now places `Display Versions` between the live artifact and the real folder tree. It lists the current `float.tex` target, every stored version, unpromoted candidate, and non-current asset as directly openable files.
- The projection does not manufacture version chronology or approval from filenames: only `float.tex` identifies the printed artifact. The explanatory posture states that provenance and supersession require a manifest or stage record.
- Display identities may now use an intentional alphabetic paired suffix such as `display01a` / `display01b`; marker resolution and the S-Display bridge preserve that suffix without changing LaTeX's figure counter.

## [0.41.8] — 2026-07-27 — every Display page reviews the same three concrete things

- A resolved paper Display page now begins its Content with the compiled Current Float, the exact live artifact referenced by `float.tex`, and an ASCII view of the unit directory as it exists on disk.
- The folder view marks a `source/`-only unit as legacy rather than implying that `intake/` and `recipe/` already exist. A new-style unit reports the target layout. This makes staged migration visible without moving assets or inventing provenance.

## [0.41.7] — 2026-07-27 — an authored PDF can be inspected beside the compiled float

- Standard Markdown image syntax now recognizes a local `.pdf` target. `![](path.pdf)` renders a native PDF object with an `open PDF` fallback, rather than an invalid `<img>`.
- A Display page can therefore show the generated `preview.pdf` Current Float first and, when comparison matters, show the underlying live display PDF in the next Content subsection. The two files have different review jobs and no longer have to compete for one preview slot.

## [0.41.6] — 2026-07-27 — a live refresh no longer throws you back to the index

- **The live refresh silently un-routed the page.** `tick()` swaps `div.wrap` wholesale, and the
  page router is pure CSS (`body:has(.q:target) .q:target{display:block}`). `:target` binds to an
  ELEMENT, not to an id: replacing the wrap destroys the section the hash pointed at, the fresh
  one carries the same id, and the browser never re-resolves the fragment. Nothing matches, so
  `body:not(:has(.q:target)) .q{display:none}` hid every page and the index came back — with the
  hash still in the URL, which is why it read as "the refresh threw me out" rather than as a bug.
- Fixed by re-navigating to the hash after the swap. Only a real navigation re-resolves `:target`;
  `history.replaceState` does not.
- Reproduced and the repair verified in headless Chrome, on a minimal page with the same three
  CSS rules: before swap `stage=true index=false`; after swap `stage=false index=true` with the
  hash still present; after repair `stage=true index=false`.
- Found by JL: "after the refresh, I was went to the index page, not the Stage page."

## [0.41.5] — 2026-07-27 — a sentence with evidence answers the same gesture

- **`summary` removed from the dblclick guard, and the form now lands in the drawer body.**
  `QA8@boardform` rules that double-click opens the add-form on a BARE sentence while a drawer
  gets its own `➕ add to this sentence` row, and that row is real — `board.js` appends one to
  every `.sapp` at load. But it is reachable only once the drawer is already OPEN, so on a
  sentence carrying evidence the gesture people actually learned did nothing, silently. 116 of
  the MISQ board's sentences are already drawers, and that number only grows as the evidence
  card becomes the default phase output, so both shapes now answer double-click.
- **The placement is the subtle half.** `mk` does `afterEl.insertAdjacentElement('afterend', …)`,
  so reusing the bare-sentence call on a drawer would insert the form INSIDE `<summary>`, where
  every click toggles the drawer and the inputs cannot be used. A drawer now passes the same two
  arguments the `➕` row path passes — insert at the end of the drawer body, while naming the
  summary's sentence as the target line — and opens the drawer first, since the two clicks
  toggled it net-zero.
- The remaining guard clauses still cover what `summary` stood in for: the sentence text resolves
  to the inner `p`, the `.sbadge` has no `p` ancestor so `!p` catches it, and a marker is a
  `<button>`.
- Found by JL double-clicking a sentence that had just gained a `> Value:` lane.

## [0.41.4] — 2026-07-27 — paper Display pages expose the editable source without replacing the float

- A per-asset `S-Display` page keeps the standard Q-template order and places its compiled
  `preview.pdf` as the first `📚 Content` subsection. It resolves the unit from the page's explicit
  `Registry id:` or `unit:` record, not from a fragile `1a` / `01` title conversion.
- The same subsection now links any PowerPoint source beside `open PDF`. A new source belongs in
  `recipe/`; legacy PPTX files in `source/`, `candidates/`, or `versions/` stay discoverable with
  an honest role label. PPTX is editable work material; `preview.pdf` is still the printable
  float, caption, label, and placement that a reviewer inspects.

## [0.41.3] — 2026-07-27 — the id regex accepts a per-unit stage token

- **A Q-consumer id may carry digits in its stage token.** `Q-[A-Za-z]+-\d+` rejected
  `Q-Sec6Results-3`, so a paper whose per-unit stage names its unit in the id (JL's
  2026-07-27 ruling) had every bracket silently un-chipped: no error, no warning, just
  grey prose where a chip belonged. Widened to `[A-Za-z0-9]+` at all six sites —
  `dialect_paper.py` `QID` and its `\cite{TOADD}`-bracket lookahead, `body.py`'s
  `MARKER` alternation (3) and `QBRACKET`.
- Verified on the MISQ paper: 10 of 10 bracket chips on `S-Main-6` still resolve `qref
  ok` after both sides of every binding were renamed.

## [0.41.2] — 2026-07-27 — folds that stay shut, and two renderer defects

- **An item body may contain no blank line.** `body.py` calls `flush()` on a
  blank line and `flush()` closes the open item, so a converted section ended at
  its first blank line and spilled the rest onto the page as literal `- ` and
  `**bold**` text. 0.41.1 guarded only the line after the item head, which moved
  the symptom instead of fixing it. Blank lines are dropped throughout an item
  body and kept inside fences.
- **`inline()` could not carry a mark across a code span.** Code spans were held
  out of the mark pass so `**` inside them stays literal; the same split cut
  every mark that SPANS one, so `**run \`check.py\` now**` rendered as literal
  asterisks. Broken since that split was written, on every board. Fixed by
  stashing code spans behind a sentinel, running the marks, then restoring.
- Added `join_wrapped`: a bold phrase that the source wraps across two lines is
  rejoined, because one row per line leaves each half with an unclosed marker.
  Editing a shipped skill to satisfy a renderer would be the wrong repair.
- All 9 boards rebuilt on the fix; none regressed. Repointed one cross-board
  link the paper board had renamed again.

## [0.41.1] — 2026-07-27 — agents are shipped units too, and every section folds

- `skillpage.py` accepts a single definition `.md` as well as a skill folder, so
  `agents/haipipe-board-reviewer-agent.md` gets a page. Both carry identical
  frontmatter, so one generator covers both rather than a second that would
  drift. A single-file unit emits the tree span EMPTY rather than omitting it:
  `sync` replaces spans it can find, and a missing one would report as an older
  page every run.
- Every numbered section is now an ITEM, so all of them fold. 0.41.0 made the
  unit's `##` a `####` paragraph heading, which never folds, and items do not
  nest either, so a top-level section had no fold at all. The board has one
  folding level inside Content and QA4 already ruled depth is read off the
  numbering. 19 collapsible sections on the skill, 4 on the agent, 0 non-folding
  headings left.
- Scope: the `Q-Skill` group covers `skills/board/` only. A page generated for
  `haipipe-probe` was a proof and was deleted.

## [0.41.0] — 2026-07-27 — a named Q family for skill pages

- **Named Q pages.** `parse.py` recognizes `Q-<Family>-<rest>.md`, so a skill
  page is `Q-Skill-haipipe-board.md` in a `Q-Skill/` group rather than `QS1-…`.
  Same shape as the named S families, same reason: a skill page is identified by
  WHAT IT IS, never by a position in a queue.
- Split the two concerns onto two pages. `QB6 · Convert a skill folder to a
  skill page` owns the mechanism and lives in QB; everything it generates lives
  in `Q-Skill`. QC5 was renamed into QB6 rather than duplicated.
- The version rides the page TITLE (`haipipe-board · v0.41.0`), so the index row
  prints it. Not the `state:` line, where a derived value competed with a health
  judgment; and never the filename, which would break every link on release.
- A skill's `###` sections became collapsible ITEMS (`- N.M · title` plus an
  indented body). A `#####` heading renders as `.ph` and never folds, so
  eleven sub-sub sections had no way to collapse.
- Fixed a blank line between an item and its body, which ENDS the item: the
  first attempt silently flattened all eleven back to prose while the markdown
  still looked right.
- Fixed `page_id_of` in `serve.py`. `stem.split("-")[0]` collapsed every named
  page into one activity row called `Q`.
- Fixed `group_home` walking past `## Pages`, which listed a new page inside
  `## Links` when its group was the last one.

## [0.40.1] — 2026-07-27 — one division per file, numbered inside

- `SKILL.md` is now ONE `### SKILL.md` division of Content, with the skill's own
  headings two levels down inside it. 0.40.0 promoted them straight to `###`,
  which scattered nine unrelated divisions across Content and lost the fact
  that they are one file.
- Depth comes from NUMBERING, not heading level: `##` becomes `#### N ·` and
  `###` becomes `##### N.M ·`. The board renders exactly two Content levels and
  `#{4,6}` are visually identical, so this is QA4's own `§6` / `§6.1` rule
  applied where a third level does not exist.
- QB6 reads `3 · 🔨 动作` over `3.1 · view` … `3.11 · close`, which is the
  structure the skill actually has.

## [0.40.0] — 2026-07-27 — the skill becomes the page's Content

- `skillpage.py` CONVERTS `SKILL.md` into Content subsections instead of
  embedding it: each `##` becomes a `###` division, each `###` a `####`
  paragraph heading, which is QA4's two-level Content grammar.
- What that buys over an embed: per-section folding, a copy button per section,
  a real anchor, a place to pin a comment, and a Content heading that counts
  them. QB6 reports 11 sections.
- Fenced blocks pass through byte for byte. `SKILL.md` holds a page-anatomy
  figure whose lines start with `## `, and demoting those would have rewritten
  14 lines of a diagram into headings.
- The managed marker now carries the skill folder as well as the hash. `sync`
  recovered the folder from the page's `![[…/SKILL.md]]` line, which vanished
  when the embed did; a machine span must not depend on rendered content to
  know its own source.
- `check.py` exempts managed spans from the hard-wrap rule too. It had flagged
  17 lines of quoted skill prose.

## [0.39.0] — 2026-07-27 — the changelog becomes Log lines

- `skillpage.py` CONVERTS `CHANGELOG.md` into `## Log` entries instead of
  embedding it: `## [0.38.2] — 2026-07-27 — title` plus its bullets becomes one
  dated `260727 · \`0.38.2\` · title` line with the bullets as indented
  continuations, which is the grammar `sort_log` already carries.
- Why it matters beyond format: the ACTIVITY dashboard counts one update per
  dated `## Log` line, so an embedded changelog counts as zero and a converted
  one puts every release onto the strip. QB6 went from 1 update to 59; the
  board total from 507 to 566.
- `check.py` now skips prose-style rules (em-dash, CJK, bold-not-a-group-title)
  inside any `<!-- haipipe:… -->` span, while keeping every structural check.
  The conversion raised 79 warnings in one pass, all of them about quoted text
  the board did not write and cannot fix without falsifying the quote. The
  exemption belongs to the mechanism: a stage's inherited contract is quoted
  material for the same reason.

## [0.38.2] — 2026-07-27 — the skill file stops hiding

- `<!-- haipipe:… -->` machine markers are dropped at RENDER. `strip_notes`
  keeps them in the file on purpose, because that is where stage.py and
  skillpage.py find their spans, but a marker is addressed to a script and six
  of them were printing as literal text on the first generated page.
- Removed the `34em` clamp on `.embed.src .emb`. A `|source` embed IS the
  page's content, not a quotation inside it, and a scrollbox nested in a
  collapsible section is two controls competing for one job.
- Moved the `SKILL.md` embed out of a `### What it is` division. A direct `###`
  in Content renders COLLAPSED, so the one thing a skill page exists to show
  was the one thing behind a click. It now sits directly under `## Content`.
  `### The other files` stays a division: it is supporting material.

## [0.38.1] — 2026-07-26 — a skill page shows the skill, and describes the rest

- Split the generated material into three managed spans, one per section it
  belongs in: the annotated folder tree in `## Diagram`, the whole `SKILL.md`
  plus a description of every other file in `## Content`, and the skill's
  `CHANGELOG.md` in `## Log` under the page's own hand-written lines.
- `## Diagram` also carries an AUTHORED workflow fence. A folder can be read
  off disk; an intent cannot.
- **Described, not reproduced.** Only `SKILL.md` is the skill's content. Every
  other file is named, sized, and given the purpose line it states about
  itself. A first cut embedded `ref/*.md` in full; JL cut it back.
- The file manifest is a fence, not a bullet list: its purpose lines are
  verbatim quotes carrying other files' punctuation, and editing a quote to
  satisfy the prose checker falsifies it.
- Purpose extraction skips YAML front matter, or every `SKILL.md` reported its
  own `name:` line as its purpose.
- QB6 renders 117,500 characters from exactly 2 embeds; 0 errors, 0 warnings on
  that page; sync idempotent and the authored workflow survives a real sync.

## [0.38.0] — 2026-07-26 — a page generated from a skill folder

- Added `skillpage.py` (`new` / `sync` / `check`), a second consumer of
  `stage.py`'s pattern rather than a second mechanism: generate once, then
  refresh only a managed span, never touching what a human typed.
- Derived and owned by the script, inside `<!-- haipipe:skill:start <hash> -->`:
  name, version, last_updated, summary, allowed-tools, folder, and the two
  embed lines. Never touched: Question, Items to Finish, Where we are,
  Comments, Log.
- `state:` is deliberately NOT derived. A version cannot say whether a skill is
  stable or mid-rewrite, so `new` seeds 🔴 OPEN and a person rules on it.
- Zero copy: `SKILL.md` and `CHANGELOG.md` are embedded with `![[...]]` and read
  at build time, so the page cannot go stale between syncs. Only the derived
  header can, which is what `check` reports, with the exact fix command.
- First subject is `haipipe-board` itself, as QB6 on the boardform board. A tool
  that cannot describe its own skill describes nothing.
- Verified: sync idempotent; a version bump caught by `check`; two sentinel
  lines in the authored sections survived a real sync; the page renders 132,256
  characters where the stub rendered 4,132.
- Fixed on the way: the first token was `../../board/...` and the embed refuses
  `..` by design, so it rendered two visible `⚠ embed not found` blocks. `rel()`
  and `resolve_token()` now walk the renderer's own ladder, because a page that
  renders one file while sync reads another is a disagreement no test catches.

## [0.37.1] — 2026-07-26 — the sweep, and the link cost it exposed

- Added `regroup.py`: moves a board's root pages into `Q<key>-<group slug>/`.
  Dry-run by default, `git mv` when tracked, `--all <root>` for a whole repo.
  The ruling had to become a command; a rule enforced by hand drifts.
- Swept all 7 flat boards: **154 pages moved, 0 left at any board root**, every
  page count held, every board rebuilt.
- **Found a real cost QA1 had denied.** `## Pages` lists bare filenames and needs
  no edit; `## Links` declares real relative paths and 17 cross-board links
  broke. `check.py` caught every one. They are repointed, and the correction is
  written into QA1 §1, `SKILL.md`, and `board-form.md` §1.
- Exempted the paper `0-lifecycle/`: `0-seed/ 1-work/ 3-display/` are already one
  folder per group, and their numbers carry lifecycle order that letters cannot.
  `regroup.py` skips any board with no pages at its root.
- Capped the folder slug at 30 characters on a word boundary.

## [0.37.0] — 2026-07-26 — group folders are the default, and named

- **Ruled (JL): one folder per Q group, on every board, from page one.** Not
  size-triggered, so a board never reorganizes itself under its reader the day
  it crosses a threshold.
- The folder is `Q<letter>-<slug of the group title>`
  (`QA-defining-a-board/`), never a bare `QA/`. A bare `QA/` writes the id
  twice and drops the group's subject, which is the half a reader cannot
  recover from the filenames inside it.
- `＋Q` writes into the folder its group already lives in; a group with no
  pages yet gets a named folder created from its `### Q<letter> · <title>`
  heading. Only a group split across two homes falls back to the board root.
- Moved this board onto it: 30 pages into 5 named folders, `board.md`
  untouched, and the rendered HTML identical apart from the 180 write-back
  path attributes that must change.
- Day counts now sit ON each activity bar instead of under it, and always
  render (`·` for a real zero). A bar scaled against a 137-update day is a
  sliver on a 7-update day, and a sliver is not a measurement.
- QA1 closed at 14/14.

## [0.36.0] — 2026-07-26 — the dashboard counts updates, and Diagram becomes writable both ways

**Activity (QD8 merged into QC2 on JL's call).**

- Changed the dashboard's unit from focus seconds to UPDATES: one dated line in
  one page's `## Log`. JL: "I don't care about the time. What I care is about
  the numbers of updates."
- The reason it is a better unit, not merely a preferred one: the timer could
  only see a browser, and most work on these boards arrives through Claude Code
  or an editor, so it was exact about a quantity that was not the work.
- Recovered the history the timer could never have had. It began 2026-07-26
  19:15 and saw one day; counting `## Log` reads 509 updates across 8 boards,
  129 pages, and 5 days, including the 245 lines from 07-22 to 07-25.
- Reads `## Log` only. `## Where we are` also carries dated lines but is status
  prose, and counting both would count one change twice.
- The span recorder still runs and nothing reads it. Its fate is an open item
  on QC2, with a recommendation to delete it.
- Moved ACTIVITY below the page cards: the board's content leads, the
  measurement of that content closes.

**Diagram (QA4 · QA2 · QD7).**

- Split the rendered `🖼 Diagram` into `▧ ASCII` (open) and `✏️ Excalidraw`
  (shut). The source keeps one plain `## Diagram`; `split_diagram()` partitions
  it on the bare-URL rule `body.py` already owned, so no page was migrated. A
  shut `<details>` never displays, so 28 lazy canvas iframes stopped loading on
  open.
- Made attaching reversible: `🗑 Remove` clears the URL line and its blank line
  and touches nothing else. Add, replace, remove returns the file byte-identical.
- Gave every page a way in: `wireXcal` walks pages rather than Diagram
  sections, so a page with no section gets a `🖼 Add a Diagram` control where
  the section would render. The endpoint had always created it; only the entry
  point was missing.
- Ruled that a drawing carries no signature: the md line must stay
  indistinguishable from a hand-edit, and git already answers who added it.
- Fixed `face.dataset.file`, an undefined variable that made
  `✨ Create one for me` report "serve.py is not running" whatever was running.

**Folder structure (QA1).**

- `＋Q` now writes into the folder its group already lives in, falling back to
  the board root when the group's pages disagree or it has none. It recognizes
  no `QA/` naming convention, which is what makes one rule cover both reasons a
  page sits in a folder: the folder is the GROUP, or the folder is the SUBJECT
  (QC3). Flat boards are unchanged by construction.
- Stated those two reasons as one rule in `ref/board-form.md` §1.

## [0.35.0] — 2026-07-26 — shared Board identity mark

- Added `assets/board-mark.svg`, a hand-authored vector of the approved
  four-page mark with a transparent speech-shaped aperture.
- Inlined the mark beside every generated Board title and reused the same
  source as an SVG data favicon, preserving the one-file offline invariant.
- Added `--board-mark-*` palette tokens to `assets/board.css`; geometry stays
  in the SVG while color schemes remain a CSS-only change.
- Added exact-geometry palette studies for Original, Clinical Teal, Warm
  Editorial, and Graphite Aurora to the Board design record.

## [0.34.0] — 2026-07-26 — Diagram's two halves, and where ACTIVITY sits

- Split the rendered `🖼 Diagram` into `▧ ASCII` (open) and `✏️ Excalidraw`
  (shut), ranked rather than paired: the figure is what a reader came for and
  the canvas is where colleagues draw together.
- Kept the SOURCE at one plain `## Diagram`. `split_diagram()` partitions the
  section on the bare-URL rule `body.py` already owned, so no page was migrated
  and a page that later gains a canvas splits itself. A URL inside a fence
  stays in the figure.
- Stopped a board from booting every canvas on open: a shut `<details>` never
  displays, so the lazy iframes wait for a click. This board holds 28.
- Emitted the canvas row even when empty ("No canvas attached yet") and moved
  the 🖌 attach button into it, so the affordance has a home.
- Moved the index `ACTIVITY` section below the page cards. The board's content
  leads and the measurement of that content closes.
- Generalized QD8's opening question away from one named reader; the stored
  span always carried an `actor` column.

## [0.33.0] — 2026-07-26 — three-line closing block

- Replaced the ten-line fenced status strip with three Markdown lines:
  linked `Board · Queue/Focus`, `status · mode`, and the next action.
- Removed repeated field labels, page title, source-file line, separators, and
  the visible raw URL. The Board attachment remains directly clickable.
- Kept the same attachment resolution, sourcing ownership rule, composed-skill
  precedence, and no-shared-status-file invariant.

## [0.32.2] — 2026-07-26 — current Paper paths only

- Removed the Paper dialect's `0-displays/` fallback. Display resolution now
  has one source, the unnumbered deliverable folder `displays/`.
- Updated Board examples and parser comments to the first-class lifecycle
  family paths.

## [0.32.1] — 2026-07-26 — composition precedence and Q/S gate semantics

- Made the reply contract composable: direct Board sessions use the exact
  `status.py` strip, while an explicitly enclosing first-class skill such as
  Paper emits one canonical block containing the deep Board link rather than
  appending two mutually exclusive blocks.
- Limited checkbox/state staleness heuristics to Q pages. S page state is a
  lifecycle gate and is intentionally independent of remaining checklist work.

## [0.32.0] — 2026-07-26 — visible session attachment

- Added a mandatory reply-ending Board status strip, following Paper's Closing
  Block pattern. It shows the Board, page-group queue, board/group/page focus,
  live work mode, next action, deep link, and owning file.
- Added read-only `status.py`, which derives durable labels from `board.md` and
  the page parser instead of maintaining a second status ledger.
- Injected the same closing-block contract into page and whole-Board sessions
  launched by `serve.py`, so attachment is visible even when the user did not
  explicitly name the page again.
- Whole-Board sourcing without an owning page group is blocked. No shared
  `STATUS.md` is created; durable outcomes still use the normal Board sync.
- Forward acceptance passed with a fresh-context agent: it read the revised
  skill, invoked `status.py` rather than hand-writing the strip, derived QD and
  QD9 from the Board files, and placed the complete block last.

## [0.31.0] — 2026-07-26 — one machine state token, optional readable detail

- Formalized the renderer's live contract: the first emoji on `state:` is one of ✅, 🟡, 🔴, or ⏸️ and is the machine status; optional text after it is page-specific human detail.
- Updated `check.py` to validate the normalized emoji rather than an exact full-line label, so real states such as `✅ PINNED · MISQ 2026` remain valid without creating a fifth status.
- Declared `/_board/` and `/_excalidraw` as live server routes so the generated HTML checker does not mistake them for missing disk files; ordinary local links are still checked.
- Made the template fixture source-aware: a construct present in the source but absent from HTML is renderer drift and therefore an ERROR, while a construct absent from the source is an explicit GAP.
- Added separate Q/S placement assertions for rationale, Stage Contract, and Content headings instead of merely counting two rendered page containers.
- Enforced the canonical required structure: Board title/spine/close/Topic/Pipeline/Pages, page title/state/owner/Question/Items/Where, and Stage Contract plus Content on S pages.

## [0.30.0] — 2026-07-26 — Board becomes a first-class family

- Moved the skill package from `skills/0_utils/haipipe-board/` to
  `skills/board/haipipe-board/`, beside the paper, probe, and task families.
- Kept the design Board at `skills/diagrams/BoardSkillBoard-260722/`; a working
  design record still does not ship inside the skill.
- Clarified Board placement: task, project, and paper Boards use the owning
  unit's `diagram/`; plugin skill-design Boards share the plugin's
  `skills/diagrams/`. `NN` sequences one topic series, so unrelated topics may
  each start at `01`.
- Added `../agents/haipipe-board-reviewer-agent.md`, a read-only packaging of
  the existing `check.py` plus zero-background cold-read workflow. The original
  session remains the writer and fixes every finding.

## [0.29.0] — 2026-07-26 — warn when a board writes markers and declares no dialect

The `dialect: paper` seam had exactly one silent failure: a board that writes `\citep{}`, `{VAL:?}` or `[Q-…]` and forgets the two frontmatter lines renders them as plain text, produces an EMPTY marker report, and looks completely fine. Nothing said anything. On a paper board that is the loss of the family's only cross-check of prose against the `.bib` and the display units.

`build.py` now says so, on the `else` branch that previously did nothing.

**The trigger is the board's own CONTENT, never its folder name.** A dialect is deletable (QBc5) and `build.py` must not learn what a paper is, so it does not look for `0-lifecycle/`; it looks for marker syntax.

**Code spans are stripped first, and that is the whole precision of the check.** A board that MEANS a marker writes it in prose; a board that DISCUSSES the syntax quotes it. Measured across the four real boards on 2026-07-26: `BoardSkillBoard-260722` has 13 mentions and `01-probe-qa-260726` has 2, all inside code fences or backticks, none meant. A naive raw match warned on both; stripping code first gives zero false positives on all four, while a real paper board with the two lines removed reports 429.

Verified: `Paper-Personality2Opioid-MISQ2026/0-lifecycle` builds byte-identically (40 pages, 22 markers), and the same folder with `dialect:`/`paper-root:` deleted now warns loudly with the exact two lines to add.


## [0.28.1] — 2026-07-26

**Driven by a real browser at last, which found two things nothing else had.** JL asked "will it work?", and the honest answer was that nobody knew: 0.27 and 0.28 were verified against a server and a stub. Chrome is installed on this machine and Node 22 ships a WebSocket, so the DevTools protocol closed that gap.

- **The app never started.** `proxy_excalidraw()` injected the boot script at `<head>`,
  which put it BEFORE the `window.__haipipeApp` assignment it reads, so `start()`
  returned quietly and no module was ever appended. The page rendered a correct badge
  over a blank screen. The boot tag now goes immediately AFTER the assignment. This had
  been shipped, reviewed and reasoned about twice without being noticed, because every
  test up to that point stubbed the very thing that was broken.
- **Opening a page dirtied the repo.** Excalidraw renormalises everything it loads
  (`version`, `versionNonce`, `updated`, `boundElements` null → []), so the editor saved
  one second after opening with nothing drawn. Two halves to the fix: the tab compares
  element CONTENT rather than raw JSON, and `xcal.py` keeps an element the browser has
  enriched instead of writing its plainer version back. Without the second half the two
  would have dirtied the file in turn forever, each undoing the other.

End to end in headless Chrome: the app mounts, our seed is what it loads, pressing `r`
and dragging produces a rectangle, and that rectangle arrives in `fig/board.excalidraw`
inside `frame-QB3` with the other 88 elements untouched and no page errors. Opening the
editor twice leaves the file byte-identical the second time; two `xcal.py` runs do too.

## [0.28.0] — 2026-07-26

**A pasted image survives, as a real file in `fig/assets/` rather than as base64 inside the scene.**

JL: *"could we make it saved? we can have an assets folder for it."* Right on both counts, and the folder is the part that matters. Excalidraw keeps images as base64 dataURLs INSIDE the document, so one screenshot is megabytes that git then re-diffs every time anyone nudges a box.

- **Bytes out, pointer in.** `stash_files()` decodes each dataURL into
  `fig/assets/<fileId>.<ext>` and leaves `{id, mimeType, path}` in the scene.
  `hydrate_files()` does the reverse on the way out, for the elements being
  returned only. Fetched through `serve.py` the scene is self-contained and the
  editor never knows; the files map is MERGED on save, so an image saved by an
  earlier tick is never lost by a later one.
- **Every `.excalidraw` GET now goes through the scene handler**, not only
  `?frame=` ones, because a whole-scene fetch needs rehydrating too.
- **IndexedDB, not localStorage.** Images live in `files-db`/`files-store`, keyed
  by fileId, which localStorage seeding never touched. The boot script seeds and
  reads that store directly.
- **The app's own module script is now HELD.** `proxy_excalidraw()` turns it into
  `window.__haipipeApp` and the boot script appends it once seeding has actually
  finished. A classic script in `<head>` was enough to beat localStorage, which
  is synchronous; it is NOT enough for IndexedDB, and an app that boots mid-seed
  renders grey placeholders. A URL with no `board=` starts the app immediately,
  so a plain visit to the editor is unaffected.
- **An image is uploaded once.** The tab tracks which fileIds the server already
  has (seeded from the scene it loaded), so a 1.5s save tick does not re-send a
  megabyte screenshot every time a line moves.

Verified over HTTP end to end: a PNG saved, landed byte-identical on disk, left
no base64 in the scene, and came back byte-identical through both the frame URL
and the whole-scene URL; a frame with no images gets an empty files map. Plus 13
new browser-stub assertions (app held until the seed lands, a plain visit still
boots, an image sent once and not again) and the 25 existing ones still passing.

⚠️ The cost of the split, worth naming because "open it in any Excalidraw" was an
argument for owning the file: read straight off disk by the VS Code or Obsidian
plugin, images show as missing, since the bytes are beside the scene rather than
in it. Through the server they are there.

⚠️ Still open on `QA4a`: deleting an image element leaves its file in
`fig/assets/` (removing it automatically would leave undo with nothing to come
back to), and editing the seeded ASCII text is still reverted by the next
`xcal.py` run.

## [0.27.0] — 2026-07-26

**The excalidraw round-trips: what you draw lands in `fig/board.excalidraw`, and opening another page no longer offers to throw it away.**

JL, on the 0.26.0 build: *"When I edit the excalidraw, the changes won't save. And when I open another new Page, it asks me to reopen again and overwrite the current one. What I added will be gone."* Both symptoms had one cause: the open-source app loads from `#url=` and saves to the browser, so the file was in the loop at neither end.

- **`assets/xcal-boot.js`, injected by the proxy.** `proxy_excalidraw()` now rewrites the
  app's HTML to add one classic `<script>` in `<head>`, which is the only window in
  which `localStorage` can be replaced (a module script is deferred; a classic one in
  head is not). The script seeds the editor from the scene file and, in the editing
  tab, pushes changes back. `#url=` is gone, so the "Replace my content" dialog has
  nothing to confirm and never appears.
- **The URL changed**: `?board=<scene>&frame=<page>` replaces `#url=…`. `xcal.py --wire`
  writes the new form; `board.md`'s `excalidraw:` line is unchanged.
- **`POST /_board/excalidraw-save` MERGES.** With `frame=`, only that frame's slice is
  replaced and the other 27 are left byte-identical, which is what lets one file be
  edited from any page. The frame's id and name are forced back on save because the
  name IS the page's link; a deleted frame is restored; deleted elements are dropped;
  the write is atomic. Without `frame=`, the whole scene is replaced.
- **An embed reads, a tab writes.** A board page carries one iframe per page, all on one
  origin sharing one storage key, so an editable embed would be 28 editors overwriting
  each other and then reading the result back as their own. An embed gets an in-memory
  storage and persists nothing; "✏️ Edit this frame" opens the one tab that writes, and
  a lock in real storage keeps it to one tab (a second drops to read-only and says so).
  The app REFUSES to restore `viewModeEnabled` from storage, found by reading its own
  per-key policy table; `activeTool` and `zenModeEnabled` do restore, and a locked hand
  tool is better anyway because panning and zooming still work.

Verified server-side over HTTP (a rectangle drawn into QB3 lands in that frame, the
other 27 slices compare identical, an unknown frame name and a path outside `--root`
are both refused) and client-side against a stubbed browser, 22 assertions covering
both modes, the save payload, the idle tick, and lock contention. **Not yet exercised
in a real browser**: no browser was reachable from the session that wrote it.

⚠️ Two edges left, both on `QA4a`: a pasted IMAGE does not survive, because Excalidraw
keeps images in a `files` map and the endpoint writes `elements` only; and editing the
seeded ASCII text in Excalidraw is reverted by the next `xcal.py` run, since that text
is a generated element (drawings around it are kept).

## [0.26.0] — 2026-07-26

**A board owns one excalidraw, a page owns one frame in it, and the frame opens onto the figure that page already had.**

- `xcal.py <board-dir>`: builds `fig/board.excalidraw` from `board.md` and the pages.
  One scene, one frame per page, one row per `## Pages` group with the group's name
  above it, each frame sized to what it holds. `--wire` also puts every frame's URL
  into its page's `## Diagram`, replacing whatever was there. It is a separate script
  from `build.py` on purpose: `build.py` runs on every file save and a scene regen
  must not.
- **Frames are seeded** with each page's first `## Diagram` fenced block, as one
  monospace text element. JL opened `?frame=QB3` on 260726 and found a blank
  rectangle, which is exactly what had been built: 28 named frames with nothing in
  them. A scaffold and its content are two deliverables and only the second one is
  visible, so shipping the first reads as a broken feature. The seed is ONE-WAY;
  the markdown stays the source, and 25 of 28 pages had a figure to give.
- **Re-running is safe**, which is the only reason it is a script. Every minted id is
  prefixed (`frame-QA4a`, `t-QA4a-fig`) so a regen renames nothing and no page's link
  dies; an unprefixed id is a human's drawing and is carried through; a frame a human
  moved keeps its position; a prefixed frame whose page has been retired is DROPPED,
  which is `QA4a`'s dead-frame rule. Verified by injecting both cases. `--fresh` is the
  one destructive mode and is never the default. Overlapping frames are reported,
  since a kept position plus a recomputed width can collide.
- `check.py` gained `open-with-done-items` and `partial-with-nothing-open`. SKILL.md's
  `sync` action has always required writing a page back in the same round; nothing
  ever noticed when a session skipped it. `QA4a` said "nothing is built and nothing is
  decided" on the day its whole route was built and running (JL 260726: think about
  how to update the related Q along the session). The check only sees `state:` and the
  boxes, so it is a backstop under the rule, not a replacement for it.
- SKILL.md: an `excalidraw` action, and `sync` now says the trigger is **substantive
  work in the session**, not opening a page. Every piece of real work belongs to some
  page even when it started as a line of chat, and work that belongs to no page is a
  new page. "Done" means written back.

⚠️ **Not closed: the write-back.** `#url=` loads, the editor saves to the browser, so
nothing drawn returns to `fig/board.excalidraw`. The scene is a view of the markdown
and not yet a place to work.

🩹 One regex cost four pages. `^\s*<url>\s*$` looks line-anchored and is not, because
`\s` spans newlines: it ate the blank lines around the URL, and an off-by-one on
`hit.end()` took the `#` of the next heading with it, welding `## Diagram` to the URL
on three pages and giving a fourth two `## Diagram` sections. All four were repaired
and `--wire` now rebuilds the section instead of splicing into it.

## [0.25.0] — 2026-07-26

**A board can now be checked, and an author note finally behaves the way the template said it did.**

- `check.py <board-dir>`: the structural half of `QA9`, read-only, four families.
  BOARD (`board.md` against disk, declared Links resolve, ids unique), FACE (required
  sections, the four state values, references resolve, one sentence per line, no
  em-dash, English-only), PAGE (the built html: local hrefs resolve, tags balance,
  ids unique, the zero-script invariant), and TEMPLATE (render `ref/q-template.md`
  as a Q AND an S, then assert each of QA9's 15 constructs). It reuses `src/parse.py`
  rather than carrying its own grammar. Report-only, exit 0; `--strict` exits 1 on
  ERROR and waits on JL's ruling about whether a red result blocks a change.
- A construct the template never demonstrates is reported as a GAP rather than
  skipped, which found three on the first run: code block, group title, excalidraw
  canvas are documented and untested.
- `parse.strip_notes`: `<!-- ... -->` author notes are dropped BEFORE the text is cut
  into sections. `ref/q-template.md` has always told authors a note "is dropped at
  generation either way" and it was not: the only strip lived in the Stage Contract
  path, so a note written anywhere else came out as escaped `&lt;!--` prose. Order
  matters and cost two attempts to learn, because `split_sections` reads a `## ` line
  INSIDE a comment as a heading, so a note listing sections was torn in half and left
  a phantom section behind. Fenced blocks are protected and `<!-- haipipe:… -->` is kept.
- The index page's ＋ button writes Boundary and Files, which `QA2` rules "strongly
  advised", and offers the optional sections as an author note. Its stub was a second
  definition of a new face carrying 4 of the template's 14 sections; a face generated
  from it arrived with no Diagram and nothing said one was available.
- `prime_context` counts unresolved comments and unticked items separately and names
  each. One number announced as "unresolved comments" made a cold agent notice the
  mismatch, fail to resolve it, and invent an explanation for it.
- `CHAT_RULES` lists the current section names, with the retired ones named as
  accepted aliases, and explains what a `>` lane is and that it is addressed to the
  turn reading it. It had described a face layout retired days earlier.
- Index rows lost their coloured left stripe (`QA10`). Every row already opens with
  the state emoji, so the bar restated it in a second language.

## [0.24.0] — 2026-07-26

**Diagram was the last body section you could only read. Now you can draw into it.**

- `🖼 Diagram` gets a `🖌 Add an Excalidraw canvas` control (`QD7`). Paste a share URL, hit
  Save, and `serve.py` writes it on a line of its own inside `## Diagram`: the same line an
  author types by hand, so the md stays the single source and an older copy of the skill
  still renders the result. Endpoint `/_board/diagram`, control `wireXcal` in `board.js`,
  styles `.xadd`. The generator was not touched.
- One canvas per face: a second paste replaces the first instead of stacking iframes. The
  response says `replaced: true` when it did.
- A face with no `## Diagram` gets one created immediately before `## Content`, which is where
  the fixed on-stage order puts it, and the response warns that a canvas without an ASCII
  figure is the half that disappears when it cannot load (`QA4 §2`).
- A URL that is not `excalidraw.com` is refused with nothing written, and the section scan
  skips fenced code blocks so example markdown inside `QA4` is never written into.
- `serve.py` takes `--host`, still defaulting to `127.0.0.1` (`QE6`). The bind address is this
  server's only access control, since there is no auth and `/_term/` is a real shell, so any
  non-loopback bind now prints a warning line at startup. Nothing changes for anyone who does
  not pass the flag.
- `QA4 §2` documents the Excalidraw half as a mechanism rather than a mention: one URL alone
  on its line, what it renders, and why the fallback link and the ASCII figure both stay.

## [0.23.0] — 2026-07-26

**The first Board UI taste pilot is live, bounded by QA10.**

- All native links, buttons, disclosures, fields, and explicit tab stops now share one
  high-contrast `:focus-visible` ring; pointer interaction keeps its existing appearance.
- Four semantic radius tokens replace unrelated one-off values: inline highlight, control,
  surface, and pill. Focused faces keep their existing zero-radius, unframed reading mode.
- `prefers-reduced-motion: reduce` now suppresses current and future transitions and animations.
- The pilot is CSS-only and reversible: it changes no Markdown grammar, generated structure,
  interaction contract, or dependency.

## [0.22.0] — 2026-07-25

**The page directory is now called Pages.**

- New and migrated boards use `## Pages` for the filenames, groups, group introductions, and display order.
- Parser and structure writers treat `Pages` as the canonical section while continuing to read old `Roster` headings.
- Board prompts, warnings, examples, Paper page creation, and the seven active boards now use the same plain term.

## [0.21.0] — 2026-07-25

**Content gets a second heading level, and 🔹 gets its meaning back.**

- `####` is now a first-class paragraph heading (`.ph`): no icon, one size below a group
  title, its own spacing. It used to be flattened to `**bold**` before rendering, and a
  full-line bold IS the group-title construct, so every paragraph arrived wearing 🔹 and
  claiming to lead a run of items. Deleting the icon would have hidden the mistake; the
  page was not over-decorating a paragraph, it was calling it something it is not.
  On the MISQ board the split came out 113 paragraph headings · 82 job lines · 31 group
  titles, with 🔹 left only on the 31 that really lead items.
- A full-line `(…)` directly under a `####` heading is that paragraph's **job line**
  (`.pj`): grey italic, on stage, one line only. It is the scan hook that lets a reader
  see what each paragraph does without reading the prose, so it is not hidden behind a
  click. Only the line immediately after the heading is read this way.
- Focus-mode spacing fix: `.q:target .ph` (0,3,0) outranked `.ph:first-child` (0,2,0), so
  the first paragraph after a section heading opened 22px low instead of 2px, and only in
  sections that begin with a heading, which is why it read as inconsistency rather than as
  a gap. `.gt` had already been patched for this once; both now share one selector.
- **The rule these render:** Content carries exactly two levels and the depth lives in the
  numbering, not the heading level. `###` is a division that folds on its own, `####` is one
  paragraph inside it, and there is no third level because the page folds exactly one. A
  division is written only when it holds something, so a flat section carries one
  `### §1 Introduction` over its paragraphs while a subsectioned one starts at `### §6.1`.
  The shape is then checkable without reading: the subsection count is the number of `###`
  headings whose number contains a dot.
- An S page title may carry the artifact's own number when it is offset from the board
  index (`S Main 7 · §6 Results`), so the derived Content heading reads
  `📚 Content · Main 7 §6 Results` and the two numbers stop competing on one screen.
- New writing rule: **an ASCII figure must survive being copied.** Never draw two trees side
  by side; the column boundary is whitespace, it disappears on paste, and the right column's
  rows read as branches of the left one. Real case: a two-column comparison of two heading
  trees came back pasted as one tree with the wrong nesting.
- Docs caught up with code that had already shipped: the levels and the job line existed only
  in `src/body.py` and `assets/board.css` and were documented in none of SKILL.md,
  `ref/board-form.md` §4/§5, `ref/writing-rules.md`, or `ref/q-template.md`. All four now
  carry them, and QA4 records the ruling, the Law, the Glossary terms, and the Lesson.

## [0.20.0] — 2026-07-25

**Sentence apparatus v1 (QA8): click a sentence, see its evidence.**

- A plain sentence followed by `>` lines now renders as a native `<details>`: the sentence
  stays on stage with a ⚑N badge; the `>` lines fold into a drawer beneath it. Typed lanes
  name the attachments (`> Citation:` 📚 · `> Value:` 🔢 · `> Display:` 🖼 · `> Check:` ⚠️ ·
  `> Q-consumer:` 🔎 · `> Link:` 🔗 · `> Source:` 📄 · `> Note:` 📝); `> WHO:` review threads
  join the same drawer with their comment styling. Implemented in `src/body.py`
  (`render_apparatus` + the `last_p` attachment walk) and `assets/board.css`.
- Attachment is by adjacency: a `>` run under a sentence (blank lines tolerated) belongs to
  that sentence; a run with no sentence above it renders as before, and the supporting folds
  (Discussion, Why here, Law, Lesson, Glossary, Log) never fold apparatus.
- Zero-script invariant holds (native details). Pages change only where `>` lines already
  follow a sentence. Piloted on the boardform lab board (QA8 ruling + QA4 self-demonstrating
  subsection); the MISQ paper board is untouched pending JL's acceptance.
- Click-to-add: `POST /_board/sentence` inserts `> Lane: text` directly under the exact
  sentence in the md (markdown-stripped anchor match, visible failure on a miss) and rebuilds.
  On the page: click a bare sentence for the lane + text form, or the "➕ add to this
  sentence" row inside any open drawer. Script-only enhancement over the no-JS reading path.
- Sentence hover tint (accent at 8%) shows which sentence a click or selection will target.
  The form opens on DOUBLE-click, leaving single click free for reading and selection.
- Copy is section-level: every section heading carries a ⧉ button that copies that whole
  section as clean plain text, folded drawers and item explanations included, with no badges,
  buttons, or highlight formatting. A per-sentence copy button was tried and removed.
- Every section folds from its own heading (Content, Items to Finish, Where we are, Files), the
  native-details mechanism Diagram already used. All open by default except Diagram, since the
  reading path must survive a reader who never clicks; folding is display-only, so Ctrl-F, the
  section ⧉ copy, and the no-JS fallback are unaffected. Expand-all and ⧉ no longer toggle the
  section they sit in, and ⧉ force-opens a folded section in its clone before copying.
- `ref/q-template.md` brought up to these rulings, then hardened by a fresh-context cold read:
  the apparatus example was itself hard-wrapped and taught the failure it warns about (a wrapped
  lane becomes its own sentence row and steals the lanes below it); the S title convention that
  feeds the Content heading was undocumented; the contract markers must not be hand-copied
  (a hand-written sha reports the page unsynchronized, and sync replaces anything between them);
  `requires:` resolves S ids bare but needs a real filename with extension for anything else.
- Opening starts fully collapsed on S pages (JL 260725: "all the things here should be hidden").
  Why this matters, the optional Stage Record, the Stage Contract, and the contract's own parts
  all begin shut, so the lead question is the only thing on stage. Q pages are unchanged.
- S Content holds the stage's real product only (QA4 Law, JL 260725). Inherited contract
  material belongs to `## Stage Contract`, settled flags and corrections to `## Where we are`,
  open work to `## Items to Finish`. The Content heading now NAMES the stage on S pages
  (`📚 Content · Main 7 Results`) instead of counting subsections; Q pages keep the count.
  Authored subsections under `## Stage Contract` are sync-safe: `replace_managed` rewrites
  only the span between the `haipipe:contract` markers (verified on the MISQ Results page).
- Comment highlights are painted with inset box-shadow instead of background-color, so text
  copied into Word no longer carries the pale yellow fill; `code_or_link` stopped
  double-escaping code spans (backticked `>` rendered as `&gt;`).

## [0.19.0] — 2026-07-25

**The reading pass: sentence lines, serif prose, Stage Contract inside Opening (JL 260725).**

- Stage Contract now renders INSIDE Opening as one collapsed disclosure after Why this matters
  and Stage Record (JL: "within the Opening. Not a separate section."). The standalone section
  between Opening and Diagram is gone; comment anchors scan it as part of Opening. Source
  anatomy is unchanged: S files keep their `## Stage Contract` section and managed markers.
- One sentence per source line is a writing hard rule (ref/writing-rules.md). The renderer has
  always given each plain prose line its own row, so a mid-sentence hard wrap became a broken
  line on the page. Both live boards were re-flowed to sentence lines (boardform 25 faces,
  MISQ lifecycle 42 faces); prose content untouched, only line boundaries.
- Face prose (Opening lead, paragraphs, item titles, group titles) switched to a serif reading
  stack: Charter / Georgia / Cambria with Times New Roman as the print-classic fallback. UI
  chrome (ids, pills, bars, code) keeps its sans/mono faces.

## [0.18.0] — 2026-07-25

**Display is independent, and S pages inherit explicit requirements and writing style.**

- Canonical paper families are now Seed, Work, Venue, Display, Main, Appendix, Submission.
  Display owns the claim-to-display map, approved assets, captions, statistical labels, and
  placement consumed by Main and Appendix.
- S metadata accepts `requires`, `style-from`, `provides`, and `contract-source-hash`. Pages
  adjacency never implies a dependency.
- `stage.py new|sync|check` creates S pages, refreshes only the managed Stage Contract block,
  and detects upstream source changes. `build.py` remains render-only and reports stale contracts.
- `stage.py sync --all` follows the explicit dependency graph in topological order; Pages order
  remains a navigation concern and never controls inheritance.
- S pages render `Stage Contract` between Opening and Diagram. Required Inputs and Writing Style
  stay separate from authored Content; upstream prose is linked and summarized, never copied whole.

## [0.17.1] — 2026-07-25

**S families are stable homes, while Pipeline owns execution and revision loops.**

- The six-family index order no longer claims every paper runs as a simple family-by-family line.
  A Pipeline may revisit Work/Displays after Narrative while keeping one stable Work group.
- Submission pages are reused per initial submission and revision round. An external decision
  reopens affected Work, Main, or Appendix pages, then returns through reconcile, compile, review,
  and submit; it does not duplicate a new S page set for every round.

## [0.17.0] — 2026-07-25

**Paper lifecycle S pages now use readable, full-name families.**

- Canonical filenames use `S-<Family>-<unit>-<slug>.md`, with six families in lifecycle order:
  Seed, Work, Venue, Main, Appendix, Submission.
- Seed can carry both `S Seed` and `S Literature`; Main exposes one page per manuscript section;
  Appendix uses `0` for control and `A-F` for units; Submission makes reconcile, compile, review,
  and submit explicit gates.
- HTML ids are readable (`#S-Main-3`, `#S-Appendix-D`), badges name the family, JSON emits
  `family`, and the index reports a separate progress fraction for each family.
- Legacy `S0`, `SM0`, and `SA0` filenames remain parse-compatible for existing boards, but the
  authoring docs and template no longer recommend those abbreviations.
- The MISQ paper board was migrated end to end, including a new literature-seed page and three
  terminal submission pages.

## [0.16.1] — 2026-07-25

**Paper lifecycle boards now expose the lifecycle as their primary index structure.**

- One Pages group represents one paper stage, ordered S0 through S5.
- The canonical S face is the first row; every Q row after it is a ruling owned by that stage.
- Stage-only groups remain visible instead of being merged into broad QA/QB/QC buckets.
- Group headings retain a unique Q family writer key, such as `QD · S4 · Display`, so index-side
  add/archive controls keep working.
- The MISQ paper lifecycle board was reorganized into one paper-level frontier group plus eight
  stage groups, with S4→QD2-QD8 and S5→QE2-QE7 ownership explicit.

## [0.16.0] — 2026-07-25

**Creating an S lifecycle stage is documented, not only rendering one (QB pass).**

The QB2 fresh-agent acceptance was re-run against the shared Q/S skill (4 Q faces + 1 S stage
on a lab data-retention topic; SKILL.md + `ref/` only, existing boards out of bounds). Verdict
YES, first-try build, gate respected, Stage Record lifted. Everything it had to invent was on
the S **authoring** side, and all of it is now written down:

- `SKILL.md` `open` steps 1 and 4 ask for Q **and** S faces, give both filename shapes
  (`Q<letter><n>-<slug>.md` / `S<order>-<slug>.md`), state S's required `## Content`, and say how
  an S is listed in `## Pages`.
- `close` and the Face section: both kinds share the same four `state:` values, and a new face of
  either kind starts 🔴 OPEN. ✅ means "every checkbox closed" on Q and "this stage's human gate
  passed" on S (what the index counts as `stages gated`). `human-gated` is not a state value.
- `ref/board-form.md` §2 gained the S state mapping plus the Pages rule (bare filename, free-text
  group heading, own group or mixed in); §3's example gained an S line.
- `ref/q-template.md`: the Q-consumer `**Probe:**` line no longer assumes a paper's `1-probes/`
  tree; on a standalone board name the real route or write `not opened yet`. Its state legend now
  carries the Q-versus-S ✅ distinction.
- The build section names the interpreter split: `build.py` / `watch.py` run on any system
  `python3`; only `serve.py` needs the repo `.venv` (the SDK requires 3.10+).

Board-side records refreshed in the same pass: QB1's stale figures (128 lines / five actions /
CHANGELOG 0.2.0) replaced with the 0.15.x reality, QB2's second run and a new `## Law`, QB4 noting
that QB5's `src/` split superseded its 850-line build.py, and the `ALIAS` / `sec()` pointers in
QB3 and QA2 repointed from `build.py` to `src/common.py`.

## [0.15.2] — 2026-07-25

**The QD2 chat drawer header is quieter, clearer, and consistent.**

- The saturated accent banner became a neutral 56px utility bar separated by one hairline.
- Face id is compact mono metadata; the full title uses the remaining width and ellipsizes in CSS,
  preserving the complete title in a tooltip.
- Terminal and close are matching 32px square controls with hover and keyboard-focus states,
  accessible labels, and a stable `>_` terminal mark instead of a platform-dependent keyboard emoji.

## [0.15.1] — 2026-07-25

**QA2's source-template contract now explicitly mirrors QA4's rendered Q/S face contract.**

- `ref/q-template.md` states the fixed visible sequence, Q-versus-S Content requiredness,
  rationale placement, Q-consumer closure rule, and optional S-only `### Stage Record` behavior.
- The board's QA2 face now specifies the source-to-render mapping for Opening, Diagram, Content,
  Items to Finish, Where we are, Files, and supporting folds; stale Q-only wording was retired.
- Two fresh-context acceptance rounds rendered realistic temporary boards. The first exposed that
  Stage Record optionality was only implied; after revision, the second rendered one Q and two S
  variants and passed with Stage Record both present and absent.

## [0.15.0] — 2026-07-25

**A chatbot on the index page (JL 260725 on QC2: "just add a chatbot in the index page").**

- It is the existing QD2 drawer and QD3 terminal, opened on `board.md` instead of one question.
  No new agent, no second engine; details recorded on QD2, entry point on QC2.
- `serve.py` accepts `file: "board.md"` as one more face: the orientation block carries the
  index's own view (spine, close, every face's state + open-comment count); board-flavored
  rules; the restricted tier's "own files" widens to any `.md` inside the board folder
  (verified: in-board Write auto-allowed, /tmp Write denied).
- The session id lands in `board.md`'s header (`session:` under `close:`), is parsed into meta
  (`src/parse.py`) and rendered as `data-bsession` on `div.wrap` (`src/page_board.py`), inside
  the live-swap region so it stays fresh without a reload. The drawer's ⌨ opens the same
  session in a real terminal (verified: same session id, proxy 200, clean release).
- `assets/board.js`: `chatOpen('board')`; the bottom-right fab now also shows on the index,
  labeled "🤖 Board chat"; index flavor of the action buttons (🧭 which question should I act
  on · 🔧 handle open comments board-wide); `follow()` returns to the board session when you
  navigate back to the index. `assets/board.css`: the fab shows whenever the drawer is closed.

## [0.14.0] — 2026-07-25

**Stage orientation moved into Opening, and Opening now uses a compass.**

- The visible heading is `🧭 Opening`, replacing the question mark with an orientation icon that
  works for both Q rulings and S lifecycle stages.
- On S faces, the automatic "Why this matters" disclosure now lives in Opening and starts open.
- An exact direct `### Stage Record` inside S Content is lifted into Opening and starts collapsed;
  the remaining stage subsections stay under Content.
- Q faces retain "Why this matters" as Content's first open subsection.

## [0.13.3] — 2026-07-25

**Colleagues replaces the generic assistant role.**

- User-facing prose now says colleague or colleagues instead of assigning everyone one generic role.
- Each colleague signs and owns work with their own initials; examples use `ZW` rather than a
  shared role identity.
- The comment picker defaults to `JL` and `CC`, while any colleague can add their own initials.

## [0.13.2] — 2026-07-25

**Diagram is now a real section and starts closed.**

- The fixed visible order is `Opening → Diagram → Content → Items to Finish → Where we are`;
  Files follows.
- Opening now contains the question lead and optional Boundary. Optional Diagram renders as a
  peer-level native `<details>` section whose heading stays visible while its figure is hidden
  until clicked.
- The figure remains in the HTML and works without JavaScript; ASCII and embedded Excalidraw
  content retain their existing rendering once opened.

## [0.13.1] — 2026-07-25

**The visible first layer is Opening, not a peer list of Question, Boundary, and Diagram.**

- The rendered hierarchy is `Opening → Content → Items to Finish → Where we are`; Files follows.
- Opening contains the actual question lead plus optional Boundary and Diagram. The rest of the
  Question becomes Content's first "Why this matters" subsection, so Q faces follow the same
  visible rhythm even without an explicit `## Content`.
- The source keeps `## Question` for precision, while `## Opening` is accepted as an alias.
- Opening uses the same section-heading hierarchy as Content, Items, and Where.

## [0.13.0] — 2026-07-25

**One face grammar now serves rulings and lifecycle stages.**

- `Q*.md` remains a board ruling; `S*.md` is a lifecycle stage. Both are recursively discovered,
  rostered, commentable, and rendered by the same face renderer.
- `## Content` lands between Diagram and Items. It is optional for Q and required for S; each
  direct `###` heading renders as a native collapsible subsection.
- Former stage `Q-consumer` blocks become recognizable checklist records under
  `## Items to Finish`. The answer must land, be interpreted, and be woven into Content before
  its box closes.
- Question settlement and stage gates have separate index summaries. A stage carries a STAGE
  badge and never inflates the question settled count.
- Focus mode now has a real narrow-viewport layout: smaller wrapping titles, zero-width-safe
  flex/detail children, and measured `clientWidth == scrollWidth` at a 390px device viewport.
- The first complete consumer is the MISQ paper lifecycle board: 14 Q rulings + 8 S stages, with
  the previous stage files archived and all lifecycle `_LOG_*.md` sidecars removed at the user's
  request.


## [0.12.1] — 2026-07-24

**The drawer terminal stops smearing on emoji + CJK (QD3, JL's fig/image.png).** The cause left standing after 0.9.2's cell-metrics fix: claude's TUI counts 🟡✅💬 as 2 cells (modern wcwidth) while the vendored xterm.min.js only ships Unicode 6 width tables that say 1 — every emoji shifts the row, full-screen repaints land off-cell, and the frames interleave into the smear. Vendored `@xterm/addon-unicode11@0.8.0` (new `vendor/xterm/addon-unicode11.js`, whitelisted in serve.py's `serve_asset`, loaded right after xterm.min.js, `unicode.activeVersion = '11'`); verified offline that the v11 provider returns width 2 for 🟡✅💬汉 where V6 said 1. The stacked second cause fixed with it: Menlo has no CJK, fallback glyphs overflow the measured row — the drawer terminal's fontFamily now carries PingFang SC / Hiragino Sans GB / Microsoft YaHei and `lineHeight: 1.2` adds the headroom. Addon load is soft-fail (console warning, terminal still opens), so an older running serve.py cannot brick the drawer.

Also in 0.12.1: **`scrub_cjk_comments` scoped to `<style>`/`<script>` blocks.** Run page-wide it treated body prose as code: QD3's `GET /_board/asset/*` glob read as a `/*` comment-opener, and the span to the next `*/` (inside QE3) was silently dropped the moment CJK landed in between — five slides (QD4–QE2) gone. build.py's no-JS invariant caught it; body prose is now never scrubbed.

## [0.12.0] — 2026-07-24

**ascii inside an item's fold (JL: "for each item's hidden text, add the ascii").** An INDENTED ` ``` ` fence in an item's explanation lines is collected into that item's hidden text (dedented, rendered as `<pre class="ip">`), instead of flushing the item and landing as a sibling block. Column-0 fences keep the old sibling behaviour, so the face stays title-only and the diagram lives behind the click — the QA4 item shape (heading + summary + prose) is unchanged, the ascii just joins it. This deliberately revisits the 1705 ascii-in-item experiment that 0.11-era reverted: that revert traded ascii away to get the QA4 shape; now both hold at once. First user: the CMS board's QC10 (AMI → CABG), all 6 items. CSS: `.bd pre.ip` one size down, horizontal scroll of its own. Regression: boardform board (28 questions) rebuilds unchanged.

## [0.11.0] — 2026-07-24

**A board can sit on an existing tree (QC3), show other files' content live (QF1), and the Python got its src/ split (QB5).** All three driven by the first board laid directly over a paper's `0-lifecycle/`.

- **folder questions (QC3, JL ruling).** A question is a `Q*.md` at ANY depth under the board folder: `q_files()` discovery (rglob, skipping path segments starting `_`/`.` and `fig/`), Pages keeps bare filenames, duplicate basenames warn and keep the first, the page's data-file carries the board-relative posix path, serve.py vets it (`vet_qpath`: no absolute, no `..`, basename must look like a Q file), archiving flattens into the board's `_archive/`, watch.py watches the whole tree. Flat boards untouched (regression: unchanged question set).
- **embeds (QF1, JL: "can a markdown file incorporate another file?").** `![[path]]` / `![[path#Section]]` on its own line pulls another file's content into the slide at build time, by reference — zero copy, zero drift, zero dialect knowledge. `src/page_stage.py` renders generically (atx AND setext headings, fences, lists, quotes, `|` record lines) under a "live from source" header; every failure mode (missing file, non-md/txt, heading not found) is a visible warning box, never a silent gap; no recursive expansion. Comments on embedded text keep living in the FACE's `## Comments` and re-anchor against the re-rendered embed at rebuild. Still open on the board: the paper-side anchors handshake (haipipe-paper-stage contracts).
- **src/ split (QB5, JL named the page modules).** build.py 995 → 70 lines, code moved VERBATIM to `src/{common,parse,body,page_board,page_question,page_stage}.py`; serve.py imports `QNAME`/`vet_qpath`/`q_files` from `src/common.py` instead of duplicating. Byte-identical proven on board.html AND `--json` BEFORE any feature landed.
- **bugfix, found by the byte-identical gate:** the old single-function `render()` reused `lab`, so any question WITH comments wore the comments count in its state pill (`✅ 💬 Comments (0 open / 7) …`) instead of its state label. Reproduced first to prove the move pure, then fixed (`cm_lab` in `src/page_question.py`).
- **doc slides (QF2, JL: "no need to generate QB3-claims.md").** A Pages line `doc: <path> <path>…` renders the listed source files DIRECTLY as one slide (id = first file's stem, title = its own `#`/setext title) — no Q wrapper at all. Doc slides are views, not questions: no state pill, no Items counting, no comment target, excluded from the settled count and the bar. Files are explicit, so `_LOG_*.md` can be shown even though `_` paths are excluded from Q discovery.
- First consumer: `examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle/` — 14 ruling Q slides + 8 doc slides after JL's scope ruling ("I think 14 ruling faces"): every stage renders straight from its own docs (0-seed, 1a-resource, 1b-claims, 2a-venue, 2b-pitch, 3-narrative, 4-display + _DISPLAY_REQUEST, z-structure), while QA1 + QD2..QD8 + QE2..QE7 keep Q files, live embeds, and comment write-back (verified over HTTP on 5599). The settled bar counts the 14 rulings only.

## [0.10.0] — 2026-07-24

**The index becomes editable (QC2, JL): groups introduce themselves, and the board's structure is writable from the page.**

- New Pages grammar: plain lines between a `### ` group heading and its first `.md` entry are the GROUP INTRO. Line 1 renders as an always-visible sentence under the group header; further lines become the click-to-expand "what this group is for, why it is here" body. Rendered as a native `<details>`, so strip-scripts still leaves the whole board readable; `parse_dir` collects intros into `meta["groups"]` and the `--json` path carries them for free.
- One structure writer: `structure_op()` in serve.py behind `POST /_board/structure`, imported by the console's boards_api (QE3: one writer set, never reimplemented). Ops: `add_group` (letter auto-picked, optional hook/body intro), `add_question` (seeds a stub Q file in the house shape, numbers past the group's max, lists it at the group's tail), `archive_question` (logs the move in the Q's `## Log`, moves the file to `_archive/` inside the board, drops the pages line; NEVER deletes), `archive_group` (refuses while the group lists any question).
- Page controls (board.js/css): ＋Q on each group header, ＋Group at the index tail, hover 🗄 on rows and headers with a two-click "sure?" confirm and an inline mini form (no native dialogs). Wired into `__boardRewire`, so they survive QD6's in-place swaps; after each op the server rebuilds and the watcher refreshes the page under you.
- Index rows carry `data-f` (their file name) and group headers carry `data-g`, so the page controls address md reality instead of guessing from display text.
- Verified: a full add→archive round trip leaves board.md byte-identical; refusal paths (non-empty group, unknown op, taken letter) exercised over HTTP on 5599 and through the console relay on 8093; the boardform board's five groups now carry real intros (moved out of `## Pipeline`, which keeps only the overall narrative, so nothing is said twice).

## [0.9.2] — 2026-07-24

**The terminal self-heals, and its columns stop lying.** JL's screenshot (QD3's Lesson) showed reconnect banners knocking six times on a terminal that had been RELEASED — reconnecting cannot revive a dead ttyd — over a TUI mangled by drifting column math.

- after 2 failed reconnects the drawer now respawns the terminal through `/_board/term` (`--resume` restores the session) instead of knocking to 6 and giving up.
- `fitTerm` reads xterm's real rendered cell size (fallback to the old constants) and refits 350ms after connect — the pty and the pane agree on width, claude repaints clean.

## [0.9.1] — 2026-07-24

**No button closes the chatbot anymore.** JL clicked the drawer's "↻ Reload to see the result" and lost the drawer — that button predated live refresh and did a hard `location.reload()`, which tears down everything the scripts built. All four reload sites (the drawer's post-write button, the drawer's ↻, the dock panel's ↻, the discussion-add success) now call `window.__boardRefresh` — the QD6 in-place swap, run immediately — so content updates under you and the drawer stays open mid-conversation. Labels renamed to "↻ Refresh in place" / "↻ Refresh". First edit made directly in `assets/board.js` since the QB4 split — checked with `node --check` on the real file.

## [0.9.0] — 2026-07-24

**Live refresh, an honest wait line, and the QB4 split.** Three JL asks in one afternoon of drawer-testing.

- **live in-place refresh (QD6).** "When the chat changed something, refresh automatically — and my chat interface is still there." The page HEAD-polls its own URL every 4s (both servers send Last-Modified; the console's page route gained HEAD) and, on change, swaps ONLY `div.wrap`: content updates under you, scroll restored, "↻ board updated" toast, held while text is selected. The chat drawer (mid-stream included), terminal, and comment dock hang off `<body>` and never notice. No Node, no reload, drawer survives — that requirement decided the design.
- **the wait line tells the truth (QD2).** serve.py emits `stage` events ("booting claude — the full tier loads the whole skill registry…", "session up — sending your message") so the drawer shows real progress instead of a static "…thinking"; the collapsed thinking block is labeled `💭 Thinking (N chars — click to reopen)`. Verified along the way: resumed sessions DO stream thinking now (the explicit `thinking={enabled}` option cured yesterday's loose end ②).
- **build.py split into assets (QB4).** 2,488 → 850 lines: the page's JS and CSS now live as REAL files — `assets/board.js` (1,173 lines, `node --check`s in place) and `assets/board.css` (465 lines) — read and inlined at build, output still ONE self-contained board.html. Byte-identical proven on a frozen board (split vs. mechanically re-joined build), a proof that caught two wrapper-newline slips before they shipped. The grammar's home stays the skill; `haichat-board/` keeps importing it.

## [0.8.0] — 2026-07-24

**The gate shows the change (duplicating the VS Code extension, step 1).** JL: "what is the backend of the vscode claude plugin? I want to duplicate it." The backend is the `claude` binary over the stream-JSON agent protocol — exactly what the drawer already drives through `claude_agent_sdk`; the visible delta was the gate.

- serve.py's permission ask events now carry `detail`: Edit → old/new strings; Write → the file's current content vs. the proposed; MultiEdit → per-edit pairs (capped at 6); Bash → the command. Truncated (4k/edit) — a gate preview, not a diff viewer.
- the drawer renders it: − red blocks, + green blocks, commands verbatim, above Allow once / Always / Deny. Strip-scripts invariant unaffected (the gate only exists in the live layer).
- honest status: emitted JS node-checked; a live gate-pop E2E is still owed (full-tier boots load the ~150-skill registry and outran the test window).
- next duplication step (QD2 ④): one persistent claude process per session, like the extension — also the cure for those slow boots.

## [0.7.1] — 2026-07-24

**`## Files` links actually open.** JL clicked `cms_production.do` on the CMS board and nothing usable happened — the link machinery (`resolve()`'s walk-up + `## Links`) was fine; the serving side wasn't.

- `EXT` widened: `.do .R .sql .tex .bib .toml .csv .tsv .ps1 .log` now count as path-like, so backticked references to them resolve (existence-checked, as always).
- `serve.py` serves source-ish suffixes as `text/plain` — they display in the browser instead of downloading (default mimetypes made `.do` an octet-stream).
- The first consumer moved: `boards_api.py` now lives in HAIChat-SPACE's **`haichat-board/`** sibling project (own service on 8094; `haichat-inlab` imports the same router). Its page serving widened to any existing file under the space root, read-only, matching serve.py — that is what makes a `## Files` click work in the console.

## [0.7.0] — 2026-07-24

**English output + the parser as a service.** JL: "put all the things in English, no Chinese anymore — in the board html or markdown."

- **the emitted page is fully English.** All user-visible chrome strings in `build.py` translated (index labels, tooltips, comment badges, the CLI summary line); `<html lang="en">`; comment quotes render as `“…”`. New `scrub_cjk_comments()` drops CJK-bearing CSS/JS comments from the **emitted** page only — the source keeps its comments for developers; the build asserts the page still reads with scripts stripped, as before.
- **comment grammar widened to curly quotes.** `CM_HEAD` (build.py) and `resolve` (serve.py) accept `“…”` alongside `「…」`/`"…"`, and `serve.py`'s writer now writes `“…”`. Found the hard way: an English board written with curly quotes parsed to zero comments — they silently vanished from the page (~19k chars of body reappeared after the fix).
- **`build.py <dir> --json`** — the parser half exposed as a service (the boardform board's QE3: one grammar, two render paths). Emits meta + per-question `{state, owner, done/total, comments_open/total, sections}` from the same code the HTML is built from, so JSON and HTML cannot disagree (asserted in the consumer's tests).
- **first external consumer: `haichat-inlab`'s `boards_api.py`** (HAIChat-SPACE, branch `feat/haichat-board`) imports `build.py`/`serve.py` from this skill dir — SPACE mounting, board discovery, page serving, and the comment/discuss/resolve write-backs, none of it re-implemented. Design record: the boardform board's QE2/QE3.
- **terminal smoothness (QD3 ①–④):** the drawer terminal now auto-reconnects with backoff (the xterm survives, scrollback intact; the post-auth resize makes claude repaint), sends a same-size resize op every 30s as keepalive, refits via ResizeObserver when the pane resizes, and pre-warms the xterm assets on ⌨ hover (assets only — never `POST /_board/term`, which takes HOLD).
- the skill's own board (`diagram/BoardSkillBoard-260722/`, 23 questions) fully translated to English — body, JL quotes, comments, logs.

## [0.6.0] — 2026-07-23

**The question page was reordered so a stranger can read it.** JL: "currently it is very very hard for a fresh eye to understand." The diagnosis was ordering, not wording — the page gave you *what we did* before *what we're deciding and why*.

- **on-stage order is now fixed: intent first, state second.** `Question → Boundary → Diagram → Items to Finish → Where we are → Files`. Previously `Now` sat above `Done when`, so a reader hit a wall of implementation detail before learning the goal, and `Why here` — the single most orienting paragraph — was buried fifth.
- **`## Question` became a lede plus bullets.** It renders through `body()` now: the first paragraph is the 21px lede, and 2–4 bullets carry *why it's hard / what breaks if we don't decide / what it affects downstream*. The acceptance bar is stated in QA4's `## Law`: **read this one section and a zero-context reader knows what the question is.**
- **new `## Boundary` section** (`.bnd`, grey rule) — what the question covers and, more importantly, what it does **not**, naming the question that owns the excluded part. Without it readers bring another question's expectations to this one. Optional but strongly recommended.
- **new `## Files` section** (`.fls`, blue rule, last on stage) — which files this question touches, and what each one's role is. Read the question, then know where to go; change a file, then know which question to write back to. Paths in backticks become clickable through `board.md`'s `## Links`. Optional but strongly recommended.
- **`## Done when` → `## Items to Finish`, `## Now` → `## Where we are`.** Plainer names for a fresh reader.
- **`## Why here` retired** — its job moved into `## Question`'s bullets. Boards that still carry the section parse fine; it renders in the bottom folds, so no content is lost.
- **no board breaks.** `ALIAS` now maps one slot to many names, so `Done when`/`Items to Finish`, `Now`/`Where we are` and the old Chinese names all resolve. Every existing question file rebuilt untouched.
- **QA2 and QA4 reopened (`✅ → 🟡`).** The layout and the template were both settled under the old structure — this change invalidates them. QA4 carries the new `## Law` and a `## Lesson` worth keeping: *it was closed ✅ that same morning and reopened by one sentence from JL, because the finish line never included "a stranger can read it."* Every one of the board's questions was then converted to the new shape — Question as lede-plus-bullets, plus `## Boundary` and `## Files`, with `## Why here` folded in and removed (18/18, verified against the *rendered* page rather than the markdown, because a substring check gets fooled by headings that appear inside ascii fences — QA2 lost a whole section to exactly that). Still owed: the fresh-agent cold read.

## [0.5.0] — 2026-07-23

- 新增 **view** 动作：「打开 <板文件夹>」= 看已有的板，不是开新板。
  之前只有 open（开新板），第 5 步还只写「打开 board.html 给用户看」而没给命令，
  新 agent 会去跑 `open board.html` —— 那是在**服务器**桌面上开，用户（Remote-SSH，
  浏览器在自己笔记本上）什么都看不到。现在写明唯一有效的方式：
  通过 VS Code IPC socket + `browser.sh` 把 `http://127.0.0.1:5599/<板>/board.html` 推过去。
- frontmatter 的 description 补上「打开这块板」触发词，并写明 view ≠ open、禁用 `open`/`file://`。
- open 第 6 步改成「按 view 那节推到用户的 VS Code 浏览器」。
- 清掉写死的「14 题」（板的题数会变，写死必过期）。

## [0.4.3] — 2026-07-23

A compose box in every question's Discussion — write a thought in bulk, it lands in `## Discussion`.

- **`## Discussion` gets a textarea.** Inside each question's Discussion fold there is now a box + signer dropdown + "➕ Add to discussion". Type a thought — a whole block, *not* pinned to a sentence the way a comment is — pick a signer, press Add: serve.py appends it as `> WHO: …` to that question's `## Discussion` and rebuilds; a reload shows it. Reuses the existing write path (new `/_board/discuss`, sibling of `/_board/comment`) and is fence-aware like the comment fix, so it never lands in a `## Discussion` line shown inside a code example. With serve.py not running the button says to hand-write it instead. The box is inert static HTML without the script, so the invariant (strip every `<script>`, the prose survives) still holds. Decided the simple way (JL): into `## Discussion`, not a new section — reuses the free-form thread that already exists.

## [0.4.2] — 2026-07-23

A third level of hierarchy inside a section — the **group topic** — plus the comment-writer bug that surfaced it.

- **a whole-line-bold `**…**` becomes a group topic.** A line that is entirely bold is no longer just a bold paragraph; it renders as a 🔹-marked, slightly-larger heading that leads a cluster of items — sitting between the section heading (`.ch`, underlined, 📍/🎯/💡) and the item names (`.bt`, `▸`). Three visible levels now: 📍 section ＞ 🔹 group ＞ ▸ item. The 🔹 is the default marker; write an emoji at the start of the bold line (`**🎨 …**`) and it becomes the marker instead — the icon is *authored*, never guessed by the generator (build.py has no LLM, and guessing an emoji from keywords is exactly the kind of machine-guess the writing rules forbid). Mixed-bold lines (`**a** b`) are untouched — only fully-bold lines convert. Documented across `ref/q-template.md` (the `## Now` example), `ref/board-form.md` §5 (syntax table) and §8 (on-stage hierarchy). QA4 asked for it — recorded through the board's own comment layer.
- **the Question block shows its name.** Every other section renders a label (📍 Now, 🎯 Done when, 💡 Why here); the question line carried only a bare `❓`. It now has a small `❓ Question` eyebrow (`.ql`, accent, above the question text), matching the rest. QA4's remaining open comment asked for exactly this — resolved and re-anchored on close (the `❓` moved into the label, so the quote moved to the question text).
- **serve.py no longer writes comments into fenced examples.** `add_comment` matched the *first* `## Comments` heading in the file — including the one inside QA4's `md 段落→页面位置` code fence — so a comment on that slide landed in the example, not the real section. It now skips ``` fences when locating `## Comments` / `## Log`. The stray comment was moved back to QA4's real `## Comments`. (A running serve.py must be restarted to pick this up.)

## [0.4.1] — 2026-07-23

Doc-consistency pass out of the first fresh-agent acceptance read (the QB2 known-gap): a new agent, given only `SKILL.md` + `ref/`, opened a real board, built it, and the build.py-invocation drift it hit got fixed across the ref spec. `SKILL.md`'s open/build sections had already been corrected; `ref/board-form.md` had been left stale — exactly the cross-file drift this skill warns about.

- **`ref/board-form.md` synced to the `<skill>/build.py` call.** §7 still showed the bare `python3 build.py <folder>`, which fails if you `cd` into the board folder (the script lives in the skill dir, not the board). It now reads `python3 <skill>/build.py <board 文件夹>` with the same "don't cd in" note the SKILL.md open/build sections carry. The last bare shorthand in SKILL.md's `sync` section was corrected too.
- **`ref/board-form.md` §2 gains the slug + default-state rules.** `-<slug>` is short lowercase English, parser-ignored; a freshly-opened Q is always `state: 🔴 OPEN`. Both were in SKILL.md's open steps but missing from the "full spec".
- **`ref/board-form.md` §3 marks board.md's required vs optional sections.** The Q-file spec (§4) already listed 必填/选填; board.md did not — `## Topic` / `## Pipeline` / `## Pages` required, `source:` / `## Links` optional, now stated.
- **known-gap surfaced, not folded in.** The acceptance read hit a question the current model has no home for — where a note that is off the board's `spine` but worth keeping should go (not ⏸️ ON HOLD, which is on-topic-deferred; not a forced Q). Drafted as a question for the skill's own board; left off SKILL.md per the graduation rule (undecided stays out of the manual). Distinct from the existing `QB3` (migrate the two older boards).

## [0.4.0] — 2026-07-23

The single-Q slide layout (QA4) is settled and closed. The focus-mode slide got the polish that finally answered its last open fork — *what belongs on stage vs. folded* — and the rule graduated into the spec.

- **section headings gain a line + an `expand all`.** Each of 📍 Now / 🎯 Done when / 💡 Why here now has an underline and, when it holds collapsible items, a right-aligned `expand all` that opens/collapses every item and code block in that section at once. Pure enhancement (`.secall` + a delegated click handler): strip the script and each item is still individually openable, all text stays in the DOM.
- **code blocks fold by default.** A ```` ``` ```` block in the prose renders as a one-line `</> code · N 行` disclosure, revealed on click or via `expand all`; `## Diagram` (the headline picture) is the one that stays open (`body(txt, fold_code=False)`). So a slide's first glance is a clean column of item names + the diagram, not walls of code.
- **the big title copies with a space.** `<span class="hid">QA4 </span>…` — the id and title were glued on copy (`QA4Single…`) because the gap was CSS `margin`, not a character; a real space now sits inside the badge so the heading copies as `QA4 Single-Q slide layout`.
- **QA4's `## Law` graduated into `ref/board-form.md §8`**, not SKILL.md — display spec stays in the spec doc, keeping SKILL.md lean (QB1's rule). The on-stage/folded rule, up-down `Now`/`Done when` stacking, long-Q scrolling (no truncate/split), no-16:9-lock, and the copyable-title note all live there now. Graduated list: `QA2 · QA4 · QA6 · QC1`.

## [0.3.0] — 2026-07-23

The graduation mechanism — SKILL.md is now defined as the board's settled questions, distilled. Plus the live layer (serve.py) gets a foothold in the manual.

- **板 ↔ SKILL.md, written down.** New SKILL.md section: this file is the crystallisation of the skill's own board (`diagram/BoardSkillBoard-260722/`). A question that reaches `✅ SETTLED` graduates its `## Law` into SKILL.md; questions still `🟡/🔴` do NOT enter the manual — so a "just-decided" rule never gets written as iron law (QD1's permission rule was written hard, then overturned — the cautionary case). SKILL.md is therefore always *the sum of settled rulings, no more*. The rule lives in QB1's `## Law`.
- **serve.py enters the manual.** New `serve` action: one server serves the whole repo root (`serve.py --root <root>`), giving every board live commenting-to-disk plus chat/terminal per question. The old `comment` text ("stage in localStorage → Sync to md") was stale — QA6 shipped Save-immediately-writes-to-disk; the section now says so, with the browser Sync/Copy path demoted to the serve.py-not-running fallback.
- **chat / terminal held as provisional.** The QD group (drawer via claude_agent_sdk, terminal via ttyd) is real and running but still `🟡` — SKILL.md carries only a pointer to it, not rules, per the graduation mechanism.
- **actions regrouped** — offline (`open · add · build · sync · link · close`, needs only build.py) vs live (`serve · comment`, needs serve.py).

## [0.2.0] — 2026-07-23

`SKILL.md` written. Comments become first-class. The zero-script promise is restated as what it actually protects.

- **`SKILL.md` + three `ref/` files** — the skill is now readable by someone who was not in the room: `ref/q-template.md` (copy this to add a question), `ref/board-form.md` (full spec: folder, numbering, section↔page map, syntax table), `ref/writing-rules.md` (how to write it so people understand, plus the cold-read prompt and its convergence test). `ref/board-example.md` was replaced — it still held the pre-0.1 single-file `[BOARD]`/`[Qn]` form.
- **`## Comments`** — inline comments pinned to a sentence, each with its own state: `- [ ] JL 「quoted sentence」 · 260723 1100` plus an indented body; `[x]` marks it solved. Open comments highlight their sentence in the prose and force the fold open; solved ones grey out and strike through. A quote that no longer matches the prose is flagged **⚠ anchor lost** on the item and in the fold label — a comment can never silently detach. `## Discussion` stays as the free-form thread.
- **in-page commenting** — select a sentence, press 💬, write, Save. Comments stage in `localStorage` and go to the md in one shot via "Sync to md" (File System Access API) or "Copy". Any 1–4 letter initials work, not just the original defaults; new names are added from the dropdown and remembered, and each gets a stable colour.
- **`watch.py`** — rebuilds on any `.md` change, so "Sync to md" → refresh is a closed loop with no Claude Code in it.
- **topic/explanation bullets** — `- heading` plus indented lines renders as a bolded lead with its explanation underneath; `## Done when` items take the same shape. Long passages stop being walls of sentences.
- **`## Log` takes a time** — `260723 1030 · what changed`; the time is optional.
- **titles are phrases, ≤14 chars** — the full question belongs in `## Question`. The board's own ten titles went from 43 chars at worst down to 8–15.
- **the invariant replaced the rule.** 0.1.0 asserted "zero `<script>` in the output". That became false the moment commenting shipped, and it was never the real guarantee anyway. What is asserted now: **strip every `<script>` and each question plus the full prose is still there** (checked on every build). Scripts may only enhance.

Known gaps (tracked on the board at `0_utils/diagram/BoardSkillBoard-260722/`): "Sync to md" has never been run end to end (QA6), no fresh-agent acceptance run (QB2), the two older boards are not migrated (QB3), and comments already written into md have no check for a broken anchor after the prose is edited.

## [0.1.0] — 2026-07-22

First working version. Board = a folder; `build.py` turns it into one static page.

- **board form** — `<unit>/diagram/<NN>-<topic>-<YYMMDD>/` holds `board.md` (title · `spine:` · `close:` · `## Topic` · `## Pipeline` · `## Pages`) plus one `Q<A><n>-<slug>.md` per question, plus generated `board.html` and `fig/`.
- **binding is by PATH** — every `Q*.md` in the folder is on the board; `## Pages` only sets order and grouping. An unlisted file still renders (under ⚠️) and warns on stderr — a missed pages entry can never drop a question.
- **Q file sections in English** — `## Question / Diagram / Done when / Now / Why here / Glossary / Discussion / Log`. Chinese section names still parse, so older boards build unchanged.
- **`## Done when` is a checklist** — `- [ ]` / `- [x]`, with an auto count (`3/5`) in the panel header.
- **`## Diagram`** — a fenced ASCII diagram per question, readable in the md and rendered as-is in the page.
- **`## Log`** — dated one-line history per question (`260722 · what changed`).
- **state labels** — `✅ SETTLED / 🟡 PARTIAL / 🔴 OPEN / ⏸️ ON HOLD`.
- **zero `<script>` in the output, asserted at build time.** Every question is a real `<section>`; collapsibles are native `<details>`; navigation is plain anchors. The page cannot render blank.
- **focus mode is pure CSS** — `:target` + `:has()` show one question full-screen, unbounded (no card border/radius/fill), 38px title, prev/next/index links. Same file serves both reading and projecting; there is no separate `deck.html`.

Known gaps (tracked on the board at `0_utils/diagram/BoardSkillBoard-260722/`): `SKILL.md` is not written (QB1), no fresh-agent acceptance run (QB2), the two older boards are not migrated (QB3), inline comments are half-built (QA6 — the md syntax parses, the CSS does not exist yet).
