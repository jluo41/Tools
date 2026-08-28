---
name: haipipe-design-workflow
description: >-
  The DesignBoard-level phase machine: six phases named after the artifact classes the lane owns — D0 Brief (frame) → D1 Card (bet) → D2 Unit (realize) → D3 Verdict (evaluate) → D4 Division (decide) → D5 PageDown — with gates GD0-GD6, each a checkable assertion over artifacts on disk. The frontier's atomic unit is the THREAD: a card until it lands, the division row after; a round is one full D0→D5 pass, and ROUND ONE ALWAYS COMPLETES — insufficiency never stalls a round, it exits as an EMIT that lands on the Brief's needs block and becomes a register question by the ordinary need-first birth, which is the problem-solution co-evolution edge. Evaluation has two mandated faces: reflect (ex-post, the judge's conformance verdict, on-disk word judged) and prospect (ex-ante, a scorable forecast of the artifact in use, written at realize and checked here). It refines the application machine's design lane (P3 = D0, P4 = D1-D5) and accepts a one-sentence COMMISSION; interior law stays with the door /haipipe-design, page lifecycle with haipipe-page-workflow, every verdict with an independent CHECK plus a human tick. Use when asking where a design round stands, whether a thread may advance, what the next runnable step is, how to commission a design end-to-end, or where a run must stop. Trigger: design workflow, run the design board, design round, commission a design, design me a message, next division, frontier thread, reflect, prospect, ex-ante, ex-post, forecast, emit a question, /haipipe-design-workflow.
metadata:
  version: "0.7.2"
  last_updated: "2026-08-28"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-design-workflow · know the thread, test the gate, close the round

Load `haipipe-design` first; it says what a DesignBoard IS and, since its 0.3.0, names this file as the lane's phase authority. This machine refines `haipipe-application-workflow`'s design lane and never contradicts it: that machine keeps the two-lane view and gates G0-G5, this one names the stations inside. It never edits a page, never runs a page's lifecycle (that is `haipipe-page-workflow`), never states board law (that is the door), and never judges content (that is the judge plus the human ticks).

## 🔤 Terminology law

A **design phase** is one digit, `D0`-`D5`. A Design PAGE id always carries two digits (`DS01`), so a one-digit `D<n>` in a design-lane document is a phase, never a page — the same digit-count rule the other machines use. Against the application machine: `🎨P3 = D0`, `🎨P4 = D1-D5`, card proposal included; the aliases frame, bet, realize, evaluate, decide, page down are legal in prose, never in a folder or file id. D5's NAME is PageDown, one word (JL 260828, "what I mean is: D5 PageDown"): the one phase whose name fuses its authority artifact (the Page) with its act (setting the round down onto it); the artifact-class test still holds, because the page is what D5 owns.

**One extension, stated openly.** The insight machine names phases by authority PAGE because its lane owns six page types; this lane's grain is finer — one DS page hosts many threads — so a design phase is named by its authority ARTIFACT class: a page, a card, a unit folder, a verdict surface, a division row, each an on-disk class with its own state words. The application machine's naming law admits this tier explicitly since its 0.8.0. The test is unchanged: a position that cannot name an artifact class of its own is a gate, which is what keeps accept at GD5 and makes the settle-back-to-frame an EDGE (emit), not a phase.

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
D5 PageDown              the pages the round grew:     the record made TRUE again: the
                         DS page · BR00 · board.md     era-sensitive surfaces reread
                         head                          against the round's outcome ·
                                                       at milestones, a cold read
   ↺ D1→D4 runs per THREAD · D5 runs ONCE per round, after every thread is
     terminal · D5→D0 turns the ROUND · exits at GD6, the round seal
```

**The thread, precisely, and since 260828 it is ONE FOLDER.** The frontier's atomic unit is a THREAD: the folder `design/DU<NN>-<slug>/`, born at proposal holding only its card.md (state words proposed · released · landed · killed), grown into the realization after release, and represented by a DIVISION ROW on the page after landing (the door's law — one division per landed unit — is untouched). Release-before-realize is folder purity now: a proposed card with sibling files is a checker ERROR, not a habit. A card at `proposed` blocks its own fan-out and nothing else: it never blocks a round from closing, it simply carries to the next round unreleased.

## 🎨 The full picture, one round

```text
                     ┌─ two births (haipipe-design §The two births of a Brief) ─┐
                     │ evidence-first: signed W handoff(s) · born-of: names them │
                     │ mandate-first:  a person names the program · needs OUT    │
                     └──────────────────────────┬────────────────────────────────┘
════ ROUND r ═══════════════════════════════════▼═══════════════════════════════
D0 frame     📌 BR00 + reads: + roster          GD0: framed is ENOUGH, not everything
D1 bet       📇 cards, one per direction        ✋ GD1 release · kill is equal-rank
D2 realize   🎨 one designer per released card, in parallel, packet = the grant ·
             the unit lands COMPLETE, prospect.md included (the arm writes it)
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
                       [refines the app machine's G4, adding the roster clause]
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
                       contract's grammar (haipipe-page-for-design), its render
                       EXISTING and current — or an emitted: row naming the BR00
                       need raised · acceptance may also be a person's recorded
                       blanket over named divisions · every thread terminal sends
                       the round to D5 · all landed threads accepted = ACCEPTED
                       [= the app machine's G5's all-accepted close]
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
                       a fifth human gate
                       [new 260828 · six rounds ran without it and the pages froze
                       at round 1, found by JL's own cold read: "别人都不知道在干嘛"]
```

**The two human gates never have an auto mode**: card release is GD1, acceptance is GD5, and with the insight lane's two (probe release, handoff signing) they are the application's four, two per door. A recorded blanket is a person's act over a NAMED set, transcribed clerically with the person's words cited in the DS page's Log; a machine's inference is never one. Every dispatch pins `mode: copilot`. A blocked gate is a clean stop: report the thread, the waiting artifact, and the person's owed decision.

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

The literature lives on the skill board, never in this file (JL 260827): `diagrams/ApplicationSkillBoard-260802/8-QD-design/QD4-round-theory/` registers the verified anchors per phase, and the full lists sit in the five QA files under `designs/Project-Application-SMSDesign/discoveries/S02_design-process-theory/`. Cite that page or a QA file, never a paper from memory.

## 🗃 Artifact mapping

```text
D0        0-BR-brief/BR00-brief/
D1        2-DS-design/DS<NN>-<slug>/design/DU<NN>-<slug>/card.md
D2        the same folder, grown: README · spec · evidence · ideation (generate/
          brainstorm) · prospect · content/
D3        the unit's judged: line (haipipe-plugin-design §verdict) ·
          design/DU<NN>-<slug>/prospect.md (anatomy: the plugin's 0.3.0;
          a unit-no-prospect checker rule is still owed)
D4        the DS page's division rows · render/ for the visible version
          1-P-principle/ stays VACANT unless promoted (haipipe-page-for-principle)
D5        the grown pages themselves, PROSE only: the DS page's head, Opening and
          Diagram · BR00 · board.md — decisions, rows and units untouched
```

## 🚚 Dispatch: one thread at a time

```text
select   the frontier thread whose gate is open and whose inputs exist; released,
         unlanded cards first
load     haipipe-design (the door) + the plugin contracts its verbs name; the
         venue pack for the unit's kind: resolves from application/venue/
run      realize through agents/haipipe-designer-agent, one per card, packet =
         the grant · pages through haipipe-page-workflow, mode: copilot always
fold     move a thread ONLY on a gate passing; every other terminal is a named
         non-decision and the thread does not move
repeat   until every thread is terminal or a gate blocks
```

## 🧾 Phase receipts

A transition leaves exactly one receipt, and every receipt lands on a surface that HAS a Log: BR00's Log for GD0, the DS page's Log for GD1-GD5, each row dated and naming the artifact id it covers (the card for a release or kill, the unit for a landing or verdict, the division for an acceptance or emit) plus the person's words when a gate was a person's. Cards and units carry state fields, not Logs; the page that hosts them is their record. No separate receipt store is authoritative.

## ⏱ Advancement is never scheduled

A gate test may be run any time; a gate may only be DECLARED passed by the human tick or judge verdict it names. Nothing here may be wired to a timer or a loop that advances threads on wall-clock time.

## 🔀 Resolving "what phase are we in"

Per thread: the highest gate whose assertion currently holds. Per page: the division rows and open cards read whole — a page-level scalar is a lie this file refuses to mint. The application machine's `🎨P<n>` reading derives from the same artifacts (P3 = BR00 owed, P4 = any thread from proposal to GD5, plus the unsealed round's D5).

## 🛑 Stop rules

- STOP at GD5: ACCEPTED ends the lane; building, shipping and measuring are task-layer work, and the effect read back is the InsightBoard's.
- STOP at any gate: report and end, never wait in a loop.
- STOP on contradiction: a thread that derives to two phases at once is reported as a defect, never repaired silently.
- **Emit and kill are convergence.** An emitted division and a killed card are terminal states equal in rank to accepted: a round rich in emitted questions is co-evolving, not failing. The defect is the thread that can neither be accepted nor say what it lacks.

## ↩ Return

The frontier threads by phase, the units realized this run with their two verdicts, the gate now blocking with the person's owed decision, the needs emitted this round, and the next runnable thread once that gate clears.
