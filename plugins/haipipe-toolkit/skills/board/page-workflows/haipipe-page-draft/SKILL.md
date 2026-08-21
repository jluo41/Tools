---
name: haipipe-page-draft
description: >-
  The DRAFT phase contract for any Board Page. DRAFT is the PLANNING phase: it is the authority to define or reopen the Page's purpose, Aims, and promised shape for one round, It ENTERS on an approved outline (phase ①, haipipe-page-outline) and executes it, naming no division the plan did not name. It is not identified by an empty file, first typing, or adding text. Load haipipe-page first, then the matching Page Type under page-types/, then this contract, and finally the stage's declared family craft files. Use when creating a Page promise, changing what an existing Page is for, adding or removing an Aim, starting a new round after REVISE or CHECK, or naming a hole and the Aim it costs without opening a card for it. Trigger: page draft, DRAFT phase, define purpose, reopen Aims, new round, the page's promise, owned hole, stake, draft boundary, who creates the card, /haipipe-page-draft.
metadata:
  version: "0.9.1"
  last_updated: "2026-08-21"
  summary: "DRAFT creates no card: it enters on landed evidence and writes each Point as sentences citing ids; PROBE (phase ②, before it) turned the marks into cards, and a hole is the blocked exception. A Log row is one line, 15-35 words, not a paragraph."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-draft · give one Page a promise

Load the contracts in this order:

```text
haipipe-page
  → matching page-types/ variant, when one exists
  → haipipe-page-draft
  → family craft: the stage's declared craft files, when the Page belongs to paper or application
```

What is DRAFT's alone: the promise may move here, and nowhere else without a new round.
Its risk runs in one direction: presenting an unavailable answer as settled fact, because a hole hidden at DRAFT reaches print wearing the same face as a real number.
So DRAFT's exit is not polish; it is a stable purpose, its Aims, and every unknown named with an owner.

## ⚡ Brief

```text
Q          convert the approved plan into page prose: one approved POINT
           becomes one or more SENTENCES that write the NUMBER, citing
           evidence by id (PP01.v1 · Display4 · a bib key)
WRITES     the target page's sections per §✍️: Opening · Diagram · Content ·
           Aims (transcribed from the plan) · States · Files · Log

WALLS
  enters only on an approved outline; names no division the plan did not name
  never edits the plan it executes; a wrong plan routes to OUTLINE for a
    v<N+1>, never a quiet fix here
  never invents a number, citation, interpretation, or rendered Display
  a hole is the BLOCKED exception and names the input it is missing;
    an unnamed blocker means PREPARE exited early: fix at OUTLINE, never here
  creates NO card: the mark-to-card move is PROBE's
  Content states the PRESENT: no past-tense contrasts, no bare date codes
    (the Log holds the past)
  reads the Page Type's outline: mode before shaping anything
    (fixed | grammar | resolved | no key = base order only)

READ ECONOMY
  read fully ONLY the target page, the plan, and this brief
  trust the plan's Answered:/Drawn: values as written; re-read only cards
    whose line ends `· recount`, plus one spot-check (this file §📖)
  batch shell calls; scope cli/check.py output to your page with grep
  never paste board-wide output or compile logs into your context; the
    board doors return compact JSON, use them

ROUTES (§🔀 · 🚫 never EVIDENCE, never COMPILE, never CLOSE)
  a Task/Discovery-backed claim lacks support → PROBE   (bank MATCH, then cards)
  an existing-Page obligation is wrong/missing → OUTLINE (repair PageX binding)
  promise is stable but realization needs work → REVISE
  version is ready for judgment     → CHECK
  promise still unsettled           → DRAFT again

FUSED    an unchanged promise may continue straight into REVISE in the same
         context; the second half runs under haipipe-page-revise's contract
         (../haipipe-page-workflow/ref/page-run-contract.md §The fused ④+⑤ pass)

RECEIPT  one phase receipt per pass, shape in §🧾 below; field law:
         ../haipipe-page-workflow/ref/page-run-contract.md
         §Receipt step, field by field
```

Open the full contract below only where this brief does not settle your case; the full text wins every conflict.

## 📥 DRAFT now ENTERS on landed evidence (260819)

Ruled by JL: "until outline is self-consistent and together with all the evidence
cards, then we are good to go ahead to draft."

