---
name: haipipe-paper-section-edit-checker
description: "CHECK phase auto-gate for section-edit. The ONLY human-involved phase in the DGPC lifecycle. DRAFT, GATHER, and POLISH run fully automatic; CHECK is where the human reviews everything at once. Runs automated sub-checkers across all phases (draft, gather, polish, meta, proof), produces a unified pass/fail report. Human then: verifies 🔍 citation candidates on Scholar, copies bibtex to .bib, confirms flagged values against source, reviews generated displays, adds > JL: comments, and decides (proceed / restart / accept). On restart, the restarted phase reads > JL: comments. Trigger: check, check section, auto-check, run checkers, gate, verification, /haipipe-paper-section-edit-checker."
argument-hint: "[section-name-or-number] [paper-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent
metadata:
  version: "1.0.0"
  last_updated: "2026-07-02"
  summary: "CHECK phase auto-gate. The ONLY human-involved phase. Runs sub-checkers → unified report → human verifies 🔍 citations/values/displays, copies bibtex to .bib, adds > JL: comments → decides restart or proceed. On restart, restarted phase reads > JL: comments."
  changelog:
    - "1.0.0 (2026-07-02): created as the general auto-gate. The former checker was actually a proof-checker (mathematical proofs only); renamed to haipipe-paper-section-edit-proof-checker and kept as one sub-checker."
  predecessors:
    - "haipipe-paper-section-edit-proof-checker (mathematical proof verification) — KEPT as sub-checker, not merged"
---

Skill: haipipe-paper-section-edit-checker
=========================================

CHECK phase auto-gate for the section-edit lifecycle. **CHECK is the ONLY human-involved phase.** DRAFT, GATHER, and POLISH run fully automatic without stopping for human input. CHECK is where the human reviews everything at once.

The check has two parts:
1. **MECHANICAL** -- the agent runs automated sub-checkers and produces a pass/fail report
2. **HUMAN** -- the human verifies flagged items, adds `> JL:` comments, and decides: proceed, restart, or accept

On restart, the restarted phase (DRAFT, GATHER, or POLISH) reads `> JL:` comments from CHECK and responds to them.

```
/haipipe-paper-section-edit-checker <section>           run all checkers, produce report
/haipipe-paper-section-edit-checker <section> draft     run only draft checks
/haipipe-paper-section-edit-checker <section> gather    run only gather checks
/haipipe-paper-section-edit-checker <section> polish    run only polish checks
/haipipe-paper-section-edit-checker <section> meta      run only meta checks
/haipipe-paper-section-edit-checker <section> proof     run only proof checks (if section has proofs)
```


## How It Works

```
┌──────────┐     ┌──────────────┐     ┌──────────────────────────┐
│ 🤖 RUN   │────▶│ 📋 REPORT    │────▶│ 🧑 HUMAN REVIEW          │
│ CHECKERS │     │ pass/fail    │     │                          │
└──────────┘     └──────────────┘     │ 1. verify 🔍 citations   │
                                      │ 2. copy bibtex → .bib    │
                                      │ 3. confirm flagged values │
                                      │ 4. review displays        │
                                      │ 5. add > JL: comments     │
                                      │ 6. decide                 │
                                      └──────────┬───────────────┘
                                                  │
                       ┌──────────────────────────┼──────────────┐
                       ▼                          ▼              ▼
                 ✅ ALL PASS                ♻️ RESTART        🤷 ACCEPT
                 section done               agent re-runs     with known
                                            phase, reads      issues
                                            > JL: comments
```

1. **Run**: execute all applicable sub-checkers mechanically
2. **Report**: present results as a structured pass/fail table
3. **Human review**: the human verifies flagged items, copies bibtex to .bib, confirms values, reviews displays, adds `> JL:` comments
4. **Decide**: proceed / restart / accept / park
5. **On restart**: the restarted phase (DRAFT/GATHER/POLISH) reads `> JL:` comments from CHECK and responds to them


## Sub-Checkers

Five groups of checks. Each group maps to a phase. Checks that don't apply to a section are marked `-- skipped` (e.g., proof checks for a section without proofs, values checks for a section without numbers).

### 📝 DRAFT checks

These verify the outline is well-formed.

