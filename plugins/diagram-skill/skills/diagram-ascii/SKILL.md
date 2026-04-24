---
name: diagram-ascii
description: Fast emoji-rich ASCII diagrams for brainstorming, folder/code overviews, and experiment progress tracking. Use when the user wants to sketch an idea, map a codebase, visualize a flow inline during discussion, or show pipeline progress. Output is plain-text with liberal emoji for visual punch.
---

# /diagram-ascii — Brainstorm & Progress Diagrams

**Purpose**: quickly sketch ideas and track progress as emoji-rich ASCII. Optimized for speed, readability, and scannability — not mechanical precision. For complex diagrams with many crossing arrows, suggest Mermaid instead.

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

## Style — Emoji-Rich

Emoji give ASCII "color." Pick 2–3 categories per diagram; don't spam.

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

## Light Rules

- Spaces only — no tabs.
- Box width ≈ longest label + 4 (padding + borders).
- Gutters ≥ 3 chars horizontally; ≥ 1 row vertically.
- **Tables**: pad cells in the same column to equal width; all `|` separators must line up vertically.
- **Emoji in tables**: prefer emoji in headers/labels rather than inside cells — monospace fonts render emoji as 1 or 2 character widths inconsistently. If emoji must appear in cells, assume 2 widths and pad accordingly.
- If output drifts after writing, re-render from scratch — don't patch individual lines.

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

**Folder tree**
```
📦 my-project/
├── 📂 src/
│   ├── 📄 index.ts
│   └── 📂 components/
├── 📂 tests/
└── 📄 README.md
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

## Anti-patterns (suggestive)

- Mixing ASCII `+--+` with Unicode `╔══╗` in one diagram
- Tabs instead of spaces
- 6+ emoji categories in one diagram (overwhelming)
- 15+ nodes with crossings — use Mermaid instead

## See Also

- `progress-log` — for image-heavy Markdown progress reports that embed ASCII sketches from this skill alongside PNG figures and tables
