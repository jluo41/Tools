---
name: paper-edit-citation
description: "Make every \\cite in an existing LaTeX draft resolve, be real, and support its claim. Topic ③ of the 4-edit cycle. Self-contained citation checks. STUB — scope defined, checklist to be filled. Trigger: check citations, verify references, citation pass, fix cites."
metadata:
  version: "0.0.1"
  status: stub
  stage: 4-edit
  topic: "③ citations"
---

# paper-edit-citation  (stub)

Topic ③ of the `4-edit` cycle. Runs **after** content and values for a section.
Self-contained: it carries its own citation-checking logic rather than
delegating to `6-review`.

Read `../_shared/` first — especially `comment-protocol.md`. Like every 4-edit
sub-skill it is **comment-first**: Round 1 inserts `%% {CC-cite-vMMDD}: finding |
suggestion ========>` and changes no text; apply waits for the human
`========> {XX}:` reply.

## Scope

Every `\cite` key resolves to a real, correctly-attributed entry in the `.bib`,
and the cited work actually supports the claim it is attached to.

## Intended checks (to be written)

- [ ] Each `% TODO[cite]` flag from the content pass is resolved with a verified ref.
- [ ] Every `\cite{key}` resolves to an entry in the project `.bib`.
- [ ] No orphan bib entries (defined but never cited) unless intentional.
- [ ] Each entry is real (author / year / venue / DOI verifiable) — no hallucinations.
- [ ] Claim-faithfulness: the cited paper supports the specific claim made.
- [ ] Citation style and placement consistent with the venue.

## Done means

- [ ] No `% TODO[cite]` left; every `\cite` resolves, is real, and is on-claim.
- [ ] The section's ③ cell → `done`.

> **Status:** stub. Fill the checklist into `ref/` when topic ③ is activated.
