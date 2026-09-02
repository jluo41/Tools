---
name: haipipe-page-draft
description: >-
  The DRAFT phase of a Board Page, step 1 of the WRITE cycle: one pass that turns the approved
  plan and its landed evidence into the page. A Section plan's sentence slot
  becomes one sentence; any other plan's point becomes one or more sentences;
  every sentence names its slot, every number carries its provenance lane,
  no hole token reaches the prose, and the old-to-new diff folds under one
  log record. Trigger: page draft, DRAFT phase, slot to sentence, write the
  number, track the change, /haipipe-page-draft.
metadata:
  version: "0.10.1"
  last_updated: "2026-09-02"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-draft · one pass that turns the plan into the page

Load, in this order: `haipipe-page` (the base), the Page Type, this file,
`haipipe-plugin-outline/ref/plan-grammar.md` (to read the plan), and
`haipipe-sentence` (the lanes this pass writes).

## ⚡ Brief

```text
Q        write the page from the approved plan and the landed evidence: a
         slot or a point becomes sentences that carry the number and cite
         their evidence by id
READS    the approved plan (Answered:/Drawn: trusted; `· recount` re-read) ·
         the page · outline/<stem>-requirement.md (generated V<n> plus
         authored W<n>) · the cards and units the plan cites
WRITES   <page>.md: Opening · Diagram · Content · Aims (rows and Now:) ·
         one record in outline/<stem>-log.md
WALLS    enters only on approved: ✅ · names no division the plan lacks ·
         never edits the plan (a wrong plan routes to OUTLINE for v<N+1>) ·
         invents no number, citation, interpretation or figure · writes no
         hole token into prose · opens no card · writes no Files, Log,
         States or Discussion section (all live in outline/) · Content
         states the present, no dates, no names as authority
ROUTES   OUTLINE (a claim lacks a landed run → SURVEY; the plan is wrong → SHAPE) ·
         REVISE (promise stable, realization needs work; may run fused in
         the same context) · CHECK · DRAFT again · HOLD
         never EVIDENCE, never COMPILE, never CLOSE
RECEIPT  §🧾; field law: ../haipipe-page-workflow/ref/page-run-contract.md
```

## ⓪ Boot · enter on landed evidence

- **The OUTLINE part has run** (SHAPE ⇄ SURVEY ⇄ LAND ⇄ EMBED), so the
  plan carries every landed value inline, each traced to a run. DRAFT writes the number; a hole is
  the exception and names the input it is missing.
- **Trust `Answered:` and `Drawn:` as written.** Re-read only a card whose
  line ends `· recount`, plus one spot-check; a mismatch means the plan is
  stale and the route is OUTLINE, not a silent correction.
- **In session or as `haipipe-page-draft-agent`, the trace is the same**: the
  page, the log record, the receipt. The WRITE cycle continues into
  `haipipe-page-revise` in the same context and writes that phase's own
  receipt step.

## ① The conversion, by Page Type

```text
page-type: section   one SLOT → one SENTENCE (two slots may make one sentence
                     when the plan pairs them)
  plan   C2.P3.B1 · S6 · C1: +9.34 MME per visit, comparison owed
  page   In 767,736 low back pain encounters, physicians … write 9.34 more total
         MME per encounter than other physicians [Q-Sec0Abstract-1]. <!-- realizes: C2.P3.B1 -->
         sentence order = slot order; a paragraph is one `#### <n>. <its point>` block

any other type       one POINT → one or more sentences
  plan   C3.P1.B4 · Robustness across specifications   🧮 PP01.v1 · 🖼 Display4
  page   The primary estimate is 0.42 (PP01.v1). It moves by less than 0.03
         across specifications (PP01.v2). Display4 compares the estimates.
         <!-- realizes: C3.P1.B4 -->
