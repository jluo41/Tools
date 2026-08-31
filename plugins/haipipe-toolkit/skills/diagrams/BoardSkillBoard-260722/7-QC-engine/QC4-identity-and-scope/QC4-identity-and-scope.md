# Why "it points at nothing" keeps coming back: identity by NAME, and lookups that return EMPTY

state: 🟡 PARTIAL · two instances fixed 260807, guards watched to fire · open: 15 name sites, 508 lookups
owner: JL
method: treat every "X does not point at Y" report as one defect class, measure the class rather than patch the instance, and require a guard that has been SEEN to fire

## Opening

Why does the same failure keep arriving in different clothes, and what makes it invisible every time?

JL reported it four times in two days, each time as a different symptom: an evidence card that opens nothing, a card that opens the PREVIOUS page's evidence, a display page with no preview, a paper board with no chips at all. They are one defect with two halves, and both halves are measurable rather than a matter of opinion.

The first half is that the engine decides WHAT A THING IS from what it is NAMED. The second half is that when the name does not match, the lookup returns an empty result instead of raising, so a total failure and a genuinely empty page produce the identical page.

JL 260807, after the fourth report, said plainly that this had happened many times and had to be dealt with properly rather than patched again. This page exists so the class has an owner, a measurement, and a closing rule. Instances get fixed on their own pages; the class closes here.

**Where this page sits**: This page moved from `QA` to `QC · Engine` on 260816, because what it rules is engine code: how a script decides what a thing IS, and what a lookup returns when it finds nothing.
`QC1` states the one Law the code's three halves follow; this page states the modelling rule every one of them breaks in the same way.

**Covered elsewhere**: The code's shape and its one Law are `QC1` (`QC1a` build, `QC1b` src, `QC1c` live). What each Page Type reads and writes is `QPs2` §7. The rule that a guard must be watched to fire is this page's `## Law`, and `QF1` is where it meets the per-change gate.

## Diagram

**The two halves, and why each one alone would have been caught**: it takes both to stay invisible.

```text
 ①  IDENTITY BY NAME                       what the page ALREADY declares
 ────────────────────────────────────      ─────────────────────────────────
 glob("S-Display-*")                  ◀──  float.tex is what makes it a unit
 family == "Display"                  ◀──  page-type: display
 MARKER  S-Display-\d+                ◀──  page-type: display
 0-lifecycle/*/workspace              ◀──  the stage was given as an argument
 glob("0-lifecycle/*/S-Literature-*") ◀──  route: outward
 the renderer decides what is a link  ◀──  🔗 QA-probe: IS the pointer
 id="pc1", unique within ONE page     ◀──  the page has an id of its own

                        │  the name changes
                        ▼
 ②  THE LOOKUP RETURNS EMPTY               573 lookup points in the engine
 ────────────────────────────────────       65 raise or report      11%
 glob  ──▶ []                              508 return empty        88%
 regex ──▶ None
 gate  ──▶ ""                              EMPTY and NOTHING-TO-DO
 .get  ──▶ None                            render the SAME PAGE
```

⚖️ Establishes that neither half is a bug in one file: half ① is a modelling choice repeated in 20 places, and half ② is the default behaviour of 88% of the engine's lookups.

## Content

### 1 · The four reports were one defect

**What JL saw, and what was actually wrong**: four symptoms, one cause each time.

```text
  260806  a display page shows no render
          the auto-preview is gated on family == "Display"; this page's
          family is QBt, so it could never fire however correct the unit
  260807  the paper board shows no evidence cards at all
          the dialect looked for 0-lifecycle/*/workspace; the folder was
          renamed to display/ on 260806 and the glob returned 0 units.
          MEASURED: units=0, labels=0 on the live MISQ paper
  260807  an evidence card opens nothing
          the 🔗 QA-probe pointer was written INSIDE a ```text fence, which
          is code, so it never became a link. There was nothing to click
  260807  a card opens the PREVIOUS page's evidence
          popcards live outside div.wrap and every page numbers them from
          pc1; navigation swapped only div.wrap, so pc1 resolved to the
          page just left
```

🔍 Establishes that "it points at nothing" is not four bugs but one class arriving four times, which is why fixing instances did not stop it.

#### 1.1 · The control that made the third one provable
(two pages, same anatomy, one difference)
`QBt5-for-value` wrote its pointer ABOVE the fence and rendered its link the whole time; `QBt4-for-literature` wrote its pointer as the fence's first row and rendered none.
Measured on the built HTML: `QBt4` had 0 links to its own two records, `QBt5` had 1 to its own.
A natural control is worth more than a reading of the renderer, because it settles the cause without anyone having to be believed.

#### 1.2 · The fourth was reproduced before it was fixed
(the simulation is the evidence, not the patch)
Navigating `QBt4` to `QBt5` was simulated on the built files, swapping only `div.wrap` exactly as the router did.
`#pc1` on the arriving page resolved to `NOT IN .bib  ·  imaginary2031typed`, which is `QBt4`'s card and precisely what JL's screenshot showed.
With `#popcards` swapped alongside the wrap, the same simulation resolved `#pc1` to `Q-Value-1 is claimed by NO probe entry`, which is `QBt5`'s own.

