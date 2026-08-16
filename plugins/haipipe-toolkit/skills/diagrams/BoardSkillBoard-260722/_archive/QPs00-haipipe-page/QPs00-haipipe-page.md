# QPs00 · The Page (Skill haipipe-page v0.26.0)
state: 🟡 in flux · door test passed 260802, scope bound unmeasured
owner: JL
page-type: design
method: unit snapshot in skill/ via skillpage.py plug; every section authored by hand (converted from the mirror kind 260815)

## Opening
What is the unit one Board Page is measured against, and is it healthy?

`haipipe-page` is that unit: the spec a page must satisfy and the door for CREATE, WORK ON, and RUN.
CREATE scaffolds one persistent Page.
WORK ON performs a known repair.
RUN follows bounded DRAFT, PROBE, REVISE, and CHECK routes until CLOSE or HOLD.
Load it when the unit is one Page; load `haipipe-board` when the Board itself is the subject.
This skill owns the Page contract and lifecycle receipt, while the Board skill owns rendering, checking, Workflow execution, and audit code.

**Where the line with `haipipe-board` runs**: both are doors, and the unit of work is what separates them.
Ask for a board and `haipipe-board` renders it, serves it and checks it.
Ask for a page and this skill decides what that page must contain, then calls those same scripts.
So the renderer, the write-back server, `check.py` and `ref/page-template.md` all live over there, and this skill cites the template rather than forking it.

**What the 260802 measurement showed**: the test removed every hint, giving three fresh agents one sentence each with no path, no skill name and no example page.
All three opened this skill unaided, at tool calls #5, #6 and #5, including the one phrased "can you clean up QF5-sentence-run for me", whose words match no trigger in the description.
They drove three pages from 15, 13 and 10 findings to zero.
The same run exposed what nobody had questioned: from that one instruction they wrote to 15 files, 1 file and 2 files, so the verb said where to start and never where to stop.
`0.10.0` wrote that bound in as steps 7 and 8, and no second run has measured it.

**What RUN adds**: an automatic run begins with an explicit raw-material packet and records one receipt per attempted Phase.
The producer writes, a mechanical worker rebuilds and identifies the exact source and render version, and a fresh reviewer performs CHECK.
The durable `_runs/page/` bundle and `pageflow.py` make illegal routes, self-approval, changed-after-check, missing human evidence, and exhausted limits visible.

**Covered elsewhere**: `haipipe-sentence` owns everything below a section, such as a comment lane attached to one sentence.
`haipipe-board-routing` is a consumer rather than a neighbour: it loads this contract to decide which page and which section an input belongs in.
The mirror kind this page was born under retired on 260815; this page is now written to `haipipe-page-for-design`, with its unit's bytes in the `skill/` plugin.

## Diagram
**What sits in this page's `skill/` plugin**: the unit snapshot, written by `skillpage.py plug` and renamed so neither the installer glob nor page discovery can mistake it for the live unit.

```
skill/haipipe-page/
  ref/page-run-contract.md    the Page RUN contract
  CHANGELOG.md                the unit's own history
  SKILL.snapshot.md           SKILL.md, renamed at plug time
```

**How the Page contract is reached**: two direct verbs, one bounded lifecycle verb, and a pure spec load share the same door.

```text
WORKFLOW  three verbs and one spec load, from the same door

  ── loaded as a SPEC ──────────────────────────────────────────
  an agent with NO board open needs to know what a page is:
  routing picking a section · a variant author in another family
  (haipipe-paper-stage was the first; retired 260805, the stage
  variant now lives at page-types/for-stage) · the chat drawer, one day
        │  it READS the contract and writes nothing
        ▼
  the sections, in their fixed on-stage order, and what each one owes
  🧭 Opening  🖼 Diagram  📚 Content  🎯 Aims  📍 States  📎 Files  🗃 folds

  ── invoked as a VERB ─────────────────────────────────────────
  CREATE                 WORK ON                 RUN
  scaffold Page          perform known repair   route unknown next work
       │                       │                       │
       └──────────┬────────────┘                       ▼
                  ▼                         producer · builder · reviewer
        haipipe-board engine                     ↺ until CLOSE | HOLD
        build.py · check.py                 receipt → pageflow.py audit

  ── the bound, added at 0.10.0 because it was measured missing ──
  steps 7 and 8: ONE page is the deliverable. A write outside it is
  allowed only when the page cannot be made correct without it, and
  it must be named in the report. A sibling's CONTENT is never
  rewritten. Three fresh agents given the same instruction wrote to
  15 files, 1 file and 2 files: the verb said where to start and
  never where to stop.
```

## Content
### 1 · What this unit is, in one screen
**Live and snapshot**: the unit ships from its own folder, and this page judges a plugged copy.
```text
  ⚙️ board/haipipe-page/            📋 this page's skill/ plugin
     the LIVE unit, ships    ──▶       the SNAPSHOT, judged
     SKILL.md · ref/ · log     plug    SKILL.snapshot.md · ref/ · log
```
`haipipe-page` is the loadable SPEC for one Board page and the door for CREATE, WORK ON, and RUN.
The live unit ships from `board/haipipe-page/` and keeps shipping from there.
The full contract text this page's judgments were about sits in `skill/haipipe-page/SKILL.snapshot.md`, in this page's own folder.

### 2 · Selection record · how this page got its shape
**The two candidates**: what each shape put in the .md, and what closed it.
```text
  🅰 MIRROR (lost)                  🅱 DESIGN + skill/ (won)
  ~640 derived lines in the .md    argument authored in the .md
  decides nothing                  settles on a SELECTION record
  Opening from a template          unit bytes live in the plugin
```
This page is the first specimen of the 260815 ruling that retired the mirror kind, so its own conversion is the selection it records.

