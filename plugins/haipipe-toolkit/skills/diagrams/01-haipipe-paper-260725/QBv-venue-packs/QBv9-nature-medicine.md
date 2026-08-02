# Nature Medicine: the desk whose bar cannot be met by rewriting

state: 🟡 PARTIAL · 24 exemplars · 7 sections · taste ✓ · the validation bar is a study-design property no retarget can supply
owner: JL
method: state what Nature Medicine requires of translational evidence, and record why this outlet is decided at the task layer rather than at the venue stage

## Opening

Most desks in this tree can be satisfied by re-argument: the same study, framed for a different reader. This one usually cannot. What is it asking for that a rewrite cannot produce?

**Where this page sits**: it is one venue target in `QBv`, one page per desk with no pack layer above it.
This page owns only what is true of `playbook-nature-portfolio/nature-medicine/`.

**Why this outlet sits upstream of the venue stage**: its headline desk-reject is retrospective single-center AI with no external validation, and prospective multi-center validation is a study-design property.
This is one of two Nature outlets decided before venue runs; npj Digital Medicine at `QBv8` is the other.

**What that means in practice**: shortlisting this outlet for a paper whose data collection is finished is usually already a mistake, and nothing in the lifecycle says so.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**Quote a norm only with its source beside it**: a budget or count from `nature-medicine/natmed-<section>/style.md` may stand in a section-kind division, but the style.md heading or the exemplar name rides on the same line, so a number is never the page's own claim.

**Say the bar is a design property, not a strength**: describing it as rigor invites a paper to try harder at revision, which is exactly what cannot work here.

✅ `prospective multi-center validation cannot be added later`  ❌ `Nature Medicine wants very rigorous validation`

## Diagram

**Bench to bedside, with the validation already done**: the bar is fixed before the paper is written.

```text
  🎯 THE TEST
     "Does this advance the practice of medicine in a way that
      crosses disciplinary boundaries?"

  ✅ WHAT CLEARS IT
     a translational breakthrough
     PROSPECTIVE or MULTI-CENTER validation
     a validated biomarker or diagnostic
     health equity work that carries solutions

  ❌ DESK-REJECT
     retrospective single-center AI with no external
       validation                          ⏳ not fixable later
     animal-only with no human path        ⏳ not fixable later
     computation with no clinical grounding

  ⏳ TWO OF THE THREE ARE DESIGN PROPERTIES
     ── decided at the task layer, months before venue
     ── so this outlet is SHORTLISTED early or not at all

  📊 24 exemplars ── the largest base in the whole tree
```

## Content

### 1 · The bar is set before the paper exists

**Two of three rejections describe the study, not the manuscript**: no revision reaches them.

```text
  🔬 what a REWRITE can fix
     ── framing · the arc · the Discussion's reach
     ── which is what makes most retargets in this tree cheap

  ⏳ what a rewrite CANNOT fix
     ── whether validation was prospective
     ── whether more than one center contributed
     ── whether a human path exists at all

  💥 so the failure mode is a paper that reaches the venue
     stage already unable to clear the desk, and gets a
     recommendation anyway
```

⏳ Establishes this outlet as a task-layer decision, a class no stage currently enforces.

#### 1.1 · The same trap exists at ISR, in a different field
(so it is a tree-wide pattern rather than a Nature quirk)
`QBv2` records that a clean identification strategy is likewise unacquirable at revision.
Both desks reward a property of how the evidence was gathered, which means the venue stage inherits a decision it did not make.

### 2 · Where it sits against its four siblings

**The clinical end of a broad portfolio**: and the boundary against npj Digital Medicine is the live one.

```text
  🏥 Nature Medicine  translational · prospective · practice
  💻 npj DM           a digital tool validated on clinical
                      outcomes
        └── both clinical, both validation-anchored

  🔀 the separation the pack draws
     Nature Medicine ── the MEDICINE advances
     npj DM          ── the TOOL changes what a clinician can do

  🌍 Nat Comms · 🧠 NHB · 🤖 NMI sit outside this pair on
     breadth, behavior, and method

  💡 and the shipped paper in this repo went to npj DM,
     not here (QBv8)
```

🔀 Establishes the live boundary as the one against npj Digital Medicine, which is where this repo's work is actually decided.

### 3 · Abstract: one paragraph that closes on a clinical action

**The abstract as an evidence report**: eight beats in one unstructured paragraph, with the study design in sentence three and a recommendation at the end.

```text
  📐 ARC · natmed-abstract/style.md "Arc"
     M1  clinical problem, patient-facing
     M2  the gap in current evidence
     M3  "Here we" pivot, naming the DESIGN
     M4  design and scale: n, sites, comparators
     M5  primary outcome: effect + 95% CI + P
     M6  secondary outcomes
     M7  clinical implication or recommendation
     M8  trial registration id, RCTs only, last sentence

  📏 BUDGET · natmed-abstract/style.md "Word budget"
     Article            150-350 w, median ~200
     RCT                250-350 w
     Brief Comm         ~180-200 w
     paragraphs         1, unstructured, no labeled fields

  🔬 MEASURED 2026-07-08 · natmed-abstract/style.md "Micro-norms"
     brinton-2026       182 w
     bean-2026          194 w
     sentences          9-10 per abstract
     words/sentence     5-32, median ~18
     citations          0
```

📝 Establishes the abstract as the first place the desk reads a study design, which is why the pivot slot and not the opening slot carries this outlet's bar.

#### 3.1 · The moves, written as slots
(each position, with what fills it rather than a sentence to copy)
M1 takes `<patient-facing fact about the clinical problem>` and never the system name, which is the first anti-pattern the pack lists.
M3 takes `Here we <study verb> a <design> in <n sites or participants>`, so the design adjectives that this desk desk-rejects on, prospective and multi-center, are visible before any result.
M5 takes `<count/denominator (%)> in <arm A> and <count/denominator (%)> in <arm B> (<estimate> <lo> to <hi>, P = <p>)`, and natmed-abstract/style.md gives the shape from brinton-2026 with the aOR, the 95% CI and the P value all inline.
M7 takes `<who> should <do what>`, addressed to clinicians, developers, policymakers or regulators.
M8 takes `<registry name>: <id>` and exists only for a trial.

#### 3.2 · What the pack forbids here
(the seven anti-patterns at natmed-abstract/style.md "Anti-patterns")
No labeled Background, Methods, Results or Conclusions fields, and never a bulleted or numbered abstract.
No opening on the method or the system name, no ending on the method, and no detailed methods such as a regression specification or a model architecture.
No effect size without its CI when a trial is reported, and no spinning of a null result: the pack's own examples state a null outcome flatly and let the reader judge.
No passive-heavy construction, since the register mixes an active author voice with reported results.

#### 3.3 · The measured layer is two papers wide
(a caveat that applies to every budget quoted in divisions 3 to 9)
Each `natmed-<kind>/style.md` opens with "Extracted from 14 Nature Medicine exemplar papers", while the exemplars block below lists 24 PDFs on disk, so seven of the stored papers have never been distilled into any norm.
Every "Micro-norms (measured 2026-07-08)" table in this pack is narrower still: it is measured from brinton-2026 and bean-2026 alone, one RCT and one AI evaluation, with two or three sampled paragraphs per paper.
So a number quoted on this page is a measurement of two papers reconciled against a stated range, never a rule the desk publishes.

