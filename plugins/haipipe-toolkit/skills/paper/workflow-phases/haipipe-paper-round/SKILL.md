---
name: haipipe-paper-round
description: >-
  Paper journey phase P5 (Round) and the Page Type contract for one bounded
  feedback-and-response cycle: an editor decision, reviewer round, or coauthor
  pass. Atomizes every concern into a coverage ledger, records dispositions,
  routes changes to the owning Pages, and closes with an approved response. Use
  when opening, triaging, answering, or closing a revision round.
metadata:
  version: "0.4.1"
  last_updated: "2026-08-31"
  group-token: "RD"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Round Identity and Intake → Feedback Coverage Ledger → Decisions and Response Strategy → Change Routing → Applied and Checked Changes → Response Package → Close Receipt and Handoff"
---

# /haipipe-paper-round · close one feedback cycle without losing an item

Load `haipipe-page`, then this Page Type, then `haipipe-page-workflow` for RUN.
Declare `page-type: round`.

## 🧭 Journey phase

This skill is journey phase P5 Round (respond) of the paper journey and owns
the `page-type: round` contract below. Opens on a feedback batch any time after
a telling exists. Closes through gate G7: every concern ledgered and routed
exactly once (Seed for new evidence, Narrative for retelling, Section for
rework) and a person approves the response receipt. `haipipe-paper-workflow`
holds the full gate assertions; this block only places the phase. The page
itself always runs through `/haipipe-page` and `haipipe-page-workflow` (OUTLINE
→ … → CHECK), never a private lifecycle.

## 🔄 Grain and boundary

Create one Round Page for one bounded batch of feedback against one named paper
build. Examples include one editor decision plus its reviews, one coauthor pass,
or one pre-submission audit whose concerns will be answered together.

```text
base paper build + received feedback
                  ↓
        one Round Page and ledger
                  ↓ routes work to
      Narrative · Sections · their evidence/plugins
                  ↓ returns checked versions to
       response package + revised build + close receipt
```

Do not create one Round per reviewer, comment, or changed Section. Keep every
atomic concern addressable inside the same Round ledger. Open a new Round when a
new decision or feedback batch arrives after closure.

A **Paper Round** is the persistent feedback cycle defined here. A **Page
workflow round** is a reopening era inside one Page's OUTLINE-to-CHECK receipt.
Never use one term or counter as the other.

## 🪪 Required identity block

Record the Round identity before triage:

```text
round-id          stable id within this paper
round-kind        editor-review · reviewer-review · coauthor · internal ·
                  foreign-desk (a review of this work's telling at a desk
                  with no Narrative on this board)
venue-page        selected Venue Page and version, or explicit none
narrative         governing Narrative Page and version · a foreign-desk
                  round parents to the SEED instead, with the desk named in
                  received-from, because its evidence still routes here
base-build        exact manuscript/PDF/version that received the feedback
received-from     editor, reviewer labels, coauthor, or internal authority
received-at       date and source location
response-due      date, explicit none, or unknown
```

Store supplied letters or memos INSIDE this Round page's folder — a received
letter floating at the repo root is homeless material (JL 260823). Preserve
their wording; never rewrite received material into a cleaner second source.
The runtime home is the DESK'S OWN ROUND GROUP (JL 260831, three groups per
desk): `0-paperboard/B<x>-<desk>-Round/RD<NN>-<event>/`, beside that desk's
-Main and -Appendix groups, so the desk's downstream story sits in three
named shelves. A foreign-desk round mints its desk's -Round group even when
that is the desk's only group. Boards with a combined `B<x>-<desk>` group or
the older lone `C1-RD-round/` group are grandfathered.

## 📐 Required Content roles

Keep all seven roles inspectable. Combine divisions only when their addresses
remain unambiguous.

```text
1  Round Identity and Intake
   identity block · received files · base build · scope · due date

2  Feedback Coverage Ledger
   one row per atomic concern; every received point appears exactly once

3  Decisions and Response Strategy
   accept · narrow · answer · decline · defer, with human authority and reason

4  Change Routing
   affected claim · Narrative row · Section · evidence/plugin obligation · owner

5  Applied and Checked Changes
   what changed · owning Page · before/after version · CHECK result

6  Response Package
   point-by-point reply, editor note, tracked-change/diff pointers, commitments

7  Close Receipt and Handoff
   ledger totals · revised build · response artifact · deferred items · next Round
```

## 📋 Feedback ledger contract

Atomize bundled feedback before routing it. Give every concern one stable id and
these fields:

