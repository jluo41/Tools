---
name: diagram-ascii
description: Fast emoji-rich ASCII diagrams for brainstorming, folder/code overviews, and experiment progress tracking. Use when the user wants to sketch an idea, map a codebase, visualize a flow inline during discussion, or show pipeline progress. Output is plain-text with liberal emoji for visual punch.
---

# /diagram-ascii — Brainstorm & Progress Diagrams

**Purpose**: quickly sketch ideas and track progress as emoji-rich ASCII. Optimized for speed, readability, and scannability — not mechanical precision. For complex diagrams with many crossing arrows, suggest Mermaid instead.

**🎨 Emoji-first — use as many as possible.** Emoji are the **primary visual scaffolding** of every diagram in this skill, not decoration. Use them densely: 📦 every box, 🏷️ every header cell, 📋 every row label, 🟢 every status indicator. More is better than fewer. Mix categories freely — a diagram packed with 6+ emoji types is the goal, not a problem. If you can put an emoji somewhere, do.

**Gallery (`ref/`)** — full worked examples. Read the relevant file when an inline template isn't enough:

| File | Use for |
|---|---|
| `ref/01-pipeline.txt` | left→right flows, branched, with error path |
| `ref/02-layered-arch.txt` | 3-tier / 5-tier / event-driven systems |
| `ref/03-folder-tree.txt` | 4 variants: basic / annotated / grouped / combined; before-after refactor |
| `ref/04-table.txt` | status table, comparison matrix, decision log, risk grid |
| `ref/05-progress-tracker.txt` | experiment dashboard, multi-run grid, burn-down |
| `ref/06-numbered-series.txt` | multi-diagram answers with `[N/TOTAL]` headers |
| `ref/07-task-progress.md` | daily progress log (`YYMMDD-progress.md`) |
| `ref/08-paper-section.txt` | argument-style diagram for a paper method section (progression + contrast + synthesis combined) |

## When to Use
- Mid-discussion idea plotting — "sketch how this works"
- Folder / codebase → visual overview
- Experiment progress tracking (pipeline stages, status grids)
- Any text diagram where emoji add scannable meaning

## When to Defer
- Crossing arrows → suggest Mermaid
- User wants a rendered image → suggest Mermaid / PlantUML / image tool
- More than ~20 nodes → split into sub-diagrams or use a real diagramming tool

## Inputs

| Input | Upstream step | Output shape |
|---|---|---|
| Natural language | Extract nouns → boxes, verbs → arrows | Inline sketch |
| Folder path | Glob top-level dirs; peek README | Tree, `.txt` file |
| Code area | Grep imports/calls; map modules | `architecture.txt` |
| Experiment run | Capture stages + their current state | `progress.txt` |
| Ongoing discussion | Capture the concept just named | Inline block, no file |

## Output

- **Inline (brainstorm default)**: fenced ```` ```text ```` block in chat.
- **Saved file**: `.txt` (never `.md` — markdown breaks monospace alignment).

## Save Location

- **User specifies the path when invoking this skill.** Example: *"sketch the pipeline and save to `examples/hainn-v0319/architecture.txt`"*.
- If no path given: default to CWD, confirm with user before writing.
- If only a directory given: pick a sensible filename (`architecture.txt`, `flow.txt`, `pipeline.txt`).

## Folder convention: one `diagram/` per module

When a repo or module accumulates 4+ ASCII diagrams describing it, put them in a dedicated **`diagram/`** folder at the module's root — not in `docs/` next to prose docs. This keeps the "things you scan visually" separate from the "things you read line-by-line."

```
my-module/
├── README.md
├── docs/                       prose docs (md, tutorials, references)
└── diagram/                    ← ASCII diagrams live here
    ├── 00-index.txt            navigation across this diagram set
    ├── 01-repo-layout.txt
    ├── 02-architecture.txt
    └── canvas-YYMMDD.excalidraw   produced by diagram-ascii-canvas
