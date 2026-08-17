
## 0.7.0 — 2026-08-17

Exposes the derived Evidence Bundle at the frozen Point address and makes the
EVIDENCE→REVISE handoff explicit for sentence realization and Display render.

## 0.6.0 — 2026-08-17

**The card is created at PROBE, not by DRAFT.** §🧾's "a card may arrive already
PROPOSED … DRAFT is allowed to create any of the three in OWED state" is
replaced by a per-kind table: 🔢 created by PROBE from the outline's mark, 📚
landed by a person (PROBE opens a card only when the key is UNKNOWN), 🖼 created
HERE and nowhere earlier, because a unit's `intake/` freezes FROM a `proof/`
that does not exist until an answer does.

- §🔎's six-step loop keeps all six steps and now names their owners: ①②③ are
  `haipipe-page-probe`'s, because they end when the question leaves, and ④⑤⑥ are
  this phase's, because they begin when something comes back.
- §🪪 corrected: `PROBE` is a LIVE phase again and is NOT this one. The alias
  holds only for receipts written before 260817, which is also how
  `65-plugin-pageflow.js` now resolves the token.
- §🔀 enters from PROBE rather than from DRAFT.

## 0.5.0 — 2026-08-16

RENAMED from `haipipe-page-probe`, and the scope moved with the name (JL 260816).

- The phase token is `EVIDENCE`; `PROBE` is normalized wherever a phase or route
  is read (`src/page_lifecycle.py`, `src/page_context.py`, the pageflow stepper),
  so the two receipts already on disk and every `· PROBE ·` Related-Pages row keep
  auditing and parsing unchanged.
- WIDENED from one evidence kind to three: a CITATION (bibex entry), a VALUE
  (probe card bound to its QA file), and a DISPLAY INTAKE (frozen snapshot plus
  the named renderer). They are one phase because they chain: bank answer ->
  probe card -> display intake -> float.tex -> latex/word.
- A card may arrive already PROPOSED by DRAFT; EVIDENCE fills it and never
  opens a second one for the same unknown. EVIDENCE may also propose a card when
  gathering reveals a claim the outline missed.
- Added step ⑥ CARD to the loop, and made it the EXIT TEST: "every claim the
  outline promised has its card on disk, and every declared display unit has a
  frozen intake and a named renderer". The old exit, "the answer came back", is
  what let QV2-lbp-regression-results reach LaTeX with 5 declared units and 2
  rendered.
- Declared the display walk's SPLIT so no step is unowned: ① INTAKE is EVIDENCE's,
  ②③④ RENDER/PICK/BUILD are REVISE's, ⑤ ACCEPT stays the human gate at CHECK.
- Receipt gains `cards` and `renderers` rows. A frozen intake with no named
  renderer is a HOLD, not a pass.
- DESIGN was weighed as the new name and rejected: `page-types/haipipe-page-for-design`
  already holds the word, and a DESIGN phase would carry DRAFT's authority over
  purpose and Aims.

haipipe-page-probe · Changelog
==============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.4.0 - 2026-08-06

The lifecycle runs COLLECT-first on evidence pages (JL 260806): collect the
new Q-consumer into the owning topic's E0 queue → translate it into an E<n>
division + its QA-probe (① ORGANIZE) → dispatch → copy the A-executor back
into the QA-probe → write each A-consumer under the division's `####
consumers` rows (⑤ INTERPRET). Vocabulary finalized: QA-probe / QA-bank, four
capital slot words; the write-surfaces table names the E0 queue and E<n>
division parts explicitly.

## 0.3.3 - 2026-08-06

Wording sweep for JL ruling B (260806: "an entry is a source file the topic
page points at, like a PDF; the board renders the topic page, never the
entry"): the persisted surface's vocabulary entry is now the probe QA (the
entry record), a hidden `<n>-<slug>.md` source record below the topic page's
probes/ folder, never a board page; one conversation, two QAs: the bank QA is
the original, the probe QA is the consumer's copy that points at it. The
family-contract and Files closings name the probe QA instead of a Probe Page.

## 0.3.2 - 2026-08-05

Load-order slot reworded for thin-paper phase 2: the last slot is the family
DOOR's probe tooling (paper: `paper/haipipe-paper/probe/`), and the family DOOR
owns the persisted Probe Page shape and checker (was: "family workers own...").

## 0.3.1 - 2026-08-05

- The description leads with the plain job before the four coined Q/A terms, per the no-undefined-jargon rule.

## 0.3.0 - 2026-08-04

- Adds the shared RUN receipt boundary: PROBE records the unknown, executor and
  consumer artifacts, evidence bindings, limits, and one legal route.
- Allows an unchanged target-Page hash only when the separate probe artifacts
  make the work auditable; PROBE still cannot CLOSE.

## 0.2.0 - 2026-08-04

- Renamed from `haipipe-board-page-for-probe-entry` and moved under `page-phases/`.
- PROBE is now a Page phase rather than an Entry Page Type.
- Retains the canonical Q-consumer, Q-executor, A-executor, and A-consumer model from `haipipe-probe`, including one Q-executor serving several Q-consumers.
- Uses `Probe Page` for the optional persisted Board surface and treats older `entry` labels as implementation vocabulary rather than another lifecycle concept.

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
