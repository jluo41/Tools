<!-- TEMPLATE · ONE SUBMISSION TARGET = ONE QBv PAGE.
     Copy this file to `<board>/QBv-venue-packs/QBv<n>-<slug>.md`, fill it, and DELETE each
     RULE comment as you satisfy it. A RULE comment never ships in a filled page.

     WHAT THIS FILE IS. The shape of a venue page, in the order its sections must run, with
     one RULE comment per rule. It states no rule that is not already in
     `haipipe-board-page-for-venue/SKILL.md` (this Page Type) or in `haipipe-board-page`
     (the base frame). Load both before filling this in; everything the base already owns is
     pointed at here, never restated. `QBv1-misq.md` on the paper board is the worked example
     the SKILL's create verb sends you to, and it is worth reading beside this file.

     WHAT A VENUE PAGE IS. One page per submission TARGET: a journal, a funder, a patent
     office, and nothing above it. It SETTLES NOTHING. Its subject is a desk outside this
     repo that publishes its own rules, changes them without telling anyone, and rejects
     papers that ignore them. The page makes that desk legible before a paper is written for
     it, and does not have an opinion about it.

     WHAT IT DOES NOT OWN. Which venue this paper picks. That decision lives in the paper
     board's Opening concern, `QB1`. This group is the catalog that decision reads. There is
     no pack-head page above the outlets: four outlets in one pack get four pages, and what
     they share is stated on each page that needs it.

     THE MECHANICAL GATE, run before calling the page finished:
       grep -c '<!-- RULE' QBv<n>-<slug>.md          must print 0
       grep -nE '<[A-Za-z?][^>]*>' QBv<n>-<slug>.md  must return only the four generated-span
                                                     markers in `## Files`
       python3 <toolkit>/skills/board/haipipe-board/cli/build.py <board-folder>
       python3 <toolkit>/skills/board/haipipe-board/cli/check.py <board-folder> | grep '^QBv'
       python3 <board-folder>/_tools/sync-exemplars.py --check
     Then READ THE RENDER, not the markdown. -->

# <Outlet>: <the desk stated in one phrase, what it buys and what it refuses>

state: 🔴 OPEN · <n> exemplars · <k> sections · <what is on the page> · <what nothing reads yet>
owner: <JL | CC>
method: <state this desk's own signals and mechanics, and record what arriving here costs a paper>
session: <written by the server when a page chat opens; delete the line until then>

<!-- RULE: THE FILENAME IS THE TYPE KEY. `QBv<n>-<slug>.md`, taking the next free `QBv<n>`,
     and the page is registered in `board.md`'s `## Pages` under `QBv`. The base resolves the
     Page Type from that filename prefix at step ①, so this page carries NO `page-type:` key;
     adding one gives the page two keys and the base calls a page with two keys defective. -->

<!-- RULE: the title says what this page is FOR, in sentence case, the base's title rule.
     For this type that means naming the DESK and what it buys or refuses, not the outlet
     alone: `MISQ: the desk that takes any method and refuses any paper whose contribution
     is one`, never `MISQ venue pack`. -->

<!-- RULE: `state:` keeps the base's four values, 🔴 OPEN · 🟡 PARTIAL · ✅ SETTLED · ⏸️ ON HOLD.
     The readable note answers ONE question: how much of this desk is actually recorded, and
     how much is still prose nobody reads. Counts, never a mood.
       ✅  🟡 PARTIAL · 15 exemplars · 7 sections · taste ✓ · the one-sentence test is unread
       🚫  🟡 PARTIAL · pack looks good
     A page whose facts are complete and whose Aims are all `⬜` is honest and common: the
     pack is a library until a lifecycle stage reads it. -->

## Opening

<One paragraph, and it is the only prose a reader sees without clicking. Say what this desk
takes, what it refuses, and end on the question this page answers about it. The base owns the
size and the split: everything before the FIRST BLANK LINE is on stage, target ~450 characters
and 520 at the ceiling.>

