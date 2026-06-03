# /paper-incubator arch

**File:** `0-incubator/01-incubator-arch.tex`

---

## Sources to Read

- `0-sections/*.tex` — paper content for extracting claims, numbers, scope
- `0-display/Table/` — generated tables for verifying numbers
- `0-display/Figure/` — generated figures for verifying claims
- `evaluation/results/` — raw evaluation outputs if tables seem stale

---

## Subsections (walked through in order)

| # | Subsection | CC summarizes as | What to discuss |
|---|-----------|------------------|-----------------|
| 1 | **One-Paragraph Summary** | Key claims, numbers, framing in plain text | Emphasis, terminology, accuracy |
| 2 | **Key Data Points** | Scale (bullet list), Validation (bullet list), Core Findings (numbered list with key numbers) | Are numbers current? Story framing right? |
| 3 | **Main Contributions** | C1, C2, ... as titled bullet groups | What to highlight/downplay, naming |
| 4 | **Storytelling Arc & Position** | 5 Acts as short paragraphs + venue fit bullets + terminology table | Narrative flow, venue criteria |
| 5 | **Scope & Boundaries** | Four lists: Deliver, Out of Scope, Limitations, Design Choices | What's in/out, honest vs strategic |

---

## Create Mode

1. Read all `0-sections/*.tex` and evaluation outputs
2. Copy `templates/arch.tex` to `0-incubator/01-incubator-arch.tex`
3. Fill in all 5 subsections based on source material
4. Present subsection 1 (One-Paragraph Summary) as readable summary
5. User reviews → CC refines → add discussion box → move to next
6. Walk through all 5 subsections

## Refine Mode

1. Read existing `01-incubator-arch.tex`
2. Present the 5 subsections as a numbered list
3. Ask user which to focus on (or start from top)
4. Present focal subsection as readable summary
5. Cross-check numbers against current `0-display/Table/` files
6. Flag stale numbers or inconsistencies
7. User gives feedback → CC updates LaTeX + discussion box
8. Continue to next subsection or stay

---

## Formatting Rules (arch-specific)

**One-Paragraph Summary:**
- Dense single paragraph, no bullets
- All key numbers inline (task count, model count, main findings)

**Key Data Points — Scale / Validation:**
```latex
\textbf{Scale:}
\begin{itemize}[nosep]
\item ...
\end{itemize}
```

**Key Data Points — Core Findings:**
```latex
\textbf{Core Findings:}
\begin{enumerate}[nosep,leftmargin=1.5em]
\item \textbf{Finding Title} (Table N):
  \begin{itemize}[nosep]
  \item specific number or claim
  \end{itemize}
\end{enumerate}
```

**Main Contributions:**
```latex
\begin{enumerate}[leftmargin=*]
\item \textbf{C1: Title --- Subtitle}
  \begin{itemize}[nosep]
  \item point
  \end{itemize}
\end{enumerate}
```
Not limited to 3 contributions — as many as the paper needs.

**Storytelling Arc:**
- 5 Acts as `\textbf{Act N --- Label:}` followed by paragraph text
- No boxes around acts (plain paragraphs)

**Fitting Position:**
- `\begin{itemize}[nosep]` mapping contributions to venue review criteria

**Terminology Quick Reference:**
```latex
\begin{tabular}{@{}p{0.47\textwidth}p{0.47\textwidth}@{}}
\toprule
\textbf{Use} & \textbf{Avoid} \\
\midrule
... & ... \\
\bottomrule
\end{tabular}
```

**Scope & Boundaries:**
- Four `\textbf{...:}` headers each followed by `\begin{itemize}[nosep]`
- What We Deliver, Out of Scope, Acknowledged Limitations, Intentional Design Choices
