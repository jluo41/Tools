# Display · adopted unit folders, shown and accepted on the page
state: 🟡 PARTIAL · contract adopted, both units real · open: --check seam, live verify, P1, git ruling
owner: JL
method: adopt the display family's unit contract verbatim at `<page>/display/<unit>/`, build the page adapter and the pane tab on the Slides pattern, and keep acceptance a person's tick
session: fe4afd59-043c-45ba-8555-ef7175b384ee

## Opening
Where does a page keep its figures and tables, now that every subfolder of a page is a plugin?
A display here is one finished figure or table, living in its own folder, called a unit.
A unit holds the approved inputs, the script that draws them, and the picture that came out.
The display skills already fixed this folder shape for papers, so the page reuses it instead of inventing a second one.
This page decides only the page side: where units live, how they show, how text cites them, and who approves.

**What a unit is**: one folder per rendered thing, such as this page's own `display/QPf5-Display1-pipeline-tikz/`.
Inside it, `intake/` holds the inputs a person approved and `recipe/` the script that draws them.
Beside those, `assets/` holds the winning picture and `preview.pdf` is the compiled look a person opens.

**Why reuse rather than redesign**: papers already make display units in this exact folder shape.
The contract file itself invites it, saying each caller "maps this bundle into its own layout through its own adapter".
The page is simply one more caller.
A second folder shape would force every drawing skill to learn two.

**Covered elsewhere**: `QPf1` rules that a page owns its folder and that every subfolder of it is a plugin.
`QPf2` is the drawing plugin and `QPf3` the slides plugin, whose own line "a slide is a display that talks" names the kinship.
The paper's version of this same adoption is the `S05-display` stage with `cli/build-displays.py`.

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
The layout above is the display family's own contract file, `display-unit-output-contract.md`, copied as it stands rather than redesigned.
The folders split into two halves: `intake/` and `recipe/` are the SOURCES, written by people and by drawing skills, while `assets/` and `preview.pdf` are BUILT from those sources, so a rebuild may overwrite the built half but never the sources.
The only page-side change is the address: the unit sits inside the page's own `display/` folder, so when the page moves, its figures move with it.

### 2 · The surface: one card per unit in the right pane
**The tab**: what a reader sees when they open 🖼 Display on a page.
```text
  right pane · 🖼 Display
    ┌─────────────────────────────────────────┐
    │ 📊 QPf5-Display1-pipeline-tikz          │
    │    preview.pdf, framed (body.py ccpdf)  │
    │    README status · 🔄 rebuild            │
    │    accepted: ⬜ · shown, NOT tickable    │
    └─────────────────────────────────────────┘
    one card per unit · empty display/ = empty state, not an error
```
The tab is built the same way the Slides tab is: a small button in the page's toolbar asks the server for this page's units, and the server writes a view that frames each unit's `preview.pdf`.
🔄 recompiles `preview.pdf` from `preview.tex`; it never reruns the recipe, never changes the inputs, and never changes an approval.
A unit is EVIDENCE: when a sentence names a unit's id in plain text, the id becomes a small button in that sentence, and clicking it opens the unit's card with its picture and its approval state.
There is a second way to attach the same evidence, for machines: a `> Display:` line written UNDER a sentence, beside the `> Citation:` and `> Value:` lines, so a program can add evidence without ever editing a person's prose.
Citing a unit that has no render yet is allowed with either form: the button then says a render is still owed.
The exports keep the evidence too: the LaTeX PDF prints a cited unit as a real figure after the paragraph that cites it, and the Word file embeds the picture with its caption and adds a 🖼 comment note on the sentence.

### 3 · The writers, and the row no machine may tick
**Who writes what**: three hands on one unit, each confined to its half.
```text
  🎨 renderer skills   haipipe-display-table · -figure · -diagram · -illustration
                       write recipe/ · assets/ · preview.pdf
  🧑 a person          rules intake/ and ticks accepted:
  🖼 the pane          shows everything · writes NOTHING
```
The renderers are the display family's existing drawing skills; this page adds none of its own.
The approval row is the one rule with teeth: a ✅ on `accepted:` means a person looked at one specific picture and said yes.
A machine that ticks it has forged a judgment, not saved time, so no machine may.

