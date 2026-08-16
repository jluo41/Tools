# Skill · the page's citations into the skill tree
state: ✅ SETTLED · the list, the index, and the boundary are lived in; the judgment vocabulary was flattened to drag-to-rank on JL's ruling 260816
owner: JL
method: give each page its own ranked skill list, seed it by scanning the page for skill names, and let the person drag the cards so the order itself is the judgment

## Opening
Which skills stand behind a page, and who says which matters most?
The shape is bibex's twin: bibex holds the page's references into the literature, and this holds its references into the skill tree.
The store is the PAGE's own `skill/<stem>.md`, one row per skill, seeded by scanning the page for names it actually writes.
The 🛠 tab is an index of cards over that store, and its center is the ORDER: the person drags a card to its rank, and top means most related.

**What the person gets per card**: the skill's name, version, description, and `last_updated` read from its own SKILL.md; a ⠿ handle to drag the card to its rank; an open-the-skill link; a note when the row carries one; and ✕, which removes the name and keeps it removed.
**What the name does**: the 🛠 tab opens on the card INDEX, clicking a card's name or `open the skill` shows that skill in the SAME frame, and the skill's bar carries ← and → walking this page's skills in ranked order plus ☰ back to the index; the one-tab ruling and the 🔍 retirement are dated in the Log.
**Covered elsewhere**: `QPf1` rules the folder; the roster row is `../../board/haipipe-plugin/ref/roster.md`; the twin whose grammar this adopts is `QPf8` (bibex); `QPf6`'s own list is the first live consumer.

## Diagram
**The list is the truth; three doors work it**: the scan seeds, the person ranks, the view only renders.
```text
  📄 <page>/<stem>.md ── skill NAMES the page writes ──▶ the SCAN
        │                       (word-bounded; /name and path forms count;
        ▼                        only names with a real SKILL.md match)
  🗃 skill/<stem>.md      PRIMARY · one row per skill: `- <name> · note: …`
        ▲                 the ORDER of the rows IS the person's rank
        ▲ refresh only APPENDS at the BOTTOM · a ` · removed` row is the
        │ person's ✕ and is never re-seeded
  three doors, one truth
    ↻ /_board/skill          re-scan · seed-append · re-render the view
    ⠿ /_board/skill-order    the drag: the store keeps exactly the new order
    ✎ /_board/skill-entry    add a name at the TOP, typo-guarded · ✕ remove
                             · ↩ restore · note
        │
        ▼
  🖼 skill/<stem>-skill.html  DERIVED · the card index the 🛠 tab frames
```

## Content
### 1 · The contract
**A MIXED plugin, like bibex**: one primary file a person rules, a derived view a rebuild may replace.
```text
  <page>/skill/
    <stem>.md           🧑 PRIMARY · the page's ranked skill list · committed
                           header says: refresh only APPENDS at the bottom
    <stem>-skill.html   ⚙️ DERIVED · the card index, regenerated freely
  flat page fallback: <board>/skill/ · every plugin's fork
  the row grammar, whole:
    - <name>              a related skill · position in the file = its rank
    - <name> · note: …    the same, with the person's free-text note
    - <name> · removed    the ✕ TOMBSTONE: off the cards, into a quiet fold
                          with ↩ restore, and a refresh never re-seeds it
```
The scan is extract-only in bibex's sense: it lists names the page literally writes, matched word-bounded against the toolkit tree's real SKILL.md folders, so a name is never invented.
A row already in the store is never edited, reordered, or removed by a refresh, and a newly scanned name lands at the BOTTOM, because everything above it is the person's order.

### 2 · The rank
**Why one gesture replaced three concepts**: the first build carried uses/designs relations, an aligned ✓, and drift dates, and JL could not read them back.
```text
  the flattening, 260816
    [designs] [uses] badges     ▶ gone · "what does the design mean?"
    ⬜ ✓ aligned {JL 260815}     ▶ gone · a tick nobody missed
    ⚠ drift date comparison     ▶ gone · with the tick it judged against
    ↑ designs upgrade           ▶ gone · replaced by dragging to the top
    the ORDER of the cards      ▶ the one judgment that remains:
                                  drag a card, the store keeps the order,
                                  top = most related, touched = ranked
```
A vocabulary the owner has to ask about is a defect, not a nuance: the relations and the tick tried to name WHY a skill mattered and WHEN the person agreed, and the drag says both without a word.
The migration preserved every earlier judgment as position: rows the person had marked most related became the top of the order, and the two rows JL ticked on `QPf3` lead that page's list still.

### 3 · The surface
**The 🛠 tab, two depths**: the index of cards, and the skill it opens onto, one frame for both.
```text
  83-plugin-skillmap.js ──POST──▶ /_board/skill ──▶ scan + INDEX view
  tab.url()  names skill/<stem>-skill.html · HEAD hit ▶ frame it
  depth 1 · THE INDEX     one card per skill: ⠿ · name · meta ·
            description · open the skill · ✕ · drag anywhere to rank
  depth 2 · THE SKILL     same frame, /_board/skillview?p&map:
            ← prev · ☰ back to the index · next → (arrow keys too)
            header card + related-skill chips, then ONE fold grammar:
            ▸ 📜 SKILL.md (open) · ▸ 📜 CHANGELOG · ▸ 📚 ref/*.md · ▸ 🗂 rest
  the drag POSTs skill-order and reloads · ✕ and ↩ POST skill-entry ·
  lit-click on the tab ▶ REFRESH, the derived half only
```

