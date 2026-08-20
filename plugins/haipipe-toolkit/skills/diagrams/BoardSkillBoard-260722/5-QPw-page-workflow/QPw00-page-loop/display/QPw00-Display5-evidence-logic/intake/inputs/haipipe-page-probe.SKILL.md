---
name: haipipe-page-probe
description: >-
  The PROBE phase contract for any Board Page, and phase ② of the page workflow. PROBE turns each MARK left by the outline pass a person has LOOKED at into a real folder under <page>/probe/PP<NN>-<slug>/, writes the stake-bearing Q-consumer and the stripped Q-executor, points the card back at the bullets it serves, and dispatches the stripped question to the bank. It is the ONLY phase that creates an evidence card: OUTLINE marks the hole and leaves nothing on disk, the PLAN gives the hole an Aim to lose (Aims live in the plan since 260819), EVIDENCE lands what comes back. Load haipipe-page, the matching Page Type, this contract, then haipipe-plugin-probe for the folder's shape and haipipe-probe for the crossing protocol. Use when an outline pass a person has LOOKED at carries a bare 📮 mark, when a question must be asked before a number may be written, when cards must be allocated for a page, or when a card must be pointed at the bullets it answers. Trigger: page probe, PROBE phase, phase 2, raise the card, allocate PP number, serves, mark to card, dispatch the question, ask the bank, stake wall, who creates the card, /haipipe-page-probe.
metadata:
  version: "0.6.0"
  last_updated: "2026-08-18"
  summary: "MATCH-runs-late is CLOSED (260819): Aims moved into the plan, so the whole phase sits directly after OUTLINE, exactly where MATCH wanted to be."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-probe · turn each mark into a card, and ask

**LOAD `haipipe-page` FIRST**, then the Page Type, then this file, then
`haipipe-plugin-probe` for the folder's shape and `haipipe-probe` for the
crossing protocol. This contract owns the PHASE. The folder, its four counts and
its state tests are the plugin's, and this file restates neither.

## 🎯 The authority test

```text
owns       mark ─▶ card: the folder, its number, its Q-consumer, its stripped
           Q-executor, its `serves:` backlink, and the dispatch
           plus the MATCH order: local card → PageX → QA bank → new dispatch
may do     create a card · merge two marks into one card · dispatch · defer
exits      every marked bullet is served by at least one card, and every card
           is `planned` or further along (the ladder is haipipe-plugin-probe's:
           planned · commissioned · answered · read, never raised/working/bound)
🚫 may not  write prose · land an answer · freeze a display intake · edit the
           approved plan · invent a mark the plan does not carry
```

Creating the card and filling it are two phases on purpose. PROBE ends the
moment the question has left; what comes back is `haipipe-page-evidence`'s.

## 🕐 Who creates the card, and why not earlier

This was the open question until 260817, and three skills answered it three
ways. It is settled here: **the card is created at PROBE. Never at OUTLINE, and
never at DRAFT.**

```text
phase       what it holds about the hole            why it may not create the card
──────────────────────────────────────────────────────────────────────────────────
① OUTLINE   the MARK: `- B4 · the four              a plan is rejectable in ten
            coordinates            📮`               seconds, and a rejected plan
            bare, no id                              must leave NOTHING on disk.
                                                     A card for a plan nobody
                                                     approved is litter with an id.

② PROBE     the CARD                                 ← here
```

**And the practical reason, which is the one that decides it.** A card's
`consumer/` side carries the STAKE: what this page loses if the answer never
comes. What the page loses is an Aim, and since 260819 the Aims are settled in
the plan itself (JL: "Aims should be move together with outline"). So the
🧑 LOOK on the plan's ① pass is the moment a complete card can exist (the
`approved:` tick closes the whole PREPARE round later), which is exactly what
let PROBE move to phase ②, directly after OUTLINE: until that ruling the Aims
were written at DRAFT, and the card had to wait two phases for its stake.

Two smaller consequences fall out of the same order:

```text
  the address is FROZEN before a card points at it, so `serves: C4.P1.B4`
  can never name a bullet that was renumbered after the tick

  the card count starts honest. `6 serve · 0 answered` on the 🧭 tab is a true
  reading of a page nobody has dispatched yet
```

