---
name: haipipe-paper-evidence
description: "A paper's evidence rules on top of haipipe-evidence and haipipe-display: citations only from verified CITE Results, one number per result in every Section, displays numbered and within the venue limit, each passing the display revise loop. Reads a whole version as one ledger and flags what disagrees (scripts/evidence_ledger.py); each display version's preview.pdf is the display, then how it was made (method.md). Use before a build or a send. Trigger: paper evidence, evidence ledger, numbers disagree, verify citations, paper displays, display preview, display method, /haipipe-paper-evidence, /haipipe-paper-display."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.6.1"
  last_updated: "2026-11-01"
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

One paper Block links many discovery Blocks (external information) and work Blocks (internal information), deposits
them into its evidence Jobs, and writes them into papers (JL 261031; haipipe-paper's four layers). Work computes on raw
data; the paper Board's three evidence Jobs hold what this paper quotes, each Task reading returned, aggregated
Results only; the writing Jobs (versions) quote them, so every number and every picture has one source:

```text
work/bNN_<topic>/  creates            paper/Paper-X/  evidence                    paper/Paper-X/j11_writing_…/  writes
jNN_/tNN_/runs/rNN/result/ ──────▶   j01_evidence_display/ colour-scheme.yaml ─▶ tNN_<section>/display/  frames it
discovery/bNN_ … CITE Results ──▶      t01_figure1-<slug>/runs/rNN/result/figure.pdf
                                       t51_etable1-<slug>/runs/rNN/result/table-body.tex
                                     j02_evidence_value/ tNN_values-<group>/ ───▶ tNN_<section>/evidence/cards.yaml
                                     j03_evidence_cite/  tNN_<claim group>/  ───▶ \citep keys in the Section
```

Until 261031 the display Job sat in the work Block (`work/bNN_.../j21_paper_displays/`) and drew there; an older
Project keeps that layout until it is moved, and the rules below read the same with "the display Job" for either.

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
   The paper Board serves them from its value Job, `j02_evidence_value`, beside `j01_evidence_display` (both moved
   onto the Board 261031; earlier `jNN_paper_work_evidence` and `jNN_paper_displays` in the work Block): one Task per
   Section, a value map `scripts/values.yaml` (each number's source Run, file and key), and a Run that writes
   `values.json`; the Section's VALUE cards read it by id (JL 261023). A setting stated in words stays on its card.
3. **Displays are the paper's.** Each `Display<n>-<slug>/` is built on cards (haipipe-display). The paper numbers them
   in Section order: the main text Display 1, 2 …, the appendix (`t2N_`) eDisplay 1, 2 …; each is cited in its
   Section's text; the main text stays within the venue's limit (its call, or what the person says).
   **A display is drawn in the paper's display Job, from work's returned Results, and framed by the Section** (JL
   261022; moved to the paper Board 261031):
   - The paper Board owns one display Job, `j01_evidence_display`, with one Task per display (`t01_figure1-<slug>`,
     `t02_table1-<slug>`, …; appendix `t51_etable1-<slug>`, …), each face with `label:`, `status:`, `answers:`,
     `cited-in:`, `layout:`, `sources:`, `made-by:`. The Job face opens with the **display plan** the
     authors agree before any Run draws (JL 261023): per display its number, title, one question, layout (rows,
     columns or axes), source Runs and open choices, taken from the team's meeting notes and slides in the Block's
     `related/`. Drawing starts after the plan is agreed; Sections write their numbers after the drawn displays pass
     review and are accepted.
     A Run in that Task draws the picture or the table body into its `result/` (`figure.pdf` and `figure.png`, or
     `table-body.tex`, plus `figures.md`). A display that reads several question Jobs still lives in that one Job.
   - The paper's unit, `tNN_<section>/display/Display<n>-<slug>/`, only frames it: its question, caption, legend,
     number, venue size and `review/rNN.md`. Its `intake/manifest.yaml` points at the display Task's Run `result/`;
     its `recipe/` copies the picture in and draws nothing. A display Run only draws from returned, aggregated
     Results; no paper folder runs analysis on raw data.
   - VALUE (Ework) cards point at the same work Block's Runs, so one Block is the source of every number and
     every picture.
   - The revise loop sends each fix where it lives: a picture problem (colour, scale, panel, denominator) goes to
     the work Run's script, which reruns; a caption, legend or question problem goes to the paper unit.
   **Every main-text and eAppendix display passes the display revise loop before the version leaves DRAFT** (JL
   261022: "display should also have a loop, like the draft is a loop; a display matters as much as the main
   text"). The loop is haipipe-display's `1_base/display/ref/display-revise-loop.md`; the paper adds three things,
   because only the paper sees all Sections:
   - **One colour scheme per paper**, kept where the pictures are drawn: the display Job's
     `j01_evidence_display/colour-scheme.yaml`, read by every display Task's Run script: the same
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


Each display version: one preview.pdf
------------------------------------

Every Run of a display Task (a version of that display) leaves, in its `result/`, the unit's `float.tex` and
`preview.pdf`: page 1 the display with its caption, pages 2 on how it was made, from `method.md` (haipipe-display's
`scripts/build_preview.py`; JL 261101). The workbench's Report › Evidence › Displays shows the newest version's
`preview.pdf`, both pages, with ⤢ Pop out.

Page 1 is the display as the paper prints it (JL 261101: "the full pdf preview, just like the one we will see in the
paper pdf"). Build it with (from the SPACE root, where `Tools/` is the Tools checkout; elsewhere use the full path):

```bash
.venv/bin/python Tools/plugins/haipipe-toolkit/skills/2_theme/paper/haipipe-paper-evidence/scripts/preview_display.py <unit> [--method-from <source preview.pdf>]
```

```text
head 1   the unit's own writing Job, built      <Board>/delivery/<that job>/latex/master.tex
head 2   else the newest built writing Job      <Board>/delivery/jNN_writing_v<MMDD>_<desk>/latex/master.tex
head 3   else the paper's default look          (and a note: build the paper, then rerun)
```

Each display Task's face names it for the Evidence list (JL 261101: "for each display, we might also want to have the
name and type"). The face is `j01_evidence_display/tNN_<slug>/tNN_<slug>.md`; under its `# title`, one `key: value`
line each (plain lines, no front matter):

```text
label: Display A                            the tab's first line (board_evidence.evidence_body)
name: Office visits by 28-day period        what it shows, in a few words
type: figure                                figure or table; else read from the newest float.tex
```

The list shows the label, then "📈 Figure · <name>" or "📊 Table · <name>" (board_results._display_line); a face with
no `name:` gives the title after "Display X," in its first line, else the folder's words.


All displays as one PDF
-----------------------

```bash
.venv/bin/python Tools/plugins/haipipe-toolkit/skills/2_theme/paper/haipipe-paper-evidence/scripts/build_displays_pdf.py <paper>/j01_evidence_display
```

Every display of the display Job in one PDF, one page each in Task order (main, then appendix): its label, caption,
and the picture or the table; a display not drawn yet gets a page that says so (JL 261101: "I also want a link for
the display, so we can view all the displays as one pdf file"). It writes `<Board>/delivery/<job>/<job>-all-displays.pdf` (the Board owns delivery/)
(generated: rerun after a display changes, never edit the PDF), and the workbench's Evidence view links it as "Open
all displays as one PDF". It finds each drawn file with the workbench's own lookup, so the page and the PDF agree.


The version ledger
------------------

```bash
L=Tools/plugins/haipipe-toolkit/skills/2_theme/paper/haipipe-paper-evidence/scripts/evidence_ledger.py
.venv/bin/python -B $L <paper>/jNN_writing_v<MMDD>_<desk>/                    every Section of one version, side by side
.venv/bin/python -B $L <paper>/jNN_writing_v<MMDD>_<desk>/ --max-displays 7   with the venue's limit on main-text displays
.venv/bin/python -B $L <paper>/jNN_writing_v<MMDD>_<desk>/ --json             for a builder or a workbench
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
❗ display drawn inside the paper  a main-text display whose intake/manifest.yaml names no Run's result/ (a work
                                  Run, or a Run in the Board's j01_evidence_display Job), or one outside the
                                  version's work-block: or Board, or one that does not exist
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
  └─ Job  jNN_writing_v<MMDD>_<desk>: the Narrative order · 🧾 this ledger, once per send
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
├── scripts/build_displays_pdf.py all of a display Job's displays as one PDF
└── tests/test_evidence_ledger.py a made-up version: two Runs, two estimates, too many displays, unreviewed displays,
                                  a display drawn inside the paper
```
