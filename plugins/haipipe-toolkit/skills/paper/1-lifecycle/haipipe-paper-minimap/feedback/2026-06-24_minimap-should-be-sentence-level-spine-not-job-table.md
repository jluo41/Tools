---
status: open
created: 2026-06-24
context: haipipe-paper-minimap skill (1-lifecycle/haipipe-paper-minimap); felt while reviewing 5-minimap.tex on Paper-Personality-Opioid-MedJournal
---
The minimap is not what I want. I want it to be like the detailed spine of the
full paper: we follow the section, then the paragraph, then the sentence. Each
sentence may just be very concise, like what point this sentence is meant to
convey. And you need to include the displays. It is more like the real paper
with the concise sentences as the point, more like the outline.

Distilled ask:
- The minimap should NOT be a paragraph-job table ("Section | Para | Job |
  Evidence anchor"). That format is too abstract and reads nothing like the
  paper.
- It should be a SENTENCE-LEVEL SPINE of the actual manuscript: Section ->
  Paragraph -> Sentence, where each sentence is a CONCISE one-line point
  stating what that sentence will convey. Think "the paper, telegraphed" — an
  outline a reader can scan top to bottom and see the whole argument unfold
  sentence by sentence.
- DISPLAYS must be placed INLINE, at the exact point in the spine where the
  figure/table is first discussed (e.g. a "Table 2 about here" callout inside
  the Results paragraph that introduces it), not only listed in a side column.
- The result should read like the real paper in miniature: section headers
  matching the manuscript (Abstract, Introduction, Methods, Results,
  Discussion, Conclusion), each paragraph broken into its sentence-points, with
  display callouts interleaved.

Why this matters:
- The minimap is the contract the write stage consumes. A job table tells the
  writer the abstract role of a paragraph but not the actual argument; a
  sentence-level spine tells the writer the exact line of reasoning, so the
  draft can be written almost directly from it.
- It also lets the author audit the whole argument fast: every claim and every
  display is visible in its real narrative position, sentence by sentence,
  before any prose is written.

Proposed solution:
1. Change the minimap TEMPLATE from the "paragraph-job" tabular to a
   sentence-level outline: `\section*{N. <Section>}` ->
   `\paragraph{<Pn> [role]}` -> a compact enumerated list where each item is one
   concise sentence-point (one idea, no em-dash, plain language), with the
   claim id tagged where relevant.
2. Place each display as an inline callout at its first-discussed paragraph,
   e.g. a boxed/bold line "[Figure 1 here: STROBE cohort flow — C0]".
3. Keep the Style Contract block (it bridges to write-principles.md) and the
   Write-Time Reconciliations as short bookend sections, but make the
   sentence-level spine the BODY.
4. Keep a small claim-and-display crosswalk at the end as a coverage check
   (no orphan claim / no orphan display), but it is secondary to the spine.

Where it touches:
- haipipe-paper-minimap/SKILL.md: replace the paragraph-job-table guidance with
  the sentence-level-spine guidance; state the display-inline rule.
- haipipe-paper-minimap/ref/ (minimap-template.tex or equivalent): ship a
  sentence-level-spine template the skill writes from.

Applied (same day, ProjB instance): 5-minimap.tex on
Paper-Personality-Opioid-MedJournal was rewritten by hand to the sentence-level
spine format (Abstract + Intro I1-I4 + Methods M1-M5 + Results R0-R6 +
Discussion D1-D5 + Conclusion, each paragraph as concise sentence-points, all six
displays placed inline). The SKILL.md + ref template update is still OPEN so the
format becomes the default for future papers.

## Recurrence 2026-06-24 (same session, format refined further)

The same session iterated the minimap format through several more user asks. ALL
of these should fold into the SKILL.md + ref/template update (still OPEN), so the
sentence-level spine ships with this shape by default:

1. Inline displays must be BOXED and SHRUNK to small thumbnails (not full-size
   floats). Implemented by redefining figure/table to a non-floating
   `\fbox{\scalebox{\mmscale}{...}}` block (`\mmscale` 0.5), with a `\@captype`
   trick so the fragment's plain `\caption` still works outside a float.
2. Paragraph index format is `<Section>.P<n>` (I.P1, M.P1, R.P0, D.P5), NOT
   I1/M1/R0.
3. Title is `Minimap: <the paper's real title>` (pull from the manuscript's
   `\title`), not a generic "Sentence-Level Spine of the Manuscript".
4. After each paragraph's sentence-points, add a CONCISE narrative note (small
   gray, hook-arrow) PULLED and condensed from `3-narrative.tex`'s already-vetted
   `\rev{}` comments. Do NOT self-author these (memory: limp if self-authored);
   transcribe the narrative's.
5. Structure must follow the VENUE. For JAMA family (consult
   `_venue/playbook-jama-portfolio` README + style-profile): Key Points
   (Question/Findings/Meaning) + structured Abstract + ~3-paragraph Introduction
   (problem -> gap -> question, each sentence anchored to a number or citation) +
   Methods + Results + Discussion (ending with Limitations) + Conclusions +
   Supplement/eAppendix.
6. Supplement displays (eTable/eFigure) RENDER in the Supplement section and are
   only CITED from Results; main-text displays render inline in their section.
   The Supplement also lists the full SI inventory (e.g. full comorbidity table,
   spec ladder, robustness, sensitivity).
7. Conclusions stays SHORT (1-2 sentences) per the JAMA norm (Schroeder 2,
   Burns 1); optionally fold it into the last Discussion beat rather than a
   separate section (strict IMRAD). Do not pad it.
8. Calibrate paragraph richness to the venue exemplar: a too-thin paragraph
   (e.g. a 2-sentence Intro opener) reads as under-built; JAMA intro paragraphs
   run ~3-5 sentences, each carrying a concrete statistic or citation.

Net: the minimap is "the paper in miniature," venue-shaped, derived from
narrative + claims + display, with boxed-thumbnail displays and per-paragraph
narrative notes. Still no professor/advisor comment layer exists in this paper;
when one does, add it as a second per-paragraph note tier (e.g. `\pnote` tagged
to the advisor) alongside the narrative note.
