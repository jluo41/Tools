# haipipe-board-page-for-skill · v0.4.2
state: 🟡 in flux · shipped 260802, applied to eight pages, one independent review 260802
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
`haipipe-board-page-for-skill` says how to write a page that MIRRORS something: a `Skill-<n>` page standing in for a skill folder, or an `Agent-<n>` page standing in for one agent file.
Load it on top of `haipipe-board-page`, which covers every page kind; reach past it to this one whenever the page you are writing is about a unit that ships somewhere else.
It shipped 260802, its rules have been applied to eight pages, and one independent review on 260802 passed the noun-swap check it was built for while failing the pages on their facts.

**Why it is separate at all**: The reason it is separate is that a mirror page decides nothing, and the base contract asks an author what their page decides.

**What a mirror page is**: a page whose subject exists on disk before the board mentions it, ships to other people, and carries its own version and its own changelog.
`Skill-0-haipipe-board.md` on this board is one: it stands in for the folder `skills/board/haipipe-board/`, which would still be there if this board were deleted.
A decision page is the opposite, because the question it asks exists nowhere but on the page.

**Why the base alone was not enough**: `haipipe-board-page` already forbids interchangeable prose, in the noun-substitution test, and five skill and agent pages were written from one template anyway.
The cause sits above that test rather than in it.
The base tells an author to open with a question and to end that paragraph on what the page decides, and a mirror page decides nothing, so the only question available is a rhetorical one about the unit itself.
On 260802 five pages opened with `Does <name> <verb> one <noun>?` followed by the same four sentences, and JL saw it by eye before any checker did.

**What it replaces the question with**: three ordered slots, written plainly for a reader who has never heard of the unit.
What is it and what is it for; when you reach for it rather than the one sibling you would otherwise pick, named; and where it stands, meaning the one thing to know before trusting it.
It also carries the rules a mirror page needs and a decision page does not: which three spans a generator owns, that `state:` is a health judgment while the version rides the title, that a page's Aims are the UNIT's open work, and how a page retires when its unit does.

**Covered elsewhere**: `haipipe-board-page` owns the frame this extends, the seven sections and their order, and this file never repeats a rule from it.
`haipipe-board/cli/skillpage.py` is the generator that writes the three managed spans; `QC3a` on this board argues its design and `QC1b` argues which units exist at all.
The stage variant, `haipipe-board-page-for-stage`, began as `haipipe-paper-stage` under the paper family; since 260805 that door is retired and all ten variants, this one included, live under the base's `page-types/`, because a variant ships where the board family maintains it.

**Where it stands**: eight skill and agent pages were rewritten to it on the day it shipped, six of them by fresh agents that loaded it with no other briefing, which is the closest thing to a test it has had.
Three of those agents died on a session limit after writing, so the batch completed but not cleanly.
A `haipipe-board-reviewer-agent` read the eight Openings consecutively on 260802, the one check this contract says it cannot pass on its own: verdict revise on the facts, and 8 of 8 survived the noun-swap pass.

## Writing Style
English only. One sentence per source line. Describe the shipped unit factually and keep generated inventory separate from human health judgment.

## Diagram
<!-- haipipe:skill:tree:start f140b94c43151dd6 board/page-types/haipipe-board-page-for-skill -->

**What `haipipe-board-page-for-skill` ships**: every file in the folder, with the one-line purpose each one states for itself.

