---
name: haipipe-paper-round
description: >-
  Paper journey phase P4 (Round) and the Page Type contract for one bounded
  feedback-and-response cycle: an editor decision, reviewer round, or coauthor
  pass. Atomizes every concern into a coverage ledger, records dispositions,
  routes changes to the owning Pages, and closes with an approved response. Use
  when opening, triaging, answering, or closing a revision round.
metadata:
  version: "0.7.0"
  last_updated: "2026-09-08"
  group-token: "RD"
  outline:
    mode: fixed
    source: "this SKILL.md"
    surface: "Opening → Outline → Content → Aims"
    shape: "Round Identity and Intake → Feedback Coverage Ledger → Decisions and Response Strategy → Change Routing → Applied and Checked Changes → Response Package → Close Receipt and Handoff"
---

# /haipipe-paper-round · close one feedback cycle without losing an item

Load `haipipe-page`, then this Page Type, then `haipipe-page-workflow` for the
shared Page lifecycle.
Declare `page-type: round`.

## 🧭 Journey phase

This skill is journey phase P4 Round (respond) of the paper journey and owns
the `page-type: round` contract below. Opens on a feedback batch any time after
a build exists. Closes through gate G5: every concern ledgered and routed
exactly once (the Story's C5 support and C6/C7 needs for new evidence, a Story C8
Section Narrative row for retelling, a Section for rework) and a person approves
the response receipt. `haipipe-paper-workflow`
holds the full gate assertions; this block only places the phase. The page
itself always runs through `/haipipe-page` and `haipipe-page-workflow` (OUTLINE
→ … → CHECK), never a private lifecycle.
Round is a Page-level control surface, not a Run, an Evidence/Execution owner,
or a second Story.

## 🔄 Grain and boundary

Create one Round Page for one bounded batch of feedback against one named paper
build. Examples include one editor decision plus its reviews, one coauthor pass,
or one pre-submission audit whose concerns will be answered together.

```text
base paper build + received feedback
                  ↓
        one Round Page and ledger
                  ↓ routes work to
      Story C5–C8 content · Sections · their evidence/plugins
                  ↓ returns checked versions to
       response package + revised build + close receipt
```

Do not create one Round per reviewer, comment, or changed Section. Keep every
atomic concern addressable inside the same Round ledger. Open a new Round when a
new decision or feedback batch arrives after closure.

A **Paper Round** is the persistent feedback cycle defined here. A **Page
workflow round** is a reopening era inside one Page's OUTLINE-to-CHECK receipt.
Never use one term or counter as the other. A Run can support work requested by
a Round, but a Round never becomes the Run's owner or numbering authority.

## 🪪 Required identity block

Record the Round identity before triage:

```text
round-id          stable id, unique across this paper (`RD<NN>`)
page-id           full Page stem (`RD<NN>-<desk>-<event>-<YYYYMMDD>`)
round-kind        editor-review · reviewer-review · coauthor · internal ·
                  foreign-desk (a review of this work's telling at a desk
                  with no §8 Section Narrative rows on this board)
venue-page        selected Venue Page and version, or explicit none
story             governing Story page, its §8 target, and version · a
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
Paper-<Slug>/
└── B<x>-<desk>-Round/
    └── RD<NN>-<desk>-<event>-<YYYYMMDD>/
        ├── RD<NN>-<desk>-<event>-<YYYYMMDD>.md  the Round control page
        ├── sent/             immutable copy of every declared submission output,
        │                     plus build-manifest.json and display-register.md
        ├── feedback/         immutable received letters, memos, and marked-up files
        ├── released/         immutable answering build with the same manifest set
        ├── response/         external Round only: approved response letter/table
        │                     and its response manifest; omitted for internal work
        └── outline/          Page Context/Outline/Evidence/Log projections
```

`sent/` and `released/` contain the exact output set declared by the paper-root
`delivery/paper-build.toml`. If a paper declares an online supplement, its PDF
and DOCX belong in both snapshots; do not freeze only the main manuscript.
The Round page records each snapshot's relative path, manifest hash, and
creation event. A missing declared output is a failed freeze, not a silently
partial Round.

`response/` is not another manuscript source or evidence lane. It is the
immutable upload-facing response package, cut only after the response content
in Role 6 has human approval; its manifest records the response paragraphs and
the ledger item ids they answer. An internal Round omits the directory and records
`no external response required` in Roles 6 and 7.

