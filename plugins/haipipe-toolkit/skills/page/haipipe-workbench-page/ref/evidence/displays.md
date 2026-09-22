# DISPLAY Results · the Page's typed visual evidence

Read this reference from `haipipe-workbench-page` when a Page Evidence Item is
`DISPLAY`, or when the 📃 Page workbench's Evidence Space must present a display unit. The Outline
workbench owns the Page-facing lane and surface. Renderer skills still
own their craft and `recipe/`; they are workers, not Page workbenches.

This reference defines the typed DISPLAY Result payload, which renderer makes
it, and how a sentence cites it. It does not define an Outline Evidence
folder.
The unit's internal shape is NOT defined here: `skills/display/ref/display-unit-output-contract.md` is adopted verbatim (QPf5, ruled JL 260815), and this reference cites it the way Delivery's `ref/latex.md` cites `md2tex.py` — a caller, never a fork.

## 🗂 Storage · one payload under one Result

```text
<page>/results/<re-run>/
├── result.yaml                   typed DISPLAY Result envelope
└── payload/<unit>/                one renderer payload; no Outline Evidence copy
    ├── intake/
    │   ├── manifest.yaml          frozen input and source hashes
    │   └── inputs/                 approved display-safe snapshots
    ├── recipe/                    renderer-owned recipe and receipts
    ├── README.md                  claim, caption, provenance, acceptance status
    ├── float.tex / preview.tex    caller wrapper and standalone preview source
    ├── preview.pdf                compiled inspection preview
    ├── assets/                    selected render; acceptance is a separate gate
    └── candidates/ · versions/    optional renderer history
```

The kind is MIXED, and the split runs through the unit: `intake/`, `recipe/`, `float.tex`, `README.md` are PRIMARY originals; `preview.pdf`, `assets/`, `candidates/`, `versions/` are regenerable from them.
What of the derived half is committed is QPf5's open Decision Now row (default ⭐B: sources + `assets/` + `float.tex` in, previews and candidates ignored) — read the row there, this file does not rule it.
The address rule is simple: the Result manifest names the resolved payload
directory. A renderer never discovers or writes an `outline/evidence/display/`
directory.

## ✍️ Writer · a family routed by kind, and a gate no machine may tick

Display writing is a ROUTING DECISION: the claim's kind picks the renderer
skill, and the renderer owns `recipe/` end to end.

```text
driven by   kind             renderer                          recipe holds
──────────────────────────────────────────────────────────────────────────────
data        📊 table         haipipe-display-table             the build script
data        📈 figure        haipipe-display-figure            the python + receipts
concept     📐 diagram       haipipe-display-diagram           the FigureSpec JSON → SVG
concept     ✒️ tex           haipipe-display-tex               the .tex source
concept     🎨 illustration  haipipe-display-illustration      the prompt + review log
```

The ✒️ row is named after the MECHANISM, not after one package (JL 260816): tikz, an
`algorithm2e` block, and a display equation are one kind, because they share the writer (a
person), the recipe (a hand-authored `.tex` that `float.tex` inputs), and now one skill.
Three names for one mechanism would be the drift.
`haipipe-display-tex` holds that kind's craft, including the rule that such a unit still owes
`assets/figure.pdf`, since a consumer's master rarely carries the author's preamble.

`haipipe-display` is the DOOR over that table (JL 260816): say what you want shown and it picks the renderer, or name the renderer directly when the kind is already clear.
The family retired its poster and slides renderers the same day; a page's talk is the slide workbench's deck, never a display unit.

Data-driven kinds take their numbers ONLY through `intake/` citing the task bank by id — ask once, cite twice (QPf5 §4); a render never invents a value.
Every unit walks the same five steps, and the hands alternate. LAND owns steps
①–④ as Result production in the caller-supplied Page unit; CHECK administers
step ⑤ after the unit can be judged in the built Page:

```text
① INTAKE 🧑 → ② RENDER ⚙️ → ③ PICK 🧑 → ④ BUILD ⚙️ → ⑤ ACCEPT 🧑
```

Only a person ticks `accepted:` in the unit's README, and a changed `intake/`
drops the tick back to ⬜. This lowercase human decision is distinct from the
Evidence Item's capitalized `Acceptance` checks: those checks make the local
DISPLAY Result ready during LAND; `accepted:` is the later CHECK gate that
binds the visible render to its inputs.

## ❄️ Intake · a data unit freezes from its Local Input, never from the workspace

A data-driven unit takes its numbers from the Evidence Item's frozen Local
Input through this path:

```text
  Supporting Execution/Discovery Result(s)
        │  LAND validates source · run · sha256 · aggregate: true
        ▼
  one frozen Evidence Item Local Input
        │  ① INTAKE reads/copies it and records the SAME sha256
        ▼
  <resolved-result>/payload/<unit>/intake/inputs/<file>
        │  ② RENDER reads the frozen copy at run time
        ▼
  assets/table-body.tex · float.tex · preview.pdf
```

**The unit never reaches into the workspace a second time.** Supporting Results
already crossed the wall and the Local Input froze their provenance. A unit
that re-pulls a source is a second, unwitnessed pull. `intake/manifest.yaml`
names the Evidence Item, Supporting Result ids/paths, and hashes. If any source
hash moves, the intake is stale and `accepted:` drops back to ⬜.

**A DATA-driven unit may only be created once the Results supporting it are
valid.** Its `intake/` freezes from the Evidence Item's Local Input, which does
not exist until LAND validates every declared Supporting Result and freezes
the Local Input. Until then the typed `DISPLAY` item carries its expectation and Run
plan but no display unit folder. A CONCEPT unit may have zero Supporting Runs
when its approved item contract is sufficient; LAND still freezes one Local
Input and executes one Local Run.

**The recipe TYPES no cell.** `recipe/` reads the frozen intake at run time, so
re-running it against the same intake yields the same bytes and a reader can
check any printed number against the bound Supporting/local Results. It also
fails loudly on a ragged read: `QC1-visitlbp-Display1-control-ladder` caught
Stata writing `="771,449"`, where the `=` outside the quote makes a CSV parser
split inside the number and deliver 11 cells where 5 were expected.

**A unit names the bullet it serves** in a `serves:` row of its README. The plan
was frozen before the unit existed, so the unit points at the plan and never
the reverse.

**A unit names its provenance authority.** LAND passes this Page-owned unit
directory directly to the renderer. The governed Result envelope and the
unit's `intake/manifest.yaml`/README record the source local Run id, resolved
Result path, unit pointer, and hashes. The Result does not first hold a duplicate
render payload that must be copied here; the unit is still not a second
independently authored Result.

In a consumer-serving canonical Task, a PHI-safe unit admitted by LAND remains
at this Page address as the narrow Page-authority exception. Its governed
`result.yaml` and `runtime.yaml` stay under
`$OUTPUT_ROOT/results/<task>/<RUNNAME>/` and point to/hash the unit. This does
not authorize any other generated output inside the Job.

## 🖼 Evidence segment · the strip that shows everything and writes nothing

`POST /_board/display` (`servers/workbench-page/plugview.py`) remains the compatibility route
that writes the derived `<stem>-view.html` shown inside the 🖼 Displays segment
of the 📃 Page workbench's Evidence Space. It is not a standalone Workbench surface.
Units lay as a horizontal strip, one filling the pane, snap-shifted right to the next; a chip row names every unit and clicking a chip shifts the strip to it.
Each card leads with the framed `preview.pdf` (or a 🕳 no-render-yet notice naming which step is missing), then the README rows, then the unit's folder tree with the ⚙️ derived halves marked — the drawn thing first, its description under it (JL 260819: "display the pdf at the very top, and then show information").
The strip header reports three independently computed counts: **declared** means a unit folder exists, **rendered** means a winning asset and `preview.pdf` both exist, and **accepted** means the README carries a human `accepted: ✅ ...` decision. Folder count is never presented as completed work.
The no-render notice is evidence-driven: it identifies the first missing step among frozen `intake/inputs`, renderer-owned `recipe/`, a winning `assets/` file, `preview.pdf`, and human acceptance. It must not claim that intake or recipe exists merely because the unit folder exists.
An empty `display/` renders the contract's ghost scaffold, so an empty tab teaches the unit shape instead of showing a blank.
The surface is read-only by contract: renderers write `recipe/` and `assets/`, a person rules `intake/` and the tick, the pane writes nothing.

