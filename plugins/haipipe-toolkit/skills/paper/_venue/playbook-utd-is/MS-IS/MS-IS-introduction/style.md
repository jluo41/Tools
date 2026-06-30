# MS-IS Introduction Style Guide

The MS-IS introduction is economics-style: longer than MISQ/ISR (3-5 pages, 7-12
paragraphs), weaves literature positioning into the introduction rather than a separate
Literature Review section, and ends with a contribution statement or a "roadmap"
paragraph. No separate Related Work section in most MS papers.

## Word budget

1,500-2,500 words (3-5 double-spaced pages). Longer than MISQ (~1,000 w) or ISR
(~1,200 w) introductions because MS-IS folds the literature positioning into the
introduction itself.

## Arc (paragraph-level structure)

The MS-IS introduction follows an economics "funnel + enumerated results" arc:

```
P1-P2   PHENOMENON + STAKES
        State the economic phenomenon, the IS artifact or digital market involved,
        and why it matters (revenue, welfare, efficiency, policy).
        Cite 3-6 foundational references (economics, OR, management science).

P3      GAP / TENSION
        State what prior work established, then pivot to what remains unresolved.
        Name the specific gap: causal direction unclear, mechanism unspecified,
        welfare consequence unknown, structural primitive unrecovered.

P4      THIS PAPER
        "In this paper, we [ask/study/model/exploit]..." followed by data, method,
        and identification strategy in 2-3 sentences. One paragraph, crisp.

P5-P8   ENUMERATED RESULTS
        "We report [N] main results." or "Our preferred estimates suggest..."
        Each main finding gets its own paragraph (or a "First,...", "Second,..."
        enumeration within 2-3 paragraphs). State direction and magnitude.
        This is the signature MS move: the introduction previews all key results
        before the reader reaches the methods section.

P9-P10  CONTRIBUTION / LITERATURE POSITIONING
        State the contribution in one paragraph, naming what is new (identified
        causal effect, characterized equilibrium, recovered structural primitive,
        welfare result). Position against 2-3 specific literature streams.
        "We contribute to the literature on [X] by [Y]."
        "Our work complements [Z] by [distinguishing feature]."

P11     ROADMAP (optional)
        "The remainder of this paper is organized as follows." One sentence per
        section. Some MS papers omit this; most include it.
```

## Signature moves (mined from Bick et al. 2026 and Cui et al. 2025)

### Enumerated results preview
The introduction previews ALL main results before the reader reaches the data section.
This is the single most distinctive MS move vs. MISQ/ISR.

From Bick et al.: "We report six main results. First, a substantial share of
respondents already use genAI at work and at home... Second,... Third,... Fourth,...
Fifth,... Sixth,..." Each finding gets a full paragraph with specific numbers.

From Cui et al.: "Our preferred estimates from an instrumental variable regression
suggest that usage of the coding assistant causes a 26.08% increase (SE: 10.3%) in
the weekly number of completed tasks." Results with standard errors in the introduction.

### Gap as unresolved economic question
Not "little is known about X" (MISQ style) but "uncertainty over [economic consequence]
reflects a lack of [specific evidence type]."

From Bick et al.: "Uncertainty over the impact of genAI on the economy in part reflects
a lack of systematic evidence on the frequency and intensity of genAI adoption."

### Data-first credibility signal
MS introductions name the data source and its credibility early (nationally
representative, RCT, natural experiment), not just the topic.

From Cui et al.: "We analyze three large-scale randomized controlled trials in
real-world environments. These experiments randomly assigned access to Copilot...
to just under five thousand software developers at Microsoft, Accenture, and an
anonymous Fortune 100 electronics manufacturing company."

### Contribution as literature positioning
Contribution paragraphs name specific literature streams and state the paper's position
relative to each, using "We contribute to..." or "Our work complements..." phrasing.

From Cui et al.: "More generally, we contribute to the literature studying the
productivity and on-the-job performance of software developers."... "Lastly, we
contribute to an emerging literature in marketing and other fields on the broader use
of large language models."

## Sentence shapes to imitate

Opening sentences:
- "[Technology/phenomenon] has rapidly emerged as [description of importance]."
- "[Economic agents] face [a decision / a tradeoff / uncertainty] about [X]."
- "Many economists expect [technology] to profoundly affect [domain]."

Gap sentences:
- "Uncertainty over [consequence] reflects a lack of [evidence type]."
- "Despite [volume of prior work], [specific question] remains open."
- "Prior work has [established X] but has not [identified/resolved/generalized Y]."

This-paper sentences:
- "This paper studies [phenomenon] using data from [source]."
- "In this project, we ask how [X] affects [Y], using [Z] as [context/example]."
- "We exploit [identification strategy] using [data covering scope]."

Results sentences (in introduction):
- "We find that [X] increases [Y] by [magnitude] (SE: [Z])."
- "Our preferred estimates suggest that [treatment] causes a [magnitude] [direction] in [outcome]."
- "The effect is [heterogeneous]: [group A] experiences [larger/smaller] gains than [group B]."

