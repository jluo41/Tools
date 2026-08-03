# Diabetes Care: the outlet whose requirements a machine could actually check

state: 🟡 PARTIAL · 25 exemplars · 6 sections · taste ✓ · the eight-item apparatus delta is enforced by nothing
owner: JL
method: state what the Diabetes Care desk wants, and record that its apparatus requirements are the one venue knowledge in this tree that is mechanically checkable

## Opening

Eight of the things Diabetes Care asks for are exact words on the page, so why does nothing check them?
> ✎ *Eight of the things Diabetes Care asks for are exact words on the page, so why does nothing check them?* Every other outlet page in this group ends ~with~ *in* a judgement a ~human~ *person* has to make. This one does ~not:~ *not. The abstract headings are fixed. So is the name of the methods section. A machine can compare those words against a manuscript and answer yes or no. This page writes the* eight ~of this desk's requirements are string-level facts about~ *down, and records that nothing in* the ~manuscript. So why is none of them checked?~ *lifecycle reads them.* · CC · 260802 1543
Every other outlet page in this group ends in a judgement a person has to make. This one does not.
The abstract headings are fixed. So is the name of the methods section. A machine can compare those words against a manuscript and answer yes or no.
This page writes the eight down, and records that nothing in the lifecycle reads them.

**Where this page sits**: it is one venue target in `QBv`, and the only one in its pack.
This page owns only what is true of `playbook-medical-journals/diabetes-care/`.

**Why this outlet is the natural first consumer of a conform pass**: its apparatus delta is a third kind of venue knowledge, distinct from taste and from section style, and the only one a machine can verify.
Apparatus delta is this page's own term; the Glossary at the foot of the page says what it covers.
> ✎ ~This~ *Apparatus delta is this page's own term; the Glossary at the foot of the page says what it covers. Diabetes Care* is the outlet *where* that ~instantiates it.~ *third kind shows up first.* · CC · 260802 1543
Diabetes Care is the outlet where that third kind shows up first.

**What the desk itself wants**: outcomes. The recurring word across its six fit signals is a clinical outcome, and device accuracy alone does not clear it.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**Every number names its source inline**: a word budget, a paragraph count, or an item count may stand on this page, but only with the `diabcare-<section>/style.md` heading or the measured exemplar that produced it named on the same line, because an unsourced number reads as this page's own claim.

**Split the checkable from the judged**: this page's value is the boundary between them, and mixing the two loses it.

✅ `the abstract headings are ADA, not JAMA`  ❌ `the paper should follow ADA conventions`

## Diagram

**Eight string-level requirements, and one judgement**: the rare desk where most of the bar is mechanical.

```text
  🤖 CHECKABLE WITHOUT JUDGEMENT
     ① ADA abstract headings ── OBJECTIVE / RESEARCH DESIGN
        AND METHODS / RESULTS / CONCLUSIONS
     ② Article Highlights, 4 narrative bullets
     ③ "RESEARCH DESIGN AND METHODS", not "Methods"
     ④ "Supplementary Material", not numbered Supplements
     ⑤ Vancouver numbered references
     ⑥ figure captions use the em-dash separator
     ⑦ ADA Standards of Care cited
     ⑧ CGM vocabulary used, not defined
        TIR  time in range          TBR  time below range
        TAR  time above range       GMI  glucose management indicator
        AGP  ambulatory glucose profile
        MARD mean absolute relative difference

  🧠 JUDGED
     🎯 "Does this change how we monitor, treat, or think
         about diabetes care for the patient in front of us?"

  ✅ FIT ── the recurring word is OUTCOMES
     CGM / digital diabetes tech validated on HbA1c, TIR,
       hypoglycemia events
     large registry or claims evidence
     ADA Standards of Care alignment
     health equity in diabetes
     AI/ML with PROSPECTIVE clinical-workflow validation
     real-world CGM / pump / closed-loop at scale

  📊 25 exemplars · 6 sections
```

## Content

### 1 · Eight requirements a conform pass could enforce today

**Nothing in the lifecycle looks at any of them**: and all eight fail silently on a retarget from JAMA.

```text
  💥 the silent-failure property
     a paper retargeted from JAMA Internal Medicine keeps its
     argument intact and its apparatus wrong, and it READS
     fine at every stage that checks prose

  🤖 what a check would need
     ── the pinned outlet (already on S-Venue-0)
     ── the eight strings (already in the pack README)
     ── nothing else

  ⚠️ so the gap is not knowledge and not design, it is that
     no one has written the pass
```

🤖 Establishes the check as buildable from artifacts that already exist.
> ✎ 🤖 Establishes the check as buildable from artifacts that already ~exist, which~ *exist. That* is what makes this outlet the ~right~ first ~consumer.~ *place to build one.* · CC · 260802 1543
That is what makes this outlet the first place to build one.

