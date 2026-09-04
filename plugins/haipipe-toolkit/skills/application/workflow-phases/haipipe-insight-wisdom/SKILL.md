---
name: haipipe-insight-wisdom
description: >-
  InsightBoard workflow phase I5 and Folder contract for Wisdom: contextual
  counsel from a bounded Knowledge claim plus the signed Design Handoff that
  is the only evidence a DesignBoard may bind. Trigger: insight wisdom,
  counsel, design handoff, I5, folder-kind wisdom, /haipipe-insight-wisdom.
metadata:
  version: "1.0.2"
  last_updated: "2026-08-31"
  workflow: haipipe-insight-workflow
  phase: I5
  folder_kind: wisdom
  primary_face: page
  page_ruling: domain-gate
  legacy_page_type: wisdom
  group-token: "W"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Context → Knowledge Cited → Counsel → Forbidden Overreach → Design Handoff"
---

# /haipipe-insight-wisdom · counsel, then hand off

Load `haipipe-folder`, `haipipe-page`, `haipipe-insight`, and the workflow.

## Position

I5 is the last Insight rung. It answers `QW`, closes the climb, and crosses to
Design only through a signed handoff. D/I/K prose never crosses directly.

## Folder Kind

Wisdom says **what the claim means here and what must not be concluded**. It
may counsel `do`, `avoid`, or `leave undecided`; it never writes message copy,
button text, send timing, variants, or another Design artifact.

## Input

One registered QW ask; Application audience/context/decision; source versions;
and unresolved gaps. Its epistemic parent is either named local K rows with
strength, rivals, and boundary, or one exact
`Task Insight Page/RF<n>@<version>` accepted by the workflow's pre-climbed
external-parent assertion. The second form is evidence input, not a handoff.

## Page Face

Use `Context → Knowledge Cited → Counsel → Forbidden Overreach → Design
Handoff`. Every `W<n>` cites a K parent. For a bridge Folder, `Knowledge Cited`
names the exact external K/W/RF row ids and Page version through PageX; it does
not copy them or pretend the RF is local K. The handoff carries finding,
strength, boundary, sources, design consequence, forbidden overreach, gaps,
`serves:`, and a final `signed:` token.

## Task Face

Test applicability against the K boundary; write bounded counsel; construct the
standalone handoff; stop for a person's signature; and reopen the counsel and
signature when a K parent changes. For a bridge, first verify the Task Page's
CHECK closure, Wisdom target, full DIKWRF trace, current source versions, I1
registration, and exact PageX pin; then contextualize it here. Under a valid
POOL verdict, non-template W Folders close by explicit deferral and export no
handoff.

## Plugins

- `pagex` required for local K parents or the exact Task RF parent;
- `outline` required;
- `probe` optional for an applicability gap;
- `code` forbidden: this phase contextualizes accepted claims.

## Gate and Closure

GI5 passes only when counsel stays inside its K parents, forbidden overreach is
visible, the handoff reads standalone, and `signed: ✅ <initials> <YYMMDD>`
records a person's decision. `signed: ⬜` is a clean stop, not permission to
infer approval. A bridge also requires the external-parent assertion to remain
current; RF settlement alone cannot pass GI5. GI6 is the following I1 register-settlement act;
this Folder does not perform or rename it.

## Handoff

Export only the signed Design Handoff. A DesignBoard binds it through PageX
and never re-derives from D/I/K Folders. A deferring W Folder exports only a
pointer to the template handoff. A Task RF never crosses this boundary directly:
the local signed W is the only Design authority.

## Files

- Page and handoff: `<WisdomFolder>/<WisdomFolder>.md`
- External-parent binding, when used:
  `<WisdomFolder>/evidence/pagex/<WisdomFolder>.md`
- Cross-board binding: the DesignBoard's `evidence/pagex/`
