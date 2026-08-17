---
name: haipipe-page-for-dash-section
description: >-
  The VARIANT contract for the SECTION DASH page, one per paper: the single rollup over the whole section family that answers which section to work on next. It loads haipipe-page for the base frame and haipipe-page-for-stage for the family grammar, then adds only what a dash needs: it is GENERATED and never argued, it decides nothing so it takes no human gate and is never counted as settled, and it requires S-Open-Venue because the only yardstick that ranks nine sections against each other is the venue blueprint's per-section allocation. Use when writing or fixing a section dash, when the dash reports a section green that its own page calls open, when a priority is stated with no measurement behind it, or when the dash has drifted into arguing instead of measuring. Trigger: section dash, S-Main-Dash, S-Appendix-Dash, dash page, section set quality, which section next, blueprint allocation, word floor, family rollup, /haipipe-page-for-dash-section.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-09"
  summary: "First cut, on JL's 260809 ruling that each multi-unit paper family gets a dash and every dash reads the venue structure."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-for-dash-section · the one page that can rank the sections

**LOAD TWO CONTRACTS FIRST.** `haipipe-page` owns the base frame; `haipipe-page-for-stage` owns the family grammar, the managed Stage Contract span, and the venue transfer tiers. This file adds only the dash overlay, and it never restates a rule either of those already carries.

**The kind this variant covers**: one dash per section family, and Appendix is not a second family.

```
kind        subject                              closes when
──────────────────────────────────────────────────────────────────────
Section     EVERY section page at once, ranked   never · a dash has no gate
dash        against the venue blueprint          and is regenerated each run
```

**Section INCLUDES Appendix, and always did (JL 260809).** One stage row, `section-edit`, runs once per unit and produces every page in both; one Page Type, `haipipe-page-for-section`, governs them; the only difference is the reader-order key, a number for the body and a letter for the appendix. `haipipe-page-for-stage` counted them as two families and had to write "Main or Appendix, per section_kind" to describe one stage. So ONE dash ranks all of them, and `S-Main-Dash` and `S-Appendix-Dash` both resolve here. A paper that keeps two dash pages is measuring one family twice and will report two different answers to "which unit next".

**The type key.** A dash declares `page-type: dash` in its frontmatter, and the line is REQUIRED. A dash wears a stage filename (`S-Main-Dash.md`), so without the key the resolver reads it as a plain stage page and loads the wrong contract. The `page-type:` key beats the filename (base, type resolution step ③); the family in the filename then picks which of the four dash contracts applies, so `S-Main-Dash` and `S-Appendix-Dash` both resolve here.

## 📏 What a dash is FOR, and the one test that keeps it honest

A dash holds ONLY what no single page in its family can hold. `S-Main-Dash` states its own job in its `method:` line, and it is the clearest statement of the type anywhere on the board:

> measure the nine section pages against the venue contract, generated on every run, and hold only what no single section page can hold

The test follows from that sentence. Before any row goes on a dash, ask whether one section page could carry it alone. If it could, it belongs on that page, and a copy here will disagree with the original within the week.

```
✅ BELONGS HERE   section 3 is at 62% of its floor while section 6 is at 140%
                  the comparison exists nowhere else, because comparison needs all nine
✅ BELONGS HERE   two sections both claim to carry C2, and no page can see the clash
🚫 BELONGS THERE  section 3's own word count, its own state, its own open rows
```

## 🏛 Why a dash REQUIRES the venue, and what that overturns

Nine pages each know their own state. None can say which one to work on next, because "next" is a ranking and a ranking needs one shared yardstick. The yardstick is the venue blueprint's per-section allocation, written once by the venue stage.

```
S-Open-Venue          the blueprint · this paper's per-section allocation
      │  read by the dash, once per regeneration
      ▼
S-Main-Dash           each section measured against ITS OWN allocation,
                      then ranked against each other
```

So the dash declares `requires: S-Open-Venue` (JL 260809: every dash considers the venue structure).

**This overturns one shipped line, deliberately.** `haipipe-page-for-stage` said a dash never takes a gate, `requires:`, or `provides:`. Two of those still hold and one does not, because the old line conflated two different things:

```
✅ STILL TRUE   no human GATE · a dash decides nothing, so nothing is ruled here
✅ STILL TRUE   never counted in a board's settled totals
🚫 OVERTURNED   no `requires:` · a dash cannot measure without the blueprint,
                and S-Display-Dash already declared `requires: S-Open-Venue`
                while three sibling dashes declared nothing
```

A `provides:` is allowed but rarely earned: what a dash hands downstream is a reading, not an artifact, and a downstream page that needs the reading can read the dash.

## 🤖 Generated, and what that forbids

The dash is regenerated on every run. That is not a performance note, it is the rule that keeps it true.

```
🤖 GENERATED   the roster · each section's state · its measurement against the
               allocation · the ranking that falls out of both
✍️ AUTHORED    only what the generator cannot reach: why a ranking is being
               overridden this week, and a named exception with its reason
🚫 NEVER       argument · a decision · a claim about one section that its own
               page does not already carry
```

An authored line that the next regeneration would contradict is a defect. Put it on the section page, or put it in this page's `## Log` where regeneration does not reach.

## 📊 Measured against the allocation, and only the binding rows bind

`haipipe-page-for-stage` splits the blueprint into rows that BIND and rows that REPORT, and the dash must carry that split visibly or it manufactures false alarms.

```
⚖️ BINDS     subsection count · H-assignments · which claim each subsection
             carries · the displays it owes
             ↳ a miss is a real finding the dash raises
📊 REPORTS   word floor · sentences per paragraph · citation density
             ↳ a miss is a measurement, shown with its number and never
               coloured as a failure
```

A dash that paints a word-floor shortfall red is reading an inherited measurement as a gate, which is the exact error the split exists to prevent. Show the number, show the floor, and let a person judge.

## 🕳 An empty cell is a STATUS, never a blank

A section with no measurement yet says so. A blank cell reads as zero, and zero reads as done.

```
⬜ not started      ❄️ on ice, on purpose      🧠 waiting on a person
📭 no allocation    the blueprint has no row for this section, which is a
                    finding about the BLUEPRINT and belongs in the dash
```

## 📥📤 What this page reads, and what it hands on

**A page is a unit of work** (`QB6` §7). A dash reads many pages and hands on a reading.

```text
 📥 INPUT   every S-Main-<n> and S-Appendix-<letter> page in the family:
              its `state:`, its Aims and States, its own measurements
            plus S-Open-Venue's blueprint block, the yardstick

 📤 OUTPUT  ✗ no artifact and no folder. The output is the ranking a person
            reads to choose the next section, and it lives on this page only.
```

The dash never writes to a section page. If a section is wrong, the finding is routed to that page and fixed there; a dash that repairs its members stops being a measurement of them.

## 📂 Files

```
haipipe-page-for-dash-section/
├── SKILL.md            this variant contract
└── CHANGELOG.md        version history
```

Owns no scripts. The base is `haipipe-page`; the family grammar is `haipipe-page-for-stage`; the unit contract for what this dash measures is `haipipe-page-for-section`; the blueprint it reads is written by the venue stage and catalogued by `haipipe-page-for-venue`.
