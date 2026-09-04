---
name: haipipe-design-workflow
description: >-
  The DesignBoard phase machine over six phase-owned Folder kinds: D0 Brief →
  D1 Card → D2 Unit → D3 Verdict → D4 Division → D5 PageDown. Owns GD0-GD6,
  thread/round frontier, dispatch, receipts, and stops; each phase skill owns
  both Folder faces and its plugins. Accepts a one-sentence commission and
  always closes a round through accept, emit, kill, or carry. Trigger: design
  workflow, design round, commission a design, frontier thread,
  /haipipe-design-workflow.
metadata:
  version: "1.0.3"
  last_updated: "2026-08-31"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-design-workflow · know the thread, test the gate, close the round

Load `haipipe-design` and `haipipe-folder` first. This is the only authority
for D0-D5 ordering and GD0-GD6. `haipipe-application-workflow` may delegate
here and record a crossing, but owns no aliases or duplicate gates. The
selected phase skill owns the Folder; Page-Face work delegates to
`haipipe-page-workflow`.

## 🔤 Terminology law

A **design phase** is one digit, `D0`-`D5`. A Design Page id carries two
digits (`DS01`), so it cannot be confused with the phase. Frame, bet, realize,
evaluate, decide, and page down are prose aliases only. PageDown is one word
and names the phase-owned cross-Folder truth pass.

Each phase is named by its owned Folder/artifact kind: Brief, Card, Unit,
Verdict, Division, or PageDown. One DS Folder hosts many threads, but each
thread artifact still has a phase contract with Page and Task faces. A position
without its own kind is a gate or Task-Face act, which keeps acceptance at GD5
and EMIT as an edge rather than another phase.

D1-D3 are three sequential identities of one physical DU Folder, not three
directories. Its address stays fixed; its one current `folder-kind` advances
`design-card → design-unit → design-verdict`, and `workflow/phase.yaml` keeps
append-only transitions, including any D3 → D2 repair edge. D4 belongs to the
parent DS Folder. D5 owns a minimal round-receipt Folder because a cross-Folder
truth pass still needs an address, two faces, and a testable seal.

**Two evaluation words, one alias law, one on-disk word.** The working words are plain — `reflect` and `prospect` — and each carries its literature name as a parenthesized alias: **reflect (ex-post)** appraises the artifact against evidence that exists; **prospect (ex-ante)** reasons forward to what will happen in use. Reflect is PERFORMED by the door's `judge` verb, and its on-disk state word is `judged` — one act, three views of it. Prospect's on-disk surface is the unit's `prospect.md`.

## 🗺 The six phases · the phases are the wager's stations

The insight lane's aliases are verbs of KNOWING (scope, ask, observe, derive, claim, hand off); this lane's are verbs of WAGERING, then one of HOUSEKEEPING — frame, bet, realize, evaluate, decide, page down (JL's word: the round's record finally SET DOWN on the page, whole and readable):

```text
phase                    authority artifact            what the phase produces
──────────────────────────────────────────────────────────────────────────────
D0 Brief (frame)         0-BR-brief/BR00 page          the frame: opportunity, audience,
                                                       outcome + kill, venue scope,
                                                       promise, needs OUT · the roster
D1 Card (bet)            design/DU<NN>-<slug>/card.md  the bets: stance · thesis ·
                                                       expected effect (the PRIOR) ·
                                                       falsification line · grant
D2 Unit (realize)        the same folder, grown         the artifact, complete: README ·
                                                       spec · evidence ⊆ grant ·
                                                       prospect.md · content/
D3 Verdict (evaluate)    the unit's verdict surface:   🪞 reflect: the judge writes
                         README judged: line ·         judged: and flips state ·
                         prospect.md (checked here,    🔮 prospect: GD4 checks the
                         written at D2)                forecast's shape and guardrails
D4 Division (decide)     the DS page's division row    ✋ accepted: per the Design page
                                                       contract's row grammar · or
                                                       emitted: naming the need raised
D5 PageDown              workflow/rounds/              the record made TRUE again: the
                         R<NN>-pagedown/ receipt +      era-sensitive surfaces reread
                         pages the round grew           against the round's outcome ·
                                                       at milestones, a cold read
   ↺ D1→D4 runs per THREAD · D5 runs ONCE per round, after every thread is
     terminal · D5→GD6 seals and STOPS · a later commissioned round re-enters D0
```

