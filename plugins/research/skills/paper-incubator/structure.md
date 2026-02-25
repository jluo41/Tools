# /paper-incubator structure

**File:** `0-incubator/02-incubator-structure.tex`

---

## Sources to Read

- `0-sections/*.tex` — actual paper section files (primary source)
- `01-incubator-arch.tex` — canonical numbers for the header
- `00-incubator-display.tex` — display inventory for placement references
- `0-display/Figure/`, `0-display/Table/` — to verify display references

---

## Canonical Numbers Header

The file starts with a comment block of approved numbers from arch.
**Always sync this when arch changes.**

```latex
% CANONICAL NUMBERS (from 01-incubator-arch.tex, JL-approved):
%   - [task count] = [factorial breakdown]
%   - [model count] ([breakdown])
%   - [context levels]: [names]
%   - Terminology: "[approved term]"
%   - Primary metric: [metric name]
%
% STATUS (as of YYYY-MM-DD):
%   ✅ Section 1: [status]
%   ⚠ Section 3: [issue]
%
% REMAINING ISSUES:
%   ⚠ [description]
```

---

## Subsections (one per paper section)

Each paper section gets its own `\section` in the structure file:

```
\section{Abstract (00_abstract.tex)}
\clearpage
\section{Section 1: Introduction (01_introduction.tex)}
\clearpage
\section{Section 2: Problem Setting (02_problem_setting.tex)}
...appendix sections...
```

---

## Create Mode

1. Read canonical numbers from `01-incubator-arch.tex`
2. Read each `0-sections/*.tex` file
3. Read display inventory from `00-incubator-display.tex`
4. Generate paragraph-level blueprint for each section
5. Present Abstract as readable summary
6. User reviews → CC refines → add discussion box → move to next
7. Walk through all sections

## Refine Mode

1. Read existing `02-incubator-structure.tex`
2. Present section list, ask user which to focus on
3. Read the actual `0-sections/NN_filename.tex` for current content
4. Compare paragraph summaries against actual content
5. Flag: stale summaries, wrong numbers, missing displays, new paragraphs
6. User gives feedback → CC updates LaTeX + discussion box
7. Continue to next section or stay

---

## How CC Summarizes a Section

```
### Section 5: Experiments and Results (05_experiments_results.tex)

**Status:** Written, ~209 lines, 4 subsections. Target: 2.5 pages.

**Displays placed here:**
- Table 3 (Context by Event) — before §5.1
- Figure R1 (LLM Win Rates) — before §5.1
- Figure R4 (4-panel scatter) — §5.3

**Paragraphs:**
- P1 (Protocol — 4 sentences): 18 models, zero-shot, 60 tasks
- §5.1 P1 (Main findings — 5 sentences): GPT-4o-mini best, Chronos competitive
- §5.2 P1 (Context ablation — 6 sentences): Context Integration Gap, 8/10 degrade
- §5.3 P1 (Fairness — 4 sentences): T1D 49% harder, age effects

⚠ P1 still says "21 models" — should be 18 (canonical)

What would you like to change?
```

---

## Section Entry Structure

### 1. Status Comment Block
```latex
% Status: [Written/Draft/Placeholder]. ~N lines. N subsections.
% Target: N pages.
% Numbers: [✅ or ⚠ with note]
```

### 2. Display Placement (if any)
```latex
\subsection*{Display: Figure R1 --- placed before §5.1}
\begin{figure}[H]
\centering
\includegraphics[width=0.95\textwidth]{Figure/filename.pdf}
\caption{Caption with version notes.}
\label{fig:label}
\end{figure}
```

### 3. Paragraph-Level Summary
```latex
\textbf{P1 (Topic --- N sentences):}
\parasummary{What the paragraph covers, key claims, numbers cited.}
```

For sections with subsections:
```latex
\subsubsection*{§N.M Subsection Title}

\textbf{P1 (Topic --- N sentences):}
\parasummary{Content summary.}
```

---

## Formatting Rules (structure-specific)

**Extra packages** (beyond shared set):
- `longtable`, `ulem` (for `\sout{}`), `multirow`

**Extra custom commands:**
- `\parasummary{text}` — italic paragraph summary
- `\displayref{text}` — yellow-highlighted display reference
- `\resolved{text}` — green background (issue fixed)
- `\inconsistency{text}` — red background (problem flagged)

**Figure paths:**
- `\graphicspath{{../0-display/}}` — figures load from paper's display directory

**Document extras:**
- Includes `\tableofcontents` + `\clearpage` after `\maketitle`
- Margin: `0.8in` (tighter than arch/display's `1in`)

**Status indicators in content:**
- `\resolved{text}` for items that have been verified/fixed
- `\inconsistency{text}` for items that contradict source material
- `\sout{text}` for content that was removed (preserved for history)
