<!-- TEMPLATE · ONE MEETING = ONE `Meeting-<n>` PAGE.

     DO NOT COPY THIS FILE TO MAKE A PAGE. A Meeting page is GENERATED:

       python3 <toolkit>/skills/board/haipipe-board/cli/meetingpage.py new \
               <board-folder> <path/to/note.md> --group QG --stamp YYMMDD

     The note must carry `type: meeting` frontmatter and the six `echo-meeting`
     summary headings (`### TL;DR`, `### Diagram`, `### Key Points`,
     `### Decisions`, `### Action Items`, `### Open Questions`). The generator
     picks the next free `Meeting-<n>`, writes the file from its own stub, and
     registers it in `board.md` under the group. Copy this file by hand instead
     and you get a page with no managed spans: `meetingpage.py sync` can never
     refresh it, and `check.py` reports it as broken forever.

     SO WHAT IS THIS FILE FOR. Two jobs.
       1. It is the MAP of the generated page, so a person can see at a glance
          which bytes are the machine's and which are theirs.
       2. It holds the TWO AUTHORED BLOCKS a person pastes into the generated
          page: the Opening paragraph, and the `### Routing` groups in Aims and
          States. Those blocks carry `<angle-bracket>` slots and RULE comments;
          delete each RULE comment on the real page as you satisfy it. Every
          other RULE comment here is read-only reference and never ships.

     LOAD FIRST: `haipipe-board-page` (the base frame: section order, the five
     rows per section, title rule, numbering, Decision Now shape, evaluation)
     and this folder's `SKILL.md` (the variant contract). This file repeats no
     base rule. It states only what a record of talk adds.

     WHAT THIS PAGE IS NOT.
       a decision, of any kind             -> the page that owns the subject
       an argument that grew out of talk   -> a new Q page, proposed by
                                              `haipipe-board-routing`
       the note itself                     -> the vault note, which stays the
                                              source of truth and is re-imported
       a settled unit                      -> a Meeting page is NEVER counted in
                                              a board's settled total (SKILL.md).
                                              KNOWN DIVERGENCE 260806: the engine
                                              does count it. `src/page_board.py`
                                              excludes `doc`, `stage`, `skill`,
                                              and `agent` from the settled sum
                                              and not `meeting`, so today one
                                              Meeting page inflates the board's
                                              and its group's denominator. Do not
                                              fix that on the page.

     LANGUAGE. This one page type is EXEMPT from the board's English-only rule
     and from the em-dash ban. A meeting happened in the language it happened
     in, and "fixing" a quotation falsifies the record. `check.py` keys the
     exemption on the `Meeting-<n>-` filename and applies it to the whole file,
     including the seeded Aims and Decision Now lists, which are quotations too.
     The exemption is for QUOTED MATERIAL. Your own board-facing prose, the
     Opening and every Routing row, is written in English like any other page;
     nothing will report you if it is not.

     NO markdown pipe tables in hand-written parts (JL 2026-07-10): every
     would-be table is record lines. An imported table inside a managed span
     stays as it was imported. -->

# <the note's own title, imported by the generator>
state: 🟡 PARTIAL · imported; nothing routed yet
owner: JL
method: three managed spans sync from the vault note; what it changed on this board is written by hand

<!-- RULE: the head is written by the generator and the title is the note's
     `# ` line, so the base's sentence-case purpose-title rule does not bind it.
     `state:` still takes one of the FOUR page values. This type reads them as:
       🟡 PARTIAL   imported; at least one decision is not routed yet
       ✅ SETTLED   the record is faithful AND every decision-shaped line in
                    `### What the meeting decided` has a routed State row
       ⏸️ ON HOLD   the note is wrong or incomplete and a re-import is pending
       🔴 OPEN      the generator ran and nobody has read the page yet
     The closing test is mechanical, and it is the only test this type has:
     zero `⬜ ... Not yet routed` rows under `### Routing`. -->

## Opening

<!-- RULE: THE HEAD SPAN IS MACHINE-OWNED. DO NOT EDIT ANYTHING BETWEEN THE
     MARKERS. `meetingpage.py sync` replaces the whole span whenever the note's
     hash changes, so a sentence written in here is a sentence that disappears
     without warning, and a sentence CHANGED in here is a falsified quotation.
     The start marker carries the note hash and the note path, which is how a
     sync finds its own source. -->

<!-- haipipe:meeting:head:start <16-hex-hash> <board-relative/path/to/note.md> -->
<the note's TL;DR, one line per source line, in the language it was written in>

<`created` timestamp> · <N> transcript lines · <N> chapters · recorded by `<source>`
<!-- haipipe:meeting:head:end -->

