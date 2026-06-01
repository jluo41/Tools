# /paper-incubator display

**File:** `0-incubator/00-incubator-display.tex`

---

## Sources to Read

- `0-display/Figure/` and `0-display/Table/` — checked-in display outputs
- `evaluation/scripts/` — scripts that generate each display (for provenance)
- `evaluation/results/` — intermediate outputs (Source path in provenance)
- `1-config.yaml` — metrics, model lists, paths driving the evaluation pipeline

**Evaluation pipeline flow:**
```
1-config.yaml → evaluation/scripts/*.py → evaluation/results/ → 0-display/
```

---

## Subsections (one per display)

Each display is a `\subsection` on its own page. The first display has no
`\clearpage`; all subsequent displays start with `\clearpage`.

**Display numbering:** `Display 1`, `Display 2`, ... sequential.

---

## Create Mode

1. Scan `0-display/Figure/` and `0-display/Table/` for all outputs
2. Match each to its generating script in `evaluation/scripts/`
3. Generate the full display file with an entry per display
4. Present Display 1 as readable summary (see below)
5. User reviews → CC refines → add discussion box → move to next
6. Walk through each display

## Refine Mode

1. Read existing `00-incubator-display.tex`
2. Scan `0-display/` for any uncataloged displays → offer to add them
3. Present display list, ask user which to focus on
4. Present focal display as readable summary
5. User gives feedback → CC updates LaTeX + discussion box
6. Continue to next display or stay

---

## How CC Summarizes a Display

```
### Display 3: Main Results (Table 1)

**Visual:** Table with 18 models × 6 demographic columns + overall

**Key takeaways:**
- GPT-4o-mini best overall (32.61 ct-CRPS)
- Chronos-Large competitive without context (33.24)
- T1D 49% harder than T2D across all models

**Methodological notes:**
- Zero-shot evaluation, no fine-tuning
- ct-CRPS = Clarke Error Grid-weighted CRPS

**Provenance:**
- Script: evaluation/scripts/2-generate-Table1-and-Table2.py
- Source: evaluation/results/2-generate-Table1-and-Table2/
- Current: 0-display/Table/Table1-eventglucose-main_Main.tex

What would you like to change in the analysis?
```

---

## Display Entry Structure

Each display subsection contains (in order):

### 1. Rendered Visual
```latex
\begin{figure}[H]   % or \begin{table}[H]
\centering
\includegraphics[width=0.95\textwidth]{0-display/Figure/filename.pdf}
\caption{Caption}
\end{figure}
```

### 2. Deep Analysis
`\subsubsection*{Deep Analysis: Topic}`

Sub-topics (all required):

| Sub-topic | What it covers |
|-----------|---------------|
| **Generation Methodology** | How the display was produced (script, selection criteria) |
| **Critical Insights** | Numbered: `CRITICAL INSIGHT #1: Title` |
| **What This Actually Shows** | Honest interpretation (numbered list) |
| **Methodological Transparency** | Caveats, selection bias, limitations |
| **Connections to Other Displays** | `→ Display M:` cross-references |

### 3. Provenance Footer (required)
```latex
\textbf{Source:} \texttt{evaluation/results/...}\\
\textbf{Current:} \texttt{0-display/Figure/...}\\
\textbf{Script:} \texttt{evaluation/scripts/...}
```

---

## Formatting Rules (display-specific)

- Figures use `0-display/Figure/filename.pdf` paths (compiled from repo root)
- Tables use `\input{0-display/Table/filename.tex}` wrapped in `\begin{table}[H]`
- Critical Insights numbered sequentially: `CRITICAL INSIGHT #1`, `#2`, ...
- Connections use `$\rightarrow$ \textbf{Display M:}` format
- Commented-out displays (`% \subsection{...}`) preserved for history
- All numbers must match the rendered tables/figures exactly
