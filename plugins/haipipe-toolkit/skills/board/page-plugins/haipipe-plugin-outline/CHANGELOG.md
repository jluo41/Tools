# CHANGELOG · haipipe-plugin-outline

## 0.9.0 — 2026-08-17

Adds the derived Point-addressed Evidence Bundle. The outline surface joins
sentence scaffolds, Probe/Bibex/proof/Display resources, and owner feedback
without creating an `evidence/` copy or mutating the approved plan.

## 0.7.0 — 2026-08-17

**The plan is SKIMMED, so the evidence stops outweighing the sentence** (JL
260817, with a screenshot: "太肥太胖了 … 你把这些 outline 都给挤得不知道去哪儿
了"). 0.6.0 shrank the popover, which was the wrong target: the weight was in
the ROW.

```
                      was                          now
────────────────────────────────────────────────────────────────────────
chip placement        a sibling of .row's flex,    inside the sentence's
                      so each one was a COLUMN     own span, inline
                      that stole the text's width
chip shape            14px, 999px radius, 0 9px    10.5px monospace, 4px
                      → 22px tall, wrapped to      radius, 0 4px, nowrap
                      two lines beside a 19px row  → 17px tall, one line
note text             "Gray2021 in bibex/"         "Gray2021"
                      "no unit declared yet"       "owed"
                      "↩ PP04 serve this bullet    "↩ PP04 0/1"
                       · 0 of 1 answered"
row                   13px, 3px 0 1px padding      12px/1.4, 1px 0
addr column           62px, 600 weight             42px, right-aligned
```

Measured in Chrome at a 660px pane, same page, same 66 rows: document height
2017 → 1807 px, widest tag 143×22 → 124×17 px. The structural half (inline
instead of a flex column) is not in those two numbers, because CSS alone cannot
undo it; the screenshot pair is its evidence.

- 🚫 **No emoji inside a tag.** `⬜` and `📄` render at full glyph size in a
  10.5px tag and double its width. The dashed border and muted colour already
  say "not landed", so `PP01 answered 1📄 ⬜` is now `PP01 answered 1`.
- **A fact is never printed twice on one row.** The ↩ backlink is suppressed
  for a card the row already names as a chip, so `🔢 PP01 answered 1` no longer
  drags `↩ PP01 ✓` behind it. It still fires where it is the only speaker: a
  bare mark, or a bullet with no mark at all, which is the normal case since
  the plan is frozen before the card exists.
- **A plain bullet can now carry a ↩ too.** It used to `continue` before the
  backlink was computed, so a card serving an unmarked sentence showed nowhere.
- `&nbsp;` was written into a string that then went through `_e()`, so the plan
  card's header printed the five literal characters (`0 accepted &nbsp; aim 9`).
  Separators moved into the markup.

## 0.6.0 — 2026-08-17

**The evidence card is sized as a NOTE** (JL 260817: "现在我感觉这个 evidence
card 太大了"). It opens beside a 13px outline row, so a 34em/14px panel with
13/16 padding read as a modal. Measured in Chrome before and after:

```
🔢 PP01   512×131 px  →  339×120        📚 Deyo2015  367×86 px  →  327×64
🔢 PP03   512×109 px  →  339×101        width       34em/14px  →  25em/12.5px
```

- **A citation prints `Author et al.`**, not the author list. Six names is what
  made a 📚 panel twice a 🔢 panel's height, and the key in the panel's own
  title bar already carries the first author. `Dowell2022` went 235 → 144 chars.
- BibTeX's `---` prints as an EN dash, never three raw hyphens and never an
  em dash (JL's standing rule).
- **A chip no longer prints its id twice.** `🎯 A4.2 → A4.2` was visible in the
  260817 screenshot: with an id the note stays empty, and only a bullet with NO
  id spends the note on saying it is untracked.

Also in this pass, and it is the reason the size question got asked at all: the
🧭 join read a card's state through `raised`/`working`/`bound`, three words
`haipipe-plugin-probe` 0.7.0 had retired, so two ANSWERED cards on
`QC1-visitlbp` rendered `⬜ 0 of 1 bound`. The join now resolves through the
protocol's own ladder (`_pstate`), keeps the retired words as aliases, counts a
`read` card toward `accepted`, and prints `all answered` / `2 of 3 answered`.

## 0.5.0 — 2026-08-17

**🧮 proof earns NO folder**, closing the ⬜ this file opened on 260817. The
ruling is `haipipe-page-probe` §🧭's: a proof lands as prose, and the pulled
file a derivation rests on already lives in a probe card's `proof/`, so a
second home for the same material would be one thing filed twice. A 🧮 bullet
carries no id and no card backlinks it.

## 0.4.0 — 2026-08-17

**The PHASE moves out to `page-workflows/haipipe-page-outline`** (0.1.0, same
day). This file kept both the material and the phase's rules while the phase had
no home; now it states neither twice and points at the contract instead. DRAFT's
own §🗂 was trimmed at the same time and no longer owns the outline.

**Each evidence ref opens as the board's own evidence card** (JL 260817: "我想让
它有点像那个 evidence card 一样"). Chip in the line, popover panel beside it,
holding the THING itself as `haipipe-sentence` §🃏 requires: the reference as
printed, the probe card's own question, the display unit's own claim.

- Native `popover`, no script: deleting every `<script>` must leave the panel
  readable, and it is real body text rather than a `title=` attribute.
- The class is `.evchip`, NOT `.chip`: the lens toggle buttons already own
  `.chip` on this page, and reusing it made the two fight (found by driving it).
- Two parser bugs fixed the same way: BibTeX `{CDC}` protects capitalisation and
  is not part of the title, and a README `claim` wraps onto the next line.

## 0.3.1 — 2026-08-17

**📚 means a published work, never a sibling board page** (JL 260817 asked
whether C1 should have citations and why there were so few). It had NONE: the
page's `bibex/QC1-visitlbp.bib` held zero entries, and the three 📚 marks in its
plan pointed at `QB1`, `QB2`, `QB3`, which are board pages.

- `_disk_state` now reads `bibex/*.bib`, so a 📚 is checkable like 🔢 and 🖼:
  `in bibex/` · `🚨 not in bibex/` · `🚨 <id> is a board page, not a citation`.
- A cross-reference to a sibling page is a different act from a citation and is
  written in the bullet's own words, without the mark.

## 0.3.0 — 2026-08-17

**A bullet is a POINT, not a sentence** (JL 260817: "一个 bullet point 我们可能有几个 sentences 去 cover，所以我感觉可能还是 B 比较好"). The proof was in the plan's own text: one bullet listed six OLS specification families, which is plainly several sentences, not one.

- The address is `C<n>.P<n>.B<n>`. One `B` becomes 1..n `S` at REVISE, and
  `C<n>.P<n>` is shared with the sentence address so the link survives.
- `haipipe-sentence` keeps `S` on the rendered page. Neither redefines the other.
- `C` STAYS and is not decoration (JL asked why): Aims use `A` and page-wide uses
  `P` in that same slot, so dropping it would collide `C1` with `A1`. It prints
  ONCE on the section heading; the rows carry only `P<n>.B<n>`, the part that
  changes.

**A bullet with no mark is the normal case, not a defect.** 0.2.0 required a mark
on every line and flagged bare ones 🕳. That made the plan unreadable and buried
the few lines that actually owed something. A mark is now the exception, written
at the END of a bullet, because that is where the card will hang on the real
sentence.

**THE PAGE NOW folds shut** (JL 260817: "第二部分还有必要要吗？我感觉有点
confusing"). The tab shows two halves answering two different questions, and
neither was labelled: 🧭 THE PLAN, what the page said it would cover, and
📄 THE PAGE NOW, what is written today. Both are labelled now and the second
collapses to one line, since on a page whose aims carry no ids it was nine empty
cards in the reader's way.

- Empty-division wording fixed: "nothing lands here yet" read as "this part is
  fine". It now says "no aim, state or file on this page names this part", which
  is the actual reason.

## 0.1.0 — 2026-08-16

First contract for a plugin that had already SHIPPED without one.

- The engine, checker, and drawer JS landed in commit `711b964c` ("Ship the
  pagex and outline plugins"), and QPf12's own state line recorded the gap:
  `open: marks on old pages, plugin skill`. Without a SKILL.md no agent could
  discover the surface or knew what `§N` meant, so pages kept being written
  with every aim unanchored.
- Records the four facets as built: storage NONE (live, storage-less, the QPf1
  folderstat precedent), writer NOBODY (rule-based, no model call at render
  time), surface `GET /_board/outline` with the 🧭 By division and 🚦 By
  progress lenses, boundary deliberately OFF the plugin roster as a meta-surface
  twinned with 📂 folder.
- Adds the DRAFT link (JL 260816, "is that before the draft, we should also have
  a outline for this page as well?"): this tab is WHERE a DRAFT outline is read
  and approved. DRAFT writes the material — divisions, `### A<n>` groups, `§N`
  anchors — and the surface reads it back. No outline phase and no outline file:
  a fifth phase would only take DRAFT's authority over what divisions exist.
- States the one-click test: a page whose 🧭 tab is one big 🌐 card has no plan
  yet, only prose.
