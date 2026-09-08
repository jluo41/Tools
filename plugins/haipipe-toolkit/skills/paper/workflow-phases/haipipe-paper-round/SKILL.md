---
name: haipipe-paper-round
description: >-
  Paper journey phase P4 (Round) and the Page Type contract for one bounded
  feedback-and-response cycle: an editor decision, reviewer round, or coauthor
  pass. Atomizes every concern into a coverage ledger, records dispositions,
  routes changes to the owning Pages, and closes with an approved response. Use
  when opening, triaging, answering, or closing a revision round.
metadata:
  version: "0.6.0"
  last_updated: "2026-09-07"
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

This skill is journey phase P4 Round (respond) of the paper journey and owns
the `page-type: round` contract below. Opens on a feedback batch any time after
a build exists. Closes through gate G5: every concern ledgered and routed
exactly once (the Story's §6 Evidence Board for new evidence, a Story §8
Section Control row for retelling, a Section for rework) and a person approves
the response receipt. `haipipe-paper-workflow`
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
      Story §6/§8 rows · Sections · their evidence/plugins
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
                  with no §8 Section Control rows on this board)
venue-page        selected Venue Page and version, or explicit none
story             governing Story page, its §8 target, and version
                  (`narrative` is the pre-260907 name of this field) · a
                  foreign-desk round names the desk in received-from and
                  still parents to the Story, because its evidence routes there
base-build        exact manuscript/PDF/version that received the feedback
received-from     editor, reviewer labels, coauthor, or internal authority
received-at       date and source location
response-due      date, explicit none, or unknown
```

A Round BEGINS with a delivery and ENDS with one (0.5.0, JL 260907): the
version you sent that drew the comments, and the version you released with
every ledgered concern answered. Both are frozen inside the Round's folder,
beside what came back:

```text
B<x>-<desk>-Round/RD<NN>-<event>-<yymmdd>/
├── RD<NN>-<event>-<yymmdd>.md   the ledger: every comment, its route, what changed
├── sent/                        what WE SENT · the PDF + DOCX + build-manifest that
│                                drew the comments · copied from delivery/ on send
├── feedback/                    what CAME BACK · letters, memos, marked-up PDFs
├── released/                    what WE RELEASED · the PDF + DOCX + manifest with
│                                every ledgered concern answered · cut on close
└── outline/ …
```

A professor's pass, a coauthor pass, and a desk decision are all Rounds of the
same shape; the folder name says which. The next Round's `sent/` repeats this
Round's `released/`: one file copied twice is cheap, and the two manifests'
hashes show whether anything slipped in between (a difference is explained on
the Log). The last Round's `released/` is the accepted manuscript, so nothing
dangles. Root `delivery/` stays the factory; `sent/` and `released/` are copies
cut from it, never edited. Store supplied letters or memos in `feedback/` — a
received letter floating at the repo root is homeless material (JL 260823).
Preserve their wording; never rewrite received material into a cleaner second
source. (`files/` was the pre-0.5.0 name of `feedback/`.)
The runtime home is the DESK'S OWN ROUND GROUP (JL 260831, three groups per
desk): `B<x>-<desk>-Round/RD<NN>-<event>/` at the paper root, beside that desk's
-Main and -Appendix groups, so the desk's downstream story sits in three
named shelves. A foreign-desk round mints its desk's -Round group even when
that is the desk's only group. Boards with a combined `B<x>-<desk>` group or
the older lone `C1-RD-round/` group are grandfathered.

## 📐 Required Content roles

Keep all seven roles inspectable. Combine divisions only when their addresses
remain unambiguous.

```text
1  Round Identity and Intake
   identity block · what was sent (`sent/`: path, date, recipient, manifest
   hash) · what came back (`feedback/`) · scope · due date

2  Feedback Coverage Ledger
   one row per atomic concern; every received point appears exactly once

3  Decisions and Response Strategy
   accept · narrow · answer · decline · defer, with human authority and reason

4  Change Routing
   affected claim · Story §8 row · Section · evidence/plugin obligation · owner

5  Applied and Checked Changes
   what changed · owning Page · before/after version · CHECK result

6  Response Package
   point-by-point reply, editor note, tracked-change/diff pointers, commitments

7  Close Receipt and Handoff
   ledger totals · the released build (`released/`: path, manifest hash) ·
   response artifact · deferred items · next Round
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
affected Story Section Control row and version
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
| evidence the paper does not yet hold (new analysis class, ablation, downstream outcome) | the Story's §6 Evidence Board — a new or reopened E-row, with a §6.4 work row |
| contribution, claim role, or paper order | the Story's §8 Section Control row (and its compile-order block) |
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
gates impose (a Section whose concern also routes to the Story waits on the
Story; two Sections sharing one §2B block are one reopening). The fold on
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
pagex/    bounded links to the Venue, Story, affected Pages, and checked versions
probe/    unresolved interpretation or response questions owned by this Round
bibex/    citations used in the response letter itself
display/  coverage maps, before/after comparisons, or response-only exhibits
latex/    generated response letter or Round PDF
word/     generated response DOCX when requested
```

New substantive paper evidence belongs on the Story (§6) or the Section Page
whose prose will use it. Values remain storage-less inside probe cards and are cited
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

Gate G5 (the per-round gate) leaves its receipt Log row on this page,
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
