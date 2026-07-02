# 1-diff/ — Tracked-Changes PDF Workflow

Purpose: produce a tracked-changes PDF showing what changed between a
baseline commit (e.g. last submission) and the current working tree, so
co-authors and reviewers can see exactly what's new.

Working tree is NEVER modified. All output goes into per-baseline subdirs.

## Layout

```
1-diff/
├── README.md                      ← this file
├── .gitignore                     ← excludes snapshots + build aux
│
└── vs-<tag>-<sha>/                ← one subdir per (baseline, target) pair
    ├── <main>-DIFF.pdf            ← the tracked-changes PDF (commit this)
    ├── <main>-DIFF.tex            ← latexdiff source (commit this)
    ├── silenced-changes.txt       ← noise-filter rules (commit this)
    ├── config.sh                  ← (optional) per-diff overrides
    ├── old/                       ← baseline snapshot (gitignored)
    ├── new/                       ← current snapshot (gitignored)
    └── 0-displays → new/0-displays  ← symlink so figures resolve
```

Naming: `vs-<tag>-<sha>` — e.g., `vs-v0503-a362838` reads as
"diff against v0503 (commit a362838)".

## Usage

Build a fresh tracked-changes PDF (script lives in the skill folder):

```
cd <anywhere-inside-paper-repo>
<path-to-skill>/scripts/make-diff.sh <baseline-commit-or-tag> [<tag-name>]
```

Examples:

```
make-diff.sh a362838 v0503        # against v0503 — produces vs-v0503-a362838/
make-diff.sh c982fb4 v0429        # against v0429
```

The script walks UP from the current dir to find the paper root (no need
to be IN the paper root).

## Noise filter

When the audit pass produces many small numerical fixes, those clutter the
tracked-changes PDF. Suppress them by listing (old, new) pairs in
`<subdir>/silenced-changes.txt`:

```
6.7	6.5
3.5	3.4
54.1	54.3
```

(Tab-separated. Lines starting with `#` are ignored. `protect-block: NAME`
directives prevent the silencer from touching text inside `\NAME{...}`
— defaults to ABSTRACT/TITLE/abstract/title.)

## What gets committed

- ✅ DIFF.pdf, DIFF.tex, silenced-changes.txt, config.sh, README.md, .gitignore
- ❌ old/, new/ — full source snapshots; regenerated from git on demand
- ❌ build aux files (.aux, .bbl, .log, etc.)
- ❌ symlinks (0-displays) — recreated each build
