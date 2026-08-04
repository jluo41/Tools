---
name: haipipe-paper-check
description: "CHECK phase worker (internal). Called as a stage's declared human gate. All current paper stages declare one gate here; earlier declared phases run unattended. Runs automated sub-checkers, seeds in-file CHECK comments, and presents the approval or restart decision."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent
metadata:
  version: "0.3.5"
  last_updated: "2026-07-26"
  summary: "CHECK phase worker (internal) -- the LAST human gate of a stage, and by default its ONLY one: runs the deterministic sub-checkers (./checks.sh), seeds `> CHECK:` comments in-file at every flag site, and gates human review. Its compile option follows the canonical 2-src build or an explicit tex target. What it walks is the stage doc plus its nested S03/S04 entries. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-check (internal phase worker)
=====================================================

CHECK phase worker.
Called by stage skills as the gate at the end of their declared phase sequence.
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


## How It Works

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


## Locating the probe checker

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


## Gate Modes (copilot | autopilot)

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


## Sub-Checkers

Five groups of checks, one per phase (+ META, + PROOF).
Checks that don't apply to a section are marked `-- skipped` (e.g., proof checks for a section without proofs, values checks for a section without numbers).

The deterministic text-match rows below are runnable in one shot: `./checks.sh <tex-or-paper-dir> --md <stage-doc-or-section.md> --md <nested-entry.md>`.
The judgment rows (does the citation SUPPORT the claim, is the VALUE traceable, does the DISPLAY match) are human/reviewer work and are described once under **Human Actions During CHECK** -- the tables here only say what gets flagged, not how the human resolves it.

### 📝 DRAFT checks — verify the outline is well-formed

| Check | How to verify | Pass condition |
|---|---|---|
| structure block exists | grep for ``` block with ¶ counts in outline .md | block present with counts |
| all ¶ have headlines | each `### P#.` heading has text after it | no empty headings |
| all ¶ have previews | each ¶ heading has a `(parenthetical preview)` below it | no missing previews |
| draft sentences present | each ¶ block has sentences (not just heading + preview) | ≥1 sentence per ¶ |
| sentence counts in range | count sentences per ¶ vs venue norm (e.g., 5-7 for MISQ) | all within range or flagged ⚠️ |
| USER comments resolved | each `> USER:` has a `> CC:` response below it | no orphan USER comments |

### 📚 PROBE checks — verify every OWNED hole landed its answer

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

### 💎 REVISE checks — verify prose quality

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

### 📐 META checks — verify whole-section integrity

| Check | How to verify | Pass condition |
|---|---|---|
| terms consistent | grep for term variants (e.g., "clinical ambiguity" vs "clinical uncertainty") | one term per concept |
| claims traceable | each claim sentence has either a citation or is "our study" framing | no unsupported claims |
| \label/\ref resolve | `./checks.sh` (broken \ref + orphan \label) | zero broken refs (orphans ⚠️) |
| compiles clean | `./checks.sh --compile` (wraps ./2-src/compile.sh) | zero LaTeX errors |
| no TODO markers | `./checks.sh` (TODO/FIXME/XXX) | zero matches |

### 🔬 PROOF checks — only if the section has proofs

Runs only if the section contains `\begin{proof}`, `\begin{theorem}`, or `\begin{lemma}`.

| Check | How to verify | Pass condition |
|---|---|---|
| proof checker passes | dispatch to haipipe-paper-proof-checker (Agent tool) | verdict PASS or WARN |

The proof-checker (sibling in 3-check/) produces its own detailed report; this checker extracts the verdict.
See Relation to sibling.

### 📚 EVIDENCE checks — only when the run is pre-submission

Runs only when the gate is being opened ahead of a submission, not at an ordinary per-section gate. Resolving every DOI at every section gate is unaffordable, and a pass too expensive to run is a pass that silently never runs.

| Check | How to verify | Pass condition |
|---|---|---|
| evidence walk passes | dispatch to haipipe-paper-check-evidence (Agent tool) | verdict PASS or WARN |

Three axes, each failing differently: every cited work EXISTS, its metadata is right, and it actually supports the sentence citing it; every number RE-DERIVES from its source; every display matches its claim and renders clean in the compiled PDF.