```
haipipe-board-page-for-skill/
  CHANGELOG.md          90 ln  haipipe-board-page-for-skill · Changelog
  SKILL.md             292 ln  /haipipe-board-page-for-skill · a skill page is not a decision page
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
<!-- haipipe:skill:body:start f140b94c43151dd6 board/page-types/haipipe-board-page-for-skill -->

**haipipe-board-page-for-skill** · `0.4.2` · last shipped 2026-08-04

- folder   `board/page-types/haipipe-board-page-for-skill/`
- tools    not declared
- summary  Now lives under page-types/ and composes its mirror-page structure with the current Page Phase.

### SKILL.md




**LOAD `haipipe-board-page` FIRST.** It owns the base: the sections and their fixed order, the five rows that define each one, the title rule, the numbering, and the evaluation contract.
This file adds only what a skill page needs and a decision page does not.
It never repeats a base rule, because a copied rule is the thing that goes a night out of date while the contract moves.
After resolving this Page Type, load the current contract from `page-phases/`; generated spans constrain the phase write surface but do not replace the phase authority test.

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


- 1 · 📄 The whole page, in one picture
      Every rule in this file lands in one of these slots. Read this figure first; the sections below only say WHY.
      ```
      # haipipe-board-page · v0.11.1          ← 🤖 title · the version is DERIVED
      state: 🟡 in flux · door test passed    ← 🧑 HEALTH + the evidence for it
      owner: JL                               ← 🧑 who rules on this unit
      method: three managed spans sync…       ← 🧑 one line, how the page is kept

      ## Opening                              ← 🧑 YOURS. the three slots:
        ❶ what is it, what FOR                     ONE visible paragraph, then a
        ❷ when, vs ONE NAMED sibling               BLANK LINE, then More details
        ❸ where it stands, with evidence           as **Label**: prose parts
        🚫 the lead sentence never ends in ?

      ## Writing Style                        ← 🧑 OPTIONAL, delete if unused

      ## Diagram
        <!-- skill:tree:start … -->   ← 🤖 the folder, one purpose line
        **What `x` ships**: …  ```tree```          per file · caption is generated
        <!-- …:end -->                             an AGENT's tree is EMPTY: kept
        **How `x` is used**: …               ← 🧑 YOURS. caption, then ONE figure
        ```text  WORKFLOW … ```                    drawing how the unit is used

- 2 · Content
        <!-- skill:body:start … -->   ← 🤖 the unit's SKILL.md, its own
        … the whole file …                         bytes. NEVER write in here.
        <!-- …:end -->

- 3 · Aims                                 ← 🧑 the UNIT's open work
        - [ ] 🔧 <what it still owes>               checkboxes, no A<n> ids
              <why, indented>

- 4 · States                               ← 🧑 dated records, newest first
        <one plain paragraph: where it stands>
        - 260802 CC · 🔎 <title>
          <what happened, indented>

- 5 · Files                                ← ❌ OMITTED. the tree above already
                                                   lists every file it ships

