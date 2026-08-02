# haipipe-board-page-for-skill · v0.1.0
state: 🟡 in flux · hours old, applied once, never reviewed
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
`haipipe-board-page-for-skill` says how to write a page that MIRRORS something: a `Skill-<n>` page standing in for a skill folder, or an `Agent-<n>` page standing in for one agent file.
Load it on top of `haipipe-board-page`, which covers every page kind; reach past it to this one whenever the page you are writing is about a unit that ships somewhere else.
The reason it is separate is that a mirror page decides nothing, and the base contract asks an author what their page decides.
It is hours old, its rules have been applied to seven pages once, and no independent reviewer has judged the result.

**What a mirror page is**: a page whose subject exists on disk before the board mentions it, ships to other people, and carries its own version and its own changelog.
`Skill-0-haipipe-board.md` on this board is one: it stands in for the folder `skills/board/haipipe-board/`, which would still be there if this board were deleted.
A decision page is the opposite, because the question it asks exists nowhere but on the page.

**Why the base alone was not enough**: `haipipe-board-page` already forbids interchangeable prose, in the noun-substitution test, and five roster pages were written from one template anyway.
The cause sits above that test rather than in it.
The base tells an author to open with a question and to end that paragraph on what the page decides, and a mirror page decides nothing, so the only question available is a rhetorical one about the unit itself.
On 260802 five pages opened with `Does <name> <verb> one <noun>?` followed by the same four sentences, and JL saw it by eye before any checker did.

**What it replaces the question with**: three ordered slots, written plainly for a reader who has never heard of the unit.
What is it and what is it for; when you reach for it rather than the one sibling you would otherwise pick, named; and where it stands, meaning the one thing to know before trusting it.
It also carries the rules a mirror page needs and a decision page does not: which three spans a generator owns, that `state:` is a health judgment while the version rides the title, that a page's Aims are the UNIT's open work, and how a page retires when its unit does.

**Covered elsewhere**: `haipipe-board-page` owns the frame this extends, the seven sections and their order, and this file never repeats a rule from it.
`haipipe-board/cli/skillpage.py` is the generator that writes the three managed spans; `QC3a` on this board argues its design and `QC1b` argues which units exist at all.
`haipipe-paper-stage` is the other variant in the toolkit, and the contrast is the point: that one ships under the paper family because paper is its consumer, while this one ships beside the base because for these two kinds the consumer IS the board family.

**Where it stands**: seven roster pages were rewritten to it on the day it shipped, six of them by fresh agents that loaded it with no other briefing, which is the closest thing to a test it has had.
Three of those agents died on a session limit after writing, so the batch completed but not cleanly.
No `haipipe-board-reviewer-agent` has read the seven Openings consecutively, which is the one check this contract says it cannot pass on its own.

## Writing Style
English only. One sentence per source line. Describe the shipped unit factually and keep generated inventory separate from human health judgment.

## Diagram
<!-- haipipe:skill:tree:start 6d4adef91655cf4f board/haipipe-board-page-for-skill -->

**What `haipipe-board-page-for-skill` ships**: every file in the folder, with the one-line purpose each one states for itself.

```
haipipe-board-page-for-skill/
  CHANGELOG.md          49 ln  haipipe-board-page-for-skill · Changelog
  SKILL.md             170 ln  /haipipe-board-page-for-skill · a roster page is not a decision page
```

<!-- haipipe:skill:tree:end -->

**Where this contract sits, and what it adds**: the base covers every page kind, and this one covers only the two that mirror something.

