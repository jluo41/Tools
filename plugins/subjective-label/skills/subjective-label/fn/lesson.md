---
name: subjective-label-lesson
description: "Utility verb. Captures a hard-won lesson about subjective annotation methodology — LLM persona behavior, kappa statistics, embedding geometry, calibration gotchas, dataset quirks, or any 'wish I knew this before I started' insight. Unlike feedback (about the skill being wrong), a lesson is about the METHODOLOGY being surprising. `lesson list` shows all lessons; `lesson search <keyword>` finds relevant ones."
argument-hint: "[\"<what-happened-and-what-to-do>\"] | list | search <keyword>"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Lesson (capture hard-won knowledge, consult before acting)

Captures lessons learned the hard way about subjective annotation — things that
surprised us, cost us time, or would have saved hours if we'd known upfront.
These are about the METHODOLOGY being surprising, not about the skill docs being
wrong (that's feedback). A lesson is a "don't touch the stove" note for future
labeling projects.

The key contract: BEFORE starting /sl-init, /sl-iterate, or /sl-validate, the
agent MUST scan the lesson/ folder for relevant lessons and flag any that apply.
Lessons are guardrails, not just history.

## Three verbs

### Capture: `/subjective-label lesson "<what-happened>"`

```
1. READ existing lessons in lesson/ to check for duplicates.
2. SAME-TOPIC test: does this lesson cover the same gotcha as an existing one?
   a. SAME TOPIC -> UPDATE the existing file:
      - add a "## Update YYYY-MM-DD" section with the new detail
      - do NOT overwrite prior content
   b. NEW TOPIC -> CREATE lesson/<NN>-YYMMDD-<short-slug>.md
      where NN = max existing number + 1, zero-padded to 2 digits,
      and YYMMDD is today's date (e.g. 260626).
3. WRITE the lesson using the schema below.
4. CONFIRM: show the file path and one-line summary.
```

### List: `/subjective-label lesson list`

```
Print all lessons, one line each:
  <NN> · <YYMMDD> · <title> · <when-to-apply one-liner>
Sorted by number.
```

### Search: `/subjective-label lesson search <keyword>`

```
Grep lesson/*.md for the keyword(s). Print matching lessons with the
relevant excerpt. Use this BEFORE labeling work to check for gotchas.
```

## Lesson file schema

```markdown
# Lesson NN: <Short Title>

## The Problem
<What happened — the surprise, the error, the silent failure.>

## The Symptom
<How you noticed — wrong kappa, biased labels, persona drift, etc.>
<Optional — omit if the problem IS the symptom.>

## The Solution
<What to do instead. Config changes, prompt adjustments, process changes.>

## Why It Works (or Why It Fails)
<The underlying reason — so the reader understands, not just follows.>

## When to Apply
<Conditions that trigger this lesson — topic type, corpus size, label count, etc.>

## Caveats
<Edge cases, things this fix doesn't cover.>
<Optional — omit if none.>
```

## The contract: lessons are guardrails

```
BEFORE starting annotation methodology work, the agent MUST:
  1. Scan lesson/ for lessons relevant to the planned action.
  2. If any match, FLAG them to the user:
     "⚠️ Lesson 03 applies: MiniLM embeddings collapse humor + sarcasm.
      Consider using a larger model for this topic."
  3. If the user proceeds anyway, note it but do not block.

This is NOT optional. Lessons exist because we burned time on these
exact mistakes. The whole point is to not repeat them.
```

## Example lesson topics (not yet captured)

```
  LLM persona behavior:
    "Personas are order-sensitive — the first option gets favored"
    "GPT-4 personas are more agreeable than Claude personas"

  Kappa statistics:
    "Cohen's kappa is undefined when one rater uses only one category"
    "Kappa is misleadingly low for imbalanced label distributions"

  Embedding geometry:
    "MiniLM collapses semantically different but syntactically similar texts"
    "Cluster count > 20 fragments the corpus too much for init_map"

  Calibration:
    "Persona order in the prompt affects agreement rates"
    "Few-shot examples in the guideline prompt cause anchoring bias"

  Dataset quirks:
    "GoEmotions has 28 labels but annotators reliably distinguish ~12"
    "Short texts (<10 words) have much lower inter-annotator agreement"
```

## Distinction from other verbs

```
  lesson   "LLM personas order-bias the first label option"
           -> about the METHODOLOGY being surprising -> lesson/

  feedback "sl-iterate retrains the classifier every time, too slow"
           -> about the SKILL being clunky -> feedback/
```
