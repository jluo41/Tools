## 0.6.1 — 2026-08-18

- Pointer added to `../haipipe-page-workflow/ref/phase-cards.md` §⑦, which
  states this phase and every sibling in the SAME six fields
  (`❓ ASKS · 📥 READS · 📤 WRITES · 🚪 EXITS · ✋ TICK · 🔀 ROUTES`). This
  contract still owns the reasoning; the card is the readable-across-phases
  summary, and the contract wins when they disagree.
- Board backlink retargeted: `QPw7`/`QPw8`/`QPw9` became `QPw00a`/`QPw00r`/
  `QPw00g` when JL ruled that pages which are not phases may not carry
  phase numbers.
- **Coherence sweep (260819)**: CHECK routes to all SEVEN of CLOSE | OUTLINE |
  PROBE | EVIDENCE | DRAFT | REVISE | HOLD, in §🔀, the receipt, and the
  description; the ticks table's `verified` and `read:` lanes are ③c and ③v
  per phase-cards; the common path reads PREPARE(①②③) → DRAFT → REVISE →
  CHECK.


## 0.6.0 — 2026-08-18

The tick roster was WRONG at 0.5.0: five, not four.

- 0.5.0 rostered FOUR person-reserved ticks and omitted the probe card's `read:`,
  whose reserving rule is `haipipe-plugin-probe`: "Only a person may tick it, and
  a changed `target` or a re-pulled `proof/` drops the tick back."
  Caught by an independent CHECK on `QPw00g-human-gate` the same day.
- Recorded which two of the five REVERT on changed inputs: `read:` and
  `accepted: ✅`. The other three do not.
- Recorded the sixth human-reserved write that is deliberately excluded because it
  is an ORDER and not a field: the row rank in `skill/` and `pagex/`.
- Corrected "no single surface collects them": `haipipe-board/live/outline.py`
  already collects four of the five, read-only, with no `<n> of <n>` count and
  no row for the Page Type's RULING.

## 0.5.0 — 2026-08-18

The gate is ACCEPT-BIASED, and the four ticks are rostered (JL 260818).

- Added `## ✋ The gate is ACCEPT-BIASED`, on JL's words "human should be more
  likely to accept it": present a gate only when `mechanical_errors` for that
  page is ZERO, so the gate is a confirmation rather than an inspection.
- Stated the one line the bias may not move: silence is not consent, and a
  required gate with no durable passed evidence still routes to HOLD.
- Rostered the board's FOUR ticks a machine may never write, with the file each
  lives on, the rule that reserves it, and its phase: `approved:` ①,
  `verified` ④, `accepted: ✅` ⑦, the Page Type's ruling ⑦.
- Recorded that no single surface collects the four, and pointed at `QPw00g`.
- Added the Board page backlink: `QPw6-check` argues this phase.

## 0.4.0 — 2026-08-16

CHECK judges the BUILT artifact, not only the Markdown (JL 260816).

- Added the built-artifact gate with six deterministic findings computed by the
  new `haipipe-board/src/page_evidence.py` and reported by `cli/check.py`:
  `display-declared-not-rendered` (naming the first missing step),
  `display-cited-not-embedded`, `display-rendered-not-cited`,
  `display-accept-stale`, `latex-untitled`, `projection-stale`.
- Stated the three-count rule: declared, rendered, and accepted are independent,
  folder count is never completed work, and a version whose declared count
  exceeds its rendered count does not pass.
- CHECK administers display-walk step ⑤ ACCEPT and never ticks it.
- Phase token PROBE -> EVIDENCE throughout.

haipipe-page-check · Changelog
==============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.3.1 - 2026-08-05

- Opening now states CHECK's own risk (becoming a hidden revision) instead of the shared ownership couplet.

## 0.3.0 - 2026-08-04

- Adds the shared RUN receipt and immutable version gate: CHECK records the
  source/render identity, verdict, findings, evidence, route, and human gate.
- Enforces producer != judge, re-CHECK after every content change, CLOSE only
  after pass, and HOLD for missing human evidence or concurrent mutation.

## 0.2.0 - 2026-08-04

- Renamed from `haipipe-board-page-for-stage-check` and moved under `page-phases/`.
- CHECK now applies to any Page Type, judges one concrete version, and routes to close, REVISE, PROBE, DRAFT new round, or an explicit hold.
- Removes the assumptions that CHECK is always last, always human, or always feeds the next DRAFT.
- Corrects `new round`: it reopens the promise on the same persistent Page and does not automatically create another unit.

## 0.1.0 - 2026-08-04

**Created** (JL: "ok, I agree, please go ahead and make them.").

Split out of the family workers so the four-phase loop has ONE rulebook instead of
one per family. Measured 260804: the paper and application families each shipped
their own draft/probe/revise/check hubs (1,263 lines against 531), and NONE of the
eight loaded `haipipe-page` at all, so each had copied the page grammar from
memory. `haipipe-paper-draft` still named `## Items to Finish` five times, a
section renamed that morning.

- Host-agnostic on purpose: names no venue, no markup, no checker. A family worker
  adds its artifact knowledge and obeys this file.
- Settles `QC6 A4.1`: paper and application share a CONTRACT, not folder names.
