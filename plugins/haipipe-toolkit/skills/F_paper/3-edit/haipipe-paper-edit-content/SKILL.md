---
name: haipipe-paper-edit-content
description: "Review and edit the prose CONTENT of an existing LaTeX draft at section -> paragraph -> sentence. Topic ① of the 4-edit cycle. Comment-first: Round 1 inserts %% {CC-content-vMMDD}: findings and changes NO text; apply waits for the human ========> reply. Self-contained: carries its own structure/claim/flow checks. Use when a draft exists in 0-sections/ and you want to improve what the prose says and how it is built. Trigger: edit content, review content, comment pass, tighten section, restructure paragraphs."
metadata:
  version: "0.1.0"
  status: active
  stage: 4-edit
  topic: "① content"
---

# haipipe-paper-edit-content

Topic ① of the `4-edit` cycle: editing the **prose content** of a draft that
already exists. This sub-skill is **self-contained** — it carries its own
checks for structure, claims, and flow; it does not hand the work to `6-review`.

It changes *what the prose says and how it is built*. It does **not** verify
numbers or citations against their sources (that is `haipipe-paper-edit-values` and
`haipipe-paper-edit-citation`) — but it **does flag** a missing number or citation so
those passes have a target.

## Before you start

Read the shared foundations once:

- `../_shared/comment-protocol.md` — **the comment-first contract** (read first).
- `../_shared/tex-file-anatomy.md` — what one `.tex` is (driver / wrapper / leaf).
- `../_shared/paragraph-indexing.md` — the `% Para [id] Role -- point` banner.
- `../_shared/edit-cycle.md` — the review → reply → apply loop and the grid.

Then confirm where you are: this is column ① of the grid. Pick **one section**.

## Two rounds: comment first, apply later

This skill runs in the 4-edit comment-first mode (`../_shared/comment-protocol.md`):

- **Round 1 — review (default).** Read the section and insert concise findings as
  `%% {CC-content-vMMDD}: <finding> | <suggestion> ========>` anchored to the
  sentence/paragraph. **Change no body text** — the Round 1 diff adds only `%%`
  comment lines. The checklists below are *what you look for*, not *what you
  rewrite* — each issue becomes a comment, not an edit.
- **Round 1.5 — the human replies** in place: `========> {XX vMMDD}: accept |
  reject | modify: … | discuss: …`.
- **Round 2 — apply (gated).** Only now, and only for `accept`/`modify` replies,
  make the edit. Leave `OPEN`/`reject`/`discuss` alone. For heavy sentence
  surgery, run finer annotate → reply → improve rounds (the improver edits at
  sentence level).

## The pass, top-down (use as the Round-1 review lens)

Work **section → paragraph → sentence**. Get the section's job right, then each
paragraph's point, then the sentences. Fixing sentences inside a paragraph that
should not exist is wasted work.

The full checklist for each granularity is in `ref/content-edit.md`. In short:

1. **Section** — state the section's one job in a sentence; make the paragraph
   banner skeleton (`grep '^% Para '`) tell the section's story; fix boundaries
   and order.
2. **Paragraph** — one paragraph = one point (its banner's point); topic sentence
   first; merge/split so each banner is true.
3. **Sentence** — one assertion each; cut filler; concrete over vague; one term
   per concept.

## Flag, don't fabricate

When the content needs a number or citation that is not here yet, drop a marker
instead of inventing one:

```latex
The model achieved % TODO[values] accuracy on the held-out set.
This aligns with prior work % TODO[cite] on trait extraction.
```

These are grep targets for topics ② and ③. Leaving a flag is correct; guessing a
value or a citation is not.

## Done means (this section, content topic)

**Review done (`rR`)** — Round 1 + reply complete:

- [ ] Every section/paragraph/sentence issue below is captured as a
      `%% {CC-content-vMMDD}:` comment; none silently fixed.
- [ ] Round 1 diff added only `%%` comment lines (zero body-text changes).
- [ ] The human has replied (`========> {XX}:`) to every comment in the section.

**Apply done (`aD`)** — Round 2 complete:

- [ ] Every `accept`/`modify` reply applied; `reject` dismissed; `OPEN`/`discuss` left.
- [ ] After applying: section job is one sentence and matches the file/slug;
      every banner point is true; one point per paragraph; sentences are single
      assertions; banners present with ids preserved.
- [ ] Every missing number/citation is flagged (`% TODO[...]`); none invented.

When apply is done, mark the section's content cell `aD` and pick the next section.

## Reference

- `ref/content-edit.md` — the section / paragraph / sentence checklists in full.