A professor's pass, a coauthor pass, and a desk decision are all Rounds of the
same shape; the folder name says which. The next Round normally starts by
copying this Round's `released/` into its `sent/`. If an intervening rebuild
changes the manuscript, that new build is the next Round's base and its
different manifest hash is recorded explicitly; never silently reuse an older
snapshot. The last Round's `released/` is the accepted manuscript, so nothing
dangles. Root `delivery/` stays the factory; `sent/` and `released/` are copies
cut from it, never edited. Store supplied letters or memos in `feedback/` — a
received letter floating at the repo root is homeless material (JL 260823).
Preserve their wording; never rewrite received material into a cleaner second
source. (`files/` was the pre-0.5.0 name of `feedback/`.)
The runtime home is the DESK'S OWN ROUND GROUP (JL 260831, three groups per
desk): `B<x>-<desk>-Round/RD<NN>-<event>/` at the paper root, beside that desk's
-Main and -Appendix groups, so the desk's downstream story sits in three
named shelves. A foreign-desk round mints its desk's -Round group even when
that is the desk's only group. A combined `B<x>-<desk>` group or the older
lone `C1-RD-round/` group is not a current Round location.
Here `B<x>` is a placeholder for the next free lowercase B-group letter: the
first desk uses `Bc`, the next desk continues at `Bd`, and so on. It is not a
second naming scheme.

### 🪪 Round naming law

Use the same semantic naming style as the desk's Main and Appendix shelves:

```text
Ba-MISQ-Main/       S-MISQ-Main-Results/
Bb-MISQ-Appendix/   S-MISQ-Appendix-Robustness/
Bc-MISQ-Round/      RD01-MISQ-feedback-20260825/
```

- `Bc-<desk>-Round` is the desk's Round shelf; `RD<NN>` is the semantic Round
  token and is unique across the paper, even when more than one desk exists.
- The canonical new Page stem is
  `RD<NN>-<desk>-<event>-<YYYYMMDD>`; `<event>` is a short lower-kebab label.
  Use ASCII lowercase letters, digits, and single hyphens in `<event>` (for
  example `editor-decision` or `coauthor-pass`); keep it stable after intake.
  Existing stems with an uppercase desk or an older date spelling remain
  readable history and are not bulk-renamed.
- `RD` is intentionally retained for **Round**. Do not shorten it to `R`,
  which collides with Run, or `RR`, which incorrectly narrows every Round to a
  reviewer/revision event. `rNN` and any Paper-local Run grammar belong to the
  owning Run/Page contract and never replace `RD<NN>`.
- A Round may record a Run or Result relation as `round: RD<NN>`; that relation
  does not move evidence/execution into the Paper Board or mint a new Run.

The two manifest hashes must be recorded in the new Round's identity block.
The root `delivery/` remains the mutable factory, while all Round snapshots
are immutable.

## 🧭 Page surface and control loop

Round content follows the shared Page surface exactly:

```text
## Opening   identity, base build, feedback intake, and boundary
## Outline   generated plan table: item · route · owner · state · checked version
## Content   the seven roles below, in order
## Aims      human decisions, open actions, and the G5 close test
```

`## Outline` is a projection of the Round's current plan, not a second
feedback ledger. The atomic ledger remains Role 2. Do not author `## States`,
`## Files`, `## Discussion`, or `## Log` on the Page; the corresponding records
belong under `outline/` and are linked from the Page. This keeps the Round
compatible with the common Page CHECK and prevents an old Round's meeting
notes from becoming a second authority.

The shared Page phases give the Round this control loop; they do not create a
private Round lifecycle:

```text
CONTEXT  freeze identity + inventory sent/feedback
OUTLINE  atomize concerns + propose routes (no silent disposition)
EVIDENCE record only the bounded support needed to answer or verify a concern
CONTENT  record human decisions, owning-page returns, and response paragraphs
CHECK    verify coverage, hashes, response trace, deferred handoffs, approval
```

## 📐 Required Content roles

Keep all seven roles inspectable. Combine divisions only when their addresses
remain unambiguous.

```text
1  Round Identity and Intake
   identity block · what was sent (`sent/`: exact output set, path, date,
   recipient, manifest hash) · what came back (`feedback/`: source inventory
   and hashes) · scope · due date

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
   ledger totals · the released build (`released/`: exact output set, path,
   manifest hash) · response artifact or explicit internal no-response record ·
   deferred items · next Round · approved-by · approved-at · approval record
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
affected Story Section Narrative row and version
affected Section or appendix Page
required evidence/citation/value/display work
human disposition and rationale
owning Page and owner
response strategy and response paragraph id
support/result relation (`round: RD<NN>` plus the full owner-native id)
state
before version and checked after version
open blocker or explicit deferred handoff
```