#### 1.1 · The em-dash separator is the one item worth naming twice
(because this repo's own writing rule forbids em-dashes and this venue requires one)
Diabetes Care figure captions take the form `Figure 1--Caption text.` with an em-dash separator.
A blanket em-dash removal applied to a manuscript pinned here would break a venue requirement.
> ✎ A blanket em-dash removal applied to a manuscript pinned here would break a venue ~requirement, which is exactly why~ *requirement. So* the delta belongs in a ~check and~ *check,* not in a habit. · CC · 260802 1543
So the delta belongs in a check, not in a habit.

### 2 · The desk wants an outcome, and pairs with npj Digital Medicine

**Device accuracy does not clear it**: the same rejection npj Digital Medicine makes, scoped to one disease.

```text
  💻 npj DM        rejects accuracy tables with no clinical
                   utility
  💉 Diabetes Care rejects device accuracy with no clinical
                   outcome

  🔗 so the two are a ROUTING PAIR, not alternatives
     a paper failing one usually fails the other
     ── and a paper clearing one is a live candidate at both

  🔀 what separates them
     💻 npj DM        ── any disease, digital tool angle
     💉 Diabetes Care ── diabetes only, ADA guideline angle
```

🔗 Establishes the routing pair, a term the Glossary at the foot of this page defines.
> ✎ 🔗 Establishes the *routing* pair, ~and~ *a term the Glossary at the foot of this page defines. It also establishes* the disease-versus-tool ~axis that separates them, which~ *split between the two outlets. That split* is the routing question a digital-diabetes paper actually faces. · CC · 260802 1543
It also establishes the disease-versus-tool split between the two outlets.
That split is the routing question a digital-diabetes paper actually faces.

### 3 · The abstract is four ADA labels and a four-bullet Highlights box

**Four labels, and a machine can read every one of them**: OBJECTIVE, RESEARCH DESIGN AND METHODS, RESULTS, CONCLUSIONS, in that order, with no fifth.

```text
  📐 ARC ── the four labels, in fixed order
     OBJECTIVE            context/need + study aim
     RD AND METHODS       design + source + population + key method
     RESULTS              N + demographics -> effect (CI/P) -> secondary
     CONCLUSIONS          finding restated + clinical implication

  📏 BUDGET ── diabcare-abstract/style.md "Word budget"
     Original Article     200-250 w, journal cap 250
     Brief Report         ~150-200 w
     e-Letter             no abstract, body text begins directly

  📊 MEASURED 2026-07-08 ── same file, "Micro-norms"
     Reaven 2026          245 w · 11 sent · Original Article, at the cap
     Galindo 2026         ~180 w · 8 sent · Brief Report
     OBJECTIVE            1 sent both · Reaven 26 w · Galindo 21 w
     RD AND METHODS       Reaven 4 sent / 88 w · Galindo 2 sent / 41 w
     RESULTS              Reaven 5 sent / 110 w · Galindo 2 sent / ~80 w
     CONCLUSIONS          Reaven 1 sent / 21 w · Galindo 3 sent / 42 w
     longest label        RESULTS, ~45% of Reaven's words
     citation markers     0 in either abstract

  🤖 STRING-LEVEL IN THIS SECTION
     ① the four label strings, and their order
     ① no IMPORTANCE label present anywhere
     ② four Article Highlights question strings, verbatim
     ⑤ zero Vancouver markers inside the abstract
```

📋 Establishes the abstract as the densest checkable block in the manuscript, and the one section where the article type moves the cap without moving the shape.

#### 3.1 · The OBJECTIVE opener, as four slots
(style.md "Signature moves" item 1, lines 61-65, each shape named against the exemplar it came from)
The pack names four opener shapes and a writer picks exactly one.
A stated need reads `There is a need for <tool> for <population with condition>.`, from Galindo 2026.
A known-then-gap reads `<Technology> improves <X> and reduces <Y>, but data are lacking for <role in Z>.`, from Reaven 2026.
A direct infinitive reads `To characterize <quantity> in <population> and to examine <association>.`, from Godneva 2026.
A hazard-then-aim pair puts one clinical-hazard sentence in front of `We aimed to develop <approach> for <task>.`, from Lehmann 2026.
Filling a slot is the move; lifting an exemplar's own words is not, because the register transfers between papers and the clinical content does not.

#### 3.2 · The other three labels, as slots
(style.md "Signature moves" items 2 to 5, lines 67-73)
RESEARCH DESIGN AND METHODS names the design in its opening sentence, `We conducted a <design> analysis using <data source>.`
> ✎ RESEARCH DESIGN AND METHODS names the design in its opening sentence, `We conducted a <design> analysis using <data ~source>.`, and the~ *source>.` The* pack's four exemplars differ only in which design word fills that slot. · CC · 260802 1543
The pack's four exemplars differ only in which design word fills that slot.
RESULTS leads with the sample, `Of the <N> individuals <assigned>, <n> were <included>.` or `<N> individuals were included (<n> female, age <M> years, HbA1c <M>%).`
Effects take the form `<estimate> (95% CI <lo>-<hi>)` or `<mean> vs. <mean>; P = <p>`, never a bare P value.
CONCLUSIONS restates design and finding, `In <population or design>, <outcome> was <verb> <exposure>.`, then adds one implication sentence.

#### 3.3 · The Article Highlights box is four questions, printed as strings
(the ADA's replacement for the JAMA Key Points box, README "Key differences" line 14)
The four labels are fixed text rather than paraphrases.
> ✎ The four labels are fixed text rather than ~paraphrases:~ *paraphrases. They read* `Why did we undertake this study?`, `What is the specific question we wanted to answer?`, `What did we find?`, and `What are the implications of our findings?` · CC · 260802 1543
They read `Why did we undertake this study?`, `What is the specific question we wanted to answer?`, `What did we find?`, and `What are the implications of our findings?`
The pack budgets them at 1-2 sentences, 1 sentence, 2-3 sentences carrying numbers, and 1-2 sentences (style.md lines 25-29).
Each answer is full narrative prose.
> ✎ Each answer is full narrative ~prose, where a~ *prose. A* JAMA Key Points box *instead* carries three labelled ~one-liners~ *one-liners,* under Question, Findings, and ~Meaning, which is why~ *Meaning. So* a retarget cannot map one box onto the other. · CC · 260802 1543
A JAMA Key Points box instead carries three labelled one-liners, under Question, Findings, and Meaning.
So a retarget cannot map one box onto the other.
The box is present on Original Articles and Brief Reports and absent on e-Letters and Observations, so its absence is a defect only once the article type is known.

#### 3.4 · Anti-patterns, and what the article type changes
(style.md "Anti-patterns" lines 75-84, read against the README article-type table)
The pack names eight failures here.
> ✎ The pack names eight failures ~here:~ *here. The first four:* opening OBJECTIVE with the study description before the clinical context, adding a JAMA IMPORTANCE heading, reporting P values without effect sizes, *and* using causal verbs on an observational ~design,~ *design. The last four:* writing CONCLUSIONS past what the data show, burying the sample size in the middle of RESULTS, leaving an abbreviation undefined inside the abstract, and using any JAMA-style header. · CC · 260802 1543
The first four: opening OBJECTIVE with the study description before the clinical context, adding a JAMA IMPORTANCE heading, reporting P values without effect sizes, and using causal verbs on an observational design.
The last four: writing CONCLUSIONS past what the data show, burying the sample size in the middle of RESULTS, leaving an abbreviation undefined inside the abstract, and using any JAMA-style header.
Two of the eight are string tests and six are readings, which is the same split this whole page is about.
The article type moves the budget and not the arc: the README table gives an Original Article ~4000 body words and ~40 references, a Brief Report ~2500 and ~20, and an e-Letter or Observation ~1000 words of unstructured running text with ~5 references and therefore no abstract and no Highlights box at all.
That table hedges its own display cap with "verify current author guidelines".
> ✎ That table hedges its own display cap with "verify current author ~guidelines", so~ *guidelines". So* the four-display figure is an expectation this page ~carries and~ *carries,* not a gate it can enforce. · CC · 260802 1543
So the four-display figure is an expectation this page carries, not a gate it can enforce.

#### 3.5 · Format values
(the four format metrics for this section, each value naming the pack line that records it, and one metric recorded nowhere in the tree)

```text
  📏 WORDS            Original Article 200-250 w, journal cap 250 · 245 w / 11 sentences measured in Reaven 2026
                      Brief Report ~150-200 w · ~180 w / 8 sentences measured in Galindo 2026
                      no paragraph count applies, since the abstract is one block under each of the four labels
                      [diabcare-abstract/style.md "Word budget", "Micro-norms", "Paragraph structure"]
                      expectation, not a gate: style-profile.md leaves "Exact word limits per article type" unchecked
  📚 CITATION DENSITY 0 markers per sentence, in both measured abstracts
                      [diabcare-abstract/style.md "Micro-norms", Citations row]
  🔢 VALUE DENSITY    not recorded by the pack
  📊 DISPLAYS         0 figures and 0 tables inside the abstract itself
                      the Article Highlights box and the graphical abstract page print before it
                      caps 4 for an Original Article · up to 3 total for a Brief Report · 1-2 for an e-Letter
                      those caps bound main-text displays across the manuscript, not this section
                      [README "Article types in Diabetes Care" table, and README's Display mapping]
                      expectation, not a gate: the README hedges its own cap with "verify current author guidelines"
```

Each word figure is the pack's stated range, followed by what the pack actually measured.
> ✎ Each word figure is the pack's stated ~range~ *range,* followed by what the pack actually ~measured, which is how~ *measured. Read that way,* the Original Article number ~turns out to sit~ *sits* exactly at its ~cap while~ *cap, and* the Brief Report number sits inside its range. · CC · 260802 1543
Read that way, the Original Article number sits exactly at its cap, and the Brief Report number sits inside its range.
Neither figure is a limit the desk publishes here, so both rows are expectations this page carries rather than gates it can enforce.

#### 3.6 · The language, in the papers' own words
(five sentences the pack itself quotes, one per abstract slot named in 3.1 to 3.3)

"There is a need for improved glycemia monitoring tools for people with type 2 diabetes (T2D) and end-stage kidney failure (ESKF)." [Galindo 2026]
The stated-need OBJECTIVE opener, the first of the four shapes in 3.1.

"Use of continuous glucose monitors (CGM) improves glucose control and reduces hypoglycemia, but data are lacking for its possible role in reducing other serious clinical events." [Reaven 2026]
The known-then-gap opener, the second shape in 3.1, which carries its adversative inside a single sentence.

"Twenty-two individuals were included (11 female, age 37.3 +/- 12.4 years, HbA1c 7.1 +/- 0.5%)." [Lehmann 2026]
The RESULTS lead that puts the sample first, filling the second of the two sample slots in 3.2.

"In this large TTE of CGM initiation in older T1D patients, CGM use was associated with reduced risk for all-cause mortality." [Reaven 2026]
The CONCLUSIONS restatement, design name then finding, the last slot in 3.2 and the one that carries associational language on an observational design.

"Would the use of rtCGM improve glycemic outcomes in patients with insulin-treated T2D undergoing hemodialysis?" [Galindo 2026]
The answer to the second Article Highlights question, written as narrative prose rather than the labelled one-liner a JAMA Key Points box takes, which is the whole point of 3.3.

### 4 · The introduction is untitled and turns on one adversative

**No heading is printed above it**: the section runs straight into the manuscript, and its whole load-bearing move is one pivot word.

```text
  📐 ARC ── diabcare-introduction/style.md "Arc"
     P1 context     clinical or technology domain at population scale
     P2 known       prior evidence, guidelines, existing approaches
     P3 gap         the adversative pivot: However / but / Yet / Despite
     P4 aim         what we did, first person plural
     P5 scope       optional secondary aim or scope narrowing

  📏 BUDGET ── same file, "Word budget"
     Original Article     250-1000 w · 2-5 ¶
     Brief Report         70-300 w · 1 ¶, context to gap to aim in one run
     e-Letter             ~200-400 w · 1-2 ¶, flows into methods

  📊 MEASURED 2026-07-08 ── same file, "Micro-norms"
     Reaven 2026          255 w · 2 ¶ · 5 and 5 sentences
     Galindo 2026         68 w · 1 ¶ · 3 sentences
     words per sentence   13-39, median ~23
     Reaven citations     ~6 markers / 10 distinct refs over 10 sentences
     Galindo citations    1 marker, refs 1-3, at the first sentence end
     placement            clustered at sentence ends, both papers

  🤖 STRING-LEVEL IN THIS SECTION
     ⑦ an ADA Standards of Care citation present
     ⑤ Vancouver markers, parenthetical (1), (2,3), (1-5)
     ⚠️ the adversative pivot word, once the gap sentence is located
```

🧭 Establishes the introduction as the one body section whose measured exemplars ran at half the budget the pack first stated.
> ✎ 🧭 Establishes the introduction as the one body section whose measured exemplars ran at half the budget the pack first ~stated, which~ *stated. That correction* is why its stated range is so wide. · CC · 260802 1543
That correction is why its stated range is so wide.

#### 4.1 · Signature moves, as slots
(style.md "Paragraph-by-paragraph structure" lines 33-84)
P1 opens on the technology rather than on a burden statistic: `<Technology> has been shown to improve <outcome> and reduce <event> in people with <condition>.`, from Reaven 2026.
> ✎ P1 opens on the technology rather than on a burden ~statistic,~ *statistic:* `<Technology> has been shown to improve <outcome> and reduce <event> in people with <condition>.`, from Reaven ~2026; the~ *2026. The* pack calls this technology-first ~framing~ *framing,* and contrasts it with the JAMA habit of leading on prevalence. · CC · 260802 1543
The pack calls this technology-first framing, and contrasts it with the JAMA habit of leading on prevalence.
P2 positions the study against a guideline, `The American Diabetes Association "Standards of Care in Diabetes" has recommended <recommendation>.`, from Zheng 2025.
P3 carries the pivot plus one of four stock gap phrases.
> ✎ P3 carries the pivot plus one of four stock gap ~phrases,~ *phrases. It reads* `However, there are very limited data on <relationship>.` or `However, the application of <method> to <task> remains unexplored.`, from Reaven 2026 and Zheng 2025. · CC · 260802 1543
It reads `However, there are very limited data on <relationship>.` or `However, the application of <method> to <task> remains unexplored.`, from Reaven 2026 and Zheng 2025.
P4 connects gap to design with a conjunction, `We therefore used <data source> to <estimate what>.` or `Thus, we aimed to evaluate <aim>.`, and the verb stays descriptive rather than causal.

#### 4.2 · Anti-patterns, and the one the pack contradicts itself on
(style.md "Anti-patterns" lines 100-109, read against its own micro-norm note at line 124)
The pack names eight.
> ✎ The pack names ~eight:~ *eight. The first four:* a textbook-definition opening, more than two paragraphs of known material before the gap, a causal hypothesis on observational data, *and* methods detail beyond a brief design ~mention,~ *mention. The last four:* a gap sentence with no adversative, a results preview, an omitted ADA Standards citation where the topic touches a recommendation, and a passive aim statement. · CC · 260802 1543
The first four: a textbook-definition opening, more than two paragraphs of known material before the gap, a causal hypothesis on observational data, and methods detail beyond a brief design mention.
The last four: a gap sentence with no adversative, a results preview, an omitted ADA Standards citation where the topic touches a recommendation, and a passive aim statement.
The ADA item is the unstable one.
The same file records that neither measured exemplar carries an ADA Standards citation in its introduction, so the pack lists as near-mandatory a move both of its sampled papers skip.
That makes the ADA citation a manuscript-level string check, present somewhere in the paper, rather than an introduction-level one.

#### 4.3 · What the article type changes
(the README article-type table, and style.md's reconciliation note at lines 122-124)
A Brief Report collapses P1 through P4 into a single paragraph, which is how Galindo 2026 measures at 68 words against an Original Article's 255.
An e-Letter or Observation prints no heading and no separate introduction at all: the prose runs into methods and results as one unstructured body inside a ~1000-word limit.
The pack already reconciled this budget once, cutting the stated Original Article range from 600-1000 words to 250-1000 after both exemplars measured under it.
> ✎ The pack already reconciled this budget once, cutting the stated Original Article range from 600-1000 words to 250-1000 after both exemplars measured under ~it, and that~ *it. That* correction is why the range reads unhelpfully wide today. · CC · 260802 1543
That correction is why the range reads unhelpfully wide today.

#### 4.4 · Format values
(the same four metrics, for the one section whose stated budget the pack has already had to correct against measurement)

```text
  📏 WORDS            Original Article 250-1000 w · 2-5 ¶ · 255 w / 2 ¶ / 5 and 5 sentences measured in Reaven 2026
                      Brief Report 70-300 w · 1 ¶ · 68 w / 1 ¶ / 3 sentences measured in Galindo 2026
                      13-39 words per sentence, median ~23, across both papers
                      [diabcare-introduction/style.md "Word budget" and "Micro-norms"]
                      expectation, not a gate: style-profile.md leaves "Exact word limits per article type" unchecked
  📚 CITATION DENSITY Reaven 2026 ~6 markers over 10 sentences, about 0.6 per sentence, 10 distinct refs
                      Galindo 2026 1 marker over 3 sentences, refs 1-3, at the first sentence end
                      stated section expectation 8-15 references across 3-5 paragraphs
                      [diabcare-introduction/style.md "Micro-norms" Citations row, and "Signature moves" item 6]
  🔢 VALUE DENSITY    not recorded by the pack
  📊 DISPLAYS         0 figures and 0 tables, since the pack commissions no display from this section
                      caps 4 for an Original Article · up to 3 total for a Brief Report · 1-2 for an e-Letter
                      those caps bound main-text displays across the manuscript, not this section
                      [README "Article types in Diabetes Care" table]
                      expectation, not a gate: the README hedges its own cap with "verify current author guidelines"
```

The citation row is the only one here a writer can feel while drafting.
> ✎ The citation row is the only one here a writer can feel while ~drafting, since about~ *drafting. About* 0.6 markers per sentence in an Original ~Article~ *Article,* against one marker in a whole Brief ~Report~ *Report,* is a visible difference on the page. · CC · 260802 1543
About 0.6 markers per sentence in an Original Article, against one marker in a whole Brief Report, is a visible difference on the page.
The word row is the weakest expectation on this page, because the range only reads 250-1000 after the correction 4.3 records, and a range that wide fails nothing.

#### 4.5 · The language, in the papers' own words
(five sentences the pack quotes, one per paragraph slot in 4.1, including the pivot this whole division is named for)

"Continuous glucose monitoring (CGM) has been shown to improve glycemic control and reduce hypoglycemic events in people with type 1 diabetes (pwT1D) (1,2)." [Reaven 2026]
The technology-first P1 opener, which leads on the tool instead of on a burden statistic, the first slot in 4.1.

"The American Diabetes Association 'Standards of Care in Diabetes' has recommended the inclusion of standard AGP reports for glucose assessment (6)." [Zheng 2025]
The ADA-guideline framing that positions a study against a recommendation, the P2 slot in 4.1 and the move 4.2 shows the pack contradicting itself about.

"However, there are very limited data on the potential benefits of CGM use in pwT1D for all-cause mortality (10)." [Reaven 2026]
The single adversative that turns the introduction, the P3 pivot slot in 4.1, carrying the stock phrase "limited data" with it.

"Thus, we aimed to evaluate the accuracy of extracting CGM data using NLP." [Zheng 2025]
The P4 aim, tied to the gap by a conjunction and kept descriptive rather than causal, which is the fourth slot in 4.1.

"In the current work, we focus on how glycemic profiles are associated with each of the GRADE medications" [Bergenstal 2026]
The optional P5 scope narrowing, which appears only when a paper has a secondary aim to fence off from its main one.

### 5 · The methods section is named RESEARCH DESIGN AND METHODS

**The heading is itself the requirement**: the pack calls it the single most distinctive Diabetes Care convention, and it reduces to one string comparison.

```text
  📐 SUBSECTION ORDER ── diabcare-methods/style.md, four design families
     observational   Overview · Eligibility Criteria · Data Extraction ·
                     Outcomes · Statistical Analysis · [Sensitivity] · DRA
     RCT             Study Design · Study Population · Intervention ·
                     Study Outcomes · Statistical Analysis · DRA
     ML / AI / NLP   Study Design and Population · Procedures ·
                     Outcome and Sample Size · Analysis and ML · DRA
     cost-effect.    Overview · Setting · Markov Model · Efficacy ·
                     Complications · Mortality, Costs, QoL · Analyses · DRA
     DRA             Data and Resource Availability, always terminal

  📏 BUDGET ── same file, "Word budget"
     Original Article     1500-2500 w
     Brief Report         500-800 w, heavy Supplementary offloading
     e-Letter             ~300-500 w, no section heading

  📊 MEASURED 2026-07-08 ── same file, "Micro-norms"
     Reaven 2026          ~11-13 ¶ under 7 bold subheadings
     Galindo 2026         ~5 ¶ under 4 subheadings
     sentences per ¶      Reaven 3-10 median ~7 · Galindo 2-6 median ~4
     words per sentence   11-47, median ~22
     citations            Reaven ~0.2-0.3/sentence · Galindo 0
     citation kind        methodological only, never evidentiary

  🤖 STRING-LEVEL IN THIS SECTION
     ③ the heading reads RESEARCH DESIGN AND METHODS
     ③ never Methods, Materials and Methods, or Study Design
     ⑧ every CGM metric carries its mg/dL threshold
     ⚠️ Data and Resource Availability present, and last
```

🔬 Establishes the section carrying the most checkable structure, since both its heading string and its mandatory terminal subsection are fixed text.

#### 5.1 · Signature moves, as slots
(style.md "Opening paragraph pattern" lines 60-70 and "Signature moves" lines 110-120)
The first sentence names the design, `This study was a <design> of <population> (ClinicalTrials.gov identifier: NCT<number>).` from Galindo 2026, or `We conducted a <design> analysis using <data source>.` from Reaven 2026.
Ethics approval lands within the first two or three sentences, and the registration number sits parenthetically rather than in a sentence of its own.
A machine-learning or natural-language pipeline is written as numbered steps inside one sentence, `the steps of our algorithm pipeline consist of 1) <step>, 2) <step>, 3) <step>, and 4) <step>`, from Zheng 2025.
Statistical Analysis always carries four things: the model named, the adjustment set or a pointer to a Supplementary table, the software with its version, and the significance threshold where one applies.
Devices carry manufacturer and model, and every CGM metric carries its International Consensus threshold, `%TIR 70-180 mg/dL`, `%TBR <70 mg/dL`, `%TAR >180 mg/dL and >250 mg/dL`.

#### 5.2 · Anti-patterns
(style.md "Anti-patterns" lines 122-131)
Eight again, and three of them are string tests: the wrong section heading, a missing Data and Resource Availability subsection, and a CGM metric named with no mg/dL range attached.
The other five are readings.
> ✎ The other five are ~readings:~ *readings. Three concern the analysis:* a statistical method with no specific model named, a missing software version, ~results leaking into methods, future tense in place of past,~ and a missing trial registration number on a registered study. *Two concern the prose: results leaking into methods, and future tense in place of past.* · CC · 260802 1543
Three concern the analysis: a statistical method with no specific model named, a missing software version, and a missing trial registration number on a registered study.
Two concern the prose: results leaking into methods, and future tense in place of past.
The pack also records a JAMA contrast worth carrying.
> ✎ The pack also records a JAMA contrast worth ~carrying, that~ *carrying.* JAMA methods almost always name a reporting guideline in their opening ~sentences~ *sentences,* while only one of the ten Diabetes Care exemplars named one at all. · CC · 260802 1543
JAMA methods almost always name a reporting guideline in their opening sentences, while only one of the ten Diabetes Care exemplars named one at all.

#### 5.3 · What the article type changes
(style.md line 12 for the Brief Report budget, and "Supplementary Material offloading" lines 101-108)
A Brief Report does not write shorter methods so much as move them.
> ✎ A Brief Report does not write shorter methods so much as ~relocate them:~ *move them.* Galindo 2026 fits 500 to 800 words by pushing the full inclusion and exclusion ~criteria~ *criteria,* and the self-adjustment ~guidelines~ *guidelines,* into the Supplementary Material. · CC · 260802 1543
Galindo 2026 fits 500 to 800 words by pushing the full inclusion and exclusion criteria, and the self-adjustment guidelines, into the Supplementary Material.
That makes the appendix the release valve for this section, and a Brief Report with no supplementary package is usually a methods section nobody triaged.
An e-Letter carries no methods heading at all, and its roughly 300 to 500 words sit inside the running body text.

#### 5.4 · Format values
(the same four metrics, for the longest section in the manuscript and the one whose citations are structural rather than evidentiary)

```text
  📏 WORDS            Original Article 1500-2500 w · ~11-13 ¶ under 7 subheadings measured in Reaven 2026
                      Brief Report 500-800 w · ~5 ¶ under 4 subheadings measured in Galindo 2026
                      sentences per ¶ Reaven 3-10 median ~7 · Galindo 2-6 median ~4
                      11-47 words per sentence, median ~22, the longest being enumerated criteria lists
                      [diabcare-methods/style.md "Word budget" and "Micro-norms"]
                      expectation, not a gate: style-profile.md leaves "Exact word limits per article type" unchecked
  📚 CITATION DENSITY Reaven 2026 ~11 markers across the section, about 0.2-0.3 per sentence, methodological only
                      Galindo 2026 0 numbered citations, only a trial-registration number and Supplementary pointers
                      [diabcare-methods/style.md "Micro-norms", Citations row]
  🔢 VALUE DENSITY    not recorded by the pack
  📊 DISPLAYS         0 figures and 0 tables commissioned here, and the cohort flow figure is cross-referenced from Results
                      caps 4 for an Original Article · up to 3 total for a Brief Report · 1-2 for an e-Letter
                      those caps bound main-text displays across the manuscript, not this section
                      [README "Article types in Diabetes Care" table, and diabcare-results/style.md "Opening paragraph"]
                      expectation, not a gate: the README hedges its own cap with "verify current author guidelines"
