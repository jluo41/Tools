# PNAS: the outlet whose folder is doubled and whose gate has its own section

state: 🟡 PARTIAL · 6 sections incl. pnas-significance · exemplars and taste sit one level up · no outlet-level taste
owner: JL
method: state what the PNAS desk asks of a paper and record the doubled folder name and the split between the gate's test and the gate's section

## Opening

PNAS is the only journal in this tree with a section folder of its own for the Significance Statement. The test that decides whether a paper can carry one at all sits a level up, in `playbook-pnas/taste.md`. The rules for writing it sit in `playbook-pnas/pnas/pnas-significance/style.md`. Neither file names the other, so a writer who opens one never learns the second exists. Which one comes first?
> ✎ ~This outlet has~ *PNAS is the only journal in this tree with* a section folder *of its own* for *the Significance Statement. The test that decides whether* a ~component no other journal~ *paper can carry one at all sits a level up,* in *`playbook-pnas/taste.md`. The rules for writing it sit in `playbook-pnas/pnas/pnas-significance/style.md`. Neither file names* the ~tree has, and its readiness test lives~ *other, so a writer who opens* one ~directory above it.~ *never learns the second exists.* Which one ~does a writer actually read~ *comes* first? · CC · 260802 1543

**How to read this page**: everything here is a REFERENCE, not a rulebook.
The arcs, budgets, moves and refusals below describe what published PNAS papers do, measured from the 34 exemplars on disk.
A paper that departs from them is off-pattern, which is a thing to do on purpose and not a violation.
One figure is different: `Submission-Rules` carries the desk's own published rules, and a manuscript that breaks one of those is returned unreviewed.
Every length on the page says which of the two it is.

**Where this page sits**: it is one venue target in `QBv`, and the only one in its pack.
This page owns only what is true of `playbook-pnas/pnas/`.

**Why this outlet has almost nothing of its own**: the pack has one journal, so `taste.md` and `examples/` were kept at family level and only the section folders sit here.
The group intro on the Index owns that placement split.
> ✎ ~the~ *The* group intro on the Index owns that placement ~split; this page is the outlet where it~ *split. It* is most ~confusing,~ *confusing at this outlet,* because ~`playbook-pnas/pnas/` doubles~ the ~name.~ *pack folder `playbook-pnas/` holds one outlet folder called `pnas/`, so the full path says the name twice: `playbook-pnas/pnas/`.* · CC · 260802 1543
It is most confusing at this outlet, because the pack folder `playbook-pnas/` holds one outlet folder called `pnas/`, so the full path says the name twice: `playbook-pnas/pnas/`.

**What is split apart**: the readiness test is in `playbook-pnas/taste.md`.
The section norms for the Significance Statement are in `playbook-pnas/pnas/pnas-significance/style.md`.
Neither file points at the other.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**A length number carries its source on the same line**: a budget, a count or a density may appear, tagged with the file and heading it was measured in or with the exemplar it was measured from, so it stays the pack's claim and never becomes this page's.

**Write the doubled path in full every time**: `playbook-pnas/pnas/pnas-significance/` is the real shape, and abbreviating it is how a path written from memory goes wrong.

✅ `playbook-pnas/pnas/pnas-significance/style.md`  ❌ `the significance style guide`

**The venue-page contract is a file, and this page obeys it**: it is `../../board/page-types/haipipe-page-for-venue/SKILL.md`, and `QBv1-misq.md` is its reference implementation. A rule below is stated here only so a writer editing this page meets it; the contract is what carries it.

```text
  🖼 THREE FIGURES IN `## Diagram`, IN THIS ORDER
     ① desk taste         what counts as the contribution · what is
                          desk-rejected · the desk's own test, quoted
     ② Venue-Structure    the sections in the venue's READING ORDER, each with
                          its budget, and the one ceiling over all of them
     ③ Submission-Rules   category and cap · manuscript format · references ·
                          the portal · anonymity · disclosures · the odds, the
                          clock and the money · an open row for what is NOT on
                          record · the desk's own URLs

  📎 FIVE FILES GROUPS, IN THIS ORDER
     ⚙️ Engines           what REGENERATES this page
     📋 Contracts         the venue-page contract, and the base it extends ·
                          a loadable spec is a Contract and never an Engine
     📥 Input files       the pack files this page READS
     🔗 Authority         what the DESK itself PUBLISHES, read directly and
                          never through the pack · opens with the provenance
                          stamp · holds every place the desk contradicts the pack
     📤 Generated         what `sync-exemplars.py` WRITES between markers

  🔢 A SECTION DIVISION CARRIES ITS Sec- INDEX
     ### 4 · Sec-1-Abstract: the second read, and it may not echo the first
         ▲       ▲
         │       └── Sec-<i>, counting from 0 in the venue's READING ORDER ·
         │           only an appendix takes a letter, and PNAS declares none
         └── the Content division number, which counts §1 and §2 as well
     ### A4 · 📄 Sec-1-Abstract: the second read, and it may not echo the first
              ▲  the emoji lives HERE and on the division's closing line, never
                 on the division heading: `check.py` strips it from an Aims or
                 States group name and not from a Content division, so a
                 heading-side emoji reads as group-name-drift on every section
                 at once
     ⚠️ AT THIS OUTLET Sec-<i> IS NOT THE S-Main NUMBER, and that is a real
        disagreement rather than a slip · `Venue-Structure` prints both

  📖 A VENUE PAGE IS A REFERENCE, NOT A RULEBOOK
     the pack-derived arcs, budgets, moves and refusals are suggestions drawn
     from published papers · only the desk's own published rules bind, and they
     live in the `Submission-Rules` figure and the `Authority` group
     write "the pack refuses X" rather than "do not do X", so the page never
     sounds like it is the one doing the refusing

  ⚖️ EVERY LENGTH SAYS WHOSE IT IS
     a DESK RULE is published by the venue and binding · a PACK OBSERVATION is
     a measurement of papers the pack read, and breaking it is off-pattern
     rather than a violation · a budget printed with neither label reads as a
     rule, which is how this page's 6,970-word section sum was being read

  ❓ AN UNKNOWN IS PRINTED    a slot neither source can fill is written as an
     open row in `Submission-Rules`, never left off the figure
```

**What the pack knows and what the desk says are two different sources**, and where they disagree the desk wins and the disagreement is written down. The pack is READ and never written by this plugin, so a correction lands here, not in `paper/venue/`.

## Diagram

**Six sections, one of them the gate**: and the test for that gate is one level up.

```text
  📁 playbook-pnas/                    ← FAMILY level
     taste.md          ← the READINESS TEST lives HERE
     style-profile.md
     examples/         ← 34 exemplars, HERE
     └── pnas/                          ← OUTLET level
         pnas-abstract/
         pnas-introduction/
         pnas-methods/
         pnas-results/
         pnas-discussion/
         pnas-significance/  🚪 the gate's own section
                             style.md + template.md

  🎯 THE TEST (family level)
     "Would a scientist in a completely different field read
      the Significance Statement and think 'I need to know
      this'?"

  ⚠️ the test names the section; the section does not name
     the test ── a writer arriving at either finds only half

  📏 ~6 pages · ~50,000 characters
  ❌ narrow technical advance · long discursive papers ·
     no significance statement · purely descriptive with no
     mechanism or policy implication
```

**Venue-Structure**: the sections a PNAS paper is written in, in the order the desk reads them, and what each one costs.

```text
  🏗 VENUE-STRUCTURE ── every budget below is stated with its source inline in
     the §3 to §8 division that owns it, and §10 is the desk's own gate

  index                       §    S-Main page   budget                  what the section owes
  ───────────────────────────   ──   ───────────   ─────────────────────   ──────────────────────────────
  🚦 Sec-0-Significance       §3   S-Main-1      <=120w DESK RULE ·      1 ¶, 6-7 sentences, 0 citations,
     Significance                   110-120 observed        4 slots, lay-legible throughout
  📄 Sec-1-Abstract           §4   S-Main-0      <=250w DESK RULE ·      1 unstructured ¶, 6 slots, same
     Abstract                       154-240w observed       framing as Sec-0 and none of its
                                                                         sentences
  🪝 Sec-2-Introduction       §5   S-Main-2      ~600-1,200w PACK        the unlabelled entrance, the
     Introduction                                           question posed as a question,
                                                                         and ~0.65 citations/sentence
  📊 Sec-3-Results            §6   S-Main-4      ~1,300-2,600w PACK      the largest section · carries its
     Results                                                own design context, because
                                                                         Methods is printed after it
  🏔 Sec-4-Discussion         §7   S-Main-5      ~700-1,400w PACK        argument, not summary · one late
     Discussion                                             limitations ¶, never last
  🔬 Sec-5-Methods            §8   S-Main-3      ~600-1,400w PACK        MAIN-TEXT methods only · bolded
     Methods                        of main-text methods    run-in blocks · names every SI
                                                                         item it hands off
  📦 no Sec-A    §9   none          not recorded            the SI Appendix, real and unowned:
                                                                         `section-kinds.yml` declares NO
                                                                         appendix kind for this outlet

  ⚠️ HERE THE INDEX AND THE PAGE NUMBER DISAGREE, unlike every other outlet
     Sec-<i> counts from 0 in the DESK's reading order: the Significance box is
     read first and Materials and Methods is printed last · `section-kinds.yml`
     resolves a different order (abstract 0, significance 1, methods 3), so
     Sec-0-Significance becomes S-Main-1 and Sec-5-Methods becomes S-Main-3
     nobody should convert this from memory · the column above is the conversion
     § is a third number and belongs to this page only: it counts §1 and §2, the
     two judgment divisions, ahead of the sections

  ⚖️ RULE vs OBSERVATION   the two front-block caps and the page ceiling are the
     DESK's, published and binding · every other word range above is the PACK's
     measurement of three exemplars, and the desk publishes no per-section limit
     a paper over a budget is off-pattern · a paper over the ceiling is cut

  📏 ONE CEILING OVER ALL OF IT   6 pages PREFERRED, 12 pages MAXIMUM
     the desk converts it itself: a standard 6-page article is about 4,000 words,
     50 references and 4 medium-size graphical elements
     [pnas.org author center, read 260803 through search summaries]
     💥 the six PACK ranges above sum to about 6,970 words, roughly 74% past the
        desk's own 4,000-word conversion · §8.1 carries that arithmetic, and the
        pack performs the sum nowhere
     ⚠️ the pack's "~50,000 characters" appears in NO desk instruction this page
        has read, and no pack file records the 12-page maximum at all

  ➕ A KIND IS A FLOOR, NOT A CEILING
     one kind may spread across several numbered Main pages
     the ORDER does not move: it is this venue's reading order
