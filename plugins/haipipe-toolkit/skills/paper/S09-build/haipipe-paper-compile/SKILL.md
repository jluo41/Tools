---
name: haipipe-paper-compile
description: "Compile a paper-owned LaTeX target to PDF, fix build errors, and verify output. Resolves a specific `.tex`, the Display gallery at `0-lifecycle/3-display/4-display.tex`, or the paper's unnumbered master/`2-src/compile.sh`. Compilation never approves a Board gate or advances to submission. Trigger: 编译论文, compile paper, compile Display, build PDF, 生成PDF."
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
metadata:
  version: "0.3.0"
  last_updated: "2026-07-26"
  summary: "Target-aware LaTeX compilation: explicit tex, canonical Display gallery, or full-paper master. Verifies the PDF and reports Board gate state without changing it."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# Paper Compile: LaTeX Target to Verified PDF

Compile the LaTeX paper and fix any issues: **$ARGUMENTS**

## Constants

- **COMPILER = `latexmk`** — LaTeX build tool.
  Handles multi-pass compilation automatically.
- **ENGINE = `pdflatex`** — LaTeX engine.
  Options: `pdflatex` (default), `xelatex` (for CJK/custom fonts), `lualatex`.
- **MAX_COMPILE_ATTEMPTS = 3** — Maximum attempts to fix errors and recompile.
- **TARGET** — resolved from the request:
  1. an explicit `.tex` path;
  2. “Display” → `<paper>/0-lifecycle/3-display/4-display.tex`;
  3. “full paper” → run `<paper>/2-src/compile.sh` when present, otherwise
     select the requested unnumbered root `*.tex` carrying `\documentclass`.
  If several masters exist and the user did not name one, ask; never guess.
- **MAX_PAGES** — Page limit.
  ML conferences: main body to Conclusion end (excluding references & appendix).
  ICLR=9, NeurIPS=9, ICML=8.
  **IEEE venues: references ARE included in page count.**
  IEEE journal ≈ 12-14 pages, IEEE conference ≈ 5-8 pages (all inclusive).

## Workflow

### Step 1: Resolve the paper root and target

Resolve before running a compiler. Never assume `paper/main.tex`.

1. An explicit `.tex` path wins.
2. A Display request resolves to
   `<paper>/0-lifecycle/3-display/4-display.tex`.
3. A full-paper request uses `<paper>/2-src/compile.sh` when it exists.
   Otherwise find unnumbered root `*.tex` files carrying `\documentclass`.
4. If more than one full-paper master remains and the user did not name one,
   ask which target to use. Do not pick by timestamp or filename.

The paper root is the nearest ancestor containing `0-lifecycle/`. Confirm the
resolved target is inside that paper. Reject a missing target rather than
silently compiling another file.

Check the requested toolchain without installing anything:

```bash
command -v latexmk
command -v pdflatex
command -v bibtex
```

If the required compiler is absent, return `blocked` with platform-appropriate
installation guidance. Do not modify the paper or declare its Board gate failed.

### Step 2: Compile the resolved target

For a full paper with its owned build script:

```bash
(cd "$PAPER_ROOT" && ./2-src/compile.sh)
```

For an explicit target or the Display gallery, compile from the paper root so
root-relative `\input` paths continue to resolve, while placing output beside
the target:

```bash
(cd "$PAPER_ROOT" && latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -output-directory="$(dirname "$TARGET_REL")" "$TARGET_REL")
```

Do not run a root-wide clean before compiling. It can remove useful diagnostics
and unrelated target artifacts. Capture the compiler output and inspect the
target's own `.log`; after a successful direct compile, `latexmk -c` may clean
that target's auxiliaries while preserving its PDF.

### Step 3: Error Diagnosis and Auto-Fix

If compilation fails, read the resolved target's log and fix only the error
needed to build that target:

**Missing packages:**
```
! LaTeX Error: File `somepackage.sty' not found.
```
→ Report the dependency. Installing system packages requires the user's
environment authority; removing a package is valid only when it is truly unused.

**Undefined references:**
```
LaTeX Warning: Reference `fig:xyz' on page 3 undefined
```
→ Check `\label{fig:xyz}` exists in the correct figure environment.

**Missing figures:**
```
! LaTeX Error: File `displays/display01-hero/assets/figure.pdf' not found.
```
→ Check if the file exists with a different extension (.png vs .pdf).
Update the `\includegraphics` path.

**Citation undefined:**
```
LaTeX Warning: Citation `smith2024' undefined
```
→ Add the missing entry to `references.bib` or fix the citation key.

**`[VERIFY]` markers in text:**
→ Search for `[VERIFY]` markers left by `/haipipe-paper section-edit`.
These indicate unverified citations or facts.
Flag them as content/evidence findings; compilation does not discharge them.

**Overfull hbox:**
```
Overfull \hbox (12.5pt too wide) in paragraph at lines 42--45
```
→ Minor: usually ignorable.
If severe (>20pt), rephrase the text or adjust figure width.

**BibTeX errors:**
```
I was expecting a `,' or a `}'---line 15 of references.bib
```
→ Fix BibTeX syntax (missing comma, unmatched braces, special characters in title).

**`\crefname` undefined for custom theorem types:**
→ Ensure `\crefname{assumption}{Assumption}{Assumptions}` and similar are in the preamble after `\newtheorem{assumption}`.

### Step 4: Iterative Fix Loop

```
for attempt in 1..MAX_COMPILE_ATTEMPTS:
    compile()
    if success:
        break
    parse_errors()
    auto_fix()
```

For each error:
1. Read the error message from the resolved target's log
2. Locate the source file and line number
3. Apply the fix
4. Recompile

Stop after `MAX_COMPILE_ATTEMPTS`. Return the first unresolved compiler error,
the source location, and the exact target. Do not route to an optional plugin or
rewrite unrelated prose.

### Step 5: Post-Compilation Checks

Derive the expected PDF by replacing the target's `.tex` suffix with `.pdf`.
For a build-script run, use the PDF path reported by the script and verify it is
an unnumbered deliverable.

```bash
test -s "$TARGET_PDF"
pdfinfo "$TARGET_PDF"
```

**Visual review (automated):**
If the compiled PDF exists, read it directly to check visual presentation:
- Figure quality: readable labels, legible text, distinguishable colors
- Layout: no orphaned section headers, no awkward page breaks
- Figures appear near their first text reference (not pages away)
- Tables: aligned columns, consistent decimal precision
- No overfull content visibly extending past margins

This is a quick visual scan, not a full review — the improvement loop does deeper visual review.

**Automated checks:**

- [ ] PDF exists, is non-empty, and `pdfinfo` can parse it
- [ ] No unresolved-reference or unresolved-citation warning in the target log
- [ ] Figures are rendered (not missing image placeholders)
- [ ] The PDF is not stale: its mtime is at least the target `.tex` mtime
- [ ] Every Display `\input{displays/<unit>/float.tex}` resolves when the
      target is the gallery
- [ ] Every master-reachable `\input`, `\includegraphics`, and bibliography
      target resolves when the target is a full paper

### Step 6: Page Count Verification

This step applies to a **full-paper target only**. A Display gallery reports its
page count but has no venue page-limit verdict.

**For ML conferences (ICLR/NeurIPS/ICML/CVPR/ACL/AAAI):** Main body = first page through end of Conclusion section (not necessarily §5 — could be §6, §7, or §8 depending on structure).
References and appendix are NOT counted.

**For IEEE venues:** The TOTAL page count (including references) must fit within the limit.
There is no separate "main body" counting — everything up to and including the references counts.

Use the venue pinned on the Venue S page. If no venue or limit is pinned, report
the measured page count and `limit: unknown`; never guess a compliance verdict.

If over limit:
- Identify which sections are longest
- Suggest specific cuts (move proofs to appendix, compress tables, tighten writing)
- Report: "Main body is X pages (limit: MAX_PAGES).
  Suggestion: move [specific content] to appendix."

### Step 7: Read, never mutate, the Board gate

Compilation and approval are independent:

```text
compiler verdict  = did the resolved target produce a valid PDF?
Board verdict     = did the owning S page reach ✅ with an approval receipt?
```

Read the owning S page's first state token and its `## Log`. A green state
without an actor/date approval receipt is stale and must be reported as such.
This skill never writes an S-page state, appends a receipt, advances the
frontier, or recommends submission merely because compilation succeeded.

