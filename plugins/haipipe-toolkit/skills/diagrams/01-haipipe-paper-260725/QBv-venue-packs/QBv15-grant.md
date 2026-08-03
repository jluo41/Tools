# Grant: a venue with no journal, where the reviewer buys a plan rather than a finding

state: 🟡 PARTIAL · 8 agencies as README delta tables · no outlet tree · no exemplars
owner: JL
method: state what makes a grant a venue at all, record the agency deltas as the pack's actual unit, and name the two shape rules this pack breaks on purpose

## Opening

In this system a venue is anything that fixes the structure and says in advance what it will accept. A funding agency does both, and it is stricter than a journal on each. Page limits are enforced, section names are prescribed, and the criteria are published before anyone writes. So why is its pack built so differently from the journal packs beside it?
> ✎ ~This~ *In this* system ~calls~ a venue ~whatever~ *is anything that* fixes the structure and ~states the acceptance test. An~ *says in advance what it will accept. A funding* agency does ~both harder~ *both, and it is stricter* than ~any journal: page~ *a journal on each. Page* limits are enforced, section names are prescribed, and the ~review~ criteria are published ~in advance.~ *before anyone writes.* So why ~would a funding agency not be in a tree of journals?~ *is its pack built so differently from the journal packs beside it?* · CC · 260802 1542

The difference is tense. A journal desk asks what you found, in the past. A review panel asks what you will do, why you are the one to do it, and whether the plan can be carried out. So every argument the paper system builds out of evidence has to be pointed at a plan instead.
> ✎ ~What changes~ *The difference* is ~the~ tense. A journal desk asks what you ~found.~ *found, in the past.* A review panel asks what you will do, why you are the one to do it, and whether the plan ~is feasible. Everything~ *can be carried out. So every argument* the paper system ~knows how to argue from~ *builds out of* evidence has to be ~re-aimed~ *pointed* at a ~plan.~ *plan instead.* · CC · 260802 1542

**Where this page sits**: it is one venue target in `QBv`, and the only one in its pack.
This page owns only what is true of `playbook-grant`.

**Why this pack has no outlet tree**: agencies do not have sections in the way journals do; they have prescribed backbones that differ per agency.
The pack records each agency's backbone, meaning the order of sections that agency prescribes, as a row in a delta table inside `README.md`.
> ✎ The pack ~encodes them~ *records each agency's backbone, meaning the order of sections that agency prescribes,* as *a row in a* delta *table inside `README.md`. Those* tables ~inside `README.md`, and~ *also carry each agency's review lens, meaning the criteria its panel scores a proposal against.* `stages/section-kinds.yml` *then* declares this pack blueprint-only by design, ~which~ *and that file* is where a stage reader meets the exception. · CC · 260802 1542
Those tables also carry each agency's review lens, meaning the criteria its panel scores a proposal against.
`stages/section-kinds.yml` then declares this pack blueprint-only by design, and that file is where a stage reader meets the exception.

**What the pack is missing that every journal pack has**: exemplars.
Eight agencies, no funded proposals on disk, and no `style.md` extracted from anything.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**Never transcribe the agency tables**: they live in `playbook-grant/README.md` and are cited, never copied.

**Keep the tense difference in front**: it is the whole reason a paper cannot be reformatted into a proposal.

✅ `the panel buys a plan`  ❌ `the panel reviews the work`

**Name the agency programme, not just the agency**: NSFC General Program and NSFC Young Scientists are two different backbones and the pack lists them separately.

## Diagram

**Eight agencies, one shared tense**: and a backbone that differs for every one of them.

```text
  🗣 THE TENSE ── a panel buys a PLAN, not a finding
     feasibility · track record · fit to the call
                       │
  📐 THE BACKBONE ── prescribed, and different per agency
  ┌────────────────────────────────────────────────────────┐
  │ NSF     Project Summary (1p: Overview / Intellectual   │
  │         Merit / Broader Impacts) + Project Description │
  │         (15p, Aim-based) + Results from Prior Support  │
  │ NSFC    Rationale / Research Content / Objectives /    │
  │         Plan / Feasibility / Novelty / Expected         │
  │         Outcomes / Prior Accumulation                   │
  │         General Program and Young Scientists differ     │
  │         in weighting                                    │
  │ ERC     Extended Synopsis (5p) + Part B2 (14p) with a  │
  │         WP / deliverables / milestones table           │
  │ KAKENHI Summary / Objective / Plan and Methods /       │
  │         Preparation + an explicit year-by-year plan    │
  │ DFG · SNSF · ARC · NWO · GENERIC                       │
  └────────────────────────────────────────────────────────┘

  🔍 THE LENS ── published in advance, per agency
     NSF: Intellectual Merit · Broader Impacts
     NSFC: scientific significance · novelty · feasibility
           · team
     ERC: Ground-breaking nature · Methodology · PI track record

  🚫 no outlet tree · 🚫 no exemplars · taste.md at FAMILY level
```

## Content

### 1 · Why a grant is a venue

**It fixes structure and publishes its acceptance test**: that is the whole definition this tree uses.

```text
  a VENUE, in this system, is whatever
     ① prescribes the structure           ── agencies do, harder
     ② states what will be accepted        ── published criteria
     ③ has a desk that says no first       ── eligibility + fit

  💡 an agency is a STRICTER venue than a journal on ① and ②
     and the pack's stage maps are the same four:
     ->Claims  ->Display  ->Minimap  ->Write/Edit
```

🎯 Establishes the grant as a first-class venue rather than a courtesy inclusion, on the tree's own definition.

#### 1.1 · The four stage maps survive the change of tense
(which is why this pack can sit in the same tree without a second grammar)
Claims become aims, displays become the figures a panel skims, the minimap becomes the work plan.
The lifecycle stages do not change; what they produce is aimed at a plan instead of a result.

### 2 · The agency delta is the pack's unit

**No outlet folder, so the table IS the outlet**: eight backbones and eight review lenses, in one README.

```text
  📄 README.md carries what a journal pack splits into folders
     ── the backbone table  ≈ the section tree
     ── the review-lens table ≈ taste.md

  ⚠️ so a reader who knows the journal pack shape looks for
     playbook-grant/<agency>/ and finds nothing

  ⚠️ and GENERIC is a real row: user-supplied sections, page
     limits, and criteria ── the pack's escape hatch for an
     agency it does not encode
```

📐 Establishes the delta table as the pack's real unit, and the missing outlet folder as a shape the reader has to be told about.

#### 2.1 · The exception is declared inside the thing it excepts
(so only a reader already in the pack ever learns the pack is shaped differently)
`venue/README.md` says grant and patent are not journals and encode deltas in `README.md` instead of `<journal>/` trees.
A stage resolving `packs:` never opens that file, which `stages/section-kinds.yml` in fact already declares.

### 3 · No exemplars, anywhere

**Eight agencies and nothing funded on disk**: the pack has rewards and no evidence.

```text
  📚 every journal pack   exemplar PDFs + INDEX.md per outlet
     ── the source every style.md number is extracted from

  📭 playbook-grant       0 exemplars
     ── the backbones are correct and the LANGUAGE has no
        source: no funded NSF Project Description, no NSFC
        Rationale section, nothing to imitate

  💥 and the README calls Write/Edit "the main purpose"
     ── the pack's stated main purpose is the one it cannot
        currently serve
```