```

**Submission-Rules**: the desk's own mechanics, which the pack does not record and no section division owns.

```text
  🧾 SUBMISSION-RULES ── ⚖️ THE ONE BINDING FIGURE ON THIS PAGE
     every row below is the DESK's own published rule, and none of it is in the
     pack's six section folders · everything else on this page is a reference
     ⚠️ read 260803 through SEARCH SUMMARIES ONLY: www.pnas.org and
        www.pnascentral.org both answer a direct fetch with HTTP 403 · the
        260802 rows in the Authority group were fetched directly that day ·
        RE-READ THE DESK BEFORE SUBMITTING

  🚪 TRACKS            Direct Submission ── the standard route, editor-run peer
                       review, and the only route this page can assume
                       Contributed ── the desk publishes a live
                       "Member Contributed Submissions" page saying an NAS
                       member may contribute up to 2 research manuscripts a
                       year, in their own area, with a direct significant role
                       ⚔️ UNRESOLVED: secondary summaries read on 260803 claim
                          the Contributed track was ELIMINATED in 2022, while
                          the desk's own page for it is still up · both readings
                          are recorded and NEITHER is adopted
                       Prearranged Editor ── discontinued 2014-10-01

  📁 CATEGORY & CAP    Research Article 6 pages preferred, 12 pages maximum ·
                       a standard 6-page article is ~4,000 words, 50 references
                       and 4 medium-size graphical elements
                       Brief Report 3 pages, ~1,600 words counting text, title
                       page, abstract and figure legends, 15 references · its SI
                       takes extended methods, essential datasets and videos
                       only, and NO additional tables or figures
                       Letter 500 words, 2 graphical elements, 10 references
                       the cap follows the category, so pick it first

  ✍️ FRONT BLOCKS      Significance Statement <=120 words, MANDATORY, filed by
                       the desk as "Direct and Contributed Submissions only"
                       Abstract <=250 words, unstructured narrative
                       ⚠️ search summaries add that the Significance Statement
                          must avoid citations, numbers and abbreviations · the
                          pack's own anti-pattern list says the same, and this
                          page could not confirm the DESK's exact wording

  🖼 DISPLAYS          ~4 medium-size graphical elements in a standard article ·
                       anything past the page budget moves to the SI Appendix ·
                       the desk publishes no separate figure or table COUNT that
                       this page could verify, only the page budget

  📚 REFERENCES        PNAS style · numbered in the order they appear in the
                       text · in-text numerals in parentheses "(1, 2)", NOT
                       superscript · ~50 for a standard 6-page article
                       SI references are a SEPARATE stream: a writer may not
                       cite main-text references in the SI or the reverse

  📎 SI APPENDIX       ONE PDF combining text, figures, tables, movie legends
                       and SI references · published as provided, never edited
                       or typeset · numbered S1, S2, ... · the main text must
                       stand on its own without it · frozen at acceptance
                       templates published in Word AND official Overleaf LaTeX

  🖥 SYSTEM            PNAS Central, on eJournalPress, at pnascentral.org

  🕶 ANONYMITY         SINGLE-blind on the Direct track: reviewers see the
                       authors · the EDITOR's name stays anonymous to the author
                       until acceptance
                       ⚠️ the opposite of MISQ at `QBv1`, so a manuscript
                          stripped for a double-anonymous desk is not stripped
                          for this one

  📋 DISCLOSURES       author contributions, MANDATORY · competing interests,
                       declared on the submission form · all funding sources
                       acknowledged · data availability · the ethics and
                       publication-ethics policies sit on their own desk page

  🤖 AI POLICY         AI or generative-AI use during the research process is
                       disclosed in Materials and Methods, or in Acknowledgments
                       where there is no Methods section, naming the specific
                       tool AND its model or version · AI may NOT be listed as
                       an author · AI-generated images or graphics are NOT
                       allowed unless the software is itself the subject

  🎲 ODDS & CLOCK      ~16% of Direct Submissions accepted · ~54% desk-rejected
                       at initial screening · median 18 days to first decision ·
                       ~38-46 days to a post-review decision
                       ⚠️ these came from THIRD-PARTY summaries on 260803, not
                          from a desk page · they are reported statistics rather
                          than a promise, and the weakest provenance here

  💵 MONEY             open access $4,975 with a site licence, $5,475 without ·
                       delayed open access $2,575 · institutional agreements cut
                       it, and a University of California author pays $3,355
                       ⚠️ amounts from search summaries of the desk's own
                          publication-charges page, which answers 403 · VERIFY
                          THE CURRENT AMOUNT BEFORE BUDGETING

  ❓ STILL NOT ON RECORD
     whether a SUBMISSION fee exists separately from the publication charges
     whether the Contributed track is open today ── see the ⚔️ row above
     any per-section word limit ── the desk publishes none, so all six budgets
       in Venue-Structure are the pack's
     the desk's exact wording on what a Significance Statement may not contain
     a published target time to first decision, as opposed to a reported median
     a figure or table COUNT distinct from the page budget

  🔗 THE DESK ITSELF   pnas.org/author-center/submitting-your-manuscript
                       pnas.org/author-center/editorial-and-journal-policies
                       pnas.org/author-center/publication-charges
                       pnas.org/author-center/member-contributed-submissions
                       pnas.org/author-center/publication-ethics-process
                       pnas.org/post/update/pnas-policy-for-chatgpt-generative-ai
                       pnascentral.org
```

**Open the desk**: [submitting your manuscript](https://www.pnas.org/author-center/submitting-your-manuscript) · [editorial and journal policies](https://www.pnas.org/author-center/editorial-and-journal-policies) · [publication charges](https://www.pnas.org/author-center/publication-charges) · [member contributed submissions](https://www.pnas.org/author-center/member-contributed-submissions) · [publication ethics process](https://www.pnas.org/author-center/publication-ethics-process) · [the ChatGPT and generative-AI policy](https://www.pnas.org/post/update/pnas-policy-for-chatgpt-generative-ai) · [PNAS Central, the portal](https://www.pnascentral.org/).
A row inside a figure is plain text by design, because the renderer runs the figure linker over a fence and never the inline markdown pass, so the same links are repeated here as real ones.

## Content

### 1 · The gate has a section and the section has no gate

**Two files, one requirement, no link**: the split is the outlet's only real defect.

```text
  🚪 playbook-pnas/taste.md
     "PNAS requires one; if you can't write it, the paper
      isn't ready"
     ── a READINESS test, usable before the paper exists

  📐 playbook-pnas/pnas/pnas-significance/style.md
     word budget · arc · signature moves
     ── a DRAFTING guide, usable once it does

  💥 a writer at the drafting guide never meets the readiness
     test, and a reader of the taste file never sees the
     section norms
```

🚪 Establishes the split as the outlet's own defect, distinct from the placement split the group intro records.

#### 1.1 · The readiness test is the only venue bar in this tree a bare topic can take
(so losing it inside a family-level file costs more than tidiness)
This test needs a sentence rather than a study.
> ✎ This test needs a sentence rather than a ~study, which~ *study. That* makes it the one venue bar in this tree ~usable on~ the venue ~stage's~ *stage can run on its* `--no-pin` path, against a bare topic with no paper folder. · CC · 260802 1543
That makes it the one venue bar in this tree the venue stage can run on its `--no-pin` path, against a bare topic with no paper folder.
Every other desk's signals need a design or a result before they can be scored.

### 2 · What the ceiling removes

**Six pages decides the claim count**: a retarget into PNAS is subtraction.

```text
  📏 ~6 pages · ~50,000 characters
     ❌ "long, discursive papers that could be cut by half"

  ➖ what comes OUT
     claims ── a ledger sized for MISQ does not fit
     floats ── a display set sized for Nature Medicine
               does not fit
     methods ── detail moves toward the supplement

  🔀 the opposite direction from the rest of this group
     UTD-IS   ▶ ADDS a theory section
     Nature   ▶ ADDS a related-work section
     PNAS     ▶ REMOVES
