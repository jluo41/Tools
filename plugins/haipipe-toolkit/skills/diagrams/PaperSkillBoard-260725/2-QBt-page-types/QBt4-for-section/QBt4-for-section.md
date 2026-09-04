# QBt4 · Execute exactly one current Narrative row as a Section

state: ✅ SETTLED · 0.4.0 · structure resolves from the QBv bank · S<D>/A<D> tokens in B groups
page-type: section
section_kind: results
owner: JL
method: bind prose to one Narrative row, one venue allocation, and Page-local evidence

## Opening
How does one reader-ordered manuscript or appendix unit become checked prose?
Section executes exactly one current Narrative row, and resolves its structure from the QBv Venue Page's unit division that the Narrative's venue decision binds.
Its consequential sentences bind to inspectable evidence, citations, values, or displays.

**Where this page sits**: Narrative supplies the row; assembly reads the accepted Section output. A desk's units live together in its `B<x>-<desk>/` group, main sections as `S<D><NN>` and appendices as `A<D><NN>`, alongside that desk's `RD` rounds; one contract covers main and appendix.

## Writing Style
Write to the named reader entry and exit states.
Expose unsupported obligations instead of filling them with plausible prose.
Name the structure-source as a QBv unit division or the explicit generic fallback, never a raw pack file.

## Diagram
**Section authority**: prose is downstream of contract and evidence.

```text
Seed limits ─▶ Narrative row ─▶ 🏛 QBv unit division ─▶ Page evidence ─▶ prose
                    │ carries the venue decision
                    ▼
        Ba-<desk1>/S<D><NN>-<kind>    main reading order, first desk
        Ba-<desk1>/A<D><NN>-<slug>    that desk's appendices
        Bb-<desk2>/…                  second desk, same shape
prose ships from the desk's self-contained ROOM (1-<desk><year>/), which
holds COPIES of accepted page displays and a bib assembled from bibex/
```

## Content
### 1 · Section contract
**Required binding**: the Page records the governing row, claims, reader states, constraints, structure source, evidence allowlist, and transitions.

```text
one Narrative row + one QBv unit division + landed evidence
                         ─▶ accepted Section output
```

The old resolved source, `paper/venue/**/template.md` with the `section-page-template: 1` marker, held zero marked files, so every Section silently fell back to generic; 0.2.0 re-points resolution at the QBv page the Narrative already binds.
A missing unit division is raised as a gap on the QBv page rather than filled locally.
Retargeting re-resolves the Narrative row and the QBv unit division while preserving only evidence whose meaning remains valid.

## Aims
### A1 · 📄 Section contract
- ✅ A1.1 · One current Narrative row governs one Section Page.
  **Done when:** every consequential sentence has inspectable support or a closure-blocking obligation.
  **Now:** The current contract unifies main and appendix units under one rule.
- ✅ A1.2 · Structure comes from the bank, not from stage-era pack files.
  **Done when:** every structure-source names a QBv unit division or the recorded generic fallback.
  **Now:** The 0.2.0 re-point closes the empty-universe hole; the fallback stays explicit.


## Files
- `../../paper/workflow-phases/haipipe-paper-section/SKILL.md` · source contract

## Log
260820 · Kept Section light by moving paper-wide logic to Narrative and evidence to local plugins.
260821 · 0.2.0 ruled by JL: structure resolves from the QBv Venue Page's unit division through the Narrative's binding, because the template.md universe held zero marked files; runtime splits into 1-SC-main/ and 2-SA-appendix/ with Round at 3-RD-round/.
260828 · Refreshed to 0.4.0: the 260824 group grammar replaced SC/SA groups with one `B<x>-<desk>/` group per desk holding `S<D>`/`A<D>` units and `RD` rounds together, and the room law made each desk's tex/displays/bib self-contained; `SC`/`SA` boards are grandfathered. Gate G6 reads per-unit CHECK ✅; assemble is a verb that runs anytime, watermarked DRAFT until G6 holds. Structure resolution from the QBv unit division is unchanged.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0