---
name: learn-databricks-digest
description: "Utility verb. Digests a session -- the CURRENT one, or a PAST session named/id'd as an argument -- scanning its transcript for BOTH platform lessons (gotchas, surprises, workarounds worth knowing BEFORE next time) AND feedback about the learn-databricks skill itself (lesson gaps, wrong info, outdated instructions). Distills, dedups, confirms, then routes each item to lesson/ or feedback/ accordingly. The bulk harvester for both knowledge types. Never auto-files."
argument-hint: "[\"<session-name|id>\"] [--dry-run]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Digest (condense the session into routed lessons + feedback)

Most hard-won knowledge is discovered conversationally and never filed. `digest`
is the bulk harvester: it reads a session's transcript, distills TWO kinds of
discrete items — platform LESSONS (gotchas, surprises, workarounds) and skill
FEEDBACK (lesson/journey doc gaps, wrong instructions) — dedups them, and (after
you confirm) routes each to the right destination: lesson/ or feedback/.

Typical usage: from a FRESH session (clean context), name the PAST session to
harvest -- `/learn-databricks digest "Databricks-Deploy-Session"`. With no
argument it digests the CURRENT session instead.

## Run: `/learn-databricks digest ["<session-name|id>"] [--dry-run]`

```
0. RESOLVE which session to digest:
     - NO arg   -> the CURRENT session.
     - "<id>"   -> that transcript .jsonl.
     - "<name>" -> the session /rename'd to that name.
1. SCAN the target session for TWO signal types:
     LESSON signals (platform surprises — route to lesson/):
       - "it turns out Databricks does X, which broke Y"
       - "the workaround is to Z instead of W"
       - gotchas, silent failures, surprising platform behavior
       - workarounds discovered through trial and error
       - anything that would save time if known BEFORE starting
     FEEDBACK signals (skill/doc defects — route to feedback/):
       - "this lesson is wrong/outdated/missing X"
       - "the journey doc doesn't cover Y"
       - "the instructions didn't work because Z"
       - corrections you made to the learning material
     DROP  - one-off Databricks operational commands
           - project-specific discussion (about REACH pipeline, not the lessons)
           - my own narration
2. DISTILL into discrete candidate items, ONE concern each.
   TAG each as [LESSON] or [FEEDBACK] based on the signal type:
     [LESSON]   about the PLATFORM being surprising   -> lesson/
     [FEEDBACK] about the SKILL/DOC being wrong       -> feedback/
3. DEDUP each candidate against existing items in its target folder:
     [LESSON]   dedup against lesson/*.md (same-topic -> update existing lesson)
     [FEEDBACK] dedup against feedback/*.md (same-topic -> merge)
   Tag each:  [NEW]  |  [MERGE -> <file>]  |  [DUP-IN-BATCH]
4. PRESENT the candidate list for the MANDATORY confirm gate.
   Group by type (LESSON / FEEDBACK), one line per item:
     <type> · <tag> · "<one-line summary>"
   You: approve / edit / re-classify / drop each item.
   NOTHING is written before confirm.
5. ROUTE each APPROVED item:
     [LESSON]   -> fn/lesson.md capture (same-topic updates existing lesson,
                   new topic creates lesson/<NN>-YYMMDD-<slug>.md)
     [FEEDBACK] -> fn/feedback.md capture (merge-or-create in feedback/)
6. REPORT as an ITEMIZED LIST of every item produced:
     <NEW|MERGED|DROPPED> · <LESSON|FEEDBACK> · <file.md> · "<one-line title>"
   Then close with the tally "L lessons (l new, l' merged), F feedback (f new,
   f' merged), D dropped" and "review: /learn-databricks lesson list" +
   "/learn-databricks feedback list".
```

## Scope: platform knowledge + skill feedback (not global prefs)

```
digest routes to TWO destinations:
  platform gotcha  "dbutils.notebook.run() doesn't inherit env vars"   -> lesson/
  lesson defect    "lesson 04 doesn't mention the --no-cache workaround" -> feedback/
  global pref      "always show me a diagram instead of prose"           -> PREFERENCES.md
```

## `--dry-run`

```
Scan + distill + dedup + present, then STOP -- do not file.
```

## Safeguards

```
- confirm-gated:  never auto-files.
- merge-or-create: same-topic items update existing files.
- evidence-bound:  only files feedback you can point to in the transcript.
- drop transient:  one-off commands and project talk are excluded.
- type-gated:      each item is classified LESSON vs FEEDBACK before routing;
                   the confirm gate lets you re-classify before filing.
```