- 🅰 the MIRROR kind, which lost.
  Three managed spans spliced about 640 derived lines into this file, and the page decided nothing.
  The measured failure was already on record: five skill and agent pages had Openings out of one template, because a page that decides nothing has no question to ask.
- 🅱 the DESIGN page with a `skill/` plugin, which won.
  The argument stays authored in the .md, the unit's bytes live in `skill/`, and the page settles on this selection record like any Q page.
  The unit's ongoing health stays on the `state:` line, and a new round reopens the page.

Disposition of 🅰: the span machinery in `skillpage.py` keeps serving the nine unconverted pages and retires with the last of them.
A losing candidate is recorded and never silently deleted, which is `for-design`'s own rule.

### 3 · Earlier selections this unit already carries
**One base, many doors**: every variant loads this spec and restates nothing.
```text
  📘 this base ◀── for-stage · for-design · … one door each, no forks
       └─ a variant ships with the family that OWNS it (JL 260809)
```
A type loads this base and never restates it (`QB6` §4), which is why variants are doors over this spec instead of forks.
`haipipe-paper-stage` proved the variant model from outside the family and retired into `page-types/haipipe-page-for-stage` on 260805.
A variant ships under the `page-types/` folder of the skill set that owns it (JL 260809).

## Aims
- [x] 🧪 The door test passes on evidence rather than on argument
      Three fresh agents were given one sentence each, with no path, no skill name and no example page, and all three opened this door unaided at tool calls #5, #6 and #5.
      One of them was phrased "can you clean up QF5-sentence-run for me", whose words match no trigger in the skill's description, and it opened the door anyway.
      The same run drove three pages from 15, 13 and 10 findings to zero and took the board from 210 findings to 171.
- [ ] 🛑 The scope bound holds on a second measured run
      The same three agents wrote to 15 files, 1 file and 2 files from the same instruction, so what failed was never discovery, it was where to stop.
      0.10.0 added that bound as steps 7 and 8, and nobody has re-run the measurement since, so the fix is reasoning until a second run produces a tighter spread.
- [ ] 🧹 `live/chat.py` loads this spec instead of restating it
      Four rule strings there teach an agent the page and board contracts in Python prose, and `QB8d` already caught one describing a page shape that no longer existed.
      This is `A6.1` on `QC1b`, and it is the family's one real defect: the fix costs one function and adds no version surface.
- [ ] 🧩 A page can name the unit that supports it
      `QB8a · Evidence Card` should be able to say `supported by haipipe-sentence · Evidence Card` without duplicating the board-level roster.
      The syntax is unruled and no page carries one, which is `A7.1` on `QC1b`.

- [ ] 🧩 The other nine QCskill pages convert to design pages
      This page is the specimen; the nine follow only after JL rules its shape, one plug and one authored rewrite each.

## States
This is the most proven unit in the family and also the one changing fastest: 24 releases to 0.21.0, and the only one whose door test was measured rather than assumed.
Its health is `🟡 in flux` because 0.10.0 shipped a bound that has not been re-measured, not because anything about it is unsettled.
It is also the base that variant doors extend, so the ten `page-types/` variants, the stage and display types among them, depend on this contract staying one file.

- 260802 CC · 🧪 The measurement, and the thing it accidentally proved instead
  The 260731 fan-out could not test the door: its brief pasted the path to `SKILL.md` and named `QB4` as the worked example, so all five agents read the contract as a plain file and not one of them invoked it.
  The real test removed every hint, and what it proved was the trigger surface; what it disproved was the scope, which had never been questioned.
  A test that only confirms what you expected has told you less than one that fails somewhere you were not looking.
- 260802 CC · 📄 The base and variant split makes this spec's second consumer real
  `haipipe-paper-stage` ships the S page kind under the paper family, which JL's base and variant model reads as the first variant door working as intended rather than as a leak.
  So this unit is not written only for routing: variant authors in other families resolve the same base contract, which is why a rule may never be forked into a variant.

## Log
- 260815 · [JL via CC] renamed Design-3 → QPs00: the unit page fronts its group the way QA00 fronts the board. The folder, deck, and scene stems renamed with the page; the old ids Design-3 and Skill-3 stay resolvable through board.md's alias map, and every live citer was swept to the new id. Same pass: the Opening gained its lead question, clearing the checker's opening-lead-not-a-question warning.
- 260815 1130 · [REVISE-CC] converted to a for-design page (JL 260815): the three managed spans left the file, `skillpage.py plug` wrote the unit snapshot to `skill/haipipe-page/`, and Content §2 records the selection that retired the mirror kind.
- 260806 2114 · [REVISE-CC] swept to the 260806 architecture; States release count corrected to 24 releases to 0.21.0, and the Diagram's retired "seven sections" count reworded to the on-stage-order phrasing 0.12.0 ruled.
- 260806 0140 · [REVISE-CC] card synced to disk truth after 260805 (ten types · thin-paper phase 2 · first live RUN); haipipe-paper-stage no longer cited as live, the stage variant is page-types/for-stage and the release count reads 23 to 0.20.1.
260804 · Updated the authored mirror for the third Page verb: CREATE, WORK ON, and bounded RUN now appear together, including the producer, builder, reviewer, version receipt, and audit boundary.
260802 1720 · Authored half written: the `WORKFLOW` fence replaced the template placeholder with the spec load, the two verbs and the 0.10.0 scope bound, four real Aims replaced the single health placeholder, and `state:` moved from 🔴 to 🟡 in flux. The measured door test recorded as met, and its scope failure recorded as the one Aim it left open
260731 1115 · page generated from `board/haipipe-page/` by `skillpage.py new`

