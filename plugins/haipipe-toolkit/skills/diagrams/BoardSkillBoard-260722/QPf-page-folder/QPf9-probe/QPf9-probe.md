# Probe · a page's evidence questions, asked once and cited by id
state: 🟡 PARTIAL · ruled, cards bound · open: 1-probes retirement, citation hop, tab, exclusion
owner: JL
method: give every page its own `probe/` pool with the PPNN card grammar kept whole, retire the paper's `1-probes/`, make the page the one address a probe run lands in, and let every consumer cite the card by id

## Opening
Where does a page ask its evidence questions?
In its own `probe/` folder: the `1-probes/` pool is ruled retired, and moving the orchestrators to the new address is A1.2's open work.
A probe is one evidence question with a state and, once answered, a binding to the bank's QA file.
A paper used to pool them far from the sentences that needed them; now a paper's stages are pages, so each page asks for itself.
This page owns the plugin that replaces the pool: the card, its states, its citers, and its tab.

**What a card is**: one folder per question, such as this page's own `probe/PP01-pool-census/`, holding the question in the page's own words, a `state:` line, and the binding the run fills when the answer lands.

**What the bank is**: the shared task and discovery layers that answer questions in general language, landing each answer in a `<task-folder>/QA/<n>-<slug>.md` file with its data artifact.

**What retires**: the paper-level `1-probes/` pool, ruled in this page's Law.
The PPNN card grammar survives, and the numbering now runs per page.
The paper family's probe skills must relearn their landing address, which A1.2 tracks.

**Covered elsewhere**: `QPf1` rules that a page owns its folder and every subfolder is a plugin; `QPf5` is the display plugin whose `intake/` cites a card by id, and its Law carries the ruling that births this page.

## Diagram
**Two plugins, one binding**: the example card PP07, the two citers stacked under it, and the bank behind the wall.
```text
  <page>/
    probe/PP07-drift-rate/card.md          🚪 THE ASK, once
        question · stake
        state:   raised → working → bound
        binding: → tasks/T12/QA/3-drift.md
              ▲ both citers point here, by id
    display/<unit>/intake/manifest.yaml    📥 probe: PP07
    <page>.md, a Content claim             📋 "…17.3% (PP07)"
  ──────────────────────────────────────────────────────────
  🧪 the BANK  tasks/ · discoveries/  answers in general language
```
Everything above the line belongs to the page and everything below it belongs to the bank; §3 says what may cross.
PP07 is a worked example, not one of this page's live cards, which are PP01, PP02 and PP03.

## Content
### 1 · The card, and the pool it retires
**The card's shape**: the PPNN grammar kept whole, at its one address.
```text
  <page>/probe/PP<NN>-<slug>/
    card.md
      question:      in the page's own words
      state:         raised → working → bound
      binding:       → <task-folder>/QA/<n>-<slug>.md   filled when answered
      stake:         why this page needs the answer; stays on this side
      ## Q-executor  the SAME question in general language, stake stripped;
                     the ONLY part that ever crosses to the bank
      ## bank binding  route · the bank verdict · where the target stands
      ## A-executor  a COPY of the QA answer, written at harvest
```
The grammar is the shape the retired `1-probes/PPNN` pool taught the orchestrators, taken whole so they speak it without relearning anything.
A `haipipe-probe` entry has four parts, and the card folds in three of them: the executor-facing `Q-executor` and `A-executor`, plus the `bank binding` that records where the answer landed.
It drops the fourth, the review-only `Q-consumer` map, because the card's own `question:` and `stake:` lines already hold the consumer side of the one question the card exists for.
What retires is the address, not the grammar: there is no paper-level pool, the pool is each page's own `probe/` folder, and `PP` numbers run per page.
A card is small on purpose: the probe layer is communication, not judgment, so the card carries a question, its crossing, and a binding, and no review gate.
The stake stays in the card's own `stake:` line and never enters `## Q-executor`, because an executor that knows what the asker hopes for shapes the answer around the hope.

