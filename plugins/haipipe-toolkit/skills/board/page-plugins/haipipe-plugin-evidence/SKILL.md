---
name: haipipe-plugin-evidence
description: >-
  The ONE evidence plugin for a Board Page. It owns the 🧾 Evidence tab and
  the Citation/Bib, Value, Display, and PageX lanes, including their storage,
  writers, gates, and joined lineage. PageX is a SURVEY source binding that
  LAND validates beside Supporting and local Runs, never a Result type.
  Probe remains a separately governed crossing shown inside this tab. Trigger:
  evidence plugin, evidence tab, citations, page bib, Discovery evidence bib,
  verify citation, evidence bundle, /haipipe-plugin-evidence.
metadata:
  version: "0.5.0"
  last_updated: "2026-09-02"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-plugin-evidence · one evidence authority and one tab

**LOAD `haipipe-plugin` FIRST.** This is the only Evidence plugin. It owns two
things that must agree:

```text
AUTHORITY  Citation/Bib · Value · Display · PageX storage, writers, gates,
           typed payload rules, and cross-Folder source bindings
SURFACE    the 🧾 Evidence tab: one joined view over Evidence Items,
           Supporting Runs, PageX sources, Local Runs, and ready Results
```

There is no separate Bibex, Value, Display, or PageX plugin or skill. Their
storage addresses and compatibility engine routes remain, but the folder or
endpoint name does not create another Plugin. Load only the reference needed
for the current Evidence Item:

```text
ref/citations.md   CITE authority, verification, Discovery aggregation
ref/values.md      VALUE provenance and joined value surface
ref/displays.md    DISPLAY unit, renderer dispatch, acceptance
ref/pagex.md       PageX SURVEY binding, LAND validation, cross-Folder links
evidence/probe/    haipipe-plugin-probe remains the crossing/card contract
```

## 📦 Evidence category

Since the v3 Folder, the Page's evidence lives under one category:

```text
<page>/evidence/
├── bibex/       citations/Bib storage owned by THIS skill
├── probe/       governed by haipipe-plugin-probe
├── display/     display units owned here; renderer crafts write recipe/assets
├── pagex/       PageX links and exact SURVEY bindings owned here
└── materials/   immutable external captures
```

Flat legacy lane names may remain migration symlink stubs. New work treats
`evidence/` as the category and 🧾 Evidence as its one Plugin surface.

## 📚 Citation authority

Two modes share one law: a machine may retrieve, subset, validate,
deduplicate, stable-sort, or copy a real BibTeX entry; it MUST NOT invent or
complete citation fields from memory.

```text
ordinary Page
  evidence/bibex/<stem>.bib          PRIMARY
  evidence/bibex/<stem>-bib.html     DERIVED workbench

Discovery Task Page
  results/<RUNNAME>/<RUNNAME>.bib    PRIMARY · exactly one verified Subject
                    │
                    └── validate + union completed Results
                        ↓
  evidence/bibex/<task>.bib          DERIVED Page Evidence Bib
  evidence/bibex/<task>-bib.html     DERIVED workbench
```

Corrections land at the primary authority: the Page Bib in ordinary mode, or
the owning Result Bib in Discovery mode. The derived Discovery aggregate is
never edited as the correction target. Full writer and conflict rules are in
`ref/citations.md`.

## 📡 Surface · one tab, six segments, one join

```text
🧾 Evidence
├── ⧉ By bullet      default join: one row per owing plan bullet
├── 📚 Citations     Bib workbench, verification, DOI/URL/Scholar links
├── 🚪 Cards         Probe card list
├── 🧮 Values        PP<NN>.v<n> rows with source paths
├── 🖼 Displays      display-unit strip
└── 🔗 PageX         SURVEY bindings + ranked cross-Folder borrow view
```

- **By bullet is first** because the reader asks what the Page still owes. Each
  typed item joins its Supporting Runs, PageX bindings, Local Input, Local Run,
  ready Result, and fold.
- **Counts stay separate**: `owed n · landed n · accepted n`.
- **Both failure modes are named**: 🕳 owed-and-absent and 🎈 present-and-uncited.
- **The surface calls no model.** It writes only through the owning lane's
  explicit pen. Citations use this skill's citation routes; every other pen
  stays with its lane contract.

## 🔒 Writers, gates, and walls do not collapse

| Lane | Writer | Human gate | Wall |
|---|---|---|---|
| Citations/Bib | trusted-entry copy/subset; Discovery deterministic builder | `verified` | never compose citation fields from memory |
| Probe | raise/bind crossing | `read:` | consumer stake never crosses |
| Values | LAND through this plugin's typed payload rule | rides owning read gate | aggregates only; never raw rows |
| Display | renderer craft dispatched through this plugin | `accepted:` | intake frozen after supports/PageX validate |
| PageX | this plugin's ranked-link/source-binding writer | human rank | exact authority link, never copy or Result |

The tab offers no “approve all” control. Each judgment remains beside the
artifact whose contract owns it.

## 🗺 Workflow relation

`haipipe-page-outline` SURVEY writes each item's Supporting Runs, optional
PageX bindings, Local Input, and Local Run plan. `haipipe-page-evidence` LAND
validates every Supporting Result and PageX authority, freezes one Local Input,
and finishes exactly one local Run before the item becomes ready. EMBED folds
only that ready `VALUE`, `CITE`, or `DISPLAY` Result. A PageX link is never a
fourth Result type and never substitutes for either Run layer. Discovery's
ACQUIRE cycle produces per-Subject Results; SYNTHESIZE promotes completed
Results through this skill's citation aggregation; CLOSE checks the joined
evidence without minting an umbrella Run.

## 🗺 Status · 🟢 live

`live/evidence.py` serves the segmented surface and its POST twin;
`84-plugin-evidence.js` registers the one tab row. The former standalone
Citation, Value, Display, Probe, and PageX strip rows are segments here. The
former Value, Display, and PageX Skill entrypoints retired into `ref/`; their
engine routes and storage remain compatibility internals of this one plugin.

## 📂 Files

- `ref/citations.md` — citation/Bib storage, writers, verification, and
  Discovery aggregate authority.
- `ref/values.md` — VALUE provenance and the joined Values segment.
- `ref/displays.md` — DISPLAY unit shape, renderer dispatch, and acceptance.
- `ref/pagex.md` — PageX source bindings, storage, safety, and joined view.
- `../haipipe-plugin-probe/SKILL.md` — the separately governed crossing/card
  contract presented inside this tab.
- `../haipipe-plugin-outline/ref/evidence-bundle.md` — the per-bullet join.
- `../../haipipe-board/cli/evidence-status.py` — counts and snapshot.
- `../../haipipe-board/live/evidence.py` — segmented surface and citation pens.
- `../../haipipe-board/assets/js/10-drawer/84-plugin-evidence.js` — one tab row.
- `../../page-workflows/haipipe-page-evidence/SKILL.md` — LAND/EMBED workflow.