Use `open`, `routed`, `applied`, `answered`, `declined`, or `deferred` as ledger
states. `open` and `routed` are non-terminal. `applied` means a changed owning
Page has passed CHECK and is waiting for the response trace; it is not terminal
for an external Round. `answered` is the terminal state for a checked change or
for a justified answer requiring no manuscript change. `declined` requires a
human rationale, and `deferred` requires a named owner, reason, and next-Round
handoff. Never use a blank state and never drop a concern because it causes no
manuscript change.

## 🔀 Route work; do not absorb it

Keep authority with the artifact being changed:

| Concern | Owning destination |
|---|---|
| evidence the paper does not yet hold (new analysis class, ablation, downstream outcome) | the Story's C5 evidence proposition plus the corresponding C6 Discovery or C7 Task need |
| contribution, claim role, or paper order | the Story's §8 Section Narrative row (and its compile-order block) |
| section argument, wording, placement, or limitation | owning Section Page |
| missing analysis or factual support | consuming Page's typed Evidence Item; a new study need also changes Story C7 |
| citation request | consuming Page's CITE Evidence Item and verified source set |
| number correction | consuming Page's VALUE Evidence Item and accepted local Result |
| table or figure change | owning Page's `display/<unit>/` |
| response wording and coverage | this Round Page |

For a `foreign-desk` Round, the received desk is named in the identity and
the route still lands first on the governing Story. A request about the
telling becomes a human-approved C8 candidate row; it does not create a
foreign Section or let the Round write a second manuscript.

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
`landed:` version first, and G5 runs `feedback-coverage` board-wide before
this page may close.

The phrase **routed exactly once** means one ledger row and one route decision,
not that a concern can name only one affected artifact. A single route may
name a primary owning Page plus a required Story C5/C6/C7 or C8 update; those
linked destinations remain one coordinated route under the same item id. Do
not clone the concern into a second ledger row or create duplicate work items.

The Round records routes and checked returns. It does not become a second home
for revised section prose, research values, citations, or paper displays. A
ledger item may say `applied` only after the owning Page names a checked version;
“edited” or “agent finished” is not proof.

## 🃏 Evidence and delivery boundary

The Round does not own an Evidence/Execution lane. Its Context and ledger may
point to an accepted Result, a source hash, or a checked Page version, but it
does not create a new Discovery block, Task block, Run, or typed evidence item.
If a concern needs substantive new evidence, route it to the Story's C5
support and C6/C7 need, then let the external Discovery/Task/Run owner return
the result. If a Section needs a local CITE/VALUE/DISPLAY item, the consuming
Section owns that item and its Page workflow. The Round records only the
relation and the returned version.

New substantive paper evidence changes C5 support and affected C6/C7 needs on
the Story; the Section whose prose uses it binds its own typed Evidence Item.
Round feedback is stored in `feedback/`, not converted into a new evidence
authority. Do not recreate retired PageX or legacy evidence, bibex, or
standalone value plugin lanes.

The Delivery plugin owns generated manuscript artifacts. On a person's send
act it freezes the current build into this Round's `sent/`; after the Round's
CHECK and human close approval it freezes the answering build into
`released/`. The Round page records the paths and hashes; it never edits the
generated `delivery/` tree.

## ✍️ Response contract

For an external Round, make every response item traceable:

```text
review item id → disposition → checked change/evidence → response paragraph
```

Distinguish completed changes from commitments. Do not claim a revision is
complete until its owning Page has passed CHECK and the revised build contains
that version. For an internal Round, record `no external response required` in
Role 6 and the close receipt instead of inventing an external letter. The
internal item-by-item decision record still remains required.

## ✋ Human authority

Reserve these acts for a person:

- approve consequential accept, narrow, decline, or defer decisions;
- approve the final response package;
- approve Round closure.

A machine may propose dispositions, route accepted work, and close an already
answered Decision Now row with the human's words. It may not manufacture the
decision or mark the Round closed from ledger counts alone.

Gate G5 (the per-round gate) leaves its receipt row under `outline/` and a
linked summary in Role 7, stating the gate, assertion results, snapshot hashes,
and who approved the response receipt.

## ✅ Closing checks

Close only through CHECK when:

- the Round identity names one feedback batch and one base build;
- every received concern appears exactly once in the ledger;
- every item has a terminal disposition with inspectable support;
- every applied change names the owning Page and its checked after-version;
- `sent/` and `released/` each contain the complete declared delivery output
  set, and both manifest hashes are recorded;
- every external response paragraph maps back to ledger items;
- the revised paper build and external response artifact, when required, are
  regenerated and recorded; an internal Round records the explicit no-response
  decision;
- every deferred item names a reason, owner, and next-Round handoff;
- a person approves the response and close receipt, with identity, timestamp,
  and approval record recorded.

After closure, treat the Round as a historical record. Later feedback opens a
new Round Page; it does not rewrite the closed one.

This variant owns no scripts.