<!-- RULE: the drawer below the blank line is a list of labelled parts, which is the base's
     shape, not this type's. TWO of the parts are this type's own and a venue page is not
     finished without them:
       **How to read this page** the REFERENCE versus BINDING split, stated before anything
                                 else, because a page full of measured numbers reads as a
                                 specification if nobody says otherwise
       **Covered elsewhere**     the base puts an exclusion in the drawer under this label, and
                                 this type's standing exclusion is which venue the paper picks,
                                 which is `QB1` on the paper board and never this page
     The three below are what the reference implementation carries and are the parts a reader
     of a venue page looks for; keep the labels identical across outlet pages so a reader who
     has read one can scan the next:
       **Where this page sits**  one venue target in `QBv`, one page per desk, no pack layer
                                 above it, and which pack folder this page owns
       **Why this outlet matters to this repo**  which paper targets it, or that none does yet
       **What is unread**        what the page records that no skill or stage actually reads -->

**How to read this page**: everything here is a REFERENCE, not a rulebook.
<The arcs, budgets, moves and refusals below describe what the pack measured or prescribed, and
a paper that departs from them is off-pattern rather than wrong.>
One figure is different: `Submission-Rules` carries the desk's own published rules, and a
manuscript that breaks one of those is <returned unreviewed>.
Every length on this page says which of the two it is.

**Where this page sits**: <one venue target in `QBv`, one page per desk, no pack layer above it.
This page owns only what is true of `<pack path>`.>

**Why this outlet matters to this repo**: <which paper targets it, and what that costs, or that
nothing targets it yet and this page is catalog.>

**What is unread**: <the facts on this page that no lifecycle stage or skill reads today.>

**Covered elsewhere**: <which venue this paper picks is the paper board's `QB1`. The venue rules
themselves live in `haipipe-board-page-for-venue`, which this page instantiates.>

## Writing Style

How this page must be written. Read it before editing, and edit to it.

<!-- RULE: the base and `QB4-overall.md` own the page grammar, the section order and the
     sentence rules. Do not restate them here. Write only the rules this TYPE adds, and the
     three below are required because every one of them is a way this page goes wrong. -->

**Inherited from the base**: the page grammar, the section order and the sentence rules come
from `haipipe-board-page` and `QB4-overall.md`, and are not restated here.

**A number may be stated, but never claimed**: in a section division a word budget, a paragraph
count or a citation density may appear only with its source named inline, a `style.md` line
number, an exemplar name, or the desk's own page. Never as this page's own claim.

**Say what the desk REFUSES, not what it prefers**: a preference does not decide a submission.

✅ `<a better classifier is not a MISQ paper>`  ❌ `<MISQ values theory highly>`

**Write the pack's refusals as the pack's**: `the pack refuses more than ~<n> words`, never
`do not exceed ~<n> words`, so the page never sounds like it is the one doing the refusing.

## Diagram

<!-- RULE: THREE FIGURES, IN THIS ORDER, and a page missing one is incomplete rather than
     short. The base's caption rule applies to each: one `**Name**: what it shows.` line
     directly above the fence.
       ① desk taste        would this desk even look at my paper?
       ② Venue-Structure   what am I actually writing?
       ③ Submission-Rules  what does the portal demand on the day I upload, and what am I
                           signing up for by choosing this desk? -->

**<Desk taste>**: what counts as the contribution at this desk, what is rejected before review,
and the test it is screened on.

```text
  ✅ WHAT COUNTS AS THE CONTRIBUTION
     <the shapes this desk buys, one per line>   [<pack file> lines <a-b>]

  🧰 METHOD   <what is permitted, and whether the method may ever be the claim>

  ❌ DESK-REJECT
     <what is refused before review, one named refusal per line>   [<pack file> lines <a-b>]

  🎯 THE TEST, in the desk's own words
     "<the desk's own one-sentence screen, quoted>"   [<source>]

  📊 <n> exemplars · <k> sections   [<pack file> lines <a-b>]
```

**<Venue-Structure>**: the sections a <outlet> paper is written in, in the desk's reading order,
and what each one costs.

