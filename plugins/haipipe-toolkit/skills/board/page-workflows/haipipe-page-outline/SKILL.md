---
name: haipipe-page-outline
description: >-
  The OUTLINE phase contract for any Board Page, and phase ① of the page workflow.
  It agrees the Page shape, types each evidence obligation, and uses Probe's
  PageX lane for exact accepted-Page bindings before prose is written. Task or
  Discovery obligations are handed to Probe's QA lane in the next phase. Its
  deliverable is a versioned file at <page>/outline/<stem>-outline-v<N>.md and it
  exits only when a person approves it. The Page Type supplies WHICH WORDS the
  plan may use; this phase supplies WHICH ARGUMENT their sequence makes, and
  runs that as the first of five self-consistency checks. Trigger: page outline,
  OUTLINE phase, plan the page, story arc, arc check, division order, PageX,
  accepted Page evidence, approve the outline, /haipipe-page-outline.
metadata:
  version: "0.10.0"
  last_updated: "2026-08-22"
  summary: "0.10.0 takes the ARC: the Page Type supplies WHICH WORDS a page may use and this phase supplies WHICH ARGUMENT they are arranged to make, so the sequence-is-the-argument rule, the three forbidden orderings and the swap test move here from haipipe-page-for-task and reach all ten types; self-consistency grows to FIVE checks with ARC first, and its third test is that the heaviest finding owns a division rather than a bullet inside someone else's. 0.9.0 put Aims in the plan file and made the version rule protect a promise, never a format."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-outline · agree the shape before writing a word of it

**LOAD `haipipe-page` FIRST**, then the Page Type, then this file, then `haipipe-plugin-outline` for the file's own shape. This contract owns the PHASE: its authority, its exit, and what it may not touch. The plugin owns the file and the tab, and this file never restates them.

## ⚡ Brief

```text
Q          agree the SHAPE of the page before a word of it is written:
           sections, paragraphs, bullets, and what each bullet still owes
WRITES     <page>/outline/<stem>-outline-v<N>.md only; never the page itself

WALLS
  never writes prose, lands a card, or dispatches a question
  never invents a division the Page Type does not allow (§📐: read the
    type's outline: block; fixed | grammar | resolved | no key = base order)
  never ticks `approved:`; that tick is a person's
  a tick belongs to the version it ticked: evidence moving an approved
    plan makes a v<N+1>, never a quiet edit
  heads and Notes state the PRESENT: no past tense, no bare date codes
  an answered ask is APPENDED to its own bullet, never re-bulleted;
    a built unit's Drawn: is transcribed from its README claim
  the four checks (① coverage ② address ③ value ④ shape) run and pass
    BEFORE the person is asked

READ ECONOMY
  read fully ONLY the target page, the plan, and this brief
  trust the plan's Answered:/Drawn: values as written; re-read only cards
    whose line ends `· recount`, plus one spot-check (haipipe-page-draft §📖)
  batch shell calls; scope cli/check.py output to your page with grep
  never paste board-wide output or compile logs into your context; the
    board doors return compact JSON, use them

ROUTES (§🔀)
  source: page ─▶ Probe/PageX exact-file binding here in OUTLINE
  source: task|discovery ─▶ Probe/QA after the person's LOOK
  any of the four ❌ ─▶ fix the plan HERE. The person is not asked yet.
  four pass, new Task/Discovery question ─▶ 🧑 LOOK, then ② PROBE
  four pass, existing card or other landing gap ─▶ 🧑 LOOK, then ③ EVIDENCE
  four pass, nothing owed, approved ✅ ──▶ ④ DRAFT
  not yet ⬜ ────▶ stay in OUTLINE, or HOLD if the person is unavailable
  a Page Type refuses the shape ──▶ fix the plan, never the Page Type,
                                    unless the mismatch is a real finding
                                    against that type (record it as one)

RECEIPT  one phase receipt per pass, shape in §🧾 below; field law:
         ../haipipe-page-workflow/ref/page-run-contract.md
         §Receipt step, field by field
```

Open the full contract below only where this brief does not settle your case; the full text wins every conflict.

## 🎯 The authority test

```text
owns       the SHAPE: which sections, which paragraphs, which bullets,
           and what each bullet still owes
           and the AIMS: one target plus its `Done when:` test each, agreed
           HERE and living in the plan file (moved off the page 260819, JL:
           "Aims should be move together with outline"; DRAFT transcribes)
may do     add · delete · move · rewrite, freely, while unapproved
exits      FOUR machine checks pass, THEN a person ticks `approved:`
           (the four are §🚦 below; the person judges DIRECTION, not arithmetic)
🚫 may not write prose · land a card · dispatch a question · invent a
           division the Page Type does not allow
```

