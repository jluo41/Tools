---
name: haipipe-page-for-narrative
description: >-
  The VARIANT contract for the NARRATIVE page, one per paper: the page that holds what the paper claims, why this desk should care, the order those claims are argued in, and the section-by-section outline every Section page then executes. It loads haipipe-page for the base frame and haipipe-page-for-stage for the chain and gate, then adds only what narrative carries: the merged seed, claims and pitch material, the arc that decides which claim peaks, and the outline that applies the venue blueprint's allocation to that arc. It is venue-ALIGNED, so a retarget rewrites it. Use when writing or fixing a narrative page, when the argument order does not match what the desk rewards, when a claim has no section to land in, or when a section page is executing an outline nobody wrote. Trigger: narrative page, S-Work-N, argument order, arc, claim order, outline, seed, pitch, claims ledger, retarget, venue structure, /haipipe-page-for-narrative.
metadata:
  version: "0.1.1"
  last_updated: "2026-08-10"
  summary: "Narrative owns the claim-to-display selection gate: it selects Value or Literature candidates, while formal Paper Display retains acceptance and placement."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-for-narrative · the claims, their order, and the outline that follows

**LOAD TWO CONTRACTS FIRST.** `haipipe-page` owns the base frame; `haipipe-page-for-stage` owns the chain, the managed Stage Contract span, the venue transfer tiers, and the human gate. This file adds only the narrative overlay.

**The kind this variant covers**: one narrative per paper.

```
kind        subject                                closes when
──────────────────────────────────────────────────────────────────────
Narrative   what the paper claims · in what order  its human gate passes ·
            · and the outline that follows         one page, never per unit
```

**The type key.** A narrative page declares `page-type: narrative` in its frontmatter, and the line is REQUIRED: it wears an ordinary stage filename (`S-Work-N-narrative.md`) and IS a stage, so without the key it resolves as a plain stage page and loses this overlay. The `page-type:` key beats the filename (base, type resolution step ③), the same way a section unit declares `page-type: section`.

## 🎯 One page, four things that used to be four pages

JL merged seed, claims and pitch into narrative on 260809. The merge is not tidying: those four were always one act, split across four pages that each held a quarter of an argument and could not check themselves against the other three.

```
🌱 WHAT IS TRUE     the idea, and what the work actually establishes   (was seed)
📊 WHAT IS CLAIMED  the claim ledger: C1, C2, C3, each testable        (was claims)
📣 WHY THIS DESK    why these claims matter to THIS outlet's reader    (was pitch)
🎼 IN WHAT ORDER    the arc: which claim peaks, which sets it up,      (narrative)
                    which bounds it
📐 AND THEN         the section-by-section outline that follows
```

The real page already argued this before the merge was written. Its Opening asks: *"What argument order makes C1 the paper's peak while using C2 and C3 to establish consequence and boundary?"* That question cannot be answered without the ledger and cannot be asked without the desk, so the page was already carrying all four.

## 🆓📌 The venue-free core stays visible inside a venue-aligned page

`haipipe-page-for-stage` splits the lifecycle into venue-free and venue-aligned, and the merge crosses that line. Narrative as a whole is VENUE-ALIGNED: a retarget rewrites it. But part of what it now holds is true wherever the paper goes, and that part must stay separable or a retarget costs the idea as well as the arc.

```
🆓 SURVIVES A RETARGET   the claim ledger, and what the work establishes
                         ↳ its own Content division, and a retarget REREADS
                           it rather than rewriting it
🎯 REWRITTEN ON RETARGET the pitch, the arc, and the whole outline
                         ↳ these were written FOR one desk
```

A narrative page that cannot say which of its divisions survive a retarget has lost the property the old seed page existed to protect. State it on the page.

## 📐 The outline is where the blueprint meets the arc

This is what narrative hands downstream, and it is the reason narrative reads the venue rather than merely mentioning it.

```
S-Open-Venue      the blueprint · the section list and each section's allocation
      +
   the arc        which claim peaks, and what has to be true before it lands
      ▼
📐 THE OUTLINE    one row per section, in reader order:
                    which claim this section carries
                    what it must establish before the next one
                    its allocation from the blueprint
      ▼
S-Section-<unit>  each section page executes ITS row
```

The outline is the one arithmetic no other page can do: the venue stage knows the allocation but not the argument, and a section page knows its own row but not what the section before it established. A section written against no outline row is a section whose place in the arc nobody decided.

`stage.md` already declares this binding, so the contract only names it:

```
venue_aligned: true
venue_contract:
  read_first: S01-opening/S-Open-Venue.md   # Structural Blueprint beats + Writing Principles
```

## 🚫 What narrative may NOT do

```
🚫 write the prose      a section's sentences belong to its own page
🚫 bind a number        a value binding is the Value route's, by path
🚫 place a display      the display's placement record is its own
✅ decide the ORDER, and say what each section owes the one after it
```

The test: if a line would still be true after the sections were reordered, it is not narrative's line.

## 🎭 Phases, and the one that matters here

The base's four phases apply. PROBE is the one worth naming: an arc frequently depends on a fact the paper does not yet have, and the temptation is to write the arc as though the answer went the way you hope.

```
DRAFT   propose the ledger and the arc
PROBE   the arc rests on an unknown result · raise it and STOP
REVISE  land the answer, then re-cut the order if the answer changed it
CHECK   a human gate: does this order sell these claims to THIS desk
```

An arc built on an assumed result is the most expensive defect in the lifecycle, because every section executes it before anyone notices.

## 🖼 Claim-to-display selection, not evidence copying

Narrative does not carry raw evidence, binds no number, and places no float. It reads the candidate
Display cards paired with Value and Literature probes, then makes the rhetorical judgment that no
evidence page can make: whether a reader must **see** this result to understand a named claim.

```
candidate card       probe-linked table · figure · matrix · map, or not-displayable
        │
Narrative selection  name C<n> + role (punchline | support | boundary | background)
        │
Paper Display         requested formal unit, then sourced → rendered → human accepted → placed
```

The selection is a line in the relevant outline row: candidate path, claim id, role, and decision
(`selected` or `parked`). A selected card must already say what it lets the reader see. No card,
no selection; `not-displayable` is a decision Narrative respects rather than overrides.

## 📥📤 What this page reads, and what it hands on

**A page is a unit of work** (`QB6` §7).

```text
 📥 INPUT   S-Open-Venue's blueprint: the section list and each allocation
            the Value and Literature dashes, for what is actually established,
            still owed, and available to show as a candidate display

 📤 OUTPUT  ✗ no folder and no .tex. The output is the ORDER plus the outline:
              → every Section page reads its own outline row
              → selected candidate cards may open formal Paper Display requests
              → the Round stage reopens this page when a reviewer attacks
                the argument rather than a number
```

## 📂 Files

```
haipipe-page-for-narrative/
├── SKILL.md            this variant contract
└── CHANGELOG.md        version history
```

Owns no scripts. The base is `haipipe-page`; the chain and gate are `haipipe-page-for-stage`; the sections that execute the outline are `haipipe-page-for-section`; the blueprint it reads is written by the venue stage and catalogued by `haipipe-page-for-venue`; the live specimen is the MISQ paper's `0-lifecycle/S02-work/S-Work-N-narrative.md`.
