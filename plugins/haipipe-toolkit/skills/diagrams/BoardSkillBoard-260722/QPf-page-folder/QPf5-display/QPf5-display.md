# Display · adopted unit folders, shown and accepted on the page
state: 🟡 PARTIAL · the unit contract is adopted from the display family; the page adapter, the tab, and the boundary are open aims
owner: JL
method: adopt the display family's unit contract verbatim at `<page>/display/<unit>/`, build the page adapter and the pane tab on the Slides pattern, and keep acceptance a person's tick
session: fe4afd59-043c-45ba-8555-ef7175b384ee

## Opening
Where does a page's display live, now that every subfolder of a page is a plugin?
A display is one rendered unit, such as a table or a figure.
Each unit is a folder carrying its sources, its recipe, and the winning asset.
The display family already fixed that folder's shape in a source-agnostic contract.
So this page adopts that contract at `<page>/display/<unit>/` rather than designing a new one.
It decides only the page side: how units are found, shown, and accepted.

**What a unit is**: one folder per rendered thing, such as `display/QPf5-Display1-drift-bands/`, holding `intake/` (the approved numbers), `recipe/` (the script that renders), `assets/` (the winning render), and `preview.pdf` (what a person looks at).
**Why adopt rather than design**: the contract says of itself that a caller "maps this bundle into its own layout through its own adapter"; the page is one more caller, and a second unit grammar would fork every renderer.
**Covered elsewhere**: `QPf1` rules that a page owns its folder and every subfolder is a plugin; `QPf2` is the draw plugin and `QPf3` the slide plugin, whose own line "a slide is a display that talks" names their kinship; the paper's adapter for the same contract is `S05-display` with `cli/build-displays.py`.

## Diagram
**One contract, two callers**: the paper stage and the page adopt the same unit folder; only the adapter differs.
```text
  📜 display-unit-output-contract.md · source-agnostic, one unit = one folder
        │
        ├──▶ 📄 the PAPER's adapter (built)
        │      S05-display/display/<unit>/ ──build-displays.py──▶ displays/
        │
        └──▶ 📋 the PAGE's adapter (this page's A1)
               <page>/display/<unit>/
                 ├ intake/ · recipe/        the sources
                 ├ assets/ · preview.pdf    the derived render
                 └ README.md                claim · kind · status
               shown as a 🖼 tab in the right pane (A2)
               accepted by a person, never by the pane (A3)
```

## Content
### 1 · The contract, adopted and not forked
**The plugin's full tree**: one `display/` per page, one folder per unit, every unit the same shape.
```text
  <page>/
    <page>.md                          the page, on stage
    display/                           🖼 the plugin · discovery never enters
      <PageID>-Display1-<slug>/        ONE rendered unit
        README.md      claim · kind · caption-job · fragility · status
        intake/        🧑 caller-owned, provenance-bound values
          manifest.yaml
          inputs/      small approved summary CSV or JSON extracts only
        recipe/        🎨 renderer-owned script, spec, receipts
        float.tex      caption + label + asset reference
        preview.tex    standalone wrapper that inputs float.tex
        preview.pdf    ⚙️ compiled look, what the tab frames
        assets/        ⚙️ the WINNING render
        candidates/    pre-decision renders
        versions/      superseded variants, kept for history
      <PageID>-Display2-<slug>/        the next unit, same shape
```
The layout above is `display-unit-output-contract.md`, quoted rather than redesigned.
`intake/` and `recipe/` are primary material a person rules; `assets/` and `preview.pdf` are derived and a rebuild may overwrite them.
The one page-side change is the address: the unit root is the page's own `display/` folder, so the unit travels with the page it illustrates.

