# haipipe-paper-check · v0.3.6
state: ⚫ RETIRED 260805 · page logic in board/page-phases/haipipe-board-page-check; checkers declared per stage.md checker: line
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

**Retired 260805 (thin-paper phase 2, QC6).** The CHECK worker dissolved into three homes: the page logic lives on in `board/page-phases/haipipe-board-page-check`, the evidence craft became `paper/S06-main/section-edit/check-evidence-craft.md`, and the proof pass became the craft pack `paper/S09-build/proof-checker/`. Check scripts are now declared per stage by each stage.md `checker:` line and run before CHECK judges. The worker folders retired to `paper/_old/workers/`. The account below is the pre-fold record and stays as written.

## Opening
REPLACE THIS PARAGRAPH. Load `haipipe-board-page-for-skill` and write the three slots it names, in its order, in plain words: ❶ what `haipipe-paper-check` is and what it is FOR, ❷ when you reach for it rather than the ONE sibling you would otherwise pick, named, ❸ where it stands, meaning the one thing to know before trusting it.

NEVER open a skill page with a question. This stub used to seed `{name} is a shipped unit: what does it still owe, and is it healthy?`, and on 260802 five pages generated from it all opened with the same rhetorical question in the same four-slot shape, because a skill page DECIDES NOTHING and so has nothing to ask.
Delete these instructions once the paragraph is written; the FIRST BLANK LINE above is the split, and everything below it is the `More details` drawer, written as labelled parts.
`Opening` is the lead section's ONE name on every page kind (JL 260731: "just one single Opening"); `Question` survives only as a legacy alias for pages written before the rename.

## Writing Style
English only. One sentence per source line. Describe the shipped unit factually and keep generated inventory separate from human health judgment.

## Diagram
<!-- haipipe:skill:tree:start e8374e077346678f paper/_old/phase-hubs/haipipe-paper-check -->

**What `haipipe-paper-check` ships**: every file in the folder, with the one-line purpose each one states for itself.

```
haipipe-paper-check/
  CHANGELOG.md         160 ln  haipipe-paper-check — Changelog
  checks.sh            277 ln
  SKILL.md             456 ln  Skill: haipipe-paper-check (internal phase worker)
```

<!-- haipipe:skill:tree:end -->

**How `haipipe-paper-check` is used**: REPLACE THIS CAPTION with what your figure below actually shows.

```
WORKFLOW  (authored: a folder can be read off disk, an intent cannot)
Draw how this skill is actually used: the entry point, what it reads,
what it writes, and where it hands off. Delete this fence AND the
caption line above it if the tree is the whole story.
```

## Content
<!-- haipipe:skill:body:start e8374e077346678f paper/_old/phase-hubs/haipipe-paper-check -->

**haipipe-paper-check** · `0.3.6` · last shipped 2026-08-04

- folder   `paper/_old/phase-hubs/haipipe-paper-check/`
- tools    Bash, Read, Write, Edit, Grep, Glob, Agent
- summary  Paper-specific CHECK worker layered on haipipe-board-page-check; runs declared stage checks, seeds findings, and applies the paper's human gate.

### SKILL.md



Skill: haipipe-paper-check (internal phase worker)
=====================================================

CHECK phase worker.
Called by stage skills as the gate at the end of their declared phase sequence.
**LOAD THE PAGE LAYERS FIRST:** `../../../../board/page-types/haipipe-board-page-for-stage/SKILL.md`, then `../../../../board/page-phases/haipipe-board-page-check/SKILL.md`.
The generic contract owns judgment and routing.
This file adds paper checks, in-file comments, and the stage's declared human gate.
**HOW MANY GATES A STAGE OPENS IS THE STAGE'S OWN DECLARATION, not this file's.** Read `gates:` in the stage's contract at `../../../1-lifecycle/haipipe-paper-stage/stages/<order>-<key>/stage.md` before you open anything:

```text
gates: [check]           the default, and what all 8 current stages declare.
                         DRAFT, PROBE and REVISE run unattended; THIS is the only stop.
                         Safe because probe_depth caps PROBE at free work — an unattended
                         run cannot spend, so there is nothing earlier to authorize.
```

⛔ Never open a gate the contract did not declare, and never skip one it did. If `gates:` is
absent from a contract, treat it as `[check]` and say so in the report — a missing declaration is
a contract defect worth surfacing, not a licence to invent a gate.
CHECK is where everything is reviewed at once: by the human (copilot mode, default) or by a reviewer subagent standing in (autopilot mode; see Gate Modes below).

**Not user-facing.**
Users invoke stage skills:
```
/haipipe-paper claims           → claims skill calls this internally for CHECK phase
/haipipe-paper pitch            → pitch skill calls this internally for CHECK phase
/haipipe-paper section-edit §3  → section-edit skill calls this internally
```

The check has three parts: (1) **MECHANICAL** -- run automated sub-checkers, produce a pass/fail report; (2) **SEED `> CHECK:` COMMENTS** -- plant every flagged item at its exact spot in the working doc so the human's in-file pass is guided by the file itself; (3) **HUMAN** -- walk the `> CHECK:` comments, answer with `> USER:` comments, decide (proceed / restart / new round / accept / park -- see the 🧑 Decision menu in Report Format).
On restart, the restarted phase reads the `> CHECK:` comments + their `> USER:` replies and responds to them.



- 1 · How It Works
      1. **Run**: execute all applicable sub-checkers.
         For deterministic text checks run
         `./checks.sh <tex-or-dir> [--md <working-doc>] [--stage-page <S-page>] [--depth N] [--compile]`
         and paste its ✅/⚠️/❌ lines. `--stage-page` verifies the newest REVISE
         provenance record in that S page's `## Log`.
         For the PROBE contract (one direct topic `requires:`, four required `####` sections, valid state, and parent-register trace) run the paper probe checker (locate it per **Locating the probe checker** below). Any FAIL line means the gate cannot go green.
         Judgment checks (citation support, value provenance, display correctness) stay manual.
      2. **Report**: present results as a structured pass/fail table (see Report Format).
      2.5. **Seed `> CHECK:` comments**: every flagged/🔍/⚠️ item is planted as ONE `> CHECK:` comment at the exact spot it refers to -- in the stage doc (or section `.md`), in the nested entry page, or in the tex -- one line stating the issue + the judgment needed, with concrete values, never an abstract description.
      The chat report is the map; the in-file `> CHECK:` comments are what the human actually walks.
      A CHECK that hands over with a clean file and a chat-only report is DEFECTIVE (test-123333333: JL entered 0-seed.md to review and found nothing to guide the pass).
      3. **Human review**: the human walks the `> CHECK:` comments and replies `> USER:` under each (see Human Actions During CHECK for the per-track steps).
      4. **Decide**: proceed / restart / new round / accept / park.
      5. **On restart**: the restarted phase reads the `> CHECK:` comments and their
         `> USER:` replies and responds to each; resolved threads move verbatim to the
         owning S page's `## Log`.

