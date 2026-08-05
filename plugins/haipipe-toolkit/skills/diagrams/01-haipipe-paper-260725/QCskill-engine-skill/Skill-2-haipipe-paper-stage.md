# haipipe-paper-stage · v0.9.1
state: 🟡 PARTIAL · account written; the acceptance test is open in Items
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
What makes a lifecycle stage a repeatable, inspectable unit rather than a loose folder of prose, and which contract decides what that stage may do?

This page examines the one-stage executor: it resolves one declared stage, creates or refreshes that stage's S page, and drives only the phases and gate the contract permits.

## Diagram
<!-- haipipe:skill:tree:start 2f15bb4d02d080dd paper/haipipe-paper-stage -->

**What `haipipe-paper-stage` ships**: every file in the folder, with the one-line purpose each one states for itself.

```
haipipe-paper-stage/
  ref/
    03-paper-lifecycle.md    109 ln  Paper Lifecycle
    04-lifecycle-map.md      158 ln  Paper Lifecycle Map
    08-stage-gate.md         234 ln  Stage Gate Protocol
    09-stage-illuminate.md    69 ln  Illuminate + Elicit Protocol
  stages/
    CONTRACT.md              226 ln  The stage contract form
    index.yml                 37 ln
    section-kinds.yml         90 ln
  CHANGELOG.md               172 ln  haipipe-paper-stage — Changelog
  check-contracts.py         209 ln  Check every stage contract against stages/CONTRACT.md, and against a real paper.
  create-page.py             437 ln  Create one paper lifecycle S page through the Board's shell primitive.
  section-stats.py           302 ln  Measure an S page's prose FORM and print the structure block for `## Diagram`.
  SKILL.md                   261 ln  Skill: haipipe-paper-stage
```

<!-- haipipe:skill:tree:end -->

```
stage key + paper root
         │
         ▼
stages/index.yml ──▶ exactly ONE stages/<key>/stage.md
         │                  contract + craft + declared phases/gates
         ▼
Board identity: board_family + board_unit
         │                  S page if absent; managed contract if stale
         ▼
DRAFT ──▶ PROBE ──▶ REVISE? ──▶ CHECK (the declared human gate)
         │
         └── `requires` / `style-from` / `provides` are explicit Board
             handoffs, never inferred from the order of index rows.
```

## Content
<!-- haipipe:skill:body:start 2f15bb4d02d080dd paper/haipipe-paper-stage -->

**haipipe-paper-stage** · `0.9.1` · last shipped 2026-08-01

- folder   `paper/haipipe-paper-stage/`
- tools    Bash, Read, Write, Edit, Grep, Glob, Skill
- summary  Board-first stage router: unfinished work is expressed as Content-linked Aims with a separate factual row in States per Aim.

### SKILL.md



Skill: haipipe-paper-stage
==========================

The single entry point for every stage of the paper lifecycle.

```text
/haipipe-paper-stage <stage-name> [paper-dir] [phase] [stage-args...]
                     ▲
               always first
