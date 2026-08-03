# Nature Machine Intelligence: the desk that wants the method and the impact, and refuses either alone

state: 🟡 PARTIAL · 20 exemplars · 7 sections · taste ✓ · the only outlet in the tree where the method may BE the contribution
owner: JL
method: state what NMI requires of a method paper, and record that this is the one desk in the tree that does not treat method-as-contribution as a rejection

## Opening

What does Nature Machine Intelligence ask of a paper that no other desk in this tree asks?
> ✎ ~Every~ *What does Nature Machine Intelligence ask of a paper that no* other desk in this tree ~treats~ *asks? It asks for two things at once, and it refuses* a ~method as an enabler~ *paper that brings only one. The first half is a novel method,* and ~refuses it as a claim. This one takes~ *this is the only desk in the tree that lets* the method ~as~ *be* the ~contribution, and then~ *claim. The second half is impact outside machine learning, so the work must matter to someone who does not build models. This page records what the desk* asks ~a second question~ *of each of its seven sections, in* the ~ML venues do not. What is that second question?~ *pack's own numbers.* · CC · 260802 1545
It asks for two things at once, and it refuses a paper that brings only one.
The first half is a novel method, and this is the only desk in the tree that lets the method be the claim.
The second half is impact outside machine learning, so the work must matter to someone who does not build models.
This page records what the desk asks of each of its seven sections, in the pack's own numbers.

**Where this page sits**: it is one venue target in `QBv`, one page per desk with no pack layer above it.
This page owns only what is true of `playbook-nature-portfolio/NMI/`.

**Why this outlet is the tree's exception**: `QBv1` records MISQ refusing method-as-contribution outright, and `QBv5` records JAMA refusing an AI paper with no patient-outcome impact.
NMI accepts the method as the claim, and then asks for impact beyond the ML community as well.
> ✎ NMI accepts the method as the ~claim~ *claim,* and then ~requires~ *asks for* impact beyond the ML ~community, which is a conjunction~ *community as well. It adds the second demand* rather than ~a substitution.~ *trading one for the other.* · CC · 260802 1545
It adds the second demand rather than trading one for the other.

**What is unusual on disk**: the outlet folder is the only one in the tree named in capitals, `NMI/`, with `NMI-<section>/` beneath it. Every sibling uses a lowercase slug.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**Quote a number with its source, never own it**: a word budget, paragraph count or density may appear in a section division, but only with the file block or exemplar it was measured from named on the same line, and the page never states a norm as its own claim.

**Always name both halves**: the method AND the impact, never one of them, because dropping either half describes a different venue.

✅ `the method AND the impact`  ❌ `a strong methodological contribution`

## Diagram

**Both halves, or neither**: a novel method and demonstrated impact outside ML.

```text
  🎯 THE TEST
     "Does this advance what machines can learn, reason about,
      or do ── and does it matter beyond the ML community?"

  ✅ WHAT CLEARS IT
     a NOVEL method with real-world or scientific impact
     rigorous evaluation ── ablations · strong baselines ·
       failure analysis

  ❌ DESK-REJECT
     an incremental architecture tweak
     off-the-shelf ML where only the DATASET is new
     unvalidated "human-level" claims

  🔀 THE TREE'S EXCEPTION
     🏛 MISQ    method-as-contribution ── DESK-REJECT
     🏥 JAMA    AI with no patient outcome ── DESK-REJECT
     💻 npj DM  benchmark with no clinical question ──
                DESK-REJECT
     🤖 NMI     method IS the contribution ── ✅
                and then impact beyond ML is REQUIRED

  📊 20 exemplars · folder is NMI/ in capitals, alone in
     the tree
```

## Content

### 1 · The bar is both halves: the method AND the impact

**Two halves that fail differently**: and each half alone names a different venue.

```text
  🤖 method only, no outside impact
     ── an ML conference paper

  🏥 impact only, off-the-shelf method
     ── npj Digital Medicine, or JAMA if the outcome is
        clinical

  ✅ NMI wants BOTH, in one paper

  🔬 and it names the evaluation apparatus it expects
     ablations · strong baselines · failure analysis
     ── the third is the one most often missing
```

🔀 Establishes the two halves as a routing test: the half that is missing names where the paper actually belongs.
> ✎ 🔀 Establishes the ~conjunction~ *two halves* as *a routing test:* the ~routing instrument: which~ half *that* is missing names where the paper actually belongs. · CC · 260802 1545

#### 1.1 · "Off-the-shelf ML where only the dataset is new" describes a common shape in this repo
(so the rejection is worth reading before a study is framed as a method paper)
Applying an existing model to a new corpus is not a method contribution at this desk.
The same work is welcome at npj Digital Medicine if the claim moves from the model to what a clinician can now measure.

### 2 · Where a rejected NMI paper goes

**The missing half names the destination**: this is the only desk in the tree that routes on subtraction.

```text
  ❌ rejected for "only the dataset is new"
     ▶ 💻 npj DM ── if the claim becomes clinical measurement
     ▶ 🌍 Nat Comms ── if the finding travels across fields

  ❌ rejected for "incremental architecture tweak"
     ▶ an ML venue outside this tree entirely

  ❌ rejected for an unvalidated "human-level" claim
     ▶ nowhere, until the claim is bounded
     ── this is a claim-scope error, the same class QBv11
        records for WEIRD samples, and equally fixable
```

🔀 Establishes a concrete next outlet for each rejection, which no other page in this group can currently offer.
> ✎ 🔀 Establishes a concrete ~descent path~ *next outlet* for each rejection, which no other page in this group can currently offer. · CC · 260802 1545

### 3 · The abstract is one unstructured paragraph

**No labels, no citations, one block**: the only structure an NMI abstract has is the order of its beats, and every number below is quoted from `NMI-abstract/style.md`.

```text
  📝 ARC ── one paragraph, beats in this order
     S1-2  the problem, why it matters broadly (NOT the method)
     S3    the gap, what was not possible
     S4    "Here we ..." pivot + system NAME + acronym expansion
     S5-6  what the method does, high level
     S7-8  results ── directional, or ONE headline metric
     S9    significance / broad applicability

  📏 MEASURED  [NMI-abstract/style.md]
     word budget      160-270w, median ~200    "Word budget"
     paragraphs       1                        "Paragraph structure"
     sentences        6-10                     "Paragraph structure"
     words/sentence   ~25-32, median ~28       micro-norms 2026-07-08
     citations        0                        micro-norms, "0 in both"
     measured on      serapio-garcia-2025 193w · qiao-2025 223w
     corpus spread    mon-williams-2025 ~160w · gu-2026 ~270w

  🎰 SLOTS ── patterns to fill, never sentences to copy
     pivot   "Here we <verb> <system> (<acronym expansion>)"
     hedge   "we found that" · "we show that" · "we demonstrate"
     close   "This <system> can be broadly applied to <domain>"

  ⛔ THE PACK NAMES  [NMI-abstract/style.md anti-patterns]
     labeled fields: Background / Methods / Results / Conclusions
     opening on the method name
     closing on the method or on a metric
     p-values, confidence intervals, regression coefficients
     passive-heavy construction
     anything past ~270 words
```

📝 Establishes the abstract as the one NMI section carrying no citation at all, so the venue's superscript rule has nothing to act on here.

#### 3.1 · The zero-citation measurement changes what a placeholder can be
(so an abstract draft that reaches for a citation command has already left the venue)
`NMI-abstract/template.md` reads the micro-norm "Citations | 0 in both" as a drafting rule: neither `\citep{key}` nor `\cite{TOADD}` should appear in an NMI abstract.
An unverified headline number is written as a value placeholder instead, and PROBE traces it.
That makes the abstract the only one of the seven kinds whose draft carries a single placeholder class.

#### 3.2 · Format values
(what the pack measures for an NMI abstract, and the two rows it leaves empty)