Contribution sentences:
- "We contribute to the literature on [X] by [providing the first / identifying / characterizing]."
- "Our work complements [specific prior papers] by [distinguishing feature]."

## Anti-patterns

- **No separate Literature Review section.** MS-IS folds literature positioning into
  the introduction (contribution paragraphs) and into the Theory/Model section. A
  standalone "2. Related Work" section is an ISR/MISQ convention, not MS.
- **No vague importance claims.** "This is an important topic" without economic stakes.
  Every importance claim must name the stake: revenue, welfare, efficiency, policy cost.
- **No IS-insider jargon in the introduction.** Avoid TAM, UTAUT, technology acceptance
  model, IS success model. MS readers include economists, OR scholars, and management
  scientists who do not know these frameworks. Use plain economic language.
- **No hypotheses in the introduction.** MS empirical papers state results directly in
  the introduction; hypotheses (if used at all) appear in the Theory/Model section.
  Many MS papers skip formal hypotheses entirely and state "predictions" or derive
  propositions from a model.
- **No "the rest of this paper is organized as follows" without having previewed results
  first.** The roadmap comes AFTER the enumerated results, not before.

## Contrast with MISQ/ISR introductions

| Dimension | MS-IS | MISQ | ISR |
|-----------|-------|------|-----|
| Length | 3-5 pages | 1.5-2 pages | 1.5-2.5 pages |
| Results preview | Yes, enumerated with magnitudes | No | Sometimes briefly |
| Separate lit review | No (folded into intro + model) | Often yes | Often yes |
| Hypotheses in intro | No (results instead) | No | Sometimes briefly |
| IS jargon | Avoided | Welcome | Moderate |
| Contribution statement | Literature-stream positioning | "What is new" paragraph | Theoretical/empirical/methodological |
| Roadmap paragraph | Common | Rare | Rare |

## Enrichment needs

- [x] Mine a healthcare-domain MS-IS introduction (Shukla et al. 2021 or Angst et al.
  2010) to capture how IS-specific phenomena are introduced to the MS economics audience.
  **RESOLVED**: See healthcare-domain patterns below (Huesmann 2025, Chao/Larkin 2022).
- [x] Mine an analytical MS-IS introduction to capture how the model setup is previewed
  (proposition preview instead of results preview).
  **RESOLVED**: See structural/hybrid patterns below (Feng 2025, Burtch 2026).

---

## Enriched from additional exemplars (2026-06-29)

Sources: 8 published MS papers (Huesmann 2025, Chao/Larkin 2022, Feng 2025, Cui 2025,
Krakowski 2026, de Kok 2025, Chen 2025, Burtch 2026).

### Healthcare-domain introduction conventions

Healthcare MS papers (Huesmann 2025, Chao/Larkin 2022) introduce the phenomenon in
clinical terms first, then translate to economics:

**Huesmann opening pattern** (lab-in-field physician experiment):
"Improving the quality of care is a key objective for hospitals. For clinical leaders,
one important aspect of doing so is to motivate individual physicians to provide
high-quality care."
- Opens with the hospital operations problem, not with an economic model
- Names the specific clinical activity early ("adenoma detection rates," "colonoscopy")
- Grounds the phenomenon in medical-society recommendations before pivoting to
  economic analysis
- Uses "clinical leaders" as the decision-maker throughout (not "managers" or "firms")

**Chao/Larkin opening pattern** (quasi-experiment, physician prescribing):
"Hospitals, health center administrators, insurance companies, and regulators have
long struggled with the tradeoffs inherent in pharmaceutical marketing to physicians."
- Opens with a stakeholder-tension statement naming multiple parties
- Heavy citation density in the first two paragraphs (~15 citations in 2 pages)
- Names specific dollar amounts for stakes: "average a retail cost of $5,800 per drug
  per year," "prescription drugs now account for 15%-17% of total healthcare expenditures"
- The introduction spans 4 full pages before the Background section begins

**Healthcare introduction funnel**:
```
P1-P2   CLINICAL PROBLEM + DOLLAR STAKES
        Name the healthcare phenomenon, the stakeholders, and the
        dollar magnitude (spending, cost savings, welfare).

P3-P4   POLICY/INTERVENTION + MIXED EVIDENCE
        Describe the policy or mechanism under study. State that
        prior evidence is mixed or incomplete. Name specific
        prior studies and their limitations.

P5-P6   THIS PAPER + IDENTIFICATION
        "This paper uses/tests/analyzes [design] to [question]."
        Name the data, the quasi-experiment or RCT, the sample size.

P7-P9   RESULTS PREVIEW (enumerated or sequential)
        State key findings with direction. For healthcare:
        name the affected drugs/physicians/patients specifically.

P10     CONTRIBUTION + MECHANISM
        "Our results provide [evidence type]..." Position against
        prior disclosure/feedback/prescribing literature.

P11     ROADMAP
        "This paper is organized as follows."
```

### Separate literature section: correction to the "no separate lit review" rule

The original guide states "No separate Literature Review section" as an anti-pattern.
This is overstated. Among the 8 published papers:

