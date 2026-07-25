# HANDOFF · S-faces: haipipe-paper-stage and haipipe-board become one format

Date: 2026-07-25
From: the session that built the MISQ lifecycle board (QC3 folder-Qs, QB5 src split,
      QF1 embeds, QF2 doc slides) and then designed S-faces with JL.
For: the next session (fresh context) that will BUILD the S-face pilot.
Status of this design: SETTLED in discussion with JL through 2026-07-25, EXCEPT the
      open items in section 9. Nothing below is implemented yet. No commits anywhere.

READ THIS WHOLE FILE BEFORE TOUCHING ANY FILE. The design went through several
reversals; earlier ideas (a `stage:` adapter directive, deriving sections at build
time) are DEAD, superseded by the S-face design in section 4. Do not resurrect them.


## 1 · What problem this solves

Two skills own the same paper folder and could not read each other:

```
haipipe-paper-stage                       haipipe-board
(skills/paper/1-lifecycle/...)            (skills/0_utils/haipipe-board)
─────────────────────────────             ─────────────────────────────
writes 0-lifecycle/<stage>/<stage>.md     renders Q<letter><n>-<slug>.md faces
setext sections, Status: prose line,      atx sections: ## Question,
Q-consumer blocks, > CHECK: comments      ## Items to Finish, ## Where we are,
DPRC phases fill it                       ## Comments; state: glyph line
```

The MISQ paper board (examples/Project-Personality-OpioidRx/papers/
Paper-Personality2Opioid-MISQ2026/0-lifecycle/board.md) currently bridges them with
`doc:` slides (QF2): the stage docs are dumped raw onto the page. JL rejected that
look: "I cannot have it looks like the Q-template."

JL's ruling (verbatim, 2026-07-24/25, across several messages):
- "I want both haipipe-paper-stage and haipipe-board can work together."
- "the items to finish might from the Q-consumer, right? and Question part, should
  be the content. And I want to make each paragraph to be each subsection."
- (on Where we are) "it is more like the items we fixed, right?"
- "we might don't use the _LOG as well, or we might treat the the stage as the
  stage.md as well? ... Keep things to be simple."
- "0-seed/0-seed.md should it just be SA0-seed.md? and then we have
  SA1-resource.md??? maybe we can put the current version asiden and make the new
  ones?"
- "Could we change the Question to be Topic: xxx and then Content: this will be the
  content of the previous stage content ... and for others we will be the same?"

The final shape: THE STAGE FILE ITSELF IS REWRITTEN INTO BOARD GRAMMAR (an "S-face"),
both skills read and write that one file, and the board needs no adapter at all.
One format, two skills, no derivation logic, no drift between a face and its backing
doc, and the live comment layer works on stages again (doc slides had to give it up).


## 2 · Where everything is (paths inventory)

Board skill (all board code lives here):
  Tools/plugins/haipipe-toolkit/skills/0_utils/haipipe-board/
    build.py            thin entry (~70 lines), imports src/, asserts no-JS invariant
    src/common.py       ST/STN state map · ALIAS section names · sec() · stinfo() ·
                        QNAME regex · vet_qpath() · q_files() rglob discovery
    src/parse.py        split_blocks/split_sections · parse_board · parse_doc (QF2) ·
                        parse_q · parse_file · parse_dir (recursive discovery,
                        `doc:` Roster branch)
    src/body.py         inline renderer · comments parse/render · ![[embed]] hook
    src/page_question.py  render_question(q, prv, nxt)
    src/page_stage.py   QF1 embeds (EMBED regex, _section, setext support) +
                        QF2 render_doc_slide
    src/page_board.py   render() cover+index+assembly · TPL · scrub_cjk_comments ·
                        to_json
    serve.py            live layer, port 5599 (comment write-back, chat, terminal);
                        imports QNAME, q_files, vet_qpath from src.common
    watch.py            auto-rebuild
    assets/board.css, assets/board.js   inlined at build time
    SKILL.md            version 0.12.0 (a CONCURRENT session bumped it while
                        building the CMS board 01-cmsdata-260724; re-read SKILL.md
                        and CHANGELOG.md before bumping again)
    ref/board-form.md   the board grammar spec
    ref/writing-rules.md  cold-read rules

