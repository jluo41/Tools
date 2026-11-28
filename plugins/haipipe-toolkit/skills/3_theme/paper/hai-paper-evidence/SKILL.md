---
name: hai-paper-evidence
description: "A paper's evidence rules: verified citations, one number per result, displays within the venue limit; owns the value and citation Jobs. Use before a build or a send. Trigger: paper evidence, value ledger, citation check, send check, numbers disagree, /hai-paper-evidence, /hai-paper-display, /hai-paper-check."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.19.0"
  last_updated: "2026-11-23"
  aliases: [hai-paper-display, hai-paper-check]
  # version history: ./CHANGELOG.md
---

# /hai-paper-evidence · what backs the paper, Section by Section and as one version

JL 261019: "should we chagne this to hai-paper-draft? and also have a hai-paper-evidence? ... it is like we
have the paper to combine the evidence and draft together to make a draft task, right?"; then "okay, please go ahead
and do it". A paper Section is a draft Task (b32_draft s03, s41-D06), three folders side by side, one writer each:

```text
base (every theme)      paper adds                  one Section Task
hai-draft      ─▶   hai-paper-draft    ─┐   tNN_<section>/
hai-evidence   ─▶   hai-paper-evidence ─┼─▶ ├── draft/      plan and sentences
hai-display    ─▶   (this skill too)       ─┘   └── evidence/   cards.yaml · proposals.md
```