**The kinds and who draws them**: one door routes to four renderers, plus one method with no skill.
```text
  🚪 haipipe-display · the DOOR · say the ask, it picks the renderer
  🎲 data-driven · needs a ruled intake/ of numbers
     📊 -table         aggregated CSV/JSON ▶ booktabs LaTeX · recipe = the spec
     📈 -figure        results ▶ plot · recipe = the python script
  🧠 concept-driven · the intake is a spec, not numbers
     📐 -diagram       FigureSpec JSON ▶ deterministic editable SVG
     ✒️ tikz           .tikz.tex recipe ▶ vector PDF · TeX-native · no skill
     🎨 -illustration  image-gen prompt ▶ concept figure · recipe = prompt + receipts
```
A data-driven renderer draws numbers, and it may not go back to the raw data: it reads only the small approved extract in `intake/`.
A concept-driven renderer draws an idea, so it carries no numbers at all; its input is the sketch it draws.
The ✒️ tikz row is the one method with no skill behind it: a person writes the `.tikz.tex` by hand, which is how both units on this page were drawn.
Being TeX-native is what earns it a row: it inherits the paper's fonts and math labels, and `float.tex` may input it directly.
Redrawing a unit from its recipe follows the kind: a python figure reruns its script, a diagram redraws from its spec, and an AI illustration replays its saved prompt.

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
Drawing never comes first: with no approved inputs there is nothing safe to draw, and the intake contract exists to refuse exactly that.
Steps ① ③ ⑤ belong to a person and steps ② ④ to machinery, the split of hands QPf5-Display1 draws; the tab's 🔄 reruns step ④'s compile alone, never step ②'s renderer.
If the inputs change, the work flows forward again from ② to ⑤, and the old approval drops back to ⬜, because the picture a person said yes to no longer exists.

**Where ①'s numbers come from**: the evidence chain behind an intake, id-bound at every hop.
```text
  ❓ the page needs a number   ▶ raised as a PROBE · the page's own probe/ plugin (QPf9)
  🚪 probe orchestrator        ▶ sweeps the bank · reuse | enrich | fresh
  🧪 haipipe-task runs         ▶ answer lands in <task-folder>/QA/<n>-<slug>.md
                                 + the run's artifact, e.g. counts.csv · CANONICAL
  📥 intake/manifest.yaml      ▶ cites that holder BY ID · carries only a
                                 small approved extract in inputs/
```
A probe is a question card: the page asks its question once, the answer lands in the shared task bank, and from then on everyone cites the card's id instead of asking again.
`intake/` is therefore not a second copy of the data: the task's own output stays the single source, and the manifest only points at it, by id.
A unit names its evidence by id, never by a file path, and never types a number with its own hands; QPf5-Display2 draws this ask-once-cite-twice move.
The slides plugin already works this way on `QPf3`: its deck asks for an id, a resolver turns the id into the file's real path, and the template holds no digits, so a hand-typed number has nowhere to live.
That id lookup already reaches units under a page: the citation index finds a unit by its id wherever the unit sits.
Aim A1 asks for the other half, the build adapter accepting a page's `display/` as its unit root, so `--check` can report a stale page unit instead of hiding it.

## Aims
### A1 · 🧾 The contract, adopted and not forked
- A1.1 · `build-displays.py` accepts a page's `display/` as its unit root.
  **Done when:** a unit under a QPf page builds and `--check` passes, and the paper stage path still builds unchanged.

### A2 · 🖼 The surface: one card per unit in the right pane
- A2.1 · The tab ships on the Slides tab pattern: a toolbar button plus a server-written view.
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
The contract, both demo units, and the citation surfaces are real, and four things stay open: the `--check` seam, the live-browser verification behind a server restart, the boundary row, and the git ruling below.

### A1 · 🧾 The contract, adopted and not forked
- 🔨 A1.1 · `build-displays.py` still anchors on a paper stage directory: it takes the stage as its one argument and derives the paper root as that stage's `parents[1]`, so a page's `display/` is not yet a unit root it accepts and `--check` for a page unit is owed. What did land is the id lookup those units need to be cited at all: `dialect_paper.py` globs `display/*/float.tex` under the board folder, and both exports resolve `<page>/display/` units (260815-16).

### A2 · 🖼 The surface: one card per unit in the right pane
- 🧠 A2.1 · The strip view and the `/_board/display` route are written in `live/plugview.py`, and the drawer's client half in `assets/js/10-drawer/84-plugin-evidence.js`, which registers the 🖼 Display tab (260815-16). The Done-when's real-browser check waits on the server restart that loads them.

### A3 · 🧠 The writers, and the row no machine may tick
- 🧠 A3.1 · Waiting on A2.1's live check, and on nothing else. The written pane is read-only by construction: `plug_display` prints each unit's README rows and frames its `preview.pdf`, its 🔄 recompiles only the derived preview, and no route anywhere edits an `accepted:` row.

### A4 · 🏭 How a unit is generated
- ✅ A4.1 · Met 260815 by `display/QPf5-Display2-small-paper-tikz/`, the TeX-native walk: concept intake ①, the TikZ recipe authored and compiled ②, the v2 candidate picked after the v1's clipped bank box ③, and `preview.pdf` plus `assets/figure.pdf` built ④; only ⑤ waits, and its ⬜ is in the unit's README where no machine may tick it. The engine is xelatex: each unit's `preview.log` names XeTeX as what produced the render on disk, and xelatex is what the tab's 🔄 runs, while both unit READMEs still write the rebuild as `pdflatex preview.tex`, a wording correction owed to those units. The sibling `Display1` re-kinded to TikZ and rendered the same day (`Display1-pipeline-tikz`); its illustration plan waits in the unit's `versions/`.

