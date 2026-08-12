<!-- TEMPLATE · ONE DISPLAY UNIT = ONE BOARD PAGE.
     Copy this file to `<board>/<group>/<page-id>-<slug>.md`, fill it, and DELETE every RULE
     comment as you satisfy it. A RULE comment never ships in a filled page.

     LOAD BEFORE WRITING, in this order:
       1. `haipipe-page/SKILL.md`                     the base frame every page keeps
       2. `haipipe-board/ref/page-template.md`              the authoritative base template
       3. `page-types/haipipe-page-for-display/SKILL.md`   this type's contract
     This file adds NO rule to those three. Where a section below says "base rules apply", go
     read the base; a summary copied into a template is a second authority and it drifts.

     WHAT THIS TEMPLATE SPELLS OUT is only what a DISPLAY page adds, and each addition is one
     sentence of the type contract:
       · Content MIRRORS the unit's folder; it does not argue a question
       · the acceptance ladder, ① REQUESTED ② SOURCED ③ RENDERED ④ ACCEPTED ⑤ PLACED
       · every number the unit shows carries provenance, from a Value binding or a named run
       · one placement record per consumer, binding the unit to the sentence that cites it

     WHAT THIS PAGE IS NOT. It holds nothing true of more than one unit:
       which units the work ships       -> the owning stage or control page
       float numbering across units     -> the paper family's submission stage
       the venue's display limits       -> the venue page
       the `displays/<unit>/` anatomy   -> the paper and display families
     A display page is mirror-shaped like a Skill page and differs in one fact that decides
     everything: a Skill page's unit is maintained elsewhere and closes when it SHIPS, while this
     unit is produced by this project and closes only when a person ACCEPTS a specific render.

     WORKED EXAMPLE: `QBt3-for-display.md` on the boardform board is a filled page of this type.
     Read it beside this file. Where the two disagree, the contract wins and that page is the
     defect.

     MECHANICAL GATE, run before anyone is asked to look at the page:
       grep -c 'RULE:' <page>.md            must print 0
       grep -nE '<[^>]{1,60}>' <page>.md    must print nothing outside a fenced figure
     A finished page has zero <angle-bracket> slots and zero RULE comments. Then build, run
     `cli/check.py <board> | grep '^<PAGE>'`, and read the RENDER, not the markdown.

     English only. No em-dashes. One sentence per source line. -->

# <page id> · <what this page is FOR, in sentence case>

<!-- RULE: the base rule stands unchanged: the title says what the PAGE is for, in sentence case,
     capitalizing the first word and proper nouns and nothing else. On a display page that is
     almost always the unit's own subject, so write `Figure 3 · Drift falls as a type key ages`
     rather than `Figure 3` or `The drift display page`. A reader on the Index gets this line and
     nothing else before choosing, and "a display page" tells them nothing. A page whose purpose
     genuinely is not the unit's subject, such as a worked example of this Page Type, titles that
     purpose instead. -->

state: <🔴 OPEN | 🟡 PARTIAL | ✅ SETTLED | ⏸️ ON HOLD> · rung <①..⑤> <REQUESTED | SOURCED | RENDERED | ACCEPTED | PLACED> · <one clause: what this rung is waiting on>
page-type: display
owner: <the person whose yes IS the acceptance>
method: <one line: how this unit gets built, accepted, and placed>
provides: <path to the render this page ships, or delete this line>

<!-- RULE: THE STATE LINE CARRIES TWO THINGS, health first and rung second, and the order is
     forced. The type contract says a display page's state answers "how far up the ladder is
     this unit?". `cli/check.py` raises `bad-state` on any state line whose FIRST token is not
     one of the four health emoji. A bare rung is therefore an ERROR on every board today.
     Write the health word first and the rung as the next token: it passes the checker and loses
     nothing. This conflict is real and UNRULED; `QBt3-for-display` carries it as an open
     Decision Now row. Do not resolve it on your own page. -->

<!-- RULE: `page-type: display` is REQUIRED and it is the only key that makes this page a display
     page. A display unit usually wears a stage-shaped filename such as `S-Display-4c-drift`, and
     without this key the base resolver reaches step ④ and reads the page as a plain stage page.
     The key BEATS the filename (base, type resolution step ③). Write it even though it is
     decorative today: `src/parse.py` and `cli/check.py` do not read it yet, so nothing reports a
     page that omits it, which is exactly why the writer has to. -->

