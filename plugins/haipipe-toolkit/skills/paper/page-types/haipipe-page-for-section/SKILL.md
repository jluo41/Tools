---
name: haipipe-page-for-section
description: >-
  The VARIANT contract for a SECTION Page: one page per reader-ordered section unit of a paper or application, produced by a stage that runs once per unit. It loads haipipe-page for the base and haipipe-page-for-stage for the chain and gate, then adds only what a section page carries and a plain stage page does not: the section kind, the venue contract block whose blueprint line BINDS this unit alone, the template resolved per venue and kind, and the landing surface where citation, value, and display bindings reach prose. This is the type that CONNECTS to for-venue: the QBv catalog is read once by the venue stage, the blueprint allocates the desk's totals per section, and this page consumes its own allocation. Use when writing or fixing a section page, when its venue binding is wrong or missing, when a retarget must say what gets rewritten, or when a landed answer never reached the sentence that owed it. Trigger: section page, S-Main, S-Appendix, section kind, venue contract block, blueprint binds, word budget, section edit page, retarget section, /haipipe-page-for-section.
metadata:
  version: "0.1.1"
  last_updated: "2026-08-05"
  summary: "First cut, on JL's 260805 admission. Rejected earlier as for-main; readmitted as for-section because section is cross-family and carries typed records for-stage does not."
  outline:
    mode: resolved          # fixed | grammar | resolved
    source: "paper/venue/playbook-<pack>/<venue>/<venue>-<kind>/template.md (95 on disk)"
    shape: "resolved by (venue x kind): paragraph blocks with per-block budgets and anti-patterns"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-for-section · one reader-ordered unit, bound to one venue allocation

**LOAD TWO CONTRACTS FIRST.** `haipipe-page` owns the base frame; `haipipe-page-for-stage` owns everything a chained, gated page needs: `requires` / `style-from` / `provides`, the managed Stage Contract span, the venue transfer tiers, and the rule that ONE stage reads the venue catalog. This file restates none of that; it adds only the section overlay, the same way `for-literature` adds a route over the topic core.

**The kind this variant covers**: one page per section UNIT, in any family that edits by section.

```
kind      produced by                          closes when
──────────────────────────────────────────────────────────────────────
Section   a stage declaring runs: per-unit,    ITS OWN human gate passes,
unit      one page per reader-ordered unit     judged against its venue floor
```

The paper family files these as `S-Main-<n>-<slug>` and `S-Appendix-<letter>-<slug>`; the application family's section-edit produces its own. "Section" is cross-family, which is why this type exists while `for-main` was rejected: Main names one family's region, section names a shape both have.

**The type key.** A section page declares `page-type: section` in its frontmatter, and the line is REQUIRED: `S-Main-3-theory` is letter for letter a stage filename, and the key is what routes the page here instead of stopping at `-for-stage`. The `page-type:` key beats the filename (base, type resolution step ③).

## 🔗 The venue chain, which is the reason this type exists

The chain is drawn once, in `-for-stage`'s "ONE stage reads the venue page, and it is the venue stage": the QBv catalog is read once by the venue stage, the blueprint turns the desk's totals into per-section allocations, and every later page reads the blueprint. This page does not redraw it. What it adds is the unit grain: this page consumes ITS OWN allocation through its `### Venue contract` block, a POINTER and never a copy. The blueprint line is BINDING for this unit alone; the style line is reference only; the override line SAYS whether a per-section desk rule exists, because such a rule outranks the blueprint.

The block is the typed record that makes this a type. Other stage pages carry a venue contract block too, `S-Open-Pitch` among them; what no other stage page carries is one PER READER-ORDERED UNIT, allocating that unit's own budget and shape. Its three lines answer the three questions a retarget asks: what binds, what merely advises, and what the desk itself said.

## 🎚 The section kind is a JOIN KEY, and the template is one of three things it joins

A section declares its KIND from a closed set the family owns (introduction, methods, results, discussion, appendix, and the set grows). The kind is the one name that ties three things together: the venue division, the blueprint block, and the template. Three owners wrote them at different times, and the kind is what lines them up:

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

## 🗂 The outline is RESOLVED, and here is the one line that resolves it

This is the only Page Type whose outline comes from OUTSIDE itself, so it declares `outline: mode: resolved` and names the source rather than listing divisions (JL 260816: "page-for-section it is kind of different"). It is not thinner than the others; it is the RICHEST, because 95 of these templates are already written and each carries per-block budgets, arcs, and anti-patterns that no generic shape could hold.

