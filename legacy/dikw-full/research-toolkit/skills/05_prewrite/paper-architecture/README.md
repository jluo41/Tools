# Paper Architecture Overview Skill

**Version:** 1.0
**Created:** 2026-02-07

## What Does This Skill Do?

Generates a concise strategic architecture overview (150-300 lines) for academic papers that includes:

- ✅ One-paragraph elevator pitch
- ✅ Key data points with concrete numbers
- ✅ Three main contributions ranked with emphasis %
- ✅ Theoretical and policy implications
- ✅ 5-act storytelling arc for writing
- ✅ Strategic framing guidance (what to emphasize/avoid)
- ✅ Scope and boundaries (what's in/out)
- ✅ Venue-specific positioning

**Purpose:** Strategic decision-making tool for paper writing, NOT a summary.

---

## Quick Start

### Basic Usage:

```bash
/paper-architecture @paper-structure.md
```

The skill will:
1. Auto-detect paper type, venue, contributions, and strategic constraints
2. Generate complete 9-section overview immediately
3. Allow you to refine with conversational comments

### With Context:

```bash
/paper-architecture @paper-structure.md @slides-with-results.pdf

Note: Downplay causality, emphasize measurement innovation.
Target venue: MISQ.
```

### From Scratch:

```bash
/paper-architecture

[Then paste your abstract or describe your paper]
```

---

## What Gets Auto-Detected

The skill automatically infers:

### 1. Paper Type
- **Design Science** - if sees "artifact", "design principles", "instantiation"
- **Pure Theory** - if sees "theoretical framework", "propositions", "mechanisms"
- **Pure Empirical** - if sees "regression", "coefficient", "p<0.05", "N="
- **Hybrid** - if multiple types detected (e.g., Empirical + Artifact)

### 2. Target Venue
- Searches for mentions of "MISQ", "MIS Quarterly", "ISR", "JMIS"
- Defaults to MISQ if not found

### 3. Contributions (Typically 2-4)
- Searches for: "contribution", "we contribute", "our work advances"
- Ranks by text distribution
- Auto-assigns emphasis % (e.g., 40%, 40%, 20%)
- Labels as Primary/Secondary/Tertiary

### 4. Strategic Constraints
- **downplay_causality** - if sees "suggestive", "IV" + "not significant"
- **emphasize_innovation** - if sees "first to", "novel", "unprecedented"
- **acknowledge_incomplete_evidence** - if sees "exploratory", "preliminary"
- **acknowledge_scope_limitations** - if sees "single case", "limited generalizability"

### 5. Key Data Points
- Sample sizes: N=, "226K physicians", "24.7M prescriptions"
- Validation metrics: "kappa", "correlation", "MAE"
- Effect sizes: "β=", "OR=", "coefficient"
- Significance: "***", "p<0.05"
- Consistency: "8/8 positive", "all outcomes"

---

## Output Structure

### 9 Required Sections:

1. **Overall Contribution** - One paragraph (3-5 sentences)
2. **Key Data Points** - Scale, validation, core findings
3. **Three Main Contributions** - Ranked with emphasis %
4. **Theoretical Implications** - 3-5 items (T1-T5)
5. **Policy Implications** - 3-5 items (P1-P5)
6. **Storytelling Arc** - 5 acts in visual boxes
7. **Narrative Strategy** - Language guidance (DO/AVOID)
8. **SCOPE & BOUNDARIES** - What's in/out, limitations vs design choices
9. **Paper Positioning** - Venue-specific framing

---

## Refinement Workflow

After initial generation, you can refine conversationally:

```
> JL: Make artifact contribution 50%, reduce causal to 10%
>> CC: DONE - Updated emphasis to 50/40/10 across all sections

> JL: Add boundary about not testing other Big Five traits
>> CC: DONE - Added to "What Is Out of Scope" section:
       "Other Big Five traits: conscientiousness, neuroticism,
        openness, extraversion not tested (agreeableness focus only)"

> JL: Stronger language avoiding "causality" claims
>> CC: DONE - Updated Section 7 with 3 new AVOID phrases:
       ❌ "We prove causality"
       ❌ "Definitively establish causal effects"
       ❌ "Agreeableness causes overprescription"
```

---

## Examples

See `examples/` directory:

- **`example-empirical-artifact.md`** - Hybrid paper (measurement + empirical + causal)
  - Shows how skill handles incomplete IV evidence
  - Demonstrates downplaying causality while maintaining rigor
  - Illustrates SCOPE & BOUNDARIES section with specific analyses

More examples coming soon:
- Pure theory paper
- Pure design science paper
- Meta-analysis/review paper

---

## Success Criteria

The overview succeeds if you can use it to:

1. ✅ Pitch your paper in 30 seconds (Overall Contribution)
2. ✅ Decide what to emphasize in abstract (Contribution rankings)
3. ✅ Structure your introduction (5-Act Story Arc)
4. ✅ Avoid over-claiming (Language Guidance DO/AVOID)
5. ✅ Position for target venue (Paper Positioning section)
6. ✅ Frame discussion section (Theoretical + Policy Implications)
7. ✅ Make strategic writing decisions (Primary vs Secondary emphasis)

**If you still ask "What should I emphasize?" → Skill failed**
**If you can immediately start writing → Skill succeeded**

---

## Quality Guarantees

Every output includes:

- ✅ Auto-detected configuration shown at top
- ✅ All emphasis % sum to 100%
- ✅ Concrete numbers (not "large" or "significant")
- ✅ Specific analyses in scope/boundaries (not vague)
- ✅ Copy-pasteable language examples (≥3 DO, ≥3 AVOID)
- ✅ Story arc matches contribution emphasis
- ✅ Total length: 150-300 lines (5-minute read)

---

## When to Use This Skill

### ✅ Use When:
- You have results but haven't written the full paper yet
- You need to make strategic decisions about emphasis
- You're positioning for a specific venue (MISQ, MIS, ISR)
- You have evidence limitations (incomplete IV, single case, etc.)
- You want to ensure honest framing of contributions

### ❌ Don't Use When:
- Paper is already written (use for next paper instead)
- You just need a summary (this is a strategic blueprint, not summary)
- You haven't collected data yet (too early)

---

## Common Use Cases

### Use Case 1: "I have incomplete IV evidence, how do I frame it?"
```
/paper-architecture @paper-structure.md

Note: IV results are 2/4 significant, missing first-stage diagnostics.
```

Skill will:
- Auto-detect incomplete evidence
- Position IV as "supplementary" (lower emphasis %)
- Generate language avoiding "proves causality"
- Add to SCOPE & BOUNDARIES: limitations vs design choices

### Use Case 2: "What should I emphasize for MISQ?"
```
/paper-architecture @abstract.md

Target: MISQ
```

Skill will:
- Detect paper type (design science vs empirical vs theory)
- Rank contributions matching MISQ priorities
- Generate venue-specific positioning section
- Adjust language for rigor + relevance balance

### Use Case 3: "I have 3 contributions, how do I rank them?"
```
/paper-architecture @paper-draft.md
```

Skill will:
- Auto-detect contributions from text
- Calculate emphasis % based on evidence strength
- Label as Primary/Secondary/Tertiary
- Ensure story arc matches rankings

---

## Tips for Best Results

1. **Provide detailed source documents**
   - Longer paper structures = better auto-detection
   - Include actual results (not just placeholders)
   - Slides with numbers help extract key data points

2. **Add context in your invocation**
   - Mention strategic constraints: "downplay causality"
   - Specify venue if not in document: "Target: MISQ"
   - Note any emphasis preferences: "emphasize artifact over empirical"

3. **Refine conversationally**
   - Don't expect perfection on first generation
   - Use `> JL:` comments to adjust emphasis, add boundaries, refine language
   - Skill learns from your preferences during refinement

4. **Check auto-detected config**
   - Review the config box at top of output
   - Verify paper type, contributions, and constraints detected correctly
   - Request changes if detection missed something important

---

## Troubleshooting

### "Skill detected wrong paper type"
```
> JL: Actually this is design science + empirical, not pure empirical
>> CC: DONE - Updated paper type to "empirical_with_artifact" and
              rebalanced contribution emphasis to 40% artifact, 40% empirical
```

### "Emphasis % don't match my evidence strength"
```
> JL: IV evidence is weaker, should be 10% not 20%
>> CC: DONE - Adjusted to 45/45/10 distribution; updated all sections
              to reflect tertiary status of causal contribution
```

### "Missing a boundary I want to highlight"
```
> JL: Add to Out of Scope: "Experimental validation not conducted"
>> CC: DONE - Added to "What Is Out of Scope" section with neutral framing
```

---

## Files in This Skill

```
.claude/skills/paper-architecture/
├── README.md                           ← You are here
├── skill.md                            ← Main skill instructions
└── examples/
    ├── example-empirical-artifact.md   ← Hybrid paper example
    ├── example-pure-theory.md          ← Coming soon
    └── example-design-science.md       ← Coming soon
```

---

## Version History

**v1.0** (2026-02-07)
- Initial release
- 9-section structure with auto-detection
- Support for empirical + artifact hybrid papers
- Strategic constraint detection
- Conversational refinement workflow

---

## Feedback & Issues

If the skill generates incorrect outputs or you have suggestions:

1. Use conversational refinement to fix immediate issues
2. Document patterns that consistently fail
3. Share feedback with skill maintainer for improvements

---

## Related Skills

- **`/coding-by-logging`** - For code review and iterative improvement
- **`/paper-structure-planning`** - For detailed paragraph-level paper structures (precedes this skill)

**Workflow:** `/paper-structure-planning` → `/paper-architecture` → Write paper

---

End of README
