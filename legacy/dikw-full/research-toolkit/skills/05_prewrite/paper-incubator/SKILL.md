Skill: paper-incubator
======================

Three subcommands for creating and interactively refining the incubator
LaTeX working documents in `0-incubator/`.

```
/paper-incubator display   →  00-incubator-display.tex
/paper-incubator arch      →  01-incubator-arch.tex
/paper-incubator structure →  02-incubator-structure.tex
```

On invocation, read this file for the session protocol, then read the
matching subcommand file (`arch.md`, `display.md`, or `structure.md`)
for detailed rules. Templates live in `templates/`.

---

Session Protocol
================

Every subcommand follows the same conversation loop:

### Step 1: Detect Mode

- **File exists** → Refine mode: present subsection list, ask which to focus on
- **File missing** → Create mode: read sources, generate the whole file from
  template, then walk through subsection by subsection for review

### Step 2: Read Sources

Read the subcommand-specific sources listed in `arch.md`, `display.md`,
or `structure.md`. These provide ground-truth numbers and content.

### Step 3: Present Focal Subsection

Show a **readable summary/interpretation** of the subsection — NOT raw LaTeX.
Digest the content into a scannable format: headings, key numbers, bullet
points. Flag anything that needs attention (stale numbers, missing content,
inconsistencies with source material).

Example presentation:
```
### Key Data Points (current state)

**Scale:** 60 task instances (12 strata × 5 conditions), 18 models

**Core Findings (9 items):**
1. Best overall: GPT-4o-mini (32.61)
2. Light context helps: 6/12 models improve with ProfileOnly
3. Rich context harms: 8/10 LLMs degrade
...

⚠ GPT-4o-mini score may be stale (Table 1 shows 31.50)

What would you like to change?
```

### Step 4: User Feedback

User gives feedback in natural language. CC interprets and acts.

### Step 5: Update & Record

1. **Edit the LaTeX file** — apply the requested changes to actual content
2. **Add a discussion box** — record the exchange at the top of the subsection
3. **Show what changed** — brief summary of updates (not raw diff)

### Step 6: Next or Stay

Ask the user: more changes on this subsection, or move to next?
Loop back to Step 3. When done with all subsections, the session ends.
User compiles themselves (`./1-compile.sh` or `pdflatex`).

---

Discussion Box Convention
=========================

Every exchange is recorded in the LaTeX file:

```latex
\fbox{\parbox{0.95\textwidth}{
\textbf{> JL:} [User's feedback in their own words]\\
\textbf{>> CC:} [ACTION]. [What changed, 1-2 sentences].
}}
\vspace{0.3cm}
```

**Actions:** DONE, UPDATED, ADDED, FIXED, REMOVED, REFRAMED

**Multi-round** — append new exchanges to the same box:
```latex
\textbf{> JL:} First feedback.\\
\textbf{>> CC:} FIXED. Changed X.\\
\textbf{> JL:} Follow-up.\\
\textbf{>> CC:} UPDATED. Also changed Y.
```

---

Shared LaTeX Rules
==================

All three files are **standalone compilable** documents sharing:

- `\documentclass[10pt]{article}` with `geometry`, `booktabs`, `xcolor`,
  `hyperref`, `enumitem`, `amssymb`, `graphicx`, `float`
- Custom commands: `\critical{}` (red), `\high{}` (orange), `\medium{}` (blue)
- Section hierarchy: `\section{}` → `\subsection{}` → `\subsubsection*{}`
- Every `\subsection` except the first gets `\clearpage`
- Lists always use `[nosep]`; figures/tables always use `[H]`
- Separator comments: `% ===` (section), `% ---` (subsection), `% · · ·` (sub)
- Content integrity: exact numbers from tables/figures, exact model/task names

---

Dependencies
============

```
1-config.yaml
     │
     ▼
evaluation/scripts/*.py → evaluation/results/ → 0-display/Figure/, Table/
                                                       │
     01-incubator-arch.tex                             │
            │                                          │
            │ canonical numbers                        │ rendered visuals,
            │ terminology                              │ provenance
            ▼                                          ▼
     02-incubator-structure.tex ◀── 0-sections/   00-incubator-display.tex
            (paragraph blueprint)    (paper content)   (display catalog)
```

**Create order:** arch → display → structure

**Refine:** any order; propagate canonical number changes from arch to structure.

---

File Layout
===========

```
.claude/skills/paper-incubator/
  SKILL.md                    ← you are here (router + protocol)
  arch.md                     ← /paper-incubator arch rules
  display.md                  ← /paper-incubator display rules
  structure.md                ← /paper-incubator structure rules
  templates/
    arch.tex                  ← full compilable template
    display-entry.tex         ← single display entry (append)
    structure-entry.tex       ← single section entry (append)
```
