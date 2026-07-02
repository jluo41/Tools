---
name: image-ppt-feedback
description: "Utility verb. Captures a complaint/confusion/wish about the image-ppt SKILLS or SCRIPTS themselves (a step is clunky, compose mis-places text, crop_qc over-flags, a flag is missing), ROUTED at capture time to the right sub-skill/script. `feedback list` shows open items; `feedback move` re-routes a mis-filed item."
argument-hint: "[\"<text>\" | list | move <file> <target>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Feedback (capture skill/script defects, route at capture, fix later)

Captures feedback about the image-ppt SKILLS or their scripts (a step is clunky, output is
wrong, a feature is missing) and FILES IT in the `feedback/` folder. Does NOT fix anything;
fixing is a separate revision pass. Distinguish from lessons: feedback is about the TOOL, not
about the vectorization craft.

## Capture: `/image-ppt feedback "<text>"`

```
1. INFER the target sub-skill/script from the text (see "Routing" below).
2. MERGE-OR-CREATE (inbox must NOT grow without bound):
   a. Read OPEN (and fixed) items already in feedback/.
   b. SAME-TOPIC test: same underlying concern, not just same category.
   c. SAME TOPIC -> UPDATE in place (append recurrence, bump count, reopen if fixed).
   d. NEW TOPIC  -> CREATE feedback/<YYYY-MM-DD>_<short-slug>.md.
3. CONFIRM where it landed (MERGED or NEW).
```

### Routing (topic categories)

```
  analyze, grid, bbox, items.json, crop, crop_qc, compose, connectors,
    panels, text placement, render_diff, evaluate_icons   -> figure-to-svg-replica
  decompose, primitives, score_icon, center_svg,
    render_compare, per-icon draw                          -> image-to-svg
  compose, master-svg, export                              -> figure-to-svg-replica (compose)
  router, menu, lesson/feedback/digest plumbing            -> image-ppt
  NO MATCH                                                  -> general (feedback/ root)
```

### One file per item (schema)

```
---
status: open | fixed
created: YYYY-MM-DD
updated: YYYY-MM-DD
occurrences: 1
context: <sub-skill or script name, or "general">
fixed_in: ""
regressed: ""
---
<the feedback, in the reporter's words>

## Recurrences
- YYYY-MM-DD: <the new phrasing, verbatim>

Fix: <added when resolved>
```

## List: `/image-ppt feedback list`

```
Grep feedback/*.md for `status: open`, print newest-first.
```

## Move: `/image-ppt feedback move <file> <target>`

```
Re-tag the context field.
```