```

➖ Establishes PNAS as the tree's only subtractive retarget, so its cost lands on the claim ledger rather than on prose.
> ✎ ➖ Establishes PNAS as the tree's only subtractive retarget, ~which is why~ *so* its cost lands on the claim ledger rather than on prose. · CC · 260802 1543

### 3 · Sec-0-Significance: the gate you pass before the section you write

**One block, two jobs**: `taste.md` uses it to decide whether the paper should exist, and `pnas-significance/style.md` uses it to decide how the paragraph runs.

```text
  🚦 ROLE 1 · READINESS GATE      [playbook-pnas/taste.md]
     the test    "Would a scientist in a completely different
                  field read the Significance Statement and
                  think 'I need to know this'?"
     the ruling  a missing one is a desk-reject signal: "PNAS
                  requires one; if you can't write it, the
                  paper isn't ready"

  📐 ROLE 2 · DRAFTED SECTION     [pnas-significance/style.md]
     cap        <=120 words, MANDATORY, a submission requirement
     measured   112w guzikevits-2024 · 116w rathje-2024 ·
                120w mei-2024         [style.md "Word budget"]
     floor      budget 110-120; a 60-word one wastes the slot
     shape      1 paragraph · 6-7 sentences, median 7
     sentence   8-33 words, median 17  [style.md "Micro-norms"]
     citations  0 across all three exemplars

  🧩 FOUR SLOTS INSIDE THE ONE PARAGRAPH
                              [style.md "Paragraph structure"]
     1  domain stakes in lay terms           1-2 sent
     2  what this paper does                 1 sent
     3  headline finding, declarative        1-3 sent
     4  implication beyond the specialty     1 sent

  🔗 WHEN IT IS DRAFTED           [README.md "-> Claims"]
     after   the claim-evidence map is stable
     before  the Abstract, which inherits its framing
     drives  the Abstract framing, the intro advance paragraph,
             and the first Discussion implication

  🔡 SLOT PATTERNS, not sentences to copy
                              [style.md "Signature moves" 1-4]
     open   "<domain activity> must be provided <norm> and <norm>."
     pivot  "Here, we <plain verb> <object>." /
            "We develop a <method> to assess <target>."
     find   "We present robust evidence showing that <finding>."
     close  "The findings underscore the critical need to <act>
            to ensure <goal> for all."

  ❌ ANTI-PATTERNS                [style.md "Anti-patterns"]
     over 120 words · far under ~110 · any citation · any
     statistic, effect size or acronym a lay scientist misses
     (VAS, F1, API) · the Abstract's order or sentences ·
     "may potentially contribute to..." · opening on your method
     or on your field's internal literature gap
```

🚦 Establishes the Significance Statement as one artifact doing two jobs, a test a bare topic can already fail and a paragraph carrying the tightest measured budget in the pack.

#### 3.1 · The ceiling this gate sits under
(so a writer who passes the test still has to fit the paper inside it)
`playbook-pnas/taste.md` puts the article budget at about 6 pages, roughly 50,000 characters, and lists "long, discursive papers that could be cut by half" among its desk-reject signals.
Adding the maximum of every `Word budget` line across the six `pnas-<kind>/style.md` files gives about 6,970 words, before references and captions.
> ✎ Adding the maximum of every `Word budget` line across the six `pnas-<kind>/style.md` files gives about 6,970 ~words~ *words,* before references and ~captions, so~ *captions. So* those six ranges are one shared ceiling to spend ~against rather than~ *against, not* six independent allowances. · CC · 260802 1543
So those six ranges are one shared ceiling to spend against, not six independent allowances.
Division 2 records what a retarget spends to buy that room: claims, floats, and methods detail, in that order.

#### 3.2 · Format values
(the gate's paragraph carries the tightest budget in the pack, and the gate itself carries none)

```text
  📏 WORDS            <=120 hard cap, budget 110-120 · 1 ¶ ·
                      6-7 sentences (median 7) · 8-33 words per
                      sentence (median 17)
                      [pnas-significance/style.md "Word budget",
                      "Micro-norms"]
                      120 is 1.7% of the 6,970-word six-section sum
                      recorded at 3.1 · running total 120 / 6,970
                      THE GATE ITSELF HAS NO LENGTH: the readiness
                      test scores a topic that has no draft yet
                      [playbook-pnas/taste.md "The one-sentence test"]
  📚 CITATION DENSITY 0.0 markers per sentence, zero citations across
                      all three exemplars
                      [pnas-significance/style.md "Micro-norms"]
  🔢 VALUE DENSITY    not recorded by the pack
                      [no style.md in this venue tree records numeric
                      values per sentence]
  📊 DISPLAYS         none: "A Significance Statement has NO figure,
                      table, or citation to file"
                      [pnas-significance/template.md:28]
```

#### 3.3 · The language, in the papers' own words
(five moves the significance style.md attributes by name, one per slot of the four-slot paragraph)

"Pain treatment must be provided adequately and impartially." [Guzikevits 2024]
The universal-stakes opening, and the shortest sentence the pack records anywhere: 8 words, no jargon, no citation, filling slot 1 on this division's figure.

"However, existing text analysis methods have a number of shortcomings." [Rathje 2024]
The gap in one lay sentence, and the way slot 1 reaches slot 2 without naming a literature.
> ✎ The gap in one lay sentence, ~which is how~ *and the way* slot 1 reaches slot 2 without naming a literature. · CC · 260802 1543

"We develop a Turing test to assess the behavioral and personality traits exhibited by AI." [Mei 2024]
The pivot, slot 2, in exactly the plain-verb form the figure carries as "We develop a <method> to assess <target>."

"Notably, female patients are less likely than males to be prescribed pain-relief medications for the same complaints." [Guzikevits 2024]
The finding, slot 3, declarative and carrying no statistic: this is the sentence a scientist in a completely different field is meant to read and want.

"The findings underscore the critical need to address psychological biases in healthcare settings to ensure fair and efficient treatment for all." [Guzikevits 2024]
The policy close, slot 4, and the source of the figure's "The findings underscore the critical need to <act> to ensure <goal> for all."

### 4 · Sec-1-Abstract: the second read, and it may not echo the first

**Same topic, forbidden sentences**: the desk reads the Significance Statement first, so the Abstract has to say the same thing without repeating it.

```text
  📄 BUDGET                       [pnas-abstract/style.md]
     cap        <=250 words, hard cap
     measured   154w mei-2024 · 237w guzikevits-2024 ·
                240w rathje-2024      [style.md "Word budget"]
     shape      1 unstructured paragraph, no labelled fields
     sentences  6-11, median 9        [style.md "Micro-norms"]
     sentence   8-43 words, median 24
     citations  0 · numbers 2-6 lay-legible anchors (N, %, r)

  🧩 SIX SLOTS IN ONE PARAGRAPH
                              [style.md "Paragraph structure"]
     1  broad framing OR a blunt "We do X"     1-2 sent
     2  question or hypothesis, plain terms    1 sent
     3  data, scale, design, N in parentheses  1-2 sent
     4  findings, headline first + robustness  2-4 sent
     5  convergent evidence, multi-study only  1-2 sent
     6  interpretive close with a stance       1-2 sent

  🔡 SLOT PATTERNS, not sentences to copy
                              [style.md "Signature moves" 1-6]
     open-broad  "In the pursuit of <goal>, <activity> stands
                 as a cornerstone."
     open-blunt  "We administer a <test> to <system>."
     hypothesis  "Leveraging insights from <prior finding>, we
                 hypothesize that <relation>."
     scale       "Our investigation spans <sources>, including
                 <unit> (N = <n>)."
     robustness  "<result>; this <effect> persists even after
                 adjusting for <controls>."
     close       "We argue that the findings reflect
                 <interpretation>."

  ❌ ANTI-PATTERNS                [style.md "Anti-patterns"]
     labelled Background/Methods/Results fields · citations ·
     the finding buried behind a methods recital · the
     Significance Statement's sentences or order · stacked
     specialist metrics · "implications are discussed" with no
     implication named