- 2 · Locating the probe checker
      Installed skills flatten the tree, so a hard-coded relative path (`../../1-probe/...`) is NOT reliable.
      Glob for it — but **glob UNAMBIGUOUSLY**: TWO files named `check-probe-cards.sh` exist on disk (the paper family's, under `haipipe-paper-probe/`, and the application family's, under `haipipe-application-probe/`).
      A bare `find ... -name check-probe-cards.sh | head -1` can resolve to the WRONG FAMILY and silently check a paper against application invariants.
      Filter on the path, and fail LOUDLY when nothing matches:
      ```sh
      CHK=$(find -L ~/.claude/skills ./.claude/skills "${CLAUDE_PLUGIN_ROOT:-/nonexistent}" -maxdepth 4 \
              -path "*haipipe-paper-probe*" -name check-probe-cards.sh 2>/dev/null | head -1)
      [ -n "$CHK" ] || { echo "FAIL: paper checker not found"; exit 1; }

      sh "$CHK" <paper_root>                      # whole-paper entry pass
      sh "$CHK" <paper_root> --stage <stage-key>  # gate-scoped pass (see the per-stage table)
      ```
      A missing checker is a FAIL, never a silent skip: a gate that cannot run its checker has not checked anything.
      `--stage <stage-key>` asserts only the entries whose parent topic register names this stage.
      Without it, ONE in-flight `commissioned` build reds the gate of EVERY downstream stage for as long as the build runs, and every other stage's un-run entries red THIS one (JL resource-stage ruling C8-i).

- 3 · Gate Modes (copilot | autopilot)
      Mode spec is owned by `../../../1-lifecycle/ref/08-stage-gate.md`. Mode is an
      invocation/session choice, default copilot, and the selected mode plus actor is
      recorded in the S page's `## Log`.
      What changes INSIDE this worker:
      ```
      🧑 copilot     steps 2.5-4 above run as written: the worker seeds the `> CHECK:` comments, the human
                     reviews and decides.
      🤖 autopilot   > CHECK: comments are seeded the same (step 2.5 is mode-independent), then dispatch
                     ONE fresh-context reviewer subagent (Agent tool) that plays the review seat:
                     - reads the stage artifact + the pass/fail report + the > CHECK: comments + exit criteria
                     - leaves > REVIEWER: comments in the working doc (same places a human would)
                     - returns a verdict: proceed | restart-from-<DRAFT|PROBE|REVISE> | accept (+ reasons)
                     - on restart, the restarted phase reads > REVIEWER: comments exactly as it
                       would read > USER: comments
                     HUMAN-ONLY items are NEVER delegated or silently passed: 🔍 citation
                     verification + bibtex copying (agents never touch .bib) and any item the
                     reviewer marks "needs the human" go to a DEFERRED human queue, listed in the
                     verdict and in the gate-ledger Notes; the human clears the queue at the next
                     copilot touchpoint. The human can reopen any agent-approved gate later.
      ```
      The judgment step always happens; autopilot only changes WHO sits in the review seat.

- 4 · Sub-Checkers
      Five groups of checks, one per phase (+ META, + PROOF).
      Checks that don't apply to a section are marked `-- skipped` (e.g., proof checks for a section without proofs, values checks for a section without numbers).
      The deterministic text-match rows below are runnable in one shot: `./checks.sh <tex-or-paper-dir> --md <stage-doc-or-section.md> --md <nested-entry.md>`.
      The judgment rows (does the citation SUPPORT the claim, is the VALUE traceable, does the DISPLAY match) are human/reviewer work and are described once under **Human Actions During CHECK** -- the tables here only say what gets flagged, not how the human resolves it.

- 4.1 · 📝 DRAFT checks — verify the outline is well-formed
      | Check | How to verify | Pass condition |
      |---|---|---|
      | structure block exists | grep for ``` block with ¶ counts in outline .md | block present with counts |
      | all ¶ have headlines | each `### P#.` heading has text after it | no empty headings |
      | all ¶ have previews | each ¶ heading has a `(parenthetical preview)` below it | no missing previews |
      | draft sentences present | each ¶ block has sentences (not just heading + preview) | ≥1 sentence per ¶ |
      | sentence counts in range | count sentences per ¶ vs venue norm (e.g., 5-7 for MISQ) | all within range or flagged ⚠️ |
      | USER comments resolved | each `> USER:` has a `> CC:` response below it | no orphan USER comments |

