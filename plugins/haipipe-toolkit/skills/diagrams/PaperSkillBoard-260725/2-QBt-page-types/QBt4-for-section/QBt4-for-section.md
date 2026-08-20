# QBt4 · Execute exactly one current Narrative row as a Section

state: ✅ SETTLED · current Section contract validated
page-type: section
section_kind: results
owner: JL
method: bind prose to one Narrative row, one venue allocation, and Page-local evidence

## Opening
How does one reader-ordered manuscript or appendix unit become checked prose?
Section resolves its structure from the selected Venue and section kind, then executes exactly one current Narrative row.
Its consequential sentences bind to inspectable evidence, citations, values, or displays.

**Where this page sits**: Narrative supplies the row; assembly reads the accepted Section output.

## Writing Style
Write to the named reader entry and exit states.
Expose unsupported obligations instead of filling them with plausible prose.

## Diagram
**Section authority**: prose is downstream of contract and evidence.

```text
Seed limits ─▶ Venue rules ─▶ Narrative row ─▶ Page evidence ─▶ prose
```

## Content
### 1 · Section contract
**Required binding**: the Page records the governing row, claims, reader states, constraints, structure source, evidence allowlist, and transitions.

```text
one Narrative row + venue × kind structure + landed evidence
                         ─▶ accepted Section output
```

Retargeting re-resolves the Narrative row and venue structure while preserving only evidence whose meaning remains valid.

## Aims
### A1 · 📄 Section contract
- A1.1 · One current Narrative row governs one Section Page.
  **Done when:** every consequential sentence has inspectable support or a closure-blocking obligation.

## States
### A1 · 📄 Section contract
- ✅ A1.1 · The current contract unifies main and appendix units under one rule.

## Files
- `../../paper/page-types/haipipe-page-for-section/SKILL.md` · source contract

## Log
260820 · Kept Section light by moving paper-wide logic to Narrative and evidence to local plugins.
