---
name: subjective-label-digest
description: "Utility verb. Digests a session -- the CURRENT one, or a PAST session named/id'd as an argument -- scanning its transcript for BOTH methodology lessons (annotation gotchas, LLM behavior surprises, kappa pitfalls) AND feedback about the subjective-label skill itself (clunky steps, missing features). Distills, dedups, confirms, then routes each item to lesson/ or feedback/ accordingly. The bulk harvester for both knowledge types. Never auto-files."
argument-hint: "[\"<session-name|id>\"] [--dry-run]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Digest (condense the session into routed lessons + feedback)

Most hard-won knowledge is discovered conversationally and never filed. `digest`
is the bulk harvester: it reads a session's transcript, distills TWO kinds of
discrete items — methodology LESSONS (annotation gotchas, persona behavior,
kappa pitfalls) and skill FEEDBACK (clunky steps, wrong behavior, missing
features) — dedups them, and (after you confirm) routes each to the right
destination: lesson/ or feedback/.

Typical usage: from a FRESH session (clean context), name the PAST session to
harvest -- `/subjective-label digest "Empathy-Labeling-Init"`. With no argument
it digests the CURRENT session instead.

## Run: `/subjective-label digest ["<session-name|id>"] [--dry-run]`

```
0. RESOLVE which session to digest:
     - NO arg   -> the CURRENT session.
     - "<id>"   -> that transcript .jsonl.
     - "<name>" -> the session /rename'd to that name.
1. SCAN the target session for TWO signal types:
     LESSON signals (methodology surprises — route to lesson/):
       - "it turns out personas are order-sensitive"
       - "kappa was misleadingly low because of label imbalance"
       - "the embedder collapsed humor and sarcasm into one cluster"
       - gotchas about LLM behavior, statistics, embeddings, datasets
       - anything that would save time if known BEFORE starting
     FEEDBACK signals (skill defects — route to feedback/):
       - "sl-iterate is too slow because it retrains every time"
       - "the init dialogue didn't ask about my purpose"
       - "the trajectory plot is hard to read"
       - complaints about the TOOL, not the methodology
     DROP  - one-off labeling decisions
           - project-specific discussion (about THIS corpus, not the method)
           - my own narration
2. DISTILL into discrete candidate items, ONE concern each.
   TAG each as [LESSON] or [FEEDBACK] based on the signal type:
     [LESSON]   about the METHODOLOGY being surprising   -> lesson/
     [FEEDBACK] about the SKILL being wrong/clunky        -> feedback/
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
   f' merged), D dropped" and "review: /subjective-label lesson list" +
   "/subjective-label feedback list".
```

## Scope: methodology knowledge + skill feedback (not global prefs)

```
digest routes to TWO destinations:
  methodology gotcha  "personas order-bias the first option"          -> lesson/
  skill defect        "sl-init doesn't ask about purpose"             -> feedback/
  global pref         "always show me a diagram instead of prose"     -> PREFERENCES.md
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