#### 3.4 · Format values
(the four format numbers a drafting agent needs, each with the pack line it comes from and the base it was measured on)

```text
  📏 WORDS            150-350 w · median ~200 · RCT 250-350 w · 1 unstructured paragraph · 9-10 sentences · 5-32 w/sentence, median ~18   [natmed-abstract/style.md · Word budget + Micro-norms · measured base brinton-2026 + bean-2026 ONLY, of 24 papers on disk]
  📚 CITATION DENSITY 0 per sentence · this outlet's abstracts carry no numbered references   [natmed-abstract/style.md · Micro-norms · measured base brinton-2026 + bean-2026 ONLY]
  🔢 VALUE DENSITY    not recorded by the pack   [no natmed-<kind>/style.md records numeric values per sentence under that name or any other]
  📊 DISPLAYS         not recorded by the pack   [natmed-abstract/style.md carries no display line, and its arc ends on the trial registration id]
```

#### 3.5 · The language, in the papers' own words
(five sentences natmed-abstract/style.md already quotes, one move each, tied to the slots at 3.1)
"Prioritizing artificial intelligence (AI)-detected imaging findings may reduce the time to diagnosis of lung cancer." [Varoquaux 2026]
The translational opener: M1 is filled by a patient consequence, and the AI enters as the thing being tested rather than the thing being announced.
"LLMs now achieve nearly perfect scores on medical licensing exams, but this does not necessarily translate to accurate performance in real-world settings." [Bean 2026]
The evidence-tier gap sentence: M2 names the tier that exists, exam performance, against the tier that does not, real-world performance.
"Here we conducted a pragmatic, cluster-randomized trial in 16 primary care facilities in Kenya." [Brinton 2026]
The design declaration: M3's `Here we <study verb> a <design> in <n sites or participants>`, with the site count inside the pivot itself.
"corresponding to a ratio of geometric means of 0.97 (95% confidence interval (CI) = 0.93-1.02; P = 0.31)" [Varoquaux 2026]
The primary-endpoint sentence with its estimate: M5 carrying the point estimate, the 95% CI and the P value in one parenthesis.
"In this trial, LLM assistance was safe but did not reduce treatment failure within 14 days and any benefit, if present, is probably modest." [Brinton 2026]
The plainly stated null, which is the nearest thing an abstract has to a limitation, and the anti-pattern at 3.2 that forbids spinning it.

### 4 · Introduction: a clinical funnel that names the missing tier

**The funnel and its gap sentence**: four to five flat paragraphs that narrow from a patient burden to a named evidence gap, then pivot to the study.

```text
  📐 ARC · natmed-introduction/style.md "Arc"
     P1  clinical problem, patient burden
     P2  current practice and its limitations
     P3  technology promise, then the NAMED gap
     P4  "Here we" / "In this study, we" pivot
     P5  optional scope preview: sites, comparators

  📏 BUDGET · natmed-introduction/style.md "Word budget"
     words              350-1,200, typical 750-1,000
     paragraphs         4-9, modal 4-5
     Brief Comm         no labeled Introduction, first 350-500 w

  🔬 MEASURED 2026-07-08 · natmed-introduction/style.md "Micro-norms"
     brinton-2026       4 paragraphs
     bean-2026          9 paragraphs
     sentences/para     4-11, median ~4-5
     words/sentence     12-64, median ~26
     markers/paper      ~13-15, ~22-25 distinct refs
     density            0.4-0.7 per sentence
     pivot paragraph    0-1 references

  ⚖️ SHORTER THAN NMI ON PURPOSE
     NMI                550-1,600 w, opens on domain importance
     Nature Medicine    350-1,200 w, opens on a patient burden
```

🩺 Establishes the gap sentence as the load-bearing slot: it is where the paper names which tier of evidence is missing, and therefore which tier its own design must supply.

#### 4.1 · The gap slot names a tier, not an absence
(why "little is known" fails here and "prospective evidence remains limited" passes)
natmed-introduction/style.md requires the gap to be specific and named, and its exemplars all name an evidence tier: brinton-2026 says prospective interventional evidence from real-world studies remains limited, osullivan-2026 says it remains unclear whether the model replicates expert decision-making, and zhou-2026 names the underrepresentation of multi-ethnic populations and the lack of validation for multidisease risk stratification.
The slot is `However, <evidence tier> evidence for <population or setting> remains <limited | untested | poorly characterized>.`
This is the sentence the venue stage can read to see whether the paper has claimed a tier it did not actually collect, which is the failure division 1 above describes.

#### 4.2 · The moves and the anti-patterns
(what fills P1 and P4, and the seven things the pack refuses)
P1 takes `<condition or setting> accounts for <burden>` or `Globally, there is a <shortage or gap> in <care>`, with the subject being patients or a health system, never a technology.
P4 takes `Here we conducted a <design> in <setting>` or `To address this, we introduce <system>`, framed as clinical evidence generation rather than a technical advance, and the citation density falls to zero or one marker.
A study-design or CONSORT Figure 1 may be cited from P4, and natmed-introduction/template.md rules that this figure is a display request, never a probe question.
The pack forbids opening with the technology, a separate Related Work or Background subsection, a bulleted "First, Second, Third" contribution list, author-year citations, more than two or three sentences per prior-work category, results inside the introduction, and framing the contribution as a technical advance.

#### 4.3 · Format values
(the same four rows for the Introduction, the section whose citation density this pack states most precisely)

```text
  📏 WORDS            350-1,200 w · typical 750-1,000 · 4-9 paragraphs, modal 4-5 · 4-11 sentences/paragraph, median ~4-5 · 12-64 w/sentence, median ~26   [natmed-introduction/style.md · Word budget + Micro-norms · measured base brinton-2026 + bean-2026 ONLY, of 24 papers on disk]
  📚 CITATION DENSITY ~0.4-0.7 per sentence · ~13-15 markers per paper, ~22-25 distinct refs · 0-1 markers in the pivot paragraph   [natmed-introduction/style.md · Micro-norms · measured base brinton-2026 + bean-2026 ONLY]
  🔢 VALUE DENSITY    not recorded by the pack   [no natmed-<kind>/style.md records numeric values per sentence under that name or any other]
  📊 DISPLAYS         no budget of its own · the pivot paragraph may CITE Fig. 1, the study-design schematic or CONSORT diagram that the Results budget pays for   [natmed-introduction/style.md · Signature moves 4 · saab-2026 and brinton-2026]
```

#### 4.4 · The language, in the papers' own words
(four sentences natmed-introduction/style.md already quotes, plus the two moves its arc has no slot for)
"Infectious diseases account for the majority of the 2.5 million deaths that occur each year among children aged 1-59 months." [Nijman 2026]
The translational opener: P1 puts a patient burden in the subject position, which is the anti-pattern test 4.2 states.
"However, prospective interventional evidence from real-world clinical studies, particularly in LMICs, remains limited." [Brinton 2026]
The evidence-tier gap sentence, filling the 4.1 slot with the exact tier this desk rejects papers for failing to supply.
"In this study, we aim to introduce Reti-Pioneer, a multitask framework, and conduct a biology-linked, stepwise, multi-site clinical validation study" [Zhou 2026]
The design declaration: the P4 pivot carries multi-site inside the noun phrase, so the validation tier is readable before any result.
"Figure 1 shows the CONSORT diagram of participant and cluster progression throughout the trial." [Brinton 2026]
The one display reference this section makes, which 4.2 rules is a display request and never a probe question.
No primary-endpoint sentence and no limitation appear here: natmed-introduction/style.md forbids results in the Introduction, and its arc has no limitation position.

