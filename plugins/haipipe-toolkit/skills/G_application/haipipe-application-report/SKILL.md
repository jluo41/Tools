---
name: haipipe-application-report
description: "Report specialist of the haipipe-application family. STUB. Will be an outer-loop session producing external stakeholder reports (regulator / executive / partner) from the project's K/W knowledge base. Reads K_knowledge + W_wisdom from E_insight, can trigger /haipipe-insight ask, writes to examples/<project>/applications/reports/. NEVER writes back to insights/. NOTE: for the internal Q&A synthesis previously called 'insight-report', use insight-session's sessions/<DATE>.md log instead — that scope moved entirely to G_application. Trigger: report, stakeholder report, briefing, exec summary, regulator doc, /haipipe-application report."
argument-hint: [--audience regulator|executive|partner] [--project <path>] [--slug <slug>] "<intent>"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-application-report   (STUB)
============================================

**Status: STUB.** Mirrors `haipipe-application-message` structure but
not yet filled out for the report case.

Defer to the sibling files:
  - `../haipipe-application/SKILL.md`
  - `../haipipe-application/ref/audience-requirements.md`
  - `../haipipe-application/ref/application-input-contract.md`
  - `../haipipe-application-message/SKILL.md`     (reference impl)


Disambiguation: this is NOT the old `haipipe-insight-report`
-------------------------------------------------------------

The old `haipipe-insight-report` (now deleted) was the internal
question-answering synthesis doc. That role is covered by
`insight-session`'s `insights/sessions/<DATE>_<slug>.md` log + the
K/W entries the session writes.

`haipipe-application-report` is **external stakeholder facing**:
- audience ∈ {regulator, executive, partner}
- has audience-specific tone / length / citation format
- cites K/W from insights/ but is itself an external artifact


Expansion notes
----------------

```
Audiences:        regulator   (formal; full footnoted citations; ≤ 1500 words)
                  executive   (direct, outcome-oriented; ≤ 600 words)
                  partner     (professional; inline cites; ≤ 800 words)

Output:           applications/reports/<YYYY-MM-DD>_<audience>_<slug>.md

Schema additions: include `scope: [<topics>]` and `period: <date range>`
                  in frontmatter
```


Risk profile
-------------

WRITES new file under `applications/reports/`. May trigger
`/haipipe-application ask`. NEVER writes to insights/.


Specialist tail
----------------

```
status:    stub_invoked | (post-expansion: ok | blocked | failed | gap_unresolved)
summary:   "Report specialist is a stub; expand following message specialist pattern"
next:      Implement following haipipe-application-message/SKILL.md
```
