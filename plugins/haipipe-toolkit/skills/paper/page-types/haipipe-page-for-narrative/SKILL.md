---
name: haipipe-page-for-narrative
description: >-
  The VARIANT contract for the NARRATIVE page, exactly one per paper. It reads the accepted Opening plus venue structure and existing source Pages, then designs the paper's claim roles, argument arc, reader journey, section-by-section map, PageX source allocation, display moments, and handoff to Section pages. It does not absorb Opening, write section prose, or rediscover evidence. Use when deciding argument order, repairing a section map, assigning existing Pages to claims or sections, retargeting the story, or checking what each Section page must execute. Trigger: narrative page, paper arc, reader journey, section map, claim order, PageX allocation, page-type narrative, /haipipe-page-for-narrative.
metadata:
  version: "0.2.0"
  last_updated: "2026-08-17"
  summary: "Narrative is the story architecture between Opening and Section: it maps claims and existing Pages into reader order without owning Opening, evidence discovery, or prose."
  outline:
    mode: grammar
    source: "Opening handoff + venue blueprint + PageX source Pages"
    shape: "promise → claim roles → arc → reader journey → section map → source allocation → display moments → Section handoff"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-for-narrative · turn the promise into reader order

**LOAD `haipipe-page` FIRST.** It owns the shared Page frame and lifecycle. Load `haipipe-page-for-stage` when Narrative is an S page, `haipipe-page-for-opening` for its upstream contract, and `haipipe-plugin-pagex` when resolving existing source Pages.

This variant covers exactly one Narrative per paper.

```text
kind       subject                                  closes when
─────────────────────────────────────────────────────────────────────────
Narrative  the paper's claims in reader order and   a person accepts the
           the section map that executes that order  Section handoff
```

Declare `page-type: narrative`. The key is required and beats the filename under the base Page resolver.

## 🧭 Boundary

```text
Opening     establishes identity, venue position, promise, and hard limit
Narrative   decides claim roles, order, transitions, sections, and source allocation
Section     writes and revises prose against one assigned row
```

Narrative is not `for-argument` and not `for-paper-map`. Those are two views of the same Narrative responsibility and do not receive separate Page Types.

Narrative does not absorb Seed, Claims, Venue, or Pitch content. It reads the Opening handoff and keeps only the architecture needed downstream. A canonical Claims control page may still own claim status; Narrative assigns rhetorical roles and landing points without becoming a second ledger.

## 📥 Preferred and compatibility inputs

Preferred input is one accepted Opening page plus the venue blueprint and existing source Pages.

```text
Opening handoff + venue blueprint + PageX source Pages
                         ▼
                     Narrative
                         ▼
               one assignment per Section page
```

Until old runtimes migrate, synthesize the Opening input read-only from legacy Seed, Venue, Pitch, and Claims pages. Do not paste those pages into Narrative and do not delete them during compatibility reads.

## 🧬 Grammar Content outline

Every Narrative must perform the following roles, but the number and titles of divisions may follow the paper's actual logic.

```text
Promise           restate the accepted Opening handoff and hard limit
Claim roles       peak · setup · consequence · mechanism · boundary · support
Argument arc      what must be understood before each claim can land
Reader journey    what the reader believes, asks, and learns in sequence
Section map       one row per reader-ordered manuscript or appendix section
Source allocation which existing Pages support each claim and section
Display moments   what must be seen, not merely stated, and where it earns attention
Section handoff   the exact packet each Section page executes
```

The instance outline is a grammar, not a fixed list. A short empirical paper may combine roles; a theory paper may repeat setup and consequence. It is defective only when a role needed for handoff has no home.

## 📐 The Section map is the governing artifact

Write one row per section in reader order:

```text
section-id | reader job | claim role | must establish | PageX sources |
display moment | allocation/limit | enters from | hands to
```

- `reader job` says what changes for the reader.
- `must establish` is a proposition, not a topic label.
- `PageX sources` names existing Pages, never copied raw evidence.
- `display moment` may say `none`; Narrative requests attention but does not render or place a float.
- `enters from` and `hands to` make transitions inspectable.

A Section page must point to exactly one current row. Reordering rows reopens every affected Section assignment.

## 🔎 PageX and Probe are parallel

Narrative normally allocates existing Board Pages through PageX. It may inspect their internal probes and displays through those Page boundaries, but it does not redo their discovery.

Probe remains the direct route to Task and Discovery folders. If a required claim has no existing Page, Narrative records the gap and routes it to the owning Probe workflow; it does not create a local evidence investigation.

```text
existing Board Page ── PageX ──▶ source allocation
Task / Discovery folder ─ Probe ─▶ owning Page ─ PageX ─▶ Narrative
```

This is the current clean separation. PageX and Probe remain parallel contracts until a later design decision changes their relationship.

## 🎯 Retargeting

Narrative is venue-aligned and normally rewrites on retarget:

- Reread Opening's venue-free identity and newly aligned promise.
- Re-resolve section kinds and allocations from the new venue blueprint.
- Preserve source Page identities unless their relevance changed.
- Recut claim roles, arc, reader journey, display moments, and Section rows.

Do not protect an old order merely because prose already exists. Existing Sections become inputs to revision, not authority over the new map.

## 📥📤 Runtime shape

```text
<NarrativePage>.md
├── outline/    Narrative outline and section-map material
└── pagex/      bindings to existing source Pages
```

Narrative owns no `probe/`, `proof/`, manuscript `.tex`, bibliography bank, or display unit.

**Output:** the accepted Section map and one bounded handoff packet per Section page. It may open display requests through the display plugin, but formal rendering, acceptance, and placement remain with the owning Page and Section.

## ✅ Closing checks

- The Narrative promise matches Opening and does not exceed its hard limit.
- Every important claim has a rhetorical role and a landing section.
- Every Section row names a reader job, required establishment, and downstream handoff.
- Every source allocation resolves to an existing Page or is explicitly marked as a routed gap.
- Display moments serve named claims rather than decorating topics.
- No legacy control-page prose, raw evidence, local Probe work, or section prose has been copied into Narrative.
- A Section agent can execute its row without inventing the paper's global order.

## 📂 Skill files

```text
haipipe-page-for-narrative/
├── SKILL.md
└── CHANGELOG.md
```

This variant owns no scripts.