```text
  📏 WORDS            160-270w, median ~200 · 1 paragraph · 6-10 sentences ·
                      ~25-32 words/sentence, median ~28
                      [NMI-abstract/style.md "Word budget" + "Paragraph
                       structure" + micro-norms 2026-07-08]
  📚 CITATION DENSITY 0 per sentence · "NMI abstracts carry no numbered
                      citations"
                      [NMI-abstract/style.md micro-norms, "Citations | 0 in both"]
  🔢 VALUE DENSITY    not recorded by the pack
  📊 DISPLAYS         not recorded by the pack · the guide records structure
                      alone, "One paragraph only. No line breaks, no
                      sub-sections, no bullet lists", and names no figure and
                      no table anywhere in the file
                      [NMI-abstract/style.md "Paragraph structure"]
```

#### 3.3 · The language, in the papers' own words
(four attributed sentences from the abstract guide, one per beat of the arc above)
"Completing complex tasks in unpredictable settings challenges robotic systems, requiring a step change in machine intelligence." [mon-williams-2025]
The S1-2 opening beat, where the problem takes the first sentence and the method is not named yet.
"Here, we present a comprehensive psychometric methodology..." [serapio-garcia-2025]
The S4 pivot slot, in the exact shape the SLOTS block records as "Here we <verb> <system>".
"CSFM outperforms traditional approaches and maintains robust performance across varying lead configurations..." [gu-2026]
The S7-8 results beat: the baseline comparison is stated, hedged and directional, with no statistic attached.
"This framework can be broadly applied to the analysis of multimodal omics studies and reveals more powerful biological insights from limited cohort sizes." [mataraso-2025]
The S9 close, and the impact-beyond-ML half, placed in the last sentence rather than the first.
> ✎ The S9 close, and the impact-beyond-ML ~half of the conjunction,~ *half,* placed in the last sentence rather than the first. · CC · 260802 1545

### 4 · The introduction is a funnel that ends on the contribution

**Broad stakes narrow to a gap, then open onto the system**: the contribution paragraph is always the last or second-to-last one, and it is deliberately the sparsest in citations.

```text
  🔻 ARC ── a funnel, 4-8 paragraphs
     P1         domain importance, why this matters to the world
     P2..P(n-2) approaches BY TYPE, each followed by its limitation
     (gap)      a sentence folded into the last background ¶
     P(n-1)     "Here we ..." + system NAME + (Fig. 1)
     P(n)       optional preview: what was run, not what it found

  📏 MEASURED  [NMI-introduction/style.md]
     word budget      550-1,600w, typical 650-1,100  "Word budget"
     paragraphs       4-8, modal 4-5                 "Word budget"
     sentences/¶      2-13, median ~5                micro-norms
     words/sentence   13-35, median ~21              micro-norms
     references       15-40 across the introduction  move 5
     markers          ~30 per introduction           micro-norms
     density          serapio ~1.0/sentence, qiao ~0.7/sentence
     the ~11 outlier  serapio-garcia-2025 folds a titled background
                      subsection into the lead; count untitled
                      leads only and it stays inside 6-8

  🎰 SLOTS
     hook     clinical significance | rhetorical question |
              field-transformation claim
     gap      "<approach category> <exists verb> <refs>, but
              <limitation>", closing on "remains underexplored"
     contrib  "Here we <verb> <system> (<acronym>; Fig. 1)"
     defer    "we further detail related work in Supplementary
              Note <A.n>"

  ⛔ THE PACK NAMES  [NMI-introduction/style.md anti-patterns]
     opening with "We propose X to solve Y"
     a Related Work subsection inside the introduction
     a bulleted contribution list
     author-year citations
     more than one paragraph per approach category
     results or data analysis in the introduction
```

🔻 Establishes the citation-density split that no other section repeats: the background paragraphs hold ~14 to ~50 references while the contribution paragraph holds 2-3.

#### 4.1 · Citations render as superscript numbers, and the key stays real
(so the numeric rendering is a sync-time fact, not a licence to write a number into the draft)
`NMI-introduction/template.md` states the rule for every NMI kind.
> ✎ `NMI-introduction/template.md` states the rule for every NMI ~kind: the outlet~ *kind. A citation* renders ~citations~ as *a* superscript ~numbers~ *number* in the naturemag style, never ~author-year, and often in ranges~ *as author-year. Ranges* such as "refs ~1-5".~ *1-5" are common.* · CC · 260802 1545
A citation renders as a superscript number in the naturemag style, never as author-year.
Ranges such as "refs 1-5" are common.
The draft still authors a real `\citep{key}` verified against the .bib, because only the rendered form is numeric.
Where no key exists, the draft carries `\cite{TOADD}` with the owning question id until PROBE closes it.

#### 4.2 · The paragraph count contradicts itself inside one file
(so a drafter quoting "the" paragraph count is quoting one of two numbers)
`NMI-introduction/style.md` gives "4-8 paragraphs typical (modal 4-5)" in its Word budget block, and lists qiao-2025 there at ~900 words in 4 paragraphs.
Its own micro-norms table then reports paragraphs as "6-11 (qiao ~6)".
The reconciliation note explains the ~11 high end but not the qiao gap, so the page records both numbers rather than picking one.