**The thread, precisely, is ONE EVOLVING FOLDER.** The frontier's atomic unit
is `design/DU<NN>-<slug>/`, born at D1 holding only card.md, grown at D2, and
judged at D3 without moving. The current phase identity changes in place and
the transition history remains readable. After landing it is represented by a
DIVISION ROW on the parent D4 Page (one division per landed unit). A proposed
card with sibling realization files is a checker ERROR. A card at `proposed`
blocks its own fan-out and nothing else; it carries to the next round unreleased.

## 🎨 The full picture, one round

```text
                     ┌─ two births (haipipe-design §The two births of a Brief) ─┐
                     │ evidence-first: signed W handoff(s) · born-of: names them │
                     │ mandate-first:  a person names the program · needs OUT    │
                     └──────────────────────────┬────────────────────────────────┘
════ ROUND r ═══════════════════════════════════▼═══════════════════════════════
D0 frame     📌 BR00 + reads: + roster          GD0: framed is ENOUGH, not everything
D1 bet       📇 cards, one per wager            ✋ GD1 release · kill is equal-rank
D2 realize   🎨 one designer per released card, in parallel, packet = the grant ·
             the unit lands COMPLETE, prospect.md included (the designer writes it)
D3 evaluate  🪞 reflect: the judge (fresh context, never the arm) checks grant ⊆ ·
                spec · rails mechanically, stance fidelity by cold read, then
                writes the unit's judged: line — GD3
             🔮 prospect: GD4 checks prospect.md's four blocks and guardrails ·
                a failed verdict returns the thread to D2 for re-realization
                under the same card, or the person kills the card
D4 decide    each division: ✋ accepted  ──▶ all threads terminal, all landed ones
             accepted = the lane's ACCEPTED close ──────────────────────────────┐
             or EMIT: the missing insight lands as a new row on BR00's needs    │
             block; the register question is then born need-first from it       │
D5 page down 📰 the grown pages reread AS DOCUMENTS: title · Opening · Diagram ·│
             scope · Law · state lines · board.md Topic/close, against what the │
             round changed; staleness repaired, decisions untouched · GD6 seals │
             the round, then STOP ──────────────────────────────────────────────┤
════ ROUND r+1 ══ (insight lap answers → back to D0, reframed) ═════════════════│
                                                                                │
outer loop:  task layer ships + measures ◀──────────────────────────────────────┘
             → the InsightBoard reads the ACTUAL effect back as new D rows
             → whoever lands that read-back appends a dated scored: line to each
               affected unit's prospect.md (predicted vs measured) — the same
               post-acceptance bookkeeping class as staleness clearing
             → the scores condition the next round's bets (calibration)
```

## 🎲 The four postures, and why generate and brainstorm exist

D1's cards take four POSTURES toward evidence, and the lane needs them all or it is not a design lane (vary/challenge/propose added 0.3.0, brainstorm 0.5.0, each after a live round exposed the gap). The stance WORDS are the direction plugin's six; the postures group them:

```text
posture      stance words                  the license comes from
──────────────────────────────────────────────────────────────────────────────
vary         follow · follow-all ·         the fielded set: recombining house
             ignore                        styles, one degree of freedom
challenge    bet-against <claim>           the claim itself (the grant includes
                                           what it bets against)
brainstorm   brainstorm <audience>         NOTHING licenses it and nothing need:
                                           a pool is not a claim, so it owes no
                                           warrant · insights enter as
                                           INSPIRATION, the fielded set enters
                                           only as the AVOID list, and reuse is
                                           forbidden outright (direction law 5)
propose      generate <mechanism>          a THEORY: warrant-insight (who this
                                           is for · brief-only admissible when
                                           no insight row exists, the missing
                                           insight emitted in the same round)
                                           + warrant-theory (the mechanism),
                                           per the direction plugin's law 4 —
                                           never a data gradient, so W-page
                                           prohibitions on gradient-derived
                                           wording stand
```