```

The per-stage skills are GONE. `/haipipe-paper-seed`, `/haipipe-paper-venue`, and the other six
no longer exist — every stage comes through here, stage key first.


- 1 · Procedure
      **Step 1 — resolve the stage.**
      Read `stages/index.yml`. This is the ONLY file that enumerates all stages, and it is deliberately
      small. Match `$1` against each row's `key`; if `$1` is not a key, match the user's phrasing against
      `triggers`. Ambiguous or absent → list the keys and ask; never guess a stage.
      **Step 2 — load exactly ONE stage.**
      ```text
      migrated: true   -> Read stages/<dir>/stage.md   ← the contract (frontmatter) + craft (body)
      migrated: false  -> Skill("<legacy_skill>", args="<the rest of $ARGUMENTS>") and STOP.
                          Say plainly that the stage has not been cut over yet.
      ```
      ⛔ NEVER read the other stages' `stage.md` files. Loading all eight is a 7.5x context regression
      over the per-stage skills this replaces, and it is the specific failure mode this layout exists to
      avoid. One invocation, one stage file.
      **Step 2a — ensure this stage's Board page exists.**
      The Paper stage is the only public creator for paper lifecycle pages. Resolve the page by the
      selected contract's stable `board_family` + `board_unit`; do not store or guess a literal
      filename. If the page is absent, create its Board shell and stage-specific Content scaffold with:
      ```sh
      python3 create-page.py <stage-key> <paper-root>
      ```
      `create-page.py` selects the stage template, then calls `haipipe-board/cli/stage.py new` for the
      filename, face grammar, listing under Pages, and managed Stage Contract. It does not draft the
      research substance. For a dynamic `runs: per-unit` page, pass the resolved identity and directory
      with `--family`, `--unit`, `--slug`, and `--directory`; Section-edit also requires
      `--section-kind`, which resolves the exact template from the Venue page's `Section Styles`
      record (or its declared generic fallback). `--template` is an explicit repair/testing override,
      not the normal routing path. Do not create a sidecar request or handoff file; unfinished work
      stays in that page's `## Aims`, with its current fact in `## States`.
      **Step 3 — read the loop, once.**
      The declared phase loop, the gates, and the phase-transition contract are NOT restated per stage.
      They live at:
      ```text
      probe/haipipe-probe/SKILL.md          the probe layer + the DRAFT/PROBE phase rules
      ./ref/08-stage-gate.md                the stage gate + Phase Transition Contract
      ```
      **Step 4 — drive the stage's declared phases.**
      Run the phases listed in that stage's `phases:` field, in order, each through its `Skill()`
      dispatch: draft → `haipipe-board-page-draft` (page logic) + the `../workers/` draft leaves ·
      probe → `haipipe-paper-probe` (in `../workers/`) · revise → `haipipe-board-page-revise` + the
      revise leaves · check → `haipipe-board-page-check` + the check leaves. A phase executed inline did
      not happen.
      - `phases:` is a LIST, not a type. venue declares `[draft, probe, check]` — it raises real
        `Q-Venue-<n>` entries that PROBE answers, but produces a contract rather than prose, so it has
        no REVISE. Run what the stage declares; never pad a list to four.
      - INVARIANT: `phases` always ends with `check`. That is the human gate.
      - `runs: per-unit` means the phase list runs once PER UNIT. Use it when units have independent
        human gates. Section Edit already implements this grain; Display qualifies by the same rule,
        but its current central-artifact contract remains `runs: once` until the tracked migration is
        complete. A stage whose output gates as one thing remains `runs: once`.
      - `commissions:` names worker skills this stage hands units to (display → the four renderers).
        Those workers stay independently registered and are invoked by name.
      - `gates:` declares this stage's HUMAN stops, the same way `phases:` declares its phases. The
        default is `[check]` — ONE gate, at the end. DRAFT, PROBE and REVISE run unattended.
        Never open a gate a stage did not declare, and never skip one it did.
      **Step 4a — synchronize the lifecycle board mapping.**
      Each stage contract declares two stable identity fields:
      ```text
      board_family   stable ownership group: Seed, Work, Venue, Display, Main, or Appendix
      board_unit     the page's unit inside that family
      ```
      Board tooling owns the filename and resolves it from that identity. These fields do not change
      stage execution order and do not replace `artifact:`. The actual run still follows
      `stages/index.yml`, `upstream`, and `downstream`; for example Narrative is followed by the
      independent Display family before manuscript sections consume its assets. After any phase changes
      the artifact, sync the resolved S face in the same turn: update its page-level
      `state:`, `## Aims`, `## States`, and `## Log`, then rebuild the board. When the S face embeds the
      artifact, do not copy its Content. Submission and revision are downstream board rounds, not extra
      router stages here.
      The mapped S face may declare `requires:`, `style-from:`, and `provides:`; all three are optional.
      When present, they are board contracts, not router edges: `requires` is the sole authoritative
      dependency declaration and names upstream outputs this page must honor,
      `style-from` names the venue or project writing contract, and `provides` states the compact
      downstream handoff. A stage contract may carry `read_order:` as optional craft guidance for the
      sequence in which DRAFT opens material; it is not a second dependency graph. Create or refresh the
      managed `## Stage Contract` block with
      `haipipe-board/cli/stage.py`; never copy whole upstream Content, and never let `build.py` edit
      Markdown. If the board reports a stale contract after an upstream change, run explicit
      `stage.py sync` before CHECK.
      **Step 4b — the PROBE ceiling.**
      `probe_depth:` is what makes a single CHECK gate safe: PROBE may only dispatch work whose cost
      sits at or below the ceiling, so an unattended run cannot spend.
      ```text
      depth  bank:    what it takes                        cost
        0    reuse    results already answer it            free — nothing runs
        1    run      old script, new config               costs
        2    code     must write new code first            costs
        3    new      open a new task-folder               costs most
      ```
      The ladder is the bank's own (`task/haipipe-task/fn/qa.md`, "How deep"), and the consumer's
      `bank:` verdict maps onto it 1:1. The rule is one line:
      ```text
      dispatch when depth(bank) <= probe_depth, else DEFER the entry
      ```
      Default is `0`, so a plain run HARVESTS and never orders. Raise it for one invocation:
      ```text
      /haipipe-paper-stage <stage> <paper> probe             ceiling 0 — harvest only, free
      /haipipe-paper-stage <stage> <paper> probe --depth 1   also allow reruns of existing code
      /haipipe-paper-stage <stage> <paper> probe --depth 3   unsealed — may open new task-folders
      ```
      ⚠️ `--depth` AUTHORIZES SPEND. Passing it is the human act that a removed DRAFT gate used to be.
      Report what each raise actually dispatched; never raise it on your own initiative.
      ⚠️ Depth is a proxy for KIND of work, not AMOUNT: a depth-1 rerun over a large cohort can cost
      far more than a depth-2 script that counts rows.
      **Step 5 — verify before CHECK.**
      Run the probe-card checker scoped to THIS stage key. Locate it layout-agnostically (installed
      skills flatten the tree) and filter on the paper family — two files of that name exist on disk
      with different invariants:
      ```sh
      # The RELATIVE path resolves even from an installed symlink, because the link's target
      # sits in the real tree — prefer it. The find is the fallback, and it needs -L: installed
      # skills are symlinks and a find without -L descends into nothing and returns zero hits.
      CHK="../workers/haipipe-paper-probe/check-probe-cards.sh"
      [ -f "$CHK" ] || CHK=$(find -L ~/.claude/skills ./.claude/skills "${CLAUDE_PLUGIN_ROOT:-/nonexistent}" -maxdepth 4 \
                               -path '*haipipe-paper-probe/check-probe-cards.sh' 2>/dev/null | head -1)
      [ -n "$CHK" ] && [ -f "$CHK" ] || { echo 'FAIL: paper probe checker not found'; exit 1; }
      sh "$CHK" <paper_root> --stage <stage-key>
      ```
      `--stage <key>` IS PART OF THE COMMAND. Without it the checker globs the whole paper and this
      stage's gate inherits every other stage's open work.
      PASS 1's vacuous-green test works for every stage key as of 2026-07-20. It fires when NO entry
      serves this stage while the stage doc still has unanswered Q-consumer blocks — the case where a
      green would mean "nothing was ever opened". Before that fix it was keyed on "any probe file
      exists", so on a mature paper it was unreachable for every stage, resource included.

