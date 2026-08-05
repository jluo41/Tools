---
name: haipipe-paper-conform
description: "Audit a paper folder against the layout contract: the delete test (rm -rf 0-* 1-* 2-* must leave a paper that still compiles), two numbered roots, direct S01–S10 lifecycle folders, nested S03/S04 topic probes, displays/ as the only home of an asset, sections/ naming + wiring, and every \\input/\\includegraphics/\\bibliography target resolving. Report-only; routes each finding to the skill that fixes it. Trigger: check paper structure, structure audit, paper folder check, validate paper layout, conformance, delete test, /haipipe-paper-conform."
allowed-tools: Bash, Read, Grep, Glob
metadata:
  version: "0.2.2"
  last_updated: "2026-07-26"
  summary: "Conformance audit for the paper-folder layout; report-only. THE machine test for the delete test and the eight-family board."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-conform (3-deliver)
=======================================

Answer one question: **does this folder conform to the layout ruled on the design board (QA6)?**
Report-only; this skill never edits a file.

It is the verification step `haipipe-paper-scaffold` and `haipipe-paper-restructure` run before
they may report `ok`, and it is the only thing that can tell you a paper folder is correct.

The contract, in one line
-------------------------

**The NUMBER is the delete test.**

```text
0-lifecycle/   the board, including nested S03/S04 probe entries
2-src/         how the deliverable is BUILT, not what it is
<unnumbered>   IS the deliverable

rm -rf 0-* 1-* 2-*     and the paper still compiles and still submits
```

A file that breaks the build when deleted has no business carrying a number. That is not a
convention this skill enforces by taste; block J below runs it as an actual test, by resolving
every `\input`, `\includegraphics` and `\bibliography` target the masters reach and asserting
none of them sits behind a number.

Usage
-----

```
/haipipe-paper-conform <paper-dir>
/haipipe-paper-conform          (current dir)
```

Workflow
--------

### Step 1: Run the mechanical checks

```bash
scripts/check_structure.sh <paper-dir>
```

Exit 0 = conforms, 1 = findings, 2 = not a paper folder (no `0-lifecycle/`).

| Block | Checks |
|-------|--------|
| A folder | `0-lifecycle/` exists at all; every paper is Board-first |
| B numbers | exactly two numbered roots are legal: `0-lifecycle` and `2-src`. Any other top-level `[0-9]-*` file or folder is a finding. Missing `2-src/` is a ⚠ before the manuscript upgrade |
| C assets | no `figures/`, `Figures/` or `0-displays/`; no `Figure/`/`Table/` flat buckets under `displays/`. A display is a UNIT and its render lives in `displays/<unit>/assets/` |
| D board | `0-lifecycle/` holds direct `S01-opening` through `S10-round` folders, `_archive/`, and generated Board indexes. S03 and S04 may hold `probes/<topic>/` entries; S05 may hold its display workspace. Each `S-<Family>-…` page sits in its family folder |
| E masters | unnumbered `*.tex` carrying `\documentclass`. None yet is a ⚠: legal before the manuscript upgrade |
| F build | `2-src/compile.sh` present + executable once a master exists; a surviving `1-compile.sh` is a ✗ |
| G naming | `sections/` + `appendices/`: `NN[-MM]_<slug>.tex` / `X_<slug>.tex` grammar, `NN` and `NN-MM` contiguity, `NN-MM` groups have their `NN_` wrapper. A surviving `0-sections/` is a ✗ |
| H wiring | every section file `\input` exactly once (orphans ✗, double-inputs ⚠); wrappers hold only `\input` lines; unstarred `\section{}` in a leaf ⚠ |
| I paths | every `\input`, `\includegraphics`, `\bibliography` target exists on disk |
| **J delete test** | **no target the deliverable reaches, and no master, `.bib`, `.cls` or `.bst`, sits behind a `0-`/`1-`/`2-` prefix** |
| K hygiene | lingering aux files ⚠; a surviving `STATUS.md` ⚠ (its frontier is derived from disk, so a stored one can only go stale) |

### Step 2: Judgment checks (the script cannot see these)

Read briefly and report, do not fix:

- Filename slug still describes the file's content (`02-05_trait-rating-correlation.tex` should be about trait-rating correlation).
- Driver `\input` order matches the venue's section order.
- Appendix leaves (`A_*`..`Z_*`) are reached only from the appendix driver, main sections only from the main driver.
- A `displays/<unit>/` whose `float.tex` is `\input` by nothing (a parked display, not a defect; say so).
- A display unit missing its `assets/` (the render was never produced) versus missing its `float.tex` (the unit was never wired).

### Step 3: Report + route

Present findings as a table, severity-ranked (✗ before ⚠), each row with its fix route:

| Finding | Fix route |
|---------|-----------|
| Any block B / C / G ✗, or a J delete-test failure | the restructure flow (retired; this skill owes its repair half, see `../../_old/README.md`); the old layout needs migrating, not patching |
| Numbering gap, orphan, wrapper prose, stray asset, in an otherwise conforming folder | same retired restructure flow, repair mode (debt: `../../_old/README.md`) |
| Missing folder/driver/compile script (skeleton incomplete) | `/haipipe-paper-folder` (the scaffold upgrade it owes, see `../../_old/README.md`) |
| Block D: an unowned build product or sidecar inside `0-lifecycle/` | move it out; only the declared `S05-display/` workspace exception belongs there |
| Block D: an `S-…` page in the wrong family folder | `/haipipe-board` owns the filename rule (`stage.py resolve`); move the file, then rebuild |
| Broken `\includegraphics` (the render was never produced) | the Display stage; the render comes from a task or discovery run, never from ad-hoc plotting |
| Broken `\cite` / bib content problems | `/haipipe-paper-check-evidence` (out of scope here; only the `.bib` file's existence is checked) |
| Prose problems noticed in passing | the section stage (mention, do not expand) |

Clean run = say so in one line and stop; do not invent findings.

What this skill deliberately does NOT check
-------------------------------------------

- Whether the prose is any good, whether a claim is supported, whether a citation resolves to a real paper. Those are `2-audit`'s and CHECK's.
- Whether a `[Q-…]` bracket is discharged. That is the phase workers' and `check-probe-cards.sh`'s.
- Whether the paper compiles. That is `/haipipe-paper-compile`; this skill only asserts that the pieces a compile would need are present and reachable.

Return contract
---------------

```
status:    ok (conforms) | findings | failed
summary:   counts: ✗ / ⚠, one line per finding category; ALWAYS state the J verdict explicitly
artifacts: [findings table]
next:      the single highest-leverage fix route from Step 3
```
