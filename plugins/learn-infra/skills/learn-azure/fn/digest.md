---
name: learn-azure-digest
description: "Utility verb. Digests a session -- the CURRENT one, or a PAST session named/id'd as an argument -- scanning its transcript for feedback about the learn-azure wiki/diagrams (gaps, wrong info, outdated instructions, missing concepts), distilling discrete items, deduping, and after a MANDATORY confirm gate routing each through feedback capture. The bulk harvester for /learn-azure feedback. Never auto-files."
argument-hint: "[\"<session-name|id>\"] [--dry-run]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Digest (condense the session into routed feedback)

Most feedback is given conversationally and never filed. `digest` is the bulk
harvester: it reads a session's transcript, distills the discrete pieces of
feedback you gave about the LEARNING MATERIAL (wiki gaps, wrong instructions,
outdated concepts, confusing diagrams), dedups them, and (after you confirm)
routes each into the feedback/ inbox.

Typical usage: from a FRESH session (clean context), name the PAST session to
harvest -- `/learn-azure digest "Azure-Setup-Session"`. With no argument it
digests the CURRENT session instead.

## Run: `/learn-azure digest ["<session-name|id>"] [--dry-run]`

```
0. RESOLVE which session to digest:
     - NO arg   -> the CURRENT session.
     - "<id>"   -> that transcript .jsonl.
     - "<name>" -> the session /rename'd to that name.
1. SCAN the target session for LEARNING-MATERIAL feedback signals:
     KEEP  - "this wiki page is wrong/outdated/missing X"
           - "the diagram doesn't show Y"
           - "the invite instructions didn't work because Z"
           - "we should add a page about W"
           - corrections you made to the material
     DROP  - one-off Azure/Databricks operational commands
           - project-specific discussion (about REACH, not the wiki)
           - my own narration
2. DISTILL into discrete candidate items, ONE concern each.
3. DEDUP each candidate against existing feedback/ items.
   Tag each:  [NEW]  |  [MERGE -> <file>]  |  [DUP-IN-BATCH]
4. PRESENT the candidate list for the MANDATORY confirm gate.
   You: approve / edit / drop each item. NOTHING is written before confirm.
5. ROUTE each APPROVED item through feedback capture (fn/feedback.md
   merge-or-create).
6. REPORT as an ITEMIZED LIST of every item produced:
     <NEW|MERGED|DROPPED> · <file.md> · "<one-line title>"
   Then close with the tally and "review: /learn-azure feedback list".
```

## Scope: learning-material feedback only

```
digest files ONLY feedback about wiki/diagram content into the inbox.
Global behavioral preferences (how the agent should act) go to PREFERENCES.md.
  wiki defect    "the invite page is missing the Graph API workaround"  -> inbox
  global pref    "always show me a diagram instead of prose"            -> PREFERENCES.md
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
```
