---
name: figure-to-svg-lesson
description: "Utility verb. Captures a hard-won lesson about figure/icon VECTORIZATION — which shapes resist primitive hand-authoring, when to keep raster, scorer gotchas, fidelity details that matter. Unlike feedback (a skill/script is broken), a lesson is about the CRAFT being surprising. Load-bearing lessons get MERGED into the work skills' steps; the folder is inbox + archive. `lesson list` shows all; `lesson search <kw>` finds relevant ones."
argument-hint: "[\"<what-happened-and-what-to-do>\"] | list | search <keyword>"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Lesson (capture hard-won vectorization knowledge, consult before drawing)

Captures lessons learned the hard way about turning raster figures/icons into clean editable
SVGs — things that surprised us, cost iterations, or would have saved a redraw if known
upfront. These are about the CRAFT being surprising (a glyph won't reduce to primitives, a
scorer lies on inverted polarity, a delivery format needs a trick), NOT about a script being
buggy (that's feedback).

The key contract: lessons don't stay in this folder — a load-bearing lesson gets its rule
**merged into the relevant SKILL.md at the step where it applies**, so the work skills carry
the current guardrails inline and need no runtime folder scan. The lesson file remains as the
full story and provenance. Capturing without merging protects nobody.

## Three verbs

### Capture: `/figure-to-svg lesson "<what-happened>"`

```
1. READ existing lessons in lesson/ to check for duplicates.
2. SAME-TOPIC test: does this cover the same gotcha as an existing lesson?
   a. SAME TOPIC -> UPDATE the file: add a "## Update YYYY-MM-DD" section; do NOT overwrite.
   b. NEW TOPIC  -> CREATE lesson/<NN>-<YYMMDD>-<short-slug>.md
      where NN = max existing number + 1, zero-padded to 2 digits, YYMMDD = today.
3. WRITE the lesson using the schema below.
4. MERGE: if the lesson is load-bearing (would change how a step is done), also add its
   one-line rule into the relevant SKILL.md at the step it guards — that's the real
   deliverable; the file is provenance.
5. CONFIRM: show the file path, one-line summary, and where (or whether) it was merged.
```

### List: `/figure-to-svg lesson list`

```
Print all lessons, one line each:
  <NN> · <YYMMDD> · <title> · <when-to-apply one-liner>
Sorted by number.
```

### Search: `/figure-to-svg lesson search <keyword>`

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
crop resolution, etc.>

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
