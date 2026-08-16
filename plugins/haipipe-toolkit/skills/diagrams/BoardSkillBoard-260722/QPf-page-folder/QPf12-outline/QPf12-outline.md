# Outline · the page re-read per division, from §N anchors, live
state: 🟡 BUILT · engine, tab, and both lenses live (260816) · open: migration, plugin skill
owner: CC
method: one anchor mark §N on aim, state, and file rows; a live tab parses it into per-division cards with two lenses; no claude at render time
session: 190ceaff-4d09-4915-8536-5ce0f28913ec

## Opening
Can a page's aims, states, and files say which Content division each belongs to, so a machine can re-read the page per division without judging?
A division is one `### N ·` part of Content; today the tie between a division and its aims lives only in the writer's head.
This page decides one anchor mark, `§N`, written on an aim, state, or file row.
A live 🧭 Outline tab parses it: one card per division with its aims, ticks, and state receipts; unanchored lines gather under 🌐 page-wide.

**Succeeds when**: the tab renders from the `.md` alone, instantly, and the same parse that draws it also reports whether the page is aligned.

**Rule-based over authored**: an authored mapping costs claude minutes on every regenerate and can map the same page two different ways; an anchor written in the material is judged once, by the writer, and parsed forever. Ruled JL 260816: "我不想每一次都靠一个 code 去做这件事".
**The family shape**: 📂 folder (`QPf1`) shows what the page's folder holds; this tab shows what the page's prose holds. Both are live, storage-less meta-surfaces: no subfolder, no roster row, nothing to go stale.
**Covered elsewhere**: the roster that this plugin deliberately has no row in is `../../../board/haipipe-plugin/ref/roster.md`; the folder tab precedent for live no-store rendering is `QPf1`; the section grammar the anchors lean on (`### N ·` divisions, Aims/States `### A<n>` groups) is owned by `/haipipe-page` and `ref/page-template.md`.


## Diagram
**One anchor, one parse, two lenses**: the judgment is in the material; the machine only sorts.

```text
  📄 page.md                      ⚡ GET /_board/outline (live, no-store)
  ┌─────────────────────┐         ┌──────────────────────────────┐
  │ ## Content          │         │ 📏 CHECK  bad §N → named      │
  │  ### 1 ·  ### 2 ·   │  ──▶    │           loose lines → count │
  │ ## Aims             │         ├──────────────────────────────┤
  │  - [x] §1 aim …     │         │ 🧭 By division   🚦 By progress│
  │  - [ ] §2 aim …     │         │  div card:        ⬜ open first│
  │ ## States  §1 …     │         │  aims+ticks       ✅ done      │
  │ ## Files  `f.py` §1 │         │  state receipts   〔div〕badge │
  └─────────────────────┘         │  🌐 page-wide = the to-anchor  │
       ✍️ anchored by the writer   │     worklist                  │
          once, at write time     └──────────────────────────────┘
```

## Content
### 1 · The §N anchor
**Two grammars, one meaning**: the template already anchors; `§N` catches what it does not.

```text
  ① the A-grammar    ### A3 group  ·  id A3.1     already says "division 3"
     (free)          ### P  group  ·  id P1       already says "page-wide"

  ② the §N anchor · POSITION is what makes it an anchor
     🎯 Aims    - [x] 📂 §1 the text …    LEADS, after box, emoji, or id
     📍 States  §1 shipped 260815 …       LEADS the line
     📎 Files   `build.py` §1 §2          TRAILS, and may be several
     🗃 Log     never anchored            it is a time axis

  ✋ not anchors, all four seen on real pages
     `QB6` §7 · [QB7 §3](…)   a division of ANOTHER page
     §5.1 · §4.3              a sub-division
     §Required Inputs         a named section, no number
     "Every number §4 prints" a manuscript section, in ordinary prose
```
📌 This part fixes the mark itself: what it points at, where it may appear, and what an unanchored line means.

A page written to the current template needs NO anchor at all.
Its Aims and States are already grouped `### A3 ·` and its ids already read `A3.1`, and both name division 3; `P1` already says page-wide.
So the first grammar is free, and this page is its own proof: every one of its aims maps with zero anchors written.
The `§N` anchor exists for what that grammar does not reach, which is every page written before it and every line that sits outside a group.
The anchor is the literal token `§N`, where N is the number of a `### N ·` division in this page's own Content.

