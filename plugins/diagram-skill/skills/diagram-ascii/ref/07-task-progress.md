# 260425 — diagram-ascii skill restructure

Worked folder: `Tools/plugins/diagram-skill/skills/diagram-ascii/`

Goal: separate spec from gallery.

---

## 09:15  📋 Plan

```text
Before                          After
+-----------+                   +----------+      +----------+
| SKILL.md  |                   | SKILL.md |      | ref/     |
|  rules    |        →          |  rules   |  +   | full     |
|  templ.   |                   |  brief   |      | worked   |
|  examples |                   |  templ.  |      | examples |
+-----------+                   +----------+      +----------+
```

```text
+------------------------+------------+
| 📋 Task                | 🟢 Status  |
+------------------------+------------+
| Folder tree concepts   | ⬜         |
| Numbered series rule   | ⬜         |
| Build ref/ gallery     | ⬜         |
+------------------------+------------+
```

---

## 10:30  🔧 Folder tree — design 4 variants

```text
basic              annotated                 grouped                  annotated+grouped
─────              ─────────                 ───────                  ─────────────────
src/               code/                     skills/                  1-PIPELINE/
├─ index.ts        ├─ haipipe/  (editable)   ├─ 0_subject/            │
└─ tests/          ├─ hainn/    (editable)   │   └─ SKILL.md          ├─ 1-Source/  →  fn_source/
                   └─ haifn/    (DO NOT EDIT)│                        ├─ 2-Record/  →  fn_record/
                                             ├─ 1_data/               │
                                             │  (umbrella)            ├─ 5-Inst/    →  fn_model/
                                             │   ├─ data/             │  (run builder)
                                             │   └─ data-source/      │
                                             │                        └─ 6-End/     →  fn_endpoint/
                                             └─ 2_model/
```

Rules: Unicode tree chars · annotations padded to consistent column · floating callouts on own line.

---

## 12:00  📊 Mid-day checkpoint

```text
+-----------------+   +----------------+   +-------------+   +----------+
| ✅ Folder tree  |-->| ✅ Numbered    |-->| ⏳ Gallery  |-->| ⬜ Wrap  |
+-----------------+   +----------------+   +-------------+   +----------+
```

---

## 14:15  ⚡ Pivot — rolled back the multi-file split

```text
Tried (rejected)                       Doing instead
────────────────                       ─────────────
SKILL.md  (index only)                 SKILL.md  (full spec)
├── 0-overview.txt                          +
├── 1-inputs-outputs.txt               ref/  (gallery of examples)
├── 2-style.txt                        ├── 01-pipeline.txt
├── 3-templates.txt                    ├── 03-folder-tree.txt
└── 4-antipatterns.txt                 └── 07-task-progress.md ← this file
```

Why: SKILL.md should BE the spec, not a TOC. Splitting forces 5 reads per invocation.

---

## 16:00  ✅ Wrap-up

```text
+------------------------+------------+
| 📋 Task                | 🟢 Status  |
+------------------------+------------+
| Folder tree concepts   | ✅         |
| Numbered series rule   | ✅         |
| Build ref/ gallery     | ✅         |
| + progress log example | ✅         |
+------------------------+------------+
```

Tomorrow: dogfood the gallery on a real session.
