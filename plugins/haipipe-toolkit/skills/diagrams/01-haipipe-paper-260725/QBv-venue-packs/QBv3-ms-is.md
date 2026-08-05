# MS-IS: the desk that thinks in equilibria and welfare, not constructs and implications

state: 🟡 PARTIAL · 10 exemplars · 7 sections · taste ✓ · the vocabulary switch is recorded nowhere a writer reads
owner: JL
method: state what Management Science's IS department requires that its UTD-IS siblings do not, and record the vocabulary switch a paper has to make to arrive here

## Opening

MS-IS is the Information Systems department of Management Science, and the pack's own taste file gives this desk its sharpest line. It thinks in mechanisms, equilibria and welfare. It does not think in constructs, theories or implications. That is a claim about words, not topics: a paper can keep its subject here and still have to change every term it uses. So what does a paper have to become?
> ✎ *MS-IS is the Information Systems department of Management Science.* The pack's own taste file gives this desk its sharpest ~line. MS-IS~ *line: it* thinks in mechanisms, equilibria, and welfare, not in constructs, theories, and implications. That is a ~vocabulary~ claim ~rather than a topic one.~ *about words, not about topics. A paper can keep its subject and still have to change every term it uses.* So what does a paper have to become? · CC · 260802 1538
> ✎ MS-IS is the Information Systems department of Management ~Science. The~ *Science, and the* pack's own taste file gives this desk its sharpest ~line: it~ *line. It* thinks in mechanisms, ~equilibria,~ *equilibria* and ~welfare,~ *welfare. It does* not *think* in constructs, ~theories, and~ *theories or* implications. That is a claim about words, not ~about topics. A~ *topics: a* paper can keep its subject *here* and still have to change every term it uses. So what does a paper have to become? · CC · 260802 1545

**How to read this page**: everything here is a REFERENCE, not a rulebook.
The arcs, budgets, moves and refusals below describe what published Management Science papers do, measured from the exemplars on disk.
A paper that departs from them is off-pattern, which is a thing to do on purpose and not a violation.
One figure is different: `Submission-Rules` carries the desk's own published rules, and a manuscript that breaks one of those is returned unreviewed.
Every length on the page says which of the two it is.

**The six words in the question**: a mechanism is the economic story of how one thing moves another, and `5` carries the pack's own list of the names it wants used, switching costs and adverse selection among them.
An equilibrium is where that story settles, once no agent wants to move again.
Welfare is who ended up better or worse off, counted as surplus.
Those three are what this desk asks for.
The three it refuses are a construct, a named idea from a behavioral theory such as TAM, measured on a survey scale; a theory, the body of work that construct came from; and an implication, a sentence about what the field should think next.
The Glossary at the foot of this page defines these and the rest of the desk's vocabulary.

**Where this page sits**: it is one venue target in `QBv`, one page per desk with no pack layer above it.
This page owns only what is true of `playbook-utd-is/MS-IS/`.

**Why the vocabulary matters more here than anywhere else in the tree**: this desk explicitly warns against IS-insider jargon, because Management Science readers outside IS may not know it.
Every other outlet assumes its own field's vocabulary; this one assumes a wider readership that does not share it.

**What is missing**: nothing records the construct-to-mechanism translation, so it is done from scratch every time.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**A number may appear, and only with its source on the same line**: a word budget, a paragraph count or a citation density belongs here when the `MS-IS/MS-IS-<section>/style.md` line or the exemplar it was measured from is named beside it, so it reads as the pack's measurement rather than as this page's own claim.
An uncited number is a transcription and must come out; a whole style file replayed as prose is one too.
The theory folder is `MS-IS-theory-model/` on disk, which `stages/section-kinds.yml` aliases to the canonical `theory` kind.

**Use this desk's vocabulary when describing this desk**: mechanism, equilibrium, welfare. Writing about MS-IS in construct language reproduces the exact failure it rejects.

✅ `what welfare consequence follows`  ❌ `what the theoretical implications are`

**The contract this page answers to** is `../../board/page-types/haipipe-board-page-for-venue/SKILL.md`, and its reference implementation is `QBv1-misq.md`. Every rule in the block below belongs to that contract, not to this page, so a rule changed here is changed there in the same pass.

```text
  🖼 THREE FIGURES        what each one answers
     ① desk taste         what counts as the contribution · what is desk-rejected · the test
     ② Venue-Structure    which sections, in reading order, and the budget each carries
     ③ Submission-Rules   category and cap · manuscript format · references · system ·
                          anonymity · disclosures · odds, clock, money · the desk's own URLs

  📎 FIVE FILES GROUPS
     ⚙️ Engines           what regenerates this page
     📋 Contracts         the venue-page contract, and the base it extends ·
                          a loadable spec is a Contract and never an Engine
     📥 Input files       the pack files this page reads
     🔗 Authority         what the DESK publishes, read directly and never through the pack ·
                          opens with a provenance line · holds every desk-versus-pack clash
     📤 Generated         what a tool WRITES into this page, between markers

  📖 A VENUE PAGE IS A REFERENCE, NOT A RULEBOOK (JL 260803)
     the pack-derived arcs, budgets, moves and refusals are suggestions
     drawn from published papers · only the desk's own published rules bind,
     and they live in the Submission-Rules figure and the Authority group
     write "the pack refuses X" rather than "do not do X", so the page never
     sounds like it is the one doing the refusing

  ⚖️ EVERY LENGTH SAYS WHOSE IT IS (JL 260803)
     a DESK RULE is published by the venue and binding · a PACK OBSERVATION is
     a measurement of papers the pack read, and breaking it is off-pattern
     rather than a violation · a budget printed with neither label reads as a
     rule, which is how three abstract ranges in one style file were being read

  🔢 A SECTION DIVISION CARRIES ITS Sec- INDEX (JL 260803)
     ### 3 · Sec-0-Abstract: one prose paragraph with five hidden beats
         ▲       ▲
         │       └── Sec-<n>, counting from 0, so the index IS the number of
         │           the S-Main page it becomes · the appendix takes Sec-A
         └── the Content division number, which counts §1 and §2 as well
     ### A3 · 📏 Sec-0-Abstract: one prose paragraph with five hidden beats
              ▲  the emoji lives HERE and on the division's closing line,
                 never on the division heading: check.py strips it from an
                 Aims group name and not from a division, so a heading-side
                 emoji reads as group-name-drift on every section at once
     🔢 the index counts from ZERO, not one, and the `Sec-` prefix is what
        makes that readable: a bare `0-Abstract` looks like a typo, and a
        1-based index would sit one off the S-Main page forever
     🔤 only the appendix takes a letter, because this venue letters its own
        Online Appendix sections A, B, C and Sec-A matches them
```

## Diagram

**A formal result, or an identified effect with an economic reading**: and no third option.

```text
  📈 WHAT COUNTS
     a formal model characterizing an EQUILIBRIUM
     a specified MECHANISM
     a recovered STRUCTURAL PRIMITIVE
     an identified causal effect with a WELFARE reading

  🧮 THE APPARATUS
     numbered Propositions / Theorems with proofs
     comparative statics
     welfare analysis
     managerial implications derived FROM the results,
       never asserted beside them

  ❌ DESK-REJECT
     behavioral / survey work with no formal grounding
     IS-insider jargon (TAM, UTAUT) with no economic reading
     empirical work with no structural interpretation
       ── reduced form is OK, but it must speak to a mechanism
     a pure ML/AI method paper with no economic question

  🎯 THE TEST
     "What economic mechanism or equilibrium does this paper
      characterize, and what is the welfare consequence?"

  📊 10 exemplars · the most economics-adjacent of the three
     IS outlets in this pack
```

**Venue-Structure**: the sections an MS-IS paper is written in, in reading order, and what each one costs.

```text
  🏗 VENUE-STRUCTURE ── every budget below is stated with its source
     inline in the §3 to §9 division that owns it, and §10 is the desk's own gate

  index                   §    page           words                       what the section owes
  ───────────────────────   ──   ────────────   ─────────────────────────   ────────────────────────────────
  📏 Sec-0-Abstract       §3   S-Main-0       150w target, 100-220w       1 ¶ of prose, five beats and not
                                              observed · ≤250w is the      one of them labelled
                                              DESK's own cap
  🔢 Sec-1-Introduction   §4   S-Main-1       ~1,300-2,500w · 9-13 ¶      the results enumerated with their
                                                                           magnitudes, BEFORE the data arrives
  🧮 Sec-2-Theory         §5   S-Main-2       3,000-5,000w analytical     a numbered Proposition, its
                                              1,500-2,500w empirical       intuition in plain words, and the
                                                with theory                proof at a different address
                                              500-1,000w empirical
                                                with no formal theory
  📐 Sec-3-Methods        §6   S-Main-3       ~1,250-3,000w · 13-22 ¶     the estimating equation as a
                                                                           display, every term defined under
                                                                           it, the identifying assumption said
  📊 Sec-4-Results        §7   S-Main-4       2,000-4,000w incl. tables   the primary result first, carrying a
                                              and figures · robustness     coefficient, a standard error, and a
                                              may add 1,000-2,000w         percentage of the control mean
  ⚖️ Sec-5   §8   S-Main-5       500-2,500w standalone       an action for a named decision
                                              500-1,000w inline            maker, and a welfare statement for
                                              500-1,000w conclusion        a market or platform paper
                                              1,000-2,500w combined
  🗂 Sec-A-Appendix       §9   S-Appendix-A   not recorded in words       3-6 lettered sections, 10-20 tables
                                              main paper 13-16 typeset     and figures, and every proof, so the
                                              pp · the appendix is         body pointer names a letter and
                                              routinely longer             never reads bare

  🔢 THE INDEX AND THE PAGE ARE THE SAME NUMBER   Sec-<n> counts from 0, so
     Sec-3-Methods becomes S-Main-3 and nobody converts anything · § is a third
     number and belongs to this page only: it counts the judgment divisions
     §1 and §2 ahead of the sections, and the desk's own gate at §10

  📏 NO CEILING AT INITIAL SUBMISSION   the desk publishes NO page limit on a
     first submission, only a Department Editor's right to reject a manuscript
     for excessive length · the 47 pp of 25 lines double-spaced, or 32 pp of 33
     lines at 1.5 spacing, binds an INVITED REVISION alone, and the desk states
     that "an online appendix will not count toward the page limit"
     [pubsonline.informs.org submission guidelines, fetched and verified 260802]

  ⚖️ RULE vs OBSERVATION   the 250-word abstract cap is the DESK's, published
     and binding, and it is the ONLY length rule an initial submission has ·
     every word budget in the column above is the PACK's measurement of the
     papers it read, and the desk publishes no per-section limit at all
     a paper over a budget is off-pattern · a paper over the abstract cap has
     broken a published rule at the portal

  ⚠️ THREE PAGE FIGURES THAT DO NOT RECONCILE, and none of them is a cap
     ~35 pp of text          playbook-utd-is/README.md L148, the pack's own
                                          estimate, matching no number the desk states
     13-16 typeset pp        MS-IS-appendix/style.md L89, measured on two
                                          published articles
     47 pp / 32 pp           the desk, and for an INVITED REVISION only
     `9.3` records the first two and states that neither file names its unit

  ✅ AN ONLINE TIER EXISTS, AND THE DESK EXPECTS IT   unlike MISQ, this desk
     directs analytical proofs and data analysis into the electronic companion,
     and rules that its contents "should not be critical for the proper
     evaluation of the paper" · that sentence is the triage test `9` runs

  ➕ A KIND IS A FLOOR, NOT A CEILING
     one kind may spread across several numbered Main pages
     the ORDER does not move: it is this venue's reading order
```

