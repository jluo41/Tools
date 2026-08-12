---
name: haipipe-page-for-dash-literature
description: >-
  The VARIANT contract for the LITERATURE DASH page, one per paper: the single rollup over every Literature topic, carrying the literature map, the paper's gap contract, and the coverage check no topic page can perform. It loads haipipe-page for the base frame and haipipe-page-for-stage for the family grammar, then adds only what a literature dash needs: the gap contract that belongs to the whole concern rather than to any one topic, the map of which topic owns which claim, and the requirement to read S-Open-Venue because the desk decides how much related work the paper owes and where it sits. Use when writing or fixing a literature dash, when a novelty claim rests on no topic, when the gap contract is restated differently on two topic pages, or when the dash has started arguing a topic instead of mapping it. Trigger: literature dash, S-Literature-Dash, dash page, gap contract, literature map, topic coverage, novelty, related work, /haipipe-page-for-dash-literature.
metadata:
  version: "0.2.0"
  last_updated: "2026-08-10"
  summary: "Literature Dash now rolls up both the gap map and the candidate Literature Display queue paired with every probe."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-for-dash-literature · the topics this paper has, and the gap they add up to

**LOAD TWO CONTRACTS FIRST.** `haipipe-page` owns the base frame; `haipipe-page-for-stage` owns the family grammar and the managed Stage Contract span. This file adds only the literature-dash overlay.

**The kind this variant covers**: one dash per literature family.

```
kind         subject                             closes when
──────────────────────────────────────────────────────────────────────
Literature   EVERY Literature topic at once,     never · a dash has no gate
dash         plus the gap the set adds up to     and is regenerated each run
```

**The type key.** A literature dash declares `page-type: dash` in its frontmatter, REQUIRED, because it wears a stage filename (`S-Literature-Dash.md`). The family in the filename picks this contract.

## 🕳 The gap contract belongs to the CONCERN, not to a topic

This is the rule that makes the page exist. A paper's gap is a single statement: what is not known, and why this paper is the thing that closes it. Four topic pages each cover part of the field, and NONE of them can state the gap, because a gap is the shape of what all four leave uncovered.

```
✅ BELONGS HERE   the gap contract, stated once for the whole concern
✅ BELONGS HERE   which topic owns which claim, and which claim no topic owns
🚫 BELONGS THERE  a topic's own sources, its own verdicts, its own answers
```

A gap contract restated on a topic page is a second authority that will drift, and the drift is invisible because both copies read plausibly.

## 🖼 The Literature Display queue

Every Literature probe has one same-numbered candidate card. The dash rolls up the card's `state`,
takeaway, claim, and role, so the paper can see which positioning findings want a literature matrix
or map. It does not turn the card into a second citation digest or a final float.

```
probe answer → candidate Literature Display → Narrative selection → Paper Display request
                     candidate | parked | not-displayable
```

`not-displayable` is a valid, useful result. A `selected` card must name the claim it serves; a
`paper-bound` card must point to its formal Display unit. A missing card is a management defect,
not an implicit decision that the evidence cannot be shown.

## 🏛 Why a literature dash reads the venue

How much related work a paper owes, and whether it sits in its own section or is threaded through the theory, is the desk's decision, not the field's.

```
S-Open-Venue     the blueprint · whether §2 Literature exists, how long it is,
                 and the citation density the desk's papers carry
      │
      ▼
S-Literature-    the topic set checked against that: enough topics to fill what
Dash             the desk expects, and the gap stated in the register the desk
                 publishes in
```

So the dash declares `requires: S-Open-Venue` (JL 260809). Before this rule the real page declared `requires: S-Open-Seed` alone, which told it what the paper is about and nothing about what the desk expects it to cover.

Note the split `haipipe-page-for-stage` draws: citation density is a REPORTED row copied from the pack, not a binding one. The dash shows the number against the desk's measurement and never colours a miss as a failure.

## 🗺 The map, and the route it sends every claim down

```
topic → the page that owns it → its QA-probe records → the discovery bank
```

The dash names each topic and points; it never carries a source, a verdict, or an answer. That is the outward route's own machinery and it lives on the topic page, one click away.

## 🕳 An empty cell is a STATUS, never a blank

```
⬜ topic opened, nothing collected yet
🧠 answers landed, waiting on a person to turn them into positioning
📭 a claim the paper makes that NO topic covers   ← a finding, not a blank
❄️ deliberately out of scope, with the reason on the row
```

## 📥📤 What this page reads, and what it hands on

**A page is a unit of work** (`QB6` §7).

```text
 📥 INPUT   every Literature topic page: its E divisions, its QA-probe bindings
              into the discovery bank, and the same-numbered candidate Display cards
            S-Open-Seed, for what the paper claims
            S-Open-Venue's blueprint, for what the desk expects

 📤 OUTPUT  the gap contract, which the seed, pitch and section pages cite
            rather than restate · plus the topic map
```

## 📂 Files

```
haipipe-page-for-dash-literature/
├── SKILL.md            this variant contract
└── CHANGELOG.md        version history
```

Owns no scripts. The base is `haipipe-page`; the family grammar is `haipipe-page-for-stage`; the unit contract is `haipipe-page-for-literature`; the candidate-card contract is `haipipe-board/ref/topic-display-card.md`; the QA-probe anatomy is `haipipe-board/ref/topic-entry-contract.md`; the live specimen is the MISQ paper's `0-lifecycle/S03-literature/S-Literature-Dash.md`.