Board-skill's OWN board (dogfood, flat):
  Tools/plugins/haipipe-toolkit/skills/0_utils/diagram/01-boardform-260722/
    QA1..QF2 faces · board.md · board.html
    QF1-embed.md is 🟡 with "paper-side handshake" open: the S-face design
    SUPERSEDES that handshake item (see section 8, bookkeeping).

Paper skill (the other half of the handshake):
  Tools/plugins/haipipe-toolkit/skills/paper/1-lifecycle/haipipe-paper-stage/
    SKILL.md
    stages/index.yml            one row per stage (key, order, dir, triggers)
    stages/<dir>/stage.md       machine-readable CONTRACT (yaml frontmatter:
                                artifact, log, sections, formatting, q_id_pattern,
                                done_criteria, gates, probe_depth) + craft prose
    stages/<dir>/template.md    the skeleton DRAFT copies from
    dirs: 0-seed 1a-resource 1b-claims 2a-venue 2b-pitch 3-narrative 4-display
          5-section-edit

The live paper (the pilot target):
  examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/
    0-lifecycle/                THE BOARD FOLDER (board.md + board.html at top)
      board.md                  Roster today: QA1 + 14 ruling Q faces + 9 `doc:`
                                lines (stage docs rendered raw, QF2)
      QA1-frontier.md           paper-level ruling (frontier contradiction)
      0-seed/0-seed.md          + _LOG_0-seed.md (+ _LOG_0-seed.archive.md)
      1a-resource/1a-resource.md, 1b-claims/1b-claims.md, 2a-venue/2a-venue.md,
      2b-pitch/ (PITCH_LOG.md, README.md; artifact is .tex),
      3-narrative/ (README.md), 4-display/4-display.md + _DISPLAY_REQUEST.md,
      5-section-edit/z-structure/z-structure.md + per-unit folders
      4-display/QD2..QD8, 5-section-edit/<unit>/QE2..QE7   the 14 ruling faces
    ../STATUS.md ../_TODO.md    paper-level state (QA1's sources)

Live server: `python3 <board-skill>/serve.py --root <Physician-SPACE repo root>
--port 5599 --daemon <log>`; view at
http://127.0.0.1:5599/examples/.../0-lifecycle/board.html
NEVER `open board.html` or file:// (breaks fetch, and on Remote-SSH there is no
display); always the http URL.


## 3 · What is already built and working (do not redo)

- QC3 folder questions: `Q*.md` discovered at ANY depth under the board folder
  (rglob in src/common.py q_files(), skipping path segments starting with `_` or
  `.` and `fig/`). Roster lists bare filenames. Comment write-back carries the
  board-relative posix path (vet_qpath). Verified live on nested faces (QD2 etc.).
- QB5 src split: build.py is a thin entry; regression gate was byte-identical
  rebuild of the flat dogfood board (one real bug found and fixed that way: the
  state pill was clobbered by the comments label; fix is `cm_lab` in
  page_question.py).
- QF1 embeds: `![[path]]` and `![[path#Section]]` render at build time, atx AND
  setext headings both supported (page_stage.py _section/_is_setext_head).
- QF2 doc slides: `doc: <path> <path>` Roster lines render source files raw; no
  state, no checklist, excluded from the settled count; 📄 rows in the index.
- The MISQ board is live with 15 Q faces (QA1 + QD2..QD8 + QE2..QE7) and 9 doc
  slides; serve.py write-back onto nested faces confirmed over HTTP.
- ALIAS already accepts the new section names (src/common.py):
  "Done when" resolves from "Items to Finish"; "Now" resolves from "Where we are".
  So checklist fraction (frac_done in page_board.py) works with `## Items to
  Finish` OUT OF THE BOX. Do not rename sections in code; use sec() everywhere.

State glyphs (src/common.py ST): ✅ done/SETTLED · 🟡 wip/PARTIAL · 🔴 todo/OPEN ·
⏸️ hold/ON HOLD. stinfo() shows any prose after the glyph as the pill label.


## 4 · THE SETTLED DESIGN: S-faces

