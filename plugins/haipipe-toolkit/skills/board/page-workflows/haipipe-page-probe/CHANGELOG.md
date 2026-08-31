## 0.12.1 · 2026-08-31

Category-folder sweep: lane paths read `<page>/evidence/<lane>` or
`<page>/delivery/<lane>` (haipipe-page 0.47.0 §📁); flat names are the same
lane during migration (stubs).


## 0.12.0 · 2026-08-31

The TASK-route batch gets a home: the page's collection job
(`task/haipipe-task-for-page`) enters the MATCH ladder at step 2 and receives
the dispatched questions via `/haipipe-task qa "<q>" <job>`. The one-door rule
(haipipe-probe-q-executor-agent) and the Discovery route are unchanged.

## 0.11.0 — 2026-08-21

- **A missing task folder stopped being a HOLD.** §🔀's `no allowed bank can
  answer → HOLD` read as "no folder exists", so a perfectly answerable question
  could stall the page. It now reads `no bank can answer IN PRINCIPLE (route:
  none)`, with the distinction stated beside it: a missing folder is `T4 FRESH`,
  it dispatches normally, and the executor opens the leaf at depth 3. The rule
  lives in `haipipe-probe` §💰 · §③ (R13/R15, restored there 260821); this file
  carries only the routing consequence.
- **The receipt reports the TIER SPREAD.** `cards:` gains `tier`, and a new
  `tiers:` row counts how many landed on each of T0-T4. Per CC-7 most should be
  T2; an all-T3/T4 page is a lazy MATCH or a starving bank, and the receipt is
  where that becomes visible instead of just expensive.

## 0.10.0 — 2026-08-21

- **Three mirrored sections deleted.** §🧱 Organize and strip, §🔎 MATCH before
  DISPATCH and §📮 DISPATCH restated `haipipe-probe` §①②③ near-verbatim — the same
  `--check-only` block, the same `task | discovery | none` table, the same "our
  paper" / "we need to show" phrase list. That is the §🪞 mirror this family
  forbids, and it had already drifted (see below). One §🧱 replaces all three and
  carries only what the shared contract does NOT say: the page-local card pass in
  front of the bank pass, the one-door dispatch rule, and the three states PROBE
  may leave behind. 7.6 KB → 4.4 KB of body.
- **`🔗 PageX` removed from §🧭.** The mark authority is `haipipe-plugin-outline`
  §📐 and it defines FIVE marks (🎯 📮 🧮 📚 🖼). This file had a sixth. PageX is
  a LANE resolved in OUTLINE, never a bullet mark — the drift a restated table
  produces, caught in the 260821 skills audit.
- **The one-door rule is now stated here.** `haipipe-probe` 0.14.0 recorded JL's
  260820 ruling that only `haipipe-probe-q-executor-agent` may cross to the
  banks; §📮 still said "the shared probe executor" without naming it. §🧱 ② now
  names the agent and names what a phase producer may never call directly.
- ⚠️ **Changelog gap.** This file jumped 0.7.0 → 0.10.0: SKILL.md shipped 0.8.0
  and 0.9.0 with no entry here. Their content is in the git log, not in this
  file, and is not reconstructed.

## 0.7.0 — 2026-08-20

- **The dispatch names its agent** (JL ruling A, 260820): PROBE crosses to the
  bank through haipipe-probe-q-executor-agent ONLY — the batch carries per
  card the PP id, stripped question, route, bank verdict and the card.md
  bind-back path — and no page-family hand calls
  haipipe-task/discovery-orchestrator-agent directly. Until now this section
  named the orchestrators and no carrier, which is how a session hand-rolled
  its own crossing on 260820.

## 0.6.0 — 2026-08-19

- **📮 probe and 🧮 value are now SEPARATE marks** (JL: "You mean you put the
  probe and values together? I want to separate them"). 📮 = this point needs
  a QUESTION answered — bare before ② raises the card, `📮 PP<NN>` after; the
  answer may be a finding or a folder of numbers. 🧮 = this point QUOTES one
  value, `PP<NN>.v<n>`, out of an answered card's `## Values` block, and
  `checks/values.py` re-computes it. 📮 deliberately shares phase ②'s glyph
  (same concept) and is end-anchored in the scanners so prose about the phase
  never reads as a mark.
- **Coherence sweep (260819)**: the summary and description caught up with
  §🔗's CLOSED ruling and the Aims-in-plan move; §🧭's mark table trades the
  retired ✅ for a 🧮 row (the mark quotes `PP<NN>.v<n>`); §🕐's bare ask
  wears 📮, not 🧮; the receipt and the phase's release gate on the 🧑 LOOK
  after the ① pass, with `approved:` closing the round later.

## 0.5.2 — 2026-08-19

- **The value mark is 🧮** (JL: "🧮 maybe this one?" — he never liked 🔢).
  🔢 stays accepted as the legacy alias, so pre-260819 plans remain legal.
  The abacus was the proof mark retired earlier on 260819 and is revived with
  its new meaning: a recomputable number, which is what `checks/values.py`
  does to every one of them.

## 0.5.1 — 2026-08-19

- **Identity fixed: PROBE is phase ②** (frontmatter and footer said ③, one
  place behind the 260819 order).
- **§🕐's argument caught up with the Aims ruling**: it argued "Aims are
  written at DRAFT, so PROBE is the earliest complete card" — since 260819 the
  Aims are settled in the approved plan, which is exactly what let PROBE move
  to ②. The card-at-PROBE ruling itself is unchanged. Found by the Display3
  rebuild agent.

