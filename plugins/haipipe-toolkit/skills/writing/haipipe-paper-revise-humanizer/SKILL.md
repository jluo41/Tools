---
name: haipipe-paper-revise-humanizer
description: >-
  Remove AI-writing patterns from academic prose while preserving scholarly
  precision, evidence-tied claims, and venue voice. Six-layer audit plus a
  venue-grounded clarity pass; default mode applies fixes directly with %%
  why-comments. Trigger: humanize, de-AI, remove AI tells, academic voice,
  humanizer, /haipipe-paper-revise-humanizer.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  argument_hint: "[section-or-file] [--grant] [--venue <venue>]"
  version: "0.2.6"
  last_updated: "2026-08-05"
  source: "Based on AIScientists-Dev/academic-humanizer (MIT license). Catalog VENDORED at ./ref/pattern-catalog.md (upstream submodule under references/ is provenance only)"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# haipipe-paper-revise-humanizer

Remove AI-writing patterns from academic prose while preserving scholarly precision and voice.
This is a REVISE worker that runs alongside `revise-content` (what sentences say + how paragraphs weave).
This skill reviews HOW sentences sound.

## Reference

The full pattern catalog is VENDORED in this skill: `ref/pattern-catalog.md` (+ `ref/before-after.md` worked examples).
Read it and `ref/venue-sciwrite.md` before every audit pass.
It contains:
- 12+ general AI-tell patterns with before/after examples
- 11 academic-specific AI-tell categories with examples
- Constructs to preserve (hedging, passive voice, citations, numbers)
- Claim-evidence discipline rules
- Voice/venue matching guidance
- Funding-proposal mode (NSF/NIH)

House rule (JL 2026-07-07): skills are SELF-CONTAINED — a SKILL never depends on `references/` content at runtime.
The upstream source (AIScientists-Dev/academic-humanizer, a submodule under `references/`) is archival provenance only; refresh the vendored copy from it deliberately, never point at it from a workflow.

## Six-layer audit

```
Layer  What it checks                         Action
-----  -------------------------------------  -----------------------
  1    General AI-tells                        fix: inflated framing, promotional language,
                                               filler phrases, em-dashes, overlong sentences
  2    Academic AI-tells                       fix: over-claiming verbs, significance hype,
                                               empty intensifiers, novelty padding, formulaic
                                               openers, connective overuse, citation dumping
  3    Preserve legitimate constructs          DO NOT touch: evidence-tied hedging, passive voice,
                                               "we", semicolons, definitions, equations, citations
  4    Claim-evidence discipline               fix: unbacked claims (add evidence or soften),
                                               verb stronger than evidence (downgrade),
                                               vague magnitude (quantify with range)
  5    Voice/venue matching                    match author's prior voice if available;
                                               calibrate to venue register (MISQ: theory-forward;
                                               Nature: terse; JAMA: clinical; grant: vision+feasibility)
  6    Funding-proposal mode (--grant only)    fix: vague importance, method-as-aim,
                                               dominoed aims, ambition without feasibility,
                                               boilerplate broader impacts
```

## Workflow (automatic apply with explanatory comments)

REVISE is fully automatic.
No comment-first, no waiting for human approval.

```
1. READ the section tex or outline. Note venue from S-Venue-0-venue.md.
   If author samples exist (prior papers), read a sample first.
   Read ../../paper/haipipe-paper/ref/prose-quality.md for universal rules.

2. AUDIT + APPLY (in one pass):
   Walk the section sentence by sentence through all 6 layers.
   Fix each finding directly. For non-trivial changes, leave a comment:
     %% {CC-humanizer}: [L1] "delve" replaced with "examines" (AI tell)
     %% {CC-humanizer}: [L2] "extensive experiments" tightened to "three datasets" (empty intensifier)
     %% {CC-humanizer}: [L4] "demonstrates superiority" downgraded to "outperforms" (verb > evidence)

3. SECOND PASS: re-read the cleaned text to catch introduced patterns
   (rewriting sometimes creates new AI-tells)

4. DONE: the comments stay for CHECK to review.
   The human sees what changed and why, can add > USER: to restart if needed.

## Venue-grounded clarity gate

Before applying any language edit, enforce the four gates in `ref/venue-sciwrite.md`:

1. **Meaning invariance:** preserve claims, scope, causal strength, defined terms, numbers, citations, and display references.
2. **Venue fit:** read the owning S page's `## Stage Contract` and its inherited venue-writing contract before using any exemplar shape.
3. **SciWrite clarity:** remove clutter, restore a direct verb where it does not replace a technical term, fix buried predicates, and keep terminology exact.
4. **Human voice:** remove AI tells without deleting legitimate hedging, passive voice, or authorial `we`.