```

The citation row is what separates this section from the introduction.
> ✎ The citation row is what separates this section from the ~introduction, since a~ *introduction. A* methods marker names an algorithm or a prior methods paper rather than supporting a ~finding, and a~ *finding. A* Brief Report ~can legitimately~ *may* carry none at ~all.~ *all, and that is not a defect.* · CC · 260802 1543
A methods marker names an algorithm or a prior methods paper rather than supporting a finding.
A Brief Report may carry none at all, and that is not a defect.
The word row is met by relocation rather than by compression, which 5.3 records, so a Brief Report near the top of its range usually has an untriaged Supplementary package behind it.

#### 5.5 · The language, in the papers' own words
(five sentences the pack quotes, one per slot in 5.1, from the design name down to the threshold that makes a CGM metric legible)

"This study was a crossover RCT of people with T2D and ESKF undergoing hemodialysis (ClinicalTrials.gov identifier: NCT04473430)." [Galindo 2026]
The design-first opener with the registration number sitting parenthetically rather than in a sentence of its own, the first slot in 5.1.

"Veterans were considered eligible for inclusion if they were >30 and <85 years of age, had T1D" [Reaven 2026]
The eligibility clause, which states its bounds as numbers rather than as prose criteria, the population slot the pack quotes twice.

"Weighted pooled logistic regression models with restricted cubic splines for time were then fitted within each treatment strategy" [Reaven 2026]
The named analytic model, first of the four things 5.1 requires every Statistical Analysis paragraph to carry.

"logistic regression (LR) with ridge regularization (C = 1, class weights = 1.0), random forest (number of estimators = 100)" [Lehmann 2026]
The machine-learning variant of that same slot, where naming the model expands into naming its hyperparameters.

"percentage time below range (%TBR) <70 mg/dL" [Galindo 2026]
The CGM metric written with its International Consensus threshold attached, which is the exact string A5.2 wants a check to look for.

### 6 · The results section carries the shortest sentences and the caption separator

**One result per sentence, and no citations at all**: every quantitative claim points at a numbered Table, Figure, or Supplementary item instead of at a reference.

```text
  📐 ARC ── diabcare-results/style.md "Subsection structure"
     1  Participant Characteristics  N + demographics + Table 1 + flow ref
     2  [primary outcome]            named for the outcome, not a hypothesis
     3  [secondary outcomes]         one result per sentence
     4  [subgroup / sensitivity]     heterogeneity, robustness, neg. controls

  📏 BUDGET ── same file, "Word budget"
     Original Article     1000-2000 w
     Brief Report         400-700 w, bold subheaders allowed
     e-Letter             ~300-600 w, continuous paragraphs

  📊 MEASURED 2026-07-08 ── same file, "Micro-norms"
     Reaven 2026          ~7-8 ¶ under 3 subheadings
     Galindo 2026         3 ¶, one opener plus 2 subsections
     sentences per ¶      Reaven 5-8 median ~7 · Galindo 3-8 median ~3
     words per sentence   8-35, median ~16, shortest of any section
     citations            0 markers in either Results section

  🤖 STRING-LEVEL IN THIS SECTION
     ⑥ figure captions read Figure 1--Caption text.
     ⑥ table captions read Table 1--Caption text.
     ⑧ TIR / TBR / TAR reported with their mg/dL ranges
     ⚠️ Fig. abbreviated in every cross-reference, main and supplementary