<one question, ending in a question mark, asking what this meeting changed for THIS BOARD>
<what the meeting settled here, one sentence.>
<what it reopened here, one sentence.>
<which pages should not be read without it, one sentence naming them.>

<!-- RULE: THIS BLOCK IS YOURS, AND IT IS THE ONE THING THE NOTE CANNOT SAY
     ABOUT ITSELF. The note knows what was said; only a person knows what it did
     to this board. Write it, and delete this comment.

     A page whose Opening is left as the generator's prompt, or deleted and not
     replaced, fails `check.py` with `opening-empty`: `strip_fences(...,
     prose_only=True)` skips managed spans, so an Opening that holds only the
     head span holds no prose at all. That is the state of the one live Meeting
     page today.

     Three mechanics bite the moment you write this block, and none of them is
     visible from the page:
       · The FIRST LINE must end in `?`. Once prose exists, the checker treats
         your first line as the page lead and fires `opening-lead-not-a-question`
         otherwise. There is no Meeting exemption for that rule.
       · Keep the block under 520 characters. The checker measures it as the
         on-stage paragraph.
       · It nevertheless RENDERS INSIDE `More details`, not on stage. The
         renderer splits `## Opening` at its FIRST BLANK LINE, and that blank
         line is inside the head span, between the TL;DR and the meta line. So
         the on-stage lead a reader sees is the imported TL;DR. This is a
         generator defect, not something to work around: never move your prose
         into the span to get it on stage. -->

## Writing Style
Preserve the meeting's language in quoted material. Write Board-facing interpretation in plain English, one sentence per source line, and never alter the imported record to improve its style.

<!-- RULE: the generator seeds this section once and `sync` never touches it, so
     it is editable. Add a rule only when this meeting needs one the sentence
     above does not give, such as how a speaker's initials map to real names. -->

## Diagram

<!-- RULE: MACHINE-OWNED. DO NOT EDIT BETWEEN THE MARKERS. The figure is the
     note's `### Diagram` block, already ASCII, already fenced. When the note has
     no diagram the generator writes `no diagram in the summary` inside a fence,
     and that is the honest state: do not draw a replacement, because a figure
     invented after the fact is not part of the record. Fix it in the note and
     re-run `sync`. -->

<!-- haipipe:meeting:diagram:start <16-hex-hash> -->
```text
<the note's ### Diagram figure>
```
<!-- haipipe:meeting:diagram:end -->

## Content

<!-- RULE: MACHINE-OWNED, AND IT IS THE RECORD. DO NOT EDIT BETWEEN THE MARKERS.
     Five kinds of division arrive here, in this fixed order, all from the note:
       ### Key points                 from `### Key Points`
       ### What the meeting decided   from `### Decisions`, plus one fixed line
                                      saying routing is a separate pass
       ### <n> · <chapter title>      one per `## Conversation` chapter, each an
                                      Obsidian `> [!quote]-` callout flattened
                                      into a `>` run, which this board already
                                      folds into sentence apparatus
       ### Transcript                 the raw live transcript, last
     FIDELITY IS THE WHOLE POINT. A paraphrase that sharpens what someone said is
     a record of a meeting that did not happen. If a quote needs interpreting,
     interpret it in the Opening or in a Routing row, never by editing the quote.

     KNOWN FINDING CLASS, and it is expected: every chapter division fires
     `division-no-figure`, because a chapter of talk has no face diagram. Do not
     satisfy that warning by inventing figures; they would be inside the managed
     span and the next sync would delete them anyway. The live page carries 14 of
     these warnings and they are correct behavior, not a repair list. -->

<!-- haipipe:meeting:body:start <16-hex-hash> -->
### Key points

- <one bullet per Key Points row>

### What the meeting decided

Each of these belongs on the page that owns it; routing them is a separate pass, and this list is the record it works from.

- <one bullet per Decisions row>

### <n> · <chapter title> `[<start>-<end>]`

> 💡 **Gist:** <the chapter's gist line>

> **<speaker>：** <what they said>

### Transcript

> [<time>] <speaker> <line>
<!-- haipipe:meeting:body:end -->

## Aims

<!-- RULE: SEEDED ONCE, THEN YOURS. The generator writes `### From the meeting`
     at birth from the note's `### Action Items` and NEVER writes here again,
     because you tick these and a resync would eat your state. `sync` refreshes
     the three spans above and nothing else.

     A Meeting page carries NO Aims of its own beyond this seeded list and the
     routing debt below. It never argues a position and never closes a question.
     The moment an Aim here starts making a case, that case is a Q page waiting
     to be proposed, and `haipipe-board-routing` proposes it. -->

### From the meeting
- P<n> · <the action item, in the words the note used>
  **Done when:** The action is completed or routed to its owning page.