## Aims
### A1 · 🗃 The contract
- [x] A1.1 · The store, the scan, and the safe refresh shipped.
      Shipped 260815 and lifecycle-tested on `QPf6`; flattened 260816 to the ranked-list grammar, with old-grammar stores parsing cleanly and migrating on their next write, and all 15 live stores migrated in place.
- [x] A1.2 · One page's list carries a person's own order, not a machine's.
      Done 260815 in the first vocabulary and preserved through the 260816 migration: the rows JL worked on `QPf3` lead that page's list as its top ranks.

### A2 · 🧑 The rank
- [x] A2.1 · The cards, the pen, and the typo guard shipped; the rank became the one judgment.
      Shipped 260815 as relation-badge cards and flattened 260816: the badges, the ✓, and the drift flag came out, and the ⠿ drag with /_board/skill-order went in.
- [x] A2.2 · The first REAL judgment on a list is JL's.
      Done 260815: JL worked two `QPf3` rows through the browser, and the migration carried that judgment forward as those rows' position at the top.

### A3 · 🖼 The surface
- [x] A3.1 · One workbench action round-trips in a real browser.
      Done 260815: JL's clicks landed through the view's own buttons, the POST, and the reload, on the address JL uses.

### P · 🚧 The boundary
- [x] P1 · Discovery treats `skill/` as plugin material and warns on nothing inside it.
      Done by construction: `src/common.py`'s `_in_plugin` boundary makes EVERY non-page subfolder of a folded page invisible to discovery, names `skill/` as its motivating case, and the board builds clean with live skill/ folders on QPf3 and QPf6; a name list would have been the weaker rule.

## States
Every aim closed on lived use, not on tests, and the 260816 flattening supersedes the relation and tick vocabulary the 260815 rounds shipped.
- ✅ A1.1 · Lifecycle-tested 260815 on QPf6; the 260816 migration rewrote all 15 live stores to the ranked-list grammar in place.
- ✅ A1.2 · QPf3's list leads with the rows JL worked 260815, carried into position by the migration.
- ✅ A2.1 · The flattened index is live: ⠿ drag, ✕ with the removed fold, ＋ add-at-top, and no judgment chrome.
- ✅ A2.2 · The first real judgment is JL's, preserved as order.
- ✅ A3.1 · JL's own clicks round-tripped through the view's buttons, the POST, and the reload.
- ✅ P1 · The `_in_plugin` boundary in `src/common.py` covers `skill/` generically and the board builds clean around live skill/ folders.
- The git fate of the DERIVED view follows `QPf6`'s one Decision row; the store itself is committed, like the page bib.

## Law
- ✂️ The scan seeds, the person RANKS (JL 260816: "we just need to show these skills and the user can drag and rank them themselves")
      A scanned name lands at the bottom of the list; the order is the person's judgment, ✕ is the person's removal, and a refresh never edits, reorders, or removes a row it finds.

## Files
### ⚙️ Engines
- `../../board/haipipe-board/live/skillmap.py`
  The three doors whole: the skill index, the scan, the store writer, the drag order, the pen, the card view.
- `../../board/haipipe-board/assets/js/10-drawer/83-plugin-skillmap.js`
  The registry entry whose `tab` spec the shell builds the 🛠 tab from.

### 🧪 Evidence
- `../QPf6-latex/skill/QPf6-latex.md`
  The first live list, migrated 260816: five names in ranked order, the two the page designs from on top.

## Log
- 260816 · [RULE-JL] the judgment vocabulary came out whole (JL: "what does the design mean? I didn't get it? … maybe we don't need to have these concept … we just need to show these skills and the user can drag and rank them themselves"): relations, the aligned ✓, and drift dates left the store and the cards, the order became the one judgment saved by dragging through the new /_board/skill-order, /_board/skill-verify was removed, all 15 live stores migrated in place with the designs-first display order preserved as the initial rank, and the extracted skill moved to 0.2.0 the same hour.
- 260816 · [REVISE-CC] the surface caught up with the night's last ruling (JL: one tab, with the index to go back to): §3 gained the two-depth figure, card INDEX then the skill in the same frame with ← ☰ →, and the Opening's name-click line follows, and the retired 🔍 staging tab left the state line; the tab machinery's removal lives in live/shell.py and the index/card view in live/skillmap.py.
- 260816 0056 · [CHECK-CC] closed on JL's word ("so are we good to close it now?") after verifying every aim on disk: A1.2/A2.2/A3.1 by QPf3's two rows worked from JL's browser, P1 by the generic `_in_plugin` boundary in `src/common.py` plus a clean build around live skill/ folders; the one leftover, QPf6's CC-declared row awaiting JL, is recorded in States rather than holding the page open.
- 260815 2258 · [REVISE-CC] the name-click grew up (JL: "open a new small tab, the whole split should be the skill, like the display split, with ← and →"): the inline lazy iframe of 2240 is retired, the 🛠 card's NAME now posts to the shell, which stages a 🔍 Skill tab framing `/_board/skillview`, and the view itself carries ← → over the page's skills in card order with arrow keys live; standalone workbenches fall back to a browser tab.
- 260815 2240 · [REVISE-CC] two workbench rulings landed (JL: "only keep the most relative ones" · "each skills we can click and show its content"): pruning became a tombstone, so a person's not-relevant survives every refresh with the removed names in a ↩-restorable fold, and the card's NAME began toggling the skill's live bundle view inline as a lazy iframe; my test tombstone was reverted, because pruning is a person's judgment.
- 260815 · [DRAFT-CC] page born with the build (JL ruled the plugin into being the same hour): A1/A2 record what shipped and was route-tested, and the store format and refresh rule are written as the contract; the relation vocabulary and drift rule this draft carried were flattened away 260816.