```text
WORKFLOW  load the base, then add what a mirror page needs

   📄 haipipe-board-page          the BASE · every page kind
      seven sections, fixed order · the title rule · numbering
      the evaluation contract · the noun-substitution test
        │
        │  loaded FIRST, and never repeated below
        ▼
   🪞 haipipe-board-page-for-skill        ONLY the delta
      ┌────────────────────────────────────────────────────┐
      │ 🧭 Opening   ❶ what is it, what for                │
      │              ❷ when, versus ONE named sibling      │
      │              ❸ where it stands, with evidence      │
      │              🚫 never a question: it decides nothing│
      │ ✍️ spans     which 3 a generator owns, which        │
      │              sections are a person's               │
      │ 🩺 state:    HEALTH, not version · version rides    │
      │              the title · the note carries evidence │
      │ 🎯 Aims      the UNIT's open work, including a      │
      │              defect another page ROUTED here       │
      │ 🗄 retire    archive · deregister · alias BOTH ids  │
      └────────────────────────────────────────────────────┘
        │
        ▼
   the two kinds it governs
   Skill-<n>-<slug>   mirrors a skill FOLDER   tree span is drawn
   Agent-<n>-<slug>   mirrors ONE agent FILE   tree span is EMPTY,
                                               emitted, never omitted

   ⚠️ the test is NOT the author's to pass: the Openings are read
      CONSECUTIVELY in board order by a fresh reviewer, because a
      writer knows which unit they meant and cannot see the swap
```

## Content
<!-- haipipe:skill:body:start 6d4adef91655cf4f board/haipipe-board-page-for-skill -->

**haipipe-board-page-for-skill** · `0.1.0` · last shipped 2026-08-02

- folder   `board/haipipe-board-page-for-skill/`
- tools    not declared
- summary  First cut: the roster-page variant, opened because five Skill Openings came out of one template and the base could not have prevented it.

### SKILL.md




**LOAD `haipipe-board-page` FIRST.** It owns the base: the seven sections, their fixed order, the five rows that define each one, the title rule, the numbering, and the evaluation contract.
This file adds only what a roster page needs and a decision page does not.
It never repeats a base rule, because a copied rule is the thing that goes a night out of date while the contract moves.

**The two kinds this variant covers**: both mirror something that ships elsewhere.

```
kind    filename              mirrors                        closes when
──────────────────────────────────────────────────────────────────────────
Skill   Skill-<n>-<slug>.md   one skill FOLDER · SKILL.md    the unit ships
Agent   Agent-<n>-<slug>.md   one agent FILE   · <name>.md   the unit ships
                              NEITHER is ever counted in the board's settled total
```

`<n>` orders the roster and never carries the version, because a filename that changed every release would break every link to the page.
A skill is LOADED into a context and an agent is DISPATCHED into a fresh one (JL 260731), which is why they are two kinds and not one.


- 1 · 🪞 What makes a roster page different
      A Q page asks a question and closes when its Aims are met. An S page closes when its human gate passes.
      A roster page **decides nothing**. Its subject exists on disk before the board mentions it, ships to other people, carries its own version and its own changelog, and closes only when the unit ships.
      Three consequences, and every rule below comes from one of them:
      ```
      1  it has no question       →  its Opening INTRODUCES; it does not ask
      2  its Content is not ours  →  the unit's own bytes, in a managed span
      3  it has a HEALTH          →  state: is a judgment about the unit, not a version
      ```