Examples teach the shape of a move, never wording to copy. A candidate that fails any gate is not proposed.

When the author selected candidate-diff mode in `haipipe-paper-revise`, do not change prose directly. Emit the complete candidate in an adjacent `> Note:` lane using the required `~~removed~~` and `**inserted**` notation, model/date suffix, and no-TeX-sync rule defined by that hub.

COMPUTE the diff, never write it by hand: `python3 <skills>/writing/haipipe-writing/cli/wdiff.py record --host paper --old … --new … --when "<YYYY-MM-DD>"` returns the word-level marks already in this host's notation, and `check` audits them (JL 260801, `--host` added 260802). A model asked to show a diff writes a whole-sentence swap, because that is what a diff feels like from the inside. The marks differ between the two hosts (`~old~ *new*` on a board, `~~removed~~ **inserted**` here) and the tool emits both, so pass `--host paper` and convert nothing yourself.

Layer 1 of the pattern catalog now lives at `<skills>/writing/haipipe-writing/ref/ai-tells.md`. It describes how a machine writes in any register, so no paper owns it; Layers 2 to 6 stay in `ref/pattern-catalog.md`.
```

## Key rules from the reference

These are the most important rules.
For the full catalog with examples, read the reference.

### Always remove
- Em-dashes (recast as commas, colons, parentheses, or separate sentences)
- "delve, underscore, intricate, tapestry, testament, landscape (abstract), pivotal, showcase, foster, leverage (filler), realm, seamless"
- "In recent years, X has attracted increasing attention"
- "paves the way for", "sheds light on", "of paramount importance"
- "extensive/comprehensive/thorough experiments"
- "to the best of our knowledge"
- Sentences over ~30 words with 3+ subordinate clauses (compress, don't split)
- Starting consecutive sentences with Moreover/Furthermore/Additionally

### Never remove
- Evidence-tied hedging: "suggests", "is consistent with", "may indicate"
- Passive voice when actor is irrelevant
- "we" (standard academic first-person plural)
- Semicolons in moderation
- Any number, equation, citation, or formal definition

### Claim-evidence rule
Every empirical claim must: (a) be backed by a number/figure/table/citation, (b) have verb strength matching evidence strength.
"Shows" not "proves".
Ranges not point estimates unless method stated.

## Relation to other REVISE workers

```
REVISE phase:
  revise-content     -> WHAT sentences say + HOW paragraphs weave
                        (structure, claims, flow, transitions)
  revise-humanizer   -> HOW sentences sound (AI patterns, voice)  <- THIS
  revise-results     -> results-specific narration

Order (BINDING, not typical): place → content (incl. its weave step) → humanizer → results (if applicable). `place` runs FIRST because substituting landed values after the prose workers would re-open sentences they had already finished — the shipped text would then never have been reviewed in its final form. The hub `haipipe-paper-revise` owns this order; see its SKILL.md.
Content decisions before language cleanup.
```

## Venue-specific calibration

The skill reads the venue from `S-Venue-0-venue.md` and calibrates:
- **MISQ/ISR**: theory-forward, mechanism language OK, moderate hedging
- **Nature/Science**: terse, direct, results-forward
- **JAMA/Lancet**: clinical framing, patient-outcome language
- **Grant (--grant flag)**: vision+feasibility, ambitious verbs OK if backed by evidence

When `--grant` is passed, Layer 6 (funding-proposal mode) activates.
