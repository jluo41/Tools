# Known Bugs

Issues you'll hit when running `make-diff.sh` against real papers, with
diagnosis and fixes. All of these are encoded in the script — this file
documents *why* the workarounds exist, so future maintainers don't undo
them.

---

## 1. Empty page 1, title block on page 2

**Symptom**: page 1 of the diff PDF is blank except for the running header;
page 2 has the journal nameplate + title + abstract that should be on page 1.

**Diagnosis**: word-level diff inside `\TITLE{}` (or analogous title macro)
overruns the fixed-height title block. The class engine reserves a
multi-line title region; struck-through old title + colored new title
together exceed it, kicking the whole title page forward by one.

**Fix**: exclude title macros from word-level diff via `--exclude-textcmd`.
Diff renders only the new title (deletions silently dropped). For INFORMS:
`TITLE,RUNTITLE,RUNAUTHOR`. For ACM/IEEE/standard: `markboth,thanks`.

**Recovery if you still want the old title visible**: edit `old/master.tex`
to use the same title as `new/master.tex`. The title-line shows zero diff;
deletion + addition can be documented as a comment alongside the title in
the source instead.

---

## 2. perl stderr leaks into diff.tex preamble (also empty page 1)

**Symptom**: same as bug #1 but title macros aren't to blame — even after
syncing titles between old/ and new/, page 1 stays blank.

**Diagnosis**: the silencer's diagnostic summary (`Protected blocks: ...`,
`Total silenced: 11`) leaked from stderr into stdout via a bash `2>&1`
redirect. Those lines became plain text at the top of diff.tex, before the
preamble. LaTeX rendered them as content on page 1, pushing the title page
to page 2.

**Fix in script**: replace `2>&1` with `2> >(sed 's/^/    /' >&2)` so stderr
goes to the terminal, not into the output file.

**Detection**: `head -3 1-diff/<sub>/<main>-DIFF.tex` — if the first lines
are anything other than `%DIF` comments or class-setup commands, you've
got a leak. Strip them with `sed -i '1,Nd'` and patch the redirect.

---

## 3. latexdiff treats \ABSTRACT as opaque, abstract changes invisible

**Symptom**: the abstract changed in the source, but in the diff PDF the
old abstract is replaced by the new one wholesale (no inline tracking).

**Diagnosis**: `\ABSTRACT{...}` (INFORMS uppercase) isn't in latexdiff's
default safe-cmd list, so it's treated as opaque — the whole macro
invocation is one delete + one add.

**Fix**: `--append-textcmd=ABSTRACT` tells latexdiff to descend and
word-level-diff the contents.

**Caveat**: only works if the abstract content is plain LaTeX (citations,
basic emphasis). If it has math or unusual environments, latexdiff may still
give weird results.

---

## 4. Silencer hides changes inside the abstract too

**Symptom**: `silenced-changes.txt` correctly hides the body's audit-fix
arithmetic (e.g. `6.7→6.5`) but ALSO hides the same change in the abstract.
For high-stakes review, every abstract change should remain visible.

**Diagnosis**: regex-based silencing matches the (old, new) pattern
everywhere it appears, including inside `\ABSTRACT{...}`.

**Fix**: `protect-block: ABSTRACT` directive in `silenced-changes.txt`
(or `silence-minor-changes.pl` defaults). The script splits the document
into protected and unprotected segments, applies silencing only to the
unprotected ones.

---

## 5. git archive fails when class files were added after baseline

**Symptom**: `make-diff.sh` errors out with
`fatal: pathspec 'informs4.cls' did not match any files`.

**Diagnosis**: the script archives a glob like `*.cls` against the baseline
commit. If the user added `informs4.cls` later (e.g., when starting the
submission build), it's missing in the older baseline, and `git archive`
refuses the whole archive call.

**Fix**: archive only files that exist at the baseline (filter with
`git ls-tree --name-only`). For class/style/logo files missing at the
baseline, copy the current versions into `old/` so the diff still
compiles.

---

## 6. latexdiff-vc tries `latex` (DVI mode) on PDF includes

**Symptom**: using `latexdiff-vc --git --flatten` instead of the manual
git-archive approach: errors with
`Something went wrong in executing: latex -draftmode -interaction=batchmode`.

**Diagnosis**: `latexdiff-vc --flatten` runs `latex` (not `pdflatex`) to
generate the .bbl during preprocessing. Plain `latex` produces DVI output
and can't include `.pdf` graphics — most modern papers fail.

**Fix**: don't use `latexdiff-vc`. Use a manual extraction pipeline:
`git archive` → write to `old/` → run plain `latexdiff --flatten` between
`old/master.tex` and `new/master.tex`. That's what `make-diff.sh` does.

---

## 7. Master tex file doesn't exist at the baseline commit

**Symptom**: `fatal: pathspec '0-Submission-v0429.tex' did not match any
files` even though the file exists in the working tree.

**Diagnosis**: the submission tex was added in a later commit. Older
baselines only had the working master tex (`0-MainPaper.tex`).

**Fix in script**: detect this case (`git cat-file -e $SHA:$MAIN_TEX`),
fall back to any `0-*.tex` (excluding `*-DIFF.tex` and `*-Submission-*.tex`)
that exists at the baseline. User can also explicitly pass the master tex
as the third argument: `make-diff.sh <commit> <tag> 0-MainPaper.tex`.

---

## 8. No abstract diff because the baseline already has the new abstract

**Symptom**: you expected to see the abstract rewrite tracked, but the diff
shows zero changes inside `\ABSTRACT{...}`.

**Diagnosis**: the abstract was rewritten in a commit BEFORE your chosen
baseline. The diff is faithful — there's nothing different between baseline
and current.

**Fix (synthetic baseline)**: edit `old/0-sections/00_abstract.tex` (or
equivalent) to be the version from an EARLIER commit that pre-dates the
rewrite. After editing, re-run latexdiff and recompile manually:

```bash
cd 1-diff/<sub>/
latexdiff --flatten <flags> old/master.tex new/master.tex > <main>-DIFF.tex
perl <skill-dir>/scripts/silence-minor-changes.pl silenced-changes.txt \
    <main>-DIFF.tex.bak > <main>-DIFF.tex 2> >(sed 's/^/    /' >&2)
# then bibtex + pdflatex pipeline
```

This is a "synthetic baseline" — useful when you want one diff PDF to show
the substantive arc of revisions without committing co-authors to chasing
multiple baseline commits. Document the synthesis in `<sub>/README.md`.

---

## 9. Audit-fix arithmetic clutters the diff

**Symptom**: 30+ small numerical change markers (6.7→6.5, 3.5→3.4, etc.)
across the body, drowning out the substantive prose changes.

**Diagnosis**: the values audit produced many small fixes that were
individually approved but bulk together produce visual noise.

**Fix**: list (old, new) pairs in `silenced-changes.txt` so the silencer
silently accepts each pair outside protected blocks. Co-authors see only
the prose changes; the audit-fix arithmetic was already approved upstream.

**Anti-pattern**: silencing changes that the user has NOT explicitly
audited. The silencer is for "we already verified these and don't need to
relitigate" — not for general noise reduction.

---

## Adding a new bug

When you hit a new failure mode:

1. Add a numbered section here with **Symptom**, **Diagnosis**, **Fix**.
2. If the fix is a script change, encode it in `make-diff.sh` or
   `silence-minor-changes.pl` and link to the bug number from a comment.
3. Update `SKILL.md` "Anti-patterns" if the bug came from a tempting
   shortcut you should warn future users away from.
