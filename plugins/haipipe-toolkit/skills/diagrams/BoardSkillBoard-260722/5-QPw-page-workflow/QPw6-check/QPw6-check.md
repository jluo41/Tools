# Check: judge the built version, plant each finding where it applies, and route it
state: 🟡 IN PROGRESS · the built-artifact findings run; the semantic pass never dispatched · open: 4
owner: CC
method: separate judging from repairing, then name the eight machine findings and the routes a person's authority is needed for; a pass claim with no visible evidence is a defect here
session: ec8c7879-3e0f-484e-a3fe-b41b1bfb50fc

## Opening
This version is on disk and someone has to say where it goes next, so who judges it and what may they never do?

CHECK is phase ⑦ and the only phase that may CLOSE, which is also why it is the only one forbidden to change what it judges.
It judges the BUILT deliverable rather than the markdown: a declared display unit that never rendered, a cited unit the projection never embedded, and a PDF with no title block are CHECK findings and not cosmetics.
Its risk is becoming a hidden revision, curing its own finding and calling the same version checked, so the fix always runs under another phase and the changed version comes back for a fresh look.
Two hard rules bound it: the actor that produced a version may not be its CHECK actor, and a required human gate without durable passed evidence routes to HOLD rather than CLOSE.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**A route is named for every finding**: "fail" without an owner leaves the next worker guessing, so every defect described here names which of the five routes it takes.
A rule that states a defect without its route is half written.

**Machine and semantic findings are never blurred**: eight findings are computed deterministically and the rest are judgment, and the two have different reliability.
Say which is which every time, because a reader trusts a computed count and must not extend that trust to a judgment.

**The gate belongs to the Page Type, not to this phase**: this page says how a gate is administered and never says which pages have one.
Never invent a gate and never skip a declared one.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram
The four steps, the eight computed findings, the five routes, and the two rules that make a verdict trustworthy.

```text
✅ CHECK · phase ⑦ of 7 · the ONLY phase that may CLOSE
┌─────────────────────────────────────────────────────────────────────────┐
│ reads   the RENDERED page · purpose · Aims · evidence · constraints      │
│ writes  findings · comments · the check record · a proposed ruling       │
│ 🚫 does repair a substantive finding inside the same CHECK pass          │
│    NOT                                                                   │
└─────────────────────────────────────────────────────────────────────────┘

① MECHANICAL  run deterministic checks, preserve their EXACT result
② SEMANTIC    judge function, evidence, readability, local requirements
③ SEED        plant each actionable finding at its page, section,
              sentence, or artifact
④ DECIDE      route using the finding's REQUIRED AUTHORITY

the eight ROUTED findings · src/page_evidence.py · cli/check.py reports
  (the file emits TEN rule ids; display-cited-unit-missing and
   display-counts-split are not in the contract's route table)
  display-declared-no-claim        ─▶ DRAFT
  display-declared-not-rendered    ─▶ REVISE   names the FIRST missing step
  display-intake-unfrozen          ─▶ EVIDENCE
  display-cited-not-embedded       ─▶ REVISE
  display-rendered-not-cited       ─▶ REVISE
  display-accept-stale             ─▶ EVIDENCE
  latex-untitled                   ─▶ REVISE
  projection-stale                 ─▶ REVISE

the five routes
  ✅ CLOSE      the version meets the closing rule
  🧵 REVISE     purpose and Aims stand, realization needs work
  🔎 EVIDENCE   a promised claim has no card behind it
  ✍️ DRAFT      purpose or Aims must reopen, a NEW ROUND
  ⏸ HOLD       a named accepted defect, or parked with a record

two rules that make the verdict worth anything
  the PRODUCER of a version may not be its CHECK actor
  checked_version must equal both version fields, or it is HOLD
```
📌 Only `verdict: pass` may route to CLOSE, and a required human gate with no durable passed evidence routes to HOLD.

## Content

### 1 · CHECK judges and may not repair
**The separation rule**: the only phase that may close is the only one forbidden to change what it judges.

