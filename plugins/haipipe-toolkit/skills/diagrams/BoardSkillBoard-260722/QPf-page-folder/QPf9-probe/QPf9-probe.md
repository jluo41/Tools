# Probe · a page's evidence questions, asked once and cited by id
state: 🟡 PARTIAL · the plugin is ruled and the card grammar is adopted; the landing address, the citation hop, and the tab are open aims
owner: JL
method: mirror the paper's `1-probes/` at `<page>/probe/` with the PPNN card grammar unchanged, give the orchestrators the page as a landing address, and let every consumer cite the card by id

## Opening
Where does a page ask its evidence questions, now that a page is a small paper?
A probe is one evidence question with a state and, once answered, a binding to the bank's QA file.
A paper keeps its probes in `1-probes/`; a page had no such place.
So a display bound its own answers and a sentence in Content had nowhere to ask at all.
JL ruled the page is a small paper, so `probe/` joins the roster beside `display/`.
This page owns that folder: the card, its states, its citers, and its tab.

**What a card is**: one folder per question, such as `probe/PP01-drift-rate/`, holding the question in the page's own words, a `state:` line, and the binding the orchestrator fills.
**What the bank is**: the shared task and discovery layers that answer questions in general language, landing each answer in a `<task-folder>/QA/<n>-<slug>.md` file with its data artifact.
**Covered elsewhere**: `QPf1` rules that a page owns its folder and every subfolder is a plugin; `QPf5` is the display plugin whose `intake/` cites a card by id, and its Law carries the 260815 ruling that births this page; the paper's `1-probes/` pool keeps working unchanged for consumers that are not pages.

## Diagram
**Two plugins, one binding**: the probe owns the ask, the display cites it, the bank stays behind the wall.
```text
  <page>/
    probe/PP01-drift-rate/          🚪 THE ASK, once
      card.md   question · state: raised → working → bound
                binding: → tasks/T12/QA/3-drift.md
        ▲ cite by id          ▲ cite by id
    display/<unit>/intake/    <page>.md, a Content claim
      manifest.yaml            "…17.3% (PP01)"
      probe: PP01
  ──────────────────────────────────────────────────────────
  🧪 the BANK  tasks/ · discoveries/  answers in general language
     the stake stays in the card; the QA file never sees it
```

## Content
### 1 · The card, adopted from the paper's pool
**The card's shape**: the PPNN grammar unchanged, at a new address.
```text
  <page>/probe/PP<NN>-<slug>/
    card.md
      question    in the page's own words, stake included
      state:      raised → working → bound
      binding:    → <task-folder>/QA/<n>-<slug>.md   filled when answered
```
The grammar is the paper's `1-probes/PPNN` shape taken whole, so the probe orchestrator and its collector speak it without relearning anything.
The only change is the address: the pool is the page's own `probe/` folder, and `PP` numbers run per page.
A card is small on purpose: the probe layer is communication, not judgment, so the card carries a question, a state, and a binding, and no review gate.

### 2 · Ask once, cite twice
**The one-home rule**: the binding lives in the card, and every consumer points at the card.
```text
  🚪 probe/PP01/card.md      the ONLY place the binding is written
        ▲                          ▲
  📥 intake/manifest.yaml    📋 a Content sentence
     probe: PP01                cites PP01 beside its number
```
Before this plugin, a display unit's manifest bound the answer itself, so a second consumer of the same number would have duplicated the binding.
Now the manifest names the card and the card names the holder, one hop each.
A citer never copies the binding, so a re-answered question changes one file and every citer follows.

### 3 · The states, and who moves each one
**Three states, three hands**: the consumer asks, the orchestrator claims, the collector binds.
```text
  ⬜ raised    🧑/📄 the consumer writes the card: the question, no binding
  🔨 working   🚪 the orchestrator claims it before the lifecycle runs
  ✅ bound     🚪 the collector writes the binding when the QA file lands
```
A `working` card means someone is already on it: a second session reads the state line and waits rather than re-running the bank.
The stake never crosses the wall: the card holds why the page needs the number, and the question reaches the bank stripped to general language.
A card may also close negative: a bank answer of "not supported" is still a binding, and the citing claim inherits that verdict rather than hiding it.

### 4 · The surface: the probe tab
**The tab**: the page's open questions at a glance, read-only.
```text
  right pane · 🚪 Probe
    ┌────────────────────────────────────────┐
    │ ⬜ PP02 band sizes, controlled?         │
    │ 🔨 PP03 external validity sweep         │
    │ ✅ PP01 drift rate per band → QA/3      │
    └────────────────────────────────────────┘
    one row per card · states from the state: lines
    ✅ rows link their QA file · the tab writes NOTHING
```
The tab is the Slides sandwich again: a drawer plugin asks a `live/` endpoint, the endpoint globs the page's `probe/`, and the rows render from the cards' own state lines.
It writes nothing, because every state transition already has an owner in §3.

## Aims
### A1 · 🧾 The card, adopted from the paper's pool
- A1.1 · The orchestrators accept a page's `probe/` as a landing address.
  **Done when:** a question raised on this page's own card comes back bound, with the QA path written by the collector and not by hand.

### A2 · 🔗 Ask once, cite twice
- A2.1 · An intake manifest resolves a card by id.
  **Done when:** a `QPf5` unit's `manifest.yaml` says `probe: PP<NN>` and the build resolves card and binding to the holder without a path anywhere.

### A4 · 🚪 The surface: the probe tab
- A4.1 · The tab ships through the Slides sandwich.
  **Done when:** a page with one card shows 🚪 Probe in the right pane with the card's real state, verified in a real browser.

### P · 🚧 The boundary
- P1 · `probe/` joins the plugin exclusion.
  **Done when:** discovery never lists a file under any page's `probe/` and `check.py` names `probe/` a known plugin folder.

## States
The ruling and the card grammar are the settled half; nothing that moves a card is built yet.
- ⬜ A1.1 · The orchestrators land only in a paper's `1-probes/` today.
- ⬜ A2.1 · `manifest.yaml` has no `probe:` line yet; `QPf5` A1 shares this seam.
- ⬜ A4.1 · No drawer plugin and no `live/` endpoint exist for probe.
- ⬜ P1 · Discovery's exclusion list does not know `probe/` by name.

## Files
### ⚙️ Engines
- `../../board/haipipe-board/live/deck.py`
  The Slides endpoint A4 copies; the probe endpoint sits beside it.
- `../../board/haipipe-board/assets/js/10-drawer/70-plugin-slides.js`
  The drawer plugin A4 copies for its client half.

### 📋 Contracts
- `QPf-page-folder/QPf5-display/QPf5-display.md`
  The display plugin whose `intake/` is this plugin's first citer; its Law carries the birth ruling.

### 🧪 Checks
- `../../board/haipipe-board/cli/check.py`
  Where P1's exclusion and the plugin-folder validation land.

## Log
- 260815 · [DRAFT-CC] page born from JL's ruling on `QPf5`: a page is a small paper, so `probe/` mirrors `1-probes/` beside `display/`; the card grammar adopted whole, the one-home citation rule written, and the landing address, the citation hop, and the tab opened as aims.
