---
name: haipipe-page-for-dash
description: >-
  The Paper Page Type for a regenerated dashboard over one Page or plugin
  family. It reports every unit, obligation, state, and gap without owning
  acceptance or decisions. Use for section, probe, citation, or display rollups
  and for choosing which underlying unit to inspect next.
metadata:
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Family Scope → Generated Rows → Authored Interpretation"
---

# /haipipe-page-for-dash · measure a family without ruling it

Load `haipipe-page` first. Declare:

```yaml
page-type: dash
dash_family: section | probe | citation | display
```

Only these four current family names are valid. A retired `value` or
`literature` dashboard must be migrated explicitly before this contract runs.

## 📊 Grain and boundary

One Dash covers every current unit of one family. It is regenerated and never
closes. It has no acceptance gate, selection authority, or hand-edited unit
state.

```text
source Pages/plugins ── fresh scan ──▶ generated rows
Narrative/Venue obligations ─────────▶ expected rows and yardsticks
human reading ───────────────────────▶ authored set-level interpretation
```

Fix a problem on its owning Page or plugin unit; rebuild the Dash to observe the
change.

## 📦 Family payloads

| `dash_family` | One row per | Required row content |
|---|---|---|
| `section` | Section Page | Narrative row/version, phase, claims, evidence/display gaps, venue fit |
| `probe` | QA card | consumer point, question, bank/source, answer/proof state, stale state |
| `citation` | citation card/key | claiming point, source, verification, bibliography state, consumers |
| `display` | display unit | message, intake version, artifacts, Page bindings, acceptance state |

An expected but absent unit appears as a row. A present unit with no obligation
appears as an orphan row. Blank cells are forbidden: use explicit states such as
`none required`, `not created`, `blocked`, `stale`, or `not accepted`.

## ✍️ Generated and authored regions

```text
GENERATED   unit rows, counts, paths, versions, and mechanical states
AUTHORED    what the set adds up to, the dominant gap, and what to inspect next
```

Never put a decision into generated rows. Never let authored interpretation
overwrite a unit's own acceptance state.

## ✅ Rebuild checks

- The source family was scanned fresh from disk.
- Every expected and orphan unit is represented.
- Every cell has an explicit state.
- Links open the owning Page/plugin unit and concrete artifact where applicable.
- The authored reading distinguishes measurement from decision.
- Rebuilding twice with unchanged inputs produces the same generated rows.

This variant owns no scripts and no independent Page workflow gate.