An S-face is a stage file written in board grammar. It REPLACES the old stage doc
as the artifact BOTH skills use. It is a sibling of the Q-face template with two
changes: no `## Question` (a stage is not a question); instead a `Topic:` meta line
plus a `## Content` section holding the stage's substance as subsections.

### 4.1 Naming

RECOMMENDED (not yet confirmed by JL, see open item 9a): `S<order>-<dir-suffix>.md`
using the paper's own stage orders from stages/index.yml, living inside the stage
folder:

```
0-seed/S0-seed.md            2a-venue/S2a-venue.md      4-display/S4-display.md
1a-resource/S1a-resource.md  2b-pitch/S2b-pitch.md      5-section-edit/ (per unit,
1b-claims/S1b-claims.md      3-narrative/S3-narrative.md  LATER, see 9c)
```

JL's first sketch was `SA0-seed.md`, `SA1-resource.md`. The recommendation to JL
was: use the paper's existing stage letters (0, 1a, 1b, 2a, 2b, 3, 4, 5) rather
than inventing a new sequence, because (a) those are the original terms everyone
greps, (b) `SA`/`SB` would shadow the board's Q-group letters (QA, QB, ...).
GET JL'S ONE-WORD CONFIRM AT PILOT REVIEW; the pilot only creates ONE file so a
rename is cheap.

### 4.2 The S-face skeleton

```
# S0 · 0-seed · <working title of the paper>
state: 🟡 REVISE complete, awaiting CHECK
owner: <who holds the pen; usually CC with JL at the gate>
Topic: <one line: what this stage exists to establish, e.g. the seed contract's
       one_line "Why might this paper exist?">

## Content
### Seed Question
<the old section's prose, verbatim, one sentence per line>
### Motivations
...
### Landscape
...  (inline `> CHECK:` blocks STAY here, anchored where they were)
### Tentative Claim Shape
...

## Items to Finish
- [ ] <open item, one line, traceable: cite the Q id or the CHECK's first line>
- [ ] ...

## Where we are
<the Status story: one line per FIXED thing; record lines, never pipe tables>

## Q-consumer
## Q-Seed-1 · <title>          <-- kept INTACT, the paper skill's probe ledger
**Description:** ...
**Reason:** ...
**Probe:** -> 1-probes/...
**Answer:** ...

## Comments
- [ ] **JL**: ...
```

### 4.3 The routing rules (old stage doc -> S-face), settled with JL

```
old stage doc element                        -> S-face destination
──────────────────────────────────────────────────────────────────────────
Status: <prose>  (line 5)                    -> state: <glyph> <same prose kept
                                                verbatim as the pill label>
title (setext ====)                          -> # S<order> · <dir> · <title>
content sections (everything BEFORE           -> ## Content, each old setext
  Q-consumer: Seed Question, Motivations,       section becomes one ###
  Landscape, Tentative Claim Shape, ...)        subsection; prose NOT rewritten,
                                                only re-homed (JL: "each
                                                paragraph to be each subsection")
Q-consumer section + ## Q-<Stage>-<n> blocks -> ## Q-consumer, INTACT, verbatim
Q block with **Answer:** FILLED              -> one line in ## Where we are
                                                (id + verdict opening sentence)
Q block with **Answer:** empty or            -> one unticked box in
  `deferred -> <STAGE>`                         ## Items to Finish (cite the id)
> CHECK: ... (open, "Judgment needed")       -> STAYS inline in ## Content where
                                                anchored; ALSO one unticked box in
                                                ## Items to Finish (label = the
                                                block's first line)
> CHECK [RESOLVED <date> ...]                -> stays inline; ALSO one line in
                                                ## Where we are (the headline)
_LOG_<stage>.md                              -> NOT read, NOT rendered, NOT moved.
                                                JL: "we might don't use the _LOG".
                                                It stays in the folder for the
                                                paper skill's history.
```

state glyph mapping from the old Status prose (fallback 🟡; ALWAYS keep the
original prose after the glyph so the pill can never silently lie):

```
contains DRAFT (and no later phase)             -> 🔴
contains PROBE / REVISE / pre-REVISE /          -> 🟡
  awaiting CHECK / awaiting GATE
gate confirmed / pinned (e.g. 2a-venue          -> ✅
  "Status: pinned (MISQ, 2026)")
parked / on hold                                -> ⏸️
```

