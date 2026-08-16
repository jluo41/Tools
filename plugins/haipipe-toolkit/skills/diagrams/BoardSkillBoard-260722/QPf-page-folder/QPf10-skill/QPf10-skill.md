# Skill · the page's citations into the skill tree
state: ✅ SETTLED · the map, the workbench, and the boundary are lived in; JL's own ticks landed through the browser and the page closed 260816
owner: JL
method: give each page its own skill map, seed it by scanning the page for skill names, and work it through cards that show drift, take a person's aligned ✓, and land a person's declared relations
session: 368050b2-ca7a-4229-a0dc-9745de6a0086

## Opening
Which skills does a page lean on, and which skills are designed from what it rules?
The shape is bibex's twin: bibex holds the page's references into the literature, and this holds its references into the skill tree.
The store is the PAGE's own `skill/<stem>.md`, one row per skill, seeded by scanning the page for names it actually writes.
The 🛠 tab is a workbench over that store, and its center is DRIFT: the skill's `last_updated` beside the page's newest Log date beside a person's dated ✓.

**What the person gets per card**: the skill's name, version, description, and `last_updated` read from its own SKILL.md; the relation badge; an open-SKILL.md link; ⬜ with a ✓-aligned button, or ✅ with who and when; a ⚠ drift flag the moment the skill moves past the tick; and ↑ designs to upgrade a scanned row.
**What the name does**: the 🛠 tab opens on the card INDEX, clicking a card's name or `open the skill` shows that skill in the SAME frame, and the skill's bar carries ← and → walking this page's skills in card order plus ☰ back to the index; the one-tab ruling and the 🔍 retirement are dated in the Log.
**Covered elsewhere**: `QPf1` rules the folder; the roster row is `../../board/haipipe-plugin/ref/roster.md`; the twin whose grammar this adopts wholesale is `QPf8` (bibex); `QPf6`'s own map is the first live consumer.

## Diagram
**The map is the truth; three doors work it**: the scan seeds, a person ticks and declares, the view only renders.
```text
  📄 <page>/<stem>.md ── skill NAMES the page writes ──▶ the SCAN
        │                       (word-bounded; /name and path forms count;
        ▼                        only names with a real SKILL.md match)
  🗃 skill/<stem>.md      PRIMARY · one row per skill:
        ▲                 - <name> · relation: uses|designs
        ▲ refresh only      · aligned: {JL 260815} · note: …
        │ APPENDS, never removes or edits a row a person holds
        │
  three doors, one truth
    ↻ /_board/skill          re-scan · seed-append · re-render the view
    ✓ /_board/skill-verify   writes aligned = {WHO YYMMDD} onto the row
    ✎ /_board/skill-entry    lands a PERSON's declared relation; refuses a
                             name with no SKILL.md behind it (typo guard)
        │
        ▼
  🖼 skill/<stem>-skill.html  DERIVED · the card view the 🛠 tab frames
```

## Content
### 1 · The contract
**A MIXED plugin, like bibex**: one primary file a person rules, a derived view a rebuild may replace.
```text
  <page>/skill/
    <stem>.md           🧑 PRIMARY · the page's skill map · committed
                           header says: refresh only APPENDS
    <stem>-skill.html   ⚙️ DERIVED · the workbench view, regenerated freely
  flat page fallback: <board>/skill/ · every plugin's fork
  relations, exactly three:
    uses     this page leans on that skill's behavior · the scan may claim it
    designs  this page RULES part of that skill's contract · a person's word
    ignored  a person's "not relevant" TOMBSTONE: off the cards, into a quiet
             fold with ↩ restore, and a refresh can never re-seed the name
```
The scan is extract-only in bibex's sense: it lists names the page literally writes, matched word-bounded against the toolkit tree's real SKILL.md folders, so a relation is never invented.
A row already in the store is never overwritten or removed by a refresh, because a person may have upgraded it.

### 2 · Drift, the card's center
**Why this plugin earns its place**: a page rules, a skill implements, and then one moves without the other.
```text
  the card puts three dates side by side
    skill last_updated   from the skill's own frontmatter
    page last moved      the newest stamp in this page's ## Log
    aligned {JL 260815}  the person's dated judgment
  skill moves past the tick ▶ ⚠ drifted flag · the tick STAYS, flagged,
  because a recorded judgment is history, not something a machine unsays
```
The ✓ means "I read both and they agree", which no machine may claim; the demo ticks of the build round were reverted for exactly that reason, matching `QPf8`'s rule.

### 3 · The surface
**The 🛠 tab, two depths**: the index of cards, and the skill it opens onto, one frame for both.
```text
  83-plugin-skillmap.js ──POST──▶ /_board/skill ──▶ scan + INDEX view
  tab.url()  names skill/<stem>-skill.html · HEAD hit ▶ frame it
  depth 1 · THE INDEX     one card per skill: name · relation · meta ·
            description · ✓ aligned / undo · ↑ designs · ✕ · open the skill
  depth 2 · THE SKILL     same frame, /_board/skillview?p&map:
            ← prev · ☰ back to the index · next → (arrow keys too)
            header card + related-skill chips, then ONE fold grammar:
            ▸ 📜 SKILL.md (open) · ▸ 📜 CHANGELOG · ▸ 📚 ref/*.md · ▸ 🗂 rest
  the view's buttons POST skill-verify / skill-entry themselves and
  reload · lit-click on the tab ▶ REFRESH, the derived half only
```