- 2 · Rebuild the Board after every write
      Ruled 2026-07-26 (design board `QA1`, `QA4`). `/haipipe-paper` is the single
      thing a human types, and `enter` leaves them LOOKING at `⑧` in a browser. That
      makes a stale `board.html` a defect, not an inconvenience: the human is reading
      a picture of a paper that no longer exists.
      ```text
         a stage run writes S-<Family>-<n>-<slug>.md
              │
              ├─ DRAFT   → ## Content + Content-linked Q-consumer records in ## Aims
              ├─ PROBE   → the entry pointers
              ├─ REVISE  → the same page + %% why-comments, when declared
              ├─ CHECK   → page-level state: ✅   (a HUMAN writes this)
              │
              └─ then ALWAYS: call ③ haipipe-board build on 0-lifecycle/
                              and put the deep link in the closing block
      ```
      **Two directions, both mandatory.**
      ```text
      AFTER a write   rebuild, or the browser shows the previous version
      BEFORE a read   RE-READ the page off disk. A human comment or a `>` lane
                      may have arrived through serve.py since this session last
                      looked, so ⑧'s markdown can change underneath ①. Never
                      cache a page across a phase boundary.
      ```
      The second is the one that keeps the two-channel design honest: `③` writes `⑧`
      from a human's click, so `①` may never assume it wrote the page last.
      Calling is not owning. `③` owns the build, the filename rule and the html;
      this skill calls it and renders nothing.

