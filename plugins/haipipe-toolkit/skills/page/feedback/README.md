# skills/page/feedback · what JL asked for, session by session

One file per session, written by `haipipe-page/fn/reflect.md`. Each record holds
every input JL gave in that session, verbatim and in order, what the assistant
understood and did with it, and the changes JL wants in this skill family.

These are **drafts**. No record has been reviewed by JL, and nothing here has
been applied to a skill. A record is evidence, not a decision.

## The records

| Record | Session | Turns | Corrections | Wanted changes |
|---|---|---:|---:|---:|
| `260914-paper-misq-lit-v3.md` | Paper-MISQ-Lit-v3 | 163 | 30 | 16 |
| `260914-paper-misq-theory-v2.md` | Paper-MISQ-Theory-v2 | 134 | 43 | 7 |
| `260914-paper-misq-intro-v3.md` | Paper-MISQ-Intro-v3 | 127 | 28 | 13 |
| `260914-paper-misq-empirical-v2.md` | Paper-MISQ-Empirical-v2 | 94 | 25 | 11 |
| `260914-paper-misq-results-v2.md` | Paper-MISQ-Results-v2 | 92 | 24 | 10 |
| `260914-paper-misq-conclusion-v2.md` | Paper-MISQ-Conclusion-v2 | 24 | 8 | 7 |
| `260914-paper-misq-discussion-v2-last-part.md` | Paper-MISQ-Discussion-v2-last-part | 21 | 3 | 11 |
| `260914-paper-misq-abstract-v3.md` | Paper-MISQ-Abstract-v3 | 10 | 2 | 6 |
| `260914-haipipe-page-reflect.md` | Haipipe-Page reflect | 4 | 2 | 4 |
| **total** | 9 sessions, 2026-09-12 to 2026-09-14 | **669** | **165** | **85** |

All eight paper sessions worked on the MISQ paper. Seven wrote into
`examples/Project-Personality-OpioidRx/papers/Paper-AgreeablePrescriptionDiscretion/`.
Literature Review wrote into the older root `Paper-Personality2Opioid-MISQ2026/`,
which is why that section is ahead there and behind in the current paper.

## What repeats across sessions

Ranked by how many separate sessions raised it. A theme raised in six sessions
is a contract problem, not a bad turn.

### 1 · A build reports success while the file is stale · 7 sessions

The single largest theme, and every instance was caught by JL rereading the
artifact, never by the system refusing to report done.

- no mandatory source-hash or timestamp check before a delivery Run says
  complete: Theory 3, Conclusion 4, Empirical 8, Intro 7, Lit 9, Discussion 1
- `docx2pdf.py` keeps the previous PDF when Chrome headless fails, and still
  reports success: Discussion 6
- the LaTeX exporter prints raw `\citep{Key}` text instead of failing when the
  Page's `.bib` is missing: Discussion 7, and the same defect at Theory 1
- Word DOCX, its PDF twin and its view HTML are not built as one snapshot, so
  they drift apart from the same source: Intro 6
- tables silently vanish because the exporter still reads the retired
  `outline/evidence/display/` instead of `results/**/payload/`: Results 7,
  Empirical 9

Owners: `page-plugins/haipipe-plugin-delivery/SKILL.md`, its `ref/latex.md`
and `ref/word.md`, and `page-plugins/_shared-export/`.

### 2 · The reply shows a status line instead of the material · 4 sessions

JL asked to see the actual paragraph, diagram or document, not a link and a
state word.

- every Run reply must carry the rendered material: Empirical 1 (4 turns),
  Lit 1 (4 turns)
- a section review returns a compact before and after proposal, not a full
  redraft or a rubric dump: Discussion 3
- the reply shape JL converged on: Run heading, per-sentence breakdown, a
  location, before, after and reason table, links last: Lit 2
- print the manuscript into the reply rather than linking it: Abstract 4
- give a short diagnosis and labeled options, do not touch the Draft yet:
  Theory 5 (6 turns)
- a requested comparison belongs in chat, never in a Run file: Intro 13

Owners: `haipipe-page/ref/user-check-packet.md`,
`page-workflows/haipipe-page-workflow/ref/writing-step-template.md`. The last
three are global preferences owned by `AGENTS.md` and `CLAUDE.md`.

### 3 · Run naming and Run lifecycle · 5 sessions

`haipipe-page/ref/page-run-families.md` is the most named file in the whole
set, eleven times.

- the documented Delivery family is `rd01_web`, `rd02_latex`, `rd03_word`, but
  every session used `rd00_content`, `rd01_latex`, `rd02_word`, with
  `rd00_content` invented mid-session: Results 4, Theory 4, Empirical 5