Report-only, like the proof-checker: it seeds `> CHECK:` comments at the exact spot and never edits prose. Fixes route back through REVISE. An item the human declines to fix becomes a `{CONCERN:<risk>} [Q-<Stage>-<n>]` so it stays visible at every later gate rather than evaporating.

FAIL is reserved for the two that block a submission outright: a citation to a paper that does not exist, and a number that cannot be re-derived from any named source.


## Report Format

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


## Human Actions During CHECK

CHECK is where every human action in the lifecycle happens.
The entry point is the `> CHECK:` comments: open the working docs the report's CHECK COMMENTS SEEDED line names and walk them -- each flagged item below is anchored by one, so the pass is guided, not a self-service hunt.
Reply `> USER:` under each as you go (plus any free `> USER:` comments of your own).

### Citation verification

1. Open the nested entries the report names and find all 🔍 sources in their `#### a-executor` bodies (harvested candidates not yet in .bib)
2. Click the `> SEARCH: [Scholar](url)` link for each 🔍 source
3. Read the paper abstract, confirm it supports what the `#### a-executor` says the source establishes
4. On Scholar, click the cite icon, select BibTeX, copy the bibtex block
5. Paste the bibtex into the `.bib` file
6. In the entry, mark verified `> ✅ SEARCH:` / rejected `> ❌ SEARCH: reason`
7. On restart, the agent places newly verified keys into the `\cite{TOADD} [Q-<Stage>-<n>]` holes that own them

**The agent NEVER generates bibtex — the human copies it from Scholar into `.bib`.
Bibtex lives ONLY in `.bib`, never in a probe entry or any markdown.**

### Values verification

1. Open the nested entries the report names and find all ⚠️ (mismatch) and 🔍 (source unknown) values in their `#### a-executor` bodies
2. For ⚠️ values: open the source path the `#### a-executor` names, confirm which number is correct (prose or source)
3. For 🔍 values: locate the source the agent could not find
4. For ❌ method claims: confirm the method is implemented or decide to drop the claim
5. Add `> USER:` comments with corrections or decisions; on restart the agent re-traces

### Display review

1. Review generated display outputs (figures, tables) linked to the section
2. Check that each display's content matches the claim it supports
3. Check that numbers in displays match the values harvested in the entries' `#### a-executor` bodies
4. Add `> USER:` comments on layout, labeling, content, or revisions needed
5. Flag any DR row in `0-lifecycle/3-display/_DISPLAY_REQUEST.md` still short of `done`; on restart the agent re-routes it

### Decide

1. Read the CHECK report (pass/fail summary + CHECK COMMENTS SEEDED line), review any ⚠️ warnings
2. Confirm every `> CHECK:` comment has a `> USER:` reply
3. Decide: proceed / restart from a phase / new round / accept with issues / park

### On restart

When the human restarts from a phase (e.g., "restart from PROBE"):
- The agent re-runs that phase and reads ALL `> CHECK:` comments with their `> USER:` replies, plus every free `> USER:` comment, and responds to each (a `> CHECK:` comment with no reply is surfaced back to the human, never silently skipped)
- DRAFT restart: revise the outline per `> USER:` feedback
- PROBE restart: re-audit, place newly verified keys from .bib into the holes that own them (in the .md, then sync); new-candidate requests from `> USER:` comments become nested topic entries, dispatched by the PROBE phase (never inline search)
- REVISE restart: re-apply prose quality rules addressing `> USER:` style concerns; each change carries a why-comment


## Applicability Beyond Section-Edit

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


## Relation to sibling

```
3-check/
  haipipe-paper-check/           ← THIS (auto-gate orchestrator)
  haipipe-paper-proof-checker/   ← sub-checker (math proofs only)
```

The checker CALLS the proof-checker when needed.
The proof-checker never runs alone as the CHECK phase gate.


## Done criteria

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


## Who calls this skill

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

## Sibling phase workers

| Phase | Worker | Called after |
|---|---|---|
| DRAFT | haipipe-paper-draft | -- |
| PROBE | haipipe-paper-probe | DRAFT |
| REVISE | haipipe-paper-revise | PROBE |
| CHECK (this) | haipipe-paper-check | REVISE |