### 2 · Ask once, cite twice
**The one-home rule**: the binding lives in the card, and every consumer points at the card.
```text
  🚪 probe/PP07-drift-rate/card.md   the ONLY place the binding is written
        ▲ one hop up, by id · never a copy of the binding
  📥 intake/manifest.yaml            probe: PP07
  📋 a Content sentence              cites PP07 beside its number
```
Before this plugin, a display unit's manifest bound the answer itself, so a second consumer of the same number would have duplicated the binding.
Now the manifest names the card and the card names the holder, one hop each.
A citer never copies the binding, so a re-answered question changes one file and every citer follows.
This page walks its own rule with three live cards in its own `probe/` folder, all bound: the migration's census (PP01), the orchestrators' landing constraint (PP02), and the family's own skill count (PP03).
All three crossed through `haipipe-probe`'s loop for real: the stake-stripped Q-executors went out through the collector agent, the task bank claimed and answered each in its own `tasks/<folder>/QA/` file, and the bindings carry the paths the collector returned.
The sentences that need those answers cite the ids instead of restating the questions.

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
    ┌──────────────────────────────────────────────┐
    │ ✅ PP01-pool-census                           │
    │ the question, in the page's own words        │
    │ binding: → tasks/A01_repo_inventory/…/QA/…   │
    │ the card folder's tree                       │
    └──────────────────────────────────────────────┘
      ◀ one card fills the pane · shift right for the next ▶
    a citing chip lands on #PP<NN> · the tab writes NOTHING
```
The structure is the display split's, taken whole: a horizontal strip of blocks, one per card, a chip row naming every id, and per-card anchors so a citation lands on the card it names.
The filling is probe's own: the state badge, the question, the binding, and the card folder's tree.
The tab is still the Slides sandwich: a drawer plugin asks a `live/` endpoint, the endpoint globs the page's `probe/`, and each block renders from the card's own state line.
It writes nothing, because every state transition already has an owner in §3.

## Aims
### A1 · 🧾 The card, and the pool it retires
- A1.1 · A card raised in a page's own `probe/` reaches the bank and comes back bound.
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
The ruling, the card grammar, and the crossing to the bank are the settled half; the `1-probes/` sweep, the citation hop, the tab's browser check, and the discovery exclusion stay open.

### A1 · 🧾 The card, and the pool it retires
- ✅ A1.1 · Met 260816: three questions raised on this page's own cards went out stake-stripped through the collector agent, the task bank claimed and answered each, and the bindings carry the QA paths the collector returned, not paths written by hand; where the orchestrators themselves write is A1.2's, and PP02 says that address is still hard-coded.
- ⬜ A1.2 · The sweep has not started, and PP01 and PP02 have scoped it: no live paper or application carries a `1-probes/` pool (all three surviving directories are fixtures), `1-probes/` is a fixed path segment in about 300 live occurrences and no agent accepts a caller-supplied landing directory, and the paper family already retired `1-probes/` for papers, so the shared probe skill disagrees with the paper checker today.

### A2 · 🔗 Ask once, cite twice
- ⬜ A2.1 · `manifest.yaml` has no `probe:` line yet; `QPf5` A1 shares this seam.

### A4 · 🚪 The surface: the probe tab
- 🧠 A4.1 · `plugview.py` and the drawer row exist, the strip structure landed, and the page's three cards render in it, ✅ PP01 ✅ PP02 ✅ PP03 with their bindings shown; the real-browser check waits on a server restart, which is outside this page.

### P · 🚧 The boundary
- ⬜ P1 · Discovery's exclusion list does not know `probe/` by name.

## Files
### ⚙️ Engines
- `../../board/haipipe-board/live/plugview.py`
  The probe endpoint A4.1 ships in: `plug_probe` globs the page's `probe/` and lays the cards out as a strip.
- `../../board/haipipe-board/assets/js/10-drawer/84-plugin-evidence.js`
  The drawer file that registers the 🚪 Probe tab, A4.1's client half.

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
- 260816 · [REVISE-CC] 🔍 the page stopped contradicting its own cards
      A cold reader found the page saying one thing and its three cards on disk saying another, so this pass moved the page onto the cards.
      A1.1 claimed "the orchestrators land in a page's `probe/`, and nowhere else", which is the opposite of what this page's own PP02 answer reports: `1-probes/` is a fixed path segment in about 300 live occurrences and no agent accepts a caller-supplied landing directory.
      Its `Done when` never asked for that, so A1.1 was restated as the thing actually proved, a card raised here reaching the bank and coming back bound, and its State row now hands the orchestrators' address to A1.2 by name instead of quietly disagreeing with it.
      §1's card-grammar figure said the stake rides inside `question`, while all three cards on disk carry their own `stake:` line, so the figure gained that row and lost the claim.
      §1 also called the card's three `##` sections "`haipipe-probe`'s own entry parts"; that entry has four, so the sentence now names the three the card folds in and says it drops the review-only `Q-consumer` map, because the card head already carries the consumer side.
      §2's figure wrote `probe/PP07/card.md`, dropping the slug that §1's own grammar and the Diagram both require, and it is now the full `PP07-drift-rate/` address.
      The Diagram and §2 both drew their two citers side by side, which dies on paste, so each figure is now one stacked tree.
      `## States` was a flat list of five rows against four Aims groups, so it gained the `### A1 · 🧾`, `### A2 · 🔗`, `### A4 · 🚪` and `### P · 🚧` headings and the rows moved under them.