POSITION is what separates an anchor from prose, and it has to be.
The `§` sign was in use on these boards long before this plugin, and a paper-section page writes `§4` in ordinary sentences to mean the manuscript's own section 4.
No reading of the characters alone can tell those two apart, so the anchor is recognized only where prose does not put one: leading an Aim or State row, or trailing a Files row.
An aim or state line carries at most one anchor, and it leads, after the checkbox, the state emoji, a decorative emoji, or the aim's id.
A Files row carries several, and they trail at the end, because one code file often serves several divisions.
Everything in the middle of a sentence is prose and is left alone.
An unanchored line is legal and means page-wide: it belongs to the whole page, not to one division.
So an existing page with no anchors at all parses cleanly today; its outline is simply one 🌐 card, which is honest and uninformative.
Log lines never take an anchor: the Log is ordered by time, and cutting it into divisions would cut its story.
The anchor points by number, so whoever renumbers Content divisions owes the page's anchors in the same edit; the parser catches an out-of-range `§N`, and it cannot catch an in-range one that now points at the wrong part.

### 2 · The live surface: check and view in one walk
**The tab's two jobs**: the same parse measures the page and draws it.

```text
  ── the answer, before any detail ──────────────────────
  🧭 QPf11-pagex
  How does a page borrow a file from another page …    ← the page's OWN
  ███████░  11 of 12 done · ⬜ 1 to do · 🗣 1 waiting     lead question
  ──────────────────────────────────────────────────────

  header   ✅ every line is placed · ⚠️ 3 lines not placed in any part
           · ❌ §7 points at a part that does not exist
  chips    [🧭 By part]  [🚦 What is left]

  a card    1 · The contract                        2/2
            what a person writes and keeps          ← the brief
            ⬜ STILL TO DO   open aims, always in sight
            ▸ ✅ 2 DONE      finished work, folded away
            ▸ 📍 MORE        notes and files, folded away
  🧭 lens   one card per division · under its title, ONE LINE saying
           what the division is about · then ✅ done aims (each with
           its §-matched state receipt), then ⬜ open aims · 🌐 last
  🚦 lens   ⬜ open bucket FIRST (the page's to-do) then ✅ done ·
           every aim wears a 〔div N〕 badge linking back

  one aim on a card · three parts, three jobs
    🎯 the goal    plain voice · the id ONCE, as a dim tag on the right
    📍 NOW …       the State beneath it, behind a `now` label
    🗣 the ask     a Decision Now row is neither, and gets its own card

  the brief, read in this order and never invented
    📌 the job line     `📌 This part fixes …` · `📋 Establishes …`
    🏷 else the caption  `**The tab**: the first surface renders …`
    ✍️ else the first plain sentence
    ⬜ else nothing      a wrong summary is worse than none
```
📌 This part fixes the surface: rendered live on every open, never written to disk, wrong anchors shown rather than thrown.

The view is rendered by `GET /_board/outline` on every open and stored nowhere, on the `QPf1` precedent: a status written to disk starts aging the moment it lands.
Because nothing is stored, this plugin has no staleness, no ✨ Regenerate, no subfolder, and no roster row: like 📂 it is a meta-surface over the page, the family's second.
Checking is not a separate gate: an out-of-range `§N` renders as a named ❌ on the card it tried to reach, and every unanchored aim or state swells the 🌐 card, so the 🌐 card doubles as the worklist for anchoring the page.
The two lenses are the same parsed data sorted twice, switched by chips client-side with no second request; a third lens later is one more chip, never a new writer.
In the 🚦 lens the ⬜ bucket renders first, because opening that lens is asking what this page still owes.

THE ANSWER COMES BEFORE THE DETAIL, and that is a requirement, not a taste.
This surface is read by someone with ADHD, in a language that is not their first, and the first version failed both: it opened straight into division 1, every line was a long sentence, and finished work was printed in full above the one thing still to do.
So the top of the tab now carries the page's own lead question, saying what the page is for before any aim is listed, then one line of numbers: how many aims, how many done, how many left, how many decisions wait on a person.
Each card shows its count on the right, its brief under its title, and its OPEN aims in plain sight, while finished aims fold behind a count that can be clicked.
Nothing is hidden and nothing is invented; what changes is the ORDER, so a reader who takes in one screen gets the state of the page and not the middle of a paragraph.
The words follow the same rule: `loose lines` became `lines not placed in any part`, `aligned` became `every line is placed`, and `By division` became `By part`, because a reader meeting the tab has no reason to know this plugin's shorthand.

