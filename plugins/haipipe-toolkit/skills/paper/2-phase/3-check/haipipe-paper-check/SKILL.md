---
name: haipipe-paper-check
description: "CHECK phase worker (internal). Called by stage skills as the ONLY human-involved phase in the DPRC lifecycle. DRAFT, PROBE, and REVISE run fully automatic; CHECK is where the human reviews everything at once. Runs automated sub-checkers, produces a unified pass/fail report, then the human verifies and decides. Users invoke stage skills (seed, claims, pitch...), not this skill directly."
argument-hint: "[section-name-or-number] [paper-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent
metadata:
  version: "1.4.0"
  last_updated: "2026-07-03"
  summary: "CHECK phase worker (internal). The ONLY human-involved phase. Called by stage skills to run sub-checkers and gate human review."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
  predecessors:
    - "haipipe-paper-proof-checker (mathematical proof verification) — KEPT as sub-checker, not merged"
---

Skill: haipipe-paper-check (internal phase worker)
=====================================================

CHECK phase worker. Called by stage skills as the auto-gate for the DPRC lifecycle. **CHECK is the ONLY judgment-involved phase.** DRAFT, PROBE, and REVISE run fully automatic without stopping for input. CHECK is where everything is reviewed at once -- by the human (copilot mode, default) or by a reviewer subagent standing in (autopilot mode; see Gate Modes below).

**Not user-facing.** Users invoke stage skills:
```
/haipipe-paper claims        → claims skill calls this internally for CHECK phase
/haipipe-paper pitch         → pitch skill calls this internally for CHECK phase
/haipipe-paper section-edit §3  → section-edit skill calls this internally
```

The check has two parts:
1. **MECHANICAL** -- the agent runs automated sub-checkers and produces a pass/fail report
2. **HUMAN** -- the human verifies flagged items, adds `> USER:` comments, and decides: proceed, restart, or accept

On restart, the restarted phase (DRAFT, PROBE, or REVISE) reads `> USER:` comments from CHECK and responds to them.


## How It Works

```
┌──────────┐     ┌──────────────┐     ┌──────────────────────────┐
│ 🤖 RUN   │────▶│ 📋 REPORT    │────▶│ 🧑 HUMAN REVIEW          │
│ CHECKERS │     │ pass/fail    │     │                          │
└──────────┘     └──────────────┘     │ 1. verify 🔍 citations   │
                                      │ 2. copy bibtex → .bib    │
                                      │ 3. confirm flagged values │
                                      │ 4. review displays        │
                                      │ 5. add > USER: comments     │
                                      │ 6. decide                 │
                                      └──────────┬───────────────┘
                                                  │
                       ┌──────────────────────────┼──────────────┐
                       ▼                          ▼              ▼
                 ✅ ALL PASS                ♻️ RESTART        🤷 ACCEPT
                 section done               agent re-runs     with known
                                            phase, reads      issues
                                            > USER: comments
```

1. **Run**: execute all applicable sub-checkers mechanically
2. **Report**: present results as a structured pass/fail table
3. **Human review**: the human verifies flagged items, copies bibtex to .bib, confirms values, reviews displays, adds `> USER:` comments
4. **Decide**: proceed / restart / accept / park
5. **On restart**: the restarted phase (DRAFT/PROBE/REVISE) reads `> USER:` comments from CHECK and responds to them


## Gate Modes (copilot | autopilot)

Mode spec is owned by `../../../wiki/08-stage-gate.md` (`gate_mode` in STATUS.md, default copilot). What changes INSIDE this worker:

```
🧑 copilot     steps 3-4 above run as written: the human reviews and decides.
🤖 autopilot   after the mechanical report, dispatch ONE fresh-context reviewer subagent
               (Agent tool) that plays the review seat:
               - reads the stage artifact + the pass/fail report + exit criteria
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
| USER comments resolved | each `> USER:` has a `> CC:` response below it | no orphan USER comments |

### 📚 PROBE checks

These verify the three probe tracks (citation/values/display) are complete. Since PROBE runs automatically, some items require human action during CHECK.

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
- Add `> USER:` comments on layout/labeling revisions
- On restart, agent re-routes failed tasks

### 💎 REVISE checks

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
| proof checker passes | dispatch to haipipe-paper-proof-checker | verdict PASS or WARN |

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

## 📚 PROBE
  ✅ citation density: 0.41 (norm ≥ 0.25)
  ❌ 2 🔍 candidates unverified (Eddy 1984, Deyo 2015)
  ✅ no ⚠️ citation issues
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
```


## What Each Decision Does

