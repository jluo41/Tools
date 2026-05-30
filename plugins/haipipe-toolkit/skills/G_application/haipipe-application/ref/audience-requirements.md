Audience Requirements — schema shared by all G_application kinds
=================================================================

Every application artifact (message / ui / report) has an **audience**.
The audience determines tone, length, technical depth, and which K/W
entries are appropriate to cite.

This file defines the shared schema. Kind-specialists read it in Phase 6
(self-review) to verify the draft matches its declared audience.


Audience taxonomy
==================

```
patient               end-user with diabetes / CGM
clinician             endocrinologist / nurse / care team
designer              product / UX designer
dev                   engineer implementing the feature
regulator             FDA / IRB / data-protection reviewer
executive             internal leadership / partner exec
partner               commercial partner / collaborator
researcher            academic peer (note: paper goes through F_paper, not here)
```

If a request's audience is "researcher", consider whether it should
actually be routed to F_paper instead.


Per-audience constraints
=========================

```
audience       tone               jargon            length            citations
─────────      ──────────         ──────────        ──────────        ──────────
patient        warm, plain        avoid             ≤ 200 words       inline (plain ref)
clinician      precise, clinical  expected          ≤ 400 words       inline (K-id)
designer       visual, concrete   minimal           ≤ 300 words +     in caption
                                                    + sketch
dev            precise, terse     expected          ≤ 500 words +     code-fence cites
                                                    + interface
regulator      formal, neutral    spelled out       ≤ 1500 words      footnote + K-id
executive      direct, outcome-   minimal           ≤ 600 words       endnote
               oriented
partner        professional       moderate          ≤ 800 words       inline
```


Citation rules
===============

Every claim that comes from project K/W MUST cite the entry id. Format
depends on audience but the id must appear somewhere traceable:

```
inline (K-id)        "(K03)"  or  "(see K03)"
footnote + K-id      "¹ K03_lhm_film_overfit"
endnote              "See knowledge entry K03."
inline (plain ref)   "Based on our research..."  (NO K-id visible to patient;
                                                   but artifact frontmatter
                                                   MUST list cited_K / cited_W)
```

**Always** record `cited_K` / `cited_W` in the artifact's frontmatter,
regardless of audience-facing format. The frontmatter is the
machine-traversable trail.


Frontmatter schema (artifacts)
===============================

Every application artifact begins with:

```yaml
---
kind:         message | ui | report
audience:     <one of taxonomy above>
intent:       "<one-line restatement of the request>"
created:      YYYY-MM-DD
cited_K:      [K01, K03]
cited_W:      [W02]
triggered:    [exp_ids if any]   # E_insight sessions / probes spawned during creation
status:       draft | reviewed | shipped | superseded
---
```

Status flow: `draft → reviewed → shipped` (or `superseded` if a later
artifact replaces it).


Self-review checklist (Phase 6)
================================

The kind-specialist runs through this before write:

```
[ ] Audience matches declared audience (tone / jargon / length within range)
[ ] Every factual claim has a cited_K or cited_W in frontmatter
[ ] No K/W cited as "confirmed" if its insight status is `contested` or `superseded`
[ ] No code, no Python, no plots embedded (kind=ui may have ASCII sketches only)
[ ] If gap was identified but unresolved (Phase 3 skipped or insight-session blocked),
    artifact carries a `status: draft` + a "## Open questions" section
```


When NOT to use G_application
==============================

```
"explain to me what we know about X"     → /haipipe-insight ask
"write a paper section on X"             → /paper-* (F_paper)
"draft a new W entry recommending X"     → /haipipe-insight wisdom
"log today's session findings"           → insight-session writes sessions/ log
```