```

- Numbered prefix (`00-`, `01-`, …) for ordering and easy reference ("see 03").
- Cross-references between diagrams use the relative path inside the folder (e.g. `diagram/03-foo.txt`), not `docs/...`. After a rename this stays correct.
- `_pngs/` (intermediate renders) and `canvas-*.excalidraw` are produced by `diagram-ascii-canvas` and can stay in the same folder; gitignore them if you want.

When you're producing a new diagram for a module that doesn't yet have a `diagram/` folder, create it. Don't add to `docs/`.

## Style — Emoji-Rich

**Use as many emoji as possible.** Pull from multiple categories in the same diagram — combining People + Services + Data + Status in one sketch is *encouraged*, not "spam." The palette below is a menu, not a quota.

| Category | Examples |
|---|---|
| People | 🧑 user · 👥 team · 🧑‍💻 dev |
| Services | 🤖 agent · 🌐 web · 🔧 tool · ⚙️ process · 📦 package |
| Data | 🗄️ database · 📊 metrics · 📂 folder · 📄 file · 📥 input · 📤 output |
| AI / Model | 🧠 model · 🎯 target · 💡 idea |
| Flow | 🔁 loop · 🔀 branch · ⚡ event · 🚀 launch |
| Status | ✅ done · ❌ failed · ⏳ running · ⬜ pending · 🔥 hot · 🟢🟡🔴 |
| Experiment | 🧪 experiment · 📥 load · ⚙️ preprocess · 🧠 train · 📊 eval · 🚀 deploy |
| Issues | 🚩 flag · ⚠️ warning · 🐛 bug |

## Box & Arrow Defaults

Single-line ASCII unless cramped. Don't mix styles in one diagram.

```
+----------+      +----------+      +----------+
| 📥 Input |----->| 🧠 Model |----->| 📤 Save  |
+----------+      +----------+      +----------+
```

## Section dividers (for canvas-friendly files)

When a `.txt` is going to be split into sections (for `diagram-ascii-canvas`, or just for human scanning), put an explicit divider line between sections:

```
─§ Section Title ────────────────────────────────────
```

ASCII fallback when Unicode is awkward to type:

```
--§ Section Title ------------------------------------
```

Format:

- Begins with one or more dashes (`─` or `-`), then `§`, then the title.
- Optional trailing run of dashes pads the line out for visual weight (≈ 60 chars total looks good).
- The marker line itself is **consumed** by the canvas tool (not rendered into the PNG); only the title is kept and shown above the section's image.
- The `§` symbol is the unambiguous trigger — it's what makes detection 100% precise. Don't use stand-alone `===` or `---` lines to mark sections; box borders use those, and the canvas tool will not split on them.

Example skeleton:

```
🌳 Repo Layout
═══════════════════════════════

(intro paragraph + headline diagram)

─§ Folder tree ──────────────────────────────────────

📦 my-project/
├── 📂 src/
└── 📂 tests/

─§ Navigation hint ──────────────────────────────────

🔍 "Where is X?"
 ├─ HTTP route?  →  app/main.py
 └─ MCP tool?   →  app/mcp_server.py
```

Tool behavior:

- File with markers → one PNG per section (titles from the marker).
- File with no markers → one PNG for the whole file (the canvas tool does not guess section boundaries from box borders).

## Light Rules

- Spaces only — no tabs.
- Box width ≈ longest label + 4 (padding + borders).
- Gutters ≥ 3 chars horizontally; ≥ 1 row vertically.
- **Tables**: pad cells in the same column to equal width; all `|` separators must line up vertically.
- **Emoji in tables**: prefer emoji in headers/labels rather than inside cells — monospace fonts render emoji as 1 or 2 character widths inconsistently. If emoji must appear in cells, assume 2 widths and pad accordingly.
- If output drifts after writing, re-render from scratch — don't patch individual lines.
- **Numbered series**: when a response contains 3 or more diagrams, prefix each with a numbered header (see template below) so the user can reference them by number in follow-up questions.

### Folder Tree Rules

- Use Unicode tree characters (`├──`, `└──`, `│`), never ASCII dashes for tree lines.
- Annotations go to the right of the path, separated by 2+ spaces, padded to a consistent column across siblings.
- Floating group labels (e.g. `(umbrella)`) sit on their own line, indented to align with the `│` column of their parent — not on the same line as the path entry.
- Blank lines between sibling groups are allowed and encouraged for scannability — they do not break the tree structure.
- Omit `📄` / `📂` emoji when the path suffix (trailing `/` or extension) already makes the type obvious.

## Templates

**Pipeline** (left → right)
```
+----------+     +------------+     +----------+
| 📥 Load  |---->| ⚙️ Process |---->| 📤 Save  |
+----------+     +------------+     +----------+
```

**Layered** (top → bottom)
```
+-------------------+
| 🧑 User           |
+-------------------+
         |
