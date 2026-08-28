---
name: haipipe-discovery-review
description: "Review type specialist for the discovery layer: analyze across sources — judge a claim (prior_art_check / counterevidence -> verdict.md) or map a field (landscape_review / benchmark_landscape -> landscape.md). Dispatches research-lit / comm-lit-review / academic-researcher; owns the Review Output Contract. Trigger: judge claim, prior art, counterevidence, landscape, lit review for a discovery, /haipipe-discovery-review."
argument-hint: "[<discovery-folder> | \"<claim-or-topic>\"]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.1.0"
  last_updated: "2026-07-03"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-discovery-review (type specialist)
=================================================

Owns the `Review` type: the Execute stage of a Review discovery-folder, or a one-off analysis. `role:` picks the flavor — judge (prior_art_check, counterevidence -> `verdict.md`) or synthesize (landscape_review, benchmark_landscape -> `landscape.md`).

Workers: `research-lit` (default, multi-source), `comm-lit-review` (communications domain), `academic-researcher` (cross-discipline template).

Procedure (Execute of a Review folder)
--------------------------------------

1. Read `discovery.yaml`: `question`, `role`, and `sources`. If `sources.from_source_folder` names a Search folder, read ITS sources.md/notes.md instead of searching; otherwise search + read inline (writing sources.md + notes.md as work products).
2. Dispatch a review worker with the Review Output Contract (below) appended to its args.
3. Judge roles: weigh evidence for/against, write `verdict.md` (status + confidence + Answer + Evidence + Caveats). Synthesize roles: cluster the field, write `landscape.md` (taxonomy + gaps + references). Templates: `haipipe-discovery/ref/discovery-yaml-schema.md`.
4. Counter-evidence is reported, never smoothed over; a verdict never overstates what the sources say.
5. Return to the caller: the terminal path, the verdict status (or cluster/gap counts for a landscape), and the NEEDS-VERIFICATION count. discovery.yaml itself is the orchestrator's to write, not this skill's.

One-off calls (no folder): same analysis, returned INLINE in the terminal's format — write no files.

Review Output Contract (canonical home)
---------------------------------------

Append this to the args of any review-worker dispatch. Short author-year tags alone are NOT matchable by the reader. Every analysis MUST satisfy all five rules.

```
1. FULL NAMES, never bare tags. Each paper gets a FULL citation on first mention AND a line in
   the reference list: full title (verbatim), full author list (first three + et al. only when
   >= 6 authors), venue with vol(issue):pages or "arXiv preprint"/status, year + a LOCATOR
   (arXiv ID / DOI / URL). A short tag in prose is OK only if it maps to exactly one full entry.
2. NUMBERED REFERENCE LIST at the end ("References (full, verified)"): one self-contained,
   deduped line per paper; any in-text mention matches exactly one numbered entry.
3. DISAMBIGUATE COLLISIONS. Same author+year papers each get a distinguishing nickname in EVERY
   mention (Lu et al. 2025a vs Lu et al. 2025b). Never leave two papers both as "Lu 2025".
4. ONE-LINE PLAIN FINDING per paper (jargon-free).
5. VERIFICATION FLAG per paper: VERIFIED (id/DOI/venue confirmed via search) vs NEEDS-VERIFICATION.
   Never assert an unchecked citation; fabrication is the worst failure.
```

Any per-paper listing follows the one-paper-one-subsection rule (full title in the heading, never a table; canonical format: `haipipe-discovery/ref/source-format.md`). For deeper rigor (systematic search + adversarial citation verification), escalate to the deep-research lit-review pipeline (`Tools/plugin-workflows/academic-research-skills/deep-research`, mode `lit-review`).

This skill only executes; the folder lifecycle (Plan/Report) belongs to `/haipipe-discovery`.