- a whole-section rewrite needs its own identity, distinct from paragraph and
  structure Runs: Empirical 4
- directing the session to the next Run means the current one is accepted and
  closed: Intro 12, and the same rule unapplied at Results 2
- once a Run is accepted the next one should open in the same reply:
  Empirical 2
- a newly named scope opens in parallel, it does not wait for an open Run to
  close: Discussion 4
- never delete a Run, mark it historical with a pointer to what replaced it:
  Lit 12
- a Run marked complete still renders as Held because the closing heading does
  not match what the parser expects: Lit 4 (4 times in one session)
- check the Page's own Run inventory for its grouping convention before
  proposing new Runs: Intro 11

### 4 · The server behind every link · 4 sessions

- it died and needed a manual restart at least eight times in one session:
  Empirical 11, five times in another: Lit 14, seven turns in a third:
  Conclusion 1, twice in a fourth: Abstract 2
- two stale listeners served cached pages at once, so the page JL opened was
  wrong twice over: Conclusion 1
- one stable Draft Workspace address, never a Run-lens link: Conclusion 2

Owner: `haipipe-page/fn/serve.md`. Running it as a persistent process rather
than a foreground one is the change most often implied.

### 5 · Draft and Content drift apart · 4 sessions

- adopting the Draft into Page Content is not a named step, and one session
  both denied it exists and created it anyway: Empirical 5
- the adoption step should diff Draft against Content and name every
  unadopted paragraph before any export is built: Lit 9
- a review Run's recommendations were adopted one at a time, so a partly
  applied review looked like a server bug: Conclusion 3
- candidate prose that no longer matches a changed Shape is still shown as
  current: Empirical 3
- the rendered paragraph address is one higher than the source address:
  Abstract 3, Discussion 5
- the Opening paragraph has no canonical address, which cost about fifteen
  turns: Lit 3

### 6 · Evidence labels and migration · 4 sessions

- a mechanical lint for the documented placeholder syntax, since output drifted
  into `$V_{E09\_levels}$` and `/table{...}`: Results 1
- the unresolved VALUE convention took four rounds to settle: Intro 10
- the semantic citation placeholder `\cite{C_<meaning>}` should be canonical
  rather than rediscovered: Lit 10, Theory 2
- a resolved citation should appear as a real citation in Draft, not stay a
  raw label: Results 6
- the v4 migration has no awareness of a section's own BibTeX store, which is
  the root cause of the garbled PDF citations: Theory 1
- a migration must confirm display assets stay reachable by the exporter:
  Empirical 9

### 7 · Editing scope and prose rules · 4 sessions

- revise means constrained edit with provenance labels, not a free rewrite:
  Intro 8 (3 restatements), Theory 6
- an ambiguous mid-loop remark is a fix directive, not a status question:
  Lit 13
- route quality checks through the rubric tools that already exist,
  `writing/haipipe-writing/cli/score.py` and `ref/plain-rules.md`, instead of
  inventing reviewers each time: Empirical 6 (7 turns)
- over-protective hedging was the most repeated correction of the Results
  session: Results 10, and the same dimension was added by hand mid-session in
  Lit 7
- one argumentative job per sentence: Intro 9
- named AI-voice patterns to check before showing a draft: Conclusion 5
- the same clause repeated across sibling Bullets of one paragraph:
  Conclusion 6
- a source named in prose and repeated in a trailing parenthetical: Lit 15

### 8 · Single findings worth keeping

- the Run Space renderer misreads Evidence Runs as orphan Results, and omits
  the Delivery lane when it is empty: Intro 1, Intro 2, in
  `haipipe-page/live/runs.py`
- the live Board server can serve pre-v4 tab labels and inject computed numbers
  that are not in the Outline source: Intro 4
- a double-escaping bug in `md2tex.py` silently truncated a PDF mid-sentence,
  found and fixed in session: Intro 5
- a git status check inside a submodule reads the repository root and reports
  no changes: Discussion 10
- the Page CHECK report should say why CHECK is still pending: Discussion 11
- the audit template JL hand-typed three times in one session should become a
  real function: Lit 11
- deriving one Section's Structure Run from a sibling's has no documented
  pattern: Abstract 5

## How to use this folder

1. Read a record for one session, or read this index for the pattern.
2. Decide which items to act on. JL owns that decision; nothing here is a
   mandate and repetition is evidence, not authority.
3. Apply a change through the normal skill revision pass, one tag at the end of
   the body of work, not one per item.
4. Validate with a fresh subagent on a realistic task, per the repository's
   own rule about testing a revised skill.

A record's `status:` stays `draft · not yet reviewed by JL` until JL says
otherwise. Reflect writes records; it never edits a skill.