- 4.2 · 📚 PROBE checks — verify every OWNED hole landed its answer
      What CHECK walks is the **stage doc** (or section `.md`) and the paper's **nested S03/S04 entries**. Since PROBE runs automatically, the judgment items require human action during CHECK (see Human Actions During CHECK).
      **The entries** — the mechanical spine, run first:
      | Check | How to verify | Pass condition |
      |---|---|---|
      | entries verify clean | `sh "$CHK" <paper_root> --stage <stage-key>` (locate `$CHK` per **Locating the probe checker**) | exit 0; any FAIL line reds the gate |
      | every hole is OWNED | grep the stage doc / section `.md` for `\cite{TOADD}` and `{VAL:?` | each carries a `[Q-<Stage>-<n>]` id (a bare placeholder = a hole nobody owns) |
      | every owner resolves | each `[Q-<Stage>-<n>]` appears in a direct topic Q-consumer register and points to one nested entry | no dangling id |
      | harvest landed | each such entry's `#### a-executor` is non-empty | ⚠️ if any is still empty (the answer has not come back) |
      **Citation:**
      | Check | How to verify | Pass condition |
      |---|---|---|
      | density meets venue norm | count cited sentences / total sentences in the stage doc or section `.md` | ratio ≥ venue threshold |
      | 🔍 sources listed | grep the entries' `#### a-executor` bodies for `🔍` | ⚠️ if any remain (human verifies during CHECK) |
      | all factual assertions cited | compare factual sentences vs cited sentences | no uncited factual claims |
      | all \cite{key} in .bib | `./checks.sh` (broken \cite) | zero broken refs |
      | no bibtex in markdown | `./checks.sh --md <stage-doc> --md <nested-entry.md>` | zero bibtex blocks (bibtex lives ONLY in .bib) |
      **Values:**
      | Check | How to verify | Pass condition |
      |---|---|---|
      | every number is sourced | each number in the prose traces to a value harvested in some entry's `#### a-executor`, or to a `\ref`-ed display | all traced |
      | placed values grep their source | `grep -F '<value>' <the source path the a-executor names>` | every placed value hits (a value with no source hit is REJECTED) |
      | 🔍 unknown sources listed | grep the `#### a-executor` bodies for `🔍` | ⚠️ if any remain (human locates during CHECK) |
      | method claims checked | claims about a method the paper implements | ⚠️ if any is unimplemented (human confirms during CHECK) |
      **Display:**
      | Check | How to verify | Pass condition |
      |---|---|---|
      | all needed displays linked | check \ref{fig/tab} in tex resolve to displays/ | all resolve |
      | no missing displays | compare narrative display needs vs linked units | all covered |
      | pending DR rows listed | grep `0-lifecycle/3-display/_DISPLAY_REQUEST.md` for rows not `done` | 📨 ⚠️ if any remain (never pre-place a `\ref` for a unit that does not exist) |

- 4.3 · 💎 REVISE checks — verify prose quality
      | Check | How to verify | Pass condition |
      |---|---|---|
      | no AI voice patterns | `./checks.sh` (high-signal tells: delve/utilize/tapestry/seamless/… — noisy connectives excluded) | zero matches (or flagged ⚠️) |
      | no em-dashes | `./checks.sh` (em-dash) | zero matches |
      | Pn.Sn markers sequential | `./checks.sh` (Pn.Sn sequence — flags gaps/dupes per ¶) | sequential within each ¶ |
      | sentence count matches | count Pn.Sn markers vs outline sentence count | counts match |
      | outline ↔ tex synced | compare outline sentences vs tex sentences | content matches |
      | banner points match content | read each `% Para [X.P#]` and verify the ¶ below matches | all match |
      (em-dash is a ❌ FAIL in checks.sh -- absolute house rule, same tier as TODO; AI-voice and Pn.Sn stay ⚠️ because they have legitimate false-positive room.
      JL 2026-07-07: "统一提议。")

- 4.4 · 📐 META checks — verify whole-section integrity
      | Check | How to verify | Pass condition |
      |---|---|---|
      | terms consistent | grep for term variants (e.g., "clinical ambiguity" vs "clinical uncertainty") | one term per concept |
      | claims traceable | each claim sentence has either a citation or is "our study" framing | no unsupported claims |
      | \label/\ref resolve | `./checks.sh` (broken \ref + orphan \label) | zero broken refs (orphans ⚠️) |
      | compiles clean | `./checks.sh --compile` (wraps ./2-src/compile.sh) | zero LaTeX errors |
      | no TODO markers | `./checks.sh` (TODO/FIXME/XXX) | zero matches |

- 4.5 · 🔬 PROOF checks — only if the section has proofs
      Runs only if the section contains `\begin{proof}`, `\begin{theorem}`, or `\begin{lemma}`.
      | Check | How to verify | Pass condition |
      |---|---|---|
      | proof checker passes | dispatch to haipipe-paper-proof-checker (Agent tool) | verdict PASS or WARN |
      The proof-checker (sibling in 3-check/) produces its own detailed report; this checker extracts the verdict.
      See Relation to sibling.

- 4.6 · 📚 EVIDENCE checks — only when the run is pre-submission
      Runs only when the gate is being opened ahead of a submission, not at an ordinary per-section gate. Resolving every DOI at every section gate is unaffordable, and a pass too expensive to run is a pass that silently never runs.
      | Check | How to verify | Pass condition |
      |---|---|---|
      | evidence walk passes | dispatch to haipipe-paper-check-evidence (Agent tool) | verdict PASS or WARN |
      Three axes, each failing differently: every cited work EXISTS, its metadata is right, and it actually supports the sentence citing it; every number RE-DERIVES from its source; every display matches its claim and renders clean in the compiled PDF.
      Report-only, like the proof-checker: it seeds `> CHECK:` comments at the exact spot and never edits prose. Fixes route back through REVISE. An item the human declines to fix becomes a `{CONCERN:<risk>} [Q-<Stage>-<n>]` so it stays visible at every later gate rather than evaporating.
      FAIL is reserved for the two that block a submission outright: a citation to a paper that does not exist, and a number that cannot be re-derived from any named source.

