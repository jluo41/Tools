# Display · adopted unit folders, shown and accepted on the page
state: 🟡 PARTIAL · folder shape copied, both units real · open: --check seam, live check, P1, git question
owner: JL
method: copy the display family's folder shape into `<page>/display/`, build the adapter and the tab the way Slides did, and keep the yes a person's click
session: f11e6b87-fddb-4c7d-ae98-a9a17cffc0ce
## Opening
Where does a page keep its figures and tables?
One finished figure or table sits in its own folder, and this page calls that folder a unit.
A unit holds the numbers a person approved, the script that draws them, and the picture that came out.
The drawing skills already gave papers this exact folder shape, so a page copies it.
This page settles the page side only: where a unit sits, how it shows, how text points at it, and who says it is good.

**What is inside one unit**: one folder per drawn thing, such as this page's own `display/QPf5-Display1-pipeline-tikz/`.
`intake/` holds the numbers a person approved, and `recipe/` holds the script that draws them.
`assets/` holds the picture that won, and `preview.pdf` is the built page a person opens to look at it.

**Why copy instead of redesign**: papers already build units in this exact folder shape.
The rules file asks for this, saying each caller "maps this bundle into its own layout through its own adapter".
A page is just one more caller.
A second folder shape would make every drawing skill learn two.

**Covered elsewhere**: `QPf1` rules that a page owns its folder, and that every subfolder of it is a plugin.
`QPf2` is the drawing plugin and `QPf3` is the slides plugin, whose own line "a slide is a display that talks" says how close they are.
The paper does the same copying in its `S05-display` stage, with `cli/build-displays.py`.

## Diagram
**One folder shape, two users**: the paper stage and a page keep the same unit folder, and only the joining piece differs.
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
### 1 · The same folder shape as a paper, at a new address
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
📌 A page keeps its figures in the same folder shape a paper uses, so nobody has to learn a second one.
The tree above is copied from the display family's own rules file, `display-unit-output-contract.md`, word for word.
The folders split in two.
`intake/` and `recipe/` are yours to write, filled by people and by drawing skills.
`assets/` and `preview.pdf` are rebuilt for you from those two.
So a rebuild may replace the built half, and it never touches the half you wrote.
The one page-side change is the address.
The unit sits inside the page's own `display/` folder, so when the page moves, its figures move with it.

### 2 · Every unit shows as a card, and a sentence can point at it
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
📌 Each unit shows as one card in the right pane, and naming its id in a sentence turns that id into a button.
The tab is built the way the Slides tab is.
A small button in the page's toolbar asks the server for this page's units.
The server then writes a view that frames each unit's `preview.pdf`.
🔄 builds `preview.pdf` again from `preview.tex`.
It never reruns the recipe, never changes the inputs, and never changes a yes.
A unit is EVIDENCE.
Name a unit's id in plain text, and that id turns into a small button in the sentence.
Click it, and the unit's card opens with its picture and its yes-or-no state.
There is a second way to attach the same evidence, made for machines.
It is a `> Display:` line under a sentence, beside the `> Citation:` and `> Value:` lines.
That way a program can add evidence without ever editing a person's words.
You may point at a unit that has no picture yet, in either form.
The button then says a drawing is still owed.
The exports carry the evidence too.
The LaTeX PDF prints a named unit as a real figure, right after the paragraph that names it.
The Word file puts the picture in with its caption, and adds a 🖼 comment note on the sentence.

### 3 · Three hands touch a unit, and only one may say yes
**Who writes what**: three hands touch one unit, and each stays in its own half.
```text
  🎨 renderer skills   haipipe-display-table · -figure · -diagram · -illustration
                       write recipe/ · assets/ · preview.pdf
  🧑 a person          rules intake/ and ticks accepted:
  🖼 the pane          shows everything · writes NOTHING
```
📌 Drawing skills fill the folder, but the yes on a picture is always a person's click.
The drawing skills already belong to the display family, and this page adds none of its own.
The `accepted:` row is the one rule with teeth.
A ✅ there means a person looked at one exact picture and said yes.
A machine that ticks it has faked a judgment, not saved time, so no machine may tick it.