How a bullet is WRITTEN — a terse Capitalized HEAD, then its folded
`Note:`/`Answered:`/`Drawn:` line, the mark last, every bullet carrying one of
the three — is the plugin's §✂️, stated once there and not restated here.

**A head or Note states the PRESENT, never the past** (JL 260820: "我们这里
不是做 log 的地方，content 永远只包含最新的东西"): no "Before <date> it was
X", no "this used to be Y". The plan describes what the page will SAY NOW;
what changed and when belongs to the page's `## Log` and the run's receipts.
A renumber or a reversal therefore rewrites the bullet clean instead of
narrating the old state next to the new one. Attribution is part of the same
rule: a bare date code ("260819") or a person's name as authority never sits
in a head or Note — the plan states the rule, and Log rows, Discussion, and
ticks carry who and when (haipipe-page-draft §🕰, ruled 260820).

## 📐 The Page Type's `outline:` block is READ, not assumed

**Every Page Type that exists already declares its mode.** All ELEVEN LIVE types
do, in an `outline:` block under `metadata:`. Until 260819 nothing in this phase
read it, so a plan's shape was whatever its author felt like:

```text
  mode: fixed      brief · insight · round · seed · venue          (5)
                   the type LISTS the divisions. Fill them. Do not add, drop
                   or reorder.
  mode: grammar    intervention · narrative · task                 (3)
                   a closed FIRST-WORD set plus an order rule. Choose how many
                   of each; write the free title after the fixed word.
  mode: resolved   artifact · section · stage                      (3)
                   the outline lives OUTSIDE the type, at the path its `source:`
                   names. RESOLVE it first. A missing source is a HOLE, never
                   a licence to invent one.
```

⚠️ **This list was wrong from 260819 to 260822**: it named `dash`, a RETIRED type,
and omitted `round`, a live one. The COUNT was accidentally right, which is why
nobody caught it for three days — and the retired type was still on disk, under an
`_archive/`, answering greps and looking authoritative.

That is what got the whole archive convention deleted the same day (JL: "我既然把
它变成 archive 了，意思就是说要把它们都删掉…旧的东西会误导我们"). Nine archive
roots, 487 files, removed from the skill tree; `skills/STRUCTURE.md` carries the
rule. A retired type is now DELETED, so this list can only ever drift by omission,
never by naming something that no longer exists.

`find <skills>/*/page-types -maxdepth 1 -type d -name 'haipipe-page-for-*'` is the
authority, and it is the only one.

Probe is the evidence-acquisition family. OUTLINE owns its PageX branch because
accepted Page context can change the plan before any QA work is dispatched.
PageX records exact accepted files and bounded scopes in `pagex/`; it never
creates a mirror `probe/` card. Task/Discovery obligations stay source-typed in
the outline and move to the QA branch during PROBE/EVIDENCE.

**No `page-type:` key is the flexible DEFAULT** (`haipipe-page-draft` 0.7.3): the
plan then owes the base section order and nothing more. That is 247 of this
repo's 274 pages, so the common case is no check at all beyond the base.

**This is a machine-checkable exit, and it runs BEFORE the person is asked.** A
plan whose shape contradicts its declared type wastes the one gate that is
supposed to be cheap:

```text
  fixed     a division the type does not list, or a missing one   ❌ reject
  grammar   a first word outside the closed set, or an order the
            rule forbids                                          ❌ reject
  resolved  no `source:` resolved, or a shape copied from a
            sibling page instead                                  ❌ reject
```

`checks/outline.py` reports it as `plan-shape-off-type`. A rejection here is not a
finding against the person; it is the phase refusing to spend a human tick on a
shape a file already answered.

An operation does not identify OUTLINE. Adding a section to the PLAN is OUTLINE; adding a section to the PAGE is DRAFT. The two are different files.

## 🎭 The TYPE gives the WORDS. This phase gives the ARGUMENT. (260822)

Ruled by JL, deciding where a story arc belongs when there are ten Page Types:
"我们也会有其他的 pages 所以这个 four types 就是我们提供什么样的 outline
template，然后 haipipe-page-outline 目的就是想要讲什么样的 story arcs."

```text
  the PAGE TYPE     WHICH WORDS this page may use, in what order,
  (10 of them)      and how many of each                     ── the TEMPLATE
                    read from metadata.outline, §📐 above

  THIS PHASE        WHICH ARGUMENT those words are arranged to make,
  (one of it)       on this page, this round                 ── the ARC
```

**Why the split had to be made.** The rule below lived inside
`haipipe-page-for-task` from its 0.7.0 until 260822, so nine other types had no
statement of it at all — and the failure it prevents is not task-shaped. Any
page whose divisions were ordered by the author's history passes every
mechanical check and still fails its reader. A `fixed`-mode type suffers it too:
the type lists the divisions, and the arc question becomes what each one is FOR
and whether the list, filled this way, argues anything.

**⛔ ROLE-COMPLETE IS NOT ARC-COHERENT.** A plan may carry every word its type
allows, each division correct and each in present tense, and still not be a
report. That is the commonest shape that passes every check and fails its
reader, and it fails for one reason: the order came from the author's history
instead of the reader's need.

**Three orderings all read as a log, and the third is nearly invisible:**

```text
  ① run order          the order the scripts executed
  ② config order       the order the yaml files sit in
  ③ 🔴 LEARNING ORDER  the order the AUTHOR found things out
```

① and ② are easy to catch, because the division titles carry the machinery's own
names. ③ survives every mechanical check. Each division states the present, cites
its evidence and names what the reader learns; nothing on the page mentions a
date. The diary is in the SPACING between divisions, and only a reader who does
not already know the story can feel it.

**The swap test, one question per boundary:**

```text
  For each pair of adjacent divisions, name why N must come before N+1.

  ✅ "Method must precede Result, or the number cannot be believed."
  ✅ "Data must precede Method, or the sample the method ran on is unknown."
  ✅ "Concept must precede Landscape, or the field map is in unmet terms."
  🔴 "That is the order we found them in."
     └─ reorder. A reason that is a date is not a reason.
```

Ruled 260820 (JL, on a Board plan whose divisions ran old-machinery, its-gap,
new-machinery, measurement, contract, proposal): every head was present tense and
every count was checked, and the divisions still fell into three blocks that
matched what was known before the session, what the session did, and what it left
open. The repair merged the two machinery divisions into one, because they are two
halves of one machine and their only separation was arrival time.

**⛔ THE BIGGEST FINDING GETS A DIVISION, NOT A BULLET INSIDE SOMEONE ELSE'S**
(260822, found by running this section against `QC1-postrain-replication` before
writing it). That page's largest measured effect — training cutting
non-termination roughly tenfold, on two benchmarks and two measurement surfaces —
was bullet `B7` inside a division titled for the run that happened to produce it.
The plan was coverage-complete, address-clean and value-checked. It was also
mis-weighted, and no existing check could say so.

```text
  a finding's WEIGHT is not what produced it, it is what a reader carries away
  ⇒ if the strongest sentence on the page cannot be found from the table of
    contents, the arc is wrong even when every division is correct
```

**What this section does NOT do.** It does not choose the words — the type did
that, and a word outside the type's set is a SHAPE failure, not an ARC failure.
It does not judge whether the plan aims at the right thing; that is the person's,
at `approved:`.

## 🚧 Why this is a phase and not a step inside DRAFT

It was a step inside DRAFT until 260817, and the day it stopped being one is on the record. One phase owned both "agree the shape" and "write the page", so a single done-report covered both, and the plan ended up pasted into the page's own `## Content` where it immediately went stale (`QC1-visitlbp`, CMSRegBoard).

**The gate is the cheapest one on the board, which is the whole argument for it.**

```text
  change a section list   BEFORE the prose   one line
  change a section list   AFTER  the prose   the prose
```

A phase whose entire output fits on one screen, and which a person can reject in ten seconds, belongs in front of every expensive phase rather than folded into one.

## 🔁 The PREPARE loop, and why this phase repeats (260819)

Ruled by JL: "outline 之后就直接 probe 准备证据，基于证据我们再改 outline，直到
outline 自己是自洽的."

```text
  ┌── PREPARE · repeat until self-consistent ─────────────┐
  │   🧭 OUTLINE ──▶ 📮 PROBE ──▶ 🃏 EVIDENCE             │
  │       ▲                            │                  │
  │       └──── the answer changes the plan ───────────────┤
  └──────────────────────┬────────────────────────────────┘
                         ▼ 🚧 ONE gate: the plan AND its evidence
                     ✏️ DRAFT
```

**Evidence does not confirm a plan; it changes it.** That is the whole reason
this is a loop and not a line, and 260819 produced two worked cases on
`QPw00-page-loop`: a division the plan wanted turned out to score 0 of 4 on the
split tests and was folded away, and a count of 17 was recomputed as 13. Neither
was a defect. A plan written before its evidence is a guess.

## 🚦 Self-consistent means FIVE things, and each one is checkable

"Until the outline is self-consistent" has to be a test, or the loop cannot stop
and "it feels about right" becomes the gate. It is these five, in this order:

```text
  ⓪ ARC        the division SEQUENCE argues something, and the plan says what
               ⓪.1 the plan carries one `arc:` line: the argument the sequence
                   makes, in one sentence. "This page reports the results of X"
                   is a table of contents, not an argument, and fails.
               ⓪.2 every ADJACENT PAIR passes the swap test (§🎭): name why N
                   must precede N+1. A reason that is a date, a run name or a
                   config name is not a reason.
               ⓪.3 the plan's HEAVIEST finding has its own division. A finding
                   a reader cannot reach from the division list is mis-weighted
                   however correct its bullet is.
               ⚠️ runs FIRST, because a plan with the wrong arc is not worth
                  address-checking; the other four verify a shape ⓪ accepts.
  ① COVERAGE   the plan⇄disk join, BOTH directions. Forward: every mark is
               served by at least one card — the PROBE receipt already
               reports `coverage: n of n`. Reverse: every display unit on
               disk is cited by ≥1 bullet, or retired; an orphaned 🖼 is a
               COVERAGE failure, not a footnote (JL 260819, on seeing
               Display4 under "on disk, cited by no bullet": "you should
               try to make every display to be used")
  ② ADDRESS    every card's `serves:` names an address this plan really has
               ⚠️ three cards on QPw00 pointed at renumbered bullets on 260819
  ③ VALUE      every recomputable number matches the repo
               `checks/values.py`, and it caught 17-vs-13 on its first run
  ④ SHAPE      the plan's divisions match the Page Type's declared mode
               `plan-shape-off-type`; no `page-type:` key = base order only
```

⚠️ **⓪ and ④ are different questions and neither substitutes for the other.**
④ asks whether the words are the type's; ⓪ asks whether their order is an
argument. A plan can pass ④ with every word legal and fail ⓪ because it is a run
log wearing correct prefixes — which is precisely the failure §🎭 exists to name.

**All five run BEFORE the person is asked.** That is what makes the human tick
worth something: a machine says the plan is consistent with what is on disk, and
the person answers the one question no file can, which is whether the plan is
aimed at the right thing.

⓪ is the one of the five a machine can only half-run: `arc:` present is
mechanical, and whether the sentence is an argument is a judgement the phase
makes and the person may overturn. It is stated as a check anyway, because a
judgement with a written form is arguable and one with none is not.

**An answered ask is APPENDED, never re-asked and never re-bulleted** (JL
260819, on `📮 PP04 answered · 5 values`: "我们其实需要更新一下这个 bullet
points，把那 5 个 value 也列出来，这样的话就是有问有答"): when a bullet's card
lands its `## Values`, the SAME bullet gains the answer — prose quoting each
value id inline (`PP<NN>.v<n>` then the number and its meaning) — and the 📮
mark stays end-anchored. The ask and the answer live on one bullet; a new
bullet for the answer is wrong, and an asking bullet left answer-less after
its card landed is fold debt.

The same rule reaches 🖼 (JL, same night: "做完之后把这个图填上去…再 append 到
bullet points 上，说这个 Display 已经做好了，并描述它说明了什么"): a built
unit's citing bullet gains `Drawn: <what the figure shows>`, TRANSCRIBED from
the unit's own README claim, never composed fresh. Evidence must WORK on the
plan's face: a value says what its number means, a display says what its
picture shows.

**The fold marks a self-referential value `· recount`** (JL 260820): a value
that counts the RUN'S OWN artifacts — receipts in `_runs/`, checker findings,
a pinned hash — moves every time a later phase appends, so its `Answered:`
line ends in `· recount`. DRAFT re-reads only these cards and trusts every
unmarked value as the plan states it (haipipe-page-draft §📖); QPw00's first
DRAFT re-read all 14 evidence folders to find 3 drifts, and all 3 were
self-referential counts.

⚠️ **A tick belongs to the version it ticked.** If evidence changes the plan after
`approved: ✅`, that is a `v<N+1>` and a new tick, not a quiet edit. On 260819 the
tick stayed on `v2` while `v2` was edited five more times, and all three stale
`serves:` addresses came from exactly that.

## 📦 The deliverable, and the one thing that ends the phase

```text
<page>/outline/<stem>-outline-v<N>.md      the plan · AUTHORED · versioned
        approved: ⬜  →  ✅                 🚧 a person, never a machine
```

The file's shape, its `C<n>.P<n>.B<n>` addressing, its five marks and its version rules are `haipipe-plugin-outline`'s, stated once there. What belongs HERE is what ends the phase: **a person reads the 🧭 tab and ticks `approved:`.** And the person's job there is to BREAK it, not bless it (JL 260819: "人看的时候不是去 approve，而是去 break——看看这个 outline 是不是你想要的，有些图是不是觉得不行"): hunt for the division that argues nothing, the figure that shows the wrong thing, the answer that dodges its ask. The tick means "I tried to break it and failed", which is the only meaning that survives a machine already having checked the arithmetic. No machine may write that tick, for the same reason no machine accepts a display render: what it judges is whether a plan is the right plan, and no check reaches that.

## 🔓 Before the tick it is a working document

```text
  ✍️ unapproved   discuss it · rewrite it · DELETE a bullet that is wrong
                  no version, no record, nobody agreed to it yet
  🔒 approved     frozen · correct as of that date
  ✍️ v2           the work moved on · `supersedes: v1` · v1 is KEPT
```

**The version rule protects a PROMISE, never a FORMAT** (JL 260819: "remove
all the legacy-grammar, I don't want to maintain the old things"). A plan
written under an older grammar is REWRITTEN into the current grammar on its
next OUTLINE pass — in place while unapproved, as `v<N+1>` when a tick froze
it, Aims moved into the file included. On 260819 `QC1-visitlbp`'s plan sat two
days in the 260817 long-sentence grammar because a fold pass read "append,
never edit" as covering format too, and no machine check said otherwise. The
sweep now FAILS such bullets as `bullet-missing-note` (`checks/outline.py`,
every plan, no legacy carve-out); a plan showing any may not be put to the
person.

**`v2` does not mean `v1` was wrong** (JL 260817). It means `v1` was right then and the work has since moved, which is why the old version is kept rather than corrected. A plan deleted while unapproved needs no record at all.

## 🕳 What OUTLINE does with a hole

A bullet may name evidence it does not have. That is the phase working, not failing:

```text
  ✅ "- B2 · Does the estimate survive the placebo test?   📮 PP02"
  ✅ "- B3 · Five coefficients at each rung        🧮 PP02.v1"
     names what is owed. PROBE dispatches it, EVIDENCE lands it.

  🚫 "- B2 · The five coefficients are stable"
     asserts an answer nobody has. That is not a plan, it is a guess.
```

OUTLINE marks the hole and STOPS. It does not raise the card, it does not ask the bank, and it does not write the sentence. A plan that already knows every answer was written after the fact.

## 🔀 Exit and routing

```text
  any of the four ❌ ─▶ fix the plan HERE. The person is not asked yet.
  four pass, new Task/Discovery question ─▶ the 🧑 LOOK, then ② PROBE
  four pass, existing card or other landing gap ─▶ the 🧑 LOOK, then ③ EVIDENCE
  four pass, nothing owed, approved ✅ ──▶ ④ DRAFT
  not yet   ⬜  ────▶  stay in OUTLINE, or HOLD if the person is unavailable
  a Page Type refuses the shape ──▶ fix the plan, never the Page Type,
                                    unless the mismatch is a real finding
                                    against that type (record it as one)
```

OUTLINE never routes to REVISE. A new Task/Discovery question never skips PROBE;
OUTLINE may route directly to EVIDENCE only for an existing raised card, a
citation/display landing gap, or another support item that needs no dispatch.

## 🧾 RUN receipt

The receipt records what a later reader cannot reconstruct: which version was produced, whether it was approved, and by whom.

```text
phase: OUTLINE
file: <page>/outline/<stem>-outline-v<N>.md
supersedes: v<N-1> | —
counts: sections · paragraphs · bullets · marks by kind
approved: ✅ <who> <date>  |  ⬜ waiting
next: OUTLINE | PROBE | EVIDENCE | DRAFT | HOLD
```

The counts go in because they are the honest size of the plan, and because a later phase's own exit test compares against them.

## 📂 Files

```
haipipe-page-outline/
├── SKILL.md            this phase contract
└── CHANGELOG.md        version history
```

Owns no scripts. The base is `haipipe-page`; the file and the 🧭 tab are `haipipe-plugin-outline`'s; the loop and the receipt are `haipipe-page-workflow`'s; the next phase is `haipipe-page-draft`, which no longer owns the outline.

**This phase in six fields** (❓ asks · 📥 reads · 📤 writes · 🚪 exits · ✋ tick · 🔀 routes):
`../haipipe-page-workflow/ref/phase-cards.md` §①. That file states every phase in the SAME fields, so one phase can be read next to another; this contract states the reasoning behind them.

**The Board page that argues this contract** is `QPw1-outline` on `BoardSkillBoard-260722`, created 260818 when JL ruled one page per workflow step. Its `## Law` rows and its `### Decision Now` carry what this contract leaves open.