- 5 · Report Format
      ```markdown
      # CHECK REPORT: §N Section-Name
      # Date: YYYY-MM-DD

      ## Summary
      PASSED: NN   FAILED: NN   WARNING: NN   SKIPPED: NN
      📌 CHECK COMMENTS SEEDED: NN  (list the files, e.g. 0-seed.md ×2, PP01_welldoc-feasibility.md ×3)

      ## 📝 DRAFT
        ✅ structure block present (6 ¶)
        ✅ all ¶ have headlines + previews
        ✅ draft sentences: 38 total
        ⚠️ P2 has 8 sentences (venue norm: 5-7)

      ## 📚 PROBE
        ✅ check-probe-cards.sh --stage section-edit: exit 0 (4 entries)
        ✅ every hole OWNED (3 \cite{TOADD}, all carrying this unit's Q-Sec<unit><Slug>-<n> id)
        ✅ citation density: 0.41 (norm ≥ 0.25)
        ❌ 2 🔍 sources unverified (Eddy 1984, Deyo 2015 — PP02 QX1 a-executor)
        -- values: skipped (no numbers in this section)
        -- display: skipped (no displays in this section)

      ## 💎 REVISE
        ✅ no AI voice patterns
        ✅ no em-dashes
        ✅ Pn.Sn sequential (38 markers)
        ✅ outline ↔ tex synced

      ## 📐 META
        ✅ terms consistent
        ✅ claims traceable
        ✅ \cite resolves
        ✅ compiles clean
        ✅ no TODO markers

      ## 🔬 PROOF
        -- skipped (no \begin{proof} in this section)

      ─────────────────────────────────
      PASSED: 14   FAILED: 1   WARNING: 1   SKIPPED: 4
      ─────────────────────────────────

      ## ❌ FAILED items

      1. PROBE/citation: 2 🔍 candidates unverified
         → recommend: restart from PROBE/citation (verify on Scholar)
         → OR: accept (defer verification)

      ## ⚠️ WARNING items

      1. DRAFT: P2 has 8 sentences (venue norm 5-7)
         → informational, not blocking

      ## 🧑 Decision

      - [ ] ✅ PROCEED to next lifecycle stage (all critical items pass)
      - [ ] ♻️ RESTART this stage from: _____ (DRAFT / PROBE / REVISE) — fix issues, re-check
      - [ ] 🔄 NEW ROUND of this stage (keep artifacts, run another DPRC cycle to deepen)
      - [ ] 🤷 ACCEPT with known issues (log what's deferred)
      - [ ] ⏸️ PARK this section (switch to another section, come back later)

      (resource stage adds THREE exits, not two -- see the Stage Exit Invariant AMENDMENT below)
      ```
      **Stage Exit Invariant: CHECK is the ONLY door out of a stage.**
      For every stage EXCEPT `resource`, its verdicts move in exactly two directions: ♻️ restart re-opens a PHASE within the SAME stage (DRAFT / PROBE / REVISE -- never another stage); ✅ proceed (or 🤷 accept) crosses the gate to the NEXT stage.
      Going BACK across stages (e.g. redoing seed while the frontier is section-edit) is NOT a CHECK outcome -- that is a lifecycle loopback: re-enter the earlier stage (🔥 moves there, 🚀 stays at the frontier), and it runs its own DPRC and its own CHECK gate.
      **AMENDMENT -- `resource` only: THREE directions, not two (JL ruling C7, 2026-07-14; spec in `../../../1-lifecycle/ref/08-stage-gate.md`).**
      The two verdicts above admit no KILL.
      The resource gate adds a third exit:
      ```
      ✅ proceed  -> claims                       the normal forward gate; maturity: resource
      🔥 reseed   -> [LOOPBACK -> SEED]           every demand row is UNOBTAINABLE: the paper cannot be
                                                  written as seeded. 🔥 moves back to seed (🚀 stays at
                                                  the frontier); seed runs its own DPRC cycle.
      🅿️ park     -> maturity: resource-blocked   the demand is real, the resource is in flight or
                                                  behind a DUA, and there is nothing to do but wait.
      ```
      Rationale: a stage whose PURPOSE is discovering that the paper CANNOT BE WRITTEN must be able to SAY SO.
      Without `reseed` and `park` this gate could only `promote -> claims`, mechanically handing a DEAD PAPER FORWARD -- the exact failure the stage was built to end.
      `reseed` and `park` are offered at the resource gate ALONGSIDE the five standard decisions; a CHECK run on resource that does not offer them is DEFECTIVE.
      The amendment does NOT generalize -- every other stage still has exactly the two directions above.

- 6 · Human Actions During CHECK
      CHECK is where every human action in the lifecycle happens.
      The entry point is the `> CHECK:` comments: open the working docs the report's CHECK COMMENTS SEEDED line names and walk them -- each flagged item below is anchored by one, so the pass is guided, not a self-service hunt.
      Reply `> USER:` under each as you go (plus any free `> USER:` comments of your own).

- 6.1 · Citation verification
      1. Open the nested entries the report names and find all 🔍 sources in their `#### a-executor` bodies (harvested candidates not yet in .bib)
      2. Click the `> SEARCH: [Scholar](url)` link for each 🔍 source
      3. Read the paper abstract, confirm it supports what the `#### a-executor` says the source establishes
      4. On Scholar, click the cite icon, select BibTeX, copy the bibtex block
      5. Paste the bibtex into the `.bib` file
      6. In the entry, mark verified `> ✅ SEARCH:` / rejected `> ❌ SEARCH: reason`
      7. On restart, the agent places newly verified keys into the `\cite{TOADD} [Q-<Stage>-<n>]` holes that own them
      **The agent NEVER generates bibtex — the human copies it from Scholar into `.bib`. Bibtex lives ONLY in `.bib`, never in a probe entry or any markdown.**

- 6.2 · Values verification
      1. Open the nested entries the report names and find all ⚠️ (mismatch) and 🔍 (source unknown) values in their `#### a-executor` bodies
      2. For ⚠️ values: open the source path the `#### a-executor` names, confirm which number is correct (prose or source)
      3. For 🔍 values: locate the source the agent could not find
      4. For ❌ method claims: confirm the method is implemented or decide to drop the claim
      5. Add `> USER:` comments with corrections or decisions; on restart the agent re-traces

- 6.3 · Display review
      1. Review generated display outputs (figures, tables) linked to the section
      2. Check that each display's content matches the claim it supports
      3. Check that numbers in displays match the values harvested in the entries' `#### a-executor` bodies
      4. Add `> USER:` comments on layout, labeling, content, or revisions needed
      5. Flag any DR row in `0-lifecycle/3-display/_DISPLAY_REQUEST.md` still short of `done`; on restart the agent re-routes it

- 6.4 · Decide
      1. Read the CHECK report (pass/fail summary + CHECK COMMENTS SEEDED line), review any ⚠️ warnings
      2. Confirm every `> CHECK:` comment has a `> USER:` reply
      3. Decide: proceed / restart from a phase / new round / accept with issues / park

- 6.5 · On restart
      When the human restarts from a phase (e.g., "restart from PROBE"):
      - The agent re-runs that phase and reads ALL `> CHECK:` comments with their `> USER:` replies, plus every free `> USER:` comment, and responds to each (a `> CHECK:` comment with no reply is surfaced back to the human, never silently skipped)
      - DRAFT restart: revise the outline per `> USER:` feedback
      - PROBE restart: re-audit, place newly verified keys from .bib into the holes that own them (in the .md, then sync); new-candidate requests from `> USER:` comments become nested topic entries, dispatched by the PROBE phase (never inline search)
      - REVISE restart: re-apply prose quality rules addressing `> USER:` style concerns; each change carries a why-comment