An Aim and its State are two different sentences, and the card has to keep them looking different.
An Aim says what should become true; a State says what is true now.
Printed as two alike lines that both open with the same id and both wear a tick, they read as one sentence said twice, and a reader stops trusting either.
So the id prints once, as a dim tag on the right, the goal keeps the plain voice, and the status sits under it behind a small `now` label in the State's own emoji.
A `Decision Now` row is a third thing again, an ask a person still owes, so it is neither counted as a state nor dropped: unanswered asks get their own card at the top, because a page waiting on someone should say so before it lists what it has done.

A division card also says in one line what its division is about, and that line is read, never written.
The template already asks each division for one: the `📌` line under its face diagram, saying what the part settles.
Pages in the wild write the same line in their own hand, `📋 Establishes the reading protocol`, so the reader looks for the SHAPE, an emoji then a sentence, rather than for one emoji.
A division with no such line falls back to its figure caption, then to its first plain sentence, and a division with none of the three shows no brief at all.
That last step is the same rule the anchors follow: a summary nobody wrote is not invented, because a wrong one costs the reader more than a missing one.

### 3 · Migration: authored once, mechanical forever
**Claude's one appearance**: propose anchors into the `.md`, be reviewed, leave.

```text
  ✍️ claude -p  reads page  ──▶  proposes §N per aim/state  ──▶  👀 JL reviews
                                                                    │
  ⚡ forever after: the parser reads what the writer wrote   ◀──────┘ written into .md
```
📌 This part fixes how existing pages get their anchors without hand-writing sixty of them.

Existing pages predate the anchor, so their outlines would open as one 🌐 card each.
The migration is a one-time pass per page: claude proposes an anchor for each aim and state line, the proposal is written into the `.md` as ordinary text, and a person reviews the diff before it lands.
After that pass the judgment lives in the material and claude never renders, which is the whole point of the rule-based route.
New pages anchor at write time: the writer who creates an aim knows its division better than any later reader.

## Aims
### A1 · The §N anchor
- A1.1 · The anchor rule is stated once, on this page, and nowhere contradicts the page template.
  **Done when:** Content §1 names the token, its three legal sections, the multi-anchor Files exception, and the unanchored default, and `/haipipe-page` needs no edit to coexist with it.
- A1.2 · A bad anchor is caught mechanically.
  **Done when:** An out-of-range `§N` on any parsed page renders as a named ❌ in the tab.

### A2 · The live surface: check and view in one walk
- A2.1 · The parser and renderer ship as one live module.
  **Done when:** `live/outline.py` answers `GET /_board/outline` with the per-division cards for any page, no-store, nothing written to disk.
- A2.2 · The tab is on the rail.
  **Done when:** A drawer registration shows 🧭 Outline in the right pane and the shell's same-src reload keeps it fresh, the `QPf1` two-layer contract.
- A2.3 · Both lenses work from one payload.
  **Done when:** The 🧭 and 🚦 chips re-sort client-side with no second request, and the 🚦 lens lists ⬜ before ✅.
- A2.4 · A division card says what its division is about, in the page's own words.
  **Done when:** Each card carries one line under its title, taken from the division's job line, caption, or first sentence, and a division with none of those shows no brief rather than an invented one.
- A2.6 · A reader learns where the page stands from one screen, without reading a paragraph.
  **Done when:** The tab opens with the page's own lead question and a count of done, left, and waiting; each card shows its own count and brief; open aims are in sight while finished ones fold; and no label uses this plugin's shorthand.
- A2.5 · A goal, its status, and an open ask never look like the same sentence.
  **Done when:** An aim's id prints once, its State sits under it behind a `now` label, and an unanswered Decision Now row shows as an ask on its own card instead of being read as a fact about an aim.

### A3 · Migration: authored once, mechanical forever
- A3.1 · The QPf pages of this board carry anchors.
  **Done when:** Each sibling page's aims and states wear reviewed `§N` anchors, landed as ordinary `.md` edits.

### P · Page-level
- P1 · The plugin proves itself on QPf1-folder.
  **Done when:** QPf1's outline renders both lenses correctly against a hand-check of its two divisions, seven aims, and states.
- P2 · No page anywhere breaks it, and no row ever goes missing.
  **Done when:** Every page on every board parses, renders, and lands each of its aims and states on exactly one card, with no anchor flagged that its writer did not write.