- 6 · Log
        260802 2100 · <what changed by hand>  ← 🧑 your lines go ON TOP
        <!-- skill:log:start … -->    ← 🤖 the unit's CHANGELOG, converted
        <!-- …:end -->                             into dated Log lines
      ```

      (the markers above are shortened on purpose: a literal one inside this figure reaches every mirror page's Content span, and on 260803 that fed `sync` a fake marker and cost one page its Aims, States and Log.)

      🤖 = `skillpage.py` writes it and `sync` rewrites it. Touching it is pointless: the next `sync` erases you.
      🧑 = a person writes it and no script may touch it. This is the half that makes the page worth more than an `ls`.

      ## 🪞 What makes a skill page different

      A Q page asks a question and closes when its Aims are met. An S page closes when its human gate passes.
      A skill page **decides nothing**. Its subject exists on disk before the board mentions it, ships to other people, carries its own version and its own changelog, and closes only when the unit ships.

      Three consequences, and every rule below comes from one of them:

      ```
      1  it has no question       →  its Opening INTRODUCES; it does not ask
      2  its Content is not ours  →  the unit's own bytes, in a managed span
      3  it has a HEALTH          →  state: is a judgment about the unit, not a version
      ```

      ## 🧭 The Opening a skill page owes (the rule this skill was opened for)

      **The failure, measured 260802.** Five skill and agent pages on `01-boardform-260722` had Openings in one shape:

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
      The cause is upstream of the test: the base's Opening shape is `the question, what its words mean, why that is hard, what this page decides`, and a skill page **decides nothing**.
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
      🚫 THE LEAD SENTENCE NEVER ENDS IN `?`      mechanical, so nobody has to judge
                                                  "rhetorical". check.py enforces it
                                                  as `skillpage-opening-is-a-question`
      🚫 paraphrase the unit's own description:   Content already carries those bytes;
                                                  a paraphrase is a lossy second copy
      🚫 use the own · hard-part · depend ·       four slots produce four filler
         healthy scaffold                         sentences and one form letter
      🚫 claim health the page cannot show        ❸ names evidence or says it is missing
      ```

      **❶❷❸ is CONTENT, not a template.** The three slots say what the paragraph must ANSWER; they do not fix the order of your sentences or hand you an opening move. This matters because the base forbids a reusable scaffold, and a rule that names three slots is one keystroke away from becoming the next form letter.

      The first batch written to this contract already showed the pull: 7 of 8 put a second-person pick-me line second ("Load it when...", "Reach for it when...", "Dispatch it rather than..."), and 6 of 8 closed by confessing what has not happened yet. It survived review only because each slot carried a DIFFERENT checkable fact: 155 releases, 15-1-2 files, a one-day-old merge, never dispatched, three writers died on a limit. Answer all three; do not reach for the same sentence shape to do it.

      **The checker agrees with this contract, and did not always.** Until 260802 `check.py` warned `opening-lead-not-a-question` on every page whose lead was not a question, with no page-kind exemption, so the seven pages that obeyed THIS contract each carried a warning telling them to put the question back. A writer working the checker's list would have regressed all seven. The exemption shipped the same day the first reviewer dispatch found it. If you meet a checker rule that contradicts something here, that is a defect in one of them and not a thing to work around silently.

      **The test, and it is not the author's to pass.** Read the changed Openings CONSECUTIVELY in board order, not one at a time. A page that is clear alone still fails if its Opening would introduce its sibling after a noun swap. Dispatch `haipipe-board-reviewer-agent`; the writer's own read cannot see this, because the writer knows which unit they meant.

      ## ✍️ Derived and authored: the split a machine enforces

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

      ## 🏗 A skill page is GENERATED, never copied from the template

      **Do not follow the base's `create a new page` steps for these two kinds.** The base tells you to copy `ref/page-template.md` and then register the page in `board.md` yourself. Both are wrong here, and following them literally produces a hand-typed page with no managed spans, which `skillpage.py check` then reports as `no managed block` forever.

      ```bash
      python3 <board-skill>/cli/skillpage.py new <board> <skill-or-agent-path> \
              --group <GROUP-KEY> --stamp "YYMMDD HHMM"
              #      ▲ the KEY only, `QC`, never the full heading `QC · Engine`
      ```

      The `<n>` in `Skill-<n>` is the PAGE NUMBER, not the unit. `new` takes `max(existing) + 1`, and an archived page in `_archive/` does not count, so a retired `Skill-1` leaves its number spent rather than free. The base writes this slot as `Skill-<unit>-<slug>`, where "unit" means the shipped thing everywhere else in this family; read it as the ordinal here.

      ### Which base sections a skill page carries

      ```
      🧭 Opening        REQUIRED · authored · the three slots above
      ✍️ Writing Style  optional · newer pages carry it, older ones do not
      🖼 Diagram        REQUIRED · derived tree + ONE authored WORKFLOW fence
      📚 Content        REQUIRED · derived · the unit's own bytes, never authored
      🎯 Aims           REQUIRED · authored · the UNIT's open work
      📍 States         REQUIRED · authored
      📎 Files          OMITTED, and that is correct here: the derived Diagram tree
                        already lists every file the unit ships, so a Files section
                        would be a second, staler copy of it
      🗃 folds          Log is derived-plus-authored; the rest optional
      ```

      The base marks `Files` "allowed, advised against"; for this kind it is simply omitted, and no skill page carries one.

      ## 🔌 Shipping it is not the last step: REGISTER it

      A new skill folder is invisible to every agent until it is linked into the skill roster. The variant this file describes shipped on 260802 and was NOT linked, so `Skill(haipipe-board-page-for-skill)` failed for a whole day while the folder sat on disk. A blind door test found it: the agent concluded the skill did not exist and fell back to the base contract, which is exactly the failure this variant was written to prevent.

      ```bash
      cd Tools && ./install.sh --global      # links every plugin skill; the documented step
      ln -s <repo>/Tools/plugins/haipipe-toolkit/skills/<family>/<unit> ~/.claude/skills/<unit>
      ```

      A session already running keeps its old roster, so the link helps the NEXT session and every agent dispatched after it, not the one that shipped the skill.

      ## 🩺 `state:` is health, and only a person writes it

      The page `state:` line keeps the base's four values, and on a skill page it answers one question: **is this unit stable, in flux, in question, or parked?**

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

      ## 🎯 Aims and States on a skill page

      A skill page's Aims are **the unit's own open work**, not the page's. The page is finished the moment it describes the unit truthfully; the unit is not.

      Three sources fill them, and the third is the one people miss:

      ```
      ① what the unit itself still owes      unbuilt verbs, unwritten contracts
      ② what is unproven about it            shipped but never run, never measured
      ③ a defect another page ROUTED here    because this unit ships the file
      ```

      ③ is correct routing, not passing the buck: the page that finds a defect is rarely the page that ships the file, and a finding parked on the finder's page is a finding nobody owns. Name the page it came from.

      **The FORM here overrides the base, and that override is claimed on purpose.** The base wants `- A<n>.<m> · target` ids with a testable `Done when` and one State row mirroring every Aim id exactly once, and `writing-rules.md` forbids a checkbox on a canonical Aim. A skill page does none of that:

      ```
      ✅ ON A SKILL PAGE   Aims    - [ ] / - [x] <emoji> <the unit's open work>
                                   indented explanation · no A<n> id · no Done when
                           States  dated records, NOT one row per Aim
                                   - YYMMDD WHO · <emoji> <title>
      WHY  the base's Aim ids key to CONTENT DIVISIONS, and this page's Content is
           the unit's own bytes in a managed span. There are no divisions of OURS to
           key to, so an A<n> id would point at somebody else's headings.
           An Aim here is a to-do about the UNIT, and a checkbox is honest about that.
      ```

      Flagged by the first independent reviewer, which correctly refused to judge the Aim-to-State map on eight pages because three contracts disagreed and none claimed the override.

      **Never leave `Page generated <date>. Nothing ruled yet.`** on a page whose unit ships. That is the generator's stub, and it is a claim that nobody has looked, which stops being true the moment somebody has.

      ## 🗄 When a unit retires

      `git mv` the page into `_archive/`, remove its line from `board.md` `## Pages`, and add BOTH its id and its old `Q-Skill-<name>` alias to `## Links` pointing at the archived path, so every existing citation still resolves. Then grep the board for prose that still names the unit as live: a Log line recording what was true when written STAYS, and a sentence in live prose claiming it still ships is now false.

      Proven on `haipipe-board-index`, retired 260802: the page went to `_archive/`, its id still resolved, and the sweep found eight live-prose sentences on four other pages plus one dead citation on a sibling board.

      ## 📂 Files

      ```
      page-types/haipipe-board-page-for-skill/
      ├── SKILL.md            this variant contract
      └── CHANGELOG.md        version history
      ```

      Owns no scripts. The generator is `haipipe-board/cli/skillpage.py`; the base frame is `haipipe-board-page`; the writing standard is `haipipe-board/ref/writing-rules.md`; the roster's design record is the board's `QC3a` (how a folder becomes a page) and `QC1b` (which units exist at all).

