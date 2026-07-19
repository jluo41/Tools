haipipe-paper-revise — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


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
