---
name: image-ppt
description: "Router + knowledge layer for the image-ppt plugin (figure/icon vectorization to editable SVG). Routes to the two work skills (image-to-svg, figure-to-svg-replica) and exposes the knowledge verbs: `lesson` (hard-won vectorization gotchas, consulted BEFORE drawing), `feedback` (defects in the skills/scripts), `digest` (harvest a session into lessons + feedback). Use when the user says /image-ppt, or wants to capture/list a lesson or feedback, or digest a session."
---

Skill: image-ppt (router + knowledge layer)
===========================================

Entry point for the **image-ppt** plugin — replicate raster figures and icons as clean,
editable, hand-authored SVGs. This skill routes to
the two work skills and owns the shared **knowledge layer** (lessons + feedback).

Invocation:  /image-ppt <command> [args]


Sub-commands
------------

  Do the work:
  vectorize-icon    One raster icon crop  -> faithful hand-authored SVG   -> /image-to-svg
  vectorize-figure  A whole infographic   -> master editable SVG          -> /figure-to-svg-replica

  Knowledge layer:
  lesson    Capture / list / search vectorization gotchas (consulted BEFORE drawing)
  feedback  Capture / list defects in the skills or scripts
  digest    Bulk-harvest lessons + feedback from a session transcript

  (no sub-command) Show this menu and ask what the user wants.


Routing
-------

Parse $ARGUMENTS for the sub-command token, then invoke the match:

  vectorize-icon    ->  /image-to-svg
  vectorize-figure  ->  /figure-to-svg-replica
  lesson            ->  fn/lesson.md    (capture / list / search)
  feedback          ->  fn/feedback.md  (capture / list / move)
  digest            ->  fn/digest.md    (harvest -> lesson/ + feedback/)


The contract: lessons are guardrails
-------------------------------------

BEFORE any vectorization work (starting `figure-to-svg-replica`, or hand-authoring an icon
in `image-to-svg`), the agent MUST scan `lesson/` for relevant lessons and FLAG any that
apply — e.g. "⚠️ Lesson 01: interlocking/organic glyphs resist primitive drawing; offer a
stock/raster route now, not after 3 rejections." Lessons exist because we already burned
time on these exact mistakes. This is not optional; the whole point is to not repeat them.
Both work skills point here in their opening "Before you start" note.


Layout
------

  fn/lesson.md      verb: capture/list/search vectorization lessons
  fn/feedback.md    verb: capture/list/move skill defects
  fn/digest.md      verb: harvest a session -> lessons + feedback
  lesson/           the lessons (guardrails), one file each, NN-YYMMDD-slug.md
  feedback/         the defect inbox, one file each, YYYY-MM-DD_slug.md