- 7 · Applicability Beyond Section-Edit
      This checker pattern works for any declared phase list ending in CHECK. Venue
      omits REVISE; the checker does not invent it.
      For non-section-edit stages:
      | Stage | DRAFT checks | PROBE checks | REVISE checks | META checks |
      |---|---|---|---|---|
      | seed | all five declared sections filled (Seed Question, Motivations, Landscape, Tentative Claim Shape, Q-consumer) | every entry serving a `Q-Seed-<n>` has a resolving `**target**` on disk and a non-empty `### a-executor`, and each Q-consumer's answer is written back into 0-seed.md | seed is readable | ready to advance to **resource** |
      | resource | `Resource Description` + `Q-consumer` on `S-Work-0-resources.md`; every resource closes on `### Serves & carries`; every Seed forward pointer is consumed or explicitly declined in that page's `## Log` | every `Q-Resource-<n>` has landed its Answer, is explicitly deferred, or is a `commissioned` BUILD entry; scoped checker exits 0 | if declared, sharpen woolly fitness rulings | **the load-bearing sentence, asked verbatim:** "Does every hypothesis have a resource that is HAVE+FIT, or a COMMISSIONED build with an owner and a DATE, or a SCOPE CUT the human said out loud?" |
      | claims | H1/H2/H3 listed | all claims linked to evidence | claims well-stated | no unsupported GAPs |
      | venue | Venue Decision + Relevant Files + Section Styles + Requirements + Q-consumer are filled; each Section Styles row resolves both `style:` and `template:` | every `Q-Venue-<n>` has a real entry and landed Answer, or a declared above-ceiling `deferred` entry; scoped checker exits 0 | `--` (Venue omits REVISE by declaration) | the pin remains provisional until CHECK records the approving actor and date |
      | pitch | cover letter drafted | venue pack consulted | readability rules pass | Editor's Chair Test |
      | narrative | design contract drafted | claims linked to beats | arc/flow coherent | all beats [READY] |
      | display | display plan exists | all displays generated | visual quality | all linked in tex |
      When invoked for a non-section-edit stage, the checker resolves that stage's
      `../../../1-lifecycle/haipipe-paper-stage/stages/<order>-<key>/stage.md`, reads
      its declared `phases:`, `template:`, and `done_criteria:`, and treats that
      contract as authoritative. It never looks for a per-stage `SKILL.md`.
      **Resource gate — the pass/fail rulings the load-bearing sentence implies**
      (spec: `../../../1-lifecycle/haipipe-paper-stage/stages/1a-resource/stage.md`):
      ```text
      commissioned + owner: + eta: in the FUTURE            -> PASS   (a build in flight must not red the gate)
      commissioned + no owner:                              -> FAIL   (an unowned build is a wish)
      commissioned + eta: PASSED, no receipt                -> FAIL   (C6: `commissioned` is not a laundering token)
      a BUILD entry with no `cross-project:`                -> FAIL   (C4: empty is a FAIL; `none-found` is legal)
      commissioned, no matching human `--depth N` authorization
        recorded in the S page's ## Log                    -> FAIL   (dispatched behind the human's back)
      a fitness ruling that does not say what it KILLS      -> FAIL   ("probably fine" is a DEFECT, not an answer)
      a demand with NO resource                             -> NOT A FAILURE. It is a SCOPE CUT, said out loud
                                                                      by the human and logged in the S page. The paper
                                                                      gets smaller; the paper does not get wrong.
      ```
      The entry-status rulings (eta, owner, cross-project) are already enforced mechanically by the checker — RUN it and SHOW its output, never eyeball the entries.
      The fitness ruling and the scope cut are judgment items: seed them as `> CHECK:` comments and let the human answer.
      Resource's decision menu carries THREE exits, not two — see the AMENDMENT under **Stage Exit Invariant**.

- 8 · Relation to sibling
      ```
      3-check/
        haipipe-paper-check/           ← THIS (auto-gate orchestrator)
        haipipe-paper-proof-checker/   ← sub-checker (math proofs only)
      ```
      The checker CALLS the proof-checker when needed.
      The proof-checker never runs alone as the CHECK phase gate.

- 9 · Done criteria
      CHECK phase is done when:
      - [ ] All sub-checkers have run (deterministic ones via `./checks.sh`)
      - [ ] Report produced and presented to human
      - [ ] Every flagged/🔍/⚠️ item seeded as a `> CHECK:` comment in-file (CHECK COMMENTS SEEDED line in the report; a clean-file handover is a defective CHECK)
      - [ ] Human has verified 🔍 citation candidates (or deferred)
      - [ ] Human has confirmed flagged values (or deferred)
      - [ ] Human has reviewed generated displays (or deferred)
      - [ ] Every `> CHECK:` comment has a `> USER:` reply, or is covered by the recorded decision (accept/park logs unanswered ones as deferred)
      - [ ] Human has decided: proceed / restart / new round / accept / park
      - [ ] If restart: agent re-runs the phase reading the `> CHECK:` threads + free `> USER:` comments, then re-checks
      - [ ] Owning S page `## Log` updated with check result + human actions taken