<!-- RULE: THIS FIGURE IS THE READING INDEX, and it is how a reader finds their way into
     Content. Three hops, and the figure has to make all three visible:
       ① the index column here names every section kind the desk publishes
       ② each `Sec-<i>-<Kind>` reappears as the heading of the Content division that owns it
       ③ the same name reappears behind an emoji as that division's Aims and States group
     A reader asking "what does this desk want in Methods" reads the row, jumps to the
     division, and reads its Aims group. Nothing else on the page joins those three. -->

<!-- RULE: `Sec-<n>` COUNTS FROM ZERO and carries the `Sec-` prefix, so the index IS the number
     of the `S-Main` page a paper writes: `Sec-3-Methods` becomes `S-Main-3`, and nobody
     converts anything. Only the appendix takes a letter, `Sec-A`, because a desk that letters
     its own appendix sections gives a lettered index two meanings at once. A bare `0-Abstract`
     reads as a typo, which is what the prefix is for. -->

<!-- RULE: `Sec-<i>` = `S-Main-<i>` is a PROPERTY, not a law, so CHECK it rather than assume it.
     It holds only where the desk's reading order matches the order `section-kinds.yml`
     resolves. When the two disagree, `Sec-<n>` follows the RESOLVER, because the index exists
     to JOIN the S-Main page a paper actually writes, and an index that tracks the desk stops
     being a join key the moment the two differ. The desk's printed order gets its own column
     in this figure, which is where describing the desk belongs. -->

<!-- RULE: THE DESK'S LIST CAN BE LONGER THAN THE RESOLVER'S, AND THAT GAP IS A FINDING. A kind
     the desk requires and the resolver does not declare means a draft built from the resolver
     alone reaches the portal with a required field empty. A kind the resolver declares and the
     desk does not publish means a block the desk will not take. Print each gap in this figure
     and open an Aim on it. -->

<!-- RULE: THREE NUMBERS PER SECTION, AND ONLY ONE PAIR AGREES. The venue index counts from 0
     and `S-Main-<n>` counts from 0, so those two LINE UP; the Content division number is the
     one that differs, because it counts the judgment divisions ahead of it. State that in the
     figure; do not make a reader work it out. -->

<!-- RULE: WHEN THE DESK PUBLISHES A TOTAL, ADD THE PACK'S PARTS UP AND PRINT THE SUM AGAINST
     IT. This is a required row, not a nicety: it went 3 for 3 the first time anyone checked,
     because a pack measures PUBLISHED papers section by section and a published page is not a
     submission budget. Neither source is wrong and the page resolves nothing: print both, name
     the cap as the binding one, and open an Aim on how the body gets allocated. -->

<!-- RULE: EVERY LENGTH SAYS WHOSE IT IS. A DESK RULE is published by the venue and binds. A
     PACK OBSERVATION is a measurement of papers the pack read, and breaking it is off-pattern.
     A number printed with neither label reads as a rule.
       ✅  120-160w observed, no desk cap · ~250w ruled acceptable JL 260803
       ✅  55 pp Research Article · the DESK's cap, counting everything
       🚫  120-160 words, do NOT exceed ~185
     WHEN THE PACK MEASURED NOTHING, do not borrow the stronger word. The contract rules this
     for a pack holding zero published works: use the weaker label and say on the page why the
     measured tier is missing, the way `QBv15-grant` does with AGENCY RULE against PACK RECORD.
     A journal pack with an empty `examples/` is in the same position. -->

