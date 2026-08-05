# Comment Protocol

Canonical detail spec for inline comments across ALL paper skills. The door
(`../SKILL.md`, "Comment lifecycle") carries the binding subset and points here;
this file carries the full formats. If the two ever disagree, the door wins on
the binding rules and this file wins on format detail.

## Actor ids

The `{...}` token names **who** authored that line. Keep it short. One flat namespace:

| Kind | Examples | Note |
|------|----------|------|
| AI tool / agent | `CC` (Claude Code), `GPT`, `GEM` (Gemini), `CDX` (Codex) | reviewing tools; append `-<topic>` on findings |
| Person | initials (`AU`, `CO1`, etc.) | authors / coauthors |
| Role | `R1`, `R2`, `AC`, `ED` | numbered reviewers, area chair, editor |

**The human actor id is asked, never assumed.** At the start of a cycle the skill asks the user for their initials (and the pass date `vMMDD`). Never default to any specific initials.

## Two comment formats

In outline `.md` files, blockquote style:

```markdown
> USER: comment about this paragraph
> CC: response to the comment
```

Used in: section `.md` files, seed, claims, pitch, narrative, and nested S03/S04 probe entry pages.

In `.tex` files, LaTeX comment style:

```latex
%% {CC-content-v0531}: finding | suggestion ========>
```

Used in: `sections/*.tex`, `4-display.tex`, rebuttal files.

## The two marks (tex format)

Finding (the comment):

```
%% {<actor>-<topic>-vMMDD}: <one-line finding> | <one-line suggestion>
```

- `<actor>` -- who wrote it. A reviewing AI appends the topic for traceability: `CC-content`, `CC-values`, `GPT-cite`.
- `vMMDD` -- the pass date (e.g. `v0531`). New round = new date.
- `<finding> | <suggestion>` -- what's wrong, then what to do. One line each.

Reply (same line, after the separator):

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

## S-page `## Log` format

Every lifecycle S page owns both its current content and history. There is no
live `_LOG` sidecar. Insert new dated phase records directly under that page's
`## Log` heading, newest first. If the working document is the S page itself,
move the resolved thread from its content position down into its own `## Log`.

**Insertion is non-destructive.** The previous newest entry stays byte-intact;
the new entry slots between `## Log` and that entry.

**Entry headings carry date + HH:MM**
(`### 2026-07-05 13:29 — [PHASE] PROBE — START`), so the S page
doubles as a coarse on-disk timeline. Legacy undated entries stay as-is.

```markdown
### 2026-07-03 10:14 — [DRAFT] resolved comments

### Seed Question
> USER: don't use "discretion", too academic
> CC: reframed to "room for judgment"
-> applied
```

Why move, not copy: the working document stays readable as content; each phase
gets a clean slate; the S page preserves the full reasoning chain beside the
artifact it explains; a reopened comment is written fresh, not resurrected.

## Round invariants (tex comment-first, when used)

| Round | A skill MAY | A skill MUST NOT |
|-------|-------------|------------------|
| **1 -- review** | insert `%% {CC-...}:` comment lines | change any body text, banner, label, or value |
| **2 -- apply** | apply changes for `accept` / `modify` replies | touch any `OPEN` comment; apply a `reject` |

Round 1 diff adds only comment lines. If any non-comment line changed, the pass violated the protocol.