## 📎 Page label · the display is cited by a `D_` placeholder

What no other workbench has: a display unit is an EVIDENCE CARD the Page's own
prose cites. The Page-facing citation is a LaTeX-like placeholder in the
sentence where the claim lives; the later resolver maps it to the display's
Result/Card:

```text
Steps ① ③ ⑤ are a person's and steps ② ④ are machinery
— the split of hands \\figure{D_hands} draws.
                     └────🖼 display card────┘
```

The `> Display:` lane under a sentence is retired for v4. A DISPLAY Result
owns its payload and the Evidence Space card links to it; the plan only names
the Evidence Item and Bullet.
The Result manifest is the index for the card. It exposes the current preview,
status, and provenance without discovering an Outline Evidence folder.
In Page prose, use `\\table{D_<slug>}` for a table, `\\figure{D_<slug>}` for a
figure, or `\\algorithm{D_<slug>}` for an algorithm block. All are
`DISPLAY` labels; `display_kind` differentiates table, figure, and algorithm.
Conceptual diagrams and AI-generated illustrations are cited as ordinary
figures with `\\figure{D_<slug>}`; they do not create `\\diagram` or
`\\illustration` Page syntax. These macros are Page placeholder syntax that is intentionally LaTeX-like; they are
not promised to compile as standalone native LaTeX commands. The LaTeX
delivery worker translates the bound display into its real float/environment,
while web/Word projections use their own renderer. The authored Page keeps the
same `D_` token across projections.
renderer-owned unit id (for example `Display1`) belongs in the Result/Card
metadata, not as a competing Page placeholder. A backticked token quotes the
syntax and is not resolved.
Naming a ⬜ unit is legal and useful — it binds a pending render, and the chip says what is owed.
Candidate rendering does not wait for final Page closure: PHI-safe aggregate
intake may be rendered for review while a worker-specific provenance gate is
open. EMBED may interpret the DISPLAY Result after its authored `Acceptance`
checks pass. Final Page closure and release still require the separate human
`accepted:` decision when declared.
THE PROJECTIONS INHERIT THE CITATION (JL 260816): the latex export embeds a cited unit as a real float after the citing paragraph (the winning asset, the unit's own caption and label), and the word export embeds the rasterized figure with the inline `(Figure n)` and a 🖼 Display comment on the sentence — the per-projection mechanics are Delivery's `ref/latex.md` and `ref/word.md`, not this file's.


## 🚫 Retired locations

`outline/evidence/display/`, flat `display/`, and symlink stubs are not read by
v4. Move their material to `_archive/legacy-outline-evidence/` and create a
typed DISPLAY Result. Historical files do not qualify for the user-check
packet and never become new write targets.

## 📂 Files and ownership

- `../../../../display/ref/display-unit-output-contract.md`
  The unit's internal shape; adopted verbatim, never forked.
- `../../../../../servers/workbench-page/evidence.py`
  The Evidence Space DISPLAY card and preview: read-only.
- `<page>/results/<re-run>/result.yaml`
  The Result index: typed manifest → Evidence card.
- `../../../../../servers/workbench-page/assets/js/10-drawer/07-workbench-outline.js`
  The drawer registration for the shared Outline workspaces.
- `../../../haipipe-workbench/ref/roster.md`
  The Result/payload storage contract owned by the Run producer.