#### 4.3 · Format values
(the introduction's budget, with the paragraph row carrying the two numbers 4.2 records)

```text
  📏 WORDS            550-1,600w, typical 650-1,100 · 4-8 ¶ modal 4-5 in the
                      budget block, against 6-11 in the micro-norms table ·
                      2-13 sentences/¶, median ~5 · 13-35 words/sentence,
                      median ~21
                      [NMI-introduction/style.md "Word budget" + micro-norms
                       2026-07-08; the paragraph clash is recorded at 4.2]
  📚 CITATION DENSITY serapio ~1.0/sentence · qiao ~0.7/sentence · ~30 markers
                      per introduction · near-zero in the contribution ¶
                      [NMI-introduction/style.md micro-norms 2026-07-08]
  🔢 VALUE DENSITY    not recorded by the pack
  📊 DISPLAYS         no figure or table count recorded · the guide records a
                      REFERENCE only, "(Fig. 1)" in the contribution paragraph,
                      pointing at the architecture or overview figure
                      [NMI-introduction/style.md move 4 + "Contrast with IS
                       journals": "NMI commonly references Fig. 1 in the
                       contribution paragraph"]
```

#### 4.4 · The language, in the papers' own words
(four attributed sentences, one per stage of the funnel this division draws)
"Machine learning (ML) models are powerful tools for detecting complex patterns, yet their 'black-box' nature limits their interpretability" [chen-w-2025]
The P1 hook slot in its field-transformation form: domain importance first, and the method nowhere.
"Late fusion approaches struggle to learn cross-modal interactions." [mataraso-2025]
One approach category and its limitation in a single clause, which is the background paragraph's whole unit of work.
"...their application to personalized normative modelling of the heart from population data remains underexplored." [qiao-2025]
The terminal gap sentence, closing on the exact phrase the gap slot names, "remains underexplored".
"To address these challenges, we develop a foundation model, the cardiac sensing foundation model (CSFM; Fig. 1)..." [gu-2026]
The contrib slot, carrying both the acronym expansion and the figure pointer the DISPLAYS row above records.

### 5 · Related work is three destinations, not a section

**The kind is declared and the section does not exist**: `stages/section-kinds.yml` gives `related-work` to all five Nature outlets and to no outlet in any other pack, and none of NMI's eight exemplars carries a standalone one.

```text
  🧭 WHERE THE POSITIONING ACTUALLY GOES
     Introduction background   the GAP
     Results subsection        HEAD-TO-HEAD, 2-4 named methods
     Discussion                positioning-by-CONTRAST
     Supplementary Note        the extended review, as a pointer

  📏 MEASURED  [NMI-related-work/style.md]
     positioning ¶    intro background 3-5 · discussion 2-4
     sentences/¶      3-8, median ~5
     words/sentence   13-30, median ~22
     intro refs       ~16 (gu-2026) to ~53 (mon-williams-2025)
     background ¶     hold ~14 to ~50 of them
     contribution ¶   2-3
     density          intro background ~1.0-1.5 markers/sentence,
                      the highest local density in the corpus;
                      discussion positioning ~0.3/sentence
     per prior work   1-2 clauses, cited as a trend

  🎰 SLOTS
     gap        "<category> has been proposed <refs>. However,
                <limitation>." x 2-3, then "remains underexplored"
     head2head  "<System> outperforms <prior approaches>"
                ── written as a Results subsection heading
     contrast   "So far, only <n> previous studies have <verb>,
                all in <scope limitation>"
     synergy    "should not be seen as a competitor to these lines
                of work, but rather as synergistic"

  ⛔ THE PACK NAMES  [NMI-related-work/style.md anti-patterns]
     a standalone Related Work / Literature Review / Background /
       Prior Work heading, called a structural violation
     a full paragraph reviewing one work
     chronological organization
     author-year citations
     front-loading all positioning into the Introduction
     discussing an individual paper's contribution at length
```

🧭 Establishes that the related-work unit is a draft with three destinations and no section of its own.
> ✎ 🧭 Establishes that the related-work unit is a draft with three ~addressees~ *destinations* and no ~home~ *section* of its ~own, which is why~ *own. So* its output is measured on *paragraphs* borrowed ~paragraphs.~ *from other sections.* · CC · 260802 1545
So its output is measured on paragraphs borrowed from other sections.

#### 5.1 · The kind name says section and the pack says otherwise
(so this is the one kind whose name a drafter must not take literally)
`section-kinds.yml` separates two positioning kinds that are not aliases: the IS family's `theory` DEVELOPS a model and its hypotheses, while the Nature family's `related-work` SITUATES the paper against prior literature.
The separation is real, but at NMI the situating happens inside three other sections rather than under a heading of its own.
`NMI-related-work/template.md` opens with a structural warning that says so.
> ✎ `NMI-related-work/template.md` opens with a structural warning that says ~so, and instructs~ *so. It also tells* the draft gate to ~confirm~ *check* with the author that ~a~ *no* standalone section is ~not~ wanted. · CC · 260802 1545
It also tells the draft gate to check with the author that no standalone section is wanted.

#### 5.2 · The family README states the same rule one level up
(so the retired family page's only load-bearing claim about this kind is recorded here)
`playbook-nature-portfolio/README.md` lists "No standalone Related Work section" among the conventions holding across all five outlets, citing every `*-related-work/style.md`.
It routes the positioning to Introduction for the gap, Results for the head-to-head, and Discussion for the comparison, with extended review deferred to Supplementary.
That is the same three-destination pattern this division records, so the outlet and the family agree and neither one licenses a heading.

#### 5.3 · Format values
(a unit with no section of its own, so its budget is stated as a charge against the three sections that carry it)

```text
  📏 WORDS            no budget of its own · it SPENDS 3-5 Introduction
                      background ¶ + 2-4 Discussion positioning ¶ + one
                      Results head-to-head subsection · 3-8 sentences/¶,
                      median ~5 · 13-30 words/sentence, median ~22
                      [NMI-related-work/style.md micro-norms 2026-07-08:
                       "metrics are taken on the embedded positioning content"]
  📚 CITATION DENSITY intro background ~1.0-1.5 markers/sentence, the highest
                      local density in the corpus · discussion positioning
                      ~0.3/sentence · 1-2 clauses per prior work
                      [NMI-related-work/style.md micro-norms 2026-07-08]
  🔢 VALUE DENSITY    not recorded by the pack
  📊 DISPLAYS         no display of its own · it SPENDS one Results subsection,
                      which the results template then obliges to carry a
                      figure · the exemplar is pontikos-2025's subsection
                      "Eye2Gene predictions outperform other AI approaches"
                      [NMI-related-work/style.md "How related work appears in
                       Results" + NMI-results/template.md line 31]
```

#### 5.4 · The language, in the papers' own words
(five attributed sentences: the gap that starts the unit, then one per destination it is spent on)
"Existing foundation models are predominantly based on ECG data and are largely confined to standard 12-lead configurations." [gu-2026]
Destination one, the Introduction gap: a category is named and limited in one sentence, with no paper reviewed.
"efforts have been made to extend interpretable ML methods to discover interactions among features" [chen-w-2025]
The same destination at category level, which is the brevity rule the guide states as 1-2 clauses per prior work.
"Eye2Gene predictions outperform other AI approaches" [pontikos-2025]
Destination two, the Results head-to-head, written as a subsection heading rather than as prose.
"Our approach based on LLM embeddings should not be seen as a competitor to these lines of work, but rather as synergistic." [doerig-2025]
Destination three, the Discussion positioning-by-contrast, filling the synergy slot this division records.
"we further detail related work in Supplementary Note A.2" [serapio-garcia-2025]
Destination four, the Supplementary pointer.
> ✎ Destination four, the Supplementary ~pointer, which is how the~ *pointer. The* extended review leaves the main text *this way* without leaving the paper. · CC · 260802 1545
The extended review leaves the main text this way without leaving the paper.

### 6 · Methods is last, and it is where the equations live

**A recipe placed after Discussion**: architecture, then training, then evaluation, then data provenance, closing on two mandatory availability subsections.

```text
  🔬 PLACEMENT ── all 8 exemplars agree
     Discussion [-> Conclusion] -> Methods -> Data availability
       -> Code availability -> References
     Methods is NEVER between Introduction and Results
     Methods is NEVER merged with Results

  🔬 ARC
     architecture -> training/optimization -> loss/objective
       -> datasets -> evaluation -> baselines -> [ethics]
       -> reporting summary -> data availability -> code availability

  📏 MEASURED  [NMI-methods/style.md]
     word budget      1,200-3,000w, 2.5-4 pages   "Word budget"
     subsections      7-16                        move 1
     per exemplar     chen-w 7 · mon-williams 7 · qiao 8 · gu 8 ·
                      pontikos 11 · serapio 12 · mataraso 14 ·
                      doerig 16
     paragraphs       ~10-16, subsection-driven   micro-norms
     sentences/¶      4-8, median ~6              micro-norms
     words/sentence   18-30, median ~24           micro-norms
     citations        ~0.3-0.5/sentence           micro-norms
     equations        0 (serapio · mon-williams · doerig) ·
                      3 (gu · mataraso) · 6 (chen-w) · 10 (qiao)

  🎰 SLOTS
     hyperparam  optimizer, learning rate, batch size, epochs,
                 GPU model + memory, wall-clock
     versions    "Python <v>, NumPy <v>, ... PyTorch <v>"
     split       "<n> train / <n> validation / <n> test" plus the
                 STRATEGY word: patient-wise, subject-wise,
                 family-aware, stratified
     equation    prose setup -> "(Eq. <k>)" -> variable definitions
     closers     Reporting summary · Data availability ·
                 Code availability

  ⛔ THE PACK NAMES  [NMI-methods/style.md anti-patterns]
     Methods before Results
     Methods combined with Results
     omitted hyperparameters
     omitted Data or Code availability
     all datasets in one prose paragraph
     primary equations placed in Results
     exclusively passive voice
```

🔬 Establishes the section that carries the reproducibility half of the desk's evaluation demand, and the two mechanics a drafter meets nowhere else.

#### 6.1 · Superscript rendering, real key
(so a Methods draft never writes the rendered form)
`NMI-methods/template.md` repeats the outlet rule at the point of use: NMI renders citations as superscript numbers in the naturemag style, never author-year.
The draft authors a real `\citep{key}` grep-verified against the .bib, because the key is real and only the rendering is numeric.
The density in Methods clusters where an architecture, a tool, a dataset, or a prior method is first named.

#### 6.2 · An equation is drafted as prose, a label, and its variables
(so the display math never enters the markdown that cannot hold it)
`NMI-methods/template.md` marks this with a warning: NMI Methods carry numbered display equations, but the board's markdown allows no LaTeX except citation commands.
So an equation is drafted here as its prose setup, then the marker "(Eq. k)", then the variable definitions.
> ✎ So an equation is drafted here as its prose setup, then the marker "(Eq. k)", then the variable ~definitions, and the~ *definitions. The* display math body is authored at sync-to-tex. · CC · 260802 1545
The display math body is authored at sync-to-tex.
An equation is neither a display request nor a question, which separates it from every figure in the paper.

#### 6.3 · The evaluation apparatus is split across three files, and one third has no home
(so the desk's third demand is the one a drafter can silently skip)
`taste.md` desk-rejects a paper with "no ablation, no comparison to strong baselines, no failure analysis", and the section guides place only two of those three.
The baseline SETUP is a Methods subsection, and the head-to-head NUMBER is a Results subsection.
> ✎ The baseline SETUP is a Methods subsection, *and* the head-to-head NUMBER is a Results ~subsection, and~ *subsection.* `NMI-appendix/style.md` sends "Robustness checks and ablation details" to Supplementary Information. · CC · 260802 1545
`NMI-appendix/style.md` sends "Robustness checks and ablation details" to Supplementary Information.
Failure analysis is named in `taste.md` and in this page's Diagram, and in none of the seven section guides.
> ✎ Failure analysis is named in `taste.md` and in this page's Diagram, and ~appears~ in none of the seven section ~guides, so~ *guides. So* the pack cannot say what a failure-analysis paragraph looks ~like~ *like,* or where it sits. · CC · 260802 1545
So the pack cannot say what a failure-analysis paragraph looks like, or where it sits.

#### 6.4 · Format values
(the Methods budget, and the one display class this outlet carries that a board's markdown cannot hold)

```text
  📏 WORDS            1,200-3,000w over 2.5-4 pages · 7-16 subsections ·
                      ~10-16 ¶, subsection-driven · 4-8 sentences/¶, median
                      ~6 · 18-30 words/sentence, median ~24
                      [NMI-methods/style.md "Word budget" + micro-norms
                       2026-07-08]
  📚 CITATION DENSITY ~0.3-0.5/sentence, clustered where an architecture, a
                      tool, a dataset or a prior method is first named
                      [NMI-methods/style.md micro-norms 2026-07-08]
  🔢 VALUE DENSITY    not recorded by the pack
  📊 DISPLAYS         figures + tables: not recorded by the pack · the style
                      file names neither anywhere
                      [NMI-methods/style.md, whole file]
                      NUMBERED DISPLAY EQUATIONS, counted apart from figures
                      and tables and recorded per exemplar: 0 for
                      serapio-garcia-2025, mon-williams-2025 and doerig-2025 ·
                      3 for gu-2026 and mataraso-2025 · 6 for chen-w-2025 ·
                      10 for qiao-2025
                      [NMI-methods/style.md move 2]
                      the equation BODY is authored at sync-to-tex, because
                      the board's markdown allows no LaTeX but citation
                      commands; the .md holds prose, "(Eq. k)" and variables
                      [NMI-methods/template.md line 4]
```

#### 6.5 · The language, in the papers' own words
(five attributed sentences from the Methods guide, one per component of the recipe)
"The model consists of three GCN layers and one FC layer, with four attention heads, a feed-forward size of 1,024" [qiao-2025]
The architecture move that opens the arc, stated as a parts list rather than as a design argument.
"learning rate was set to 0.0001; batch size was set to 16; Dropout probability was fixed at 50%" [pontikos-2025]
The hyperparam slot this division records, at the level of detail the desk's reproducibility demand needs.
> ✎ The hyperparam slot this division records, at the ~grain~ *level of detail* the desk's reproducibility demand needs. · CC · 260802 1545
"subject-wise splitting to prevent data leakage" [gu-2026]
The split slot, and specifically its STRATEGY word, which the guide treats as mandatory alongside the ratios.
"Python 3.10.6, NumPy 1.23.3, Pandas 1.5.0, SciPy 1.9.1, scikit-learn 1.1.2, PyTorch 1.12.1, Gensim 4.3.0" [mataraso-2025]
The versions slot, pinned to the patch level, which no other section kind in this outlet asks for.
"described in detail in Supplementary Note A.7.2" [serapio-garcia-2025]
The deferral that keeps Methods inside its budget, and the reason division 9's tier decision is made before drafting.

### 7 · Results is the longest section and every heading is a claim

**Claim plus evidence, one unit at a time**: each subsection asserts a finding in its heading and spends its paragraphs proving it against a figure.

```text
  📊 ARC ── escalating from technical proof to significance
     [optional] method overview, conceptual, enough to read on
     technical validation ── reconstruction, reliability, benchmarks
     application / clinical utility
     advanced analysis ── interpretability, external validation
     [optional] accessibility ── web app, code release

  📏 MEASURED  [NMI-results/style.md]
     word budget      2,000-4,000+w, 5-8 pages   "Word budget"
     share            ~40-50% of the main text   "Word budget"
     paragraphs       11-20                      micro-norms
     sentences/¶      3-8, median ~5             micro-norms
     words/sentence   8-30, median ~20           micro-norms
     citations        qiao ~0.15/sentence, serapio near-zero
     subsections      3 to 9 across the 8 exemplars
     main figures     4 to 6 across the 8 exemplars
     main tables      0 for six exemplars; pontikos 2, serapio 1

  🎰 SLOTS
     heading   "<System> <active verb>s <capability>"
     stat      "<metric> of <value> (95% CI: <lo>, <hi>)"
     stat      "r = <v>, 95% CI [<lo>, <hi>], P = <p>"
     report    "We found that ..." · "We show that ..." ·
               "we assessed the ability of ..."
     micro-arc purpose -> setup -> result with a figure reference
               -> optional one-sentence interpretation
     two-tier  claim heading, then bold-inline, then italic-inline

  ⛔ THE PACK NAMES  [NMI-results/style.md anti-patterns]
     neutral headings: "Experiment 1", "Ablation study",
       "Performance comparison"
     result tables in the main text
     statistics lifted out of prose into a stat table
     Methods placed before Results
     a result paragraph with no figure or panel reference
     all benchmarks front-loaded before any application result
```

📊 Establishes where the strong-baseline half of the desk's demand becomes visible: a claim-headed head-to-head subsection whose figure carries the numbers.

#### 7.1 · The template hardens a mapping the style file's own table softens
(so a drafter following the template will refuse a layout three exemplars actually use)
`NMI-results/style.md` move 2 states a strict figure-subsection mapping, and `NMI-results/template.md` turns it into a failure condition: a result subsection with no figure display request fails the mapping.
The same style file's measured table then shows mataraso-2025 at 9 subsections to 6 figures and pontikos-2025 at 7 to 4, which is roughly 1.5 and 2 subsections per figure.
Only gu-2026, chen-w-2025 and mon-williams-2025 are actually 1:1.
> ✎ Only gu-2026, chen-w-2025 and mon-williams-2025 are actually ~1:1, so~ *1:1. So read* the template's hard ~gate should be read~ *rule* as a ~target rather than~ *target, not as* a measurement. · CC · 260802 1545
So read the template's hard rule as a target, not as a measurement.

#### 7.2 · The dominant in-text reference here is the paper's own back matter
(so low literature density in Results is a norm, not an omission)
`NMI-results/style.md` reports that both measured papers cross-reference their own Extended Data and Supplementary Tables far more than prior literature.
Literature clusters only where a baseline or a measure is first named.
Inline statistics with p-values and confidence intervals belong here and are forbidden in the abstract, which is the sharpest per-section split in the pack.

#### 7.3 · Format values
(the longest section, and the row the pack cannot fill is the one a benchmark-dense Results needs most)

```text
  📏 WORDS            2,000-4,000+w over 5-8 pages, ~40-50% of the main text ·
                      11-20 ¶ · 3-8 sentences/¶, median ~5 · 8-30
                      words/sentence, median ~20
                      [NMI-results/style.md "Word budget" + micro-norms
                       2026-07-08]
  📚 CITATION DENSITY qiao ~0.15/sentence · serapio near-zero · the lowest
                      literature density in the paper, because the dominant
                      in-text reference is the paper's own back matter
                      [NMI-results/style.md micro-norms 2026-07-08]
  🔢 VALUE DENSITY    not recorded by the pack
  📊 DISPLAYS         MEASURED 3 to 9 subsections against 4 to 6 main figures,
                      running 1:1 to ~2 subsections per figure ·
                      mataraso-2025 9 to 6 = ~1.5 · pontikos-2025 7 to 4 = ~2 ·
                      only gu-2026, chen-w-2025 and mon-williams-2025 are
                      truly 1:1, so 3 of 8 · main tables 0 for six exemplars,
                      pontikos 2, serapio 1
                      [NMI-results/style.md move 2 mapping table + move 3]
                      THE HARDER RULE: NMI-results/template.md line 31 turns
                      the same mapping into a failure condition, "a result
                      subsection with no figure DR FAILS the NMI
                      figure-subsection mapping" · read it as a target, not as
                      the measurement above
                      [NMI-results/template.md line 31]
```

#### 7.4 · The language, in the papers' own words
(five attributed sentences, one per rung of the claim-plus-evidence unit)
"Diamond reveals drivers of health-related mortality" [chen-w-2025]
The heading slot, "<System> <active verb>s <capability>", asserting the finding before any evidence is shown.
"We first assessed MeshHeart on the task of mesh reconstruction." [qiao-2025]
The purpose sentence that opens the micro-arc, naming what was tested before the setup arrives.
"CSFM achieved a macro-F1 of 0.677 (95% confidence intervals (CI): 0.656, 0.699)" [gu-2026]
The stat slot in prose, which is the form forbidden in the abstract and required here.
"We show that COMET achieves state-of-the-art predictive modelling results" [mataraso-2025]
The baseline comparison, hedged with "We show that" rather than claimed outright.
> ✎ The baseline comparison, hedged with "We show that" rather than claimed ~outright, which~ *outright. This* is ~how~ *where* the desk's ~strong-baseline~ demand ~surfaces.~ *for strong baselines shows up.* · CC · 260802 1545
This is where the desk's demand for strong baselines shows up.
"the faithfulness score increased from 0.74 to 0.88 with RAG" [mon-williams-2025]
A before-and-after value pair, and an instance of exactly the numeric content the VALUE DENSITY row above shows no style file in this pack counts.

### 8 · Discussion is short, pairs every limitation, and never ends on one

**A quarter the length of Results, with a fixed rhythm**: restate the contribution, position it, name the limitations with their future directions, close on significance.

```text
  🎬 ARC
     P1     contribution restatement at synthesis level,
            NOT a repeat of the abstract
     P2-P3  interpretation + positioning against named prior work
     P4     limitations, EACH paired with a future direction
     P5     conclusion / broader significance / forward look

  📏 MEASURED  [NMI-discussion/style.md]
     word budget      450-2,000w                 "Word budget"
     relative length  1/3 to 1/4 of Results      "Word budget"
     paragraphs       4-13, modal 4-7            "Word budget"
     per exemplar     mataraso ~450w/4¶ · gu ~450w/4¶ ·
                      chen-w ~650w/5¶ · mon-williams ~950w/6¶ ·
                      pontikos ~1,100w/7¶ · qiao ~1,100w/7¶ ·
                      doerig ~1,500w/~10¶ · serapio ~2,000w
     sentences/¶      4-8, median ~6             micro-norms
     words/sentence   18-30, median ~22          micro-norms
     citations        ~0.2/sentence, clustered in the limitations
                      and broader-implications paragraphs
     the ~13 outlier  serapio-garcia-2025 labels sub-heads into
                      short paragraphs; qiao runs unlabeled at 7

  🎯 TITLE VARIANTS ── pick one, the blueprint decides
     "Discussion" alone, optionally + a separate "Conclusion"
     "Discussion and conclusion" combined  [gu-2026]
     no Conclusion heading, but "In conclusion, ..." opens the
       final paragraph  [mon-williams · pontikos · qiao]

  🎰 SLOTS
     restate     "Our results demonstrate that <system>
                 <generalization claim>"
     enumerate   "First, we ... Second ... Third ... Finally ..."
                 ── allowed HERE, refused in the Introduction
     limits      "There are several limitations to this study."
                 "Despite these promising results, our work has
                 several limitations."
     pairing     "<limitation> -> <future direction>", every time
     close       "In conclusion, <synthesis> <forward look>"

  ⛔ THE PACK NAMES  [NMI-discussion/style.md anti-patterns]
     a Discussion longer than Results
     new results or data introduced here
     omitted limitations
     a limitation with no paired future direction
     the abstract repeated verbatim as the opening
     a literature survey disguised as Discussion
     ending on a limitation
```

🎬 Establishes the only place the pack asks a paper to say what it cannot do, and the pairing rule that keeps that admission from being the last thing a reader sees.

#### 8.1 · Sub-headed is the exception, and the exemplar count says so
(so a drafter reaching for four labelled sub-heads is copying one paper out of eight)
`NMI-discussion/style.md` move 5 names sub-headed Discussion as present but rare.
> ✎ `NMI-discussion/style.md` move 5 names sub-headed Discussion as present but ~rare, and only~ *rare. Only* serapio-garcia-2025 uses ~it:~ *it, under four sub-heads:* Limitations and future work, Broader implications, Ethical considerations, Conclusion. · CC · 260802 1545
Only serapio-garcia-2025 uses it, under four sub-heads: Limitations and future work, Broader implications, Ethical considerations, Conclusion.
Its ~13 paragraph count is a consequence of that labelling, not of a longer argument.
The default is un-sub-headed, and qiao-2025 runs seven unlabeled paragraphs at the same word count.

#### 8.2 · Format values
(the shortest prose section, and the only one whose budget is stated relative to another section)

```text
  📏 WORDS            450-2,000w, 1/3 to 1/4 the length of Results · 4-13 ¶,
                      modal 4-7 · 4-8 sentences/¶, median ~6 · 18-30
                      words/sentence, median ~22
                      [NMI-discussion/style.md "Word budget" + micro-norms
                       2026-07-08]
  📚 CITATION DENSITY ~0.2/sentence in both measured papers, clustered in the
                      limitations and broader-implications paragraphs where
                      prior work is contrasted
                      [NMI-discussion/style.md micro-norms 2026-07-08]
  🔢 VALUE DENSITY    not recorded by the pack
  📊 DISPLAYS         not recorded by the pack · the style file names no figure
                      and no table anywhere, and the nearest thing it says is
                      the anti-pattern against introducing new results or data
                      here
                      [NMI-discussion/style.md, whole file + anti-patterns]
```

#### 8.3 · The language, in the papers' own words
(five attributed sentences walking the fixed rhythm this division records)
"Our results demonstrate that CSFM robustly generalizes across a wide range of clinical scenarios, devices and input configurations." [gu-2026]
The P1 restate slot, pitched at synthesis level rather than repeating the abstract.
"First, we developed MeshHeart...Second, we demonstrated MeshHeart's capability..." [qiao-2025]
The enumerate slot, allowed here and refused in the Introduction, which is the pack's sharpest per-section split on rhetoric.
"There are several limitations to this study." [mataraso-2025]
The limits slot in its stock form, opening the P4 admission the desk expects of every paper.
"The current focus is pairwise interactions; higher-order is important but combinatorially hard." [chen-w-2025]
One real limitation, scoped to a capability rather than to the data, and short enough to pair immediately with its future direction.
"This work has important implications for AI alignment and harm mitigation, and informs ethics discussions concerning AI anthropomorphization, personalization and potential misuse." [serapio-garcia-2025]
The P5 close on significance, and the impact-beyond-ML half again.
> ✎ The P5 close on significance, and the impact-beyond-ML half ~again, which is why this~ *again. A* section ~may never end~ *that ends* on a ~limitation.~ *limitation ends on the wrong half.* · CC · 260802 1545
A section that ends on a limitation ends on the wrong half.

### 9 · The back matter is two tiers with independent counters

**Extended Data is reviewed, Supplementary Information is not**: the two tiers differ in status, review process, file location, and cap, and their numbering never mixes.

```text
  🗄 TIER 1 ── Extended Data
     where     end of the main article PDF, after References,
               before the Reporting Summary
     status    peer-reviewed, part of the published article
     cap       10 items TOTAL, figures + tables combined
     holds     captions and legends only, NO running prose
     for       supporting evidence reviewers must inspect:
               full data tables summarized in the main text,
               distribution plots, heatmaps, per-condition
               breakdowns
     optional  gu-2026 and qiao-2025 use none at all

  🗄 TIER 2 ── Supplementary Information
     where     a separate online-only PDF linked from the article
     status    not peer-reviewed to the same standard
     cap       none; commonly 20-60+ pages
     for       background and related-work expansions, detailed
               methodology, extended results, dataset descriptions,
               full prompt text, parameter sweeps, robustness
               checks and ablation details

  🔢 NUMBERING ── independent per tier, and per type within a tier
     Extended Data Fig. N        Extended Data Table N
     Supplementary Fig. N        Supplementary Table N
     Supplementary Note A.N.M    (hierarchical: A.1, A.1.1, A.6.3)
     Supplementary Information section N.M
     Extended Data Fig. 1 and Supplementary Fig. 1 are DIFFERENT
       objects; the counters never merge

  ⚖️ TRIAGE ── what belongs where
     main text        core figures the argument needs
     Extended Data    essential support a reviewer must inspect
     Supplementary    supporting but not essential
     the reason       reviewers may not examine Supplementary
                      Information as closely

  📏 MEASURED  [NMI-appendix/style.md, from 2 exemplars only]
     main text        14-15 published pages
     Extended Data    typically 2-6 pages inside the article PDF
     serapio-2025     4 ED figures + 7 ED tables = 11 items,
                      OVER the 10-item cap; the guide flags it
                      and says treat 10 as the submission target
     qiao-2025        0 Extended Data items, all back matter
                      routed to Supplementary Information
     prose metrics    N/A ── count items, not sentences

  ⛔ THE PACK NAMES  [NMI-appendix/style.md anti-patterns]
     mixing Extended Data and Supplementary numbering
     running prose inside Extended Data
     abbreviating a label after first use: never "ED Fig."
     a bare number: "Supplementary Note A.6", never "Note A.6"
     an essential figure parked in Supplementary Information
     more than 10 Extended Data items
```

🗄 Establishes the tier decision as a triage made before any display unit is built.
> ✎ 🗄 Establishes the tier decision as a triage made before any display unit is ~built, because the~ *built. The* tier fixes the label, the counter, and whether a reviewer will read the ~item.~ *item at all.* · CC · 260802 1545
The tier fixes the label, the counter, and whether a reviewer will read the item at all.

#### 9.1 · This is the thinnest guide in the outlet, by exemplar count
(so its numbers carry less weight than the six sections around it)
`NMI-appendix/style.md` opens by declaring it was extracted from 2 exemplar papers, where every other NMI section guide declares 8.
Its two measured papers also diverge on the central question: serapio-garcia-2025 uses both tiers while qiao-2025 uses none, so the corpus offers no majority behaviour to imitate.
The 10-item cap survives that thinness because it is Nature portfolio policy rather than a measurement.
> ✎ The 10-item cap survives that thinness because it is Nature portfolio policy rather than a ~measurement, which is why~ *measurement. So* the guide keeps ~it while flagging~ *the cap, and still flags* its own exemplar for breaking it. · CC · 260802 1545
So the guide keeps the cap, and still flags its own exemplar for breaking it.

#### 9.2 · Format values
(every row here rests on two exemplars, and those two disagree, so the caveat is repeated rather than stated once)

```text
  📏 WORDS            prose metrics N/A, count items and not sentences · main
                      text 14-15 published pages · Extended Data typically
                      2-6 pages · Supplementary Information 20-60+ pages
                      [NMI-appendix/style.md "Length norms" + micro-norms
                       2026-07-08, FROM 2 EXEMPLARS where every sibling guide
                       declares 8, and the two disagree on tiers]
  📚 CITATION DENSITY N/A · appendix items are cross-referenced from the main
                      text, not cited in running prose
                      [NMI-appendix/style.md micro-norms 2026-07-08, FROM 2
                       EXEMPLARS where every sibling guide declares 8, and the
                       two disagree on tiers]
  🔢 VALUE DENSITY    not recorded by the pack · and the guide that would have
                      recorded it is the 2-exemplar one whose two papers
                      disagree on tiers
  📊 DISPLAYS         qiao-2025 0 Extended Data items, all back matter routed
                      to Supplementary · serapio-garcia-2025 11 items, being
                      4 ED figures + 7 ED tables, OVER the 10-item cap ·
                      main-text display items 5 figures each, plus serapio's
                      1 summary table
                      [NMI-appendix/style.md micro-norms 2026-07-08, FROM 2
                       EXEMPLARS where every sibling guide declares 8, and this
                       row IS the disagreement rather than a norm]
```

#### 9.3 · The language, in the papers' own words
(this guide carries no Signature moves block and no Exemplar sentences block, so these come from its cross-reference section, and from two papers only)
"Further statistical details are available in Supplementary Information section 1." [gu-2026]
The pointer written inside a clause, carrying the full label, which is the naming rule this division records.
> ✎ The ~clause-integrated pointer,~ *pointer written inside a clause,* carrying the full label, which is the naming rule this division records. · CC · 260802 1545
"see Supplementary Note A.1.2 on the background of personality science" [serapio-garcia-2025]
The inline directive, hierarchically numbered, and the form the related-work unit's fourth destination arrives in.
"results are summarized in Table 1 and raw reliability data are provided in Extended Data Tables 1 and 2" [serapio-garcia-2025]
One sentence naming a main-text table and a Tier 1 item together, which shows the two counters running side by side without merging.
"Extended data is available for this paper at [DOI]." [serapio-garcia-2025]
The Additional information availability line, present only when Tier 1 is used, and therefore absent from gu-2026, which uses none.
Three of these four are the same paper, because the guide has only two, which is the thinness 9.1 records showing up in its quotations as well as in its numbers.

## Aims

### A1 · 🔀 The bar is both halves: the method AND the impact
- A1.1 · An ML-shaped candidate is scored on both halves rather than on novelty.
  **Done when:** a paper missing the impact half is not shortlisted here.

### A2 · 🔀 Where a rejected NMI paper goes
- A2.1 · The rejection-to-destination routing is available to the venue stage.
  **Done when:** a rejection from this desk produces the next outlet rather than a restart.

### A3 · 📝 The abstract is one unstructured paragraph
- A3.1 · An NMI abstract draft can be judged against the pack without opening the pack.
  **Done when:** a 300-word draft, a labeled-field draft, or one carrying a citation command is caught on this page rather than at CHECK.

### A4 · 🔻 The introduction is a funnel that ends on the contribution
- A4.1 · The background-to-contribution citation split is known before an introduction is drafted.
  **Done when:** a draft introduction holds 2-3 references in its contribution paragraph and the rest in its background paragraphs.
- A4.2 · The two conflicting paragraph counts inside `NMI-introduction/style.md` are visible to whoever quotes one.
  **Done when:** a drafter citing a paragraph count names which block of that file it came from.

### A5 · 🧭 Related work is three destinations, not a section
- A5.1 · No NMI draft opens a standalone Related Work heading.
  **Done when:** the related-work unit produces three addressed blocks and the manuscript gains no heading.

### A6 · 🔬 Methods is last, and it is where the equations live
- A6.1 · The two outlet mechanics are stated where a drafter meets them, not only in the pack.
  **Done when:** a Methods draft carries no author-year citation and no LaTeX equation body, and every equation reads as prose plus a variable list plus an "(Eq. k)" marker.
- A6.2 · The unplaced third of the evaluation apparatus is on the record.
  **Done when:** a paper aimed here decides where its failure analysis goes, rather than dropping it because no section guide asks for it.

### A7 · 📊 Results is the longest section and every heading is a claim
- A7.1 · A Results plan is checkable against the venue before any prose exists.
  **Done when:** a neutral subsection heading, a main-text stat table, or a figure-free result subsection is caught at plan time.
- A7.2 · The strict figure-subsection mapping is used as a target, not as a measured fact.
  **Done when:** a Results layout that runs 1.5 subsections per figure is not rejected on the strength of a rule three exemplars break.

### A8 · 🎬 Discussion is short, pairs every limitation, and never ends on one
- A8.1 · Every limitation in a draft Discussion carries its own future direction.
  **Done when:** the limitations paragraph has as many forward moves as admissions, and the section closes on significance.

### A9 · 🗄 The back matter is two tiers with independent counters
- A9.1 · The tier decision is made before the display units are built.
  **Done when:** each planned back-matter item carries its tier and its full label, and the Extended Data count is at most 10.

## States

### A1 · 🔀 The bar is both halves: the method AND the impact
- ⬜ A1.1 · Not started. Both halves are prose in `NMI/taste.md`.

### A2 · 🔀 Where a rejected NMI paper goes
- ⬜ A2.1 · Not started. The routing is written here for the first time.

### A3 · 📝 The abstract is one unstructured paragraph
- ⬜ A3.1 · Not started. The budget, the sentence pattern and the zero-citation measurement are on the page; no draft has been scored against them.

### A4 · 🔻 The introduction is a funnel that ends on the contribution
- ⬜ A4.1 · Not started. The split is recorded from the reference-density table in `NMI-related-work/style.md`.
- ⬜ A4.2 · Not started. Both counts are on the page and neither has been raised with the pack's owner.

### A5 · 🧭 Related work is three destinations, not a section
- ⬜ A5.1 · Not started. The three destinations are recorded; the DRAFT-gate confirmation lives in `NMI-related-work/template.md` and has not been exercised here.

### A6 · 🔬 Methods is last, and it is where the equations live
- ⬜ A6.1 · Not started. Both mechanics are written into division 6; no Methods draft exists to test them on.
- ⬜ A6.2 · Not started. The gap is recorded: failure analysis appears in `taste.md` and in none of the seven section guides.

### A7 · 📊 Results is the longest section and every heading is a claim
- ⬜ A7.1 · Not started. The heading rule, the table rule and the figure rule are on the page.
- ⬜ A7.2 · Not started. The clash between `NMI-results/template.md` and its own style file's table is recorded and unresolved.

### A8 · 🎬 Discussion is short, pairs every limitation, and never ends on one
- ⬜ A8.1 · Not started. The pairing rule and the three title variants are recorded.

### A9 · 🗄 The back matter is two tiers with independent counters
- ⬜ A9.1 · Not started. The tiers, counters and triage rule are recorded; the 10-item cap has no checker behind it.

## Files

- `../../paper/venue/playbook-nature-portfolio/NMI/taste.md` · the desk signals and the one-sentence test
- `QBv8-npj-digital-medicine.md` · where a dataset-only paper goes when the claim becomes clinical
- `QBv1-misq.md` · the desk that refuses outright what this one accepts

<!-- exemplars:begin -->

📚 **Exemplars** · 20 papers on disk · the section guides were mined from 2 to 8 of them, so 12 stored papers back no norm, regenerated by `sync-exemplars.py`

- `../../paper/venue/playbook-nature-portfolio/NMI/examples/andani-2025-natmi-histopathology-protein-dl.pdf` · Andani 2025
- `../../paper/venue/playbook-nature-portfolio/NMI/examples/augustine-2026-natmi-immunotherapy-drug-target-ml.pdf` · Augustine 2026
- `../../paper/venue/playbook-nature-portfolio/NMI/examples/butt-2026-natmi-meta-learning-foundation-prediction.pdf` · Butt 2026
- `../../paper/venue/playbook-nature-portfolio/NMI/examples/chen-w-2025-natmi-interaction-discovery-ml.pdf` · Chen-W 2025
- `../../paper/venue/playbook-nature-portfolio/NMI/examples/deltadahl-2025-natmi-blood-cell-morphology-dl.pdf` · Deltadahl 2025
- `../../paper/venue/playbook-nature-portfolio/NMI/examples/doerig-2025-natmi-visual-brain-aligned-llm.pdf` · Doerig 2025
- `../../paper/venue/playbook-nature-portfolio/NMI/examples/eloff-2025-natmi-instanovo-peptide-sequencing.pdf` · Eloff 2025
- `../../paper/venue/playbook-nature-portfolio/NMI/examples/gu-2026-natmi-cardiac-multimodal-foundation-model.pdf` · Gu 2026
- `../../paper/venue/playbook-nature-portfolio/NMI/examples/ing-2025-natmi-multimodal-cancer-latent-variable.pdf` · Ing 2025
- `../../paper/venue/playbook-nature-portfolio/NMI/examples/karthikeyan-2025-natmi-tcr-generation.pdf` · Karthikeyan 2025
- `../../paper/venue/playbook-nature-portfolio/NMI/examples/mataraso-2025-natmi-ml-ehr-omics-analysis.pdf` · Mataraso 2025
- `../../paper/venue/playbook-nature-portfolio/NMI/examples/medany-2025-natmi-rl-ultrasound-microrobots.pdf` · Medany 2025
- `../../paper/venue/playbook-nature-portfolio/NMI/examples/mon-williams-2025-natmi-embodied-llm-robots.pdf` · Mon-Williams 2025
- `../../paper/venue/playbook-nature-portfolio/NMI/examples/morehead-2026-natmi-dl-protein-ligand-docking.pdf` · Morehead 2026
- `../../paper/venue/playbook-nature-portfolio/NMI/examples/pontikos-2025-natmi-retinal-disease-phenotyping-ml.pdf` · Pontikos 2025
- `../../paper/venue/playbook-nature-portfolio/NMI/examples/qiao-2025-natmi-personalized-heart-dynamics-model.pdf` · Qiao 2025
- `../../paper/venue/playbook-nature-portfolio/NMI/examples/serapio-garcia-2025-natmi-psychometric-personality-llms.pdf` · Serapio-Garcia 2025
- `../../paper/venue/playbook-nature-portfolio/NMI/examples/torres-2026-natmi-generative-ai-peptide-antibiotic.pdf` · Torres 2026
- `../../paper/venue/playbook-nature-portfolio/NMI/examples/wang-2026-natmi-synthetic-xray-medical-devices.pdf` · Wang 2026
- `../../paper/venue/playbook-nature-portfolio/NMI/examples/wohlwend-2025-natmi-dl-tcell-epitope-prediction.pdf` · Wohlwend 2025

- `../../paper/venue/playbook-nature-portfolio/NMI/examples/INDEX.md` · the pack's own manifest, not an exemplar

<!-- exemplars:end -->

<!-- kinds:begin -->

📐 **Section kinds** · 7 declared in `stages/section-kinds.yml`, regenerated by `sync-exemplars.py`

`section-edit` runs once per kind, and writes one page each. That is 6 numbered `S-Main-<n>` pages, plus `S-Appendix-<letter>`.

- `S-Main-0` · abstract
- `S-Main-1` · introduction
- `S-Main-2` · related-work
- `S-Main-3` · methods
- `S-Main-4` · results
- `S-Main-5` · discussion
- `S-Appendix-A` · appendix

A kind is the SMALLEST unit a paper gets here, not a ceiling.
One kind can spread across several numbered Main pages.
This repo's own MISQ paper runs to `S-Main-8-conclusion`, and the numbers above move with it.
The ORDER does not move. It is this venue's reading order, not a house default.

<!-- kinds:end -->

🔗 **Authority** · the venue's own instructions, fetched and verified 260802

- [Submission guidelines](https://www.nature.com/natmachintell/submission-guidelines) · the per-journal door, which routes to two pages that matter here. [Formatting your initial submission](https://www.nature.com/natmachintell/submission-guidelines/initial-formatting) governs what is sent first: "We accept initial submissions in PDF, Word or TeX/LaTeX formats; if you are using TeX/LaTeX, please submit compiled PDFs." [AIP and formatting](https://www.nature.com/natmachintell/submission-guidelines/aip-and-formatting) governs the accepted manuscript: "Please submit your manuscript in either Word or TeX/LaTeX format. We do not accept PDFs for final submissions." That second page is portfolio boilerplate served per journal: it is about 98% identical to the same page at Nature Medicine and Nature Human Behaviour once the journal name is substituted, so its rules bind all three.
- [Content types](https://www.nature.com/natmachintell/content) · per journal, and the only place the limits differ from the siblings. An Article takes a main text of up to 3,500 words excluding abstract, Methods, references and figure legends, which is the tightest of the four Nature-branded outlets in this group, an abstract of up to 150 words and unreferenced, up to 6 display items (figures and/or tables), and around 50 references as a guideline. There is no Brief Communication here and no short primary format at all: the submittable types are Article, Analysis, Correspondence, Review, Perspective, Comment, Matters Arising and the Reusability Report, and that last one is not a shorter tier but a subtype, "Articles that specifically test the robustness and reusability of previously published code".
- [Springer Nature LaTeX author support](https://www.springernature.com/gp/authors/campaigns/latex-author-support) · the published LaTeX package, and this journal sends authors to exactly this address, saying they may go there to "download the Springer Nature LaTeX template". A journal-specific class file does not exist; the instruction is "To submit a TeX/LaTeX file, please use any of the standard class files such as article.cls, revtex.cls or amsart.cls." The template itself is portfolio-wide and wider, usable "for any Springer Nature journal inclusive of Springer, Nature Portfolio, and BMC".
- Tiers, and both claims this board makes · the 10-item Extended Data cap is CONFIRMED at source, and this outlet is one of the two the pack cites as its origin, so the borrowing is now anchored rather than inherited. The journal's line is "A maximum of 10 Extended Data display figures is permitted." The unit is display FIGURES, not items, and the tier below it is subordinate to it, since "Supplementary Figures should be used only for cases when the use of Extended Data to report these findings is not appropriate." The no-standalone-Related-Work rule is CONFIRMED too, from an exhaustive list rather than a prohibition: "Article should be divided as follows: Introduction (without heading), Results, Discussion, Methods", followed by "Results and Methods should be divided by topical subheadings; the Discussion does not contain subheadings." Four blocks are permitted, none of them is prior work, and the two that host it may carry no heading of their own.

## Law

- NMI is the one desk in this tree where the method may be the contribution, and it still wants both halves: a method that advances what machines can do, AND impact that reaches beyond the ML community. Neither half alone is enough.
  The half that is missing names the outlet the paper actually belongs to. So a rejection here is a routing result rather than a dead end.

## Glossary

- **Both halves**: this desk's requirement that a paper carry both a novel method and demonstrated impact outside ML, unique in the venue tree.
- **Failure analysis**: the third element of the evaluation apparatus this desk names, alongside ablations and strong baselines.

## Log

260802 · Opened with the QBv outlet pages, from `playbook-nature-portfolio/NMI` at `Venue-Paper@fe25a88`.
260802 · Added divisions 3-9, one per section kind, from the seven `NMI-<kind>/style.md` + `template.md` pairs.
  Folded in the retired family page, `playbook-nature-portfolio/README.md` + `style-profile.md`.
  Relaxed the Writing Style bullet to allow a number carrying its source.
  Recorded three clashes: the related-work name against the pack's no-standalone rule, the introduction paragraph count against itself, and the results figure mapping against its own exemplar table.
  Recorded one hole: failure analysis has no section guide.
260802 · Added an 🔗 Authority block to `## Files`, from the journal's own pages fetched and verified that day.
  This outlet is one of the two the pack names as the origin of the 10-item Extended Data cap.
  The journal states it directly, as "A maximum of 10 Extended Data display figures is permitted".
  So the borrowing is anchored rather than inherited, and its unit is display FIGURES rather than items.
  It CONFIRMS the no-standalone-Related-Work rule from an exhaustive four-block Article division.
  That resolves the first of the three clashes the entry below records.
  On LaTeX: TeX/LaTeX at both stages, no journal class file, and the journal's own link to the Springer Nature LaTeX template, whose URL is now recorded.
260802 · Added 14 subsubsections, two per section-kind division.
  The first is a `Format values` block quoting WORDS, CITATION DENSITY, VALUE DENSITY and DISPLAYS, with each figure's source named inline.
  The second is a `The language, in the papers' own words` block quoting 4-5 attributed sentences per kind from the guides' own Signature moves and Exemplar sentences.
  Nothing was measured from a paper: `examples/` holds PDFs only, so every number is quoted from an `NMI-<kind>/style.md` block.
  Recorded a second hole across all seven kinds.
  VALUE DENSITY is the per-sentence count of numeric values in prose that this repo marks with `{VAL:?}`.
  It is recorded by only 2 of the 95 style.md files in the venue tree, and by none of this outlet's seven.
  Both sit at JAMA flagship, and both call it `Estimate density` (`jama-results/style.md:114`, `jama-letter/style.md:119`).
  That bites hardest in an ML Results section where the benchmark numbers are the evidence.
  The seven guides record only words per sentence and citations per sentence.
260802 1545 · Rewritten for a reader whose English is weak, with `haipipe-writing`.
  Twenty `> ✎` word-level records in all.
  They cover the Opening lead, one sentence in its More details part, and four figure readbacks that bolted a clause onto a finished sentence.
  The other fourteen are Content sentences that ran long, or did the same.
  The Opening lead now answers its own question on stage.
  It used to end on "What is that second question?", so a reader had to click to learn what the second demand was.
  The three long entries above were split into indented continuation lines, which the Log renderer joins back into one entry each, so what they record is unchanged.
  Those three carry no `> ✎` record, and this entry is their record instead.
  A record placed inside a Log entry sets the renderer's continuation state to none.
  Every line under it then falls out of the entry and renders as a loose paragraph with no date.
  That is a defect in `src/body.py`, not in the entries, and it is left for the page that owns the renderer.
  This page's own word `the conjunction` is retired in favour of `both halves` and `the method AND the impact`.
  It was replaced in seven places: the Writing Style rule, division 1, the matching Aims and States groups, the `A1.1` State row, the Law and the Glossary entry.
  Those seven sit in a heading, a bullet or a list row, which `cli/wdiff.py` will not anchor a record under, so this entry is their record.
  No number, no `style.md` line reference and no exemplar name was changed.
