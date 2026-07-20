---
name: haipipe-paper-revise-content
description: "Review and edit prose CONTENT at section → paragraph → weave → sentence. REVISE phase (fully automatic): applies changes directly, leaves %% {CC-content}: why-comments for CHECK. Self-contained — carries its own structure/claim/flow checks including the weave step (¶-to-¶ arc, hinges, rhythm). Trigger: edit content, review content, tighten section, restructure paragraphs, weave, paragraph flow, transitions, /haipipe-paper-revise-content."
argument-hint: "[section-name-or-number] [paper-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "1.4.0"
  last_updated: "2026-07-19"
  summary: "REVISE worker: edit prose CONTENT at section->¶->weave->sentence, change directly + leave why-comments. Carries the ¶-flow weave step (arc/hinges/rhythm, ref/weaving.md). Fully automatic."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# haipipe-paper-revise-content

REVISE phase worker: editing the **prose content** of a draft that already exists.
This skill changes *what the prose says and how it is built*.
Fully automatic -- applies changes directly, no human gate.

It does **not** verify numbers or citations against their sources (that is `haipipe-paper-check-evidence`), and it does **not** substitute a landed answer into a placeholder (that is `haipipe-paper-revise-place`, which has already run) -- but it **does flag** a number or citation the prose still needs, so the next DRAFT pass has a target.

## Before you start

Read the shared prose rules:

- `../../REF/prose-quality.md` -- universal writing rules (one idea per sentence, no em-dash, compress not split, no AI voice, <=6 sentences/paragraph, Pn.Sn markers)

Then confirm where you are: this is the REVISE phase, content worker.
Pick **one section**.

## Automatic apply with explanatory comments

REVISE is fully automatic.
The agent:

1. Reads the section (outline .md and/or .tex)
2. Applies fixes directly (no waiting for human approval)
3. Leaves a `%% {CC-content}: <why>` comment next to each non-trivial change explaining WHY the change was made

The comments are for CHECK to review.
The human sees what changed and why, and can add `> USER:` comments to restart REVISE if needed.

Trivial changes (whitespace, marker fixes) do not need comments.
Only explain changes where the WHY is not obvious from the diff.

## The pass, top-down

Work **section -> paragraph -> weave -> sentence**.
Get the section's job right, then each paragraph's point, then how the paragraphs connect, then the sentences.
Fixing sentences inside a paragraph that should not exist is wasted work.

1. **Section** -- state the section's one job in a sentence; make the paragraph banner skeleton (`grep '^% Para '`) tell the section's story; fix boundaries and order.
2. **Paragraph** -- one paragraph = one point (its banner's point); topic sentence first; merge/split so each banner is true.
3. **Weave** -- paragraph-to-paragraph flow: ARC (order/logic/redundancy, 🔴 first), HINGES (each Pn->Pn+1 seam picks up what Pn put down; content linkage, never bare connectives), RHYTHM (role variety).
   Method + severity discipline + role vocabulary: `ref/weaving.md`.
4. **Sentence** -- one assertion each; cut filler; concrete over vague; one term per concept.

## Flag, don't fabricate

When the content needs a number or citation that is not here yet, drop a marker instead of inventing one:

```latex
The model achieved {VAL:? held-out accuracy} accuracy on the held-out set.
This aligns with prior work \cite{TOADD} [Q-<Stage>-<n>] on trait extraction.
```

The bracket names the question that will settle it; a placeholder without one is a hole nobody owns.
Leaving a flag is correct; guessing a value or a citation is not.

## Done means

- [ ] Every paragraph has one clear job matching its banner
- [ ] One idea per sentence, no filler, concrete over vague
- [ ] Every missing number is `{VAL:? <what>} [Q-<Stage>-<n>]`, every missing citation `\cite{TOADD} [Q-<Stage>-<n>]`; none invented
- [ ] Non-trivial changes have `%% {CC-content}: <why>` comments for CHECK
- [ ] Banners present with ids preserved
- [ ] prose-quality.md rules all applied

## Reference

- `ref/content-edit.md` -- the section / paragraph / sentence checklists in full.
- `ref/weaving.md` -- the weave step: paragraph-flow diagnosis (ARC / HINGES / RHYTHM, severity + roles).
- `ref/write-principles.md` -- condensed revision rule sheet (comment preservation, hard rules).
- `ref/example-intro-logic-flow.txt` -- worked logic-flow example for an intro.
- `../../REF/prose-quality.md` -- universal prose rules.