## States
### Decision Now
- [ ] 🗣 Does the §N anchor enter the page template and `/haipipe-page`, or stay a convention this plugin reads?
      📍 `Part` Content §1
      🔔 `Why now` the grammar is being written; where it is owned decides who must obey it
      ⭐ `A ·` stay plugin-local until proven on this board, then canonize; costs nothing if the shape changes
      `B ·` canonize now in `ref/page-template.md` and `/haipipe-page`; every new page anchors from birth, but a shape change later touches the contract twice
      🛑 `Blocks` nothing; the engine and this board's migration proceed either way
      🤖 `If nobody answers` A takes effect

### A1 · The §N anchor
- ✅ A1.1 · Met; Content §1 on this page states the full rule, and it adds no section and renames nothing the template owns.
- ✅ A1.2 · Met; `§7` against a two-division page renders as `❌ §7: no such division` in the header, from `parse_outline`'s `bad` list.

### A2 · The live surface: check and view in one walk
- ✅ A2.1 · Met; `live/outline.py` answers `GET /_board/outline` no-store and writes nothing, proven at HTTP 200 against both QPf12 and QPf1.
- ✅ A2.2 · Met; `07-plugin-outline.js` registers 🧭 Outline second on the rail, and the built page carries the label and the route.
- ✅ A2.3 · Met; both lenses render server-side into one payload and the chips toggle with no second request.
- ✅ A2.6 · Met; QPf11 now opens on "How does a page borrow a file from another page and read it live, without copying it?" over `11 of 12 done · 1 to do`, and its four cards fit one screen with only the unfinished one expanded. Guarded as tier ⑤ of `checks/outline.py`, which fails if the purpose line, the count, or the open-before-done order is lost.
- ✅ A2.5 · Met; the id prints once as a right-hand tag, the state reads `NOW …` under its goal, and `### 🗣 Decision Now` is recognized with its leading emoji, which it was not before: QPf11's pending ask had been counted as a state row. Guarded as tier ④ of `checks/outline.py`.
- ✅ A2.4 · Met; 771 of 788 divisions across all six boards show a brief read from their own text, and of the 17 without one, 16 are cards the safety net drew for divisions Content never declared and the last is a division written entirely as bold group titles over bullets, with no sentence to take.

### A3 · Migration: authored once, mechanical forever
- 🔨 A3.1 · Started on QPf1 by hand, three anchors landed; the other QPf pages are unanchored and open as one 🌐 card each.

### P · Page-level
- ✅ P1 · Met; QPf1 renders §1 and §2 as their own cards with the rest under 🌐, and QPf12 maps every aim with no anchors at all through the A-grammar.
- ✅ P2 · Met and GUARDED; `checks/outline.py` walks 299 pages across all six boards plus 18 anchor shapes and 6 page shapes, and it runs first in `checks/run.py`, so a parser that would swallow an aim fails the board's standing checklist rather than a reader's eye.

## Files
### ⚙️ Engines
- `../../../board/haipipe-board/live/outline.py`
  The parser and renderer; the one place the anchor grammar is executed. §1 §2
- `../../../board/haipipe-board/cli/serve.py`
  Routes `GET /_board/outline`; one route line, on the folderstat pattern. §2
- `../../../board/haipipe-board/assets/js/10-drawer/07-plugin-outline.js`
  Registers 🧭 Outline second on the rail, right after 📂 Folder. §2

### 📋 Contracts
- `../../../board/haipipe-board/ref/page-template.md`
  The section grammar the anchors lean on; edited only if Decision Now picks B.

### 🧪 Checks
- `../../../board/haipipe-board/checks/outline.py`
  The standing check: the position rule, six page shapes, and every page of every board, offline. Registered first in `checks/run.py`. §1 §2
- `../../../board/haipipe-board/live/folderstat.py`
  The live no-store precedent this module copies: same walk measures and lists. §2

## Law
- 260816 JL · 📏 Rule-based beats authored for the outline mapping
      The aim-to-division tie is written into the `.md` as a `§N` anchor and parsed; no claude call at render time.
      An authored mapping was designed first and rejected: it costs minutes and money per regenerate, goes stale, and can map the same page two ways ("我不想每一次都靠一个 code 去做这件事，还是说你觉得这其实是 OK 的？" answered: not OK).
- 260816 JL · ⚡ The outline is live and storage-less
      Rendered on every open, written nowhere, so it can never be stale; the plugin therefore has no subfolder and no roster row, the family's second meta-surface after 📂 folder.
