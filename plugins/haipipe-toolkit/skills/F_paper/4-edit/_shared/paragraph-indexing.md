# 4-edit / shared — paragraph indexing

The standard for tagging paragraphs so each one has a **stable handle** to edit,
track, and reference across edit rounds. Every 4-edit sub-skill uses it.

This formalizes the existing `0-sections/` banner. One change from the original:
the identifying token is no longer the **positional** `P1/P2` (which renumbered on
every insert) — it is a **stable id** that never moves.

## The paragraph banner

```latex
% =========================================================
% Para [trait-rating.setup] Setup -- why correlate traits with star ratings
% =========================================================
Having characterized the distribution of physician personality traits, we next
examined how these traits relate to the star ratings patients assign...
```

Three comment lines directly above the paragraph. The middle line carries
everything:

```
% Para [<stable-id>] <Role> -- <one-line point>
```

| Token | Meaning | Stable? |
|-------|---------|---------|
| `[<stable-id>]` | permanent handle for this paragraph | **Yes — never rewritten** |
| `<Role>` | the paragraph's job in the section's argument | — |
| `<one-line point>` | the single point the paragraph makes | — |

Reading order is implicit (top-to-bottom in the file); the **id**, not a number,
is how you refer to a paragraph — so a TODO that says "tighten
`trait-rating.method`" stays valid even after the paragraph moves.

Grep the skeleton of any section with `grep '^% Para '`.

## `[stable-id]` convention

`<section-slug>.<para-slug>`:

- `<section-slug>` matches the filename slug (`02-05_trait-rating-correlation`
  → `trait-rating`).
- `<para-slug>` is a short kebab noun chosen from the paragraph's **point**, not
  its position (`setup`, `method`, `result`, `types`, `type-empath`).

```
trait-rating.setup   trait-rating.method   trait-rating.result
cluster.types        cluster.type-empath   cluster.type-expert
```

Unique within the file; globally readable when prefixed by the filename.
**Numbering scope is per file** — ids restart in each `.tex`; do not carry them
across `\input` boundaries.

### The one rule

**Never rewrite an id.** When you insert, delete, or reorder paragraphs, the
banners simply move with their paragraphs — there is no number to renumber. A new
paragraph gets a fresh id; a deleted paragraph's id retires with it.

## `<Role>` taxonomy

Universal roles (any section):

`Setup` · `Method` · `Result` · `Interpretation` · `Transition` · `Bridge`

Section-flavored roles (use when they fit better):

| Section | Typical roles |
|---------|---------------|
| Introduction | `Hook` · `Gap` · `Approach` · `Contribution` · `Roadmap` |
| Results | `Setup` · `Method` · `Result` · `Interpretation` |
| Discussion | `Summary` · `Comparison` · `Implication` · `Limitation` |
| Methods | `Design` · `Data` · `Procedure` · `Analysis` |

One role per paragraph. If two fit, the paragraph is doing two jobs — split it
(a content-edit finding).

## Going finer: sentence-level work

The banner is the **paragraph** unit, which is the grain 4-edit operates at. When
a job needs **sentence surgery** (rewriting, splitting, annotating individual
sentences), the Stage-1 `paper-edit-format-checker` nests sentence tags under the
paragraph and the `paper-edit-improver` edits them:

```latex
% =========================================================
% Para [trait-rating.result] Result -- agreeableness correlates strongest
% =========================================================
%% ---- P3.S1 ----
Agreeableness showed the strongest positive correlation ($r = 0.747$)...
%% ---- P3.S2 ----
Violin shapes tighten at higher trait levels...
```

`P3.S1` is positional and local to the paragraph; the banner's `[stable-id]` is
the durable handle for the paragraph as a whole. Use banners for 4-edit content
passes; use `Pn.Sm` only when you have descended into sentence editing.

## Banner hygiene checklist

- [ ] Every paragraph has exactly one banner, directly above it (no blank line
      between banner and prose).
- [ ] The id is unchanged from before the edit (or newly minted for a new para).
- [ ] `<Role>` is a single role from the taxonomy.
- [ ] `<one-line point>` is one clause and matches what the paragraph argues.
- [ ] No positional `Pn` is used as the paragraph's identity (ids only).
