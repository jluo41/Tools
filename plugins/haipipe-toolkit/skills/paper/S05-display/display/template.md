<!-- TEMPLATE · ONE DISPLAY ASSET = ONE S PAGE.
     Copy this file to 0-lifecycle/S05-display/S-Display-<N>-<slug>.md, fill it, and DELETE every
     RULE comment as you satisfy it. A RULE comment never ships in the filled page.

     WHAT CHANGED (2026-07-26): this stage used to emit ONE gallery document holding every
     display as a `### Figure N -- displayNN` block. Displays gate independently, so the unit of
     work is the asset, not the gallery (QB2b). The gallery survives only as the GENERATED
     4-display.tex, which \inputs each unit's float.tex.

     WHAT THIS PAGE IS NOT. It does not hold anything true of more than one asset:
       a ruling other assets must follow  -> S-Venue-3-decisions
       float numbering across all assets  -> S-Submission-0-reconcile
       the venue's display limits         -> S-Venue-0-venue
       the unit FOLDER anatomy            -> ../../../4-display/ref/paper-adapter.md
       the round's coverage sweep         -> S-Submission-0-reconcile
     There is no display control page. Which claim each asset serves is READ off the `serves:`
     line of each asset page, never maintained as a second map.

     NO markdown pipe tables anywhere (JL 2026-07-10): every would-be table is record lines. -->

# S Display <N> · <Figure|Table M> <short name>
state: 🔴 OPEN
owner: JL
method: build the asset from a task's numbers, caption it, place it, and pass the gate
requires: <upstream S ids, comma separated>
style-from: S-Venue-0
provides: <what a downstream section may rely on, one line>

<!-- RULE: `state:` begins with one of the Board's FOUR values: 🔴 OPEN · 🟡 PARTIAL ·
     ✅ SETTLED (its human gate passed) · ⏸️ ON HOLD. A short readable detail may follow the emoji
     (for example, `🔴 rendered but REVISE-blocked`); the evidence and full explanation belong in
     `## States`, not in the state line. -->

## Question
Does <this display> carry <claim CN> for the reader, and is it built from evidence rather than assertion?

<!-- RULE: the paragraph under the question explains why THIS asset earns space in the paper.
     A display that no sentence calls is not a display; it is a leftover. -->
<one paragraph: what the reader cannot see without it>

## Boundary
- ✅ Covered here
  This one asset: what it shows, where its numbers came from, how it is rebuilt, and where it is placed.
- ↪ Covered elsewhere
  Rulings that bind more than one asset are `S-Venue-3`; numbering across assets is `S-Submission-0`; the unit folder anatomy is the skill's output contract.

## Content

<!-- BOARD VIEW: once `unit:` is present, the lifecycle Board injects the reader-facing review
     sequence before this authored text: Current Float → Live display artifact → Display Versions
     → Current display folder. Display Versions inventories saved versions, candidates, and
     non-current assets without promoting any of them: only `float.tex` selects the current
     artifact. The folder is always the real on-disk shape and labels a legacy `source/` layout
     honestly; it does not claim a migration that has not happened.
     These are renderer-injected Board subsections, NOT Markdown headings to copy into each
     allocated page. Validate them in generated `board.html`. An unallocated page without a
     `unit:` record writes its own five empty-state subsections instead. -->

### Display explanation
unit: displayNN-<slug>
takeaway: <what the reader learns in five seconds, one sentence>
serves: <§section> · claim <CN> · called by <the beat or sentence that cites it>
kind: <figure | table | diagram | illustration>
status: <planned | data-ready | candidates | rendered | input-ready | inserted | reviewed>

<!-- RULE: `serves:` is load-bearing. Reading all the asset pages' `serves:` lines IS the
     claim-to-display map, which is why no separate map file exists. Keep it one line. -->

<!-- RULE: `unit:` is the stable bridge from this Paper-owned page to the renderer-owned folder.
     A paper Board renders the unit's current `preview.pdf` as the first subsection of `📚 Content`.
     The preview is the compiled float the manuscript will print; if it is missing, the Board says
     so visibly instead of making a reader infer the display from text. -->

### Provenance
<!-- RULE: THE CHAIN IS THE POINT OF THIS PAGE. Six links, each a real path, so any number in
     the manuscript can be walked back to the run that produced it and forward to the sentence
     that states it.
       · ②-⑤ all live inside the unit folder, so they are RESOLVABLE: a checker can verify each
         one exists. Write the real path, never "see the unit folder".
       · ① and ⑥ are judgments, not lookups. ① may sit outside the paper (a task run, possibly
         on the secure server); ⑥ is which sentence cites it.
       · A link that does not exist yet is written `(none yet)` with one clause saying why.
         A planned display has ①-⑤ empty and that is honest; a rendered display with an empty
         ① means a number was typed by hand, which the output contract forbids. -->

① run       <task holder + run that produced the canonical aggregate, or "concept (no data)">
② intake    displays/displayNN-<slug>/intake/manifest.yaml + inputs/source_data.csv
③ recipe    <see the three shapes below>
④ result    displays/displayNN-<slug>/assets/<figure.pdf | table-body.tex>
⑤ float     displays/displayNN-<slug>/float.tex
⑥ reader    <S-Main-N> · §<X> P<n>

rebuild: <the one command that regenerates ④, or why it cannot be run here>

