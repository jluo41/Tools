---
name: haipipe-page-for-dash-value
description: >-
  The VARIANT contract for the VALUE DASH page, one per paper: the single rollup over every Value topic, holding the binding rule, the staleness rule, and the inventory of number sets this paper asks a reader to believe. It loads haipipe-page for the base frame and haipipe-page-for-stage for the family grammar, then adds only what a value dash needs: the rule that makes a number BOUND, the rule that makes a bound number STALE, the topic inventory no single topic page can hold, and the requirement to read S-Open-Venue because the desk's structure decides which sections owe numbers at all. Use when writing or fixing a value dash, when a number is quoted with no run behind it, when a rerun silently invalidated a bound value, or when the dash has started restating what a topic page already says. Trigger: value dash, S-Value-Dash, dash page, binding rule, staleness, value inventory, which numbers this paper owes, task route, /haipipe-page-for-dash-value.
metadata:
  version: "0.2.0"
  last_updated: "2026-08-10"
  summary: "Value Dash now rolls up both binding status and the candidate Value Display queue paired with every probe."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-for-dash-value · which numbers this paper owes, and what makes one bound

**LOAD TWO CONTRACTS FIRST.** `haipipe-page` owns the base frame; `haipipe-page-for-stage` owns the family grammar and the managed Stage Contract span. This file adds only the value-dash overlay.

**The kind this variant covers**: one dash per value family.

```
kind      subject                                closes when
──────────────────────────────────────────────────────────────────────
Value     EVERY Value topic at once, plus the    never · a dash has no gate
dash      rules that govern all of them          and is regenerated each run
```

**The type key.** A value dash declares `page-type: dash` in its frontmatter, and the line is REQUIRED, because the page wears a stage filename (`S-Value-Dash.md`) and would otherwise resolve as a plain stage page. The family in the filename picks this contract.

## 📦 Value absorbs RESOURCE (JL 260809)

There is no separate resource family. A resource page asked "what do we actually have to draw on", and that is an INWARD question answered by the task bank, which is the Value route's whole definition.

The evidence for the merge was already on the real pages: `S-Work-R1-cms` points at `tasks/A11_CMS-pipeline/A01_cms_pipeline/` and sits at `🔴 EVIDENCE pending`, with no `route:` line and no `E` divisions. It was an inward evidence page that never adopted the inward contract.

```
what it asks                          what it is
────────────────────────────────────────────────────────────────
"what does the CMS extract contain?"  an inward question · an INVENTORY answer
"what is the coefficient for C1?"     an inward question · a BINDING answer
                                      ↳ same route · same bank · same QA-probe
```

So the dash inventories both kinds, and the difference is what the answer looks like, never which machinery carries it. An inventory answer binds no claim and is complete when the topic can state what exists and what it does not.

## ⚖️ The two rules that live here and nowhere else

A Value topic page holds its own numbers. What no topic page can hold is the RULE that governs all of them, because a rule stated on four pages is four rules that will disagree.

```
🔗 THE BINDING RULE     what makes a number BOUND rather than quoted:
                        a target path to a QA-bank file that resolves, plus the
                        run that produced it, plus the claim it serves
🕰 THE STALENESS RULE   what makes a bound number STOP being bound:
                        the run was re-executed, the specification changed, or
                        the cohort was recut, and the binding was not re-read
```

Both rules are AUTHORED, not generated, and they are the reason this page survives regeneration. Everything else on the dash is a measurement against them.

## 🖼 The Value Display queue

Every Value probe has one same-numbered candidate card. The dash rolls up the card's `state`,
takeaway, claim, and role, so the paper can see whether a useful number is visible as a proposed
table or figure. It does not redraw the card or turn a candidate into a final float.

```
probe answer → candidate Value Display → Narrative selection → Paper Display request
                    candidate | parked | not-displayable
```

`not-displayable` is a valid, useful result. A `selected` card must name the claim it serves; a
`paper-bound` card must point to its formal Display unit. A missing card is a management defect,
not an implicit decision that the evidence cannot be shown.

## 🏛 Why a value dash reads the venue

A number is not owed in the abstract. It is owed because some section has to state it, and which sections exist is the desk's decision, written into the blueprint by the venue stage.

```
S-Open-Venue     the blueprint · which sections exist, and what each one owes
      │
      ▼
S-Value-Dash     the inventory, checked against that: a section the desk
                 requires whose numbers no topic covers is a GAP, and only
                 the dash can see it, because a topic page knows its own
                 numbers and not the section list
```

So the dash declares `requires: S-Open-Venue` (JL 260809). This is what turns the inventory from a list into a coverage statement.

## 📋 The inventory, and the line it must not cross

```
✅ BELONGS HERE   the topic roster · how the topics were cut · which topic
                  covers which claim · which sections are covered by none
✅ BELONGS HERE   the count of bound, unbound and stale across all topics
🚫 BELONGS THERE  a topic's own numbers, its own open rows, its own answers
```

The dash names each topic and sends every claim down to the page that owns it. A dash that restates a topic's numbers has made a copy, and a copy of a number is the exact failure the binding rule exists to prevent.

## 🕳 An empty cell is a STATUS, never a blank

```
⬜ no topic opened yet for this claim
🧠 bound, waiting on a person to accept the run
❄️ deliberately deferred, with the reason on the row
📭 the desk requires a section that no topic serves  ← a finding, not a blank
```

## 📥📤 What this page reads, and what it hands on

**A page is a unit of work** (`QB6` §7).

```text
 📥 INPUT   every Value topic page in the family: its E divisions, its QA-probe
              bank bindings, and the same-numbered candidate Display cards
            plus S-Open-Venue's blueprint, for which sections owe numbers

 📤 OUTPUT  ✗ no artifact. The output is the coverage reading plus the two
            rules, which downstream pages cite rather than restate.
```

The dash never edits a topic page or a QA-probe. A wrong binding is routed to the topic that owns it.

## 📂 Files

```
haipipe-page-for-dash-value/
├── SKILL.md            this variant contract
└── CHANGELOG.md        version history
```

Owns no scripts. The base is `haipipe-page`; the family grammar is `haipipe-page-for-stage`; the unit contract is `haipipe-page-for-value`; the candidate-card contract is `haipipe-board/ref/topic-display-card.md`; the QA-probe anatomy is `haipipe-board/ref/topic-entry-contract.md`; the live specimen is the MISQ paper's `0-lifecycle/S04-value/S-Value-Dash.md`.
