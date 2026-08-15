# The skill plugin: the page's citations into the skill tree
state: 🟡 PARTIAL · the store, the workbench, and its three doors shipped; the first human tick and the boundary are open
owner: JL
method: give each page its own skill map, seed it by scanning the page for skill names, and work it through cards that show drift, take a person's aligned ✓, and land a person's declared relations

## Opening
Which skills does a page lean on, and which skills are designed from what it rules?
The shape is bibex's twin: bibex holds the page's references into the literature, and this holds its references into the skill tree.
The store is the PAGE's own `skill/<stem>.md`, one row per skill, seeded by scanning the page for names it actually writes.
The 🛠 tab is a workbench over that store, and its center is DRIFT: the skill's `last_updated` beside the page's newest Log date beside a person's dated ✓.

**What the person gets per card**: the skill's name, version, description, and `last_updated` read from its own SKILL.md; the relation badge; an open-SKILL.md link; ⬜ with a ✓-aligned button, or ✅ with who and when; a ⚠ drift flag the moment the skill moves past the tick; and ↑ designs to upgrade a scanned row.
**Covered elsewhere**: `QPf1` rules the folder; the roster row is `../../board/haipipe-page-plugin/ref/roster.md`; the twin whose grammar this adopts wholesale is `QPf8` (bibex); `QPf6`'s own map is the first live consumer.

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
  relations, exactly two:
    uses     this page leans on that skill's behavior · the scan may claim it
    designs  this page RULES part of that skill's contract · a person's word
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
**The 🛠 tab**: the bibex sandwich, with the view carrying its own controls.
```text
  83-plugin-skillmap.js ──POST──▶ /_board/skill ──▶ scan + view
  tab.url()  names skill/<stem>-skill.html · HEAD hit ▶ frame it
  the view's buttons POST skill-verify / skill-entry themselves and
  reload · lit-click on the tab ▶ REFRESH, the derived half only
```

## Aims
### A1 · 🗃 The contract
- [x] A1.1 · The store, the scan, and the safe refresh shipped.
      Shipped 260815 and lifecycle-tested on `QPf6`: the scan seeded four real relations, a person-pen'd `designs` row survived a re-refresh untouched, and the typo guard refused a name with no SKILL.md.
- [ ] A1.2 · One page's map earns a `designs` row from a person, not a test.
      **Done when:** a page carries a designs relation a person declared or confirmed, with the demo declarations reverted or re-affirmed.

### A2 · 🧑 Drift, the card's center
- [x] A2.1 · The cards, drift dates, tick, undo, pen, and typo guard shipped.
      Shipped 260815 and screenshot-verified: four cards with version, description, relation badge, ↑ designs, ✓ aligned, and the ＋ form.
- [ ] A2.2 · The first REAL aligned ✓ is JL's.
      **Done when:** a row carries `aligned: {JL …}` because JL read the page and the SKILL.md and clicked ✓; the build round's test tick was reverted for exactly this reason.

### A3 · 🖼 The surface
- [ ] A3.1 · One workbench action round-trips in a real browser.
      **Done when:** a ✓ or a declared relation lands through the view's own button, the POST, and the reload, on the address JL uses.

### P · 🚧 The boundary
- [ ] P1 · `skill/` joins the checker's known-plugin list.
      **Done when:** `check.py` names `skill/` a known plugin folder and warns on nothing inside it.

## States
The store and workbench are built and route-tested; what remains is lived use.
- ✅ A1.1 · Lifecycle-tested 260815 on QPf6: seed, preserve-on-refresh, typo guard.
- ⬜ A1.2 · QPf6's `designs: haipipe-page-plugin` row is CC's declaration from the build round; it awaits JL's word or reversal.
- ✅ A2.1 · View screenshot-verified 260815 with QPf6's four real cards.
- ⬜ A2.2 · Every tick written so far was a test's and has been reverted.
- ⬜ A3.1 · The routes are live-tested; the view's own buttons await a browser round-trip after the next server restart.
- ⬜ P1 · `check.py` does not yet know `skill/` by name.
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
- 260815 · [DRAFT-CC] page born with the build (JL ruled the plugin into being the same hour): A1/A2 record what shipped and was route-tested, A1.2/A2.2 hold the person's half, and the store format, the two-relation vocabulary, and the drift rule are written as the contract.