### 2 · The surface: one card per unit in the right pane
**The tab**: what a reader sees when they open 🖼 Display on a page.
```text
  right pane · 🖼 Display
    ┌─────────────────────────────────────────┐
    │ 📊 QPf5-Display1-drift-bands            │
    │    preview.pdf, framed (body.py ccpdf)  │
    │    README status · 🔄 rebuild            │
    │    accepted: ⬜ · shown, NOT tickable    │
    └─────────────────────────────────────────┘
    one card per unit · empty display/ = empty state, not an error
```
The tab is the Slides sandwich with a different filling: a drawer plugin posts to a `live/` endpoint, the endpoint lists the page's units, and the pane frames each `preview.pdf` through the PDF object path `src/body.py` already renders.
🔄 rebuild runs the unit's recipe and refreshes the derived half; it never touches `intake/` and never touches an acceptance row.
A unit is EVIDENCE the content cites, and the citation lives IN the sentence: the unit's id named in prose chips as the evidence card in place, carrying its acceptance state and linking its block in the strip.
The `> Display:` lane beside `> Citation:` and `> Value:` stays the FILING surface: a machine appending evidence writes a lane and never edits prose, and a binding no sentence carries naturally lands there.
Either surface naming a ⬜ unit binds a pending render, not accepted evidence.
The projections inherit the citation (JL 260816): the latex export embeds a cited unit as a real float after the citing paragraph, built from the winning asset and the unit's own caption, and the word export embeds the rasterized figure with an inline figure number and a 🖼 Display comment on the sentence.

### 3 · The writers, and the row no machine may tick
**Who writes what**: three hands on one unit, each confined to its half.
```text
  🎨 renderer skills   haipipe-display-table · -figure · -diagram · …
                       write recipe/ · assets/ · preview.pdf
  🧑 a person          rules intake/ and ticks accepted:
  🖼 the pane          shows everything · writes NOTHING
```
The renderers are the display family's existing skills, dispatched the way `task-for-display` already dispatches them; this page adds no renderer.
Acceptance follows the model the slide plugin already borrowed: a ✅ means a person looked at a specific render and said yes, so a machine that ticks one has forged a judgment, not saved time.

**The four renderers**: which skill draws which kind, and what each one's recipe is.
```text
  🎲 data-driven · needs a ruled intake/ of numbers
     📊 -table         aggregated CSV/JSON ▶ booktabs LaTeX · recipe = the spec
     📈 -figure        results ▶ plot · recipe = the python script
  🧠 concept-driven · the intake is a spec, not numbers
     📐 -diagram       FigureSpec JSON ▶ deterministic editable SVG
     ✒️ tikz           .tikz.tex recipe ▶ vector PDF · TeX-native: the paper's
                       fonts, math labels, and float.tex may input it directly
     🎨 -illustration  image-gen prompt ▶ concept figure · recipe = prompt + receipts
  🧩 -poster · -slides  composites, assembling units the renderers above made
```
A data-driven renderer may not recompute from raw data; it reads the approved extract in `intake/` and nothing else.
A concept-driven renderer carries no numbers, so its intake is the spec it draws.
The rebuild differs the same way: a figure rebuild reruns its python script, a diagram rebuild is deterministic from its spec, and an illustration rebuild replays a receipted prompt.

### 4 · How a unit is generated
**The pipeline**: five steps from approved numbers to an accepted render, and who moves each one.
```text
  ① 📥 INTAKE     🧑 the caller fills intake/: manifest.yaml + small
                     approved extracts, every value provenance-bound
  ② 🎨 RENDER     the matching renderer skill runs, dispatched through
                     task-for-display; it fills recipe/ + candidates/
  ③ 🧑 PICK       a person picks the winner; it moves to assets/,
                     the losers stay in candidates/ or versions/
  ④ ⚙️ BUILD      preview.tex compiles to preview.pdf; the adapter's
                     --check reports a stale unit instead of hiding it
  ⑤ 🧠 ACCEPT     a person reads the render and ticks accepted:
```
The pipeline never starts at ②: a renderer given no ruled `intake/` has nothing provenance-bound to draw, which is what `display-intake-contract.md` exists to refuse.
Steps ① ③ ⑤ are a person's and steps ② ④ are machinery, the split of hands QPf5-Display1 draws; 🔄 rebuild on the tab is step ④ alone, rerun.
A changed `intake/` flows forward, ② to ⑤, and the acceptance falls back to ⬜ because the bytes a person said yes to are gone.

**Where ①'s numbers come from**: the evidence chain behind an intake, id-bound at every hop.
```text
  ❓ the page needs a number   ▶ raised as a PROBE · the page's own probe/ plugin (QPf9)
  🚪 probe orchestrator        ▶ sweeps the bank · reuse | enrich | fresh
  🧪 haipipe-task runs         ▶ answer lands in <task-folder>/QA/<n>-<slug>.md
                                 + the run's artifact, e.g. counts.csv · CANONICAL
  📥 intake/manifest.yaml      ▶ cites that holder BY ID · carries only a
                                 small approved extract in inputs/
```
`intake/` is not a second data store: the task output stays canonical, and the manifest points back at the exact holder and run that produced it.
A unit names its evidence by id, never by path, and never types a number; QPf5-Display2 draws this ask-once-cite-twice move.
The slide plugin already walks this chain on `QPf3`: its deck declares `needs: QA-probe/QBt5-for-value/1-artifact-paths`, the resolver turns the id into the artifact's path, and the template carries no digits, so a hand-typed value has nowhere to live.
A1's adapter is what makes the same id resolution work for a unit under a page.