| Check | How to verify | Pass condition |
|---|---|---|
| structure block exists | grep for ``` block with ¶ counts in outline .md | block present with counts |
| all ¶ have headlines | each `### P#.` heading has text after it | no empty headings |
| all ¶ have previews | each ¶ heading has a `(parenthetical preview)` below it | no missing previews |
| draft sentences present | each ¶ block has sentences (not just heading + preview) | ≥1 sentence per ¶ |
| sentence counts in range | count sentences per ¶ vs venue norm (e.g., 5-7 for MISQ) | all within range or flagged ⚠️ |
| JL comments resolved | each `> JL:` has a `> CC:` response below it | no orphan JL comments |

### 📚 GATHER checks

These verify the three gather tracks are complete. Since GATHER runs automatically, some items require human action during CHECK.

**Citation:**

| Check | How to verify | Pass condition |
|---|---|---|
| density meets venue norm | count cited sentences / total sentences in _CITATION_ | ratio ≥ venue threshold |
| 🔍 candidates listed | grep _CITATION_ for `🔍` status entries | ⚠️ if any remain (human verifies during CHECK) |
| no ⚠️ remaining | grep _CITATION_ for `⚠️` status entries | zero ⚠️ entries |
| all factual assertions cited | compare outline factual sentences vs cited sentences | no uncited factual claims |
| all \cite{key} in .bib | grep tex for \cite, check each key in .bib | zero broken refs |
| no bibtex in _CITATION_ | grep _CITATION_ for `@article`, `@inproceedings`, etc. | zero bibtex blocks (bibtex lives ONLY in .bib) |

**Citation: human action during CHECK:**
- Click Scholar links for 🔍 entries, verify papers exist and support assertions
- Copy bibtex from Scholar to `.bib` (the agent NEVER generates bibtex)
- Mark verified: `> ✅ SEARCH:` / rejected: `> ❌ SEARCH: reason`
- On restart, agent auto-places newly verified keys

**Values:**

| Check | How to verify | Pass condition |
|---|---|---|
| all numbers in _VALUES_ | compare numbers in tex vs entries in _VALUES_ | all tracked |
| ⚠️ mismatches listed | grep _VALUES_ for `⚠️` | ⚠️ if any remain (human confirms during CHECK) |
| 🔍 unknown sources listed | grep _VALUES_ for `🔍` | ⚠️ if any remain (human locates during CHECK) |
| method claims checked | grep _VALUES_ for `❌` method claims | ⚠️ if any remain (human confirms during CHECK) |

**Values: human action during CHECK:**
- For ⚠️ entries: check source file, confirm which number is correct
- For 🔍 entries: locate the source the agent could not find
- For ❌ method claims: confirm implementation or decide to drop
- On restart, agent re-traces with human-provided corrections

**Display:**

| Check | How to verify | Pass condition |
|---|---|---|
| all needed displays linked | check \ref{fig/tab} in tex resolve to 0-displays/ | all resolve |
| no missing displays | compare narrative display needs vs linked units | all covered |
| pending displays listed | check for ungenerated/failed task outputs | ⚠️ if any remain |

**Display: human action during CHECK:**
- Review generated display outputs for correctness
- Confirm display content matches supporting claims
- Add `> JL:` comments on layout/labeling revisions
- On restart, agent re-routes failed tasks

### 💎 POLISH checks

These verify prose quality.

| Check | How to verify | Pass condition |
|---|---|---|
| no AI voice patterns | grep for common AI tells (Furthermore, Moreover, delve, utilize, underscore, landscape, tapestry) | zero matches (or flagged ⚠️) |
| no em-dashes | grep for `---` or `—` | zero matches |
| Pn.Sn markers sequential | parse `%% ---- Pn.Sn ----` markers, check sequence | sequential within each ¶ |
| sentence count matches | count Pn.Sn markers vs outline sentence count | counts match |
| outline ↔ tex synced | compare outline sentences vs tex sentences | content matches |
| banner points match content | read each `% Para [X.P#]` and verify the ¶ below matches | all match |

### 📐 META checks

These verify whole-section integrity.

