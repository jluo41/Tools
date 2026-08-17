---
name: haipipe-page-for-dash
description: >-
  The VARIANT contract for a DASH Page: one page that shows EVERY unit of one family at once, measured against the venue, so a reader can tell which unit to work on next. It replaces the four per-family dash contracts merged on 260816, which shared one closing rule word for word. It loads haipipe-page for the base frame and adds only what a dash needs: the rule that a dash NEVER closes because it is regenerated each run, the required dash_family field naming which family it rolls up, the requirement to read the venue before measuring anything, the generated-versus-authored split, and the rule that an empty cell is a status rather than a blank. Use when writing or fixing a dash page, when a dash has started ruling something instead of measuring it, when a dash was hand-edited and the next build erased the edit, or when an empty cell was read as nothing to do. Trigger: dash page, S-Family-Dash, dash_family, rollup, which unit next, wiring map, inventory, gap contract, allocation, empty cell, regenerated, /haipipe-page-for-dash.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-16"
  summary: "The four per-family dash contracts merged into one on JL's 260816 ruling. dash_family: is promoted from a specimen-only fallback to a REQUIRED field on every dash."
  outline:
    mode: fixed          # fixed | grammar | resolved
    source: "this SKILL.md"
    shape: "regenerated every run; one row per unit of the declared dash_family"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-for-dash · every unit of one family at once, and never a gate

**LOAD `haipipe-page` FIRST.** It owns the base frame. What this file guards is MEASURING WITHOUT RULING: a dash shows a whole family against the venue so a person can pick what to do next, and the moment it decides something instead of showing it, the next build erases the decision.

**The kind this variant covers**: one page per FAMILY rollup.

```
kind    subject                              closes when
──────────────────────────────────────────────────────────────────────
Dash    EVERY unit of one family at once,    never · a dash has no gate
        measured against the venue           and is regenerated each run
```

**Why this is ONE contract and not four.** Until 260816 this type shipped as `for-dash-section`, `-value`, `-display` and `-literature`. Their `closes when` cells were identical, character for character, and so were their type key, their venue rule, their generated/authored split, and their empty-cell rule. Four contracts sharing one closing rule is one type whose family is a FIELD, not four types (JL 260816). What actually differed between them was payload, and payload lives in `### 2` below.

**The type key.** A dash declares `page-type: dash` in its frontmatter and the line is REQUIRED: a dash wears a stage filename (`S-Main-Dash.md`, `S-Value-Dash.md`), so without the key the resolver reads it as a plain stage page and loads the wrong contract. The `page-type:` key beats the filename (base, type resolution step ③).

**`dash_family:` is REQUIRED on every dash.** It was a specimen-only fallback while four contracts existed and the filename could pick between them; with one contract the filename picks nothing, so the field is the only thing that says which family this dash rolls up.

```
page-type: dash
dash_family: section | value | display | literature
```

A dash carrying a `S-<Family>-Dash` filename declares `dash_family:` anyway, and the two must agree. Two keys that can disagree is the defect the resolution table exists to prevent, so a mismatch is fixed on the page and never in the resolver.

## 🏛 A dash reads the VENUE, and that is what makes it a measurement

A dash that reports a family against nothing is a list. What turns a list into a dash is the yardstick, and the yardstick is the desk: the venue blueprint's allocation for sections, the venue's structure for which units are owed at all.

```
  venue blueprint  ━━▶  the allocation each unit is measured against
  the family       ━━▶  the units, read fresh from disk each run
  the dash         ══▶  unit × allocation, one row per unit
```

⚠️ Read the venue page BEFORE measuring. A dash built without it reports effort, not fit, and a family can be 100% complete against nothing.

## 🤖 Generated, and what that forbids

The rows are BUILT from the family's pages on every run. Anything typed into a generated row is gone at the next build, silently, and the page will look correct while it is wrong.

```
  🤖 GENERATED   the rows: unit · state · measurement · what is missing
                 🚫 never hand-edited · the build overwrites it
  ✍️ AUTHORED    the reading above the rows: what the SET adds up to,
                 which is the one thing a generator cannot compute
```

A dash rules NOTHING. It has no gate, no acceptance, no selection. When a dash's reading says a unit is wrong, the fix goes on the unit's own page, and the dash shows it fixed on the next run.

## 🕳 An empty cell is a STATUS, never a blank

This rule was written identically in all four merged contracts, which is how load-bearing it is.

```
  ✅ "—  no display requested"        a real state, read as such
  ❌ (blank)                          read as "nothing to do here"
```

A blank cell and a cell meaning "this unit owes nothing" look the same to a reader and mean opposite things. Every cell carries a value, and "none" is a value.

## 📦 What each family's dash carries

The shared rules above bind every dash. This is the payload that differs, one row per family, and the detail behind each row is preserved in `_archive/`:

```
dash_family    the family's units        what this dash's rows carry
──────────────────────────────────────────────────────────────────────────
section        every section page        the venue allocation per unit, and
                                         which unit to work on next
value          every page with a         the binding rule, the staleness rule,
               value/ plugin card        and the inventory of number sets
display        every page with a         the four-hop wiring map, and the
               display/ plugin unit      reader-order rehearsal
literature     every page with a         the gap the SET adds up to, and the
               bibex/ plugin entry       topic map every claim routes down
```

⚠️ The value, display and literature families are PLUGIN lanes, not Page Types: their per-unit contracts were retired on 260816 for carrying a property every page has. A dash over a plugin lane works exactly as before, because a dash rolls up what pages CARRY, never what type they wear.

## 📥📤 What this page reads, and what it hands on

```text
 📥 INPUT   the venue page          the yardstick, read once per run
            every unit of the family read fresh from disk, never a cached list
 📤 OUTPUT  one row per unit, plus the authored reading of what the SET means
            ▶ a person picks the next unit to work on, and goes to ITS page
```

## 📂 Files

```
haipipe-page-for-dash/
├── SKILL.md            this variant contract
└── CHANGELOG.md        version history

_archive/haipipe-page-for-dash-{section,value,display,literature}/
                        the four merged contracts, kept whole for their payload detail
```

Owns no scripts. The base is `haipipe-page`; the venue yardstick is `haipipe-page-for-venue`; the section family's units are `haipipe-page-for-section`; the other three families are plugin lanes owned by the board family (`<page>/display/`, `<page>/probe/`, `<page>/bibex/`).