- 3 · Layout
      ```text
      haipipe-paper-stage/
      ├── SKILL.md                   this file — the only registered skill here
      ├── create-page.py             Paper's public creator; composes Board shell + stage scaffold
      └── stages/
          ├── index.yml              the index (small, always read)
          └── <order>-<key>/         one folder per stage
              ├── stage.md           frontmatter = CONTRACT · body = CRAFT
              │                      (no `name:` field — this is DATA, not a skill)
              ├── template.md        the artifact skeleton + its inline <!-- RULE --> comments
              └── …                  that stage's own support files. They are NOT uniform:
                                     2b-pitch has readability.md · 4-display has checklist.md
                                     and figure-logic.md · 5-section-edit has NEITHER — its
                                     template is its own rulebook and its section norms come
                                     from the venue packs. Never assume a file exists because
                                     another stage has one.
      ```
      Adding a stage = one folder + one row in `index.yml`. No new skill, no version bump, no
      `description` edit.

- 4 · Status — all 8 stages live, Board-first creation ready
      ```text
      ✅ seed · resource · claims · venue · pitch · narrative · display · section-edit
      ```
      The 8 legacy stage skills are GONE — unregistered and retired to `../_old/`, which is treated as
      DELETED, not as a rollback. Everything a live path needs was salvaged out of it first:
      every `*-template.md`, `pitch-readability.md`, `figure-logic.md`, `CHECKLIST.md`,
      the shared `display-unit-output-contract.md`.
      Nothing under `../_old/` may be referenced by a live file.
      Wired to this skill, verified 2026-07-20 (hub rows repointed 2026-08-05, thin-paper phase 1):
      ```text
      haipipe-board-page-draft   DRAFT page logic (the retired haipipe-paper-draft's Step 1 rule
                                 lives on here: read stages/<dir>/stage.md + template.md)
      haipipe-paper-lifecycle    every stage key -> Skill("haipipe-paper-stage", args="<key> …")
      haipipe-paper              same rule stated in its dispatch block
      haipipe-board-page-check   CHECK page logic (gate table keyed on stage NAME, not skill name)
      ../workers/                the flat LaTeX-side phase leaves the stage.md declarations dispatch
      4 display renderers        STAY registered; the shared contract moved to ../../4-display/ref/
                                 and all 12 relative paths were rewritten
      ```
      The stage system has been driven against a real MISQ paper. Known business
      blockers remain declared on their S pages; they are not hidden by this router.
### The other files

10 files besides `SKILL.md` and `CHANGELOG.md`, each with the purpose it states about itself. They are described here, not reproduced: the folder is the copy.

```
check-contracts.py             209 ln  Check every stage contract against stages/CONTRACT.md, and against a real paper.
create-page.py                 437 ln  Create one paper lifecycle S page through the Board's shell primitive.
ref/03-paper-lifecycle.md      109 ln  Paper Lifecycle
ref/04-lifecycle-map.md        158 ln  Paper Lifecycle Map
ref/08-stage-gate.md           234 ln  Stage Gate Protocol
ref/09-stage-illuminate.md      69 ln  Illuminate + Elicit Protocol
section-stats.py               302 ln  Measure an S page's prose FORM and print the structure block for `## Diagram`.
stages/CONTRACT.md             226 ln  The stage contract form
stages/index.yml                37 ln
stages/section-kinds.yml        90 ln
```

<!-- haipipe:skill:body:end -->

## Aims
- [x] 📜 Make the contract the source of stage behavior
      The stage key is resolved in `../../paper/haipipe-paper-stage/stages/index.yml`; the executor reads only that
      stage's `stage.md`, never all eight contracts and never an invented phase.
- [x] 🧩 Make S-page identity explicit
      `board_family` plus `board_unit` identifies the Board page.  Board owns
      its filename and shell; the stage supplies the selected template and
      stage-specific Content scaffold.
- [x] 🚦 Keep phase and spend boundaries visible
      `phases:` dictates the sequence, `gates:` dictates human stops, and
      `probe_depth:` limits unattended evidence work.  A caller alone may raise
      the ceiling with `--depth`.
- [ ] 🧪 Exercise a dynamic section-edit page
      Verify that a per-unit section resolves its venue section style, identity,
      inherited contract, and CHECK scope without leaking another section's
      state into the run.

## States
The stage page now makes its three controls legible: one selected contract, one explicit S-page identity, and one declared phase-and-gate path.
The dynamic per-section path is the remaining acceptance case to run through this page.

## Log
260727 · Audited against `board.md`'s decision-only rule, which says `state:` is about the DECISION and that implementation does not gate this board. Every open item here is implementation or a test, not an undecided question, so the page was reporting itself as open because code was missing. Flipped with no ruling made.
260727 1440 · Created the stage-executor page from `paper/haipipe-paper-stage/`.
It records contract selection, Board identity, and phase/gate ownership as separate controls.

<!-- haipipe:skill:log:start 2f15bb4d02d080dd paper/haipipe-paper-stage -->

Converted from the skill's own `CHANGELOG.md`: 16 releases.

260801 · `0.9.1` · Board section labels are paired plurals
      - Synchronizes stage status rows under canonical `## States`, paired with
        `## Aims`; singular State remains the name of one record.
      - Migrates every active stage contract and Q-consumer template to canonical Aim
        records (`P<n>`) with a Done-when condition, while retaining old headings as
        read-only parser aliases.
      - Updates `create-page.py` to replace the canonical Board shell sections and
        emit one matching State row for each generated Aim; `section-stats.py` now
        stops Content at either canonical headings or legacy aliases.
