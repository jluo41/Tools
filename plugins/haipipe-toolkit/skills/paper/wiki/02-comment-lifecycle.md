# Comment Convention and Lifecycle

Unified rule for inline comments across ALL paper skills. Every phase worker, lifecycle stage, and orchestrator follows this convention.

## Actor ids

The `{...}` token names **who** authored that line. Keep it short. One flat namespace:

| Kind | Examples | Note |
|------|----------|------|
| AI tool / agent | `CC` (Claude Code), `GPT`, `GEM` (Gemini), `CDX` (Codex) | reviewing tools; append `-<topic>` on findings |
| Person | initials (`AU`, `CO1`, etc.) | authors / coauthors |
| Role | `R1`, `R2`, `AC`, `ED` | numbered reviewers, area chair, editor |

**The human actor id is asked, never assumed.** At the start of a cycle the skill asks the user for their initials (and the pass date `vMMDD`). Never default to any specific initials.

## Two comment formats

### In outline .md files: blockquote style

```markdown
> USER: comment about this paragraph
> CC: response to the comment
```

Used in: section outlines, seed, claims, pitch, narrative, _CITATION_, _VALUES_.

### In .tex files: LaTeX comment style

```latex
%% {CC-content-v0531}: finding | suggestion ========>
```

Used in: 0-sections/*.tex, 4-display.tex, rebuttal files.

## The two marks (tex format)

### Finding (the comment)

```
%% {<actor>-<topic>-vMMDD}: <one-line finding> | <one-line suggestion>
```

- `<actor>` -- who wrote it. A reviewing AI appends the topic for traceability: `CC-content`, `CC-values`, `GPT-cite`.
- `vMMDD` -- the pass date (e.g. `v0531`). New round = new date.
- `<finding> | <suggestion>` -- what's wrong, then what to do. One line each.

### Reply (same line, after the separator)

```
%% {CC-content-v0531}: claim stated as causal. | Soften to "associated with". ========> {AU v0531}: accept
```

- `========>` -- the reply separator (literal, eight `=` then `>`).
- Reply verb vocabulary: `accept` / `reject` / `modify: <how>` / `discuss: <q>` / `done`.

## Anchoring (tex files)

A comment sits on its **own line, directly below the text it refers to**:

```latex
Agreeableness showed the strongest positive correlation ($r = 0.62$).
%% {CC-values-v0531}: 0.62 here vs 0.747 in the table. | Reconcile. ========>
```

For wrapped paragraphs, use `@"quote"` to anchor: `%% {CC-content-v0531}: @"we next examined" opener is throat-clearing. | Start with the finding.`

## Comment lifecycle

Comments come from two places:
1. **Inline in the working file**: `> USER:` comments (outline) or `%% {USER}:` comments (tex)
2. **Session (chat)**: direction, reasoning, taste decisions -- agent writes these into the file as `> USER:` (quoting what the user said)

```
1. User adds comment in the .md file (or says it in session, agent writes it in)
2. CC responds underneath
3. Work happens, content changes
4. User confirms resolved
5. Comment thread MOVES to _LOG (with -> applied / -> rejected / -> deferred)
6. Working file stays clean
```

### Rules

1. **Comments live in the working document while active.** They sit next to the content they discuss.
2. **Agent never removes a comment.** Only the user confirming resolution triggers the move.
3. **Resolved comments move to `_LOG`**, grouped by phase and date. The comment thread is preserved verbatim.
4. **Session comments that represent decisions** are written into the working document so they enter the same lifecycle. Ephemeral chat that is not a decision disappears with the session.
5. **Each phase starts with a clean file.** When draft closes and probe begins, all draft-phase comments have been resolved and moved to `_LOG`.

### _LOG format

**Ordering: newest entry at the TOP.** A `_LOG` is read to answer "what just happened", so new phase/date blocks are INSERTED directly under the file's H1 title, not appended at the bottom (reverse-chronological, like a changelog). Within one block, lines stay in writing order. When touching a legacy bottom-appended `_LOG`, reorder its blocks newest-first in the same edit (JL, 2026-07-05).

**Insertion is non-destructive.** The previous top entry keeps its `## <date> — <phase>` heading and body byte-intact; the new block slots BETWEEN the H1 and that heading. An insert that eats the prior entry's heading is a defect (live test-2-2222: the top-insert clobbered the `## 2026-07-04 — DRAFT` heading and left its bullets orphaned).

**Block headings carry date + HH:MM** (`## 2026-07-05 13:29 — [PHASE] PROBE — START`), so the `_LOG` doubles as a coarse on-disk timeline of the run (JL, 2026-07-05; fine-grained view = 0_utils/haipipe-run-timeline over the transcripts). Legacy undated/time-less headings stay as-is; only new blocks get stamped.

```markdown
## draft  2026-07-03

### Seed Question
> USER: don't use "discretion", too academic
> CC: reframed to "room for judgment"
-> applied

### Motivations
> USER: lead the first motivation with a puzzle
> CC: done, led with "the puzzle is..."
-> applied
```

### Why move, not copy

- The working document stays readable as content, not buried in old discussion.
- Each phase gets a clean slate.
- `_LOG` preserves the full reasoning chain for future reference.
- If a comment is reopened, it is written fresh (new `> USER:` comment), not resurrected from `_LOG`.

## REVISE phase: no comment-first

REVISE is the exception. REVISE workers apply changes directly (no comment-first round). They leave `%% {CC-<worker>}: <why>` comments explaining non-trivial changes. These comments are for CHECK to review, not for a human reply cycle. The human reviews in CHECK and can add `> USER:` comments to restart REVISE.

## Round invariants (tex comment-first, when used)

| Round | A skill MAY | A skill MUST NOT |
|-------|-------------|------------------|
| **1 -- review** | insert `%% {CC-...}:` comment lines | change any body text, banner, label, or value |
| **2 -- apply** | apply changes for `accept` / `modify` replies | touch any `OPEN` comment; apply a `reject` |

Round 1 diff adds only comment lines. If any non-comment line changed, the pass violated the protocol.
