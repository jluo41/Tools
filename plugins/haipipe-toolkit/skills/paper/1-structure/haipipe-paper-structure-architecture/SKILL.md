---
name: haipipe-paper-structure-architecture
description: "Generate a versioned architecture + section minimap for an academic paper as ONE markdown file (vNN-architecture-minimap.md): config table, key numbers, 5-act arc, paragraph-level section minimap with A/B options, appendix plan, language guide, page budget. Trigger: paper architecture, architecture overview, strategic blueprint, section minimap, /haipipe-paper-structure-architecture."
argument-hint: "[@paper-sections-dir-or-file] [context notes]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "3.1.0"
  last_updated: "2026-06-08"
  summary: "Strategic architecture + section minimap generator. Single versioned .md file. Config table, aligned tables, substantial appendix plan, MISQ-format page budget."
  changelog:
    - "3.1.0 (2026-06-08): updated template to match v03 output. Config as table. Aligned column widths. Appendix plan substantial (~half of paper). Clean final version has no discussion history. Added worked example."
    - "3.0.0 (2026-06-08): merged architecture + minimap into ONE versioned .md file."
    - "2.1.0 (2026-06-05): added frontmatter and renamed."
    - "2.0 (2026-02-08): prior unregistered version."
---

# Paper Architecture + Section Minimap Generator

**Version:** 3.1
**Purpose:** Generate ONE versioned markdown file combining strategic overview with paragraph-level section minimap. All decisions tracked inline. Output ready to hand to a writing agent.

If `0-lifecycle/1-pitch/1-pitch.tex` exists in the paper folder, read it first. The
architecture should expand the current one-minute pitch into a 5-act arc and
section minimap; it should not invent a competing hook, surprise, or so-what.
If the architecture needs a different public-facing story, update the pitch
through `/haipipe-paper-structure pitch` and log the reason.

---

## Output

**Single file:** `vNN-architecture-minimap.md`
- `v01` = first draft with `> JL:` placeholders for open choices
- After user annotates → `v02` with choices locked + `==========> {CC}` replies
- Final clean version (e.g. `v03`) = all locked, no conversation history, ready for writing
- Keep old versions for audit trail

**Location:** user-specified (typically `1-rounds/<revision>/2-paper-architecture/`)

---

## Workflow

### Step 1: Auto-Detect (Silent)

Read input files and detect:
- Current paper pitch: `0-lifecycle/1-pitch/1-pitch.tex` if present
- Paper type: empirical / design-science / theory / hybrid
- Venue + page limit (MISQ Research Article = 55 pages)
- Contributions: rank by emphasis %, separate contributions (empirically tested) from implications (theoretical only)
- Strategic constraints: downplay_causality, prior_work_dependency, acknowledge_incomplete_evidence
- Key metrics: sample sizes, effect sizes, significance levels

### Step 2: Generate the Architecture-Minimap File

Follow the template below. Rules:
- One sentence per line — no mid-sentence wrapping
- Emoji on every paragraph role
- **Table column widths aligned** — pad cells so all `|` separators line up vertically
- A/B options as bullet points under each section
- Configuration as a table (not bullet list)
- Appendix plan is substantial (~half of total pages for empirical papers)
- Page budget at the end with body + appendix + refs + buffer = total

### Template

````markdown
# Paper Architecture — [Short Paper Name]

**Version:** v01 (YYYY-MM-DD)
**Status:** [N] open choices, annotate with `> JL:` to lock

## Configuration

| Field          | Value                                                     |
|----------------|-----------------------------------------------------------|
| Type           | [detected type]                                           |
| Venue          | [venue] ([N] pages max, [format details])                 |
| C1 ([X]%)      | [title — 1 line]                                         |
| C2 ([Y]%)      | [title — 1 line]                                         |
| Implications   | [list] (discussion only, not contributions)               |
| Samples        | [list with N]                                             |
| Constraint     | [key constraints, 1 line]                                 |

## Key Numbers

| Spec                    | Outcome                   |   Coeff |      p |
|-------------------------|---------------------------|--------:|-------:|
| [spec]                  | [outcome]                 | [coeff] |    [p] |

[Summary: "X/Y specs significant at p<Z"]

## 5-Act Story Arc

1. **Hook / Gap:**     [1 line; inherits Hook from PAPER_PITCH.md if present]
2. **Setup:**          [1 line]
3. **Surprise:**       [1 line; inherits Surprise from PAPER_PITCH.md if present]
4. **Mechanism:**      [1 line]
5. **So What / Impact:** [1 line; inherits So What from PAPER_PITCH.md if present]

## Section Minimap — Main Body (~[N] pages)

### §1 [Title] ([N] pages, [N] paras)

| P | Role            | Content                            |
|---|-----------------|-------------------------------------|
| 1 | 🧩 Puzzle        | [1-line content]                   |
| 2 | 🤖 Context       | [1-line content]                   |
| 3 | ❓ Gap           | [1-line content]                   |
| 4 | 📐 This paper    | [1-line content]                   |
| 5 | 📊 Preview       | [1-line content]                   |
| 6 | 💡 Contributions | [1-line content]                   |

**CHOICE #1 — [topic]:**
- **A ([label]):** [description] — [pro]. [con].
- **B ([label]):** [description] — [pro]. [con].