- 2 · 🧭 The Opening a roster page owes (the rule this skill was opened for)
      **The failure, measured 260802.** Five roster pages on `01-boardform-260722` had Openings in one shape:
      ```
      line 1   Does `<name>` <verb> one <noun> for <consumers>?
      line 2   <what it owns>
      line 3   The hard part is <X> without <Y>.
      line 4   <consumers> depend on <Z>.
      line 5   It is healthy when <W>.
      ```
      Read alone each is clear. Read consecutively they are one letter with the nouns swapped, which is the failure `haipipe-board-reviewer-agent` 0.4.0 exists to catch and which JL caught first by eye.
      **The base could not have prevented it, and that is why this file exists.**
      The base already carries the noun-substitution test, so the rule was on the books and five writers broke it anyway.
      The cause is upstream of the test: the base's Opening shape is `the question, what its words mean, why that is hard, what this page decides`, and a roster page **decides nothing**.
      A writer obliged to produce a question about a unit that decides nothing can only manufacture a rhetorical one, and "Does X do X well?" has exactly one answer, "that is what it is for", which carries no information.
      Give five writers the same impossible slot and they will fill it the same way. The slot was the defect, not the writers.
      **What replaces it.** The visible paragraph answers three questions, in this order, in plain words for a reader who has never heard of the unit:
      ```
      ❶ WHAT IS IT, and what is it FOR
           one line. A reader who stops here should be able to say what it does.
      ❷ WHEN DO I REACH FOR IT, rather than its sibling
           name the sibling you would otherwise pick, and the line between them.
           A boundary stated against a real neighbour is checkable; "it owns X" is not.
      ❸ WHERE DOES IT STAND
           the one thing to know before trusting it: what is unproven, unbuilt,
           unruled, or moving fast. Never "it is healthy when ...", which describes
           a hypothetical unit rather than this one.
      ```
      Keep the base's physical shape unchanged: one visible paragraph, the FIRST BLANK LINE is the split, `More details` below it as labelled parts.
      **Four things a roster Opening may never do:**
      ```
      🚫 open with a rhetorical question          it decides nothing, so it asks nothing
      🚫 paraphrase the unit's own description:   Content already carries those bytes;
                                                  a paraphrase is a lossy second copy
      🚫 use the own · hard-part · depend ·       four slots produce four filler
         healthy scaffold                         sentences and one form letter
      🚫 claim health the page cannot show        ❸ names evidence or says it is missing
      ```
      **The test, and it is not the author's to pass.** Read the changed Openings CONSECUTIVELY in board order, not one at a time. A page that is clear alone still fails if its Opening would introduce its sibling after a noun swap. Dispatch `haipipe-board-reviewer-agent`; the writer's own read cannot see this, because the writer knows which unit they meant.

- 3 · ✍️ Derived and authored: the split a machine enforces
      `haipipe-board/cli/skillpage.py` owns three spans and nothing else. Everything outside them is a person's.
      ```
      DERIVED · skillpage.py sync rewrites, hash-checked
        ## Diagram  <!-- haipipe:skill:tree:… -->   the folder tree, one purpose line per file
        ## Content  <!-- haipipe:skill:body:… -->   the unit's SKILL.md, its own bytes
        ## Log      <!-- haipipe:skill:log:… -->    its CHANGELOG, converted to Log lines
        the title's `· v<version>`                  so the index row shows it unmaintained

      AUTHORED · a script that rewrites one of these is a defect
        ## Opening · the WORKFLOW fence in Diagram · ## Aims · ## States
        · the page's own hand-written ## Log lines · state: · owner: · method:
      ```
      `sync` replaces only the marked spans; `check` REPORTS a stale hash instead of rewriting, so drift is visible rather than possible.
      **A green `check` means less than it looks.** `digest()` hashes the frontmatter's derived facts only, by its own docstring, "so prose edits never look like drift". ✅ means the metadata is current, NOT that the page's copy of the `SKILL.md` still matches it. Byte equality needs a regenerate-and-diff by hand.
      ```bash
      python3 <board-skill>/cli/skillpage.py new   <board> <unit> --group "<GROUP>" --stamp "YYMMDD HHMM"
      python3 <board-skill>/cli/skillpage.py sync  <board> [<page>|--all]
      python3 <board-skill>/cli/skillpage.py check <board>
      ```
      An AGENT is one file, so its tree span renders EMPTY rather than being omitted: `sync` replaces spans it can find, and a missing one reports forever as an older page needing repair.
      The WORKFLOW fence carries the whole picture on an agent page, because there is no tree to carry it.

- 4 · 🩺 `state:` is health, and only a person writes it
      The page `state:` line keeps the base's four values, and on a roster page it answers one question: **is this unit stable, in flux, in question, or parked?**
      A version cannot answer it: a unit at `0.1.0` may be finished and one at `0.9.4` mid-rewrite. So `new` seeds `🔴 OPEN` and a person changes it. The version rides the TITLE, never `state:` and never the filename, so a machine number and a human judgment never compete for one line.
      **The readable note after the emoji must carry the evidence**, not a mood:
      ```
      ✅  🟡 in flux · ~60 releases in 11 days, 3 open defects
      ✅  🟡 in question · existence unruled since 260729
      ✅  🟡 in flux · consumers declared, none measured
      🚫  🟡 in flux                    ← says nothing a reader can check
      🚫  🟡 in flux · v0.9.0           ← that is the title's job
      ```
      `🔴 OPEN` on a unit that ships is almost always a page nobody finished, not a real judgment.