### 5 · Related work: the kind with no section of its own

**Declared everywhere in this family, printed nowhere**: `related-work` is a real section-edit unit for all five Nature outlets, and its output is distributed prose rather than a heading.

```text
  📋 DECLARED · stages/section-kinds.yml "outlets"
     Nature family     all five outlets carry related-work
     IS family         carry theory instead, which DEVELOPS a model
     every other pack  carry neither
     not aliases       SITUATES against literature vs DEVELOPS one

  🚫 NEVER PRINTED · natmed-related-work/style.md "The core rule"
     standalone heading   NONE of the 14 exemplars carries one
     Introduction         the evidence gap, primary location
     Discussion           positioning against prior trials
     Results              rare, only to motivate a benchmark comparison
     Supplementary        extended review, when needed

  📏 BUDGET · natmed-related-work/style.md "Micro-norms"
     allotment          none, draws on introduction + discussion
     intro background   2-3 paragraphs per paper
     discussion         1 positioning paragraph per paper
     sentences/para     4-11, median ~5 intro, ~9 discussion
     words/sentence     12-44, median ~24

  📚 THE CITATION PEAK OF THE WHOLE MANUSCRIPT
     markers/para       3-5 per intro background paragraph
     density            0.5-1.0 per sentence
     distinct refs      brinton-2026 ~25, bean-2026 ~22
     next paragraph     0-1, the contribution pivot

  🪜 ORDERED BY EVIDENCE TIER, NEVER BY DATE
     retrospective -> vignette -> prospective -> real-world
```

🔗 Establishes the only kind whose page projects into three manuscript sections instead of becoming one, and records that the tier ladder it sorts on is the same ladder this desk rejects on.

#### 5.1 · A declared unit whose output the manuscript never shows
(what section-edit runs on, and where the prose actually lands)
`stages/section-kinds.yml` declares `related-work` for all five Nature outlets and for no outlet in any other pack, so this is a real unit: section-edit runs on it and writes it an `S-Main-<n>` page like any other section.
What that page holds is a distributed positioning narrative rather than a section draft, and its paragraphs project into the Introduction, the Discussion and, rarely, the Results, while the manuscript never grows a heading called Related Work.
The pack says so in three independent places: natmed-related-work/style.md opens on the core rule that no standalone section exists and calls one a structural violation, natmed-introduction/style.md repeats it as signature move 6 and as an anti-pattern, and the family README carries it as a convention holding across every `*-related-work/style.md` in the pack.
It is also not the IS family's `theory`, and section-kinds.yml states the difference instead of aliasing the two: `theory` develops a model and its hypotheses, `related-work` situates a paper against prior literature.
natmed-related-work/template.md closes the loop by ruling that a `related-work` unit expecting a standalone heading is itself the defect, to be flagged as a norm conflict in the log.

#### 5.2 · The two halves, as slots
(what the introduction half and the discussion half each take)
The introduction half takes `<evidence category> have shown <result>. However, <the limitation of that category>.` repeated for two or three categories, each characterized in one or two clauses and never reviewed paper by paper.
It closes on the gap statement that division 4 owns.
The discussion half takes `Our finding of <X> <aligns with | contrasts with> <prior evidence>, which reported <Y>.`, positioning by study design, population or capability rather than by date.
The rare Results touch takes a single clause naming the prior benchmark that motivates a comparison, and natmed-related-work/style.md gives bean-2026 scoring a targeted subset of MedQA as its only exemplar.
The pack forbids a standalone section, full-paragraph reviews of single works, chronological ordering, author-year citations, front-loading all comparison into the introduction, and dense citation inside the contribution paragraph.

#### 5.3 · One exemplar in this file is borrowed
(a known hole the pack itself marks)
natmed-related-work/style.md carries a positioning-by-scale example lifted from an NMI exemplar, marked in the file as borrowed and to be replaced when a Nature Medicine paper is mined for the same move.
Both this file and natmed-discussion/template.md repeat the borrowed line, so replacing it is a two-file edit.

#### 5.4 · Format values
(a unit with no section of its own, so its rows record what it COSTS the sections that host it)

```text
  📏 WORDS            no allotment of its own · it spends 2-3 Introduction background paragraphs and 1 Discussion positioning paragraph per paper, and rarely one Results clause · 4-11 sentences/paragraph, median ~5 in the intro half and ~9 in the discussion half · 12-44 w/sentence, median ~24   [natmed-related-work/style.md · The core rule + Micro-norms · measured base brinton-2026 + bean-2026 ONLY, of 24 papers on disk]
  📚 CITATION DENSITY ~0.5-1.0 per sentence, the densest in the manuscript · 3-5 markers per Introduction background paragraph · distinct intro refs brinton-2026 ~25, bean-2026 ~22   [natmed-related-work/style.md · Micro-norms · measured base brinton-2026 + bean-2026 ONLY]
  🔢 VALUE DENSITY    not recorded by the pack   [no natmed-<kind>/style.md records numeric values per sentence under that name or any other]
  📊 DISPLAYS         none of its own, and it adds no figure or table to the Introduction, Discussion or Results that host it · an extensive background overflows into Supplementary Information instead   [natmed-related-work/style.md · The core rule, location 3]
```

