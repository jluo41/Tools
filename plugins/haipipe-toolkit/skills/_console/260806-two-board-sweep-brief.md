# The two-board sweep · shared ground-truth brief (260806, JL: "放手一搏,一页一个 sub-agent")

Every page agent reads THIS FILE FIRST, then its one target page, then works.

## The architecture as of 260806 (correct any page that contradicts it)

1. ONE DOOR: the paper family registers exactly ONE skill, `paper/haipipe-paper` (0.7.0).
   Retired into it: -enter, -lifecycle, -stage (260805), folder/conform/compile/diffpdf/
   project/to-overleaf/to-word as fn/ verbs, round/rebuttal as S10 stage DATA (260806).
   All old paper skills live in `paper/_old/`. Stage data: S01-opening … S10-round
   (stage.md contract+craft, template.md, craft .md files, checker scripts).
2. THE ENGINE: `board/haipipe-page` 0.21.0. Page = TYPE x PHASE. Ten types under
   `board/page-types/`, four phases under `board/page-phases/`. Verbs CREATE / WORK ON /
   RUN (receipts under _runs/, first live RUN 260805 on QB8e).
3. EVIDENCE PAGES (the 260806 redesign): for-literature/for-value 0.4.0. A page declares
   `route: outward|inward` in its metadata HEAD (resolution step 2; the old
   `### Q-consumer register` marker is RETIRED). Content = one `### E<n> · <question>`
   division per Q-executor conversation + standing `### E0 · incoming` queue. Each E<n>
   owns: `🔗 QA-probe:` pointer line, `#### consumers` (collected Q-consumers + their
   A-consumer interpretations + row states), `#### answer digest`.
4. NAMES: files are QA-bank (the original, tasks|discoveries/.../QA/<n>-<slug>.md,
   `# Q` = Q-executor, `## Answer` = A-executor) and QA-probe (the paper's hidden stub,
   probes/L|V<nn>-<topic>/<n>-<slug>.md, digit-first so the page glob never sees it).
   "entry" is informal only. Slot words, four, CAPITALS everywhere incl. heading slots:
   Q-consumer, A-consumer, Q-executor, A-executor. Relations: one E<n> <-> one QA-probe;
   many QA-probes -> one QA-bank. Consumer pair lives on visible pages; executor pair
   lives in the two QA files; the stake never crosses to the bank.
5. LOG GRAMMAR (ruled, contracts pending the paused Log pass): one line per event,
   `- <date> [<time>] · [<PHASE>-<actor>] <what moved> [→ pointer]`; bare `[CC]` only for
   meaning-preserving housekeeping; label by the AUTHORITY exercised; old lines never
   rewritten.
6. Chip/evidence cards: register rows on evidence pages render cite/val chips whose
   popover cards fold PDF previews shut (haipipe-board 0.124.x-era renderer).
7. Commits: Tools bcd5e1cd is the baseline of this sweep.

## Per-page protocol (each agent, ONE page)

- Read this brief, then the target page COMPLETELY.
- Fix ONLY what is false, dead, or retired-presented-as-live against the ground truth:
  facts, paths, skill names, section grammar, state-line claims. Keep the page's voice.
- History is frozen: dated `## Log` entries, `## Law` rulings, Discussion lanes,
  `> USER:` lines are NEVER edited (a retired name inside dated history is legal).
- Style: English only, no em-dashes, record lines not pipe tables, one idea per line.
- Add exactly one Log line at top of `## Log`:
  `- 260806 <HHMM> · [REVISE-CC] swept to the 260806 architecture; <main correction>`.
- Do NOT rebuild the board (the sweep coordinator rebuilds once per wave).
- Do NOT touch any other file. Self-check is local evidence, never approval.

## Rosters (skip _archive/, board/, fig/, _runs/; pages already swept 260806 are marked ✓skip)

BOARDFORM `Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/`:
wave B1: QB-delivery/QB1-form.md · QB2-board-webpage-design.md · QB2a-sidebar.md ·
         QB3-folderq.md · QB4-overall.md
wave B2: QB-delivery/QB7-diagramattach.md · QB8-overview.md ·
         QB8e-sentence-details-lifecycle.md · QB5-page-loop.md · QB6-page-types.md
         (QB5/QB6 got partial updates 260806: verify rather than rewrite)
wave B3: QCskill-engine-skill/ all 10 (Skill-0,3,4,5,6,7,8 + Agent-1,2,3)
         (synced 260805 night: verify against 260806 evidence redesign, esp. Skill-3/
          Skill-0 probe wording)
wave B4: QA-design/QA0-three-folders.md · QA1-concepts.md · QA2-question-group-design.md ·
         QA3-the-round.md · QA4-board-skillset.md (fresh 260805 slide page: verify only)
wave B5: QC-engine/ all pages (ls at dispatch)
wave B6: QD-working/ all pages
wave B7: QE-sharing/ + QF-execute/ all pages
wave B8: QG-meeting/ + meeting/ pages (Meeting-* are generated: verify, never re-generate)

PAPER BOARD `Tools/plugins/haipipe-toolkit/skills/diagrams/01-haipipe-paper-260725/`:
wave P1: QA-design/QA0 · QA1 · QA2 · QA3 · QA4 · QA5 ✓ · QA6 · QA7 (swept 260806 morning:
         verify only the evidence-page sections against the E-division redesign)
wave P2: QA-design/QA8 · QA9 · QA10 · QA11 ✓ + QC-engine/QC1 · QC1a · QC2 · QC3
wave P3: QC-engine/QC3a · QC3b · QC3c · QC3d · QC4 · QC4a · QC5 · QC6 ✓partial
wave P4: QBv-venue-packs/ QBv0..QBv16 (verify Sec- index + section-kinds path claims only;
         these are venue catalogs, architecture rarely leaks in)
wave P5: QCskill-engine-skill/Skill-0-haipipe-paper.md ✓ + QF/QR/S groups (list at dispatch)

## Coordinator notes found mid-sweep (do not act on these as a page agent)

- DATE LABEL: the wall clock read 2026-08-05 all through this sweep, and every
  commit today is stamped 260805, but the brief and ~100 Log lines say 260806.
  Five page agents flagged it independently and each matched the wave rather
  than split the convention. Uniform now, one normalization pass owed, JL's
  call whether the receipts read 260805 or the sweep keeps its 260806 label.
- ENGINE BUG (closeout item 8): a backticked path token inside a `###` heading
  renders a `.fp` chip whose href never goes through `tree_reroot()`, so the
  board-root-relative path stays at board-root depth inside every cross-page
  link preview, and it nests an `<a>` inside an `<a>`. One such heading on
  QE5 produced 66 dead-href ERRORs across the built tree. Worked around at the
  source (backticks dropped from that heading); the renderer is still wrong.
- board.md Links repointed 260806: `haipipe-paper-stage/` to `paper/_old/`
  (retired 260805), and `02-method-260722/` to its renamed folder
  `02-subjective-label-260722/`. Board is back to its 2-error baseline.

## Per-board closeout (coordinator)

1. Rebuild the board once per wave; check.py after the final wave (no new ERRORs vs
   baseline: boardform 173/2, paper design 195/75).
2. ONE fresh haipipe-board-reviewer-agent per board: cold-read ALL changed Openings
   consecutively in Board order; interchangeable or form-letter prose fails.
3. Findings route back as single-page fix agents; then one final rebuild + commit
   "Two-board sweep to the 260806 architecture" quoting JL's 放手一搏 line.