```text
  was   🧭 OUTLINE ─▶ ✏️ DRAFT ─▶ 📮 PROBE ─▶ 🃏 EVIDENCE ─▶ 🖊 REVISE
                       writes <VALUE HOLE> and waits two phases

  now   ┌ 🧭 OUTLINE ⇄ 📮 PROBE ⇄ 🃏 EVIDENCE ┐  loops until self-consistent
        └──────────────┬───────────────────────┘
                       ▼
                    ✏️ DRAFT   writes the NUMBER
```

**So a hole is now the EXCEPTION, not the normal case.** It is what a genuinely
BLOCKED question leaves behind, and it must name the input that is missing rather
than just marking a gap:

```text
  ✅ "Four phases have no measured duration [PP05: the receipt shape carries no
      start/end pair, and three phases have no receipt at all]"
  🚫 "The effect is <HOLE>."   on a page whose PREPARE loop said it was done
```

A hole with no named blocker means the PREPARE loop exited early, and the fix is
a `v<N+1>` at OUTLINE, not a placeholder here.

**What DRAFT keeps** is the conversion, which is the whole phase: one approved
POINT becomes one or more SENTENCES, each citing the evidence it uses by id
(`PP01.v1`, `Display4`, a bib key) rather than restating it.

## 📖 Trust the plan's answers; recount only what is marked (JL 260820)

The approved outline already carries every landed value inline, because the
PREPARE loop appends `Answered:` and `Drawn:` lines in place (有问有答,
haipipe-plugin-outline §✂️). Re-deriving all of them from disk is what made
QPw00's first DRAFT re-read 7 cards and 7 READMEs to confirm numbers the plan
already stated, and it found drift in exactly the values that count the run
itself.

```text
  trust      every Answered:/Drawn: value, quoted from the plan as written
  recount    ONLY a value whose Answered: line ends in `· recount` — the
             outline marks these because they count the run's own artifacts
             (receipts, findings, a pinned hash) and so move under DRAFT's
             feet; re-read just that card and quote the card
  spot-check one card of your choosing; a mismatch there means the plan is
             stale and the route is OUTLINE, not a silent correction
```

The card stays the binding source; what this rule removes is the blanket
re-read, not the hierarchy.

**The fused ④+⑤ pass**: when the promise is unchanged, the controller may
ask this phase to continue straight into REVISE in the same context
(haipipe-page-workflow ref/page-run-contract.md §The fused ④+⑤ pass). The
second half runs under haipipe-page-revise's own contract and writes its own
receipt step; nothing about either phase's walls changes.

## 🎯 The authority test

DRAFT decides what the Page is trying to become in the current round:

```text
owns       purpose · Aims · the page's promise  (the OUTLINE left 260817)
may do     add · delete · move · rewrite
exits      when the outline is stable enough to test, investigate, or realize
```

An operation does not identify DRAFT.
Adding a paragraph for an existing Aim is REVISE.
Adding a new Aim, removing a promised result, or changing the Page's purpose is DRAFT.

DRAFT may run on an empty Page, repeat before handoff, or reopen a mature Page after REVISE or CHECK.
Returning to DRAFT because purpose or Aims changed starts a new round on the same persistent Page.

## 🧬 Three layers own the page, and only the third is DRAFT's

Content shape has an owner at every altitude, and DRAFT's first move is to find out which layer already answered (JL 260816: "there are structure for the page format, right? but there is not structure for the content").

```text
layer        owner                       fixes                          for
──────────────────────────────────────────────────────────────────────────────────────
FRAME        haipipe-page · QPs1         the SECTION ORDER              every page kind
             "every kind opens in the same order, and only Content changes shape"
CONTENT      the matching Page Type      the DIVISION SHAPE             one page kind
             for-design: one division per candidate · for-view: exactly four
             (QA inputs · View body · Displays · Consumers), topic-specific
             subsections only under division 2 · for-skill: the generated bytes
INSTANCE     DRAFT                       THIS page's actual outline     one page
```

**Read the Page Type's declared shape before proposing anything.** DRAFT INSTANTIATES that shape for this subject, and inventing a different one when the Page Type declares one is the defect.