<!-- haipipe:skill:body:end -->

## Aims
- [ ] 🧪 The three slots are tried by someone who did not design them
      Six fresh agents applied them on the day the contract shipped, and every one was briefed by the same session that wrote the contract.
      A slot only its author can fill is the failure this page exists to describe, one level up.
- [ ] 🩹 The generator cannot be broken by a skill that documents the generator
      This contract's outline figure spelled out the managed markers, that text reached `sync` through this page's own Content span, and `sync` matched the QUOTE instead of the real marker and deleted this page's Aims, States and Log.
      `skillpage.py` now anchors the marker search at a line start and the figure no longer spells one out, and nothing yet TESTS that a self-documenting skill survives a sync.
- [x] 🧑‍⚖️ The eight Openings are read consecutively by a fresh reviewer
      Ran 260802. Verdict `revise`, and the pass this contract exists for returned 8 of 8: every Opening fails the sibling noun-swap on a named, dated or measured fact.
      The reviewer named slot 2, naming the sibling you would otherwise pick, as the single rule that did it.
- [x] 📄 The whole page is shown in one picture
      JL asked what the expected outline was and this contract had never drawn one: ten sections of prose and no figure.
      0.4.0 opens with it and marks every slot machine-written or person-written.

## States
The contract shipped 260802, has been applied to eight pages, and has been through one independent review that passed the check it was built for and failed the pages on their facts.
Its health is `🟡 in flux` because everything in it is new, and the two things it most needs have not happened: a writer who did not design it, and a test that it cannot break its own generator.

- 260803 CC · 🩹 It broke the generator by documenting the generator
  The outline added at 0.4.0 spelled a managed marker inside a fence, that text landed in this page's Content span, and `sync` spliced from the quote instead of the real marker.
  `has_block` had been hardened against exactly this in 260726 and `cmd_sync` never was, so the bug waited for the first skill whose subject IS the mechanism.
  This page is the only one that could have found it, which is an argument for mirroring a tool with its own tool.
