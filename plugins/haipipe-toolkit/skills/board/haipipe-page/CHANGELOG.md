## 0.56.2 · 2026-09-03

- Align the canonical Page tree with the Outline-owned Evidence Workspace:
  evidence lanes now live under `outline/evidence/`, while root
  `<page>/evidence/` is legacy migration input only.
- Keep `runs/` and `results/` as the optional local execution presenter and
  preserve `workflow/` as the machine phase-receipt lane.

## 0.56.1 · 2026-09-02

- Specify the Page Outline as `Address · Planned move · Evidence ·
  Supporting Run · Local Run`. Item state stays in Evidence-chip colour and
  detail rather than occupying a duplicate Status column.

## 0.56.0 · 2026-09-02

- Move manuscript Section writing rules out of the product Page source and
  into authored W records in `outline/<stem>-requirement.md`, beside the
  generated venue V records. Section Opening remains one reader paragraph.

## 0.55.2 · 2026-09-02

- Retire the Page-authored Narrative map. The one Page-level Outline is the
  current plan's derived table; no second map or source block is authored.

## 0.55.1 · 2026-09-02

- Specify the Page reader default: Opening stays visible; Outline opens with
  its plan table first; the optional Narrative map and all other Page folds
  start closed.

## 0.55.0 · 2026-09-01

- Make the Page's `▤ Outline table` a real review grid: `Address · Planned
  move · Evidence · Source / run · Status`. C/P headers preserve reader order;
  B rows join their typed Evidence Item and surveyed route without creating a
  second plan or evidence authority.

## 0.54.0 · 2026-09-01

- Replace the Page's optional `Diagram` section with `Outline`. The Page now
  shows its optional narrative map plus a read-only `▤ Outline table` projected
  from the current `outline/<stem>-outline-v<N>.md`; the outline plugin and all
  eight canonical process records remain unchanged and authoritative.

## 0.53.0 · 2026-09-01

- Rename the optional presenter from Execution to Runs: Execute stays a
  workflow action and the surface lists durable Run identities.
- Let a Page resolve either Folder-local Results or a canonical Task Page's
  Job-backed `results/<task>/<run>/` without copying generated output.
- Retire the stale "LOWER, CODE part" wording; Task-side Runs are primary and
  scripts/config/notebooks are conditional projections.

## 0.52.1 · 2026-09-01

- Rename the optional lower capability from Code to Execution: Run/Result
  pairs are stable, while scripts are optional implementation material.
- Keep Execution beneath the Task Face and outside lifecycle authority.

## 0.52.0 · 2026-09-01

- §🎭 states the workflow as two parts of named cycles (SHAPE · SURVEY · LAND
  · EMBED · WRITE · CHECK) with the run-anchored evidence law; the authority
  test routes by cycle; the type registry's four fields map to cycles; the
  glossary gains item row and cycle, and PROBE leaves it.

## 0.51.3 · 2026-08-31

- Route an in-place Folder's Page Face from
  `workflow/phase.yaml current.folder-kind` before Markdown frontmatter;
  legacy Page Type and filename routing remain compatibility fallbacks.

## 0.51.2 · 2026-08-31

- Align the glossary with Folder-native evidence storage:
  `evidence/probe/`, `evidence/display/`, and `evidence/bibex/` are canonical;
  flat lanes remain migration aliases only.

## 0.51.1 · 2026-08-31

- Clarify the Code seam: every displayed number produced by code crosses one
  page-serving collection job and QA binding; local Code may only validate or
  reshape non-authoritative intermediates.

## 0.51.0 · 2026-08-31

- Page is now explicitly the Page Face of a Folder. A migrated Folder resolves
  `folder-kind:` to its workflow-phase skill before consulting legacy
  `page-type:` compatibility.
- Application Page semantics moved into twelve I0-I5/D0-D5 phase contracts;
  `principle` left the compatibility inventory and remains a subordinate D4
  role.

## 0.50.0 · 2026-08-31

studio/ (JL: "this one is closer to the human"): the third category folder,
holding chat/ and draw/ — the person's own room on the page, where they talk
and sketch and the chat may redraw on their ask. Earned by nature, not count.

## 0.49.1 · 2026-08-31

A unit may carry README.md, DERIVED only (JL): a generated projection of the
two-part tree as it stands, for strangers reading the raw folder (GitHub);
never hand-written — the law stays in this file and the roster. Generator =
folderstat's walk with a --write flag (declared, not yet shipped).

## 0.49.0 · 2026-08-31

v5 (JL: "we don't need a specific code folder — treat the page/task folder AS
the code folder; two parts, the upper page part and the lower code part"):
the code/ wrapper of 0.48.0 is gone. The unit root is the code home, exactly
as a task folder already is: scripts/ (script files, any language, config/
inside) is the tidy home while a script may equally live in an evidence lane;
runs/ and results/ are REQUIRED members wherever code exists, at root; a
result never sits inside evidence/ and becomes evidence only through a probe
card's binding. Page and task now share one root grammar with zero wrappers.

## 0.48.0 · 2026-08-31

v4 of the category folder (JL: "code results and config should be separated
from the evidence"): the execution family gets its own top-level `code/`
(scripts any language · config/ · runs/ = the one door · results/), out of
evidence/. The gate line separates them: evidence is CITED material behind a
human gate; code/results is machinery, regenerable, gate-free, never PHI; a
result becomes evidence only when a probe card binds it. On a task unit this
family IS the folder root, so the page mirrors the task exactly.


## 0.47.1 · 2026-08-31

Internal drift caught by the Workflow Table Skill Coverage static-quality
review: the collection-job
paragraph still ranked the job in the retired `task/` lane; it ranks among
`evidence/pagex/` links now (the merge this same file's tree already stated).


## 0.47.0 · 2026-08-31

The category page folder (JL's evening rulings, v3): evidence/ holds bibex ·
probe · display · pagex · code · materials; delivery/ holds latex · word ·
slide · render; runs/ is the one execution door (code anywhere in the folder,
only a runs/ ticket calls it, simple-code law); meeting leaves the page
(project/SPACE level, parsed into outline/); the task lane merges into pagex
(a task folder IS a page folder); logging/ retired. Migration = per page,
whole, with flat-name SYMLINK STUBS so unpatched engine paths keep resolving;
piloted on QPf1-folder (bibex 200 via stub, 🧾 tab 200, roster scan silent).
Engine de-symlinking is tracked debt, per file.


## 0.46.0 · 2026-08-31

The unit symmetry (JL: "we should have the workflow and outline in both of
them"): every unit folder, page or task, carries outline/ (human half) AND
workflow/ (machine half). On a page, workflow/receipts/ takes one receipt per
pass, written by the RUN controller; the log record keeps its one-line
headline and points there. Roster row `workflow/` added; task side keeps its
plan.yaml/report.yaml unchanged and gains outline/ with its first real
collection job.


## 0.45.0 · 2026-08-31

The Page Type registry (JL: "the page types might be a function in other
skills' content"): `ref/type-registry.md` holds one record per engine key —
`outline` (mode; shape stays in a contract's frontmatter) · `evidence` (what
the kind owes exactly; feeds PROBE and the collection job) · `prose` ·
`closing`, with `standing: contract | key-only`. `cli/pagetypes.py --check`
grew the tooth: engine↔registry drift, contract records with missing fields
or dead law paths, and `registry-gap` for a key-only record with live pages
(fires today on collection·labeling·view; the missing-field branch proven on
a broken record first). Zero-page application types stay shipped, marked
dormant in their records — retiring their folders touches a family other
sessions run.


## 0.44.0 · 2026-08-31

Pointer, not inline (JL asked whether to fold it in): §📁 names the page-serving
collection job — task-type `page`, contract `task/haipipe-task-for-page`, ranked
first in the `task/` lane — as the code-shaped answerer of a page's task-route
cards. The card address `PP<NN>.v<n>` and every phase authority are unchanged.



## 0.43.0 — 2026-08-31
Rewritten to one lane, "what a page IS": 787 → 395 lines, present tense, no
attribution in the law (who ruled and when lives here). Each rule now has one
home and this file points at it:
- **Moved out**: the four-axis evaluation rubric, its four verdicts, review
  units and batch-voice test → `haipipe-page-check` §📏 (this file keeps the
  requirement-resolution order and a pointer); the five heading tests and the
  H1 verb-phrase rule → `haipipe-board/ref/writing-rules.md` §A heading is a
  lookup key; the write-for-the-render examples → one line each, owned by
  `page-template.md` and `writing-rules.md`.
- **Retired from the page contract**: the five-row section table with
  `folds Discussion · Law · Lesson · Glossary · Log` (log, discussion and
  files live in `outline/`; the folds are `Law · Lesson · Glossary`); every
  reference to `## States`, `## Files` and a page-side `## Log`; the ten-step
  create and eight-step work-on lists, now one paragraph each; the retired
  `route:` step ② row of the type table; the `##`-heading narration of what
  keys used to mean.