## 📮 One mark is not one card

The plan marks what a SENTENCE owes. A card is what a BANK can answer. Those are
different units, and PROBE is where they are matched.

```text
  many bullets ─▶ one card    the usual case. `PP04` on QC1-visitlbp serves
                              C3.P1.B3 · C3.P3.B3 · C7.P2.B1, because all three
                              are answered by reading one script.

  one bullet ─▶ many cards    legal. B4 may owe both a coefficient and the N
                              behind it, from two different runs.

  a mark ─▶ no card           only when a card already serving another bullet
                              answers it too. Add the address to that card's
                              `serves:`; never open a second one.
```

**A question is asked ONCE.** Before allocating, read the page's existing cards:
a duplicate card is the exact failure the id exists to prevent.

## 🔗 MATCH order · PageX is reuse, not another bank

Before PROBE dispatches anything, it runs the same ordered lookup for every
value or reference obligation:

```text
1. current Page cards and Bibex
2. PageX borrowed files and the source Page's live material
3. task/discovery QA bank, by reading a specific answer
4. only then: create a new card and dispatch
```

PageX is a ranked live borrow list, not a second QA bank and not a new phase.
It may reveal an exact existing Probe answer, proof file, or Display unit. When
the answer is exact, create a local binding that points to the existing QA
path or cite the fully qualified Display id; do not ask the bank again. A
topic-similar PageX file is only a candidate: if it does not literally answer
the Q-executor, `bank: new|run|code` remains the honest verdict.

The lookup must leave a small audit trace in the PROBE receipt:

```text
match: PP03 · PageX/QC0-results/probe/PP02/card.md · reuse
match: B4   · no exact PageX/QA answer · new → dispatched
```

The board's `POST /_board/pagex-match` endpoint can produce the read-only
candidate shortlist. Its overlap score is navigation only; PROBE must open the
candidate and record `reuse` only when the neutral Q-executor is literally
answered. A shortlist entry is never evidence by itself.

This is the smoothness rule: reuse is cheap and visible, while a new Probe is
opened only after the nearest existing answer has been read and rejected.

✅ **The MATCH-runs-late defect is CLOSED (260819).** It was open from 260818,
when JL put the lookup before DRAFT: "OUTLINE, then the probe (pagex), and the
draft". This contract agreed about MATCH and refused about the card, on one
argument: the card's `consumer/` side carries the STAKE, the stake is an Aim, and
Aims were written at DRAFT.

**That argument died the next day.** JL ruled the Aims into the plan file itself
(260819, `haipipe-page-outline` 0.3.0), so the stake is on disk before this phase
starts and nothing about the card needs DRAFT any more.

```text
  was   🧭 OUTLINE ─▶ ✏️ DRAFT ─▶ 📮 PROBE     the page paid for its scaffolds,
                                              then found the answer existed
  now   🧭 OUTLINE ─▶ 📮 PROBE ─▶ 🃏 EVIDENCE ─▶ back to OUTLINE
                      the lookup runs before anything is written
```

So MATCH is not split out as its own phase, and does not need to be: the whole of
this phase now sits where MATCH wanted to be.

**This phase routes back to ① OUTLINE, never forward to DRAFT.** What comes back
either confirms the plan or changes it, and only the plan's own four-check gate
ends the PREPARE loop.

## ↩ The link runs BACKWARD, and the number is allocated here

```text
  card.md      serves: C4.P1.B4 · C3.P1.B3      ← written by PROBE
  the bullet   knows nothing about the card      ← the plan never changes
```

The number is the next free `PP<NN>` **on that page**, two digits, allocated at
creation and never reused; the slug is the plugin's naming rule. A bullet reads
as done only when EVERY card in its backlink has LANDED (`answered`,
`answered-local` or `read`), never when any one has, because "one number landed,
one question still open" is not an answered bullet.

The backlink's shape and the four counts live in `haipipe-plugin-probe` §↩.

## 🧭 Which marks PROBE acts on

The plan carries five marks and only some of them are questions:

