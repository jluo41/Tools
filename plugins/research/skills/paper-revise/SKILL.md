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
```

Examples:
```
/paper-revise 0-sections/01_introduction.tex
/paper-revise 0-sections/03_method.tex "Reviewer 2 says the notation is inconsistent with Section 4. Tighten the problem setup."
/paper-revise 0-sections/05_results.tex "Subgroup analysis needs more statistical rigor per R1. Also cut redundancy with the appendix."
/paper-revise 0-sections/01_introduction.tex apply
```

The author can provide:
- Just a file → CC reads, analyzes, and starts section-level discussion
- A file + comments → CC uses the comments to guide its analysis and priorities
- A file + "apply" → CC applies all accepted annotations (Phase 3)

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

**Present all questions at once.** Then discuss one by one with the
author. This is more efficient than discovering issues mid-annotation.

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
reorganization, discuss here. The author may want to:
- **Accept the structure** → proceed to annotation
- **Reorder subsections** → CC adjusts, re-presents
- **Merge/split subsections** → CC proposes how
- **Change what a subsection argues** → CC revises the plan

This discussion may take multiple rounds. That's expected and valuable.

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

Ask questions that invite both minor and major changes:

```
For this paragraph:

1. What is the ONE point this paragraph should make?
2. [Specific question about logic, not just wording]
3. [Flag if the current sentences don't match the agreed role from Phase 1]

Current logic: [CC's reading of what the paragraph currently argues]
Agreed role:   [what this paragraph should do per the revision plan]
Gap:           [where current logic doesn't match the agreed role]

Options:
  A. Keep the logic, just tighten sentences
  B. Restructure — keep some sentences, rewrite others to match new logic
  C. Rewrite from scratch — tell me what you want it to say

Or give me your raw thoughts and I'll help shape them.
```

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
%% Comments: [reviewer macro]{R1.Q3: Needs stronger statistical support.}
%% Comments: [author macro]{R1.Q3: Added significance tests and CIs.}
%% Author:
```

**KEY CONVENTION:** The original sentence is commented out with a single
`%` prefix. The `%% Proposed:` label sits on its own line. The revised
text follows as the ACTIVE line (no prefix, compiles in LaTeX).
Metadata lines (`%% Changes:`, `%% Reason:`, `%% Comments:`, `%% Author:`)
use `%%` prefix as before.

**The `%% Comments:` lines** use whatever comment macros the paper
defines (detected in Phase 1 Step 1). Common patterns:
- `\ra{}`/`\jl{}` — reviewer/author initials
- `\rev{}`/`\resp{}` — reviewer comment/response
- `\RC{}`/`\AR{}` — reviewer comment/author response
- `\todo{}` — general action items

The author can copy these directly into Overleaf where they compile
with the paper's existing macros. This ensures:
- The reviewer's original comment is preserved alongside the change
- The author's reply explains what was done
- Coauthors see the full discussion trail

If no comment macros are detected, use plain text:
```latex
%% Comments: [R1.Q3] Needs stronger statistical support.
%% Comments: [Response] Added significance tests and CIs.
```

Multiple reviewer comments stack on separate lines:
```latex
%% Comments: [reviewer macro]{R2.W1: Claim unsupported by evidence.}
%% Comments: [author macro]{R2.W1: Added three citations and quantitative comparison.}
%% Comments: [reviewer macro]{R3.W2: Redundant with Section 4.}
%% Comments: [author macro]{R3.W2: Removed here, kept in Section 4 only.}
```

Only add `%% Comments:` lines when a reviewer comment is relevant to
that sentence. Not every sentence needs them.

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
%% Comments: [reviewer macro]{R1.W2: Claim unsupported at this point.}
%% Comments: [author macro]{R1.W2: Deleted. Evidence now in Results section.}
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

**Wait for author response.** They may:
- **Accept** → move to next paragraph
- **Modify** → CC adjusts specific annotations
- **Add thoughts** → author writes in `%% Author:` fields themselves later
- **Rethink** → go back to paragraph discussion

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
   (Optional, author-initiated)
   /paper-revise <file> apply
   └── Replace originals with accepted proposals, clean up
```
