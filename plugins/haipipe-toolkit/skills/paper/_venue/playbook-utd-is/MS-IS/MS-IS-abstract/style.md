# MS-IS Abstract Style Guide

The structured abstract is Management Science's signature differentiator from MISQ and
ISR (both use unstructured prose abstracts). Every MS submission must use this format.

## Format

Five labeled sections in bold italic, each followed by a colon and roman text. Under
200 words total (MS guideline: 250 words or fewer; aim for 150-200 for IS-department
papers). One to three sentences per section. No technical jargon in the abstract.

```
**Problem definition:** [1-2 sentences]
**Academic/practical relevance:** [1-2 sentences]
**Methodology:** [1-2 sentences]
**Results:** [2-3 sentences]
**Managerial implications:** [1-2 sentences]
```

## Section-by-section arc

### Problem definition (1-2 sentences)
State the research problem as a concrete decision, tension, or market failure. Name the
IS artifact, digital market, or technology involved. Do not state a research question
("we ask whether..."); state the problem ("firms face the challenge of..."; "consumers
must decide..."; "the design of X creates a tension between Y and Z").

Sentence shape:
- "[Economic agent] face(s) [decision/challenge] in [IS context]."
- "The [design/policy/technology] of [X] creates [tension/tradeoff] between [Y] and [Z]."
- "[IT artifact] has transformed [market/process], but [specific gap or unknown]."

Anti-patterns:
- Starting with "This paper studies..." (save that for Methodology).
- Vague problem statements ("little is known about X").
- Naming a theory instead of a problem.

### Academic/practical relevance (1-2 sentences)
State why the problem matters for (a) academic understanding and (b) practical
decision-making. This is the "so what" before the method. Name the specific
literature gap or unresolved question. Connect to managerial stakes (revenue, welfare,
efficiency, policy).

Sentence shape:
- "Understanding [X] is important because [academic gap] and [practical stake]."
- "Despite [volume of prior work], [specific unresolved question] remains open."
- "Answering this question has implications for [policy/platform design/firm strategy]."

Anti-patterns:
- Restating the problem definition.
- Listing multiple literatures without naming the gap.
- Pure academic relevance without practical stakes (MS demands both).

### Methodology (1-2 sentences)
Name the method, data, and identification strategy concisely. For analytical papers:
"We develop a [type] model of [agents/decisions]." For empirical papers: "We use
[data description] and employ [identification strategy]." For hybrid: state both.
Include sample size or data scope if space permits.

Sentence shape:
- "We develop a game-theoretic model of [agents] choosing [actions] under [information structure]."
- "We exploit [natural experiment / RCT / policy change] using [data] covering [scope]."
- "We combine [analytical model] with [empirical validation] using [data]."

Anti-patterns:
- Excessive methodological detail (save for the body).
- Naming software or packages.
- "We use machine learning" without specifying the identification logic.

### Results (2-3 sentences)
State the key findings with direction and, when possible, magnitude. Lead with the
primary result. For analytical papers: state the equilibrium characterization and its
key comparative static. For empirical papers: state the causal estimate (effect size,
significance, direction). Add one supporting result or boundary condition.

Sentence shape:
- "We find that [X] increases [Y] by [magnitude] (SE: [Z])."
- "We characterize the equilibrium and show that [comparative static]."
- "The effect is [stronger/weaker] when [moderator], suggesting [mechanism]."
- "Our results are robust to [key robustness check]."

Anti-patterns:
- Listing all results without hierarchy (the abstract has one primary).
- Vague findings ("we find significant effects").
- Claiming causality without naming the identification strategy in Methodology.

### Managerial implications (1-2 sentences)
State what decision-makers should DO differently, not what the paper found. Translate
the result into actionable guidance for managers, platform designers, or policymakers.
For market/platform papers: state the welfare consequence. End the abstract here.

Sentence shape:
- "Our findings suggest that [managers/policymakers] should [action] to [outcome]."
- "Platform designers can improve [welfare/efficiency] by [design change]."
- "These results imply that [policy/intervention] may [consequence]."

Anti-patterns:
- Restating the result in different words.
- "Future research should..." (never in the abstract).
- Generic implications ("our findings have important implications for practice").
- Ending on the method rather than the implication.

## Word budget

| Section | Target | Range |
|---------|--------|-------|
| Problem definition | 30 w | 20-40 w |
| Academic/practical relevance | 30 w | 20-40 w |
| Methodology | 30 w | 20-40 w |
| Results | 50 w | 40-70 w |
| Managerial implications | 25 w | 15-35 w |
| **Total** | **165 w** | **120-200 w** |

## Contrast with MISQ/ISR abstracts

| Dimension | MS-IS | MISQ / ISR |
|-----------|-------|------------|
| Format | 5 labeled sections | Unstructured prose |
| Word limit | < 200 w (guideline: 250) | <= 150 w |
| Ending | Managerial implication (actionable) | Theoretical contribution |
| Jargon level | No IS-insider terms (TAM, UTAUT) | IS constructs acceptable |
| Tone | Economic/decision-oriented | Theory-centered |

## Enrichment needs

- [x] Mine 2-3 published MS-IS structured abstracts to capture exact phrasing patterns
  (the preprint versions from Bick et al. and Cui et al. use unstructured abstracts;
  the structured format is applied during MS typesetting). Target: Shukla et al. (2021),
  Angst et al. (2010), Wang et al. (2023) from the exemplar fetch-list.
  **RESOLVED**: See correction below. Published MS papers use unstructured prose abstracts.
- [x] Verify exact word limit from current MS submission guidelines (reported as 250 in
  guidelines; effective IS practice appears to be 150-200).
  **RESOLVED**: Published abstracts range from 100-250 words of unstructured prose.

---

## Enriched from additional exemplars (2026-06-29)

Sources: 8 published MS papers (Huesmann 2025, Chao/Larkin 2022, Feng 2025, Cui 2025,
Krakowski 2026, de Kok 2025, Chen 2025, Burtch 2026) spanning healthcare management,
marketing, IS, and accounting departments.

### CRITICAL CORRECTION: MS publishes unstructured prose abstracts

The original guide claimed that structured 5-section abstracts are "Management Science's
signature differentiator." This is **incorrect for published papers**. All 8 published MS
papers examined (including final typeset versions with INFORMS copyright, volume, and
issue numbers) use a single unstructured prose paragraph prefixed with "**Abstract.**"
No labeled sub-sections appear in any of them.

The 5-section format (Problem definition / Academic relevance / Methodology / Results /
Managerial implications) may appear in MS author guidelines or in certain departments
(e.g., Operations Research), but it is not applied to the published versions in the IS,
healthcare management, marketing, or accounting departments. Authors submitting to
MS-IS should use unstructured prose abstracts following the patterns below.

### Revised format

One continuous paragraph, prefixed with bold "**Abstract.**" Typical length 120-220 words.
No labeled sub-sections. A Keywords line appears below the abstract, separated by
bullet dots.

### Published abstract arc (implicit, not labeled)

The five conceptual beats from the original guide still appear in the prose, but as
an implicit arc within a single paragraph rather than labeled sections:

1. **Problem/context** (1-2 sentences): Name the phenomenon, market, or technology.
2. **Gap/motivation** (1 sentence): State what is unresolved or contested.
3. **Method** (1-2 sentences): Name the design, data, and identification strategy.
4. **Key findings** (2-4 sentences): State results with direction and magnitude.
5. **Implication** (0-1 sentence): Translate to action. Often omitted or folded into the
   findings sentences.

### Opening sentence patterns (from published papers)

- **Question opening**: "Do pharmacy benefit managers (PBMs) reduce spending on
  prescription drugs?" (Feng 2025)
- **Technology statement**: "Generative large language models (GLLMs), such as ChatGPT
  and GPT-4 by OpenAI, are emerging as powerful tools for textual analysis tasks in
  accounting research." (de Kok 2025)
- **Problem statement**: "Hospital and healthcare administrators name high prescription
  drug costs as one of their largest problems." (Chao/Larkin 2022)
- **Phenomenon + gap**: "Although relative performance feedback in the form of rankings
  appears to be effective in improving health outcomes, it may have either motivating
  or demotivating effects for individual physicians." (Huesmann 2025)
- **Technology + decision**: "Humans and artificial intelligence (AI) algorithms
  increasingly interact on unstructured managerial tasks." (Krakowski 2026)
- **Methodological gap**: "We consider the common setting where one observes a large
  number of opinionated text documents and related covariates..." (Chen 2025)

### Results phrasing in the abstract

Published MS abstracts report specific numbers, not vague findings:

- "...our analysis reveals a 26.08% increase (standard error: 10.3%) in completed tasks
  among developers using the AI tool." (Cui 2025)
- "We show a significant postdisclosure reduction in brand name drug prescriptions by
  Massachusetts physicians, relative to control physicians in other states." (Chao/Larkin 2022)
- "...the most granular ranking system with ranks spanning the entire range of possible
  outcomes maximizes overall physician effort." (Huesmann 2025)
- "The new GPT method achieves an accuracy of 96% and reduces the non-answer error
  rate by 70%..." (de Kok 2025)
- "Counterfactuals suggest that, relative to a market with price-setting by drug
  manufacturers and patients who face coinsurance, PBMs reduce overall spending by 28%,
  without greatly limiting patient access." (Feng 2025)

### Keywords line

All published MS papers include a Keywords line below the abstract, with terms separated
by bullet dots. Examples:

- "**Keywords:** ability . lab-in-the-field experiment . rankings . relative performance
  feedback . status concerns" (Huesmann 2025)
- "**Keywords:** conflicts of interest . disclosure . social image . pharmaceutical
  marketing . detailing" (Chao/Larkin 2022)
- "**Keywords:** drug pricing . industries: pharmaceutical . demand inertia . dynamic
  programming . Markov" (Feng 2025)

### History/Funding/Supplemental block

All published MS papers include a metadata block below the abstract with:
- **History:** "This paper was accepted by [Editor Name], [department]."
- **Funding:** Grant acknowledgments.
- **Supplemental Material:** Link to online appendix and data files at doi.org.

### Revised word budget

| Element | Target | Range |
|---------|--------|-------|
| Full abstract paragraph | 150 w | 100-220 w |
| Keywords line | 4-6 terms | 3-8 terms |

### Healthcare-domain abstract conventions (from Huesmann, Chao/Larkin)

Healthcare MS papers name the clinical context concretely in the abstract:
- Name the specific clinical activity ("adenoma detection rates," "prescriptions for
  262 drugs in nine drug classes")
- Name the provider type ("physicians," "clinical leaders," "pharmaceutical companies")
- Name the policy or intervention ("2009 payment disclosure policy in Massachusetts,"
  "ranking systems")
- State the sample: "5,730 physicians in five states over 48 months" (Chao/Larkin)
- State the design: "controlled lab-in-the-field experiment with practicing and future
  physicians as subjects (N = 352)" (Huesmann)

### LLM/text-analytics abstract conventions (from de Kok, Chen)

Methodological/tool papers use a framework-then-case-study structure:
- State the tool and its potential (1-2 sentences)
- Acknowledge limitations (1 sentence)
- Describe the framework contribution (1-2 sentences)
- Demonstrate with a case study and report performance metrics (2-3 sentences)
- State practical implications for researchers/editors (1 sentence)