### 2 · Half one: the engine names things instead of reading their declaration

**Where the engine spells out a name**: a grep for hardcoded name shapes across `src/` and `cli/`.

```text
  20 sites across 7 files spell out what a thing is CALLED
  ────────────────────────────────────────────────────────────
  dialect_paper.py   6   S-Display-\d · display\d{2} · 0-lifecycle
  display-report.py  3   S-Display-(\d+) · S-Main-(\w+)- · S-Display-Dash.md
  body.py            2   the MARKER alternation's unit branch
  check.py           2   S-Main-1 · S-Main-1-template.md
  display_unit.py    2   glob("S-Display-*") · "S-Main-"
  build-displays.py  1   S-Display-x
  refresh.py         1   S-Main-[0-9]*.md
```

In every one of those, the page already carries the answer: `page-type:`, `route:`, or the presence of `float.tex`. The name is a PROXY for a declaration that exists, and a proxy is exactly what breaks on a rename.

⚙️ Establishes the size of half one: 20 places, each a rename away from returning nothing.

### 3 · Half two: 88% of lookups cannot fail loudly

**What a failed lookup returns**: measured over every lookup call in `src/` and `cli/`.

```text
  lookup points                573
  raise, exit, or report        65      11%
  return an empty result       508      88%
```

`glob` finds nothing and returns `[]`. A regex does not match and returns `None`. A gate does not fire and returns `""`. Nothing distinguishes THE ANSWER IS NOTHING from I COULD NOT LOOK, and the page renders either way.

The one guard that does exist in the display path was written after the failure had already cost something: `authoring_dir()` exits with "REFUSING to run, because an empty source tree here means every shipped file looks orphaned and gets deleted", added the day a renamed folder nearly unlinked 25 shipped files. That is the pattern: guards are added after the failure hurts, and 508 sites have not hurt yet.

🧾 Establishes that half two is the default, not an oversight, so it must be closed by a rule rather than by care.

### 4 · What shipped on 260807, and what it cost to trust it

**What shipped**: two guards and one container, each verified by being SEEN to fire.

```text
  cli/check.py · check_evidence_pointer          reads the SOURCE line, not
    evidence-pointer-in-fence      ERROR         the rendered anchor, because
    evidence-pointer-missing       ERROR         no existing check can see a
                                                 link that was never generated

  assets/js/70-router.js       + #popcards swap  the path a reader takes
  assets/js/20-live-refresh.js + #popcards swap  the auto-rebuild path
  src/page_board.py            popcards wrapped in <div id="popcards">
```

Both were verified against a failing case rather than a passing one. `check_evidence_pointer` was run against a scratch copy with the defect reinstated and watched to fire at the exact line, then the copy was deleted. The swap was proven by simulating the navigation on the built files and reading which card `#pc1` resolved to, before and after.

✅ Establishes the closing standard for this class: a guard nobody has watched fail is not yet a guard.

#### 4.1 · The router was found second, and would have been missed
(the first patch went to the wrong path)
`20-live-refresh.js` was patched first; it is the AUTO-REBUILD path. The path a reader takes when clicking a page is `70-router.js`, which fetches `?fragment=wrap` and swaps separately.
A grep for every site that replaces the body found it: 2 swap paths, not 1.
Fixing one and stopping would have left the reported symptom exactly as reported, which is the failure mode this whole page is about.

## Aims

### Decision Now

- [ ] 🗣 Do the 20 name-pattern sites get converted in one pass, or one file at a time with a regression between each?
      📍 `§2` measures them: 20 sites across 7 files, 5 already converted on 260807.
      🔔 `Why now` the converted five all touch the live MISQ paper, and one of them, the `workspace` to `display` rename, had already broken every evidence card on that board without anyone noticing. The next conversion carries the same risk.
      ⭐ `A ·` one file at a time, each followed by the MISQ regression in `A2.2`, which costs seven rounds and makes any breakage attributable to one file.
      `B ·` one pass, which is faster and makes a regression impossible to attribute.
      🛑 `Blocks` starting the conversion at all.
      🤖 `If nobody answers` the five converted sites stand and the other 15 stay, so the class stays open and the next rename repeats it.


### A1 · 🔍 The four reports were one defect
- ✅ A1.1 · Every "points at nothing" report is triaged against this class before it is patched.
  **Done when:** each new instance is logged in `§1`'s table with its cause named, or is shown to belong to a different class.
  **Now:** Met 260807: four reports triaged, each cause named and measured, in `§1`.