**The path, resolvable in one step:**

```text
paper/venue/playbook-<pack>/<venue>/<venue>-<kind>/template.md

  MISQ + introduction  → playbook-utd-is/MISQ/MISQ-introduction/template.md
  npj DM + methods     → playbook-nature-portfolio/npj-digital-medicine/
                           npjdm-methods/template.md
```

```bash
# the outline this page must execute, resolved from its own two keys
ls paper/venue/playbook-*/"$VENUE"/"$VENUE"-"$KIND"/template.md
```

**What arrives is a fillable skeleton, not a description.** The MISQ introduction template hands over `### P1. Phenomenon hook -- why this matters now`, `### P2. (optional) Deepen the stakes`, `### P3. What is known -- brief positioning`, each with its paragraph budget (~4-6 sentences, ~24-25 words each, citation density ~0.5/sentence clustered in the hook and contribution blocks) and its named anti-pattern ("do NOT open with a literature-review paragraph"). DRAFT's job here is to CHOOSE the variant and the ¶ counts against this paper's claim structure, not to invent an arc.

**A missing template is a HOLE, never an invented outline.** If `(venue × kind)` resolves to nothing, the venue pack owes one; say so and stop. Copying a sibling section's shape is the failure this type exists to prevent, because two sections of one paper have different jobs and the desk knows it.

## 📥 The landing surface: where the three record types reach prose

A section page is where the other types' records become sentences:

```
citation binding   (for-literature)  →  the \citep on the claiming sentence
value binding      (for-value)       →  the number, with its provenance lane
display acceptance (for-display)     →  the \ref, and the placement record
                                        points back at THIS sentence
```

A binding that landed on its topic page but never reached the owing sentence is this page's open work, visible at its gate. The hole grammar itself is the phases' (`page-workflows/`); this page only says where the paid debt lands.

## 🔁 What a retarget rewrites

A section page is venue-ALIGNED: retargeting the work to another venue rewrites the venue contract block, re-resolves the template, and re-judges the prose against the new floor, while the section's claims, evidence bindings, and unit identity survive. The split between what survives and what rewrites is `for-stage`'s venue-free against venue-aligned rule, applied at unit grain.

**The template.** NOT fixed here, and resolved by a PAIR, `(venue, section_kind)`. The venue page's matching `### Sec-<n>-<Kind>` division states the shape that desk expects, and the venue pack carries the skeleton. A MISQ introduction and a Nature introduction differ in SHAPE, not only in wording, so one template for this type would flatten the very difference a venue page exists to record. Both halves of the pair are declared in the page's own head, which is what makes the lookup mechanical rather than a hunt.

## 📥📤 What this page reads, and what it hands on

**A page is a unit of work** (`QB6` §7). A section page is the ONE type with no input folder, because its raw material is the prose on the page itself.

```text
 📥 INPUT   ✗ no folder. The material IS this page's own ## Content, plus the
            three bindings that LAND here from other pages:
              a citation binding  (for-literature)  → the \citep on the sentence
              a value binding     (for-value)       → the number, with provenance
              a display acceptance(for-display)     → the \ref, and the placement

 📤 OUTPUT  <paper root>/sections/<nn>_<slug>.tex   FLAT, and reader-ordered
              ▶ never a subdirectory: on the live MISQ paper
                `find sections appendices -type d` returns only the two roots
              ▶ the shipped filename carries the READER's number, never the
                board page id: S-Main-4-measurement.md ships 04_personality_extraction.tex
              ▶ the mapping is not 1:1: 8 S-Main pages, 14 files in sections/
```

The one line where this type touches the display type is an `\input` of a shipped float, for example `sections/05_data_variables.tex` reaching `displays/S-Display-3c-variable-operationalization/float.tex`. That is how a display reaches a reader, and a float nothing inputs prints `??` however finished the unit is.

## 📂 Files

```
haipipe-page-for-section/
├── SKILL.md            this variant contract
└── CHANGELOG.md        version history
```

Owns no scripts. The frame is `haipipe-page-for-stage`; the catalog side is `haipipe-page-for-venue`; the record producers are `-for-literature`, `-for-value`, `-for-display`; the paper family's stage is `paper/S06-main/section-edit/stage.md`, which declares the closed kind set and the per-unit identity this contract requires but never contains.
