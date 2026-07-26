haipipe-paper-stage — Changelog
================================

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
