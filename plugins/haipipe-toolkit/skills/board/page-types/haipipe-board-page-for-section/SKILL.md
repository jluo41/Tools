---
name: haipipe-board-page-for-section
description: >-
  The VARIANT contract for a SECTION Page: one page per reader-ordered section unit of a paper or application, produced by a stage that runs once per unit. It loads haipipe-board-page for the base and haipipe-board-page-for-stage for the chain and gate, then adds only what a section page carries and a plain stage page does not: the section kind, the venue contract block whose blueprint line BINDS this unit alone, the template resolved per venue and kind, and the landing surface where citation, value, and display bindings reach prose. This is the type that CONNECTS to for-venue: the QBv catalog is read once by the venue stage, the blueprint allocates the desk's totals per section, and this page consumes its own allocation. Use when writing or fixing a section page, when its venue binding is wrong or missing, when a retarget must say what gets rewritten, or when a landed answer never reached the sentence that owed it. Trigger: section page, S-Main, S-Appendix, section kind, venue contract block, blueprint binds, word budget, section edit page, retarget section, /haipipe-board-page-for-section.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-05"
  summary: "First cut, on JL's 260805 admission. Rejected earlier as for-main; readmitted as for-section because section is cross-family and carries typed records for-stage does not."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board-page-for-section · one reader-ordered unit, bound to one venue allocation

**LOAD TWO CONTRACTS FIRST.** `haipipe-board-page` owns the base frame; `haipipe-board-page-for-stage` owns everything a chained, gated page needs: `requires` / `style-from` / `provides`, the managed Stage Contract span, the venue transfer tiers, and the rule that ONE stage reads the venue catalog. This file restates none of that; it adds only the section overlay, the same way `for-literature` adds a route over the topic core.

**The kind this variant covers**: one page per section UNIT, in any family that edits by section.

```
kind      produced by                          closes when
──────────────────────────────────────────────────────────────────────
Section   a stage declaring runs: per-unit,    ITS OWN human gate passes,
unit      one page per reader-ordered unit     judged against its venue floor
```

The paper family files these as `S-Main-<n>-<slug>` and `S-Appendix-<letter>-<slug>`; the application family's section-edit produces its own. "Section" is cross-family, which is why this type exists while `for-main` was rejected: Main names one family's region, section names a shape both have.

## 🔗 The venue chain, which is the reason this type exists

```
🗂 QBv<n> catalog     every desk's rules          for-venue owns this page
      │  read ONCE, by the venue stage
      ▼
📌 the blueprint      the desk's TOTALS allocated per section:
                      word budget · subsection count · density · H-assignments
      │  read by every section page
      ▼
✍️ THIS PAGE          ### Venue contract block · a POINTER, never a copy:
                      blueprint <- BINDING for this unit alone
                      style     <- reference only
                      override  <- a per-section desk rule outranks the blueprint,
                                   and the block SAYS whether one exists
```

The block is the typed record that makes this a type: no other stage page carries a per-unit venue binding. Its three lines answer the three questions a retarget asks: what binds, what merely advises, and what the desk itself said.

## 🎚 The section kind is a JOIN KEY, and the template is one of three things it joins

A section declares its KIND from a closed set the family owns (introduction, methods, results, discussion, appendix, and the set grows). The kind is not a label; it is the join key lining up three surfaces that were written at different times by different owners:

```
  section_kind = "theory"  joins
  ① the venue page's MATCHING DIVISION   for-venue cuts QBv Content by the
       (QBv1 · Sec-3-Theory)             venue's own reading index, so venue
                                         and section pages match division-to-division
  ② the blueprint's per-kind block       the allocation, BINDING for this unit
  ③ the (venue × kind) template          a MISQ introduction and a Nature
                                         introduction differ in SHAPE, not length
```

This join is what for-stage cannot provide and why this type exists: a stage page chains page-to-page; only a section page joins division-to-division with the venue's own catalog. The join stays TWO-HOP: ① is read by the venue stage alone, and this page consumes ② and ③. A section page never copies structure from a sibling section; it takes it from its own resolved template.

## 📥 The landing surface: where the three record types reach prose

A section page is where the other types' records become sentences:

```
citation binding   (for-literature)  →  the \citep on the claiming sentence
value binding      (for-value)       →  the number, with its provenance lane
display acceptance (for-display)     →  the \ref, and the placement record
                                        points back at THIS sentence
```

A binding that landed on its topic page but never reached the owing sentence is this page's open work, visible at its gate. The hole grammar itself is the phases' (`page-phases/`); this page only says where the paid debt lands.

## 🔁 What a retarget rewrites

A section page is venue-ALIGNED: retargeting the work to another venue rewrites the venue contract block, re-resolves the template, and re-judges the prose against the new floor, while the section's claims, evidence bindings, and unit identity survive. The split between what survives and what rewrites is `for-stage`'s venue-free against venue-aligned rule, applied at unit grain.

## 📂 Files

```
haipipe-board-page-for-section/
├── SKILL.md            this variant contract
└── CHANGELOG.md        version history
```

Owns no scripts. The frame is `haipipe-board-page-for-stage`; the catalog side is `haipipe-board-page-for-venue`; the record producers are `-for-literature`, `-for-value`, `-for-display`; the paper family's stage is `paper/S06-main/section-edit/stage.md`, which declares the closed kind set and the per-unit identity this contract requires but never contains.
