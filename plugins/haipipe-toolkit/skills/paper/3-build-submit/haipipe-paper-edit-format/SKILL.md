---
name: haipipe-paper-edit-format
description: "Bring an existing LaTeX draft into line with venue formatting and style conventions. CHECK-phase whole-paper format pass in build-submit. Self-contained format checks. STUB — scope defined, checklist to be filled. Trigger: format pass, venue style, fix formatting, style conventions."
metadata:
  version: "0.0.1"
  status: stub
  stage: build-submit
  topic: format
---

# haipipe-paper-edit-format  (stub)

CHECK-phase whole-paper format pass in the build-submit layer. Runs **after** per-section editing (DRAFT/GATHER/POLISH/CHECK) is complete and the substance is settled. Self-contained: carries its own style checks.

Like every build-submit sub-skill it is **comment-first**: Round 1 inserts `%% {CC-format-vMMDD}: finding | suggestion ========>` and changes no text; apply waits for the human `========> {XX}:` reply.

## Scope

Surface conventions: the draft follows the target venue's style for headings, abbreviations, units, numbers, capitalization, and reference format.

## Intended checks (to be written)

- [ ] Abbreviations/acronyms spelled out on first use, used consistently after.
- [ ] Number and unit style per venue (e.g. `5\%` vs `5 percent`; SI spacing).
- [ ] Heading case and depth match the venue template.
- [ ] Figure/table caption style and placement per venue.
- [ ] Math formatting conventions (operators, vectors, function names).
- [ ] Reference list style matches the `.bst` / venue requirement.

## Done means

- [ ] Paper conforms to venue style.

> **Status:** stub. Fill the checklist into `ref/` when the format pass is activated.