⚠️ Establishes the gap between the pack's stated purpose and what is on disk to serve it.

### 4 · NSF: Intellectual Merit and Broader Impacts, and a 15-page description

**Two published criteria and a 15-page description**: NSF is one of only two agencies in this pack whose page limits the README states at all.

```text
  📐 BACKBONE ── README Minimap table
     Project Summary            1 page
       Overview · Intellectual Merit · Broader Impacts
     Project Description        15 pages, Aim-based
     References Cited           no limit stated
     Results from Prior Support no limit stated

  📐 BACKBONE ── README Agencies table, under ->Write/Edit
     Project Summary · Project Description (Aims)
     References · Biosketch · Budget Justification
     Data Management Plan

  🔍 REVIEW LENS ── README Agencies table
     Intellectual Merit · Broader Impacts

  ✍️ TONE ── style-profile.md, per-agency notes
     clear direct English
     Aim-based bold headings
     one preliminary-data paragraph per aim
     Broader Impacts concrete and specific, never generic
```

🏛 Establishes the NSF backbone, its two stated page limits, and the published two-criterion lens the pack scores every NSF artifact against.

#### 4.1 · The two README tables describe different NSF proposals
(so which sections exist depends on which stage is reading, and no stage is told that)
The Minimap row carries Results from Prior Support and the Agencies row does not.
The Agencies row carries Biosketch, Budget Justification and Data Management Plan, and the Minimap row does not.
A Minimap stage and a Write/Edit stage reading the same pack therefore build different section lists for the same agency, and nothing in the pack reconciles them.

#### 4.2 · Broader Impacts is the one criterion the pack states four separate times
(which makes it the NSF lens the writing stages are most likely to actually apply)
The Claims map tells a proposal to frame the gap for this agency and names Broader Impacts as NSF's mission language.
`taste.md` lists broader-impacts boilerplate among its triage-reject signals, and asks for impacts specific to this project and this agency.
`style-profile.md` repeats it in the NSF tone note as concrete and specific, never generic.
The Agencies table then scores it as one of exactly two criteria, so a generic Broader Impacts paragraph loses half the published lens rather than a stylistic preference.

#### 4.3 · Format values
(NSF is one of only two agencies here carrying a stated limit, and the limit is counted in pages)

```text
  📏 WORDS            not recorded · NSF bounds PAGES, not words: Project Summary 1p and
                      Project Description 15p, with References Cited and Results from
                      Prior Support carrying no stated limit
                      [playbook-grant/README.md, the Minimap agency table]
  📚 CITATION DENSITY not recorded by the pack
  🔢 VALUE DENSITY    not recorded, and absent by construction: value density counts the
                      numeric values a sentence carries, no style.md anywhere in the venue
                      tree records it, and this pack has no style.md to record it in
  📊 DISPLAYS         nothing NSF-specific · the -> Display map names 4 exhibits for the
                      whole grant family and for no agency: a conceptual framework or
                      overview diagram as the hero tied to the primary aim,
                      preliminary-data figures one per aim, a timeline or Gantt chart, and
                      a budget-justification table with amounts left as [AMOUNT]
                      [playbook-grant/README.md, the -> Display map]

  ⚠️ blueprint-only, so a stage resolving `packs:` gets ZERO hits here and the only
     binding format contract is the paper's own S-Venue-0 blueprint
     [stages/section-kinds.yml, the blueprint-only declaration]
```