```

📊 Establishes the section where this repo's own em-dash ban would do real damage, since the caption separator here is a venue requirement rather than a house habit.

#### 6.1 · The caption separator, spelled out a second time
(item ⑥ of the eight, and the one requirement this repo's own writing rule collides with)
A Diabetes Care caption is written `Figure 1--Caption text.` and `Table 1--Caption text.`, with no space on either side of the separator.
The two-hyphen form is how the pack itself writes it on disk, and how this page must write it.
> ✎ The two-hyphen form is how the pack itself writes it on ~disk~ *disk,* and how this page must write ~it; the~ *it. The* printed journal sets the same separator as a dash, ~which~ *and that dash* is the character a repo-wide rule forbids in prose. · CC · 260802 1543
The printed journal sets the same separator as a dash, and that dash is the character a repo-wide rule forbids in prose.
That collision is exactly why the requirement belongs to a check that knows which outlet the manuscript is pinned to, rather than to a habit that applies everywhere.

#### 6.2 · Signature moves, as slots
(style.md "Opening paragraph" lines 41-53 and "Number formatting conventions" lines 62-73)
The opening paragraph reports the analytic N first, then demographics, then its cross-references.
> ✎ The opening paragraph reports the analytic N first, then demographics, then its ~cross-references,~ *cross-references. It reads* `Among <N> participants enrolled, <n> were included in the ~analysis.`~ *analysis.`,* followed by `The sample's mean age was <M> years, <p>% (n = <n>) were women (Table 1).` · CC · 260802 1543
It reads `Among <N> participants enrolled, <n> were included in the analysis.`, followed by `The sample's mean age was <M> years, <p>% (n = <n>) were women (Table 1).`
Numbers take fixed forms.
> ✎ Numbers take fixed ~forms: a~ *forms. A* mean and SD ~as~ *read* `<M> ± <SD>`, *and* counts ~as~ *read* `<n> ~(<p>)`,~ *(<p>)`.* P values *are* italic and ~without a~ *carry no* leading ~zero~ *zero,* as *in* `P = ~0.28`, and intervals as~ *0.28`. Intervals read* `95% CI ~<lo>-<hi>`~ *<lo>-<hi>`,* or the comma variant `(95% CI <lo>, <hi>)`. · CC · 260802 1543
A mean and SD read `<M> ± <SD>`, and counts read `<n> (<p>)`.
P values are italic and carry no leading zero, as in `P = 0.28`.
Intervals read `95% CI <lo>-<hi>`, or the comma variant `(95% CI <lo>, <hi>)`.
Null results carry their interval or P value and no softening, so a reader judges precision rather than tone.
The hero display for a CGM paper is a stacked bar of time in each glycemic range, printed in the standardized colors.
> ✎ The hero display for a CGM paper is a stacked bar of time in each glycemic range, *printed in the standardized colors. The bands are* Very Low under 54, Low 54 to 70, Target 70 to 180, High 180 to 250, and Very High over 250 ~mg/dL, in the standardized colors.~ *mg/dL.* · CC · 260802 1543
The bands are Very Low under 54, Low 54 to 70, Target 70 to 180, High 180 to 250, and Very High over 250 mg/dL.

#### 6.3 · Anti-patterns, and the clash the pack already resolved
(style.md "Anti-patterns" lines 123-132, and the CLASH note at line 147)
The pack names eight.
> ✎ The pack names ~eight:~ *eight. The first four:* interpreting inside Results, saying significant with no number attached, P values with no effect size, *and* methods statements in Results ~paragraphs,~ *paragraphs. The last four:* causal verbs on observational data, spinning a null result as a trend, burying the primary outcome behind secondary ones, and dropping the CGM threshold ranges. · CC · 260802 1543
The first four: interpreting inside Results, saying significant with no number attached, P values with no effect size, and methods statements in Results paragraphs.
The last four: causal verbs on observational data, spinning a null result as a trend, burying the primary outcome behind secondary ones, and dropping the CGM threshold ranges.
One earlier rule was withdrawn against measurement: the guide had said Brief Reports carry no Results subheaders, Galindo 2026 carries two, and the pack now allows them.
That withdrawal is worth carrying because it is the pattern to expect across this tree, a stated norm measured against a real exemplar and corrected rather than asserted once.

#### 6.4 · What the article type changes
(the README article-type table)
The article type caps the displays this section may commission.
> ✎ The article type caps the displays this section may ~commission: an~ *commission. An* Original Article gets four tables and figures, a Brief Report up to three in total, and an e-Letter or Observation one or two. · CC · 260802 1543
An Original Article gets four tables and figures, a Brief Report up to three in total, and an e-Letter or Observation one or two.
Reference budgets move with it, roughly 40, 20, and 5, and since Results itself carries no citations that whole budget is spent by the introduction and the discussion.
The table's own note sends the reader to current author guidelines to verify the display cap, so it sets an expectation rather than a gate.

#### 6.5 · Format values
(the same four metrics, for the section where the one missing metric would have mattered most)

```text
  📏 WORDS            Original Article 1000-2000 w · ~7-8 ¶ under 3 subheadings measured in Reaven 2026
                      Brief Report 400-700 w · 3 ¶ measured in Galindo 2026, an opener plus 2 subsections
                      sentences per ¶ Reaven 5-8 median ~7 · Galindo 3-8 median ~3
                      8-35 words per sentence, median ~16, the shortest of any section
                      [diabcare-results/style.md "Word budget" and "Micro-norms"]
                      expectation, not a gate: style-profile.md leaves "Exact word limits per article type" unchecked
  📚 CITATION DENSITY 0 markers in either measured Results section
                      every quantitative claim routes to a numbered Table, Figure or Supplementary item instead
                      [diabcare-results/style.md "Micro-norms", Citations row]
  🔢 VALUE DENSITY    not recorded by the pack
  📊 DISPLAYS         this is the section that commissions the manuscript's displays, and article type caps them
                      caps 4 for an Original Article · up to 3 total for a Brief Report · 1-2 for an e-Letter
                      caption separator Figure 1--Caption text. and Table 1--Caption text., no space either side
                      hero display for a CGM paper, a stacked bar of time in each glycemic range
                      [README "Article types in Diabetes Care" table, and diabcare-results/style.md lines 98-99 and 115]
                      expectation, not a gate: the README hedges its own cap with "verify current author guidelines"