- 5 · 🎯 Aims and States on a roster page
      A roster page's Aims are **the unit's own open work**, not the page's. The page is finished the moment it describes the unit truthfully; the unit is not.
      Three sources fill them, and the third is the one people miss:
      ```
      ① what the unit itself still owes      unbuilt verbs, unwritten contracts
      ② what is unproven about it            shipped but never run, never measured
      ③ a defect another page ROUTED here    because this unit ships the file
      ```
      ③ is correct routing, not passing the buck: the page that finds a defect is rarely the page that ships the file, and a finding parked on the finder's page is a finding nobody owns. Name the page it came from.
      States carries one dated record per real event, in the base's `- YYMMDD WHO · <emoji> <title>` form with indented body lines. **Never leave `Page generated <date>. Nothing ruled yet.`** on a page whose unit ships: that is the generator's stub, and it is a claim that nobody has looked, which stops being true the moment somebody has.

- 6 · 🗄 When a unit retires
      `git mv` the page into `_archive/`, remove its line from `board.md` `## Pages`, and add BOTH its id and its old `Q-Skill-<name>` alias to `## Links` pointing at the archived path, so every existing citation still resolves. Then grep the board for prose that still names the unit as live: a Log line recording what was true when written STAYS, and a sentence in live prose claiming it still ships is now false.
      Proven on `haipipe-board-index`, retired 260802: the page went to `_archive/`, its id still resolved, and the sweep found eight live-prose sentences on four other pages plus one dead citation on a sibling board.

- 7 · 📂 Files
      ```
      haipipe-board-page-for-skill/
      ├── SKILL.md            this variant contract
      └── CHANGELOG.md        version history
      ```
      Owns no scripts. The generator is `haipipe-board/cli/skillpage.py`; the base frame is `haipipe-board-page`; the writing standard is `haipipe-board/ref/writing-rules.md`; the roster's design record is the board's `QC3a` (how a folder becomes a page) and `QC1b` (which units exist at all).
<!-- haipipe:skill:body:end -->

## Aims
- [ ] 🧑‍⚖️ The seven Openings are read consecutively by a fresh reviewer
      This contract states that the consecutive read is the test and that the author cannot run it, so until `haipipe-board-reviewer-agent` has read the batch in board order, the rewrite is unjudged.
      Three of the six writers died on a session limit after writing, so the batch also needs confirming as complete rather than assumed.
- [ ] 🧪 The three slots are tried by someone who did not design them
      Six fresh agents applied them on the day the contract shipped, and every one of them was briefed by the same session that wrote the contract.
      A slot that only its author can fill is the failure this whole page exists to describe, one level up.
- [ ] 🛠 `skillpage.py new --group` stops describing the wrong thing
      It takes the group KEY, `QC`, but given the full heading `QC · Engine` it fails with "no group ... (heading must be `### Q<key> · title`)", which describes the HEADING format and so implies the argument should be the full heading.
      Found while generating this very page. `skillpage.py` ships in `haipipe-board`, so the fix belongs to `Skill-0` and this row is routing it there.
- [x] 🖼 The generated Diagram carries a caption, per `QB4` §2
      JL read `Skill-0` on 260802 and found the figure had none.
      Fixed in the GENERATOR rather than on the pages, because a caption written inside a managed span is erased by the next `sync`; `tree_block()` now emits it and one `sync --all` captioned every existing page.

## States
The contract shipped and was immediately used on seven pages, which is more evidence than most first cuts get and still not a test.
Its health is `🟡 in flux` for a plain reason: everything in it is one day old, and the one check it names as decisive has not been run.

- 260802 JL · 🪞 Opened on a question, not a defect report
  JL asked "this is skill page, and it is kind of special, how do we deal with it? Like should we have haipipe-board-page-for-skill?" after reading five roster Openings that were visibly one letter.
  The instinct was right for a reason worth recording: the base already carried the rule those pages broke, so tightening the rule would have changed nothing.