Exploration is the lane's duty, not its indulgence: the fielded set can only ever rank what someone dared to write (QD4 §2-3's anchors — Dorst's abduction, Dow's parallel prototyping). A generate card is bold at the CARD and honest at the VERDICT: the wager may reach past the data, the prospect stays information-typed, and the experiment settles it. The symmetric failure is also named: a designer on a generate card that quietly nominates fielded copy has changed lanes without a card, and GD3 fails it on the novelty block.

**Designing a message set is not designing an experiment** (JL 260828, and the reason the brainstorm posture exists). Two rounds' worth of retreat to fielded copy had one root: comparator duties — a control cell, an allocation, a predicted effect — were being charged to the act of WRITING, so the incumbent had to be present in every unit and the writing shrank to fit around it. The brainstorm posture cuts the duties apart. Its round produces a POOL: N newly authored messages for one audience, zero reuse, no comparator, no forecast, judged only on count, newness, mutual distinctness and rails (haipipe-plugin-design §pool). Every entry IS a candidate arm, a real message that could be fielded; what it lacks is an allocation, which is the only thing separating a candidate from an experiment's arm. Which entries get fielded, against which control, at what size, is the FIELDING decision and belongs to the task layer downstream. GD4 does not reach a pool unit, and a pool that is never fielded is still a completed unit, because the design space written down is the deliverable.

**Realization is two movements, not one** (JL 260828: design is not conclusion — it opens from the data, then closes). A generate unit's D2 runs DIVERGE then CONVERGE on the unit's `ideation.md` (haipipe-plugin-design §ideation): first quantity under deferred judgment — five or more candidates, two or more angles, intuition admitted and labeled, no rail-checking, no citing, fielded copy not re-read — then the selection table, where every candidate is dispositioned, finalists are mapped to the warrant legs, pass the rails, and land in `content/` as the variant set. The same mechanism said differently is a different arm, and which verbalization wins is an empirical question the variant set exists to field — the open is where the design space is explored, the close is where it earns its evidence chain, and neither movement may impersonate the other.

## 🧭 Round one always completes

A round may discover mid-flight that the insight is insufficient; the round still closes. Designing is itself the inquiry that reveals what is missing — the move talks back — so stalling a round to "get more insight first" discards the very instrument that names the gap. Insufficiency has exactly one legal exit, and it uses the family's existing machinery end to end: an `emitted:` row on the division names the gap, the gap lands as a row on BR00's needs block (a design-side file, so no pen crosses), and the register question is born NEED-FIRST from that need exactly as `haipipe-insight` rules — no third birth exists. A round CLOSES when every thread is terminal: accepted, emitted, or killed, with proposed cards carrying over freely; the round then SEALS at GD6, the D5 PageDown.

## 🔮 Prospect, and its three guardrails

The card's expected effect is a declaration; prospect is the WORK that sharpens it into a scorable forecast: a walkthrough of the artifact as the recipient meets it, the mechanism the thesis relies on, a predicted effect with stated uncertainty, and the conditions under which the bet fails. The DESIGNER writes it while realizing the unit (its procedure step 5); D3 checks it and never writes it. Three guardrails keep it from corroding the evidence chain:

```text
① grant-only     prospect may cite ONLY evidence inside the card's grant — a
                 simulation may not invent data
② forecast-typed its output is a FORECAST, never a claim: it may not be written
                 as K/W prose and may never land on any InsightBoard
③ scored, not cited   nothing cites a prospect as support; the outer loop appends
                 the dated scored: line after the effect reads back, and the
                 score conditions later bets
```

## 🚪 The gates

Each gate is an assertion over artifacts that already exist; a gate that cannot be tested by reading named files is misdesigned. GD0 is per-DS-page (its BR00 and `reads:` clauses are board-level and shared); the rest are per-thread.