Real 0-seed values for the pilot (verified against the live file 2026-07-25):
- state: 🟡 REVISE complete, awaiting CHECK
- Where we are gets: Q-Seed-1 UNOCCUPIED at medium-high confidence (raised by the
  2026-07-20 depth-1 enrich); Q-Seed-2 EXISTS and physician-linkable via
  `prscrbr_id` on the Part D table; Q-Seed-3 precedent exists (Wang, Liu, Zhang &
  Liu 2021, npj Primary Care Respiratory Medicine); plus the RESOLVED CHECK
  (Bandi, Dey & Rao 2024 read and classified non-occupying; sweep extended).
- Items to Finish gets: 3 owed HUMAN-ONLY bibtex keys (Kristensen 2022, Hrazdil
  2020, Wang 2021: zero hits in 0-Personality-Opioid-MISQ2026.bib; agents never
  write bibtex); the em-dash sweep (16 in prose, checks.sh absent); the direct
  Scopus/WoS query + gray-lit sweep (the last step medium-high -> high).

### 4.4 Migration mechanics ("put the current version aside")

- Move the old doc to `<stage>/_archive/<stage>.md` (underscore segment: the board
  discovery, watch.py, and embeds all already skip it). NOTHING is deleted.
- `_LOG_*.md` files are NOT touched, NOT moved.
- The new S-face is born by RE-HOMING the old file's real content under the new
  headings. Do not rewrite prose, do not drop any `> CHECK:` or `> JL:` line
  (deleting a `> JL:` line is a standing hard NO), do not "improve" wording.
- board.md Roster: the group's `doc:` line for that stage is REPLACED by the bare
  S-face filename (discovery finds it nested, same as Q-faces). Example, QB group
  after the pilot:
  ```
  ### QB · 0-seed · 1a-resource · 1b-claims
  S0-seed.md
  doc: 1a-resource/1a-resource.md 1a-resource/_LOG_1a-resource.md
  doc: 1b-claims/1b-claims.md 1b-claims/_LOG_1b-claims.md
  ```
  (the other two convert only after JL approves the pilot).


## 5 · Board-skill code changes (small; the design's whole point)

File by file. Everything stays inside src/ plus serve.py's shared imports.

- src/common.py
  · QNAME today: `^Q[A-Za-z0-9]*[-_A-Za-z0-9]*\.md$`. Extend to accept S-faces
    (e.g. `^[QS][A-Za-z0-9]*[-_A-Za-z0-9]*\.md$`) OR add a parallel SNAME; pick
    ONE and keep vet_qpath/serve.py consistent. Extending QNAME is simpler and
    makes comment write-back to S-faces work with zero serve.py changes.
  · q_files(): rglob currently only `Q*.md`; must also yield `S*.md` (same
    segment filter). Watch for collisions: no existing file in either live board
    starts with `S` (verified for 01-boardform-260722 and the MISQ 0-lifecycle;
    re-verify with a glob before shipping, and check 01-cmsdata-260724 too, the
    CMS board another session built).