#### 4.4 · The language, in the proposals' own words
(there are none, so what follows is the pack's own slot patterns and what each illustrates)

The README names `examples/` as the home of funded-proposal content and says in the same paragraph that it is not yet built, so no NSF sentence exists on disk to quote.
What the pack wrote instead is two family-level slot patterns.
The gap statement reads "Despite progress in [X], [specific gap] remains unaddressed because [reason]. This proposal addresses it by [approach], which will [expected impact]." [`style-profile.md`, Gap statement]
> ✎ *The gap statement reads* "Despite progress in [X], [specific gap] remains unaddressed because [reason]. This proposal addresses it by [approach], which will [expected impact]." [`style-profile.md`, Gap statement] ~illustrates the paragraph the~ *The* profile calls *that paragraph* the single most important sentence in the proposal, and `taste.md` repeats its opening clause as the gap a panellist wants to find. · CC · 260802 1542
The profile calls that paragraph the single most important sentence in the proposal, and `taste.md` repeats its opening clause as the gap a panellist wants to find.
"Building on [preliminary result], we will [objective]; success yields [deliverable]." [`style-profile.md`, Aims and hypotheses] illustrates the rationale to objective to deliverable trace every aim is asked to make.
Neither pattern names NSF, so the only NSF-specific language guidance on disk is a tone note of four clauses.
> ✎ Neither pattern names NSF, so the only NSF-specific language guidance on disk is a ~four-clause~ tone ~note:~ *note of four clauses. It asks for* clear direct English, Aim-based bold headings, one preliminary-data paragraph per aim, and Broader Impacts *that are* concrete and specific [`style-profile.md`, per-agency tone notes]. · CC · 260802 1542
It asks for clear direct English, Aim-based bold headings, one preliminary-data paragraph per aim, and Broader Impacts that are concrete and specific [`style-profile.md`, per-agency tone notes].
A tone note describes language rather than showing it.
> ✎ A tone note describes language rather than showing ~it, and the~ *it. The* README calls the Write/Edit map "the main purpose" of the pack, so what is missing is the pack's own stated centre. · CC · 260802 1548
The README calls the Write/Edit map "the main purpose" of the pack, so what is missing is the pack's own stated centre.

### 5 · NSFC: one backbone, two programmes, four more with no row

**The General Program and Young Scientists share every section and differ in weight**: the pack records the weighting and never says which sections a writer changes.

```text
  📐 BACKBONE ── README Minimap, NSFC General Program
     ① Rationale and Significance    README's own gloss
     ② Research Content
     ③ Research Objectives
     ④ Research Plan
     ⑤ Feasibility Analysis
     ⑥ Novelty
     ⑦ Expected Outcomes
     ⑧ Prior Accumulation
     emphasis   the scientific problem, and accumulation

  ⚖️ YOUNG SCIENTISTS ── same eight sections
     weighting    independence and growth potential
     eligibility  age 35 or under

  📏 PAGE LIMITS ── none stated, for either programme

  🔍 REVIEW LENS ── README Agencies table
     scientific significance · novelty · feasibility
     · research team

  ✍️ TONE ── style-profile.md
     Rationale positioned at the international frontier
     numbered innovation points
     Prior Accumulation cites the applicant's own work
     a detailed feasibility analysis

  🚫 NOT ENCODED ── 4 more sub-programmes the README names
     and gives no backbone row
```

⚖️ Establishes the eight-section NSFC backbone shared by both encoded programmes, the weighting that separates them, and the four sub-programmes the pack names without encoding.

#### 5.1 · Every NSFC section name on this page is a gloss, and only the first is the README's
(because this board is English only and the pack's NSFC rows are not)
The README glosses its first NSFC section as rationale and significance and leaves the other seven untranslated.
The eight English names above are this page's own Diagram glosses, carried down into Content so a reader never has to open the pack to see the shape.
The review lens is glossed the same way, from the four criteria the Agencies table lists untranslated.

#### 5.2 · The pack lists six NSFC sub-programmes and encodes two
(so a proposal pinned to any of the other four falls back on a row nobody chose for it)
The README's `Relationship to the venue layer` section names six NSFC sub-programmes as the deep knowledge the `playbook-grant/` skill carries.
The Minimap table then carries a row for the General Program and one for Young Scientists, and none for the remaining four.
> ✎ The Minimap table then carries a row for the General Program and one for Young Scientists, and none for the remaining ~four, which the~ *four. The* README names *those four* only in ~Chinese~ *Chinese,* and this page glosses *them* as Excellent Young Scientists, Distinguished Young Scholars, Overseas Excellent Young Scientists, and the Key Program. · CC · 260802 1542
The README names those four only in Chinese, and this page glosses them as Excellent Young Scientists, Distinguished Young Scholars, Overseas Excellent Young Scientists, and the Key Program.
Nothing in the pack says which row those four resolve to, and GENERIC is the only honest answer the pack currently offers.

#### 5.3 · Format values
(nothing is recorded for either encoded programme, and the absence covers all four metrics)

```text
  📏 WORDS            not recorded by the pack · neither the General Program row nor the
                      Young Scientists row states a word count or a page limit
                      [playbook-grant/README.md, the Minimap and Agencies tables]
  📚 CITATION DENSITY not recorded by the pack
  🔢 VALUE DENSITY    not recorded by the pack, absent by construction, see 4.3
  📊 DISPLAYS         nothing NSFC-specific · the -> Display map's 4 exhibits, see 4.3,
                      are family-wide and name no agency, and neither NSFC row adds one
                      [playbook-grant/README.md, the -> Display map]

  ⚠️ blueprint-only, so a stage resolving `packs:` gets ZERO hits here and the only
     binding format contract is the paper's own S-Venue-0 blueprint
     [stages/section-kinds.yml, the blueprint-only declaration]
```

#### 5.4 · The language, in the proposals' own words
(no funded NSFC proposal is on disk, and the guidance that exists is written in a language this board does not carry)

The pack stores no NSFC proposal, so the eight-section backbone has correct headings and no sample of what goes under any of them.
The only NSFC-specific language guidance is the tone note, and this page glosses it in English.
> ✎ The only NSFC-specific language guidance is the tone note, ~glossed here:~ *and this page glosses it in English. It asks for* a formal Chinese academic register, a rationale section positioned at the international frontier, *and* numbered innovation ~points,~ *points. It also asks for* a prior-accumulation section citing the applicant's own publications, and *for* a detailed feasibility analysis [`style-profile.md`, per-agency tone notes]. · CC · 260802 1542
It asks for a formal Chinese academic register, a rationale section positioned at the international frontier, and numbered innovation points.
It also asks for a prior-accumulation section citing the applicant's own publications, and for a detailed feasibility analysis [`style-profile.md`, per-agency tone notes].
Each of those five clauses names a section, and none shows a sentence.
> ✎ Each of those five clauses names a ~section~ *section,* and none shows a ~sentence, and the~ *sentence. The* note's own terms are Chinese, so a writer working from this board gets a gloss of a description of prose that is not on disk. · CC · 260802 1548
The note's own terms are Chinese, so a writer working from this board gets a gloss of a description of prose that is not on disk.
The two slot patterns quoted in 4.4 are the pack's only sentence-shaped guidance and they are written in English, which is the register the NSFC note itself rules out.
The README calls the Write/Edit map the pack's main purpose, and NSFC is the row where that map is furthest from being usable.

### 6 · ERC: two documents, and the short one stands alone

**The Extended Synopsis is read by panellists who never open Part B2**: which is why the pack calls it self-contained and gives it 5 of the 19 pages.

```text
  📐 BACKBONE ── both README tables agree here
     Extended Synopsis            5 pages, self-contained
     Scientific Proposal Part B2  14 pages
       carrying a WP (work package) / deliverables /
       milestones table        ── Minimap row only

  📏 PAGE LIMITS ── 5 + 14, the pack's only other stated
     limit besides NSF

  🔍 REVIEW LENS ── README Agencies table
     Ground-breaking nature · Methodology
     · PI track record

  ✍️ TONE ── style-profile.md
     high-risk / high-gain narrative
     self-contained Extended Synopsis
     WP table with deliverables and milestones
     strong PI narrative

  🎯 MISSION LANGUAGE ── Claims map
     high-risk / high-gain is ERC's counterpart of
     NSF's Broader Impacts
```

🚀 Establishes the one agency whose backbone the two README tables agree on, and the work-package table as an agency-specific display the Display map never lists.

#### 6.1 · The work-package table is named in the Minimap and missing from the display set
(so the one display ERC actually scores has no row in the stage that produces displays)
The Display map lists four grant-family displays: the conceptual framework diagram as hero, preliminary-data figures, a timeline or Gantt chart, and a budget-justification table.
The ERC work-package table overlaps the timeline without being the same object, because it binds deliverables and milestones to work packages rather than to dates.
`style-profile.md` states that a timeline with concrete milestones and deliverables is itself a feasibility argument.
> ✎ `style-profile.md` states that a timeline with concrete milestones and deliverables is itself a feasibility ~argument, which~ *argument. Feasibility* is the criterion the Agencies table calls Methodology, so this table is scored rather than decorative. · CC · 260802 1542
Feasibility is the criterion the Agencies table calls Methodology, so this table is scored rather than decorative.

#### 6.2 · Format values
(the pack's only other stated limit, and its only agency-specific exhibit)

```text
  📏 WORDS            not recorded · ERC bounds PAGES, not words: Extended Synopsis 5p and
                      Scientific Proposal Part B2 14p, 19 in total
                      [playbook-grant/README.md, the Minimap and Agencies tables, the one
                      agency where the two agree]
  📚 CITATION DENSITY not recorded by the pack
  🔢 VALUE DENSITY    not recorded by the pack, absent by construction, see 4.3
  📊 DISPLAYS         a WP / deliverables / milestones table, named inside the Part B2
                      backbone [playbook-grant/README.md, the Minimap agency table] and
                      repeated as a tone requirement [style-profile.md, per-agency tone
                      notes] · the -> Display map's 4 family exhibits, see 4.3, do not
                      carry it, which is the gap 6.1 states

  ⚠️ blueprint-only, so a stage resolving `packs:` gets ZERO hits here and the only
     binding format contract is the paper's own S-Venue-0 blueprint
     [stages/section-kinds.yml, the blueprint-only declaration]
```

#### 6.3 · The language, in the proposals' own words
(no funded ERC synopsis is on disk, so the pack's hardest language requirement has no demonstration)

ERC is the one agency whose tone note asks a whole document to do something, rather than asking one section to say something.
> ✎ ERC is the one agency whose tone note asks a whole document to do ~something~ *something,* rather than ~a~ *asking one* section to say ~something: the~ *something. The* Extended Synopsis must be ~self-contained~ *self-contained,* and the narrative *must be* compelling and high-risk / high-gain [`style-profile.md`, per-agency tone notes]. · CC · 260802 1542
The Extended Synopsis must be self-contained, and the narrative must be compelling and high-risk / high-gain [`style-profile.md`, per-agency tone notes].
Nothing on disk shows what a self-contained five-page synopsis reads like, because the pack stores no funded ERC proposal.
The Claims map names high-risk / high-gain as ERC's mission language and pairs it with NSF's Broader Impacts [`playbook-grant/README.md`, the -> Claims map].
> ✎ The Claims map names high-risk / high-gain as ERC's mission language and pairs it with NSF's Broader Impacts [`playbook-grant/README.md`, the -> Claims ~map], which~ *map]. That* tells a writer which words to aim ~at~ *at,* and not how to build a sentence around them. · CC · 260802 1542
That tells a writer which words to aim at, and not how to build a sentence around them.
The two slot patterns in 4.4 are the only sentence shapes the pack offers and neither is a synopsis opening.
So the pack states an imitation purpose for ERC and holds nothing to imitate, on the one row where the requirement is a whole document.

### 7 · KAKENHI: the year-by-year plan is the feasibility argument

**Five sections across two README rows, and no single row carries all five**: the Minimap opens on a Summary the Agencies row drops, and the Agencies row adds a human-rights section the Minimap drops.

```text
  📐 BACKBONE ── README Minimap row
     Summary · Objective · Plan and Methods
     · Preparation
     plus an explicit year-by-year plan

  📐 BACKBONE ── README Agencies row
     Objective · Plan and Methods · Preparation
     · protection of human rights

  📏 PAGE LIMITS ── none stated anywhere in the pack

  🔍 REVIEW LENS ── README Agencies row, glossed here
     academic importance · originality
     soundness of the plan · ability to carry it out

  ✍️ TONE ── style-profile.md
     the formal declarative register of Japanese
       academic prose
     societal significance and originality up front
     concrete yearly milestones
     cite KAKEN-funded related projects
```

📅 Establishes the KAKENHI backbone and its untranslated review lens, and the year-by-year plan as the requirement no other agency in the pack makes explicit.

#### 7.1 · The year-by-year plan is feasibility evidence, not formatting
(which is why it survives translation and the section headings do not)
`style-profile.md` requires the plan to carry concrete yearly milestones, and repeats the requirement in the KAKENHI tone note rather than leaving it to the backbone row.
`taste.md` counts a timeline with concrete milestones among the feasibility evidence that makes a panellist lean forward, for every agency in the family.
So the KAKENHI delta is not that a timeline is wanted, which is family-wide, but that the panel expects it broken out by year and named as its own section.

#### 7.2 · The English on this page is a translation the pack does not own
(so a writer who needs the exact Japanese headings has to open the agency's own forms)
The README glosses four KAKENHI sections and leaves the review criteria and the human-rights section untranslated.
This page glosses the remaining five items, marks them as glosses, and carries no Japanese, because the board is English only.
The pack has no English KAKENHI backbone anywhere, so nothing on disk can be cited as the authority for these names.

#### 7.3 · Format values
(no limit of any kind, against a backbone the README takes the trouble to describe twice)

```text
  📏 WORDS            not recorded by the pack · no word count and no page limit in either
                      of the two KAKENHI rows
                      [playbook-grant/README.md, the Minimap and Agencies tables]
  📚 CITATION DENSITY not recorded by the pack
  🔢 VALUE DENSITY    not recorded by the pack, absent by construction, see 4.3
  📊 DISPLAYS         nothing KAKENHI-specific in the map · the year-by-year plan the
                      Minimap row requires is a backbone section rather than an entry in
                      the -> Display map, whose 4 family exhibits, see 4.3, name no agency
                      [playbook-grant/README.md, the Minimap agency table and the
                      -> Display map]

  ⚠️ blueprint-only, so a stage resolving `packs:` gets ZERO hits here and the only
     binding format contract is the paper's own S-Venue-0 blueprint
     [stages/section-kinds.yml, the blueprint-only declaration]
```

#### 7.4 · The language, in the proposals' own words
(the register the pack names is Japanese, the pack holds no Japanese prose, and this board carries none either)

The tone note asks for the formal declarative register of Japanese academic writing, with societal significance and originality stated up front.
> ✎ The tone note asks for the formal declarative register of Japanese academic writing, *with* societal significance and originality stated up ~front,~ *front. It also asks for* concrete yearly milestones, and *for* citations to KAKEN-funded related projects [`style-profile.md`, per-agency tone notes]. · CC · 260802 1542
It also asks for concrete yearly milestones, and for citations to KAKEN-funded related projects [`style-profile.md`, per-agency tone notes].
A register is the hardest thing to convey by description and the easiest to convey by example, and the pack has no funded KAKENHI proposal to serve as that example.
The README's KAKENHI rows are section names in Japanese, glossed only in part, so the pack's own text is not a sample of proposal prose either.
The two slot patterns in 4.4 are English, would have to be rewritten in that register before a writer could use them here, and the pack says nothing about how.
So the Write/Edit map the README calls its main purpose reaches KAKENHI as an instruction to imitate a voice that appears nowhere on disk.

### 8 · DFG, SNSF, ARC and NWO: one line each, and a shared claim that fits one

**Four agencies whose entire encoding is a backbone and a lens**: no page limits, no tone note of their own, and a grouped style rule that only DFG's sections support.

```text
  agency  backbone, README Agencies   review lens
  ──────────────────────────────────────────────────────
  DFG     State of the Art            Scientific quality
          Objectives                  Originality
          Work Programme              Feasibility
          Bibliography · CV           PI qualification

  SNSF    Summary                     Scientific relevance
          Research Plan               Originality
          Timetable · Budget          Feasibility
                                      Track record

  ARC     Project Description         Research quality
          Feasibility                 Feasibility
          Benefit · Budget            Benefit to Australia

  NWO     Summary                     Scientific quality
          Proposed Research           Innovative character
          Knowledge Utilisation       Knowledge utilisation

  📏 PAGE LIMITS ── none stated, for any of the four

  ⚠️ style-profile.md groups all four under a
     state-of-the-art-then-objectives backbone
     ── only DFG has a State of the Art section
```

🧩 Establishes the four thinnest rows in the pack as one unit, and the grouped tone note as a claim three of them do not support.

#### 8.1 · Three of the four score feasibility outright, and NWO scores use instead
(which is the one routing question this group actually poses to a writer)
DFG, SNSF and ARC each name feasibility as a scored criterion in the README's Agencies table.
NWO does not: its three criteria are scientific quality, innovative character and knowledge utilisation, and `style-profile.md` says NWO stresses knowledge utilisation.
A proposal built for the other three therefore arrives at NWO with its feasibility case intact and its utilisation case absent, which is the same silent-failure shape a journal retarget has.

#### 8.2 · These four are where the pack's per-agency knowledge runs out
(so they are the rows most likely to be wrong and the least likely to be noticed)
Each of the four is one backbone string and one lens string.
> ✎ Each of the four is one backbone string and one lens ~string, with no~ *string. None of them carries a* page limit, ~no~ *a* sub-programme, ~and no~ *or a* tone note beyond the two clauses `style-profile.md` gives ARC and NWO. · CC · 260802 1548
None of them carries a page limit, a sub-programme, or a tone note beyond the two clauses `style-profile.md` gives ARC and NWO.
NSF, NSFC, ERC and KAKENHI each get a second description in the Minimap table and a paragraph of their own in the per-agency tone notes; these four get neither.
The README states that the deep agency knowledge is carried in the `playbook-grant/` skill.
> ✎ The README states that the deep agency knowledge is carried in the `playbook-grant/` ~skill, so~ *skill. So* a thin row here is not evidence *that* the knowledge is missing, only that this pack does not hold it. · CC · 260802 1542
So a thin row here is not evidence that the knowledge is missing, only that this pack does not hold it.

#### 8.3 · Format values
(one block for four agencies, because the pack records the same absence four times over)

```text
  📏 WORDS            not recorded by the pack, for any of the four · no word count and no
                      page limit for DFG, SNSF, ARC or NWO
                      [playbook-grant/README.md, the Agencies table, the only table
                      carrying these four at all]
  📚 CITATION DENSITY not recorded by the pack
  🔢 VALUE DENSITY    not recorded by the pack, absent by construction, see 4.3
  📊 DISPLAYS         nothing specific to any of the four · SNSF names a Timetable and a
                      Budget, ARC a Budget, DFG a Bibliography and a CV, all of them
                      backbone sections rather than entries in the -> Display map, whose
                      4 family exhibits, see 4.3, name no agency
                      [playbook-grant/README.md, the Agencies table and the -> Display map]

  ⚠️ blueprint-only, so a stage resolving `packs:` gets ZERO hits here and the only
     binding format contract is the paper's own S-Venue-0 blueprint
     [stages/section-kinds.yml, the blueprint-only declaration]
```

#### 8.4 · The language, in the proposals' own words
(four agencies share two clauses of tone guidance between them, and hold no proposal at all)

The whole of the pack's language guidance for these four is one line.
> ✎ The whole of the pack's language guidance for these four is one ~line:~ *line. It gives them* a state-of-the-art-then-objectives backbone, *and adds that* ARC stresses benefit to ~Australia,~ *Australia and* NWO stresses knowledge utilisation [`style-profile.md`, per-agency tone notes]. · CC · 260802 1548
It gives them a state-of-the-art-then-objectives backbone, and adds that ARC stresses benefit to Australia and NWO stresses knowledge utilisation [`style-profile.md`, per-agency tone notes].
DFG and SNSF get no clause of their own in it, so two of the four have no language guidance in this pack whatsoever.
No funded DFG, SNSF, ARC or NWO proposal is on disk, which leaves those two clauses as the only thing a writing stage can act on for the group.
8.1 already names the routing consequence, and the language gap sharpens it.
> ✎ 8.1 already names the routing consequence, and the language gap sharpens ~it: a~ *it. A* proposal built for the other three arrives at NWO with no knowledge-utilisation prose, and nothing here shows what such prose sounds like. · CC · 260802 1542
A proposal built for the other three arrives at NWO with no knowledge-utilisation prose, and nothing here shows what such prose sounds like.
A one-line note still looks like guidance.
> ✎ A one-line note still looks like ~guidance, which is why~ *guidance. So* this is the group where the distance from the README's stated main purpose is both largest and hardest to notice. · CC · 260802 1542
So this is the group where the distance from the README's stated main purpose is both largest and hardest to notice.

### 9 · GENERIC: the escape hatch, and three fields nobody is asked for

**The pack encodes eight agencies and one row for everything else**: GENERIC takes user-supplied sections, page limits and criteria, and the pack names no place to supply them.

```text
  🚪 GENERIC ── the row, identical in both README tables
     sections      user-supplied
     page limits   user-supplied
     criteria      user-supplied

  🎯 HOW ANY ROW IS SELECTED ── README, "How to use"
     the agency and sub-programme are set in the
     proposal's STATUS.md `venue` field, which selects
     the per-agency delta in the minimap

  ⚠️ so GENERIC selects a row with three empty fields
     ── no schema, no template, no prompt
     ── and the Write/Edit stage still runs

  🧭 WHO NEEDS IT TODAY
     the 4 NSFC sub-programmes with no row
     every agency outside the 8 the pack encodes
```

🚪 Establishes GENERIC as a row the pack can select and cannot fill, which is the difference between an escape hatch and a hole.

#### 9.1 · GENERIC is the only row whose review lens is also user-supplied
(so it is the one target in this tree that ships with no acceptance test at all)
Every other row in the README's Agencies table names its criteria, because an agency publishes them in advance.
> ✎ Every other row in the README's Agencies table names its criteria, because an agency publishes them in ~advance, which~ *advance. That* is the property division 1 uses to call a grant a venue. · CC · 260802 1542
That is the property division 1 uses to call a grant a venue.
GENERIC names none, and until a person types three fields in, a proposal pinned to it has a venue by name and not by this tree's own definition.
The escape hatch is therefore also the one place the definition this page opens with stops holding, and the pack does not say so.

#### 9.2 · Format values
(the one row whose page limit is deferred rather than simply missing, which leaves six of the pack's nine agency rows stating none at all)

```text
  📏 WORDS            not recorded, and not the pack's to record · page limits are one of
                      GENERIC's three user-supplied fields
                      [playbook-grant/README.md, the Minimap and Agencies tables]
  📚 CITATION DENSITY not recorded by the pack
  🔢 VALUE DENSITY    not recorded by the pack, absent by construction, see 4.3
  📊 DISPLAYS         nothing GENERIC-specific · displays are not among the row's three
                      user-supplied fields, and the -> Display map's 4 family exhibits,
                      see 4.3, reach this row the same way they reach every other
                      [playbook-grant/README.md, the Agencies table and the -> Display map]

  ⚠️ blueprint-only, so a stage resolving `packs:` gets ZERO hits here and the only
     binding format contract is the paper's own S-Venue-0 blueprint
     [stages/section-kinds.yml, the blueprint-only declaration]
```

#### 9.3 · The language, in the proposals' own words
(the one row carrying neither a proposal nor a description of one)

Every other agency in the pack gets at least a clause in the per-agency tone notes, and GENERIC gets no line there at all [`style-profile.md`, per-agency tone notes].
It therefore inherits family guidance only: the two slot patterns quoted in 4.4 and the significance-first arc.
> ✎ It therefore inherits family guidance only: the two slot patterns quoted in ~4.4,~ *4.4 and* the significance-first ~arc, and~ *arc. The third piece is* `taste.md`'s question, "Could the panelist, after one read of the Specific Aims page, retell the gap, the aims, and why this team will deliver". · CC · 260802 1542
The third piece is `taste.md`'s question, "Could the panelist, after one read of the Specific Aims page, retell the gap, the aims, and why this team will deliver".
That question is the family's own acceptance test, and it shows what the pack expects a reader to be able to do after one page.
> ✎ That question is the family's own acceptance test, and it ~illustrates~ *shows* what the pack expects a reader to be able to do after one ~page, which for~ *page. For* GENERIC *it* is the only test on offer, because 9.1 shows *that* the row's criteria are user-supplied too. · CC · 260802 1542
For GENERIC it is the only test on offer, because 9.1 shows that the row's criteria are user-supplied too.
No funded proposal is on disk for any agency, so a GENERIC target arrives with no sample, no tone note, and no criteria.
> ✎ No funded proposal is on disk for any agency, so a GENERIC target arrives with no sample, no tone note, and no ~criteria,~ *criteria. That is* three ~absences~ *absences,* where every other row has at least one field filled. · CC · 260802 1542
That is three absences, where every other row has at least one field filled.
The Write/Edit map is still what a GENERIC proposal reaches, and at this row it carries nothing that was written for the agency being written to.

### 10 · The appendix question: supporting documents, not an overflow

**A proposal has no appendix, and the journal packs' appendix has no counterpart here**: supporting documents are named rows of the backbone itself, with their own forms and their own readers.

```text
  📄 THE PAGE-LIMITED NARRATIVE ── all the pack states
     NSF  Project Summary 1p + Project Description 15p
     ERC  Extended Synopsis 5p + Part B2 14p
     ── no other agency in the pack has a stated limit

  📎 SUPPORTING DOCUMENTS the pack names, by agency
     NSF      References Cited            Minimap row
              Results from Prior Support  Minimap row
              References · Biosketch      Agencies row
              Budget Justification        Agencies row
              Data Management Plan        Agencies row
     DFG      Bibliography · CV
     SNSF     Budget
     ARC      Budget
     KAKENHI  protection of human rights

  🚫 NAMED NOWHERE IN THE PACK
     letters of support
     facilities and other resources
     current and pending support
     mentoring or training plans

  📐 AND NO APPENDIX PAGE EXISTS
     section-kinds.yml declares no kinds for this pack,
     so the appendix -> S-Appendix-<letter> mapping every
     journal outlet gets is not generated here
```

🗂 Establishes the supporting document as this venue's answer to the appendix question, and names the four supporting documents the pack does not carry.

#### 10.1 · A supporting document cannot absorb narrative overflow
(which is the practical difference from a journal appendix, and the reason the split matters)
A journal appendix takes what the main text cannot hold, and the same reviewer reads both.
> ✎ A journal appendix takes what the main text cannot hold, and the same reviewer reads ~both, which is why~ *both. So* a page-limited section can push material into it. · CC · 260802 1542
So a page-limited section can push material into it.
An agency's supporting documents are separate uploads on their own forms, and the pack states no page limit for any of them.
> ✎ An agency's supporting documents are separate uploads on their own forms, *and* the pack states no page limit for any of ~them, and nothing~ *them. Nothing* about them relaxes the 15-page NSF Project Description or the 14-page ERC Part B2. · CC · 260802 1542
Nothing about them relaxes the 15-page NSF Project Description or the 14-page ERC Part B2.
`taste.md` pushes the burden the other way: preliminary data, existing datasets, infrastructure and a timeline with concrete milestones are feasibility evidence the panel expects inside the narrative, not filed behind it.

#### 10.2 · The budget justification is a display unit, and the one rule the pack states about it is a ban
(so the pack's only instruction on writing a supporting document is about what may not be written)
The Display map lists a budget-justification table among the four grant-family displays.
> ✎ The Display map lists a budget-justification table among the four grant-family ~displays, mapping~ *displays. It maps* cost categories to aims, *in* narrative only, with amounts left as `[AMOUNT]` placeholders. · CC · 260802 1542
It maps cost categories to aims, in narrative only, with amounts left as `[AMOUNT]` placeholders.
`taste.md` and `style-profile.md` both repeat the ban: never fabricate an amount, a publication or a credential, and leave a `[AMOUNT]` or `[TODO]` placeholder instead.
That is the whole of what the pack says about how a supporting document is written, and it says nothing about what belongs in one.

#### 10.3 · Results from Prior Support is claim-bearing, which no journal appendix is
(so the closest thing to an appendix here is scored, not tolerated)
The Claims map lists PI track record among the two to four supporting claims a grant proposal is built from, alongside preliminary-data feasibility and broader impact.
`taste.md` asks for the gap to be positioned against competing funded projects.
> ✎ `taste.md` asks for the gap to be positioned against competing funded ~projects, and~ *projects.* ERC, DFG and SNSF each score ~it~ *that record* in the README's Agencies table, as PI track record, PI qualification and track ~record respectively.~ *record, in that order.* · CC · 260802 1542
ERC, DFG and SNSF each score that record in the README's Agencies table, as PI track record, PI qualification and track record, in that order.
So the material a journal writer would file as back matter is a named backbone section at NSF, and a scored criterion at three more agencies.
> ✎ So the material a journal writer would file as back matter is a named backbone section at ~NSF~ *NSF,* and a scored criterion at three more ~agencies, which~ *agencies. That* is four of the pack's nine rows. · CC · 260802 1542
That is four of the pack's nine rows.

## Aims

### A1 · 🎯 Why a grant is a venue
- A1.1 · The tense change is stated where a paper is converted into a proposal.
  **Done when:** converting a claim ledger into aims names what each claim becomes, rather than reusing it.

### A2 · 📐 The agency delta is the pack's unit
- A2.1 · The blueprint-only declaration and this pack's own contents cannot disagree.
  **Done when:** adding a per-section pack here fails until `section-kinds.yml` stops calling it blueprint-only.

### A3 · ⚠️ No exemplars, anywhere
- A3.1 · At least one funded proposal per agency this repo actually targets lands in the pack.
  **Done when:** the language guidance the README calls its main purpose has a source on disk.

### A4 · 🏛 NSF: Intellectual Merit and Broader Impacts, and a 15-page description
- A4.1 · The Minimap row and the Agencies row name one NSF backbone.
  **Done when:** References Cited, Results from Prior Support, Biosketch, Budget Justification and Data Management Plan sit in one list, and no stage can read a shorter one.

### A5 · ⚖️ NSFC: one backbone, two programmes, four more with no row
- A5.1 · The Young Scientists weighting is written as something a writer can act on.
  **Done when:** the delta names which of the eight sections change, rather than only that the emphasis moves to independence and growth potential.
- A5.2 · The four named but unencoded NSFC sub-programmes either get a row or are dropped from the README's list.
  **Done when:** a proposal pinned to one of them resolves to a stated backbone, instead of falling back on the General Program row without saying so.

### A6 · 🚀 ERC: two documents, and the short one stands alone
- A6.1 · The WP / deliverables / milestones table is produced by the Display stage, not only described in the Minimap.
  **Done when:** an ERC proposal's work-package table is a display unit with the same standing as the hero overview diagram.

### A7 · 📅 KAKENHI: the year-by-year plan is the feasibility argument
- A7.1 · The KAKENHI backbone is stated once, with both the Summary and the human-rights section in it.
  **Done when:** the Minimap row and the Agencies row cannot name different sections for the same agency.

### A8 · 🧩 DFG, SNSF, ARC and NWO: one line each, and a shared claim that fits one
- A8.1 · The grouped tone note stops claiming a backbone three of its four agencies do not have.
  **Done when:** the state-of-the-art-then-objectives line is scoped to DFG, or the other three rows carry the section that would justify it.

### A9 · 🚪 GENERIC: the escape hatch, and three fields nobody is asked for
- A9.1 · The three user-supplied fields have a place to be supplied.
  **Done when:** pinning GENERIC asks for sections, page limits and criteria, and a proposal cannot reach Write/Edit with all three empty.

### A10 · 🗂 The appendix question: supporting documents, not an overflow
- A10.1 · The main-narrative versus supporting-document split is stated as a rule rather than inferred from backbone rows.
  **Done when:** a writer asking where a data management plan or a biosketch goes gets the answer from the pack instead of from the agency's call text.
- A10.2 · The four supporting documents the pack names nowhere are either encoded or declared out of scope.
  **Done when:** letters of support, facilities and other resources, current and pending support, and mentoring plans each have a stated home or a stated absence.

## States

### A1 · 🎯 Why a grant is a venue
- ⬜ A1.1 · Not started. The stage maps exist; the claim-to-aim conversion is unwritten.

### A2 · 📐 The agency delta is the pack's unit
- ✅ A2.1 · Resolved on inspection, and replaced. `stages/section-kinds.yml` names grant and patent blueprint-only by design, in a file both venue and section-edit read.

### A3 · ⚠️ No exemplars, anywhere
- ⬜ A3.1 · Not started. Zero exemplars against 21 to 29 for each populated journal outlet.

### A4 · 🏛 NSF: Intellectual Merit and Broader Impacts, and a 15-page description
- ⬜ A4.1 · Not started. The two rows were compared for the first time on 260802 and neither has been changed.

### A5 · ⚖️ NSFC: one backbone, two programmes, four more with no row
- ⬜ A5.1 · Not started. The Minimap row states the weighting in one clause and names no section.
- ⬜ A5.2 · Not started. Six sub-programmes are listed in the README prose and two have rows.

### A6 · 🚀 ERC: two documents, and the short one stands alone
- ⬜ A6.1 · Not started. The Display map's four grant-family displays contain no work-package table.

### A7 · 📅 KAKENHI: the year-by-year plan is the feasibility argument
- ⬜ A7.1 · Not started. The Minimap row and the Agencies row still disagree by one section each way.

### A8 · 🧩 DFG, SNSF, ARC and NWO: one line each, and a shared claim that fits one
- ⬜ A8.1 · Not started. Only DFG's backbone opens on State of the Art; SNSF and NWO open on Summary and ARC on Project Description.

### A9 · 🚪 GENERIC: the escape hatch, and three fields nobody is asked for
- ⬜ A9.1 · Not started. The README names the `venue` field that selects a row and no field that fills GENERIC's three.

### A10 · 🗂 The appendix question: supporting documents, not an overflow
- ⬜ A10.1 · Not started. The split is readable off the backbone rows and is written down nowhere.
- ⬜ A10.2 · Not started. All four are absent from README, taste.md and style-profile.md alike.

## Files

- `../../paper/venue/playbook-grant/README.md` · the agency backbone and review-lens tables, plus the four stage maps
- `../../paper/venue/playbook-grant/taste.md` · the panel's test, at family level
- `../../paper/venue/playbook-grant/style-profile.md` · the per-agency tone notes, the only per-agency writing guidance on disk
- `QBv16-patent.md` · the other non-journal pack, same shape exception

<!-- exemplars:begin -->

📚 **Exemplars** · 0 papers on disk, regenerated by `sync-exemplars.py`

Filed at FAMILY level under `../../paper/venue/playbook-grant/examples/`, not under the outlet (the group intro on the Index).

- none. No `examples/` folder under `../../paper/venue/playbook-grant/`, so this outlet states section norms with no exemplar behind them.

<!-- exemplars:end -->

<!-- kinds:begin -->

📐 **Section kinds** · none declared in `stages/section-kinds.yml`, so this venue is blueprint-only: the S-Venue-0 blueprint is binding and no per-section pack is resolved.

<!-- kinds:end -->

🔗 **Authority** · the agency's own rules, fetched and verified 260802

- [NSF Proposal and Award Policies and Procedures Guide, NSF 24-1](https://www.nsf.gov/policies/pappg/24-1) · the binding preparation rules for every NSF proposal. Current version NSF 24-1, published 22 January 2024, applying to proposals submitted or due on or after 20 May 2024, supplemented by policy notices NSF 26-200 and NSF 26-202 for awards from December 2025 and January 2026. Every NSF number below is stated in [Chapter II, Proposal Preparation Instructions](https://www.nsf.gov/policies/pappg/24-1/ch-2-proposal-preparation).
- [NSFC 2026 Project Guide](https://www.nsfc.gov.cn/p1/2931/4077/2026nxmzn.html) · the annual guide that is this agency's own application authority, posted from January 2026, Chinese-language only. [The 2026 notice on applications and completions](https://www.nsfc.gov.cn/p1/3381/2824/99667.html), dated 14 January 2026, is the instruction telling applicants to read that guide's application-instructions section before writing and to draft in the online system from 15 January 2026, also Chinese-language only.
- [ERC Advanced Grant, how to apply](https://erc.europa.eu/apply-grant/advanced-grant) · the scheme page carrying the call documents, both Work Programmes and the Information for Applicants for the 2026 call. [The Work Programme 2026](https://erc.europa.eu/news-events/news/erc-work-programme-2026-adopted) was adopted 8 July 2025, and [the changes it introduces](https://erc.europa.eu/news-events/news/changes-2026-and-2027-work-programmes) are what restructure the scientific proposal into Part I and Part II.
- [JSPS KAKENHI application procedure and forms](https://www.jsps.go.jp/english/e-grants/grants09.html) · the official English-language door to the Grants-in-Aid application procedures and to the Electronic Application System in which the Research Proposal Document is written. The procedures are issued per fiscal year and per research category rather than as one standing guide, so this page routes to the year's documents and states no limit itself.
- [DFG Proposal Preparation Instructions, form 54.01](https://www.dfg.de/resource/blob/168314/9c1a931f2b58c0ec2ccfa7023fb687c7/54-01-en-data.pdf) · version 06/26, the instructions for a Project Proposal, reached from [the Research Grants forms and guidelines page](https://www.dfg.de/en/research-funding/funding-opportunities/programmes/individual/research-grants/forms-guidelines), which also names form 53.01 elan as the project-description template.
- [SNSF requirements for the research plan](https://www.snf.ch/en/257qx6wxjo72ODHy/page/funding/documents-downloads/regulations-requirements-for-the-research-plan) · the agency's own research-plan rules: length, formatting, the five required sections, the original-text requirement, and the ban on annexed documents.
- [NWO Open Competition Domain Science M 2026/2027](https://www.nwo.nl/en/calls/open-competition-domain-science-m-2026/2027) · one live call carrying its own Call for Proposals document and the application forms the agency requires. NWO publishes rules per call rather than as one standing guide, and [the calls index](https://www.nwo.nl/en/calls) is where a target picks the document that binds it.
- CONFIRMS both NSF page limits this page carries at 4, 4.3 and 10. PAPPG 24-1 states "Each proposal must contain a summary of the proposed project not more than one page in length", covering Overview, Intellectual Merit and Broader Impacts, and that the Project Description "may not exceed 15 pages", with conformance to the 15 pages "strictly enforced".
- CORRECTS Results from Prior NSF Support, recorded at 4, 4.3 and 10 as carrying no stated limit. The same PAPPG sentence limits it to five pages and counts those five INSIDE the 15, so a proposal that owes the section has 10 pages of new narrative rather than 15. References Cited stays unlimited in pages, which the same passage states, and that half of the row is right.
- CONFIRMS the 5-page ERC synopsis and CORRECTS its 14-page partner, recorded at 6, 6.2 and 10. From the 2026 calls the ERC renamed the Extended Synopsis to Part I of the Scientific Proposal and kept it at five pages; Part B2 became Part II and dropped to seven pages for Starting, Consolidator and Advanced Grants, ten for Synergy Grants, with the budget and resources justification outside the count. The 19-page total at 6.2 is therefore 12 for the three single-investigator schemes, and feasibility moved out of the Step 1 assessment into Part II.
- CORRECTS the "no page limits stated" rows for DFG and SNSF at 8 and 8.3. DFG form 54.01 caps the project description at 25 pages, up to 17 for sections 1 to 3 and up to 8 from section 4, in no less than Arial 11 with 1.2 line spacing. SNSF caps the research plan at 15 pages AND 60,000 characters including spaces, 17 and 68,000 for collaborative projects, with the first limit reached applying. Both are published by the agency and simply absent from the pack, so the absence at 8.3 is the pack's and not the agencies'.
- CONTRADICTS 8.1 and A8.1 on the state-of-the-art opening. Both read the grouped style note as fitting DFG alone. DFG form 54.01 does open on "Starting point: State of the art and preliminary work" followed by "Objectives and work programme", and the SNSF research plan's first two required sections are "Current state of research" and "Current state of your own research", so two of the four support the note rather than one, and A8.1's fix has to scope it to DFG and SNSF.
- NOT VERIFIED, and deliberately unwritten. No ARC URL appears above: arc.gov.au refused every connection attempted on 260802, with read timeouts and HTTP/2 stream errors on three separate paths, so the one agency in the DFG group whose criteria the pack states most specifically has no authority link here. Separately, the NWO call weights its assessment as scientific quality 75% and scientific or societal impact 25%, two criteria against the three the pack's Agencies table lists for NWO, which 8.1 leans on.

## Law

- A grant is a venue because it prescribes structure and publishes its acceptance test, and it is a stricter one than any journal on both counts.
  A panel buys a plan, so every lifecycle artifact is re-aimed from what was found to what will be done.
> ✎ A panel buys a plan, so every lifecycle artifact is re-aimed from what was found to what will be ~done, and a~ *done. A* claim converted into an aim without changing tense has not been converted. · CC · 260802 1548
  A claim converted into an aim without changing tense has not been converted.

## Glossary

- **Backbone**: an agency's prescribed section sequence, which plays the role a journal's section tree plays in the other packs.
- **Review lens**: the published criteria a panel scores against, which plays the role `taste.md` plays for a journal.
- **GENERIC**: the pack's escape-hatch row, for an agency whose sections, page limits, and criteria the user supplies.

## Log

260802 · Authority block added at the end of Files, from the agencies' own rules rather than the pack, covering seven of the nine rows.
> ✎ 260802 · Authority block added at the end of Files, from the agencies' own rules rather than the pack, covering seven of the nine rows. NSF's two page limits are confirmed at ~source, and~ *source.* Results from Prior NSF Support is corrected: it is capped at five pages and counted inside the 15, which this page recorded as unlimited in three places. ERC's five-page synopsis survives under a new name, Part I, while the 14-page Part B2 does ~not: it~ *not. Part B2* is now Part ~II~ *II,* at seven pages for Starting, Consolidator and Advanced Grants and ten for Synergy, so 19 becomes 12. Two of the four thin rows do state limits the pack calls ~absent,~ *absent:* DFG at 25 pages split 17 plus ~8~ *8,* and SNSF at 15 pages and 60,000 ~characters, and~ *characters.* SNSF also opens its research plan on the current state of research, which breaks the claim at 8.1 and A8.1 that only DFG supports the grouped state-of-the-art note. ARC is the one agency with no link: arc.gov.au refused every connection tried that day. · CC · 260802 1542
  NSF's two page limits are confirmed at source.
  Results from Prior NSF Support is corrected: it is capped at five pages and counted inside the 15, which this page recorded as unlimited in three places.
  ERC's five-page synopsis survives under a new name, Part I, while the 14-page Part B2 does not.
  Part B2 is now Part II, at seven pages for Starting, Consolidator and Advanced Grants and ten for Synergy, so 19 becomes 12.
  Two of the four thin rows do state limits the pack calls absent: DFG at 25 pages split 17 plus 8, and SNSF at 15 pages and 60,000 characters.
  SNSF also opens its research plan on the current state of research, which breaks the claim at 8.1 and A8.1 that only DFG supports the grouped state-of-the-art note.
  ARC is the one agency with no link: arc.gov.au refused every connection tried that day.
260802 · Added a Format values block and a language subsubsection to each of the six agency divisions, twelve in all.
> ✎ 260802 · Added a Format values block and a language subsubsection to each of the six agency divisions, twelve in all. Of the twenty-four metric rows, three carry a ~value:~ *value. Two are* NSF's and ERC's page counts, which the pack states in place of any word budget, and *the third is* ERC's WP / deliverables / milestones table. Citation density is recorded nowhere in the ~pack, and value~ *pack. Value* density is absent by construction, since no style.md in the venue tree records it and this pack has no style.md at all. The pack stores no funded proposal, so the language subsubsections quote the two slot patterns `style-profile.md` wrote for ~itself and~ *itself. They also* name the per-agency tone note as the only agency-specific guidance on disk, which describes prose rather than showing it. · CC · 260802 1542
  Of the twenty-four metric rows, three carry a value.
  Two are NSF's and ERC's page counts, which the pack states in place of any word budget, and the third is ERC's WP / deliverables / milestones table.
  Citation density is recorded nowhere in the pack.
  Value density is absent by construction, since no style.md in the venue tree records it and this pack has no style.md at all.
  The pack stores no funded proposal, so the language subsubsections quote the two slot patterns `style-profile.md` wrote for itself.
  They also name the per-agency tone note as the only agency-specific guidance on disk, which describes prose rather than showing it.
260802 · Expanded Content with one division per agency the README encodes, plus one on what a proposal has instead of an appendix.
> ✎ 260802 · Expanded Content with one division per agency the README encodes, plus one on what a proposal has instead of an appendix. Each division carries that agency's backbone, its page limits, and its published review lens, with the source named inline. Three findings came out of writing ~them: the~ *them. The* README describes NSF and KAKENHI in two tables that name different ~sections, only~ *sections. Only* NSF and ERC have any stated page ~limit, and the~ *limit. The* pack names six NSFC sub-programmes while encoding two. All CJK in the pack's NSFC and KAKENHI rows is carried here as English glosses, marked as glosses where the README does not supply one. · CC · 260802 1542
  Each division carries that agency's backbone, its page limits, and its published review lens, with the source named inline.
  Three findings came out of writing them.
  The README describes NSF and KAKENHI in two tables that name different sections.
  Only NSF and ERC have any stated page limit.
  The pack names six NSFC sub-programmes while encoding two.
  All CJK in the pack's NSFC and KAKENHI rows is carried here as English glosses, marked as glosses where the README does not supply one.
260802 · Corrected against `stages/section-kinds.yml`, found while answering how a Content division becomes an S-Main page.
> ✎ 260802 · Corrected against `stages/section-kinds.yml`, found while answering how a Content division becomes an S-Main page. That file already carries the glob rule for the section ~abbreviation,~ *abbreviation and* an outlet-to-kinds map measured on ~disk,~ *disk. It also carries* the `theory-model` ~alias,~ *alias* and ~the blueprint-only declaration for~ *declares* grant and ~patent.~ *patent blueprint-only by design.* Four claims on this group that something was undeclared were wrong, and the Aims they carried are replaced by drift guards. · CC · 260802 1542
  That file already carries the glob rule for the section abbreviation and an outlet-to-kinds map measured on disk.
  It also carries the `theory-model` alias and declares grant and patent blueprint-only by design.
  Four claims on this group that something was undeclared were wrong, and the Aims they carried are replaced by drift guards.
260802 · Opened with the QBv group, from `playbook-grant` at `Venue-Paper@fe25a88`.