260801 · `0.9.0` · Stage work uses Aims and State
      - Replaced active `Items to Finish` and `Where we are` instructions with
        Content-linked Aims and one factual State row per Aim.
      - Kept the page-level CHECK gate distinct from individual Aim status and added
        Log synchronization for transitions.
260727 · `0.8.8` · Display review blocks are a Board projection
      - The Display template now says plainly that Current Float, live artifact, Display Versions,
        current folder, and explanation are injected in generated `board.html` for allocated units.
        They are not headings an author copies into every source page.
      - An unallocated Display request has no `unit:` record and therefore writes the same five
        empty-state subsections itself. This makes both the source and validation surface unambiguous.
260727 · `0.8.7` · Display questions, work, and editable sources are distinct
      - Display's Board-native `## Items to Finish` now makes the Q-consumer distinction explicit:
        `Q-Display<unit>-<n>` is an unresolved, stake-bearing question with Description, Reason, Probe,
        and Answer; a known edit/render/promote action remains an ordinary work item. Per-unit ids avoid
        collisions between independently gated display pages.
      - A PPTX is an optional editable source in `recipe/`, with `export.md` recording its export into a
        PDF/SVG asset. The unit still compiles the asset through `float.tex` into `preview.pdf`; this is
        the one reviewable paper artifact. Legacy PPTX files remain historical editable sources until a
        deliberate migration.
      - The state template now matches the Board contract: its first emoji carries the machine state and
        a short readable detail may follow.
260727 · `0.8.6` · section-edit's closed_when matches QC0's S4
      - `closed_when` said the agent places the real thing "retiring the placeholder and its bracket
        together", which is right for a citation and wrong for a value. Split: a CITATION retires
        both, a VALUE retires only the placeholder and gains a `> Value:` lane.
      - `prose_rule` now names the FINISHED form, not only the two unfinished ones, and a new
        `done_criteria` line fails a placed number carrying neither bracket nor lane — the state that
        looks finished and reports nothing.
260727 · `0.8.5` · section-edit's Q-consumer id carries its unit
      - **`q_id_pattern` is now `Q-Sec<unit><Slug>-<n>`, not `Q-Section-<n>` (JL ruling).** This
        stage declares `runs: per-unit`, so the unit IS the stage instance and its token must say
        which unit: `S-Main-0-abstract` -> `Q-Sec0Abstract-<n>`, `S-Main-6-results` ->
        `Q-Sec6Results-<n>`, `S-Appendix-A-prompts` -> `Q-SecAPrompts-<n>`. Both halves are read
        off the S page filename, so an id cannot drift from the page that owns it.
      - No change to `/haipipe-probe`: `Q-<Stage>-<n>` was always the contract, and it already
        states that consumer ids never collide. section-edit was the one stage breaking it.
      - Why it is not cosmetic: the resolver takes the FURTHEST-ALONG match among entries claiming
        an id, so a shared id let a DEFERRED question inherit an ANSWERED one's state. On the MISQ
        paper `Q-Section-1` named three different questions on three pages, and nine chips read
        `ok`/`ready` against pages whose own records read DEFERRED or no-live-probe.
      - `template.md` and `TEMPLATES.md` updated; `TEMPLATES.md`'s "section-edit id scoping" open
        question is closed.