| Check | How to verify | Pass condition |
|---|---|---|
| terms consistent | grep for term variants (e.g., "clinical ambiguity" vs "clinical uncertainty") | one term per concept |
| claims traceable | each claim sentence has either a citation or is "our study" framing | no unsupported claims |
| \label/\ref resolve | run check_refs.py or grep-based cross-check | zero broken refs |
| compiles clean | run ./1-compile.sh, check for errors | zero LaTeX errors |
| no TODO markers | grep for `TODO`, `FIXME`, `XXX` in tex | zero matches |

### 🔬 PROOF checks

Only runs if the section contains `\begin{proof}`, `\begin{theorem}`, or `\begin{lemma}`.

| Check | How to verify | Pass condition |
|---|---|---|
| proof checker passes | dispatch to haipipe-paper-section-edit-proof-checker | verdict PASS or WARN |

When proof checks are needed, the checker dispatches to the proof-checker skill (sibling in 3-check/) via Agent tool. The proof-checker produces its own detailed report; the checker extracts the verdict.


## Report Format

```markdown
# CHECK REPORT: §N Section-Name
# Date: YYYY-MM-DD

## Summary
PASSED: NN   FAILED: NN   WARNING: NN   SKIPPED: NN

## 📝 DRAFT
  ✅ structure block present (6 ¶)
  ✅ all ¶ have headlines + previews
  ✅ draft sentences: 38 total
  ⚠️ P2 has 8 sentences (venue norm: 5-7)

## 📚 GATHER
  ✅ citation density: 0.41 (norm ≥ 0.25)
  ❌ 2 🔍 candidates unverified (Eddy 1984, Deyo 2015)
  ✅ no ⚠️ citation issues
  -- values: skipped (no numbers in this section)
  -- display: skipped (no displays in this section)

## 💎 POLISH
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

1. GATHER/citation: 2 🔍 candidates unverified
   → recommend: restart from GATHER/citation (verify on Scholar)
   → OR: accept (defer verification)

## ⚠️ WARNING items

1. DRAFT: P2 has 8 sentences (venue norm 5-7)
   → informational, not blocking

## 🧑 Decision

- [ ] ✅ PROCEED to next lifecycle stage (all critical items pass)
- [ ] ♻️ RESTART this stage from: _____ (DRAFT / GATHER / POLISH) — fix issues, re-check
- [ ] 🔄 NEW ROUND of this stage (keep artifacts, run another DGPC cycle to deepen)
- [ ] 🤷 ACCEPT with known issues (log what's deferred)
- [ ] ⏸️ PARK this section (switch to another section, come back later)
```


## What Each Decision Does

```
✅ PROCEED         this stage is done → advance to the next lifecycle stage
                   section-edit: check done → section complete, move to next section or build-submit
                   claims: check done → pin venue → pitch
                   pitch: check done → narrative

♻️ RESTART         a specific phase has failures → loop back to fix
                   "restart from GATHER" = re-run gather workers, then re-check
                   "restart from DRAFT" = revise outline, then re-gather, re-polish, re-check
                   the restart target determines how much rework happens

🔄 NEW ROUND       artifacts are OK but could be deeper → run another full DGPC cycle
                   keeps all existing artifacts, adds a new round of refinement
                   e.g., first round drafted 5 sentences per ¶ → new round adds detail
                   logged as round N+1 in _LOG

🤷 ACCEPT          some checks failed but the human decides they're not blocking
                   failures are logged as "accepted issues" in _LOG
                   the section can proceed but the issues travel with it

⏸️ PARK            this section needs something that isn't ready yet
                   e.g., waiting for a probe to return, or a co-author decision
                   switch to another section, come back when the blocker resolves
```

The decision is recorded in the _LOG with the check report, so future sessions know what was decided and why.


## Human Actions During CHECK

CHECK is the ONLY human-involved phase. DRAFT, GATHER, and POLISH run fully automatic. Everything the human needs to do happens here:

### Citation verification

1. Open _CITATION_ and find all 🔍 entries (agent-found candidates not yet in .bib)
2. Click the `> SEARCH: [Scholar](url)` link for each 🔍 entry
3. Read the paper abstract, confirm it supports the assertion stated in _CITATION_
4. On Scholar, click the cite icon (`"`), select BibTeX, copy the bibtex block
5. Paste the bibtex into the `.bib` file (bibtex lives ONLY in .bib, never in _CITATION_ or markdown)
6. In _CITATION_, change `> SEARCH:` to `> ✅ SEARCH:`
7. For wrong/irrelevant papers: change to `> ❌ SEARCH: reason`

