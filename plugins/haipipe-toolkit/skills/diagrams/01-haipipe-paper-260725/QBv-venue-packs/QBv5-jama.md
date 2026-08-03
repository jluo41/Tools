# JAMA: the desk whose test is what a clinician does on Monday

state: 🟡 PARTIAL · 19 exemplars · 7 sections · taste ✓ · its exemplar count is inflated by 3 misfiled JNO papers
owner: JL
method: state JAMA's own desk signals and one-sentence test, and record that this outlet's examples folder is also holding its sibling's

## Opening

JAMA's desk runs one test, and this page calls it the Monday test: will a practising clinician change what they do Monday morning because of this result?
> ✎ JAMA's ~test is~ *desk runs one test, and this page calls it* the ~shortest in the tree and the hardest to fake:~ *Monday test:* will a practising clinician change what they do Monday morning because of this result? ~Everything else~ *It is the shortest bar any venue on this board sets, and the hardest to fake. Every other thing* the desk asks for ~is downstream of that.~ *follows from that one question.* So which papers ~actually~ clear ~it?~ *it, and which ones does it throw out?* · CC · 260802 1540
It is the shortest bar any venue on this board sets, and the hardest to fake.
Every other thing the desk asks for follows from that one question.
So which papers clear it, and which ones does it throw out?

**Where this page sits**: it is one venue target in `QBv`, one page per desk with no pack layer above it.
This page owns only what is true of `playbook-jama-portfolio/jama-flagship/`.

**Why this outlet is the ceiling and rarely the target**: the bar is practice change at national scale, and the portfolio's own delta table says so.
For this repo's prescribing work, `QBv6` records the outlet the pack actually names.

**What is wrong with its folder**: `examples/` holds 23 files, three of which are JAMA Network Open papers filed here rather than under `jama-netopen/`.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**State a number only with its source**: a word budget or a paragraph count may appear in a section division, but the `jama-flagship/jama-<section>/style.md` line or the named exemplar it came from is given in the same breath, and this page never asserts a norm as its own.

✅ `~350w for the structured abstract (jama-abstract/style.md line 7)`  ❌ `the abstract runs about 350 words`

**State the bar as an action, not as a quality**: this desk's own test is behavioural and paraphrasing it as importance loses the test.

✅ `will a clinician change what they do Monday`  ❌ `is the finding important`

## Diagram

**One question, asked of the reader's next week**: and five ways to fail it.

```text
  🎯 THE TEST
     "Will a practicing clinician change what they do Monday
      morning because of this result?"

  ✅ WHAT CLEARS IT
     a question affecting millions, answered definitively
       ── RCT · large cohort · meta-analysis
     patient-centered outcomes ── mortality · morbidity ·
       quality of life · functional status
     public-health significance in the FIRST paragraph
     STROBE / CONSORT / PRISMA compliance, pre-registered
       where possible
     policy relevance ── guidelines · CMS decisions
     a clean Key Points box: Question / Findings / Meaning,
       one sentence each

  ❌ DESK-REJECT
     surrogate endpoints with no clinical outcome
     single-center with small N where large registries exist
     an incremental drug trial with no practice implication
     an AI/ML method paper with no patient-outcome impact
     overclaimed generalizability from a convenience sample

  📊 23 files in examples/ ── 3 of them are JNO papers ⚠️
```

## Content

### 1 · What the Monday test actually excludes

**Two of the five rejections are about endpoints, not scale**: a large study can fail this desk on what it measured.

```text
  🚫 surrogate endpoints alone
     ── the study can be enormous and still not answer the
        question the test asks

  🚫 an AI/ML method paper with no demonstrated impact on
     patient outcomes
     ── the nearest failure mode to this repo's work, and the
        same one npj Digital Medicine names at QBv8

  💡 so the binding constraint is the OUTCOME VARIABLE, which
     is fixed at the task layer and not at venue
```

🎯 Establishes the outcome variable as the gate, which places this outlet upstream of the venue stage like ISR and Nature Medicine.

#### 1.1 · The first paragraph carries a stated requirement
(which makes it one of the few section-level rules a desk names in its taste file)
The signals ask for public-health significance in the first paragraph, not somewhere in the Introduction.
That is a placement rule from the desk itself, and `jama-introduction/style.md` is where it has to be honoured.

### 2 · The three misfiled JNO papers

**A count that is wrong in two directions at once**: this folder is over by three and its sibling is empty.

```text
  📂 jama-flagship/examples/
     burns-2024-jamanetworkopen-opioid-variation
     jamanetworkopen-2026-antipsychotic-by-clinician-type
     jamanetworkopen-2026-peer-feedback-hospitalist-antibiotic

  ✅ jno-taste.md names all three and points here on purpose
  💥 but this outlet's style.md numbers were extracted from a
     folder containing another outlet's papers

  ⚠️ so the defect is not only filing: a JAMA word budget may
     rest partly on JNO prose
```

⚠️ Establishes the misfiling as a possible contamination of this outlet's own norms, not only a navigation problem.

### 3 · The structured abstract, and the Key Points box beside it

**Seven labeled fields and a three-line box**: the abstract is not paragraphs, and the box is a separate element the desk calls mandatory.

```text
  🧾 THE SEVEN FIELDS, FIXED ORDER
     IMPORTANCE                             1-2 sent · ~30w
     OBJECTIVE                              1 sent · ~20-30w
     DESIGN, SETTING, AND PARTICIPANTS      2-3 sent · ~50-60w
     EXPOSURES (obs) / INTERVENTIONS (RCT)  ~20-30w / ~40-60w
     MAIN OUTCOMES AND MEASURES             1-2 sent · ~40-60w
     RESULTS                                3-4 sent · ~100-120w
     CONCLUSIONS AND RELEVANCE              1-2 sent · ~30-40w
     ── field budgets: jama-abstract/style.md lines 32-39
     ── RCTs add a TRIAL REGISTRATION line, uncounted

  📦 KEY POINTS BOX ── three one-liners, beside the abstract
     Question  one interrogative sentence
     Findings  `In this <design> including <N> <population>,
                <key result with numbers>.`
     Meaning   `This study ...` / `Among <population>, ...`
     ── mandatory for Original Investigations across the
        flagship, JAMA IM and JAMA Network Open
        (style-profile.md line 23)

  📏 BUDGET, and the clash the pack annotates
     cap                ~350w all fields   style.md line 7
     Krebs 2018          400w raw          ⚠️ over
     Mathioudakis 2025   386w raw          ⚠️ over
     ── style.md line 104: the cap is a journal rule and JAMA's
        official count differs from a whitespace count, so 350
        is the DRAFTING target, not what a counter shows

  🔢 MEASURED SHAPE (style.md lines 96-105, 2026-07-08)
     sentences/field  1-5, median ~2 · RESULTS longest at 4
     words/sentence   ~20 Krebs · ~30 Mathioudakis
     citations        0 in both ── the abstract carries no
                      reference markers at all

  🚫 ANTI-PATTERNS (style.md lines 79-86)
     an unstructured paragraph · a missing Key Points box ·
     causal verbs on observational data · interpretation inside
     RESULTS · an estimate with no 95% CI · an OBJECTIVE that
     does not open `To <verb>`
```

🧾 Establishes the abstract as a fixed seven-slot form with a companion box, so a draft is checkable field by field before anyone judges its prose.

