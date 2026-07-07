---
name: haipipe-paper-revise-content
description: "Review and edit the prose CONTENT of an existing draft at section -> paragraph -> sentence. REVISE phase (fully automatic). Applies changes directly, leaves %% {CC-content}: comments explaining WHY each change was made for CHECK review. Self-contained: carries its own structure/claim/flow checks. Reads REF/prose-quality.md for universal rules. Trigger: edit content, review content, tighten section, restructure paragraphs, /haipipe-paper-revise-content."
argument-hint: "[section-name-or-number] [paper-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "1.1.1"
  last_updated: "2026-07-07"
  summary: "REVISE worker: edit prose CONTENT at section->¶->sentence, change directly + leave why-comments. Self-contained structure/claim/flow checks. Fully automatic."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# haipipe-paper-revise-content

REVISE phase worker: editing the **prose content** of a draft that already exists. This skill changes *what the prose says and how it is built*. Fully automatic -- applies changes directly, no human gate.

It does **not** verify numbers or citations against their sources (that is `haipipe-paper-probe-values` and `haipipe-paper-probe-citation`) -- but it **does flag** a missing number or citation so those PROBE-phase passes have a target.

## Before you start

Read the shared prose rules:

- `../../REF/prose-quality.md` -- universal writing rules (one idea per sentence, no em-dash, compress not split, no AI voice, <=6 sentences/paragraph, Pn.Sn markers)

Then confirm where you are: this is the REVISE phase, content worker. Pick **one section**.

## Automatic apply with explanatory comments

REVISE is fully automatic. The agent:

1. Reads the section (outline .md and/or .tex)
2. Applies fixes directly (no waiting for human approval)
3. Leaves a `%% {CC-content}: <why>` comment next to each non-trivial change explaining WHY the change was made

The comments are for CHECK to review. The human sees what changed and why, and can add `> USER:` comments to restart REVISE if needed.

Trivial changes (whitespace, marker fixes) do not need comments. Only explain changes where the WHY is not obvious from the diff.

## The pass, top-down

Work **section -> paragraph -> sentence**. Get the section's job right, then each paragraph's point, then the sentences. Fixing sentences inside a paragraph that should not exist is wasted work.

1. **Section** -- state the section's one job in a sentence; make the paragraph banner skeleton (`grep '^% Para '`) tell the section's story; fix boundaries and order.
2. **Paragraph** -- one paragraph = one point (its banner's point); topic sentence first; merge/split so each banner is true.
3. **Sentence** -- one assertion each; cut filler; concrete over vague; one term per concept.

## Flag, don't fabricate

When the content needs a number or citation that is not here yet, drop a marker instead of inventing one:

```latex
The model achieved % TODO[values] accuracy on the held-out set.
This aligns with prior work % TODO[cite] on trait extraction.
```

These are grep targets for the PROBE phase (values and citation workers). Leaving a flag is correct; guessing a value or a citation is not.

## Done means

- [ ] Every paragraph has one clear job matching its banner
- [ ] One idea per sentence, no filler, concrete over vague
- [ ] Every missing number/citation is flagged (`% TODO[...]`); none invented
- [ ] Non-trivial changes have `%% {CC-content}: <why>` comments for CHECK
- [ ] Banners present with ids preserved
- [ ] prose-quality.md rules all applied

## Reference

- `ref/content-edit.md` -- the section / paragraph / sentence checklists in full.
- `../../REF/prose-quality.md` -- universal prose rules.