### Intake
<!-- RULE: values live in Intake, not in recipe. `manifest.yaml` must name the exact task holder,
     run, canonical artifact, snapshot hash, and what this display is allowed to use. A small
     summary CSV is copied to intake/inputs/ so the render is portable. The task's output remains
     the source of truth. Concept figures record their narrative context here and leave values out
     unless they show real numeric facts. -->
manifest: `displays/displayNN-<slug>/intake/manifest.yaml`
values: <task holder · run · canonical source_data.csv, or "none: concept display">
snapshot: <intake/inputs/source_data.csv and sha256, or "none">
context: <narrative / table-description source, if used>

<!-- RULE: ③ HAS THREE SHAPES and picking the wrong one hides where the work lives.
       FIGURE  the paper draws it, so ③ is `recipe/gen_<slug>.py` IN THIS UNIT,
               reading the ② snapshot. ① and ③ are different places.
       TABLE   a task generates it and the paper COPIES the result, so ③ is a
               POINTER to the task, written as `recipe/REBUILD.md`. ① and ③ are
               then the SAME task folder.
       PPTX    a human edits the figure, so ③ is `recipe/<slug>.pptx` plus
               `recipe/export.md`. It exports a PDF/SVG into `assets/`; `float.tex`
               still references that export and `preview.pdf` remains the review view.
     Never copy a task's generation code into the unit. The pointer is the link;
     a copy is a second source that will drift from the first.

     A unit that cannot be rebuilt here still needs `recipe/REBUILD.md`. Say why:
     the run is on a secure server, the report is dated, the data is PHI. "Cannot
     rebuild" recorded with a reason is provenance; an empty recipe/ is a hole. -->

<!-- RULE: `⑥ reader` names the paragraph for a human. The BINDING is the
     `> Display:` lane under the citing sentence (QC0's adjacency rule), not a
     coordinate written here. Do not invent a second pointer format. -->

### Spec
<!-- RULE: what the asset MUST show, in the shape the venue allows. This is the only part a
     re-render reads. Panels, axes, what is encoded by position or shape rather than hue, the
     caption's job, and the venue's width or count limit from S-Venue-0. -->
<record lines, or a fenced sketch when the layout needs one>

caption job: <what the caption must explain without overclaiming>

### Wrapper
<!-- RULE: this is the Paper-owned specification a renderer may serialize, never compose or
     revise. It remains blank/pending while candidates are explored. Before finalization it must
     contain the approved literal caption, stable label, and venue-compatible placement. -->
caption: <approved literal caption, or "pending">
label: <fig:slug | tab:slug, or "pending">
placement: <t | b | htbp, or "pending">

### Fragility
<!-- RULE: what makes this asset wrong rather than merely old, and what moves WITH it. A cohort
     re-run that changes this figure usually changes a table and a sentence too; name them, so a
     re-run does not silently leave two of the three stale. -->
<one or two record lines>

## Aims
<!-- RULE: Aims names the intended outcomes for this one display. Use a P record only for an
     unresolved semantic or evidence question. Known build work and the human gate are ordinary
     Aim records. Numbers come from the bank, never from the agent: a value the agent typed is a
     defect, not a draft. Route uncertainty through EVIDENCE. -->

### Display output
- A1.1 · Build, render, and promote the declared display artifact.
  **Done when:** The approved artifact exists, is rebuildable from its declared provenance, and is selected by `float.tex`.
- A1.2 · Pass this display unit's human gate.
  **Done when:** JL confirms the unit is built, captioned, correctly labeled, and placed.

### P · Stage questions
- P<n> · Q-Display<unit>-<n> · <question title>
  **Done when:** The answer has landed, been interpreted, and been woven into Content.
  **Description:** <what this asset needs to know>
  **Reason:** <which Spec / Wrapper / caption / reader assertion depends on the answer, and what breaks>
  **Probe:** not opened yet
  **Answer:** <empty until EVIDENCE or a documented human ruling>

## States
### Display output
- ⬜ A1.1 · Not started; the display artifact has not yet been built and promoted.
- ⬜ A1.2 · Not started; no human gate ruling has been recorded.

### P · Stage questions
- ⬜ P<n> · Not started; Q-Display<unit>-<n> has not been organized into a probe entry.

## Files
<!-- RULE: name the ARTIFACTS, not the folder. "the unit folder" is not a way to reach anything.
     Cross-page dependencies come after the artifacts. -->
- `displays/displayNN-<slug>/intake/manifest.yaml`
  Binds the task holder and canonical artifact to the approved snapshot this unit read.
- `displays/displayNN-<slug>/intake/inputs/source_data.csv`
  The small display-safe snapshot. Replaced through materialization, never hand-edited.
- `displays/displayNN-<slug>/recipe/gen_<slug>.py`
  Regenerates the asset from the intake snapshot.
- `displays/displayNN-<slug>/recipe/<slug>.pptx` (optional)
  Editable PowerPoint source. `recipe/export.md` records its export into `assets/`; it is never the float itself.
- `displays/displayNN-<slug>/assets/<asset>`
  The live asset. `float.tex` is the only thing that references it.
- `displays/displayNN-<slug>/float.tex`
  Caption, `\label`, and the asset reference. A number typed in here is a defect.

## Log
<!-- RULE: the candidate history belongs HERE, not in Content. Which candidates were rendered,
     which was accepted, who ruled it and when. Content says what the display IS; the Log says
     how it got here. Never delete a `> USER:` line: resolve it and move it here verbatim. -->
YYMMDD · <what changed>