**The kinds, and who draws them**: one door sends the ask to five drawing skills, four scripted and one written by hand.
```text
  🚪 haipipe-display · the DOOR · say the ask, it picks the renderer
  🎲 data-driven · needs a ruled intake/ of numbers
     📊 -table         aggregated CSV/JSON ▶ booktabs LaTeX · recipe = the spec
     📈 -figure        results ▶ plot · recipe = the python script
  🧠 concept-driven · the intake is a spec, not numbers
     📐 -diagram       FigureSpec JSON ▶ deterministic editable SVG
     ✒️ -tex           .tex recipe ▶ vector PDF · TeX-native · a person writes it
     🎨 -illustration  image-gen prompt ▶ concept figure · recipe = prompt + receipts
```
A data-driven skill draws numbers, and it may not go back to the raw data.
It reads only the small approved copy in `intake/`.
A concept-driven skill draws an idea, so it holds no numbers at all, and its input is the sketch itself.
In the ✒️ row a person draws by hand: they type the picture as `.tex` code, and that is how both units on this page were drawn.
It gets its own row because the drawing is TeX code, so it uses the document's own fonts and math, and `float.tex` can pull the file in as it is.
The skill is named after that way of drawing, not after one package, so `haipipe-display-tex` covers a TikZ figure, an algorithm block, and a math display (JL 260816).
Such a unit still owes a built `assets/figure.pdf`.
A document that pulls the code in rarely has the same setup lines at the top of the file.
Drawing a unit again from its recipe depends on the kind.
A python figure reruns its script, a diagram redraws from its spec, and an AI picture replays its saved prompt.

### 4 · The order of the work, and which steps need a person
**The five steps**: from approved numbers to a picture a person accepts, and who moves each step.
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
📌 Nothing is drawn before a person approves the numbers, and nothing is finished before a person looks.
Drawing never comes first.
With no approved inputs there is nothing safe to draw, and the intake rules exist to refuse exactly that.
Steps ① ③ ⑤ belong to a person, and steps ② ④ belong to the machine.
QPf5-Display1 draws that split of hands.
The tab's 🔄 reruns step ④'s build alone, never step ②'s drawing skill.
If the inputs change, the work runs forward again from ② to ⑤.
The old yes drops back to ⬜, because the picture a person agreed to no longer exists.

**Where step ①'s numbers come from**: each hop points at the one before it by id, never by a copy.
```text
  ❓ the page needs a number   ▶ raised as a PROBE · the page's own probe/ plugin (QPf9)
  🚪 probe orchestrator        ▶ sweeps the bank · reuse | enrich | fresh
  🧪 haipipe-task runs         ▶ answer lands in <task-folder>/QA/<n>-<slug>.md
                                 + the run's artifact, e.g. counts.csv · CANONICAL
  📥 intake/manifest.yaml      ▶ cites that holder BY ID · carries only a
                                 small approved extract in inputs/
```
A probe is a question card.
The page asks its question once, the answer lands in the shared task list, and after that everyone points at the card's id instead of asking again.
So `intake/` is not a second copy of the data.
The task's own output stays the one source, and the manifest only points at it, by id.
A unit names its evidence by id, never by a file path, and it never types a number by hand.
QPf5-Display2 draws that move: ask once, point at it twice.
The slides plugin already works this way on `QPf3`.
Its deck asks for an id, a small helper turns the id into the file's real path, and the template holds no digits at all.
So a hand-typed number has nowhere to live.
That id lookup already reaches units under a page, because the citation index finds a unit by id wherever the unit sits.
Aim A1 asks for the other half.
The build adapter should accept a page's `display/` as a unit root, so `--check` can report an out-of-date page unit instead of hiding it.

## Aims
### Decision Now
- [ ] 🗣 What should git keep of a unit?
      The paper commits its built `displays/`, but a page unit's `candidates/` and `versions/` can get heavy.
      A · commit the whole unit, history and all, so the board carries everything it needs.
      ⭐B · commit what a person wrote plus the winning `assets/` and `float.tex`, and gitignore `preview.pdf`, `candidates/`, `versions/`.
      🛑 Blocks: live now, both units landed 260815 with a `preview.pdf` and an `assets/figure.pdf` each, and one keeps a `versions/`.
      🤖 If nobody answers: B, matching the paper's rule that a built file can be deleted and made again.


