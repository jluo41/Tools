haipipe-board-page-probe · Changelog
=====================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

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
eight loaded `haipipe-board-page` at all, so each had copied the page grammar from
memory. `haipipe-paper-draft` still named `## Items to Finish` five times, a
section renamed that morning.

- Host-agnostic on purpose: names no venue, no markup, no checker. A family worker
  adds its artifact knowledge and obeys this file.
- Settles `QC6 A4.1`: paper and application share a CONTRACT, not folder names.