```

The empty VALUE DENSITY row is sharper here than anywhere else on this page.
A Diabetes Care Results section is among the most value-dense prose this whole tree covers.
> ✎ A Diabetes Care Results section is among the most value-dense prose this whole tree ~covers, since one~ *covers. One* result per sentence means an estimate with its interval or its P value in almost every ~line, and~ *line. And* the CGM metrics TIR, TBR, TAR, GMI and MARD each drag their thresholds along behind them. · CC · 260802 1543
One result per sentence means an estimate with its interval or its P value in almost every line.
And the CGM metrics TIR, TBR, TAR, GMI and MARD each drag their thresholds along behind them.
The pack counts words per sentence and citation markers per sentence for exactly this section, and never counts the numbers.
> ✎ The pack counts words per sentence and citation markers per sentence for exactly this ~section~ *section,* and never counts the ~numbers, and no~ *numbers. No* style.md in the venue tree does either, all 95 of them read on 260802. · CC · 260802 1543
No style.md in the venue tree does either, all 95 of them read on 260802.
So the one format metric a section-edit pass would most want at this venue is the one metric nobody measured.

#### 6.6 · The language, in the papers' own words
(five sentences the pack quotes, one per Results move in 6.2, ending on the caption whose separator a blanket em-dash pass would delete)

"Among 52 participants enrolled, 39 were included in the analysis." [Galindo 2026]
The sample-first opener, where the analytic N is the very first number in the section, the opening slot in 6.2.

"Mortality was lower with CGM initiation, yielding adjusted risk ratios of 0.90 (95% CI 0.71-0.97) to 0.84 (CI 0.72-0.97) over 1-4 years of follow-up." [Reaven 2026]
The primary effect carried with its interval rather than with a bare P value, the effect slot in 6.2.

"The %TBR <70 mg/dL was not significantly different between groups (mean 1.17% +/- 1.8 vs. 1.29% +/- 2.7; P = 0.28)." [Galindo 2026]
The CGM outcome with its threshold, both means and its P value, reported as a null with no softening, which is the anti-pattern 6.3 lists and this sentence avoids.

"Risk ratios did not differ between groups for incident nondiabetes outcomes, including outpatient and inpatient diagnoses of musculoskeletal or gastrointestinal conditions." [Reaven 2026]
The negative-control outcome, which an observational design reports so a reader can see residual confounding was looked for.

"Figure 1--Comparison of %TIR during rtCGM (intervention) and CBG testing (SOC) periods in patients with T2D undergoing hemodialysis." [Galindo 2026]
The caption in its literal two-hyphen form, the requirement 6.1 spells out and A1.2 has to protect from this repo's own writing rule.

### 7 · The discussion is printed under the heading CONCLUSIONS

**There is no DISCUSSION heading in this journal**: one section holds interpretation, prior work, mechanisms, limitations, and the closing statement.

```text
  📐 ARC ── diabcare-discussion/style.md "Arc"
     P1     principal findings, restating design + main result
     P2-P4  comparison to prior work, interpretation, mechanisms
     P5-P6  ADA Standards context, clinical implications
     P7     strengths, optional, often woven into P2-P4
     P8     limitations, 1-2 ¶
     P9     the closing paragraph, In conclusion, ...

  📏 BUDGET ── same file, "Word budget"
     Original Article     1200-2500 w · 5-12 ¶
     Brief Report         400-800 w · ~3-6 ¶
     e-Letter             ~200-400 w, no separate heading

  📊 MEASURED 2026-07-08 ── same file, "Micro-norms"
     Reaven 2026          ~10-11 ¶ under 5 named subheadings
     Galindo 2026         6 ¶, unlabeled, closing on In conclusion
     sentences per ¶      Reaven 2-6 median ~4 · Galindo 3-5 median ~5
     words per sentence   10-39, median ~21
     citations            Reaven ~0.4/sentence · Galindo ~9 markers
     clustering           up to 5 refs in one comparison sentence
     citation-free zones  Limitations and the closing ¶, both papers

  🤖 STRING-LEVEL IN THIS SECTION
     ③ the heading reads CONCLUSIONS, never DISCUSSION
     ⑦ ADA Standards of Care cited in the context paragraph
     ⚠️ In conclusion / In summary opens only the final paragraph
     ⚠️ zero citation markers in Limitations and the closing ¶
```

🧾 Establishes the section whose name is the trap, because a retarget from any other journal arrives with the right content sitting under the wrong heading.

#### 7.1 · Two legal formats, and what picks between them
(style.md lines 13 and 37-42, plus the micro-norm reading at line 168)
The flat format runs unlabeled paragraphs and closes on `In conclusion, ...`.
> ✎ The flat format runs unlabeled paragraphs and closes on `In conclusion, ~...`, which~ *...`. That* is what Galindo 2026 ~does~ *does,* across six paragraphs. · CC · 260802 1543
That is what Galindo 2026 does, across six paragraphs.
The subsectioned format gives the same arc named subheadings.
> ✎ The subsectioned format gives the same arc named ~subheadings, and~ *subheadings.* Reaven 2026 uses five of them: effects on the primary outcome, effects on interim outcomes, potential mechanisms of protection, limitations, and conclusion. · CC · 260802 1543
Reaven 2026 uses five of them: effects on the primary outcome, effects on interim outcomes, potential mechanisms of protection, limitations, and conclusion.
Length picks the format rather than taste, since a Brief Report has no room to subsection and ten unlabeled paragraphs are unreadable.

#### 7.2 · Signature moves, as slots
(style.md "Paragraph-by-paragraph structure" lines 46-129)
P1 restates design and finding, `In this <design>, we <demonstrated or found> that <main finding>.`, and a technology paper may lead instead on its clinical-significance statement.
The comparison paragraphs are where citations cluster, anchored on the ADA Standards or the Battelino 2019 time-in-range consensus.
Mechanisms are hedged into hypotheses, `We hypothesized that <mechanism> could <effect>.`, and competing explanations may stand side by side.
Limitations are listed one per clause, each usually followed by a bounded-impact clause, `Although <limitation>, <what the finding still supports>.`
The closing paragraph names the design again and ends forward, `Future studies with <what> should determine whether <question>.`

#### 7.3 · Anti-patterns
(style.md "Anti-patterns" lines 145-155)
Nine of them, and three are string tests.
> ✎ Nine of them, and three are string ~tests:~ *tests. Those three:* a heading reading ~DISCUSSION,~ *DISCUSSION;* `In conclusion` or `In summary` opening a paragraph that is not the ~last,~ *last;* and a missing ADA Standards connection where the topic touches a recommendation. · CC · 260802 1543
Those three: a heading reading DISCUSSION; `In conclusion` or `In summary` opening a paragraph that is not the last; and a missing ADA Standards connection where the topic touches a recommendation.
The other six are readings.
> ✎ The other six are ~readings:~ *readings. The first three:* opening on a mechanism before the principal findings, causal verbs on observational data, *and* new analyses appearing here for the first ~time,~ *time. The last three:* limitations written as one run-on sentence, an omitted design name in the closing paragraph, and overstated implications on a null result. · CC · 260802 1543
The first three: opening on a mechanism before the principal findings, causal verbs on observational data, and new analyses appearing here for the first time.
The last three: limitations written as one run-on sentence, an omitted design name in the closing paragraph, and overstated implications on a null result.
The pack corrected itself here against measurement too, raising the Brief Report paragraph count from 3-5 to about 3-6 after Galindo 2026 measured at six.

#### 7.4 · What the article type changes
(style.md lines 12-16)
An Original Article gets 1200 to 2500 words and can afford named subheadings; a Brief Report gets 400 to 800 and cannot.
An e-Letter or Observation has no separate section at all.
> ✎ An e-Letter or Observation has no separate section at ~all, and its~ *all. Its* roughly 200 to 400 words of interpretation sit inside the running ~body, which is why~ *body. So* a heading check has to know the article type before it may fire. · CC · 260802 1543
Its roughly 200 to 400 words of interpretation sit inside the running body.
So a heading check has to know the article type before it may fire.

#### 7.5 · Format values
(the same four metrics, for the only section whose citation figure changes inside itself)

```text
  📏 WORDS            Original Article 1200-2500 w · 5-12 ¶ · ~10-11 ¶ under 5 subheadings measured in Reaven 2026
                      Brief Report 400-800 w · ~3-6 ¶ · 6 unlabeled ¶ measured in Galindo 2026
                      sentences per ¶ Reaven 2-6 median ~4 · Galindo 3-5 median ~5
                      10-39 words per sentence, median ~21
                      [diabcare-discussion/style.md "Word budget" and "Micro-norms"]
                      expectation, not a gate: style-profile.md leaves "Exact word limits per article type" unchecked
  📚 CITATION DENSITY Reaven 2026 ~12 markers, about 0.4 per sentence, up to 5 refs in one comparison sentence
                      Galindo 2026 ~9 markers, with the same clustering
                      0 markers in Limitations and in the closing paragraph, in both papers
                      [diabcare-discussion/style.md "Micro-norms", Citations row]
  🔢 VALUE DENSITY    not recorded by the pack
  📊 DISPLAYS         0 figures and 0 tables commissioned here, since the section reads what Results already commissioned
                      caps 4 for an Original Article · up to 3 total for a Brief Report · 1-2 for an e-Letter
                      those caps bound main-text displays across the manuscript, not this section
                      [README "Article types in Diabetes Care" table]
                      expectation, not a gate: the README hedges its own cap with "verify current author guidelines"
```