```text
mark          PROBE creates                          why
──────────────────────────────────────────────────────────────────────────────────
📮 probe      probe/PP<NN>-<slug>/                   always. This is the phase.
📚 citation   probe/PP<NN>-<slug>/ ONLY when the      a known key is landed by a
              key is UNKNOWN and the bank must        PERSON into bibex/ and needs
              find the work                           no question asked
🖼 display    NOTHING                                 a unit's intake/ freezes FROM
                                                      a proof/ that does not exist
                                                      yet. EVIDENCE creates it.
🎯 aim        NOTHING                                 the plan's own (Aims live in
                                                      the plan since 260819),
                                                      tracked in ## States
🧮 value      NOTHING                                 already landed: the mark
                                                      quotes `PP<NN>.v<n>` out of
                                                      an answered card's ## Values
```

A page whose plan carries only 🎯 and 🧮 marks skips PROBE entirely. That is the
phase being unnecessary, not being skipped.

## 🧱 What crosses, and what the wall is

The wall is a PATH, not a paragraph (`haipipe-plugin-probe`):

```text
consumer/    the Q-consumer + the STAKE          🚫 never crosses
executor/    the stripped Q-executor             ✅ this, and only this, is sent
proof/       manifest.yaml only · files: []      EVIDENCE pulls into it
card.md      state: planned → commissioned       🚫 never `raised`/`working`:
                                                 retired by the plugin 0.7.0
```

PROBE dispatches to the bank by agent, in a clean context, and the clean context
IS the wall: `haipipe-task-orchestrator-agent` for work the task layer owns,
`haipipe-discovery-orchestrator-agent` for work the literature owns. What comes
back is a PATH to a QA file. Binding that path is EVIDENCE's, not this phase's.

## 🔀 Exit and routing

```text
every marked bullet served, every card planned  ─▶ ③ EVIDENCE
the bank already answered this question          ─▶ point the card at it; still EVIDENCE
no route can answer it                           ─▶ HOLD, named, with the reason
the plan turns out to owe the wrong thing        ─▶ ① OUTLINE, a v2, never a quiet edit
```

PROBE never routes to DRAFT or REVISE: a card that was opened and never landed
supports no sentence, and the plan is the only thing that may declare the
PREPARE loop finished.

## 🧾 RUN receipt

```text
phase: PROBE
outline: <page>/outline/<stem>-outline-v<N>.md   look: 🧑 <who> <date>
         🚫 not `approved:`. The 🧑 LOOK after the round's ① pass is what
         releases this phase; the `approved:` tick closes the round later.
marks: 📮 <n> · 📚 <n> asked · 🖼 <n> deferred to EVIDENCE
cards: one row per card · PP<NN> · serves: <addresses> · state · dispatched to
       🚫 a state word outside the plugin's ladder is a defect, not a variant
coverage: <n> of <n> marked bullets served      🚫 a gap is a HOLD, not a pass
next: EVIDENCE | HOLD | OUTLINE
```

**`coverage` is the line that catches this phase's failure mode.** Declaring a
card is free; the receipt reports how many marked bullets actually got one, and
a phase whose declared and created counts disagree stops rather than reports
(`haipipe-page-workflow` §🪞).

## 📂 Files

```text
page-workflows/haipipe-page-probe/
├── SKILL.md            this phase contract
└── CHANGELOG.md        version history
```

Owns no scripts. The base is `haipipe-page`; the folder and its counts are
`page-plugins/haipipe-plugin-probe`'s; the crossing protocol is
`probe/haipipe-probe`'s; the plan and the 🧭 tab are
`page-plugins/haipipe-plugin-outline`'s; the loop and the receipt are
`haipipe-page-workflow`'s. The next phase is `haipipe-page-evidence`, which
fills what this phase raised.

**This phase in six fields** (❓ asks · 📥 reads · 📤 writes · 🚪 exits · ✋ tick · 🔀 routes):
`../haipipe-page-workflow/ref/phase-cards.md` §②. That file states every phase in the SAME fields, so one phase can be read next to another; this contract states the reasoning behind them.

**The Board page that argues this contract** is `QPw3-probe` on `BoardSkillBoard-260722`, created 260818 when JL ruled one page per workflow step. Its `## Law` rows and its `### Decision Now` carry what this contract leaves open.
