# Probe · a page's evidence questions, asked once and cited by id
state: 🟡 PARTIAL · the plugin is ruled and the card grammar is adopted; the landing address, the citation hop, and the tab are open aims
owner: JL
method: give every page its own `probe/` pool with the PPNN card grammar kept whole, retire the paper's `1-probes/`, point the orchestrators at the page as the only landing address, and let every consumer cite the card by id

## Opening
Where does a page ask its evidence questions?
In its own `probe/` folder, and nowhere else: there is no `1-probes/` pool any more.
A probe is one evidence question with a state and, once answered, a binding to the bank's QA file.
A paper used to pool these questions in `1-probes/`, one folder far from the sentences that needed them; now a paper's stages are pages, and each page asks for itself.
This page owns the plugin that replaces the pool: the card, its states, its citers, and its tab.

**What a card is**: one folder per question, such as `probe/PP01-drift-rate/`, holding the question in the page's own words, a `state:` line, and the binding the orchestrator fills.
**What the bank is**: the shared task and discovery layers that answer questions in general language, landing each answer in a `<task-folder>/QA/<n>-<slug>.md` file with its data artifact.
**What retires**: the paper-level `1-probes/` pool, ruled in this page's Law; the PPNN grammar survives on the cards, the numbering runs per page, and the paper family's probe skills must relearn their landing address, which A1.2 tracks.
**Covered elsewhere**: `QPf1` rules that a page owns its folder and every subfolder is a plugin; `QPf5` is the display plugin whose `intake/` cites a card by id, and its Law carries the 260815 ruling that births this page.

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
### 1 · The card, and the pool it retires
**The card's shape**: the PPNN grammar kept whole, at its one address.
```text
  <page>/probe/PP<NN>-<slug>/
    card.md
      question    in the page's own words, stake included
      state:      raised → working → bound
      binding:    → <task-folder>/QA/<n>-<slug>.md   filled when answered
```
The grammar is the shape the retired `1-probes/PPNN` pool taught the orchestrators, taken whole so they speak it without relearning anything.
What retires is the address, not the grammar: there is no paper-level pool, the pool is each page's own `probe/` folder, and `PP` numbers run per page.
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
This page walks its own rule with three live cards in its own `probe/` folder, and the sentences that need their answers cite the ids instead of restating the questions.
PP01 asks the migration's census and PP02 the orchestrators' landing constraint; both stay raised with empty bindings until the bank answers, because a machine-owed binding written by hand is the fake this plugin exists to prevent.
PP03 asks the family's own skill count and is bound: the loop walked end to end as a SPECIMEN, its answer landed in this page's `_fixture/QA/` in the bank's QA shape, and the binding says where.
The specimen proves the shape and not A1.1, whose test is the collector's hand writing the path, not a person's.

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
**The tab**: the display split's structure, carrying cards instead of units.
```text
  right pane · 🚪 Probe
    PP01 · PP02 · PP03                 ← the chip row, one per card
    ┌────────────────────────────────────────┐
    │ ✅ PP01-drift-rate                      │
    │ the question, in the page's own words  │
    │ binding: → tasks/T12/QA/3-drift.md     │
    │ the card folder's tree                 │
    └────────────────────────────────────────┘
      ◀ one card fills the pane · shift right for the next ▶
    a citing chip lands on #PP<NN> · the tab writes NOTHING
```
The structure is the display split's, taken whole: a horizontal strip of blocks, one per card, a chip row naming every id, and per-card anchors so a citation lands on the card it names.
The filling is probe's own: the state badge, the question, the binding, and the card folder's tree.
The tab is still the Slides sandwich: a drawer plugin asks a `live/` endpoint, the endpoint globs the page's `probe/`, and each block renders from the card's own state line.
It writes nothing, because every state transition already has an owner in §3.

## Aims
### A1 · 🧾 The card, and the pool it retires
- A1.1 · The orchestrators land in a page's `probe/`, and nowhere else.
  **Done when:** a question raised on this page's own card comes back bound, with the QA path written by the collector and not by hand.
- A1.2 · The paper family retires `1-probes/`.
  **Done when:** no probe skill or orchestrator names `1-probes/` as a landing address, and a paper's stage pages ask through their own `probe/` folders.

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
- 🔨 A1.2 · `haipipe-probe`, the paper probe skills, and the orchestrator agents all still speak `1-probes/`; the retirement is ruled here, its census is asked as this page's own PP01, and the landing constraint as PP02, both raised and unanswered.
- ⬜ A2.1 · `manifest.yaml` has no `probe:` line yet; `QPf5` A1 shares this seam.
- 🔨 A4.1 · `plugview.py` and the drawer row exist, the strip structure landed 260816, and the page's three cards render in it, ⬜ PP01 ⬜ PP02 ✅ PP03 with its binding shown; the real-browser check waits on a server restart.
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

## Law
- 260816 JL · 🚪 There is no `1-probes/`: a page's `probe/` is the only pool
      Every evidence question lives on the page that needs it, at `<page>/probe/PP<NN>-<slug>/card.md`; the paper-level pool retires, because a paper's stages are pages and a second home would give one question two addresses.
      JL's words: "we will have no 1-probes... The opening is totally wrong."
      Rejected: keeping `1-probes/` beside the plugin for consumers that are not pages, because once stages are pages every asker IS a page, and the mirror framing made the pool look permanent.

## Log
- 260816 · [BUILD-CC] PP03 walked the whole loop (JL: "you can probe yourself, like for this skill set... how many skills you have"): the board family's own census asked as PP03-skill-census, answered 24 skills in four tiers into `_fixture/QA/1-board-skill-census.md` in the bank's QA shape, and bound; marked SPECIMEN on both files because the session answered it, not the bank, so A1.1 stays open on its own terms.
- 260816 · [BUILD-CC] the page became its own specimen (JL: "create the fake probe and reference and cite it to make it really work"): PP01-pool-census and PP02-landing-address raised in this page's own `probe/`, both genuine questions A1 owes the bank, cited from §2 and from the A1.2 and A4.1 state rows; the bindings stay empty until the bank answers, because a hand-written binding is the fake the plugin exists to prevent. The same hour JL named attribution parentheticals in prose jargon, so the dates moved to Law and Log and the rule landed in `writing-rules.md`.
- 260816 · [RULE-JL] the pool retires: the page had framed `probe/` as a MIRROR of the paper's `1-probes/`, and JL ruled the reverse, the REPLACEMENT; the Opening, method, §1, and A1 were rewritten from mirror-of-the-pool to the-only-pool, and A1.2 opened to carry the paper family's migration off `1-probes/`.
- 260816 · [BUILD-CC] the tab took the display split's structure (JL: "follow the structure of the display plugin split"): `plug_probe` rebuilt on the strip, one card filling the pane, a chip row of ids, per-card anchors; §4 redrawn to match.
- 260815 1900 · [JL via CC] `haipipe-plugin-probe` drafted under `page-plugins/`, round 2 of the thin-door migration: delta-only over `haipipe-plugin`.
- 260815 · [DRAFT-CC] page born from JL's ruling on `QPf5`: a page is a small paper, so `probe/` mirrors `1-probes/` beside `display/`; the card grammar adopted whole, the one-home citation rule written, and the landing address, the citation hop, and the tab opened as aims.