```text
what happens                                     phase
──────────────────────────────────────────────────────────────────
a finding is raised and planted                    CHECK
the same actor then fixes it                       an explicit PHASE
                                                   CHANGE, and the changed
                                                   version is checked AGAIN
the fix ships and nobody re-checks                 the failure this rule
                                                   exists to prevent
```
📌 Mechanical checks may run during every phase; the CHECK phase begins when their results and a semantic judgment are used to route or close a version.

#### 1.1 · The producer of a version may not be its CHECK actor
(a receipt whose producer and judge share an actor identity is a defect, not a shortcut)
Independence here is procedural rather than moral: a fresh actor has not internalized the reasons the version looks finished.
A changed version after REVISE or DRAFT receives another CHECK, and an earlier pass never transfers to it.

#### 1.2 · A version mismatch means hidden mutation and routes to HOLD
(`checked_version` must equal both the before and after version fields)
The version identity is the SHA-256 of the markdown source joined to the SHA-256 of its rendered HTML.
When those disagree with the receipt, something mutated concurrently and no verdict about that version can be trusted, so the route is HOLD rather than a re-run.

### 2 · Judge the BUILT artifact, not only the markdown
**The deliverable rule**: a page that ships a PDF or a docx is judged on what a person opens.

```text
the incident, 260816
  five display units DECLARED
  two reached LaTeX
  nobody was told, because the markdown read fine

three independent counts, and CHECK reads all three
  declared   the unit folder exists
  rendered   a winning asset AND preview.pdf both exist
  accepted   a PERSON ticked the README
  🚫 a version whose declared count exceeds its rendered count does not pass
```
📌 Folder count is never completed work, and the three counts are independent rather than stages of one number.

#### 2.1 · Rendered and unrendered are different defects with different fixes
(a unit can print correctly and still trace back to nothing)
`display-declared-not-rendered` names the FIRST missing step among intake, recipe, asset, and preview, because telling an author to re-run a renderer that already worked is how a checker loses its reader.
`display-intake-unfrozen` is the opposite case: the render is fine and the provenance is missing, so it routes to EVIDENCE rather than REVISE.

#### 2.2 · Step ⑤ ACCEPT is the human gate CHECK administers
(a machine may render, cite, build, and report, and only a person writes `accepted: ✅`)
A changed `intake/` drops that tick back to ⬜, which is the `display-accept-stale` finding.
CHECK never ticks it and never reports a unit as accepted because it looks finished.

### 3 · Put each finding where it applies
**The seeding rule**: a chat report is a map and not the review surface.

```text
the Page Type supports comment lanes   put ONE concrete finding at the exact
                                       location it concerns, and preserve the
                                       reply WITH it
the deliverable must stay clean        use the Page Type's declared ledger or
                                       review surface instead
```
📌 The gate exchange is durable input to whichever phase restarts, so the restarted phase reads each finding together with its reply rather than a summary stripped of the decision context.

