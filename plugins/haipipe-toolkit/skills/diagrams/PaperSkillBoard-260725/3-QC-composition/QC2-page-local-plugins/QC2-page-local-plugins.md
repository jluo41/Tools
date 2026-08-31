# QC2 · Compose Page-local plugins without copying their contracts into Paper

state: ✅ SETTLED · Page-local plugin boundaries validated
owner: JL
method: classify every Page-local lane by what it reads, writes, and hands back

## Opening
How does a Paper Page use existing Pages, obtain new evidence, render displays, and generate formats without owning all those implementations?
Each plugin has a narrow lane inside the consuming Page.
Paper may request the lane and assemble accepted outputs, but the plugin contract remains shared.

**Where this page sits**: QA2 fixes authority; this Page shows the concrete plugin composition.

**Why it matters**: Page-local lanes let Paper stay light while keeping every claim inspectable.

## Writing Style
Name the plugin by its one job and show where its durable output lives.
Show PageX inside the Probe family while keeping its Page and QA lanes distinct.

## Diagram
**Page-local plugin lanes**: Probe routes two source kinds into one consuming Page.

```text
Probe ─┬─ existing Pages ─▶ 🔗 pagex/ ──────┐
       └─ Task/Discovery ─▶ 🃏 probe/ ───────┤
sources ────────▶ 📚 bibex/                 ├─▶ owning Page
data/recipe ────▶ 🖼 display/                │
accepted Page ──▶ 📄 latex/ · word/ ────────┘
```

## Content
### 1 · Plugin composition
**Typed Probe routes**: PageX reuses resolved Page context while QA Probe resolves an unanswered consumer question.

```text
outline marks an obligation
   ├─ evidence acquisition ─▶ Probe ─┬─ existing Page → PageX
   │                                └─ Task/Discovery → QA Probe
   ├─ scholarly citation ───▶ Bibex
   └─ visual claim ─────────▶ Display
```

Values remain inside probe-card proof and `## Values` blocks, referenced by stable value ids.
LaTeX and Word generate projections from an accepted Page and do not become prose authority.

## Aims
### A1 · 🧩 Plugin composition
- ✅ A1.1 · Every Page-local plugin has one non-overlapping read and write boundary.
  **Done when:** Probe's PageX and QA lanes, Bibex, Display, LaTeX, and Word compose without duplicated evidence.
  **Now:** PageX now sits under Probe while keeping an independent Page-local record.


## Files
- `../../board/page-plugins/haipipe-plugin-pagex/SKILL.md` · existing Page reader
- `../../board/page-plugins/haipipe-plugin-probe/SKILL.md` · question and proof lane
- `../../board/page-plugins/haipipe-plugin-display/SKILL.md` · display units

## Log
260820 · Grouped PageX and QA acquisition under Probe without merging their storage or phases.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0