- 260816 · [REVISE-CC] 🧹 the page's citations and states caught up with what is on disk
      A review found the page describing files and progress it does not have, so this pass fixed the claims rather than the promise.
      The Engines group pointed at `live/deck.py`, which does not exist: the deck endpoint is `autodeck.py` and the probe tab's own endpoint is `plugview.py`, so both rows were repointed at the files that really serve the tab, `plugview.py` and `84-plugin-evidence.js`.
      The `state:` line still listed the landing address as open after A1.1 was met, and never mentioned P1, so it now names the four aims that really are open.
      A1.2 dropped to ⬜ because its own row says the sweep is not started, and A4.1 moved to 🧠 because its blocker, a server restart, is outside this page.
      PP01 had been standing for both a real card and an invented drift-rate example, so the Opening and the tab figure now name the real PP01-pool-census while the wiring example in the Diagram and §2 moved to PP07, which collides with nothing.
      The stake clause left the Diagram's fence for the prose under it, the drawer's labelled parts were separated by blank lines because the Opening renderer merges consecutive lines into one paragraph, and the seven older Log rows gained emoji headings with their stories folded beneath.
- 260816 · [PROBE-CC] 🧪 the three cards crossed to the bank and came back bound
      The loop ran for real, on JL's instruction: "you should call the haipipe-probe to reach to the task folder".
      The three cards gained frozen stake-free Q-executors, crossed through the collector agent to the task bank, and came back bound to answered QA files under a fresh `tasks/` tree, meeting A1.1 on its own terms.
      The hand-written `_fixture/QA` specimen from the previous round was deleted as the LAW 1 violation it was, a consumer session authoring a QA digest; the bank's own answer to the same census, 24 skills, confirmed it before it went.
      PP01 and PP02's answers reshaped A1.2: no live pool exists anywhere, the hard-coding is instruction text, and the paper family already retired `1-probes/` on its side.
- 260816 · [BUILD-CC] 🧾 PP03 walked the whole loop as the board family's own census
      JL asked the family to probe itself: "you can probe yourself, like for this skill set... how many skills you have".
      The census was asked as PP03-skill-census, answered as 24 skills in four tiers into `_fixture/QA/1-board-skill-census.md` in the bank's QA shape, and bound.
      Both files were marked SPECIMEN because the session answered the question and not the bank, so A1.1 stayed open on its own terms.
- 260816 · [BUILD-CC] 🚪 the page became its own specimen
      JL asked for a working example: "create the fake probe and reference and cite it to make it really work".
      PP01-pool-census and PP02-landing-address were raised in this page's own `probe/`, both genuine questions A1 owes the bank, and cited from §2 and from the A1.2 and A4.1 state rows.
      The bindings stayed empty until the bank answered, because a hand-written binding is the fake the plugin exists to prevent.
      The same hour JL named attribution parentheticals in prose jargon, so the dates moved to Law and Log and the rule landed in `writing-rules.md`.
- 260816 · [RULE-JL] ⚖️ the pool retires, so `probe/` replaces it instead of mirroring it
      The page had framed `probe/` as a MIRROR of the paper's `1-probes/`, and JL ruled the reverse, the REPLACEMENT.
      The Opening, method, §1, and A1 were rewritten from mirror-of-the-pool to the-only-pool.
      A1.2 opened to carry the paper family's migration off `1-probes/`.
- 260816 · [BUILD-CC] 🖼 the tab took the display split's structure
      JL asked for it directly: "follow the structure of the display plugin split".
      `plug_probe` was rebuilt on the strip: one card fills the pane, a chip row names every id, and per-card anchors catch a citation.
      §4 was redrawn to match.
- 260815 1900 · [JL via CC] 🔌 `haipipe-plugin-probe` drafted under `page-plugins/`
      Round 2 of the thin-door migration, and the skill is delta-only over `haipipe-plugin`.
- 260815 · [DRAFT-CC] 🌱 the page was born from JL's ruling on `QPf5`
      A page is a small paper, so `probe/` sat beside `display/` as a mirror of `1-probes/`; the next day's ruling replaced that framing.
      The card grammar was adopted whole and the one-home citation rule written.
      The landing address, the citation hop, and the tab opened as aims.