```text
  🏗 VENUE-STRUCTURE ── <every budget below is stated with its source inline in the division
     that owns it>

  index                  §     S-Main page    desk reads   <budget>          what the section owes
  ─────────────────────  ────  ─────────────  ───────────  ────────────────  ──────────────────────
  <emoji> Sec-0-<Kind>   §<d>  S-Main-0       <1st>        <band + label>    <what it owes>
  <emoji> Sec-1-<Kind>   §<d>  S-Main-1       <2nd>        <band + label>    <what it owes>
  <emoji> Sec-A-Appendix §<d>  S-Appendix-A   <last>       <band + label>    <what it owes>

  🔢 THREE NUMBERS, ONE PAIR AGREES   <Sec-<n> and S-Main-<n> both count from 0 and line up ·
     § is this page's own division number and counts the judgment divisions ahead of them>

  🔑 Sec-<n> FOLLOWS THE RESOLVER   <state whether the desk's reading order and
     section-kinds.yml agree here; when they do not, this column is the desk's and the index
     is the resolver's>

  ⚠️ GAPS BETWEEN THE DESK AND THE RESOLVER
     <a kind the desk requires and the resolver does not declare, or the reverse, or "none">

  ➕ THE PARTS AGAINST THE WHOLE   ⚖️ the required row
     desk total          <the published total>              DESK RULE
     pack floors sum     <sum>                              PACK OBSERVATION
     pack ceilings sum   <sum>                              PACK OBSERVATION
     <what that arithmetic means for a drafter writing to the middle of every band>

  ⚖️ RULE vs OBSERVATION   <which single number the desk publishes, and that every other
     length in the column is the pack's measurement · over a budget is off-pattern, over the
     cap is unreviewed>
```

**<Submission-Rules>**: the desk's own mechanics, which the pack does not record and no section
division owns.

<!-- RULE: THIS IS THE ONE BINDING FIGURE ON THE PAGE. Everything else is a reference; these
     rows are enforced by the desk itself. It opens with the PROVENANCE STAMP, and how the fact
     was read is part of it, because a direct fetch and a search summary are not equally strong:
       ✅  fetched and verified 260802
       ✅  re-checked 260803 through search summaries only, the site answers a direct fetch
           with HTTP 403 · re-read before submitting
       🚫  "MISQ requires APA 7th" -->

<!-- RULE: A BINDING ROW CARRIES THE MOMENT IT BITES, because it is not always submission:
       ⚖️ AT SUBMISSION   the desk checks it before an editor reads
       ⏳ AT REVISION     free at first submission, enforced later
       🎯 AT ACCEPTANCE   priced or demanded once accepted, including a waiver that must be
                          REQUESTED at submission anyway
     A page that files a revision-time cap beside a submission-time one sends a drafter to
     spend weeks on a gate that is not there yet. -->

<!-- RULE: THE ODDS, THE CLOCK AND THE MONEY BELONG ON THE PAGE. Acceptance rate, review rounds,
     cycle length, submission fee, open-access charge. None of them is in any pack, and they
     decide whether a desk is worth a year. They are the desk's reported statistics rather than
     promises, and the row says so. -->

<!-- RULE: A SLOT THE SOURCES CANNOT FILL IS PRINTED, never deleted. This figure carries an open
     `❓ NOT ON RECORD YET` row, and a deleted row is a silent gap. -->

```text
  🧾 SUBMISSION-RULES ── ⚖️ THE ONE BINDING FIGURE ON THIS PAGE
     <every row below is the DESK's own published rule, from <host>, and none of it is in the
      pack's section folders>
     ⚠️ <provenance: fetched and verified <date>, or re-checked <date> through <method>>

  📁 CATEGORY & CAP    <⚖️ AT SUBMISSION> · <the categories, and the cap each one carries> ·
                       <what the cap counts> · <what happens over it>
  📄 MANUSCRIPT        <⚖️ AT SUBMISSION> · <font, spacing, margins, page size, templates>
  📚 REFERENCES        <when it bites> · <the style, and how in-text citations open>
  🖥 SYSTEM            <the portal, and what goes into it>
  🕶 ANONYMITY         <single or double anonymous, and what has to be stripped out>
  🤖 DISCLOSURE        <what the desk requires an author to declare>
  🎲 ODDS & CLOCK      <acceptance rate · review rounds · cycle length · time to first
                       decision> · <these are the editor's reported statistics, not a promise>
  💵 MONEY             <submission fee · open-access charge and licence>
  ❓ NOT ON RECORD YET  <what the desk does not publish, and what it costs this page not to
                       know it>
  🔗 THE DESK ITSELF    <bare host paths, one per line, plain text on purpose>
```

