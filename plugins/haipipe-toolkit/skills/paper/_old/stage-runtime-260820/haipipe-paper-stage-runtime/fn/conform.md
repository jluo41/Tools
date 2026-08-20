# Door verb: conform (paper-folder conformance audit)

Answer one question: **does this folder conform to the layout ruled on the design board (QA6)?**
Report-only; this fn never edits a file.

It is the verification step the `folder` fn's manuscript upgrade runs before it may report
`ok`, and it is the only thing that can tell you a paper folder is correct.

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
convention this fn enforces by taste; block J below runs it as an actual test, by resolving
every `\input`, `\includegraphics` and `\bibliography` target the masters reach and asserting
none of them sits behind a number.

Usage
-----

```
/haipipe-paper conform <paper-dir>
/haipipe-paper conform          (current dir)
```

Workflow
--------

### Step 1: Run the mechanical checks

The check script lives with the door:

```bash
sh paper/haipipe-paper/scripts/check_structure.sh <paper-dir>
```

Exit 0 = conforms, 1 = findings, 2 = not a paper folder (no `0-lifecycle/`).

```text
A folder    0-lifecycle/ exists at all; every paper is Board-first
B numbers   exactly two numbered roots are legal: 0-lifecycle and 2-src. Any other
            top-level [0-9]-* file or folder is a finding. Missing 2-src/ is a ⚠
            before the manuscript upgrade
C assets    no figures/, Figures/ or 0-displays/; no Figure//Table/ flat buckets under
            displays/. A display is a UNIT and its render lives in displays/<unit>/assets/
D board     0-lifecycle/ holds direct S01-opening through S10-round folders, _archive/,
            and generated Board indexes. S03 and S04 may hold probes/<topic>/ entries;
            S05 may hold its display workspace. Each S-<Family>-… page sits in its family folder
E masters   unnumbered *.tex carrying \documentclass. None yet is a ⚠: legal before the
            manuscript upgrade
F build     2-src/compile.sh present + executable once a master exists; a surviving
            1-compile.sh is a ✗
G naming    sections/ + appendices/: NN[-MM]_<slug>.tex / X_<slug>.tex grammar, NN and
            NN-MM contiguity, NN-MM groups have their NN_ wrapper. A surviving
            0-sections/ is a ✗
H wiring    every section file \input exactly once (orphans ✗, double-inputs ⚠); wrappers
            hold only \input lines; unstarred \section{} in a leaf ⚠
I paths     every \input, \includegraphics, \bibliography target exists on disk
J DELETE    no target the deliverable reaches, and no master, .bib, .cls or .bst, sits
   TEST     behind a 0-/1-/2- prefix
K hygiene   lingering aux files ⚠; a surviving STATUS.md ⚠ (its frontier is derived from
            disk, so a stored one can only go stale)
```

### Step 2: Judgment checks (the script cannot see these)

Read briefly and report, do not fix:

- Filename slug still describes the file's content (`02-05_trait-rating-correlation.tex` should be about trait-rating correlation).
- Driver `\input` order matches the venue's section order.
- Appendix leaves (`A_*`..`Z_*`) are reached only from the appendix driver, main sections only from the main driver.
- A `displays/<unit>/` whose `float.tex` is `\input` by nothing (a parked display, not a defect; say so).
- A display unit missing its `assets/` (the render was never produced) versus missing its `float.tex` (the unit was never wired).

### Step 3: Report + route

Present findings severity-ranked (✗ before ⚠), each with its fix route:

```text
any block B / C / G ✗, or a J delete-test failure
        -> the restructure flow (retired; conform still owes its repair half, see
           ../_old/README.md); the old layout needs migrating, not patching
numbering gap, orphan, wrapper prose, stray asset, in an otherwise conforming folder
        -> same retired restructure flow, repair mode (debt: ../_old/README.md)
missing folder/driver/compile script (skeleton incomplete)
        -> the door's folder verb (fn/folder.md, the manuscript upgrade)
block D: an unowned build product or sidecar inside 0-lifecycle/
        -> move it out; only the declared S05-display/ workspace exception belongs there
block D: an S-… page in the wrong family folder
        -> /haipipe-board owns the filename rule (stage.py resolve); move the file, then rebuild
broken \includegraphics (the render was never produced)
        -> the Display stage; the render comes from a task or discovery run, never ad-hoc plotting
broken \cite / bib content problems
        -> the section-edit CHECK evidence lane (check-evidence-craft.md; out of scope here;
           only the .bib file's existence is checked)
prose problems noticed in passing
        -> the section-edit stage (mention, do not expand)
```

Clean run = say so in one line and stop; do not invent findings.

What this fn deliberately does NOT check
-----------------------------------------

- Whether the prose is any good, whether a claim is supported, whether a citation resolves to a real paper. Those belong to the page CHECK phase and its evidence lanes.
- Whether a `[Q-…]` bracket is discharged. That is the phase workers' and `probe/check-probe-cards.sh`'s.
- Whether the paper compiles. That is the door's `compile` verb (fn/compile.md); this fn only asserts that the pieces a compile would need are present and reachable.

Return contract
---------------

```
status:    ok (conforms) | findings | failed
summary:   counts: ✗ / ⚠, one line per finding category; ALWAYS state the J verdict explicitly
artifacts: [findings list]
next:      the single highest-leverage fix route from Step 3
```