<!-- RULE: DO NOT INVENT HEAD KEYS. `src/parse.py` recognizes only `state`, `owner`, `method`,
     `route`, `session`, `requires`, `style-from`, `provides`, and `contract-source-hash`; any
     other key is dropped without a word. So anything load-bearing must ALSO appear in the page
     body, where a reader can see it. `requires:` / `style-from:` are the stage page's keys and a
     display page does not take them.
     `provides:` is worth one caution. `ref/board-form.md` §4 calls it a short prose delivery note
     and marks it S only, while a resolver such as the boardform group's `unit.py` reads any
     `provides:` as ONE PATH and fails the page when no file sits there. A display page has a real
     artifact, so write the PATH or write nothing; the collision itself is an open Decision Now row
     on `QBt1-for-stage` and is not yours to settle. -->

<!-- RULE: THERE IS NO `## Stage Contract` ON THIS PAGE. This type declares none, so the section
     would be furniture nobody maintains. Live display pages that still resolve as stage pages do
     carry one; that inconsistency is an open Decision Now row on `QBt3-for-display` and is not
     yours to settle. There is also NO `## Boundary` section on any page (JL 260731). -->

## Opening

<!-- RULE: the base owns Opening whole: the visible paragraph is everything BEFORE the first
     blank line, 4-5 sentences, target ~450 characters and a hard ceiling of 520 measured on the
     render, plain English, no growing roster, no house skeleton. Read the base for all of it.
     WHAT A DISPLAY PAGE ADDS is only the subject: the lead question asks what THIS UNIT must
     show a reader, not whether a display should exist. -->

<!-- RULE: DO NOT PUT A BLANK LINE AFTER THE QUESTION. The first blank line is the split, so a
     blank line there leaves the page showing one bare question with its whole explanation behind
     a click, and nothing reports it. Write the question and the sentences that explain it as
     consecutive lines with no blank between them; the renderer joins them into one block. -->
<the lead question: what must this unit show a reader, and for which claim?>
<what the question's own words mean here, one clause each, with a real example>
<why getting this unit right is hard>
<what this page decides about it>

<!-- RULE: everything below the blank line renders in `More details`, and it is a LIST OF
     LABELLED PARTS, never one block of prose. The three parts below are the ones a display page
     usually owes; keep the ones that carry something and delete the rest. -->
**What this unit is**: <figure, table, or diagram; one line on what a reader looks at>

**Where its files live**: <the unit folder, and the naming rule that put it there>

**Covered elsewhere**: <the page that owns display rulings across units, the page that owns float numbering, and the page that owns the folder anatomy>

## Writing Style

<!-- RULE: required on both kinds of page (`ref/board-form.md` §4). It renders as a flat row
     inside Opening's drawer. Base rules apply; write the ones the NEXT editor of this unit needs,
     as `**Item**:` paragraphs. A display page usually owes three: what the caption may and may
     not claim, the statistical verb ceiling this unit's design allows, and the rule that a number
     is never typed into the page by hand. -->
**<Item>**: <the rule, in this page's own words>

## Diagram

<!-- RULE: ON A DISPLAY PAGE, `## Diagram` IS THE RENDER. Ladder rung ③ says a person can LOOK
     at the unit; this section is where they look, so a reader can accept or refuse the unit
     without opening the unit folder. Embed the real artifact by path with
     `![](<unit-folder>/out/preview.pdf)`, which the renderer turns into a readable PDF object;
     reproduce it as ascii only when no binary render exists yet, and say so under the fence.
     The caption line above it is required exactly as on every other figure. -->

<!-- RULE: the base's "a figure row is a label and its value, never a clause" rule is SUSPENDED
     inside this one fence, and only here, because the fence holds the artifact rather than a
     diagram drawn to explain one. Every other fence on this page obeys the rule. -->

**The render**: <what a person is looking at, and what deciding on it commits them to>

<the embed, or the reproduced render>

<one line: which render this is, where it lives on disk, and why it is reproduced here if it is>

## Content

<!-- RULE: CONTENT MIRRORS THE UNIT, it does not argue a question. Each division below answers
     one question about the unit itself, and the four numbered 1 to 4 are what the type contract
     names. Base rules bind everything else: numbering all the way down, and each division opening
     with a caption line, then a fenced `/diagram-ascii` figure, then a one or two line intro that
     starts with an emoji and says what the division ESTABLISHES. `check.py` reports a division
     with no figure and a figure with no caption; nothing reports a missing intro line. -->

<!-- RULE: the DIVISION heading carries no emoji. The emoji belongs on the matching Aims and
     States group, because `check.py` strips a leading emoji from a group name and not from a
     division heading, so an emoji on the heading fires `group-name-drift`. Use the same emoji
     that opens the division's intro line, and the three sections then line up by eye. -->

### 1 · The claim job: what this unit must show, and for which claim

**<figure name>**: <what this diagram shows>

