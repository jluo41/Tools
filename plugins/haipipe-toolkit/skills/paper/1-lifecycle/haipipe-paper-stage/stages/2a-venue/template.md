<!-- TEMPLATE (follow, don't ship). Fill 0-lifecycle/2-venue/S-Venue-0-venue.md from this skeleton: replace every <…>, and each `<!-- RULE: … -->` comment is guidance to FOLLOW then DELETE. Delete this top line too. -->
2a-venue: <paper title>
========================

Date: YYYY-MM-DD
Status: DRAFT | pinned (<outlet>, <year>)
Pack: playbook-<slug> @ <venue commit short-hash>
Outlet: <journal-dir>   (directory under the pack; THIS stage resolves every section guide from it — see Section Styles)


Venue Decision
--------------
<!-- RULE: which outlet, and WHY its rewards match the paper's strongest claim. Give the agent's RANKED suggestion — the pick + 1-2 backups (one-line why each) + the nearest rejected (its hard disqualifier). Then which claim hits which reward, as RECORD LINES, never a pipe table. Include the outlet's one-sentence desk test + this paper's answer, and the desk-reject risks this paper could trip + how it avoids them. Cite a fit question inline where the decision rests on one, e.g. [Q-Venue-1]. -->

**<Outlet full name>** (<pack slug>).
<one sentence: why this venue's rewards match the paper's strongest claim.>
Backup: <outlet 2> (<why>); <outlet 3> (<why>).
Rejected: <nearest-miss venue> — <the hard disqualifier>.
Audience: <who reads it, what they do with it>.
Desk test: "<the taste.md one-sentence test verbatim>" — <this paper's answer>.
Desk-reject risks: <the 1-2 No-list signals this paper could trip, and how it avoids them>.
Fit (record lines):
- H1 <primary> — <the reward/taste signal it satisfies> — <residual risk>. [Q-Venue-1]
- H2 <supporting> — <…> — <…>.


Relevant Files
--------------
<!-- RULE: the venue packs/guides this decision + requirements REST ON — one line each, what it gives us. Sourced from `../../../venue/playbook-<slug>/`. These are the files pitch/narrative/display/section-edit deep-dive later via the [source: …] tags recorded below. -->

- `playbook-<slug>/<journal>/taste.md` — desk-accept/reject signals + the one-sentence test.
- `playbook-<slug>/<journal>/<journal>-<section>/style.md` — per-section quantitative norms (Micro-norms).
- `playbook-<slug>/<journal>/examples/` — stored exemplars (measure these when a section guide is missing).


Section Styles (RESOLVED here — downstream reads this table, never re-derives)
------------------------------------------------------------------------------
<!-- RULE: THIS stage resolves every section style path, ONCE, and writes the result below.
     No downstream stage globs, finds, or spells a pack path — section-edit reads its row and stops.
     Resolution is a GLOB, never string concatenation: the per-journal slug is arbitrary and
     sometimes multi-token (MISQ- · jno- · diabcare- · npjdm- · natcomm- · MS-IS-), so
     concatenation happens to work for MISQ and FAILS on six other outlets.
       VEN=$(find -L ~/.claude/skills ./.claude/skills "${CLAUDE_PLUGIN_ROOT:-/nonexistent}" -type d -maxdepth 4 -path '*skills/paper/venue' 2>/dev/null | head -1)
       "$VEN/<pack>/<outlet>"/*-<kind>/style.md
       "$VEN/<pack>/<outlet>"/*-<kind>/template.md
     WHICH kinds to look for, and which this outlet actually HAS, is in
     `stages/2a-venue/section-kinds.yml` (closed set of 10; `theory-model` aliases to `theory`;
     `theory` and `related-work` are DIFFERENT sections, never aliased to each other).
     One record line per kind. Every line carries BOTH labelled fields. For a missing file write
     exactly `style: — blueprint-only` or `template: — generic-fallback`, so a reader can tell
     "no pack file" apart from "not checked". Record lines, never a pipe table. -->

abstract · style: <resolved .../*-abstract/style.md | — blueprint-only> · template: <resolved .../*-abstract/template.md | — generic-fallback>
introduction · style: <resolved .../*-introduction/style.md | — blueprint-only> · template: <resolved .../*-introduction/template.md | — generic-fallback>
theory · style: <resolved .../*-theory/style.md | — blueprint-only> · template: <resolved .../*-theory/template.md | — generic-fallback>
related-work · style: <resolved .../*-related-work/style.md | — blueprint-only> · template: <resolved .../*-related-work/template.md | — generic-fallback>
methods · style: <resolved .../*-methods/style.md | — blueprint-only> · template: <resolved .../*-methods/template.md | — generic-fallback>
results · style: <resolved .../*-results/style.md | — blueprint-only> · template: <resolved .../*-results/template.md | — generic-fallback>
discussion · style: <resolved .../*-discussion/style.md | — blueprint-only> · template: <resolved .../*-discussion/template.md | — generic-fallback>
appendix · style: <resolved .../*-appendix/style.md | — blueprint-only> · template: <resolved .../*-appendix/template.md | — generic-fallback>
letter · style: <resolved .../*-letter/style.md | — blueprint-only> · template: <resolved .../*-letter/template.md | — generic-fallback>
significance · style: <resolved .../*-significance/style.md | — blueprint-only> · template: <resolved .../*-significance/template.md | — generic-fallback>


Requirements (what the final paper must do)
-------------------------------------------
<!-- RULE: the venue's demands the final paper MUST meet — the "results" this stage hands to pitch/narrative/display/section-edit. TRANSCRIBE every number from the pack's `<journal>-<section>/style.md` (word budget + `## Micro-norms`), tag its source, NEVER invent; if a guide is missing, measure 2-3 stored exemplars and say so. Hard caps (word/display limits) stay caps even if exemplars deviate; carry any measured-vs-budget clash or "to verify" caveat verbatim.
     · Structural Blueprint — one block per manuscript section, in order.
     · Writing Principles — the prose companion to the blueprint. -->

### Structural Blueprint
Section: <name> (<role>)
  Subsections: <count> (<names>)
  Paragraphs / subsection: <count or range>
  Sentences / paragraph: <count or range (median ~k)>
  Avg sentence length: <words (median ~k)>
  Citation density: <cites per sentence, where they cluster>
  Results detail: <coefficients, p-values, effect sizes, CIs, none>
  Display units: <which figures/tables belong here>
  Adaptation: <how THIS paper's claims map onto the section, e.g. H1 → subsection 2>
  [source: <journal>-<section>/style.md "<heading>" + "Micro-norms (measured <date>)"]
<repeat per section: abstract, introduction, theory/related-work, methods, results, discussion, appendix, + venue-specific units (Key Points box, Significance Statement…)>

### Writing Principles
Language/tone: <formal vs accessible, jargon level, hedging conventions>.
Citation style: <in-text format, numbered vs author-year>.
Results presentation: <tables vs figures, statistical reporting, causal-language rules>.
Display limits: <max figures/tables, extended-data/supplement caps — journal HARD RULES>.
Abstract: <word limit, structure (prose vs labeled), arc>.
[source: <pack>/style-profile.md + section-guide anti-patterns]


Q-consumer
----------
<!-- RULE: logical source for Board `## Aims`: each venue-fit question becomes one
     `- P<n> · Q-Venue-<n>` Aim record there, with Done when / Description / Reason / Probe / Answer.
     ANSWERABLE + SPECIFIC — a concrete lookup (recent-publications check, competing-paper /
     editor check), never a vague "is this a good fit?". `Reason` names the venue decision or
     requirement it bears on; cite it inline in Venue Decision. -->

- P<n> · Q-Venue-<n> · <question title — e.g. recent-publications check>
  **Done when:** The answer has landed, been interpreted, and been woven into Content.
  **Description:** <the specific lookup — one sentence per line>
  **Reason:** <which venue decision/requirement it bears on, and why it matters if wrong>
  **Probe:** not opened yet
  **Answer:** <empty in DRAFT — PROBE fills it: the finding + [source: PP<nn>]>
