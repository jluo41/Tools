---
name: paper-diff-pdf-backup
description: "Build a tracked-changes PDF (latexdiff style) showing what changed between a baseline commit and the current working tree. Class-aware (INFORMS / ACM / IEEE / Springer LNCS / NeurIPS / ICML / Elsevier / generic article), with a scope-aware noise filter that silences audit-fix arithmetic but never hides changes inside the abstract or title. Use when user says \"build the diff PDF\", \"make a tracked-changes version\", \"diff this paper against <baseline>\", or before sending the paper to co-authors / advisor / reviewers for sign-off."
argument-hint: "[baseline-commit-or-tag] [tag-name] [main-tex]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

# Paper Diff PDF

Build a tracked-changes PDF showing what changed in the paper between a
baseline commit and the current working tree, so co-authors and reviewers
can see exactly what's new.

**Working tree is NEVER modified.** All output goes into per-baseline
subdirs under `1-diff/`.

## Why This Exists

Co-authors and editors don't want to read a full new draft and a full old
draft side-by-side. They want one PDF where additions are blue and
deletions are struck through — like Word's track-changes — so they can
focus reviewer attention on what actually changed.

`latexdiff` does this in principle, but the official `latexdiff-vc` wrapper
breaks on every modern paper class (DVI-mode bbl preprocessing fails on
PDF graphics; multi-file inputs need flattening; class-specific title
macros overrun page layout). This skill provides a class-aware driver that
handles those cases, plus a noise filter that silences audit-fix
arithmetic without hiding substantive changes in the abstract or title.

## How This Differs From Sibling Skills

| Skill | What it produces | When to use |
|---|---|---|
| `/paper-compile` | clean PDF of the current paper | every save, every iteration |
| `/paper-manual-review-values` | audit log of every numeric claim | before high-stakes submission |
| `/paper-manual-review-citations` | audit log of every cite | before high-stakes submission |
| **`/paper-diff-pdf`** | **tracked-changes PDF vs a baseline** | **when sharing changes with co-authors / advisor / reviewers** |
| `/citation-audit` | autonomous JSON+MD cite verdict | routine pre-submission check |

The manual-review skills tell you *whether each change is correct*; this
skill *visualizes the changes* for someone else to review.

## Constants

- **DIFF_TYPE = `UNDERLINE`** — latexdiff markup style. Additions blue with
  wavy underline, deletions red with strikethrough. Override via
  `LATEXDIFF_TYPE` in `1-diff/<sub>/config.sh`. Other choices: `CFONT` (color
  only), `BOLD`, `CHANGEBAR`, `TRADITIONAL`.
- **OUTPUT_DIR = `1-diff/vs-<tag>-<sha>/`** — relative to the paper root.
  One subdir per (baseline, target) pair; old subdirs stay around for
  historical reference.
- **SNAPSHOT_RETENTION = `keep`** — `old/` and `new/` snapshots stay in the
  subdir after compile (gitignored). Regenerate from git on demand by
  re-running the driver.

## Inputs

1. **Baseline commit-or-tag** (positional arg 1, required) — `a362838`,
   `v0429-tag`, `HEAD~5`, etc. Anything `git rev-parse` accepts.
2. **Tag name** (positional arg 2, optional) — human-friendly slug for the
   subdir name. `v0503` → produces `vs-v0503-a362838/`. Defaults to
   `vs-<sha>/` if omitted.
3. **Main tex** (positional arg 3, optional) — explicit master tex file.
   Auto-detected by default (prefers `0-*Submission*.tex`, then any
   `0-*.tex`). Use override when the auto-pick is wrong or when the master
   tex name has changed across baselines.
4. **(Optional) `silenced-changes.txt`** in the diff subdir — list of
   (old, new) numerical pairs to silently accept, plus `protect-block:`
   directives for blocks that the silencer must not touch.
5. **(Optional) `config.sh`** in the diff subdir — per-diff overrides
   (latexdiff flags, compiler choice, protected-block list).

## Workflow

### Phase 0: Confirm scope

Before running the driver:

1. Decide on the baseline commit. Look at `git log --oneline` for tagged
   submissions or natural milestones. Common baselines:
   - the last submission to a venue (label `v<MMDD>` or `submission`)
   - the last version reviewed by a specific co-author (label by name)
   - the last "consistency-pass" commit before the current revision
2. Confirm with the user which sections are in scope (default: all).
3. Identify the master tex. Default heuristic: `0-*Submission*.tex` first,
   else `0-*.tex`. Override if the paper uses a non-`0-` prefix.

### Phase 1: Run the driver

```bash
<this-skill>/scripts/make-diff.sh <baseline> [<tag>] [<main-tex>]
```

The script walks UP from `$(pwd)` to find the paper root (no need to be
IN the paper root). It performs six steps, all on the `1-diff/<sub>/`
sandbox:

1. Extract baseline tree via `git archive` (read-only, no checkout).
2. Copy current working tree to `new/`.
3. Auto-detect document class via `detect-paper-class.sh`; load preset
   latexdiff flags. Source `config.sh` if present (overrides).
4. Run `latexdiff --flatten` between `old/master.tex` and `new/master.tex`,
   producing `<main>-DIFF.tex`.
   - 4b. If `silenced-changes.txt` exists, run `silence-minor-changes.pl`
        to silently accept matching (old, new) pairs outside protected
        blocks.
5. Stage support files (.bib, .cls, .sty) and create the `0-display`
   symlink so figures resolve.
6. Compile with the auto-detected compiler (pdflatex / lualatex / xelatex)
   in the standard 4-pass + bibtex pipeline.

### Phase 2: Verify the output

Open `1-diff/<sub>/<main>-DIFF.pdf`. Check:

- **Page 1 starts with the title block** (no leading blank page). If page
  1 is blank, see known-bugs.md sections 1–2.
- **Title** renders cleanly (no struck-through text inside the title
  macro). If the old title is visible inside the title block and the
  result overruns, see known-bugs.md section 1.
- **Abstract** shows the changes you expect. If the abstract is wholly
  replaced (one big delete + one big add) instead of word-level tracked,
  see known-bugs.md section 3.
- **Body markup** is at the level you want. If 30+ small numerical
  changes drown out the prose changes, populate
  `silenced-changes.txt` and re-run.

### Phase 3: Iterate

Tighten the diff by editing files in the subdir:

- **Suppress audit-fix arithmetic**: add `OLD<TAB>NEW` lines to
  `silenced-changes.txt`. Re-run the driver.
- **Reveal something the silencer is hiding**: add a `protect-block: NAME`
  line so changes inside `\NAME{...}` stay visible.
- **Synthesize a baseline that didn't quite exist** (e.g., abstract
  rewrite that pre-dates the chosen commit): edit `old/master.tex` or
  `old/0-sections/<file>.tex` to be the version from an earlier commit,
  then re-run latexdiff + compile manually (skipping the driver's
  extract step).
- **Class auto-detect picks wrong macros**: write a `config.sh` with
  explicit `LATEXDIFF_EXCLUDE_TEXTCMD` etc.; re-run the driver.

### Phase 4: Commit

In the diff subdir, commit only:

- ✅ `<main>-DIFF.pdf` (the artifact)
- ✅ `<main>-DIFF.tex` (regeneratable but cheap)
- ✅ `silenced-changes.txt` (the noise filter, valuable for replay)
- ✅ `config.sh` (only if you wrote one)
- ✅ `README.md` if you added narrative about why this baseline / what to
  look at first

Don't commit `old/`, `new/`, or any build aux. The provided `.gitignore`
template handles this — copy it to `1-diff/.gitignore` once.

## Class auto-detection

`detect-paper-class.sh` greps `\documentclass` in the master tex and emits
recommended latexdiff flags. Recognized classes:

| Class | Venues |
|---|---|
| `informs0` / `informs3` / `informs4` | Management Science, ISR, MKSC, OR, MSOM, MOOR, ORSC |
| `acmart` | CHI, KDD, SIGIR, SIGCOMM, ACM TOG, etc. |
| `IEEEtran` | IEEE journals & conferences |
| `llncs` / `sn-jnl` | Springer LNCS, SN journals |
| `neurips_<year>` / `icml<year>` / `tmlr` / `colm` | ML conferences |
| `elsarticle` / `cas-sc` / `cas-dc` | Elsevier journals |
| `article` / `amsart` / `book` / `report` / `memoir` / unknown | Generic LaTeX (fallback) |

See `references/class-presets.md` for the per-class flag presets and the
reasoning. To add a new class: add a `case` arm to `detect-paper-class.sh`,
add a section to `class-presets.md`, test on a real paper of that class.

## Verification recipes

### "Is page 1 correct?"

```bash
pdftotext -f 1 -l 1 1-diff/<sub>/<main>-DIFF.pdf - | head -20
```

Expect to see the journal nameplate, title, "(Authors' names…)", and the
start of the abstract — all on page 1.

### "Are the changes I expect tracked?"

```bash
grep -c "DIFaddbegin\|DIFdelbegin" 1-diff/<sub>/<main>-DIFF.tex
```

Roughly equals the number of insertion + deletion blocks. Spot-check a few
that you remember adding by name:

```bash
grep -B1 -A1 "DIFadd.*<key phrase>" 1-diff/<sub>/<main>-DIFF.tex
```

### "Did the silencer leak stderr again?"

```bash
head -3 1-diff/<sub>/<main>-DIFF.tex
```

Should start with `%DIF LATEXDIFF DIFFERENCE FILE`. If you see plain text
like `Protected blocks: ...`, see known-bugs.md section 2 — the perl call
in the driver has a stderr redirect bug.

### "Working tree clean?"

```bash
git status --short
```