- 10 · Who calls this skill
      Stage skills call this as their CHECK phase:
      | Stage skill | What this skill checks |
      |---|---|
      | seed | seed.md done-gate (promotion criteria) |
      | resource | `Resource Description` + `Q-consumer` (the load-bearing sentence; `--stage resource` entry pass; 3 exits) |
      | claims | hypothesis list + evidence linkage |
      | venue | five-section venue contract + paired style/template resolutions + scoped venue probes + approval receipt |
      | pitch | cover letter (Editor's Chair Test, readability) |
      | narrative | story beats (all [READY], arc/flow coherence) |
      | display | display plan (all units generated, linked in tex) |
      | section-edit | section S page + tex (declared phases + meta + proof) |

- 11 · Sibling phase workers
      | Phase | Worker | Called after |
      |---|---|---|
      | DRAFT | haipipe-paper-draft | -- |
      | PROBE | haipipe-paper-probe | DRAFT |
      | REVISE | haipipe-paper-revise | PROBE |
      | CHECK (this) | haipipe-paper-check | REVISE |
### The other files

1 files besides `SKILL.md` and `CHANGELOG.md`, each with the purpose it states about itself. They are described here, not reproduced: the folder is the copy.

```
checks.sh     277 ln
```

<!-- haipipe:skill:body:end -->

## Aims
### P · Page-level health ruling
- P1 · Rule this skill's health.
  **Done when:** `state:` records a human judgment: stable, in flux, needs work, or parked.

## States
### P · Page-level health ruling
- ⬜ P1 · Page generated 260804 1627; nothing ruled yet.

## Log
- 260806 0130 · [REVISE-CC] retirement recorded: board/page-phases/haipipe-board-page-check + S06-main/section-edit/check-evidence-craft.md + S09-build/proof-checker/; checkers per stage.md checker: line
260804 1627 · page generated from `paper/phase/3-check/haipipe-paper-check/` by `skillpage.py new`

<!-- haipipe:skill:log:start e8374e077346678f paper/_old/phase-hubs/haipipe-paper-check -->

Converted from the skill's own `CHANGELOG.md`: 23 releases.

260804 · `0.3.6` · Page CHECK layering
      - Loads the Stage Page Type and generic `haipipe-board-page-check` before paper-specific gates and sub-checkers.
      - Leaves the paper's human-gate declaration local while the shared phase owns judgment and routing boundaries.
260727 · `0.3.5` · the reported id follows the per-unit scheme
      - The PROBE-axis example line now names this unit's own `Q-Sec<unit><Slug>-<n>` id rather
        than the retired shared `Q-Section-<n>` (JL ruling 2026-07-27).
260726 · `0.3.4` · CHECK follows the Board adapter
      - Placeholder ownership now resolves against Q-consumer checklist records in
        the S page's `## Items to Finish`, never a duplicate Content block.
260726 · `0.3.3` · CHECK reads declared stage contracts
      - Non-section gates now resolve `stages/<order>-<key>/stage.md`; CHECK no
        longer asks for nonexistent per-stage SKILL files.
      - Added Venue's declared no-REVISE path and paired style/template gate.
      - Updated Resource checks to `Resource Description` + `Q-consumer`.
260726 · `0.3.2`
      - Re-rooted `checks.sh --compile` from retired root `1-compile.sh` to the
        canonical `2-src/compile.sh`.
      - An explicitly named `.tex` target can compile directly with output beside
        that target; a paper directory without a build script no longer causes the
        checker to guess a master.
      - Corrected CHECK's active probe-entry globs to `1-probes/PP*/*.md`.
260726 · `0.3.1` · one current gate, S-page proof
      - All current stages declare their one human gate at CHECK.
      - `checks.sh --stage-page` reads REVISE provenance from the S page's `## Log`.
      - Resource spend is authorized by the human-supplied `--depth`, not a DRAFT gate.
260724 · `0.3.0`
      Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 3.0.0; older entries below keep their original numbers).
260719 · `3.0.0`
      Changed (JL 2026-07-19, paper/2-phase refactor — the sidecar model is retired: `1-probes/` is the only consumer-side source of truth, `_LOG_<stage>.md` the only sidecar)
      - **What CHECK walks is RE-ROOTED**: the stage doc (or section `.md`) + the paper's `1-probes/` entries. Every `_CITATION_` / `_VALUES_` / `_DISPLAY_` reference is gone from SKILL.md — they were load-bearing in NINE places (frontmatter summary, step 2.5 comment-seeding targets, the one-shot `./checks.sh` invocation, the Citation table, the Values table, the report-format SEEDED example, Citation verification, Values verification, Display review, and the seed row of the per-stage gate table). A checker that scores a document nobody writes reports a metric it cannot compute.
      - **📚 PROBE checks restructured** around the DRAFT contract "every hole is FILLED or OWNED". New leading table (**The entries**): `check-probe-cards.sh --stage <key>` exit 0 · every `\cite{TOADD}` / `{VAL:?` carries a `[Q-<Stage>-<n>]` id (a bare placeholder = a hole nobody owns) · every id resolves to a Q-consumer block AND a bound `## QX<n>` entry · the entry's `### a-executor` is non-empty. Citation/Values/Display tables re-rooted onto the `### a-executor` bodies: 🔍 sources are greppped there, and a placed value must satisfy `grep -F '<value>' <the source path the a-executor names>` (the fabrication guard, mirrored from the probe worker's ⑤).
      - **Display track** now reads `0-lifecycle/4-display/_DISPLAY_REQUEST.md` for DR rows short of `done` — 📨 pending, flagged for CHECK, never a pre-placed `\ref` for a unit that does not exist.
      - **Human Actions** re-rooted: Citation verification, Values verification, and Display review now open the `1-probes/PP*.md` entries the report names. Step 7 of citation verification states where a verified key LANDS: the `\cite{TOADD} [Q-<Stage>-<n>]` hole that owns it.
      - **Vocabulary**: `section` → ENTRY, `serves:` → `### q-consumer`, `card` → entry throughout (`--stage` scoping, the resource gate rulings block, the resource row of Who-calls-this-skill). `## Locating the card checker` → `## Locating the probe checker`; the script's `check-probe-cards.sh` filename is unchanged and still load-bearing.
      - **PROBE restart** guidance: new-candidate requests become `## QX<n>` ENTRIES (was "question SECTIONS").
      Fixed
      - **`checks.sh` no longer asserts a dead marker is the convention.** The TODO-marker block's rationale claimed `% TODO[values]` / `% TODO[cite]` are "planted in comments by DRAFT and MUST block the gate until PROBE fills them" — that convention is retired (1.8.1 already marked the flags legacy, but the comment still taught them as live). The TODO/FIXME grep itself STAYS at the ❌ tier on its own merit: unfinished work parked in a `%` comment is exactly work hidden from the compiled PDF. The two LIVE markers (`\cite{TOADD}`, `{VAL:?}`) are enforced elsewhere, not here.
      - **`checks.sh` `--md` header** re-rooted: "a markdown working doc (`_CITATION_`/`_VALUES_`/outline)" → a stage doc, a section `.md`, or a `1-probes/PP*.md` entry file.