- 260816 JL · 📎 Files rows may carry several anchors
      One code file often serves several divisions, so `§1 §2` on a Files row is legal ("一些 file 里面的内容，实际上我感觉也是可以一一对应起来").
- 260816 CC · 📍 An anchor is recognized by POSITION, never by shape alone
      Leading an Aim or State row, trailing a Files row; a `§N` anywhere else is prose and is left alone.
      Forced by the sweep, not designed: `§` already meant three other things on these boards, and a paper-section page writes `§4` in plain sentences to mean the manuscript's section 4. Shape-matching flagged four real pages that had written nothing wrong; position flags none of them.
- 260816 CC · 🅰️ The template's A-grammar is the first anchor, and it is free
      A `### A3` group and an `A3.1` id already name division 3, so a page written to the current template maps with no `§N` written at all; `§N` is the catch-up grammar for older pages and loose lines.
      Found while building the parser, not designed: QPf12 mapped every aim on the first run, while QPf1, written before the A-grammar, put all eleven of its lines under 🌐.
- 260816 CC · 🗃 The Log never takes an anchor
      A time axis cut into divisions loses its story; unruled by JL but unopposed, revisit if it chafes.

## Log
- 260816 · [JL ruled] the tab must answer before it explains ("我读完之后 no idea，不知道在干嘛", and the reader has ADHD and reads English as a second language). The failure was the ORDER, not the content: the tab opened into division 1 with no word about what the page was for, every visible line was a long sentence, and finished work was printed in full above the one thing still to do. Now the page's own lead question sits at the top over a count of done, left, and waiting; each card carries its own count and brief; open aims stay in sight and finished ones fold behind a clickable count; and the labels dropped this plugin's shorthand, so `loose lines` reads `lines not placed in any part`. Nothing is hidden and nothing is summarized by a machine, which keeps the rule-based promise intact. QPf11 went from a wall of twelve full aims to four cards on one screen with one expanded.
- 260816 · [JL ruled] a card must not print the same sentence twice ("I cannot understand what is happening", reading QPf11's card, where an Aim and its State both opened `A1.1 ·` and both wore a ✅). The id now prints once as a dim tag, the goal keeps the plain voice, the status sits under it behind a `now` label, and the per-row tick went because the group heading already said done or open. Reading QPf11 for the fix also found a parser defect it had been hiding: `### 🗣 Decision Now` carries its emoji BEFORE the name, so the block went unrecognized and its pending asks were counted as facts about an aim. Recognized now, and shown as its own 🗣 card, because a page waiting on a person should say so before listing what it has done.
- 260816 · [JL asked, CC shipped] a division card now says what its division is about ("could we also briefly say what this division is about"), and the line is READ, not written: the template's own `📌` job line first, then the figure caption, then the first plain sentence. Free, like the A-grammar was: 771 of 788 divisions across six boards already carried one. The board turned out to write that line in several hands (`📌 This part fixes`, `📋 Establishes`, `🧭 Establishes`), so the reader matches the SHAPE, an emoji then a sentence, not one emoji. One division has no brief and keeps none, because a summary nobody wrote would have to be guessed.
- 260816 · Hardened after JL asked whether it actually works: driven through the real board shell with a headless browser (menu ▸ 🧭 Outline ▸ the frame lands ▸ the chips switch ▸ the badge jumps back), then swept over 299 pages on 6 boards. The sweep found two real defects the first build had missed and neither would have crashed: an `### A6` group whose division Content never declared made its aim invisible in BOTH lenses, and shape-matched anchors flagged four innocent pages, because `§` already meant three other things here and a paper-section page writes `§4` in plain prose. Fixed by the position rule and a safety net that draws a card for any division the material names, then frozen as `checks/outline.py` inside `checks/run.py`.
- 260816 · Shipped in the same session it was opened: `live/outline.py` (parse + check + both lenses), the `GET`/`POST` pair on `serve.py`, and `07-plugin-outline.js` second on the rail. Proven at HTTP 200 on QPf12 and QPf1, with a bad anchor and a multi-anchor Files row tested apart. Two things changed on contact with the code: the template's A-grammar turned out to be a free first anchor (Law), and a State row carrying an Aim id now folds UNDER that aim as its receipt instead of listing States again, because a second full list would only re-group the page by kind, which is the defect this tab exists to fix.
- 260816 · Page opened as QPf12 (QPf11 was already taken by pagex, JL caught the collision); the rule-based route, the live storage-less surface, the two lenses, and the multi-anchor Files exception all ruled in the opening session.
