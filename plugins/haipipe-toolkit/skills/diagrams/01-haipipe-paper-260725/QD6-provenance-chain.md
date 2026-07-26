# The provenance chain
state: 🟡 PARTIAL
owner: JL
method: six links, four of them resolvable by a machine, so a number can be walked in both directions

## Question
Once a display is rendered, what makes its numbers auditable rather than merely reproducible? Six links run from the number printed in the PDF back to the run that produced it, and each one has to be checkable by somebody who was not there when it was made.

A renderer returns a winning asset, a rebuild spec and a preview. Run the spec again and you get the same picture, which is reproducibility. It does not tell you where the numbers came from, or which sentence in the manuscript now depends on them. Those two facts sit outside the renderer, and without them a display is a picture that happens to contain digits.


The approach is six links, each of them independently checkable, running from the number in the PDF back to the run that produced it. What we want is auditability rather than mere reproducibility: not just that the figure could be rebuilt, but that anyone can prove which data it actually shows.
## Boundary
- ✅ Covered here
  The chain from the producing run to the citing sentence, and which of its links a check can settle.
- ↪ Covered elsewhere
  The renderer's own contract is `QD2`; who may trigger a render is `QD5`; what a sentence pointing at a display means is `QC3` and `QC4`; how evidence is commissioned in the first place is `QBb1`.

## Diagram
```
 REPRODUCIBLE ≠ AUDITABLE. SIX LINKS, AND THE RENDERER OWNS THREE.

  ① run        the task output that produced the numbers   OUTSIDE the paper
       │                                                   🧠 a human judgment
       ▼
  ② data       source/source_data.csv, the snapshot read   ┐
       │                                                   │
  ⑦ gen code   source/gen_<slug>.py                        │ inside ONE unit
       │       parses ②, NEVER recomputes                  │ directory, so a
       ▼                                                   │ CHECK can resolve
  ⑧ result     assets/figure.pdf | table-body.tex          │ all four
       │                                                   │
  ③ float      float.tex: caption · \label · asset ref     ┘
       │
       ▼
  ④ reader     the section · paragraph · SENTENCE citing it
                                                           🧠 a human judgment

 WHY THIS IS A PAGE AND NOT A FIELD ON QD2
   QD2's bundle is ② ⑦ ⑧ only.
   it CANNOT carry ①: the renderer is HANDED evidence, not producing it.
   it CANNOT carry ④: the citing sentence does not exist when it runs.
   so the chain is the JOIN between the display family and the sentence
   family, and it sits between them rather than inside either.

 THE FAILURE IT EXISTS TO PREVENT  — 2026-07-21, not hypothetical
   a ruling flipped a section's exposure from continuous to binary.
   the PROSE was updated.  the TABLE was not, because its numbers had
   been hand-authored and nothing linked them to a producing run.
   the table silently contradicted the text it supported.
   only a manual sweep caught it.                              ⚠️

 THE DIAGNOSTIC THE CHAIN GIVES YOU
   ① empty AND ⑧ exists      the numbers were TYPED. the defect above.
   ⑧ ≠ what ③ references     the manuscript shows a superseded asset
   ⑦ missing                 nobody can rebuild it, including its author
   ④ empty                   an uncited display: a leftover, not a display
```

## Content
### The six links
```
 ①  run        the task output that produced the numbers        OUTSIDE the paper
 ②  data       source/source_data.csv, the snapshot read
 ⑦  gen code   source/gen_<slug>.py, which parses ② and never recomputes
 ⑧  result     assets/<figure.pdf | table-body.tex>
 ③  float      float.tex: caption, \label, asset reference
 ④  reader     the section, paragraph and sentence that cites it
```

Links ② ⑦ ⑧ ③ all live inside one unit directory, so a check can resolve them the way the stage-contract checker resolves declared paths. Links ① and ④ are judgments a human makes: ① may sit on a secure server, and ④ is which sentence chose to point here.

④ is a SENTENCE, and that is inherited rather than decided here. `QC0` settles it: a `>` line directly under a sentence attaches to that sentence, and the four attachment faces ride that one rule. So this chain does not carry a coordinate for ④; the `> Display:` lane under the citing sentence IS the link, and it points back by display id.

