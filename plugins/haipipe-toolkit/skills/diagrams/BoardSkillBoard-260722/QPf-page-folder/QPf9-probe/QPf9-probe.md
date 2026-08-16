# Probe · a page's evidence questions, asked once and cited by id
state: 🟡 PARTIAL · ruled, cards bound · open: 1-probes retirement, citation hop, tab, exclusion
owner: JL
method: every page gets its own `probe/` pool, the PPNN card shape stays whole, `1-probes/` retires, and every citer names the card by id

## Opening
Where does a page ask the questions it needs evidence for?
In its own `probe/` folder.
The old shared `1-probes/` pool is ruled dead, and moving the probe tools to the new address is open work (A1.2).
A probe is one question, its state, and a link to the answer once it lands.
A paper used to keep its questions far from the sentences that needed them.
Stages are pages now, so each page asks for itself.
This page owns the plugin that replaces the pool: the card, its states, who cites it, and its tab.

**What a card is**: one folder per question, like this page's own `probe/PP01-pool-census/`.
It holds the question in the page's own words, a `state:` line, and a `binding:` line, which is the link to the answer file that the run fills in.

**What the bank is**: the shared task and discovery layers that answer questions in plain, general words.
Each answer lands in a `<task-folder>/QA/<n>-<slug>.md` file, next to the data it came from.

**What goes away**: the paper-wide `1-probes/` pool, ruled in this page's Law.
The PPNN card shape stays, and the numbers start again on each page.
The paper family's probe skills must learn the new address, and A1.2 tracks that.

**Covered elsewhere**: `QPf1` rules that a page owns its folder, and that every subfolder is a plugin.
`QPf5` is the display plugin whose `intake/` cites a card by id, and its Law holds the ruling that started this page.

## Diagram
**Two plugins, one link**: the example card PP07, the two places that cite it, and the bank behind the wall.
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
Everything above the line belongs to the page, and everything below it belongs to the bank.
§3 says what may cross.
PP07 is a worked example, not one of this page's real cards, which are PP01, PP02 and PP03.

## Content
### 1 · One question, one folder, on the page that needs it
**The card's shape**: the same PPNN layout as before, now at one address.
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
📌 Each question gets its own small folder on the page that needs it, and the paper-wide pool is gone.

This is the same layout the old `1-probes/PPNN` pool taught the probe tools, kept whole so they do not have to learn a new one.
A `haipipe-probe` entry has four parts, and the card carries three of them.
It carries `Q-executor` and `A-executor`, the two parts the bank sees, plus the `bank binding` that records where the answer landed.
It drops the fourth part, the review-only `Q-consumer` map.
The card's own `question:` and `stake:` lines already say what the asking side wants.
What goes away is the address, not the layout.
There is no paper-wide pool now: the pool is each page's own `probe/` folder, and `PP` numbers start again on each page.
A card is small on purpose.
The probe layer passes messages, it does not judge, so a card holds a question, the plain version that crosses to the bank, and a link, and no review step.
Why the page wants the answer stays in the card's own `stake:` line, and it never enters `## Q-executor`.
Someone who knows what the asker hopes for will bend the answer toward that hope.

### 2 · The answer is written once, and everyone points at it
**One home**: the link lives in the card, and everyone else points at the card.
```text
  🚪 probe/PP07-drift-rate/card.md   the ONLY place the binding is written
        ▲ one hop up, by id · never a copy of the binding
  📥 intake/manifest.yaml            probe: PP07
  📋 a Content sentence              cites PP07 beside its number
```
📌 The path to an answer is written in one file only, so re-answering a question updates every place that cites it.

Before this plugin, a display figure's manifest held the answer's path itself.
A second user of the same number would then have kept a copy of that path.
Now the manifest names the card, and the card names the file that holds the answer.
Nobody keeps a copy of the path, so a re-answered question changes one file and everyone follows.
This page follows its own rule, with three real cards in its own `probe/` folder, all of them answered.
They are the migration count (PP01), the landing address limit (PP02), and the family's own skill count (PP03).
All three really went through the `haipipe-probe` loop.
The questions went out through the collector agent with the page's own reasons stripped off.
The task bank claimed each one and answered it in its own `tasks/<folder>/QA/` file.
The links in the cards are the paths the collector handed back.
The sentences that need those answers cite the ids instead of asking again.

### 3 · Three states, and one owner for each move
**Three states, three hands**: the page asks, the runner claims, the collector writes the link.
```text
  ⬜ raised    🧑/📄 the page writes the card: the question, no link yet
  🔨 working   🚪 the runner claims it before the lifecycle starts
  ✅ bound     🚪 the collector writes the link when the QA file lands
```
📌 A card is raised, then claimed, then linked, and each of those three moves has exactly one owner.

A `working` card means someone is already on it.
A second session reads that state line and waits, instead of asking the bank again.
Why the page wants the number never crosses the wall.
The card keeps that reason, and the bank sees only the question in plain, general words.
A card may also close with a no.
A bank answer of "not supported" is still an answer, and the sentence citing it must carry that no rather than hide it.

### 4 · A tab that shows every card, and changes nothing
**The tab**: the same layout the display tab uses, carrying cards instead of figures.
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
📌 One tab shows every card on the page, with its state and its link, and it changes nothing.