**No `page-type:` key is the DEFAULT, not a defect** (JL 260819: "question itself just to be very flexible"). It was read as a defect until then, which made OUTLINE illegal on 247 of this repo's 274 pages: a page with no type has no declared division shape, so the only shape it owes is the base section order. A key is what a page carries when its shape is genuinely special enough to earn a contract; carrying one to say "I am ordinary" would make the default a thing you declare, which is not a default.

Every Page Type declares HOW it supplies its outline, in an `outline:` block in its own frontmatter (JL 260816: "for the page-types, we should have this outline to be ready first, and then people can fill it"). Read that block first; it tells you what DRAFT is even allowed to decide:

```text
mode       who names the divisions              what DRAFT does
──────────────────────────────────────────────────────────────────────────────
fixed      the type lists them outright         fill them. Do not add, drop,
           for-view · for-design · for-venue    or reorder.
           for-skill · for-meeting · for-dash
           for-narrative
grammar    the type fixes a closed first-word   choose HOW MANY of each and
           set + an order/repeat rule           write the free title after
           for-task: Data · Why · Result(×n)    the fixed word
                     · Meaning(last)
resolved   the outline lives outside the type   RESOLVE it, then choose the
           for-section: (venue × kind) →        variant. Never invent one, and
             venue/playbook-*/…/template.md     never copy a sibling's shape.
           for-stage:   stage.md's product      A missing source is a HOLE.
```

GRAMMAR is the mode to reach for when a type must be ready before anyone knows the content: the closed word set makes the skeleton fillable on day one while the free title still carries this subject's own families. FIXED suits a type whose divisions never vary; RESOLVED suits one whose divisions are richer elsewhere than any generic shape could be.

**When the Page Type's shape is CONTAINER-shaped, the subject still goes at division level.** A container shape names where material came from and where it goes; `page-type: view`'s four divisions are one, which is why a seven-result-family regression report written to it prints `QA inputs` and `Displays` as its top-level sections and buries main OLS, robustness, IV, DID, and heterogeneity as subsections of `View body`. That is a readable View and an unreadable report, and it is what JL was reading when he asked why the content was not structured by result family (260816). Put the subject's families under the division the type leaves free, number them, and record the mismatch as a finding against the Page Type rather than silently reshaping the type.

## 🗂 The OUTLINE moved OUT of this phase (JL 260817)

DRAFT owned the outline until 260817 and no longer does. It is now phase ①,
`page-workflows/haipipe-page-outline`, with its own file and its own human gate.

```text
  ① OUTLINE   the SHAPE: sections · paragraphs · bullets · what each owes
              a versioned file, approved by a person       ← was DRAFT's
  ④ DRAFT     purpose · Aims · the page's own promise      ← what stays here
```

**Why it left.** One phase owning both "agree the shape" and "write the page"
let a single done-report cover both, and on `QC1-visitlbp` the outline table was
pasted into the page's own `## Content`, where it went stale at the next edit.
Changing a section list before the prose costs one line; after the prose it
costs the prose.

DRAFT now ENTERS on an approved outline and executes it: it names no division
the plan did not name. When the plan itself turns out wrong, that is a return to
OUTLINE and a `v2`, not a quiet edit here.

## ✍️ What DRAFT may write

DRAFT may write any Page section needed to expose the promise, subject to the base and matching Page Type.

```text
🧭 Opening      states the purpose now being promised
🖼 Diagram      exposes the promised shape when a figure helps
📚 Content      makes the proposed substance concrete enough to test
🎯 Aims         creates, removes, or changes the durable targets
📍 States       creates the factual initial row for each Aim
📎 Files        records the few continuations the round depends on
🗃 Log          records that the promise opened or changed
```

DRAFT is not the only phase allowed to create text or sections.
REVISE may add, delete, move, and rewrite under a fixed promise.
The difference is authority, not the visible diff.

## 🕰 Content states the present; the Log holds the past (JL 260820)

"我们这里不是做 log 的地方，content 永远只包含最新的东西." A Content sentence
never narrates what something used to be. When a rule, a number, an address,
or a shape has changed, write the current one as if it had always been so,
and let `## Log` and the run's receipts carry when and why it moved.

```text
🚫 "Before 260819 the plan wrote an id and this page held the target,
    so a renumber pointed A5.1 at the OLD A5.1"
✅ "The plan carries the target; this page realizes it by address"
    + Log row: 260819 · targets moved from the page into the plan
```