260727 · `0.8.4` · Display Intake and wrapper handoff
      - The Display-stage template now makes the Paper-owned `### Wrapper` explicit: literal caption, stable label, and placement.
      - A renderer may serialize only those already-approved fields; it cannot invent or rewrite paper-facing semantics.
      - Numeric units bind a small provenance-traceable Intake snapshot before rendering, while legacy units remain unmigrated unless deliberately converted.
260726 · `0.8.3` · Q-consumer gets a Board-native home
      - `create-page.py` now treats `Q-consumer` as a logical stage division and
        materializes it as recognizable checklist records in `## Items to Finish`.
      - It no longer emits Q-consumer under `## Content`.
      - Full Board templates such as Display preserve their own Content divisions and
        Items scaffold; Setext stage templates receive the standard Q record.
      - Narrative and Section-edit ATX headings are now recovered as Content divisions;
        Display's literal `Q-Display-<n>` placeholder is recognized without an invalid
        word-boundary assumption.
      - Dynamic Section-edit creation now resolves `--section-kind` against the Venue
        page's `Section Styles` record and honors its generic fallback; the public creator
        no longer treats `<resolved per (venue, section_kind)>` as a filename.
      - Fixed three end-to-end creation defects: new Resource pages use the declared
        `board_slug: resources`, venue-pack paths render safely outside the stage folder,
        and full-Board templates instantiate `<n>` in their own Items scaffold.
      - Setext logical divisions and pre-Q-consumer ATX content divisions are now merged
        instead of treated as alternatives, so venue-specific section templates retain
        both their structure overview and their paragraph-block scaffold.
      - Stage contracts and all venue section templates now use the same checklist
        anatomy with Description, Reason, Probe, and Answer.
      - All venue templates now carry the same no-DRAFT-gate sequence:
        DRAFT raises, PROBE fills, REVISE weaves, and CHECK presents.
260726 · `0.8.2` · phase and gate declarations win
      - Run exactly the stage's `phases:` list; an omitted phase is not a runtime skip.
      - All current stages use `gates: [check]`; `--depth` is the independent spend
        authorization.
      - Phase provenance and approvals live in the owning S page's `## Log`.
260726 · `0.8.1` · the venue pin reads the `state:` line, not an invented frontmatter key
      Found by running the skill against `Paper-Personality2Opioid-MISQ2026` rather than by reading it.
      Yesterday's `STATUS.md` retirement moved the venue pin to "`S-Venue-0-venue.md` frontmatter, `venue:`". That field does not parse. `haipipe-board`'s face grammar is a CLOSED whitelist (`src/parse.py:145`): `state|owner|method|session|requires|style-from|provides|contract-source-hash`. A `venue:` key is invisible to the board, so the frontier predicate failed on the only real paper, and the fix was never going to be "add the key" — the whitelist is `haipipe-board`'s, ruled on its own board.
      The pin needed no new field. It was already on the page's own `state:` line: `state: ✅ PINNED · MISQ 2026`. Corrected in 12 places across the stage contract, the console, the router, the two refs, the anatomy spec and `restructure`.
      Recorded on design-board face `QA4` as the third cross-package gap of the day, with the rule it produced: **`haipipe-paper` may not invent a face-grammar key.** It uses a key that already parses, or it goes to the board's own board and asks.
260726 · `0.8.0` · rebuild the board after every write, re-read before every read
      Implements the single-door ruling (design board `skills/diagrams/01-haipipe-paper-260725`, faces `QA1` + `QA4`, JL 2026-07-26): **`/haipipe-paper` is the single thing a human types**, and it CALLS `haipipe-board` to build and open the paper's `0-lifecycle/`. `haipipe-board` remains its own door for boards that are not inside a paper. Calling is not owning: `haipipe-board` still owns the format, the build, the filename rule, the html and the write-back.
      - **New `## Rebuild the Board after every write`.** `enter` now leaves the human LOOKING at the board, which turns a stale `board.html` from an inconvenience into a defect: they are reading a picture of a paper that no longer exists. Every stage run ends by calling `haipipe-board` build and putting the deep link in the closing block.
      - **And the reverse direction, which matters more.** RE-READ the S page off disk before acting. A human comment or a `>` lane may have arrived through `serve.py` since this session last looked, so the page can change underneath this skill. Never cache a page across a phase boundary. This is what keeps the two-channel design honest: `haipipe-board` writes the page from a human's click, so this skill may never assume it wrote it last.