+-------------------+
| 🌐 API            |
+-------------------+
         |
+-------------------+
| 🗄️ Database       |
+-------------------+
```

**Folder tree — basic**
```
📦 my-project/
├── 📂 src/
│   ├── 📄 index.ts
│   └── 📂 components/
├── 📂 tests/
└── 📄 README.md
```

**Folder tree — annotated** (inline role labels, right-aligned to a consistent column)
```
code/
├── haipipe/        # core framework  (editable)
├── hainn/          # ML models       (editable)
└── haifn/          # generated fns   (DO NOT EDIT)
```

**Folder tree — grouped** (blank lines between logical clusters; floating callout on its own line)
```
Tools/plugins/haipipe-toolkit/skills/
├── 0_subject/
│   └── haipipe-subject/SKILL.md
│
├── 1_data/
│  (umbrella)
│   ├── haipipe-data/SKILL.md
│   ├── haipipe-data-source/SKILL.md
│   ├── haipipe-data-record/SKILL.md
│   ├── haipipe-data-case/SKILL.md
│   └── haipipe-data-aidata/SKILL.md
│
├── 2_model/
│   └── haipipe-nn/SKILL.md
│
└── 3_endpoint/
    └── haipipe-end/SKILL.md
```

**Folder tree — annotated + grouped** (combines both: role labels and blank-line clusters)
```
code-dev/1-PIPELINE/
│
├── 1-Source-WorkSpace/    →  code/haifn/fn_source/
├── 2-Record-WorkSpace/    →  code/haifn/fn_record/
├── 3-Case-WorkSpace/      →  code/haifn/fn_case/
├── 4-AIData-WorkSpace/    →  code/haifn/fn_aidata/
│
├── 5-Instance-WorkSpace/  →  code/haifn/fn_model/
│  (run builder to regenerate)
│
└── 6-Endpoint-WorkSpace/  →  code/haifn/fn_endpoint/
```

**Branch** (fan-out)
```
                    +----------+
                +-->| ✅ Pass  |
+----------+   /    +----------+
| 🧠 Model |--+
+----------+   \    +----------+
                +-->| ❌ Fail  |
                    +----------+
```

**Table** (column widths equal, separators aligned)
```
+----------+---------+----------+
| Name     | Type    | Status   |
+----------+---------+----------+
| Client   | Node    | ✅ OK    |
| API      | Service | ⏳ Busy  |
| Database | Storage | ✅ OK    |
+----------+---------+----------+
```

**Progress tracker** (experiment pipeline with status)
```
🧪 Experiment: hainn-v0319
+------------+------------------+------------+
| Stage      | Task             | Status     |
+------------+------------------+------------+
| 📥 Load    | Pull raw CGM     | ✅ Done    |
| ⚙️ Clean   | Dedupe + impute  | ✅ Done    |
| 🧠 Train   | Fit ConvLSTM     | ⏳ Running |
| 📊 Eval    | ROC / AUC        | ⬜ Pending |
| 🚀 Deploy  | Push endpoint    | ⬜ Pending |
+------------+------------------+------------+
```

Compact inline form:
```
📥 Load → ⚙️ Clean → 🧠 Train → 📊 Eval → 🚀 Deploy
  ✅        ✅        ⏳          ⬜         ⬜
```

**Numbered series** (3+ diagrams in one response — number each so it's easy to reference)
```
── [1/3] Overall Architecture ──────────────────────────────

+----------+     +------------+     +----------+
| 📥 Input |---->| 🧠 Model   |---->| 📤 Output|
+----------+     +------------+     +----------+

── [2/3] Folder Layout ─────────────────────────────────────

code/
├── haipipe/    (editable)
├── hainn/      (editable)
└── haifn/      (generated)

── [3/3] Stage Status ──────────────────────────────────────

📥 Load → ⚙️ Clean → 🧠 Train → 📊 Eval → 🚀 Deploy
  ✅        ✅        ⏳          ⬜         ⬜