Should be unchanged from before the run. If new files appeared at the
paper root (e.g., a stray `.dvi` or `.aux`), the script regressed; see
known-bugs.md section 6.

## Anti-patterns

- ❌ "I'll just use `latexdiff-vc --git --pdf` directly." It fails on most
  modern papers (DVI-mode bbl preprocessing doesn't handle PDF graphics).
  See known-bugs.md section 6.
- ❌ "I'll edit the working tree to make the diff cleaner." The whole point
  of the sandbox is that the working tree is unchanged. Edit `old/` in the
  diff subdir if you need a synthetic baseline.
- ❌ "I'll silence everything I don't want to discuss." Silence only
  changes that have already been audited and approved. Silencing
  unverified changes hides bugs.
- ❌ "I'll silence in the abstract too." The abstract is the highest-value
  block for reviewer attention; every change there must remain visible.
  `protect-block: ABSTRACT` is on by default for good reason.
- ❌ "I'll merge two baselines into one diff by manually editing
  `old/`." It's fine to do this for ONE file (like the abstract) when the
  substantive arc spans multiple commits — but document the synthesis in
  the subdir's README so co-authors know the diff isn't a strict
  "vs commit X".
- ❌ "I'll commit `old/` and `new/` so the diff is reproducible." They're
  byte-perfect re-extractable from git. Committing them inflates the repo
  for no benefit. Use `.gitignore.tpl` from this skill.

## Output contract

For each invocation, the script writes (and the user commits a subset):

| Path | Committed? | Description |
|---|---|---|
| `1-diff/vs-<tag>-<sha>/<main>-DIFF.pdf` | ✅ | the tracked-changes PDF |
| `1-diff/vs-<tag>-<sha>/<main>-DIFF.tex` | ✅ | latexdiff source (replay-able) |
| `1-diff/vs-<tag>-<sha>/silenced-changes.txt` | ✅ | noise filter (valuable for replay) |
| `1-diff/vs-<tag>-<sha>/config.sh` | ✅ if exists | per-diff overrides |
| `1-diff/vs-<tag>-<sha>/old/` | ❌ gitignored | baseline snapshot (regenerable) |
| `1-diff/vs-<tag>-<sha>/new/` | ❌ gitignored | current snapshot (regenerable) |
| `1-diff/vs-<tag>-<sha>/0-display` | ❌ gitignored | symlink for figure resolution |

`templates/.gitignore.tpl` has the gitignore rules; copy to `1-diff/.gitignore`
on first setup.

## When to run

Run this skill:

1. **Before sending a revision to co-authors** — they review the diff PDF,
   not the full paper, and reply with comments scoped to actual changes.
2. **Before submission to a top-tier venue** — co-authors have last-mile
   approval over what changed since the previous draft.
3. **After applying reviewer comments in a revise-and-resubmit cycle** —
   the editor wants a tracked-changes PDF showing exactly what you did.
4. **After a major restructure or rewrite** — even pre-submission, this is
   the cleanest way to settle "what's actually different from yesterday's
   draft".

Do not run this skill:

- During early drafting (changes churn too fast; the diff is meaningless).
- Before the values audit (`paper-manual-review-values`) — the diff will
  be cluttered with unaudited arithmetic. Run the audit first, accept its
  fixes, then build the diff with those fixes silenced.

## Notes for the agent running this skill

- The driver hardcodes a 4-pass compile (`pdflatex` × 1, `bibtex` × 1,
  `pdflatex` × 2). If page numbers don't settle after that, run a fifth
  manual `pdflatex` pass in the subdir.
- When the user asks to "regenerate" a diff, just re-run the driver with
  the same baseline — `old/` is overwritten, `silenced-changes.txt` is
  preserved if present.
- When the user wants to compare against a baseline that doesn't have the
  modern submission build (`0-*Submission*.tex`), pass the working master
  tex explicitly: `make-diff.sh <commit> <tag> 0-MainPaper.tex`.
- The silencer's stderr summary is a useful sanity check ("Total silenced:
  N"). Keep it visible to the user — don't redirect to /dev/null. The
  driver pipes it through `sed 's/^/    /'` for indented display.
- Synthetic baselines (editing `old/` after extraction) are a legitimate
  technique. Document them in a README inside the diff subdir so co-authors
  understand what they're looking at.
- For figure-heavy papers, the `0-display → new/0-display` symlink is
  load-bearing. If you see "missing graphics" errors, the symlink is broken.

## See Also

- `paper-compile` (sibling) — clean compile, no diff
- `paper-manual-review-values` (sibling) — number-by-number audit (run first)
- `paper-manual-review-citations` (sibling) — cite-by-cite audit (run first)
- `references/class-presets.md` — per-class latexdiff flag recommendations
- `references/known-bugs.md` — failure modes + fixes (read before
  modifying the script)
- `references/compile-pipelines.md` — pdflatex / xelatex / lualatex notes