## Content

### 1 · The vocabulary switch is the arrival cost

**Constructs become mechanisms; implications become welfare**: the topic can stay put while the paper changes language entirely.

```text
  🔄 THE TRANSLATION nobody has written down
     a construct        ▶ a mechanism or a primitive
     a hypothesis       ▶ a proposition or a comparative static
     an implication     ▶ a welfare or profit consequence
     significance stars ▶ an economic magnitude

  🚫 AND THE BAN
     TAM, UTAUT, and IS-insider terms carry no meaning to a
     Management Science reader outside IS
     ── the pack says so outright
```

🔄 Establishes the arrival cost as a vocabulary translation. A MISQ paper therefore cannot be resubmitted here unedited.
> ✎ 🔄 Establishes the arrival cost as a vocabulary ~translation, which is why a~ *translation. A* MISQ paper *therefore* cannot be resubmitted here unedited. · CC · 260802 1538

#### 1.1 · Reduced form is permitted and unanchored reduced form is not
(so this is a weaker formal bar than it first reads, with a strict condition)
The desk accepts reduced-form empirics when identification is credible and theory frames the mechanism tightly.
What it refuses is empirical work with no structural interpretation at all, which is a different and lower bar than requiring a formal model.

### 2 · Where it sits against its two siblings

**Three IS outlets, three different things a theory rests on**: this one rests on economics.

```text
  🏛 MISQ   ── one primary theory, any method
  🔬 ISR    ── a named mechanism per hypothesis, identified
  📈 MS-IS  ── an economic micro-foundation, formal or
               credibly identified

  💡 the pack's lean-signal matrix routes here on
     "causal identification, economics framing" and
     "markets, platforms, economic mechanisms"

  ⚠️ and on "computational methods, large-scale data" the
     matrix points at BOTH ISR and MS-IS ── it does not decide
```

📈 Establishes MS-IS's position on the family's shared axis, and names the one matrix row that leaves the choice open.

### 3 · Sec-0-Abstract: one prose paragraph with five hidden beats

**Five beats in order, and not one of them labelled**: the five-label structured abstract in the MS submission guidelines is a typesetting artifact that no published paper carries.

```text
  📏 BUDGET · MS-IS-abstract/style.md
     target                150 w                     "Word budget" L18-23
     range                 100-220 w                 same table, L22
     paragraphs            1, unstructured prose     micro-norms L245-250
     sentences             6-7                       same
     words per sentence    10-49, median ~26         same
     citations             0 in both papers          same
     measured whole        Huesmann 205 w · Feng 130 w        L252

  🧵 THE FIVE BEATS · L25-35
     ① problem / context         1-2 sent
     ② gap / motivation            1 sent
     ③ method + identification   1-2 sent
     ④ key findings              2-4 sent
     ⑤ implication               0-1 sent

  🧩 SLOTS, not sentences to copy
     ① `[Economic agent] face(s) [decision] in [IS context].`     L45
     ③ `We develop a [type] model of [agents] choosing
        [actions] under [information structure].`                 L78
     ④ `We characterize the equilibrium and show that
        [comparative static].`                                    L96
     ④ `We find that [X] increases [Y] by [magnitude] (SE: [Z]).` L95
     ⑤ `Platform designers can improve [welfare] by [change].`    L113

  ❌ ANTI-PATTERNS the pack names
     opening `This paper studies...`                    L50
     a theory named where the problem belongs           L52
     `we find significant effects`, no magnitude        L102
     causality claimed, identification unnamed in ③     L103
     ending on the method, or on `future research`      L118, L120
     the 5-label structured format                      L222-237

  🔤 KEYWORDS  4-6 terms, bullet-dot separated, below the abstract   L155-165
```

📏 Establishes the abstract as a fixed single paragraph whose structure is invisible, so a writer who labels the beats has produced another venue's abstract.

#### 3.1 · Three word ranges live in one style file
(and a draft citing the wrong one is inside the pack and outside the budget)
`MS-IS-abstract/style.md` states 120-220 words under "Format" at L14, 100-220 in its "Word budget" table at L22, and 100-250 in the resolution note at L220.
`MS-IS-abstract/template.md` L28 resolves it to 100-220 and marks that range binding, so the table is the number to cite and the other two are residue.

#### 3.2 · One claim threads the abstract, the introduction and the discussion
(the family rule, from the README whose own page retired)
`playbook-utd-is/README.md` L134-136 states that the single `[primary]` claim drives the abstract's contribution sentence, the introduction's contribution paragraph, and the first Discussion implication.
At this desk that claim is the economic or analytical one, and README L83-86 adds that for market and platform papers it carries a welfare statement rather than firm profit alone.

#### 3.3 · Format values
(the four format metrics for the abstract, each with the style.md line it was read from)

```text
  📏 WORDS            150 w target · 100-220 w range · 1 ¶ · 6-7 sentences ·
                        10-49 w/sentence, median ~26
                        [MS-IS-abstract/style.md "Word budget" L22 · micro-norms L247-249]
  📚 CITATION DENSITY 0 per sentence · both measured abstracts carry no citation at all
                        [MS-IS-abstract/style.md micro-norms L250]
  🔢 VALUE DENSITY    not recorded by the pack
                        [the numeric result sentences at L143-153 are quoted one at a time
                         and never counted against sentences]
  📊 DISPLAYS         not recorded by the pack
                        [L155-172 names the Keywords line and the History / Funding /
                         Supplemental block, and the file counts no float]
```

