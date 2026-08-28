---
name: haipipe-plugin-outline
description: >-
  The 🧭 outline surface of a Board page: the page re-read one Content division
  at a time, each card carrying its Aims, State, Files and evidence rows,
  above them the PLAN card from the page's versioned outline file. Read-only,
  and the deliverable of the OUTLINE phase. Trigger: outline plugin, outline
  tab, page outline, OUTLINE phase, evidence bundle, approve the outline,
  /haipipe-plugin-outline.
metadata:
  version: "0.15.0"
  last_updated: "2026-08-17"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-plugin-outline · the page, read one part at a time

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface, writer, boundary.
This file owns only outline's delta: how a line says which division it belongs to, and what the tab does with that.

The gap it closes (QPf12, JL 260816): a page is grouped BY SECTION KIND, so all Content sits together, then all Aims, then all States. Reading about one part means jumping between three lists. This surface flips the axis: one card per Content division, everything belonging to it inside.

## 🎛 What this surface IS · the page's one control surface

**🧭 is not one tab among many; it is where a person stands to work a page** (JL 260817: "we need to make the outline plugin to be more important"). Every other plugin shows ONE material: 🚪 the questions, 🖼 the units, 📚 the keys, 📂 the folder. Only 🧭 shows the PLAN and, against each part of it, what that part still owes.

```text
  🚪 probe    the cards        ─┐
  🖼 display  the units        ─┼─▶  🧭 outline   one row per division:
  📚 bibex    the keys         ─┤                 what it must establish,
  📄 the .md  divisions·aims   ─┘                 and what it still owes
```

That is the promotion, and it comes from a real failure. On 260817 a page carried an outline table pasted into its own `## Content`, three prose sentences restating probe-card states, and a fourth declaring a display that did not exist. Every one of those was a person writing down what this surface should have SHOWN them. When the plan and its evidence are visible in one place, the prose has no reason to duplicate either.

**The question it answers, and no other surface can**: *what does this page still owe, division by division?* 📂 answers it for the folder, 🚦 By progress answers it for the ticks; neither joins the plan to the evidence.

## 🚧 Whose phase this is

The file is the deliverable of OUTLINE, phase ① of the page workflow. That phase's authority, its human gate and its receipt are `page-workflows/haipipe-page-outline` (260817); this file owns only the MATERIAL and the SURFACE and states neither of those twice.

```text
  🚧 the phase   what OUTLINE may do, and what ends it   ../../page-workflows/
                 (a person ticks `approved:`)              haipipe-page-outline
  🗂 the file    where it lives, its shape, its marks    ← this file
  📡 the tab     how it is read, and what it joins to    ← this file
```

## 🗂 Storage · a versioned markdown file, one per round

**Overturned 260817 (JL): the outline is a FILE.** Version 0.1.0 stored nothing and derived everything from the page's own headings. That works for reading a page that already exists and fails for the phase's real job, which is to agree what a page WILL say before it says it. A plan that lives only as a projection of the thing it is planning cannot exist before that thing does.

```text
<page>/outline/
├── <stem>-outline-v1.md      the round's plan · 🧑 AUTHORED · never regenerated
├── <stem>-outline-v2.md      the next round · `supersedes: v1`
└── <stem>-outline-v_0707.md  a date suffix is equally legal (JL 260817)
```

**The freeze happens at APPROVAL, not at creation** (JL 260817). Before the tick, `v1` is a working document: discuss it, rewrite it, delete a bullet that turned out wrong. A wrong plan during drafting is just deleted; it needs no version and no record, because nobody has agreed to it yet.

```text
  ✍️ v1, approved: ⬜   discussed many times · edited freely · delete what is wrong
        │
        │  🚧 a person ticks approved:
        ▼
  🔒 v1, approved: ✅   frozen · CORRECT AS OF THAT MOMENT
        │
        │  the work moves on: the scope grows, a direction opens
        ▼
  ✍️ v2, approved: ⬜   `supersedes: v1` · a new working document
```

