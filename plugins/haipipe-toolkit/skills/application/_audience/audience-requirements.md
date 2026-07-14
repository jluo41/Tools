Audience Requirements — schema shared by all application kinds
=================================================================

Every application artifact (message / ui / report) has an **audience**.
The audience determines tone, length, technical depth, and which ledger
claims are appropriate to cite.

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
researcher            academic peer (note: paper goes through paper, not here)
```

If a request's audience is "researcher", consider whether it should
actually be routed to paper instead.


Per-audience constraints
=========================

```
audience       tone               jargon            length            citations
─────────      ──────────         ──────────        ──────────        ──────────
patient        warm, plain        avoid             ≤ 200 words       inline (plain ref)
clinician      precise, clinical  expected          ≤ 400 words       inline (C-id)
designer       visual, concrete   minimal           ≤ 300 words +     in caption
                                                    + sketch
dev            precise, terse     expected          ≤ 500 words +     code-fence cites
                                                    + interface
regulator      formal, neutral    spelled out       ≤ 1500 words      footnote + C-id
executive      direct, outcome-   minimal           ≤ 600 words       endnote
               oriented
partner        professional       moderate          ≤ 800 words       inline
```


Citation rules
===============

Every assertion MUST cite a supported ledger claim (C##) from 1-claims.md,
and the probe SECTION whose evidence settled it (`PP<NN> § Q<n>`, whose
`target:` names the answering QA file). Format depends on audience but the
id must appear somewhere traceable:

```
inline (C-id)        "(C03)"  or  "(see C03)"
footnote + C-id      "¹ C03 — settled by PP05"
endnote              "See ledger claim C03 (PP05)."
inline (plain ref)   "Based on our research..."  (NO C-id visible to patient;
                                                   but artifact frontmatter
                                                   MUST list cites:)
```

**Always** record `cites` in the artifact's frontmatter, regardless of
audience-facing format. The frontmatter is the machine-traversable
trail.


Frontmatter schema (artifacts)
===============================

Every application artifact begins with:

```yaml
---
kind:         message | ui | report
audience:     <one of taxonomy above>
intent:       "<one-line restatement of the request>"
created:      YYYY-MM-DD
cites:        [C01 (PP03), C04 (PP07)]
triggered:    [probe_refs if any]   # probes spawned during creation
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
[ ] Every factual claim has a cites: entry in frontmatter (C## + PP##)
[ ] Nothing cited as "confirmed" if its backing evidence is contested or superseded
[ ] No code, no Python, no plots embedded (kind=ui may have ASCII sketches only)
[ ] If gap was identified but unresolved (Phase 3 skipped or the probe blocked),
    artifact carries a `status: draft` + a "## Open questions" section
```


When NOT to use application
==============================

```
"explain to me what we know about X"     → /haipipe-task qa "<question>"      (internal evidence)
                                           /haipipe-discovery qa "<question>" (external evidence)
                                           — the executor's own question door; it
                                             returns a <task-folder>/QA/<n>-<slug>.md path
"write a paper section on X"             → /haipipe-paper (paper)
"settle whether X holds"                 → /haipipe-application probe "<question>"
                                           — raises a question SECTION; the PROBE phase
                                             binds it to a QA file, and the CLAIM's status
                                             lands in 1-claims.md (there is no probe verdict)
```