- **Huesmann 2025**: "2. Literature and Hypotheses" with "2.1. Related Literature on
  Relative Performance Feedback" -- a standalone literature review section
- **Chen 2025**: "2. Literature Review" -- a full standalone literature review section
- **Chao/Larkin 2022**: "2. Background" with substantial literature review subsections
- **Krakowski 2026**: "2. Theoretical Background and Hypotheses" -- theory + lit review

The accurate rule is: MS-IS papers do NOT have a section titled exactly "Related Work"
(the MISQ/ISR convention), but they frequently have a section titled "Literature and
Hypotheses," "Background," "Literature Review," or "Theoretical Background" that serves
a similar function. The literature positioning in the introduction supplements but does
not replace this section.

### Structural/hybrid model introduction conventions

**Feng 2025** (structural model, drug pricing):
- Opens with a policy question: "What is the best approach to controlling prescription
  drug prices?"
- Names the institutional intermediary (PBMs) and explains its role for the general reader
- States an apparent contradiction in the data ("These two findings are hard to reconcile")
  and uses it as the motivation for structural modeling
- Results preview uses counterfactual language: "Counterfactuals suggest that..."
  "We find that the total cost of statins would increase by almost 50%."
- Contribution paragraph names two specific literature streams with "Our article
  contributes to..." phrasing

**Burtch 2026** (methodological contribution, EnsembleIV):
- Opens with the two-phase practice: ML prediction + statistical inference
- States the methodological problem immediately: "prediction errors will manifest as
  measurement error in the second-phase regression model"
- Names the method and its three key ingredients concisely
- States theoretical results: "we prove the consistency and asymptotic normality..."
- Contribution framed as methodological novelty: "EnsembleIV represents a novel
  methodological contribution..."

### Additional signature moves

**Dollar-magnitude stakes in healthcare introductions**:
Healthcare MS papers quantify the stakes in specific dollar terms, not abstract
importance claims:
- "$5,800 per drug per year" (Chao/Larkin)
- "15%-17% of total healthcare expenditures, with 72% attributed to brand name drugs"
  (Chao/Larkin)
- "$1.7 trillion has been spent in the last 10 years" (Chao/Larkin)

**Mixed-evidence review as gap statement**:
Instead of "little is known about X," healthcare MS papers often frame the gap as
conflicting evidence:
- "Some studies report that relative performance feedback has positive effects... Many
  studies, however, report that relative performance feedback has negative or null effects"
  (Huesmann)
- "Some administrators and scholars have advocated for mandatory disclosure... but many
  practitioners believe disclosure has little effect on prescribing, and the empirical
  evidence is mixed." (Chao/Larkin)

**"Differences from Existing Studies" subsection** (Chao/Larkin):
Section 2.3 is a dedicated subsection that positions the paper against each close
competitor, stating the specific way this paper differs. Each competitor gets 2-3
sentences. This is a common healthcare MS convention when there are several related
papers on the same policy.

**Roadmap paragraph phrasing**:
- "This paper is organized as follows. Section 2 reviews the industry background and
  related literature. Section 3 summarizes the overall empirical approach and data.
  Section 4 presents the paper's empirical results, including comprehensive robustness
  checks. Section 5 concludes." (Chao/Larkin)
- "The article is organized as follows. Section 2 discusses drug demand, the PBM
  industry, and data sources. Section 3 documents stylized facts... Section 4 presents
  a structural model... Section 5 presents model estimates. Section 6 provides
  counterfactuals. Section 7 concludes." (Feng)
- "The rest of the paper is structured as follows. In Sec. 2, we provide a literature
  review... In Sec. 3, we present the main model... Section 5 concludes." (Chen)

### Opening sentence shapes (additional from published papers)

- "[Stakeholders] have long struggled with [tradeoff] inherent in [domain]."
  (Chao/Larkin)
- "Improving [outcome] is a key objective for [institutions]. For [decision-makers],
  one important aspect is to [action]." (Huesmann)
- "What is the best approach to [controlling/managing] [domain challenge]?" (Feng)
- "Recent management research has focused on [technology] for [application], with the
  ultimate goal of [objective]." (Krakowski)
- "Rapid advancements in [technology area] have given rise to [tool type]." (de Kok)
- "Empirical researchers in the social sciences are increasingly leveraging [method]
  in a hybrid two-phase process." (Burtch)

### Field experiment introduction conventions (Krakowski 2026)

Field experiments in MS-IS introduce the setting with enough institutional detail for
the reader to evaluate external validity:
- Name the industry, geography, and firm type: "a multinational pharmaceutical company"
  "four Nordic sales subsidiaries (Denmark, Finland, Norway, and Sweden)"
- Name the AI system's function: "AI-based sales system" spanning "planning, execution,
  and evaluation"
- Describe the treatment arms concisely: "tailored interaction group... untailored
  interaction group... control group using the legacy IT system"
- State the identification strategy: "Using a difference-in-differences (DiD) approach"
- Preview both positive AND negative findings: "tailored interaction yields positive
  effects... whereas untailored interaction results in negative treatment effects"
