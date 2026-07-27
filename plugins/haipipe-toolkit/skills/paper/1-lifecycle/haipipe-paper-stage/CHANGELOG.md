haipipe-paper-stage — Changelog
================================

## [0.8.3] — 2026-07-26 — Q-consumer gets a Board-native home

- `create-page.py` now treats `Q-consumer` as a logical stage division and
  materializes it as recognizable checklist records in `## Items to Finish`.
- It no longer emits Q-consumer under `## Content`.
- Full Board templates such as Display preserve their own Content divisions and
  Items scaffold; Setext stage templates receive the standard Q record.
- Narrative and Section-edit ATX headings are now recovered as Content divisions;
  Display's literal `Q-Display-<n>` placeholder is recognized without an invalid
  word-boundary assumption.
- Dynamic Section-edit creation now resolves `--section-kind` against the Venue
  page's `Section Styles` record and honors its generic fallback; the public creator
  no longer treats `<resolved per (venue, section_kind)>` as a filename.
- Fixed three end-to-end creation defects: new Resource pages use the declared
  `board_slug: resources`, venue-pack paths render safely outside the stage folder,
  and full-Board templates instantiate `<n>` in their own Items scaffold.
- Setext logical divisions and pre-Q-consumer ATX content divisions are now merged
  instead of treated as alternatives, so venue-specific section templates retain
  both their structure overview and their paragraph-block scaffold.
- Stage contracts and all venue section templates now use the same checklist
  anatomy with Description, Reason, Probe, and Answer.
- All venue templates now carry the same no-DRAFT-gate sequence:
  DRAFT raises, PROBE fills, REVISE weaves, and CHECK presents.

## [0.8.2] — 2026-07-26 — phase and gate declarations win

- Run exactly the stage's `phases:` list; an omitted phase is not a runtime skip.
- All current stages use `gates: [check]`; `--depth` is the independent spend
  authorization.
- Phase provenance and approvals live in the owning S page's `## Log`.

## [0.8.1] — 2026-07-26 — the venue pin reads the `state:` line, not an invented frontmatter key

Found by running the skill against `Paper-Personality2Opioid-MISQ2026` rather than by reading it.

Yesterday's `STATUS.md` retirement moved the venue pin to "`S-Venue-0-venue.md` frontmatter, `venue:`". That field does not parse. `haipipe-board`'s face grammar is a CLOSED whitelist (`src/parse.py:145`): `state|owner|method|session|requires|style-from|provides|contract-source-hash`. A `venue:` key is invisible to the board, so the frontier predicate failed on the only real paper, and the fix was never going to be "add the key" — the whitelist is `haipipe-board`'s, ruled on its own board.

The pin needed no new field. It was already on the page's own `state:` line: `state: ✅ PINNED · MISQ 2026`. Corrected in 12 places across the stage contract, the console, the router, the two refs, the anatomy spec and `restructure`.

Recorded on design-board face `QA4` as the third cross-package gap of the day, with the rule it produced: **`haipipe-paper` may not invent a face-grammar key.** It uses a key that already parses, or it goes to the board's own board and asks.


## [0.8.0] — 2026-07-26 — rebuild the board after every write, re-read before every read

Implements the single-door ruling (design board `skills/diagrams/01-haipipe-paper-260725`, faces `QA1` + `QA4`, JL 2026-07-26): **`/haipipe-paper` is the single thing a human types**, and it CALLS `haipipe-board` to build and open the paper's `0-lifecycle/`. `haipipe-board` remains its own door for boards that are not inside a paper. Calling is not owning: `haipipe-board` still owns the format, the build, the filename rule, the html and the write-back.

- **New `## Rebuild the Board after every write`.** `enter` now leaves the human LOOKING at the board, which turns a stale `board.html` from an inconvenience into a defect: they are reading a picture of a paper that no longer exists. Every stage run ends by calling `haipipe-board` build and putting the deep link in the closing block.
- **And the reverse direction, which matters more.** RE-READ the S page off disk before acting. A human comment or a `>` lane may have arrived through `serve.py` since this session last looked, so the page can change underneath this skill. Never cache a page across a phase boundary. This is what keeps the two-channel design honest: `haipipe-board` writes the page from a human's click, so this skill may never assume it wrote it last.


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