```text
  claim served   <the one claim this unit carries>
  shown by       <the series, panels, or rows the render prints>
  NOT shown      <what a reader must not read off it>
  consumers      <page · section> · <page · section>
```
🎯 <Establishes the one job this unit does, so a reviewer can tell whether the render did it.>

<!-- RULE: this division is ladder rung ①, written down. A unit with no claim job is a leftover,
     and a unit that shows more than its claim job is not generous: every extra series is one
     more thing a reader must rule out before reaching the one that matters. -->
<one or two sentences, one per line>

### 2 · Provenance: one row per number the unit shows

**<figure name>**: <what this diagram shows>

```text
  value                     source                                  kind
  ─────────────────────────────────────────────────────────────────────────
  <the numbers>             <Value binding, by path, or the run>    <binding | run | derived>
```
🔢 <Establishes that nothing on the render appeared without a source.>

<!-- RULE: THIS IS THE DIVISION THE TYPE EXISTS FOR. A figure asserts without a sentence, so it
     is where an untraceable number hides best. Every number the unit prints gets a row, and each
     row's source is either a Value binding on a Value topic page, named BY PATH, or the producing
     run named here. A rendered number nothing traces is a defect of THIS page even when the
     figure looks right. A derived number names the file and the arithmetic that made it, and its
     inputs still need their own rows. -->
<one or two sentences, one per line>

### 3 · Spec: how the unit is produced, and what label is honest

**<figure name>**: <what this diagram shows>

```text
  unit       <the unit folder>
  input      <what the build reads>
  build      <the script or recipe that writes the render>
  rebuild    <the one command that regenerates it, or why it cannot be run here>
  verify     <the command that proves every input resolves>
  ─────────────────────────────────────────────────────────────────────────
  label      "<the statistical verb this design supports>":
             ① <the design fact that caps it>
             ② <the second design fact that caps it>
```
📐 <Establishes the recipe and the honest ceiling on what the figure may claim.>

<!-- RULE: this division is ladder rung ②, and it carries the label ceiling because the caption
     is downstream of the spec. A figure claiming "reduces" over a design that supports only
     "association" is the defect this division exists to catch. A unit that cannot be rebuilt here
     still records WHY: a secure server, a dated report, PHI. "Cannot rebuild" with a reason is
     provenance; a silent gap is a hole. -->
<one or two sentences, one per line>

### 4 · Placement: which sentence uses this unit

**<figure name>**: <what this diagram shows>

```text
  consumer            sentence                                landed?
  ─────────────────────────────────────────────────────────────────────────
  <page · section>    "<the words that cite it>"              <✅ cited | ⬜ named, not cited>
```
🔗 <Establishes whether the unit reached the work, which acceptance alone does not tell you.>

<!-- RULE: ONE ROW PER CONSUMER, and the row says which section, which sentence, and whether the
     citation landed. A unit that renders well and is cited by no sentence is not finished. An
     accepted-but-unplaced unit is a VISIBLE open `⬜` row, never a silent success, and it is what
     holds the page at rung ④ instead of ⑤. -->
<one or two sentences, one per line>

### 5 · Fragility: what would send this unit back down the ladder

<!-- RULE: this division is ADVISED, not required by the contract, and it is what makes the
     contract's fallback rule usable. Acceptance is of a SPECIFIC RENDER, so a re-render after
     acceptance returns the unit to rung ③, and a changed claim job returns it to ①. Write the
     events, so a person can tell when their yes expired. Delete the whole division only if this
     unit genuinely cannot change, which is almost never. -->

**<figure name>**: <what this diagram shows>

```text
  <the event>                        ──▶ <the rung it falls back to>
```
⚠️ <Establishes what makes the state line fall, so a person knows when their yes expired.>

<one or two sentences, one per line>

## Aims

<!-- RULE: base rules apply, and the grouping is mechanical: one `### A<n> · <emoji> <name>` per
     Content division, carrying that division's NUMBER and its EXACT NAME, plus the emoji from
     the division's intro line. `check.py` reports `group-name-drift` when the names differ by a
     single word. Use `P<n>` only for a target that genuinely crosses divisions. An Aim is a
     durable target with a testable `Done when`, never a task. -->

<!-- RULE: RUNG ④ IS AN AIM AND ITS DONE-WHEN NAMES A PERSON. Acceptance is a judgment no file in
     the unit folder can hold and no machine may write. Every other rung can be verified from
     disk; this one cannot, which is the whole reason this Page Type stands alone. -->

### A1 · 🎯 <the exact name of Content division 1>
- A1.1 · <the target this division makes true>
  **Done when:** <a test a reader can run against the rendered division>

### A2 · 🔢 <the exact name of Content division 2>
- A2.1 · Every number on the render traces to a source that resolves.
  **Done when:** <each source in §2 resolves, and the rows cover every value the render prints>