#### 5.5 · The language, in the papers' own words
(five sentences natmed-related-work/style.md quotes for this unit, and the one it quotes that is not this outlet's)
"Key gaps persist, including the underrepresentation of multi-ethnic populations and the lack of sufficient validation for multidisease risk stratification." [Zhou 2026]
The evidence-tier gap sentence, closing the Introduction half of the slot pair at 5.2.
"Vignette-based comparisons suggest that LLMs can match or exceed provider performance on some diagnostic and triage tasks." [Brinton 2026]
The category characterization: one clause per evidence tier, which is how the tier ladder at 5.1 gets written rather than reviewed.
"The improvement in process outcomes observed aligns with findings from both controlled and real-world studies." [Brinton 2026]
The Discussion half's alignment move, positioning by study design rather than by date.
"Our finding of no significant demographic bias contrasts with ref. 7, which reported race and sex effects in general-purpose LLMs." [Levine 2026]
The same slot in its contrast form, naming the prior finding it disagrees with instead of the year it appeared.
"we scored the LLMs on a targeted subset of the popular MedQA benchmark" [Bean 2026]
The rare Results touch, a single clause naming the benchmark that motivates a comparison.
The file's positioning-by-scale example is still the borrowed pontikos sentence from an NMI paper, marked borrowed in the file and unreplaced, so it is not quoted above and must never be shown as this outlet's own.

### 6 · Methods: a clinical protocol placed after Discussion

**A protocol, not a model card**: eight to fourteen subsections in a fixed order, ending on three mandatory availability blocks.

```text
  📐 ARC · natmed-methods/style.md "Arc"
     design -> participants -> intervention -> randomization
     -> outcomes -> sample size -> data collection
     -> statistical analysis -> ethics
     -> reporting summary -> data availability -> code availability

  📍 PLACEMENT · all 14 exemplars
     order              Discussion -> Methods -> References
     label              "Methods", never "Online Methods"

  📏 BUDGET · natmed-methods/style.md "Word budget"
     words              1,500-5,000+, 3-8 pages
     Brief Comm         ~600 w
     length rank        often the LONGEST section, above Results

  🔬 MEASURED 2026-07-08 · natmed-methods/style.md "Micro-norms"
     subsections        brinton-2026 11, bean-2026 12
     paragraphs each    1-4
     sentences/para     2-12, median ~8
     words/sentence     6-43, median ~20, shortest body section
     citations          0.05-0.1 per sentence
     cited to           reporting standards, benchmarks, instruments
```

🧪 Establishes Methods as the section where this desk's unacquirable bar is either discharged in the first sentence or exposed as absent.

#### 6.1 · The first sentence is where the validation design is declared
(the study-design opener carries prospective, multi-center and the site count)
The exemplar openers stack the design adjectives before the noun: brinton-2026 opens on a pragmatic, multicenter, parallel-group cluster-randomized controlled trial across 16 primary care facilities, and varoquaux-2026 opens on a prospective, multicenter, randomized controlled trial conducted across five NHS Trusts between stated dates.
The slot is `A <prospective | retrospective>, <multicenter | single-center>, <design> was conducted <dates> across <n> <site type>.`
A paper that cannot fill the first two positions has already met the desk-reject line drawn in the Diagram above, and no later subsection recovers it.
For an AI system paper the Participants subsection becomes dataset provenance and the Intervention subsection becomes the system description, which is the substitution that makes a single-source retrospective cohort visible as exactly one dataset.

#### 6.2 · Validation cohorts arrive through Participants, Outcomes and the standard
(three subsections carry what the desk checks, and each has its own slot)
Participants carries eligibility, recruitment and setting per site, so a multi-center design is reported as a roster rather than as an adjective.
Outcomes defines the primary and every secondary outcome precisely, and natmed-methods/template.md notes these definitions bind how Results may report them.
The reporting standard named in Methods is the tier's witness: CONSORT-AI and the CONSORT cluster extension for a trial, PRISMA 2020 for a review, TRIPOD for a prediction model, and TRIPOD is the one that governs external validation reporting.
Sample size arrives with a full power calculation, and the pack's brinton-2026 example states the design effect, the power, the two-sided alpha, the assumed loss to follow-up and the target enrollment in one chain.

#### 6.3 · Ethics is longer here than anywhere else in the portfolio
(what the pack demands by name, and what it refuses)
Ethics names the committee with its approval number, states written informed consent, records any regulatory determination, describes the Data Safety Monitoring Board for a trial, and may carry a separate equity and inclusion statement about local co-design.
natmed-methods/style.md contrasts this directly with NMI, whose Methods never name an ethics committee.
The closing subsections are mandatory: Reporting summary pointing at the Nature Portfolio Reporting Summary, Data availability, and Code availability, each with a URL or a stated access route.
The pack forbids placing Methods before Results, omitting ethics detail, omitting the sample size calculation for a trial, omitting Data or Code availability, omitting the Reporting summary pointer, merging method into result, omitting exact software versions, and writing exclusively in the passive.

#### 6.4 · Format values
(the longest section in the paper, and the one with the lowest citation density in it)

```text
  📏 WORDS            1,500-5,000+ w over 3-8 pages · Brief Communication ~600 w · 11-12 subsections, 1-4 paragraphs each · 2-12 sentences/paragraph, median ~8 · 6-43 w/sentence, median ~20   [natmed-methods/style.md · Word budget + Micro-norms · measured base brinton-2026 + bean-2026 ONLY, of 24 papers on disk]
  📚 CITATION DENSITY ~0.05-0.1 per sentence · brinton-2026 ~3-4 markers, bean-2026 ~7 · cited only to reporting standards, benchmarks and named instruments   [natmed-methods/style.md · Micro-norms · measured base brinton-2026 + bean-2026 ONLY]
  🔢 VALUE DENSITY    not recorded by the pack   [no natmed-<kind>/style.md records numeric values per sentence under that name or any other]
  📊 DISPLAYS         not recorded by the pack   [natmed-methods/style.md lists no display item in its arc, which ends on Reporting summary, Data availability and Code availability]
```

#### 6.5 · The language, in the papers' own words
(five sentences natmed-methods/style.md already quotes, four of them from the subsections this desk actually checks)
"A prospective, multicenter, randomized controlled trial was conducted between July 2023 and December 2024 across five NHS Trusts in England." [Varoquaux 2026]
The prospective and multicentre design declaration, filling the whole 6.1 slot: both unacquirable adjectives and the site count arrive in one sentence.
"This review was conducted and reported in accordance with the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA) 2020 guidelines." [Lu 2026]
The reporting standard 6.2 calls the tier's witness, here in its review form rather than the CONSORT-AI form a trial takes.
"we calculated that 265 cases per group would be needed to detect a difference with 95% power" [Varoquaux 2026]
The sample-size clause 6.2 pairs with the design, because a trial that omits it meets a Methods anti-pattern.
"For binary outcomes (including the primary outcome), a mixed-effects logistic regression model was used to estimate the aOR, with its corresponding 95% CI." [Brinton 2026]
The estimator behind the primary-endpoint sentence, promising the interval Results is then obliged to print.
"This study was approved by the NYU Langone Institutional Review Board (i23-00510)." [Restrepo 2026]
The ethics move at 6.3, named committee plus approval number, which the pack records as absent from NMI entirely.

### 7 · Results: descriptive headings, every estimate with its CI

**Two arcs and one reporting rule**: the subsection headings stay procedural, the tables stay in the main text, and no estimate appears without its interval.

```text
  📐 TWO ARCS · natmed-results/style.md "Arc"
     RCT        disposition -> primary -> secondary -> safety -> post hoc
     AI eval    setup -> main comparison -> subgroup -> robustness

  📏 BUDGET · natmed-results/style.md "Word budget"
     words              1,500-3,500, 3-6 pages
     share of body      30-45 percent, below NMI's 40-50
     bean-2026          ~1,500 w, 5 subsections, 4 figures
     brinton-2026       ~1,200 w, 6 subsections, 3 figures + 2 tables
     varoquaux-2026     ~1,800 w, 4 subsections, 5 tables + 1 figure

  🔬 MEASURED 2026-07-08 · natmed-results/style.md "Micro-norms"
     paragraphs         ~10-11 per paper, 5-6 subsections
     sentences/para     2-8, median ~3-4
     words/sentence     17-67, median ~27
     stat sentences     53-67 w, every estimate carries CI and P
     citations          ~0, Results cites its own figures and tables
```

📊 Establishes the two shapes a Nature Medicine Results can take, and records that the pack has no measured norm for reporting an external validation cohort.

#### 7.1 · The moves, as slots
(headings, inline sub-headings, statistics and tables)
A subsection heading takes a procedural noun phrase such as `Patient disposition` or `Primary outcome`, not a claim; natmed-results/style.md records declarative headings in two AI system papers, zhou-2026 and khasentino-2025, and calls descriptive headings the dominant pattern.
Inside a subsection, fine-grained results take `**<Bold inline sub-heading>.**` followed by their own statistics.
An estimate takes `<estimate> (95% CI <lo> to <hi>; P = <p>)`, with the interval written in words for trials and with a dash or colon for evaluation papers.
Main-text tables belong here and are the sharpest divergence from NMI: a baseline characteristics table and a primary-outcome-by-arm table are the standard pair, and the pack lists eight exemplars carrying between one and five main-text tables.

#### 7.2 · Where external validation actually lands
(the pack names no external-validation subsection, so three existing slots carry it)
natmed-results/style.md has no subsection for external, multi-center or held-out validation, and its two arcs stop at subgroup analyses and robustness.
The multi-site evidence therefore lands in slots the pack does measure: the disposition slot, whose enrollment sentence names every contributing site, as when varoquaux-2026 reports 97,731 chest radiographs across five NHS Trusts; the subgroup slot, listed in the AI-evaluation arc as modality, difficulty and specialty; and the per-cohort estimate itself, as when zhou-2026 reports an AUROC of 0.833 with a 95% CI of 0.810 to 0.856.
This is a hole in the pack rather than a silence of the desk, since the exemplar base includes multi-site validation papers that no style.md has been mined for, and A7.1 below holds it open.

#### 7.3 · What the pack forbids here
(seven refusals, several of them inversions of the NMI norm)
No declarative claim headings as the default, no avoidance of main-text tables, no missing CONSORT flow diagram for a trial, no reporting of positive findings only, no effect size without its CI, no safety reporting moved out of Results, and no benchmark results placed ahead of clinical outcomes in a clinical validation paper.

#### 7.4 · Format values
(the one division whose display evidence rests on nine named papers instead of two)

```text
  📏 WORDS            1,500-3,500 w over 3-6 pages · 30-45 percent of the body · ~10-11 paragraphs across 5-6 subsections · 2-8 sentences/paragraph, median ~3-4 · 17-67 w/sentence, median ~27   [natmed-results/style.md · Word budget + Micro-norms · measured base brinton-2026 + bean-2026 ONLY, of 24 papers on disk]
  📚 CITATION DENSITY ~0-0.05 per sentence · brinton-2026 ~0 markers, bean-2026 ~4-5 benchmark refs only · Results cites its own figures and tables, not the literature   [natmed-results/style.md · Micro-norms · measured base brinton-2026 + bean-2026 ONLY]
  🔢 VALUE DENSITY    not recorded by the pack · the nearest pack line is stat-bearing sentences running 53-67 words, which is a sentence LENGTH and not a per-sentence count of values   [natmed-results/style.md · Micro-norms note · measured base brinton-2026 + bean-2026 ONLY]
  📊 DISPLAYS         main text 1-6 figures and 0-5 tables · bean-2026 4 figs + 0 tables · brinton-2026 3 figs + 2 tables · varoquaux-2026 1 fig + 5 tables · lang-2026 2 figs + 4 tables · Extended Data and Supplementary are budgeted at division 9   [natmed-results/style.md · Word budget + Signature moves 3 · base = the nine papers listed there, wider than the two-paper micro-norms]
```

#### 7.5 · The language, in the papers' own words
(five sentences natmed-results/style.md already quotes, in the order the RCT arc runs)
"To assess the risks of the public using LLMs for medical advice, we conducted a randomized study" [Bean 2026]
The setup clause that opens a subsection, one sentence of purpose before any number, per the micro-arc 7.1 describes.
"Between 17 July 2023 and 31 December 2024, a total of 97,731 CXRs were performed across five diverse National Health Service (NHS) Trusts" [Varoquaux 2026]
The multicentre declaration inside the disposition slot, which 7.2 identifies as one of the three places multi-site evidence actually lands.
"adjusted odds ratio (aOR) 0.77, 95% CI 0.55 to 1.08, P = 0.13" [Brinton 2026]
The primary-endpoint estimate in the trial form of the 7.1 slot, interval spelled out in words.
"0.833 (95% CI 0.810-0.856)" [Zhou 2026]
The same slot in its evaluation form, interval written with a dash, and the per-cohort estimate 7.2 routes validation evidence into.
"The primary outcome did not differ significantly between groups, extending emerging evidence from recent randomized evaluations in other clinical settings." [Brinton 2026]
The plainly stated null, the closest Results comes to a limitation, and the refusal at 7.3 to report positive findings only.

### 8 · Discussion: limitations woven in, never the last word

**A compact close**: six to eight flat paragraphs that restate in clinical terms, position against prior trials, own the limitations, and end on a recommendation.

```text
  📐 ARC · natmed-discussion/style.md "Arc" and "Paragraph structure"
     P1    finding restated in clinical context      ~15%
     P2-3  clinical interpretation                   ~25%
     P4-5  positioning against prior evidence        ~25%
     Plim  limitations paired with mitigations       ~20%
     Pn    implications, "In conclusion"             ~15%

  📏 BUDGET · natmed-discussion/style.md "Word budget"
     words              750-1,800
     paragraphs         4-10, modal 6-8
     length rank        shorter than Results, often shorter than Methods
     Conclusion         no separate section, it opens the last paragraph

  🔬 MEASURED 2026-07-08 · natmed-discussion/style.md "Micro-norms"
     brinton-2026       7-8 paragraphs
     bean-2026          5 paragraphs
     sentences/para     3-9, median ~7
     words/sentence     14-48, median ~28
     citations          0.1-0.2 per sentence
     clustered in       positioning and limitations paragraphs
```

💬 Establishes the Discussion as the second place the design tier is spoken aloud, in the opening restatement and again in the limitation the design forces.

#### 8.1 · The opening restatement re-declares the design
(the same adjectives that Methods proved, now carrying the finding)
The exemplar openers embed the design in the restatement: varoquaux-2026 opens on a large, multisite randomized study, nijman-2026 opens on a multicountry prospective study conducted in seven locations across Asia, and lang-2026 opens on a prospective, paired, noninferiority clinical trial.
The slot is `In this <design descriptor> study <in setting>, we found <finding in clinical terms>.`
natmed-discussion/style.md forbids repeating the abstract verbatim, so the restatement sits one synthesis level above it.

#### 8.2 · Limitations are formulaic, paired and never final
(the one move a single-center paper cannot avoid)
The limitations paragraph opens on a stock phrase, and natmed-discussion/style.md catalogues eleven variants across the exemplars, from a bare "This study has limitations." to a longer request for caution and humility.
Each limitation then takes `<limitation> -> <mitigation or future direction>`, and lang-2026 supplies the pattern a single-site paper must use, pairing the single-site design with the diversity within that site.
Limitations stay woven into the prose flow and never become a labeled subsection, and the Discussion never ends on one.
The close takes `In conclusion,` or `In summary,` plus a clinical recommendation, which the pack contrasts with NMI, whose Discussion never recommends a clinical action.

#### 8.3 · What the pack forbids here
(nine refusals, and the null-result rule is the one with teeth)
No Discussion longer than Results, no new data or analysis, no omitted limitations, no ending on a limitation, no verbatim abstract, no labeled Limitations or Conclusion subsection, no omitted clinical implications, no comprehensive literature review, and no spinning of a null result.
When the primary outcome is null the pack requires one or two paragraphs explaining why, and its examples convert the interval into a clinical quantity, as brinton-2026 does by restating the estimate as between 13 fewer and 1 additional treatment failures per 1,000 patients.

#### 8.4 · Format values
(a section budgeted against Results rather than in its own right)

```text
  📏 WORDS            750-1,800 w · shorter than Results and often shorter than Methods · 4-10 paragraphs, modal 6-8 · 3-9 sentences/paragraph, median ~7 · 14-48 w/sentence, median ~28   [natmed-discussion/style.md · Word budget + Micro-norms · measured base brinton-2026 + bean-2026 ONLY, of 24 papers on disk]
  📚 CITATION DENSITY ~0.1-0.2 per sentence · brinton-2026 ~11 markers, bean-2026 ~4-5 · clustered in the prior-evidence positioning paragraph and the limitations paragraph   [natmed-discussion/style.md · Micro-norms · measured base brinton-2026 + bean-2026 ONLY]
  🔢 VALUE DENSITY    not recorded by the pack   [no natmed-<kind>/style.md records numeric values per sentence under that name or any other]
  📊 DISPLAYS         not recorded by the pack   [natmed-discussion/style.md carries no display line, and its anti-patterns forbid new data or analysis here]
```

#### 8.5 · The language, in the papers' own words
(five sentences natmed-discussion/style.md already quotes, one for each job in this division's arc)
"This multicountry prospective study, conducted in seven locations across Asia, developed and validated clinical prediction models that outperform the current standard of care." [Nijman 2026]
The design declaration restated as the finding, which is the 8.1 opener slot doing this desk's bar a second time.
"Our finding of no significant demographic bias contrasts with ref. 7, which reported race and sex effects in general-purpose LLMs." [Levine 2026]
The positioning move, set against one named prior result rather than a surveyed literature.
"The estimated effect corresponded to between 13 fewer and 1 additional treatment failures per 1,000 patients" [Brinton 2026]
The null-result explanation 8.3 requires, converting the interval into a clinical quantity instead of spinning it.
"Our study has the limitation of being a single-site investigation" [Lang 2026]
The limitation a paper that missed this desk's design bar cannot avoid, and 8.2's worked example of pairing it with a mitigation.
"CXR AI deployments should not include worklist prioritization in this context." [Varoquaux 2026]
The clinical recommendation the close must carry, the move the pack records as absent from NMI.

### 9 · Appendix: three tiers, and a hard cap of ten

**The supplementary tier system**: three tiers with strict boundaries, two numbering sequences, and a cap that forces a triage decision.

```text
  🗂 THREE TIERS · natmed-appendix/style.md "Three-tier system"
     tier             reviewed    location              cap
     Main text        yes         the manuscript        none fixed
     Extended Data    yes         same PDF, after refs  10 items TOTAL
     Supplementary    editorial   separate online file  none

  🔢 NUMBERING AND NAMING
     main             Fig. 1 · Table 1
     extended         Extended Data Fig. 1 · Extended Data Table 1
     supplementary    Supplementary Fig. / Table / Note 1
     caption form     Extended Data Table 1 | Title in sentence case.
     panels           lowercase bold a, b, c
     in-text ref      parenthetical, spelled out, never "ED"

  🔬 MEASURED 2026-07-08 · natmed-appendix/style.md "Micro-norms"
     brinton-2026     3 main figs · 2 main tables · 3 Extended Data
     bean-2026        4 main figs · 0 main tables · 7 Extended Data
     restrepo-2026    8 Extended Data items, 6 figs + 2 tables
     lengths          Article 3,000-5,000 w · Brief Comm 1,500-2,500 w
```

🗄 Establishes the ten-item Extended Data cap as the appendix's real constraint, since a multi-cohort validation paper spends that cap on its per-site breakdowns.

#### 9.1 · What belongs in each tier
(the triage rule, stated as three questions)
Main text holds the core argument: the study-design schematic, the primary-outcome figures and the key comparison plots, with both measured exemplars carrying two to four main-text figures and a Brief Communication limited to two display items.
Extended Data holds peer-reviewed supporting analyses a reviewer must see but that would interrupt the narrative, and natmed-appendix/style.md names the recurring kinds: subgroup breakdowns and secondary analyses, evaluation rubrics and instruments, representative qualitative examples, descriptive reference tables, platform screenshots and pairwise statistical comparison panels.
Supplementary Information holds everything else, and the pack names full scenario texts, detailed demographics, hyperparameter tables, power analyses, cost breakdowns and exhaustive per-condition results.
Because subgroup breakdowns are named Extended Data content, the per-site and per-cohort tables that carry this desk's external validation compete directly for the ten-item cap.

#### 9.2 · The cap and the rules that hang off it
(what a paper must do once it accepts ten items)
The cap is ten items total across Extended Data figures and tables combined, and both measured exemplars sit inside it at three and seven.
Each Extended Data item occupies one full published page, captions run 100 to 200 words, tables are typeset rather than screenshots of spreadsheets, and the main text must cite every Extended Data item at least once.
Supplementary Information is a separate file with no cap, not paginated with the article, checked editorially rather than sent to reviewers as a mandatory read.
The Nature Portfolio Reporting Summary is a separate required three-page form and is not part of Supplementary Information, and the paper closes with a fixed-order block running from Online content through Data and Code availability to the correspondence and peer-review pointers.

#### 9.3 · Two holes in this file, unlike the other six
(a contradiction the pack states without resolving, and a missing Anti-patterns section)
natmed-appendix/style.md says Extended Data and Supplementary Information have independent numbering sequences, with figures and tables both starting at 1 inside each tier, and then observes that bean-2026's Supplementary tables begin above the Extended Data table count, which it reads as suggesting a single continuous table sequence across tiers.
Both statements sit in the same file and nothing chooses between them, so a drafting agent numbering a Supplementary table has two defensible answers; A9.1 below holds it open.
This is also the only one of the seven kind files with no "Anti-patterns" heading: its prohibitions are inline, namely never abbreviating Extended Data to "ED", never exceeding ten items, never submitting a spreadsheet screenshot as a table, and never leaving an Extended Data item uncited in the main text.

#### 9.4 · Format values
(the division whose rows are display inventories, because the pack drops prose metrics here and counts items instead)

```text
  📏 WORDS            main text Article ~3,000-5,000 w · Brief Communication ~1,500-2,500 w · Extended Data captions 100-200 w at one published page per item · Supplementary Information typically 10-30 pages, no limit   [natmed-appendix/style.md · Length norms · base bean-2026 and restrepo-2026]
  📚 CITATION DENSITY not recorded by the pack   [natmed-appendix/style.md · Micro-norms preamble rules that prose sentence and word metrics do not apply to these tiers]
  🔢 VALUE DENSITY    not recorded by the pack   [no natmed-<kind>/style.md records numeric values per sentence under that name or any other]
  📊 DISPLAYS         main text brinton-2026 3 figs + 2 tables, bean-2026 4 figs + 0 tables · Extended Data brinton-2026 3 items, bean-2026 7, restrepo-2026 8, hard cap 10 total · Supplementary uncapped, bean-2026 runs to ~11 tables plus Fig. 6   [natmed-appendix/style.md · Micro-norms + Three-tier system · base brinton-2026, bean-2026, restrepo-2026]
```

#### 9.5 · The language, in the papers' own words
(the one kind file that quotes no prose, so nothing is quoted here)
natmed-appendix/style.md has no "Signature moves" heading and no "Exemplar sentences" heading, and it quotes no sentence from any paper.
Its only attributed strings are typographic: the caption form `Extended Data Table 1 | Title in sentence case.` and the in-text form `(Extended Data Fig. 1a,b)`, both credited to bean-2026 and restrepo-2026.
Those are formats and not language, so this division has no voice to copy, and writing one would put a sentence in this outlet's mouth that no exemplar said.
It is the same thinness recorded at 9.3, where the file's prohibitions sit inline because it carries no Anti-patterns heading either.

## Aims

### A1 · ⏳ The bar is set before the paper exists
- A1.1 · A validation-design gate runs before this outlet is shortlisted.
  **Done when:** a retrospective single-center study is not recommended here by the venue stage.

### A2 · 🔀 Where it sits against its four siblings
- A2.1 · The Nature Medicine against npj Digital Medicine boundary is written as a test rather than a description.
  **Done when:** a clinical digital-health candidate is routed between the two on a stated question.

### A3 · 📝 Abstract: one paragraph that closes on a clinical action
- A3.1 · The abstract variant is chosen before any budget is quoted, since Article, RCT and Brief Communication carry different word caps and only the RCT ends on a registration id.
  **Done when:** a drafted abstract states which of the three variants it fills and holds itself to that variant's cap.

### A4 · 🩺 Introduction: a clinical funnel that names the missing tier
- A4.1 · The gap sentence names an evidence tier rather than an absence of knowledge.
  **Done when:** a drafted introduction's gap sentence names retrospective, vignette, prospective or real-world evidence, and the study's own design supplies the named tier.

### A5 · 🔗 Related work: the kind with no section of its own
- A5.1 · The `related-work` S page names, paragraph by paragraph, which manuscript section receives it.
  **Done when:** a Nature Medicine paper's related-work page reads as a routing plan into introduction, discussion and results, and no draft grows a Related Work heading.
- A5.2 · The borrowed NMI positioning exemplar is replaced with a mined Nature Medicine sentence.
  **Done when:** natmed-related-work/style.md and natmed-discussion/template.md both quote a Nature Medicine paper for the positioning-by-scale move.

### A6 · 🧪 Methods: a clinical protocol placed after Discussion
- A6.1 · A draft's validation design is readable from the first sentence of its Methods.
  **Done when:** the venue stage can lift the prospective or retrospective adjective, the center count and the design from that sentence and compare them against this desk's desk-reject line.

### A7 · 📊 Results: descriptive headings, every estimate with its CI
- A7.1 · The pack carries a measured norm for reporting an external validation cohort in Results.
  **Done when:** natmed-results/style.md holds an external-validation slot mined from the multi-site exemplars on disk, with its own arc position and measured counts.

### A8 · 💬 Discussion: limitations woven in, never the last word
- A8.1 · A single-center or retrospective draft pairs the design limitation with a stated mitigation instead of leaving it bare.
  **Done when:** the limitation appears in the limitations paragraph with its mitigation, and the Discussion still closes on a clinical recommendation.

### A9 · 🗄 Appendix: three tiers, and a hard cap of ten
- A9.1 · The Supplementary numbering contradiction inside natmed-appendix/style.md is settled.
  **Done when:** the file states one rule for whether Supplementary tables continue past the Extended Data tables or restart at 1, and drops the other reading.

## States

### A1 · ⏳ The bar is set before the paper exists
- ⬜ A1.1 · Not started, and shared with `QBv8` and `QBv2`.

### A2 · 🔀 Where it sits against its four siblings
- ⬜ A2.1 · Not started. Both taste files exist and nothing compares them.

### A3 · 📝 Abstract: one paragraph that closes on a clinical action
- ⬜ A3.1 · Not started. natmed-abstract/template.md already prints the three variants at its `PICK THE VARIANT` line, and nothing forces a choice.

### A4 · 🩺 Introduction: a clinical funnel that names the missing tier
- ⬜ A4.1 · Not started. The tier vocabulary is written down in `../style-profile.md` and in natmed-related-work/style.md, and no check reads a draft against it.

### A5 · 🔗 Related work: the kind with no section of its own
- ⬜ A5.1 · Not started. The kind is declared for all five Nature outlets in `stages/section-kinds.yml` and its template already refuses a standalone heading, so only the S page's own shape is open.
- ⬜ A5.2 · Not started. The borrowed line is marked as borrowed in natmed-related-work/style.md, so the hole is known and unfilled.

### A6 · 🧪 Methods: a clinical protocol placed after Discussion
- ⬜ A6.1 · Not started, and shared with A1.1: both want the same design facts read before a venue is recommended.

### A7 · 📊 Results: descriptive headings, every estimate with its CI
- ⬜ A7.1 · Not started. Seven of the 24 stored exemplars have never been distilled, and the multi-site validation papers are among them.

### A8 · 💬 Discussion: limitations woven in, never the last word
- ⬜ A8.1 · Not started. lang-2026 supplies the pairing pattern and nothing applies it to a draft.

### A9 · 🗄 Appendix: three tiers, and a hard cap of ten
- ⬜ A9.1 · Not started. Both readings sit in natmed-appendix/style.md, one in its numbering rule and one in its bean-2026 observation.

## Files

- `../../paper/venue/playbook-nature-portfolio/nature-medicine/taste.md` · the desk signals and the one-sentence test
- `QBv8-npj-digital-medicine.md` · the sibling this outlet is decided against
- `QBv2-isr.md` · the same unacquirable-property trap in the IS family

<!-- exemplars:begin -->

📚 **Exemplars** · 24 papers on disk · the section guides were mined from 14 of them, so 10 stored papers back no norm, regenerated by `_tools/sync-exemplars.py`

- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/afshar-2025-natmed-ai-screening-opioid-use-disorder.pdf` · Afshar 2025
- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/alber-2025-natmed-llm-data-poisoning.pdf` · Alber 2025
- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/all-of-us-2026-natmed-wearables-dataset.pdf` · All-Of-Us 2026
- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/bean-2026-natmed-llm-reliability-medical-assistants.pdf` · Bean 2026
- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/bedi-2026-natmed-medhelm-holistic-eval-llms.pdf` · Bedi 2026
- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/brinton-2026-natmed-ai-clinical-decision-support-primary-care.pdf` · Brinton 2026
- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/degenhardt-2026-natmed-global-burden-opioid.pdf` · Degenhardt 2026
- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/hawkes-2026-natmed-y-chromosome-diabetes.pdf` · Hawkes 2026
- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/khasentino-2025-natmed-personal-health-llm.pdf` · Khasentino 2025
- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/lang-2026-natmed-ai-triage-mammography.pdf` · Lang 2026
- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/levine-2026-natmed-chatgpt-triage.pdf` · Levine 2026
- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/lu-2026-natmed-llm-systematic-review.pdf` · Lu 2026
- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/mccoy-2026-natmed-glp1-type1-diabetes.pdf` · Mccoy 2026
- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/nijman-2026-natmed-predicting-referral-febrile-children.pdf` · Nijman 2026
- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/osullivan-2026-natmed-llm-cardiology.pdf` · Osullivan 2026
- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/perez-2026-natmed-remote-monitoring-heart-failure.pdf` · Perez 2026
- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/restrepo-2026-natmed-llms-outperform-specialized-clinical-ai.pdf` · Restrepo 2026
- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/saab-2026-natmed-conversational-diagnostic-ai.pdf` · Saab 2026
- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/sandmann-2025-natmed-deepseek-clinical-benchmark.pdf` · Sandmann 2025
- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/tao-2026-natmed-llm-chatbot-care-transitions.pdf` · Tao 2026
- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/vaidya-2026-natmed-agentic-framework-cancer-pathology.pdf` · Vaidya 2026
- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/varoquaux-2026-natmed-ai-chest-xray-prioritization.pdf` · Varoquaux 2026
- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/yao-2026-natmed-data-driven-weight-loss.pdf` · Yao 2026
- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/zhou-2026-natmed-ai-multidisease-retinal-imaging.pdf` · Zhou 2026

- `../../paper/venue/playbook-nature-portfolio/nature-medicine/examples/INDEX.md` · the pack's own manifest, not an exemplar

<!-- exemplars:end -->

<!-- kinds:begin -->

📐 **Section kinds** · 7 declared in `stages/section-kinds.yml`, regenerated by `_tools/sync-exemplars.py`

Each kind is one unit `section-edit` runs on, and one page it writes: 6 numbered `S-Main-<n>` pages plus `S-Appendix-<letter>`.

- `S-Main-0` · abstract
- `S-Main-1` · introduction
- `S-Main-2` · related-work
- `S-Main-3` · methods
- `S-Main-4` · results
- `S-Main-5` · discussion
- `S-Appendix-A` · appendix

A kind is the MINIMUM unit a paper here gets, not a ceiling: a real paper may split one kind across several numbered Main pages (this repo's own MISQ paper runs to `S-Main-8-conclusion`), and the numbers above shift with it. What does not shift is the ORDER, which is this venue's reader order and not a house default.

<!-- kinds:end -->

🔗 **Authority** · the venue's own instructions, fetched and verified 260802

- [Submission guidelines](https://www.nature.com/nm/submission-guidelines) · the per-journal door, which routes to two pages that matter here. [Formatting your initial submission](https://www.nature.com/nm/submission-guidelines/initial-formatting) governs what is sent first: "We accept initial submissions in PDF, Word or TeX/LaTeX formats; if you are using TeX/LaTeX, please submit compiled PDFs." [AIP and formatting](https://www.nature.com/nm/submission-guidelines/aip-and-formatting) governs the accepted manuscript: "Please submit your manuscript in either Word or TeX/LaTeX format. We do not accept PDFs for final submissions." That second page is portfolio boilerplate served per journal: it is about 98% identical to the same page at Nature Human Behaviour and Nature Machine Intelligence once the journal name is substituted, so its rules bind all three.
- [Content types](https://www.nature.com/nm/content) · per journal, and the only place the limits differ from the siblings. An Article takes a main text of up to 4,000 words excluding abstract, Methods, references and figure legends, an abstract of up to 150 words and unreferenced, up to 6 display items (figures and/or tables), and around 60 references as a guideline. A Brief Communication takes up to 2,000 words INCLUDING abstract, references and figure legends, "contains no headings", takes up to 2 display items, and around 20 references.
- [Springer Nature LaTeX author support](https://www.springernature.com/gp/authors/campaigns/latex-author-support) · the published LaTeX package, and this journal sends authors to exactly this address, saying they may go there to "download the Springer Nature LaTeX template". A journal-specific class file does not exist; the instruction is "To submit a TeX/LaTeX file, please use any of the standard class files such as article.cls, revtex.cls or amsart.cls." The template itself is portfolio-wide and wider, usable "for any Springer Nature journal inclusive of Springer, Nature Portfolio, and BMC".
- Tiers, and both claims this board makes · the 10-item Extended Data cap is CONFIRMED at source, and the wording is tighter than the pack's: "A maximum of 10 Extended Data display figures is permitted." The unit is display FIGURES, not items, and the tier below it is subordinate to it, since "Supplementary Figures should be used only for cases when the use of Extended Data to report these findings is not appropriate." The no-standalone-Related-Work rule is CONFIRMED too, from an exhaustive list rather than a prohibition: "Article should be divided as follows: Introduction (without heading), Results, Discussion, Online Methods", followed by "Results and online Methods should be divided by topical subheadings; the Discussion does not contain subheadings." Four blocks are permitted, none of them is prior work, and the two that host it may carry no heading of their own.

## Law

Two of this desk's three rejections are properties of how the evidence was gathered, so the outlet is chosen at the task layer and merely confirmed at the venue stage.
A venue recommendation that ignores an unacquirable bar is not a recommendation, it is a deferral of the rejection.

## Glossary

- **Unacquirable bar**: a desk requirement that is a property of study design rather than of the manuscript, and therefore cannot be met by any revision.
- **Human path**: evidence that an animal or in-vitro result has a route to patients, one of this desk's three rejections when absent.

## Log

260802 · Opened with the QBv outlet pages, from `playbook-nature-portfolio/nature-medicine` at `Venue-Paper@fe25a88`.
260802 · Added divisions 3 to 9, one per section kind, from the seven `natmed-<kind>/style.md` and `template.md` pairs; folded in the retired family README and `../style-profile.md`; recorded at 5.1 that `related-work` is declared for all five Nature outlets and printed by none, at 7.2 that no external-validation norm is measured, and at 9.3 the Supplementary numbering contradiction.
260802 · Added an 🔗 Authority block to `## Files`, from the journal's own pages fetched and verified that day. It closes the pack's open LaTeX question: TeX/LaTeX is required or permitted at both stages, no journal class file exists, standard article.cls / revtex.cls / amsart.cls are the instruction, and the journal itself links the Springer Nature LaTeX template, whose URL is now recorded. It CONFIRMS both of this board's inherited claims at source: "A maximum of 10 Extended Data display figures is permitted", where the unit is display FIGURES rather than items, and a four-block Article division that contains no prior-work section and forbids subheadings in the Discussion.
260802 · Added a Format values and a language subsubsection to each of divisions 3 to 9: four rows each (words, citation density, value density, displays) carrying the natmed-<kind>/style.md heading and the measured base beside every number, plus 3 to 6 attributed one-sentence quotes per division taken only from what the pack already quotes; recorded that no style.md in this pack measures value density under that or any name, that every "Micro-norms (measured 2026-07-08)" table rests on brinton-2026 and bean-2026 alone while 24 papers sit on disk, that the Results display counts alone rest on nine named papers, that related-work has no budget and spends its hosts' instead, and that natmed-appendix/style.md quotes no prose at all.