### A1 · 🧾 The same folder shape as a paper, at a new address
- 🔨 A1.1 · `build-displays.py` accepts a page's `display/` as a unit root.
  **Done when:** a unit under a QPf page builds, `--check` passes, and the paper stage still builds as before.
  **Now:** `build-displays.py` still starts from a paper stage folder. It takes the stage as its one argument and works out the paper root as that stage's `parents[1]`, so it does not yet accept a page's `display/` as a unit root, and `--check` for a page unit is still owed. What did land is the id lookup those units need before anything can point at them: `dialect_paper.py` globs `display/*/float.tex` under the board folder, and both exports find `<page>/display/` units (260815-16).


### A2 · 🖼 Every unit shows as a card, and a sentence can point at it
- 🧠 A2.1 · The tab ships the way the Slides tab did: one toolbar button, plus a view the server writes.
  **Done when:** a page with one unit shows 🖼 Display in the right pane and frames its `preview.pdf`, seen in a real browser at the address JL uses.
  **Now:** The view and the `/_board/display` route are written in `live/plugview.py`, and the browser half in `assets/js/10-drawer/84-plugin-evidence.js`, which registers the 🖼 Display tab (260815-16). The real-browser look the Done-when asks for waits on the server restart that loads them.


### A3 · 🧠 Three hands touch a unit, and only one may say yes
- 🧠 A3.1 · The pane shows the yes and cannot write it.
  **Done when:** the tab draws `accepted:` rows as read-only, and `serve.py` offers no route that edits one.
  **Now:** Waiting on A2.1's live check, and on nothing else. The pane is read-only by build: `plug_display` prints each unit's README rows and frames its `preview.pdf`, its 🔄 rebuilds only the preview, and no route anywhere edits an `accepted:` row.


### A4 · 🏭 The order of the work, and which steps need a person
- ✅ A4.1 · One real unit is built end to end on this page.
  **Done when:** a unit under this page's own `display/` has walked ① to ④, its `preview.pdf` opens, and only ⑤ waits on a person.
  **Now:** Met 260815 by `display/QPf5-Display2-small-paper-tikz/`, written straight in TeX. It walked ① a concept intake, ② the TikZ recipe written and built, ③ the v2 picture picked after v1 cut off the bank box, and ④ `preview.pdf` plus `assets/figure.pdf` built; only ⑤ waits, and its ⬜ sits in the unit's README where no machine may tick it. The engine is xelatex: each unit's `preview.log` names XeTeX as what made the picture on disk, and xelatex is what the tab's 🔄 runs, while both unit READMEs still write the rebuild as `pdflatex preview.tex`, a wording fix owed to those units. The sibling `Display1` changed kind to TikZ and drew the same day (`Display1-pipeline-tikz`); its picture-generation plan waits in the unit's `versions/`.


### P · 🚧 The boundary
- 🔨 P1 · `display/` joins the list of folders discovery skips.
  **Done when:** discovery never lists a file under any page's `display/`, and `check.py` knows `display/` by name as a plugin folder.
  **Now:** Discovery already stays out, and not by a list: `src/common.py`'s `_in_plugin` skips every subfolder of a folded page, so nothing under any `display/` can show up as a page. What is owed is the by-name half of the Done-when: `check.py` checks `draw/` by name in `check_draw_folders`, and has nothing like it for `display/`.


## Discussion

### From the retired States section (merged 260831)
The folder shape, both demo units, and the two ways to point at a unit are real and working.
Four things stay open: the `--check` join, the live-browser look that waits on a server restart, the boundary row, and the git question below.

## Files
### ⚙️ Engines
- `../../board/haipipe-board/cli/build-displays.py`
  The finder A1 teaches to accept a page root; the paper stage keeps its own path.
- `../../board/haipipe-board/src/dialect_paper.py`
  A1.1's landed half: it globs `display/*/float.tex` under the board, so a page's figure becomes a button by id, like a workspace one.
- `../../board/haipipe-board/src/common.py`
  P1's landed half: `_in_plugin` skips every subfolder of a folded page, so no file under any `display/` can show up as a page.
- `../../board/haipipe-board/live/plugview.py`
  A2's server half: `plug_display` rebuilds each preview, then writes the read-only 🖼 Display view.
