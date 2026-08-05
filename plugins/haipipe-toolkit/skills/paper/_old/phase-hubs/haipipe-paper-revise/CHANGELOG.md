haipipe-paper-revise — Changelog
## 2026-08-01

- Candidate-diff mode COMPUTES its word-level marks with
  `writing/haipipe-writing/cli/wdiff.py` instead of writing them by hand (JL).
  Hand-written, the diff comes out as a whole-sentence swap, which hides what
  SURVIVED the edit; that is the one thing a candidate lane exists to show.
- The worker roster names where the migrated methods now live: the weave method
  at `writing/haipipe-writing/ref/weaving.md`, the general AI-tell catalogue at
  `writing/haipipe-writing/ref/ai-tells.md`. Both left `paper/` on 260801
  because neither is academic; everything venue-owned stayed.

================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.

## [0.2.3] — 2026-08-04 — Page REVISE layering

- Loads the Stage Page Type and generic `haipipe-board-page-revise` before manuscript workers.
- Defines REVISE by fixed purpose and Aims rather than mandatory position after PROBE.
- Keeps placement first when evidence landed and routes changed intent to DRAFT or new unknowns to PROBE.

## [0.2.1] — 2026-07-26 — provenance lives on the S page

- `[REVISE]` worker proof now lives in the owning S page's `## Log`.
- `checks.sh --stage-page` replaces the retired `_LOG` input.
- Venue guidance reads `S-Venue-0-venue.md`.
- Preserved the invocation hint under `metadata.argument_hint`, which conforms to
  the current Skill frontmatter schema.

## [0.2.0] — 2026-07-26 — the venue guard reads the venue page

Aligned with the paper-folder layout ruled 2026-07-26 on the design board (`skills/diagrams/01-haipipe-paper-260725`, face QA6): `0-sections/` to `sections/`, `0-displays/` to `displays/` (one folder per unit, the only home of an asset, no top-level `figures/`), `1-compile.sh` to `2-src/compile.sh`, and `STATUS.md` retired. The venue guard, which blocks REVISE on a venue-ALIGNED artifact when no venue is pinned, was grepping `STATUS.md`. It reads `S-Venue-0-venue.md` frontmatter.


## [0.1.6] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.6.0; older entries below keep their original numbers).

## 1.6.0 — 2026-07-19 — a fourth worker, `place`, and it runs FIRST

From the `paper/2-phase` review (`../../../_console/260719-02-PHASE-BOUNDARY-REFACTOR.md`), ruling D7.

### Changed (JL: "Follow your recommendation.")
`haipipe-paper-revise-place` joins the roster and runs before every prose worker. The dispatch order becomes `place → content → humanizer → results`, and the order is BINDING, not stylistic: substituting a landed key or number after the prose workers have run drops it into sentences they had already closed, so the text that actually ships was never reviewed in its final form. Running the de-AI pass over `{VAL:? held-out accuracy}` and swapping in `0.87` afterwards reviews a sentence that does not exist.

- `workers:` proof line widened to `place ✓ content ✓ humanizer ✓ results --`. `checks.sh --log` FAILs a `[REVISE]` entry without it, so the line and the roster must stay in step.
- Dispatch table, phase diagram, return contract, `description:` and `summary:` all updated together; the roster was previously described as "Four workers" over a list of three.
- The phase's own definition was rewritten: REVISE reads what PROBE landed in each entry's `### a-executor`, PLACES it, then rewrites. It previously stated "REVISE reads PROBE outputs (citations placed…)" as a PRECONDITION — self-referential once placement became REVISE's own first step.


## [1.5.1] -- 2026-07-10

Changed
- Wording: the .md stays markup-free APART FROM citation commands (real-citation convention, JL 2026-07-10); REVISE resolves `\cite{TOADD}` slots whose keys have landed in .bib.

## [1.5.0] -- 2026-07-09

Changed (JL ruling 2026-07-09 (LLMTrait-Section session postmortem): normalize the writing process; closes feedback/2026-07-09_revise-skipped-humanize-and-outline-first.md)
- Proof-carrying contract (binding): stage hubs reach REVISE ONLY via Skill(haipipe-paper-revise) -- inline hand-editing = "the REVISE phase did not happen"; every run writes a [REVISE] _LOG entry with `workers: content/humanizer/results` line; checks.sh --log FAILs without it.
- Order of operations pinned: revise the working .md FIRST, then sync to tex -- never tex-first (the .md is what the human reads/comments).
- Automation steps now end with "hand back to the stage hub, which OPENS CHECK -- never commit or conclude before the CHECK gate opens".

## [1.4.0] — 2026-07-08

Changed (venue lockfile wiring)
- Venue norms + venue guard repointed: primary read = the paper's `0-lifecycle/2a-venue/2a-venue.md` (Writing Principles + Structural Blueprint block); direct `_venue/playbook-*` reads demoted to fallback (2a-venue.md absent) or deep dives via its `[source: ...]` tags; STOP/warning semantics unchanged.

## [1.3.0] — 2026-07-07

Changed (T7, JL: "maybe just go into Content")
- Worker roster 4 → 3: weaving retired and merged into content (its weave step + ref/weaving.md). Default order now content (incl. weave) → humanizer → results. Kills the router↔weaving mutual-dispatch contradiction (C11) structurally. Also C13: the REF/prose-quality.md pointer corrected to ../../REF/ (was resolving into the router's own folder).

## [1.2.0] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER->PROBE, POLISH->REVISE). Phase verb is REVISE: the agent changes prose directly and leaves why-comments; the human gives preferences in CHECK.

## [1.1.0] — 2026-07-03

- reframed as internal worker. Users invoke stage skills (pitch, narrative, section-edit...), not this skill directly. Stage skills call this during their POLISH phase.

## [1.0.0] — 2026-07-03

- new hub skill for the POLISH phase. Dispatches to polish-content, -humanizer, -weaving, -results based on section needs.
