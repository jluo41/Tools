---
name: haipipe-paper-section-edit-humanizer
description: "Remove AI-writing patterns from academic prose while preserving scholarly precision, evidence-tied claims, and venue-appropriate voice. Six-layer audit: (1) general AI-tells, (2) academic AI-tells, (3) preserve legitimate constructs, (4) claim-evidence discipline, (5) voice/venue matching, (6) funding-proposal mode (conditional). Comment-first: Round 1 inserts audit findings as comments, no prose changes until user confirms. Reads the academic-humanizer reference for the full pattern catalog. POLISH worker alongside edit-content (content decisions) and edit-weaving (paragraph flow). Trigger: humanize, de-AI, remove AI tells, academic voice, humanizer, /haipipe-paper-section-edit-humanizer."
argument-hint: "[section-or-file] [--grant] [--venue <venue>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "1.0.0"
  last_updated: "2026-06-29"
  summary: "De-AI academic prose via 6-layer audit. Comment-first. POLISH worker."
  source: "Based on AIScientists-Dev/academic-humanizer (MIT license). Reference copy at Tools/references/academic-humanizer/"
  changelog:
    - "1.0.0 (2026-06-29): created from academic-humanizer repo. Integrated into POLISH phase of section-edit lifecycle."
---

# haipipe-paper-section-edit-humanizer

Remove AI-writing patterns from academic prose while preserving scholarly
precision and voice. This is a POLISH worker that runs alongside
`edit-content` (what sentences say) and `edit-weaving` (paragraph flow).
This skill reviews HOW sentences sound.

## Reference

The full pattern catalog lives in `Tools/references/academic-humanizer/SKILL.md`.
Read it before every audit pass. It contains:
- 12+ general AI-tell patterns with before/after examples
- 11 academic-specific AI-tell categories with examples
- Constructs to preserve (hedging, passive voice, citations, numbers)
- Claim-evidence discipline rules
- Voice/venue matching guidance
- Funding-proposal mode (NSF/NIH)

Path: `../../../../references/academic-humanizer/SKILL.md`
(from this skill's location: `2-section-edit/polish/haipipe-paper-section-edit-humanizer/`)

## Six-layer audit

```
Layer  What it checks                         Action
─────  ─────────────────────────────────────  ─────────────────────────
  1    General AI-tells                        flag: inflated framing, promotional language,
                                               filler phrases, em-dashes, overlong sentences
  2    Academic AI-tells                       flag: over-claiming verbs, significance hype,
                                               empty intensifiers, novelty padding, formulaic
                                               openers, connective overuse, citation dumping
  3    Preserve legitimate constructs          DO NOT flag: evidence-tied hedging, passive voice,
                                               "we", semicolons, definitions, equations, citations
  4    Claim-evidence discipline               flag: unbacked claims (add evidence or soften),
                                               verb stronger than evidence (downgrade),
                                               vague magnitude (quantify with range)
  5    Voice/venue matching                    match author's prior voice if available;
                                               calibrate to venue register (MISQ: theory-forward;
                                               Nature: terse; JAMA: clinical; grant: vision+feasibility)
  6    Funding-proposal mode (--grant only)    flag: vague importance, method-as-aim,
                                               dominoed aims, ambition without feasibility,
                                               boilerplate broader impacts
```

## Workflow (comment-first)

```
1. READ the section tex or outline. Note venue from STATUS.md.
   If author samples exist (prior papers), read a sample first.

2. AUDIT (no editing):
   Read the full academic-humanizer reference (Tools/references/academic-humanizer/SKILL.md).
   Walk the section sentence by sentence through all 6 layers.
   For each finding, insert a comment:
     %% {CC-humanizer-vMMDD}: [L1] "delve" → AI tell, replace with plain verb
     %% {CC-humanizer-vMMDD}: [L2] "extensive experiments" → empty intensifier, specify datasets
     %% {CC-humanizer-vMMDD}: [L4] "demonstrates superiority" → verb outpaces evidence, downgrade

3. REPORT to user:
   - Count of findings by layer (L1: 5, L2: 3, L4: 2, etc.)
   - Worst offenders (sentences with 2+ flags)
   - Voice observations (matches venue? matches author?)

4. WAIT for user ========> replies (accept/reject/modify per comment)

5. APPLY accepted changes only. Never alter:
   - Numbers, equations, citations, or \citep{} keys
   - Content decisions (those are edit-content's job)
   - Paragraph structure (that's edit-weaving's job)

6. SECOND PASS: re-read the cleaned text to catch introduced patterns
   (rewriting sometimes creates new AI-tells)
```

## Key rules from the reference

These are the most important rules. For the full catalog with examples, read the reference.

### Always remove
- Em-dashes (recast as commas, colons, parentheses, or separate sentences)
- "delve, underscore, intricate, tapestry, testament, landscape (abstract), pivotal, showcase, foster, leverage (filler), realm, seamless"
- "In recent years, X has attracted increasing attention"
- "paves the way for", "sheds light on", "of paramount importance"
- "extensive/comprehensive/thorough experiments"
- "to the best of our knowledge"
- Sentences over ~30 words with 3+ subordinate clauses (split)
- Starting consecutive sentences with Moreover/Furthermore/Additionally

### Never remove
- Evidence-tied hedging: "suggests", "is consistent with", "may indicate"
- Passive voice when actor is irrelevant
- "we" (standard academic first-person plural)
- Semicolons in moderation
- Any number, equation, citation, or formal definition

### Claim-evidence rule
Every empirical claim must: (a) be backed by a number/figure/table/citation, (b) have verb strength matching evidence strength. "Shows" not "proves". Ranges not point estimates unless method stated.

## Relation to other POLISH workers

```
POLISH phase:
  edit-content     → WHAT sentences say (structure, claims, flow)
  edit-humanizer   → HOW sentences sound (AI patterns, voice)  ← THIS
  edit-weaving     → HOW paragraphs flow (transitions, rhythm)
  edit-write       → fresh draft from outline (cold start)

Typical order: edit-content first, then edit-humanizer, then edit-weaving.
Content decisions before language polish before paragraph flow.
```

## Venue-specific calibration

The skill reads the venue from `STATUS.md` and calibrates:
- **MISQ/ISR**: theory-forward, mechanism language OK, moderate hedging
- **Nature/Science**: terse, direct, results-forward
- **JAMA/Lancet**: clinical framing, patient-outcome language
- **Grant (--grant flag)**: vision+feasibility, ambitious verbs OK if backed by evidence

When `--grant` is passed, Layer 6 (funding-proposal mode) activates.