**`v2` does not mean `v1` was wrong.** It means `v1` was right then and the work has since moved. That is why `v1` is kept rather than corrected: it is the record of a plan that was correct at its date, not a mistake to be fixed.

**PRIMARY material.** The file is authored by OUTLINE and read by every phase after it. Nothing regenerates it, and the page's own `.md` is never its source.

⚠️ **Storage-less was the old invariant, and it is gone; "cannot be stale" survives in a different form.** The outline file is not a cache of the page and so cannot disagree with it: it is a record of what was agreed at a moment, and the page is what was then built. `v2` supersedes `v1` rather than correcting it.

⚠️ **The surface now reads three things**: the outline file, the page `.md`, and the page's sibling plugin folders (`probe/`, `display/`, `bibex/`). It still writes nothing and still calls no model.

## 📐 The file's shape · Section ▸ Paragraph ▸ Bullet

The plan goes down to the BULLET, and a bullet is a POINT, not a sentence (JL 260817: "我们能一句话把一个 point 讲完吗? 我感觉现在这里更像是 point"). One point becomes ONE OR MORE sentences when it is drafted, so the plan and the page count different units and must say so.

```text
  🧭 outline   C3.P2.B1   one POINT      "OLS: ols-progressive the control
                                          ladder, ols-lpm-logit the binary
                                          form, ols-twopart the hurdle, …"
                             │
                             ▼  DRAFT writes a sentence scaffold with holes
  📄 page      C3.P2.S1 · S2 · S3   the sentences that point became
                             │
                             ▼  REVISE turns the scaffold into final prose
```

`C3.P2` is shared by both, so the link survives; only the last token differs, and it differs because the units differ. `haipipe-sentence` owns `S` on the rendered page and this file owns `B` in the plan; neither redefines the other.

**The letters, and why `C` stays.** `C` is the SECTION, not decoration: Aims use `A` and page-wide uses `P` in that same slot (`haipipe-sentence` §✍️, `QPs1` §0.6), so dropping it would collide `C1` with `A1`. It is printed ONCE on the section heading and the rows below carry only `P<n>.B<n>`, which is the part that changes (JL 260817).

Bullets, not prose: each line says what that point will establish, and carries what it owes.

**A division heading is a short name, never a summary sentence.** Write exactly
one separator: `## C<n> · <name>`. The name is at most 8 English words and at
most 56 characters. A second ` ·` clause is forbidden. Put the reason this
division exists in `arc:`, its paragraph briefs, or its bullets. This keeps the
division list readable without opening any detail.

**Short is not enough: the name must identify its own subject.** Do not hide
the concrete objects behind counts or generic role words such as `one
contract`, `two readers`, `the boundary`, or `the service`. Name the actual
objects when the reader needs them to understand the division, such as
`BatchReader`, `OnlineReader`, `Data API`, or `S3`.

```text
  ❌ ## C1 · Data and feature boundary · The reader contract starts by fixing what readers return
  ✅ ## C1 · Data vs. features
  ❌ ## C2 · One contract, two readers
  ✅ ## C2 · Shared lookup rules for BatchReader and OnlineReader
```

```markdown
# QC1-visitlbp · outline v1
outline-version: v1
supersedes: —
date: 260817
approved: ⬜            🚧 a person ticks this. No machine may.

## C3 · Method

### C3.P1 · What actually runs
- B1 · Script Census
  Note: the task-folder holds 61 Stata scripts and 14 PowerShell runners
- B2 · Specification Grid
  Note: 12 specification families × 5 traits, plus one summary-statistics script
- B3 · What One Run Fixes
  Note: one outcome window and one estimator family                   📮 PP04
```

**The file ends with its own `## Aims` trailing section, and the Aims live HERE
since 260819** (JL: "Aims should be move together with outline"). One Aim = one
target plus its test, and `Done when:` IS the test:

```markdown
## Aims · what must become true, and how you would know
- A3.1 · The headline coefficient carries its four coordinates.
  **Done when:** a reader can quote SPEC, window, trait form and outcome
  without opening the task folder.
```