260714 · `2.1.0`
      - "planned/dispatched cards" -> `planned` sections + unresolvable `target:`s; `status: planned card` -> `state: planned` section. (`check-probe-cards.sh` KEEPS its filename; only its internals changed.)
      - PROBE restart: new-candidate requests from `> USER:` comments become question SECTIONS in `1-probes/`, dispatched by the PROBE phase (was "probe plans -> gateway").
260714 · `1.9.0`
260714 · `2.0.0`
      - PROBE REDESIGN (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14 — R1-R18). 1-probe-plans/ -> 1-probes/ (PPNN_<topic>.md, one file per TOPIC, one SECTION per question: serves/target/state/commission/reading + ONE `## Why` per file holding the stake). Binding is by PATH: a section's `target:` points at the answering `<leaf>/QA/<n>-<slug>.md` in the bank. DELETED: `## Verdict`, the `verdicted` and `dispatched` states, `_ASK/`/`_ANS/` stubs, `answers:`, and Agent(haipipe-probe-orchestrator-agent) (the GATEWAY — archived + de-registered). A claim's STATUS now lives ONLY in 0-lifecycle/1b-claims/1b-claims.md. Dispatch is now DIRECT: the section's `commission:` block, VERBATIM, to Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent).
      - The seed done-criterion re-stated for probe SECTIONS: every section's `reading:` written and every `target:` resolving on disk.
      Added (BLOCKER 10 repair -- the worker that RUNS Gate 2 did not know the resource stage existed)
      - **`resource` row in the per-stage gate table** (Applicability Beyond Section-Edit). Before this, a live resource CHECK had NO gate criteria to apply -- the stage shipped a load-bearing sentence that the executing worker had never heard of. The META column now carries it VERBATIM: "Does every hypothesis have a resource that is HAVE+FIT, or a COMMISSIONED build with an owner and a DATE, or a SCOPE CUT the human said out loud?" The PROBE column carries the stage-scoped card pass (`sh "$CHK" <paper_root> --stage resource` exits 0).
      - **Resource gate rulings block**, below the table: `commissioned` + owner + future eta -> PASS; no owner -> FAIL (an unowned build is a wish); eta PASSED with no receipt -> FAIL (C6); a BUILD card with no `cross-project:` -> FAIL (C4); a fitness ruling that does not say what it KILLS -> FAIL; **a demand with NO resource is NOT a failure -- it is a SCOPE CUT, said out loud and logged.** Card-status rulings are checker-enforced (RUN it, never eyeball); fitness + scope cut are `> CHECK:` judgment items.
      - **`haipipe-paper-resource` row in Who calls this skill.**
      Changed
      - **Stage Exit Invariant AMENDED: two directions for every stage EXCEPT `resource`, which has THREE** (JL ruling C7, 2026-07-14; spec in `08-stage-gate.md`, which already carried the amendment while the EXECUTING worker did not -- so `reseed` and `park` were UNREACHABLE in practice). ✅ proceed -> claims · 🔥 reseed -> [LOOPBACK -> SEED] · 🅿️ park -> `maturity: resource-blocked`. Rationale: a stage whose PURPOSE is discovering the paper CANNOT BE WRITTEN must be able to SAY SO -- without these it could only `promote -> claims`, mechanically handing a DEAD PAPER FORWARD. The Report Format decision menu gains the two resource-only checkboxes. Does NOT generalize.
      - **seed row's exit fixed**: seed now advances to **resource**, not claims.
      Fixed
      - **Card-checker locator is now UNAMBIGUOUS** (new section: Locating the card checker). TWO files named `check-probe-cards.sh` exist on disk -- the paper family's and the application family's -- so the old hard-coded `../../1-probe/haipipe-paper-probe/check-probe-cards.sh` (fragile: installed skills flatten the tree) and any bare `find -name check-probe-cards.sh | head -1` could resolve to the WRONG FAMILY and silently check a paper against application invariants. Now: `find ... -path "*haipipe-paper-probe*" -name check-probe-cards.sh | head -1`, plus a LOUD failure when nothing matches (`[ -n "$CHK" ] || { echo "FAIL: paper checker not found"; exit 1; }`) -- a gate that cannot run its checker has not checked anything.
260710 · `1.8.1`
      Fixed (fresh-agent audit, C5)
      - PROBE-restart guidance: placement is md-first; new-candidate requests become probe plans -> gateway (was "search for new candidates").
      - checks.sh header: TODO[] flags marked legacy (DRAFT plants {VAL:?}/\cite{TOADD} in the .md).
260709 · `1.8.0`
      Changed (JL ruling 2026-07-09 (LLMTrait-Section session postmortem): normalize the writing process)
      - checks.sh: new `--log <file>` check -- the newest [REVISE] entry in a _LOG must carry its `workers:` proof line (missing = FAIL; REVISE present without a [GATE] draft-review on record = WARN). Enforces the proof-carrying REVISE dispatch contract.
      Fixed
      - checks.sh: `mapfile` replaced with portable while-read loops (macOS /bin/bash 3.2 has no mapfile -- dir-mode tex scan and .bib discovery silently broke, making broken-cite checks unreliable on Macs); empty --log array guarded for set -u under bash 3.2.