## Aims
### A1 · 🗃 The contract
- [x] A1.1 · The store, the scan, and the safe refresh shipped.
      Shipped 260815 and lifecycle-tested on `QPf6`: the scan seeded four real relations, a person-pen'd `designs` row survived a re-refresh untouched, and the typo guard refused a name with no SKILL.md.
- [x] A1.2 · One page's map earns a `designs` row from a person, not a test.
      Done 260815: QPf3's map carries `haipipe-plugin` and `haipipe-plugin-slide` as designs, upgraded and ticked by JL through the workbench.

### A2 · 🧑 Drift, the card's center
- [x] A2.1 · The cards, drift dates, tick, undo, pen, and typo guard shipped.
      Shipped 260815 and screenshot-verified: four cards with version, description, relation badge, ↑ designs, ✓ aligned, and the ＋ form.
- [x] A2.2 · The first REAL aligned ✓ is JL's.
      Done 260815: two QPf3 rows carry `aligned: {JL 260815}` because JL clicked ✓ in the browser; the build round's test tick had been reverted so these are the first real ones.

### A3 · 🖼 The surface
- [x] A3.1 · One workbench action round-trips in a real browser.
      Done 260815: JL's ↑ designs upgrade and both ✓ ticks landed through the view's own buttons, the POST, and the reload, on the address JL uses.

### P · 🚧 The boundary
- [x] P1 · Discovery treats `skill/` as plugin material and warns on nothing inside it.
      Done by construction: `src/common.py`'s `_in_plugin` boundary makes EVERY non-page subfolder of a folded page invisible to discovery, names `skill/` as its motivating case, and the board builds clean with live skill/ folders on QPf3 and QPf6; a name list would have been the weaker rule.

## States
Every aim closed on lived use, not on tests.
- ✅ A1.1 · Lifecycle-tested 260815 on QPf6: seed, preserve-on-refresh, typo guard.
- ✅ A1.2 · QPf3's two designs rows are JL's, upgraded and ticked through the workbench 260815.
- ✅ A2.1 · View screenshot-verified 260815 with QPf6's four real cards.
- ✅ A2.2 · The first real ✓ ticks are JL's, on QPf3's `haipipe-plugin` and `haipipe-plugin-slide` rows.
- ✅ A3.1 · JL's own clicks round-tripped through the view's buttons, the POST, and the reload.
- ✅ P1 · The `_in_plugin` boundary in `src/common.py` covers `skill/` generically and the board builds clean around live skill/ folders.
- QPf6's `designs: haipipe-plugin` row remains CC's declaration from the build round; the map preserves it and JL may tick or ignore it in passing.
- The git fate of the DERIVED view follows `QPf6`'s one Decision row; the store itself is committed, like the page bib.

## Law
- ✂️ The scan seeds, the person declares (JL 260815: "showing what skills is related to this page, or is designed based on the content of this page")
      A scanned row claims `uses` at most; `designs` and the aligned ✓ are a person's words, and a refresh never edits or removes a row it finds.

## Files
### ⚙️ Engines
- `../../board/haipipe-board/live/skillmap.py`
  The three doors whole: the skill index, the scan, the store writer, the tick, the pen, the card view.
- `../../board/haipipe-board/assets/js/10-drawer/83-plugin-skillmap.js`
  The registry entry whose `tab` spec the shell builds the 🛠 tab from.

### 🧪 Evidence
- `../QPf6-latex/skill/QPf6-latex.md`
  The first live map, 260815: three scanned `uses` rows beside one declared `designs`.

## Log
- 260816 · [REVISE-CC] the surface caught up with the night's last ruling (JL: one tab, with the index to go back to): §3 gained the two-depth figure, card INDEX then the skill in the same frame with ← ☰ →, and the Opening's name-click line follows, and the retired 🔍 staging tab left the state line; the tab machinery's removal lives in live/shell.py and the index/card view in live/skillmap.py.
- 260816 0056 · [CHECK-CC] closed on JL's word ("so are we good to close it now?") after verifying every aim on disk: A1.2/A2.2/A3.1 by QPf3's two designs rows with `aligned: {JL 260815}` ticks that landed from JL's browser, P1 by the generic `_in_plugin` boundary in `src/common.py` plus a clean build around live skill/ folders; the one leftover, QPf6's CC-declared designs row awaiting its own tick, is recorded in States rather than holding the page open.
- 260815 2258 · [REVISE-CC] the name-click grew up (JL: "open a new small tab, the whole split should be the skill, like the display split, with ← and →"): the inline lazy iframe of 2240 is retired, the 🛠 card's NAME now posts to the shell, which stages a 🔍 Skill tab framing `/_board/skillview`, and the view itself carries ← → over the page's skills in card order (designs first) with arrow keys live; standalone workbenches fall back to a browser tab.
- 260815 2240 · [REVISE-CC] two workbench rulings landed (JL: "only keep the most relative ones" · "each skills we can click and show its content"): pruning became the `ignored` tombstone relation, so a person's not-relevant survives every refresh, cards sort designs before uses with tombstones in a ↩-restorable fold, and the card's NAME now toggles the skill's live bundle view inline as a lazy iframe; my test tombstone was reverted, because pruning is a person's judgment.
- 260815 · [DRAFT-CC] page born with the build (JL ruled the plugin into being the same hour): A1/A2 record what shipped and was route-tested, A1.2/A2.2 hold the person's half, and the store format, the two-relation vocabulary, and the drift rule are written as the contract.
