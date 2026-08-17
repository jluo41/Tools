haipipe-page-for-value · Changelog
==================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.5.0 - 2026-08-10

Value is now a **Value Display** page. Every E division keeps its QA-probe pointer and adds a
same-numbered `display/<topic>/<n>-<slug>.md` candidate card. The card can propose a table or
figure, or truthfully close as `not-displayable`; it carries takeaway, claim role, and disposition
rather than duplicating evidence. Narrative selects candidates, and only a selected candidate may
request a formal Paper Display unit.

## 0.4.0 - 2026-08-06

JL's final evidence-page design (ruled 260806): the flat `### Q-consumer
register` is retired. The page declares `route: inward` in its metadata
head (the type key, base resolution step ②) and organizes Content BY EXECUTOR:
one `### E<n> · <question>` division per Q-executor conversation, each owning
exactly one QA-probe (pointer line with state), a `#### consumers` block (one
row per collected Q-consumer: source page id, stake, A-consumer, row state),
and a `#### answer digest` of 2-3 lines. `### E0 · incoming` is the standing
collect queue: a Q-consumer born on any page lands there until PROBE promotes
it. Close rule: every division's consumers are BOUND, DEFERRED, or
WITHDRAWN, AND E0 is empty.

## 0.3.0 - 2026-08-06

Entries are hidden source records, not board pages (JL ruling B, 260806: "an
entry is a source file the topic page points at, like a PDF; the board renders
the topic page, never the entry"). Description now says "one probe QA (the entry record)
nested below probes/", the LOAD paragraph states the `<n>-<slug>.md` naming,
and the stake-wall sentence names the nested probe QA. Anatomy, twin-QA naming
law, and hiding mechanism live in the core
`haipipe-board/ref/topic-entry-contract.md`; nothing else here changed.

## 0.2.1 - 2026-08-05

Paper-family projection path repointed to
`paper/haipipe-paper/probe/topic-entry-contract.md` (workers/ dissolved,
thin-paper phase 2).

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