## Aims
### A1 · 🧾 The contract, adopted and not forked
- A1.1 · `build-displays.py` accepts a page's `display/` as its unit root.
  **Done when:** a unit under a QPf page builds and `--check` passes, and the paper stage path still builds unchanged.

### A2 · 🖼 The surface: one card per unit in the right pane
- A2.1 · The tab ships through the Slides sandwich.
  **Done when:** a page with one unit shows 🖼 Display in the right pane and frames its `preview.pdf`, verified in a real browser at the address JL uses.

### A3 · 🧠 The writers, and the row no machine may tick
- A3.1 · The pane shows acceptance and cannot write it.
  **Done when:** the tab renders `accepted:` rows read-only and `serve.py` exposes no route that edits one.

### A4 · 🏭 How a unit is generated
- A4.1 · One real unit is generated end to end on this page.
  **Done when:** a unit under this page's own `display/` has walked ① to ④, its `preview.pdf` opens, and only ⑤ waits on a person.

### P · 🚧 The boundary
- P1 · `display/` joins the plugin exclusion.
  **Done when:** discovery never lists a file under any page's `display/` and `check.py` names `display/` a known plugin folder.

## States
Nothing page-side is built; the adopted contract is the settled half and every aim below is open.
- ⬜ A1.1 · `build-displays.py` still anchors on a paper stage directory.
- ⬜ A2.1 · No drawer plugin and no `live/` endpoint exist for display.
- ⬜ A3.1 · Holds vacuously today; it must still hold once A2.1 ships.
- ✅ A4.1 · Met 260815 by `display/QPf5-Display2-small-paper-tikz/`, the TeX-native walk: concept intake ①, the TikZ recipe authored and compiled ②, the v2 candidate picked after the v1's clipped bank box ③, and `preview.pdf` (68,506 bytes) plus `assets/figure.pdf` built by pdflatex ④; only ⑤ waits, and its ⬜ is in the unit's README where no machine may tick it. The sibling `Display1` unit stays a planned illustration, still blocked on the codex-image2 bridge.
- ⬜ P1 · Discovery's exclusion list does not know `display/` by name.

### Decision Now
- [ ] 🗣 What does git keep of a unit?
      The paper commits its built `displays/`; a page unit's `candidates/` and `versions/` can grow heavy.
      A · commit the whole unit, history and all, so the board is self-contained.
      ⭐B · commit sources plus the winning `assets/` and `float.tex`; gitignore `preview.pdf`, `candidates/`, `versions/`.
      🛑 Blocks: nothing until the first real unit lands.
      🤖 If nobody answers: B, matching the paper's machinery-under-the-delete-test ruling.

## Files
### ⚙️ Engines
- `../../board/haipipe-board/cli/build-displays.py`
  The resolver A1 teaches to accept a page root; the paper stage keeps its path.
- `../../board/haipipe-board/live/deck.py`
  The Slides endpoint A2 copies; the display endpoint sits beside it.
- `../../board/haipipe-board/assets/js/10-drawer/70-plugin-slides.js`
  The drawer plugin A2 copies for its client half.

### 📋 Contracts
- `../../display/ref/display-unit-output-contract.md`
  The unit layout this page adopts verbatim; if the two disagree, that file wins.
- `../../display/ref/display-intake-contract.md`
  What a caller owes `intake/` before any renderer runs.
- `../../board/page-plugins/haipipe-plugin-display/SKILL.md`
  This page's rules as a loadable skill, for a consumer with no board open.

### 🧪 Checks
- `../../board/haipipe-board/cli/check.py`
  Where P1's exclusion and the plugin-folder validation land.

## Law
- 260815 JL · 🚪 A page's probes are a plugin beside display
      A page is a small paper: `<page>/probe/` mirrors the paper's `1-probes/`, the binding lives once in the card, and an intake manifest or a Content claim cites it by id.
      JL's words: "we treat each page as a small paper... we will have a probe plugin... a probe folder along with display."
      Rejected: absorbing the question into the unit's `intake/`, because a second consumer would have to duplicate the binding; and the status quo, because it writes two files per number.
      The plugin's own contract page is `QPf9`.
