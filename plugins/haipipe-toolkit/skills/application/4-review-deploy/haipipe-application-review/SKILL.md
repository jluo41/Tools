---
name: haipipe-application-review
description: "Artifact review for the intervention lifecycle. Checks each drafted artifact against audience requirements, claim traceability, tone/length compliance, and self-review checklist. Parallel to paper's reviewer skills. Trigger: review, review artifacts, check compliance, /haipipe-application review."
argument-hint: "[variant-id] [intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-06-22"
  summary: "Artifact review — audience fit, claim traceability, compliance."
  changelog:
    - "1.0.0 (2026-06-22): initial version."
---

Skill: haipipe-application-review
====================================

Reviews drafted artifacts against the intervention's design spec,
audience requirements, and claim traceability.


Review checklist
=================

Per artifact in `0-artifacts/`:

```
[ ] Audience match: tone, jargon level, length within budget
    (per _audience/profile-<audience>/ and ref/audience-requirements.md)

[ ] Claim traceability: every factual claim in the artifact traces
    to a cited_K or cited_W in frontmatter

[ ] No contested/superseded K/W cited as confirmed

[ ] Citation format matches audience rules
    (patient: no K-id in body; clinician: inline K-id; etc.)

[ ] Content principles from 3-design.md followed

[ ] No PHI, no PII, no code, no raw data values

[ ] Call-to-action present and clear (if applicable)

[ ] Reading level appropriate for audience

[ ] Status field in frontmatter set correctly
```


Output
=======

For each reviewed artifact:

```
0-artifacts/REVIEW-<variant-slug>.md
```

```markdown
# Review: <variant-slug>

- **Verdict:** pass | revise | fail
- **Reviewed:** YYYY-MM-DD

## Checklist
- [x] Audience match
- [ ] Claim traceability — C02 not cited but claim present in body
- [x] Citation format
...

## Issues
1. <issue description + suggested fix>

## Recommendation
<pass / revise with specific feedback / fail with reason>
```


Workflow
=========

```
Step 1: Read 0-artifacts/ for drafted artifacts.
Step 2: Read audience profile, 3-design.md, 2-claims.md.
Step 3: Run checklist per artifact.
Step 4: Write REVIEW-*.md per artifact.
Step 5: Update variant status: drafted → reviewed (if pass).
Step 6: Report summary.
```


Risk profile
=============

WRITES review files to `0-artifacts/`. Updates variant status in
`0-lifecycle/4-variants.md`. READ-ONLY on everything else.