- 260802 JL · 🪞 Opened on a question, not a defect report
  JL asked "this is skill page, and it is kind of special, how do we deal with it?" after reading five Openings that were visibly one letter.
  The instinct was right for a reason worth recording: the base already carried the rule those pages broke, so tightening the rule would have changed nothing.
- 260802 CC · 🔎 The rhetorical question turned out to be GENERATED, not invented
  `skillpage.py`'s page stub seeded every Opening with a ready-made rhetorical question, and every page inherited that shape.
  Five writers were blamed for a sentence the tool wrote first, which is why the fix landed in the stub as well as in this contract.

## Log
- 260806 0140 · [REVISE-CC] card synced to disk truth after 260805 (ten types · thin-paper phase 2 · first live RUN); the "never reviewed" and "hours old" claims are corrected against the 260802 review this page's own Aims record, and the haipipe-paper-stage contrast now names the retired door and the ten page-types/ variants.
260803 · Aims, States and Log restored by hand after `sync` deleted them; the bug they exposed is fixed in `skillpage.py` and carried as an open Aim above
260802 1930 · Authored half written after the dispatched writer died on a session limit: the Opening replaced the generated rhetorical stub, and `state:` moved from 🔴 to 🟡 in flux
<!-- haipipe:skill:log:start f140b94c43151dd6 board/page-types/haipipe-board-page-for-skill -->

Converted from the skill's own `CHANGELOG.md`: 6 releases.

260804 · `0.4.2`
      - Moved under `page-types/` with the other stable Page Type variants.
      - Makes the current Page Phase a separate contract, while this variant continues to own the mirror Page's generated and authored surfaces.
260803 · `0.4.1`
      **Board bucket review, 260803** (JL: "go ahead to solve yourself, dont ask me"). Ledger: `skills/_console/260803-board-bucket-review.md`.
      - Drops "the seven sections" from the line describing what the base owns; the base no longer claims a count.
260803 · `0.4.0`
      **Opens with the whole page in one picture** (JL: "could you show what is the expected outline for the skill-page?").
      Ten sections and 240 lines said what every slot must contain and never once showed the page. A writer had to assemble the shape in their head from prose spread across the file, which is the same defect this contract was opened to fix one level down. The figure now marks every slot 🤖 machine-written or 🧑 person-written, so the split a reader most needs is the first thing they see.
      - **Merges two `## 🎯 Aims and States` sections that had drifted apart.** 0.1.0 wrote one and 0.3.0 added a second without noticing, so the contract carried two headings on one subject: one saying what Aims hold, the other claiming the form override. Found by grepping this file's own headings while answering the outline question, which is a reminder that a contract needs its own table of contents read as often as its prose.
      - `## Files` now says OMITTED in the figure rather than only in prose, since that was the one section a reader could not tell was deliberately absent.
260802 · `0.3.0`
      **Every item here came from `haipipe-board-reviewer-agent`'s first real dispatch**, which reviewed the eight pages written to 0.1.0 and reported as this contract's first independent consumer.
      **The pass this contract exists for WORKED.** All eight Openings survive noun substitution: swap in a sibling and each paragraph goes false on a named, dated or measured fact. The reviewer named slot ❷, "name the sibling you would otherwise pick", as the single rule that did it, because a paragraph naming its real neighbour cannot be swapped with that neighbour.
      - **🔴 The contract contradicted the shipped checker, and this contract lost.** `check.py` warned `opening-lead-not-a-question` on any lead not ending in `?`, with no page-kind exemption, so the seven pages that OBEYED this contract each carried a warning telling them to put the question back, while the one page that satisfied the checker was the one that broke this contract. A writer working the checker's list would have regressed all seven. `check.py` now exempts `Skill-` and `Agent-` pages and warns `skillpage-opening-is-a-question` in the opposite direction. The conflict is recorded here so the next contradiction is reported rather than worked around.
      - **🚫 The no-question rule is now MECHANICAL.** It read "open with a rhetorical question", which is a judgment call; six writers read it as "no question" and one did not. It now reads: the lead sentence never ends in `?`. A rule a checker can enforce is a rule nobody has to interpret.
      - **⚠️ ❶❷❸ is content, not a template, and this file now says so.** The reviewer's sharpest finding: the base forbids a reusable scaffold, and naming three slots is one keystroke from becoming the next form letter. The first batch already showed the pull, with 7 of 8 putting a second-person pick-me line second and 6 of 8 closing on what has not happened yet. It survived only because each slot carried a DIFFERENT checkable fact. Stated explicitly, with that measurement, as the thing to watch.
      - **🎯 The Aims-form override is claimed in writing.** The base wants `A<n>` ids, a testable `Done when`, and one State row per Aim; `writing-rules.md` forbids a checkbox on a canonical Aim; all eight skill and agent pages do none of that. The reviewer correctly refused to judge the Aim-to-State map because three contracts disagreed and none claimed the override. New `## 🎯` section claims it and gives the reason: base Aim ids key to CONTENT DIVISIONS, and a skill page's Content is the unit's own bytes in a managed span, so there are no divisions of ours to key to.