One paper Block links many discovery Blocks (external information) and work Blocks (internal information), deposits
them into its evidence Jobs, and writes them into papers (JL 261031; hai-paper's four layers). Work computes on raw
data; the paper Board's three evidence Jobs hold what this paper quotes, each Task reading returned, aggregated
Results only; the writing Jobs (versions) quote them, so every number and every picture has one source:

```text
work/bNN_<topic>/  creates            paper/Paper-X/  evidence                    paper/Paper-X/j11_writing_…/  writes
jNN_/tNN_/runs/rNN/result/ ──────▶   j02_evidence_value/ tNN_values-<group>/ ───▶ tNN_<section>/evidence/cards.yaml
                                       │ values first: its copies and its ids are all a display reads
                                       ▼
discovery/bNN_ … CITE Results ──▶    j01_evidence_display/ colour-scheme.yaml ─▶ cited in tNN_<section> (cited-in:)
                                       t01_display-a-<slug>/runs/rNN/result/figure.pdf
                                       t02_display-b-<slug>/runs/rNN/result/table-body.tex
                                     j03_evidence_cite/  tNN_<claim group>/  ───▶ \citep keys in the Section
```

Until 261031 the display Job sat in the work Block (`work/bNN_.../j21_paper_displays/`) and drew there; an older
Project keeps that layout until it is moved, and the rules below read the same with "the display Job" for either.

The base finds and shows evidence for any page; this skill adds what only a paper needs. A base skill sees one Task
at a time, so the one thing no base skill can do is read a whole version and say where its Sections disagree: that
is the ledger below.

| base skill | does, for any page | this skill adds, for a paper |
|---|---|---|
| `hai-evidence` | the card format, CITE and VALUE, `cards.py check · propose` | the citation and number rules; the version ledger |
| `hai-evidence cite` | a discovery Run's `.bib` and `facts.md` | verified before a Section closes; never `bank.bib` |
| `hai-evidence work` | a work Run's value at `file` + `key` | the same Run for the same value in every Section |
| `hai-display` | `Display<n>-<slug>/`, built on cards, the revise loop | numbered for the paper; within the venue's limit; the loop is a must, and the set is reviewed together |


The rules
---------

1. **Citations come from verified CITE Results.** A CITE card names a discovery Run; its one-entry BibTeX is the
   citation. The Page export freezes `delivery/latex/selected-bibliography/<page>.bib` from the selected, verified
   CITE Results, and `hai-paper-assemble` merges them; both are generated, never edited. Each Section keeps its
   own `draft/evidence/bibex/<task>.bib`, the source the build merges into that generated file. Never touch
   `bank.bib` or the paper's `delivery/reference.bib`. A source with no Result yet is `\citep{TOADD}` and a red
   card with `need`. Check every entry against Google Scholar or its DOI record before the Section closes. Never cite
   one paper in back-to-back sentences.
2. **One result, one number.** A number in prose comes from a VALUE card (`file` + `key` in a Run's `result/`), best
   through the research question's report (`reports/qNN_<question>/`). The same result reads from the same Run, and
   shows the same number, in the Abstract, the Results, the Discussion and the letters.
   The paper Board serves them from its value Job, `j02_evidence_value`, beside `j01_evidence_display` (both moved
   onto the Board 261031): one Task per group of printed numbers, each a value map and one Run, and the Section's
   VALUE cards bind each printed number to its value by id (the standard shape below, 0.7.0). Every printed value
   names its Runs (`checks:`), its research question and where it is printed. A setting stated in words stays on its card.
3. **Displays are the paper's.** Each display is built on cards (hai-display). The paper numbers them
   in Section order: the main text Display 1, 2 …, the appendix (`t2N_`) eDisplay 1, 2 …; each is cited in its
   Section's text; the main text stays within the venue's limit (its call, or what the person says).
   **A display is drawn in the paper's display Job, from the value Job's copies of work's returned Results, and
   cited by the Section** (JL 261022; moved to the paper Board 261031):
   - **Values first, then displays** (JL 261110: "we want the data first prepared ready in the Values, and then these
     data will be used to support the Displays"). A display Run reads only `j02_evidence_value/<Task>/runs/<value
     Run>/result/`, never a path under `work/`: the tables it plots are the value Run's copies, and every number it
     prints (a median, a mean, a percent in a corner) is an id of that Run's `values.json`, read by id, never worked
     out again in the drawing script. A number with no id gets its id in the value Job first. The displays of one
     version read one value Run; when a newer value Run changes a file a display reads, that display is drawn again
     as a new Run. The display Run's `run.yaml` `reads:` lists those value files, so the check can compare them.
   - The paper Board owns one display Job, `j01_evidence_display`, with one Task per display (`t01_display-a-<slug>`,
     `t02_display-b-<slug>`, …, `tNN_display-<letter>-<slug>`, numbered continuously; main or appendix is the plan's call; older Boards: `t01_figure1-<slug>` in number bands, still read), each face with `label:`, `status:`, `answers:`,
     `cited-in:`, `layout:`, `sources:`, `made-by:`. The **display plan** is the
     `s06-paper-displays` Studio topic (older Boards: in the Job face), which the authors agree before any Run draws (JL 261023): per display its number, title, one question, layout (rows,
     columns or axes), source Runs and open choices, taken from the team's meeting notes and slides in the Block's
     `related/`. Drawing starts after the plan is agreed; Sections write their numbers after the drawn displays pass
     review and are accepted.
     A Run in that Task draws the picture or the table body into its `result/` (`figure.pdf` and `figure.png`, or
     `table-body.tex`, plus `figures.md`). A display that reads several question Jobs still lives in that one Job.
   - **One display, one home (JL 261113).** The display Task holds all of it: question, caption, legend, number,
     venue size, `cited-in:` and its `review/rNN.md`, beside the Runs that draw it. A Section keeps no
     `display/Display<n>-<slug>/` copy; its text cites the label. An older Board's Section-side unit
     (`display/Display<n>-<slug>/` or a `results/` payload) is still read by the build and the workbench. A display Run only draws from returned, aggregated
     Results; no paper folder runs analysis on raw data.
   - VALUE (Ework) cards point at the same work Block's Runs, so one Block is the source of every number and
     every picture.
   - The revise loop sends each fix where it lives: a picture problem (colour, scale, panel, denominator) goes to
     the display Task's Run script, drawn again as a new Run (a wrong number goes back to the work Run that computed
     it); a caption, legend or question problem goes to the display Task.
   **Every main-text and eAppendix display passes the display revise loop before the version leaves DRAFT** (JL
   261022: "display should also have a loop, like the draft is a loop; a display matters as much as the main
   text"). The loop is hai-display's `1_base/display/ref/display-revise-loop.md`; the paper adds three things,
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
   keeps the Section from closing. hai-paper-draft writes the sentence; this skill checks which of the three it is.


The chain: work → value → display → writing
-------------------------------------------

Every number the paper prints passes down one chain, and each layer only does its own job (JL 261110, after a paper
whose displays drifted from its values: medians worked out in drawing scripts, displays on an older value Run, a
forecast set beside another scored on different windows, ids from an older setup mixed with current ones, and a raw
table built before a rescoring that nobody marked stale). Nine rules keep it solid:

```text
work Run ─▶ value Run (copies, gives ids) ─▶ display Run (draws by id) ─▶ Section (quotes by id)
   ✅ computes      ❌ computes nothing         ❌ computes nothing          ❌ computes nothing
```

1. **Only work computes.** A value Run copies work's returned files and gives each number an id; a display Run draws;
   a Section quotes. No layer after work computes a number the paper prints.
2. **Id before ink.** Every number a display prints (a takeaway, a corner label, a table cell) is a value id, read by
   id; a missing id fails the Run. Where the display also plots the points behind that number, it asserts that what
   it drew equals the id. The display Run writes the ids it used, with their values, to `result/values_used.csv`.
3. **Pinned versions.** A display Run names its value Run in its own config (`run.yaml` `reads:`); a Section names
   the value Run it quotes. Never "the newest". A closed Run's ticket refuses to run again: a change is a new Run.
4. **Same setup for things compared.** Each work Run writes its setup (patients, windows, scoring rule) into its
   `metrics.json`; the value Run gives those ids; a display that sets two things side by side asserts their setups
   are equal before it says so. A caption sentence about the setup is read from those ids, never typed.
5. **An older setup leaves the list.** When the setup changes, ids measured the old way stay in the old value Run
   and are not carried into the new one. No "right, but check before quoting" flags: a `flag:` on a value fails
   the check.
6. **Staleness travels down, when what was read moved.** A source work Task with a completed Run newer than the newest
   one the value Job reads there marks the value Task stale (an older Run passed over is on purpose). A display or a
   Section on an older value Run is stale only when something it read changed or left in the current one: a file it
   read under `result/` no longer byte-identical, an id it prints or quotes gone or with another value. A newer value
   Run that only adds ids leaves its readers current (JL 261111: "yes, please change them"; before, adding 25 ids
   made 12 displays stale and 16 identical Runs were drawn again).
7. **A second route for headline numbers.** The check recomputes the headline numbers with independent code, from
   the scores rather than from the Task's own output: a paper's own `scripts/recompute_check.py`, which the check
   runs when it is there.
8. **One check before a send.** The chain check runs as the value Job's paper-wide Task (`t99_paper_value_check`)
   and blocks gate G4 (hai-paper): a version is not sent while it fails.
9. **A Section reads the verdict; it never runs evidence itself (values, citations and displays).** The Board's evidence Jobs check every printed
   value (j02, `result/ledger.csv`: section, sentence, status, printed, value, source) and every citation (j03,
   `result/citations.csv`, `cited_in`). A Section keeps no `run-value-*` or `run-citation-*` Runs of its own (an
   older one moves to `runs/_old/`). Its 3 · Evidence view shows "✅ Checked at the Board": one row per printed
   value and citation of that Section, from each Task's newest Run, its status in colour (match, no anchor, owed,
   differs) and the Task as a link (JL 261113, on a Section's own Runs: "do we need this? how do you think this to
   the block level evidence???"; the workbench reader is `workbench-task-draft/page_shell/board_checks.py`). Displays the same
   (JL 261113: "Similarly, we have the displays that are in the block level as well ... we should update it to be
   the same"): a Section keeps no display unit; each display Task's `cited-in:` names the Sections that cite it, and
   a Section's 4 · Display view shows those Tasks, read only: picture, label, `status:`, accepted Run and the newest
   review score. A Section that only points to a display another Section prints ("(Extended Data Table 4)" in the
   Discussion, printed by the Extended Data Section) writes a DISPLAY item with `Expected` and `Local Input` and **no
   `Local Run` line**: a Local Run is only for a display the Section prints itself, framed into
   `results/re-display-<n>`; one pointing elsewhere fails `page.py export` ("selected Result is missing", "is not one
   of this Page's own run results") (t03_discussion 261116).

**The check**, `scripts/chain_check.py`:

```bash
python scripts/chain_check.py <paper Board> [--json]
```

It reads both value-Job shapes, the standard one below (`value_map.yaml`, `values_ledger.py`) and a copying one
(`scripts/values.yaml` with `sources:` and `values:`, Runs with `values.json` and `result/<key>/SOURCE.txt`), and
says, one line per failure: a copied file that differs from its source Run's file, or a source Run not complete; an
id whose value no longer equals its source; an id in two value Tasks; a value or display reading an older Run than
the current one; a display that reads `work/` or prints an id whose value moved; a Section binding on an older value
Run; a flagged id; and the paper's own recompute, when it fails. It writes nothing and exits non-zero on any failure.
`paper_check.py` shows it as row V11, "The chain holds" (without the recompute, to stay quick; run the script itself
before a send). What it cannot see: rule 4, since no work Run yet names its setup in a form it can compare, so a person
reads each side-by-side display for it; and a value Task with no spec to re-read from (a raw-tables Task) is checked
for copies and staleness only.

A generated preview links its addresses
---------------------------------------

A script that writes an HTML preview the workbench shows (a `values.html`, a `citations.html`, a ledger) prints every
Run address `bNN.jNN.tNN.rNN` and Section name `tNN_<name>` as a link, through the one shared helper, never a copy of
it in the script (JL 261103: "b52.j01.t01.r01 <--- how could you make this to be clickable"):

```python
import sys; sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/servers/workbench/page"))
from address_links import page_linker          # standard library only
link = page_linker(<the page folder the preview belongs to>, <the SPACE root>)
html = link(html)                              # text only; tags, attributes and existing links stay as they are
```

An address opens its folder's focus page in the whole tab (`target=_top`, the preview sits in an iframe); a Run
number shared by two Runs opens the Task. An address that finds no folder stays plain text.


The value Job and the citation Job (0.7.0)
------------------------------------------

JL 261103, via the two paper sessions: the paper value and citation evidence is a standard part of every paper Board,
not scripts each paper writes for itself; then "how do you think you can unify them together" (the MISQ ledger,
printed-first, and the JAMA one, value-first). The generic layers are hai-evidence's `cards.py` (0.9.0: a VALUE
item bound by `value: <id>`, its status, `lineage`, binding proposals); this skill adds the paper's rules on top.

```text
work/bNN_/jNN_/tNN_/runs/rNN_/result/values.csv   key, value, ..., source   ◀ the work Run computes; `source` names
        │                                          what it read (a src/inputs.yaml key, typed:"<file>", bNN.jNN.tNN.rNN)
        ▼
paper/Paper-X/j02_evidence_value/
├── tNN_<group>/scripts/value_map.yaml   1 catalog: rq, group, runs, values{what, run, where, digits, scale, unit, p}
│   └── runs/r01_read_values/result/     values.yaml (id RQ1-tNN-nnn, value, shown, checks, printed) · values.html
│                                        · ledger.csv · headline.txt
└── t99_paper_value_check/runs/r01_check_values/result/   every binding at once; numbers printed with no binding
        ▲ 2 bindings: VALUE items in each Section's evidence/cards.yaml   {run: r01, for: [S5], value: RQ1-t03-002,
        │   anchor: ['2.79']}   (a display: {display: Table 2, printed: [...]})
        │   seeded by the search into evidence/proposals.md; a person ticks once; then fixed
        3 check: match · differs · missing · no anchor · owed · pending · stale · found (searched, not bound yet)

paper/Paper-X/j03_evidence_cite/
├── tNN_<claim group>/scripts/claim_group.yaml   label, question, what, discovery, keys
│   └── runs/r01_check_citations/result/         citations.csv · citations.html · values.yaml · headline.txt
└── t99_paper_citation_check/                   all keys; checks.md (proposed-cards/ only for a Section with evidence/cards.yaml)
```

1. **A paper's j02 holds only value maps; its j03 only claim groups.** Everything else is made by the scripts:
   `gen_value_runs.py <j02>` writes each value Task's Run card and ticket and the `t99_paper_value_check` Task;
   `cite_tasks.py gen <j03>` the same for the citation Job. A face is written when missing; a face a script wrote says
   GENERATED and is rewritten. The tickets find the toolkit and a Python by walking up (`HAIPIPE_PYTHON` wins).
2. **Every printed value names its Runs, its question and its place.** Its id is `<RQ>-<tNN>-<nnn>` (or the map's own
   `id:`); its `checks:` are the work Run that computed it, then what that Run read (hai-evidence `lineage`: the
   values.csv `source` column through the work Block's `src/inputs.yaml`); each place it prints is a binding.
   So a work Run's `values.csv` keeps a `source` column; without it the lineage stops (⚠️ in the ledger).
3. **Bindings are seeded, never typed.** `values_ledger.py bind <j02>` (dry run) and `--propose` find each value in
   the printed text and the displays and add one `bind VALUE <id> to <place>` line per hit to the holder's
   `evidence/proposals.md`; a person ticks once and `--adopt` writes the ticked ones as card items (`--confirm
   [tNN_<section> ...]`: an agent confirms them all). A written binding is never rewritten by the search.
4. **The finder's guards.** A P value (`p: true`) only after "P =" or "P <"; a whole number under 10 never; a number
   with fewer than two significant digits and fewer than two decimals only inside an estimate's run; an estimate
   with a CI (`<stem>.b`, `.ci_lo`, `.ci_hi`) only as "b (lo to hi)"; its P, N or mean only where the estimate prints;
   a display row only when the display names what it was drawn from (its `intake/manifest.yaml`, its Run card's
   `reads:`) and that shares a Run with the value. Equality is exact half-up rounding at the printed precision.
5. **Both page shapes** (paper_text.py): a draft's `## 3 · Draft` lines give S ids (`for: [5]`); a Section's
   `## Content` gives its `<!-- realizes: <id> -->` ids, or `<paragraph>.<k>` for a line without one. A Section's
   printed text is its Content, each line named by its draft S id when the draft holds the same sentence.
6. **The reverse lists.** A value Task's ledger closes with its values never printed; t99 lists the numbers printed
   with no binding (a value owed, or a number still to bind).
7. **values.html, the ledger look**: Value name (its ID under it) · Where · Printed · Value · Status · Source and key, problems first; the
   source trail names each Run in words, linked to its workbench page (the address in the tooltip); a value with no
   Run or from a screen read is flagged; the values never printed sit in a closed list.
8. **Blocking (gate G4, evidence_ledger.py)**: a printed value that names no Run (`linked: false`), whose chain holds
   a typed stand-in (`screen_read`), or whose binding differs, is missing or is stale is a ❗; owed values are open
   (⬜). hai-paper's paper_check reads the same files (V3 values filled, V4 citations verified, V5 the ledger).
9. **Citation statuses** (cite_tasks.py), in order: TOADD, missing-bib, verified (a bib entry and a person's
   signature: a page-local CITE Result, or a card item `verified: ✅ <person> <date>`), card-only, bib-only; plus no
   DOI, one key with two DOIs, back-to-back sentences, citing sentences with no CITE card, and the card edits; only
   `cite_tasks.py apply`, run by a person, writes a Section's CITE items, and only into an evidence/cards.yaml that
   exists.
10. **A Section's CITE items name the Run that checked them** (must-check M-D20). A Section whose evidence lives in
   `draft/<stem>-evidence-items.md` is bound, never carded: `cite_tasks.py bind <Section Task>` (cite_bind.py) prints
   each CITE item's new `Local Run` (`Page · Evidence Item · reuse · P.j03.t01.r01 → j03_evidence_cite/.../result/
   citations.csv`, and its discovery Run as `Supporting Runs` when it names none), matched by BibTeX key; `--apply`
   writes it. An item that names a Run is kept. Draft Lab draws its ❝ card from the bound Run, else the check's row,
   else its BibTeX marked "not read yet"; `page.py health` WARNs on an unbound item and FAILs under `--final`.

```bash
E=Tools/plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper-evidence/scripts
.venv/bin/python $E/gen_value_runs.py <paper>/j02_evidence_value          # Run cards and tickets from the maps
bash <paper>/j02_evidence_value/tNN_<group>/runs/r01_read_values/r01_read_values.sh
.venv/bin/python $E/values_ledger.py bind <paper>/j02_evidence_value --propose   # then tick, then --adopt
.venv/bin/python $E/cite_tasks.py gen <paper>/j03_evidence_cite             # then each Task's ticket
.venv/bin/python $E/cite_tasks.py bind <paper>/jNN_writing_*/tNN_<section>  # dry run; --apply writes the Local Runs
```

**Migration of the two papers that made the pattern** (not done here; each in its own paper session):
1. **MISQ first** (`Paper-<the MISQ paper>`): its bindings already exist, typed in b52's
   `bind_paper_cards.py` BINDINGS and written into each Section's cards; write one value map per j02 Task from b52's
   values, keep the cards (an item with `file` + `key` still checks), run the new Runs, and require every status the
   old `values_ledger.py` gave (match, differs, missing, owed, pending) to come back the same: the old bindings are the
   regression test. Then its j03 moves to claim_group.yaml from `scripts/cite_tasks.py` GROUPS.
2. **Then JAMA** (`Paper-<the JAMA paper>`): its value maps already have the shape (`tNN_values-*/scripts/
   value_map.yaml`); run `gen_value_runs.py`, then `bind --propose`, tick, `--adopt`: its bindings are seeded by the
   search, so its ledger gains differs and missing it could not say before. Its `src/` scripts retire after that.


Each display version: one preview.pdf
------------------------------------

Every Run of a display Task (a version of that display) leaves, in its `result/`, the unit's `float.tex` and
`preview.pdf`: page 1 the display with its caption, page 2 opens with what it says (its `## Message`, JL 261103) and
goes on to how it was made, from `method.md` (hai-display's
`scripts/build_preview.py`; JL 261101). The workbench's Report › Evidence › Displays shows the newest version's
`preview.pdf`, every page, with ⤢ Pop out.

After the method pages come the earlier versions (JL 261104: "add the previous old versions at the bottom of the
pdfs"): one page each, newest first, the display page of each lower-numbered Run of the Task, headed by its Run name,
date and what changed (the card's `change:` line, else `says:`). `build_displays_pdf.py` and the paper take page 1 only,
so these pages never reach the paper.

New data or a new look means a new Run, with a `change:` line on its card. Never delete a display Run's `result/` to
redraw it: the old picture is then gone from this list.

Page 1 is the display as the paper prints it (JL 261101: "the full pdf preview, just like the one we will see in the
paper pdf"). Build it with (from the SPACE root, where `Tools/` is the Tools checkout; elsewhere use the full path):

```bash
.venv/bin/python Tools/plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper-evidence/scripts/preview_display.py <unit> [--method-from <source preview.pdf>]
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

The pool's Tasks are seeded from the display plan (hai-paper-plan `s06-paper-displays`, `display_plan.py seed`),
which also gives each its paper number: the tab's first line reads `Figure 1 (Display A)`.
The list shows the label, then "📈 Figure · <name>" or "📊 Table · <name>" (board_results._display_line); a face with
no `name:` gives the title after "Display X," in its first line, else the folder's words.


The Values tabs
---------------

A paper Board's Evidence > Values is side tabs when a Task of its value Job has a Run with `result/tables.json`; otherwise
one side tab per Task, as before (JL 261104, ScalingGlucose r04_collect_values_tables, s03-D09). The rules:

1. **Each tab is one readable topic**, never a bare id like Q04; tabs need not match questions one to one.
2. **A table is raw**: rows picked from Run outputs and arranged, no averaging, fitting or transforming. Two source rows in
   one cell show both, side by side. Tables are windows on the data, may overlap, and are raw material for the displays.
   Anything computed goes in its own tab, labelled computed.
3. **A cell is its value and a status word**, checked against the source Run on every page open, never typed. Clicking it
   opens where it came from: status, source Run, file, displays reading it, Sections quoting its values.
4. **Under the table**: "How this table is made", closed, then the numbered values the text can quote.

```yaml
# <j02>/<tNN_x>/scripts/tables.yaml, run by a ticket: build_tables.py <that file>, RESULT_DIR set
words: {h24_rmse: Error up to 2 h}          # how a column's name reads on the page
suffixes: {num: numbers}                    # the same for a name's last part
tabs:
- slug: scores                              # methods.yaml's key and the output file's prefix
  title: Model scores                       # the tab
  line: Every model, by size                # the tab's small line
  story: One sentence the table tells.
  values: [V_score]                         # id prefixes of the numbers listed below it (values.json)
  chain: [scores]                           # shared lines of methods.yaml, then its tabs.<slug>
  tables:
  - from: t02_x/scores/scores.csv           # <value Task>/<key>/<file>: the newest of its Runs holding result/<key>/<file>
    name: By size                           # optional: the first filter button
    where: {split: test}                    # keep these rows; a list keeps any
    for: {metric: {h24_rmse: Up to 2 h}}    # one table per value, a filter button each
    pivot: {rows: size, cols: epochs, value: "{metric}", also: tokens_m, also_head: "tokens, millions", also_suffix: M}
    flag: {query: "epochs <= 0.1", why: "Why this cell needs a check."}
  - from: t02_x/scores/scores.csv
    list: [size, epochs, h24_rmse]          # instead of pivot: one row per source row
```

The value Run keeps `result/<key>/<file>` beside `result/<key>/SOURCE.txt` (`copied from <path from the SPACE root>`), which
the status reads; `result/values.json` is `{id: {text, says, source}}`, `source` naming the file. A Section "quotes" a value
when its newest draft holds the id. Example: Tools' Paper-Example, `j02_evidence_value/t02_raw-value-tables`.

The display checklist
---------------------

JL 261103: "please update the /hai-paper-display's checklist". What each printed display needs before a send, in
the order a display is made; the paper checklist (hai-paper `paper_check.py`) ticks P9, V2 and V5-V10 from disk:

```text
P9  planned       a row in s06-paper-displays, within the venue's display rules (display_plan.py check)
V2  drawn         by a Run of its j01_evidence_display Task, from returned aggregate Results
V6  its message   `## Message` first in the Run's method.md: what we want to say with it, 1 to 3 sentences;
                  it opens page 2 of preview.pdf as "What this display says" (JL 261103). Written with the display,
                  in the same Run, never left for later (JL 261104: every preview said "No message written yet").
                  Plain words, the finding and not the design; numbers stay in the Takeaways, which read Evidence.
                  When the picture changes, reread it. caption_check.py fails a display with none or a longer one
V10 short caption a title of at most 15 words and a legend of at most 75 (a table's footnotes 120); it only defines
                  what is drawn: symbols, lines, colours, scales, groups, abbreviations. Findings go in ## Message and
                  Results, design and sample in Methods (JL 261103: "for the Figure caption, do not add so much things,
                  don't be too long"; the caption rule, hai-display ref/display-revise-loop.md). caption_check.py.
                  The venue's rule wins: read its author guide, write it in call.md's caption row, with any limit as
                  `at most N words`, and the check reads it (JL 261104: "let's follow the venue")
V7  examples      the venue's published displays on one canvas, sNN-paper-display-examples, compared with ours
V8  questions     each choice about it (version, layout, keep or drop) asked and answered as a collection Run
                  (hai-interaction), in j01_evidence_display/runs/ or its Task's runs/
V5  reviewed      the blind revise loop passes (rule 3), or the ledger keeps flagging it
V9  accepted      a person writes `accepted: yes` in the unit README, with their words
```

**The Displays view shows the same order** (workbench-paper G · Displays): 1 · Plan (the s06 drawing), 2 · Displays
(each Task's newest preview.pdf; each display's state is its tab's, no separate "Where each display stands" list), 3 ·
Examples (the examples drawing, else how to make it), 4 · Story by Section (the Story view's own section, the same
panel, last; JL 261109), and the page's last section, 🙋 Interaction (the
collection Runs at the Board or below, hai-interaction). The message is written in the display Run's
config (`message:`) or straight into its method.md, or in one file per Job the Runs read (ScalingGlucose:
`j01_evidence_display/src/display_messages.yaml`, by label); a paper's preview script writes `## Message` first.

Count a display Job's captions and check its messages before every review round; a venue's stated limit wins (pass it with `--legend`), and
a caption over the limit is a journal-ready finding in the revise loop. Exit 1 on an over-long caption; it changes no file:

```bash
.venv/bin/python Tools/plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper-evidence/scripts/caption_check.py <paper>/j01_evidence_display
```

All displays as one PDF
-----------------------

```bash
.venv/bin/python Tools/plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper-evidence/scripts/build_displays_pdf.py <paper>/j01_evidence_display
```

Every display of the display Job in one PDF, one page each in Task order (main, then appendix): its label, caption,
and the picture or the table; a display not drawn yet gets a page that says so (JL 261101: "I also want a link for
the display, so we can view all the displays as one pdf file"). It writes `<Board>/delivery/<job>/<job>-all-displays.pdf` (the Board owns delivery/)
(generated: rerun after a display changes, never edit the PDF), and the workbench's Evidence view links it as "Open
all displays as one PDF". It finds each drawn file with the workbench's own lookup, so the page and the PDF agree.


Before a send: one check
------------------------

AgreeableJama-Board 261123 (JL asked whether a "hai-paper-check" skill should exist): a co-author found a sentence
saying an opioid prescription "was filled" after 21.6% of visits, where the source says "the rate of opioid
prescribing was 21.6%"; no check had read a single source, and `paper_check.py` ("65 to fix") and `chain_check.py`
("947 failures") could not tell a wrong number from a missing record. Decided: no new skill. This skill already owns
citations and values "before a build or a send"; `/hai-paper-check` is its alias, and the door is one script.

```bash
E=Tools/plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper-evidence/scripts
.venv/bin/python -B $E/cite_support.py sources <paper>/j03_evidence_cite   each DOI's PubMed abstract, cached
.venv/bin/python -B $E/cite_support.py sheet   <paper>/j03_evidence_cite   one row per citing sentence and key
   hai-draft-evidence-cite-agent fills each row: reading, the source's passage, note, by
.venv/bin/python -B $E/send_check.py <paper Board> [--out send-check.md]  the door; exit = the ❗ count
```

```text
❗ prints wrong      a key that prints "?" or TOADD; one key in back-to-back sentences; a reference that prints no
                    DOI and no URL (or drops the DOI its bib holds); an access date printed as data; numbers out of
                    order of first citation (Word); a reading `wrong` or `looser`; a number the sentence quotes that
                    no supporting passage holds; a printed number that differs from its value
⬜ not recorded      no signed CITE Result; a citing sentence not read; numbers not bound; chain records disagree
🙋 a person          a reading `not checkable`; reference numbers the Word check could not find cited
```

The rule: **before any co-author round, every citing sentence has a recorded reading** in
`j03_evidence_cite/t99_paper_citation_check/support.yaml` (supports, looser, wrong, not checkable; the agent's own
partly, does not and unclear read the same), with the source's own words quoted. A number quoted from another paper
is read for what it measures, not only its digits: "filled" and "prescribed" are two measures (the reader's job;
the script checks only that the digits are in the passage). A changed sentence loses its reading and is read again.
`paper_check.py` stays the progress list; this door is the send gate.


The version ledger
------------------

```bash
L=Tools/plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper-evidence/scripts/evidence_ledger.py
.venv/bin/python -B $L <paper>/jNN_writing_v<MMDD>_<desk>/                    every Section of one version, side by side
.venv/bin/python -B $L <paper>/jNN_writing_v<MMDD>_<desk>/ [--max-displays 7]   the venue's limit on main-text displays (default: its call.md ## Displays main limit)
.venv/bin/python -B $L <paper>/jNN_writing_v<MMDD>_<desk>/ --json             for a builder or a workbench
```

It reads each Task in either shape: `evidence/cards.yaml` (hai-evidence, since 261016) or an older Page's
`draft/<stem>-evidence-items.md` (read by hai-draft's `item_table`, the parser the Page workbench uses), its
`display/Display<n>-*/`, and its `.bib` files (its own `draft/evidence/bibex/`, else each CITE card's Run).
Parts by Task number: `t00` the Abstract, `t01`-`t19` the main text, `t2N` the appendix, `t3N` the letters. Only the
Sections in the version face's `haipipe:compile-order` block are numbered, counted and compared; the rest show
`⏸ off`.

```text
❗ one value, two Runs            the same VALUE value (source, file, key) read from different Runs in two Sections
❗ one label, different estimates  an older VALUE label whose Results report different estimates, compared in
                                  one unit (a key with pp or percentage_point is in percentage points)
❗ one citation key, two entries   the same key with another year or title in two Sections' .bib files
❗ too many displays              main-text displays over --max-displays
❗ a card does not resolve        hai-evidence's cards.check, per Section
⚠️ one label, the same estimates  two Results that hold the same estimates (one copies the other: point both at one)
❗ display drawn inside the paper  a main-text display whose intake/manifest.yaml names no Run's result/ (a work
                                  Run, or a Run in the Board's j01_evidence_display Job), or one outside the
                                  version's work-block: or Board, or one that does not exist
❗ display has no question        a main-text display whose README names no question:
❗ display review not passed      a main-text display whose latest review/rNN.md fails the pass rule, or that has
                                  no round yet (the listing shows each display's latest score: r02 8.5/10 ✅)
❗ value not linked / screen read  a printed value of j02_evidence_value with no Run, or from a typed stand-in
❗ value differs / missing / stale a binding of a printed value its value Run's check failed
⚠️ one display twice              the same display name in two Sections
⚠️ the same three, on an appendix an eAppendix display drawn inside the paper, with no question:, or no passing review
⬜ open                           citations not yet verified, values not yet landed, needs not yet filled
```

**What it does not read yet**: numbers typed into table bodies or prose, and wording that drifts between Sections
("no association" in one, "close to zero" in another). Those stay a person's read of the built PDF
(hai-paper-assemble's cold read). **The venue's limit** is read from the venue's call (`venues/<venue>/call.md`, `## Displays` main limit),
or passed by hand with `--max-displays` when the person says it; a QBv desk record may not hold it.

It changes no file of the paper: the ledger is a view of the Tasks' own files, so nothing generated is tracked (`-B`
keeps Python from writing its bytecode cache beside the script). Exit 1 on a ❗. A ❗ is fixed in the Section that is
wrong (its card, its Evidence Item, its `.bib`, or the Run it reads), never by editing a built file.


Where it sits on the ladder
---------------------------

```text
Board     💡 s01 idea · 📖 s02 story (§7 allots evidence to Sections) · 🔍 s10-s19 related · ❓ reports/qNN_
  └─ Job  jNN_writing_v<MMDD>_<desk>: the Narrative order · 🧾 this ledger, once per send
      └─ Task tNN_<section>: draft/ ✎ (hai-paper-draft) · evidence/ 🧾 (this skill); its displays 📊 are the Board's display Tasks
```

Who calls it: a Section's CHECK (hai-paper-draft's closing checks), `hai-paper-assemble` before a build (gate
G4), and a person before a send. It proposes nothing itself: a missing piece is a card with `need`, and
`cards.py propose` (hai-evidence) flags what to make.


Files
-----

```text
hai-paper-evidence/
├── SKILL.md                      this contract
├── CHANGELOG.md
├── scripts/evidence_ledger.py    the version ledger (and G4 on the value Job)
├── scripts/values_ledger.py      the value engine: catalog, bindings, check (run · check · bind)
├── scripts/gen_value_runs.py     a j02's Runs and t99 from its value maps
├── scripts/build_tables.py       the Values tabs: raw rows from value Runs into tables.json
├── scripts/cite_tasks.py         a j03's claim groups: gen · run · apply · inventory
├── scripts/cite_support.py       each citing sentence read against its source: sources · sheet · check
├── scripts/send_check.py         the one check before a send: prints wrong · not recorded · a person
├── scripts/paper_text.py         what the Board prints: writing Job, Sections, sentences (both shapes), displays
├── scripts/build_displays_pdf.py all of a display Job's displays as one PDF
├── scripts/caption_check.py      each display's caption against the word limits
├── tests/test_evidence_ledger.py a made-up version: two Runs, two estimates, too many displays, unreviewed displays,
│                                 a display drawn inside the paper
└── tests/test_values_ledger.py   Tools' Paper-Example: found, tick, match, differs, owed, a display hit, never
                                  printed, printed with no binding, a screen read, an older Section shape
```
