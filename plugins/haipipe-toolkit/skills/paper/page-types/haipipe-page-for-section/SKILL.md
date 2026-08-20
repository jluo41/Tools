---
name: haipipe-page-for-section
description: >-
  The Paper Page Type for one reader-ordered manuscript or appendix Section. It
  executes exactly one current Narrative row, resolves venue-and-kind structure,
  and binds prose to Page-local values, citations, probes, and displays. Use when
  outlining, drafting, revising, checking, or retargeting one paper section.
metadata:
  outline:
    mode: resolved
    source: "paper/venue/**/template.md"
    marker: "section-page-template: 1"
    fallback: "paper/page-types/haipipe-page-for-section/ref/generic-template.md"
    shape: "current Narrative row overlaid on a current venue-and-kind template or the explicit generic fallback"
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
structure-source    resolved venue × kind template or explicit generic fallback
evidence-allowlist  card, citation, value, and display ids
transition-in/out   required joins to neighboring Sections
```

If the Narrative row is missing or stale, stop section drafting and repair the
Narrative first.

## 🧱 Content outline

Resolve paragraph or move divisions from the selected Venue and section kind.
A venue template is current only when its first metadata block carries
`section-page-template: 1`. Unmarked templates are stage-era playbook material:
they may inform a typed pack observation, but they may not become
`structure-source`. This prevents an old `0-lifecycle`, `1-probes`, or
`5-section-edit` scaffold from silently reviving the retired Paper runtime.

If no marked venue template exists, use `ref/generic-template.md` and record the
fallback; do not invent venue-specific rules.

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