- `../../board/haipipe-board/assets/js/10-drawer/84-plugin-evidence.js`
  A2's browser half: it registers the 🖼 Display tab and opens the written view in the right pane.
- `../../board/haipipe-board/assets/js/10-drawer/70-plugin-slides.js`
  The Slides tab this one copied: a toolbar button, then a view the server writes.

### 📋 Contracts
- `../../display/ref/display-unit-output-contract.md`
  The unit layout this page copies word for word; if the two disagree, that file wins.
- `../../display/ref/display-intake-contract.md`
  What a caller owes `intake/` before any drawing skill runs.
- `../../board/page-plugins/haipipe-plugin-display/SKILL.md`
  This page's rules as a loadable skill, for a user with no board open.

### 🧪 Checks
- `../../board/haipipe-board/cli/check.py`
  Where P1's owed half lands: it checks `draw/` by name in `check_draw_folders`, and has nothing like it for `display/`.

## Law
- 260815 JL · 🚪 A page's probes are a plugin beside display
      A page is a small paper: `<page>/probe/` mirrors the paper's `1-probes/`, the link lives once in the card, and an intake manifest or a Content claim points at it by id.
      JL's words: "we treat each page as a small paper... we will have a probe plugin... a probe folder along with display."
      Rejected: putting the question inside the unit's `intake/`, because a second user would then repeat the same link.
      Also rejected: leaving things as they were, because that writes two files per number.
      The plugin's own contract page is `QPf9`.
- 260815 JL · 🖼 Display is a plugin, never a page kind
      Any page may carry display units in its own `display/` folder, and no page IS a display.
      JL's words: "display will just be a Plugin, as every page will have displays of tables of figures."
      The rejected option was a `for-display` page kind beside the plugin.
      It fell because displays are material every page carries, not a subject a page argues.
      A page kind would give one word two meanings.

## Log
- 260819 1934 · [RULE-JL] the render leads the card (JL: "display the pdf at the very top, and then show information" — clicking a unit met its README description rows first, the drawn thing below the fold): `plug_display` in `live/plugview.py` now orders each card unit-name ▶ `preview.pdf` (or the 🕳 no-render notice) ▶ state line ▶ README rows ▶ folder tree; `haipipe-plugin-display` SKILL.md's card-order sentence updated to match. Verified by regenerating QPw00's view through the live route: the `<object class='pdf'>` sits before the first README row. Both viewers (5599, 5601) restarted on the new module.
- 260817 1425 · [REVISE-CC] §3's ✒️ paragraph rewritten in plainer words (JL asked for very simple English): "the one whose writer is a person" became "a person draws by hand: they type the picture as `.tex` code", "picks up" became "uses", "named after that MECHANISM" became "named after that way of drawing", "display equation" became "math display", and "the author's own preamble" became "the same setup lines at the top of the file". Same four sentences, same facts, same ids.
- 260816 · [RULE-JL] the ✒️ row got its skill (JL: "should we have a new skill for the tikz? or make -diagram include tikz?"): `haipipe-display-tex` born rather than folded into `-diagram`, because that skill compiles a JSON spec through SVG machinery while this way has no script at all, and FigureSpec has no vocabulary for named tikz styles, TeX macros, or math. Named after the MECHANISM, so one skill covers tikz, algorithm blocks, and display equations; its craft is this page's own two units, including the rule they proved, that such a unit still owes `assets/figure.pdf`.
- 📖 260816 · [REVISE-CC, JL ruled] the page was rewritten in plain words, for a reader with ADHD whose English is a second language (JL: "我真的读不下去"). The 🧭 Outline tab had been showing this page's own sentences back, and they were unreadable, so the tab was right and the prose was not. Every division title now names its consequence instead of a mechanism, each one gained a `📌` line saying in one sentence what the part settles, and every aim, `Done when:` and State row was replaced with a short plain-word version. House words went with them, `division` to part, `store` to list, `render` to read or draw, `seed` to suggest, `mint` to build. Measured with `haipipe-writing`'s `cli/score.py`: 19 sentences flagged before, 0 after, every one that remains inside this Log, which is history and was not touched. No fact, id, `§` mark or section changed; only the words.
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

- 260831 0116 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0