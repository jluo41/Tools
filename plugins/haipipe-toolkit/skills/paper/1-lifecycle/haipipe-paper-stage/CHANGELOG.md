haipipe-paper-stage — Changelog
================================

## [0.7.0] — 2026-07-26 — the eight contracts speak the ruled layout, and the gate row leaves STATUS.md

Aligned with the paper-folder layout ruled 2026-07-26 on the design board (`skills/diagrams/01-haipipe-paper-260725`, face QA6): `0-sections/` to `sections/`, `0-displays/` to `displays/` (one folder per unit, the only home of an asset, no top-level `figures/`), `1-compile.sh` to `2-src/compile.sh`, and `STATUS.md` retired. These are the skill family's most binding paths: a contract's `artifact:`, `probes:`, `units:` and `output:` resolve at run time, so a stale one does not read wrong, it writes to the wrong place.

- **`handoff:` rewritten on all six gated contracts.** Was `update STATUS.md (current_layer, maturity: X)`. Now `append the gate row to this stage's S page ## Log`. The Gate Ledger was the one part of `STATUS.md` that is HISTORY and cannot be derived from disk, so it needed a home rather than a deletion; it now sits on the page whose gate it was, where a reader is already standing.
- **`0-seed`'s loopback warning dissolved rather than reworded.** It spent four lines protecting a stored `current_layer` from being demoted by a re-run. With no stored frontier there is nothing to demote: a loopback records its gate and changes nothing else.
- **The venue pin moved.** `2a-venue`'s `pins: STATUS.md` is now `pins: 0-lifecycle/2-venue/S-Venue-0-venue.md`, into that page's own frontmatter. One page owns the venue contract; a second copy could only disagree with it.
- **`stages/CONTRACT.md` gained two sections**: the paper-folder paths a contract may name (and the four it must never name), and why `STATUS.md` is retired with where each of its four parts went.
- Verified: `check-contracts.py` `form ok` across all eight, and every `artifact:` path resolves on `Paper-Personality2Opioid-MISQ2026` except the two already known (`4-display`, blocked on QB2; `5-section-edit`, which is per-unit by design).
- Pre-existing and NOT introduced here: `2a-venue/stage.md`'s frontmatter does not parse under a strict YAML loader. It fails identically at `HEAD`. Untouched.


## [0.6.0] — 2026-07-25

**Paper Stage now has one Board-first page-creation path.**

- `create-page.py` is the public creator: it resolves one stage through `index.yml`, calls the
  Board's `stage.py new` primitive, and composes the selected stage template into Content jobs.
- Stage contracts identify pages with `board_family` + `board_unit`; Board tooling owns literal
  filenames.
- Page dependencies are optional. When present, page `requires:` is authoritative; optional
  `read_order:` remains craft guidance rather than a duplicate graph.
- Per-unit is governed by independent human gates. Section Edit implements that grain; Display
  qualifies and remains a tracked migration. The other six stages stay single-output.

## [0.5.0] — 2026-07-25

**The board mapping now carries explicit inherited contracts.**

- Display moved from Work 2 to its own `Display 0` family and board face.
- Mapped S pages may declare `requires`, `style-from`, and `provides`; these fields inform the
  board contract without changing router execution.
- The router refreshes the managed Stage Contract through `haipipe-board/stage.py` after upstream
  changes, while authored Content and legacy artifact/log paths remain untouched.

## [0.4.1] — 2026-07-25

**Stage contracts now map explicitly onto lifecycle-board S faces.**

- Every stage declared `board_family`, `board_unit`, and (at that version) `board_face`.
- The mapping is informational: stage execution still follows `index.yml`, `upstream`, and
  `downstream`, so a stable board family does not falsely redefine execution order.
- After a phase changes its artifact, the mapped S face receives same-turn state, finish-item,
  and current-status synchronization. Embedded Content is not copied.
- Submission and revision remain downstream board rounds, not new stage-router keys.

## [0.4.0] — 2026-07-20

- Consolidated eight paper stages behind one router and one stage contract loaded per invocation.
