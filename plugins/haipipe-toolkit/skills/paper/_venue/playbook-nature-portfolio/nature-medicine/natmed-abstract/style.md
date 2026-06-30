# Nature Medicine Abstract -- Section Style Guide

Extracted from 14 Nature Medicine exemplar papers (2025-2026). Supplements `style-profile.md`.

## Word budget

- 150-350 words. Median ~200 words for Articles; Brief Communications similar.
- bean-2026: ~200w. brinton-2026: ~200w. saab-2026: ~250w. levine-2026: ~200w. varoquaux-2026: ~350w. restrepo-2026: ~180w. vaidya-2026: ~200w. yao-2026: ~200w.
- Unstructured single paragraph. No labeled sub-fields (no "Background / Methods / Results / Conclusions" headers). Never bulleted or numbered.
- Clinical trial papers (RCTs) may run longer (~250-350w) because they must include trial registration numbers and specific primary outcome statistics.

## Arc

```
clinical problem / unmet need (why this matters to patients)
  -> gap or limitation (what evidence is missing, what was not tested)
  -> "Here we..." contribution pivot (name the study type + system/intervention)
  -> study design + scale (n, sites, comparators)
  -> key results (primary outcome with effect size, CI, P)
  -> clinical significance / implications close
  -> (RCTs only) trial registration number as final sentence
```

The arc is **patient-forward, evidence-centered**. Unlike NMI which leads with technical capability, Nature Medicine leads with the clinical problem and frames the contribution as evidence generation, not system building.

## Signature moves

1. **Clinical problem opening.** The first sentence establishes why the clinical problem matters to patients, not what the AI/method does:
   - "Global healthcare providers are exploring the use of large language models (LLMs) to provide medical advice to the public." [bean-2026]
   - "Real-world clinical practice is inherently multimodal, relying on the synthesis of patient history with visual information such as medical imagery and clinical documents." [saab-2026]
   - "Rigorous evidence on the performance of large language models (LLMs) in real-world, low-resource clinical settings remains limited." [brinton-2026]
   - "Prioritizing artificial intelligence (AI)-detected imaging findings may reduce the time to diagnosis of lung cancer." [varoquaux-2026]
   - "Specialized clinical artificial intelligence (AI) tools are entering medical practice despite scarce independent evaluation." [restrepo-2026]

2. **"Here we..." pivot names the study design, not just the system.** Nature Medicine pivots to the study, not the tool:
   - "Here we conducted a pragmatic, cluster-randomized trial in 16 primary care facilities in Kenya." [brinton-2026]
   - "We tested whether LLMs can assist members of the public in identifying underlying conditions and choosing a course of action (disposition) in ten medical scenarios in a controlled study with 1,298 participants." [bean-2026]
   - "Here we introduce a multimodal extension of the Articulate Medical Intelligence Explorer (multimodal AMIE)..." [saab-2026]
   - "We quantitatively evaluate two clinical AI tools, OpenEvidence and UpToDate Expert AI, built on large language models (LLMs) against three frontier LLMs..." [restrepo-2026]

3. **Primary outcome with full statistical reporting in abstract.** Unlike NMI which gives directional claims, Nature Medicine abstracts include specific effect sizes, CIs, and P values:
   - "Treatment failure occurred in 102/4,693 patients (2.2%) in the intervention arm and 94/4,654 (2.0%) in the control arm (adjusted odds ratio 0.77, 95% confidence interval 0.55 to 1.08, P = 0.13)." [brinton-2026]
   - "Median (interquartile range) times to CT were 53 days (17-145) and 53 days (19-141), with and without AI prioritization, corresponding to a ratio of geometric means of 0.97 (95% confidence interval (CI) = 0.93-1.02; P = 0.31)." [varoquaux-2026]
   - "participants identified relevant conditions in fewer than 34.5% of cases and disposition in fewer than 44.2%, both no better than the control group." [bean-2026]

4. **Trial registration as closing sentence (RCTs only).** Clinical trials end the abstract with the registration identifier:
   - "Pan-African Clinical Trials Registry: 202502499779176." [brinton-2026]
   - "ISRCTN registration: 78987039." [varoquaux-2026]