- src/parse.py
  · parse_q() already parses the S-face body correctly (generic section splitter;
    state:/owner: lines; ALIAS covers Items to Finish / Where we are). Verify id
    derivation from the filename stem gives `S0`, `S1a` etc. and that anchors
    (#S0? or #0-seed?) look right; doc slides currently use the parent folder
    name as id (`#0-seed`). DECIDE: keep filename-derived id `S0` (consistent
    with Q-faces) and let the title carry `0-seed`. Recommended: filename-derived.
  · parse_dir(): Roster branch must accept bare S-face names exactly like Q names
    (the `disk` dict is keyed by basename; adding S*.md to q_files may be all it
    takes). The `doc:` branch stays as is (QF2 remains for raw dumps).
- src/page_question.py
  · render_question(): add two small things for S-faces: render the `Topic:` meta
    line (next to owner/method), and nothing else; `## Content` renders through
    the existing generic body() with ### subheads already styled. If Q-faces and
    S-faces need visual distinction, a small `stage` chip near the id is enough.
- src/page_board.py
  · Settled count: OPEN ITEM 9b. Until JL rules, EXCLUDE S-faces from the
    `{done}/{n} settled` bar (a stage settles at its DPRC gate, not by board
    ruling) but give them normal state-glyph index rows with the completion fill
    (frac_done works via ALIAS). Implementation: mark parsed S-faces with
    kind="stage" and filter like kind=="doc" in the settled math only.
  · to_json(): carry kind="stage" through.
- serve.py: nothing, IF QNAME was extended (target() and add/archive flow through
  vet_qpath). Smoke-test a comment write onto S0-seed.md over HTTP anyway.
- watch.py: nothing (already rglobs *.md with the segment filter).

Regression gates (run ALL before showing JL):
1. Rebuild the flat dogfood board 01-boardform-260722: byte-identical to before
   your change (it contains no S-faces, so ANY diff is a bug).
2. Rebuild the CMS board 01-cmsdata-260724 if present: same byte-identical rule.
3. Rebuild the MISQ 0-lifecycle board: 15 Q faces + 8 doc slides + 1 S-face
   (pilot), 0 roster warnings, no-JS assertion passes (build.py asserts it).
4. `build.py <dir> --json` still emits and the new kind field appears.


## 6 · Paper-skill changes (haipipe-paper-stage/stages/), AFTER the pilot is liked

The contracts must make the S-face the official artifact, or the next DPRC run
will regenerate the old shape. Per stage directory:

- stage.md frontmatter:
  · artifact: -> `0-lifecycle/<dir>/S<order>-<dir-suffix>.md`
  · sections: -> the S-face list: Content (with the stage's old sections as
    NAMED ### subsections; keep their names, e.g. "Seed Question"), Items to
    Finish, Where we are, Q-consumer, Comments
  · formatting: title_rule/section_rule change from setext to atx (`#`/`##`/`###`);
    KEEP "one sentence per line"; KEEP the q_id_pattern `## Q-<Stage>-<n> · <title>`
    (unchanged, now nested under ## Q-consumer)
  · done_criteria: ADD two lines: "Items to Finish and Where we are are CURRENT at
    every phase exit (an answered Q-consumer moves its line from Items to Where;
    an open > CHECK: has a mirrored box)" and "state: glyph matches the gate
    ledger". This is the price of JL's design: those sections are now MAINTAINED,
    not derived, and CHECK is the drift gate.
- template.md: rewritten to the S-face skeleton (section 4.2), with the stage's
  own content subsections. The RULE-comment style (follow then delete) stays.
- The two templates that today have NO Status/state line at all (3-narrative,
  5-section-edit) get the `state:` line with the rest.
- index.yml: UNTOUCHED (paths in stage.md are what changes).
- SKILL.md of haipipe-paper-stage: a short "board handshake" paragraph naming the
  four anchors the board reads (state: line, ## Items to Finish, ## Where we are,
  ## Q-consumer with **Answer:** filled-vs-empty) and the phase-exit duty.

NOTE the interlock: existing stage docs at OTHER papers keep the old shape until
someone migrates them; the board still renders those via `doc:` lines. Nothing
forces a big-bang migration. The contract change only governs NEW/NEXT DPRC runs.


## 7 · Execution order (pilot first, roll later)

```
[1/6] board skill: QNAME + q_files + parse + render tweaks (section 5)
[2/6] regression gates 1-2 (byte-identical flat boards)         MUST PASS
[3/6] pilot file: 0-seed/S0-seed.md written from the real 0-seed.md by the
      routing rules (4.3); old file -> 0-seed/_archive/0-seed.md; board.md QB
      group line swapped; rebuild; serve already runs on 5599
[4/6] JL eyeballs http://127.0.0.1:5599/examples/Project-Personality-OpioidRx/
      papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle/board.html#S0
      (or #0-seed if id ruling says folder name) NEXT TO the old dump look.
      Get rulings on open items 9a/9b at the same sitting.        STOP POINT
[5/6] roll: remaining stage docs -> S-faces (1a, 1b, 2a; decide 2b/3 which file
      is the artifact, see 9d; 4-display; z-structure + units per 9c); board.md
      doc: lines replaced group by group; comment smoke test on one S-face
[6/6] paper-skill contracts (section 6) + bookkeeping (section 8)
```

Fresh-subagent validation (required by the repo's CLAUDE.md): after [5/6], have a
clean-context subagent open the board folder with only the skills' docs and ask it
to (a) read the board, (b) add a comment to an S-face, (c) run one DPRC phase
against the new contract on a scratch copy; watch whether it follows the S-face
format without the development discussion in its context. Also run a zero-background
cold read per ref/writing-rules.md and fix findings.


## 8 · Bookkeeping (ONCE, at the very end; one tag per body of work)

- Dogfood board 01-boardform-260722: add a new face for the S-face design (next
  free id in the QF group, likely QF3-stageface.md) recording JL's rulings quoted
  in section 1 and the routing table; mark QF1-embed.md's open "paper-side
  handshake" item as superseded-by-QF3 (do NOT delete QF1's text); rebuild.
- haipipe-board: SKILL.md 🗂 section + ref/board-form.md get the S-face grammar;
  CHANGELOG.md one entry; ONE version bump (from whatever is current when you
  finish; it was 0.12.0 at handoff time because a concurrent session shipped the
  CMS-board work; re-read CHANGELOG first).
- haipipe-paper-stage: its own CHANGELOG/version if it has one (check SKILL.md).
- Memory file `project-misq-lifecycle-board.md` (auto-memory dir): update the
  "open:" line to point at the S-face pilot state.
- NO COMMITS in ANY repo without JL's explicit scoped go. Three repos carry
  unrelated uncommitted work. NEVER `git add -A` at the Tools root (42 emptied
  submodules show as staged deletions there; JL said ignore them).


## 9 · Open items that need JL (ask at the [4/6] stop point, not before)

a. NAMING: `S0-seed.md / S1a-resource.md` (recommended, paper's own stage letters)
   vs JL's sketched `SA0-seed.md / SA1-resource.md`. One-word confirm.
b. SETTLED COUNT: do S-faces join the `N/N settled` bar? Recommendation: no
   (stages settle at their DPRC gate; the bar stays the rulings' bar), show state
   glyph + fill in the index only.
c. 5-section-edit SCOPE: one S-face for z-structure only, or one per unit folder
   (2-literature, 3-theory, 4-llmtrait, 6-results, 7-discussion, 9-appendix)?
   Units already carry ruling faces QE2..QE7; per-unit S-faces would sit beside
   them. Defer until the single-stage pattern is liked.
d. NON-MD STAGES: 2b-pitch's artifact is .tex (PITCH_LOG.md + README.md are the
   md surface) and 3-narrative has only README.md. Do they get S-faces authored
   fresh from those sources, or stay as `doc:` slides? Recommendation: S-faces
   authored fresh (they are exactly the stages whose raw dumps read worst), but
   it is JL's call.
e. EXTRA FILES on converted stages (4-display/_DISPLAY_REQUEST.md): keep a `doc:`
   slide, demote to a Links row, or embed `![[...]]` inside the S-face's Content?
   Recommendation: Links row (leanest; JL's standing "cut boilerplate" ruling).

## 10 · House rules that bind ALL of this work (violations got called out before)

- English only in board files, artifacts, and chat replies.
- NO EM-DASHES anywhere in authored text (JL 260724). Use colon, semicolon,
  comma, parens, or a new sentence. Never a blind sed; each one gets its own fix.
- Original terms only: the paper's real ids (D01, DR08, Q-Seed-1, PP01/QX1,
  current_layer, prscrbr_id), real file paths, real section names. No coined
  nicknames; a subagent's coined words get translated back before relaying.
- Record lines, never pipe tables, in hand-edited stage/board markdowns.
- Never delete a `> JL:` line; never delete `> CHECK:` blocks (move them intact).
- Never hand-edit board.html (generated; the no-JS assertion in build.py guards it).
- Never tick an unverified checklist item; states come from the docs' own words.
- CMS data is PHI: `_WorkSpace/1-CMS-Store`, `2-Data-Store`, any `cms_full` stay
  on the secure server; only aggregated regression outputs move. (Not directly
  touched by this work, but the paper folder is adjacent to it.)
- The board pages are viewed via http://127.0.0.1:5599/..., never file://.
- AskUserQuestion modals annoyed JL twice in this thread; prefer plain discussion
  in chat, with options drawn side by side in ascii when there is a fork.