260802 · `0.2.0`
      **Everything here was found by a blind door test**, an agent given one bare task, no skill name and no path, asked only how it WOULD add a skill page.
      - **🔌 The registration gap, and it made this skill unusable for a day.** The agent could not invoke this skill: the folder shipped on 260802 and was never linked into `~/.claude/skills/`, so `Skill(haipipe-board-page-for-skill)` failed while the folder sat on disk. It read the file directly and warned that anyone else "will conclude the skill does not exist and fall back to the base contract, which is exactly the failure the variant was written to prevent." New `## 🔌` section: shipping is not the last step, and a running session keeps its old roster either way.
      - **🏗 Two contradictory CREATE procedures, with nothing routing between them.** The base says copy `ref/page-template.md` and register the page in `board.md` yourself; `skillpage.py new` uses its own stub and writes `board.md` itself. Following the base literally produces a hand-typed page with no managed spans, which `check` then reports as `no managed block` forever. New `## 🏗` section states the generator path, and `haipipe-board-page` 0.11.1 routes the two skill and agent page kinds to it.
      - **📎 `Files` is omitted on purpose, and now says so.** No skill page carries one, the base marks it "allowed, advised against", and the reason was unwritten: the derived Diagram tree already lists every file the unit ships, so a Files section would be a second and staler copy. `Writing Style` is recorded as optional, since the two newest pages carry it and the older ones do not, and "copy the sibling page's shape" was returning different answers.
      - **🔢 The `<n>` collision is named.** It is the PAGE NUMBER, while the base writes the same slot as `Skill-<unit>-<slug>` and "unit" means the shipped thing everywhere else in the family. Also records that `new` takes `max + 1` and that an archived page in `_archive/` does not count, so a retired number is spent rather than free.
      - Records that `--group` takes the KEY (`QC`) and not the full heading, which the tool's own error message implies the opposite of.
260802 · `0.1.0`
      - **First cut**, opened on JL's ask: "this is skill page, and it is kind of special,
        how do we deal with it? Like should we have haipipe-board-page-for-skill?"
      - **The measurement that opened it.** Five skill and agent pages on `01-boardform-260722` had
        Openings in one shape: `Does <name> <verb> one <noun>?` then own, hard-part,
        depend, healthy. Read alone each was clear; read consecutively they were one letter
        with the nouns swapped. JL caught it by eye before any reviewer ran.
      - **Why the base could not have prevented it, which is the reason to ship a variant
        rather than tighten a rule.** `haipipe-board-page` already carries the
        noun-substitution test, so the rule was on the books and five writers broke it
        anyway. The cause is upstream: the base's Opening shape is `the question, what its
        words mean, why that is hard, what this page decides`, and a skill page decides
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
      - Carries the skill-page rules that were previously only on the design board's
        `QC3a`: the derived-versus-authored split across the three managed spans, that a
        green `check` covers frontmatter only and not prose, that `state:` is a health
        judgment a person writes while the version rides the title, and that an agent's
        empty tree span is emitted rather than omitted.
      - Adds two rules the board learned by doing and had written nowhere: a skill page's
        Aims may be a defect another page ROUTED here because this unit ships the file, and
        the generator's `Page generated <date>. Nothing ruled yet.` stub is a claim that
        nobody has looked, so it may not survive on a page whose unit ships.
      - Adds the retirement procedure, proven on `haipipe-board-index` the same day:
        archive the page, deregister it, alias BOTH ids to the archived path, then sweep
        live prose, since a Log line recording what was true stays and a live sentence
        claiming the unit still ships is now false.

<!-- haipipe:skill:log:end -->