The citation row is the only metric on this page with a zone inside it.
> ✎ The citation row is the only metric on this page with a zone inside ~it, since markers~ *it. Markers* cluster in the comparison and mechanism ~paragraphs~ *paragraphs,* and fall to zero in Limitations and in the closing paragraph of both measured papers. · CC · 260802 1543
Markers cluster in the comparison and mechanism paragraphs, and fall to zero in Limitations and in the closing paragraph of both measured papers.
That zero is a shape a check could look for once the paragraph boundaries are known, which is more than can be said for any word budget here.

#### 7.6 · The language, in the papers' own words
(five sentences the pack quotes, one per paragraph slot in 7.2, from the restatement that opens the section to the sentence that closes it)

"In this RCT, we demonstrated that using rtCGM for just 30 days improved glycemic control compared with CBG testing (SOC)" [Galindo 2026]
The P1 restatement of design and finding, the opener slot in 7.2, with the trial design allowing a verb an observational paper could not use.

"Previous voice research in people with diabetes has linked chronic hyperglycemia and polyneuropathy to hoarseness, vocal strain, and changed pitch (10-12)." [Lehmann 2026]
The prior-work comparison, the paragraphs where 7.5 shows the citation markers cluster.

"these findings provide further support for CGM initiation as standard of care for adult-onset type 1 diabetes" [Reaven 2026]
The ADA standard-of-care context, the slot 7.3 lists as a string test whenever the topic touches a current recommendation.

"Limitations include a restricted study period and inclusion of Medicare Fee-for-Service only." [Kahkoska 2025]
The limitation stated one per clause, the shape 7.2 requires instead of the run-on sentence 7.3 names as an anti-pattern.

"To conclude, we present an ML-based approach to detect hypoglycemia from voice, potentially complementing current detection methods" [Lehmann 2026]
The closing paragraph opening on a conclusion phrase and ending forward, which A7.1 wants checked for position as much as for wording.

### 8 · The appendix is one Supplementary Material package, not numbered supplements

**There is no Supplement 1 and no eTable**: a single figshare-hosted package, with items prefixed and numbered independently of the main text.

```text
  📦 NAMING ── diabcare-appendix/style.md "Naming convention"
     package     Supplementary Material, or Supplementary Data
     items       Supplementary Fig. n · Supplementary Table n ·
                 Supplementary Methods
     hosting     doi.org/10.2337/figshare.<ID>, in the author-info block
     never       Supplement 1 · eTable · eFigure · eMethods ·
                 lowercase supplementary · in the supplement

  ⚖️ TRIAGE ── same file, "What goes in the main text vs. supplementary"
     main text   results answering the primary or a secondary question,
                 up to ~4 tables, flow diagram, primary-outcome figure, AGP
     supplement  extended methods, model specifications, sensitivity and
                 robustness protocols, subgroup breakdowns, measurement
                 definitions, hyperparameters, reporting checklists

  📊 MEASURED ── same file, item counts by paper type
     Galindo 2026 RCT Brief       1 table · 3 figs · 0 methods
     Lehmann 2026 ML Brief        0 · 1 · 1
     Zheng 2025 NLP Original      1 · 0 · 0
     Reaven 2026 TTE Original     5 · 4 · 1 Material Methods
     Godneva 2026 observational   9 · 2 · 0
     Dupenloup 2026 cost-effect.  17 · 5 · 0
     Kahkoska 2025 e-Letter       0 · 0 · 0

  🤖 STRING-LEVEL IN THIS SECTION
     ④ Supplementary Material, never a numbered Supplement
     ④ pointers read (Supplementary Table n) or (Supplementary Fig. n)
     ⚠️ seven back-matter labels, in their fixed order
     ⚠️ the guarantor sentence inside Author Contributions
```

📎 Establishes what the appendix holds, how its two numbering streams stay apart, and where the data-sharing statement actually lives, which is not here.

#### 8.1 · Two numbering streams that never meet
(style.md "Item labeling" lines 16-24)
Main-text items take plain labels, `Fig. 1` and `Table 1`, while supplementary items take the prefix, `Supplementary Fig. 1` and `Supplementary Table 1`, each stream counting from one on its own.
Supplementary Methods is unnumbered unless several distinct method documents exist, and Reaven 2026 uses the variant label Supplementary Material Methods for its statistical detail.
No package number exists anywhere.
> ✎ No package number exists ~anywhere, which~ *anywhere. That* is the whole difference from the JAMA convention of Supplement 1, Supplement 2, and Supplement 3 carrying protocol, data, and data sharing. · CC · 260802 1543
That is the whole difference from the JAMA convention of Supplement 1, Supplement 2, and Supplement 3 carrying protocol, data, and data sharing.

#### 8.2 · What belongs here, and what only looks as if it does
(style.md "Triage rule" line 63, and the boundary at lines 82-89)
The rule is one sentence: a result that directly answers the primary or a secondary research question stays in the main text, and everything else moves.
Everything else means extended methods, statistical model specifications, sensitivity and robustness protocols, subgroup breakdowns, measurement definitions, algorithm hyperparameters and feature sets, and reporting checklists such as CHEERS.
One item that looks like it belongs here does not.
> ✎ One item that looks like it belongs here does ~not: the~ *not. The* data-sharing statement is the Data and Resource Availability subsection ~closing~ *that closes* RESEARCH DESIGN AND ~METHODS, and the~ *METHODS. The* two ~are routinely~ *get* confused because both concern data availability. · CC · 260802 1543
The data-sharing statement is the Data and Resource Availability subsection that closes RESEARCH DESIGN AND METHODS.
The two get confused because both concern data availability.
The figshare hosting sentence itself sits in the author information block on the first text page, in neither Methods nor the back matter.

#### 8.3 · The back matter is seven labels in a fixed order
(style.md "Back matter sections" lines 91-101)
Acknowledgments, Funding, Duality of Interest, Author Contributions, Prior Presentation where it applies, Handling Editors, and References, each a bold label closed by a period.
Two labels are ADA-specific, and both arrive wrong on a manuscript coming from the JAMA portfolio.
> ✎ Two labels are ~ADA-specific~ *ADA-specific,* and *both* arrive wrong on ~any~ *a* manuscript coming from the JAMA ~portfolio:~ *portfolio.* Duality of Interest is what JAMA calls Conflict of Interest Disclosures, and Handling Editors has no JAMA counterpart at all. · CC · 260802 1543
Duality of Interest is what JAMA calls Conflict of Interest Disclosures, and Handling Editors has no JAMA counterpart at all.
Author Contributions must carry the guarantor sentence.
> ✎ Author Contributions must carry the guarantor ~sentence, naming~ *sentence. It names* one author as having had full access to the study ~data~ *data,* and *as* taking responsibility for its integrity and for the accuracy of the analysis. · CC · 260802 1543
It names one author as having had full access to the study data, and as taking responsibility for its integrity and for the accuracy of the analysis.
Order, label text, and the guarantor sentence are all string-level facts.
> ✎ Order, label text, and the guarantor sentence are all string-level ~facts, which~ *facts. That* makes the back matter the second most checkable block in the ~manuscript~ *manuscript,* after the abstract. · CC · 260802 1543
That makes the back matter the second most checkable block in the manuscript, after the abstract.

#### 8.4 · There is no word budget in this section
(style.md "Micro-norms" line 118)
The pack states plainly that prose metrics do not apply to the supplement and reports item counts instead, so nothing on this page may carry a supplementary word budget.
What those counts do say is that the load tracks the study design rather than the article type.
> ✎ What those counts do say is that the load tracks the study design rather than the article ~type: a~ *type. A* cost-effectiveness Original Article ran 17 supplementary ~tables while~ *tables,* an NLP Original Article ran one, and one e-Letter carried nothing at all. · CC · 260802 1543
A cost-effectiveness Original Article ran 17 supplementary tables, an NLP Original Article ran one, and one e-Letter carried nothing at all.

