---
name: haipipe-page-for-section
description: >-
  The Paper Page Type for one reader-ordered manuscript or appendix Section. It
  executes exactly one current Narrative row, resolves venue-and-kind structure,
  and binds prose to Page-local values, citations, probes, and displays. Use when
  outlining, drafting, revising, checking, or retargeting one paper section.
metadata:
  version: "0.3.1"
  last_updated: "2026-08-24"
  summary: "0.3.1 (JL 260824): the tracked tex lives in the telling's DESK ROOM (<N>-<desk><year>/sections/), its figures include from that room's displays/ copies and its keys resolve in that room's reference.bib — rooms are self-contained per the door's room law; board address is 0-paperboard/. 0.3.0 (JL 260823): lands on disk what the 0.2.0 CHANGELOG entry recorded but the body never received — structure resolves from the QBv Venue Page's Unit Guidance division matching section_kind, through the governing Narrative's division-1 binding, never from the zero-file template universe; runtime homes take the 260823 scaffold grammar (Ba1/Ba2 desk pairs, tokens S<D>/A<D>; 1-SC-main and 2-SA-appendix boards grandfathered)."
  group-token: "S<D> | A<D>"
  outline:
    mode: resolved
    source: "the governing Narrative's division-1 QBv binding → that Venue Page's Unit Guidance division matching section_kind"
    fallback: "paper/page-types/haipipe-page-for-section/ref/generic-template.md"
    shape: "current Narrative row overlaid on the resolved venue unit guidance or the explicit generic fallback"
---

# /haipipe-page-for-section · execute one Narrative row

Load `haipipe-page`, this Page Type, and `haipipe-page-workflow`. Declare
`page-type: section` and `section_kind: <kind>`.

## 📄 Grain and authority

One Section Page owns one reader-ordered manuscript or appendix unit. Main and
appendix Sections use the same contract; numbering and venue treatment may
differ.

Authority order:

```text
Seed boundary
  → selected Venue rules
  → current Narrative row and version
  → venue × section-kind structure/template
  → landed Page-local evidence
  → current prose
```

Prose never outranks a changed Narrative row or binding desk rule.

## 🏠 Runtime home (0.3.1)

```text
0-paperboard/
├── Ba1-SM-ms-main/        S<D><NN>-<kind>   first desk's main reading order
├── Ba2-AM-ms-appendix/    A<D><NN>-<slug>   its appendix units
└── Bb1-SW-wise-main/      a later desk's pair (a pair may be single)
```

Tokens carry the desk letter per the door's group grammar: `S<D>` for main
units, `A<D>` for appendix units, `<D>` the desk's first distinctive letter.

**Where the words live (0.3.1)**: the tex a unit page tracks sits in its
telling's desk room, `<N>-<desk><year>/sections/`, and that room is
self-contained per the door's room law — the unit's `\includegraphics` paths
resolve inside the room's `displays/` (copies of accepted page-local display
units), and its citation keys resolve in the room's own `reference.bib`
(assembled from the consuming pages' `bibex/`). A unit whose tex reaches into
another room, a shared top-level folder, or a page's `display/` directly is a
defect: copy the artifact into the room and name the owning page as
provenance.

Older repos using `1-SC-main/`, `2-SA-appendix/`, the `SC`/`SA` tokens, or a
shared `0-sections/`/`0-display/` are grandfathered and migrate only on
explicit request.

## 📥 Required contract block

Record these fields in the Page before drafting:

```text
narrative-row       id + version
section-kind        abstract · introduction · theory · methods · results ·
                    discussion · appendix · venue-specific kind
reader-question     the one question this Section answers
entry-state         what the reader already believes/knows
exit-state          what must be established on exit
claim-ids           exact Narrative claims landing here
venue-allocation    binding desk rules + observed pack guidance, distinguished
structure-source    resolved QBv unit division for this kind, or the explicit
                    generic fallback
evidence-allowlist  card, citation, value, and display ids
transition-in/out   required joins to neighboring Sections
```

If the Narrative row is missing or stale, stop section drafting and repair the
Narrative first.

## 🧱 Content outline

Resolve paragraph or move divisions from the QBv Venue Page's Unit Guidance
division matching this Page's `section_kind`, reached through the governing
Narrative's division-1 binding (0.2.0: the old `section-page-template: 1`
universe held zero files, so it can no longer be a source). Raw pack `style.md`
files and stage-era playbook material stay informative: they may feed a typed
PACK OBSERVATION on the QBv page, but they may not become `structure-source`.

If the bound Venue Page has no unit division for this kind, use
`ref/generic-template.md`, record the fallback, and raise the missing division
as a gap on the QBv page; never invent venue-specific rules locally.

Each Content division states:

```text
reader move
claim ids advanced
evidence/citation/value/display bindings
expected prose or display placement
transition to the next move
known limitation or unresolved obligation
```

## 🃏 Landing evidence in prose

Literature, values, and displays are not separate Page Types. They land through
the Section's Page-local plugins:

```text
pagex/            Probe's accepted-Page lane: bounded source Page context
probe/<card>/     Probe's Task/Discovery QA lane: answer, proof, interpretation
bibex/            citation card and bibliography key used by the sentence
display/<unit>/   intake, recipe, artifacts, caption, bindings, acceptance
```

The value plugin is a storage-less surface over `probe/<card>/card.md` and the
Section prose. Cite one exact number as `PP<NN>.v<n>`; never create `value/` as
a second home.

Every consequential sentence must be one of:

- supported by one or more card/citation/value/display ids;
- explicitly framed as interpretation and bounded by its evidence;
- visibly marked as an open obligation that prevents closure.

One Section may cite many displays, including displays owned by another Page,
but it must record the source unit and accepted version. It may also own several
local displays.

## 🔁 Retargeting

On a venue change:

1. Bind the Section to the new Narrative row.
2. Re-resolve venue × kind structure and hard constraints.
3. Preserve evidence ids whose meaning and scope remain valid.
4. Reopen prose, citations, and displays whose role or placement changed.
5. Compile and CHECK the new built version.

## ✅ Closing checks

- Exactly one current Narrative row governs the Page.
- Reader entry and exit states match neighboring rows.
- Every claim and consequential sentence has inspectable support or an open
  obligation.
- Every citation key resolves; every value has provenance; every cited display
  names an accepted artifact version.
- Venue rules are distinguished from pack observations.
- The generated TeX/PDF/DOCX reflects the accepted Page version.
- CHECK, not prose completion, closes the Section.

This variant owns no scripts. It owns `ref/generic-template.md`, the explicit
fallback that keeps every Section kind executable while venue templates are
migrated one by one.