### Link ⑦ has two shapes
Discovered by walking all eleven MISQ units on 2026-07-26, after the chain was written as if ⑦ always lived in the paper.

```
 FIGURE   the paper draws it       ⑦ = source/gen_<slug>.py, reading the ② snapshot
                                   ① and ⑦ are DIFFERENT places
 TABLE    a task generates it      ⑦ = a POINTER to the task, as source/REBUILD.md
          and the paper copies     ① and ⑦ are the SAME task folder
```

A task's generation code is never copied into the unit. The pointer is the link, and a copy would be a second source that drifts from the first. That is the same reasoning that killed the claim-to-display map.

### A unit that cannot be rebuilt still owes a reason
`display04`, the main regression table, is produced from a report delivered off the CMS secure server. Its numbers are movable and its run is not, so no command in this repository can regenerate it.

That is provenance, not a defect, and it must be written down. "Cannot rebuild, because the run is on the secure server and the report is dated v0618" tells a reader that a stale number is a data fact rather than a rendering bug. An empty `source/` tells them nothing, which is how four MISQ units sat unrebuildable without anyone noticing.

### Why this is a page and not a field on QD2
`QD2`'s result bundle is ② ⑦ ⑧. It cannot carry ① because the renderer is handed evidence rather than producing it, and it cannot carry ④ because the citing sentence does not exist when the render runs. The chain is therefore the join between the display family and the sentence family, which is why it sits between them rather than inside either.

### The failure it exists to prevent
This is not hypothetical. On 2026-07-21 a ruling flipped a section's primary exposure from a continuous score to a binary indicator. The prose was updated. The results table was not, because its numbers had been hand-authored and nothing linked them back to a producing run. The table silently contradicted the text it supported, and only a manual sweep caught it.

The rule that came out of it is binding: a consumer-side unit is GENERATED from the bank's `source_data.csv`, and hand-typing numbers into a unit's `.tex` is a defect rather than a shortcut. The chain is what makes that rule checkable instead of merely stated.

### The diagnostic the chain gives you
```
 ① empty AND ⑧ exists     the numbers were typed. This is the defect above.
 ⑧ not what ③ references  the manuscript is showing a superseded asset
 ⑦ missing                nobody can rebuild it, including the person who made it
 ④ empty                  an uncited display: a leftover, not a display
```

Each of those is a question a reader of a finished unit would otherwise have to ask by hand.

## Items to Finish
- [x] 🔗 The chain is defined and proven on a real unit
      `S-Display-2` on the MISQ paper carries all six links and its seven paths resolve.
- [x] 📐 The chain is in the page template
      New display pages are born with it, and a link that does not exist yet is written `(none yet)` with a reason.
- [ ] 🧪 Resolve links ② to ③ automatically
      They are inside one directory, so this is the same check that settles stage-contract paths. Until it exists, a chain is true on the day it was written.
- [ ] 📐 Carry ① through the render bundle
      `QD2`'s result schema should name the producing run, so a rendered unit cannot come back without one.
- [x] 🧠 ④ points at the SENTENCE
      Already ruled on `QC0`, which is settled: a `>` line directly under a sentence attaches to that sentence, and `QC3` and `QC4` ride that one rule rather than inventing their own. So ④ is not an open question here; it inherits.
      `S-Display-2` writes `S-Main-7 · §6 P5`, which names the paragraph. The sentence is identified by the `> Display:` lane sitting under it, not by a coordinate in this chain.

## Where we are
Defined, templated, and demonstrated once on the MISQ paper's gradient figure, where it immediately surfaced that the accepted candidate had never been promoted, so the compiled manuscript was showing the superseded figure. That is the class of thing the chain is for.

Nothing checks it yet. Four of the six links are mechanically checkable and none of them are checked today.

## Files
- `paper/1-lifecycle/haipipe-paper-stage/stages/4-display/template.md`
  The per-asset page template that carries the chain.
- `paper/1-lifecycle/haipipe-paper-stage/stages/4-display/stage.md`
  `display_split: binding`, the bank and consumer halves that link ① separates.
- `display/ref/display-unit-output-contract.md`
  The invariant that numbers come from a task and never from the renderer.

## Log
260726 · opened, from the display work on the MISQ paper. The chain and the thirteen-condition completeness checklist were built there first and generalized here.