Why: a page is re-read for months, and every past-tense contrast is a date
the next reader must resolve before trusting the sentence next to it. The
same principle binds the plan's bullets at OUTLINE (haipipe-page-outline) and
REVISE's polish; history written into Content is a finding, not color.

The rule is really about ATTRIBUTION. `## Content` is the OFFICIAL document:
it states each rule as a fact of the system, and never says who decided it or
when. Both halves of an attribution are therefore banned from Content prose:

```text
banned in Content      a bare date code ("260819", any YYMMDD)
                       a person's name as authority ("JL ruled…",
                       "(JL 260819)", "per JL")
where they live        ## Log rows (what changed, when, on whose word)
                       ## Discussion (the quoted ruling itself)
                       tick grammar (approved: ✅ JL …, verified = {…}) —
                       ticks are signatures, not prose
the test               delete the name and the date; if the sentence
                       loses meaning, it was a Log row wearing prose
```

Ruled twice on 260820, reading the compiled PDF: "什么叫 260819 啊…我的目的
就是使这些 content 非常非常 readable" and "don't say too much 'JL' or
'YYMMDD', this is the official document".

## 📏 A Log row is one line, not a paragraph (JL 260821)

"make sure to make the logging content to be as concise as possible, current
it is too long. not good." A `## Log` row states the headline fact and stops;
it does not narrate the investigation that found it.

```text
🚫 "260820 1241 CC · REVISE pass, second look at the 1227 pass.
    Cross-checked every number the 260820 rebuild touched against
    `fetch_photos_delta.log`, `image_index.parquet` and both store
    READMEs and found four the 1227 pass had missed. `~104 url/s` for
    the delta fetch (§2.3 diagram and A2.2) was the peak instantaneous
    rate off the log's mid-run lines; the log's own `DONE` line gives
    89,010 urls in 0.26 h = ~95 url/s, and both occurrences now read
    `~95`. §4's summary table still carried `0.96% caught`..."
    (six more clauses follow)
✅ "260820 1241 CC · REVISE: fixed 3 more missed numbers (url/s
    peak-vs-avg, stale byte-repeat %, stale duplicate row). NPI2Photo's
    own README still carries the old baseline; flagged, not fixed here."
```

Roughly 15-35 words. One clause for the headline fact, at most one more for a
genuinely load-bearing caveat (who else owns a flagged gap, what stays open).
Every number, file path, and sub-step the long form listed is still
recoverable: from the diff, from a run receipt under `_runs/page/`, or from
the Content/States/Aims the change actually landed in. The Log's job is
"what changed", not "how I found it".

**Do not retroactively rewrite an OLD Log row to comply.** A Log is a
historical record; a row written before this rule existed stays as it was
written, verbose or not. Apply the rule going forward, starting from the
session that learned it.

## 🧱 Point → sentence scaffold

An approved Outline Point is a content unit, not necessarily one sentence.
DRAFT enters on landed evidence (§📥) and instantiates each Point as one or
more sentences that write the NUMBER, citing each id in place:

```text
C3.P1.B4 · Robustness across specifications   🧮 PP01.v1 · 🖼 Display4
        ↓ DRAFT
C3.P1.S1 · The primary estimate is 0.42 (PP01.v1).
C3.P1.S2 · It moves by less than 0.03 across specifications (PP01.v2).
C3.P1.S3 · Display4 compares the estimates.
```

The sentence may not invent a number, citation, interpretation, or rendered
Display: everything it states arrived through the PREPARE loop and is cited
by id. A hole is the BLOCKED exception (§📥), and it names the input it is
missing rather than just marking a gap:

```text
C3.P1.S2 · It remains <HOLE: PP02 blocked, no run for the IV spec> across
           specifications.
```

The address is the join key; the final sentence may expand, merge, or split
under REVISE while retaining `realizes: C3.P1.B4`.

For the live join, keep that backlink machine-readable in an HTML comment on
the sentence line, without making it reader-facing prose:

```text
C3.P1.S1 · The primary estimate is 0.42 (PP01.v1). <!-- realizes: C3.P1.B4 -->
```

REVISE performs the polish half: it improves the reader-facing prose and the
captions under fixed Aims, and it never changes a landed number.

## 🕳 Name the hole and the Aim it costs, then stop

