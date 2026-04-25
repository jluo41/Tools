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

## Anti-patterns (suggestive)

- Mixing ASCII `+--+` with Unicode `╔══╗` in one diagram
- Tabs instead of spaces
- 6+ emoji categories in one diagram (overwhelming)
- 15+ nodes with crossings — use Mermaid instead

## See Also

- `progress-log` — for image-heavy Markdown progress reports that embed ASCII sketches from this skill alongside PNG figures and tables