### A3 · 📐 <the exact name of Content division 3>
- A3.1 · The statistical label does not outrun the design.
  **Done when:** <the label line names every design fact that caps it>

### A4 · 🔗 <the exact name of Content division 4>
- A4.1 · Every consumer either cites the unit or shows an open unplaced row.
  **Done when:** <no `⬜` row is left in §4, at which point the state line moves to rung ⑤>

### A5 · ⚠️ <the exact name of Content division 5>
- A5.1 · The events that void acceptance are written down before acceptance is asked for.
  **Done when:** <§5 lists every path that can change a printed number>

### P · Page-level
- P1 · <the person's acceptance of this render is recorded on this page>
  **Done when:** <owner> says yes to THIS render, and the Log carries the rung with its date.

## States

<!-- RULE: base rules apply. States is a SNAPSHOT OF RIGHT NOW, so the reason a state changed and
     the history of the ladder both belong in `## Log`, not here. Mirror the Aims groups and every
     Aim id EXACTLY ONCE, with `⬜` not started, `🔨` being worked on now, `🧠` waiting on a person
     or something outside this page, `✅` met with the evidence named, or `❄️` on ice. Nothing
     reports a missing mirror row: `aim_progress` reads met and total off THIS section, so a page
     with six Aims and no rows here renders a silent `0/6` and passes the checker. -->

<!-- RULE: `### Decision Now` is optional, and when present it goes FIRST, above the per-Aim
     groups. Everything else in States is a report; this is the one part that asks the reader to
     do something. Base owns the row shape. A machine never ticks a row nobody answered, and never
     flips this page's rung ④. -->

### Decision Now
- [ ] 🗣 <the ask, as one question>
      <one or two lines: what is true today, and what it costs>
      A · <the first option, and what choosing it commits you to>
      B · <the second option, and what it commits you to>
      → <who> recommends <letter>, because <the reason it beats the other>.

### A1 · 🎯 <the exact name of Content division 1>
- <⬜ | 🔨 | 🧠 | ✅ | ❄️> A1.1 · <what is true now, with the evidence named>

### A2 · 🔢 <the exact name of Content division 2>
- <status> A2.1 · <what is true now>

### A3 · 📐 <the exact name of Content division 3>
- <status> A3.1 · <what is true now>

### A4 · 🔗 <the exact name of Content division 4>
- <status> A4.1 · <what is true now>

### A5 · ⚠️ <the exact name of Content division 5>
- <status> A5.1 · <what is true now>

### P · Page-level
- <status> P1 · <whether a person has accepted this render, and which one>

## Files

<!-- RULE: base rules apply: an action map, not an inventory, with each path in backticks and one
     line saying what you open it for. A display page's rows are the unit's own artifacts, named
     one by one. "The unit folder" is not a way to reach anything. Add `### 🔗 Related Board Pages`
     only when this page needs a precise fragment of another page. -->

- `<unit-folder>/`
  <the unit this page mirrors: what is in it, and what is generated>
- `<unit-folder>/<the build script>`
  <regenerates the render from its declared input; do not hand-edit the output>
- `<unit-folder>/out/<the render>`
  <the artifact a person accepts; generated, never hand-edited>
- `<the page or file holding the source of every number>`
  <what it supplies, and which §2 rows read it>
- `<page-types/haipipe-page-for-display/SKILL.md, by its board-relative path>`
  The contract this page is an instance of. If the two disagree, the contract wins.

<!-- RULE: the other folds, `## Law`, `## Lesson`, `## Glossary`, and `## Discussion`, are each
     optional and come straight from the base, in that order, before `## Log`. Add one only when
     it holds something; delete the heading otherwise. This type adds no rule to any of them. -->

## Log

<!-- RULE: THE LADDER LIVES HERE, one dated line per rung, newest on top. The type contract says
     the page's Log carries each rung with its date, and rung ④ additionally carries WHO accepted
     and the words they used. A re-render after acceptance gets its own line saying the unit fell
     back to ③, because a fallback nobody wrote down reads as an acceptance that still stands.
     Log is also where an answered `### Decision Now` row lands, and where a resolved `> USER:`
     thread is moved verbatim; a `> USER:` line is never deleted. -->

- <YYMMDD> · rung <①..⑤> <name> · <what happened>

<!-- RULE: when this page was driven by a Page RUN, its phase receipts belong here too, written
     as `- <YYMMDD> · [<DRAFT|PROBE|REVISE|CHECK>-<actor>] <what that phase changed>`. A rung line
     and a phase line are different records and both are kept: the rung says where the unit stands,
     the phase says who moved it. -->

