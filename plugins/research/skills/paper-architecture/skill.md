# Paper Architecture Overview Generator

**Version:** 2.0
**Created:** 2026-02-07
**Updated:** 2026-02-08
**Purpose:** Generate concise strategic architecture overviews for academic papers in Markdown or LaTeX format

---

## Overview

This skill generates a high-level paper architecture overview document (150-300 lines) that distills:
- Overall contribution in one paragraph
- Key data points and metrics
- Three main contributions with emphasis percentages
- Theoretical and policy implications
- 5-act storytelling arc
- Strategic framing guidance (what to emphasize/downplay)
- Scope and boundaries (what's in/out)
- Venue positioning

**Output Formats:**
- **Markdown** (`.md`): For collaboration, version control, and quick reference
- **LaTeX** (`.tex`): For integration into academic papers, with proper formatting and compilation support

**Target Output:** Ready-to-use strategic blueprint for writing the paper in your preferred format.

---

## Invocation

### Simple Usage (Auto-detect from file extension):
```
/paper-architecture @00-incubator-paper.tex
→ Outputs LaTeX format

/paper-architecture @paper-structure.md
→ Outputs Markdown format
```

### With Additional Context:
```
/paper-architecture @00-incubator-paper.tex @slides.pdf

Note: Downplay causality claims, emphasize measurement innovation.
Target venue: MISQ.
→ Outputs LaTeX format (detected from .tex extension)
```

### Override Auto-Detection:
```
/paper-architecture @paper.tex --format markdown
→ Forces Markdown output despite .tex input

/paper-architecture @paper.md --format latex
→ Forces LaTeX output despite .md input
```

### From Scratch (No File Provided):
```
/paper-architecture

[Paste abstract or provide paper description]
→ Defaults to Markdown format
```

**Format Detection Logic:**
- **Primary:** File extension of input file (`.tex` → LaTeX, `.md` → Markdown)
- **Override:** Explicit `--format` flag or `Format:` in message
- **Default:** Markdown (when no file provided)

---

## Workflow

### Step 0: Format Detection (Silent)

**Detect Output Format (Priority Order):**

1. **Check file extension of primary input file:**
   - If user provides `@file.tex` → **LaTeX format**
   - If user provides `@file.md` → **Markdown format**
   - This is the PRIMARY detection method

2. **Check for explicit format request:**
   - `--format latex` or `Format: LaTeX` in user message → **LaTeX format**
   - `--format markdown` or `Format: Markdown` in user message → **Markdown format**

3. **Default fallback:**
   - If no file provided and no explicit format → **Markdown format**

**Format-Specific Settings:**
- **Markdown**: Use standard markdown with boxes (┌─┐ style)
- **LaTeX**: Use appropriate LaTeX environments and commands

**Examples:**
- `/paper-architecture @00-incubator-paper.tex` → Outputs LaTeX
- `/paper-architecture @paper-structure.md` → Outputs Markdown
- `/paper-architecture @slides.pdf @paper.tex` → Outputs LaTeX (first recognized format file)
- `/paper-architecture --format markdown @paper.tex` → Outputs Markdown (explicit override)

### Step 1: Auto-Detect (Silent)

**Detect Paper Type:**
- Look for: "design principles", "artifact", "instantiation" → Design Science
- Look for: "theoretical framework", "propositions", "mechanisms" → Theory
- Look for: "regression", "coefficient", "p<0.05", "N=" → Empirical
- If multiple found → Hybrid (rank by text distribution)

**Detect Venue:**
- Search for: "MISQ", "Management Information Systems Quarterly"
- Check mentions of: "MIS Quarterly", "ISR", "JMIS"
- If not found → Default: MISQ

**Detect Contributions:**
- Search for: "contribution", "we contribute", "our work advances"
- Extract: List of claimed contributions (typically 2-4)
- Rank by: Frequency of mention, text devoted to each
- Auto-assign emphasis %: Based on paragraph distribution

**Detect Strategic Constraints:**
- If sees: "suggestive", "exploratory", "preliminary", "not definitive"
  → Add: `acknowledge_incomplete_evidence`
- If sees: "IV" + "not significant" OR "2/4 outcomes" OR "NS"
  → Add: `downplay_causality`
- If sees: "artifact", "first to", "novel", "unprecedented"
  → Add: `emphasize_innovation`
- If sees: "single case", "one context", "limited generalizability"
  → Add: `acknowledge_scope_limitations`

**Extract Key Data Points:**
- Sample sizes: N=, "226,146 physicians", "24.7M prescriptions"
- Costs: "$X per unit", "~$0.10 per physician"
- Validation metrics: "kappa", "correlation", "MAE", "RMSE"
- Effect sizes: "β=", "OR=", "coefficient"
- Significance: "*", "**", "***", "p<0.05"
- Consistency patterns: "8/8 positive", "all outcomes"

### Step 2: Generate Complete Overview

**Format Selection:** Use the format detected in Step 0 (based on input file extension or explicit override).

#### A. Markdown Output Format (for .md input files)

```markdown
Session 1: Paper Architecture Overview (YYYY-MM-DD HH:MM)
==========================================================

Location: Generated from [input files]
Status: ✅ Auto-detected configuration
Format: Markdown (from input file extension)

Auto-Detected Configuration:
┌─────────────────────────────────────────────────────────┐
│ Paper Type: [detected type]                             │
│ Target Venue: [detected venue]                          │
│ Contributions Detected: [N]                             │
│   - C1: [title] (Primary/Secondary/Tertiary, X%)        │
│   - C2: [title] (Primary/Secondary/Tertiary, Y%)        │
│   - C3: [title] (Primary/Secondary/Tertiary, Z%)        │
│ Strategic Constraints:                                  │
│   - [constraint_1] (detected from "[evidence]")         │
│   - [constraint_2] (detected from "[evidence]")         │
│ Key Metrics Extracted:                                  │
│   - [metric 1]                                          │
│   - [metric 2]                                          │
└─────────────────────────────────────────────────────────┘


OVERALL CONTRIBUTION: One-Paragraph Summary
============================================

[3-5 sentences combining: scale + innovation + findings + implications]


KEY DATA POINTS
===============

**Scale:**
- [N samples, N datapoints, timeframe, cost]

**Validation:**
- [Reliability metrics, correlations, benchmarks]

**Core Findings:**
- [Effect sizes with significance, consistency patterns]


THREE MAIN CONTRIBUTIONS
=========================

**C1: [Title] (Primary/Secondary/Tertiary, X%)**
- [Key point 1]
- [Key point 2]
- [Key point 3]
[Max 5 bullets per contribution]

**C2: [Title] (Primary/Secondary/Tertiary, Y%)**
- [Key point 1]
- [Key point 2]

**C3: [Title] (Primary/Secondary/Tertiary, Z%)**
- [Key point 1]
- [Key point 2]


THEORETICAL IMPLICATIONS
=========================

**T1: [Implication Title]**
- [Why this matters for theory]
- [Connection to literature]
[Max 3 bullets per implication, 3-5 implications total]

**T2: [Implication Title]**
- [Why this matters]

**T3: [Implication Title]**
- [Why this matters]


POLICY IMPLICATIONS
===================

**P1: [Policy Title]**
- [Actionable recommendation 1]
- [Actionable recommendation 2]
[Max 3 bullets per implication, 3-5 implications total]

**P2: [Policy Title]**
- [Actionable recommendation]

**P3: [Policy Title]**
- [Actionable recommendation]


STORYTELLING ARC
================

**Act 1: Problem & Gap**
┌─────────────────────────────────────────────────────────┐
│ [Problem statement, 1-2 lines]                          │
│ [Gap in current approaches, 1-2 lines]                  │
└─────────────────────────────────────────────────────────┘

**Act 2: Innovation**
┌─────────────────────────────────────────────────────────┐
│ [Method/artifact innovation, 2-3 lines]                 │
└─────────────────────────────────────────────────────────┘

**Act 3: Discovery**
┌─────────────────────────────────────────────────────────┐
│ [Key findings, 2-3 lines with numbers]                  │
└─────────────────────────────────────────────────────────┘

**Act 4: Mechanism**
┌─────────────────────────────────────────────────────────┐
│ [Why/how findings occur, 2-3 lines]                     │
└─────────────────────────────────────────────────────────┘

**Act 5: Impact**
┌─────────────────────────────────────────────────────────┐
│ [Theory + policy + future research, 2-3 lines]          │
└─────────────────────────────────────────────────────────┘


NARRATIVE STRATEGY
==================

**Primary Story (X% emphasis):**
"[Headline capturing primary contribution]"

**Supporting Evidence (Y% emphasis):**
"[Headline capturing secondary contribution]"

**Language to Use:**
- ✅ "[Example phrase matching strategic constraints]"
- ✅ "[Example phrase 2]"
- ✅ "[Example phrase 3]"

**Language to Avoid:**
- ❌ "[Over-claiming phrase to avoid]"
- ❌ "[Over-claiming phrase 2]"
- ❌ "[Over-claiming phrase 3]"


SCOPE & BOUNDARIES
==================

What We Deliver
---------------
- [Deliverable 1 with concrete metrics]
- [Deliverable 2 with concrete metrics]
- [Deliverable 3 with concrete metrics]
[Max 5 items, each with numbers/evidence]

What Is Out of Scope
---------------------
- [Specific analysis/claim not made]: [why out of scope]
- [Specific population/context]: [why excluded]
- [Specific methodology]: [why not conducted]
[Max 5 items, neutral framing]

Limitations vs Design Choices
------------------------------

**Acknowledged Limitations:**
- [Limitation 1]: [what's missing and impact]
- [Limitation 2]: [what's missing]
[Items that weaken claims]

**Intentional Design Choices:**
- [Choice 1]: [why this scope is appropriate]
- [Choice 2]: [justification]
[Items that reflect strategic decisions]

**Rationale:** [1-2 sentences connecting to contribution emphasis %]

Future Work Prioritization
---------------------------

**High Priority** (strengthen current claims):
- [Item 1]: [what it would add to current paper]
- [Item 2]: [what it would address]

**Medium Priority** (extend scope):
- [Item 1]: [what new contexts it would enable]
- [Item 2]: [what new questions it would answer]

**Low Priority** (aspirational):
- [Item 1]: [long-term research agenda]


PAPER POSITIONING FOR [VENUE]
==============================

**Primary Contribution:** [Type] (X%)
- [Why this fits venue priorities]
- [Unique value proposition]

**Secondary Contribution:** [Type] (Y%)
- [Why this fits venue]

**Tertiary Contribution:** [Type] (Z%)
- [Why this fits venue]
- [Caveat if needed]


===================================================================

End of Architecture Overview

> JL: [Space for user refinement comments]
```

#### B. LaTeX Output Format (for .tex input files)

For LaTeX output, use the following structure:

```latex
% Paper Architecture Overview
% Generated: YYYY-MM-DD HH:MM
% Location: [input files]
% Status: Auto-detected configuration
% Format: LaTeX (from input file extension)

\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{xcolor}
\usepackage{enumitem}
\usepackage{tcolorbox}
\usepackage{titlesec}

% Custom formatting
\definecolor{headerblue}{RGB}{0,102,204}
\titleformat{\section}{\Large\bfseries\color{headerblue}}{\thesection}{1em}{}
\titleformat{\subsection}{\large\bfseries}{\thesubsection}{1em}{}

\begin{document}

\title{\textbf{Paper Architecture Overview}}
\date{Generated: \today}
\author{Session 1}
\maketitle

\begin{tcolorbox}[colback=blue!5!white,colframe=blue!75!black,title=Auto-Detected Configuration]
\begin{itemize}[leftmargin=*,nosep]
    \item \textbf{Paper Type:} [detected type]
    \item \textbf{Target Venue:} [detected venue]
    \item \textbf{Contributions Detected:} [N]
    \begin{itemize}[nosep]
        \item C1: [title] (Primary/Secondary/Tertiary, X\%)
        \item C2: [title] (Primary/Secondary/Tertiary, Y\%)
        \item C3: [title] (Primary/Secondary/Tertiary, Z\%)
    \end{itemize}
    \item \textbf{Strategic Constraints:}
    \begin{itemize}[nosep]
        \item [constraint\_1] (detected from ``[evidence]'')
        \item [constraint\_2] (detected from ``[evidence]'')
    \end{itemize}
    \item \textbf{Key Metrics Extracted:}
    \begin{itemize}[nosep]
        \item [metric 1]
        \item [metric 2]
    \end{itemize}
\end{itemize}
\end{tcolorbox}

\section{Overall Contribution: One-Paragraph Summary}

[3-5 sentences combining: scale + innovation + findings + implications]

\section{Key Data Points}

\subsection*{Scale:}
\begin{itemize}[nosep]
    \item [N samples, N datapoints, timeframe, cost]
\end{itemize}

\subsection*{Validation:}
\begin{itemize}[nosep]
    \item [Reliability metrics, correlations, benchmarks]
\end{itemize}

\subsection*{Core Findings:}
\begin{itemize}[nosep]
    \item [Effect sizes with significance, consistency patterns]
\end{itemize}

\section{Three Main Contributions}

\subsection*{C1: [Title] (Primary/Secondary/Tertiary, X\%)}
\begin{itemize}[nosep]
    \item [Key point 1]
    \item [Key point 2]
    \item [Key point 3]
\end{itemize}

\subsection*{C2: [Title] (Primary/Secondary/Tertiary, Y\%)}
\begin{itemize}[nosep]
    \item [Key point 1]
    \item [Key point 2]
\end{itemize}

\subsection*{C3: [Title] (Primary/Secondary/Tertiary, Z\%)}
\begin{itemize}[nosep]
    \item [Key point 1]
    \item [Key point 2]
\end{itemize}

\section{Theoretical Implications}

\subsection*{T1: [Implication Title]}
\begin{itemize}[nosep]
    \item [Why this matters for theory]
    \item [Connection to literature]
\end{itemize}

\subsection*{T2: [Implication Title]}
\begin{itemize}[nosep]
    \item [Why this matters]
\end{itemize}

\subsection*{T3: [Implication Title]}
\begin{itemize}[nosep]
    \item [Why this matters]
\end{itemize}

\section{Policy Implications}

\subsection*{P1: [Policy Title]}
\begin{itemize}[nosep]
    \item [Actionable recommendation 1]
    \item [Actionable recommendation 2]
\end{itemize}

\subsection*{P2: [Policy Title]}
\begin{itemize}[nosep]
    \item [Actionable recommendation]
\end{itemize}

\subsection*{P3: [Policy Title]}
\begin{itemize}[nosep]
    \item [Actionable recommendation]
\end{itemize}

\section{Storytelling Arc}

\begin{tcolorbox}[colback=green!5!white,colframe=green!75!black,title=Act 1: Problem \& Gap]
[Problem statement, 1-2 lines]

[Gap in current approaches, 1-2 lines]
\end{tcolorbox}

\begin{tcolorbox}[colback=blue!5!white,colframe=blue!75!black,title=Act 2: Innovation]
[Method/artifact innovation, 2-3 lines]
\end{tcolorbox}

\begin{tcolorbox}[colback=orange!5!white,colframe=orange!75!black,title=Act 3: Discovery]
[Key findings, 2-3 lines with numbers]
\end{tcolorbox}

\begin{tcolorbox}[colback=purple!5!white,colframe=purple!75!black,title=Act 4: Mechanism]
[Why/how findings occur, 2-3 lines]
\end{tcolorbox}

\begin{tcolorbox}[colback=red!5!white,colframe=red!75!black,title=Act 5: Impact]
[Theory + policy + future research, 2-3 lines]
\end{tcolorbox}

\section{Narrative Strategy}

\subsection*{Primary Story (X\% emphasis):}
``[Headline capturing primary contribution]''

\subsection*{Supporting Evidence (Y\% emphasis):}
``[Headline capturing secondary contribution]''

\subsection*{Language to Use:}
\begin{itemize}[nosep]
    \item[\checkmark] ``[Example phrase matching strategic constraints]''
    \item[\checkmark] ``[Example phrase 2]''
    \item[\checkmark] ``[Example phrase 3]''
\end{itemize}

\subsection*{Language to Avoid:}
\begin{itemize}[nosep]
    \item[$\times$] ``[Over-claiming phrase to avoid]''
    \item[$\times$] ``[Over-claiming phrase 2]''
    \item[$\times$] ``[Over-claiming phrase 3]''
\end{itemize}

\section{Scope \& Boundaries}

\subsection{What We Deliver}
\begin{itemize}[nosep]
    \item [Deliverable 1 with concrete metrics]
    \item [Deliverable 2 with concrete metrics]
    \item [Deliverable 3 with concrete metrics]
\end{itemize}

\subsection{What Is Out of Scope}
\begin{itemize}[nosep]
    \item [Specific analysis/claim not made]: [why out of scope]
    \item [Specific population/context]: [why excluded]
    \item [Specific methodology]: [why not conducted]
\end{itemize}

\subsection{Limitations vs Design Choices}

\subsubsection*{Acknowledged Limitations:}
\begin{itemize}[nosep]
    \item [Limitation 1]: [what's missing and impact]
    \item [Limitation 2]: [what's missing]
\end{itemize}

\subsubsection*{Intentional Design Choices:}
\begin{itemize}[nosep]
    \item [Choice 1]: [why this scope is appropriate]
    \item [Choice 2]: [justification]
\end{itemize}

\textbf{Rationale:} [1-2 sentences connecting to contribution emphasis \%]

\subsection{Future Work Prioritization}

\subsubsection*{High Priority (strengthen current claims):}
\begin{itemize}[nosep]
    \item [Item 1]: [what it would add to current paper]
    \item [Item 2]: [what it would address]
\end{itemize}

\subsubsection*{Medium Priority (extend scope):}
\begin{itemize}[nosep]
    \item [Item 1]: [what new contexts it would enable]
    \item [Item 2]: [what new questions it would answer]
\end{itemize}

\subsubsection*{Low Priority (aspirational):}
\begin{itemize}[nosep]
    \item [Item 1]: [long-term research agenda]
\end{itemize}

\section{Paper Positioning for [VENUE]}

\subsection*{Primary Contribution: [Type] (X\%)}
\begin{itemize}[nosep]
    \item [Why this fits venue priorities]
    \item [Unique value proposition]
\end{itemize}

\subsection*{Secondary Contribution: [Type] (Y\%)}
\begin{itemize}[nosep]
    \item [Why this fits venue]
\end{itemize}

\subsection*{Tertiary Contribution: [Type] (Z\%)}
\begin{itemize}[nosep]
    \item [Why this fits venue]
    \item [Caveat if needed]
\end{itemize}

\vspace{1cm}
\hrule
\vspace{0.5cm}

\textit{End of Architecture Overview}

\vspace{0.5cm}
\textbf{User Refinement Comments:}

% JL: [Space for user refinement comments]

\end{document}
```

### Step 3: User Refinement (Conversational)

Wait for user to add refinement comments using `> JL:` format.

**User can request:**
- Change emphasis percentages: `> JL: Make artifact 50%, reduce causal to 10%`
- Add boundaries: `> JL: Add boundary about not testing other Big Five traits`
- Adjust language: `> JL: Stronger emphasis on "supplementary evidence"`
- Modify sections: `> JL: Add policy implication about medical education`

**Respond with `>> CC:`:**
- Start with action: DONE, UPDATED, ADDED
- Be specific: state what changed (1-2 sentences)
- Update relevant sections accordingly

### Step 4: Finalize

After refinements complete, save with appropriate extension and confirm:

**For Markdown:**
```
>> CC: Architecture overview finalized. Saved to:
       code-logging/0-paper-architecture-overview.md
```

**For LaTeX:**
```
>> CC: Architecture overview finalized. Saved to:
       code-logging/0-paper-architecture-overview.tex
```

**File naming convention:**
- Markdown: `0-paper-architecture-overview.md`
- LaTeX: `0-paper-architecture-overview.tex`
- Location: `code-logging/` or user-specified directory

---

## Output Requirements

### Format Selection:
- ✅ Output format matches input file extension (`.tex` → LaTeX, `.md` → Markdown)
- ✅ Format explicitly shown in generated document header
- ✅ Can be overridden with `--format` flag if needed

### Structure (Both Formats):
- ✅ All 9 sections present
- ✅ Auto-detected config shown at top
- ✅ Total length: 150-300 lines (excluding LaTeX preamble)
- ✅ Each contribution: ≤5 bullets
- ✅ Each implication: ≤3 bullets
- ✅ Emphasis % sum to 100%

### Format-Specific:

**Markdown:**
- ✅ Use unicode box characters (┌─┐│└┘) for visual boxes
- ✅ Use `**bold**` and `*italic*` for emphasis
- ✅ Use `- ` for bullets and `  - ` for sub-bullets
- ✅ Use `✅` and `❌` for visual indicators

**LaTeX:**
- ✅ Use `tcolorbox` for visual boxes (5-act arc)
- ✅ Use `\textbf{}` and `\textit{}` for emphasis
- ✅ Use `\begin{itemize}[nosep]` for compact lists
- ✅ Use `\checkmark` and `$\times$` for visual indicators
- ✅ Escape special characters: `\%`, `\_`, `\&`, `\#`, `\$`
- ✅ Include complete LaTeX preamble with required packages
- ✅ Use `\subsection*{}` for unnumbered subsections
- ✅ Color-coded tcolorboxes for 5-act storytelling arc

### Content:
- ✅ Concrete numbers (not "large" or "significant")
- ✅ Specific analyses in scope/boundaries (not vague)
- ✅ Copy-pasteable language examples (≥3 DO, ≥3 AVOID)
- ✅ Story arc matches contribution emphasis
- ✅ Neutral tone in "Out of Scope" section

### Strategic Value:
- ✅ Emphasis % reflect evidence strength
- ✅ Language guidance addresses actual over-claiming risks
- ✅ Venue positioning explains fit with journal priorities
- ✅ Honest about limitations vs design choices

---

## Auto-Detection Rules

### Format Detection:

```python
# Pseudo-code for format detection logic

def detect_output_format(user_message, attached_files):
    # Priority 1: Check explicit format override
    if "--format latex" in user_message or "Format: LaTeX" in user_message:
        return "latex"
    if "--format markdown" in user_message or "Format: Markdown" in user_message:
        return "markdown"

    # Priority 2: Check file extension of primary input file
    for file in attached_files:
        if file.endswith('.tex'):
            return "latex"
        if file.endswith('.md'):
            return "markdown"

    # Priority 3: Default
    return "markdown"
```

**Key Principle:** The format follows the source document format unless explicitly overridden.

### Paper Type Classification:

```python
# Pseudo-code for detection logic

if contains("design principles", "artifact", "instantiation"):
    if contains("regression", "p<0.05", "coefficient"):
        type = "empirical_with_artifact"  # Hybrid
    else:
        type = "design_science"  # Pure DS

elif contains("theoretical framework", "propositions", "mechanisms"):
    if contains("hypothesis", "regression", "empirical"):
        type = "theory_with_empirical"  # Hybrid
    else:
        type = "pure_theory"

elif contains("regression", "effect size", "N=", "sample"):
    type = "pure_empirical"

elif contains("meta-analysis", "systematic review", "synthesis"):
    type = "review"

else:
    type = "conceptual"  # Default
```

### Contribution Ranking:

```python
# Extract contributions
contributions = find_sections_with_keywords(
    "contribution", "we contribute", "advances", "novelty"
)

# Calculate emphasis
for contrib in contributions:
    paragraphs_devoted = count_paragraphs(contrib)
    emphasis_pct = (paragraphs_devoted / total_paragraphs) * 100

    if emphasis_pct >= 35:
        label = "Primary"
    elif emphasis_pct >= 20:
        label = "Secondary"
    else:
        label = "Tertiary"
```

### Strategic Constraints:

| Pattern Detected | Constraint Added |
|------------------|------------------|
| "suggestive", "exploratory", "preliminary" | `acknowledge_incomplete_evidence` |
| "IV" + "not significant" OR "NS" | `downplay_causality` |
| "artifact", "first to", "novel" | `emphasize_innovation` |
| "single case", "one context" | `acknowledge_scope_limitations` |
| "measurement error", "reliability" | `acknowledge_measurement_limitations` |

---

## Venue-Specific Adaptations

### MISQ:
- Emphasize: Design science artifact OR theory contribution (40%+)
- Secondary: Empirical evidence (30-40%)
- Language: "rigorous", "validated", "generalizable principles"
- Positioning: Innovation + rigor + relevance balance

### MIS Quarterly:
- Emphasize: Theoretical framework (50%+)
- Secondary: Empirical/method (30%)
- Language: "theoretical mechanisms", "conceptual development"
- Positioning: Conceptual depth and novel theorizing

### ISR:
- Emphasize: Rigor + relevance balance
- Strong methodology required
- Language: "robust evidence", "practical implications"
- Positioning: Applied context with theoretical grounding

### Conference (ICIS/AMCIS):
- More concise scope acceptable
- Emphasize: Novelty and timeliness
- Language: "emerging", "preliminary evidence"
- Positioning: Work-in-progress framing acceptable

---

## LaTeX Integration Guide

**Automatic Format Detection:** When you invoke `/paper-architecture @00-incubator-paper.tex`, the skill automatically detects the `.tex` extension and generates LaTeX output. No need to specify `--format latex`.

### Using the Generated LaTeX File

**Option 1: Standalone Document**
```bash
# Compile as standalone reference document
pdflatex 0-paper-architecture-overview.tex
```

**Option 2: Input into Main Paper**
```latex
% In your main paper document
\documentclass{article}
% ... your packages and setup ...

\begin{document}

% Include the architecture overview as an appendix
\appendix
\section{Paper Architecture Overview (Planning Document)}
\input{0-paper-architecture-overview-body.tex}

\end{document}
```

**Note:** For Option 2, you may want to extract just the body content (between `\begin{document}` and `\end{document}`) and save it as a separate `-body.tex` file.

### Converting Between Formats

**Markdown → LaTeX:**
- Can be done automatically if user requests format change
- Use: `/paper-architecture --convert-to latex @existing-overview.md`

**LaTeX → Markdown:**
- Can be done automatically if user requests format change
- Use: `/paper-architecture --convert-to markdown @existing-overview.tex`

### LaTeX Customization

Users can customize the generated LaTeX by:

1. **Colors:** Modify `\definecolor` commands in preamble
2. **Fonts:** Add `\usepackage{fontspec}` and use custom fonts
3. **Layout:** Adjust geometry package settings
4. **Box Styles:** Customize tcolorbox appearance
5. **Section Numbering:** Change `\section{}` to `\section*{}` for unnumbered sections

### Required LaTeX Packages

The skill generates LaTeX requiring these packages (included in preamble):
- `geometry` - Page layout control
- `xcolor` - Color support for headers and boxes
- `enumitem` - Custom list formatting
- `tcolorbox` - Colored boxes for storytelling arc
- `titlesec` - Custom section formatting

All packages are standard and included in most LaTeX distributions (TeX Live, MiKTeX).

---

## Examples

See `examples/` directory for:

**Markdown Examples:**
- `example-empirical-artifact.md` - Hybrid empirical + design science paper
- `example-pure-theory.md` - Pure theoretical contribution
- `example-design-science.md` - Artifact-focused paper

**LaTeX Examples:**
- `example-empirical-artifact.tex` - Hybrid empirical + design science paper (LaTeX)
- `example-pure-theory.tex` - Pure theoretical contribution (LaTeX)
- `example-design-science.tex` - Artifact-focused paper (LaTeX)

**Note:** LaTeX examples include complete preambles and can be compiled standalone or extracted for integration into main paper documents.

---

## Quality Checklist

Before finalizing, verify:

**Completeness:**
- [ ] All 9 sections present
- [ ] Auto-detected config box at top
- [ ] Key data points have actual numbers (not TBD)
- [ ] Contributions ranked and labeled with emphasis %
- [ ] Emphasis % sum to 100%
- [ ] Story arc has all 5 acts in boxes
- [ ] Language guidance has ≥3 DO and ≥3 AVOID

**Format-Specific (Markdown):**
- [ ] Unicode box characters render correctly
- [ ] Markdown formatting (bold, italic, bullets) used consistently
- [ ] Emoji indicators (✅❌) present where appropriate

**Format-Specific (LaTeX):**
- [ ] Complete LaTeX preamble with all required packages
- [ ] Special characters properly escaped (\%, \_, \&, \#, \$)
- [ ] tcolorbox environments compile without errors
- [ ] Lists use `[nosep]` option for compact formatting
- [ ] Subsections use `*` for unnumbered sections where appropriate
- [ ] Document compiles with pdflatex or xelatex

**Clarity:**
- [ ] Overall contribution readable in <30 seconds
- [ ] Each contribution ≤5 bullets
- [ ] Each implication ≤3 bullets
- [ ] No jargon without definition
- [ ] Scope boundaries specific (not vague)

**Strategic Value:**
- [ ] Emphasis % match evidence strength
- [ ] Language guidance addresses actual over-claiming risks
- [ ] Venue positioning explains fit
- [ ] Story arc coherent (acts flow logically)
- [ ] Honest about limitations vs design choices

**Brevity:**
- [ ] Total length: 150-300 lines
- [ ] No section exceeds 60 lines
- [ ] Visual elements ≤5 boxes (story arc only)
- [ ] No redundant content across sections

---

## Common Pitfalls to Avoid

### General (Both Formats):
❌ **Too Vague:** "Significant results" → ✅ "β=0.041***, 8/8 positive associations"
❌ **Too Long:** >300 lines defeats "concise overview" purpose
❌ **Over-Claiming:** Language doesn't reflect strategic constraints
❌ **Mismatch:** Story arc emphasizes different contribution than rankings
❌ **Incomplete:** Missing sections or placeholder text like "TBD"
❌ **Fabricated:** Including numbers not in source documents

### LaTeX-Specific:
❌ **Unescaped Special Chars:** `40%` → ✅ `40\%`, `item_id` → ✅ `item\_id`
❌ **Missing Packages:** Using `tcolorbox` without `\usepackage{tcolorbox}`
❌ **Numbered Sections:** Using `\subsection{}` → ✅ Use `\subsection*{}` for unnumbered
❌ **Compilation Errors:** Not testing document compilation before finalizing
❌ **Verbose Lists:** Using default itemize → ✅ Use `[nosep]` option for compact lists
❌ **Missing Document Class:** Forgetting `\begin{document}...\end{document}`

---

## Success Criteria

Document succeeds if user can:

1. ✅ Pitch paper in 30 seconds (Overall Contribution)
2. ✅ Decide abstract emphasis (Contribution % and ranking)
3. ✅ Write introduction (5-Act Arc)
4. ✅ Avoid over-claiming (Language Guidance)
5. ✅ Position for venue (Paper Positioning section)
6. ✅ Structure discussion (Implications sections)
7. ✅ Make strategic decisions (Primary vs Secondary emphasis)
8. ✅ **[LaTeX]** Integrate overview into LaTeX paper directly (properly formatted .tex file)
9. ✅ **[Markdown]** Share overview with collaborators (readable .md file)

**If user still asks "What should I emphasize?" → Skill failed**
**If user can immediately start writing → Skill succeeded**

### LaTeX-Specific Success:
- ✅ Document compiles without errors
- ✅ Can be `\input{}` into main paper document
- ✅ Visual boxes render correctly in PDF output
- ✅ Can be easily converted to sections in main paper