Before the move the plan wrote an id and the PAGE held the target, so a plan
that renumbered its divisions pointed `A4.1` at the page's OLD A4.1; nine of
sixteen ids on `QPw00-page-loop` did exactly that. DRAFT transcribes the Aims
onto the page verbatim, because inventing one there would fork the agreed
target.

**The marks, and every line carries exactly one status plus what it owes:**

```text
🎯 aim        we intend to establish this and have NOT yet
⛔ ✅ "have it" was RETIRED 260819 (see below): an unmarked bullet
              already means nothing is owed
📚 citation   owes a bib key            → bibex/
📮 probe      owes a QUESTION answered  → probe/PP<NN>/
              — bare before ② raises
              the card, `📮 PP<NN>`
              after; the answer may be
              a finding or numbers
🧮 value      QUOTES one number,        → that card's ## Values
              `PP<NN>.v<n>`, out of an
              answered card; the
              machine re-computes it
🖼 display    owes a figure or table    → display/<stem>-DisplayN-<slug>/
              · and NAMES ITS KIND: `🖼 owed · table`
```

⛔ **A fifth mark, proof, was RETIRED on 260819** (it wore 🧮 then; the glyph was revived hours later as the VALUE mark, with 🔢 as the legacy alias). It was created from one
transcribed quote and no Log row ever ruled it. JL: "我从开始到最后都没有说
proof，我一直说 probe" — going to a task folder or a discovery folder for the
evidence behind a claim IS a probe, which is 📮 (the value it yields is quoted as 🧮 PP<NN>.v<n>). The retired mark was the only
one with no plugin, no folder, no lane, no id and no backlink, and that was the
symptom. ⚠️ `proof/` the FOLDER is unaffected: it is a probe card's own.

**A 🖼 mark carries its KIND, and the bullet's own sentence is the whole design.** There is no display section in a plan: one bullet is one unit, its sentence says what the reader will see, and the mark says which renderer family draws it (JL 260817: "display 的设计都有哪些呢?").

```text
  - B4 · the funnel drawn as one waterfall, 773,566 down to     🖼 owed · figure
    765,701, with the unexplained drop as its own bar
         └── the DESIGN: what a reader sees, in the plan's own words
                                                     └── kind, so the renderer
                                                         is picked at plan time
```

The five kinds are the display family's: `table` · `figure` · `diagram` · `tex` · `illustration`. What the plan does NOT carry is `claim:`, `caption-job:`, `intake:` and the renderer's own rows; those live in the unit's README and cannot be written until a card has ANSWERED, because the intake freezes from its `proof/` (`haipipe-plugin-display` §❄️). So a plan states the INTENT and a unit states the DESIGN, and the mark goes bare `🖼 owed · <kind>` until the folder exists, then names it: `🖼 Display1 · table`.

**A 📚 names a PUBLISHED WORK, never a sibling board page** (JL 260817: "我们这里 citation 的 button 好像不是很多?"). The mark means a bib key in this page's own `bibex/`, and the surface checks it three ways:

```text
  📚 Deyo2015    in bibex/                          ✅ the key resolves
  📚 Foo2020     🚨 not in bibex/                    the key was never landed
  📚 QB1         🚨 board page, not a citation       the commonest error
```

The third row is a real defect this file caused: a plan marked `📚 QB1 · QB2 · QB3` on the page whose `bibex/` held ZERO entries. Those are board pages, and pointing prose at a sibling page is an internal cross-reference, which is a different act from citing published knowledge. A cross-reference is written in the bullet's own words; only a bib key wears 📚.

**An id on a bullet is a CITATION, not a copy.** `📮 PP01` names a card, `🧮 PP01.v2` quotes one of its values; it never restates the card's question or its state, because the evidence column below reads that live. A bullet that spells out what a card says is the same duplication that put `Evidence owed: probe/PP03-…, state raised.` into a page's prose on 260817.