```text
item-id
source actor and source anchor
verbatim quote or faithful pointer
issue kind and severity
exact concern
affected claim ids
affected Narrative row and version
affected Section or appendix Page
required evidence/citation/value/display work
human disposition and rationale
owning Page and owner
response strategy and response paragraph id
state
before version and checked after version
open blocker or explicit deferred handoff
```

Use `open`, `routed`, `applied`, `answered`, `declined`, or `deferred` as ledger
states. `applied`, `answered`, `declined`, and `deferred` are terminal only when
their proof, rationale, or handoff is recorded. Never use a blank state and
never drop a concern because it causes no manuscript change.

## 🔀 Route work; do not absorb it

Keep authority with the artifact being changed:

| Concern | Owning destination |
|---|---|
| evidence the paper does not yet hold (new analysis class, ablation, downstream outcome) | the Seed's Establishment Board — a new or reopened E-row |
| contribution, claim role, or paper order | current Narrative Page and row |
| section argument, wording, placement, or limitation | owning Section Page |
| missing analysis or factual support | consuming Page's `probe/` and proof |
| citation request | consuming Page's `bibex/` |
| number correction | consuming Page's probe-card `## Values` binding |
| table or figure change | owning Page's `display/<unit>/` |
| response wording and coverage | this Round Page |

**Where a routed concern LANDS on its owner** (260831): the owning page's
`outline/<stem>-feedback.md` (a section per Round), a register the page projects from this ledger
during its own OUTLINE pass (`haipipe-page-outline` ⓪ COLLECT). This page never
writes into another page's folder, and it never dispatches an agent at its
targets: it DECLARES reopenings. `cli/feedback.py collect --all <board>` lands
every register in one process with no agent at all, and `cli/feedback.py reopen
<board>` lists which pages hold an open row, in the order this ledger's own
gates impose (a Section whose concern also routes to a Narrative waits on that
Narrative; two Sections sharing one §2B block are one reopening). The fold on
each reopened page is the existing per-page RUN, `haipipe-page-workflow` at
OUTLINE, one page at a time or under a signed charter, each ending at a
person's `approved:`. A blind N-way fan-out buys N unapproved plans and N
ticks; the order above is what makes the ticks worth buying. `applied` here needs that register's
`landed:` version first, and G7 runs `feedback-coverage` board-wide before
this page may close.

The Round records routes and checked returns. It does not become a second home
for revised section prose, research values, citations, or paper displays. A
ledger item may say `applied` only after the owning Page names a checked version;
“edited” or “agent finished” is not proof.

## 🃏 Round-local plugins

Use Page-local plugins only for material the Round itself consumes:

```text
pagex/    bounded links to the Venue, Narrative, affected Pages, and checked versions
probe/    unresolved interpretation or response questions owned by this Round
bibex/    citations used in the response letter itself
display/  coverage maps, before/after comparisons, or response-only exhibits
latex/    generated response letter or Round PDF
word/     generated response DOCX when requested
```

New substantive paper evidence belongs on the Narrative or Section Page whose
prose will use it. Values remain storage-less inside probe cards and are cited
as `PP<NN>.v<n>`; never create a Round `value/` folder.

## ✍️ Response contract

For an external Round, make every response item traceable:

```text
review item id → disposition → checked change/evidence → response paragraph
```

Distinguish completed changes from commitments. Do not claim a revision is
complete until its owning Page has passed CHECK and the revised build contains
that version. For an internal Round, record `no external response required`
instead of inventing a response artifact.

## ✋ Human authority

Reserve these acts for a person:

- approve consequential accept, narrow, decline, or defer decisions;
- approve the final response package;
- approve Round closure.

A machine may propose dispositions, route accepted work, and close an already
answered Decision Now row with the human's words. It may not manufacture the
decision or mark the Round closed from ledger counts alone.

Gate G7 (the per-round gate) leaves its receipt Log row on this page,
stating the gate, the assertion results, and who approved the response
receipt.

## ✅ Closing checks

Close only through CHECK when:

- the Round identity names one feedback batch and one base build;
- every received concern appears exactly once in the ledger;
- every item has a terminal disposition with inspectable support;
- every applied change names the owning Page and its checked after-version;
- every external response paragraph maps back to ledger items;
- the revised paper build and response artifact are regenerated and recorded;
- every deferred item names a reason, owner, and next-Round handoff;
- a person approves the response and close receipt.

After closure, treat the Round as a historical record. Later feedback opens a
new Round Page; it does not rewrite the closed one.

This variant owns no scripts.