#### 3.4 · The language, in the papers' own words
(five sentences the abstract style file quotes with a paper's name attached, one move each)

"Do pharmacy benefit managers (PBMs) reduce spending on prescription drugs?" [Feng 2025].
Beat ① written as a bare question, which is the `[Economic agent] face(s) [decision] in [IS context]` slot turned inside out: the market's open question stands in for the agent's decision.
"Although relative performance feedback in the form of rankings appears to be effective ... it may have either motivating or demotivating effects" [Huesmann 2025].
Beats ① and ② fused into one sentence, so the phenomenon and the unresolved tension arrive together rather than in the two slots the figure lists.
"our analysis reveals a 26.08% increase (standard error: 10.3%) in completed tasks among developers using the AI tool" [Cui 2025].
Beat ④ filling the `We find that [X] increases [Y] by [magnitude] (SE: [Z])` slot exactly, and the sentence the anti-pattern `we find significant effects` is written against.
"PBMs reduce overall spending by 28%, without greatly limiting patient access" [Feng 2025].
Beat ④ for a counterfactual paper, where the magnitude is a simulated quantity rather than an estimate and the trailing clause carries the welfare reading.
"The new GPT method achieves an accuracy of 96% and reduces the non-answer error rate by 70%" [de Kok 2025].
Beat ④ for a method paper, whose primary result is a performance number rather than an effect.
> ✎ Beat ④ for a method paper, whose primary result is a performance number rather than an ~effect, which is why the~ *effect. The* slot list holds no shape for ~it.~ *that.* · CC · 260802 1545
The slot list holds no shape for that.

### 4 · Sec-1-Introduction: every result previewed before the data arrives

**Enumerated findings with magnitudes, one per paragraph**: the pack calls this the single most distinctive MS move against its two siblings.

```text
  📏 BUDGET · MS-IS-introduction/style.md
     range                 ~1,300-2,500 w             "Word budget" L8-15
     paragraphs            9-13                       micro-norms L328
     sentences per ¶       3-13, median ~6            L329
     words per sentence    6-58, median ~22           L330
     citations             12-22 per introduction     L331
     density               ~0.2-0.3 per sentence, CLUSTERED at the edges
     measured whole        Huesmann ~1,330 w · Feng ~1,505 w   L333

  🌀 THE FUNNEL · L17-53
     P1-P2  phenomenon + stakes, 3-6 foundational cites
     P3     gap, as an unresolved ECONOMIC question
     P4     this paper: data + method + identification, crisp
     P5-P8  ENUMERATED RESULTS, one finding per ¶, with magnitude
     P9-P10 contribution as literature-STREAM positioning
     P11    roadmap, optional, and only AFTER the results

  🧩 SLOTS, not sentences to copy
     P3 `Uncertainty over [consequence] reflects a lack of
         [evidence type].`                                  L102
     P4 `We exploit [identification strategy] using [data
         covering scope].`                                  L110
     P5 `We report [N] main results. First, ...`            L61
     P5 `Our preferred estimates suggest that [treatment]
         causes a [magnitude] [direction] in [outcome].`    L113
     P9 `We contribute to the literature on [X] by
         [providing the first / identifying / characterizing].`  L117

  🧭 VARIANT OPENINGS the pack measured
     healthcare      clinical terms first, DOLLAR stakes   L189-214, L256-263
     structural      an apparent contradiction in the data
                     motivates the model                    L234-244
     methodological  the method problem stated at once,
                     then `we prove consistency and
                     asymptotic normality`                  L246-254

  ❌ ANTI-PATTERNS the pack names
     vague importance with no economic stake         L125-127
     IS-insider jargon: TAM, UTAUT                   L127-129
     hypotheses in the introduction                  L130-133
     a roadmap placed BEFORE the results             L134-135
```

🔢 Establishes the introduction as the place where the paper's punchlines are spent rather than saved. An MISQ introduction cannot be reused here.
> ✎ 🔢 Establishes the introduction as the place where the paper's punchlines are spent rather than ~saved, which is why an~ *saved. An* MISQ introduction cannot be reused here. · CC · 260802 1538

#### 4.1 · The stated paragraph count and the measured one disagree
(7-12 is written at the top of the file; 9-13 is what the two measured papers run)
`MS-IS-introduction/style.md` L3 says 7-12 paragraphs, while its own micro-norms at L328 measure 9 in Huesmann 2025 and 13 in Feng 2025.
`MS-IS-introduction/template.md` L27 adopts 9-13, so the measured pair is the number a draft is checked against.

#### 4.2 · The no-lit-review rule is corrected inside its own file
(the accurate ban is on one exact section title, not on the section)
The anti-pattern at L122-124 and the contrast row at L143 both say MS-IS has no separate literature review, and L216-231 calls that overstated after counting four of eight papers that carry one.
The accurate rule the correction states: no section titled exactly "Related Work", while "Literature and Hypotheses", "Background", "Literature Review" and "Theoretical Background" are frequent and serve the same function.

#### 4.3 · Format values
(the four format metrics for the introduction, and the two the pack never took)

```text
  📏 WORDS            ~1,300-2,500 w · 9-13 ¶ · 3-13 sentences/¶, median ~6 ·
                        6-58 w/sentence, median ~22
                        [MS-IS-introduction/style.md "Word budget" L8-15 · micro-norms L328-330]
  📚 CITATION DENSITY ~0.2-0.3 per sentence · 12-22 cites per introduction, clustered at the
                        edges, with the middle walk-through paragraphs nearly cite-free
                        [MS-IS-introduction/style.md micro-norms L331]
  🔢 VALUE DENSITY    not recorded by the pack
                        [the dollar-stake sentences at L257-263 and the magnitude slots at
                         L112-113 are quoted, and no file counts them against sentences]
  📊 DISPLAYS         not recorded by the pack
                        [MS-IS-introduction/style.md names no figure and no table for this
                         section, and takes no float count]
```

#### 4.4 · The language, in the papers' own words
(six sentences the introduction style file quotes with a paper's name attached, one move each)

"We report six main results." [Bick et al. 2026].
The enumerated-results announcement, which opens the P5-P8 block on this division's figure and commits the writer to one magnitude-bearing paragraph per result.
"Uncertainty over the impact of genAI on the economy in part reflects a lack of systematic evidence" [Bick et al. 2026].
The P3 gap written as an unresolved economic question, filling the `Uncertainty over [consequence] reflects a lack of [evidence type]` slot rather than the `little is known about X` shape the pack bans.
"Our preferred estimates ... suggest that usage of the coding assistant causes a 26.08% increase (SE: 10.3%)" [Cui 2025].
A P5 result carrying its standard error inside the introduction, which is the move that makes an MISQ introduction unusable here.
"prescription drugs now account for 15%-17% of total healthcare expenditures, with 72% attributed to brand name drugs" [Chao/Larkin 2022].
The P1-P2 stake stated as a share of spending, which is the healthcare variant opening the figure records at L189-214.
"These two findings are hard to reconcile" [Feng 2025].
The structural variant opening, where an apparent contradiction in the data is the motivation for building a model rather than for running another regression.
"More generally, we contribute to the literature studying the productivity and on-the-job performance of software developers" [Cui 2025].
The P9-P10 contribution written as literature-stream positioning, filling the `We contribute to the literature on [X] by [Y]` slot.

Bick et al. is quoted twice by `MS-IS-introduction/style.md` at L61-74, and it is not one of the ten PDFs on disk.
> ✎ Bick et al. is quoted twice by `MS-IS-introduction/style.md` at ~L61-74~ *L61-74,* and *it* is not one of the ten PDFs on ~disk, so~ *disk. So* the pack's two sharpest introduction quotations come from a paper it does not store. · CC · 260802 1538
So the pack's two sharpest introduction quotations come from a paper it does not store.

### 5 · Sec-2-Theory: the model section, where a Proposition lives and its proof does not

**Numbered statement, then the intuition in plain language, then the proof elsewhere**: MS-IS carries the formal apparatus here and relegates its verification.

```text
  📏 BUDGET BY PAPER TYPE · MS-IS-theory-model/style.md L18-22
     analytical                    3,000-5,000 w
     empirical with theory         1,500-2,500 w
     empirical, no formal theory     500-1,000 w   institutional background only
     paragraphs                    13-14 prose ¶          micro-norms L414
     sentences per ¶               1-11, median ~3 (Feng model prose)
                                          median ~6 (Huesmann lit + hypotheses)   L415
     words per sentence            6-56, median ~22       L416
     citations                     1 (Feng) vs 44 (Huesmann, ~0.6/sent)   L417
     stated density                ~0.40-0.50 per sentence                L147-149
     measured whole                Feng §4 ~1,030 w prose-only · Huesmann §2 ~1,870 w   L419-420

  🧮 THE ANALYTICAL ARC · L26-51
     2.1  SETUP        agents · decision variables · information
                       structure · timing · every assumption justified
     2.2  BENCHMARK    the frictionless case, as a Lemma or Proposition,
                       to anchor the WELFARE comparison
     2.3  MAIN MODEL   the friction, the equilibrium, a numbered
                       Proposition or Theorem, plus COMPARATIVE STATICS
     2.4  EXTENSIONS   one relaxed assumption each, one Proposition each,
                       plus consumer / producer / total surplus
     2.5  PREDICTIONS  the propositions translated, for a hybrid paper

  🧩 SLOTS, not sentences to copy
     `**Proposition 1.** In the unique symmetric equilibrium, the
      platform's optimal commission rate r* is [expression].
      Moreover, dr*/d[parameter] > 0.`                          L93-94
     `*Intuition.* When [parameter] increases, [economic logic],
      leading the platform to [action].`                        L96-97
     `**Proposition 3** (Welfare). Total welfare under [regime]
      exceeds [benchmark] if and only if [condition].`          L108-110
     `We assume X because [economic reason]; this is standard
      in [cite].`                                               L129-131
     4-STEP per mechanism: name it · cite it exists · argue it
      applies HERE · state the prediction                       L133-146

  🔁 THE MECHANISM TRANSLATION TABLE · L113-126
     use  switching costs        not  lock-in, path dependency
     use  information asymmetry  not  information gap
     use  complementarity        not  synergy
     use  adverse selection      not  market for lemons
     use  search costs           not  search friction

  📄 WHERE THE PROOF GOES
     short proof     the body                            L100
     long proof      the Online Appendix, with the note
                     `All proofs are in the Online Appendix.`   L100-101

  ❌ ANTI-PATTERNS the pack names
     `Drawing on TAM, we argue...`                  L153-155
     an undifferentiated H1-H8 list, which reads as fishing   L156-157
     measurement method here: the theory takes the construct as given   L158-159
     a tautological hypothesis                      L160-161
     `we assume for simplicity` with no economic reason       L162-163
```

🧮 Establishes the theory section as this desk's load-bearing one, and fixes the proof at a different address from the result it proves.

#### 5.1 · The Proposition apparatus has no exemplar behind it
(the desk is named for formal results and the pack stores none)
The Proposition, Theorem and welfare-Proposition phrasing at L88-111 is written as a pattern, and the enrichment need at L178-180 that asked for an analytical exemplar was closed with Feng 2025.
Feng's arc at L270-297 is a structural model: numbered equations and a Bellman equation, with no Proposition anywhere in it.
> ✎ Feng's arc at L270-297 is a structural ~model of~ *model:* numbered equations and a Bellman ~equation~ *equation,* with no Proposition anywhere in ~it, so~ *it. So* none of the eight papers the pack mined shows what this desk's most distinctive apparatus actually reads like. · CC · 260802 1538
So none of the eight papers the pack mined shows what this desk's most distinctive apparatus actually reads like.
Two of the ten PDFs on disk are named by no `style.md` at all, so the gap may be smaller than it looks and nobody has checked.

#### 5.2 · The analytical budget is stated and never measured
(3,000-5,000 words is the only budget in the pack with no measurement under it)
Feng's section 4 measures ~1,030 prose words because display equations and notation are excluded by extraction, which L419 declares a measurement artifact rather than a clash.
The consequence is that the analytical range at L20 rests on no counted section, while every other budget in this pack was reconciled against one.

#### 5.3 · Format values
(the four format metrics for the model section, plus the formal objects the pack names and never counts)

```text
  📏 WORDS            analytical 3,000-5,000 w · empirical with theory 1,500-2,500 w ·
                        empirical without formal theory 500-1,000 w
                        [MS-IS-theory-model/style.md "Word budget" L20-22]
                      13-14 prose ¶ · 1-11 sentences/¶, median ~3 in Feng and ~6 in Huesmann ·
                        6-56 w/sentence, median ~22                [micro-norms L414-416]
  📚 CITATION DENSITY stated ~0.40-0.50 per sentence · measured 1 cite in Feng against 44 in
                        Huesmann, ~0.6 per sentence
                        [MS-IS-theory-model/style.md L147-149 · micro-norms L417]
  🔢 VALUE DENSITY    not recorded by the pack
                        [no numeric-per-sentence figure anywhere in MS-IS-theory-model/style.md]
  📊 DISPLAYS         not counted, named by exemplar only: a model-summary figure in Feng's
                        arc at L280 and a positioning comparison table in Chen's arc at L354-356
                      numbered Propositions and Theorems are NOT counted objects: required at
                        L40, phrased at L89-98 and L108-111, with no count and no instance
                      display equations are NOT counted objects: Feng's numbered equations 3,
                        4, 5, 8 and 10 are named at L279-289, and L419 excludes them from the
                        one word measurement the section has
```

#### 5.4 · The language, in the papers' own words
(five formal statements the model style file quotes with a paper's name attached, and the one apparatus that carries none)

"The combination of human and AI information processing, all else equal, increases decision performance." [Krakowski 2026].
The bare numbered hypothesis, this desk's minimum formal statement, stated in operational terms rather than in an IS construct.
"For individuals who cannot reach outcomes above the new threshold, effort decreases." [Huesmann 2025].
A lettered sub-part of a hypothesis, and the nearest attested thing to the comparative static the figure asks for: one parameter moves and one outcome moves with it.
"Let Z-tilde = sigma_X * Z - lambda * sigma_Z * X-hat, then Cov(Z-tilde, u) = 0." [Burtch 2026].
A numbered Lemma that carries its source in the label.
> ✎ A numbered Lemma ~carrying~ *that carries* its ~provenance~ *source* in the ~label, which~ *label. That* is how a methodological paper imports a formal result instead of proving it here. · CC · 260802 1538
That is how a methodological paper imports a formal result instead of proving it here.
"E[epsilon | X, W] = 0" [Burtch 2026].
A numbered Assumption set as a display object, the shape the slot list calls `We assume X because [economic reason]` once the reason moves to the prose below it.
"This assumption is undesirable, but necessary because of data limitations and to make estimation feasible." [Feng 2025].
The assumption justified against the pack's own anti-pattern `we assume for simplicity`, and justified by honesty rather than by economics.

The Proposition block, its `*Intuition.*` readback and the welfare Proposition at L93-98 and L108-111 carry bracketed placeholders and no paper's name, so the apparatus this division is named for is the one thing here nobody has quoted, which is what `5.1` records.

### 6 · Sec-3-Methods: the estimating equation is a display and every term is defined under it

**The identification strategy is an economic argument, not a technique**: naming the estimator is the cheap half, and the pack asks for the other half.

```text
  📏 BUDGET · MS-IS-methods/style.md
     range                 ~1,250-3,000 w             "Word budget" L18-24
     paragraphs            13 (Huesmann) - 22 (Feng)  micro-norms L457
     sentences per ¶       3-7, median ~4-6           L458
     words per sentence    8-61, median ~20           L459
     citations             4-6 per section            L460
     density               ~0.06 per sentence, ISOLATED, never clustered
     measured whole        Huesmann ~1,250 w · Feng ~2,560 w   L462

  📐 THE DEFAULT ARC · natural experiment / IV / DiD · L49-68
     3.1  data source · coverage · restrictions · summary statistics
     3.2  key variables, each with its ECONOMIC interpretation
     4.1  the variation exploited, and why it is plausibly exogenous
     4.2  threats and robustness, one concern at a time

  🧩 SLOTS, not sentences to copy
     `y_it = beta * D_it + mu_i + gamma_t + epsilon_it   (1)
      Here, beta is the coefficient of interest, D_it is ...`   L90-94
     `where:` block, one Greek letter per line, for a complex
      specification                                             L296-315
     `One may argue that [X is endogenous] because [reason].
      To address this concern, we [strategy]. [Table N] shows
      that [result].`                                           L107-109
     `standard errors are robust and clustered by [level]`      L402-412

  🧾 WHAT THE SECTION OWES, per the pack
     the estimator by its economic name: 2SLS · MLE · GMM       L139-140
     the identifying assumption stated, never implied:
       exclusion restriction (IV) · parallel trends (DiD)       L149-150
     the first-stage F in the body or a table footnote, F > 10  L116, L147-148
     the clustering level, justified when it is not obvious     L409-412
     four-layer inference when clusters are few: clustered SE,
       WCR bootstrap, jackknifed wild bootstrap, RI p-value     L414-426

  ❌ ANTI-PATTERNS the pack names
     `we use [Stata/R/Python] to estimate`             L139-140
     a method with no economic motivation              L141-143
     causal language on an observational design        L144-146
     an unreported first stage                         L147-148
     a buried identifying assumption                   L149-150
```

📐 Establishes the methods section as the place where the design is argued rather than announced, which is the difference the pack draws against a statistics section.

#### 6.1 · Threats are written in the referee's voice
(the concern is stated as an attack before it is answered)
L104-109 asks each endogeneity concern to be named as if a referee raised it, then addressed with a named strategy and a named check.
The move costs a sentence and buys the referee's own objection back in the author's wording.
> ✎ The move costs a sentence and buys the referee's own objection back in the author's ~wording, which is why the~ *wording. The* pack records it as a signature rather than a courtesy. · CC · 260802 1545
The pack records it as a signature rather than a courtesy.

#### 6.2 · Heavy machinery leaves the body by rule
(proofs, extended robustness, instrument construction and variable definitions)
L118-121 sends all four to the Online Appendix and asks the body to signpost with a section letter, and division 9 carries the address scheme that signpost has to use.
The body's job at this desk is to stay readable, not to stay complete.

#### 6.3 · Format values
(the four format metrics for the methods section, with the displays the pack calls standard)

```text
  📏 WORDS            ~1,250-3,000 w · 13 ¶ in Huesmann to 22 ¶ in Feng ·
                        3-7 sentences/¶, median ~4-6 · 8-61 w/sentence, median ~20
                        [MS-IS-methods/style.md "Word budget" L20-24 · micro-norms L457-459]
  📚 CITATION DENSITY ~0.06 per sentence · 4-6 cites per section, isolated method-precedent
                        cites, never clustered      [MS-IS-methods/style.md micro-norms L460]
  🔢 VALUE DENSITY    not recorded by the pack
                        [the balance and summary tables at L363-400 hold the numbers, and no
                         file counts numbers in the prose]
  📊 DISPLAYS         not counted, named as standard: summary statistics, balance, and first
                        stage with F > 10                                             [L111-116]
                      named by exemplar: Cui Table 2, Krakowski Table 3, Chao/Larkin Table 3
                        and Feng Table 1 at L363-400, plus a four-panel sensitivity figure
                        at L358-361
```

#### 6.4 · The language, in the papers' own words
(five sentences the methods style file quotes with a paper's name attached, one move each)

"Here, beta is the coefficient of interest, D_it is an adoption dummy that turns on after a developer first uses GitHub Copilot" [Cui 2025].
Every term defined in the sentence immediately under the display equation, which is the slot at L90-94 written out in full rather than deferred to a `where:` block.
"We exploit the experimental variation and address imperfect compliance by using assignment to treatment as an instrument for GitHub Copilot adoption." [Cui 2025].
The identification stated as an economic argument about who complies, not as the name of an estimator.
> ✎ The identification stated as an economic argument about who complies, not as the name of an ~estimator, which~ *estimator. That* is the difference this division draws against a statistics section. · CC · 260802 1538
That is the difference this division draws against a statistics section.
"We assumed a medium effect size (Cohen's d = 0.4), a conventional power of 0.8, and a statistical significance level of alpha = 0.05" [Huesmann 2025].
The a priori power analysis, an experiment-only obligation the arc lists at L206-211 and the figure's four owed items do not cover.
"We drop all branded drugs where a generic version was introduced in the middle of this time period" [Chao/Larkin 2022].
One exclusion stated with the reason it was made, the shape the data arc at L264-268 asks for once per rule rather than as a single sample-construction paragraph.
"we only have five states in the data and clustering over so few states could lead to bias" [Chao/Larkin 2022].
The clustering level justified rather than announced, which is the owed item at L409-412 and the reason the four-layer inference ladder exists at all.

The referee-voice threat pattern this division records at `6.1` is written at L107-109 with bracketed placeholders and no paper's name.
> ✎ The referee-voice threat pattern this division records at `6.1` is written at L107-109 with bracketed placeholders and no paper's ~name, so~ *name. So* the signature move has a shape and no worked sentence. · CC · 260802 1538
So the signature move has a shape and no worked sentence.

### 7 · Sec-4-Results: ordered by identification, never by hypothesis

**The primary result leads, with a coefficient, a standard error and a percentage of the control mean**: nothing warms up in front of it.

```text
  📏 BUDGET · MS-IS-results/style.md
     range                 2,000-4,000 w, tables and figures included   L18-22
     robustness            may add 1,000-2,000 w, usually to the appendix
     paragraphs            12 (Feng) - 16 (Huesmann)  micro-norms L423
     sentences per ¶       3-9, median ~5             L424
     words per sentence    6-53, median ~21           L425
     citations             0 (Huesmann) - 3 (Feng), ~0.05 per sentence   L426
     measured prose        Huesmann ~1,890 w · Feng ~1,515 w   L428

  📊 THE ARC, BY PAPER TYPE · L26-64, L199-208
     empirical      primary outcome · secondary outcomes · INLINE
                    Discussion · standalone Heterogeneity · robustness
     DiD            statistical method · progressively richer FE columns ·
                    pretrends event study · robustness · mechanisms   L210-248
     lab            nonparametric tests FIRST, then parametric OLS;
                    formal **Result** blocks mirroring the hypotheses   L250-275
     analytical     equilibrium characterization · COMPARATIVE STATICS
                    as numbered Corollaries · WELFARE · extensions      L50-64
     structural     one subsection per counterfactual scenario          L311-331

  🧩 SLOTS, not sentences to copy
     `We present our results in Table N.`                        L142
     `...increases by 26.08% (SE: 10.3%)...`                     L74-76
     `we express coefficients as percentage effects by dividing
      each by the pre-treatment mean in the control group`       L82-83
     `This corresponds to approximately [N] additional [units]
      per [period].`                                             L96-98
     `In Online Appendix [X], we show that [result] is robust
      to [alternative specification].`                           L112-114

  ⚖ WHERE THE FORMAL RESULT LANDS
     equilibrium     a Proposition, restated with its intuition   L54-55
     comparative statics   a numbered Corollary, or a part of a Proposition   L56-58
     welfare         consumer surplus · producer surplus · total,
                     compared ACROSS REGIMES                      L59-61

  ❌ ANTI-PATTERNS the pack names
     a result with no table reference               L153-154
     `we find a significant effect`                 L155-156
     causal language the design cannot carry        L157-158
     a buried null: MS referees respect honest nulls   L159-161
     LATE-versus-ATE argued in the results ¶ instead of the inline
       Discussion                                   L162-164
     robustness presented as new results            L165-166
```

📊 Establishes the results section as ordered by what identifies the estimate. A draft ordered by hypothesis reads as the wrong venue before a single number is checked.
> ✎ 📊 Establishes the results section as ordered by what identifies the ~estimate, which is why a hypothesis-ordered~ *estimate. A* draft *ordered by hypothesis* reads as the wrong venue before a single number is checked. · CC · 260802 1538

#### 7.1 · An inline Discussion sits inside Results and is not the Discussion
(two sections carry the word, and they answer different questions)
L85-93 puts a 2-4 paragraph Discussion inside or immediately after the main results, and it addresses identification limits alone: LATE against ATE, external validity, the threats.
The final section then translates into action, so a draft that argues LATE at the end has answered the reader two sections too late.

#### 7.2 · Heterogeneity is a section, not a robustness footnote
(the desk asks where the effect is strongest, not only whether it exists)
L100-108 records MS papers raising heterogeneity to a standalone section, with one table panel per subgroup.
> ✎ L100-108 records MS papers ~elevating~ *raising* heterogeneity to a standalone ~section~ *section,* with one table panel per ~subgroup, and the~ *subgroup. The* contrast row at L176 sets that against moderation hypotheses at MISQ and post-hoc analysis at ISR. · CC · 260802 1538
The contrast row at L176 sets that against moderation hypotheses at MISQ and post-hoc analysis at ISR.
Reading heterogeneity as robustness demotes the one analysis this desk treats as a finding.

#### 7.3 · Format values
(the four format metrics for the results section, plus the formal objects it prescribes and never counts)

```text
  📏 WORDS            2,000-4,000 w including tables and figures, robustness may add
                        1,000-2,000 w · 12 ¶ in Feng to 16 ¶ in Huesmann ·
                        3-9 sentences/¶, median ~5 · 6-53 w/sentence, median ~21
                        [MS-IS-results/style.md "Word budget" L18-22 · micro-norms L423-425]
  📚 CITATION DENSITY ~0.05 per sentence at most · 0 cites in Huesmann to 3 in Feng, prose
                        essentially citation-free   [MS-IS-results/style.md micro-norms L426]
  🔢 VALUE DENSITY    not recorded by the pack
                        [this is the most number-bearing section kind in the tree and no file
                         counts its numbers; L74-76 and L96-98 quote them one at a time]
  📊 DISPLAYS         not counted, conventions only: one table per major result L119, stars
                        and parenthesised standard errors L122-123, and event-study,
                        adoption-curve, histogram and comparative-static figures L132-136
                      numbered Corollaries and Propositions are NOT counted objects:
                        prescribed for the analytical arc at L50-64 and for comparative
                        statics at L56-58, with no count and no measured instance
                      display equations are not recorded for this section at all
```

#### 7.4 · The language, in the papers' own words
(five sentences the results style file quotes with a paper's name attached, and the formal result that carries none)

"on average, the number of weekly pull requests made by developers increases by 26.08% (SE: 10.3%)" [Cui 2025].
The primary result leading its section with a coefficient and a standard error, the move the figure's `We present our results in Table N` slot introduces and this one completes.
"we express coefficients as percentage effects by dividing each by the pre-treatment mean in the control group" [Cui 2025].
The convention of dividing by the control mean, stated in the prose rather than left in a table note.
> ✎ The ~percentage-of-control-mean~ convention *of dividing by the control mean,* stated in the prose rather than left in a table ~note, which~ *note. That* is what makes magnitudes comparable across outcomes. · CC · 260802 1538
That is what makes magnitudes comparable across outcomes.
"A subject's effort level depends on the ranking system design and on the subject's ability type." [Huesmann 2025].
A numbered `Result` block in the body, the only formal numbered statement any stored paper carries in a results section, and the lab-paper stand-in for a Proposition.
"We find that the total cost of statins would increase by almost 50%." [Feng 2025].
The counterfactual as the structural paper's result, which is where a comparative static actually lands when the model is estimated rather than solved.
"due to imperfect compliance, we rely on instrumental variables (IV) estimation, which identifies a LATE" [Cui 2025].
The inline Discussion opening, arguing what the design can and cannot identify inside Results, which is the split `7.1` records against the final section.

No welfare sentence and no numbered Corollary is quoted from any paper in this file.
> ✎ No welfare sentence and no numbered Corollary is quoted from any paper in this ~file: the~ *file. The* welfare arc at L59-61 and the Corollary instruction at L56-58 are ~prescriptions, so~ *prescriptions. So* the analytical half of this division rests on nothing measured. · CC · 260802 1538
The welfare arc at L59-61 and the Corollary instruction at L56-58 are prescriptions.
So the analytical half of this division rests on nothing measured.

### 8 · Sec-5-Discussion: results become an action, and a market paper states the welfare

**Not what the paper found, but what a decision-maker should do about it**: and for a market or platform paper, what happened to surplus.

```text
  📏 BUDGET · MS-IS-discussion/style.md L17-24
     inline Discussion, inside Results     500-1,000 w · 2-4 ¶
     standalone Discussion                 500-2,500 w
     final Conclusion                      500-1,000 w · 2-4 ¶
       and as short as 2 ¶ / ~220 w        Huesmann "Concluding Remarks", L22
     combined, if one section              1,000-2,500 w
     paragraphs            3 (Feng) - 9 (Huesmann)     micro-norms L444
     sentences per ¶       3-7, median ~6              L445
     words per sentence    6-57, median ~26, the LONGEST of any section   L446
     citations             1 (Feng) - 10 (Huesmann), ~0.06-0.2 per sentence   L447
     limitation ¶          cite-free                   L447
     measured whole        Huesmann §5+§6 ~1,320 w · Feng §7 ~455 w   L449

  ⚖ THE ARC, SINGLE-SECTION ANALYTICAL · L63-82
     P1  restate the contribution
     P2  the main insight in plain language, for a non-specialist
     P3  implications derived FROM the formal result
     P4  WELFARE statement, for a market or platform paper
     P5  limitations, 2-3 sentences, frank and specific
     P6  future directions, 1-2 sentences, one concrete question

  🧩 SLOTS, not sentences to copy
     `We have [modelled / identified / characterized] [X] and
      shown that [Y].`                                          L136
     `Proposition 2 implies that firms should ...`              L71-74
     `Our analysis shows that [policy/design] increases
      [consumer surplus / total welfare] by [mechanism], while
      [producer surplus] [increases/decreases]. On net,
      [total welfare is higher/lower].`                         L110-112
     `Our estimates are [specific limitation]. To the extent
      that [condition], our results may [overstate/understate]
      the true effect.`                                         L145-146
     `An important question for future research is whether
      [specific question].`                                     L150

  🧱 THREE SHAPES THE PACK MEASURED · L201-212
     Huesmann     "Implications and Discussion" then "Concluding Remarks"
     Chao/Larkin  Summary · Limitations · Managerial Implications
     Krakowski    Contributions · Future Research · Practical Implications,
                  with NO concluding section at all

  ❌ ANTI-PATTERNS the pack names
     walking through H1-H6 again                    L155-156
     `important implications for IS research and practice`   L157-158
     a future-work laundry list                     L159-160
     `causes` in the Discussion where Results said `association`   L161-162
     deep literature re-engagement, which is the MISQ move   L163-165
     a market or platform paper with NO welfare statement    L166-168
```

⚖️ Establishes the discussion as the shortest action-bearing section in the family, and the one place a welfare consequence is not optional.

#### 8.1 · The welfare requirement is stated and unexemplified
(required at L166-168, and absent from every stored paper)
The contrast row at L178 marks the welfare statement required at MS-IS and not expected at MISQ or ISR, and the pattern at L110-112 gives its wording.
Feng 2025 is the nearest market paper the pack mined, and it reports counterfactual spending changes rather than consumer surplus.
> ✎ Feng ~2025,~ *2025 is* the nearest market paper the pack mined, *and it* reports counterfactual spending changes rather than consumer ~surplus, so~ *surplus. So* the requirement has a rule, a slot, and no worked example. · CC · 260802 1538
So the requirement has a rule, a slot, and no worked example.

#### 8.2 · Two discussion budgets, and only one was revised
(500-1,500 in the contrast table, 500-2,500 everywhere else)
L426-430 revises the range up to 500-2,500 after Chao/Larkin's four-page discussion of alternative mechanisms, and L20-21 carries the revision.
The contrast row at L174 still reads 500-1,500, and `MS-IS-discussion/template.md` L23 follows the revised number, so the contrast table is the stale one.

#### 8.3 · Format values
(the four format metrics for the discussion, where two of the four are simply absent)

```text
  📏 WORDS            inline Discussion 500-1,000 w / 2-4 ¶ · standalone Discussion
                        500-2,500 w · final Conclusion 500-1,000 w / 2-4 ¶, measured as short
                        as 2 ¶ and ~220 w · combined 1,000-2,500 w
                        [MS-IS-discussion/style.md "Word budget" L19-24]
                      3 ¶ in Feng to 9 ¶ in Huesmann · 3-7 sentences/¶, median ~6 ·
                        6-57 w/sentence, median ~26, the longest of any section
                        [micro-norms L444-446]
  📚 CITATION DENSITY ~0.06-0.2 per sentence · 1 cite in Feng to 10 in Huesmann, clustered in
                        the counterargument paragraph, limitation paragraphs cite-free
                        [MS-IS-discussion/style.md micro-norms L447]
  🔢 VALUE DENSITY    not recorded by the pack
                        [no numeric-per-sentence figure in MS-IS-discussion/style.md]
  📊 DISPLAYS         not recorded by the pack
                        [MS-IS-discussion/style.md names no figure and no table for this
                         section, and takes no float count]
```

#### 8.4 · The language, in the papers' own words
(five sentences the discussion style file quotes with a paper's name attached, and the requirement that carries none)

"Taken together, our results provide clinical leaders with valuable insights into the design of performance-feedback mechanisms" [Huesmann 2025].
The P1 contribution restatement, naming the decision-maker in the same breath.
> ✎ The P1 contribution restatement, naming the decision-maker in the same ~breath, which~ *breath. That* is how a healthcare paper opens the ~action-bearing section.~ *section that asks for an action.* · CC · 260802 1538
That is how a healthcare paper opens the section that asks for an action.
"increasing the coverage of disclosure or making disclosed payments more salient ... may be an effective method for changing physician behavior" [Chao/Larkin 2022].
The P3 managerial implication derived FROM the estimate, naming both the actor and the lever, which is the move the anti-pattern `important implications for IS research and practice` is written against.
"the implementation of an advanced AI system can yield inferior outcomes even when compared with a technologically inferior IT system" [Krakowski 2026].
The practical insight stated against the reader's expectation, so the implication is a finding rather than a restatement of one.
"Most importantly, we do not observe prepolicy payment data for the treatment group" [Chao/Larkin 2022].
The P5 limitation ranked and stated flatly, in the cite-free paragraph the micro-norms measure.
"Future research could also explore the cost of tailoring, which was not addressed in this study." [Krakowski 2026].
The P6 future direction as one concrete question, which is the whole budget this desk gives it.

The welfare sentence is the one thing this desk requires that MISQ and ISR do not.
> ✎ The welfare ~sentence,~ *sentence is* the one thing this desk requires that MISQ and ISR do ~not, is~ *not. It survives here only as* a bracketed pattern at ~L110-112~ *L110-112,* with no paper's name on ~it, and the~ *it. The* `Proposition 2 implies that firms should ...` translation at L71-74 ~is equally unattributed, which is what~ *carries no name either.* `8.1` ~records.~ *records both.* · CC · 260802 1538
It survives here only as a bracketed pattern at L110-112, with no paper's name on it.
The `Proposition 2 implies that firms should ...` translation at L71-74 carries no name either.
`8.1` records both.

### 9 · Sec-A-Appendix: the Online Appendix is a separate document, lettered A onward

**Two tiers, one of them at a DOI**: a short in-paper appendix may follow the References, and everything substantial lives in a separate PDF.

```text
  🗂 THE NAME · MS-IS-appendix/style.md L6-21
     use     "Online Appendix", singular for one document
             "online appendices" when several are bundled
     never   e-companion · Electronic Companion · Supplementary Materials
     legacy  the INFORMS "EC." prefix survives in element numbering
             only: `Proposition EC.1`                        L18-20

  🅰 THE LETTERING · L29-44
     sections      A, B, C, D, E, F
     subsections   B.1, B.2, C.3, D.3
     floats        letter-prefixed, RECOMMENDED: Table B.1 · Figure A.1
     floats        continuous from the main paper, in practice: main ends
                   at Figure 6, appendix starts at Figure 7   L39-40
     the pack prefers letter-prefixed, because a revised main paper
       renumbers a continuous appendix                        L42-44

  🚪 THE TRIAGE RULE · L83-85
     main text        removing it would stop the reader evaluating the
                      PRIMARY claim
     Online Appendix  it strengthens or extends the claim but is not
                      required to follow the argument

  📥 WHAT GOES ONLINE · L70-81
     model derivations, PROOFS, propositions
     full experiment instructions, parameter tables
     robustness and sensitivity: alternative specs, Tobit, Poisson
     supplementary or abandoned experiments
     ITT alongside a LATE in the main text
     extended heterogeneity: quartile splits, alternative cutoffs
     data construction, variable definitions, balance tables

  📤 WHAT STAYS IN THE BODY · L63-68
     core theory, hypotheses, the primary identification strategy
     the research design, enough to evaluate it
     the main results: primary outcome, 1-2 key tables or figures
     heterogeneity WHEN it is a primary contribution
     discussion, limitations, conclusion

  📐 SIZE · L87-92, L116-117
     main paper        13-16 typeset pages   Huesmann 16 · Cui 13
     Online Appendix   routinely LONGER than the main paper
     typical           3-6 lettered sections · 10-20 tables and figures
     measured          Huesmann 3 lettered (A theory incl. Proposition EC.1 ·
                       B design incl. Table B.1 · C robustness to C.5)
     measured          Feng 4 lettered, 14 subsections, online items to p. A25

  🔗 HOW THE BODY POINTS AT IT · L46-59
     `see Online Appendix A`
     `See Section B.2 of the Online Appendix`
     `see Table B.1 in Online Appendix B`
     `results ... are relegated to Online Appendix E`
     🚫 never a bare `see the Online Appendix`               L58-59
```

🗂 Establishes the appendix as an addressed place rather than an overflow. That is what lets every other division say "relegate it" and mean something checkable.
> ✎ 🗂 Establishes the appendix as an addressed place rather than an ~overflow, which~ *overflow. That* is what lets every other division say "relegate it" and mean something checkable. · CC · 260802 1538

#### 9.1 · The proof leaves the body and the Proposition stays
(the split this desk's formal apparatus depends on)
`MS-IS-theory-model/style.md` L100-101 keeps short proofs in the body and sends long ones to the Online Appendix, under the note "All proofs are in the Online Appendix".
> ✎ `MS-IS-theory-model/style.md` L100-101 keeps short proofs in the body and sends long ones to the Online ~Appendix~ *Appendix,* under the note "All proofs are in the Online ~Appendix", and the~ *Appendix". The* appendix triage at L71 lists derivations, proofs and propositions as Appendix A content. · CC · 260802 1538
The appendix triage at L71 lists derivations, proofs and propositions as Appendix A content.
So the body carries the numbered statement and its intuition, the appendix carries the verification, and the main text names the letter it went to.

#### 9.2 · No stored exemplar is an appendix
(every count in this division came from an in-text cross-reference)
L119-121 records that both stored PDFs are typeset main articles, so the section counts and item counts were read out of the papers' own pointers rather than out of the supplements.
The prose micro-norms are marked not measurable at L118.
> ✎ The prose micro-norms are marked not measurable at ~L118, which~ *L118. This* is ~why this is~ *therefore* the one section kind in the pack with no ~sentence-level~ shape at *the sentence level at* all. · CC · 260802 1538
This is therefore the one section kind in the pack with no shape at the sentence level at all.

#### 9.3 · Two page counts, in two different units
(35 manuscript pages against 13-16 typeset ones)
`playbook-utd-is/README.md` L148 gives MS-IS roughly 35 pages of text with proofs, robustness and instrument items pushed online, while `MS-IS-appendix/style.md` L89 measures published main papers at 13-16 typeset pages.
Neither file states its unit.
> ✎ Neither file states its ~unit, so the~ *unit. The* two numbers ~are reconcilable~ *agree* only ~by assuming~ *if* one counts a double-spaced manuscript and the other a typeset article. · CC · 260802 1538
The two numbers agree only if one counts a double-spaced manuscript and the other a typeset article.

#### 9.4 · Format values
(the four format metrics for the appendix, the one section kind the pack sizes in items rather than in words)

```text
  📏 WORDS            not recorded by the pack
                        [prose micro-norms declared "not measurable from stored exemplars",
                         MS-IS-appendix/style.md L118; the only size norm is in PAGES, main
                         paper 13-16 typeset pp and the Online Appendix routinely longer,
                         L89-92]
  📚 CITATION DENSITY not recorded by the pack
                        [same L118 declaration: this is the one section kind in the pack with
                         no sentence-level shape at all]
  🔢 VALUE DENSITY    not recorded by the pack
                        [same L118 declaration]
  📊 DISPLAYS         counted, and the only counted metric this section kind has: 3-6 lettered
                        sections and 10-20 supplementary tables and figures is typical  [L91-92]
                      measured Huesmann: 3 lettered sections, Table B.1, Proposition EC.1, and
                        one in-paper appendix carrying Figure A.1                     [L115-116]
                      measured Feng: 4 lettered sections, 14 subsections, online Tables A1-A4+
                        and Figures A3, A10, A13 running to p. A25, no in-paper appendix
                        [L115-117]
```

#### 9.5 · The language, in the papers' own words
(five cross-reference phrasings the appendix style file carries with a bracket key, which is the whole of its attributed text)

"see Table B.1 in Online Appendix B" [Huesmann 2025].
The full pointer, naming the item and the section letter it sits in, which is the form the division's ban on a bare `see the Online Appendix` is written to produce.
"Table C.5 in Section C.3 of the Online Appendix" [Huesmann 2025].
The same pointer descending one level further, so a reader lands on the subsection rather than on the letter.
"results from this experiment are ... relegated to Online Appendix E" [Cui 2025].
The relegation verb moving a whole secondary experiment out of the body, which is the triage rule at L83-85 executed in one clause.
"For more information, see Section C of the Online Appendix" [Huesmann 2025, endnote 4].
The same pointer written inside an endnote, the third address a body has for supplementary material after the text and the float.
"Proposition EC.1" [Huesmann 2025].
The legacy INFORMS element prefix, and the pack's only numbered Proposition attached to a real paper.
> ✎ The legacy INFORMS element prefix, and the pack's only numbered Proposition attached to a real ~paper, known to the~ *paper. The* pack *knows it* as a name in a ~cross-reference rather than~ *cross-reference, not* as a statement anyone has read. · CC · 260802 1538
The pack knows it as a name in a cross-reference, not as a statement anyone has read.

`MS-IS-appendix/style.md` L118 declares its prose micro-norms not measurable.
> ✎ `MS-IS-appendix/style.md` L118 declares its prose micro-norms not ~measurable, so~ *measurable. So* these pointer phrasings are all the ~attributable~ language this section kind ~has, and no~ *can attach to a paper's name. No* sentence of appendix prose is quoted anywhere in the pack. · CC · 260802 1538
So these pointer phrasings are all the language this section kind can attach to a paper's name.
No sentence of appendix prose is quoted anywhere in the pack.

## Aims

### A1 · 🔄 The vocabulary switch is the arrival cost
- A1.1 · The construct-to-mechanism translation is written once rather than redone per paper.
  **Done when:** retargeting a MISQ or ISR paper here produces a named translation rather than a rewrite from scratch.

### A2 · 📈 Where it sits against its two siblings
- A2.1 · The undecided matrix row is resolved with a tiebreak.
  **Done when:** a computational large-scale-data paper is routed to ISR or MS-IS on a written rule.

### A3 · 📏 Sec-0-Abstract: one prose paragraph with five hidden beats
- A3.1 · The abstract's binding word range is one number rather than three.
  **Done when:** a draft is failed against a single cited range, and the two residual ranges in `MS-IS-abstract/style.md` are marked superseded in the file that carries them.

### A4 · 🔢 Sec-1-Introduction: every result previewed before the data arrives
- A4.1 · The enumerated-results preview is checkable on a draft pinned to this outlet.
  **Done when:** an introduction with no magnitude-bearing result paragraph ahead of its data section is failed by a check rather than by a reader.
- A4.2 · The stated and measured paragraph counts stop disagreeing.
  **Done when:** `MS-IS-introduction/style.md` carries one paragraph count, and it is the measured one the template already follows.

### A5 · 🧮 Sec-2-Theory: the model section, where a Proposition lives and its proof does not
- A5.1 · The Proposition, comparative-static and welfare apparatus gains an exemplar.
  **Done when:** the pack stores one MS-IS paper stating a numbered Proposition and a welfare comparison, and the phrasing block cites it by name.
- A5.2 · The analytical word budget rests on a counted section.
  **Done when:** one analytical MS-IS section is measured with its display equations included, and the 3,000-5,000 range is confirmed or reconciled against it.

### A6 · 📐 Sec-3-Methods: the estimating equation is a display and every term is defined under it
- A6.1 · The identification apparatus a draft owes is listed before the section is written.
  **Done when:** a methods draft naming no estimator, no identifying assumption, no clustering level or no first-stage F is failed once per missing item.

### A7 · 📊 Sec-4-Results: ordered by identification, never by hypothesis
- A7.1 · The organizing axis is enforced as identification and outcome.
  **Done when:** a results draft ordered H1, H2, H3 is flagged before it reaches a reader.

### A8 · ⚖️ Sec-5-Discussion: results become an action, and a market paper states the welfare
- A8.1 · The welfare statement is demanded of the papers that owe one.
  **Done when:** a market, platform or pricing paper reaching CHECK with no stated welfare consequence is failed on that alone.
- A8.2 · The discussion budget is one range rather than two.
  **Done when:** the contrast table in `MS-IS-discussion/style.md` carries the revised 500-2,500 range or loses the row.

### A9 · 🗂 Sec-A-Appendix: the Online Appendix is a separate document, lettered A onward
- A9.1 · The body-versus-appendix triage runs before the body is drafted rather than after.
  **Done when:** every proof, robustness table and instrument detail carries a lettered Online Appendix address at draft time, and no body pointer reads bare.

### P · 🧾 Targets that belong to no single section

- P1 · The desk's own submission mechanics are checked before a manuscript is uploaded, rather than discovered at the portal.
  **Done when:** a deliver run walks §10's steps and records the result of each, with the abstract counted on the final file.
- P2 · The cost of this desk is known before a paper commits to it, not after the first decision.
  **Done when:** a venue decision for this paper names the acceptance odds, the review clock and the money this desk charges, and says where each was read.
- P3 · Every row `Submission-Rules` prints as `❓ STILL NOT ON RECORD` is closed by a direct read of the desk rather than by a search summary.
  **Done when:** each open row carries a value with a `fetched and verified` stamp, or records that the desk publishes nothing on it.

## States

### A1 · 🔄 The vocabulary switch is the arrival cost
- ⬜ A1.1 · Not started. The ban on IS jargon is stated and the replacement vocabulary is not.

### A2 · 📈 Where it sits against its two siblings
- ⬜ A2.1 · Not started. The matrix row points at two outlets and stops.

### A3 · 📏 Sec-0-Abstract: one prose paragraph with five hidden beats
- ⬜ A3.1 · Not started. Three ranges sit in one style file and the template picks one of them silently.

### A4 · 🔢 Sec-1-Introduction: every result previewed before the data arrives
- ⬜ A4.1 · Not started. The signature move is described in prose and enforced by nothing.
- ⬜ A4.2 · Not started. The file's header says 7-12 and its own micro-norms say 9-13.

### A5 · 🧮 Sec-2-Theory: the model section, where a Proposition lives and its proof does not
- ⬜ A5.1 · Not started. The 8 mined exemplars are empirical, structural or methodological, and the 2 on disk that no `style.md` names are unmined.
- ⬜ A5.2 · Not started. The only measurement under the analytical budget is declared a measurement artifact.

### A6 · 📐 Sec-3-Methods: the estimating equation is a display and every term is defined under it
- ⬜ A6.1 · Not started. The five owed items are spread across the style file's anti-patterns and signature moves.

### A7 · 📊 Sec-4-Results: ordered by identification, never by hypothesis
- ⬜ A7.1 · Not started. The axis is a contrast-table row and no draft is measured against it.

### A8 · ⚖️ Sec-5-Discussion: results become an action, and a market paper states the welfare
- ⬜ A8.1 · Not started. The requirement is stated three times in the style file and shown by no exemplar.
- ⬜ A8.2 · Not started. The revision landed in the budget section and the template, and not in the contrast table.

### A9 · 🗂 Sec-A-Appendix: the Online Appendix is a separate document, lettered A onward
- ⬜ A9.1 · Not started. The triage rule exists and no artifact records which item went where.

### P · 🧾 Targets that belong to no single section
- ⬜ P1 · Not started. The mechanics reached this page on 260803, as a runnable list in §10, and no deliver run reads them.
- ⬜ P2 · Not started. The odds, the clock and the money landed 260803; nothing in the venue decision cites them.
- ⬜ P3 · Not started, and it is blocked on the site rather than on effort: `pubsonline.informs.org` answers a direct fetch with HTTP 403.

## Files

### ⚙️ Engines · what RUNS this page's subject

- `_tools/sync-exemplars.py`
  Rewrites both generated blocks in the Generated group below, from the pack folder and from `section-kinds.yml`. ⚠️ Never hand-edit between the markers: the next run overwrites it. Run it with `--check` before calling this page finished; a stale block is a count that disagrees with the folder.

### 📋 Contracts · what CARRIES a rule to other pages

- `../../board/page-types/haipipe-board-page-for-venue/SKILL.md`
  The venue-page contract: the three figures, the five Files groups, the `Sec-<n>` index, the two-source rule, and the reference-not-rulebook principle. This page reads that file rather than reading the reference page, so a rule this page discovers is written there in the same pass.
- `../../board/haipipe-board-page/SKILL.md`
  The base frame that contract extends. Load it first; it owns the seven sections and their order.
- `QBv1-misq.md`
  The contract's reference implementation, and the nearest sibling desk. Read it for the shape of a finished venue page, and for the MISQ side of every comparison `2` draws.

### 📥 Input files · what this page READS

- `../../paper/venue/playbook-utd-is/MS-IS/taste.md`
  The desk signals and the one-sentence test. Start here when what MS-IS buys is the question.
- `../../paper/venue/playbook-utd-is/MS-IS/MS-IS-theory-model/style.md`
  The model section `5` is built from, including the mechanism translation table `1` folds in. The folder is named `theory-model` on disk and resolves to the canonical `theory` kind.
- `../../paper/venue/playbook-utd-is/README.md`
  The family delta and the lean-signal matrix `2` reads, covering all four UTD-IS outlets at once.
- `../../paper/route/haipipe-paper-stage/stages/section-kinds.yml`
  The reader-side resolver: outlet ▸ section kinds. It is what the generated kinds block below is built from, and it carries the `theory-model` alias.

### 🔗 Authority · what the DESK itself PUBLISHES, read directly and never through the pack

⚠️ Provenance: the submission-guideline and LaTeX pages were fetched and verified 260802. Everything added on 260803 comes from search summaries of the desk's own pages, because `pubsonline.informs.org` answers a direct fetch with HTTP 403; each such row says so. Re-read the desk before a real submission.

- [Author / submission instructions](https://pubsonline.informs.org/page/mnsc/submission-guidelines) · one page for the whole journal, governing manuscript types, length, format, electronic companions, and the ScholarOne steps; the department is not a separate desk with its own instructions, it is the manuscript "Type" chosen at ScholarOne Step 1, and the Information Systems department states its own scope in [the departmental editorial statements](https://pubsonline.informs.org/page/mnsc/editorial-statement).
- [LaTeX template](https://pubsonline.informs.org/pb-assets/LaTeX/INFORMS-MNSC-Template-6-10-2024-1718048504857.zip) · the Management-Science-template.tex archive INFORMS ships from its [LaTeX style files page](https://pubsonline.informs.org/authorportal/latex-style-files), carrying the journal template, the submission style file, and a BibTeX style for [the INFORMS reference style](https://pubsonline.informs.org/pb-assets/INFORMSReferencesStyle-1513283897320.pdf); the instructions add that any software is accepted so long as it produces a conforming PDF, so Word is not refused, only untemplated.
- The rule the pack does not record: there is NO page limit on an initial submission at this desk, only a Department Editor's right to reject one for excessive length. The limit binds invited revisions alone, at 47 pages of 25 lines double-spaced or 32 pages of 33 lines at 1.5 spacing, and "an online appendix will not count toward the page limit". The desk also directs analytical proofs and data analysis into the electronic companion, and rules that companion contents "should not be critical for the proper evaluation of the paper", which is the test for what may leave the body.
- CONTRADICTS the pack on length: `../../paper/venue/playbook-utd-is/README.md` records "~35 pp text", which matches no number the desk states; the pack's routing of proofs and robustness to the online appendix is confirmed, but its page figure is not the journal's rule.
- CORRECTS the pack on the abstract: `../../paper/venue/playbook-utd-is/MS-IS/MS-IS-abstract/template.md` warns against "the 5-label MS submission-guideline format" as a typesetting artifact, but the current instructions state no labelled or structured abstract anywhere; the only abstract rule they carry is a cap of 250 words or less, which the pack does not record.

### 📤 Generated · what `sync-exemplars.py` WRITES into this page

<!-- exemplars:begin -->

📚 **Exemplars** · 10 papers on disk, regenerated by `_tools/sync-exemplars.py`

- `../../paper/venue/playbook-utd-is/MS-IS/examples/burtch-2026-ms-ensembleiv-ml-generated-variables.pdf` · Burtch 2026
- `../../paper/venue/playbook-utd-is/MS-IS/examples/chen-2025-ms-structural-topic-sentiment-text.pdf` · Chen 2025
- `../../paper/venue/playbook-utd-is/MS-IS/examples/cui-2025-ms-genai-software-developers-rct.pdf` · Cui 2025
- `../../paper/venue/playbook-utd-is/MS-IS/examples/dekok-2025-ms-chatgpt-textual-analysis-accounting.pdf` · Dekok 2025
- `../../paper/venue/playbook-utd-is/MS-IS/examples/digital-payment-2026-ms-customer-success-management.pdf` · Digital-Payment 2026
- `../../paper/venue/playbook-utd-is/MS-IS/examples/feng-2025-ms-pbm-drug-pricing.pdf` · Feng 2025
- `../../paper/venue/playbook-utd-is/MS-IS/examples/huesmann-2025-ms-ranking-physician-effort.pdf` · Huesmann 2025
- `../../paper/venue/playbook-utd-is/MS-IS/examples/krakowski-2026-ms-human-centered-ai-field-experiment.pdf` · Krakowski 2026
- `../../paper/venue/playbook-utd-is/MS-IS/examples/neural-networks-2026-ms-data-driven-operational-decisions.pdf` · Neural-Networks 2026
- `../../paper/venue/playbook-utd-is/MS-IS/examples/sunshine-2025-ms-disclosure-physician-prescribing.pdf` · Sunshine 2025

- `../../paper/venue/playbook-utd-is/MS-IS/examples/EBSCO_RECENT_RESULTS.md` · the pack's own manifest, not an exemplar
- `../../paper/venue/playbook-utd-is/MS-IS/examples/INDEX.md` · the pack's own manifest, not an exemplar

<!-- exemplars:end -->

<!-- kinds:begin -->

📐 **Section kinds** · none declared in `stages/section-kinds.yml`, so this venue is blueprint-only: the S-Venue-0 blueprint is binding and no per-section pack is resolved.

<!-- kinds:end -->

## Law

- MS-IS thinks in mechanisms, equilibria, and welfare rather than constructs, theories, and implications, so arriving here is a vocabulary translation and not a reframing.
  Reduced-form empirics are permitted when identification is credible and theory frames the mechanism; empirical work with no structural interpretation is not.

## Glossary

Every term here is a real term of this field, and a paper written for this desk needs all of them. What follows is a plain reading of each, not a replacement for it.

- **Desk**: the editorial department a paper is judged by. MS-IS is the Information Systems department of Management Science, and the Authority block records that it is not a separate submission site, only a manuscript Type chosen at ScholarOne Step 1.
- **The pack**: the folder of style files, templates and mined exemplar papers at `playbook-utd-is/MS-IS/`. It is the only thing this page describes.
- **Mechanism**: the economic story of how one thing moves another. `5` carries the pack's own table of the names it wants that story told in.
- **Equilibrium**: the point where every agent's choice is the best answer to every other choice, so nobody moves again.
- **Welfare**: who ends up better or worse off, counted as consumer surplus, producer surplus and the total of the two. `8` makes a statement of it obligatory for a market or platform paper.
- **Structural primitive**: a recovered parameter of the underlying economic model, one of the four things this desk accepts as a contribution.
- **Comparative static**: how an equilibrium outcome moves with a parameter, part of the apparatus this desk expects around a formal result.
- **Micro-foundation**: the account of individual choice a result rests on. `2` records that this desk asks for one where MISQ asks for a primary theory.
- **Reduced form**: an estimate of how an outcome moves with a treatment, with no model of the choices behind it. It is permitted here when identification is credible and theory frames the mechanism, and refused when it speaks to no mechanism at all.
- **Identification**: the argument that an estimate measures the effect claimed and not something else. `6` asks for it as an economic argument about who is affected, never as the name of an estimator.

## Log

260802 1538 · Rewritten for a reader whose English is weak, with `haipipe-writing`.
  Twenty-four `> ✎` word-level records over twenty-three sentences.
  They cover the Opening paragraph twice, four figure readbacks that bolted a clause onto a finished sentence, and eighteen Content sentences that ran long or did the same, each split at the hinge.
  No number, no `style.md` line reference and no paper's name was changed.
  The Opening drawer gained a part defining the six words its question uses.
  The Glossary grew from two entries to ten, so every field term this desk needs is kept and anchored rather than simplified away.
  The five long entries below were split into indented continuation lines, which the Log renderer joins back into one entry each, so what they record is unchanged.
  One sentence could not be recorded. The closing sentence of `5.4` quotes the pack's `*Intuition.*` block name, and `cli/wdiff.py` refuses any text carrying `*` because that is its own insertion mark, so that 41-word sentence is left as it stands.
260802 · Corrected against the desk. Management Science states NO page limit on an initial submission.
  The 47 and 32 page rules bind invited revisions only, with the online appendix excluded.
  So the pack's "~35 pp text" matches no stated number at any stage.
  Two more. The packs warn against a structured five-label abstract that the current instructions no longer state anywhere.
  And none of them records the one real rule, a 250-word abstract cap.
  MS-IS and MS-Marketing share ONE submission page.
  The department is a ScholarOne manuscript Type, not a separate desk, though their taste files differ legitimately.
260802 · Authority sub-block added at the end of Files, from Management Science's own submission guidelines rather than from the pack.
  The MNSC LaTeX archive was fetched and is a real archive.
  The first finding is structural. The department is not a separate desk with its own instructions; it is the manuscript Type chosen at ScholarOne Step 1.
  The Information Systems scope statement sits on the journal's shared editorial-statement page, so QBv3 and QBv4 answer to one authority and differ only in that statement.
  Two corrections follow. There is no page limit on an initial submission at all.
  The 47-page or 32-page limit binds invited revisions only, with the online appendix excluded.
  So the family README's "~35 pp text" matches no number the desk states, while its routing of proofs to the online appendix is confirmed.
  The instructions state no structured abstract anywhere, only a cap of 250 words the pack does not record.
260802 · Two subsubsections added to each of the seven section-kind divisions.
  One is a `Format values` block carrying WORDS, CITATION DENSITY, VALUE DENSITY and DISPLAYS, with the `style.md` line each was read from.
  The other is a `The language, in the papers' own words` block, quoting only sentences the pack already attributes to a paper.
  Three findings came out of it.
  VALUE DENSITY, the numeric-per-sentence figure this repo's value marker refers to, is recorded by NO section kind at this desk.
  No extracted-text exemplar exists to measure it from either, since the only two `.md` files under `examples/` are the pack's own manifests.
  Numbered Propositions, Theorems and display equations are named as required apparatus and never counted as objects, in the model section and in the results section alike.
  The appendix inverts the pattern. It is the one kind with no word budget and no citation density, and the only one whose displays are counted.
260802 · Seven section-kind divisions added, one per kind this outlet declares.
  Each carries the pack's measured budget with its `style.md` line, the arc, the signature moves as slot patterns, and the anti-patterns the pack names by hand.
  The formal apparatus is now addressed: Propositions and comparative statics in `### 5`, the estimating equation in `### 6`, welfare in `### 7` and `### 8`, proofs in `### 9`.
  The load-bearing content the retired family page carried was folded in from `playbook-utd-is/README.md`: the one-claim thread through abstract, introduction and discussion, the market-paper welfare claim, and the manuscript-length figure.
  Three numbers that do not reconcile are recorded as sub-paragraphs rather than smoothed over: three abstract ranges, two discussion ranges, and an analytical budget with no counted section under it.
  The Writing Style bullet was relaxed from never transcribing a norm to citing every number inline.
260802 · Corrected against `stages/section-kinds.yml`, found while answering how a Content division becomes an S-Main page.
  That file already carries the glob rule for the section abbreviation, an outlet-to-kinds map measured on disk, the `theory-model` alias, and the blueprint-only declaration for grant and patent.
  Four claims on this group that something was undeclared were wrong, and the Aims they carried are replaced by drift guards.
260802 · Opened with the QBv outlet pages, from `playbook-utd-is/MS-IS` at `Venue-Paper@fe25a88`.