#### 3.1 · The box and the headings are the family's shared shape, and the delta table is what splits the outlets
(this is the knowledge that used to sit one level up, in the portfolio README)
`style-profile.md` line 23 makes the Key Points box mandatory across the flagship, JAMA Internal Medicine and JAMA Network Open, and line 36 gives all three the same seven headings.
What separates them is not the form but the bar.
> ✎ What separates them is not the form but the ~bar, recorded as the~ *bar. The* per-journal delta table at `playbook-jama-portfolio/README.md` lines ~110-121: this~ *110-121 records what each one rewards. This* outlet rewards broad practice-changing findings, JAMA IM rewards prescribing and overuse work, and JAMA Network Open rewards soundness over novelty. · CC · 260802 1540
The per-journal delta table at `playbook-jama-portfolio/README.md` lines 110-121 records what each one rewards.
This outlet rewards broad practice-changing findings, JAMA IM rewards prescribing and overuse work, and JAMA Network Open rewards soundness over novelty.
So a retarget inside this family keeps the abstract's shape and changes what IMPORTANCE has to argue.

#### 3.2 · The family style file is not grounded in this outlet
(which matters the moment a writer reaches for the shared profile instead of the flagship's own)
`style-profile.md` lines 3-10 say its templates come from JAMA Network Open papers plus one JAMA IM paper.
> ✎ `style-profile.md` lines 3-10 say its templates come from JAMA Network Open papers plus one JAMA IM ~paper, while the~ *paper. The* flagship per-section guides come from flagship Original ~Investigations:~ *Investigations instead:* Krebs 2018, Mathioudakis 2025, Cipriani 2026, Rotenstein 2026. · CC · 260802 1540
The flagship per-section guides come from flagship Original Investigations instead: Krebs 2018, Mathioudakis 2025, Cipriani 2026, Rotenstein 2026.
The same file leaves the per-outlet abstract cap open at line 88, an unticked box asking for the exact limit from author instructions.
For this desk the flagship `jama-<section>/style.md` files are the grounded source and the profile is the siblings' voice.

#### 3.3 · Format values
(every row names the `jama-abstract/style.md` line it came from, and stops where the pack stops)

```text
  📏 WORDS            ~350w cap · 7 labeled fields · 1-5 sent/field, median ~2 · ~20-30 w/sent   [jama-abstract/style.md lines 7, 98-100]
  📚 CITATION DENSITY 0 per sentence, in both measured exemplars   [jama-abstract/style.md line 101]
  🔢 VALUE DENSITY    at least 1 estimate with a 95% CI and/or P per RESULTS sentence, and 0 in every other field except MAIN OUTCOMES   [jama-abstract/style.md line 105, under "Micro-norms (measured 2026-07-08)"]
  📊 DISPLAYS         not recorded by the pack   [checked jama-abstract/style.md, which names the Key Points box and no figure or table]
```

#### 3.4 · The language, in the papers' own words
(one quotation per move, taken from the Signature moves and Key Points blocks of `jama-abstract/style.md`)

"Limited evidence is available regarding long-term outcomes of opioids compared with nonopioid medications for chronic pain." [Krebs 2018]
The IMPORTANCE opener, closing on the gap rather than on the problem, and filling the first of the seven fields listed above.

"To evaluate the efficacy of a web-based tool to personalize antidepressant treatment." [Cipriani 2026]
The OBJECTIVE field, one sentence opening `To <verb>`, which the anti-pattern list above turns into a hard shape requirement.

"How is adoption of artificial intelligence (AI) scribes associated with changes in electronic health record (EHR) time expenditure and weekly visit volume?" [Rotenstein 2026]
The Key Points Question line, the one question that sits beside the abstract in the box this part of the page records as mandatory.
> ✎ The Key Points Question line, the ~interrogative~ *one question* that sits beside the abstract in the box this ~division~ *part of the page* records as mandatory. · CC · 260802 1540

"mean 12-month BPI interference was 3.4 for the opioid group and 3.3 for the nonopioid group (difference, 0.1 [95% CI, -0.5 to 0.7])." [Krebs 2018]
The RESULTS field carrying its full statistical package, which is where the value density above is concentrated.

"AI scribe adoption was associated with modest decreases in total EHR time and documentation time and with a modest increase in weekly visit volume." [Rotenstein 2026]
The CONCLUSIONS AND RELEVANCE sentence in associational voice, the field the anti-pattern list forbids writing causally.

### 4 · The introduction that is over in three paragraphs

**Problem forward and method light**: it names the clinical problem, names what is missing, announces the study, and stops.

```text
  🚪 THE ARC ── 4 beats, flat, no subsections
     P1 clinical problem + burden, with a concrete number
     P2 current approaches + their limitations
     P3 GAP, built on however / but / although / yet (optional)
     P4 this study: design + objective, past tense
     ── jama-introduction/style.md lines 12-18 and 70-79

  📏 BUDGET 150-800w · 3-5 ¶   style.md line 7
     Krebs 2018         146w · 3 ¶   measured
     Mathioudakis 2025  299w · 4 ¶   measured
     Cipriani 2026     ~650w · 4 ¶   estimate, not re-measured
     Rotenstein 2026   ~450w · 3 ¶   estimate, not re-measured
     ── style.md lines 8 and 92

  ✍️ FIRST SENTENCE, as a slot
     `<Condition> affects approximately <N>% of <population>
      and <consequence>.`
     `<Activity> in the <system> requires substantial
      <resource>, averaging <quantity>.`
     🚫 never a literature citation as the subject

  ✍️ GAP AND CLOSE, as slots
     gap    `Although previous trials have assessed <X>, none
             <the specific missing condition>.`
     close  `This <design> was conducted to <evaluate|compare|
             determine> <intervention> <vs comparator> <on
             outcomes> <in population>.`

  🔢 CITATION DENSITY ~0.5-0.8 per sentence, CLUSTERED
     heavy in the burden and gap paragraphs
     ── and the study-announcement paragraph cites NOTHING
     ── style.md line 90

  🚫 ANTI-PATTERNS (style.md lines 61-68)
     a findings preview · a contribution list · a roadmap
     sentence · more than five paragraphs
```

🚪 Establishes the shortest introduction in this tree, and the moves an IS-trained writer would add here that this desk rejects.

#### 4.1 · Three beats travel from an IS introduction and all three fail here
(so a retarget from `QBv1` or `QBv2` is a deletion job before it is a writing job)
The anti-patterns name the findings preview, the contribution list and the roadmap sentence.
> ✎ The anti-patterns name the findings preview, the contribution list and the roadmap ~sentence, and all~ *sentence. All* three are required beats at the IS desks this board carries. · CC · 260802 1540
All three are required beats at the IS desks this board carries.
`jama-introduction/style.md` line 42 states the consequence the desk wants instead: the reader moves directly from "this study did X" into Methods.

#### 4.2 · Format values
(the citation row is the only density this section's file measures, and the two empty rows say so rather than borrowing one)

```text
  📏 WORDS            150-800w · 3-5 ¶ · 1-4 sent/¶, median ~3 · median ~21 w/sent   [jama-introduction/style.md lines 7, 87-89]
  📚 CITATION DENSITY ~0.5-0.8 per sentence, clustered in the burden and gap ¶, and the study-announcement ¶ is uncited   [jama-introduction/style.md line 90]
  🔢 VALUE DENSITY    not recorded by the pack   [checked jama-introduction/style.md Micro-norms lines 85-90, which count citations and words but no estimates]
  📊 DISPLAYS         not recorded by the pack   [checked jama-introduction/style.md]
```

#### 4.3 · The language, in the papers' own words
(one quotation per beat of the four-beat arc printed above, from Signature moves and Exemplar sentences)

"Prediabetes affects approximately 38% of US adults and has a growing global prevalence." [Mathioudakis 2025]
The P1 burden opener, and the live instance of the `<Condition> affects approximately <N>% of <population>` slot printed above.

"Human scribes can reduce EHR time, but their scalability is constrained by cost and workforce availability." [Rotenstein 2026]
The P2 beat, naming the current approach and its limitation in a single sentence rather than in a literature review.

"However, there is no consensus on which pretreatment characteristics can accurately predict efficacy and acceptability of specific antidepressants." [Cipriani 2026]
The P3 gap built on `however`, one of the four contrastive conjunctions the desk's gap move accepts.

"Although previous randomized trials have assessed digital adaptations of the DPP, none had experimental groups that were fully automated and AI-based" [Mathioudakis 2025]
The same gap beat in its `Although ... none ...` shape, which is the gap slot printed above.

"In this randomized clinical trial, we compared the PETRUSHKA tool with usual care." [Cipriani 2026]
The P4 close, one past-tense sentence announcing the study, and the shortest instance of the close slot printed above.

### 5 · Methods: the longest section, and it always ends the same way

**Two invariants and a very long middle**: the opening paragraph names design, ethics and reporting standard, and Statistical Analysis is always last.

```text
  🔬 THE ARC (jama-methods/style.md lines 12-20)
     design + ethics + reporting standard
       -> setting + population + eligibility
       -> randomization + blinding      (RCT)
       -> interventions, arm by arm     (RCT)
       -> outcomes defined precisely
       -> Statistical Analysis          ALWAYS LAST, ALWAYS ALONE

  📏 BUDGET 1,500-3,000w RCT · 800-1,500w observational
     style.md line 7
     Krebs 2018        ~1,700w · 10+ subsections   measured
     Mathioudakis      ~1,600w ·  8 subsections    measured
     Cipriani          ~2,000w ·  6 subsections    estimate
     Rotenstein        ~1,500w ·  7 subsections    estimate
     ── style.md lines 8 and 126

  📐 REPORTING STANDARD, named in the FIRST paragraph
     CONSORT  trials
     STROBE   observational
     PRISMA   named by taste.md as a fit signal, covered by no
              section file in this pack ⚠️

  ✍️ SLOTS
     `The <institution> institutional review board approved the
      protocol and <participants> provided written informed
      consent.`
     `This report followed the <CONSORT|STROBE> reporting
      guideline.`
     `Eligible <participants> had <condition> defined as
      <clinical threshold>.`
     `The primary outcome was <outcome>, assessed with the
      <instrument> (<abbrev>; range, <X>-<Y>; higher scores =
      <direction>).`
     `<K> post hoc sensitivity analyses were conducted:
      (1) ... (2) ...`

  🔢 MEASURED SHAPE (style.md lines 119-128)
     paragraphs      20-21 over 10-13 titled subsections
     sentences/¶     median 3-4
     words/sentence  median 16-22 · instrument and list
                     sentences run 80-160
     citations       ~0.2-0.3/sentence · half of Krebs' markers
                     sit in the two outcome-definition ¶

  🚫 ANTI-PATTERNS (style.md lines 92-99)
     no reporting standard · results described here · Statistical
     Analysis merged into another subsection · a skipped power
     calculation · a vague outcome with no instrument, range,
     direction or MCID · intervention detail left only in a
     Supplement
```

🔬 Establishes Methods as the paper's bulk, with the reporting standard as a first-paragraph obligation rather than a submission checkbox.

#### 5.1 · The observational layout is a different subsection set, not a shortened one
(and it is the layout this repo's prescribing work would actually file)
`jama-methods/style.md` lines 41-48 record Rotenstein 2026's set: Study Setting and Population, Variables, Main Analytic Approach, Subgroup Analyses, Sensitivity Analyses, then a domain-specific one.
Randomization, Interventions and Sample Size drop out, and a sentence naming the analytic framework replaces the power calculation.
> ✎ Randomization, Interventions and Sample Size drop out, and ~an analytic-framework~ *a* sentence *naming the analytic framework* replaces the power calculation. · CC · 260802 1540
The two invariants survive the swap: the opening paragraph still names design, ethics and STROBE, and Statistical Analysis is still last.

#### 5.2 · Format values
(the longest section in the paper, and the pack measures only two of these four things about it)

```text
  📏 WORDS            1,500-3,000w RCT · 800-1,500w observational · 20-21 ¶ over 10-13 subsections · 1-10 sent/¶, median 3-4 · median 16-22 w/sent   [jama-methods/style.md lines 7, 121-123]
  📚 CITATION DENSITY ~0.2-0.3 per sentence · 14 to 24 markers · many ¶ uncited, and half of Krebs' sit in the two outcome-definition ¶   [jama-methods/style.md lines 124, 128]
  🔢 VALUE DENSITY    not recorded by the pack   [checked jama-methods/style.md Micro-norms lines 119-128]
  📊 DISPLAYS         not recorded by the pack   [checked jama-methods/style.md, whose line 8 excludes table, box and figure text from its word count without counting them]
```

#### 5.3 · The language, in the papers' own words
(one quotation per Signature move, walking the arc printed above from the opening paragraph to the last subsection)

"This report followed the Consolidated Standards of Reporting of Trials (CONSORT) reporting guideline." [Cipriani 2026]
The reporting-standard sentence of the opening paragraph, which is the slot printed above and the first of this section's two invariants.

"Chronic pain was defined as pain nearly every day for 6 months or more." [Krebs 2018]
The clinical-threshold half of the eligibility slot, where a population is defined by a measurable rule rather than by a label.

"Both BPI scales yield 0 to 10 scores (higher score = worse function or intensity)." [Krebs 2018]
The range-and-direction half of the outcome slot printed above, which the anti-pattern list makes mandatory alongside the instrument name.

"A sample of 276 participants (138 per group) was calculated to provide 80% power at a 1-sided significance level of .05." [Mathioudakis 2025]
The power calculation that opens Statistical Analysis in an RCT, the section's second invariant and always its last subsection.

"The primary analytic approach was a difference-in-differences framework using multivariable ordinary least-squares models." [Rotenstein 2026]
The observational replacement for that power calculation, and the sentence that carries the layout swap recorded at `5.1`.

### 6 · Results: prose that carries numbers and nothing else

**Zero citations, full statistical packages, a display named in every claim**: the section's bulk lives in its tables and figures.

```text
  📊 THE ARC (jama-results/style.md lines 12-20)
     participant flow, referencing the flow Figure
       -> baseline characteristics, referencing Table 1
       -> primary outcome with the full statistical package
       -> secondary outcomes, nulls stated plainly
       -> adverse events
       -> subgroup and sensitivity

  📏 BUDGET 700-1,800w of PROSE   style.md line 7
     Krebs 2018        ~800w   measured
     Mathioudakis      ~725w   measured
     Cipriani        ~1,400w   estimate
     Rotenstein      ~1,800w   estimate
     ── style.md lines 8 and 113

  ✍️ SLOTS
     flow      `Of <N> enrolled <patients>, <n> were excluded
                and <N'> were <randomized|included> (Figure <X>).`
     baseline  `Mean age was <X> years (SD, <Y>) and <N> (<%>)
                were <sex> (Table 1).`
     binary    `<N> of <N'> (<%>) in the <group> <achieved
                outcome> compared with <n> of <n'> (<%>)
                (adjusted <RR|OR>, <X> [95% CI, <L>-<U>];
                P = <value>).`
     null      `<outcome> did not significantly differ between
                the 2 groups (overall P = <value>).`

  🔢 MEASURED SHAPE (style.md lines 106-115)
     paragraphs      8-10 over 4-6 titled subsections
     sentences/¶     median 2-3
     words/sentence  median 23-26 · primary-outcome sentences
                     run 30-60+
     citations       0 in both ── Results prose cites nothing

  ⚖️ TWO ACCEPTABLE ESTIMATE DENSITIES (style.md line 114)
     Krebs         10 "95% CI" and 12 P values in 29 sentences
     Mathioudakis  1 CI and 3 P values in prose, the rest pushed
                   to Figure 2 and the eTables

  🚫 ANTI-PATTERNS (style.md lines 81-89)
     interpretation here · an outcome with no CI and no P · a
     missing participant flow · a display discussed but not
     named · causal verbs · a subgroup result with no interaction
     test · a favorable and an unfavorable result in one sentence
```

📊 Establishes Results as a purely factual register with two legitimate densities, so a lean Results is not automatically an underreported one.

#### 6.1 · The display set is fixed before the prose is written
(so a missing display is a build request and never a sentence)
`playbook-jama-portfolio/README.md` lines 62-70 name the family's standard set of displays.
> ✎ `playbook-jama-portfolio/README.md` lines 62-70 name the family's standard ~set: a mandatory~ *set of displays. Two of them are mandatory:* Table 1, *and* a ~mandatory~ STROBE cohort flow ~diagram, the~ *diagram. The* primary-association display ~as~ *is* the ~hero~ *hero,* tied to the one primary ~claim, a~ *claim. A* subgroup forest plot ~for~ *carries* the vulnerable-population ~amplification, and a~ *amplification. A* dose-response figure *is added* when relevant. · CC · 260802 1540
Two of them are mandatory: Table 1, and a STROBE cohort flow diagram.
The primary-association display is the hero, tied to the one primary claim.
A subgroup forest plot carries the vulnerable-population amplification.
A dose-response figure is added when relevant.
`jama-results/style.md` move 5 requires each of them to be named inline, right where its data are discussed.
> ✎ `jama-results/style.md` move 5 requires each of them to be named ~inline~ *inline, right* where its data are ~discussed, as~ *discussed. The forms it accepts are* `(Table 2)`, `(Figure 1)` ~or~ *and* `(Figure 3 and eTable 14 in Supplement ~2)`, and line~ *2)`. Line* 86 *of the same file* makes ~the~ *an* unnamed display a defect on its own. · CC · 260802 1540
The forms it accepts are `(Table 2)`, `(Figure 1)` and `(Figure 3 and eTable 14 in Supplement 2)`.
Line 86 of the same file makes an unnamed display a defect on its own.

#### 6.2 · Format values
(the only section in this pack whose file measures all four, because the estimate density it records is the value density under another name)

```text
  📏 WORDS            700-1,800w of prose · 8-10 ¶ over 4-6 subsections · 1-7 sent/¶, median 2-3 · median 23-26 w/sent, primary-outcome sentences 30-60+   [jama-results/style.md lines 7, 108-110]
  📚 CITATION DENSITY 0 per sentence in both papers, the only superscripts being table and figure footnote letters   [jama-results/style.md line 111]
  🔢 VALUE DENSITY    Krebs 10 "95% CI" instances and 12 P values in 29 prose sentences · Mathioudakis 1 CI and 3 P values, the rest pushed to Figure 2 and the eTables · either is acceptable   [jama-results/style.md line 114 "Estimate density", under "Micro-norms (measured 2026-07-08)"]
  📊 DISPLAYS         Table 1 · STROBE cohort flow diagram · primary-association hero · subgroup forest plot · dose-response figure when relevant   [playbook-jama-portfolio/README.md lines 62-70]
```

#### 6.3 · The language, in the papers' own words
(one quotation per Signature move, in the order the arc printed above runs them)

"Of 265 enrolled patients, 25 withdrew prior to randomization and 240 were randomized (Figure)." [Krebs 2018]
The participant-flow opener, and the flow slot printed above with its display named inline exactly as move 5 requires.

"Mean age was 58.3 years (range, 21-80) and 32 patients (13.0%) were women (Table 1)." [Krebs 2018]
The baseline slot: one sentence of demographics, ending on the Table 1 reference that `6.1` lists as mandatory.
> ✎ The baseline ~slot,~ *slot:* one sentence of ~demographics~ *demographics,* ending on the Table 1 reference that `6.1` ~makes a mandatory unit.~ *lists as mandatory.* · CC · 260802 1540

"AI scribe adoption was associated with 13.4 (95% CI, 9.1-17.7) fewer minutes of EHR time" [Rotenstein 2026]
The primary-outcome clause carrying its estimate and CI together, which is the sentence the estimate density above is counting.

"The risk difference was -0.2% (1-sided 95% CI: -8.2%; Figure 2), demonstrating that the AI-led DPP intervention met the noninferiority margin of -15.0%." [Mathioudakis 2025]
The same move in its noninferiority shape, and the leaner of the two densities, since this paper sends the rest of its numbers to a display.

"Electronic health record time outside work hours did not change significantly." [Rotenstein 2026]
The plain null statement, stated as flatly as a positive finding, which is the null slot printed above.

### 7 · Discussion: short, hedged, and closing on two fixed subsections

**Limitations and Conclusions are titled subsections, never loose paragraphs**: everything before them is interpretation this desk expects to be cautious.

```text
  🧭 THE ARC (jama-discussion/style.md lines 12-20)
     restate the key finding with design + population
       -> comparison to prior work, 2-3 ¶
       -> mechanism and clinical interpretation, hedged
       -> strengths, 0-1 ¶
       -> Limitations   dedicated titled subsection
       -> Conclusions   dedicated titled subsection

  📏 BUDGET 600-1,500w   style.md line 7
     Krebs 2018       ~640w ·  8 ¶   measured, and the floor
     Mathioudakis   ~1,130w · 11 ¶   measured
     Cipriani       ~1,500w          estimate
     Rotenstein     ~1,200w          estimate
     ── style.md lines 8 and 111

  ✍️ SLOTS
     open   `Among <population>, <intervention> compared with
             <comparator> did not result in significantly better
             <outcome> over <time>.`
     prior  `These <multisite> findings extend evidence from
             <prior work type>.`
     hedge  `<exposure> was associated with <outcome>, but the
             clinical importance of this finding is unclear; the
             magnitude was <small|modest>.`
     limits `This study has several limitations. First, <threat +
             direction of bias>. Second, <threat>.`
     close  `<finding restated>. Future studies should assess
             <next questions>.`

  🔢 MEASURED SHAPE (style.md lines 104-113)
     paragraphs      8-11 total · 5-9 body ¶ before Limitations
     Limitations     the longest single ¶, 9-10 sentences, one
                     per enumerated limitation
     words/sentence  median 20-23
     citations       ~0.2-0.3/sentence, concentrated in the
                     prior-work ¶ ── the opening restatement,
                     Limitations and Conclusions are UNCITED

  🚫 ANTI-PATTERNS (style.md lines 76-85)
     no Limitations subsection · no Conclusions subsection · new
     data introduced here · a Discussion longer than Methods plus
     Results · a skipped prior-work comparison · a long standalone
     Strengths subsection · a Conclusions ending on a method
```

🧭 Establishes the Discussion as the section with the most fixed furniture, where the enumerated Limitations paragraph is a form and not a courtesy.

#### 7.1 · The hedge is a family rule, and this repo's work has a named framing inside it
(which is the sentence-level face of the observational language bar)
`style-profile.md` lines 72-79 set the tone as measured, patient centered and policy aware, and forbid causal verbs on observational data.
> ✎ `style-profile.md` lines 72-79 set the tone as measured, patient centered and policy aware, *and* forbid causal verbs on observational ~data, and~ *data. The same lines* give this repo's prescribing work its framing: agreeable approximates saying yes, clinical firmness can protect, and the mechanism is presented as a trade-off rather than a fault. · CC · 260802 1540
The same lines give this repo's prescribing work its framing: agreeable approximates saying yes, clinical firmness can protect, and the mechanism is presented as a trade-off rather than a fault.
`jama-discussion/style.md` move 3 supplies the hedging vocabulary the desk reads as appropriate: may, could, it is possible that, suggesting.

#### 7.2 · Format values
(the section that argues about numbers without restating many, and the pack counts citations here rather than estimates)

```text
  📏 WORDS            600-1,500w · 8-11 ¶ total, 5-9 body ¶ before Limitations · 1-10 sent/¶, median ~4 · median 20-23 w/sent   [jama-discussion/style.md lines 7, 98, 106-108]
  📚 CITATION DENSITY ~0.2-0.3 per sentence, concentrated in the prior-work ¶, with the opening restatement, Limitations and Conclusions uncited in both   [jama-discussion/style.md line 109]
  🔢 VALUE DENSITY    not recorded by the pack   [checked jama-discussion/style.md Micro-norms lines 104-113]
  📊 DISPLAYS         not recorded by the pack   [checked jama-discussion/style.md, and its anti-pattern list forbids new data here]
```

#### 7.3 · The language, in the papers' own words
(one quotation per Signature move, ending on the two titled subsections this section always closes with)

"This study in 5 academic medical centers found that adoption of AI scribes was associated with modest reductions in total EHR time" [Rotenstein 2026]
The opening restatement, which names the design and the setting before it names the finding, and is the open slot printed above.

"These multisite findings extend evidence from a growing body of single-site studies regarding the EHR time benefits of AI scribes" [Rotenstein 2026]
The prior-work comparison, the beat the anti-pattern list refuses to let a draft skip, and the only place citations cluster.

"but the clinical importance of this finding is unclear; the magnitude was small" [Krebs 2018]
The hedge clause, which concedes the size of an effect the same sentence has just reported, matching the hedge slot printed above.

"First, the complexity of interventions precluded masking of patients." [Krebs 2018]
One enumerated limitation naming its threat, from the dedicated Limitations subsection that opens on `This study has several limitations.`

"Results do not support initiation of opioid therapy for moderate to severe chronic back pain" [Krebs 2018]
The Conclusions clause, ending on a clinical implication rather than on a method, which is the close slot printed above.

### 8 · Supplements: numbered by the journal, e-prefixed by the author

**This desk has no appendix**: it has numbered Supplements, and the body addresses them with both numbers at once.

```text
  📎 THE FOUR ROLES (jama-appendix/style.md lines 18-28)
     Supplement 1  trial protocol + statistical analysis plan
                   REQUIRED for RCTs · often 30-80 pp
     Supplement 2  every eTable, eFigure, eMethods · 15-30 pp
     Supplement 3  study group / investigator list, if any
     Supplement 4  data sharing statement
     ── non-RCT papers use fewer; Supplement 1 still holds the
        protocol and SAP whenever one exists

  🔤 THE "e" PREFIX, a SEPARATE numbering stream
     main text     Table 1 · Figure 1        plain labels
     supplement    eTable 1 · eFigure 1 · eMethods
     ── sequential within type, no gaps, and the two streams
        never overlap   style.md lines 30-41
     ── eMethods is singular unless there are several distinct
        sections

  🔗 HOW THE BODY CITES INTO ONE
     `eTable 2 in Supplement 2`
     `eFigure 3, eTables 16-19 in Supplement 2`
     `available in Supplement 1`   protocol and SAP, no eItem
     `appears in Supplement 3`     study group list
     🚫 never a bare `eTable 2`
     🚫 never `in the Supplement`
     ── style.md lines 43-63; line 123 records that every
        observed reference in both exemplars used the full form

  ⚖️ THE TRIAGE RULE (style.md line 84)
     MAIN TEXT   anything answering the primary or secondary
                 hypothesis: Table 1, the flow Figure, the
                 primary-result Figure, core secondary tables,
                 key sensitivity results stated in prose
     SUPPLEMENT  robustness checks · subgroup breakdowns ·
                 intervention implementation detail ·
                 protocol-level measurement descriptions ·
                 extra baseline stratifications

  📊 OBSERVED INVENTORY (style.md lines 115-122)
     Krebs 2018         Supplements 1-2 · up to eTable 10
     Mathioudakis 2025  Supplements 1-4 · up to eTable 20 ·
                        eFigures 1-4 · eMethods
     ⚠️ lower bounds: the Supplement PDFs are not stored, so the
        counts come from the main text's cross-references
```

📎 Establishes the Supplement as an addressed destination rather than an overflow bin, so the triage decision happens before drafting and not after a length check.
> ✎ 📎 Establishes the Supplement as an addressed destination rather than an overflow bin, ~which is why~ *so* the triage decision happens before drafting ~rather than~ *and not* after a length check. · CC · 260802 1540

#### 8.1 · Authors label the items, the journal numbers the Supplements
(so the manifest is authorable but half of every address is not final until production)
`jama-appendix/style.md` lines 92-97 record that each Supplement is a separate uploaded PDF, never appended to the manuscript, and that JAMA assigns the Supplement numbers during production.
The author controls `eTable 1` and `eFigure 1`; the `in Supplement M` half of every cross-reference is only confirmed once the editorial office says so.

#### 8.2 · Format values
(the one section whose file states outright that prose metrics do not apply to it, which is why three rows here are counts of items and pages)

```text
  📏 WORDS            no word or ¶ budget: "Prose metrics are N/A for supplements" · Supplement 2 runs 15-30 pp · Supplement 1 often 30-80 pp   [jama-appendix/style.md lines 89-90, 113]
  📚 CITATION DENSITY not recorded by the pack   [jama-appendix/style.md line 113, which declares prose metrics N/A for supplements]
  🔢 VALUE DENSITY    not recorded by the pack   [jama-appendix/style.md line 113, the same declaration]
  📊 DISPLAYS         up to eTable 10 (Krebs) · up to eTable 20 plus eFigures 1-4 and eMethods (Mathioudakis) · both lower bounds, counted from main-text cross-references because the Supplement PDFs are not stored   [jama-appendix/style.md lines 113, 117-122]
```

#### 8.3 · The language, in the papers' own words
(and this is the one section whose file has no Signature moves block, so it quotes no sentences of its own)

`jama-appendix/style.md` carries no attributed sentence.
> ✎ `jama-appendix/style.md` carries no attributed ~sentence: it~ *sentence. It* has neither a Signature moves *heading* nor an Exemplar sentences ~heading,~ *one,* and what it quotes from the two papers are cross-reference fragments. · CC · 260802 1540
It has neither a Signature moves heading nor an Exemplar sentences one, and what it quotes from the two papers are cross-reference fragments.
Those fragments are still the papers' own strings, so they are given here as fragments, and nothing is added to make them read as prose.

"eFigure 3, eTables 16-19 in Supplement 2" [Mathioudakis 2025]
The full `eItem N in Supplement M` address in its longest observed form, and the shape the block above forbids shortening to a bare eItem.

"available in Supplement 1" [Mathioudakis 2025]
The protocol and SAP reference, which carries no eItem at all because the whole Supplement is the thing being addressed.

"appears in Supplement 3" [Mathioudakis 2025]
The study-group listing reference, the third of the four Supplement roles printed above and the one a non-RCT usually drops.

"The trial protocol and statistical analysis plan are in Supplement 1." [Krebs 2018]
The one complete sentence the pack quotes about a Supplement, and it sits in `jama-methods/style.md` move 1 rather than in this section's own file.

### 9 · The Research Letter: a whole paper under 600 words

**A compressed article with no abstract and no Key Points box**: three inline pipe labels stand in for the entire section apparatus.

```text
  ✉️ THE HARD CAPS (jama-letter/style.md lines 7-14)
     words       <=600, body text only, draft to 500-600
     references  <=6
     displays    1 Figure OR 1 Table, some letters carry both
     no abstract · no Key Points box

  📏 MEASURED, and both exemplars are over
     Yang 2026    ~666w body · 8 ¶
     Cantor 2025  ~640w body · 9 ¶
     ── style.md lines 10 and 118 log this as an annotated
        over-cap observation, NOT license to exceed 600

  🏷 INLINE PIPE LABELS, never headings (style.md lines 16-27)
     [unlabeled opening]  problem + gap + objective
     `Methods |`     data source, population, measures,
                     analysis, STROBE, software
     `Results |`     findings with 95% CI and P
     `Discussion |`  the finding, then limitations + implication

  ✍️ SLOTS
     open     `For decades, <guidelines> have <discouraged>
               <practice> because <clinical rationale>.`
     object   `This study examined <patterns> of <exposure>
               among <population> from <year> to <year>.`
     methods  `Methods | We used the <dataset> linked to
               <claims> from <date range>.`
     result   `In adjusted analyses, <X>% (95% CI, <L>%-<U>%)
               of <population> in <year> <had outcome>,
               declining to <Y>% (95% CI, <L>%-<U>%) in <year>,
               a <Z>-percentage point decrease (P = <value>).`
     close    `Study limitations include <brief list>.
               <implication for policy or practice>.`

  🔢 MEASURED SHAPE (style.md lines 110-119)
     Yang    2 opening ¶ · 3 Methods · 1 Results · 2 Discussion
     Cantor  1 opening ¶ · 4 Methods · 2 Results · 2 Discussion
     citations  exactly 6 in each, the cap, FRONT-LOADED ──
                Results and Discussion are nearly uncited
     density    Yang's single Results ¶ carries 19 "95% CI"

  🚫 ANTI-PATTERNS (style.md lines 83-93)
     an abstract or Key Points box · formal headings instead of
     pipe labels · more than 6 references · more than one Figure
     and one Table · a Discussion past 2 ¶ · a skipped STROBE ·
     a detailed statistical description · separate Limitations
     or Conclusions subsections · a findings preview up top
```

✉️ Establishes the letter as a full compressed study rather than a short paper, so its caps bind the study design and not only the prose.
> ✎ ✉️ Establishes the letter as a full compressed study rather than a short paper, ~which is why~ *so* its caps bind the study design and not only the prose. · CC · 260802 1540

#### 9.1 · This outlet has the letter kind, and the pack wrongly denies it to JAMA Network Open
(so a retarget between two siblings in one family can force a format rewrite)
`stages/section-kinds.yml` lines 80-82 give the `letter` kind to `jama-flagship` and to `jama-im`.
> ✎ `stages/section-kinds.yml` lines 80-82 give *the* `letter` *kind* to `jama-flagship` and to ~`jama-im`, and withhold it~ *`jama-im`. It withholds that kind* from `jama-netopen`. That withholding is wrong: verified 260802, JAMA Network Open publishes Research Letters at 800 words, 10 references and up to 2 small tables or ~figures, so~ *figures. So* the omission is a gap in the pack rather than a property of that desk. · CC · 260802 1540
It withholds that kind from `jama-netopen`.
That withholding is wrong: verified 260802, JAMA Network Open publishes Research Letters at 800 words, 10 references and up to 2 small tables or figures.
So the omission is a gap in the pack rather than a property of that desk.
A letter moving to the open-access sibling has to become an Original Investigation.
> ✎ A letter moving to the open-access sibling has to become an Original ~Investigation, which~ *Investigation. That* means acquiring a structured abstract and a Key Points box, ~both of which~ *and* the letter format forbids *both* at `jama-letter/style.md` lines 13-14. · CC · 260802 1540
That means acquiring a structured abstract and a Key Points box, and the letter format forbids both at `jama-letter/style.md` lines 13-14.
That is a rewrite decided at venue, not a reformat done at revise.

#### 9.2 · The letter pack contradicts itself on how many Discussion paragraphs there are
(and the measured note at the bottom of the file is the one to follow)
`jama-letter/style.md` line 92 still forbids separate Limitations and Conclusions subsections, on the grounds that both belong inside "the single Discussion paragraph".
> ✎ `jama-letter/style.md` line 92 still forbids separate Limitations and Conclusions ~subsections~ *subsections,* on the grounds that both ~fold into~ *belong inside* "the single Discussion ~paragraph", while line~ *paragraph". Line* 89 and the 2026-07-08 reconciliation at line 117 ~record~ *say otherwise:* both stored letters ~using~ *use* TWO Discussion ~paragraphs, and~ *paragraphs.* `jama-letter/template.md` splits them into P5 and P6. · CC · 260802 1540
Line 89 and the 2026-07-08 reconciliation at line 117 say otherwise: both stored letters use TWO Discussion paragraphs.
`jama-letter/template.md` splits them into P5 and P6.
Take the measured two-paragraph split.
> ✎ Take the measured two-paragraph ~split; the surviving singular~ *split. The word "single" at line 92* is stale wording *left* inside one anti-pattern line. · CC · 260802 1540
The word "single" at line 92 is stale wording left inside one anti-pattern line.

#### 9.3 · Format values
(the second place in this pack where an estimate density is on record, and it is the densest single paragraph anywhere in the tree)

```text
  📏 WORDS            <=600w hard cap, draft to 500-600 · 8-9 ¶ · 1-9 sent/¶, median ~3 · median 21-23 w/sent, Results sentences 30-50   [jama-letter/style.md lines 9, 104, 112-114]
  📚 CITATION DENSITY ~0.2 per sentence · exactly 6 references in each letter, the cap · front-loaded, and Results and Discussion are nearly uncited   [jama-letter/style.md line 115]
  🔢 VALUE DENSITY    Yang's single Results ¶ carries 19 "95% CI" instances · Cantor's two Results ¶ carry 5 · every quantitative claim gets its CI inline   [jama-letter/style.md line 119 "Estimate density", under "Micro-norms (measured 2026-07-08)"]
  📊 DISPLAYS         1 Figure OR 1 Table, some letters carrying both · Yang a 3-panel Figure · Cantor 2 Tables   [jama-letter/style.md lines 12, 63]
```

#### 9.4 · The language, in the papers' own words
(one quotation per block of the pipe-labelled structure printed above, from the two stored letters)

"For decades, clinical guidelines have discouraged use of high-risk central nervous system (CNS)-active medications" [Yang 2026]
The cold open, stating the clinical problem in its first clause with no preamble, which is the open slot printed above.

"We characterized trends in physician participation in the Medicare program between 2013 and 2023" [Cantor 2025]
The objective sentence that closes the unlabeled opening, and the letter's whole substitute for an Introduction.

"Methods | We used the Health and Retirement Study (HRS) linked to Medicare fee-for-service claims from January 1, 2013, to December 31, 2021." [Yang 2026]
The Methods pipe label doing the work of a heading, followed immediately by the data source, which is the methods slot printed above.

"In adjusted analyses, 19.9% (95% CI, 18.1%-21.6%) of beneficiaries in 2013 received 1 or more potentially inappropriate CNS-active prescriptions" [Yang 2026]
The trend sentence with its CI inline, one instance of the 19 that make this paragraph the densest in the pack.

"Study limitations include unavailable Medicare Advantage data, potentially missing clinical information" [Yang 2026]
The limitations clause, folded into the Discussion block.
> ✎ The limitations ~clause~ *clause,* folded into the Discussion ~block, which is how a letter carries what an~ *block. An* Original Investigation gives *limitations* a titled ~subsection.~ *subsection; the letter format forbids one.* · CC · 260802 1540
An Original Investigation gives limitations a titled subsection; the letter format forbids one.

## Aims

### A1 · 🎯 What the Monday test actually excludes
- A1.1 · The outcome-variable gate is scored before venue rather than at submission.
  **Done when:** a paper with only surrogate endpoints is not shortlisted for this outlet.

### A2 · ⚠️ The three misfiled JNO papers
- A2.1 · The three JNO papers move to `jama-netopen/examples/`.
  **Done when:** this folder holds only JAMA flagship papers and both counts are true.
- A2.2 · The flagship section norms are re-checked against the corrected folder.
  **Done when:** no `jama-<section>/style.md` number rests on a JNO exemplar.

### A3 · 🧾 The structured abstract, and the Key Points box beside it
- A3.1 · A draft abstract for this outlet is checked field by field before its prose is judged.
  **Done when:** an abstract missing a labeled field, the Key Points box, or a 95% CI in RESULTS fails on shape alone.

### A4 · 🚪 The introduction that is over in three paragraphs
- A4.1 · The three IS-family beats are removed whenever a paper is retargeted into this outlet.
  **Done when:** an introduction arriving from `QBv1` or `QBv2` carries no findings preview, no contribution list and no roadmap sentence.

### A5 · 🔬 Methods: the longest section, and it always ends the same way
- A5.1 · The reporting standard is named in the first Methods paragraph, matched to the design.
  **Done when:** every draft names CONSORT or STROBE in its opening paragraph, and a review-shaped paper is flagged because this pack has no PRISMA section file.

### A6 · 📊 Results: prose that carries numbers and nothing else
- A6.1 · The standard display set exists as build requests before the Results prose is written.
  **Done when:** Table 1 and the cohort flow diagram are requested units, and every result claim in the prose names the display it comes from.

### A7 · 🧭 Discussion: short, hedged, and closing on two fixed subsections
- A7.1 · Limitations and Conclusions are present as titled subsections in every draft.
  **Done when:** a Discussion lacking either one fails, and each enumerated limitation names a threat and its direction of bias.

### A8 · 📎 Supplements: numbered by the journal, e-prefixed by the author
- A8.1 · Every supplementary cross-reference in the body carries both numbers.
  **Done when:** no bare eItem and no `in the Supplement` survives in a draft pinned to this outlet.

### A9 · ✉️ The Research Letter: a whole paper under 600 words
- A9.1 · The three letter caps are scored at venue, before the format is chosen.
  **Done when:** a study needing more than 600 words, more than 6 references, or more than one display is not routed to the letter format.
- A9.2 · The stale single-paragraph Discussion line in `jama-letter/style.md` is corrected to the measured range.
  **Done when:** the anti-pattern line and the reconciliation note in that file agree on 1-2 paragraphs.

## States

### A1 · 🎯 What the Monday test actually excludes
- ⬜ A1.1 · Not started. The test is prose in `jama-flagship/taste.md`.

### A2 · ⚠️ The three misfiled JNO papers
- ⬜ A2.1 · Not started. Three files, named in the sibling's taste file, sitting here.
- ⬜ A2.2 · Not started, and dependent on A2.1.

### A3 · 🧾 The structured abstract, and the Key Points box beside it
- ⬜ A3.1 · Not started. The field order and the box live in `jama-abstract/style.md` and `style-profile.md`, and no check reads either.

### A4 · 🚪 The introduction that is over in three paragraphs
- ⬜ A4.1 · Not started. The three anti-patterns are prose in `jama-introduction/style.md` lines 61-68.

### A5 · 🔬 Methods: the longest section, and it always ends the same way
- ⬜ A5.1 · Not started. CONSORT and STROBE each have a section file; PRISMA is named only in `taste.md`.

### A6 · 📊 Results: prose that carries numbers and nothing else
- ⬜ A6.1 · Not started. The standard display set is prose in `playbook-jama-portfolio/README.md`.

### A7 · 🧭 Discussion: short, hedged, and closing on two fixed subsections
- ⬜ A7.1 · Not started. Both subsections are mandatory in `jama-discussion/style.md` and enforced by nothing.

### A8 · 📎 Supplements: numbered by the journal, e-prefixed by the author
- ⬜ A8.1 · Not started. The `eItem N in Supplement M` form is a grep away and no check runs it.

### A9 · ✉️ The Research Letter: a whole paper under 600 words
- ⬜ A9.1 · Not started. Both stored letters run over the 600-word cap, which the pack annotates rather than resolves.
- 🧠 A9.2 · Waiting on a pack edit outside this page: `jama-letter/style.md` line 92 still says single, lines 89 and 117 say 1-2.

## Files

- `../../paper/venue/playbook-jama-portfolio/jama-flagship/taste.md` · the desk signals and the Monday test
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/jama-introduction/style.md` · where the first-paragraph rule has to land
- `QBv7-jama-network-open.md` · the outlet whose exemplars are in this folder

<!-- exemplars:begin -->

📚 **Exemplars** · 19 papers on disk, regenerated by `sync-exemplars.py`

- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/article2338266-2015-jama-medical-marijuana-for-treatment-of-chronic-pain-and-other-medical-and-psychiatric.pdf`
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/article2503508-2016-jama-cdc-guideline-for-prescribing-opioids-for-chronic-pain-united-states-2016.pdf`
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/bronfort-2025-jama-spinal-manipulation-and-clinician-supported-biopsychosocial-self-management-for-ac.pdf` · Bronfort 2025
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/cantor-2025-jama-physician-medicare-participation.pdf` · Cantor 2025
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/cashin-2026-jama-low-back-pain-a-review.pdf` · Cashin 2026
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/cipriani-2026-jama-decision-support-antidepressant.pdf` · Cipriani 2026
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/dijk-2025-jama-clinical-decision-support-imaging.pdf` · Dijk 2025
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/holste-2025-jama-ai-echocardiography-deep-learning.pdf` · Holste 2025
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/jamanetworkopen-2026-antipsychotic-by-clinician-type.md` · Jamanetworkopen 2026 · +xml
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/jamanetworkopen-2026-peer-feedback-hospitalist-antibiotic.md` · Jamanetworkopen 2026 · +xml
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/krebs-2018-jama-effect-of-opioid-vs-nonopioid-medications-on-pain-related-function-in-patients.pdf` · Krebs 2018
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/kroenke-2014-jama-telecare-collaborative-management-chronic-pain-primary-care.pdf` · Kroenke 2014
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/mathioudakis-2025-jama-ai-lifestyle-diabetes-prevention.pdf` · Mathioudakis 2025
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/miller-2025-jama-digital-health-lung-cancer-screening.pdf` · Miller 2025
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/nguyen-2025-jama-payments-physicians-ai-devices.pdf` · Nguyen 2025
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/peachman-2016-jama-opioid-guidelines-mindfulness-pain-relief.pdf` · Peachman 2016
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/peachman-2022-jama-will-the-new-cdc-opioid-prescribing-guidelines-help-correct-the-course-in.pdf` · Peachman 2022
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/rotenstein-2026-jama-ai-scribes-clinician-time.pdf` · Rotenstein 2026
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/yang-2026-jama-cns-prescribing-older-adults-letter.pdf` · Yang 2026

- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/JAMA_EXPANSION_RESULTS.md` · the pack's own manifest, not an exemplar
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/burns-2024-jamanetworkopen-opioid-variation.md  (a note about the paper, no article text on disk)` · the pack's own manifest, not an exemplar

<!-- exemplars:end -->

<!-- kinds:begin -->

📐 **Section kinds** · 7 declared in `stages/section-kinds.yml`, regenerated by `sync-exemplars.py`

`section-edit` runs once per kind, and writes one page each. That is 6 numbered `S-Main-<n>` pages, plus `S-Appendix-<letter>`.

- `S-Main-0` · abstract
- `S-Main-1` · introduction
- `S-Main-2` · methods
- `S-Main-3` · results
- `S-Main-4` · discussion
- `S-Appendix-A` · appendix
- `S-Main-0` of its OWN paper · letter, a standalone article format rather than a section of this one

A kind is the SMALLEST unit a paper gets here, not a ceiling.
One kind can spread across several numbered Main pages.
This repo's own MISQ paper runs to `S-Main-8-conclusion`, and the numbers above move with it.
The ORDER does not move. It is this venue's reading order, not a house default.

<!-- kinds:end -->

🔗 **Authority** · the venue's own instructions, fetched and verified 260802

- [JAMA Instructions for Authors](https://jamanetwork.com/journals/jama/pages/instructions-for-authors) · the flagship's own article-type limits, abstract and Key Points requirements, and editorial policies. The JAMA Network runs a [per-journal index](https://jamanetwork.com/pages/instructions-for-authors) rather than one shared document: the manuscript-preparation, Key Points and reporting-guideline wording is common template text repeated on each journal's page, while every word, reference and display limit is stated per journal, so a number for this desk has to come from the JAMA page and never from a sibling's.
- [JAMA For Authors](https://jamanetwork.com/journals/jama/pages/for-authors) · the submission hub, and the accepted format is Word rather than LaTeX. The Network's shared line reads "For submission and review, please submit the manuscript as a Word document. Do not submit your manuscript in PDF format.", verified verbatim on the JAMA Internal Medicine, JAMA Network Open and JAMA Neurology instruction pages; the flagship page truncates before its own copy of it. LaTeX is named nowhere on any JAMA page fetched, so this repo's markdown-to-LaTeX projection has no accepted landing at this desk and a .docx conversion is a submission requirement, not a convenience.
- CONTRADICTS the pack on the Research Letter, and adds a display cap the pack never recorded. The journal states 800 words of text, 10 references and "up to 2 small tables or figures", against the 600 words, 6 references and one Figure OR one Table at `jama-letter/style.md` lines 7-14, which are the pack's MEASURED figures from stored exemplars; on the official limit both stored letters, annotated at ~666w and ~640w as over-cap, sit comfortably inside it. The Original Investigation entry reads "3000 words of text ... with no more than a total of 5 tables and/or figures", and that display cap appears nowhere in this pack. The abstract ceiling `style-profile.md` line 88 leaves open stays open for the flagship, whose Original Investigation entry says only "A structured abstract is required" and defers to an Abstracts for Reports of Original Data sub-section this fetch could not reach; 350 words is stated outright on the JAMA Internal Medicine and JAMA Network Open pages.
- The `eItem N in Supplement M` address form is NOT a journal instruction. The only Supplement sentence reachable on this page is "If a research manuscript is accepted for publication, the Protocol will be published as a Supplement.", and neither eTable nor eFigure appears in it at all, so the address form at `jama-appendix/style.md` lines 43-63 is a correct reading of published JAMA articles and AMA house style rather than a rule the desk states to authors.

## Law

- This desk's bar is a change in clinical action, so the binding constraint is the outcome variable, which is fixed at the task layer and cannot be acquired during a retarget.
  An exemplar is filed under the outlet it exemplifies, because a section norm extracted from a folder inherits whatever is in it.

## Glossary

- **Monday test**: this desk's own one-sentence bar, asking whether a practising clinician changes what they do because of the result.
- **Surrogate endpoint**: a measured proxy standing in for a clinical outcome, sufficient for many venues and named as a desk-reject here.

## Log

260802 · Readability pass over the whole page, run with `haipipe-writing`.
  The Opening now names the Monday test in the same breath as the question it stands for, and drops the house word "tree".
  Seventeen sentences in Content prose were split or reworded, three of them to cut a bolted-on explanatory clause.
  The four long entries below were split into short sentences, and no fact, number or source citation changed.
  Every rewritten Content sentence carries its own `✎` word-level record.
  This section cannot show one, so this entry is the trail for the four below.
260802 · Corrected against the journal's own instructions.
  `9.1` said JAMA Network Open does not have the `letter` kind, and treated that omission as deliberate.
  The journal publishes Research Letters, so `section-kinds.yml` is incomplete and this page had repeated the pack's gap as a finding.
  The pack's letter limits (600 words, 6 references, 1 display) are MEASURED exemplar figures, not the journal's rule, which is 800 / 10 / 2.
260802 · Authority sub-block added at the end of Files, from the journal's own instructions rather than the pack.
  Three findings the pack cannot see.
  First, the Research Letter's real limits are 800 words, 10 references and up to 2 small tables or figures.
  So the 600 and 6 at `jama-letter/style.md` lines 7-14 are measured exemplar figures rather than the journal's rule, and the two letters logged as over-cap are not over anything.
  Second, Original Investigations carry an undocumented display cap of 5 tables and/or figures total.
  Third, the `eItem N in Supplement M` address form is nowhere in the instructions, so it is house style read off published articles.
  Submission is Word, and LaTeX is not named on any JAMA page fetched, so a conversion step sits between this repo's projection and this desk.
260802 · Two subsubsections added to each of the seven section divisions.
  The first is a `Format values` block carrying WORDS, CITATION DENSITY, VALUE DENSITY and DISPLAYS, with the `jama-<kind>/style.md` line behind each.
  The second is a `The language, in the papers' own words` block of 4-5 short attributed quotations, one per Signature move.
  Value density is on record in three files only.
  It is "Estimate density" at `jama-results/style.md` line 114 and `jama-letter/style.md` line 119.
  It is the per-RESULTS-sentence rule at `jama-abstract/style.md` line 105.
  The other four rows read `not recorded by the pack`, and nothing was measured.
  The only extractable exemplars in this folder are the three JNO papers whose presence `A2.2` exists to undo.
260802 · Seven section-kind divisions added at `### 3` through `### 9`.
  That is one section per kind `stages/section-kinds.yml` gives `jama-flagship`.
  Each carries its arc, its budget with the `style.md` line or exemplar the number came from, its signature moves as slot patterns, and the anti-patterns the pack names.
  Family knowledge from the retired pack page moved in.
  It landed at `3` (the shared seven abstract headings and the Key Points box), `3.1` (the outlet delta table), `6.1` (the standard display set) and `7.1` (the no-blame framing).
  The Writing Style bullet on section norms relaxed from never-copy to cite-the-source.
260802 · Opened with the QBv outlet pages, from `playbook-jama-portfolio/jama-flagship` at `Venue-Paper@fe25a88`.