Run submission-readiness checks only when the user explicitly asks, only for a
full-paper target, and only after all required Board gates are green with
receipts:

- [ ] **Anonymous**: no author names, affiliations, or self-citations that reveal identity
- [ ] **Page limit**: main body within MAX_PAGES (to end of Conclusion)
- [ ] **Font embedding**: all fonts embedded in PDF
  ```bash
  pdffonts main.pdf | grep -v "yes"  # should return nothing (or only header)
  ```
- [ ] **No supplementary mixed in**: appendix clearly after `\newpage\appendix`
- [ ] **File size**: reasonable (< 50MB for most venues, < 10MB preferred)
- [ ] **No `[VERIFY]` markers**: search the PDF text for leftover markers

### Step 8: Output Summary

```markdown
## Compilation Report

- **Status**: SUCCESS / FAILED
- **Target**: <resolved tex or 2-src/compile.sh>
- **PDF**: <resolved PDF>
- **Pages**: X; full-paper breakdown when applicable
- **Within page limit**: YES / NO / NOT APPLICABLE / UNKNOWN
- **Errors fixed**: [list of auto-fixed issues]
- **Warnings remaining**: [list of non-critical warnings]
- **Undefined references**: 0
- **Undefined citations**: 0
- **Board gate**: approved / open / stale / not associated (read-only)

### Next Steps
- [ ] Visual inspection of PDF
- [ ] If content/evidence warnings remain, return to the owning Paper stage
- [ ] If the owning S page is not approved, run `/haipipe-paper <stage> check`
```

## Key Rules

- **Never delete the user's source files** — only modify to fix errors
- **Never hardcode `main.tex`** — resolve the requested target
- **Compilation is not approval** — never mutate or infer a Board gate
- **Never recommend submission from compiler success alone**
- **Don't suppress warnings** — report them, let the user decide
- **If LaTeX is not installed**, provide clear installation instructions rather than failing silently
- **Font embedding is critical** — some venues reject PDFs with non-embedded fonts
- **Page count rules differ by venue** — ML conferences: main body to Conclusion (refs excluded).
  **IEEE venues: total pages including references.**

## Common Venue Requirements

| Venue | Style File | Citation | Page Limit | Refs in limit? | Submission |
|-------|-----------|----------|------------|----------------|------------|
| ICLR 2026 | `iclr2026_conference.sty` | `natbib` (`\citep`/`\citet`) | 9 pages (to Conclusion end) | No | OpenReview |
| NeurIPS 2025 | `neurips_2025.sty` | `natbib` (`\citep`/`\citet`) | 9 pages (to Conclusion end) | No | OpenReview |
| ICML 2025 | `icml2025.sty` | `natbib` (`\citep`/`\citet`) | 8 pages (to Conclusion end) | No | OpenReview |
| IEEE Journal | `IEEEtran.cls` [journal] | `cite` (`\cite{}`, numeric) | ~12-14 pages (Transactions) / ~4-5 (Letters) | **Yes** | IEEE Author Portal / ScholarOne |
| IEEE Conference | `IEEEtran.cls` [conference] | `cite` (`\cite{}`, numeric) | 5-8 pages (varies by conf) | **Yes** | EDAS / IEEE Author Portal |