260726 · `0.7.0` · the eight contracts speak the ruled layout, and the gate row leaves STATUS.md
      Aligned with the paper-folder layout ruled 2026-07-26 on the design board (`skills/diagrams/01-haipipe-paper-260725`, face QA6): `0-sections/` to `sections/`, `0-displays/` to `displays/` (one folder per unit, the only home of an asset, no top-level `figures/`), `1-compile.sh` to `2-src/compile.sh`, and `STATUS.md` retired. These are the skill family's most binding paths: a contract's `artifact:`, `probes:`, `units:` and `output:` resolve at run time, so a stale one does not read wrong, it writes to the wrong place.
      - **`handoff:` rewritten on all six gated contracts.** Was `update STATUS.md (current_layer, maturity: X)`. Now `append the gate row to this stage's S page ## Log`. The Gate Ledger was the one part of `STATUS.md` that is HISTORY and cannot be derived from disk, so it needed a home rather than a deletion; it now sits on the page whose gate it was, where a reader is already standing.
      - **`0-seed`'s loopback warning dissolved rather than reworded.** It spent four lines protecting a stored `current_layer` from being demoted by a re-run. With no stored frontier there is nothing to demote: a loopback records its gate and changes nothing else.
      - **The venue pin moved.** `2a-venue`'s `pins: STATUS.md` is now `pins: 0-lifecycle/2-venue/S-Venue-0-venue.md`, into that page's own frontmatter. One page owns the venue contract; a second copy could only disagree with it.
      - **`stages/CONTRACT.md` gained two sections**: the paper-folder paths a contract may name (and the four it must never name), and why `STATUS.md` is retired with where each of its four parts went.
      - Verified: `check-contracts.py` `form ok` across all eight, and every `artifact:` path resolves on `Paper-Personality2Opioid-MISQ2026` except the two already known (`4-display`, blocked on QB2; `5-section-edit`, which is per-unit by design).
      - Pre-existing and NOT introduced here: `2a-venue/stage.md`'s frontmatter does not parse under a strict YAML loader. It fails identically at `HEAD`. Untouched.
260725 · `0.6.0`
      **Paper Stage now has one Board-first page-creation path.**
      - `create-page.py` is the public creator: it resolves one stage through `index.yml`, calls the
        Board's `stage.py new` primitive, and composes the selected stage template into Content jobs.
      - Stage contracts identify pages with `board_family` + `board_unit`; Board tooling owns literal
        filenames.
      - Page dependencies are optional. When present, page `requires:` is authoritative; optional
        `read_order:` remains craft guidance rather than a duplicate graph.
      - Per-unit is governed by independent human gates. Section Edit implements that grain; Display
        qualifies and remains a tracked migration. The other six stages stay single-output.
260725 · `0.5.0`
      **The board mapping now carries explicit inherited contracts.**
      - Display moved from Work 2 to its own `Display 0` family and board face.
      - Mapped S pages may declare `requires`, `style-from`, and `provides`; these fields inform the
        board contract without changing router execution.
      - The router refreshes the managed Stage Contract through `haipipe-board/stage.py` after upstream
        changes, while authored Content and legacy artifact/log paths remain untouched.
260725 · `0.4.1`
      **Stage contracts now map explicitly onto lifecycle-board S faces.**
      - Every stage declared `board_family`, `board_unit`, and (at that version) `board_face`.
      - The mapping is informational: stage execution still follows `index.yml`, `upstream`, and
        `downstream`, so a stable board family does not falsely redefine execution order.
      - After a phase changes its artifact, the mapped S face receives same-turn state, finish-item,
        and current-status synchronization. Embedded Content is not copied.
      - Submission and revision remain downstream board rounds, not new stage-router keys.
260720 · `0.4.0`
      - Consolidated eight paper stages behind one router and one stage contract loaded per invocation.

<!-- haipipe:skill:log:end -->
