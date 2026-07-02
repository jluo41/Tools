---
name: image-ppt-digest
description: "Utility verb. Digests a session -- the CURRENT one, or a PAST session named/id'd as an argument -- scanning its transcript for BOTH vectorization LESSONS (glyphs that resist primitives, raster fallbacks, scorer/QC gotchas, crop/resolution gotchas) AND skill/script FEEDBACK (clunky steps, wrong behavior, missing flags). Distills, dedups, confirms, then routes each item to lesson/ or feedback/. The bulk harvester. Never auto-files."
argument-hint: "[\"<session-name|id>\"] [--dry-run]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Digest (condense a session into routed lessons + feedback)

Most hard-won knowledge is discovered conversationally and never filed. `digest` is the bulk
harvester: it reads a session's transcript, distills TWO kinds of discrete items — craft
LESSONS (a glyph wouldn't reduce to primitives, a scorer lied on inverted polarity, a delivery
format needed a trick) and skill/script FEEDBACK (a step is clunky, behavior is wrong, a flag
is missing) — dedups them, and (after you confirm) routes each to lesson/ or feedback/.

Typical usage: from a FRESH session (clean context), name the PAST session to harvest --
`/image-ppt digest "Figure3-Vectorize"`. With no argument it digests the CURRENT session.

## Run: `/image-ppt digest ["<session-name|id>"] [--dry-run]`

```
0. RESOLVE which session to digest:
     - NO arg   -> the CURRENT session.
     - "<id>"   -> that transcript .jsonl.
     - "<name>" -> the session /rename'd to that name.
1. SCAN the target session for TWO signal types:
     LESSON signals (craft surprises — route to lesson/):
       - "the handshake never worked as hand-drawn primitives"
       - "score_icon PASSed but it looked wrong" / "polarity broke the score"
       - "crop_qc over-flagged the white-on-navy icons"
       - "keep the logos/photos as raster"
       - "a low-res crop still vectorizes fine — resolution-independent output"
       - anything that would save a redraw if known BEFORE starting
     FEEDBACK signals (skill/script defects — route to feedback/):
       - "compose mis-placed the multi-line labels"
       - "crop_qc should auto-detect inverted polarity"
       - "grid_overlay needs a tighter --crop default"
       - complaints about the TOOL, not the craft
     DROP  - one-off drawing decisions for THIS figure
           - project-specific discussion (about this deck, not the method)
           - my own narration
2. DISTILL into discrete candidates, ONE concern each. TAG [LESSON] or [FEEDBACK].
3. DEDUP each candidate against existing items in its target folder:
     [LESSON]   dedup against lesson/*.md  (same-topic -> update existing lesson)
     [FEEDBACK] dedup against feedback/*.md (same-topic -> merge)
   Tag each:  [NEW]  |  [MERGE -> <file>]  |  [DUP-IN-BATCH]
4. PRESENT the candidate list for the MANDATORY confirm gate, grouped by type:
     <type> · <tag> · "<one-line summary>"
   You: approve / edit / re-classify / drop each item. NOTHING is written before confirm.
5. ROUTE each APPROVED item:
     [LESSON]   -> fn/lesson.md capture   (update existing, or new lesson/<NN>-<YYMMDD>-<slug>.md)
     [FEEDBACK] -> fn/feedback.md capture (merge-or-create in feedback/)
6. REPORT an ITEMIZED LIST of every item produced:
     <NEW|MERGED|DROPPED> · <LESSON|FEEDBACK> · <file.md> · "<one-line title>"
   Close with the tally and "review: /image-ppt lesson list" + "/image-ppt feedback list".
```

## Scope: craft knowledge + skill feedback (not global prefs)

```
  craft gotcha  "interlocking hands don't reduce to primitives"     -> lesson/
  skill defect  "crop_qc over-flags inverted-polarity icons"        -> feedback/
  global pref   "always give me the diff side-by-side"              -> not here (user memory)
```

## `--dry-run`

```
Scan + distill + dedup + present, then STOP -- do not file.
```

## Safeguards

```
- confirm-gated:  never auto-files.
- merge-or-create: same-topic items update existing files.
- evidence-bound:  only files items you can point to in the transcript.
- drop transient:  one-off drawing choices and project talk are excluded.
- type-gated:      each item is classified LESSON vs FEEDBACK before routing;
                   the confirm gate lets you re-classify before filing.
```
