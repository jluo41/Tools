---
name: subjective-label-feedback
description: "Utility verb. Captures a complaint/confusion/wish about the subjective-label SKILL itself (clunky steps, wrong behavior, missing features), ROUTED at capture time to the right sub-skill. `feedback list` shows open items; `feedback move` re-routes a mis-filed item."
argument-hint: "[\"<text>\" | list | move <file> <skill>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Feedback (capture skill feedback, route at capture, fix later)

Captures feedback about the subjective-label SKILL (steps are clunky, output is
hard to read, a feature is missing, behavior is wrong) and FILES IT in the
`feedback/` folder. Does NOT fix anything; fixing is a separate revision pass.
Distinguish from lessons: feedback is about the TOOL, not about annotation
methodology.

## Capture: `/subjective-label feedback "<text>"`

```
1. INFER the target sub-skill from the text (see "Routing" below).
2. MERGE-OR-CREATE (inbox must NOT grow without bound):
   a. Read OPEN (and fixed) items already in feedback/.
   b. SAME-TOPIC test: same underlying concern, not just same category.
   c. SAME TOPIC -> UPDATE in place (append recurrence, bump count, reopen if fixed).
   d. NEW TOPIC -> CREATE feedback/<YYYY-MM-DD>_<short-slug>.md.
3. CONFIRM where it landed (MERGED or NEW).
```

### Routing (topic categories)

```
  init, seed, setup, scaffold       -> sl-init
  iterate, loop, batch, panel       -> sl-iterate
  validate, benchmark, kappa, ceil  -> sl-validate
  scale, cascade, tier, batch-label -> sl-scale
  status, dashboard, trajectory     -> sl-status
  sampler, sampling, pool           -> agent: sampler
  embedder, embed, cluster, FAISS   -> agent: embedder
  classifier, train, uncertainty    -> agent: classifier
  persona, panel, labeler           -> agent: labeler-panel
  moderator, escalate, surface      -> agent: moderator
  prober, probe, boundary           -> agent: prober
  analyzer, disagreement, category  -> agent: disagreement-analyzer
  gallery, guideline, keeper        -> agent: gallery-keeper
  validator, public dataset         -> agent: validator
  NO MATCH                          -> general (feedback/ root)
```

### One file per item (schema)

```
---
status: open | fixed
created: YYYY-MM-DD
updated: YYYY-MM-DD
occurrences: 1
context: <sub-skill or agent name, or "general">
fixed_in: ""
regressed: ""
---
<the feedback, in the reporter's words>

## Recurrences
- YYYY-MM-DD: <the new phrasing, verbatim>

Fix: <added when resolved>
```

## List: `/subjective-label feedback list`

```
Grep feedback/*.md for `status: open`, print newest-first.
```

## Move: `/subjective-label feedback move <file> <category>`

```
Re-tag the context field.
```