**The agent NEVER generates bibtex. The human copies bibtex from Google Scholar into .bib. No bibtex block ever appears in _CITATION_.**

### Values verification

1. Open _VALUES_ and find all ⚠️ (mismatch) and 🔍 (source unknown) entries
2. For ⚠️ entries: check the source file, confirm which number is correct (prose or source)
3. For 🔍 entries: locate the source file the agent could not find
4. For ❌ method claims: confirm the method is implemented or decide to drop the claim
5. Add `> JL:` comments with corrections or decisions

### Display review

1. Review generated display outputs (figures, tables) linked to the section
2. Check that each display's content matches the claim it supports
3. Check that numbers in displays match _VALUES_ entries
4. Add `> JL:` comments on layout, labeling, content, or revisions needed
5. Flag any pending/failed displays that need task re-runs

### General review

1. Read the CHECK report (pass/fail summary)
2. Review any ⚠️ warnings
3. Add `> JL:` comments anywhere in the outline, _CITATION_, _VALUES_, or tex
4. Decide: proceed / restart from a phase / accept with issues / park

### On restart

When the human decides to restart from a phase (e.g., "restart from GATHER"):
- The agent re-runs that phase
- The agent reads ALL `> JL:` comments added during CHECK and responds to them
- For DRAFT restarts: the agent revises the outline based on `> JL:` feedback
- For GATHER restarts: the agent re-audits, places newly verified keys from .bib, searches for new candidates per `> JL:` requests
- For POLISH restarts: the agent re-applies prose quality rules, addressing `> JL:` style concerns


## Applicability Beyond Section-Edit

This checker pattern works for ANY lifecycle stage that follows DRAFT→GATHER→POLISH→CHECK. For non-section-edit stages:

| Stage | DRAFT checks | GATHER checks | POLISH checks | META checks |
|---|---|---|---|---|
| seed | seed.md exists, evidence needs listed | probe plans created for gaps | seed is readable | promotion gate criteria |
| claims | H1/H2/H3 listed | all claims linked to evidence | claims well-stated | no unsupported GAPs |
| pitch | cover letter drafted | venue pack consulted | readability rules pass | Editor's Chair Test |
| narrative | design contract drafted | claims linked to beats | arc/flow coherent | all beats [READY] |
| display | display plan exists | all displays generated | visual quality | all linked in tex |

When invoked for a non-section-edit stage, the checker reads the stage's SKILL.md to discover what its done-gate criteria are, then checks those criteria mechanically.


## Relation to sibling

```
3-check/
  haipipe-paper-section-edit-checker/         ← THIS (auto-gate orchestrator)
  haipipe-paper-section-edit-proof-checker/   ← sub-checker (math proofs only)
```

The checker CALLS the proof-checker when needed. The proof-checker never runs alone as the CHECK phase gate.


## Done criteria

CHECK phase is done when:
- [ ] All sub-checkers have run
- [ ] Report produced and presented to human
- [ ] Human has verified 🔍 citation candidates (or deferred)
- [ ] Human has confirmed flagged values (or deferred)
- [ ] Human has reviewed generated displays (or deferred)
- [ ] Human has decided: proceed / restart / accept
- [ ] If restart: agent re-runs phase reading > JL: comments, then re-checks
- [ ] _LOG updated with check result + human actions taken


## Anti-patterns

- ❌ Skipping the report and declaring "checks pass" without running them
- ❌ Running only one sub-checker and calling it done
- ❌ Auto-proceeding without human decision on failures
- ❌ Treating warnings as failures (warnings are informational)
- ❌ Using the proof-checker as the general checker (it's one sub-check)
- ❌ Stopping for human input during DRAFT, GATHER, or POLISH (those are fully automatic; CHECK is the ONLY human gate)
- ❌ Generating bibtex during CHECK (human copies from Scholar; agent never generates bibtex)
- ❌ Putting bibtex in _CITATION_ or any markdown (bibtex lives ONLY in .bib)
- ❌ Ignoring > JL: comments on restart (the restarted phase must read and respond to them)