<!-- RULE: EMBED THE DESK'S LINKS TWICE, ON PURPOSE. A row inside a fence is plain text: the
     renderer runs `esc()` and the figure linker over a fence and never the inline markdown
     pass, so a URL in a figure will not be clickable. Bare hosts go in the figure so it stays
     readable when copied; the same links are repeated as real markdown links directly under
     it. NEVER put a bare URL alone on its own line inside `## Diagram`: that is the Excalidraw
     canvas slot. -->

**Open the desk**: [<page>](<url>) · [<page>](<url>) · [<the portal>](<url>).
A row inside a fenced figure is plain text by design, so the same links are repeated here as
real ones.

## Content

<!-- RULE: CONTENT IS CUT BY THE VENUE'S OWN READING INDEX, and it runs in three bands:
       ① the JUDGMENT divisions, `§1` upward, one per thing the desk decides about a paper
          before its sections matter. Not fixed in number; `QBv1` runs three: what the desk
          buys and refuses, what arriving here costs, and which sibling outlet a paper leans
          to with the tie-break that pins it here.
       ② ONE SECTION DIVISION PER SECTION KIND THE DESK PUBLISHES, in the desk's reading
          order, each named with its `Sec-<i>` index.
       ③ the UPLOAD GATE, last, turning the binding figure into a runnable list.
     Every division follows the base's Content rules: `### <n> · <name>`, a caption line, the
     face figure, then the one-line establish sentence. -->

### 1 · <What the desk buys, and what it will not>

**<caption>**: <the one thing that is true of this desk and not of its siblings.>

```text
  <the face figure for this division, drawn with /diagram-ascii, emoji on every row,
   under ~80 columns>
```

<emoji> Establishes <what this division settles, one line>.

#### 1.1 · <heading>
(<the one-line job of this paragraph>)
<Prose, one sentence per line, every desk or pack fact carrying its source inline.>

### 2 · <What arriving here costs>

**<caption>**: <what a paper gains, changes and pays by retargeting here.>

```text
  🧩 GAINS    <what this desk asks for that no sibling does>
  🔄 CHANGES  <what a paper arriving from another desk has to re-argue>
  📦 COSTS    <what the desk demands that is a decision rather than a formatting step>
```

<emoji> Establishes <the arrival cost, so a retarget is decided early>.

### 3 · <Which sibling outlet a paper leans to, and what pins it here>

**<caption>**: <the family delta is the tie-break; the outlet is chosen on the row where the
siblings differ.>

```text
  🧭 THE FAMILY   <pack family> ── <k> outlets, one pack
  ✅ SIGNALS THAT LEAN <OUTLET>   <one per line>
  ➡️ SIGNALS THAT LEAN AWAY       <signal ── the sibling it leans to, one per line>
  ⚖️ TIE-BREAK ORDER              <the ordered test that decides>
  📌 ONCE CHOSEN                  <what the pin re-runs downstream>
```

<emoji> Establishes <this outlet's position among its siblings>.

<!-- RULE: FROM HERE, ONE DIVISION PER SECTION KIND, and each repeats the SAME FIVE PARTS,
     which is what makes sections comparable across venues:
       heading    `### <n> · Sec-<i>-<Kind>: <what this section is, in the desk's terms>`
       caption    the one thing that is true of it here and not elsewhere
       fence      📐 ARC · 📏 BUDGET · 🧱 SHAPE · 🔀 VARIANT or 🖼 DISPLAYS OWED
       establish  `<emoji> Establishes ...`, one line, and the emoji lives HERE
       <n>.1      The moves, as slots        fill the shape; never lift the sentence
       <n>.2      What the pack refuses      each a named anti-pattern, not a preference
       <n>.3      Format values              words · citation density · value density · displays
       <n>.4      The language, in the papers' own words   5-6 attributed sentences, one move each -->

<!-- RULE: NO EMOJI ON A SECTION DIVISION HEADING, however tempting the symmetry. It lives on
     the Aims and States group and on the division's closing establish line. `check.py` strips
     an emoji from a group name and not from a division, so ten divisions produce twenty
     group-name-drift warnings at once. Written, built, reverted, 260803. -->

