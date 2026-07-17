# venue-template.md

Fill-in skeleton for `0-lifecycle/2-venue/2-venue.md`.
Same conventions as the sibling stage templates: `=====` for the document title, `-----` for sections, no `#` headings, one sentence per line.
Every number in the Structural Blueprint is TRANSCRIBED from the pinned outlet's `<journal>-<section>/style.md` (word budget + `## Micro-norms` block) and tagged with its source; numbers are never invented.

```text
2-venue: <paper title>
=======================

Date: YYYY-MM-DD
Status: DRAFT | pinned (<outlet>, <year>)
Pack: playbook-<slug> @ <venue commit short-hash>
Outlet: <journal-dir>   (the directory name under the pack, e.g. jama-im -- downstream resolves section guides from this)
Blueprint derived: YYYY-MM-DD from <journal>-*/style.md (Micro-norms measured <date>)


Venue Choice
------------

**<Outlet full name>** (<pack slug>).
<One sentence: why this venue's rewards match the paper's strongest claim.>
<One sentence: what the enabler is and why it is not the claim (if applicable).>
Backup: <outlet 2> (<one-line why>); <outlet 3> (<one-line why>).
Rejected: <nearest-miss venue> -- <the hard disqualifier, one line>.


Venue Profile
-------------

Audience: <who reads this journal and what they do with it>.
Rewards: <2-4 desk-accept signals, digested from <journal>/taste.md>.
Desk-reject risks for THIS paper: <the 1-2 No-list signals this paper could trip, and how it avoids them>.
One-sentence test: "<the taste.md test verbatim>" -- <one line: this paper's answer>.


Structural Blueprint
--------------------

<One block per manuscript section, in manuscript order.>
<Transcribe measured values; keep ranges as ranges; carry any measured-vs-budget clash or "to verify" caveat the guide flags.>

Section: <name> (<role in the paper>)
  Subsections: <count> (<subsection names>)
  Paragraphs per subsection: <count or range>
  Sentences per paragraph: <count or range (median ~k)>
  Avg sentence length: <words (median ~k)>
  Citation density: <citations per sentence, and where they cluster>
  Results reported: <yes/no>
  Results detail: <coefficients, p-values, effect sizes, CIs, none>
  Display units: <which figures/tables belong here>
  Adaptation: <how THIS paper's claims map onto the section, e.g. H1 -> subsection 2>
  [source: <journal>-<section>/style.md "<heading>" + "Micro-norms (measured <date>)"]

<Repeat per section: abstract, introduction, theory/related-work, methods, results, discussion, appendix/supplement, plus venue-specific units (Key Points box, Significance Statement, ...).>


Writing Principles
------------------

Language/tone: <formal vs accessible, jargon level, hedging conventions>.
Citation style: <in-text format, numbered vs author-year>.
Results presentation: <tables vs figures, statistical reporting, effect-size conventions, causal-language rules>.
Display limits: <max figures/tables, extended-data or supplement caps -- journal HARD RULES stay rules even if exemplars deviate>.
Abstract conventions: <word limit, structure (prose vs labeled), arc>.
[source: <pack>/style-profile.md + section-guide anti-patterns]


Fit Assessment
--------------

| Claim | Venue scope hit | Residual risk |
|---|---|---|
| H1 <primary> | <which reward/taste signal it satisfies> | <what could still bounce it> |
| H2 <supporting> | <...> | <...> |
| H3 <supporting> | <...> | <...> |


Q-consumer
----------

The venue-fit questions this stage raises — one ## per question: id, title, what it wants.
(Route + who answers organized at APPROVE, into the probe file.)

## Q1 · <recent-publications check>
<Has this venue published adjacent work in the last 2-3 years; who edited it; what it implies for framing.>

## Q2 · <competing-paper / editor check>
<...>
```

## Rules

- **Transcribe, don't invent.** Blueprint numbers come from the outlet's section guides; if a guide is missing, measure 2-3 stored exemplars in `<journal>/examples/` and say so in the source tag.
- **Hard caps stay caps.** Journal-imposed limits (word caps, display caps) are rules; measured exemplar deviations are annotations, never a new budget.
- **Carry caveats.** A guide's measured-vs-budget clash or "to verify" marker transfers into the blueprint block verbatim intent; do not silently pick one number.
- **Staleness check.** If `venue` has moved past the recorded pack commit, re-derive the blueprint (re-transcribe Micro-norms); the venue pin itself does not change unless the user retargets.
- **Retarget = full rewrite.** A new outlet rewrites this whole file; claims is venue-free and survives.