### A2 · ⚙️ Half one: the engine names things instead of reading their declaration
- 🔨 A2.1 · No engine site decides what a thing IS from what it is CALLED.
  **Done when:** the grep in `§2` returns 0 sites, each replaced by the declaration the page already carries (`page-type:`, `route:`, `float.tex`).
  **Now:** 5 of 20 converted 260807: `display_unit.units()` selects by `float.tex`, `dialect_paper` accepts both authoring folder names and the specimen layout, `MARKER`'s unit branch is built from the index, `section_pages()` and `literature_pages()` read the head key. 15 remain, listed in `§2`.
- ✅ A2.2 · The five sites already converted stay converted, and the MISQ paper is the regression.
  **Done when:** `dialect_paper` indexes 11 units, `build-displays.py --check` and `display-report.py --check` both exit 0, on every later change.
  **Now:** Held on every change 260807: `dialect_paper` indexes 11 units and 11 labels on the MISQ paper, and both `--check` commands exit 0.


### A3 · 🧾 Half two: 88% of lookups cannot fail loudly
- ⬜ A3.1 · An IDENTITY lookup that finds nothing says so, instead of returning empty.
  **Done when:** every lookup that resolves a page, a unit, or a record to its identity either raises or reports, and the 11% in `§3` is measured again.
  **Now:** Measured 260807 and not started: 573 lookup points, 65 guarded. The one guard in the display path was written only after a rename nearly deleted 25 shipped files.


### A4 · ✅ What shipped on 260807, and what it cost to trust it
- ✅ A4.1 · Every guard in this class has been observed to fire on a real failing case.
  **Done when:** each guard's Log row names the case it was watched to catch and how that case was produced.
  **Now:** Met for both 260807 guards. `check_evidence_pointer` was watched to fire at `QBt4-for-literature.md:73` on a scratch copy with the defect reinstated; the `#popcards` swap was proven by simulating the navigation on the built files and reading which card `#pc1` resolved to.


## Files

- `../../../../board/haipipe-board/src/dialect_paper.py`
  6 of the 20 name-pattern sites, and the one whose failure hid longest: it indexed 0 units on the live MISQ paper for a day.
- `../../../../board/haipipe-board/src/body.py`
  The `MARKER` alternation whose unit branch decided which names could become an evidence card; now built from the index by `use_paper()`.
- `../../../../board/haipipe-board/src/display_unit.py`
  The shared anchor rules, and the model for what a converted site looks like: a unit is a folder with a `float.tex`, not a folder with a name.
- `../../../../board/haipipe-board/cli/check.py`
  Carries `check_evidence_pointer`, the first check in this class that reads a source line rather than a rendered anchor.
- `../../../../board/haipipe-board/assets/js/70-router.js`
  The navigation path a reader actually takes, and the one the first patch missed.
- `../../../../board/haipipe-board/assets/js/20-live-refresh.js`
  The auto-rebuild path, which carries the same two lines.
- `../PaperSkillBoard-260725/4-QBt-page-types/QBt4-for-literature/QBt4-for-literature.md`
  The instance page for the pointer-in-fence defect; its Log records the 260806 decision that caused it, marked reversed in place.
- `3-QPs-page-structure/QPs2-page-types/QPs2-page-types.md`
  `§7` owns what each type reads and writes; this page owns why those pointers stop resolving.

## Law

- 260807 · JL · A guard nobody has watched fail is not yet a guard. Every check in this class ships with the failing case it was observed to catch, and how that case was produced.

## Log

- 260816 · [MIGRATE-CC, JL ruled] the page moved `QA5` → `QC4` with the QA restructure, and its title lost the stale `QC5 ·` prefix it had carried since the 260815 renumber.
  QA is the group that argues what must be true before any artifact exists, and this page argues how the shipped code models identity, which is `QC`'s subject.
  `QC4` was last used for the round-trip page in the 260815 renumber, so the number is reused under the 260801 precedent and the old row leaves `## Links`; the round trip is `QC3`.
- 260807 1600 · [DRAFT-CC] Opened on JL's instruction after the fourth report of the same symptom in two days, and after he said plainly that patching instances was no longer acceptable. The page exists because the four reports were being treated as four bugs: a display page with no preview, a paper board with no chips, an evidence card that opens nothing, and a card that opens the previous page's evidence. They are one class with two halves, and both halves are measured here rather than argued: 20 sites that decide what a thing IS from what it is CALLED, and 573 lookup points of which 508 return an empty result instead of raising, so a rename and a genuinely empty page render identically. Two guards shipped the same day and both were verified against a FAILING case, which is now this page's Law. The fourth instance also produced the pattern's own best illustration: the first patch went to `20-live-refresh.js`, the auto-rebuild path, while the path a reader actually clicks is `70-router.js`; a grep for every body-replacing site found two, and stopping at one would have left the reported symptom exactly as reported.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0