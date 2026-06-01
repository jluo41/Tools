# 4-edit / scripts

Helper scripts that make the comment-first protocol **enforceable**, not just
documented.

## check_comment_only.sh

Gates a pass: proves it changed no prose. The whole point of comment-first
(Stage 2 annotate) is that the prose is untouched — this is the mechanical check.

```sh
# annotate / comment-only gate — active prose must be BYTE-IDENTICAL
scripts/check_comment_only.sh <orig.tex> <new.tex>

# format-check gate (Stage 1) — same WORDS, re-wrapping to one-sentence-per-line allowed
scripts/check_comment_only.sh --mode words <orig.tex> <new.tex>
```

- Exit `0` pass · `1` prose changed · `2` usage/IO error.
- "Active prose" = lines that are not whole-line LaTeX comments (`^%`) and not blank.
- It strips comments+blanks from both files and diffs the remainder. A raw
  line-diff is deliberately avoided — inserting banner/comment blocks makes it
  resync poorly and falsely report prose as "added".

Use it after every Stage 1 (`--mode words`) and Stage 2 (default) edit. It is the
backstop that caught a fabricated sentence during the `_test/` dry run.