## 0.5.0 — 2026-08-19

- **The MATCH-runs-late defect is CLOSED.** It stayed open on one argument: the
  card carries the stake, the stake is an Aim, and Aims were written at DRAFT. JL
  ruled the Aims into the plan file on 260819, so the argument died and the whole
  phase moved to where MATCH wanted to be. No MATCH phase is split out.
- PROBE now routes back to ① OUTLINE, never forward. What comes back confirms or
  changes the plan, and only the plan's four-check gate ends the PREPARE loop.

## 0.4.2 — 2026-08-19

- **🧮 proof RETIRED.** JL 260819: "我从开始到最后都没有说 proof，我一直说
  probe". The mark came from ONE transcribed quote ("citation, display, values
  and proofs") and no Log row ever ruled it. Going to a task folder or a
  discovery folder for the evidence behind a claim IS a probe, which is 🔢.
  It was the only mark with no plugin, no folder, no lane, no id and no
  backlink, and that was the symptom rather than a design.
  ⚠️ `proof/` the FOLDER is untouched: it belongs to a probe card.

- §🧭's mark table loses its 🧮 row; the plan carries five marks, not six.

## 0.4.1 — 2026-08-18

- Pointer added to `../haipipe-page-workflow/ref/phase-cards.md` §③, which
  states this phase and every sibling in the SAME six fields
  (`❓ ASKS · 📥 READS · 📤 WRITES · 🚪 EXITS · ✋ TICK · 🔀 ROUTES`). This
  contract still owns the reasoning; the card is the readable-across-phases
  summary, and the contract wins when they disagree.
- Board backlink retargeted: `QPw7`/`QPw8`/`QPw9` became `QPw00a`/`QPw00r`/
  `QPw00g` when JL ruled that pages which are not phases may not carry
  phase numbers.


## 0.4.0 — 2026-08-18

MATCH runs LATE, recorded as an open defect (JL 260818).

- Added the timing defect to `§🔗 MATCH order`: MATCH needs only the outline's
  MARK and not the stake, so nothing requires DRAFT to precede it, yet it lives
  inside PROBE which runs after DRAFT. A page therefore pays for its sentence
  scaffolds before discovering the answer already existed.
- Recorded JL's reading that put the lookup second ("OUTLINE, then the probe
  (pagex), and the draft") and why he is right about MATCH and not about the
  card, whose `consumer/` side needs the stake DRAFT writes.
- Stated why a split would be named MATCH and never PAGEX: PageX is one of
  MATCH's three lookups, so naming the phase after it is like naming EVIDENCE
  "bibex". Scored 2.5 of 4 versus 0.5 of 4 on `QPw00 §7.2`'s split test.
- Added the Board page backlink: `QPw3-probe` argues this phase.
haipipe-page-probe · Changelog
==============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions
match SKILL.md frontmatter `version:`. Newest first.

## 0.3.0 — 2026-08-17

Adds PageX/MATCH as the first read-only reuse lookup before QA-bank work. Exact
reuse keeps the existing QA path or Display id; similarity alone never closes
a question.

## 0.1.0 — 2026-08-17

First contract. PROBE was listed as a phase in `haipipe-page-workflow` 0.2.0 but
had no file of its own and borrowed `haipipe-page-evidence`, so three skills gave
three different answers to the same question (JL 260817: "具体的 proof 应该由谁来
做？我还没想好这部分是在 draft 阶段来做，还是在 outline 阶段来做？"):

```
haipipe-page-draft §🃏        DRAFT creates the card in OWED state
haipipe-page-evidence §🧾     "a card may arrive already PROPOSED" by DRAFT
haipipe-plugin-outline §📐    "the card is created at PROBE"
```

**The ruling: PROBE creates it. Never OUTLINE, never DRAFT.**

- OUTLINE may not, because a plan is rejectable in ten seconds and must leave
  nothing on disk; a card for a plan nobody approved is litter with an id.
- DRAFT may not, because the mark IS the proposal, and a second file saying the
  same thing is `haipipe-page-workflow` §🪞's duplication rule.
- The deciding reason is the STAKE: a card's `consumer/` side carries what the
  page loses if the answer never comes, that is an Aim, and Aims are written at
  DRAFT. PROBE is the earliest phase at which a complete card can exist.

Also fixed here rather than left open:

- **One mark is not one card.** Many bullets may share one card (`PP04` on
  QC1-visitlbp serves three), one bullet may need two, and a mark already
  covered gets its address appended to the existing card's `serves:` rather
  than a second card.
- **Which marks PROBE acts on**: 🔢 always; 📚 only when the key is unknown;
  🖼 never (its intake freezes FROM a `proof/` that does not exist yet, so
  EVIDENCE creates the unit); 🧮 never, which settles `haipipe-plugin-outline`'s
  open "⬜ whether 🧮 earns a folder" as NO: a proof is prose, resting on a
  pulled file that already lives in a probe card's `proof/`.
- **`coverage:` in the receipt**: how many marked bullets actually got a card.
  Declaring is free; this is the count that makes a gap a HOLD.

Siblings changed in the same pass: `haipipe-page-draft` 0.6.0 (§🃏 deleted),
`haipipe-page-evidence` 0.6.0 (the "DRAFT proposes" paragraph replaced),
`haipipe-page-workflow` 0.3.0 (the member table points here), `haipipe-page`
0.4.0 (seven phases in the lifecycle table).
