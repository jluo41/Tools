<!-- TEMPLATE · ONE DISPLAY ASSET = ONE S PAGE.
     Copy this file to 0-lifecycle/3-display/S-Display-<N>-<slug>.md, fill it, and DELETE every
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

<!-- RULE: `state:` is one of the board's FOUR values and nothing else. 🔴 OPEN · 🟡 PARTIAL ·
     ✅ SETTLED (its human gate passed) · ⏸️ ON HOLD. The detail ("candidate C rendered, awaiting
     promotion") is a sentence in `## Where we are`, not a state. -->

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

### What it shows
takeaway: <what the reader learns in five seconds, one sentence>
serves: <§section> · claim <CN> · called by <the beat or sentence that cites it>
kind: <figure | table | diagram | illustration>
status: <planned | data-ready | candidates | rendered | input-ready | inserted | reviewed>

<!-- RULE: `serves:` is load-bearing. Reading all the asset pages' `serves:` lines IS the
     claim-to-display map, which is why no separate map file exists. Keep it one line. -->

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

① run       <task folder that produced the numbers, or "concept (no data)">
② data      displays/displayNN-<slug>/source/source_data.csv
③ gen code  <see the two shapes below>
④ result    displays/displayNN-<slug>/assets/<figure.pdf | table-body.tex>
⑤ float     displays/displayNN-<slug>/float.tex
⑥ reader    <S-Main-N> · §<X> P<n>

rebuild: <the one command that regenerates ④, or why it cannot be run here>

<!-- RULE: ③ HAS TWO SHAPES and picking the wrong one hides where the code lives.
       FIGURE  the paper draws it, so ③ is `source/gen_<slug>.py` IN THIS UNIT,
               reading the ② snapshot. ① and ③ are different places.
       TABLE   a task generates it and the paper COPIES the result, so ③ is a
               POINTER to the task, written as `source/REBUILD.md`. ① and ③ are
               then the SAME task folder.
     Never copy a task's generation code into the unit. The pointer is the link;
     a copy is a second source that will drift from the first.

     A unit that cannot be rebuilt here still needs `source/REBUILD.md`. Say why:
     the run is on a secure server, the report is dated, the data is PHI. "Cannot
     rebuild" recorded with a reason is provenance; an empty source/ is a hole. -->

<!-- RULE: `⑥ reader` names the paragraph for a human. The BINDING is the
     `> Display:` lane under the citing sentence (QC0's adjacency rule), not a
     coordinate written here. Do not invent a second pointer format. -->

### Spec
<!-- RULE: what the asset MUST show, in the shape the venue allows. This is the only part a
     re-render reads. Panels, axes, what is encoded by position or shape rather than hue, the
     caption's job, and the venue's width or count limit from S-Venue-0. -->
<record lines, or a fenced sketch when the layout needs one>

caption job: <what the caption must explain without overclaiming>

### Fragility
<!-- RULE: what makes this asset wrong rather than merely old, and what moves WITH it. A cohort
     re-run that changes this figure usually changes a table and a sentence too; name them, so a
     re-run does not silently leave two of the three stale. -->
<one or two record lines>

## Items to Finish
<!-- RULE: this is the page's queue and it is where a Q-Display question lives. A question this
     asset cannot answer itself becomes a row here, recognizable as `Q-Display-<n>`, and the row
     closes only when the answer landed AND was woven into the Spec or the caption.
     Numbers come from the bank, never from the agent: a value the agent typed is a defect, not
     a draft. Route it through PROBE. -->
- [ ] 🔎 Q-Display-<n> · <what evidence this asset needs>
      Which link of the chain it fills, and what breaks if the number differs.
- [ ] 📈 <build, render, or promote step>
- [ ] 🧠 Close this unit's gate
      JL confirms the unit is built, captioned, correctly labeled, and placed.

## Where we are
<the actual state in one or two sentences, with numbers where there are numbers>

## Files
<!-- RULE: name the ARTIFACTS, not the folder. "the unit folder" is not a way to reach anything.
     Cross-page dependencies come after the artifacts. -->
- `displays/displayNN-<slug>/source/gen_<slug>.py`
  Regenerates the asset from the snapshot beside it.
- `displays/displayNN-<slug>/source/source_data.csv`
  The snapshot this render read. Replaced, never edited.
- `displays/displayNN-<slug>/assets/<asset>`
  The live asset. `float.tex` is the only thing that references it.
- `displays/displayNN-<slug>/float.tex`
  Caption, `\label`, and the asset reference. A number typed in here is a defect.

## Log
<!-- RULE: the candidate history belongs HERE, not in Content. Which candidates were rendered,
     which was accepted, who ruled it and when. Content says what the display IS; the Log says
     how it got here. Never delete a `> USER:` line: resolve it and move it here verbatim. -->
YYMMDD · <what changed>