```

📄 Establishes the Abstract as the Significance Statement's non-parallel twin, inheriting its framing and barred from its wording.

#### 4.1 · The register these two front blocks set for everything after them
(because the family style file states it once, for the whole manuscript, and no section file repeats it)
`playbook-pnas/style-profile.md` puts four rules under "Sentences": write declarative and significance-forward, one idea per sentence, define a cross-field term at first use, and stack no buzzwords.
> ✎ `playbook-pnas/style-profile.md` puts four rules under "Sentences": *write* declarative and significance-forward, *keep* one idea per sentence, *define* a term ~that crosses a disciplinary boundary defined~ at first ~use,~ *use when it crosses in from another field,* and *stack* no ~buzzword stacks.~ *buzzwords.* · CC · 260802 1543
> ✎ `playbook-pnas/style-profile.md` puts four rules under "Sentences": write declarative and significance-forward, ~keep~ one idea per sentence, define a *cross-field* term at first ~use when it crosses in from another field,~ *use,* and stack no buzzwords. · CC · 260802 1548
Its "Contribution framing" block rules that a method novel elsewhere is an enabler in Methods here, not the headline.
> ✎ Its "Contribution framing" block rules that a method novel elsewhere is an enabler in Methods ~rather than~ *here, not* the ~headline, which~ *headline.* `playbook-pnas/README.md` repeats *that* in its "-> Claims" ~map~ *map,* as the reason PNAS admits exactly one `[primary]` claim plus 2 to 4 supporting ones. · CC · 260802 1543
`playbook-pnas/README.md` repeats that in its "-> Claims" map, as the reason PNAS admits exactly one `[primary]` claim plus 2 to 4 supporting ones.
Its "Tone & preferences" block adds the reporting furniture: the method executed by its own standards, explicit data and code availability, and domain reporting standards such as CONSORT where they apply.

#### 4.2 · Format values
(the one section where the pack comes close to a value density and still stops short of one)

```text
  📏 WORDS            <=250 hard cap · 1 unstructured ¶ · 6-11
                      sentences (median 9) · 8-43 words per sentence
                      (median 24)   [pnas-abstract/style.md "Word
                      budget", "Micro-norms"]
                      250 is 3.6% of the 6,970-word six-section sum ·
                      running total 370 / 6,970
  📚 CITATION DENSITY 0.0 markers per sentence, zero citations across
                      all three exemplars
                      [pnas-abstract/style.md "Micro-norms"]
  🔢 VALUE DENSITY    not recorded by the pack. The nearest record is
                      a PER-SECTION count, 2-6 lay-legible anchors
                      (N, %, r) per abstract, and a count per section
                      is not a density per sentence
                      [pnas-abstract/style.md "Micro-norms"]
  📊 DISPLAYS         none: "A PNAS abstract has NO figure or table to
                      file"   [pnas-abstract/template.md:30]
```

#### 4.3 · The language, in the papers' own words
(five attributed moves, including the two openings the pack rules equally legal)

"In the pursuit of mental and physical health, effective pain management stands as a cornerstone." [Guzikevits 2024]
The broad-stakes opening, slot 1 on this division's figure, used when the domain still needs motivating.

"We administer a Turing test to AI chatbots." [Mei 2024]
The blunt opening, the same slot 1 done in 8 words; the pack calls both exemplar-attested and tells the writer to choose by how much motivating the domain needs.

"Our investigation spans emergency department (ED) datasets from two countries, including discharge notes of patients arriving with pain complaints (N = 21,851)." [Guzikevits 2024]
The scale anchor, slot 3, which puts N in parentheses inside the design sentence instead of opening a methods recital.

"Across these datasets, a consistent sex disparity emerges." [Guzikevits 2024]
The headline finding, slot 4, stated before any texture or robustness clause reaches it.

"We argue that GPT and other LLMs help democratize automated text analysis..." [Rathje 2024]
The interpretive close, slot 6, and the sentence most at risk of repeating the Significance Statement's own close.

### 5 · Sec-2-Introduction: unlabelled, question-shaped, and where every citation lives

**The section with no heading**: PNAS prints the introduction without a label, so its first three words carry the whole entrance.

```text
  🪝 BUDGET                       [pnas-introduction/style.md]
     range      ~600-1,200 words     [style.md "Word budget"]
     measured   640w / 4 ¶ guzikevits-2024 · ~1,100w / 7 ¶
                rathje-2024 plus a labelled ~350w "Overview"
                bridge · ~1,200w / 8 ¶ mei-2024
     heading    none: the text starts after the abstract
     sentences  6-10 per ¶, median 7  [style.md "Micro-norms"]
     sentence   3-45 words, median 23; the 3-word floor is the
                cold open, theory sentences run 25-40
     citations  ~0.65 markers/sentence, the peak of the paper;
                densest ¶ 10 markers in 7 sentences (rathje-P5)
     refs       31 mei · 52 guzikevits · 87 rathje, median ~50

  🧩 ARC                [style.md "Paragraph structure"]
     P1   universal hook plus an immediate scale fact
     P2   theory or mechanism from prior work, citation-dense
     P3   the question posed as a question, then inconclusive
          prior evidence
     P4   "The main goal of the present work" plus a design
          preview
     P5+  optional findings preview or Overview bridge

  🔀 THREE HOUSE-LEGAL VARIANTS, and the pick sets the ¶ count
                          [template.md "Structure overview"]
     PSYCHOLOGY  ~4 ¶, straight to Results     [guzikevits-2024]
     ECONOMICS   ~8 ¶, closes on 3-4 findings-preview ¶
                                               [mei-2024]
     OVERVIEW    ~7 ¶ plus a labelled "Overview" subsection,
                 the one place a PNAS intro carries a heading
                                               [rathje-2024]

  🔡 SLOT PATTERNS, not sentences to copy
                          [style.md "Signature moves" 1-5]
     cold open  "<Phenomenon> is ubiquitous." then a scale fact
                carrying its citation
     question   "Do <subjects> receive less <treatment> than
                <comparison>?"
     prior      "The few studies that tested this question have
                failed to <converge>."
     pivot      "The main goal of the present work is to <act>."
     theory     "...spanning <domain a> (12), <domain b> (13),
                and <domain c> (14, 15)."

  ❌ ANTI-PATTERNS            [style.md "Anti-patterns"]
     opening on the method or the model · a field-internal gap
     ("<field> research has not examined...") · a full
     literature review · the contribution deferred past ¶4-6 ·
     an introduction over ~25% of main text
```

🪝 Establishes the introduction as the paper's only citation-dense section and the one whose entrance is a phenomenon rather than a literature.

#### 5.1 · Format values
(the citation peak of the paper, and the one section the pack also caps as a percentage)

```text
  📏 WORDS            ~600-1,200 · 4-8 ¶ · 6-10 sentences per ¶
                      (median 7) · 3-45 words per sentence (median
                      23)   [pnas-introduction/style.md "Word
                      budget", "Micro-norms"]
                      1,200 is 17.2% of the 6,970-word six-section
                      sum · running total 1,570 / 6,970
                      inside its own second cap: "Do NOT let the
                      intro exceed ~25% of main text"
                      [pnas-introduction/style.md "Anti-patterns"]
  📚 CITATION DENSITY ~0.65 markers per sentence, 34 across 52 sampled
                      sentences, the peak of the paper; the densest
                      single ¶ carries 10 markers in 7 sentences
                      (rathje-2024 P5)
                      [pnas-introduction/style.md "Micro-norms"]
  🔢 VALUE DENSITY    not recorded by the pack
                      [no style.md in this venue tree records numeric
                      values per sentence]
  📊 DISPLAYS         none across the three exemplars; a schematic is
                      filed as a display request and rathje-2024's
                      "Overview" bridge is prose, not a float, so no
                      share of the ~6 main figures is reserved here
                      [pnas-introduction/template.md:34]
```

#### 5.2 · The language, in the papers' own words
(the cold open the pack records twice and cannot record consistently, plus three more attributed moves)

"Pain is ubiquitous." [Guzikevits 2024]
The cold open at its shortest, 3 words, and the anchor of the figure's "<Phenomenon> is ubiquitous." slot pattern.

"As Alan Turing foresaw to be inevitable, modern AI has reached the point of emulating humans: holding conversations, providing advice, writing poems, and proving theorems." [Mei 2024]
The same slot at 25 words, filed under the same "Cold open" heading of the same file.
Signature move 1 calls this move a "Two-to-four-word cold open", while the file's own "Exemplar sentences" list attests a 25-word one.
> ✎ Signature move 1 calls this move a "Two-to-four-word cold ~open"~ *open",* while the file's own "Exemplar sentences" list attests a 25-word ~one, so~ *one. So* the numeric claim and the exemplar set conflict inside *one file,* `pnas-introduction/style.md`. · CC · 260802 1543
So the numeric claim and the exemplar set conflict inside one file, `pnas-introduction/style.md`.

"Do female patients receive less pain treatment than males for similar complaints?" [Guzikevits 2024]
The research question posed as a literal question, the figure's `question` slot, and the move that keeps a PNAS intro off a field-internal gap sentence.

"The few studies that tested this question have failed to provide a consistent conclusion." [Guzikevits 2024]
The inconclusive-prior-evidence move, the figure's `prior` slot: prior work enters as an unsettled record rather than as a review.

"The main goal of the present work is to conduct a rigorous examination of pain management decisions by patients' sex." [Guzikevits 2024]
The contribution pivot, the figure's `pivot` slot, landed in paragraph 4 of 4 in the psychology variant.

### 6 · Sec-3-Results: the largest section, and every claim arrives fully armed

**Finding, slice, control, replicate**: each subsection escalates the same claim's robustness instead of starting a new topic.

```text
  📊 BUDGET                       [pnas-results/style.md]
     range      ~1,300-2,600 words, the largest main-text
                section              [style.md "Word budget"]
     measured   ~1,300w guzikevits-2024 · ~2,500w mei-2024 ·
                ~2,600w rathje-2024
     order      Results before Discussion, Methods usually at
                the end, so Results carries its own design
                context
     paragraphs ~9-20 across 3-7 named subsections
                                     [style.md "Micro-norms"]
     sentences  5-10 per ¶, median 6
     sentence   6-81 words, median 22; the 81-word ceiling is
                one real sentence carrying three bracketed
                stat blocks
     citations  ~0.08 markers/sentence, instruments only
     callouts   1-5 figure or table callouts per paragraph
     floats     up to ~6 main figures for a Research Article,
                each claim to one display, the [primary] claim
                to the hero      [README.md "-> Display"]

  🧩 ARC, per subsection  [style.md "Paragraph structure"]
     P1  purpose sentence plus a dataset one-liner (N, source)
     P2  primary outcome, fully loaded headline stat
     P3  subgroup or per-level slices, figure callouts
     P4  multivariate model walk, control escalation
     P5  interaction and concordance tests, precise nulls
     P6  robustness reruns, hand-off to SI Appendix

  🔀 THREE SUBSECTION SCHEMES
                          [template.md "Structure overview"]
     PER-STUDY      "Study 1. / Study 2.", 3 subs ~9 ¶
                                            [guzikevits-2024]
     PER-CONSTRUCT  headed by construct, 7 subs ~15 ¶
                                            [rathje-2024]
     LETTERED       "A. / B." plus numbered sub-subsections,
                    6 subs ~20 ¶            [mei-2024]

  🔡 SLOT PATTERNS, not sentences to copy
                          [style.md "Signature moves" 1-7]
     opener  "Study 1 tested our hypothesis that <subjects>
             receive less <treatment> than <comparison>."
     stat    "<outcome> was lower for <group A> than <group B>
             [<pct> vs. <pct>, <test>(<df>, n = <n>) = <value>,
             P < <p>, <effect> = <value>]."
     sweep   "This <disparity> was observed in <all strata>
             (Fig. 1A), for <each level> (Fig. 1B) and among
             <both rater types> (Fig. 1C)."
     walk    "The <effect> persisted after adding controls for
             <set> (b = <b>, SE = <se>, P = <p>) (Table 1,
             Model 2)."
     echo    "As in Study 1, <subjects> were less likely to
             <outcome>."
     hand-off "A similar pattern was observed (SI Appendix,
             Table S2)."

  ❌ ANTI-PATTERNS            [style.md "Anti-patterns"]
     an inferential claim without test, N, P and effect size ·
     a generic heading ("Main Results") · methods exposition
     beyond one design sentence · nulls hidden or pushed to SI
     when they bear on the claim · literature cited for
     anything but instruments · a subsection ending on a number
```

📊 Establishes Results as the section that must carry its own design context, because Materials and Methods is printed after it.

#### 6.1 · Format values
(the largest claim on the shared ceiling, and the only section the main-figure budget lands on)

```text
  📏 WORDS            ~1,300-2,600, the largest main-text section ·
                      ~9-20 ¶ across 3-7 subsections · 5-10 sentences
                      per ¶ (median 6) · 6-81 words per sentence
                      (median 22)   [pnas-results/style.md "Word
                      budget", "Micro-norms"]
                      2,600 is 37.3% of the 6,970-word six-section
                      sum, the largest single claim on it · running
                      total 4,170 / 6,970
  📚 CITATION DENSITY ~0.08 markers per sentence, 3 across 40 sampled
                      sentences, instruments and benchmarks only
                      [pnas-results/style.md "Micro-norms"]; the same
                      file's "Anti-patterns" line writes the same
                      figure as ~0.1, so the section rounds itself
                      two ways
  🔢 VALUE DENSITY    not recorded by the pack. The pack states the
                      requirement PER CLAIM instead: no primary
                      inferential claim without test statistic, N,
                      P-value and effect size inline
                      [pnas-results/style.md "Anti-patterns"]
  📊 DISPLAYS         the whole main-figure budget lands here, "up to
                      ~6 main figures" for a Research Article, each
                      claim to one display and the [primary] claim to
                      the hero   [playbook-pnas/README.md
                      "-> Display"], plus Table 1 Models 1-4 and the
                      SI Appendix tables · 1-5 callouts per ¶
                      [pnas-results/style.md "Micro-norms"]; how the
                      ~6 divide across figures is not recorded by the
                      pack
```

#### 6.2 · The language, in the papers' own words
(five attributed moves, one per rung of the finding, slice, control, replicate escalation)

"Study 1 tested our hypothesis that female patients receive less pain treatment than male patients." [Guzikevits 2024]
The purpose-first subsection opener, the figure's `opener` slot, and the one design sentence a subsection is allowed to spend.

"This sex disparity was observed in all age groups (Fig. 1A), for each pain score (from 0 to 10; Fig. 1B)..." [Guzikevits 2024]
The consistency sweep, the figure's `sweep` slot: one sentence asserts the pattern everywhere and hands the detail to the panels.

"The interaction between patient sex and physician sex was not a significant predictor..." [Guzikevits 2024]
The precise null, carried with the same stat block as a positive result rather than dismissed with an adjective.

"A similar pattern of sex disparity was observed (SI Appendix, Table S2)." [Guzikevits 2024]
The hand-off, the figure's `hand-off` slot, and the pointer convention that division 9 records as the SI Appendix's only written rule.

"Overall, GPT appears to be effective at multilingual sentiment analysis, with performance comparable to top-performing machine learning models from several years ago." [Rathje 2024]
The one-sentence interpretive summary that closes a subsection, and the reason the anti-pattern list forbids ending one on a number.
> ✎ The *one-sentence* interpretive ~micro-summary~ *summary* that closes a subsection, ~which is why~ *and the reason* the anti-pattern list forbids ending one on a number. · CC · 260802 1543

### 7 · Sec-4-Discussion: it opens above the findings and closes higher still

**Altitude, not summary**: the first paragraph re-enters the finding at societal or historical height, and the last one leaves it higher.

```text
  🏔 BUDGET                       [pnas-discussion/style.md]
     range      ~700-1,400 words     [style.md "Word budget"]
     measured   ~700w / 4 ¶ mei-2024 · ~1,350w / 7 ¶
                guzikevits-2024 · ~1,300w / ~12 ¶ rathje-2024
                plus a separate ~120w "Conclusions" heading
     headings   none inside the Discussion, all three exemplars
     sentences  4-9 per ¶, median 5   [style.md "Micro-norms"]
     sentence   10-50 words, median 25, longer than Results
                because the sentences carry argument, not stats
     citations  ~0.2 markers/sentence, back above Results and
                far below the introduction's ~0.65
     close      the shortest paragraph of the paper: 4
                sentences, ~73 words     [guzikevits-2024]

  🧩 ARC                  [style.md "Paragraph structure"]
     P1  elevated restatement of the advance
     P2  defend the interpretation: the skeptic's question,
         posed literally and answered
     P3  mechanism, theory-linked and honestly bounded
     P4  reconcile conflicting literature through a proposed
         moderator
     P5  practical implications: who should act
     P6  limitations, one late paragraph, each with a redirect
     P7  "To conclude": advance, mechanism, broad significance

  🔀 THREE LAYOUTS        [template.md "Structure overview"]
     FULL-7        one role per paragraph   [guzikevits-2024]
     COMPRESSED-4  merge P2-P4 and P5-P7    [mei-2024]
     SPLIT-12      more, shorter ¶ plus a "Conclusions" anchor
                                            [rathje-2024]

  🔡 SLOT PATTERNS, not sentences to copy
                          [style.md "Signature moves" 1-7]
     restate   "The present work reveals a systematic
               <advance>: <restated in words, no stat blocks>."
     skeptic   "Does <observed pattern> constitute <the strong
               reading>?"
     bound     "We note that our data did not allow us to tie
               <x> to <y> within the same study."
     moderator "We speculate that a previously overlooked
               factor may explain <the conflict>."
     limit     "In terms of limitations, given that <scope>,
               it is important to <redirect>."
     close     "To conclude, the present research provides
               <evidence> for <advance>."

  ❌ ANTI-PATTERNS            [style.md "Anti-patterns"]
     a number-by-number Results recap · dodging the obvious
     objection · limitations scattered instead of concentrated
     · new DATA introduced here, though a new moderator
     hypothesis is exemplar-attested and allowed · ending on
     limitations · a mechanism the design cannot support
```

🏔 Establishes the Discussion as an argument section rather than a summary, with its one honest limitations paragraph placed late and never last.

#### 7.1 · Format values
(an argument section priced like a second introduction, and display-free while it costs that much)

```text
  📏 WORDS            ~700-1,400 · 4-12 ¶ · 4-9 sentences per ¶
                      (median 5) · 10-50 words per sentence (median
                      25)   [pnas-discussion/style.md "Word budget",
                      "Micro-norms"]
                      1,400 is 20.1% of the 6,970-word six-section
                      sum · running total 5,570 / 6,970
                      the close is the shortest ¶ of the paper: 4
                      sentences, ~73 words   [guzikevits-2024]
  📚 CITATION DENSITY ~0.2 markers per sentence, 7 across 34 sampled
                      sentences, back above Results and far below the
                      introduction's ~0.65
                      [pnas-discussion/style.md "Micro-norms"]
  🔢 VALUE DENSITY    not recorded by the pack
                      [no style.md in this venue tree records numeric
                      values per sentence]
  📊 DISPLAYS         none: "A PNAS Discussion is DISPLAY-FREE across
                      all three exemplars"
                      [pnas-discussion/template.md:36]
```

#### 7.2 · The language, in the papers' own words
(six attributed moves up the altitude arc, ending on the close and not on the limitation)

"The present work reveals a systematic sex-related disparity in pain management..." [Guzikevits 2024]
The elevated restatement, the figure's `restate` slot, arriving only after a paragraph that opened on the 2010 Declaration of Montreal rather than on the result.

"Does the fact that female patients receive less analgesics than males constitute a bias?" [Guzikevits 2024]
The skeptic's question, the figure's `skeptic` slot, posed literally and then answered with enumerated evidence.

"We note that our data did not allow us to tie biased pain management decisions to stereotypical pain judgments within the same study." [Guzikevits 2024]
The honesty clause bounding the mechanism, the figure's `bound` slot, and how a mechanism paragraph stays inside what the design can support.

"We speculate that a previously overlooked factor may explain the presence or absence of a sex bias in these studies." [Guzikevits 2024]
The conflict reconciliation, the figure's `moderator` slot, and the one place the anti-pattern list admits a brand-new hypothesis.

"In terms of limitations, given that our human data are collected from students, it is important to expand the reference population..." [Mei 2024]
The limitation, the figure's `limit` slot, marked explicitly, concentrated in one late paragraph and paired with its redirect.

"To conclude, the present research provides robust evidence for healthcare providers' sex bias against female patients in pain management..." [Guzikevits 2024]
The close, the figure's `close` slot, and the reason the limitation above it can never be the last paragraph.

### 8 · Sec-5-Methods: Materials and Methods, printed last, and half of it lives somewhere else

**The SI split is the section**: the main text keeps only what a reader needs to trust the headline analyses, and names by hand every item it hands off.

```text
  🔬 BUDGET                       [pnas-methods/style.md]
     range      ~600-1,400 words of MAIN-TEXT methods
                                     [style.md "Word budget"]
     measured   ~600w mei-2024 · ~700w guzikevits-2024 ·
                ~1,400w rathje-2024
     position   usually LAST, after the Discussion; a short
                numbered Methods before Results is also
                house-legal            [mei-2024]
     blocks     ~4-15 bolded run-in sub-blocks: ~8 guzikevits ·
                ~4 mei · ~15 rathje  [style.md "Micro-norms"]
     sentences  5-15 per block, median 10, the longest
                paragraphs in the paper
     sentence   6-54 words, median 16, the shortest sentences
                in the paper
     citations  ~0.04 markers/sentence: instruments, source
                datasets, deposited data
     SI rate    about one SI pointer per block; guzikevits'
                ~700w Methods makes 4 SI references and its
                Results 7 more

  🧩 ARC, bolded run-in sub-blocks and never prose flow
                                        [style.md "Arc"]
     Data collection.       source, years, N, criteria,
                            variables, IRB
     Statistical analysis.  test-by-test walk in Results order,
                            alpha, software versions
     Study population. / Study plan.   recruitment, n,
                            preregistration URL
     Data, Materials, and Software Availability.
                            repository and accession

  🔡 SLOT PATTERNS, not sentences to copy
                          [style.md "Signature moves" 1-7]
     criteria   "we obtained <records> that fulfilled the
                following prespecified inclusion criteria:
                <a>; <b>; <c>."
     variables  "The data included <family>: <a>, <b>, <c>
                (SI Appendix, Table S1A)."
     walk       "In the first step, the only explanatory
                variable was <x>. In the second step, <set>."
     IRB        "The study was approved by the <institution>
                IRB committee (Protocol no. <id>)."
     exclusion  "We also excluded <case> because <reason>."
     availability "Anonymized <data> have been deposited in
                <repository URL>."

  ❌ ANTI-PATTERNS            [style.md "Anti-patterns"]
     results or effect sizes reported here · variable
     dictionaries, prompt texts or robustness grids dumped in
     the main text · an SI item nobody points at · a missing
     IRB, preregistration, software version or availability
     statement · flowing narrative instead of run-in blocks ·
     exclusions listed without reasons
```

🔬 Establishes Methods as the section whose real size is set by what it exports to the SI Appendix rather than by what it prints.

#### 8.1 · Format values
(the row that closes the running total, and shows the ceiling already over-subscribed)

```text
  📏 WORDS            ~600-1,400 of MAIN-TEXT methods · ~4-15 bolded
                      run-in blocks · 5-15 sentences per block
                      (median 10) · 6-54 words per sentence (median
                      16)   [pnas-methods/style.md "Word budget",
                      "Micro-norms"]
                      1,400 is 20.1% of the 6,970-word six-section
                      sum · running total 6,970 / 6,970, which CLOSES
                      the sum
                      the only whole-article ceiling the pack states
                      is ~6 pages, about 50,000 CHARACTERS
                      [playbook-pnas/taste.md and README.md]; no file
                      converts words into characters, and no file
                      performs the sum at all, so the six ranges are
                      spent as six independent allowances and the
                      ceiling is over-subscribed before references,
                      captions and the reference list are counted
  📚 CITATION DENSITY ~0.04 markers per sentence, 2 across 56 sampled
                      sentences, the floor of the paper
                      [pnas-methods/style.md "Micro-norms"]
  🔢 VALUE DENSITY    not recorded by the pack
                      [no style.md in this venue tree records numeric
                      values per sentence]
  📊 DISPLAYS         no main-text figure or table in any of the three
                      exemplars; the exports (variable dictionaries
                      Tables S1A and S1B, further analysis tables S2
                      to S5) sit in the SI Appendix, outside the ~6
                      main-figure budget · about one SI pointer per
                      block   [pnas-methods/style.md "Word budget",
                      "Micro-norms"]
```

#### 8.2 · The language, in the papers' own words
(six attributed moves across the arc's four blocks, two of them the compliance furniture)

"Consequently, we obtained discharge notes that fulfilled the following prespecified inclusion criteria:" [Guzikevits 2024]
The criteria move, the figure's `criteria` slot, written as one semicolon-chained load-bearing sentence rather than as a list.

"The data included personal characteristics of the patient: sex, age group, ethnicity, pregnancy status... (SI Appendix, Table S1A)." [Guzikevits 2024]
The variable inventory, the figure's `variables` slot, naming the family in the main text and pushing the dictionary to the SI Appendix.

"We used a temperature of 0 to obtain the highest probability predictions of the models." [Rathje 2024]
The procedural declarative that gives this section the shortest median sentence in the paper.

"In all tests in this study and the next ones, we set an a priori two-sided alpha = 0.05." [Guzikevits 2024]
The statistical walk, the figure's `walk` slot, stating the decision rule before Results ever uses it.

"The study was approved by the Hadassah Medical Center IRB committee (Protocol no. 0563-20-HMO)." [Guzikevits 2024]
The IRB sentence, the figure's `IRB` slot, and the first of the four items the pack calls mandatory furniture.

"Anonymized patient data have been deposited in https://osf.io/heznx/ (52)." [Guzikevits 2024]
The availability statement, the figure's `availability` slot, and the last block of the paper.

### 9 · There is no appendix kind, and the SI Appendix is why

**Alone in the tree, and it is the bigger half**: `section-kinds.yml` gives PNAS six kinds and no appendix, while every other outlet in that file ends its list with one. `pnas-methods/style.md:14` calls the SI Appendix split "the defining constraint" of the Methods section, and on `guzikevits-2024` the main Methods runs about 700 words while the SI carries the variable dictionaries and five further analysis tables. So the unowned artifact is the larger one.

```text
  📐 stages/section-kinds.yml
     pnas:   [abstract, significance, introduction, methods,
              results, discussion]        # no appendix
     others  every remaining outlet in the file closes its
             list with `appendix`

  ➡️ WHERE THE MATERIAL GOES INSTEAD
     the target   "SI Appendix, section N / Table S_ / Fig. S_",
                  named from the main text, one pointer per item
     variable dictionaries   ▶ SI Appendix, Tables S1A / S1B
                               [guzikevits-2024, methods style.md]
     further analysis tables ▶ SI Appendix, Tables S2 to S5
                               [guzikevits-2024, methods style.md]
     robustness reruns       ▶ the Results P6 hand-off
                               [pnas-results/style.md]
     prompts, extra regressions, full variable tables
                             ▶ SI  [pnas-methods/style.md]

  📏 WHY IT LEAVES THE MAIN TEXT
     the JOURNAL: 6 pages preferred, 12 pages maximum, and a
       standard 6-page article is about 4,000 words, 50 refs
       and 4 medium graphical elements  [pnas.org, 260802]
     the PACK: ~6 pages · ~50,000 characters, and the
       character figure is sourced nowhere
     ❌ desk-reject signal: "long, discursive papers that
        could be cut by half"

  🕳 WHAT THE PACK DOES NOT GIVE   ── narrowed 260802
     no si style.md · no word budget · no arc ·
     no S-Main page
     the SI exists in the pack only as a POINTER convention
     inside pnas-methods/style.md and pnas-results/style.md

  ✅ WHAT THE JOURNAL DOES GIVE, and the pack does not carry
     an SI template in Word AND in official Overleaf LaTeX
     a composition rule ── ONE PDF combining text, figures,
       tables, movie legends and SI references
     a numbering rule ── S1, S2, ...
     a reference rule ── SI and main text are SEPARATE streams
     ── so "no template" and "no ordering rule" were WRONG
        on this page until 260802
```

📦 Establishes the SI Appendix as real, load-bearing and unowned, and as the section the pack itself calls the defining constraint.
> ✎ 📦 Establishes the SI Appendix as real, load-bearing and unowned, and as the section the pack itself calls the defining ~constraint: the~ *constraint. The* ceiling pushes ~the majority~ *most* of the Methods into ~it~ *it,* and no file in the pack says what shape it takes once it lands. · CC · 260802 1543
> ✎ 📦 Establishes the SI Appendix as real, load-bearing and unowned, and as the section the pack itself calls the defining constraint. The ceiling pushes most of the Methods into ~it,~ *the SI,* and no file in the pack says what shape it takes once it lands. · CC · 260802 1548
The ceiling pushes most of the Methods into the SI, and no file in the pack says what shape it takes once it lands.

#### 9.1 · What a writer does with no SI guide
(because the material still has to be written, and the pack stops at the pointer)
`pnas-methods/style.md` gives the SI its only two rules: every item is pointed to by name from the main text, and about one pointer belongs in each methods block.
`pnas-results/style.md` adds that guzikevits-2024 references the SI Appendix more than ten times in Results alone, seven of them in Study 1.
Neither file says how long an SI section runs, what order its sections take, or which of its tables need a display unit built.
> ✎ Neither file says how long an SI section runs, what order its sections take, or which of its tables need a display unit ~built, so~ *built. So* the SI is ~currently~ shaped by whatever the main text could not hold. · CC · 260802 1543
So the SI is shaped by whatever the main text could not hold.

#### 9.2 · What the journal itself says, fetched 260802
(because this division claims the SI is unowned, and half of that claim is about the pack rather than about PNAS)
The PNAS author center rules that "SI will be published as provided by the authors and will not be edited or typeset".
> ✎ The PNAS author center rules that "SI will be published as provided by the authors and will not be edited or ~typeset", so~ *typeset". So* the SI Appendix is the one part of a PNAS paper that reaches the reader in the author's own hand. · CC · 260802 1543
So the SI Appendix is the one part of a PNAS paper that reaches the reader in the author's own hand.
It arrives as a single artifact: "SI Appendix: Supply a single PDF, combining all text, figures, tables, movie legends, and SI references."
Three rules bound what may leave the main text, and the pack states none of them.
The first is absolute: "The main text of the paper must stand on its own without the SI."
The second governs the Methods split this division is named for.
> ✎ The second governs the Methods split this division is named ~for: a~ *for. A* writer who moves detailed materials and methods *out* "must provide sufficient detail in the main-text methods to enable a reader to follow the logic of the procedures and ~results", and~ *results". The same rule adds that* "The main article text also must reference the SI methods". · CC · 260802 1543
A writer who moves detailed materials and methods out "must provide sufficient detail in the main-text methods to enable a reader to follow the logic of the procedures and results".
The same rule adds that "The main article text also must reference the SI methods".
The third is a floor the split may not cross: "If a paper is fundamentally a study of a new method or technique, then the methods must be described completely in the main text."
Two conventions land underneath them.
Supporting figures and tables are numbered "starting with S1, S2, etc.", which is the form division 6 quotes from guzikevits-2024 without a source behind it.
SI references are their own stream, "cited in numerical order as they appear in the SI", and a writer may not "cite main-text references in the SI and vice versa".
One deadline closes the section: SI "cannot be altered by authors after acceptance", so the SI is finished at acceptance rather than at proof.
So this division's finding holds in half.
PNAS gives the SI no word budget and no arc.
> ✎ PNAS gives the SI no word budget and no ~arc, which~ *arc. That* is what leaves the hand-off ~unshaped~ *unshaped,* and *it* keeps A9.1 open. · CC · 260802 1543
So the hand-off has no shape, and A9.1 stays open.
> ✎ ~That is what leaves~ *So* the hand-off ~unshaped,~ *has no shape,* and ~it keeps~ A9.1 *stays* open. · CC · 260802 1548
It does give a composition rule, a numbering rule, a reference rule, a revision deadline, and an SI Appendix template in both Word and LaTeX, all listed under Files.
> ✎ It does give a composition rule, a numbering rule, a reference rule, a revision deadline, and an SI Appendix template in both Word and LaTeX, all listed under ~Files, so~ *Files. So* those four gaps are a transcription this pack has not ~done rather than~ *done, not* a rule nobody wrote. · CC · 260802 1543
So those four gaps are a transcription this pack has not done, not a rule nobody wrote.

## Aims

### A1 · 🚪 The gate has a section and the section has no gate
- A1.1 · `pnas-significance/style.md` and the family `taste.md` point at each other.
  **Done when:** a writer arriving at either file reaches the other.

### A2 · ➖ What the ceiling removes
- A2.1 · The subtraction is quantified before a retarget into PNAS is accepted.
  **Done when:** retargeting here names how many claims and floats have to come out.

### A3 · 🚦 Sec-0-Significance: the gate you pass before the section you write
- A3.1 · The 120-word cap is settled by a recount rather than by eye.
  **Done when:** a Significance Statement leaves the stage with its word count stated and inside the 110 to 120 band.

### A4 · 📄 Sec-1-Abstract: the second read, and it may not echo the first
- A4.1 · The Abstract and the Significance Statement are compared as a pair before submission.
  **Done when:** the comparison for shared sentences and shared order is recorded somewhere, not left for a reviewer to find.

### A5 · 🪝 Sec-2-Introduction: unlabelled, question-shaped, and where every citation lives
- A5.1 · The introduction variant is chosen before drafting, since it fixes the paragraph count.
  **Done when:** the paper names one of the three house-legal variants and its paragraph budget follows from that pick.

### A6 · 📊 Sec-3-Results: the largest section, and every claim arrives fully armed
- A6.1 · Every inferential claim carries its stat block, and every callout has a display unit behind it.
  **Done when:** no Results sentence states a primary claim without test, N, P and effect size, and every figure, table and SI pointer resolves.

### A7 · 🏔 Sec-4-Discussion: it opens above the findings and closes higher still
- A7.1 · Limitations sit in exactly one late paragraph and the section does not end there.
  **Done when:** the last paragraph is the significance close and every limitation carries a future-research redirect.

### A8 · 🔬 Sec-5-Methods: Materials and Methods, printed last, and half of it lives somewhere else
- A8.1 · Every exported item is named from the main text and the four compliance sentences are present.
  **Done when:** each SI item has a main-text pointer, and IRB or consent, preregistration, software versions and the availability statement all appear.

### A9 · 📦 There is no appendix kind, and the SI Appendix is why
- A9.1 · The SI Appendix has a written shape, so the material the ceiling removes has somewhere to land.
  **Done when:** the pack carries an SI guide, or this page records the ruling that the SI stays unspecified and names who owns that.

## States

### A1 · 🚪 The gate has a section and the section has no gate
- ⬜ A1.1 · Not started. Neither file references the other.

### A2 · ➖ What the ceiling removes
- ⬜ A2.1 · Not started. The `-> Claims` and `-> Display` maps carry the reason and no retarget reads them.

### A3 · 🚦 Sec-0-Significance: the gate you pass before the section you write
- ⬜ A3.1 · Not started. `pnas-significance/template.md` asks for a recount at draft and after revise, and nothing performs one.

### A4 · 📄 Sec-1-Abstract: the second read, and it may not echo the first
- ⬜ A4.1 · Not started. Both style files forbid parallelism and neither names who compares the two blocks.

### A5 · 🪝 Sec-2-Introduction: unlabelled, question-shaped, and where every citation lives
- ⬜ A5.1 · Not started. The three variants live in `pnas-introduction/template.md` and no stage records which one a paper picked.

### A6 · 📊 Sec-3-Results: the largest section, and every claim arrives fully armed
- ⬜ A6.1 · Not started. The display dependency is declared in `pnas-results/template.md` as display-request rows and is audited nowhere on this page.

### A7 · 🏔 Sec-4-Discussion: it opens above the findings and closes higher still
- ⬜ A7.1 · Not started. The ordering rule sits in the `pnas-discussion/style.md` anti-patterns list and nothing enforces it.

### A8 · 🔬 Sec-5-Methods: Materials and Methods, printed last, and half of it lives somewhere else
- ⬜ A8.1 · Not started. `pnas-methods/style.md` calls all four mandatory furniture and no check counts them.

### A9 · 📦 There is no appendix kind, and the SI Appendix is why
- ⬜ A9.1 · Not started. The pack holds no SI file of any kind.

## Files

- `../../paper/venue/playbook-pnas/taste.md` · the readiness test, at family level
- `../../paper/venue/playbook-pnas/pnas/pnas-significance/style.md` · the gate's section norms, at outlet level

<!-- exemplars:begin -->

📚 **Exemplars** · 34 papers on disk, regenerated by `_tools/sync-exemplars.py`

Filed at FAMILY level under `../../paper/venue/playbook-pnas/examples/`, not under the outlet (the group intro on the Index).

- `../../paper/venue/playbook-pnas/examples/EXEMPLARS.md`
- `../../paper/venue/playbook-pnas/examples/LLM-SILICON-SUBJECTS-LANDSCAPE.md`
- `../../paper/venue/playbook-pnas/examples/PNAS-STYLE-ANALYSIS.md`
- `../../paper/venue/playbook-pnas/examples/abdellaoui-2025-sexlessness-personality.pdf` · Abdellaoui 2025
- `../../paper/venue/playbook-pnas/examples/allen-2024-callousness-cooperation.pdf` · Allen 2024
- `../../paper/venue/playbook-pnas/examples/argyle-2025-ai-political-persuasion.pdf` · Argyle 2025
- `../../paper/venue/playbook-pnas/examples/ashton-2025-personality-birth-order.pdf` · Ashton 2025
- `../../paper/venue/playbook-pnas/examples/bagley-2026-racial-disparities-media.pdf` · Bagley 2026
- `../../paper/venue/playbook-pnas/examples/bail-2024-generative-ai-social-science.pdf` · Bail 2024
- `../../paper/venue/playbook-pnas/examples/bonetti-2025-soccer-psychological-profile.pdf` · Bonetti 2025
- `../../paper/venue/playbook-pnas/examples/cherep-2026-ai-agents-nudges.pdf` · Cherep 2026
- `../../paper/venue/playbook-pnas/examples/chiba-okabe-2026-trust-moral-hazard.pdf` · Chiba-Okabe 2026
- `../../paper/venue/playbook-pnas/examples/gabriel-2024-llm-sdoh-classifiers.pdf` · Gabriel 2024
- `../../paper/venue/playbook-pnas/examples/granulo-2026-ai-labor-democratic-legitimacy.pdf` · Granulo 2026
- `../../paper/venue/playbook-pnas/examples/guzikevits-2024-sex-bias-pain.pdf` · Guzikevits 2024
- `../../paper/venue/playbook-pnas/examples/hackenburg-2025-llm-persuasion.pdf` · Hackenburg 2025
- `../../paper/venue/playbook-pnas/examples/hannikainen-2024-medical-aid-dying.pdf` · Hannikainen 2024
- `../../paper/venue/playbook-pnas/examples/huang-2024-impulsivity-stable-trait.pdf` · Huang 2024
- `../../paper/venue/playbook-pnas/examples/jones-2026-llm-turing-test.pdf` · Jones 2026
- `../../paper/venue/playbook-pnas/examples/kuan-2025-behavioral-nudges-13m.pdf` · Kuan 2025
- `../../paper/venue/playbook-pnas/examples/laurito-2025-ai-ai-bias.pdf` · Laurito 2025
- `../../paper/venue/playbook-pnas/examples/loru-2025-simulation-judgment-llm.pdf` · Loru 2025
- `../../paper/venue/playbook-pnas/examples/ma-2025-llm-biomedical-challenges.pdf` · Ma 2025
- `../../paper/venue/playbook-pnas/examples/mei-2024-turing-test-chatbots.pdf` · Mei 2024
- `../../paper/venue/playbook-pnas/examples/pataranutaporn-2025-llm-wellbeing-simulation.pdf` · Pataranutaporn 2025
- `../../paper/venue/playbook-pnas/examples/peng-2024-promotional-language-science.pdf` · Peng 2024
- `../../paper/venue/playbook-pnas/examples/peter-2025-anthropomorphic-agents.pdf` · Peter 2025
- `../../paper/venue/playbook-pnas/examples/rathje-2024-gpt-psychological-text.pdf` · Rathje 2024
- `../../paper/venue/playbook-pnas/examples/smerdon-2025-discrimination-gig-economy.pdf` · Smerdon 2025
- `../../paper/venue/playbook-pnas/examples/stuhler-2024-gender-agency-fiction.pdf` · Stuhler 2024
- `../../paper/venue/playbook-pnas/examples/sultan-2024-misinformation-meta-analysis.pdf` · Sultan 2024
- `../../paper/venue/playbook-pnas/examples/vafa-2025-wage-disparities-foundation-models.pdf` · Vafa 2025
- `../../paper/venue/playbook-pnas/examples/xu-2024-teacher-personality-text.pdf` · Xu 2024
- `../../paper/venue/playbook-pnas/examples/zettler-2025-dark-personality-countries.pdf` · Zettler 2025

- `../../paper/venue/playbook-pnas/examples/INDEX.md` · the pack's own manifest, not an exemplar

<!-- exemplars:end -->

<!-- kinds:begin -->

📐 **Section kinds** · none declared in `stages/section-kinds.yml`, so this venue is blueprint-only: the S-Venue-0 blueprint is binding and no per-section pack is resolved.

<!-- kinds:end -->

🔗 **Authority** · the venue's own instructions, fetched and verified 260802

- [PNAS author center: submitting your manuscript](https://www.pnas.org/author-center/submitting-your-manuscript) · article types and their length, manuscript order, the front-block caps, and the Supporting information rules
- [SI Appendix template, Word](https://www.pnas.org/pb-assets/authors/PNAStemplateSI-1755285180080.docx) · the page's own "See the PNAS SI template" link, and the file division 9 says the pack does not have
- [SI Appendix template, LaTeX on Overleaf](https://www.overleaf.com/latex/templates/pnas-template-for-supplementary-information/wqfsfqwyjtsd) · the official LaTeX half of the same row, which Overleaf and the NAS state they built together
- [Research article template, Word](https://www.pnas.org/pb-assets/authors/PNASTemplateforMainManuscript-1755285180130.docx) and [PNAS LaTeX main template](https://www.pnas.org/pb-assets/authors/PNAS-template-main-1764608845890.tex) · the templates table runs Word beside LaTeX for research article, Brief Report and SI Appendix alike
- THE CEILING IS PAGES, AND THE JOURNAL CONVERTS IT: "The preferred length of these articles is 6 pages, but PNAS allows articles up to a maximum of 12 pages", and "a standard 6-page article is approximately 4,000 words, 50 references, and 4 medium-size graphical elements"
- CONTRADICTS the pack, twice: the about 50,000 characters carried by `playbook-pnas/taste.md` and by the figures at 3.1 and 8.1 appears nowhere in the instructions, and no file in the pack records the 12-page maximum at all
- So the six-section sum of about 6,970 words recorded at 8.1 runs about 74% past the journal's own 4,000-word conversion of the preferred article, and fits only a manuscript spending its way toward the 12-page ceiling
- The 4 medium-size graphical elements of a standard article sit under the "up to ~6 main figures" that `playbook-pnas/README.md` gives Results at 6.1, so the display budget on this page is the ceiling case and not the preferred one
- The 120-word Significance Statement cap at 3.2 is confirmed, and it is SCOPED: the page files it as "Significance statement (Direct and Contributed Submissions only)", a restriction no file in the pack records
- The 250-word Abstract cap at 4.2 is confirmed, and the page adds a rule the same division's anti-pattern list contradicts: "Cite all references in the abstract in full within the abstract itself AND in the text", so a citation there is accommodated rather than forbidden
- Brief Reports are their own article type at 3 pages, about 1,600 words and 15 references, and their SI "is limited to extended methods, essential supporting datasets, and videos (no additional tables or figures)"; this page records only the Research Report

## Law

- The PNAS Significance Statement is a readiness gate before it is a section. Its test and its section norms sit in two files that do not reference each other, so a writer meets one half at a time.
  A retarget into this outlet subtracts claims and floats rather than adding sections, which is the opposite of every other retarget in this group.

## Glossary

- **Doubled path**: `playbook-pnas/pnas/`, where the pack and its single outlet share a name, and the source of most mis-written paths to this outlet.

## Log

260802 · Rewrite pass for a weak-English reader, run through `/haipipe-writing`. The Opening now names both files and what is wrong between them. Its drawer writes the doubled path in full, as this page's own Writing Style already required. Long sentences split in `### 1`, `3.1`, `4.1`, `5.2`, `6.2`, `### 9`, `9.1`, `9.2`, Law and five Log entries. Every fact, number, source and quotation is unchanged. Two edits carry no change record, because `cli/wdiff.py` refuses any line holding an asterisk or a tilde: the `What is split apart` part and the Law record.
260802 · Corrected against the journal. Two of the four gaps this page claimed at `### 9` were wrong. PNAS publishes an SI template in Word and in official Overleaf LaTeX, plus a composition, numbering and reference-stream rule. No word budget and no arc remain true, and `A9.1` still stands on those. The length claim was wrong too, in the direction that matters. The journal states 6 pages preferred and 12 maximum, and CONVERTS it itself: about 4,000 words for a standard 6-page article. So the pack's about 50,000 characters is unsourced. The six per-section budgets, summing to about 6,970 words, then run roughly 74 percent past the journal's own figure. A paper drafted to this pack's budgets is far too long.
> ✎ 260802 · Corrected against the journal. Two of the four gaps this page claimed at `### 9` were ~wrong:~ *wrong.* PNAS publishes an SI template in Word and in official Overleaf LaTeX, plus a composition, numbering and reference-stream rule. No word budget and no arc remain true, and `A9.1` still stands on those. The length claim was ~also~ wrong *too,* in the direction that ~matters: the~ *matters. The* journal states 6 pages preferred and 12 ~maximum~ *maximum,* and CONVERTS it ~itself,~ *itself:* about 4,000 words for a standard 6-page ~article, so~ *article. So* the pack's about 50,000 characters is ~unsourced and the~ *unsourced. The* six per-section ~budgets~ *budgets,* summing to about 6,970 ~words~ *words, then* run roughly 74 percent past the journal's own figure. A paper drafted to this pack's budgets is far too long. · CC · 260802 1543
260802 · JL: PNAS has the SI things, check that. `### 9` strengthened with the pack's own framing. `pnas-methods/style.md:14` calls the SI Appendix split the DEFINING constraint of the Methods section. And guzikevits-2024's main Methods is about 700 words, against an SI holding the variable dictionaries plus five analysis tables. The finding is not that PNAS lacks an appendix. It is that the larger artifact is the one with no kind, no style guide, no template and no S page.
> ✎ 260802 · JL: PNAS has the SI things, check that. `### 9` strengthened with the pack's own ~framing:~ *framing.* `pnas-methods/style.md:14` calls the SI Appendix split the DEFINING constraint of the Methods ~section, and~ *section. And* guzikevits-2024's main Methods is about 700 ~words~ *words,* against an SI holding the variable dictionaries plus five analysis tables. The finding is not that PNAS lacks an ~appendix, it~ *appendix. It* is that the larger artifact is the one with no kind, no style guide, no template and no S page. · CC · 260802 1543
260802 · Opened with the QBv outlet pages, from `playbook-pnas/pnas` at `Venue-Paper@fe25a88`.
260802 · Added divisions 3 to 9: one per section kind, from each `pnas-<kind>/style.md` and `template.md`, plus the no-appendix division from `stages/section-kinds.yml`. Folded in the retired pack head's `taste.md`, `README.md` and `style-profile.md` content. Relaxed the length-number rule to cite-with-source.
> ✎ 260802 · Added divisions 3 to 9: one per section ~kind~ *kind,* from each `pnas-<kind>/style.md` and `template.md`, plus the no-appendix division from ~`stages/section-kinds.yml`; folded~ *`stages/section-kinds.yml`. Folded* in the retired pack head's `taste.md`, `README.md` and `style-profile.md` ~content, and relaxed~ *content. Relaxed* the length-number rule to cite-with-source. · CC · 260802 1543
260802 · Added an Authority block to Files and a `9.2` to the SI division, both from the PNAS author center fetched that day. Three findings landed against the pack. First, the ceiling is stated in PAGES, with the journal's own conversion (6 preferred, 12 maximum, a 6-page article about 4,000 words). So the about 50,000 characters at 3.1 and 8.1 is unsourced, and the 6,970-word sum runs about 74% past the preferred length. Second, PNAS does publish an SI Appendix template in Word and LaTeX, so division 9's template gap belongs to the pack and not to the journal. Third, the SI carries five rules the pack has no file for: single PDF, published as provided, S1 numbering, its own reference stream, and frozen at acceptance. What survives is the real hole: no SI word budget and no SI arc. That is what A9.1 is still open on.
> ✎ 260802 · Added an Authority block to Files and a `9.2` to the SI division, both from the PNAS author center fetched that day. Three findings *landed* against the ~pack:~ *pack. First,* the ceiling is stated in ~PAGES~ *PAGES,* with the journal's own conversion (6 preferred, 12 maximum, a 6-page article about 4,000 ~words), so~ *words). So* the about 50,000 characters at 3.1 and 8.1 is ~unsourced~ *unsourced,* and the 6,970-word sum runs about 74% past the preferred ~length;~ *length. Second,* PNAS does publish an SI Appendix template in Word and LaTeX, so division 9's template gap belongs to the pack and not to the ~journal; and~ *journal. Third,* the SI carries five rules the pack has no file ~for,~ *for:* single PDF, published as provided, S1 numbering, its own reference stream, and frozen at acceptance. What survives is the real hole: no SI word budget and no SI ~arc, which~ *arc. That* is what A9.1 is still open on. · CC · 260802 1543
260802 · Added a `Format values` and a `The language, in the papers' own words` subsubsection to each of the six section-kind divisions. The WORDS rows now carry the running sum to 6,970 / 6,970, against a ceiling the pack states only in characters. VALUE DENSITY reads `not recorded by the pack` in all six. And the introduction's cold open is recorded as a conflict inside one file.
> ✎ 260802 · Added a `Format values` and a `The language, in the papers' own words` subsubsection to each of the six section-kind ~divisions; the~ *divisions. The* WORDS rows now carry the running sum to 6,970 / ~6,970~ *6,970,* against a ceiling the pack states only in ~characters,~ *characters.* VALUE DENSITY reads `not recorded by the pack` in all ~six, and~ *six. And* the introduction's cold open is recorded as a conflict inside one file. · CC · 260802 1543