```
✅ PROCEED         this stage is done → advance to the next lifecycle stage
                   section-edit: check done → section complete, move to next section or build-submit
                   claims: check done → pin venue → pitch
                   pitch: check done → narrative

♻️ RESTART         a specific phase has failures → loop back to fix
                   "restart from PROBE" = re-run probe workers, then re-check
                   "restart from DRAFT" = revise outline, then re-probe, re-revise, re-check
                   the restart target determines how much rework happens

🔄 NEW ROUND       artifacts are OK but could be deeper → run another full DPRC cycle
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

**Stage Exit Invariant: CHECK is the ONLY door out of a stage.** Its verdicts move in exactly two directions: ♻️ restart re-opens a PHASE within the SAME stage (DRAFT / PROBE / REVISE -- never another stage); ✅ proceed (or 🤷 accept) crosses the gate to the NEXT stage. Going BACK across stages (e.g. redoing seed while the frontier is section-edit) is NOT a CHECK outcome -- that is a lifecycle loopback: re-enter the earlier stage (🔥 moves there, 🚀 stays at the frontier), and it runs its own DPRC and its own CHECK gate.


## Human Actions During CHECK

CHECK is the ONLY human-involved phase. DRAFT, PROBE, and REVISE run fully automatic. Everything the human needs to do happens here:

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
5. Add `> USER:` comments with corrections or decisions

### Display review

1. Review generated display outputs (figures, tables) linked to the section
2. Check that each display's content matches the claim it supports
3. Check that numbers in displays match _VALUES_ entries
4. Add `> USER:` comments on layout, labeling, content, or revisions needed
5. Flag any pending/failed displays that need task re-runs

### General review

1. Read the CHECK report (pass/fail summary)
2. Review any ⚠️ warnings
3. Add `> USER:` comments anywhere in the outline, _CITATION_, _VALUES_, or tex
4. Decide: proceed / restart from a phase / accept with issues / park

### On restart

When the human decides to restart from a phase (e.g., "restart from PROBE"):
- The agent re-runs that phase
- The agent reads ALL `> USER:` comments added during CHECK and responds to them
- For DRAFT restarts: the agent revises the outline based on `> USER:` feedback
- For PROBE restarts: the agent re-audits, places newly verified keys from .bib, searches for new candidates per `> USER:` requests
- For REVISE restarts: the agent re-applies prose quality rules, addressing `> USER:` style concerns; each change carries a why-comment


## Applicability Beyond Section-Edit

This checker pattern works for ANY lifecycle stage that follows DRAFT→PROBE→REVISE→CHECK. For non-section-edit stages:

| Stage | DRAFT checks | PROBE checks | REVISE checks | META checks |
|---|---|---|---|---|
| seed | 3 sections filled (question/motivations/claim shape) | _DISCOVERY_ takeaways linked (if probe ran) | seed is readable | ready to advance to claims |
| claims | H1/H2/H3 listed | all claims linked to evidence | claims well-stated | no unsupported GAPs |
| pitch | cover letter drafted | venue pack consulted | readability rules pass | Editor's Chair Test |
| narrative | design contract drafted | claims linked to beats | arc/flow coherent | all beats [READY] |
| display | display plan exists | all displays generated | visual quality | all linked in tex |

When invoked for a non-section-edit stage, the checker reads the stage's SKILL.md to discover what its done-gate criteria are, then checks those criteria mechanically.


## Relation to sibling

```
3-check/
  haipipe-paper-check/         ← THIS (auto-gate orchestrator)
  haipipe-paper-proof-checker/   ← sub-checker (math proofs only)
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
- [ ] If restart: agent re-runs phase reading > USER: comments, then re-checks
- [ ] _LOG updated with check result + human actions taken


## Anti-patterns

- ❌ Skipping the report and declaring "checks pass" without running them
- ❌ Running only one sub-checker and calling it done
- ❌ Auto-proceeding without human decision on failures
- ❌ Treating warnings as failures (warnings are informational)
- ❌ Using the proof-checker as the general checker (it's one sub-check)
- ❌ Stopping for human input during DRAFT, PROBE, or REVISE (those are fully automatic; CHECK is the ONLY human gate)
- ❌ Generating bibtex during CHECK (human copies from Scholar; agent never generates bibtex)
- ❌ Putting bibtex in _CITATION_ or any markdown (bibtex lives ONLY in .bib)
- ❌ Ignoring > USER: comments on restart (the restarted phase must read and respond to them)


## Who calls this skill

Stage skills call this as their CHECK phase:

| Stage skill | What this skill checks |
|---|---|
| haipipe-paper-seed | seed.md done-gate (promotion criteria) |
| haipipe-paper-claims | hypothesis list + evidence linkage |
| haipipe-paper-pitch | cover letter (Editor's Chair Test, readability) |
| haipipe-paper-narrative | story beats (all [READY], arc/flow coherence) |
| haipipe-paper-display | display plan (all units generated, linked in tex) |
| haipipe-paper-section-edit | section outline + tex (full DPRC check: draft + probe + revise + meta + proof) |

## Sibling phase workers

| Phase | Worker | Called after |
|---|---|---|
| DRAFT | haipipe-paper-draft | -- |
| PROBE | haipipe-paper-probe | DRAFT |
| REVISE | haipipe-paper-revise | PROBE |
| CHECK (this) | haipipe-paper-check | REVISE |