<!-- RULE: A BLUEPRINT-ONLY PACK HAS NO EXEMPLAR LANGUAGE. The five-part shape presumes measured
     work. When the pack holds zero published papers, drop `<n>.4` entirely and say on the page
     why it is missing; never print four subsubsections with empty rows to satisfy the shape.
     The same holds inside `<n>.3`: `🔢 VALUE DENSITY  not recorded by the pack` is a finding,
     and deleting the row is a silent gap. -->

### <n> · Sec-<i>-<Kind>: <what this section is, in the desk's terms>

**<caption>**: <the one thing that is true of this section here and not elsewhere.>

```text
  📐 ARC      <the section's order of moves>   [<style.md> lines <a-b>]
  📏 BUDGET   <band> · <DESK RULE | PACK OBSERVATION>   [<style.md> line <n>]
     measured <exemplar> ~<n>w · <exemplar> ~<n>w   [<style.md> lines <a-b>]
  🧱 SHAPE    <paragraph count, sentences per paragraph, words per sentence>   [lines <a-b>]
  🔀 VARIANT  <what changes between paper types>   [<template.md> lines <a-b>]
  🖼 DISPLAYS OWED   <the displays this section must carry, or none>   [<template.md> line <n>]
```

<emoji> Establishes <what this division settles about this section, one line>.

