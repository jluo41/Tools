---
name: haipipe-paper-evidence
description: "A paper's evidence rules on top of haipipe-evidence and haipipe-display: citations only from verified CITE Results, one number per result in every Section, displays numbered and within the venue limit, each passing the display revise loop. Reads a whole version as one ledger and flags what disagrees (scripts/evidence_ledger.py). Use before a build or a send. Trigger: paper evidence, evidence ledger, numbers disagree, verify citations, paper displays, /haipipe-paper-evidence, /haipipe-paper-display."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.3.2"
  last_updated: "2026-10-26"
  aliases: [haipipe-paper-display]
  # version history: ./CHANGELOG.md
---

# /haipipe-paper-evidence · what backs the paper, Section by Section and as one version

JL 261019: "should we chagne this to haipipe-paper-draft? and also have a haipipe-paper-evidence? ... it is like we
have the paper to combine the evidence and draft together to make a draft task, right?"; then "okay, please go ahead
and do it". A paper Section is a draft Task (b32_draft s03, s41-D06), three folders side by side, one writer each:

```text
base (every theme)      paper adds                  one Section Task
haipipe-draft      ─▶   haipipe-paper-draft    ─┐   tNN_<section>/
haipipe-evidence   ─▶   haipipe-paper-evidence ─┼─▶ ├── draft/      plan and sentences
haipipe-display    ─▶   (this skill too)       ─┘   ├── evidence/   cards.yaml · proposals.md
                                                    └── display/    Display<n>-<slug>/
```