#### 8.5 · Format values
(the same four metrics, for the one section where three of the four are empty by the pack's own statement rather than by omission)

```text
  📏 WORDS            not recorded by the pack
                      [diabcare-appendix/style.md "Micro-norms": prose metrics do not apply to the supplement]
  📚 CITATION DENSITY not recorded by the pack
                      [diabcare-appendix/style.md "Micro-norms", the same line]
  🔢 VALUE DENSITY    not recorded by the pack
  📊 DISPLAYS         supplementary items are counted, never capped
                      Galindo 2026 1 table / 3 figs · Reaven 2026 5 / 4 / 1 · Dupenloup 2026 17 / 5 / 0
                      main text takes up to ~4 tables, the flow diagram, the primary-outcome figure and the AGP
                      caps 4 for an Original Article · up to 3 total for a Brief Report · 1-2 for an e-Letter
                      those caps bound main-text displays and never the supplementary package
                      [diabcare-appendix/style.md item-count table and its main-text triage list]
                      [README "Article types in Diabetes Care" table]
                      expectation, not a gate: the README hedges its own cap with "verify current author guidelines"
```

Three empty rows here are the pack drawing a boundary rather than leaving a hole.
> ✎ Three empty rows here are the pack drawing a boundary rather than leaving a ~hole, since it~ *hole. It* says outright that prose metrics do not apply to a ~supplement~ *supplement,* and reports item counts in their place. · CC · 260802 1543
It says outright that prose metrics do not apply to a supplement, and reports item counts in their place.
The one row with content inverts what every other section's DISPLAYS row says, because the supplement is where the article-type cap is escaped rather than where it binds.

#### 8.6 · The language, in the papers' own words
(the three author-attributed sentences this section's style guide actually carries, and why there are only three)

"Deidentified participant data will be made available 24 months after publication" [Galindo 2026]
The time-bounded Data and Resource Availability sentence, which 8.2 places at the end of Methods rather than in the back matter this division owns.

"The VA supports that data (deidentified participant data) from approved studies be made publicly available upon request." [Reaven 2026]
The same slot filled by an institution instead of by a clock, so release is gated on a review process rather than on a date.

"(Supplementary Tables 2-11)" [Dupenloup 2026]
The main-text pointer in its range form, the prefixed label 8.1 keeps in a numbering stream that never meets the main-text one.

Everything else this section owns is printed as template text that names no author.
> ✎ Everything else this section owns is printed as ~unattributed~ template ~text: the~ *text that names no author. The* guarantor sentence carries a bracketed initials placeholder, and the clean Duality of Interest form and the figshare hosting line name no paper at all. · CC · 260802 1543
The guarantor sentence carries a bracketed initials placeholder, and the clean Duality of Interest form and the figshare hosting line name no paper at all.
So the quotations stop at three, and nothing may be attributed to a paper the pack did not attribute it to.

## Aims

### A1 · 🤖 Eight requirements a conform pass could enforce today
- A1.1 · The eight-item delta is implemented as a check on a manuscript pinned to this outlet.
  **Done when:** a Diabetes Care manuscript can be failed on apparatus with no human reading it.
- A1.2 · The em-dash caption requirement is exempted from any blanket em-dash rule.
  **Done when:** a repo-wide em-dash pass cannot break a caption in a paper pinned here.

### A2 · 🔗 The desk wants an outcome, and pairs with npj Digital Medicine
- A2.1 · A digital-diabetes candidate is routed on the disease-versus-tool axis.
  **Done when:** the choice between the two outlets is made on a stated question rather than by preference.

### A3 · 📋 The abstract is four ADA labels and a four-bullet Highlights box
- A3.1 · The four label strings and their order are checked on a manuscript pinned here.
  **Done when:** a missing or reordered ADA label, or any IMPORTANCE heading, fails with nobody reading the abstract.
- A3.2 · The Article Highlights box is checked as four verbatim question strings, gated on article type.
  **Done when:** an Original Article or Brief Report missing the box fails, and an e-Letter is never asked for one.

### A4 · 🧭 The introduction is untitled and turns on one adversative
- A4.1 · The ADA Standards of Care requirement is scoped to the manuscript rather than to this section.
  **Done when:** the citation check passes on a paper citing the Standards anywhere, matching what both measured exemplars actually do.

### A5 · 🔬 The methods section is named RESEARCH DESIGN AND METHODS
- A5.1 · The heading string and the terminal Data and Resource Availability subsection are both checked.
  **Done when:** a paper headed Methods, or one missing that closing subsection, fails on the string alone.
- A5.2 · Every CGM metric named in this section is checked for its mg/dL threshold.
  **Done when:** a bare TIR, TBR, or TAR carrying no range is reported as a finding.

### A6 · 📊 The results section carries the shortest sentences and the caption separator
- A6.1 · The caption separator form is checked on every figure and table caption.
  **Done when:** a caption written with a period or a colon is reported, with A1.2's exemption already in force.
- A6.2 · The display count this section may commission is bounded by the article type.
  **Done when:** a Brief Report asking for a fourth display is caught before submission rather than at the desk.

### A7 · 🧾 The discussion is printed under the heading CONCLUSIONS
- A7.1 · The heading string is checked, and the placement of In conclusion with it.
  **Done when:** a section headed DISCUSSION fails, and In conclusion opening any paragraph but the last is reported.

### A8 · 📎 The appendix is one Supplementary Material package, not numbered supplements
- A8.1 · Supplementary labels and pointers are checked against the ADA forms.
  **Done when:** Supplement 1, eTable, eFigure, or a lowercase supplementary pointer fails on a manuscript pinned here.
- A8.2 · The seven back-matter labels, their order, and the guarantor sentence are checked.
  **Done when:** a reordered back matter or a missing guarantor sentence is reported with nobody reading it.

## States

### A1 · 🤖 Eight requirements a conform pass could enforce today
- ⬜ A1.1 · Not started. All eight are prose bullets in the pack README.
- ⬜ A1.2 · Not started. No exemption exists, and the conflict is recorded here for the first time.

### A2 · 🔗 The desk wants an outcome, and pairs with npj Digital Medicine
- ⬜ A2.1 · Not started. Both taste files exist and nothing compares them.

### A3 · 📋 The abstract is four ADA labels and a four-bullet Highlights box
- ⬜ A3.1 · Not started. The four labels and their order are recorded here and enforced nowhere.
- ⬜ A3.2 · Not started. The four question strings are recorded; no article-type gate exists to hang them on.

### A4 · 🧭 The introduction is untitled and turns on one adversative
- ⬜ A4.1 · Not started, and now blocked on a pack contradiction: the ADA citation is listed as near-mandatory while neither measured exemplar carries one here.

### A5 · 🔬 The methods section is named RESEARCH DESIGN AND METHODS
- ⬜ A5.1 · Not started. Both strings are fixed text and nothing compares them.
- ⬜ A5.2 · Not started. The thresholds are listed in the pack's style profile and in no check.

### A6 · 📊 The results section carries the shortest sentences and the caption separator
- ⬜ A6.1 · Not started, and dependent on A1.2, since a check and a blanket rule cannot both own the separator.
- ⬜ A6.2 · Not started. The README's own display cap is hedged, so the bound needs verifying before it can be enforced.

### A7 · 🧾 The discussion is printed under the heading CONCLUSIONS
- ⬜ A7.1 · Not started. This is the single likeliest silent failure on a retarget, and nothing looks at it.

### A8 · 📎 The appendix is one Supplementary Material package, not numbered supplements
- ⬜ A8.1 · Not started. The forbidden JAMA forms are listed in the pack and matched by nothing.
- ⬜ A8.2 · Not started. The seven labels and the guarantor sentence are recorded in order and never compared.

## Files

- `../../paper/venue/playbook-medical-journals/diabetes-care/taste.md` · the desk signals and the one-sentence test
- `../../paper/venue/playbook-medical-journals/README.md` · the eight-item apparatus delta and the article-type table, from the retired pack head page
- `../../paper/venue/playbook-medical-journals/style-profile.md` · the language to imitate, the CGM vocabulary table, and the caption format
- `../../paper/venue/playbook-medical-journals/diabetes-care/diabcare-abstract/style.md` · the four ADA labels, the Highlights box, and the measured per-label budgets
- `../../paper/venue/playbook-medical-journals/diabetes-care/diabcare-introduction/style.md` · the context-known-gap-aim arc and the reconciled word budget
- `../../paper/venue/playbook-medical-journals/diabetes-care/diabcare-methods/style.md` · the fixed heading, the four design-family orders, and the terminal subsection
- `../../paper/venue/playbook-medical-journals/diabetes-care/diabcare-results/style.md` · the number formats, the caption separator, and the display conventions
- `../../paper/venue/playbook-medical-journals/diabetes-care/diabcare-discussion/style.md` · the CONCLUSIONS heading and the limitations-then-closing arc
- `../../paper/venue/playbook-medical-journals/diabetes-care/diabcare-appendix/style.md` · the Supplementary naming, the triage rule, and the back-matter order
- `QBv8-npj-digital-medicine.md` · the outlet this one pairs with

<!-- exemplars:begin -->

📚 **Exemplars** · 25 papers on disk, regenerated by `sync-exemplars.py`

- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/ajjan-2026-diabcare-gdac-cgm-hba1c-alignment.pdf` · Ajjan 2026
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/belfort-2026-diabcare-cgm-metrics-insulin-resistance-obesity.pdf` · Belfort 2026
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/bergenstal-2026-diabcare-cgm-profiles-grade-trial.pdf` · Bergenstal 2026
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/cleland-2026-diabcare-ai-systems-retinopathy-comparison.pdf` · Cleland 2026
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/daultrey-2026-diabcare-temperature-hypoglycemia-cgm-t1d.pdf` · Daultrey 2026
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/dave-2026-diabcare-deep-learning-retinopathy-screening.pdf` · Dave 2026
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/dupenloup-2026-diabcare-cgm-remote-monitoring-pediatric.pdf` · Dupenloup 2026
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/galindo-2026-diabcare-cgm-t2d-hemodialysis.pdf` · Galindo 2026
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/godneva-2026-diabcare-time-in-range-normoglycemia.pdf` · Godneva 2026
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/he-2026-diabcare-glycemic-profiles-cgm-t2d.pdf` · He 2026
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/kadiyala-2026-diabcare-hba1c-gmi-cystic-fibrosis.pdf` · Kadiyala 2026
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/kahkoska-2025-diabcare-claims-algorithm-cgm-uptake.pdf` · Kahkoska 2025
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/kok-2026-diabcare-cgm-missing-data-duration.pdf` · Kok 2026
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/lehmann-2026-diabcare-ml-voice-hypoglycemia-detection.pdf` · Lehmann 2026
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/lizoain-2026-diabcare-cgm-accuracy-postbariatric.pdf` · Lizoain 2026
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/montaser-2026-diabcare-time-below-range-hypoglycemia.pdf` · Montaser 2026
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/narasaki-2026-diabcare-cgm-mortality-dialysis.pdf` · Narasaki 2026
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/niu-2026-diabcare-minimed780g-no-bolus.pdf` · Niu 2026
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/park-2026-diabcare-gmi-hba1c-discordance-t1d.pdf` · Park 2026
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/reaven-2026-diabcare-cgm-mortality-t1d-veterans.pdf` · Reaven 2026
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/rodriguez-2026-diabcare-iscgm-hospitalizations-t2d.pdf` · Rodriguez 2026
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/sherr-2026-diabcare-hypoglycemia-burden-technology-t1d.pdf` · Sherr 2026
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/vonconta-2026-diabcare-cgm-inpatient-mard-algorithm.pdf` · Vonconta 2026
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/zelnick-2026-diabcare-glycemic-biomarker-accuracy-dialysis.pdf` · Zelnick 2026
- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/zheng-2025-diabcare-nlp-cgm-data-extraction.pdf` · Zheng 2025

- `../../paper/venue/playbook-medical-journals/diabetes-care/examples/INDEX.md` · the pack's own manifest, not an exemplar

<!-- exemplars:end -->

<!-- kinds:begin -->

📐 **Section kinds** · 6 declared in `stages/section-kinds.yml`, regenerated by `sync-exemplars.py`

`section-edit` runs once per kind, and writes one page each. That is 5 numbered `S-Main-<n>` pages, plus `S-Appendix-<letter>`.

- `S-Main-0` · abstract
- `S-Main-1` · introduction
- `S-Main-2` · methods
- `S-Main-3` · results
- `S-Main-4` · discussion
- `S-Appendix-A` · appendix

A kind is the SMALLEST unit a paper gets here, not a ceiling.
One kind can spread across several numbered Main pages.
This repo's own MISQ paper runs to `S-Main-8-conclusion`, and the numbers above move with it.
The ORDER does not move. It is this venue's reading order, not a house default.

<!-- kinds:end -->

🔗 **Authority** · the venue's own instructions, fetched and verified 260802

- [Diabetes Care instructions for authors](https://diabetesjournals.org/care/pages/instructions-for-authors) · the article types and their published limits, the abstract format, Article Highlights, and Supplemental Material
- THE ORIGINAL ARTICLE NUMBERS ARE GATES, NOT EXPECTATIONS: "The word count limit for Original Articles is 4,000 words, excluding words in tables, table legends, figure legends, title page, acknowledgments, and references", plus "no more than 40 references" and "no more than a combination of 4 tables and/or figures", with the abstract "should not exceed 250 words"
- So the hedge every `Format values` block carries, that the README's caps need verifying against current author guidelines, is answered for this type, and 3.5, 4.4, 5.4, 6.5 and 7.5 may drop it
- The ADA heading set at 3 is confirmed by name: the abstract "format should include four sections: Objective ..., Research Design and Methods ..., Results ..., and Conclusions ..."
- The published manuscript order confirms two divisions at once: "title page, structured abstract, introduction (no heading), Research Design and Methods, Results, Conclusions, Acknowledgments, References, tables, and figure legends"
- CONTRADICTS the pack on Brief Reports: the limit is "1,500 words, excluding the 150 word abstract", not the about 2,500 recorded at 3.4, and the abstract is "no more than 150 words", not the about 150 to 200 at 3.5
- CONTRADICTS the pack on Brief Report displays: "Brief Reports may contain a combination of 4 tables/figures", not the up to 3 total that every DISPLAYS row on this page repeats; the 20-reference figure matches
- A Brief Report body shape this page has no record of: the abstract "should be followed by a short introduction (2-3 sentences) and four concise sections: Research Design and Methods, Results, Conclusions, and References"
- CONTRADICTS the pack on Letters, and splits one figure into two: "Letters do not have abstracts and should not exceed 500 words for comments and responses or 750 words for Observations (excluding a maximum of 5 references)", against the single about 1,000 words recorded at 3.4
- The second Article Highlights question carries a plural marker 3.3 drops: the journal prints "What is the specific question(s) we wanted to answer?", so the verbatim string check A3.2 asks for would fail on the form this page records
- Article Highlights reach wider and carry a cap the pack records nowhere: required for "Original Articles, Brief Reports, Images and Reports, Reviews, and Perspectives in Care", placed "immediately after the abstract", and "75 to 130 words or fewer, including the questions"
- THE SUBMISSION LABEL IS NOT THE PRINTED ONE: the file "must be clearly labeled as 'Online-Only Supplemental Material'" and is pointed at as "Supplemental Table S1", where division 8 records the published forms Supplementary Material and Supplementary Table n
- The figshare hosting at 8 is confirmed and its agent named: supplemental files "will be uploaded to Figshare by ADA production staff and linked to the article", searchable at diabetesjournals.figshare.com/Care
- The supplement is reviewed and never typeset, which the pack does not record: files "are subject to peer review but will not be composed, copyedited, or proofread by production staff"
- The Data and Resource Availability placement at 8.2 is confirmed: the statement goes "under the heading 'Data and Resource Availability' at the end of the 'Research Design and Methods' section"
- THE CAPTION SEPARATOR IS NOT AN AUTHOR INSTRUCTION: the page asks only that legends sit in a "Figure Legends" section after the references and states no separator form, so the `Figure 1--Caption text.` shape at 6.1 is house typesetting read off published papers, which weakens A6.1 and leaves A1.2 standing
- The back matter the journal publishes is not the seven labels at 8.3: the Acknowledgments carries Funding and Assistance, Conflict of Interest, Author Contributions and Guarantor Statement, Artificial Intelligence, and Prior Presentation, and the phrase Duality of Interest appears nowhere in the instructions
- The guarantor sentence at 8.3 is confirmed and placed: it "should appear at the end of the Author Contributions paragraph", and "Modified statements or generic statements indicating that all authors had such access are not acceptable"

## Law

Eight of this desk's requirements are string-level facts about the manuscript.
> ✎ ~-~ Eight of this desk's requirements are string-level facts about the ~manuscript, so~ *manuscript. So* this is the one outlet in the tree ~that~ *a machine* can ~be failed by a machine,~ *fail,* and every one of ~them~ *the eight* fails silently on a retarget from the JAMA portfolio. · CC · 260802 1543
So this is the one outlet in the tree a machine can fail, and every one of the eight fails silently on a retarget from the JAMA portfolio.
  This venue requires an em-dash caption separator, so a blanket em-dash rule must exempt a manuscript pinned here.

## Glossary

- **Apparatus delta**: the checkable differences in headings, boxes, reference format, and caption punctuation between two venue families.
- **Routing pair**: two outlets whose rejections overlap so closely that a candidate clearing one is live at both, here Diabetes Care and npj Digital Medicine.

## Log

260802 · Opened with the QBv outlet pages, from `playbook-medical-journals/diabetes-care` at `Venue-Paper@fe25a88`.
260802 · Added one Content division per section kind (3 abstract, 4 introduction, 5 methods, 6 results, 7 discussion, 8 appendix). Each carries its arc, its sourced budget, its slot patterns, and the pack's own anti-patterns.
> ✎ 260802 · Added one Content division per section kind (3 abstract, 4 introduction, 5 methods, 6 results, 7 discussion, 8 ~appendix), each carrying~ *appendix). Each carries* its arc, its sourced budget, its slot patterns, and the pack's own ~anti-patterns; folded~ *anti-patterns. 260802 · Folded* the retired pack head page's ADA-versus-JAMA delta and article-type table into ~them;~ *those divisions, and* relaxed the Writing Style bullet from never transcribing a number to always sourcing one. · CC · 260802 1543
260802 · Folded the retired pack head page's ADA-versus-JAMA delta and article-type table into those divisions, and relaxed the Writing Style bullet from never transcribing a number to always sourcing one.
260802 · Added an Authority block to Files from the Diabetes Care instructions for authors, fetched that day. It closes the expectation-versus-gate hedge for Original Articles and corrects three of the pack's other types.
> ✎ 260802 · Added an Authority block to Files from the Diabetes Care instructions for authors, fetched that ~day, which~ *day. It* closes the expectation-versus-gate hedge for Original Articles and corrects three of the pack's other types. *260802 ·* The Original Article limits are published and match the pack exactly: 4,000 body words, 250-word abstract, 40 references, 4 tables and/or figures. *260802 ·* Brief Reports do not: 1,500 words against the pack's about 2,500, a 150-word abstract cap, and 4 displays against the pack's up to 3. *260802 ·* Letters are two limits and not one, 500 words for comments and responses against 750 for Observations, both under the about 1,000 the pack carries. *260802 ·* Article Highlights print the second question with a plural marker the pack ~drops~ *drops,* and carry a 75 to 130 word cap it does not record. *260802 ·* The caption separator is nowhere in the instructions, so 6.1's form is house typesetting rather than a published rule. · CC · 260802 1543
260802 · The Original Article limits are published and match the pack exactly: 4,000 body words, 250-word abstract, 40 references, 4 tables and/or figures.
260802 · Brief Reports do not: 1,500 words against the pack's about 2,500, a 150-word abstract cap, and 4 displays against the pack's up to 3.
260802 · Letters are two limits and not one, 500 words for comments and responses against 750 for Observations, both under the about 1,000 the pack carries.
260802 · Article Highlights print the second question with a plural marker the pack drops, and carry a 75 to 130 word cap it does not record.
260802 · The caption separator is nowhere in the instructions, so 6.1's form is house typesetting rather than a published rule.
260802 · Added two subsubsections per section division: a `Format values` block carrying WORDS, CITATION DENSITY, VALUE DENSITY and DISPLAYS, with each value sourced to a pack line, and a quotation set from the pack's own exemplar sentences.
> ✎ 260802 · Added two subsubsections per section division: a `Format values` block carrying WORDS, CITATION DENSITY, VALUE DENSITY and ~DISPLAYS~ *DISPLAYS,* with each value sourced to a pack line, and a quotation set from the pack's own exemplar sentences. *260802 ·* VALUE DENSITY came back empty in all six, since no style.md in the venue tree counts numeric values per sentence, all 95 read on ~260802; the~ *260802. 260802 · The* appendix additionally records no word and no citation ~figure~ *figure,* by the pack's own statement. *260802 ·* Labelled every word budget and every display cap an expectation rather than a gate, because the README hedges its cap with "verify current author guidelines" and style-profile.md still leaves "Exact word limits per article type" unchecked. · CC · 260802 1543
260802 · VALUE DENSITY came back empty in all six, since no style.md in the venue tree counts numeric values per sentence, all 95 read on 260802.
260802 · The appendix additionally records no word and no citation figure, by the pack's own statement.
260802 · Labelled every word budget and every display cap an expectation rather than a gate, because the README hedges its cap with "verify current author guidelines" and style-profile.md still leaves "Exact word limits per article type" unchecked.
260802 · Rewrote for a reader whose English is weak: the Opening lead, 42 Content and Law sentences, and three overlong Log entries.
> ✎ 260802 · Rewrote for a reader whose English is weak: the Opening lead, ~35~ *42* Content and Law sentences, and three overlong Log ~entries~ *entries. 260802 · The Log* split ~into dated lines that record~ *records* the same ~facts. Every~ *facts on dated lines, and every* change *on this page* carries a word-level ✎ record computed by `writing/haipipe-writing/cli/wdiff.py`. · CC · 260802 1543
260802 · The Log split records the same facts on dated lines, and every change on this page carries a word-level ✎ record computed by `writing/haipipe-writing/cli/wdiff.py`.
260802 · Expanded the six CGM acronyms at their first appearance in the Diagram (TIR, TBR, TAR, GMI, MARD, AGP), since the page is not the manuscript and only the manuscript may leave them undefined.