```text
GD0  frame → bet       BR00 past 🔴 · born-of: resolves, or the mandate is named and
                       every unmet need is a register row OUT · board reads: set ·
                       the roster names this DS page
GD1  bet → realize     ✋ per card: proposed → released, a person's act — card by
                       card, or by a person's recorded blanket over NAMED cards
                       (haipipe-plugin-design §card law 1) · a release binds only
                       cards that EXIST when the words are recorded · no expected
                       effect, no release · kill is the equal-rank terminal
GD2  realize → verdict the unit exists complete beside its card: README ·
                       spec · evidence · prospect.md · content/ · evidence ⊆ grant ·
                       the card's state flipped to landed · a generate unit's
                       spec carries the novelty block (surface · mechanism · both
                       warrant anchors) and its ideation.md carries both movements:
                       five-plus candidates, two-plus angles, every candidate
                       dispositioned, finalists ⊆ candidates
GD3  reflect passes    ex-post: grant ⊆, spec acceptance list and venue rails are
                       machine-checkable; stance fidelity is the judge's cold-read
                       judgment · the judge audits the acceptance list against its
                       declared sources (narrowing invention is a finding, widening
                       invention fails) · on a generate unit the judge byte-checks
                       novelty (any cell identical to a fielded template fails) and
                       audits the ideation record: finalists ⊆ candidates, every
                       disposition reasoned, no fielded quote among candidates —
                       the judge NEVER re-judges the discards, deferred judgment
                       would be retroactively deleted if it did ·
                       the judge writes the unit's judged: line and flips
                       state: judged · the judge is never the unit's designer
GD4  prospect passes   DOES NOT REACH a pool unit (brainstorm posture: a pool is
                       not a bet, so there is nothing to forecast) · otherwise
                       ex-ante: prospect.md carries walkthrough, mechanism,
                       predicted effect + uncertainty, failure conditions · cites
                       nothing outside the grant · a generate unit's prospect may
                       carry the theory's direction, marked theory-typed with its
                       QA anchor, never a numeric or data-derived one · NOT
                       retroactive: units accepted before 260827 and record-mode
                       units are exempt (haipipe-plugin-design §prospect)
GD5  decide            per division: ✋ an accepted: row satisfying the Design page
                       contract's grammar (haipipe-design-division), its render
                       EXISTING and current — or an emitted: row naming the BR00
                       need raised · acceptance may also be a person's recorded
                       blanket over named divisions · every thread terminal sends
                       the round to D5 · all landed threads accepted = ACCEPTED
GD6  page down → seal  the round CLOSES only when the grown pages read true as
                       documents: no era-frozen claim survives (title, Opening,
                       Diagram, scope sections, Law, state lines, and board.md's
                       Topic and close all agree with the round's outcome), and
                       every count a page states agrees with the rows on disk ·
                       at a MILESTONE round, and always before the board is shown
                       to an outside reader, a fresh zero-background cold read
                       (haipipe-board-reviewer-agent) must pass the 60-second
                       test: a stranger can say what the board is, what it
                       produced, and what is open · D5 touches PROSE only — a
                       decision-level defect found here is reported and routes to
                       the next round, never repaired in place · judge-class, not
                       a third Design cross-phase gate
                       [new 260828 · six rounds ran without it and the pages froze
                       at round 1, found by JL's own cold read: "别人都不知道在干嘛"]
```

**The two Design cross-phase authority gates never have an auto mode**: card
release is GD1 and acceptance is GD5. Together with Insight's two, they are the
Application's four domain authority transfers. Page Workflow may still require
local outline, read, or verified ticks while authoring a Folder; those are
nested Page-Face controls and can pause a copilot run, but they do not create
new GD transitions. A recorded blanket is a person's act over a NAMED set,
transcribed clerically with the person's words cited in the DS Folder's
`outline/<DS-stem>-log.md`; a machine's inference is never one. Every dispatch
pins `mode: copilot`. A
blocked gate is a clean stop: report the thread, waiting artifact, and decision.

The shared Page owner RULING map is explicit: D0 none, D1 reuses GD1, D2 none,
D3 none, D4 reuses GD5, D5 none. The reused receipt is one decision seen at two
altitudes, never a second tick. Other Page-local plugin ticks can hold the Page
run but cannot release a Card or accept a Division.

## 🚪 The commission entry

One sentence commissions a design end-to-end; everything between the ✋ gates is automatic:

```text
/haipipe-design-workflow "design <message/job> for <audience> on <venue>,
                          reading <InsightBoard pages | signed handoffs>"
/haipipe-design-workflow "brainstorm <n> new messages for <audience> on <venue>,
                          inspired by <pages | QA files>, avoiding <fielded set>"

resolve the board (scaffold through the umbrella if absent) → GD0: birth the Brief
if missing, write reads: from the commission → D1: propose cards → STOP at GD1,
cards presented → on release (or a person's recorded blanket) → D2-D3 fan out and
evaluate → STOP at GD5, renders visible, decisions owed → after the decisions
land, D5 pages the round down (the grown pages made true and readable) and GD6 seals it
```

## 📚 Why each phase, in the literature

The literature lives on the skill board, never in this file (JL 260827): `diagrams/ApplicationSkillBoard-260802/8-QD-design/QD4-round-theory/` registers the verified anchors per phase, and the full lists sit in the Task Page QA files under `designs/Project-Application-SMSDesign/discoveries/b02_design_process_theory/j01_design_process_theory_inquiry/`. Cite a Task Page or QA file, never a paper from memory.

## 🗃 Artifact mapping

```text
D0        0-BR-brief/BR00-brief/
D1        2-DS-design/DS<NN>-<audience>-<job>-<venue>/design/DU<NN>-<slug>/card.md
D2        the same folder, grown: README · spec · evidence · ideation (generate/
          brainstorm) · prospect · content/
D3        the unit's judged: line (haipipe-plugin-design §verdict) ·
          design/DU<NN>-<slug>/prospect.md (anatomy: the plugin's 0.3.0;
          a unit-no-prospect checker rule is still owed)
D4        the DS page's division rows · delivery/render/ for the visible version
          1-P-principle/ stays VACANT unless promoted (haipipe-design-division)
D5        workflow/rounds/R<NN>-pagedown/ records the pass; the grown DS page,
          BR00 and board.md remain authoritative — decisions and units untouched
```

## 🚚 Dispatch: one thread at a time

```text
select   the frontier thread whose gate is open and whose inputs exist; released,
         unlanded cards first
load     the matching haipipe-design-<phase> Folder skill + haipipe-design
         (the door) + the plugin contracts its Task Face names; the
         venue pack for the unit's kind: resolves from application/venue/
run      realize through agents/haipipe-designer-agent, one per card, packet =
         the grant · pages through haipipe-page-workflow, mode: copilot always
fold     move a thread ONLY on a gate passing; every other terminal is a named
         non-decision and the thread does not move
repeat   until every thread is terminal or a gate blocks
```

## 🧾 Phase receipts

A transition leaves exactly one record in the granting Folder's canonical
`outline/<stem>-log.md`: BR00 records GD0 and the parent DS Folder records
GD1-GD5. Each record is dated and names the artifact id it covers (the card for
a release or kill, the unit for a landing or verdict, the division for an
acceptance or emit), plus the person's words when the gate was a person's.
Cards and units carry state fields, not private Logs; no embedded Page log
section or separate receipt store is authoritative.

## ⏱ Advancement is never scheduled

A gate test may be run any time; a gate may only be DECLARED passed by the human tick or judge verdict it names. Nothing here may be wired to a timer or a loop that advances threads on wall-clock time.

## 🔀 Resolving "what phase are we in"

Per thread: the highest gate whose assertion currently holds. Per Design
Folder: read division rows and open cards together. A board-level scalar is a
lie this workflow refuses to mint; the crossing workflow reports this native
frontier unchanged.

## 🛑 Stop rules

- GD5 is the outward-acceptance boundary: never build, ship, or measure here.
  The dispatcher must still run D5, record the PageDown receipt, pass GD6, and
  only then stop the round.
- STOP at any gate: report and end, never wait in a loop.
- STOP on contradiction: a thread that derives to two phases at once is reported as a defect, never repaired silently.
- **Emit and kill are convergence.** An emitted division and a killed card are terminal states equal in rank to accepted: a round rich in emitted questions is co-evolving, not failing. The defect is the thread that can neither be accepted nor say what it lacks.

## ↩ Return

The frontier threads by phase, the units realized this run with their two verdicts, the gate now blocking with the person's owed decision, the needs emitted this round, and the next runnable thread once that gate clears.