A paper is a pair (JL 261022: "for the display, it should be in the b03?"; "for /haipipe-paper, we should have a
paper block and a work block to provide the displays and E-work, right?"). The paper Board writes; its work Block
computes, so every number and every picture has one source:

```text
work/bNN_<topic>/                      computes                   paper/Paper-X/jNN_v<MMDD>_<desk>/   writes
├── jNN_<question>/tNN_/runs/rNN/result/ ── VALUE card ──────────▶  tNN_<section>/evidence/cards.yaml
└── j21_paper_displays/  colour-scheme.yaml                      tNN_<section>/display/
    ├── t01_table1/runs/rNN/result/table-body.tex ── intake ─────▶  ├── Display1-table1-<slug>/   frames it
    └── t02_figure1_<slug>/runs/rNN/result/figure.pdf ── intake ──▶  └── Display2-figure1-<slug>/  frames it
                                                                       question · caption · legend · number
                                                                       · venue size · review/rNN.md
version face: work-block: work/bNN_<topic>
```

The base finds and shows evidence for any page; this skill adds what only a paper needs. A base skill sees one Task
at a time, so the one thing no base skill can do is read a whole version and say where its Sections disagree: that
is the ledger below.

| base skill | does, for any page | this skill adds, for a paper |
|---|---|---|
| `haipipe-evidence` | the card format, CITE and VALUE, `cards.py check · propose` | the citation and number rules; the version ledger |
| `haipipe-evidence cite` | a discovery Run's `.bib` and `facts.md` | verified before a Section closes; never `bank.bib` |
| `haipipe-evidence work` | a work Run's value at `file` + `key` | the same Run for the same value in every Section |
| `haipipe-display` | `Display<n>-<slug>/`, built on cards, the revise loop | numbered for the paper; within the venue's limit; the loop is a must, and the set is reviewed together |


The rules
---------

1. **Citations come from verified CITE Results.** A CITE card names a discovery Run; its one-entry BibTeX is the
   citation. The Page export freezes `delivery/latex/selected-bibliography/<page>.bib` from the selected, verified
   CITE Results, and `haipipe-paper-assemble` merges them; both are generated, never edited. Never touch
   `bank.bib` or the paper's `delivery/reference.bib`. A source with no Result yet is `\citep{TOADD}` and a red
   card with `need`. Check every entry against Google Scholar or its DOI record before the Section closes. Never cite
   one paper in back-to-back sentences.
2. **One result, one number.** A number in prose comes from a VALUE card (`file` + `key` in a Run's `result/`), best
   through the research question's report (`reports/qNN_<question>/`). The same result reads from the same Run, and
   shows the same number, in the Abstract, the Results, the Discussion and the letters.
   The work Block serves them from one Job, `jNN_paper_work_evidence`, beside `jNN_paper_displays`: one Task per
   Section, a value map `scripts/values.yaml` (each number's source Run, file and key), and a Run that writes
   `values.json`; the Section's VALUE cards read it by id (JL 261023). A setting stated in words stays on its card.
3. **Displays are the paper's.** Each `Display<n>-<slug>/` is built on cards (haipipe-display). The paper numbers them
   in Section order: the main text Display 1, 2 …, the appendix (`t2N_`) eDisplay 1, 2 …; each is cited in its
   Section's text; the main text stays within the venue's limit (its call, or what the person says).
   **A display is drawn by the work Block, framed by the paper** (JL 261022):
   - The paper's work Block (`work/bNN_.../`, named by the version face's `work-block:` line, or `board.md`'s) owns
     one display Job, `j21_paper_displays` (`j21_<venue>_displays` when the Project has several venues), with one
     Task per display (`t01_table1`, `t02_figure1_<slug>`, ...). The Job face opens with the **display plan** the
     authors agree before any Run draws (JL 261023): per display its number, title, one question, layout (rows,
     columns or axes), source Runs and open choices, taken from the team's meeting notes and slides in the Block's
     `related/`. Drawing starts after the plan is agreed; Sections write their numbers after the drawn displays pass
     review and are accepted.
     A Run in that Task draws the picture or the table body into its `result/` (`figure.pdf` and `figure.png`, or
     `table-body.tex`, plus `figures.md`). A display that reads several question Jobs still lives in that one Job.
   - The paper's unit, `tNN_<section>/display/Display<n>-<slug>/`, only frames it: its question, caption, legend,
     number, venue size and `review/rNN.md`. Its `intake/manifest.yaml` points at the work Run's `result/`; its
     `recipe/` copies the picture in and draws nothing. No paper folder runs analysis or plotting code.
   - VALUE (Ework) cards point at the same work Block's Runs, so one Block is the source of every number and
     every picture.
   - The revise loop sends each fix where it lives: a picture problem (colour, scale, panel, denominator) goes to
     the work Run's script, which reruns; a caption, legend or question problem goes to the paper unit.
   **Every main-text and eAppendix display passes the display revise loop before the version leaves DRAFT** (JL
   261022: "display should also have a loop, like the draft is a loop; a display matters as much as the main
   text"). The loop is haipipe-display's `1_base/display/ref/display-revise-loop.md`; the paper adds three things,
   because only the paper sees all Sections:
   - **One colour scheme per paper**, kept where the pictures are drawn: the display Job's
     `work/bNN_.../j21_paper_displays/colour-scheme.yaml`, read by every display Task's Run script: the same
     thing the same colour in every display, a colour never meaning two things, tick labels black.
   - **The set is reviewed together once**: at least one round's `{units}` is every cited display of the version,
     main text then eAppendix in paper order, so the reviewer's cross-display verdict (one story with no gaps,
     redundancy between displays, colour consistency) covers the whole paper. Each unit keeps its own block and
     that verdict in `review/rNN.md`.
   - **The pass rule holds for every cited display**: overall at least 8/10 and question, readability, honesty and
     journal-ready each at least 7/10, in its latest round. After 4 rounds without a pass the loop stops and the
     person gets the open problems. `accepted:` is never ticked before a pass. The ledger below shows each
     display's latest score and flags a miss.
4. **Claim words fit the design.** An observational design says "association", never a causal verb; a claim
   never outruns the evidence card under it.
5. **Every consequential sentence is one of three**: backed by a card (an older Page: a typed Evidence Item and
   its accepted local Result), framed as interpretation and bounded by its evidence, or a visible open need that
   keeps the Section from closing. haipipe-paper-draft writes the sentence; this skill checks which of the three it is.


The version ledger
------------------

```bash
L=Tools/plugins/haipipe-toolkit/skills/2_theme/paper/haipipe-paper-evidence/scripts/evidence_ledger.py
.venv/bin/python -B $L <paper>/jNN_v<MMDD>_<desk>/                    every Section of one version, side by side
.venv/bin/python -B $L <paper>/jNN_v<MMDD>_<desk>/ --max-displays 7   with the venue's limit on main-text displays
.venv/bin/python -B $L <paper>/jNN_v<MMDD>_<desk>/ --json             for a builder or a workbench
```

It reads each Task in either shape: `evidence/cards.yaml` (haipipe-evidence, since 261016) or an older Page's
`draft/<stem>-evidence-items.md` (read by haipipe-draft's `item_table`, the parser the Page workbench uses), its
`display/Display<n>-*/`, and its `.bib` files (`draft/evidence/bibex/` on an older Page, else each CITE card's Run).
Parts by Task number: `t00` the Abstract, `t01`-`t19` the main text, `t2N` the appendix, `t3N` the letters. Only the
Sections in the version face's `haipipe:compile-order` block are numbered, counted and compared; the rest show
`⏸ off`.

```text
❗ one value, two Runs            the same VALUE value (source, file, key) read from different Runs in two Sections
❗ one label, different estimates  an older VALUE label whose Results report different estimates, compared in
                                  one unit (a key with pp or percentage_point is in percentage points)
❗ one citation key, two entries   the same key with another year or title in two Sections' .bib files
❗ too many displays              main-text displays over --max-displays
❗ a card does not resolve        haipipe-evidence's cards.check, per Section
⚠️ one label, the same estimates  two Results that hold the same estimates (one copies the other: point both at one)
❗ display drawn inside the paper  a main-text display whose intake/manifest.yaml names no work Run's result/, or
                                  one outside the version's work-block:, or one that does not exist
❗ display has no question        a main-text display whose README names no question:
❗ display review not passed      a main-text display whose latest review/rNN.md fails the pass rule, or that has
                                  no round yet (the listing shows each display's latest score: r02 8.5/10 ✅)
⚠️ one display twice              the same display name in two Sections
⚠️ the same three, on an appendix an eAppendix display drawn inside the paper, with no question:, or no passing review
⬜ open                           citations not yet verified, values not yet landed, needs not yet filled
```

**What it does not read yet**: numbers typed into table bodies or prose, and wording that drifts between Sections
("no association" in one, "close to zero" in another). Those stay a person's read of the built PDF
(haipipe-paper-assemble's cold read). **The venue's limit** is passed by hand: a venue's call (`venues/<venue>/call.md`)
or the person says it; a QBv desk record may not hold it.

It changes no file of the paper: the ledger is a view of the Tasks' own files, so nothing generated is tracked (`-B`
keeps Python from writing its bytecode cache beside the script). Exit 1 on a ❗. A ❗ is fixed in the Section that is
wrong (its card, its Evidence Item, its `.bib`, or the Run it reads), never by editing a built file.


Where it sits on the ladder
---------------------------

```text
Board     💡 s01 idea · 📖 s02 story (§7 allots evidence to Sections) · 🔍 s10-s19 related · ❓ reports/qNN_
  └─ Job  jNN_v<MMDD>_<desk>: the Narrative order · 🧾 this ledger, once per send
      └─ Task tNN_<section>: draft/ ✎ (haipipe-paper-draft) · evidence/ 🧾 · display/ 📊 (this skill)
```

Who calls it: a Section's CHECK (haipipe-paper-draft's closing checks), `haipipe-paper-assemble` before a build (gate
G4), and a person before a send. It proposes nothing itself: a missing piece is a card with `need`, and
`cards.py propose` (haipipe-evidence) flags what to make.


Files
-----

```text
haipipe-paper-evidence/
├── SKILL.md                      this contract
├── CHANGELOG.md
├── scripts/evidence_ledger.py    the version ledger
└── tests/test_evidence_ledger.py a made-up version: two Runs, two estimates, too many displays, unreviewed displays,
                                  a display drawn inside the paper
```
