---
name: paper-revise
description: "Interactive revision of LaTeX section files through structured discussion. Use when the user wants to revise a paper section, annotate sentences, discuss paragraph logic, or apply accepted changes. Also use when the user mentions /paper-revise, revise section, annotate paper, or paper revision."
---

Skill: paper-revise
===================

Interactive revision of LaTeX section files through structured discussion.
Works top-down: Section logic → Paragraph logic → Sentence edits.
Active author discussion at every level before any edits are made.
The discussion IS the work — sentence annotation is just the final step.

Usage
=====

```
/paper-revise <file> [author comments]
/paper-revise <file> apply
/paper-revise <file> reindex
/paper-revise <file> clean-l1
/paper-revise <file> clean-l2
```

Examples:
```
/paper-revise 0-sections/01_introduction.tex
/paper-revise 0-sections/03_method.tex "Reviewer 2 says the notation is inconsistent with Section 4. Tighten the problem setup."
/paper-revise 0-sections/05_results.tex "Subgroup analysis needs more statistical rigor per R1. Also cut redundancy with the appendix."
/paper-revise 0-sections/01_introduction.tex apply
/paper-revise 0-sections/01_introduction.tex reindex
/paper-revise 0-sections/01_introduction.tex clean-l1
/paper-revise 0-sections/01_introduction.tex clean-l2
```

The author can provide:
- Just a file → CC reads, analyzes, and starts section-level discussion
- A file + comments → CC uses the comments to guide its analysis and priorities
- A file + reviewer feedback + "apply"/"update with"/"clean with" → CC enters **Phase 2-fast** (lightweight reviewer-feedback apply): edits the active text AND attaches one `%% Comments: {INITIALS} ...` line per sentence; no `%% Proposed:` / `%% Changes:` / `%% Reason:` / `%% Author:` blocks
- A file + "apply" → CC applies all accepted annotations (Phase 3)
- A file + "reindex" → CC renumbers sentence-index tags after structural shifts (Phase 3b)
- A file + "clean-l1" → CC strips metadata but keeps index headers + `%% Comments:` lines (Phase 3c)
- A file + "clean-l2" → CC strips everything except index headers (Phase 3c)

---

Core Principles
===============

1. **Discussion first, edits last** — The discussion about logic and
   structure IS the primary work. Sentence annotation is just recording
   the conclusions. Never skip straight to sentence edits.
2. **Logic restructuring is normal** — At section and paragraph level,
   the author may want to rethink the whole argumentative flow:
   reorder paragraphs, merge or split them, change what a paragraph
   argues, or rewrite the section logic entirely. CC should actively
   support this, not just polish existing sentences.
3. **Top-down flow** — Section logic first, then paragraph logic,
   then sentence edits. Never jump ahead.
4. **One paragraph at a time** — Never modify more than one paragraph
   per editing round. Get agreement, then move to the next.
5. **Author voice preserved** — Leave `%% Author:` fields for the author
   to record their own thoughts. Never fill these in for the author.
6. **Annotations are persistent** — Annotations stay in the file as a
   working document. The author may apply changes manually, or use
   `/paper-revise apply` later. CC never removes annotations unless
   the author explicitly runs `apply`.
7. **Author comments drive priorities** — If the author provides comments
   with the invocation, those comments set the direction. CC should
   address them before offering its own suggestions.
8. **Interactive decision cards** — At every decision point where the
   author must choose between discrete options (A/B/C), use the
   `AskUserQuestion` tool to present interactive cards the author can
   navigate with arrow keys. This replaces printing plain-text option
   lists. The tool supports 1-4 questions per call, 2-4 options per
   question, and always includes an "Other" option for free-text input.
