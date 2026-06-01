# 4-edit / shared — sentence format (Stage 1: format-check)

Stage 1 of the edit-cycle normalizes a leaf `.tex` into the canonical working
layout so the later stages have stable anchors to attach comments to. It changes
**layout only — never wording**.

## The canonical layout

A normalized leaf carries two indices: the **paragraph banner** (stable id, from
`paragraph-indexing.md`) and the **sentence separator** `%% ---- Pn.Sm ----`
(positional). They coexist:

```latex
\subsection{Trait--Rating Correlation}

% =========================================================
% Para [trait-rating.result] Result -- agreeableness correlates strongest
% =========================================================
%% ---- P3.S1 ----
Agreeableness showed the strongest positive correlation ($r = 0.747$).
%% ---- P3.S2 ----
Violin shapes tighten at higher trait levels.
%
%% ---- P3.S3 ----
A multiple regression confirmed each trait contributes independently.
```

- **Banner `[id]`** — the durable handle for the paragraph (never renumbered).
- **`Pn`** — paragraph number, positional, restarts at `P1` per file.
- **`Sm`** — sentence number within the paragraph, positional, restarts per paragraph.
- **One sentence per line.** Each `%% ---- Pn.Sm ----` tag sits directly above its
  sentence; a lone `%` line may separate sentences for readability.

This is the same `Pn.Sm` convention the real npjDM `0-sections/` files already
use — Stage 1 makes every leaf consistent with it.

## What format-check does (and does not) do

| Does | Does NOT |
|------|----------|
| split wrapped paragraphs to one-sentence-per-line | reword, merge, or cut any sentence |
| insert `%% ---- Pn.Sm ----` separators | change a number, citation, or `\label` |
| add a paragraph banner where one is missing | reorder paragraphs or sentences |
| renumber `Pn.Sm` after structural shifts (reindex) | rewrite a stable `[id]` |

**Invariant: same words, new layout.** A format-check diff touches only
whitespace, line breaks, and `%%` index lines — concatenating the active text
before and after must yield identical prose.

## Numbering scope

`Pn` restarts at 1 in each `.tex` file (do not continue across `\input`). `Sm`
restarts at 1 in each paragraph. This keeps tags stable when sub-files are
rearranged. Reindexing after splits/merges is done by the
`paper-edit-format-checker` (it renumbers `Pn.Sm` and forward cross-references
but never touches sentence text or comments).

## Why this is Stage 1

Stages 2–4 attach comments to specific sentences (`%% {CC-…}` below a
`%% ---- Pn.Sm ----` line) and apply edits to specific sentences. Without the
one-sentence-per-line + `Pn.Sm` layout, a comment cannot point cleanly at its
target and the improve stage cannot apply a change to a single sentence. So
format-check runs first, once, before annotation.

## Quick checklist

- [ ] Every paragraph has a banner with a stable `[id]`.
- [ ] Every sentence has its own line and a `%% ---- Pn.Sm ----` tag.
- [ ] `Pn` restarts per file; `Sm` restarts per paragraph.
- [ ] Concatenated prose is byte-identical to before (no wording changed).