260707 · `1.7.0`
      Changed (skillset-diagnose FIX round; threads T1/T10 + findings D2-D9)
      - Gate wiring (T1, JL: "同意你的意见"): step 1 Run now ALSO runs the probe checker `check-probe-cards.sh <paper_root>` — a FAIL line (planned/dispatched card, unresolved ref, `harvest: OWED` lane, bibtex/table in a working doc) means the gate cannot go green. Closes the seed-stage incident class (probe ✅ shown over an unrun probe; three sibling docs had promised this wiring, code was absent).
      - em-dash upgraded ⚠️→❌ in checks.sh (T10, JL: "统一提议。") — absolute house rule, same tier as TODO; AI-voice/Pn.Sn stay ⚠️ (false-positive room). SKILL row note added.
      - Decision enumeration: intro line 25 (D2) and the flow diagram (D3) reconciled to the full 5 outcomes (proceed/restart/new round/accept/park).
      - checks.sh hardening: bibtex-leak grep matches ANY entry type via `@word{key,` shape (D4; was 7 hardcoded types); XXX dropped from TODO tier — collides with double-blind placeholders (D5); `\cite` present + no .bib found is now a loud ⚠️ with a --depth hint, not a silent skip, and the split-bib-below-depth false-positive caveat is documented (D6); AI-voice grep runs on comment-stripped text like em-dash (D8); `--depth`/`--md` argument parsing guarded against flag-swallowing (D9).
      Changed (skill-quality pass: contract was sound but prose was ~412 lines with each rule stated 4-6×, guaranteeing drift on the next edit)
      - De-duplicated: "CHECK is the ONLY human phase" collapsed from ~6 statements to 2 (intro + one anti-pattern); bibtex rule collapsed from ~6 to 2 (one bolded rule + one anti-pattern, anti-patterns 387/388 merged); the per-track "human action during CHECK" blocks that duplicated the standalone section removed from the Sub-Checker tables and folded into a single **Human Actions During CHECK** home; the "three parts" list folded into the intro so the flow is shown once as diagram + one step list.
      - Frontmatter: dropped the nonstandard `predecessors:` key (proof-checker relation already documented in-body); version → 1.6.0, last_updated → 2026-07-07; outcome enumeration reconciled to the full 5 (proceed/restart/new round/accept/park) everywhere.
      - ~412 → ~285 lines, zero contract/behavior change.
      Added
      - `checks.sh` — self-contained deterministic MECHANICAL sub-checks: em-dash, AI-voice tells, TODO/FIXME/XXX, bibtex-in-markdown, broken `\cite` (not in any .bib), broken `\ref` (no matching `\label`), orphan `\label` (defined, never `\ref`-ed → ⚠️), and Pn.Sn sequence (gaps/dupes per ¶ → ⚠️). Emits ✅/⚠️/❌ lines for direct paste into the report; comments stripped so `%% ---- Pn.Sn ----` markers don't false-flag as em-dashes; exit 1 on any ❌. Flags: `--md <file>` (bibtex-leak scan of a working doc, repeatable), `--depth N` (widen tex/bib scan for deep layouts / split bibs), `--compile` (opt-in, wraps `./1-compile.sh` and greps its log for LaTeX errors). `_external/` and `_archive/` trees excluded so reference bibs don't mask real broken cites.
      - AI-voice list tuned to high-signal tells only (delve/utilize/tapestry/seamless/showcase/intricate/nuanced/realm/underscore/leverage); noisy academic connectives (Furthermore/Moreover/Additionally) dropped — on a live paper they produced 8 false hits and buried the 1 real one.
      - The stale `check_refs.py` reference (the script lived only under `_archive/`) is retired — the META `\label/\ref`/compile and PROBE `\cite`/bibtex rows now point at `./checks.sh`, which is shipped in-folder and validated against a real paper (`Paper-FairGlucose-icml2026`: caught 3 real broken cites, 5 broken refs, 4 TODOs).
260705 · `1.5.2`
      Changed (JL: 为啥不叫comments — one mechanic, one name)
      - "pin" vocabulary dropped throughout: the feature is plain `> CHECK:` comments (comment family: > USER: / > CC: / > REVIEWER: / %% {CC-worker}: / > CHECK:). Report line renamed PINS SEEDED -> CHECK COMMENTS SEEDED. Mechanics unchanged.
260705 · `1.5.1`
      Fixed (audit of 1.5.0: pin contract landed in the front half, back half still spoke pre-pin language — the sections a fresh session reads as the operational contract)
      - On-restart reads pins + replies (unanswered pin = surfaced back, never silently skipped); done criteria gain pin-seeded + pin-replied gates; anti-patterns gain clean-file handover + pin-ignoring; Human Actions entry point = walk the pins (not self-service flag hunting); pin targets include _DISPLAY_; report Summary carries a PINS SEEDED line (count + files).
260705 · `1.5.0`
      Added (test-123333333: JL entered 0-seed.md for the CHECK pass and found a clean file — flags lived only in the chat report; JL: "check的时候我需要进去仔细看，然后你加comments 之类的，这些你有做吗")
      - SEED THE PINS (step 2.5, mode-independent): every flagged/🔍/⚠️ report item is planted as ONE `> CHECK:` comment at its exact spot in the working doc (issue + judgment needed, concrete values). Chat report = map, in-file pins = what the human walks; clean-file handover is DEFECTIVE. Human replies `> USER:` per pin; restart reads pins + replies; resolved pins archive to _LOG per the comment lifecycle. Autopilot reviewer reads the pins too.
260704 · `1.4.1`
      Fixed
      - Seed row PROBE check updated: `_DISCOVERY_ takeaways linked` -> `_PROBE/ plan takeaways backfilled + _CITATION_ candidates eyeballable` (naming unification).
260703 · `1.4.0`
      - Gate Modes section added (JL: copilot 人给 comments / autopilot 派 subagent 给 comments，必须有 approval 动作): mode spec owned by 08-stage-gate.md; autopilot dispatches ONE fresh-context reviewer subagent that leaves > REVIEWER: comments + returns proceed|restart|accept; HUMAN-ONLY items (Scholar bibtex verification) are marked DEFERRED into a human queue, never silently passed; humans can reopen agent-approved gates.
      - Stage Exit Invariant added under What Each Decision Does (JL: only check can jump out the current stage): restart re-opens a phase WITHIN the same stage; proceed/accept is the only cross-stage move; cross-stage loopback is a lifecycle re-entry, not a CHECK outcome.
260703 · `1.3.0`
      - renamed haipipe-paper-checker -> haipipe-paper-check. Phase workers are named by the phase verb (draft/probe/revise/check); agent nouns are reserved for sub-tools (proof-checker stays).
260703 · `1.2.0`
      - phase spine renamed DGPC -> DPRC (GATHER->PROBE, POLISH->REVISE); sibling worker names updated; seed check row aligned with the 3-section seed.
260703 · `1.1.0`
      - reframed as internal worker. Users invoke stage skills (seed, claims, pitch...), not this skill directly. Stage skills call this during their CHECK phase.
260702 · `1.0.0`
      - created as the general auto-gate. The former checker was actually a proof-checker (mathematical proofs only); renamed to haipipe-paper-proof-checker and kept as one sub-checker.

<!-- haipipe:skill:log:end -->