5. **Null results stated plainly.** Nature Medicine does not spin negative results; they are reported directly:
   - "The primary outcome did not differ significantly between groups." [brinton-2026]
   - "AI prioritization of CXR requested by UK primary care has no significant impact on the lung cancer pathway." [varoquaux-2026]
   - "In this trial, LLM assistance was safe but did not reduce treatment failure within 14 days and any benefit, if present, is probably modest." [brinton-2026]

6. **Close on clinical implication or recommendation, not the method.** The penultimate or final sentence (before trial registration) states what clinicians or policymakers should do:
   - "Moving forward, we recommend systematic human user testing to evaluate interactive capabilities before public deployments in healthcare." [bean-2026]
   - "CXR AI deployments should not include worklist prioritization in this context." [varoquaux-2026]
   - "These findings highlight the need for independent, real-world evaluation of AI tools before they enter clinical settings." [restrepo-2026]

## Exemplar sentences (shape, not content)

**Opening move** (clinical problem first):
- "Global healthcare providers are exploring the use of large language models (LLMs) to provide medical advice to the public." [bean-2026]
- "Real-world clinical practice is inherently multimodal, relying on the synthesis of patient history with visual information such as medical imagery and clinical documents." [saab-2026]
- "Rigorous evidence on the performance of large language models (LLMs) in real-world, low-resource clinical settings remains limited." [brinton-2026]

**Gap sentence**:
- "LLMs now achieve nearly perfect scores on medical licensing exams, but this does not necessarily translate to accurate performance in real-world settings." [bean-2026]
- "Although large language models (LLMs) have shown promise in diagnostic dialogue, their evaluation has been largely restricted to text-only interactions, failing to capture the complexity of modern remote care delivery." [saab-2026]

**Findings sentence** (clinical outcome with statistics):
- "Treatment failure occurred in 102/4,693 patients (2.2%) in the intervention arm and 94/4,654 (2.0%) in the control arm (adjusted odds ratio 0.77, 95% confidence interval 0.55 to 1.08, P = 0.13)." [brinton-2026]
- "multimodal AMIE demonstrated superior performance on 29 of 32 evaluation axes, including seven of nine metrics that assess multimodal reasoning." [saab-2026]

## Anti-patterns

- Do NOT use structured/labeled fields (Background, Methods, Results, Conclusions). Nature Medicine uses one unstructured paragraph.
- Do NOT open with the method or system name. Open with the clinical problem or unmet need.
- Do NOT omit effect sizes and CIs from the abstract when reporting a clinical trial. Nature Medicine expects specific numbers.
- Do NOT end on the method. End on clinical implications, a recommendation, or trial registration.
- Do NOT spin null results. State them plainly and let the reader judge.
- Do NOT use passive-heavy construction. Nature Medicine abstracts mix active voice ("We tested", "We conducted", "Here we introduce") with result statements.
- Do NOT include detailed methods (regression specifications, model architectures) in the abstract. State the study type and scale.

## Paragraph structure

One paragraph only. No line breaks, no sub-sections, no bullet lists.

Sentence count: 8-15 sentences following this pattern:
1. Clinical problem / unmet need (1-2 sentences)
2. Gap or limitation of current evidence (1 sentence)
3. "Here we..." contribution pivot + study design (1 sentence)
4. Study scale and comparators (1-2 sentences)
5. Primary outcome with statistics (1-3 sentences)
6. Secondary outcomes or key secondary findings (1-2 sentences)
7. Clinical significance / recommendations (1 sentence)
8. Trial registration (1 sentence, RCTs only)

## Contrast with NMI

- NMI abstracts name a system and its capability. Nature Medicine abstracts name a clinical study and its findings.
- NMI abstracts give directional claims ("outperforms", "achieves"). Nature Medicine abstracts give specific effect sizes with CIs and P values.
- NMI abstracts never include p-values or CIs. Nature Medicine regularly does.
- NMI closes on broad applicability of the system. Nature Medicine closes on clinical recommendations or policy implications.
- NMI never includes trial registration numbers. Nature Medicine does for RCTs.
- NMI abstracts run 160-270 words. Nature Medicine Articles run 150-350 words (RCTs are longer).
- NMI opens with domain importance (broad). Nature Medicine opens with specific clinical problem (narrower, patient-facing).