#### 3.1 · A pass claim needs visible evidence, not an assertion
(the receipt's `evidence` field carries visible support for every pass claim)
An Aim reported as met with nothing pointed at is the same defect as a number with no card behind it.
This is why a CHECK that finds nothing still writes what it read.

### 4 · Human gates belong to the Page Type, and may never be invented or skipped
**The gate rule**: CHECK administers whatever gate its Page Type declares and assumes none.

```text
a Q decision page      may close when its Aims are met
a Stage page           may require an explicit human ruling
a Skill mirror         may close when its unit ships

a machine MAY   gather evidence · plant comments · propose a ruling ·
                close an answered decision row per the base contract
a machine MAY   claim that a person approved a page when no person did
NEVER
```
📌 A required gate with no durable passed evidence routes to HOLD, which means silence is never consent even when everything else passes.

#### 4.1 · The gate is accept-biased, and that changes what is SHOWN
(JL 260818: "human should be more likely to accept it")
A person is asked to sign only after the computed findings are all zero, so the gate is a confirmation rather than an inspection.
The bias changes the presentation and never the writer: `QPw00g` is the open question of putting all four of the board's human ticks on one pre-cleared surface.

### 5 · CHECK is not necessarily last
**The position rule**: it may appear whenever a concrete version needs judgment.

```text
it may repeat after REVISE
it may open EVIDENCE when a promised claim has no card
it may send the page into a NEW DRAFT ROUND when the promise reopened

the common DRAFT → EVIDENCE → REVISE → CHECK path is a useful route,
not a mandatory sequence
```
📌 Returning to DRAFT creates no new page and no new unit: it starts a new round on the same persistent page.

#### 5.1 · CHECK cannot route to CHECK
(a judged version reaches a second judgment only through a producer)
`QPw00-Display2-route-relation` derives this from the route table rather than asserting it, and it is the rule that keeps the phase from becoming a hidden revision loop.
A second opinion on an unchanged version is not a route; it is the same verdict from a different actor.

## Aims

### Decision Now
- [ ] 🗣 Rule whether WARNINGS may block CLOSE, or only errors may
      📍 `Part` §2, judge the built artifact
      🔔 `Why now` the first live RUN on 260805 recorded that warnings do not gate CLOSE, which leaves the semantic judge as the only defence on a page whose every finding is a WARN, and this board carries 37 warns today
      ⭐ `A ·` keep errors as the only mechanical gate and require the semantic judge to state, in the receipt's evidence field, that it read the warn list: cheap, and it removes the silent path without making a style warn able to block a page
      `B ·` promote a named subset of warns to blocking, which closes the hole mechanically but means a `state-line-long` or an `em-dash` warn can hold a finished page
      🛑 `Blocks` A2.1, and item ⑤ of the 260805 run's own defect list
      🤖 `If nobody answers` A takes effect, because it keeps the existing gate and adds only a reading obligation


### A1 · 👁 CHECK judges and may not repair
- ✅ A1.1 · No receipt on this board shows the same actor as producer and judge of one version.
  Done when a receipt audit over `_runs/page/` finds no shared actor identity across the two roles.
  **Now:** Met. Read from `260805-0216-QB8e`: `role: producer` is `haipipe-board-creator-agent#r1s2` and `#r1s4`; `role: judge` is `haipipe-board-reviewer-agent#r1s1`, `#r1s3`, `#r1s5`. No shared actor identity.
- ✅ A1.2 · Every version mismatch on this board routed to HOLD rather than a re-run.
  Done when every receipt whose `checked_version` disagrees with its version fields carries `route: HOLD`.
  **Now:** Met vacuously. `QPw00r-receipts` is live and the audit surface is `cli/pageflow.py` with `src/page_lifecycle.py`; the one live run carries no version mismatch, so no receipt needed the HOLD route.


### A2 · 📦 Judge the BUILT artifact, not only the markdown
- ⬜ A2.1 · No page on this board passes with a declared count above its rendered count.
  Done when `cli/check.py` reports zero `display-declared-not-rendered` findings.
  **Now:** Not met. `cli/check.py` reports one `display-declared-not-rendered` on `QPf6-Display1-latex-proof` today.
- ✅ A2.2 · Every finding names the first missing step rather than the whole walk.
  Done when every `display-declared-not-rendered` message names one of intake, recipe, asset, or preview.
  **Now:** Met. The finding names the first missing step, and it currently reports `① INTAKE`.


### A3 · 🧩 Put each finding where it applies
- ⬜ A3.1 · No CHECK pass on this board reported only into chat.
  Done when every finding from a dispatched CHECK exists at a page location as well as in its receipt.
  **Now:** Not measurable yet, because the semantic pass has never been dispatched from this board.


### A4 · 🚪 Human gates belong to the Page Type, and may never be invented or skipped
- ✅ A4.1 · No machine has claimed a person's approval on this board.
  Done when every `human_gate.status: passed` in a receipt names a durable tick that exists on disk.
  **Now:** Met so far. No receipt on this board carries a `human_gate.status: passed`, so none has claimed one falsely.
- ⬜ A4.2 · The accept-bias rule is implemented rather than only stated.
  Done when a gate is presented only after `mechanical_errors` for that page is zero.
  **Now:** Not started. The accept-bias rule was ruled on 260818 and nothing presents a gate yet.


### A5 · 🔀 CHECK is not necessarily last
- ✅ A5.1 · No receipt on this board routes CHECK to CHECK.
  Done when a receipt audit finds no CHECK row whose route is CHECK.
  **Now:** Met. `QPw00-Display2-route-relation` derives the no-CHECK-to-CHECK law and no receipt violates it.


## Files
### 📋 Contracts · what CARRIES a rule to other pages
- `page-workflows/haipipe-page-check/SKILL.md`
  The phase contract itself, and the authority on its procedure.
- `haipipe-sentence/SKILL.md`
  The sentence-level lane contract, loaded when findings are planted in comment lanes.
- `agents/haipipe-board-reviewer-agent.md`
  ⚠️ The actor this board dispatches for CHECK, and it holds NO write tool, so the hand that performs step ③ SEED is unnamed. Aim A3.1 is unachievable until it is.
### 🧪 Checks · what CATCHES a page breaking a rule
- `haipipe-board/src/page_evidence.py`
  Computes the built-artifact findings deterministically at step ①. It emits TEN rule ids; the contract's table routes eight of them, and `display-cited-unit-missing` and `display-counts-split` are the two it does not.
- `haipipe-board/cli/check.py`
  Reports them, plus the board's mechanical error and warn counts.
### 📤 Output files · what a BUILD writes
- `board/QPw/QPw6-check.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit it; the markdown is the only source.

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `continues · ALL` · [QPw5 §3](5-QPw-page-workflow/QPw5-revise/QPw5-revise.md)
  The phase that built what this one judges, and the owner of every REVISE route named here.
- `constrained by · ALL` · [QPw00 §10](5-QPw-page-workflow/QPw00-page-loop/QPw00-page-loop.md)
  The audit invariants and the route relation that derives the no-CHECK-to-CHECK law.
- `reads · ALL` · [QPw4 §1](5-QPw-page-workflow/QPw4-evidence/QPw4-evidence.md)
  The three lanes whose exit tests several of these findings re-check on the built artifact.

## Law
- 260816 JL · 📦 **CHECK judges the BUILT artifact**: a page shipping a PDF or docx is judged on what a person opens
  Five declared display units reached LaTeX as two and nobody was told, because the markdown read fine.
  The option rejected was treating build defects as cosmetics for a later cleanup, which loses because the reader finds them first.
- 👁 **CHECK may not repair what it judged**: the fix runs under another phase and the changed version returns for a fresh look
  If the same actor fixes a finding, the work changes phase explicitly and an earlier pass never transfers.
- 🧑 **The producer may not be the judge**: a shared actor identity across the two roles is a defect
  A fresh actor has not internalized the reasons the version looks finished.
- 🚪 **No machine claims a person's approval**: a required gate with no durable passed evidence routes to HOLD
  Silence is never consent, however much else has passed.
- 260818 JL · ✋ **The gate is accept-biased**: a person is asked to sign only after the computed findings are zero
  The bias changes what is presented and never who writes the tick.
- 🔁 **CHECK cannot route to CHECK**: a judged version reaches a second judgment only through a producer
  A second opinion on an unchanged version is the same verdict from a different actor, not a route.

## Glossary
- 👁 **finding**: one concrete defect, planted at the location it concerns, naming the route it takes.
- 📦 **the three counts**: declared, rendered, and accepted, independent of each other, all three read by CHECK.
- 🧭 **checked_version**: the SHA-256 of the markdown source joined to the SHA-256 of its rendered HTML.
- 🚪 **human gate**: the ruling a Page Type declares, administered by CHECK and written only by a person.
- ⏸ **HOLD**: the route for a named accepted defect, a missing gate evidence, or a version mismatch.

## Log
- 260818 · [DRAFT-CC] page created, completing the six phase pages of the loop. Written from `haipipe-page-check`. Five divisions: the judge-may-not-repair separation with its two trust rules, the built-artifact rule with the three independent counts, the seeding of findings at their location, the Page-Type-owned human gate including JL's 260818 accept-bias ruling, and the fact that CHECK is not necessarily last. The eight computed findings are named with their routes in the Diagram and the current live counts are written into States rather than described. One thing the 260805 live RUN raised and nobody has ruled became the Decision Now row: warnings do not gate CLOSE, which leaves the semantic judge as the only defence on a WARN-only page, and this board carries 37 warns today.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0