#### <n>.1 · The moves, as slots
(fill the shape; never lift the exemplar's sentence)
<Move: `<the slot pattern with its variables in brackets>` [move <k>, <exemplar>].>

#### <n>.2 · What the pack refuses
(each is a named anti-pattern, not a preference)
<The pack refuses <the anti-pattern> [<style.md> line <n>].>

#### <n>.3 · Format values
(every number here is the pack's own, carried with the line that records it)

```text
  📏 WORDS            <band · paragraphs · sentences per paragraph>   [<style.md> lines <a-b>]
  📚 CITATION DENSITY <per sentence, per exemplar>   [<style.md> line <n>]
  🔢 VALUE DENSITY    <the figure, or `not recorded by the pack`>
  📊 DISPLAYS         <what this section carries>   [<template.md> line <n>]
```

#### <n>.4 · The language, in the papers' own words
(the sentences behind the <n>.1 slots, one move each)
"<the exemplar's own sentence>" [<exemplar>]
<What move it is, and why it reads that way [<style.md> line <n>].>

<!-- RULE: THE PAGE ENDS WITH THE GATE AS A RUNNABLE LIST. The last Content division turns the
     binding figure into an ordered checklist run ONCE on the final file, because a rule
     remembered while drafting is a rule half-applied. It also names the ONE step a finished
     paper cannot fix in an afternoon, which at every desk with a hard cap is the page count. -->

### <last> · Before you upload: the binding rules as a list you can run

**<caption>**: everything here is enforced by the desk, not by us.

```text
  ✅ BEFORE YOU UPLOAD ── run top to bottom, on the FINAL file

  ① <the step, and the trap in it>
  ② <the step>
  ③ <the step>
  ④ <the step>
  ⑤ <the step>
  ⑥ <the step>
  ⑦ UPLOAD   <the portal, and what goes with the file>
```

✅ Establishes the desk's own gate as a <k>-step list, so the binding rules are executed once at
the end rather than remembered while drafting.

#### <last>.1 · <the step that actually fails>
(it is the only rule here that a finished paper cannot fix in an afternoon)
<Why the other steps are minutes of work on a file that already exists, and why this one is a
content decision made months earlier.>

<!-- RULE: WHEN THE TARGET IS NOT A JOURNAL, four of the rules above bend, and each bend is a
     real adaptation rather than permission to skip the section:
       1 NO RESOLVER        `section-kinds.yml` declares zero kinds for a grant or a patent, so
                            no S-Main page exists and the index cannot be "the S-Main number".
                            `QBv15` used `Row-<i>-<AGENCY>`, the pack's own unit; `QBv16` read
                            its index off 37 CFR 1.77(b), with HOLES, so the index is not
                            contiguous.
       2 ONE TARGET, MANY DESKS   `Venue-Structure` becomes a MATRIX, one lane per agency or
                            office; or PIN one, say so in three places, and keep the others'
                            deltas as their own divisions.
       3 "PACK OBSERVATION" IS EMPTY   the label means measured from published work, and these
                            packs hold zero funded proposals and zero filings. Use AGENCY RULE
                            versus PACK RECORD, and say on the page why the measured tier is
                            missing.
       4 A RULE NEEDS ITS CYCLE   a funder's guidelines expire every round and an office's fees
                            are dated, so a non-journal row also says which CYCLE it binds.
     The unfixable step also moves: at a funder it is CHOOSING THE AGENCY, and at a patent
     office it is what the specification failed to disclose. Verify that at source. -->

## Aims

<!-- RULE: this variant does NOT override the base's Aim form. Ids, `Done when`, and one State
     row per Aim id all apply. The group is `### A<n> · <emoji> <index>-<Kind>: <name>`,
     mirroring its Content division exactly, and `### P` holds a target belonging to no single
     section, such as the submission mechanics or propagating a change to sibling pages. -->

<!-- RULE: an Aim on a venue page is almost always the same shape: SOMETHING THE PACK RECORDS
     AND NOTHING READS. `Done when` names the RUN that would prove it, not the reading.
       ✅  Done when: an abstract draft records its variant and its measured word count
                      against the 120-160 budget.
       🚫  A4.1 · Understand the abstract norms. -->

### A1 · <emoji> <name of Content division 1, verbatim>
- A1.1 · <the target, as a state that becomes true>
  **Done when:** <the run that would prove it>

### A<n> · <emoji> Sec-<i>-<Kind>: <the division name, verbatim>
- A<n>.1 · <the target>
  **Done when:** <the run that would prove it>

### P · <emoji> Targets that belong to no single section
- P1 · <the desk's own submission mechanics are checked before a manuscript is uploaded>
  **Done when:** <the run that walks the gate list and records the result of each step>

## States

<!-- RULE: States mirrors every Aim id exactly once, in the same groups and the same order, and
     keeps the base's vocabulary: ⬜ not started · 🔨 being worked on · 🧠 waiting on a person or
     something outside this page · ✅ met with the evidence named · ❄️ on ice.
     KEEP STATES HONEST AGAINST THE FOLDS: a Log line saying a question was settled beside a
     State row still reading `⬜ Not started` is the drift this board exists to catch, and it
     happened on `QBv1` between 260802 and 260803. -->

<!-- RULE: `### Decision Now` is optional and goes FIRST when present, holding the choices only
     a person can make. Its row shape is the base's, one option per line, each saying what
     choosing it commits you to. Delete the heading when there is nothing to decide. -->

### A1 · <emoji> <name of Content division 1, verbatim>
- ⬜ A1.1 · <what is true now, and what the evidence for it is>

### A<n> · <emoji> Sec-<i>-<Kind>: <the division name, verbatim>
- ⬜ A<n>.1 · <what is true now>

### P · <emoji> Targets that belong to no single section
- ⬜ P1 · <what is true now>

## Files

<!-- RULE: FIVE GROUPS, IN THIS ORDER. `Authority` and `Generated` are this type's own
     additions; the other three are the base menu's names, and both additions state an ACTION,
     which is the base's test for a group name.
       ⚙️ Engines       what REGENERATES this page
       📋 Contracts     THIS contract, and the base it extends
       📥 Input files   the pack files this page READS
       🔗 Authority     what the DESK itself PUBLISHES
       📤 Generated     what a tool WRITES into this page, between markers -->

### ⚙️ Engines · what REGENERATES this page

- `<_tools/sync-exemplars.py>`
  <What it rewrites, and from what.> ⚠️ Never hand-edit between the markers: the next run
  overwrites it.

### 📋 Contracts · what CARRIES a rule to other pages

<!-- RULE: THIS CONTRACT GOES IN `Contracts`, NEVER IN `Engines` (JL 260803 asked which). An
     Engine is something you RUN and open to change behavior; a Contract CARRIES a rule to
     other pages, and a loadable spec that never executes is named there. The row also has to
     say the link runs BOTH ways: a rule changed on the page is changed in the contract in the
     same pass, and a sibling outlet page reads the contract rather than reading this page. -->

- `<path>/board/page-types/haipipe-board-page-for-venue/SKILL.md`
  The venue-page contract: the three figures in fixed order, the `Sec-<n>` index rule, the
  desk-outranks-pack rule, these five Files groups, and the rule that an unfillable slot is
  printed rather than dropped. <Say which direction this page sits in: the reference
  implementation changes the contract in the same pass, and every other outlet page reads the
  contract rather than this page.>
- `<path>/board/haipipe-board-page/SKILL.md`
  The base frame that contract extends. Load it first; it owns the sections and their order.

### 📥 Input files · what this page READS

<!-- RULE: THE PACK IS READ AND NEVER WRITTEN BY THIS PLUGIN. The packs are their own
     repository, `jluo41/Venue-Paper`, pinned as a submodule, so a correction found here lands
     on this page and never in `paper/venue/`. -->

- `<paper/venue/playbook-<family>/<OUTLET>/taste.md>`
  <The desk signals and the one-sentence test. Start here when what this desk buys is the
  question.>
- `<paper/venue/playbook-<family>/<OUTLET>/<OUTLET>-<section>/style.md>`
  <What the section divisions are built from.>
- `<paper/venue/playbook-<family>/README.md>`
  <The family delta and the lean-signal matrix that the tie-break division folds in.>
- `<stages/section-kinds.yml>`
  The reader-side resolver: outlet to section kinds. It is what the generated kinds block below
  is built from, and what `Sec-<n>` follows when it and the desk disagree.

### 🔗 Authority · what the DESK itself PUBLISHES, read directly and never through the pack

<!-- RULE: THIS GROUP OPENS WITH THE PROVENANCE STAMP, the same date-and-method stamp the
     `Submission-Rules` figure carries, and then holds the desk's own links.
     IT ALSO CARRIES EVERY PLACE THE DESK CONTRADICTS THE PACK, naming both readings. The desk
     wins, and the disagreement is the most valuable thing on the page, so it is never quietly
     resolved. `QBv1` records three: an observed page range against a published submission
     ceiling, no reference style recorded where the desk requires one, and none of the
     submission mechanics recorded at all. A desk can also contradict ITSELF, and the page
     prints both readings when it does. -->

⚠️ Provenance: <what was fetched and verified on what date, what was re-checked by what weaker
method and why, and that the desk is re-read before a real submission>.

- [<page name>](<url>) · <what this page of the desk governs>
- [<page name>](<url>) · <what this page of the desk governs>
- CONTRADICTS the pack on <topic>: <what the pack records, from which file>, against <what the
  desk publishes>. <Which one binds.>
- <What the pack does not record at all, and what the desk requires instead.>

### 📤 Generated · what `<sync-exemplars.py>` WRITES into this page

<!-- RULE: NEVER HAND-EDIT BETWEEN THESE MARKERS: the next run overwrites it. The blocks are
     replaced by a marker regex so they may sit under any heading, but keep the kinds block
     AFTER the exemplars block, and run `sync-exemplars.py --check` before calling the page
     finished. A stale block is a count that disagrees with the folder. If the board has no
     generator, say so in the span and open an Aim on it rather than deleting the span, because
     a deleted span hides the missing engine. -->

<!-- exemplars:begin -->
<!-- exemplars:end -->

<!-- kinds:begin -->
<!-- kinds:end -->

## Law

<!-- RULE: optional and folded, the base's own section. A venue page uses it for a ruling about
     THIS desk that binds from now on, dated and attributed. Delete the heading if unused. -->

- <YYMMDD> <who> · <emoji> <the rule, stated first>
      <One sentence naming what now binds, then why it changed.>

## Glossary

<!-- RULE: optional and folded. One row per word on this page an outsider would stumble on, the
     term bold, the definition after a colon. Delete the heading if unused. -->

- **<term>**: <definition>

## Log

<!-- RULE: newest first, one dated line per change. A Log line records what was true when it was
     written, so an older line is never rewritten to match a newer ruling; the correction is a
     new line. Times come from the clock, never invented. -->

<YYMMDD> · <what changed, and why>
