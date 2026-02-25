# /paper-incubator

Three commands for building and refining the incubator working documents in `0-incubator/`.

## Commands

```
/paper-incubator display      Catalog every figure/table with deep analysis
/paper-incubator arch          Paper architecture: summary, contributions, story arc, scope
/paper-incubator structure     Section-by-section paragraph blueprint with display placement
```

## How It Works

1. Invoke a command (e.g., `/paper-incubator arch`)
2. CC reads the file — if it exists, asks which subsection to focus on; if not, generates it from template
3. CC presents a **readable summary** of the focal subsection (not raw LaTeX)
4. You give feedback in natural language
5. CC updates the `.tex` file and adds a `> JL:` / `>> CC:` discussion box
6. Say "next" to move on, or keep refining the current subsection

## Files

| File | What it does |
|------|-------------|
| `SKILL.md` | Session protocol, shared LaTeX rules, dependency diagram |
| `arch.md` | Rules for the 5 arch subsections |
| `display.md` | Rules for display entries, deep analysis, provenance |
| `structure.md` | Rules for paragraph blueprints, canonical numbers |
| `templates/arch.tex` | Full compilable starting template |
| `templates/display-entry.tex` | Single display entry to append |
| `templates/structure-entry.tex` | Single section entry to append |

## Dependencies

```
evaluation/scripts → evaluation/results → 0-display/
                                              ↓
arch ──canonical numbers──▶ structure ◀── 0-sections/
                               ↕
                            display
```

Create order: **arch → display → structure**. Refine in any order.

## The Three Incubator Files

| File | Purpose |
|------|---------|
| `0-incubator/00-incubator-display.tex` | One page per display: rendered visual + deep analysis + provenance |
| `0-incubator/01-incubator-arch.tex` | Summary, key data, contributions (C1-C5), 5-act story arc, scope |
| `0-incubator/02-incubator-structure.tex` | Every paragraph summarized, every display placed, status tracked |

All three are standalone compilable LaTeX documents. Compile with `./1-compile.sh 00-incubator-display.tex` (auto-routes to `0-incubator/`).