9. **Keep the .tex file clean — no narrative comment blocks.** The .tex
   file is a working document, but only `%% ---- PX.SY [bracket-note] ----`
   index headers and `%% Comments: {INITIALS} ...` lines belong in it.
   **Do NOT add:**
   - Retired-content notes ("RETIRED per X v0506: Old P7 absorbed into…")
   - Multi-line section-divider comments ("NEW P6: Study Design + Findings
     Preview — Combines old P5 with abbreviated preview… Closes intro on
     results…")
   - Restructure-explainer headers ("NEW per Ritu v2026-05-06 — restructure
     §1.1 into intro · removed bold tags · etc.")
   - "FIGURE 1 — anchored to new P6" type position-explainer headers
   These belong in the **commit message**, in a **separate revision-log
   file** (e.g. `1-feedback/v0506feedback/revision-log.md`), or in your
   conversation with the author — never in the .tex itself. The .tex
   should compile to a paper, not read as a project journal. The bracket
   note inside an index header (`[NEW per Ritu — feasibility]`) is the
   one and only place a one-line provenance hint is allowed.
   Use the `preview` field to show quoted LaTeX snippets or before/after
   text when the decision benefits from seeing the actual content.
   Batch related questions together (up to 4) but keep unrelated
   decisions in separate calls so the author can focus.

---

Phase 1: Section-Level Review
=============================

### Step 1: Read and Orient

Read the target file. Detect structure automatically:
- Paragraphs = blocks of text separated by blank lines
- Subsections = `\subsection{}` or similar LaTeX commands
- Reviewer comment macros = auto-detect from the file (common patterns:
  `\ra{}`, `\rev{}`, `\todo{}`, `\comment{}`, `\RC{}`, or custom macros
  defined in the preamble). Note the convention for use in `%% Comments:`
  lines later.
- Existing annotations = `%% Proposed:`, `%% Diff:`, or similar
- Figure/table blocks = `\begin{figure}` ... `\end{figure}` (skip these)
- Algorithm/listing blocks = `\begin{algorithm}` ... `\end{algorithm}` (skip)

Number paragraphs sequentially: P1, P2, P3, ... based on order of
appearance. If subsections exist, note them: P1 (under §2.1), etc.

### Index format (sentence tags only)

The file uses **exactly one** index-tag form — never anything else:

```
%% ---- P1.S1 ----                       # sentence index
%% ---- P1.S1 [bracket note] ----        # sentence index with optional pass tag
```

**Do NOT add bare paragraph header lines** like `%% ---- P1 ----` or
`%% ---- P1: D-Agent at Data level ----`. Paragraph boundaries are
implicit: a blank line in the source separates paragraphs, and the
paragraph number is encoded in each sentence's `Pn.Sm` tag. Adding a
standalone `%% ---- Pn ----` header is noise — the user has explicitly
rejected this pattern.

The bracket note `[...]` is allowed only on sentence tags, where it
records the revision pass (e.g., `[v0506 RA — substitute]`,
`[DELETE per v0506 RA]`, `[NEW per Gordon comment v2026-05-04]`).

No `Pn: description`, no `P-XY` letter codes, no slash variants. Keep
it boring so reindex and clean modes can rely on the format.

### Paragraph numbering scope

`Pn` numbering **restarts at 1 in each .tex file**. Do not continue
numbering across `\input{}` boundaries. If `03_research_design.tex`
includes `03-1_empirical_setting.tex`, `03-2_stage1_message_design.tex`,
etc. via `\input`, each sub-file starts its own `P1`, `P2`, … sequence.
Sentence numbering also restarts within each paragraph as `S1`, `S2`, …

This keeps tags stable when sub-files are rearranged, split, or moved
between sections — the file itself is the numbering scope.

**Detect the paper's comment conventions early.** Look for:
- Custom macros in the preamble (e.g., `\newcommand{\ra}`, `\newcommand{\rev}`)
- Inline comments using `% TODO:`, `% FIXME:`, or similar
- Color-coded macros (e.g., `\textcolor{red}{...}`)
Record what you find — use these same macros in `%% Comments:` lines
so annotations are consistent with the paper's existing workflow.

### Step 2: Present Section Map

Show the author a **readable section map** — NOT raw LaTeX:

```
Section: [Title] ([filename])
===============================

Structure:
  P1  [Role] — [topic summary from first sentence]            [N sentences]
  P2  [Role] — [topic summary]                                 [N sentences]
  --  Figure/Table placement
  P3  [Role] — [topic summary]                                 [N sentences]
  §[Subsection Title]
    P4  [Role] — [topic summary]                               [N sentences]
    P5  [Role] — [topic summary]                               [N sentences]
  ...

Comment macros detected: [e.g., \ra{}, \rev{}, \todo{}, or none found]

Reviewer Comments:
  [list any reviewer comments found, grouped by paragraph]

[If author provided comments, address them here:]
Author's Direction: "[quoted author comments]"
  → This affects [specific paragraphs and why]

Overall Assessment:
  - [CC's analysis of section flow and structure]
  - [Issues CC noticed]
  - [How author's comments relate to what CC sees]
```

### Step 3: Prepare Decision Questions

Before discussing section logic, prepare a **numbered list of decision
questions** covering all structural, content, and consistency issues.
Each question should include:
- The specific paragraph/sentence it relates to (e.g., "§5.1 P3")
- A direct quote or paraphrase of the relevant text
- Why this is an issue (e.g., redundancy, inconsistency, reviewer comment)
- Options (A/B/C) with CC's recommendation

This gives the author a complete map of decisions before any work begins.
The author can then go through questions one by one, making decisions
efficiently without losing context.

Format:
```
Questions for [Section] Revision
=================================

**CATEGORY (e.g., STRUCTURE, REDUNDANCY, CONTENT)**

**Q1.** [Question about a specific decision]
Context: §X.Y P3 currently says: "[quote]"
Issue: [why this needs a decision]
Options:
  - (A) [option]
  - (B) [option]
My take: [CC's recommendation]
```

**Present all questions at once** as a text overview first so the author
sees the full scope. Then walk through decisions using `AskUserQuestion`
interactive cards, batching up to 4 related questions per call.

Each question becomes an `AskUserQuestion` entry:
- `question`: the decision question with context
- `header`: short category tag (e.g., "Structure", "Redundancy")
- `options`: 2-4 choices, put CC's recommendation first with "(Recommended)"
- `preview`: use this to show the relevant LaTeX snippet or quote so
  the author can see what they're deciding about without scrolling

Example call for two structure questions:
```
AskUserQuestion(questions=[
  {
    question: "P3 mixes motivation and method. How should we handle it?",
    header: "Structure",
    options: [
      {label: "Split into two (Recommended)", description: "P3a = motivation, P3b = method setup"},
      {label: "Keep merged", description: "Tighten but keep as one paragraph"},
      {label: "Move method part to §3", description: "Delete method sentences here, absorb into Method"}
    ],
    preview: "P3 currently says:\n\\textit{Our approach is motivated by...}\n[5 sentences later]\n\\textit{Specifically, we define the loss as...}",
    multiSelect: false
  },
  {
    question: "P5-P6 overlap with the abstract. Cut or keep?",
    header: "Redundancy",
    options: [
      {label: "Cut P6, keep P5 (Recommended)", description: "P5 is stronger; P6 restates without adding"},
      {label: "Merge into one paragraph", description: "Combine the non-redundant parts"}
    ],
    preview: "P5: \\textit{We show that...}\nP6: \\textit{Our results demonstrate that...}\nAbstract: \\textit{We demonstrate that...}",
    multiSelect: false
  }
])
```

This replaces the old workflow of printing all options as text and
waiting for the author to type A/B/C. The author navigates with arrow
keys and selects, or picks "Other" to provide free-text input.

### Step 3b: Describe Proposed Structure

After questions are resolved, present the **proposed structure** for the
section showing what each subsection/paragraph will contain, approximate
sentence counts, what's kept/cut/added, and how moved content is absorbed.

Format:
```
Section N: [Title] -- Proposed Structure
=========================================

§N.1  [Subsection title]                          [~X sentences]

  P1: [Topic] [~N sentences]
    - [sentence-level plan]
    - [what's kept, cut, or added]

  P2: [Topic] [~N sentences]
    - ...

§N.2  [Subsection title]                          [~X sentences]
  ...

Total: ~XX sentences, ~Y pages
```

Include a comparison table showing current vs. proposed sentence counts
per subsection. If the author has identified a reference paper at the
target venue as a size benchmark, compare against it.

**Wait for author response.** The author should confirm the structure
before any annotation begins. This prevents wasted work if the author
wants a different organization.

### Step 3c: Section-Level Discussion

If the proposed structure requires further discussion about logic or
reorganization, present the decision using `AskUserQuestion`:

```
AskUserQuestion(questions=[
  {
    question: "How would you like to proceed with the proposed structure?",
    header: "Structure",
    options: [
      {label: "Accept structure", description: "Proceed to paragraph-level annotation"},
      {label: "Reorder subsections", description: "CC adjusts order and re-presents the plan"},
      {label: "Merge/split subsections", description: "CC proposes how to combine or break apart"},
      {label: "Change argument", description: "Tell CC what a subsection should argue instead"}
    ],
    multiSelect: false
  }
])
```

If the author picks "Change argument" or "Other", follow up with
discussion. This may take multiple rounds. That's expected and valuable.

### Step 4: Record Section Agreement

After discussion, add the agreed revision plan as a comment block at the
**bottom** of the file (after all content, so it doesn't interfere with
LaTeX compilation). The plan serves as a persistent blueprint that both
CC and the author can reference during paragraph-by-paragraph work.

```latex
%
%
%
%% ============================================================
%% REVISION PLAN (agreed YYYY-MM-DD)
%% Target: [venue]. ~N pages, ~N sentences.
%% Direction: [author's stated goal]
%% ============================================================
%%
%% STRUCTURAL CHANGES:
%%   - [e.g., "Merge old P1-P9 into 4 paragraphs"]
%%   - [e.g., "Remove framing X, replace with framing Y"]
%%   - [e.g., "Move Figure 1 to after P4"]
%%
%% ------------------------------------------------------------
%% PROSE SECTION (~N sentences, ~N pages)
%% ------------------------------------------------------------
%%
%% P1: [Topic] [N sentences]
%%   - [sentence-level plan]
%%   - [sentence-level plan]
%%
%% P2: [Topic] [N sentences]
%%   - ...
%%
%% ------------------------------------------------------------
%% §[SUBSECTION TITLE] (~N sentences)
%% ------------------------------------------------------------
%%
%% P5: [Block] [N sentences]
%%   - ...
%%
%% ============================================================
```

**Why at the bottom:** The plan is a working document. Placing it at the
bottom keeps it out of the way of LaTeX compilation while remaining
visible when scrolling through the file. It also stays close to the end
of the content, making it easy to find.

### Step 5: Reference Links for New Citations

When the revision plan introduces new references not yet in the bib file,
add a **CANDIDATE REFERENCES** block after the revision plan with
clickable DOI/URL links organized by paragraph. The author clicks each
link to verify the paper, then manually adds bib entries.

```latex
%% ============================================================
%% CANDIDATE REFERENCES TO ADD (click to verify, then add bib entries)
%% ============================================================
%%
%% §X.X references (PY):
%%   AuthorLastName et al. Year — "Short title" — Journal
%%     https://doi.org/10.XXXX/XXXXX
%%
%%   AuthorLastName Year — "Short title" — Journal
%%     https://doi.org/10.XXXX/XXXXX
%%
```

**Why:** The author manages the bib file manually (often via Overleaf).
CC should never guess bib entries without verification. Providing
clickable links lets the author verify each paper and add entries at
their own pace. Organize links by paragraph so it's clear which
references go where.

---

Phase 2: Paragraph-Level Review
================================

Work through paragraphs one at a time.

### Step 1: Present the Paragraph

For the focal paragraph, show in readable form:

```
Paragraph P1: [topic]
======================

Role in section: [what this paragraph should accomplish per the agreed plan]

Sentences:
  S1: [first ~80 chars of sentence]...
  S2: [first ~80 chars]...
  S3: [first ~80 chars]...
  ...

Reviewer comments here: [list any]

[CC's analysis]:
  - [topic coherence assessment]
  - [which sentences serve the topic, which don't]
  - [connection to author's stated direction]
```

### Step 2: Paragraph Discussion (Logic First)

This is the most important step. Before touching any sentences, discuss
the paragraph's **logic and purpose** with the author.

First, present the analysis as text:

```
Current logic: [CC's reading of what the paragraph currently argues]
Agreed role:   [what this paragraph should do per the revision plan]
Gap:           [where current logic doesn't match the agreed role]
```

Then present the decision using `AskUserQuestion` with a preview
showing the paragraph content:

```
AskUserQuestion(questions=[
  {
    question: "How should we handle this paragraph?",
    header: "P[N] Logic",
    options: [
      {label: "Keep logic, tighten", description: "Current argument is fine — just polish sentences"},
      {label: "Restructure", description: "Keep some sentences, rewrite others to match the agreed role"},
      {label: "Rewrite from scratch", description: "Tell CC what you want it to say (pick Other to explain)"}
    ],
    preview: "Current P[N] ([N] sentences):\n  S1: [first ~60 chars]...\n  S2: [first ~60 chars]...\n  ...\n\nAgreed role: [role from revision plan]",
    multiSelect: false
  }
])
```

If the author has paragraph-specific sub-questions (e.g., "should we
keep S3?" or "which framing?"), batch those as additional questions
in the same `AskUserQuestion` call (up to 4 total).

**Wait for author response.**

The author may:
- State the paragraph's purpose in their own words
- Describe a new argumentative logic for the paragraph
- Point to specific sentences to change
- Ask CC to propose a restructured version
- Provide raw thoughts / bullet points for CC to formalize
- Say "the current logic is fine, just polish"

If the author provides raw thoughts or a new logic, CC should:
1. Propose a new sentence plan (what each sentence should say)
2. Discuss the plan with the author
3. Only then proceed to sentence annotation

This discussion may take multiple rounds. That's expected.

### Step 3: Annotate Sentences

After paragraph-level agreement on the logic, annotate each sentence.
If the author agreed to a new logic, the annotations should reflect
that new logic — not just polish the old sentences.

**CRITICAL: One sentence per annotation block.** Every `%% ---- PX.SY ----`
block must contain exactly ONE sentence as the active text. If a proposed
change produces multiple sentences, split them into separate annotation
blocks (P1.S1, P1.S2, P1.S3, etc.). Never combine multiple sentences
into a single annotation block — this makes it impossible for the author
to review, accept, or reject individual sentences. When splitting multi-
sentence originals, each new block gets its own `%% ---- PX.SY ----` tag.

**Annotation format (compile-ready):**

The proposed text is ACTIVE (uncommented, compiles in LaTeX).
The original text is COMMENTED OUT with single `%` prefix.
This way the file always compiles with the latest proposed changes.

```latex
%
%% ---- P1.S1 ----
% Original sentence text here.
%% Proposed: %%
Revised sentence text here.
%% Changes:
%%   (1) "old phrase" → "new phrase"
%%   (2) "another old" → "another new"
%% Reason: Why this change serves the agreed paragraph topic.
%% Comments: {RA} R1.Q3: Needs stronger statistical support.
%% Comments: {JL} R1.Q3: Added significance tests and CIs.
%% Author:
```

**KEY CONVENTION:** The original sentence is commented out with a single
`%` prefix. The `%% Proposed:` label sits on its own line. The revised
text follows as the ACTIVE line (no prefix, compiles in LaTeX).
Metadata lines (`%% Changes:`, `%% Reason:`, `%% Comments:`, `%% Author:`)
use `%%` prefix as before.

**The `%% Comments:` lines** use a curly-brace initials tag followed by
a space and the comment text. **Format:** `%% Comments: {INITIALS} text`
— note the space after the closing brace, **no colon**.

Common initials patterns (detect from the paper in Phase 1 Step 1):
- `{RA}` / `{JL}` — reviewer / author initials (e.g., RA = a coauthor's
  initials, JL = the lead author's initials)
- `{R1}` / `{R2}` / `{R3}` — numbered reviewers
- `{AC}` — associate editor / area chair
- `{TODO}` — general action items

Examples:
```latex
%% Comments: {RA} C#12: These are referenced often -- where do they come from?
%% Comments: {JL} C#12: Grounded with citations. Capabilities detailed in §2.2.
```

If the paper defines LaTeX macros for inline reviewer comments (e.g.,
`\ra{}`, `\jl{}`), those still go inside the active text. The
`%% Comments:` annotation lines, by contrast, are **comment-only** (they
never compile) and use the curly-brace `{INITIALS} text` form regardless
of whether the paper defines macros.

**Replying to an existing comment.** When CC (or a coauthor) responds to
an existing `%% Comments: {INITIALS} ...` line, the reply is **appended
inline to the same line**, separated by `========>`. It does **not**
start a new line and does **not** open a fresh `%% Comments:` thread:

```latex
%% Comments: {JL} v0517: rewrite the above two, maybe just to be one single sentence. ========> {CC} v0517: merged the two agent fragments into one sentence; dropped the Table 1 cite.
```

**Format:** `<existing %% Comments: line> ========> {INITIALS} v<DATE>: <reply text>`
— eight equals signs, a `>`, a space, then `{INITIALS}` and the body
in the same `{INITIALS} text` form. The entire thread (question +
reply) lives on one physical line, so a question-and-answer pair stays
visually glued together.

The visual rule: `%% Comments:` opens a thread; `========>` appends a
reply to that same line. A reader skimming the file sees the original
ask and the response side-by-side without scanning down. A new
`%% Comments:` line is reserved for raising a **new** point on the
sentence, never for replying.

Multiple replies can chain on the same line:
```latex
%% Comments: {RA} R2.W1: Claim unsupported. ========> {JL} R2.W1: Added three citations and CIs. ========> {RA} R2.W1: Citations fine, numbers still soft. ========> {JL} R2.W1: Re-ran with 95% CIs; tightened.
```

Two unrelated reviewer threads on the same sentence stay as separate
`%% Comments:` lines, each with their own inline arrow replies:
```latex
%% Comments: {RA} R2.W1: Claim unsupported by evidence. ========> {JL} R2.W1: Added three citations.
%% Comments: {RA} R3.W2: Redundant with Section 4. ========> {JL} R3.W2: Removed here, kept in §4 only.
```

Only add `%% Comments:` lines when a reviewer comment is relevant to
that sentence. Not every sentence needs them. When you are *responding*
to an existing comment rather than raising a new point, always append
`========>` to the existing line, never open a new `%% Comments:` line.

**Variants:**

DELETE — sentence should be removed:
```latex
%
%% ---- P1.S4 [DELETE] ----
% Original sentence to be deleted.
```

DELETE blocks are **minimal**: just the tag and the original (commented
with single `%`). No active text. No `%% Reason:` or `%% Author:` lines.
Only add `%% Comments:` lines when a reviewer comment is relevant:

```latex
%
%% ---- P1.S6 [DELETE] ----
% This approach has generated valuable results, but faces a...
%% Comments: {RA} R1.W2: Claim unsupported at this point.
%% Comments: {JL} R1.W2: Deleted. Evidence now in Results section.
```

KEEP — no changes needed:
```latex
%
%% ---- P1.S1 ----
Original sentence that is fine.
%% KEEP
%% Author:
```

For KEEP, the original stays as the active text. No commented-out line
needed since the active text IS the original.

NEW — adding a sentence that doesn't exist in the original:
```latex
%
%% ---- P1.S4 [NEW] ----
%% Proposed: %%
New sentence text written per the revision plan.
%% Source: Adapted from old P2.S3 / written fresh per revision plan.
%% Reason: Needed to complete the argument in new P1.
%% Author:
```

For NEW sentences, `%% Proposed:` on its own line, then the new text
as the active line. `%% Source:` explains where the content comes from.

Complete rewrite:
```latex
%
%% ---- P1.S3 ----
% Original sentence here.
%% Proposed: %%
Completely different sentence here.
%% Changes:
%%   (1) Complete rewrite — refocused from X to Y
%% Reason: Aligns with agreed paragraph topic.
%% Author:
```

### Step 4: Present Summary

After annotating, show a readable before/after:

```
Paragraph P1 — Summary
========================

  S1: REVISE — simplify phrasing
  S2: REVISE — consolidate citations, remove vague claim
  S3: REWRITE — refocus on the core argument
  S4: DELETE — interrupts the argument
  S5: DELETE — belongs elsewhere
  ...

Result: N sentences → M sentences

All `%% Author:` fields are empty for your thoughts.
Accept and move to P2, or adjust something?
```

### Step 5: Author Feedback

Present the decision using `AskUserQuestion`:

```
AskUserQuestion(questions=[
  {
    question: "How do you want to proceed with P[N] annotations?",
    header: "P[N] Review",
    options: [
      {label: "Accept, next paragraph", description: "Annotations look good — move to P[N+1]"},
      {label: "Modify annotations", description: "Adjust specific sentences (tell CC which ones)"},
      {label: "Rethink paragraph", description: "Go back to paragraph logic discussion"}
    ],
    multiSelect: false
  }
])
```

The author can also pick "Other" to write in `%% Author:` fields or
provide free-text feedback.

---

Phase 2-fast: Reviewer Feedback Direct Apply
=============================================

**When the author invokes `/paper-revise <file> "<reviewer feedback>"` and
asks to "apply", "update with", or "clean with" reviewer comments, default
to this lightweight flow — NOT the full Phase 2 annotation block.**

The user wants the file to converge with minimum scaffolding. The full
`%% Proposed:` / `%% Changes:` / `%% Reason:` / `%% Author:` block (Phase 2
Step 3) is the wrong shape for this case — it was rejected as "too
complicated" in real use. Inline edits without a comment trail are also
wrong — they lose the audit record.

### The rule (do BOTH for each reviewer note)

1. **Update the active sentence text** to reflect the reviewer's
   suggestion (the actual edit lands in the prose).
2. **Attach a single `%% Comments: {INITIALS} v<DATE>: <verbatim or
   near-verbatim reviewer note>` line** under that sentence as the
   audit trail.

That's it. No `%% Proposed: %%`, no `%% Changes:`, no `%% Reason:`,
no `%% Author:`, no commented-out original line. The comment line IS
the trail; git history captures the diff.

### Format

```latex
%% ---- P1.SX [optional pass tag] ----
<updated active sentence>
%% Comments: {RA} v<YYMMDD>: <reviewer note, near-verbatim>
%
```

`{INITIALS} text` — space after the closing brace, no colon. Multiple
reviewers stack as separate `%% Comments:` lines.

### Multi-note consolidation and arrow conventions

When a sentence has **multiple coauthor notes** (and optional coauthor
self-replies), consolidate them into ONE `%% Comments:` line with visual
separators, then append the JL reply at the end. Two visual markers are
used — never interchange them:

| Marker | Role |
|---|---|
| `----------` (4+ dashes, no arrowhead) | **Separator** between coauthor notes on the same sentence |
| `==========>` (4+ equals + arrowhead) | **JL reply marker** — never used as a separator |
| `-----> {JL}` in the index header | **Resolved marker** — promoted into `%% ---- PX.SY -----> {JL} [...] ----` once every coauthor note on the sentence has a JL reply |

Multiple notes get `[1]`, `[2]`, `[3]` enumeration so the JL reply can
reference them by number:

```latex
%% ---- P2.S6 -----> {JL} [v0516 GG — lit-review = positioning] ----
What is missing is knowledge creation infrastructure ...
%% [1] Comments: {GG} v0515 note: [HL: "..."] rewrite the ending ... ---------- [2] Comments: {GG} v0515 reply: a literature review is positioning, not related-work. ==========> {JL} v0516: thanks GG. Applied (1) by adding P2.S7 (artifact + DIKW) and (2) by adding P2.S8 (contribution claim).
%
```

A single coauthor note drops the `[1]` prefix and the separator:

```latex
%% ---- P2.S4 -----> {JL} [v0515 GG — claim-verb softened] ----
Organizational learning theory signifies the importance of learning ...
%% Comments: {GG} v0515: claim-verb softened from "explains why" to "signifies the importance of". ==========> {JL} v0515: applied GG rewrite verbatim; dropped redundant "from experience".
%
```

**Why two distinct markers:**
- Dashes (`----------`) are visually quiet — they read as inter-note separators.
- Equals + arrowhead (`==========>`) are visually loud — they mark the *response* that closes the loop. `grep "==========>"` returns every JL reply in the file.
- The header `-----> {JL}` is the resolution-marker convention: `grep "-----> {JL}"` returns every fully-closed sentence block.

**Common mistakes to avoid:**
- Using `==========` (no arrowhead) as a note separator: conflates "still a coauthor note" with "JL replying". Use `----------` between notes.
- Using `==========>` for both separator AND reply: same problem. The arrowhead is reserved for JL.
- Forgetting to promote the index header to `-----> {JL}` after writing the JL reply: the audit grep will miss the block.
- Mixing `✅` with the arrow convention: ✅ is deprecated in this workflow; `-----> {JL}` replaces it.

### When to skip

- **Reviewer's note no longer has a target** (the underlying text was
  rewritten and the highlighted phrase is gone): skip both the edit
  and the comment, and report which were skipped at the end.
- **Reviewer's note is genuinely ambiguous** (e.g., a caret with `...`,
  or a vague rephrasing that could mean several things): ask via
  `AskUserQuestion` before applying. Don't attach an unresolved comment
  to a sentence whose text you've already edited.

### When to fall back to the full Phase 2 block

- Logic restructuring (paragraph reorganization, multi-sentence rewrite).
- Contested decisions where the trail of options/rationale matters.
- Cases where the author explicitly asks for the full block.

In all other reviewer-feedback applies, **default to Phase 2-fast**.

### Before/after example

Reviewer note (extracted from PDF):
- HL on `"DIKW"` → "use full form with DIKW in parens"

Wrong (full block — too much scaffolding for a one-line edit):
```latex
%% ---- P1.S6 ----
% The Agentic AI method, equipped with analytical tools and structured DIKW reasoning agents, ...
%% Proposed: %%
The Agentic AI method, equipped with analytical tools and structured Data-Information-Knowledge-Wisdom (DIKW) reasoning agents, ...
%% Changes:
%%   (1) "DIKW" → "Data-Information-Knowledge-Wisdom (DIKW)" — first-use spell-out
%% Reason: RA — acronyms must be spelled out on first appearance.
%% Comments: {RA} v0506: HL "DIKW" — use full form with DIKW in parens
%% Author:
```

Right (Phase 2-fast):
```latex
%% ---- P1.S6 ----
The Agentic AI method, equipped with analytical tools and structured Data-Information-Knowledge-Wisdom (DIKW) reasoning agents, produces superior interventions: ...
%% Comments: {RA} v0506: HL "DIKW" — use full form with DIKW in parens
%
```

---

Phase 3: Apply Mode (Author-Initiated Only)
=============================================

**CRITICAL:** Apply mode is ONLY invoked when the author explicitly runs:
```
/paper-revise 0-sections/01_introduction.tex apply
```

CC never applies changes or removes annotations on its own. The
annotations are a **persistent working document** — the author may:
- Apply changes manually by editing the file themselves
- Fill in `%% Author:` fields with their own thoughts
- Modify `%% Proposed:` lines before applying
- Leave annotations in place across multiple sessions
- Run `apply` when ready

When apply IS invoked:
1. Read the file, find all `%% ---- PX.SY ----` annotated sentences
2. For each:
   - `KEEP` → remove annotation lines, keep original sentence
   - `DELETE` → comment out the original sentence, remove annotations
   - `<proposed text>` → replace original with proposed, remove annotations
3. Remove all separator lines and annotation comments
4. Keep any reviewer/response macros in the active text (these are
   part of the paper's review workflow, not CC annotations)
5. Present summary of all changes

---

Phase 3b: Reindex Mode (Author-Initiated Only)
===============================================

**CRITICAL:** Reindex mode is ONLY invoked when the author explicitly runs:
```
/paper-revise <file> reindex
```

**Use case.** After splitting, merging, reordering, or inserting paragraphs,
the `%% ---- PX.SY ----` index tags become inconsistent with the new
paragraph structure (e.g., paragraph 1 was split into two paragraphs, so
everything below shifts +1). Reindex renumbers the index tags to match
the current physical paragraph layout — without changing any sentence
content, comments, or other annotation metadata.

**Algorithm:**
1. Walk the file from top to bottom.
2. Detect paragraph boundaries: a paragraph ends at a blank line that
   separates one block of active sentences from the next. Skip
   `\section{}`, `\subsection{}`, `\begin{figure}`/`\end{figure}`,
   and pure comment-block headers when computing boundaries.
3. Number paragraphs sequentially: P1, P2, P3, ... in order of physical
   appearance. Continue numbering across `\subsection{}` boundaries
   (paragraphs are continuous through the section unless the author
   explicitly asks for subsection-relative numbering).
4. Within each paragraph, number active `%% ---- PX.SY [...] ----`
   blocks sequentially as S1, S2, S3, ...
   - Preserve sub-letter suffixes (S3b, S6b) — these mark sentences
     inserted between others and should keep their letter unless the
     author asks for a full renumber.
   - DELETE blocks still get a sentence number (they hold a slot in
     the structure).
5. Update each tag's `PX.SY` while preserving the bracket note text
   (e.g., `[NEW per Gordon comment v2026-05-04]`).
6. Update **forward cross-references** in bracket notes that point to
   a paragraph that has shifted (e.g., "result preview belongs in P6
   (RQ1)" becomes "P7 (RQ1)" if RQ1's paragraph shifted from P6 to P7).
7. Leave **historical "was PX.SY" notes unchanged.** These are temporal
   records of older numbering and overwriting them erases revision
   history. Example: `[NEW, contribution, was P6.S6]` stays as-is even
   if the current sentence is now P7.S7.
8. Update section-header comment lines (e.g., `% NEW P3: Our Approach`
   → `% NEW P4: Our Approach`) when the paragraph index shifts.

**Workflow:**
1. Compute the proposed renumbering.
2. Present a diff to the author:
   ```
   Reindex preview
   ===============
   P3 split into P1+P2; downstream paragraphs shift +1.

   Tag changes:
     P2.S1 → P3.S1   (lines 52)
     P2.S2 → P3.S2   (line 54)
     ...
     P8.S8 → P9.S8   (line 237)

   Cross-reference fixes:
     P4.S5 bracket note: "P6 (RQ1)" → "P7 (RQ1)"
     Figure comment: "ref in P4.S1" → "ref in P5.S1"
   ```
3. Wait for author confirmation.
4. Apply edits.

CRITICAL: Reindex never modifies sentence text, `%% Comments:` lines,
`%% Proposed:`, `%% Reason:`, `%% Author:`, or any other annotation
content. Only the `PX.SY` portion of index tags and forward
cross-references move.

---

Phase 3c: Clean Modes (Light / Heavy)
======================================

**CRITICAL:** Clean modes are ONLY invoked when the author explicitly runs:
```
/paper-revise <file> clean-l1
/paper-revise <file> clean-l2
```

**Purpose.** Two levels of partial cleanup that strip annotation metadata
while preserving the structural skeleton. Useful when the file has
accumulated heavy annotation noise and the author wants a tidier working
document, but is **not yet ready** for the full `apply` reset (which
removes all index tags too).

The two levels differ only in whether `%% Comments:` lines are kept.

### Level 1: keep index + comments (`clean-l1`)

Keeps:
- `%% ---- PX.SY [...] ----` index header lines
- `%% Comments: ...` lines (reviewer/response trail)
- The active sentence text (after applying any proposed revision)

Removes:
- `%% Proposed: %%`, `%% Changes:`, `%% Reason:`, `%% Source:`,
  `%% Author:`, `%% KEEP` lines
- The commented-out `%` original line (since the proposed text becomes
  the active text)

### Level 2: keep index only (`clean-l2`)

Keeps:
- `%% ---- PX.SY [...] ----` index header lines
- The active sentence text (after applying any proposed revision)

Removes:
- Everything else: `%% Proposed:`, `%% Changes:`, `%% Reason:`,
  `%% Source:`, `%% Author:`, `%% KEEP`, `%% Comments:`, and the
  commented-out original

### Algorithm (both levels)

For each `%% ---- PX.SY [...] ----` block:
1. Determine the final active text:
   - If the block has `%% Proposed: %%` followed by an active line, use
     the active line as the kept text (the proposal is now the sentence).
   - If the tag carries `[DELETE]`, drop the active text entirely; keep
     the index header line on its own (the slot stays visible so reindex
     and re-discussion still work).
   - Otherwise keep the existing active text.
2. Strip the metadata lines per the level (above).
3. Re-emit the block with kept lines only.
4. Preserve the single `%` separator line between blocks.

### Workflow

1. Read the file and count what would change at the chosen level:
   ```
   Clean-l1 preview
   ================
   Will apply 17 proposed revisions.
   Will remove 42 metadata lines (Proposed/Changes/Reason/Source/Author/KEEP).
   Will keep 23 %% Comments: lines.
   Will keep 31 index header lines (incl. 4 [DELETE] slots).
   ```
2. Show 2-3 sample blocks before/after so the author can verify the
   transformation looks right.
3. Wait for author confirmation.
4. Apply edits.

CRITICAL: Both levels are **partial** cleanups. The file is still in
"annotation mode" after `clean-l1` or `clean-l2` — index tags persist,
so `/paper-revise` can resume targeted work, and re-running discussion
on individual sentences still works. The full reset is `apply`.

If the author wants `clean-l1` followed by `apply` later, that's fine —
`apply` operates on whatever state remains. But `clean-l2` discards
`%% Comments:` lines permanently, so warn the author if comments contain
unaddressed reviewer feedback.

---

Resuming a Session
==================

When `/paper-revise <file>` is invoked on a file that already has annotations:

1. **Detect existing state:**
   - Revision plan at the bottom (`%% REVISION PLAN`) → read it for context
   - `%% ---- PX.SY ----` annotation blocks → note which paragraphs are done
   - `%% Author:` fields with content → the author has left feedback

2. **Report what's already done:**
   Show the author: "Found revision plan + annotations for P1-P4.
   P5-P8 are not yet annotated. Resume from P5?"

3. **Resume from where the author left off.** Skip re-annotating
   paragraphs unless the author explicitly asks to revisit them.
   If the author filled in `%% Author:` fields with objections or
   new ideas, address those before moving forward.

4. **If the revision plan has changed** (author edited it manually),
   acknowledge the changes and adjust the annotation approach.

---

Discussion Style
================

CC is an **active collaborator**:

- **Ask questions** — "This paragraph mixes two topics. Split or keep?"
- **Offer analysis** — "S7-S9 make claims before the evidence is
  presented. Want to move them to Discussion or cut them?"
- **Ask for raw input** — "What do you want this paragraph to say in
  your own words? I'll help turn it into formal text."
- **Flag inconsistencies** — "The abstract says X but this says Y."
- **Suggest alternatives** — "Instead of deleting, we could move to P5."
- **Connect to author's comments** — "You said you wanted to strengthen
  the motivation. S3 is the right place for that."
- **Respect author authority** — Author has final say. If they disagree,
  record their reasoning in `%% Author:` and move on.
- **Write like a human researcher** — Proposed text should read like it
  was written by an academic, not generated by AI. Avoid em dashes (---),
  rhetorical flourishes, and overly polished phrasing. Prefer plain
  academic prose: semicolons, colons, "which" clauses, and simple
  conjunctions. When in doubt, write plainly.

---

Cross-Section Consistency
=========================

When revising one section, check what other sections say about the same
topics. Common consistency issues:
- Terminology changes must propagate (if you rename a concept in one
  section, grep for the old name across all sections)
- Content moved between sections must not be duplicated (e.g.,
  interpretation moved from Results to Discussion)
- Claims in Introduction must match what Results actually show
- Contribution list in Introduction/Conclusion must stay aligned
- Notation introduced in Method must be used consistently in Results
- Abstract claims must reflect the revised content, not the old version

After annotating, do a quick consistency check and flag any cross-section
issues for the author.

---

Self-Review Step
================

After completing annotations for a section, review your own work:
- Did you follow the annotation format consistently?
- Are all relevant reviewer comments addressed with `%% Comments:` lines?
- Do `%% Comments:` lines use the paper's own comment macros (detected
  in Phase 1)?
- Does proposed text avoid em dashes, promotional language, AI-sounding prose?
- Are there cross-section inconsistencies?

Present the review honestly to the author. If you find issues, fix them
before declaring the section complete.

---

Size Benchmarking
=================

When revising a section, compare the proposed size against:
1. The current version (how much are we cutting/adding?)
2. A reference paper at the target venue (if the author names one)
3. Typical page limits for the venue (if known)

Present a comparison table:
```
| Section      | Current       | Proposed      | Reference (if any) |
|--------------|---------------|---------------|---------------------|
| Introduction | ~70 sentences | ~48 sentences | ~47 sentences       |
| Method       | ~55 sentences | ~50 sentences | ~52 sentences       |
| Results      | ~43 sentences | ~38 sentences | ~40 sentences       |
```

This helps the author gauge whether the revision is too aggressive or
too conservative. If no reference paper is available, comparing current
vs. proposed is still valuable for tracking scope changes.

---

Session Flow
============

```
/paper-revise <file> ["author comments"]
        │
        ▼
   Phase 1: Section-Level Review
   ├── Read file, detect structure
   ├── Present section map (address author comments)
   ├── Prepare decision questions (numbered, with context)
   ├── Discuss questions one by one with author
   ├── Describe proposed structure (with size comparison)
   ├── Author confirms structure
   └── Record agreed revision plan at BOTTOM of file
        │
        ▼
   Phase 2: Annotation
   ├── For minor edits: one paragraph at a time
   │   ├── Present paragraph + analysis
   │   ├── Discuss logic, then annotate
   │   ├── Author accepts or adjusts
   │   └── Move to next paragraph
   ├── For structural rewrites: batch annotate after
   │   full structure is agreed (more efficient for
   │   large reorganizations)
   ├── Add reference links for new citations
   ├── Self-review annotations
   └── Present complete summary

   Phase 2-fast: Reviewer Feedback Direct Apply
   ── When invocation includes reviewer comments + "apply"/"update with"
   │   ├── For each reviewer note that targets a specific sentence:
   │   │   ├── Update the active text inline
   │   │   └── Attach ONE %% Comments: {INITIALS} v<DATE>: ... line
   │   ├── Skip notes whose target text was rewritten (report skipped)
   │   ├── Ask via AskUserQuestion if the suggestion is ambiguous
   │   └── NO %% Proposed / Changes / Reason / Author blocks
        │
        ▼
   File now has:
   - Revision plan at bottom of file
   - Sentence annotations with PX.SY separators
   - Reference links with DOI/URLs
   - Empty %% Author: fields for author's thoughts
   Author works with this at their own pace.
        │
        ▼
   (Optional, author-initiated — three reset modes)
   /paper-revise <file> reindex
   └── Renumber PX.SY tags after structural shifts (Phase 3b)
       Preserves all sentence text, comments, and metadata.

   /paper-revise <file> clean-l1
   └── Apply proposed revisions; strip Proposed/Changes/Reason/Author
       lines but KEEP index headers + %% Comments: trail (Phase 3c).

   /paper-revise <file> clean-l2
   └── Apply proposed revisions; strip everything except index headers
       (drops %% Comments: too) (Phase 3c).

   /paper-revise <file> apply
   └── Full reset: replace originals with accepted proposals, remove
       ALL annotation scaffolding including index tags (Phase 3).
```
