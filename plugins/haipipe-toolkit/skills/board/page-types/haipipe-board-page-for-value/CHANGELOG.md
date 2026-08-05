haipipe-board-page-for-value · Changelog
==============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.2.0 - 2026-08-05

**De-parallelized from the literature sibling; the route key is explicit** (review fix).

- The register carries a REQUIRED `route: inward` line (the base's type
  resolution step ②); it is what separates a page that must produce numbers
  from one that searches for papers.
- Close semantics moved to the core's new Register-row states section in
  `haipipe-board/ref/topic-entry-contract.md`; this file keeps only what BOUND
  means here: run, specification, and QA file named by path, paths that
  resolve.
- LOAD paragraph, close section, Files closer, and frontmatter summary
  rewritten in the inward route's own voice, producing what must exist; the
  two topic contracts no longer pass a noun-swap.

## 0.1.0 - 2026-08-05

**Created on JL's ruling** (QB6 Decision Now, option D + display standing alone:
"how about the -for-literature, and -for-values, and -for-display, I want to
include them as well").

The topic types load ONE shared core, `haipipe-board/ref/topic-entry-contract.md`,
and add only their route's translation layer, so the register and entry anatomy
is stated once. Display is mirror-shaped but stands alone: its unit is produced
BY the project and closes on human acceptance, not on shipping.