### Routing

<!-- RULE: THIS GROUP IS YOURS, AND IT IS WHY THIS PAGE TYPE EXISTS. The
     generator does not write it, because the note's `### Decisions` list lands
     inside the managed body span where no pointer can survive a sync. Add one
     Aim here for EVERY line under `### What the meeting decided`.

     WHAT ROUTING MEANS. A decision spoken in a meeting is NOT RULED until it
     lands on the page that owns the subject. Routing is that landing: you find
     the owning page, and `haipipe-board-routing` writes the ruling there as a
     `### Decision Now` row for a choice still open, or as a dated record plus a
     `## Log` line for a choice already made. The OWNING page keeps the ruling.
     This page keeps the QUOTE and a pointer to where it went.
     A decision that lives only here has the same defect as one that lives only
     in chat: no Blocks, no Default, no trace of the options weighed, and nobody
     finds it when they open the page it actually binds.

     NUMBERING: continue the `P<n>` series the seeded group started, so States
     can mirror every id exactly once. If the note listed nine action items, the
     first routing Aim is `P10`. -->

- P<n> · Route "<the decision, quoted from the body span>" to the page that owns it.
  **Done when:** `<PageId>` carries the ruling as a Decision Now row or a dated record, and this page's State row names that page.

## States
Imported <YYMMDD> from `<board-relative/path/to/note.md>`.
<one line saying how much has been routed, replacing the seeded "Nothing has been routed onto the Q pages yet" once it stops being true>

### Decision Now

<!-- RULE: SEEDED ONCE from the note's `### Open Questions`, then yours. These
     are questions the MEETING left open, one `- [ ]` row each; a tick says the
     question is answered or has moved to its own page.

     PLACEMENT: the base puts `### Decision Now` FIRST in States, above the
     per-Aim groups (JL 260802), and that is what this template does. The
     generator currently emits it AFTER `### From the meeting`. That is a
     generator defect; reorder it by hand, since nothing here is managed.

     An open question that turns out to need a real ruling is not answered here.
     It is routed, exactly like a decision, and this row then closes with a
     pointer to the page that took it. -->

- [ ] <the open question, quoted from the note>
      Raised in this meeting and still open; a tick here says it is answered or has moved to its own page.

### From the meeting
- ⬜ P<n> · Imported from the meeting; not yet routed.

### Routing

<!-- RULE: one row per Routing Aim, mirroring its id exactly once, and this
     group IS the page's closing test.

     A NOT-YET-ROUTED DECISION LOOKS LIKE THIS, and it is the page's only open
     work:

       - ⬜ P10 · Not yet routed. No page on this board carries this ruling.

     A routed one names where it landed and when, so a reader can walk from the
     quote to the ruling in one hop:

       - ✅ P10 · Routed 260806 to `QC3b` §3 as a dated record.
       - ✅ P11 · Routed 260806 to `QB4` States as a Decision Now row, still open there.

     Use `🧠` when the routing target does not exist yet and a person must first
     approve the page that would own it; that is a board-altitude proposal and
     `haipipe-board-routing` owns it. The page closes when no `⬜` row is left. -->

- ⬜ P<n> · Not yet routed. No page on this board carries this ruling.

## Files
### Engines
- `<relative path to>/haipipe-board/cli/meetingpage.py`
  Reads the note and writes the three managed spans; seeds Aims and Decision Now once.

<!-- RULE: the generator's stub writes this path as
     `../../board/haipipe-board/meetingpage.py`, which is wrong twice: it omits
     the `cli/` folder, and the number of `../` depends on how deep the group
     folder sits. Write the path that actually resolves from this page, and
     `check.py` will confirm it. -->

### Input files
- `<board-relative/path/to/note.md>`
  The vault note this page mirrors, written by `jluo41/echo-meeting`.
- `<recording path, when the note embeds one>`
  The recording the note embeds.

<!-- RULE: an embedded recording arrives as an OBSIDIAN VAULT path, not a repo
     path, so `check.py` reports it as `dead-file-path` and will keep doing so.
     That warning is correct and the path is still worth naming. Say in the
     description line that it is a vault path, so the next reader does not spend
     a pass trying to repair a file that was never in this repo. -->

### Output files
- This page
  The artifact half. The consequences half is whatever routing lands on the pages that own the decisions.

## Log

<!-- RULE: the generator writes the import line. Every routing write adds one
     dated line here naming the decision and the page it landed on, so the Log
     is the audit trail of the closing test. Never delete a `> USER:` line:
     resolve it and move it here verbatim. -->

<YYMMDD> · Routed "<decision>" to `<PageId>`
<YYMMDD> · Imported from `<board-relative/path/to/note.md>` by `meetingpage.py`
