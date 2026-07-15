---
name: haipipe-application-review
description: "Artifact review for the intervention lifecycle. Checks each drafted artifact against audience requirements, claim traceability, tone/length compliance, and self-review checklist. Parallel to paper's reviewer skills. Trigger: review, review artifacts, check compliance, /haipipe-application review."
argument-hint: "[artifact-id] [intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.1.0"
  last_updated: "2026-07-06"
  summary: "Artifact review — audience fit, claim traceability, compliance. Paper-alignment sweep: old-spine paths (3-design/4-variants/2-claims.md) replaced; retired verdict word removed."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
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
    to an adopted A id in frontmatter (artifact -> adopted A -> C -> anchor)

[ ] No refuted C or [STALE]-tagged A cited as settled evidence

[ ] Citation format matches audience rules
    (patient: no C-id in body; clinician: inline C-id; etc.)

[ ] Element specs from 0-lifecycle/4-display/4-display.md (when present)
    and the venue style-profile followed

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
- [ ] Claim traceability — C2 not cited but claim present in body
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
Step 2: Read the audience profile, 0-lifecycle/1d-advice/1d-advice.md,
        0-lifecycle/1c-claims/1c-claims.md, and
        0-lifecycle/4-display/4-display.md (if the venue required it).
Step 3: Run checklist per artifact.
Step 4: Write REVIEW-*.md per artifact.
Step 5: Update artifact status frontmatter: draft → reviewed (if pass).
Step 6: Report summary.
```


Risk profile
=============

WRITES review files to `0-artifacts/` and the reviewed artifact's status
frontmatter. READ-ONLY on everything else.