The layout is the display tab's, taken whole.
It is a sideways strip of blocks, one block per card, with a row of chips naming every id.
Each card has its own mark in the page, so a citation lands on the card it names.
What fills a block is probe's own: the state badge, the question, the link, and the card folder's file tree.
The wiring is the same three-layer one the Slides tab uses.
A tab plugin asks a `live/` endpoint, the endpoint scans the page's `probe/` folder, and each block is drawn from the card's own state line.
It writes nothing, because §3 already gives every state change an owner.

## Aims
### A1 · 🧾 One question, one folder, on the page that needs it
- A1.1 · A card raised in a page's own `probe/` reaches the bank and comes back with a link to the answer.
  **Done when:** a question raised on this page's own card comes back answered, with the QA path written by the collector and not by hand.
- A1.2 · The paper family stops using `1-probes/`.
  **Done when:** no probe skill or runner names `1-probes/` as a place to land, and a paper's stage pages ask through their own `probe/` folders.

### A2 · 🔗 The answer is written once, and everyone points at it
- A2.1 · An intake file finds a card by its id alone.
  **Done when:** a `QPf5` figure's `manifest.yaml` says `probe: PP<NN>`, and the build finds the card and the answer with no path written anywhere.

### A4 · 🚪 A tab that shows every card, and changes nothing
- A4.1 · The tab ships on the same wiring the Slides tab uses.
  **Done when:** a page with one card shows 🚪 Probe in the right pane with the card's real state, seen in a real browser.

### P · 🚧 What page discovery must skip
- P1 · `probe/` is skipped when pages are found.
  **Done when:** no file under any page's `probe/` is ever listed as a page, and `check.py` knows `probe/` as a plugin folder.

## States
Settled: the ruling, the card shape, and the crossing to the bank.
Still open: the `1-probes/` clean-up, the citation hop, the tab's browser check, and the skip rule for `probe/`.

### A1 · 🧾 One question, one folder, on the page that needs it
- ✅ A1.1 · Met 260816: three questions raised on this page's own cards went out through the collector agent with the page's own reasons stripped off.
  The task bank claimed and answered each one, and the links in the cards are the paths the collector returned, not paths typed by hand.
  Where the probe tools themselves write is A1.2's job, and PP02 says that address is still fixed in the code.
- ⬜ A1.2 · The clean-up has not started, and PP01 and PP02 have measured it.
  No live paper or application carries a `1-probes/` pool, because all three surviving folders are fixtures.
  `1-probes/` is a fixed path in about 300 live places, and no agent takes a landing folder from its caller.
  The paper family already dropped `1-probes/` for papers, so the shared probe skill and the paper checker disagree today.

### A2 · 🔗 The answer is written once, and everyone points at it
- ⬜ A2.1 · `manifest.yaml` has no `probe:` line yet, and `QPf5` A1 sits on the same join.

### A4 · 🚪 A tab that shows every card, and changes nothing
- 🧠 A4.1 · `plugview.py` and the tab row exist, the strip layout landed, and the page's three cards show in it: ✅ PP01 ✅ PP02 ✅ PP03, each with its link.
  The real-browser check waits on a server restart, which is outside this page.

### P · 🚧 What page discovery must skip
- ⬜ P1 · The skip list does not know `probe/` by name yet.

## Files
### ⚙️ Engines
- `../../board/haipipe-board/live/plugview.py`
  The endpoint A4.1 ships in.
  `plug_probe` scans the page's `probe/` folder and lays the cards out as a strip.
- `../../board/haipipe-board/assets/js/10-drawer/84-plugin-evidence.js`
  The file that registers the 🚪 Probe tab, A4.1's browser half.

### 📋 Contracts
- `QPf-page-folder/QPf5-display/QPf5-display.md`
  The display plugin whose `intake/` is the first thing to cite a card.
  Its Law holds the ruling that started this page.

### 🧪 Checks
- `../../board/haipipe-board/cli/check.py`
  Where P1's skip rule and the plugin-folder check will land.

## Law
- 260816 JL · 🚪 There is no `1-probes/`, and a page's own `probe/` is the only pool
      Every evidence question lives on the page that needs it, at `<page>/probe/PP<NN>-<slug>/card.md`.
      The paper-wide pool goes away, because a paper's stages are pages now, and a second home would give one question two addresses.
      JL's words: "we will have no 1-probes... The opening is totally wrong."
      Rejected: keeping `1-probes/` beside the plugin for askers that are not pages.
      Once stages are pages, every asker is a page, and calling `probe/` a mirror made the old pool look permanent.

## Log
- 📖 260816 · [REVISE-CC, JL ruled] the page was rewritten in plain words, for a reader with ADHD whose English is a second language (JL: "我他妈真的读不下去"). The 🧭 Outline tab had been showing this page's own sentences back, and they were unreadable, so the tab was right and the prose was not. Every division title now names its consequence instead of a mechanism, each one gained a `📌` line saying in one sentence what the part settles, and every aim, `Done when:` and State row was replaced with a short plain-word version. House words went with them, `division` to part, `store` to list, `render` to read or draw, `seed` to suggest, `mint` to build. Measured with `haipipe-writing`'s `cli/score.py`: 20 sentences flagged before, 9 after, every one that remains inside this Log, which is history and was not touched. No fact, id, `§` mark or section changed; only the words.
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
