---
name: haipipe-page-for-dash-display
description: >-
  The VARIANT contract for the DISPLAY DASH page, one per paper: the single rollup over every display unit, carrying the WIRING map from unit to LaTeX label to the citing sentence to the shipped PDF, plus a reader-order rehearsal walked in the venue's own section order. It loads haipipe-page for the base frame and haipipe-page-for-stage for the family grammar, then adds only what a display dash needs: the wiring map no unit page can hold, the rehearsal that reads displays in the order a reader meets them, and the requirement to read S-Open-Venue because reader order IS the desk's section structure. Use when writing or fixing a display dash, when an accepted unit reaches no sentence, when a float prints ?? in the built PDF, or when the rehearsal has drifted out of the venue's section order. Trigger: display dash, S-Display-Dash, dash page, wiring map, reader order, rehearsal, placement, float, shipped PDF, /haipipe-page-for-dash-display.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-09"
  summary: "First cut, on JL's 260809 ruling that each multi-unit paper family gets a dash and every dash reads the venue structure."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-for-dash-display · where every display stands, in the order a reader meets it

**LOAD TWO CONTRACTS FIRST.** `haipipe-page` owns the base frame; `haipipe-page-for-stage` owns the family grammar and the managed Stage Contract span. This file adds only the display-dash overlay.

**The kind this variant covers**: one dash per display family.

```
kind      subject                                closes when
──────────────────────────────────────────────────────────────────────
Display   EVERY display unit at once, wired      never · a dash has no gate
dash      end to end and walked in reader order  and is regenerated each run
```

**The type key.** A display dash declares `page-type: dash` in its frontmatter, REQUIRED, because it wears a stage filename (`S-Display-Dash.md`). The family in the filename picks this contract.

## 🔌 The wiring map: four hops, and a unit is only finished at the fourth

A display unit page carries its own acceptance. What it cannot see is whether the accepted unit actually reaches a reader, because that answer lives in four different files.

```
① UNIT      the display page and its folder        for-display owns this
② LABEL     the \label inside float.tex
③ SENTENCE  the \ref in the section that cites it  for-section owns this
④ PDF       the float actually printed in the built paper

🚫 a unit green at ① and dark at ③ is the failure this map exists to catch:
   accepted, rendered, and cited by nobody
🚫 a float nothing \inputs prints ?? however finished the unit is
```

No unit page can hold this map, because every hop after ① lives outside the unit. That is exactly the dash test.

## 🏛 Why a display dash reads the venue, and what "reader order" means

The rehearsal walks the displays in the order a reader meets them, and that order is not the display family's order. It is the desk's section structure, allocated by the venue stage.

```
S-Open-Venue     the blueprint · the section list, in reader order
      │
      ▼
S-Display-Dash   §0 Abstract · §1 Introduction · §2 Literature · …
                 each division holding the displays that land in that section,
                 with the current preview and a plain-language placement comment
```

That is why the real page is divided by `§n` and not by unit id, and why the dash declares `requires: S-Open-Venue` (JL 260809). Re-sectioning at a new desk re-orders this page, which is the correct blast radius: a retarget really does change where every figure lands.

## 🎭 What the rehearsal is FOR, and what it may not become

```
✅ REHEARSAL     the display-relevant beat of each section, then the current
                 preview, then a plain comment on whether it lands there
🚫 NOT A COPY    never the section's prose, and never the unit's caption:
                 both have owners, and a copy drifts within the week
🚫 NOT A GATE    acceptance of a render is the UNIT page's human gate
                 (for-display, rung ④) and never happens here
```

## 🤖 Generated map, authored rehearsal

This dash is the one that mixes both, so the split has to be stated.

```
🤖 GENERATED   the wiring map · unit, label, citing sentence, shipped-or-not
✍️ AUTHORED    the rehearsal comment on each section: does this display land
               where the argument needs it
```

An authored line inside the generated map is overwritten on the next run. Put judgment in the rehearsal, never in the map.

## 🕳 An empty cell is a STATUS, never a blank

```
⬜ requested, nothing rendered      🧠 rendered, waiting on acceptance
📭 accepted but cited by NO sentence     ← the map's whole reason to exist
❓ cited but the float prints ?? in the built PDF
```

## 📥📤 What this page reads, and what it hands on

**A page is a unit of work** (`QB6` §7).

```text
 📥 INPUT   every S-Display unit page and its folder (float.tex, preview)
            every section page's \ref citations
            the built PDF, for whether the float actually printed
            S-Open-Venue's blueprint, for reader order

 📤 OUTPUT  ✗ no artifact. The output is the wiring map plus the rehearsal,
            read by a person deciding what is still unwired.
```

`haipipe-board/cli/display-report.py` produces the display-to-section map this dash carries; the dash is where a person reads it in reader order with a comment attached.

## 📂 Files

```
haipipe-page-for-dash-display/
├── SKILL.md            this variant contract
└── CHANGELOG.md        version history
```

Owns no scripts. The base is `haipipe-page`; the family grammar is `haipipe-page-for-stage`; the unit contract is `haipipe-page-for-display`; the sentence that cites a unit belongs to `haipipe-page-for-section`; the live specimen is the MISQ paper's `0-lifecycle/S05-display/S-Display-Dash.md`.