```

- **`<!-- realizes: C<n>.P<m>.B<k> -->` ends every sentence** (or the last
  sentence of a point). It is the join to the plan, it survives REVISE, and
  the 🧭 tab reads it. A Section sentence without one is
  `sentence-without-realizes`.
- **A slot with no sentence, or a sentence with no slot, is a finding**, not
  a choice; the fix is OUTLINE, never a sentence the plan did not agree.

## ② Five rules every sentence obeys

1. **The number is written, and it carries its lane**:
   `> Value: <what> · <source page, bracket or card> · state=verified|provisional`
   directly under the sentence. A number with no lane is unverifiable
   (`number-without-lane`).
2. **No hole token in prose**, three cases: a real number not yet checked is
   written with `state=provisional`; a number that does not exist yet, where
   the sentence's shape needs it, is `{VAL:? what is owed} [Q-<id>]`, which
   renders as an unbound chip; a number that can be added as a clause later
   gets a clean sentence, a `> Comment CC` lane naming the item row, and the
   row at SURVEY. A hole with no named blocker means the OUTLINE part exited early: OUTLINE.
3. **Evidence is cited by id**, `PP01.v1`, `Display4`, a bib key, never
   restated; a display is cited where the plan drew it, and its caption is
   REVISE's.
4. **Content states the present.** No "it used to be", no bare date code, no
   person named as authority; the log carries who and when
   (`content-attribution`). The test: delete the name and the date; if the
   sentence loses meaning, it was a log record wearing prose.
5. **Plain words for a weak-English reader**: a term defined the first time
   it is used, a common word over a rare one, and nothing the venue refuses
   (V3).

## ③ What this pass writes on the page

- **Opening**: the visible paragraph above the first blank line, the drawer
  below it. **Diagram**: when a figure helps, redrawn to the plan's arc.
  **Content**: numbered all the way down (`### 3 ·`, `#### 3.1 ·`).
- **Aims**: the plan's 🎯 marks resolve to rows on the page. This pass writes
  a row the page lacks (target and `Done when:`) and every row's `Now:` as a
  fact about the draft (`drafted 0137: nine sentences, 229 words`); it ticks
  only what visible evidence shows.
- **Not on the page**: `## Files`, `## Log`, `## States`, `## Discussion`. A
  question this pass cannot answer is a `D<nn>` record in
  `outline/<stem>-discussion.md`.
- **The frame is `haipipe-page`'s, the division shape is the Page Type's**;
  this pass instantiates the shape for this subject and reshapes neither.
  When a container-shaped type buries the subject, the subject's families go
  under the division the type leaves free, numbered, and the mismatch is a
  finding against the type.

## ④ Track the change

- **One log record per pass**: `### YYMMDD HHMM · DRAFT from plan v<N>: <one
  line>`, with the `~~old~~ → new` diff folded under it, sentence by sentence
  (old first words → new slot → why). Nothing signed is deleted; a superseded
  `> Note:` candidate is kept verbatim in the fold.
- **A single-sentence change made later** (REVISE, or the page chat) is a
  `> ✎ ~old~ *new* · WHO · YYMMDD HHMM` lane under the sentence plus one log
  record; a whole-paragraph rewrite is the log record alone.
- **The plan is untouched** and the page Aim's `Now:` says what landed.

## 🔀 Routes

```text
a claim lacks a landed run                    → OUTLINE (SURVEY: the table gains a row)
the plan is wrong, or an existing-Page binding
  is missing                                   → OUTLINE (SHAPE)
promise stable, realization needs work         → REVISE (fused when the context continues)
version ready for judgment                     → CHECK
promise still unsettled                        → DRAFT again
```

A Page Type may declare a gate; this pass never invents one, never routes to
CLOSE, and never calls its own output checked.

## 🧾 Receipt

```text
phase: DRAFT
plan: v<N> approved ✅ <who> <date>
page: <page>/<stem>.md
sentences: n written · n realizes: · n with a Value lane · n provisional · n {VAL:?}
aims: n rows · n Now: updated · n added
log: <the record's headline>
route: DRAFT | OUTLINE | REVISE | CHECK | HOLD
reason: <the authority exercised and why this route follows>
reopens_promise: true | false
```

## ✅ Exit sweep

Before the pass returns, run the checker scoped to the page and clear every
line this pen owns: `content-attribution` 0 in Content and Diagram,
`sentence-without-realizes` 0 on a Section page, `number-without-lane` 0. A
flagged line inside a frozen display transcription is listed for the display
walk, never edited here.

## 📂 Files

```text
haipipe-page-draft/
├── SKILL.md            this phase
└── CHANGELOG.md        version history, and the only home for what this phase used to say
```

Owns no scripts. The base is `haipipe-page`; Page Type variants live under
`page-types/`; the plan grammar is `haipipe-plugin-outline/ref/plan-grammar.md`;
the lanes are `haipipe-sentence`'s; the run behind every number is found at
SURVEY and made at LAND (`haipipe-page-outline`, `haipipe-page-evidence`). The
six-field card is `../haipipe-page-workflow/ref/phase-cards.md` §WRITE. The design page is
`QPw2-draft` on `BoardSkillBoard-260722`.