- 260815 JL · 🖼 Display is a plugin, never a page kind
      Any page may carry display units in its own `display/` folder, and no page IS a display.
      JL's words: "display will just be a Plugin, as every page will have displays of tables of figures."
      The rejected option was a `for-display` page kind beside the plugin; it fell because displays are material every page carries, not a subject a page argues, so a kind would give one word two meanings.

## Log
- 260816 · [RULE-JL] a clicked card shows its display at once (JL: "how to make it show the display directly as default?"): opening an evidence card now expands its first preview fold, lazily and one fold only, so the 260806 ruling that folded previews (two stacked objects buried the links) still holds at page load.
- 260816 · [BUILD-CC] the projections now carry the evidence (JL: "both word and latex didn't include the display?"): the latex export embeds each cited unit as a float after its citing paragraph (winning asset + authored caption, no tikz needed in the master), and the word export bridges the grammar gap with a temp ref injection plus md2docx's new `--display-root`, landing the figure, the inline number, and the 🖼 Display comment; verified on this page's own PDF and docx, both units present in both.
- 260816 · [RULE-JL] the display citation moved into the content sentence (JL: "it should be in the content sentence, right?", after the render showed a lane latched onto the wrong sentence): §4's two lane rows became ids named in prose, chipping in place by the always-a-card rule, and §2's grammar now names the sentence as the citation's home with the `> Display:` lane kept as the machine's filing surface.
- 260815 · [BUILD-CC] the page's rules became a loadable skill (JL: "we might have the page-plugins in skills/board/page-plugins"): `page-plugins/haipipe-plugin-display` born beside draw/latex/word, owning only the page-side delta (unit address, kind routing, the five-step walk, the `> Display:` lane) and citing the unit contract verbatim; the roster's stale display row corrected to 🟢 MIXED and probe got its missing row. This page stays the design record; the skill is the door a consumer loads with no board open.
- 260815 · [REVISE-CC] the page now cites its own cards (JL: "why are they not cited as the evidence cards in the content?"): §4 cites D1 at the pipeline it draws and D2 at the evidence chain, §2 rules the `D<n>` citation grammar with the pending-render caveat; the strip gained the indented folder tree and the unit name-list chips the same hour.
- 260815 · [BUILD-CC] Display1 got its render (JL: "I think we should have a pdf here"): re-kinded from the bridge-blocked illustration to TikZ as `Display1-pipeline-tikz`, now drawing §4's five steps; the illustration plan is preserved in its `versions/`. The strip gained per-unit anchors, so a citation can land on the exact unit it names.
- 260815 · [BUILD-CC] the demo unit shipped and A4.1 closed: `Display2-small-paper-tikz` walked ① to ④ with the TeX-native method (JL asked for tikz), one refinement round, deterministic rebuild by pdflatex; §3's taxonomy gained the ✒️ tikz row the same hour. Acceptance ⑤ stays JL's.
- 260815 · [PROBE-CC] the first unit walked as far as the session allows: `QPf5-Display1-small-paper` scaffolded on this page with a concept intake (no values, per the intake contract) and the illustration prompt authored to the CVPR rules; the codex-image2 bridge is absent from the toolkit's mcp-servers/, so ② stops at planned and A4.1 reads 🔨.
- 260815 · [RULE-JL] the probe row closed as the plugin: `probe/` joins the roster beside `display/`, the ruling is in Law, and `QPf9` is born to carry its contract; §4's chain now names the page's own `probe/` as where a need is raised.
- 260815 · [REVISE-CC] §3 gained the four-renderer taxonomy, data-driven against concept-driven, and §4 the evidence chain behind intake: probe to task to QA holder to manifest, id-bound at every hop (JL asked who generates and where the data comes from).
- 260815 · [REVISE-CC] §1's figure widened to the plugin's full tree (JL: record the folder structure), and §4 born: the five-step generation pipeline, with A4.1 asking for the first walked unit.
- 260815 · [RULE-JL] the plugin-or-page-kind row closed as A, plugin only; the ruling and the rejected kind are in Law.
- 260815 · [DRAFT-CC] page born in the plugin round: the display family's unit contract adopted at `<page>/display/<unit>/`, the page adapter, the tab, and the boundary opened as aims, and the plugin-or-page-kind choice put to JL.