```

Header format: `── [N/TOTAL] Title ──` (dashes fill to ~60 chars). Omit the total if the count isn't fixed upfront.

## Use case: Daily progress log

Pair this skill with a `YYMMDD-progress.md` file in the working folder to track a day's work as a sequence of diagrams. See `ref/07-task-progress.md` for a full worked example.

Conventions:

- **Filename**: `YYMMDD-progress.md` (e.g. `260425-progress.md`).
- **One section per timestamp**: `## HH:MM  emoji  brief title` (≤ 5 words).
- **Diagrams ≥ 80% of the page; prose ≤ 20%.** If a sentence can be a diagram, make it one.
- **Each entry's main diagram shows the work itself** — folder layouts being designed, before/after of a pivot, alternatives compared side-by-side. The status pipeline (`📥 → ⚙️ → 🧠 …`) is a 1-line checkpoint, not the bulk of any entry.
- **Refresh the punch-list table** at start of day and at wrap-up so the log opens and closes with a clear scoreboard.
- **Pivots get a before/after**: explicitly show what was tried and abandoned vs. what's being done now, with one line of "why" underneath.

## Logical relations (for argument-style diagrams)

When diagramming a paper section, an idea, or a design rationale, the **logical glue** matters as much as the boxes. Use these primitives so progression / contrast / synthesis are visible at a glance.

### 1. Progression — A builds on B builds on C

```
+-------+      +-----------+      +-------------+
| 朴素  | ──▶ | + 约束    | ──▶ | + 反事实    |
+-------+      +-----------+      +-------------+
   📉             📊                  ✅
  weak           working            best
```

Right-pointing chain. Each step shows the **delta** (`+ X`). Bottom emoji is a status thermometer.

### 2. Contrast / reversal — "you'd expect X, but actually Y"

```
🤔 intuition              ⚡ reality
+-------------+    ✗     +-------------+
| more data   | ─ ─ ─ ▶ | accuracy ↓  |
| → better    |  fails  | (noise wins)|
+-------------+          +-------------+
                ⚠️
           "scale ≠ free"
```

Dashed arrow `─ ─ ─▶` for "expected-but-disproven" causation. Tagline between.

### 3. Synthesis — many sources, one conclusion (fan-in)

```
📊 exp A ─┐
📈 exp B ─┼──▶  🎯 shared finding
📉 exp C ─┘
```

### 4. Tension / trade-off

```
                  🎯
  📐 accuracy  ◀── ?? ──▶  ⚡ speed
                    ↕
                  🤝 our method
                  (Pareto corner)
```

### 5. Causation vs correlation (use **different** arrow styles)

```
A ━━▶ B    causal     (thick)
A ─ ─▶ B   only correlated  (dashed)
A ══▶ B    implies / theorem  (double)
A  ↯  B    counter-example / does NOT imply
```

### 6. Hypothesis tree — claim with branches of support

```
              🎯 our claim
         ┌────────┴────────┐
         ✅ support 1       ✅ support 2
       (exp §4.2)         (theory §3)
         │                  │
       ┌─┴─┐              ┌─┴─┐
       📊  📈             📐  📜
```

### Paper section → recommended pattern

| Section | Pattern(s) | Why |
|---|---|---|
| Intro / motivation | contrast + tension | sets up the gap |
| Related work | progression / matrix | "the line that leads to us" |
| Method | progression chain + causal arrows | step + dependency |
| Experiments | fan-in synthesis | many setups → one finding |
| Ablation | matrix or progression | "remove X, drop to Y" |
| Discussion | hypothesis tree | claim → supports → evidence |
| Conclusion | synthesis triangle | wrap everything into one line |

For a worked-through method section using all of the above, see `ref/08-paper-section.txt`.

## Anti-patterns (suggestive)

- Mixing ASCII `+--+` with Unicode `╔══╗` in one diagram
- Tabs instead of spaces
- **Plain-text labels with no emoji** — looks dead; defeats the purpose of this skill. If a box, header, row, or status has no emoji, you've under-decorated it.
- 15+ nodes with crossings — use Mermaid instead

## See Also

- `diagram-ascii-canvas` — when you've produced 3+ `.txt` diagrams in one folder and the user wants to see them all on one canvas (for spatial layout, drawing connections between them, design review). Screenshots each `.txt` and embeds them into a single `.excalidraw` file. After producing multiple `.txt` files, offer this as a follow-up: *"要把这些拼成一张 Excalidraw 大图吗？"*
- `progress-log` — for image-heavy Markdown progress reports that embed ASCII sketches from this skill alongside PNG figures and tables