- **Stated for the first time**: a pass may run inside a person's session or
  as the phase's agent, and both leave the same trace (artifact, one log
  record, receipt); a person's chat ruling is transcribed with the quote;
  `outline/` is the process folder with seven record kinds, grammar in
  `haipipe-plugin-outline/ref/`; the location grammar gains the bullet address
  and the `D<nn>` thread.
- **Kept as is**: the type-resolution table and the generated inventory block
  (its `—` cells are `pagetypes.py`'s output, not hand-written); `### Decision
  Now` inside Aims (the one-home question, `D<nn>` versus Decision Now, is an
  open ruling and is not decided here).

## 0.42.0 — 2026-08-31

- **The page is the Aims' only home** (JL 260831, BoardSkillBoard QPf12 row 2:
  "In the Page as well, and should map to the content"). Reverses
  haipipe-plugin-outline 0.16.0's "the page keeps no copy": one row per Aim
  with tick, `Done when:` and `Now:` on the page; the plan keeps the shape and
  its 🎯 marks and no Aim rows; `### A<n>` maps to Content division `<n>`,
  which `check.py group-no-division` already enforces.
- **`## Files` retired from the page** (QPf12 row 3, "A"): the action map is
  `outline/<stem>-files.md`, `### F<n>` records with `Path` and `Role`, the
  a Related Board Page as a record with `Role: related` and its row verbatim; `pagecontext.py` and
  `check.py` read it, the 🧭 tab shows it as 📎 Files.

## 0.41.0 — 2026-08-31

- **The contract now states the 260819 merge it had only logged.** 0.34.0
  retired `## States` into `## Aims`, yet the section table, the conveys
  table, `🎯 One Aim, one State`, Decision Now, preview, create and work-on
  steps all still named States as a required section (JL 260831, on the
  MISQ paper board: "I think we removed the state from the page as well").
  One Aim is one row: tick, target, `Done when:`, `Now:`; a live ask is the
  Aim's `Now:` line marked `🧠`; `### Decision Now` keeps its shape and is
  reserved inside Aims. `haipipe-board/ref/page-template.md` and
  `ref/board-form.md` §4 carry the same change in the same round.

## 0.40.2 — 2026-08-29

- Page titles now target three to five visible words and have a hard ceiling of
  six. Acronyms, identifiers, and hyphenated compounds count as one word; a
  colon does not create a second allowance, and the page id is not part of the
  title. The shared template inherits the rule, and `check.py` reports
  `title-too-long` when a Page exceeds it.

## 0.40.1 — 2026-08-28

- `preview.py` now also takes a group or board folder (one roster line per
  page); those grains belong to `haipipe-board` 0.146.0, and this contract's
  preview subsection points there instead of a glob recipe.

## 0.40.0 — 2026-08-28

The 260828 field test (PaperSkillBoard-260725 repair, 14 minutes, 12 frictions)
settled 10 MATCH · 1 SKILL GAP · 3 EXPECTATION GAP against a sealed ledger.
This release is the gap's repair plus one commissioned feature.

- PREVIEW joins the verbs (JL request): `haipipe-board/cli/preview.py <page>`
  prints one screen — title, the Opening's visible paragraph, Aims joined to
  their States, the Content division list, the last Log row. The contract had
  already made those the page's summary surfaces; the tool only collects them.
  A gist, never a substitute for WORK ON's whole-file read.
- The laws are now readable before the act (frictions F11/F2, gap E13): the
  engine block points at `check.py --rules` (every finding code + message,
  derived from the checker's own source) and at `pagetypes.py` (the live type
  inventory). The field actor had learned all 19 of its WARNs from error text
  after writing, and counted Page Types by git archaeology, because nothing on
  a skill surface pointed at either.

## 0.39.0 — 2026-08-28

The contract had grown into five documents in one file — a type registry, a
section grammar, a writing guide, a verb door, an evaluation rubric — and no
reader needed more than a quarter of it, so no reader ever proofread the rest.
Measured before the rewrite: 32% of the file was two sections telling the same
retirement story, and they had already contradicted each other. −25% by
character; every rule kept, every retirement narration moved here.

- **The inventory is DERIVED.** `haipipe-board/cli/pagetypes.py` (new) reads
  the three places a Page Type actually lives — the shipped `*/page-types/`
  folders, `check.py`'s `PAGE_TYPE_VALUES`, and every `page-type:` line on the
  boards — and emits the table between markers in §🧬. `--check` exits 1 on
  drift. The hand-written table could not stay equal to a Python tuple and a
  folder listing, and on 260828 it was wrong in both directions at once: four
  keys were live on disk with no row (`question` 4 pages, `roadmap` 2,
  `ideation` 2, `collection` 2), and six keys the table called retired were
  still accepted by the checker. Drift is a finding now, not a paragraph.
  First run: 7 drifts, all real.
- **§🗂 `The Page Types that exist, and why the rest went (260819)` DELETED.**
  It was a second telling of §🧬 and carried the false rows: it listed
  `intervention` and `artifact` as live application types 355 lines after the
  same file declared both retired. Its two unique rulings — no key is the
  DEFAULT, and a discovery folder does not get its own type — moved into §🧬.
- **§📁 `What a page is on disk` ADDED.** The base contract for what a page IS
  never showed the page's own folder; `<page-dir>/` lived in `haipipe-paper`
  and `paper/README.md`, so a consumer owned the definition of the thing. The
  lane roster stays `haipipe-plugin`'s.
- **The admission test opens §🧬 as the grain law.** "A property every page
  carries cannot tell one kind of page from another" is the sentence that
  decides what earns a Page Type, and it was buried mid-file inside a
  retirement argument.
- **§✍️ gains a HEADING law**, five mechanical tests, governing this
  contract's own `##`, every page's `###` divisions, and every skill's H1:
  states the law not the topic · no count · no date · no self-reference · a
  clause after the comma earns its place only by ruling out a real mistake.
  Test ⑤ catches machine prose, whose commonest form is the negative
  restatement. Applied to this file the same day: eleven headings rewritten,
  `Seven Page Phases, independent of Page Type` → `Phases, independent of
  type` (the count had said `Four` until the 260817 split), `Three verbs, and
  this skill is the door for all three` → `Create · work on · run`, and the H1
  from a noun phrase about the document to `one shape every page keeps`.
- **§✅ `Closing checks` ADDED**, the one property this contract failed on its
  own eight-property ruler: every variant carries grep-able closing checks and
  the base carried none, which is why it could drift unnoticed.
- **History evicted to this file**, per the standing erasure ruling ("a doc
  states the CURRENT contract and never names the dead thing"). Gone from the
  contract: the dash merge-then-retire story, the four types deleted 260819,
  the display/literature/value retirement argument, the slide-deck history,
  the Writing Style relocation, the section renames, the `## Boundary`
  removal narration, the 260802 scope measurement. What survived is only
  history that is still a live rule — `route:` still parses, the retired
  section names still alias, the top-level `## Writing Style` still parses.
- Two false claims deleted rather than corrected, because neither was
  load-bearing: "TWELVE Page Type variants ship across five skill sets" (19
  across four), and a roster row naming `subjective-label/page-types/` as the
  owner of `haipipe-page-for-labeling`, a folder that does not exist.

## 0.38.0 — 2026-08-20

- **`page-type: dash` DELETED.** JL proposed merging it into `haipipe-paper-narrative`
  instead; the merge was rejected because Dash covered four families
  (`section · probe · citation · display`) and only `section` was ever
  Narrative-shaped, so folding it in would have stranded the other three with
  no owner. A `closes when: never` type that owns no gate and states no
  decision was never Page-shaped to begin with. It is `/haipipe-paper status
  [family]` now, a plain regenerated command owned by the paper family, not a
  resolvable Page Type. Contract archived whole at
  `paper/page-types/_archive/haipipe-page-for-dash/`. Twelve live Page Type
  variants remain (was thirteen).

## 0.37.2 — 2026-08-20

- Moved `haipipe-page-for-insight` in the owner roster from Task to Application.
  The Page remains Task-backed for source/run/staleness/Probe authority and now
  closes on an Application Design Handoff.

## 0.37.2 — 2026-08-20

- **The QA-file entry says what the NUMBER means and bans the shorthand**
  (JL 260820: "what is the QA/5? how to understand it?"). The number is the
  order that task folder answered questions in, not a rank or a version, and
  "QA/5" in a reply names nothing anyone can open.

## 0.37.1 — 2026-08-20

- **`ref/glossary.md`**, the family's word list (JL 260820: "cards <--- what is
  cards? do we have this glossary?"). Thirty-odd terms, each beside the PATH it
  names: card, display unit, mark, plan, bullet, tick, stake, bank, QA file,
  producer, judge. It restates no rule and points at the owning section where a
  word already has one. §🔤 added to SKILL.md so the file is findable.

## 0.36.0 — 2026-08-19

- **Four Page Types DELETED**: `for-design` (104L, 3 pages declared it, no
  speciality left), `for-meeting` (78L, 0 pages, it is a plugin and
  `haipipe-plugin-meeting` already ships), `for-skill` (311L, 0 pages, same),
  `for-view` (0 pages declared it, everything is a view now). JL ruled each.
- **No `page-type:` key is the DEFAULT**, and no `question` type was created for
  it: "question itself just to be very flexible" (JL 260819).
- **A discovery folder is a special TASK**, not a sibling type. `task` will carry
  which kind of folder it reads.
- **`insight` becomes a subclass of `task`.** Its DIKW chain was already written
  (Data → Information → Knowledge → Wisdom); only its parentage changes.
- `opening` → `seed`, venue-free; `narrative` stays venue-embedded and resolved.
  Both still to do.
- 15 types → 11 on disk, 8 in the intended shape once seed and the task subclass
  land.

## 0.35.0 — 2026-08-19

- **`Writing Style` moves INSIDE `## Opening` as a `###` subsection.** JL 260819:
  "I don't want to have the Writing style to be in the main page, please put it
  under the subsection in the Openning." It already rendered inside the Opening
  drawer, so only the source shape changed.
- The reason it does not belong on the main run: a top-level section answers a
  READER's question about the subject, and this one answers a WRITER's question
  about the page. On the main run it sat between Diagram and Content asking the
  reader to skip it.
- The top-level `## Writing Style` still parses. 123 of 274 pages carry it, and
  deleting someone else's text on read is a silent loss.

## 0.34.0 — 2026-08-19

- **`## States` RETIRED, merged into `## Aims`.** One Aim is now one row carrying
  its tick, its `Done when:` test and its `Now:` fact together. JL 260819, after
  reading the 🧭 tab's division card and asking whether the page still needs both
  sections when the card joins them anyway.
- The argument is this page family's own history: on 260819 the checker reported
  `aim-stated-twice` and `state-without-aim` on `QPw00-page-loop`, and a
  duplicated `### A7` group heading left the parser taking whichever it met last.
  One id in two places is one fact with two owners.
- A State row with no Aim id was never a status. It becomes the Aim's optional
  Plan, or it leaves the page.
- The plan file keeps target and test, never status: a plan freezes at approval
  and a status changes daily, so a moving fact inside a frozen file is exactly
  what the 260817 ruling forbids.

## 0.33.0 — 2026-08-18

- RUN's dispatch may NOT be delegated to a subagent. A subagent is not handed
  the `Workflow` tool, so `run <page>` runs in the session it was typed in.
  Proved by dispatching `haipipe-page-orchestrator-agent` as itself for the
  first time on 260818: it returned `blocked` at its own step 2, with 0 steps
  and no receipt, because three of the seven tools it declares were absent.

haipipe-page · Changelog
========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.32.0 — 2026-08-17

**Task/Insights and Application receive globally unique Page Types.** Step ③ now
resolves `insight`, `brief`, `intervention`, and `artifact`, raising the roster
to sixteen variants across six owning skill sets. Application deliberately uses
Brief rather than Paper Opening and Intervention rather than Board Design, so a
`page-type:` key remains sufficient without consulting the current family.

## 0.31.0 — 2026-08-17

**Paper Opening is a first-class Page Type.** `page-type: opening` resolves to
`haipipe-page-for-opening`, upstream of Narrative and Section. The roster now
states the live total: twelve variants across five owning skill sets, including
the previously omitted Task Page Type. Narrative's roster line now describes
story architecture and source allocation rather than ownership of all claims.

## 0.30.0 — 2026-08-17

**Seven Page Phases, not four.** §🎭's table and its authority test now list
OUTLINE, DRAFT, PROBE, EVIDENCE, REVISE, COMPILE, CHECK, with the load path for
each. The three splits and the failure each one allowed stay in
`page-workflows/haipipe-page-workflow`; this table only stopped contradicting
them. The authority test gains `the section list itself is being agreed →
OUTLINE`, `a marked hole has no card open for it → PROBE`, and `a card is open
and its answer must land → EVIDENCE`.

## 0.29.0 - 2026-08-16

**display, literature and value retired as Page Types** (JL 260816): "every page
will have them, so I will treat them more like the page plugins." They fail the
admission law for the plainest reason available: a property EVERY page carries
cannot distinguish one kind of page from another, so it changes no closing rule,
and a kind that changes no closing rule is plugin material (the same law that
retired for-slide at 0.26.0).

- Type resolution drops step ② entirely. `route: outward` / `route: inward` no
  longer pick a contract. The HEAD LINE ITSELF SURVIVES: `src/topic_entry_contract.py`
  still trusts it and it still names the evidence lane, so no code changed here.
  A page carrying `route:` now falls through to ④ or ⑤ and resolves by filename.
- Type resolution drops the step-③ key `page-type: display`.
- `paper/page-types/haipipe-page-for-{display,literature,value}/` moved whole to
  `paper/page-types/_archive/`, which `install.sh` prunes, so the retired
  contracts stay readable without shipping.
- Each already had a plugin lane shipping BESIDE its type, which is what made the
  duplication visible: `<page>/display/` (QPf5), `<page>/bibex/` (QPf8),
  `<page>/probe/` (QPf9) on the design board.
- The four family DASHES SURVIVE. A dash is a rollup page with its own closing
  rule, and it rolls up pages carrying a plugin exactly as well as pages that
  wore a type.
**The four per-family DASHES merged into one** (JL 260816, same session: "maybe
just one thing for all"). Their `closes when` cells were identical character for
character, all four reading `never · a dash has no gate and is regenerated each
run`, and so were their type key, their venue rule, their generated-versus-authored
split, and their empty-cell rule. Four contracts stating one closing rule is one
type whose family is a FIELD.

- `paper/page-types/haipipe-page-for-dash/` is the merged contract. It states the
  shared rules once and carries a four-row payload table for what differs.
- `haipipe-page-for-dash-{section,value,display,literature}/` moved whole to
  `_archive/`, keeping their payload detail readable.
- `dash_family: section | value | display | literature` is PROMOTED from a
  specimen-only fallback to REQUIRED on every dash, including one wearing an
  `S-<Family>-Dash` filename, where the two must agree. With one contract the
  filename picks nothing, so the field is the only thing that says which family.
- Step ③ now resolves every key to exactly ONE contract; the key-and-filename
  cooperation that existed only for `dash` is gone.

- Seventeen variants become ELEVEN. Re-run `install.sh --global` (repo root) so
  the seven removed symlinks stop resolving.

⬜ NOT DONE, needs a separate pass: three code sites still name the retired
contracts in comments or accept their keys —
`cli/bib-from-bank.py:91` (accepts `page-type: literature`),
`src/dialect_paper.py:714` and `src/parse.py:149` (comments naming for-value /
for-literature). None is load-bearing for resolution; all three now describe a
world that no longer exists.

## 0.28.0 - 2026-08-16

**The `state:` line is a row, not a paragraph** (JL 260816, ruled on the design
board's QPs1 after reading QPf9's four-clause line): after the status word, at
most two ` · ` parts — what stands, then `open:` with a short list or a count —
and the whole line under 110 characters. `check.py` gained a `state-line-long`
warning; `ref/page-template.md` carries the same rule beside the title contract.

## 0.27.0 - 2026-08-15

**RUN moved out to `page-workflows/haipipe-page-workflow`** (JL 260815, ruled in
the Page-Workflow session): the workflow gets one nameable HEAD skill beside its
four member contracts, matching the one-folder-one-workflow shape every family's
`page-workflows/` follows. `ref/page-run-contract.md` moved with it. This skill
keeps CREATE, WORK ON, and the page contract; its RUN verb is now a handoff that
states only the two entry rules (new Page starts at DRAFT after CREATE, existing
Page with unknown next authority starts at CHECK). Phase load paths updated from
the renamed `page-phases/` to `page-workflows/`.

## 0.26.0 - 2026-08-15

**for-slide retired** (JL 260815, ruled on the design board's QPf3): a deck is
plugin material at `<page>/slide/<page>-deck.html`, authored by an agent
(`/_board/autodeck`) and regenerated on demand, never a Page Type.

- Type resolution drops the step-③ key `page-type: slide`.
- `page-types/haipipe-page-for-slide/` removed from the family; its specimen
  is archived on the design board (`_archive/QBt9-for-slide.md`).
- Sixteen variants ship. Re-run `install.sh --global` (repo root) so the removed
  variant's symlink stops resolving.

## 0.24.0 - 2026-08-09

**Five paper variants admitted** (JL 260809), taking the roster to sixteen across
three skill sets.

- Four family DASHES, one per multi-unit paper family:
  `for-dash-section`, `-value`, `-display`, `-literature`.
- `for-narrative`, which absorbs seed, claims and pitch and adds the
  section-by-section outline the Section pages execute.
- Type resolution gains two step-③ keys. `page-type: narrative` behaves like
  `page-type: section`. `page-type: dash` is the first key that resolves to a
  FAMILY of contracts: the key says the page is a rollup and the
  `S-<Family>-Dash` filename says which of the four, so a key and a filename
  cooperate here instead of one beating the other.
- Two merges recorded on JL's ruling, both grounded in the real pages:
  **Value absorbs resource**, because `S-Work-R1-cms` already pointed at
  `tasks/A11_CMS-pipeline/` and sat at PROBE pending with no `route:` line;
  **Section includes Appendix**, because one stage row and one Page Type already
  governed both and only the reader-order key differed.

## 0.23.0 - 2026-08-09

- Page Type variants now ship under the `page-types/` folder of the SKILL SET
  THAT OWNS THEM (JL 260809). Every skill set carries its own `page-types/`, so
  the folder a variant sits in is what names its owner.
- Eleven variants across three skill sets, replacing the "ten, all here" roster:
  five in `board/page-types/` (for-stage, for-skill, for-meeting, for-slide,
  for-design), five in `paper/page-types/` (for-venue, for-section, for-display,
  for-literature, for-value), one in `subjective-label/skills/page-types/`
  (for-labeling).
- `for-stage` stays on the board side on purpose: a stage page is a BOARD
  mechanism (chain, managed contract span, human gate) that the paper and
  application families both instantiate, not a paper artifact.
- Supersedes "ships WHERE THE BOARD FAMILY MAINTAINS IT" (JL 260803), which held
  only while one family owned every variant.
- The base contract, the Type resolution table, and the phase grammar are
  unchanged. Only ownership and the roster moved.

## 0.22.0 - 2026-08-09

- Renamed from `haipipe-board-page` to `haipipe-page` (JL 260809), so the three
  altitudes read board, page, sentence, one word each.
- The 14 units built on this stem followed it: the 10 `page-types/` variants,
  the 4 `page-phases/` contracts, plus `haipipe-page-orchestrator-agent` and the
  externally maintained `haipipe-page-for-labeling`.
- No contract change. Every section rule, the Type resolution table, the phase
  grammar, and the RUN receipt are byte-identical apart from the name.
- `haipipe-board-routing` deliberately kept its prefix, on JL's call, so the
  family no longer names its members by one rule. The trade is recorded in the
  family `CHANGELOG.md`: this name now reads as a peer of `/haipipe-paper`
  rather than as a unit under the Board door.

## 0.21.0 - 2026-08-06

Resolution step ② re-keyed (JL's evidence-page ruling, 260806): the two
evidence types resolve by the HEAD `route: outward | inward` line, one line in
the metadata head right after `owner:`/`method:`, replacing the retired
`### Q-consumer register` marker + register route line. The variant table now
says "evidence page" for the pair; `haipipe-board/ref/topic-entry-contract.md`
declares the line.

## 0.20.1 - 2026-08-05

Resolve-order slot reworded for thin-paper phase 2: the last slot is
"family craft: the stage's declared craft files (and for probe, the family
door's probe tooling)". Family-specific stage data (the paper door's stages/
and craft files) stays in its own family; `haipipe-paper-stage` is retired.

## 0.20.0 - 2026-08-05

**One resolution table, every type machine-resolvable** (review fix). The stale
"Six Page Types" table, written when six types existed, is replaced by a single
resolution table covering ALL types, resolved in a fixed order: ① filename
prefix (`Skill-`/`Agent-` → for-skill, `Meeting-` → for-meeting, `QBv` →
for-venue), ② the register's REQUIRED `route: outward | inward` line
(for-literature / for-value, declared in `haipipe-board/ref/topic-entry-contract.md`),
③ the REQUIRED frontmatter `page-type: display | slide | design | section`,
④ the `S-<Family>-<unit>` stage filename, ⑤ the Q filename. Exactly one key
matches or the page is defective. A `page-type:` key beats the filename, which
settles the S-Display-4c stage/display double match and the QA4 Q-file slide
page.

- Four stale self-contradictions fixed: the six-type heading and table; "the
  three Page Type variants maintained here" (ten); the "five implemented types
  need only four prefixes" sentence (the glob decides membership only, the
  table decides type); the claim that Meeting "has no contract in any skill"
  (it has for-meeting).
- The admissions paragraph is split into short sentences; "ride the stage
  shape" now reads "look like stage-page filenames".

## 0.19.0 - 2026-08-05

**for-design admitted** (JL, ruled A on the design board's QB6; his definition,
260805: "we want to design some messages, say message A, B, C for one group of
people; the Content divisions ARE the different messages"). One page per design
BRIEF, its Opening stating audience, goal, and constraints; one Content division
per CANDIDATE, each carrying the artifact itself, its rationale, and its fit to
the brief's criteria; Aims are the criteria. Closes on a SELECTION record naming
the winner, why, and each loser's disposition (dropped · kept for A/B test ·
merged). Sits upstream of for-display: design selects the candidate, display
accepts its render. A losing division is never silently deleted, because the
rationale for NOT choosing is part of the design record.

## 0.18.0 - 2026-08-05

**for-slide admitted** (JL, on the Page-for-Slide branch). One page per deck, one
division per slide, each carrying its outline plus the PNG export of the built
slide; the live html-ppt deck stays a linked artifact because the board strips JS.
The slide binding (division · source · render · acceptance) is its typed record.

## 0.17.0 - 2026-08-05

**Two more Page Types admitted** (JL, same day, thought against the paper skill board and the MISQ board together).

- `for-section`: loads `for-stage`, adds the section kind, the venue contract block (blueprint BINDING, style reference, override stated), and the landing surface for the three record types. Reverses the for-main rejection: Main is one family's region, section is a cross-family shape.
- `for-meeting`: the routing rule for spoken decisions; Meeting pages stop being contract-less.
- The types table's Meeting row now states the real closing rule.

## 0.16.0 - 2026-08-05

**Three Page Types admitted** (JL, QB6 Decision Now: D, plus display standing alone).

- `page-types/haipipe-page-for-literature` and `-for-value`: two types over ONE loaded topic core (`ref/topic-entry-contract.md`), each adding only its route's translation layer. They resolve by the register marker plus route direction, not by filename.
- `page-types/haipipe-page-for-display`: mirror-shaped, but its unit is produced by the project and closes on human acceptance of a specific render.
- The Six Page Types section now lists six variants and says why the last three were admitted.

## 0.15.1 - 2026-08-05

**Nine review findings applied** (fresh-context cold read, verdict REVISE; JL: "go ahead to update it").

- The Decision Now reservation now admits the unsettled S-page exception (`### Needs JL · tick these`) instead of stating the rule as settled while a variant contradicted it.
- The "A CHANGE IS FINISHED" paragraph split to one sentence per line; the QC1b consumer chain split at its double colon.
- The boundary figure names `cli/serve.py` and `cli/check.py` with their dir, as it already did for `src/`.

## 0.15.0 - 2026-08-04

- Adds `### 🔗 Related Board Pages` as the fixed, typed Files group for bounded
  cross-Page context rather than configuration inheritance or dependency
  inference.
- Defines relation + Page Phase + Page id + scope + Board-relative path rows.
  Scope is either one whole Page or one direct Content division; a division
  brings its Page identity, Opening, and matching Aims/States group.
- Requires agents and Page RUN to resolve the current phase through
  `cli/pagecontext.py`, one hop only. Broken paths, mismatched Page ids, missing
  scopes, and malformed rows stop as mechanical findings instead of silently
  dropping context.
- Emits Page identity and Opening once when one phase selects several scopes on
  the same target, after the first fresh-context trial exposed the repetition.

## 0.14.0 - 2026-08-04

- Adds the concrete `RUN` verb for one bounded, non-linear Page lifecycle. It is
  not named `ADVANCE` because phases may repeat, branch, HOLD, or begin a new
  DRAFT round.
- Adds `ref/page-run-contract.md`, the common raw-material packet, phase receipt,
  version identity, role-separation, durable audit bundle, legal-route, stop,
  and fault-test contract shared by all four Page Phases.
- Requires the producer, mechanical builder, and judge to have distinct actor
  identities and verifies that each version is exactly its two declared
  lowercase SHA-256 digests.
- Makes the CLI independently rehash the current source and rendered Page, so
  agreement among receipt fields cannot substitute for artifact identity.
- Audits the preserved packet against the run and enforces receipt-to-receipt
  version continuity, start-phase identity, gate identity, and declared bounds.
- Wires RUN to the Board-owned Workflow and deterministic lifecycle auditor.

## 0.13.0 - 2026-08-04

- Adopts QB9's lifecycle vocabulary without adding an `ADVANCE` verb: one persistent Page combines a stable Page Type with a current DRAFT, PROBE, REVISE, or CHECK phase.
- Adds the load order `base → matching Page Type → current Page Phase → family worker` and routes phases by authority rather than add, delete, move, or rewrite operations.
- Moves the three `for-*` variants under `page-types/` and names the four direct phase contracts under `page-phases/`.
- Defines returning to DRAFT after purpose or Aims change as a new round on the same Page.
- Changes the section write table from generic machine permissions to phase authority, including the correction that changing Aim intent is DRAFT rather than REVISE.

## 0.12.0 - 2026-08-03

**Board bucket review, 260803** (JL: "go ahead to solve yourself, dont ask me"). Ledger: `skills/_console/260803-board-bucket-review.md`.

- **"The seven sections" is gone.** It was an invented count, cited as settled by four files, and it disagreed with its own authority and with the template: `ref/board-form.md` §4 fixes the ON-STAGE order at FIVE, and `ref/page-template.md` carries 13 `##` headings. Every statement now points at the authority instead of restating a number.
- The kind table went from three kinds to **six**, with the note that `src/common.py` globs four prefixes because a `Skill-` page rides the `S` glob.
- Both variants are named, with which page kind each governs, so a `QBv` author is routed. Only `haipipe-page-for-skill` was named before.
- The variant location rule is MAINTAINER-based, matching the door.
- The Opening budget says target ~450, hard ceiling 520, which is what `check.py` enforces. It had said "under ~450", a limit nothing checked.

## 0.11.1 - 2026-08-02

- Routes the two skill and agent page kinds away from this skill's own `create a new page` steps. They are GENERATED by `haipipe-board/cli/skillpage.py new`, which writes the page from its own stub and registers it in `board.md` itself; copying `ref/page-template.md` and registering by hand produces a page with no managed spans that the checker reports as broken forever.
- Found by a blind door test that followed this contract literally and hit the contradiction: two create procedures existed and nothing said which applied.

## 0.11.0 - 2026-08-02

- Names `haipipe-page-for-skill` as the variant for the Skill and Agent mirror
  kinds, and says to load it before writing or fixing any `Skill-<n>` or `Agent-<n>`
  page. It is the one variant that ships BESIDE this skill rather than under a
  consumer family, because for those two kinds the consumer IS the board family.
- Records why that variant had to exist rather than a tighter rule here. This skill
  already carries the noun-substitution test, so the rule was on the books when five
  skill and agent pages came out of one template on 260802. The cause is upstream of the test:
  this skill's Opening shape ends in `what this page decides`, and a mirror page
  decides nothing, so a writer obliged to ask a question can only manufacture a
  rhetorical one. The empty slot was the defect, not the writers.

## 0.10.0 - 2026-08-02

- `working on an existing page` gains steps 7 and 8: ONE page is the deliverable,
  a write outside it is allowed only when the page cannot be made correct without
  it and must be named in the report, and a sibling page's CONTENT is never
  rewritten. Step 5 sends an agent to other files on purpose; nothing bounded it.
- The verb now states the measurement that produced the rule. Three fresh agents
  were each given one sentence and nothing else on 260802. All three found this
  skill unaided (at tool calls #5, #6, #5) and drove their page to zero findings,
  including the one whose wording matches no trigger in the description. They then
  disagreed completely about reach: 1 file versus 15, the wide one touching four
  shipped `SKILL.md`, four `CHANGELOG.md`, six sibling pages and `board.md`.
  Neither was wrong on the merits, which is exactly why the bound had to be written
  rather than left to judgment.

## 0.9.0 - 2026-08-02

- A machine now CLOSES a `### Decision Now` row once the person has answered it,
  recording which option, who ruled, when, and the words they used (JL 260802:
  "I think you should close it automatically, please go ahead and do it").
  It still may not close a row nobody answered, and may not flip a page-level
  human gate; a machine's own recommendation is never an answer. Before this a
  row answered in chat and acted on within the hour still rendered as pending,
  so the page reported work as waiting that had already shipped.

## 0.8.1 - 2026-08-02

- Repointed every design-board citation after `QC1b`'s 260802 Content rebuild: the door test
  moved from `QC6 §7` to `QC1b §1`, the anchored-write rule from `QC6 §9` to `QC1b §4`, and the
  human-decision rule from `QC6 §10` to `QC1b §5`.
- Corrected the named next step. The rule strings it must replace are not in `cli/serve.py` and
  there are not one of them: they moved to `live/chat.py` in the `QC2c` live-layer split, and
  there are four (`CHAT_RULES`, `FULL_RULES`, `BOARD_CHAT_RULES`, `BOARD_FULL_RULES`).

## 0.8.0 — 260802

- TWO VERBS, and this skill is the door for both (JL 260802: "could we just
  rely on haipipe-page for this purpose? like haipipe-page create
  a new xxx on the topic of xxx, or working on the xxx"): `create a new page
  on <topic>` scaffolds from the template and registers it in the roster;
  `working on <page>` brings an existing page up to the contract, starting
  from the checker's findings rather than the top of the file.
- The boundary was restated rather than broken. "Never renders, serves or
  checks" meant this skill does not CONTAIN that code; it does call it. A
  reader asking for one page should not have to know which script does what.
- The engine commands both verbs run are listed once, so nobody memorises
  them, with the note that `watch.py` covers `.md` only.

## 0.7.0 — 260802

- Usage stated at the top of the revise section: `/haipipe-page <page>`,
  and START FROM THE CHECKER FINDINGS rather than the top of the file, because
  each finding already names the rule it breaks and the part it is in.
- Four spots caught up with QB4: the Aim status vocabulary is `⬜ 🔨 🧠 ✅ ❄️`
  (shape, not hue) and is NOT the page `state:` set; an Aims or States group is
  `A<n>` carrying its Content part's number, name and emoji; Files groups are a
  menu of ACTIONS (Engines · Contracts · Checks · Input · Output); and an Aim id
  points at a Content PART.

- Makes `haipipe-page` the prose authority loaded by every one-page writer
  instead of copying an Opening checklist into assignment prompts.
- Keeps the physical Opening shape but removes the fixed sentence count and
  rhetorical slot order; difficulty, failure, downstream effect, and success
  are review probes rather than one sentence each.
- Requires an existing page to be read completely before its Opening changes,
  adds the noun-substitution self-check, and keeps independent approval with a
  fresh reviewer.
- Adds a batch readability unit so individually clear pages still fail when
  they repeat the same sentence stems or form-letter argument across a Board.

## 0.5.1 - 2026-08-01

- Clarified the base/variant boundary: a consumer variant defines Content and
  may fill typed records through declared Aims, States, and Stage Contract
  extension points, but it never redefines the shared frame sections.

## 0.5.0 - 2026-08-01

- Keeps requirements in the page spec instead of copying them into a separate
  evaluation skill.
- Resolves base, variant, page-local, Stage Contract, division, and paragraph-job
  requirements before judging.
- Defines four axes (mechanics, function, evidence, readability), four verdicts,
  and one evidence-bearing report row per section or Content unit.
- Assigns execution to the existing `check.py`, `✅ Quality Check`, and fresh
  Board reviewer surfaces.

## 0.4.1 - 2026-08-01

- Canonicalized the paired section labels as `Aims / States`: both are plural
  collections, while one Aim still maps to one current State record.
- Kept singular `State` as a legacy input alias alongside `Where we are` and
  `Now`.

## 0.4.0 - 2026-08-01

- The page contract now separates durable intent from present fact. `## Aims` holds stable Content-linked targets (`A3.1`, with `P1` for page-level targets), a testable `Done when`, and an optional temporary `Plan`. `## State` mirrors every Aim exactly once with ⬜, 🟡, 🟠, ✅, or ⏸️. State transitions go to Log; Decision Now remains the human-only checkbox edge. A Content division may have zero, one, or many Aims, while every Aim must have one current State row.
- The fixed sequence is `Opening → Diagram → Content → Aims → State → Files`. The contract no longer teaches the retired generated Structure row or checkbox-based page completion. Historical `Items to Finish`, `Done when`, `Where we are`, and `Now` remain parser aliases, not canonical authoring guidance.

## 0.3.0 - 2026-08-01

- The five-row section contract (JL 260801, ruled as option A on the design board's
  QB4 Decision Now): every section answers ONE reader question, and the same five
  rows define each section's contract — conveys · holds · source · rules · omit.
  The seven-sections table gains the reader-question ladder plus the
  misplaced-sentence rule (substance in Opening → Content, contract material in
  Content → Stage Contract, settled flags → Where we are, open work → Items to
  Finish). Long form stays on the board's QB4a-QB4g faces; the compact form now
  lives here and in `ref/q-template.md`'s How-to-use comment, where a writer
  actually meets it.

## 0.2.0 - 2026-07-31

- Decision Now: the one RESERVED subsection name inside `## Where we are` (JL, same
  day: "don't make the decision here ... Always go to the corresponding Q's Where we
  are's subsection of Decision Now"). It lists the decisions a machine proposes and
  the human must make, one `- [ ]` row each with the ask, the options, and a
  recommendation; the human answers by ticking; an answered row moves into the
  page's dated record. The 260729 contextual-naming rule stands for every other
  subsection; this is its single exception.
- The tick rule now names the landing spot: a machine PROPOSES a tick as a Decision
  Now row, never in chat alone.
- The board pages `QB4e` (the Where-we-are face) and `QC6` on the design board carry
  the first two live subsections.

## 0.1.0 - 2026-07-31

- First cut, created on JL's order ("make the haipipe-board thinner, and have other
  skills, like haipipe-page ... please creating them now") from the roster the
  design board had already settled: QC6 §8's shape is one door, two SPECS, two VERBS,
  and this is the page SPEC the routing and digest verbs LOAD.
- Contract-first: no code moved. It owns what a page IS (the three kinds over one
  base, the seven sections in their fixed order, the write anchors), and it cites
  `haipipe-board/ref/q-template.md` as the authority rather than forking it.
- Carries the two machine-write rules with their provenance: writes land at a
  SECTION BOUNDARY, never a byte offset (QC6 §9, after a concurrent session spliced
  a heading into the middle of another page's Question sentence on 260730), and a
  transcript-reading verb may propose a tick but never tick or flip `state:`
  (QC6 §10, because reporting a claim is not verifying it).
- Names its own next step from QC6 §7: `serve.py`'s `CHAT_RULES` becomes a consumer
  of this contract instead of a hand-rolled copy, which has already rotted once
  (QB5d caught it describing a page shape that no longer existed).
## 0.57.0 · 2026-09-04

- Adopt `00 CONTEXT`, `01 OUTLINE`, `02 EVIDENCE`, `03 CONTENT`, and
  `04 CHECK` as the Page phases.
- Add generated `outline/<stem>-context.md` and start new Page Runs at CONTEXT.
- Replace active DRAFT/REVISE phase authority with `haipipe-page-content`.
- Remove PageX from new Page evidence storage; keep old lanes read-only and
  route cross-Folder evidence through Supporting Run Results.
