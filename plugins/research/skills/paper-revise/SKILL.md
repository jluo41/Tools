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
/paper-revise 0-sections/01_introduction.tex "Focus on reviewer comments about evidence gaps. I want the opening to land the one-shot evaluation problem faster."
/paper-revise 0-sections/03_method.tex "Make the DIKW explanation less jargon-heavy. Reviewer C#11 is right that the IT analogy is forced."
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
- Reviewer comments = `\ra{}`, `\rahigh{}`, or any comment patterns
- Existing annotations = `%% Proposed:`, `%% Diff:`, or similar
- Figure/table blocks = `\begin{figure}` ... `\end{figure}` (skip these)

Number paragraphs sequentially: P1, P2, P3, ... based on order of
appearance. If subsections exist, note them: P1 (under §2.1), etc.

### Step 2: Present Section Map

Show the author a **readable section map** — NOT raw LaTeX:

```
Section: Introduction (01_introduction.tex)
============================================

Structure:
  P1  Context — [topic summary from first sentence]          [N sentences]
  P2  Gap — [topic summary]                                   [N sentences]
  --  Figure 1 placement
  P3  Opportunity — [topic summary]                            [N sentences]
  P4  Challenge — [topic summary]                              [N sentences]
  §Research Questions
    P5  RQ intro                                               [N sentences]
    P6  RQ1 — [topic]                                          [N sentences]
    P7  RQ2 — [topic]                                          [N sentences]
  ...

Reviewer Comments:
  [list any reviewer comments found, grouped by paragraph]

[If author provided comments, address them here:]
Author's Direction: "Focus on reviewer comments about evidence gaps..."
  → This affects P1 (S3-S6 lack citations) and P3 (scale claims unsupported)

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
per subsection. If a reference paper (e.g., Chen & Chan) was used as
a size benchmark, compare against it.

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
%%   - [e.g., "Remove IT paradox framing entirely"]
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

**Annotation format (compile-ready):**

The proposed text is ACTIVE (uncommented, compiles in LaTeX).
The original text is COMMENTED OUT with single `%` prefix.
This way the file always compiles with the latest proposed changes.

```latex
%
%% ---- P1.S1 ----
% Original sentence text here.
%% Proposed:
Revised sentence text here.
%% Changes:
%%   (1) "old phrase" → "new phrase"
%%   (2) "another old" → "another new"
%% Reason: Why this change serves the agreed paragraph topic.
%% Comments: \ra{C\#7: Reader wants evidence -- not just opinion.}
%% Comments: \jl{C\#7: Added citations. Removed unsupported claim.}
%% Author:
```

**KEY CONVENTION:** The original sentence is commented out with a single
`%` prefix. The `%% Proposed:` label sits on its own line. The revised
text follows as the ACTIVE line (no prefix, compiles in LaTeX).
Metadata lines (`%% Changes:`, `%% Reason:`, `%% Comments:`, `%% Author:`)
use `%%` prefix as before.

**The `%% Comments:` lines** contain copy-pasteable `\ra{}` and `\jl{}`
macros. The author can copy these directly into Overleaf where they
compile with the paper's existing comment macros. This ensures:
- Ritu's original comment is preserved alongside the change
- The author's reply explains what was done
- Coauthors on Overleaf see the full discussion trail

Multiple reviewer comments stack on separate lines:
```latex
%% Comments: \ra{C\#11: IT value analogy feels contrived.}
%% Comments: \jl{C\#11: Removed IT paradox framing per revision plan.}
%% Comments: \ra{C\#13: Again, said before. REDUNDANT.}
%% Comments: \jl{C\#13: Stated once in P2, removed elsewhere.}
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
% This approach has generated valuable interventions, but faces a...
%% Comments: \ra{C\#7: Reader wants evidence -- not just opinion.}
%% Comments: \jl{C\#7: Deleted. Now supported empirically in RQ3 results.}
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
%% Proposed:
The next design cycle then restarts from intuition rather than building on accumulated experimental evidence.
%% Source: Adapted from old P2.S3 / written fresh per revision plan.
%% Reason: Needed to complete the one-shot argument in new P1.
%% Author:
```

For NEW sentences, `%% Proposed:` on its own line, then the new text
as the active line. `%% Source:` explains where the content comes from.

Complete rewrite:
```latex
%
%% ---- P1.S3 ----
% Original sentence here.
%% Proposed:
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
  S2: REVISE — remove "gold standard", consolidate citations
  S3: REWRITE — refocus on one-shot evaluation gap
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
4. Keep reviewer macros (`\ra{}`, etc.)
5. Present summary of all changes

---

Converting Old Annotations
===========================

If the file has old-format `%% Diff:` lines, convert them during
paragraph processing:

Old format:
```latex
Sentence text.
%% Diff: -Sentence text.- ++Revised text.++
%% Reason: Explanation.
```

Convert to:
```latex
%
%% ---- PX.SY ----
Sentence text.
%% Proposed: Revised text.
%% Changes:
%%   (1) [specific phrase-level changes]
%% Reason: Explanation.
%% Author:
```

---

Discussion Style
================

CC is an **active collaborator**:

- **Ask questions** — "This paragraph mixes two topics. Split or keep?"
- **Offer analysis** — "The reviewer is right that S7-S9 are unsupported
  this early. Want to move them or cut them?"
- **Ask for raw input** — "What do you want this paragraph to say in
  your own words? I'll help turn it into formal text."
- **Flag inconsistencies** — "The abstract says X but this says Y."
- **Suggest alternatives** — "Instead of deleting, we could move to P5."
- **Connect to author's comments** — "You said you wanted to emphasize
  the one-shot gap. S3 is the right place for that."
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
- Terminology changes (e.g., removing "IT paradox") must propagate
- Content moved between sections (e.g., interpretation from Results to
  Discussion) must not be duplicated
- RQ framing in intro must match RQ references in Results and Discussion
- Contribution claims in Discussion must match intro's RQ structure

After annotating, do a quick consistency check and flag any cross-section
issues for the author.

---

Self-Review Step
================

After completing annotations for a section, review your own work:
- Did you follow the annotation format consistently?
- Are all relevant reviewer comments addressed with `%% Comments:` lines?
- Are `%% Comments:` lines copy-pasteable `\ra{}` and `\jl{}` macros?
- Does proposed text avoid em dashes, promotional language, AI-sounding prose?
- Are there cross-section inconsistencies?

Present the review honestly to the author. If you find issues, fix them
before declaring the section complete.

---

Size Benchmarking
=================

When revising a section, compare the proposed size against:
1. The current version (how much are we cutting/adding?)
2. A reference paper at the target venue (e.g., Chen & Chan 2024 for MS)

Present a comparison table:
```
| Section | Current | Proposed | Reference paper |
|---|---|---|---|
| Intro | ~70 sentences | ~48 sentences | ~47 sentences |
| Lit review | ~43 sentences | ~34 sentences | ~38 sentences |
```

This helps the author gauge whether the revision is too aggressive or
too conservative.

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