> JL:

---

### §2 [Title] ([N] pages, [N] subsections)

| Sub  | Content              | Pages | Status         |
|------|----------------------|------:|----------------|
| §2.1 | [topic]             |   [N] | Keep / Trim    |
| §2.2 | [topic]             |   [N] | Keep / Trim    |

**CHOICE #2 — [topic]:**
- **A ([label]):** [description] — [pro]. [con].
- **B ([label]):** [description] — [pro]. [con].

> JL:

---

### §N [Title] ([N] pages) — LOCKED

| Sub  | Content                    | Pages |
|------|----------------------------|------:|
| §N.1 | [content]                 |   [N] |
| §N.2 | [content]                 |   [N] |

Locked. [reason].

---

[... all sections ...]

### §8 Conclusion ([N] page, [N] sentences)

| P | Role              | Content                     |
|---|-------------------|-----------------------------|
| 1 | 📊 Main finding    | [1-line]                   |
| 2 | 📐 Key number      | [1-line]                   |

---

## Appendix Plan (~[N] pages)

| App | Content                                              | Pages |
|-----|------------------------------------------------------|------:|
| A   | [content — be specific about what goes here]        |   [N] |
| B   | [content]                                            |   [N] |
| C   | [content]                                            |   [N] |

## Language Guide

**Use:** [comma-separated phrases]

**Avoid:** [comma-separated phrases]

## Page Budget Summary

| Component       | Pages |
|-----------------|------:|
| Main body       |  [N]  |
| Appendix        |  [N]  |
| References      |  [N]  |
| Buffer          |  [N]  |
| **Total**       |**[N]**|
````

### Step 3: User Refinement

User annotates open choices with `> JL:`. Respond with `==========> {CC}` inline. Save as `v02`.

### Step 4: Clean Final Version

After all choices locked, produce a clean version (e.g. `v03`) that:
- Removes all `> JL:` / `==========> {CC}` conversation history
- Replaces choice blocks with "Locked: [decision]." one-liners
- Keeps only the final state — ready to hand to a writing agent

---

## Key Principles

1. **ONE file, versioned** — no separate overview + minimap + .txt
2. **Markdown only** — planning document, not a paper component
3. **One sentence per line** — no mid-sentence wrapping
4. **Emoji on paragraph roles** (🧩 ❓ 📐 📊 💡 🤖 🔬 🛡️ 🔀 🔧 🏆 🎯 📄 👥 🔗)
5. **Table column widths aligned** — pad cells so `|` separators line up vertically
6. **Section headers use `§`** — write `§1`, `§2.3`, not `S1`, `S2.3` (Unicode section sign, not letter S)
6. **A/B options as bullet points** — not side-by-side ASCII boxes
7. **Configuration as table** — not bullet list (scans better)
8. **Contributions vs implications** — be explicit: only empirically tested claims are contributions
9. **Appendix is substantial** — for empirical papers, appendix ≈ half the paper (prompts, validation details, variable construction, robustness tables, alternative specs)
10. **Page budget** — body + appendix + refs + buffer = venue limit. Show the split.
11. **Concise** — 100-200 lines for the final clean version

---

## Section Minimap Conventions

**Paragraph-level sections** (intro, methods, empirics, conclusion):
- `| P | Role | Content |` table with emoji on Role

**Subsection-level sections** (lit review, theory, discussion):
- `| Sub | Content | Pages | Status |` table

**Locked sections:** "Locked. [reason]." one-liner, no choice block.

**Emoji palette for roles:**
🧩 puzzle/problem, 🤖 context/method, ❓ gap, 📐 this paper, 📊 results/finding, 💡 contribution/insight, 🔬 validation, 🛡️ robustness/limitation, 🔀 comparison/contrast, 🔧 practical, 🏆 selection, 🎯 focus, 📄 data, 👥 human, 🔗 bridge/connection

---

## Auto-Detection Rules

| Pattern in text                      | Constraint to add              |
|--------------------------------------|--------------------------------|
| "suggestive", "exploratory"          | acknowledge_incomplete_evidence|
| "IV" + weak first stage              | downplay_causality             |
| "under review", "unpublished"        | prior_work_dependency          |
| "single case", "one context"         | acknowledge_scope_limitations  |

---

## Quality Checklist

- [ ] Configuration is a table with aligned columns
- [ ] All tables have aligned column widths (pad cells)
- [ ] Every paragraph role has an emoji
- [ ] Open choices have `> JL:` placeholder (v01) or are locked (final)
- [ ] Appendix plan is substantial with specific content per appendix
- [ ] Page budget: body + appendix + refs + buffer = venue limit
- [ ] Contributions vs implications clearly separated
- [ ] 5-act arc preserves the current `0-lifecycle/1-pitch/1-pitch.tex` hook,
      surprise, and so-what, or the pitch log records why it changed
- [ ] One sentence per line throughout
- [ ] Final clean version has no `> JL:` / `{CC}` history
- [ ] Total file length: 100-200 lines (final version)

---

## Examples

See `examples/` for worked output:
- `example-empirical-artifact.md` — hybrid empirical + design science (v2.0 format, older)
- `example-misq2026-v03.md` — MISQ behavioral validation paper (v3.1 format, current)