### P · 🚧 The boundary
- 🔨 P1 · Discovery already stays out, and not by a list: `src/common.py`'s `_in_plugin` skips every subfolder of a folded page, so nothing under any `display/` can surface as a page. What is owed is the by-name half of the Done-when: `check.py` validates `draw/` by name in `check_draw_folders` and has no equivalent that knows `display/`.

### Decision Now
- [ ] 🗣 What does git keep of a unit?
      The paper commits its built `displays/`; a page unit's `candidates/` and `versions/` can grow heavy.
      A · commit the whole unit, history and all, so the board is self-contained.
      ⭐B · commit sources plus the winning `assets/` and `float.tex`; gitignore `preview.pdf`, `candidates/`, `versions/`.
      🛑 Blocks: live now, both units landed 260815 with a `preview.pdf` and an `assets/figure.pdf` each, and one keeps a `versions/`.
      🤖 If nobody answers: B, matching the paper's machinery-under-the-delete-test ruling.

## Files
### ⚙️ Engines
- `../../board/haipipe-board/cli/build-displays.py`
  The resolver A1 teaches to accept a page root; the paper stage keeps its path.
- `../../board/haipipe-board/src/dialect_paper.py`
  A1.1's landed half: it globs `display/*/float.tex` under the board, so a unit under a page chips by id like a workspace one.
- `../../board/haipipe-board/src/common.py`
  P1's landed half: `_in_plugin` skips every subfolder of a folded page, so no file under any `display/` can surface as a page.
- `../../board/haipipe-board/live/plugview.py`
  A2's server half: `plug_display` recompiles each preview, then writes the read-only 🖼 Display view.
- `../../board/haipipe-board/assets/js/10-drawer/84-plugin-evidence.js`
  A2's client half: it registers the 🖼 Display tab and opens the written view in the right pane.
- `../../board/haipipe-board/assets/js/10-drawer/70-plugin-slides.js`
  The Slides tab this surface was patterned on: a toolbar button, then a view the server writes.

### 📋 Contracts
- `../../display/ref/display-unit-output-contract.md`
  The unit layout this page adopts verbatim; if the two disagree, that file wins.
- `../../display/ref/display-intake-contract.md`
  What a caller owes `intake/` before any renderer runs.
- `../../board/page-plugins/haipipe-plugin-display/SKILL.md`
  This page's rules as a loadable skill, for a consumer with no board open.

### 🧪 Checks
- `../../board/haipipe-board/cli/check.py`
  Where P1's owed half lands: it validates `draw/` by name in `check_draw_folders` and has no equivalent that knows `display/`.

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
- 260816 · [REVISE-CC] the second review round's list closed against the shipped code: §2's 🔄 now says what `plug_display` really runs, `preview.tex` ▶ `preview.pdf` and nothing else, so it no longer claims to redraw `assets/`; §3's ✒️ tikz row shrank to a value with its two prose clauses moved under the figure; §4 and State A1.1 stopped describing A1 as an id lookup the Aim never asked for, and both now name the build adapter and `--check`; A2.1 joined A3.1 at 🧠, the two waiting on the same server restart; the States intro regained the git ruling its `state:` line counts; Files gained `src/dialect_paper.py` and `src/common.py`, the two engines State rows already leaned on, and the Checks row narrowed to P1's owed by-name half. On the engine name: each unit's `preview.log` records XeTeX and the tab runs `xelatex`, so the page now says xelatex; both unit READMEs still say `rebuild = pdflatex preview.tex`, and that correction belongs to those units, not to this page.
- 260816 · [REVISE-CC] the page rewrote for a cold reader and its claims were re-checked against disk (JL: "if I am a new person, I don't know what you are talking about"): every section now says its thing in plain words and defines a term before leaning on it, the invented drift-bands example became the page's real units, and Content's `(JL 260816)` parentheticals moved out of the prose, where this Log is their home. States was rewritten ONCE in that pass: it gained the `### A<n>` group headings mirroring Aims, A1.1 and A2.1 read 🔨 with what actually landed, A3.1 moved ⬜ ▶ 🧠 because it waits only on A2.1's live check, A4.1's stale Display1-blocked note became the TikZ render that shipped and dropped its byte count, P1 was restated as owed only in `check.py`'s by-name validation since `src/common.py`'s `_in_plugin` already excludes every page subfolder generically, the Engines row naming `live/deck.py` repointed to `live/plugview.py` with `84-plugin-evidence.js` added as the client half, and the Decision Now blocker was corrected, the units having landed.
- 260816 · [RULE-JL] the display family cut to four renderers and a door (JL, in two steps: "只保留一个就行了" then, on seeing the shape, "figure 和 table 是不是也可以保留呢" and "poster 和 slides 我们都不要了"): `haipipe-display` stays as a pure router, table and figure return as full skills, and the poster and slides renderers retire with their paper-side doors and the content-plan spec that served them alone, parked under `_todo/`. §3's taxonomy now names ✒️ tikz as the method with no skill, which is how both of this page's units were drawn.
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
