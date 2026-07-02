# 4-edit dry-run — `02-05_trait-rating-correlation.tex`

A sandbox test of Stage 1 (format-check) + Stage 2 (annotate) on a real section.
The live manuscript was **not** touched — everything here is a copy.

Files:
- `02-05_original.tex` — verbatim copy of the real section.
- `02-05_stage1_formatted.tex` — after format-check (paragraph banners added).
- `02-05_stage2_annotated.tex` — after a content annotation pass (comments added).

## Invariant checks (final: all pass)

| Check | Result |
|-------|--------|
| Active prose **byte-identical** original → stage 2 (21 active lines) | ✅ PASS |
| Stage 2 added **only** `%% {CC-content-v0531}:` comments | ✅ (6 comments) |

**Canonical verifier** = strip comments/blanks from both files and `diff` the
remaining prose:

```sh
strip(){ grep -v '^%' "$1" | grep -v '^[[:space:]]*$'; }
diff <(strip original.tex) <(strip stage2.tex)   # must be empty
```

This is robust; a plain line-`diff` is **noisy** (inserting banner blocks between
sentences makes `diff` resync poorly and report prose as "re-added"). Use the
strip-and-compare form for the verifier script.

## ⚠️ The check caught a real error — note this

On the **first** run, CHECK 3 FAILED: the stripped-prose diff showed one extra
line. Cause: while hand-building the stage files I had **invented a `P3.S5b`
sentence that does not exist in the source**, and then "found" it as a duplicate
(a fabricated finding). The mechanical check flagged it immediately; the bogus
sentence and its finding were removed.

Lesson, and the whole point of comment-first + the verifier: **an annotator must
not introduce text in Round 1, and the strip-prose diff makes any violation
impossible to miss.** This is exactly why the verifier script is the #1 follow-up.
(There is **no** duplicate-synthesis bug in the real manuscript.)

## What format-check had to do (Stage 1)

The real file **already** uses one-sentence-per-line + `%% ---- Pn.Sm ----` tags,
so format-check reduced to **adding 3 paragraph banners** (one per paragraph):

```
% Para [trait-rating.setup]      Setup  -- does each trait retain variance independent of the rating?
% Para [trait-rating.partial]    Result -- correlations strong but partials stay non-zero
% Para [trait-rating.regression] Result -- Big Five independently predict the rating (R^2=0.803)
```

Preserved verbatim: the header "Logic diagram" comment block, the figure block,
the `%` sentence separators, and the **provenance brackets** already in the tags
(`[NEW v0519: …]`, `[was P1.S1 in v0518; …]`). These are the allowed one-line
hints, so they stay.

## Format decision (resolves the #2 fork)

- Confirmed: real `0-sections/` = `%% ---- Pn.Sm ----`, **no banners**. Our banner
  layers on top cleanly without disturbing the existing tags → **adopt
  banner + `Pn.Sm`** (validated on real data).
- **Migration cost is low** for already-tagged files (banners only). Untagged
  files would also need sentence-splitting — still mechanical, same words.
- **Stale doc found:** `0-sections/README.md` describes a third, older format and
  lists wrong filenames (`01-introduction.tex`). Should be updated (follow-up).

## Content findings the annotator surfaced (6)

1. `[trait-rating.setup]` paragraph does several jobs — a Setup para also delivers a result (S3, r=0.81) and a caveat (S4); move the result to P2.
2. `P1.S3` r=0.81 vs `P2.S2` r=0.814 for the same quantity → cross-topic flag to the values pass (`% TODO[values]`).
3. Term drift: "trait--satisfaction" vs the caption's "review rating score" for one measure → consistency pass.
4. `P1.S4` packs two assertions on a `;` → split.
5. `P2.S1` restates the figure caption → cut/compress to a `\ref`.
6. `P3.S2` (violin-shape aside) interrupts the Big-Five → regression flow → relocate.

The annotator correctly **flagged** the numeric mismatch (#2) and term drift (#3)
for their own topic passes rather than fixing them in the content pass — the
cross-topic hand-off the protocol intends.

## Verdict

The 5-stage design survives contact with a real file. Comment-first is
enforceable; banners coexist with the existing `Pn.Sm` tags; the annotator finds
genuine, actionable issues; and the verifier caught a fabricated line on the first
pass — which is the safety property we want.

## Recommendations (next)

1. **Verifier script** — `scripts/check_comment_only.sh <orig> <new>` wrapping the
   strip-and-compare diff + the "added lines are all `%%`" check, so Stage 1/2
   output is **gated, not trusted**. Highest-value add (this dry-run proves why).
2. **Apply to the real file** — if you accept the format, run Stage 1 on the live
   `02-05…tex` (banners only) and commit as the first migrated section.
3. **Fix `0-sections/README.md`** to document the banner + `Pn.Sm` convention.
4. **Wire `/haipipe-paper-section-edit`** — confirm the orchestrator + `agents/` are invocable in
   the plugin manifest (untested).