**A 🎯 aim bullet names the Aim it belongs to, and that is the whole link to `## States`** (JL 260817; the Aims' home moved into the plan file 260819, §📐 above). The id grammar already exists and this surface already parses it, so nothing new is invented:

```text
  🧭 plan bullet     - the choice has never been written down            🎯 A2.1
  🧭 plan ## Aims    - A2.1 · Confirm LBP as the lead, and say why
                       Done when: the rationale is one readable division
  📄 page ## Aims    the same rows, TRANSCRIBED at DRAFT, never invented there
  📄 page ## States  - ⬜ A2.1 · No rationale recorded
```

One id ties the four: the plan's bullet says what the sentence will establish, the plan's `## Aims` says what must become true and how a reader would know, the page carries the transcription, and `## States` says whether it has become true. A 🎯 bullet with no Aim id is an intention nobody is tracking, and an Aim with no bullet is a target no sentence is aiming at; the tab shows both as named rows rather than silence.

An UNMARKED bullet needs no id, because a plain point has nothing to track. The marks point at cards, and cards carry their own state on disk. (`✅ have it` was RETIRED 260819: it claimed backing without NAMING it, so nothing could recheck it; a backed point either cites its id or stands as plain prose, and the ↩ backlink already shows every card that serves a bullet. The glyph also worked two other jobs — the tick syntax `approved: ✅` and phase ⑦ — which produced a phantom-chip bug the same day. JL failed to read the mark three times; a mark that needs explaining fails its only job. Zero plans carried it at retirement.)

**A mark carries an id only when the id already EXISTS.** A 📚 can, because a bib key is found before it is cited. A 📮 or 🖼 usually cannot: the card is created at PROBE, after this file was frozen. So the mark is bare, and the CARD names the bullet it serves (`haipipe-plugin-probe` §↩). The 🧭 tab joins from that side and prints `↩ PP04 serve this bullet · 2 of 3 answered`.

**Each mark names what a bullet OWES; a plugin names WHERE it is answered.
The two use different words for the same thing, on purpose:**

```text
  the mark        what the bullet owes      the plugin that owns the answer
  ────────────────────────────────────────────────────────────────────────
  📚 citation     a published work           haipipe-plugin-bibex    bibex/
  📮 probe        a question and its card    haipipe-plugin-probe    probe/
🧮 value        one quoted PP<NN>.v<n>     haipipe-plugin-value    the card's ## Values
  🖼 display      a figure or table          haipipe-plugin-display  display/
```

The middle row is the one that trips people, and it tripped JL twice on 260819:
the mark is `value` and the folder is `probe/`, so there is no plugin called
`value` and there should not be one. A probe IS how a value is obtained: you go
to a task folder or a discovery folder and ask. Adding a fourth plugin would be
a second home for one folder, which is exactly why the proof mark was retired.

**A paragraph carries 3 to 6 bullets. Seven is two paragraphs** (JL 260819:
"我们 C2 的话，你这里是只要求一个 paragraph 吗？还是说我们可能写多个 paragraph
会好一些？"). The `### C<n>.P<n> · …` line is a BRIEF, and the tab prints it above
the bullets; eight bullets under one brief means the brief cannot describe them.
Split by IDEA, not by count: `C2` went from one paragraph of eight to three of
three, and the three briefs are what OUTLINE decides, where the Aims are agreed,
and the tick that ends the phase.

**A bullet NEVER carries a markdown heading mark** (JL 260819, twice: "I dont
like '####', could you change it to somehing else?" and "Do not use '##' in the
outline"). Name the part in words or with the § anchor, because `##` and `####`
are the file's own syntax and a reader parses them as structure before they
parse them as a reference:

```text
  ❌ "- B2 · replace #### 2.1, 2.2 and 2.3 with one pointer paragraph"
  ❌ "- B4 · `## Opening` says where this page sits"
  ✅ "- B2 · §4.1, 4.2 and 4.3 collapse to one pointer paragraph"
  ✅ "- B4 · the Opening section says where this page sits"
```

The same rule bans a `## ` line anywhere except a `## C<n> ·` division heading
and the file's own trailing sections. The tab counts divisions by position, so
a stray `## ` in a preamble became a phantom C1 and shifted every address below
it by two (found 260818 by driving the parser, fixed in `live/outline.py` by
matching `^## C\d+` and nothing else).

**A bullet with NO mark is the normal case, not a defect** (JL 260817). Requiring a tag on every line made the plan unreadable and buried the few lines that actually owed something. A mark is the EXCEPTION: it is written only where that point needs evidence, and it sits at the END of the bullet, because that is where the card will hang on the real sentence.

## ⚙️ Writer · nobody, including no model

There is no author. The division tie is read from the material, two grammars deep, and **no model is called at render time** (JL 260816: "我不想每一次都靠一个 code 去做这件事" — I don't want to depend on a code run every time).

```text
① the A-grammar     `### A3` group and id `A3.1` already carry division 3.
                    `P1` says page-wide and means it. Nothing to add.
② the §N anchor     a loose checkbox aim, a State line, or a Files row may
                    write `§2` to name division 2. A Files row may carry
                    several. UNANCHORED IS LEGAL and means 🌐 page-wide.
```

`POST /_board/outline` exists only so the shell's `tab: {url, write}` contract holds; it writes nothing.

## 📡 Surface · one parse, two lenses

`GET /_board/outline?path=<board>&file=<page>` (`live/outline.py`), drawer `assets/js/10-drawer/07-plugin-outline.js`, sorted `07-` so it sits right after 📂 in the rail.

```text
🧭 By division    one card per `### N ·`, with its aims, ticks, and state receipts
🚦 By progress    the same data sorted again, ⬜ before ✅ ON PURPOSE:
                  opening this lens is asking what the page still owes
🌐 page-wide      the card for everything unanchored — it doubles as the
                  worklist for anchoring the page
```

Both lenses render server-side from one parse and toggle client-side with no second request. A bad anchor renders as a named ❌ rather than vanishing.

## 🃏 The evidence column · what each division still owes

✅ **Shipped 260817** (`live/outline.py`, `plan_card`). The plan card sits above the division cards and joins each bullet to what is on disk, so no page ever needs a sentence about a card's state again:

```text
kind          read from                              the row shows
─────────────────────────────────────────────────────────────────────────────
📚 citation   bibex/<stem>.bib                       key · in bibex/ or not
📮 probe      probe/PP<NN>-<slug>/card.md            id · planned → commissioned
              + whether proof/ holds files             → answered → read 🧑
                                                      🚫 answered, proof/ empty
🖼 display    display/<stem>-DisplayN-<slug>/         id · declared → rendered →
              README.md + assets/ + preview.pdf      accepted, human tick only
```

A division owes a card when its prose cites that card's id. So the join is the CITATION, and it runs both ways, which is what makes the two failure modes visible at a glance:

```text
  🕳 OWED, NOTHING THERE   a division cites `Display2` and no unit folder exists
                           ← the 260817 failure: the sentence WAS the deliverable
  🎈 THERE, UNCITED        a card exists that no division names
                           ← evidence nobody is using, or a citation that got lost
```

Both render as a named row, never as a blank. An empty cell is a status, never a blank, is the same rule the display and probe strips already carry.

**The counts are computed independently, never inferred from each other**, exactly as the two strips do it: a folder existing is not a rendered unit, and a rendered unit is not an accepted one. The card header shows `3 owed · 2 landed · 1 accepted` and never collapses those into one number.

## 🪪 The plan is SKIMMED, so the evidence never outweighs the sentence

The plan is read to find out what a page will cover. Every pixel the evidence
takes is a pixel the sentence does not get, and on 260817 the evidence won:
`📚 Gray2021 in bibex/` rendered as a two-line rounded pill on its own column
and pushed the bullet into half the pane (JL, with a screenshot: "你把这些
outline 都给挤得不知道去哪儿了").

**Four rules, and each one is a thing that went wrong:**

```text
① INLINE, never a column   chips live INSIDE the sentence's own span. As
                           siblings of the row's flex they became columns,
                           stole the text's width, then wrapped themselves.
② a TAG, not a pill        10.5px monospace · nowrap · 4px radius · 0 4px
                           padding. The 14px 999px-radius pill was 22px tall
                           beside a 19px row.
③ the note is a WORD       `in bibex/` → nothing (the colour says it resolves)
                           `no unit declared yet` → `owed`
                           `↩ PP04 serve this bullet · 0 of 1 answered`
                              → `↩ PP04 0/1`
④ never say it twice       a chip is `emoji · id · note`, so a note repeating
                           the id printed `🎯 A4.2 → A4.2`; and the ↩ tag is
                           SUPPRESSED for a card the row already names, since
                           `📮 PP01 answered 1` `↩ PP01 ✓` is one fact twice.
```

🚫 **No emoji inside a tag.** At 10.5px a `⬜` or `📄` renders at full glyph size
and doubles the tag's width; the tag's own dashed border and muted colour
already say "not landed".

**The ↩ tag earns its place in the case the row cannot cover**: the plan is
frozen before the card exists, so the mark is usually BARE, and then the
backlink is the only thing that names the card at all.

**The three levels read apart** (JL 260819, four-preview pick): a division
head is bold at the edge; a paragraph row carries its own `C<n>.P<m>` address
plus a short accent tick in the left gutter; bullets are plain rows. All
addresses share one left-aligned column, so every title starts at the same x.

### The popover panel

A chip in the line, a panel beside it holding the THING itself: the reference as printed, the card's own question, the unit's own claim. Native `<popover>`, no script, so deleting every `<script>` leaves the panel readable as body text. It is a marginal note, not a modal:

```text
                    was            now       measured in Chrome
  ─────────────────────────────────────────────────────────────
  🧮 probe card     512×131 px     339×120   PP01, the longest
  🧮 probe card     512×109 px     339×101   PP03
  📚 citation       367× 86 px     327× 64   Deyo2015
  width             34em/14px      25em/12.5px
```

**A 📚 panel prints `Author et al.`, never the author list.** Six names is what made a citation panel twice a probe panel's height, and the key in the panel's own title bar already carries the first author. BibTeX's `---` prints as an EN dash rather than three raw hyphens.

## ✂️ The bullet itself is CONCISE: a head, then its evidence (260819)

The same skim argument reaches the bullet's own words. JL, on a bullet whose
colon unpacked a whole vocabulary before its mark: "它的核心目的明显就是为了做
一个图…你冒号后面的东西其实都有点喧宾夺主了…越 concise 越好，最好只有几个字说
明你的要点，后面再加上后续的证据。"

```text
  one bullet = HEAD · hidden detail · mark

  HEAD        a terse LABEL or a QUESTION, Capitalized, aim ≤ 10 words
              ("Figure for Whole Workflow Loop" · "What is the number
              of plans passing all four checks?") — JL 260819
  hidden      continuation lines the surface FOLDS behind a click:
   detail       Note: <one concise explanation>   authored at OUTLINE
                Answered: <ids + numbers>         appended by the fold
                Drawn: <what the figure shows>    appended by the fold
                An Answered: line ends in `· recount` when its value
                counts the RUN'S OWN artifacts (receipts, findings, a
                pinned hash) and so drifts as phases append; DRAFT
                re-reads ONLY these cards and trusts the rest as
                written (JL 260820, after QPw00's DRAFT re-read all
                14 folders to find 3 drifts, all self-referential)
              every bullet carries one of these; a head a reader might
              not parse owes its Note
  mark        end-anchored, unchanged grammar, on the LAST line
```

**How the surface folds it (JL 260819: "点击之后能看到…简明扼要的解释…without
'>'"):** the row shows only HEAD + chips and looks exactly like a plain row —
no disclosure marker of any kind, hover is the affordance; clicking the row
unfolds the detail as muted body text, the `Note:`/`More:` label stripped.
Native details element, script-free, and the summary hard-resets every
typography property because the board shell's own drawer styles cascade into
the injected card (one folded bullet rendered as a section heading before the
reset).

**What the head may not carry**: anything that lives behind the bullet's own
mark — the card's question, the unit's claim, a contract's rule. That detail
is one popover away; restating it in the head makes the guest upstage the
host (喧宾夺主) and the plan stops being skimmable. A head that needs more
than one clause of unique detail is usually two points, which is an address
decision, not a licence for a long line.

**Plain, common words, in heads and Notes alike** (JL 260819, on a head reading
`The control rung.`: "你这里用了一些非常奇怪的单词…不要用这样的词了"): the
reader is a weak-English reader, so a rare word fails even when it is apt. A
technical term survives only as the thing's real NAME (`iv-overid`,
Callaway–Sant'Anna), defined at first use; metaphor vocabulary (`rung`) is
rewritten to the plain thing it means (`SPEC`, `control set`, `step`).

## 🧵 What it is for, and what it is NOT

Two jobs, and they are small ones (JL 260817):

```text
  ① a person reads it fast and knows what this page will cover
  ② it says which sentences still owe something, so nothing is
     quietly dropped between the plan and the page
```

🚫 **It is not a controller.** DRAFT drafts every sentence anyway, REVISE revises anyway, CHECK checks anyway. Writing out which phase consumes which mark adds a second copy of the workflow and buys nothing: the marks say what is owed, and the phases do their own jobs.

🔒 **Once approved, a version's PROMISE is never rewritten; the fold's appends are the one exception, and they add, never edit.** A bullet marked 🎯 aim stays 🎯 aim in an approved `v1`, because that is what was intended that day. The fold APPENDS `Answered:`/`Drawn:` detail (and the `📮 PP<NN>` id once a card serves a bullet) into bullets in place — into the working file while `approved:` is ⬜, or into `v<N+1>` after a tick, because a tick belongs to the version it ticked. What is actually on disk is read from the folders. A plan that rewrote its own heads and marks as work landed would always look finished, and the gap between what was promised and what got built would be invisible.

## 🔗 The Evidence Bundle · a derived view, not another folder

The 🧭 surface may show a compact **Evidence Bundle** for each Point. It joins
the frozen address `C<n>.P<n>.B<n>` to the sentence scaffold and to every live
resource that names that address:

```text
C3.P1.B4
  ├─ sentence scaffold   realizes: C3.P1.B4
  ├─ Probe card(s)       serves: C3.P1.B4
  ├─ Bibex key(s)        cited by the point/sentence
  ├─ proof/              owned by the Probe card
  └─ Display unit(s)     serves: C3.P1.B4
      └─ feedback        owner-held `read` / `accepted` / `verified` decision
```

This is a projection, not `<page>/evidence/`. Probe, Bibex, proof, and Display
remain in their own plugin folders; the bundle recomputes their current state
and never edits the approved plan. A human choice such as `selected: Display2`
belongs on the owning Display unit, not in a copied bundle manifest.

The full logical shape and status rules live in
`ref/evidence-bundle.md`. The outline renderer may show only the compact form:
`2 sentences · 2 probes · 1 citation · 1 display · feedback 2 · evidence-ready`.

## 📂 Files

- `../../haipipe-board/live/outline.py`
  The parse and both lenses, the GET route, and `plan_card`: the outline file reader and its join against probe/, display/ and bibex/, plus `_pstate`, which resolves a card's state word through the plugin's own ladder and keeps the three retired words readable.
- `../../haipipe-board/checks/outline.py`
  The standing check for the two promises above.
- `ref/evidence-bundle.md`
  The derived Point-to-sentence/evidence join and its status rules.
- `../../haipipe-board/assets/js/10-drawer/07-plugin-outline.js`
  The drawer registration and the client-side lens toggle.
- `../../../diagrams/BoardSkillBoard-260722/4-QPf-page-folder/QPf12-outline/QPf12-outline.md`
  The design page that ruled the anchor grammar and the two lenses.
- `../../page-workflows/haipipe-page-outline/SKILL.md`
  The PHASE whose deliverable this file is. DRAFT no longer owns the outline.
