# Values lane · every number, and where it came from

Read this reference from `haipipe-plugin-outline` when a Page Evidence Item is
`VALUE`, or when the 🧭 Outline plugin's Evidence Workspace must explain a number's provenance. The
Outline plugin owns the lane and surface; `haipipe-plugin-probe` still owns
any legacy card whose `## Values` block supplies the value.

## 🎛 The gap it closes

A probe card is ONE question. Its answer usually holds SEVERAL numbers, and a
sentence uses one of them (JL 260819: "probe 是一个大 folder，里面放了所有的
value，而有的时候我们在正文里面只会用到一个具体的 value").

```text
  evidence/probe/PP01-phase-contract-count/  one question, four numbers
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
📦 storage   NONE. The number lives in evidence/probe/PP<NN>/proof/ with its source, run
             and sha256. A <page>/value/ folder would be a second home for one
             thing, which is the rule that retired the proof mark on 260819 (its glyph 🧮 now means value here).
📡 surface   the 🧮 Values segment of the 🧭 Outline plugin's Evidence Workspace. One row per
             value on the page, read live on every open.
✍️ writer    NOBODY. EVIDENCE writes the `## Values` block in card.md when the
             answer lands. This surface never writes and calls no model.
🚧 boundary  reads evidence/probe/*/card.md and the Page's own .md. Nothing else.
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

## 📡 Evidence segment · one parse, one table

`GET /_board/value?path=<board>&file=<page>` (`live/value.py`) remains the
compatibility route loaded inside the 🧭 Outline plugin's Evidence Workspace. It is not a
standalone Plugin surface.

```text
  id        what it is                    number   from                 used by
  ─────────────────────────────────────────────────────────────────────────────
  PP01.v1   phases the loop declares      7        phase-census.json    §1
  PP01.v2   contracts that ship           6        phase-census.json    🎈 nobody
  PP05.v1   phases with a duration        0        why_empty            §15
```

`POST /_board/value` exists only so the shell's `tab: {url, write}` contract
holds; it writes nothing.

## 📂 Files and ownership

This reference owns no scripts. `haipipe-plugin-outline` owns the Page-facing
lane and joined surface; the phase that binds a ready value is
`page-workflows/haipipe-page-evidence` at LAND. The card, its states, and any
legacy `## Values` grammar remain `haipipe-plugin-probe`'s until that storage
is migrated.

**The Board page that argues this contract** is `QPw4v-value` on
`BoardSkillBoard-260722`.
