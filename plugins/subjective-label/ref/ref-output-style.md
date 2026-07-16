Reference: Output Style Contract
================================

Every artifact this plugin writes must be **scannable in one glance**. A
researcher should see *what was done and where it stands* without reading prose.
This contract is binding on all skills and agents (sl-init, sl-iterate,
sl-validate, sl-status, gallery-keeper).

Principles
----------

1. **Result first.** Line 1 of every rendered file = the conclusion + the key
   number (status, κ, what changed). Never open with background.
2. **Tables/bullets over paragraphs.** No multi-sentence prose where a row will
   do. Any `reasoning` / `note` / changelog entry ≤ 1 line.
3. **Machine JSON gets a rendered `.md` twin.** Keep `*.jsonl` / `*.json` for the
   pipeline, but every one a human reads (trajectory, per-version eval, gallery)
   also gets a compact `.md` rendering written next to it.
4. **Cheatsheet + detail, layered.** Long documents (the guideline) keep full
   detail for the labeler, but ship a one-screen cheatsheet for humans.
5. **One-page dashboard.** `REPORT.md` and `/sl-status` fit in ≤ 15 lines: the
   whole project state at a glance.

Required rendered files (write/refresh these whenever the underlying data changes)
---------------------------------------------------------------------------------

- `REPORT.md`               — project dashboard (sl-init Step 9; refresh each iterate/validate)
- `eval/trajectory.md`      — version trajectory table + sparkline (every measurement)
- `gallery/gallery.md`      — gold items as a table (gallery-keeper, each write)
- `guideline/cheatsheet.md` — label + tiebreaker cheatsheet (gallery-keeper, each guideline change)

Templates
---------

### REPORT.md  (≤ 15 lines)
```
# {task} — {dimension} ({LABELS})

status **{status}**   guideline **v{N}**   gallery **{G}**   anchor **{A}**

| metric | value |
|--------|-------|
| anchor κ (vs gold) | {k} (acc {acc}) |
| generalization κ (fresh batch) | {kgen} |
| panel κ ({engines}) | {kpanel} |
| validate — {dataset} | agent {ka} {≥/<} ceiling {kc} → {converged/below} |

engine: {engine}
next: **{next command}** {one-line why}
```

### eval/trajectory.md
```
# Guideline trajectory
anchor: {A} items (fixed) · metric: Cohen's κ, majority vs gold

| ver | change | κ | acc | panel κ* |
|-----|--------|---|-----|----------|
| v01 | {≤1-line change} | {k} | {acc} | {kp} |
| ... |

\* panel κ = {engineA} vs {engineB} agreement

{ascii sparkline: κ on y, versions on x, one ● per version, mark dips/convergence}

converged at v{N} ({criterion})
```

### gallery/gallery.md
```
# Gold gallery — {dimension} (n={G})
| id | text (≤80 chars) | label | why (≤1 line) | diff |
|----|------|-------|-----|------|
| {id} | {excerpt}… | {LABEL} | {reasoning} | {boundary/clear} |
```

### guideline/cheatsheet.md
```
# {dimension} — decision cheatsheet
Full rules the labeler uses: guideline.md.

| label | signal | example |
|-------|--------|---------|
| {LABEL} | {≤6 words} | "{short quote}" |

Tiebreakers (N)
1. {≤1 line}  ...
```

Anti-patterns (do NOT do)
-------------------------
- Dumping a one-line JSON blob as the human-facing trajectory.
- Multi-paragraph changelog entries (compress to `vNN | what changed | κ`).
- A status/report that requires scrolling to grasp.
- Deleting guideline detail to shorten it — layer a cheatsheet instead.
