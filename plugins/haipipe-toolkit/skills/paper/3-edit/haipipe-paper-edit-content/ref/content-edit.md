# paper-edit-content — section / paragraph / sentence checklists

The full content pass at three granularities. Work top-down. See the parent
`SKILL.md` for scope and `../../_shared/` for file anatomy and the banner format.

> **Read these as a Round-1 review lens, not an edit list.** In Round 1 each
> failed checkbox becomes one `%% {CC-content-vMMDD}: <finding> | <suggestion>
> ========>` comment anchored to the target — you change no prose. The fixes
> described below happen only in Round 2, after the human replies `accept` /
> `modify`. See `../../_shared/comment-protocol.md`.

---

## Granularity 1 — Section

The unit: **one section = one job** in the paper's argument.

Before editing prose, state the section's job in one sentence. If you can't, the
scope is wrong — fix that first.

Checklist:

- [ ] **Job stated** — one sentence naming what this (sub)section contributes.
- [ ] **Maps to the file** — the job matches the filename slug and the
      `\subsection{}` title; rename both if it drifted (keep figure/`\label`
      keys per anatomy rules).
- [ ] **Order** — the section sits in the right place (check the wrapper's
      `\input` order and the surrounding sections' jobs).
- [ ] **Boundaries** — content that belongs elsewhere is moved out; missing
      content is pulled in.
- [ ] **Banner skeleton reads** — `grep '^% Para '` on the file: the sequence of
      `[id] Role -- point` lines should tell the section's story on its own. A
      gap, a duplicated role, or a point that doesn't follow from the last is a
      structural finding.
- [ ] **No orphan claims** — every claim is supported here or explicitly points
      to where it is.

Section-level moves: split a section doing two jobs; merge two doing one; reorder
paragraphs (banners move with them — no renumbering); cut a paragraph whose point
duplicates another's (its id retires).

---

## Granularity 2 — Paragraph

The unit: **one paragraph = one point** — the point written in its banner.

If you can't summarize a paragraph in its banner's one-line point, it is doing
too much — split it (new paragraph, new id). If two adjacent paragraphs share a
point, merge them.

Checklist:

- [ ] **Prose matches the banner point** — the paragraph argues exactly what its
      banner claims; if the prose drifted, fix the prose or fix the banner
      (whichever is true), never leave them disagreeing.
- [ ] **Topic sentence first** — the opening sentence states the point; the rest
      support it.
- [ ] **One point only** — no second idea smuggled into the tail.
- [ ] **Evidence attached or flagged** — a claim that needs a number or citation
      has one, or is marked `% TODO[values]` / `% TODO[cite]`.
- [ ] **Transitions** — the paragraph connects to the one before and after; the
      `Role` sequence should feel like a path, not a list.
- [ ] **Length** — roughly 3–8 sentences. A 1-sentence paragraph is a flag; a
      12-sentence paragraph is two paragraphs.

---

## Granularity 3 — Sentence

The unit: **one sentence = one assertion**, as short as the meaning allows.

Checklist:

- [ ] **Subject-verb early** — the reader meets the actor and action before the
      qualifiers.
- [ ] **One assertion** — split sentences that join two real claims with
      `and` / `which` / `;` when both deserve weight.
- [ ] **Cut hedges and filler** — "it is important to note that", "in order to",
      "very", throat-clearing openers ("In this section we…").
- [ ] **Concrete over vague** — name the thing; replace "performs well" with the
      number (or `% TODO[values]` if the number isn't here yet).
- [ ] **One term per concept** — use a single name per concept; note variants for
      the consistency pass rather than silently picking one across sections.
- [ ] **Active where it carries** — prefer active voice unless the object is the
      true topic.
- [ ] **House voice** — plain academic prose; avoid em dashes, rhetorical
      flourishes, and AI-tell phrasing.

Sentence editing is the **last** thing you do to a paragraph, after its point and
position are settled. For heavy sentence-by-sentence surgery, run finer
annotate → reply → improve rounds — the `paper-edit-improver` edits at the
`Pn.Sm` sentence level the Stage-1 format-checker laid down.

---

## Flagging the other topics (don't fix them here)

Content editing surfaces work for later passes. Drop an inline marker instead of
guessing:

```latex
The model achieved % TODO[values] accuracy on the held-out set.
This aligns with prior work % TODO[cite] on trait extraction.
```

`% TODO[values]` → topic ② (`haipipe-paper-edit-values`).
`% TODO[cite]`   → topic ③ (`haipipe-paper-edit-citation`).

Leaving a flag is correct; inventing a number or a citation is not.

---

## Done means (content, one section)

These are the **apply-done** targets (after Round 2). For the round-by-round
gate (review-done vs apply-done) see the parent `SKILL.md`.

- [ ] Section job is one sentence and matches the file.
- [ ] Every banner point is true; one point per paragraph; right length.
- [ ] Sentences are single assertions, filler cut, terms consistent in-section.
- [ ] Banners present, ids preserved, new ids only for new paragraphs.
- [ ] Every missing number/citation flagged, none invented.
