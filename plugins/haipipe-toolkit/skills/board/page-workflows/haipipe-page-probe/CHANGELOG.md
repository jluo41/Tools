## 0.4.1 — 2026-08-18

- Pointer added to `../haipipe-page-workflow/ref/phase-cards.md` §③, which
  states this phase and every sibling in the SAME six fields
  (`❓ ASKS · 📥 READS · 📤 WRITES · 🚪 EXITS · ✋ TICK · 🔀 ROUTES`). This
  contract still owns the reasoning; the card is the readable-across-phases
  summary, and the contract wins when they disagree.
- Board backlink retargeted: `QPw7`/`QPw8`/`QPw9` became `QPw00a`/`QPw00r`/
  `QPw00g` when JL ruled that pages which are not phases may not carry
  phase numbers.


## 0.4.0 — 2026-08-18

MATCH runs LATE, recorded as an open defect (JL 260818).

- Added the timing defect to `§🔗 MATCH order`: MATCH needs only the outline's
  MARK and not the stake, so nothing requires DRAFT to precede it, yet it lives
  inside PROBE which runs after DRAFT. A page therefore pays for its sentence
  scaffolds before discovering the answer already existed.
- Recorded JL's reading that put the lookup second ("OUTLINE, then the probe
  (pagex), and the draft") and why he is right about MATCH and not about the
  card, whose `consumer/` side needs the stake DRAFT writes.
- Stated why a split would be named MATCH and never PAGEX: PageX is one of
  MATCH's three lookups, so naming the phase after it is like naming EVIDENCE
  "bibex". Scored 2.5 of 4 versus 0.5 of 4 on `QPw00 §7.2`'s split test.
- Added the Board page backlink: `QPw3-probe` argues this phase.
haipipe-page-probe · Changelog
==============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions
match SKILL.md frontmatter `version:`. Newest first.

## 0.3.0 — 2026-08-17

Adds PageX/MATCH as the first read-only reuse lookup before QA-bank work. Exact
reuse keeps the existing QA path or Display id; similarity alone never closes
a question.

## 0.1.0 — 2026-08-17

First contract. PROBE was listed as a phase in `haipipe-page-workflow` 0.2.0 but
had no file of its own and borrowed `haipipe-page-evidence`, so three skills gave
three different answers to the same question (JL 260817: "具体的 proof 应该由谁来
做？我还没想好这部分是在 draft 阶段来做，还是在 outline 阶段来做？"):

```
haipipe-page-draft §🃏        DRAFT creates the card in OWED state
haipipe-page-evidence §🧾     "a card may arrive already PROPOSED" by DRAFT
haipipe-plugin-outline §📐    "the card is created at PROBE"
```

**The ruling: PROBE creates it. Never OUTLINE, never DRAFT.**

- OUTLINE may not, because a plan is rejectable in ten seconds and must leave
  nothing on disk; a card for a plan nobody approved is litter with an id.
- DRAFT may not, because the mark IS the proposal, and a second file saying the
  same thing is `haipipe-page-workflow` §🪞's duplication rule.
- The deciding reason is the STAKE: a card's `consumer/` side carries what the
  page loses if the answer never comes, that is an Aim, and Aims are written at
  DRAFT. PROBE is the earliest phase at which a complete card can exist.

Also fixed here rather than left open:

- **One mark is not one card.** Many bullets may share one card (`PP04` on
  QC1-visitlbp serves three), one bullet may need two, and a mark already
  covered gets its address appended to the existing card's `serves:` rather
  than a second card.
- **Which marks PROBE acts on**: 🔢 always; 📚 only when the key is unknown;
  🖼 never (its intake freezes FROM a `proof/` that does not exist yet, so
  EVIDENCE creates the unit); 🧮 never, which settles `haipipe-plugin-outline`'s
  open "⬜ whether 🧮 earns a folder" as NO: a proof is prose, resting on a
  pulled file that already lives in a probe card's `proof/`.
- **`coverage:` in the receipt**: how many marked bullets actually got a card.
  Declaring is free; this is the count that makes a gap a HOLD.

Siblings changed in the same pass: `haipipe-page-draft` 0.6.0 (§🃏 deleted),
`haipipe-page-evidence` 0.6.0 (the "DRAFT proposes" paragraph replaced),
`haipipe-page-workflow` 0.3.0 (the member table points here), `haipipe-page`
0.4.0 (seven phases in the lifecycle table).