When the Page needs a fact it cannot support, DRAFT leaves a VISIBLE hole in the
target prose and records which Aim goes unmet if it stays a hole.

```text
target prose     "The effect is <HOLE>." [Q-<local-id>]
## Aims          the Aim that hole belongs to
## States        that Aim's honest current row
```

The stake is exactly that pairing: what the Page loses if the answer never
comes. PROBE copies it into the card's `consumer/` side; DRAFT writes it here
and opens no file under `probe/`.
The Page Type or family names the physical hole and id shape.
Never invent a value or source to avoid a hole.

## 🃏 DRAFT creates NO card (260817, reversing 260816)

DRAFT was allowed to create the evidence card in OWED state until 260817. It no
longer is, and nothing replaces the move: **the outline's MARK is the proposal,
and `haipipe-page-probe` turns it into a folder.**

```text
① OUTLINE   `- B4 · the four coordinates      📮`   the mark. Nothing on disk.
② PROBE     probe/PP<NN>-<slug>/ · serves: C4.P1.B4
④ DRAFT     the sentence that writes the answer     ← what stays here
```

**Why it left.**

```text
duplication   a card that only repeats the mark is a second copy of the plan,
              which is haipipe-page-workflow §🪞 exactly
```

A second reason about the stake died 260819: Aims live in the plan since then,
so the card carries its stake from the plan and PROBE runs before this phase.

So DRAFT still names the hole and its owner. It does not open the file:

```text
DRAFT owns       purpose · Aims · the promise · the visible hole in target prose
PROBE owns       the card · its number · its Q-executor · serves: · the dispatch
EVIDENCE owns    the landed citation · the answered value · the frozen intake
```

## 🔀 Exit and routing

DRAFT has no mandatory next phase.
Route by what the Page now needs:

```text
Task/Discovery-backed claim lacks support → PROBE   (bank MATCH, then cards)
existing-Page obligation is wrong/missing → OUTLINE (repair PageX binding)
promise is stable but realization needs work → REVISE
version is ready for judgment     → CHECK
promise still unsettled           → DRAFT again
```

A Page Type or local contract may declare a gate.
DRAFT never invents one.

## 🧾 RUN receipt

When called by RUN, read `../haipipe-page-workflow/ref/page-run-contract.md` and
return its common phase receipt. DRAFT's receipt must additionally make these
facts explicit:

```text
reason             which purpose, Aim, or promised shape DRAFT defined
artifacts          the target Page and any declared source it changed
evidence           the exact Page locations that expose the promise
route              DRAFT | PROBE | REVISE | CHECK | HOLD
                   🚫 not EVIDENCE, not COMPILE: EVIDENCE is reached only
                   through PROBE inside the PREPARE loop, and COMPILE is
                   folded into REVISE (260819)
reopens_promise    false for repeated DRAFT in the same unsettled round
```

DRAFT never routes directly to CLOSE and never calls its own output checked.
If this DRAFT was entered from another phase, the controller already opened the
new round; DRAFT records that round rather than incrementing it again.

## 📂 Files

```text
page-workflows/haipipe-page-draft/
├── SKILL.md            this phase contract
└── CHANGELOG.md        version history
```

Owns no scripts.
The base is `haipipe-page`; Page Type variants live under `page-types/`; the shared question crossing is `probe/haipipe-probe` and begins at ② PROBE, which owns the crossing and the dispatch.
The Board engine owns execution and audit; this phase owns only its authority and receipt.

**This phase in six fields** (❓ asks · 📥 reads · 📤 writes · 🚪 exits · ✋ tick · 🔀 routes):
`../haipipe-page-workflow/ref/phase-cards.md` §④. That file states every phase in the SAME fields, so one phase can be read next to another; this contract states the reasoning behind them.

**The Board page that argues this contract** is `QPw2-draft` on `BoardSkillBoard-260722`, created 260818 when JL ruled one page per workflow step. Its `## Law` rows and its `### Decision Now` carry what this contract leaves open.

## ✅ Exit checklist: the official-document sweep

Before this phase returns, run the board checker scoped to the page and clear
every `content-attribution` line your pen owns: no bare date codes, no person
named as authority, in `## Content` or Diagram prose. A flagged line inside a
frozen display transcription is LISTED for the display walk, never edited
here.