- 260802 CC · 🔎 The rhetorical question turned out to be GENERATED, not invented
  `skillpage.py`'s page stub seeded the Opening with `{name} is a shipped unit: what does it still owe, and is it healthy?`, and every page generated from it inherited that shape.
  Five writers were blamed for a sentence the tool wrote first, which is why the fix landed in the stub as well as in this contract.
- 260802 CC · 🖼 The Diagram caption was fixed in the generator, and that is the general rule
  A derived figure owes a derived caption: a caption a person writes inside a managed span is erased by the next `sync`, and one written just outside it survives while nothing generates it, so every new page would start non-compliant.
  The authored `WORKFLOW` fences still take a hand-written caption, and the stub now ships a placeholder one so a new page starts with the line present.

## Log
260802 1930 · Authored half written by the main session after its dispatched writer died on a session limit: the Opening replaced the generated rhetorical stub, the `WORKFLOW` fence and its `QB4` caption were drawn, four Aims opened including one defect routed to `Skill-0`, and `state:` moved from 🔴 to 🟡 in flux
260802 1900 · page generated from `board/haipipe-board-page-for-skill/` by `skillpage.py new`

<!-- haipipe:skill:log:start 6d4adef91655cf4f board/haipipe-board-page-for-skill -->

Converted from the skill's own `CHANGELOG.md`: 1 releases.

260802 · `0.1.0`
      - **First cut**, opened on JL's ask: "this is skill page, and it is kind of special,
        how do we deal with it? Like should we have haipipe-board-page-for-skill?"
      - **The measurement that opened it.** Five roster pages on `01-boardform-260722` had
        Openings in one shape: `Does <name> <verb> one <noun>?` then own, hard-part,
        depend, healthy. Read alone each was clear; read consecutively they were one letter
        with the nouns swapped. JL caught it by eye before any reviewer ran.
      - **Why the base could not have prevented it, which is the reason to ship a variant
        rather than tighten a rule.** `haipipe-board-page` already carries the
        noun-substitution test, so the rule was on the books and five writers broke it
        anyway. The cause is upstream: the base's Opening shape is `the question, what its
        words mean, why that is hard, what this page decides`, and a roster page decides
        nothing. A writer obliged to ask a question about a unit that decides nothing can
        only manufacture a rhetorical one, and "Does X do X well?" has one answer that
        carries no information. The slot was the defect, not the writers.
      - Replaces that slot with three ordered questions the visible paragraph answers:
        what the unit is and is for; when you reach for it rather than its named sibling;
        and where it stands, meaning the one thing to know before trusting it. The base's
        physical shape is unchanged: one visible paragraph, first blank line is the split.
      - Names four things a roster Opening may never do, each traced to the measurement:
        a rhetorical question, a paraphrase of the unit's own `description:` (Content
        already carries those bytes), the four-slot scaffold, and a health claim the page
        cannot show.
      - States that the consecutive read is the test and that it is NOT the author's to
        pass, because the writer knows which unit they meant and therefore cannot see the
        substitution failure.
      - Carries the roster-page rules that were previously only on the design board's
        `QC3a`: the derived-versus-authored split across the three managed spans, that a
        green `check` covers frontmatter only and not prose, that `state:` is a health
        judgment a person writes while the version rides the title, and that an agent's
        empty tree span is emitted rather than omitted.
      - Adds two rules the board learned by doing and had written nowhere: a roster page's
        Aims may be a defect another page ROUTED here because this unit ships the file, and
        the generator's `Page generated <date>. Nothing ruled yet.` stub is a claim that
        nobody has looked, so it may not survive on a page whose unit ships.
      - Adds the retirement procedure, proven on `haipipe-board-index` the same day:
        archive the page, deregister it, alias BOTH ids to the archived path, then sweep
        live prose, since a Log line recording what was true stays and a live sentence
        claiming the unit still ships is now false.

<!-- haipipe:skill:log:end -->
