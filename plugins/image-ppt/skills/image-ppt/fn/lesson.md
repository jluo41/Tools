---
name: image-ppt-lesson
description: "Utility verb. Captures a hard-won lesson about figure/icon VECTORIZATION — which shapes resist primitive hand-authoring, when to keep raster, crop/QC and scorer gotchas, PPTX embedding tricks, fidelity details that matter. Unlike feedback (a skill/script is broken), a lesson is about the CRAFT being surprising. `lesson list` shows all; `lesson search <kw>` finds relevant ones. Consult BEFORE drawing."
argument-hint: "[\"<what-happened-and-what-to-do>\"] | list | search <keyword>"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Lesson (capture hard-won vectorization knowledge, consult before drawing)

Captures lessons learned the hard way about turning raster figures/icons into clean editable
SVGs — things that surprised us, cost iterations, or would have saved a redraw if known
upfront. These are about the CRAFT being surprising (a glyph won't reduce to primitives, a
scorer lies on inverted polarity, a delivery format needs a trick), NOT about a script being
buggy (that's feedback).

The key contract: BEFORE starting `figure-to-svg-replica`, or hand-authoring an icon in
`image-to-svg`, the agent MUST scan the `lesson/` folder for relevant lessons and flag any
that apply. Lessons are guardrails, not just history.

## Three verbs

### Capture: `/image-ppt lesson "<what-happened>"`

```
1. READ existing lessons in lesson/ to check for duplicates.
2. SAME-TOPIC test: does this cover the same gotcha as an existing lesson?
   a. SAME TOPIC -> UPDATE the file: add a "## Update YYYY-MM-DD" section; do NOT overwrite.
   b. NEW TOPIC  -> CREATE lesson/<NN>-<YYMMDD>-<short-slug>.md
      where NN = max existing number + 1, zero-padded to 2 digits, YYMMDD = today.
3. WRITE the lesson using the schema below.
4. CONFIRM: show the file path and one-line summary.
```

### List: `/image-ppt lesson list`

```
Print all lessons, one line each:
  <NN> · <YYMMDD> · <title> · <when-to-apply one-liner>
Sorted by number.
```

### Search: `/image-ppt lesson search <keyword>`

```
Grep lesson/*.md for the keyword(s); print matching lessons with the relevant excerpt.
Use this BEFORE vectorizing to check for gotchas (e.g. "handshake", "logo", "white on dark").
```

## Lesson file schema

```markdown
# Lesson NN: <Short Title>

## The Problem
<What happened — the surprise, the wasted redraw, the confident-but-wrong output.>

## The Symptom
<How you noticed — user rejected it twice, score PASSed but it looked wrong, crop_qc over-flagged.>
<Optional — omit if the problem IS the symptom.>

## The Solution
<What to do instead. Method switch, raster fallback, geometry recipe, QC/scoring adjustment.>

## Why It Works (or Why It Fails)
<The underlying reason — so the reader understands, not just follows.>

## When to Apply
<Triggers — glyph type (organic/interlocking/logo/photo), polarity (white-on-dark), crop size,
delivery format (PPT), etc.>

## Caveats
<Edge cases this fix doesn't cover.>  <Optional — omit if none.>
```

## Distinction from other verbs

```
  lesson   "interlocking hands don't reduce to primitives — use a stock glyph or raster"
           -> about the CRAFT being surprising  -> lesson/
  feedback "crop_qc over-flags white-on-navy icons as LOOSE/OFF-CTR"
           -> about a SCRIPT being wrong        -> feedback/
```
