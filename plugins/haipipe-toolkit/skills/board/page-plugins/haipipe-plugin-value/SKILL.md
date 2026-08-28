---
name: haipipe-plugin-value
description: >-
  The 🧮 value surface of a Board page: every number the page owes or uses, one
  row each, joining each probe card's ## Values block to the PP<NN>.v<n>
  citations in the prose. No storage of its own. Answers which number came
  from where, and which answered number nobody uses. Trigger: value plugin,
  value tab, PP01.v2, unsourced number, cite a number, /haipipe-plugin-value.
metadata:
  version: "0.1.1"
  last_updated: "2026-08-19"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-plugin-value · every number, and where it came from

**LOAD `haipipe-plugin` FIRST**, then `haipipe-plugin-probe` for the card and its
`## Values` block. This file owns only the delta: the join, the surface, and the
two failures it makes visible.

## 🎛 The gap it closes

A probe card is ONE question. Its answer usually holds SEVERAL numbers, and a
sentence uses one of them (JL 260819: "probe 是一个大 folder，里面放了所有的
value，而有的时候我们在正文里面只会用到一个具体的 value").

```text
  probe/PP01-phase-contract-count/     one question, four numbers
    v1  phases the loop declares   7
    v2  contracts that ship        6
    v3  person-reserved ticks      5
    v4  runs executed              → not here, PP02 owns it

  §1  uses v1     §13 uses v4
```

Until 260819 both sentences could only write `[PP01]`, so nobody could tell which
number each used, and a value nobody used looked exactly like one everybody did.

## 🧊 Four facets, and only two of them exist

```text
📦 storage   NONE. The number lives in probe/PP<NN>/proof/ with its source, run
             and sha256. A <page>/value/ folder would be a second home for one
             thing, which is the rule that retired the proof mark on 260819 (its glyph 🧮 now means value here).
📡 surface   THIS. One row per value on the page, read live on every open.
✍️ writer    NOBODY. EVIDENCE writes the `## Values` block in card.md when the
             answer lands. This surface never writes and calls no model.
🚧 boundary  reads probe/*/card.md and the page's own .md. Nothing else.
```

**Storage-less is not a new idea on this board**: `haipipe-plugin-outline` 0.1.0
shipped that way. The difference is that outline later grew a file because a plan
must exist before the thing it plans; a value cannot exist before its answer, so
it never will.

## 📐 The id, and where it is allocated

The grammar is `haipipe-plugin-probe` §🧮's and is not restated here beyond the
shape:

```text
  PP01.v2      card PP01, its second value
  ## Values    in card.md, written at EVIDENCE, never earlier
  - v2 · what the number IS · the number · where in proof/ it was read from
```

A row whose last field names no file is not a value; it is a number somebody
typed. The surface renders that as a named 🚨 rather than dropping the row.

## 🔗 The join runs BOTH ways, which is the whole point

```text
  🕳 UNSOURCED   the prose carries a number and cites no PP<NN>.v<n>
                 ← the failure this surface exists for
  🎈 UNUSED      a card holds a value no sentence cites
                 ← a question that was answered for nobody
  ✅ BOUND       both sides agree, and the row shows the number and its file
```

Both render as a named row, never as a blank, which is the same rule the probe
and display strips already carry.

## 📡 Surface · one parse, one table

`GET /_board/value?path=<board>&file=<page>` (`live/value.py`), drawer
`assets/js/10-drawer/08-plugin-value.js`, sorted `08-` so it sits after 🧭.

```text
  id        what it is                    number   from                 used by
  ─────────────────────────────────────────────────────────────────────────────
  PP01.v1   phases the loop declares      7        phase-census.json    §1
  PP01.v2   contracts that ship           6        phase-census.json    🎈 nobody
  PP05.v1   phases with a duration        0        why_empty            §15
```

`POST /_board/value` exists only so the shell's `tab: {url, write}` contract
holds; it writes nothing.

## 📂 Files

```
page-plugins/haipipe-plugin-value/
├── SKILL.md            this contract
└── CHANGELOG.md        version history
```

Owns no scripts of its own. The card, its states and the `## Values` grammar are
`haipipe-plugin-probe`'s; the four facets are `haipipe-plugin`'s; the phase that
writes a value is `page-workflows/haipipe-page-evidence`, stage ② BIND.

**The Board page that argues this contract** is `QPw4v-value` on
`BoardSkillBoard-260722`.
