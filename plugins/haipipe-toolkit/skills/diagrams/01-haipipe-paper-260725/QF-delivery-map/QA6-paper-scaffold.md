# ⑦ The paper folder: what exists on disk
state: 🟡 PARTIAL
owner: JL
method: test the proposed submission-cut and three-role projection model against the accepted 0/1/2 copy-only rule

## Question
What is in one paper's folder, and how can a reader tell at a glance which parts are the manuscript and which are the machinery that produced it? A mature paper accumulates a board, a probe pool, generated LaTeX, display units, build scripts, archives and a compiled PDF, all in one directory. Without a rule that directory becomes a place where you check three things before daring to delete anything.

The proposed replacement rule treats the prefix as a packaging boundary rather than a taste: numbered paths stay out of the journal submission cut, while the unnumbered tree must still compile and submit by itself.
The old `rm -rf 0-* 1-* 2-*` wording described running that test on a copy; it never meant that `0-lifecycle/`, which holds the authoritative S pages, was safe to erase from the working repository.
The live paper now also has `3-dist/`, so the fixed claim that there are three numbered folders and only three is reopened here.

The second rule is that nothing exists before it is needed. A new paper gets a control plane and one runnable page; every other page arrives when its unit is allocated, and the LaTeX toolchain arrives at the Display or section frontier and not before. What we want is a folder where every file present is a file somebody asked for, so an absence is information rather than an oversight.

## Boundary
- ✅ Covered here
  What a paper folder contains, the numbered and unnumbered split, what exists at creation versus later, and what crosses this folder's edges.
- ↪ Covered elsewhere
  What is on the board inside it is `QA7`; how a question leaves it is `QA5`; markdown versus tex authority is `QB2d`; who creates a page is `QA8`; what a display unit contains is `QC3` and `QD1`. What a STAGE is as an object, and what it takes to make one work, is the whole `QB` group, anchored at `QB1`; this face owns only which stages exist and which folder each one fills.

## Diagram
```
   A PAPER FOLDER.   PROPOSED GENERALIZATION OF THE 0/1/2 COPY TEST
                     ● = exists on day 0   ○ = absent until allocated

   Paper-X/
   │
   ├─ ✂️ NUMBERED · PROPOSED: excluded from submission cut ─────────────┐
   │                                                                    │
   ● │  0-lifecycle/     ⑧ THE BOARD, and nothing but the board        │
   │ ● │    board.md · board.html                                       │
   │ ● │    0-seed/   ○ 1-work/   ○ 2-venue/    ○ 3-display/           │
   │ ○ │    4-main/   ○ 5-appendix/ ○ 6-submission/ ○ 7-round/         │
   │ ○ │    _archive/                                                   │
   │ │                                                                  │
   ● │  1-probes/        the near side of the wall            → ⑤       │
   │ ○ │    PPnn_<topic>/QXn_<slug>.md   topic-scoped, cross-stage      │
   │ │                                                                  │
   ○ │  2-src/           how the deliverable is BUILT, not what it is   │
   │   │    compile.sh · compile.ps1 · config.yaml · setup.sh           │
   │ │                                                                  │
   🟡│  3-dist/          proposed fourth: review/handoff projections     │
   │   │    tex/         candidate LaTeX + proof PDF, never the source  │
   │   │    word/        coauthor copies; edits return to the S page    │
   │   └────────────────────────────────────────────────────────────────┘
   │
   └─ 📦 UNNUMBERED · PROPOSED JOURNAL SUBMISSION PROJECTION ───────────┐
                                                                       │
     ○   <paper>.tex        the driver: \\input each section            │
     ○   <paper>.bib        HUMAN-ONLY. An agent greps; never writes.   │
     ○   <paper>.pdf        the compiled artifact                       │
     ○   sections/          GENERATED from ⑧'s 4-main pages. ONE WAY.   │
     ○   appendices/        GENERATED from ⑧'s 5-appendix pages         │
     ○   displays/          one folder per unit. THE ONLY home of an    │
     │                      asset. There is NO top-level figures/.      │
     ○   <venue>.cls · <venue>.bst      the venue shell                 │
                                                                       │
     └─────────────────────────────────────────────────────────────────┘

   ── proposed generalized packaging test ───────────────────────────
      on a copy: remove [0-9]-*  and the paper still compiles/submits
      this is a SUBMISSION-CUT test, not permission to erase sources
```

```
   ── INSIDE ONE DISPLAY UNIT.  the delete test, one level down ─────

      displays/displayNN-<slug>/
        📦 float.tex      the \caption + \label the section \inputs
        📦 assets/        the promoted render: figure.pdf | table-body.tex
        ─────────────────────────────────────────────────────────────
        ✂️ README.md      what this display argues, and for which claim
        ✂️ preview.tex    a one-page standalone, to look at it alone
        ✂️ preview.pdf    the build product of that
        ✂️ source/        REBUILD.md, the script, the query
        ✂️ candidates/    renders we did not pick
        ✂️ versions/      renders we picked before

      2 of 8 ship. The unit is the ONE place the numbered/unnumbered
      split does not reach, because a unit is a folder, not a prefix.
      → the ruling that closes this is in Discussion, not yet made.

   ── ⚠️ why figures/ was WRONG, and is now gone ────────────────────
      It came from the npjDM2025 layout, which predates display units.
      Before migration, figures/ held 5 loose PNGs under ai_generated/
      and ZERO \includegraphics in the whole paper pointed at any of
      them. They now live in _archive/figures-orphan/. Every real
      graphic is already inside a unit's assets/.
      A second home for the same kind of thing is the exact defect
      this face forbids everywhere else.
```

```
   ── WHO WRITES WHAT, and WHICH SKILL THIS RULE CHANGED ────────────
      ✅ rewritten to this layout on 260726
      ⬜ still names paths that no longer exist   (old-path · STATUS.md)
      ➖ never names a paper path; nothing here to change

      WHAT ON DISK      WHO WRITES IT                 UPDATED?
      ─────────────────────────────────────────────────────────────
      Paper-X/          /haipipe-paper enter          ✅  0.5.0
      0-lifecycle/      haipipe-paper-folder          ✅  0.5.0
        board.md/html   /haipipe-board            ③   ➖  CALLED by ①,
                        never typed (QA4)                 not typed
        S-*.md          haipipe-paper-stage           ✅  0.7.0  8 contracts
      1-probes/         haipipe-paper-probe       ⑤   ✅  0.7.0
      2-src/            haipipe-paper-compile         ✅  0.2.0
      3-dist/tex/       md2tex.py                    🟡 candidate only
      3-dist/word/      md2docx.py                   ✅ handoff export
      sections/         md2tex.py promotion          🔴 not implemented
      appendices/       md2tex.py promotion           "
      displays/         haipipe-paper-stage           (the Display stage)
        assets/         a task or discovery run       ➖  across the wall
                        haipipe-paper-draft-display   ✅  0.2.0  finds only
      <paper>.tex       haipipe-paper-scaffold        ✅  0.2.0
      <paper>.bib       NOBODY. HUMAN-ONLY.           ➖  an agent greps
      <paper>.pdf       haipipe-paper-compile          "
      <venue>.cls/bst   the venue pack                ✅  90 templates
      whole tree        haipipe-paper-conform         ✅  0.2.0  THE test
                        haipipe-paper-restructure     ✅  0.2.0  migrates in
                        haipipe-paper-lifecycle       ✅  0.4.0  the router
                        haipipe-paper-diffpdf         ✅  0.2.0

      THE SPEC ITSELF   2-phase/REF/paper-folder-anatomy.md   ✅ rewritten
        its old "0- means manuscript source of truth" table said the
        OPPOSITE of the delete test. That table is why the family
        drifted; it is now the delete-test table.
```

```
   ── WHAT THE FOUR ✅ ARE, and why conform went first ───────────────

      conform 0.2.0       the delete test stopped being a convention
        the AUDITOR       and became block J of check_structure.sh:
                          resolve every \input · \includegraphics ·
                          \bibliography a master reaches, assert none
                          sits behind a number. Block D checks board
                          purity + one family one folder. 141 → 250 ln.

      folder 0.5.0        Board-first and minimal: README, .gitignore,
        DAY 0             0-lifecycle/ with board.md + ONE Seed page.
                          No STATUS.md. No 0-displays/. No empty tree.

      scaffold 0.2.0      reframed as THE MANUSCRIPT UPGRADE, not paper
        THE UPGRADE       creation. Its SIX TEMPLATES were rewritten,
                          not just its prose: driver, supplementary,
                          sections-README, wrapper, leaf, compile.sh.

      restructure 0.2.0   was migrating papers INTO the shape this rule
        THE MIGRATION     forbids, which made it the most harmful one
                          to leave stale. Now inverted, and the delete
                          test is a THIRD gate beside prose parity and
                          compile parity.

   ── conform first was deliberate ──────────────────────────────────
      It is READ-ONLY, so it could not break anything, and once it is
      correct it is the pass/fail test the other three are written
      against. Before it, nothing could tell you a folder was right,
      and the old version FAILED a folder that was.

      $ conform/scripts/check_structure.sh <paper>
      on the 260726 migration baseline:
                          exit 1 · 56 findings · 18 delete-test
```

```
   ── never created in advance ──────────────────────────────────────
      ✗ a request file · a Handoff sidecar · a generic section stub
      ✗ an empty stage tree · a page for a unit nobody has asked for

   ── the manuscript upgrade, at the Display or section frontier ────
      the venue shell, sections/, the .bib, the driver .tex and 2-src/
      arrive TOGETHER. A paper that never reaches Display never grows
      a LaTeX toolchain.
```

## Content
### Four numbered work areas, with different reasons
The proposed four-area model is: `0-lifecycle/` is the authoritative Board and S-page source, `1-probes/` binds evidence, `2-src/` carries build recipes, and `3-dist/` carries derived review and handoff projections.
Under the proposal, they share one packaging property rather than one durability property: none belongs in the journal submission cut.

That distinction repairs a hidden contradiction in the old phrase "number by deletability".
The unnumbered `sections/` tree is generated and may be rebuilt, while the numbered `0-lifecycle/` tree contains the source whose loss would destroy the reviewed paper record.
If accepted, the prefix answers "does this ship to the journal?", not "may I erase this from the working repository?"

### Proposed source, candidate, and submission roles
Under the proposal, the S page is the source authority for prose, evidence bindings, and the human gate.
`3-dist/tex/` is the candidate projection: a safe place to generate and inspect LaTeX without overwriting the file currently used for submission.
The unnumbered `sections/`, `appendices/`, `displays/`, root driver, bibliography, venue files, and PDF form the submission projection that the journal receives.

Neither LaTeX tree may become an authoring source.
A coauthor change from Word or LaTeX is backported into the S page, reviewed there, and regenerated forward.

```text
PROPOSED FLOW
S page ## Content                         SOURCE AUTHORITY
       │
       ├── generate ──▶ 3-dist/tex/       CANDIDATE PROJECTION
       │                    │
       │                    ├─ structure + evidence non-regression
       │                    ├─ compile parity
       │                    └─ human diff gate
       │                              │
       │                           promote
       │                              ▼
       └──────────────────────▶ sections/ + appendices/
                                      │
                                      ▼
                              root master + root PDF
                              SUBMISSION PROJECTION

       └── export ───▶ 3-dist/word/    HANDOFF PROJECTION
                             edits return to the S page, never sideways
```

Promotion is the missing operation in the proposed model.
It would replace a named submission target only after the candidate passes its structural, evidence, compile, and human-diff gates.
It is not a second authoring direction.

### The manifest is wiring, not status
The proposed manifest lives at `2-src/projection.yaml`.
It records projection units: the S-page Content that supplies prose, the S page whose human gate permits delivery, the submission entrypoint, and the ordered files that unit writes.
It does not record whether a gate passed, what was last promoted, or which PDF is current; those are run receipts and page history, not build configuration.

```yaml
schema: haipipe.paper.projection/v1
master: Personality-Opioid-MISQ2026.tex
target_roots: [sections, appendices]
dependency_roots: [displays]
candidate_root: 3-dist/tex
units:
  main-5:
    source:
      page: 0-lifecycle/4-main/S-Main-5-empirical.md
      select: content
    gate: S-Main-5
    entry: sections/05_data_variables.tex
    outputs:
      - path: sections/05_data_variables.tex
        role: prose
  appendix-a:
    source:
      page: 0-lifecycle/5-appendix/S-Appendix-0-control.md
      select: "heading:A. Agreeableness Scoring Prompts and Rubric"
    gate: S-Appendix-A
    entry: appendices/A_llm_prompts.tex
    outputs:
      - path: appendices/A_llm_prompts.tex
        role: wrapper
        inputs:
          - appendices/A-1_annotator_prompt_template.tex
          - appendices/A-2_judge_llm_prompt_template.tex
      - path: appendices/A-1_annotator_prompt_template.tex
        role: prose
        select: "heading:<required source division>"
      - path: appendices/A-2_judge_llm_prompt_template.tex
        role: prose
        select: "heading:<required source division>"
excluded_pages:
  S-Main-Dash: lifecycle control, not manuscript prose
unreachable:
  - path: sections/05-1_data_source_cms_data.tex
    disposition: retain
    reason: legacy leaf; separate human decision required
```

- **`select: content`**
  Reads the complete `## Content` except `### Stage Record`.
- **`select: heading:<exact title>`**
  Reads one unique `###` division and its `####` paragraphs; a missing or repeated heading blocks generation.
- **`role: wrapper`**
  Contains only its listed `inputs` in that exact order and no prose.
  Its `entry` must also appear once in `outputs`; every wrapper input must name another output in the same unit.
- **Canonical paths**
  Every path is a paper-root-relative POSIX path.
  Absolute paths, `..`, symlinks that escape the paper root, duplicates after normalization, and cycles in the target-root `\input` graph block G0.
- **Unreachable disposition**
  Every existing `.tex` under a target root that the master does not reach must be listed as `retain`, `backport`, or `retire`, with a reason.
  Promotion reports the disposition but never carries it out; retirement is a separate human-approved operation.
- **Exact coverage**
  Starting from the root master's `sections/` and `appendices/` inputs, recurse only while the next file remains under a declared `target_root`.
  Every reachable target-root file belongs to exactly one projection unit, and every Main or Appendix S page appears as a source, gate, or explicit exclusion.
  Inputs that cross into `displays/`, the venue shell, bibliography, style, images, and other compile material enter the hashed dependency set; their ownership stays with Display or Venue rather than being reassigned to QA6.

### Six refusal gates before promotion
| Gate | What must be true | What blocks |
|---|---|---|
| G0 · Coverage | Target-root recursion is acyclic; every reachable target has one unit; `entry` and wrapper order are explicit; every other target-root `.tex` has a disposition | Escaping or duplicate path, missing owner, undeclared reachable file, unresolved wrapper input, unlisted orphan |
| G1 · Source | Every selector is unique and non-empty; the named gate page's `state:` begins `✅`; no selected source carries an unresolved evidence marker | Open gate page, missing source region, `{VAL:?}`, `\cite{TOADD}`, or broken citation/display/value binding |
| G2 · Candidate | Generation writes only to `3-dist/tex/<run_id>/` and produces exactly the normalized target set | Any write into the submission tree, unexpected output, nondeterministic rerun, or changed selected-Content/manifest/dependency digest |
| G3 · Evidence | Candidate citation keys, display labels, and resolved value bindings match the S page and do not silently drop bindings still present in the prior target | Comparing counts alone; any target-only binding must first be backported or deliberately removed on the S page |
| G4 · Compile | Copy the complete hashed dependency set into an isolated build root and compile the candidate master with the same shell and input order | Any fallback through `TEXINPUTS` to live `sections/`, `appendices/`, `displays/`, bibliography, class, style, or image; missing dependency; undefined citation/reference; a PDF existing by itself |
| G5 · Human promotion | The reviewer sees every target diff and evidence delta, approves an immutable check receipt, and a second promotion receipt proves the reviewed bytes became the submission bytes | Stale receipt, changed target/dependency, partial approval, post-target digest unlike candidate digest, or orphan deletion |

Promotion is transactional rather than a direct overwrite.
The checked files are staged together, the pre-check target hashes are verified again, and any failed replacement rolls the set back.
`run_id` is the SHA-256 of the canonical manifest, selected Content, and dependency-set digests; the separate candidate digest is computed after generation over normalized output paths and bytes.

The proposed runtime owner is a new callable `haipipe-paper-project` skill at `3-deliver/1-build/haipipe-paper-project/`, with `project.py generate`, `check`, and `promote`.
It calls the QC5 LaTeX adapter, the existing conform checks, and the compile skill; no such skill or executable exists yet.
`md2tex.py` remains a candidate adapter and never receives a submission-write flag.

Check and promotion receipts are separate append-only JSON records under `2-src/projection-receipts/`.
Both use SHA-256 over canonical paper-relative paths plus file bytes:

- **Check receipt**
  Records `receipt_id`, manifest digest, exact selected-Content digest, gate page ids and states, dependency-closure digest, pre-target digest, candidate digest, normalized target list, timestamp, and reviewer.
- **Promotion receipt**
  References the check receipt and, before any write, recomputes the manifest digest, selected-Content digest, every gate page's first-token `✅`, dependency-closure digest, pre-target digest, and approved candidate digest.
  Any mismatch refuses promotion.
  After the transaction it records the actual post-target digest, approver, timestamp, and success or rollback.
- **Hash scope**
  The source digest covers only the exact selected Content regions, not page frontmatter or `## Log`, so appending a receipt pointer does not invalidate the reviewed source.
  The post-target digest must equal the candidate digest over the same normalized target paths.
- **Page history**
  Each affected S page receives `[PROMOTE] check=<id> promote=<id> pre=<digest> post=<digest> approver=<who>` in `## Log`; the full records remain in `2-src/projection-receipts/`.
  Neither the manifest nor a shared status file stores a mutable "current" pointer.

### What the MISQ manifest would expose immediately
The root master reaches 9 section entrypoints, exactly the manuscript sources `S-Main-0` through `S-Main-8`; `S-Main-Dash` is control and must be explicitly excluded.
Five other section files are unreachable orphans: the three `05-*` leaves and two `06-*` leaves.

The master reaches 6 appendix entrypoints plus 5 nested leaves, for 11 reachable appendix files gated by `S-Appendix-A` through `S-Appendix-F`.
Three appendix files are unreachable orphans: `B-1_alternative_overprescription_thresholds.tex`, `B_robustness_tables.tex`, and `D_extended_literature_review.tex`.

The six A through F pages are gate pages: all are `🔴 OPEN` and their Content carries only `Stage Record` plus `Appendix scope`.
The substantive A through F prose is centralized on `S-Appendix-0`, so that page is a source rather than an exclusion.
Its divisions still do not contain every prompt/table leaf verbatim, which means a truthful selector cannot yet cover all 11 targets.
G1 therefore fails on both the open unit gates and incomplete leaf-source coverage.

### Why the current candidate cannot be promoted yet
The current `md2tex.py` correctly defaults to `3-dist/tex/`, but its declared `--into-sections` option is unused and should be removed rather than turned into a direct-overwrite shortcut.
It writes S-page filenames such as `S-Main-5-empirical.tex`, while the submission tree uses venue-facing entrypoint names.
It does not read a manifest, distinguish delivery pages from control pages, compute the master's reachable target set, or produce a promotion receipt.
The generated candidate PDF is 47 pages while the current submission PDF is 46 pages, which proves that a successful compile is not parity.

Generation and promotion should remain separate commands.
`md2tex.py` owns the QC5 conversion into a candidate; the proposed `haipipe-paper-project` runtime consumes the manifest and passed receipt.
No `--into-sections` generation mode is needed.

### One family, one folder
Inside `0-lifecycle/`, the folder name IS the S family name: SEVEN families, and eight folders. The mismatch is deliberate and is not yet resolved. `Round` was ruled a family on 260726 and the board tooling never learned it: `FAMILIES` in `haipipe-board/stage.py:25` is seven names, `resolve_filename("Round", …)` raises, and the live paper's `7-round/` holds only `_archive/` with zero `S-Round` pages. So the eighth folder exists and its family does not. Before 260726 the folders carried the old STAGE order and the two disagreed badly. `Work` was split across `1a-resource/` and `1b-claims/`, `Venue` across three, and `5-section-edit/` held Main, Appendix and Submission at once while Submission was also split with `6-submission/`. Nine folders, eight families, and not one clean mapping.

A reader can now place a page from its name alone: `S-Main-6-results.md` is in `4-main/`, and nothing else could be.

The eight families are not the eight stages, and the folders are named for the families. Which stage fills which folder, and what each one asks:
```
 STAGE            asks                                     ──▶ FAMILY      FOLDER
 0-seed           why might this paper exist?                  Seed 0      0-seed/
 1a-resource      does the evidence EXIST, and can it
                  CARRY a claim?                               Work 0      1-work/
 1b-claims        supported, weak, or GAP?                     Work 1        "
 2a-venue         which outlet, and what does it demand?       Venue 0     2-venue/
 2b-pitch         what is it selling, in one minute?           Venue 1       "
 3-narrative      how do claims become a manuscript arc?       Venue 2       "
 4-display        what figure or table carries each claim?     Display 0   3-display/
 5-section-edit   does each section's prose do its job?        Main <n>    4-main/
                                                               Appendix <A> 5-appendix/
 ──────────────────────────────────────────────────────────────────────────────────
 (no stage)                                                    Submission  6-submission/
 (no stage)     ⚠️ RULED a family 260726, NOT in FAMILIES     Round       7-round/
                    resolve_filename("Round", …) raises; 0 live pages
```
Three stages fill Venue, two fill Work, one fills either Main or Appendix depending on the section, and two families are filled by no stage at all. So the folder tree answers "where do I read this" and says nothing about what produced it. `QB2b` owns that seam; what a stage IS as an object is `QB1`.

A stage also declares whether it SURVIVES a change of journal, and that split is a fact about the stage set rather than about any one stage:
```
── venue_aligned:   free | aligned | venue_role ──────────────────
      TEST   could a different journal change this stage's ANSWER?

      venue-FREE                       survives a retarget untouched
      ┌──────────────────────────────────────────────┐
      │ 0-seed        why might this exist            │
      │ 1a-resource   does it exist, does it carry    │  THE SCIENCE
      │ 1b-claims     supported / weak / GAP          │
      └──────────────────────────────────────────────┘
                          │
                     2a-venue   ◄── THE PIN, `venue_role`,
                          │          neither free nor aligned
      ┌──────────────────────────────────────────────┐
      │ 2b-pitch      what it sells, to whom          │
      │ 3-narrative   reveal order, section list      │  THE TELLING
      │ 4-display     display budget, conventions     │
      │ 5-section-edit house style, citation density  │
      └──────────────────────────────────────────────┘
      venue-ALIGNED                      rewritten on retarget

      ⚖️ the line falls between what is TRUE and how it is TOLD.
         A claim's status does not change because a different editor
         reads it. A narrative's ORDER does.

   ── the case that hurts, and still lands aligned ──────────────────
      MISQ ──rejected──▶ another outlet
        evidence   KEPT         every claim, number and probe entry
        figures    MOSTLY LOST  limits and conventions differ
      expensive, and still right: a figure is an argument made FOR a
      venue, not a fact about the world.

   ── WHO READS THESE FIELDS, AND HOW THEY FAIL ────────────────────
      fields   runs · venue_aligned · unit · units · units_from
      reader   ③ THE EXECUTOR · an agent, reading prose        → QB1
      fails    🔇 SILENT. display declares `runs: once` over eleven
               independently gated units and nothing has ever raised.
      to bind  ✅ THIS ONE IS CHECKABLE, cheaply: a stage that declares
               `units:` must declare `runs: per-unit`. `4-display`
               declares the first and not the second, which is the whole
               defect, expressible as one assertion.
```
Evidence is venue-free. A retarget may rewrite how a paper is told and may not reopen what it found. What retargeting concretely does to each aligned stage has never been run end to end, so it is design rather than practice.

The set of stages is OPEN, and deliberately so. Adding one costs a row in `stages/index.yml`, a folder, and two files: no new skill, no version bump. Compiling, submitting and answering reviewers all sit outside the eight today and none of those exclusions was ever argued in writing, so if one should become a stage the argument is available rather than blocked. Rounds went the other way on 260726: ruled a family rather than a stage, so `7-round/` exists outside the stage contracts. The live folder still has only `_archive/` and zero `S-Round` pages because the family remains unimplemented.

The folder is also PURE. Every file in it is an S page or the board's own index, never a `.tex`, an asset or a scratch note. The moment something else lands there the board stops being a control plane and becomes a folder that happens to contain some pages.

### What crosses this folder's edge
```
 ① ──▶ ⑦   IN, and only through a stage run. The paper CONSUMES the
           settled contract and never stores a copy: no SKILL.md, no
           stage contract, no venue pack is ever copied in.

 ⑧ ──▶ ⑦   IN, by generation. 0-lifecycle/ is INSIDE this folder and is
           where the real Content lives. sections/ and appendices/ are
           produced FROM those pages. One direction, md to tex, never back.

 ⑦ ──▶ the wall   OUT. 1-probes/ holds one entry per question this paper
           cannot answer, bound BY PATH to a QA file in tasks/ or
           discoveries/. The paper asks; it never computes.

 ⑦ ──▶ ②   NOTHING. A paper never writes to a design board.
```
Almost nothing here is authored in place. The prose arrives from `⑧`, the numbers and citations across the wall, the LaTeX is generated. What this folder genuinely owns is the SHAPE: which containers exist, and which are allowed to be empty.

## Items to Finish
- [ ] 🗃 `.board-refs.bbl` is machinery sitting in the unnumbered half
      `refs.py` writes it into the paper root: the rendered bibliography a citation chip's panel prints, 62 KB on MISQ.
      A journal does not receive it, so the proposed submission-cut rule places it behind a numbered path, probably under `2-src/`.
      Dot-prefixed so face discovery skips it, and it should be in the paper's `.gitignore` either way.
      Filed rather than moved because changing its home means changing `refs.py` and a real paper folder.
- [x] 🌱 Choose a minimal scaffold
      A new paper receives no speculative LaTeX, no section stubs, and no page for a unit nobody has asked for.
- [x] 🧭 Make the scaffold Board-first
      `0-lifecycle/board.md` and one Seed page make a new paper runnable immediately.
- [ ] 🔢 Rule the prefix as a submission-cut boundary and admit or reject `3-dist/`
      The proposal is that every numbered path stays out of the journal package, while the unnumbered tree compiles and submits alone.
      This replaces "safe to delete" with "excluded from the submission cut", because `0-lifecycle/` is numbered and authoritative while `sections/` is unnumbered and generated.
      The live `3-dist/` satisfies the proposed rule, but the fourth numbered folder is not settled until JL accepts this replacement.
- [x] 🧾 Design the projection manifest contract
      Proposed at `2-src/projection.yaml`: target and dependency roots, source selector, separate gate page, entrypoint, ordered wrapper inputs, outputs, excluded pages, and explicit orphan disposition.
      Only the recursive `sections/` and `appendices/` target closure is page-owned; Display and venue dependencies retain their own owners and enter the compile hash set.
- [ ] 🗺 Populate and validate the MISQ manifest
      Map 9 Main entrypoints and 11 reachable Appendix files, exclude `S-Main-Dash`, and assign `retain`, `backport`, or `retire` to the 5 section plus 3 appendix orphans without acting on them.
      `S-Appendix-0` supplies centralized A through F source divisions; the six unit pages supply the human gates.
      All six gates are open, and some prompt/table leaf bytes still lack an exact source selector.
- [x] 🚦 Design the candidate-to-submission gate sequence
      G0 coverage, G1 source, G2 isolated candidate, G3 evidence non-regression, G4 compile, and G5 human transactional promotion.
      G4 hashes and copies external dependencies so candidate compile cannot fall back to the live paper root; page-count difference is review evidence rather than a mechanical veto.
- [ ] 🔧 Separate generation from promotion
      Remove the unused `--into-sections` flag from `md2tex.py`.
      Candidate generation stays in QC5; create the proposed `haipipe-paper-project` runtime with separate generate, check, and promote actions and two append-only receipts.
- [ ] 🧪 Exercise the one gated Main page without promoting it
      Generate, check, compile, and render the full target diff for `S-Main-1-introduction.md`, the only current Main page whose state begins `✅`.
      Stop before submission replacement; the first run tests the contract, not the manuscript.
- [x] 🗂 One family, one folder
      Seven S families with a folder each, plus `7-round/` whose family is declared and unimplemented; 40 pages migrated on the MISQ paper with none lost.
- [ ] 🔧 Make `Round` a family, or rule that it is not one
      It was ruled one on 260726 and `FAMILIES` in `haipipe-board/stage.py:25` still lists seven, so `resolve_filename("Round", …)` raises and `7-round/` cannot receive a named page. Either add it there and in `check-contracts.py:40`, or say rounds are a folder with a different naming rule and stop calling them a family.
- [x] 🖼 Delete `figures/` from the layout
      It predates display units. The MISQ migration moved its 5 orphan PNGs, which no `\includegraphics` in the paper points at, into `_archive/figures-orphan/`; every real graphic already sits in a unit's `assets/`. A second active home for the same thing is the defect this face forbids elsewhere.
- [x] ✂️ The venue split is stated
      `PHILOSOPHY.md` and the per-stage `venue_aligned:` field, with `venue_role` for the pin itself.
- [ ] 📐 Define what retargeting does to each aligned stage
      Rewrite from scratch, or re-derive while keeping the argument. Different operations; the contracts do not distinguish them.
- [ ] 🧠 Rule whether a retarget reopens the claims stage
      It should not, by this design. Say so explicitly, because the temptation at a new venue is to re-cut the claims to fit.

- [ ] ✂️ Rule where a display unit's working half lives
      2 of a unit's 8 members ship: `float.tex` and `assets/`. `README.md`, `preview.tex`, `preview.pdf`, `source/`, `candidates/` and `versions/` never do, so `displays/` fails the delete test as it stands. See Discussion.
- [x] 🛠 Teach the four BUILD skills this layout
      Done 260726. `conform` 0.2.0 was rewritten around the delete test as an executable check (block J) plus board purity (block D); at the pre-migration baseline it failed the MISQ paper with 56 findings. `folder` 0.5.0 scaffolds Board-first with one runnable Seed page and creates no `STATUS.md`. `scaffold` 0.2.0 reframed as the manuscript upgrade, with its six templates rewritten, not just its prose. `restructure` 0.2.0 migrates INTO the new shape and gained the delete test as a third non-negotiable gate.
- [x] 🧹 Align the remaining skills with this layout
      Done 260726, in four phases ordered by BINDING rather than by mention count. ① `haipipe-paper-stage` 0.7.0: eight `stages/*/stage.md` contracts, whose `artifact:`/`probes:`/`units:`/`output:` resolve at run time, so a stale one does not read wrong, it WRITES to the wrong place. ② `haipipe-paper-enter` 0.5.0, the console. ③ `haipipe-paper-lifecycle` 0.4.0, the router. ④ the tail: `probe` 0.7.0, `draft-display` 0.2.0, `diffpdf` 0.2.0, `compile` 0.2.0, `revise` 0.2.0.
      Two things the plan had not counted, both found by measuring directories instead of `SKILL.md`: `2-phase/REF/paper-folder-anatomy.md`, the shared spec every build skill cites, whose prefix table asserted the OPPOSITE rule and is the reason the family drifted; and 90 venue templates carrying one identical stale line.
- [x] 📍 Rule STATUS.md out of existence
      Adopted 260726 on JL's proposal, with the Gate Ledger landing in each S page's `## Log`, one row on the page whose gate it was. That was the only blocker: it is the one part of the file that is history and cannot be re-derived. `current_layer`/`maturity` are derived from disk; the `venue:` pin moved to `S-Venue-0-venue.md` frontmatter. `folder` no longer creates the file, `conform` warns when one exists, `restructure` migrates its rows out before removing it, and `DRIFT` was retired with it: it named the gap between a stored frontier and disk, and there is no stored frontier. What replaced it is narrower and real, `STALE`, an S page whose own `state:` over-claims about itself.
- [x] 🧨 Make the MISQ paper pass its own test
      Done 260726 with `restructure` 0.2.0. Block J now reads `✓ nothing the deliverable needs sits behind a number`, and the test was also run for real on a copy: `rm -rf 0-* 1-* 2-*` then a four-pass compile produces the PDF. All three gates passed: prose parity byte-identical once path-bearing lines are excluded, compile parity 42 pages to 42 pages, delete test green. 56 findings to 47, and the 18 delete-test failures to zero. What the other 47 are is in Where we are; none of them is this item.
- [ ] 🧪 Create one paper and enter it
      A fresh agent should open its Board and work Seed without adding or guessing another control file.

## Where we are
The 260726 layout was implemented on the MISQ paper, but the later arrival of `3-dist/` reopens its fixed count and exposes that "numbered means deletable" conflated packaging with authority.
The paper now has four numbered work areas: `0-lifecycle/`, `1-probes/`, `2-src/`, and `3-dist/`.
The proposed replacement is a submission-cut rule: numbered paths do not ship to the journal, while the unnumbered projection must compile and submit alone.

The rule also gained a machine check on 260726. The four `1-build/` skills were rewritten, and `haipipe-paper-conform` 0.2.0 turned the delete test from a convention into block J: it resolves every `\input`, `\includegraphics` and `\bibliography` target a master reaches and asserts none sits behind a number. At the pre-migration baseline, the MISQ paper exited 1 with 56 findings, 18 of them delete-test failures including the driver `.tex` and the `.bib`. The current result is recorded below.

The rest of the family has now been told too. Twelve skills were aligned on 260726, ordered by binding rather than by mention count: the eight stage contracts first, then the console, the router, and the tail. With them went the two things a `SKILL.md`-only count had missed: `2-phase/REF/paper-folder-anatomy.md`, the shared spec every build skill cites, whose prefix table asserted the opposite rule and is the reason the family drifted at all; and 90 venue templates carrying one identical stale line.

The paper was migrated on 260726 before `3-dist/` existed.
That migration unnumbered the driver, bibliography, PDF, `sections/`, `appendices/`, and `displays/`; moved build recipes into `2-src/`; archived the obsolete loose assets; and placed lifecycle history on its owning S pages.
The later exporters added `3-dist/tex/` and `3-dist/word/` without revisiting this page, which is why the on-disk tree and the three-folder Law diverged.

`STATUS.md` closed on the way, which is why that ruling is now `[x]`. The Gate Ledger was the only blocker and it landed exactly where this page proposed: seed and the seed re-run on `S-Seed-0`, pitch on `S-Venue-1`, claims on `S-Work-1`, narrative on `S-Venue-2`, display on `S-Display-0`, and the three rows belonging to no single page on `S-Venue-3` alongside the Restart Note and the display-directory note. The 2026-07-20 `> CHECK` block travelled with them, intact, annotated as dissolved rather than answered: both horns of its question were about which stored frontier to trust, and there is no longer one.

The current conform run reports 47 findings: 34 errors and 13 warnings, with block J green and zero delete-test failures.
Four errors belong to board purity and five to broken display targets; the other section, display, and formatting findings are owned outside this prefix decision.
This page does not freeze their finer breakdown because the checker output is the current source of truth.

The proposed model removes the false `sections/` versus `3-dist/tex/` authority choice.
Under it, the S page is the source authority, `3-dist/tex/` is a candidate projection, and the unnumbered tree is the submission projection.
JL confirmed that this is the Paper skill Board and asked for the design to continue.
That instruction produced a concrete manifest schema and six refusal gates; it did not authorize a submission-tree overwrite.

The live master-reachable set is now measured rather than inferred from folder counts: 9 section entrypoints and 11 appendix files.
Five section files and three appendix files are unreachable orphans.
`S-Appendix-0` centralizes the A through F source divisions while the six unit pages own the human gates and list their target files.
All six unit gates are open, and the centralized source still lacks exact selectors for some prompt/table leaves, so the proposed G1 gate would stop every Appendix promotion today.

The model remains proposed until JL accepts its prefix and three-role rulings.
Implementation remains blocked behind that acceptance, creation of the proposed runtime, a populated MISQ manifest, and one candidate-only trial.

The display unit's working half remains a separate open split.
Because `displays/` is inside the unnumbered submission tree, its six non-shipping members still travel with the two files the journal needs.

## Files
- `3-deliver/1-build/haipipe-paper-conform/scripts/check_structure.sh`
  THE machine test for this face. Blocks A to K; block J is the delete test, block D is board purity and one-family-one-folder. Exit 0 conforms, 1 findings, 2 not a paper folder.
- `3-deliver/1-build/`
  The other three: `haipipe-paper-folder` (Board-first minimal scaffold), `-scaffold` (the manuscript upgrade), `-restructure` (migrate an existing paper in). All four rewritten 260726.
- `0-enter/haipipe-paper-enter/SKILL.md`
  The entry path that creates and opens the initial board; 9 old-layout mentions, the second-worst.
- `1-lifecycle/haipipe-paper-lifecycle/SKILL.md`
  The router that names paths on the way through; 6 mentions.
- `README.md`
  The family map, which still describes the older complete-folder shape.
- `3-deliver/4-ship/haipipe-paper-to-word/md2tex.py`
  Generates the current candidate projection in `3-dist/tex/`; declares but does not implement `--into-sections`, which this design proposes removing.
- `QC-the-sentence-with-evidence-card/QC5-sentence-to-latex.md`
  Owns conversion semantics and evidence extraction; QA6 owns only where candidates land and how they may be promoted.
- `2-src/projection.yaml`
  Proposed manifest location; the file does not exist yet.
- `2-src/projection-receipts/`
  Proposed append-only check and promotion receipt location; the directory does not exist yet.
- `3-deliver/1-build/haipipe-paper-project/`
  Proposed runtime owner for generate, check, and promote; no skill or executable exists yet.
- `examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/`
  The measured tree: four numbered work areas, 9 reachable section entrypoints, 11 reachable appendix files, 8 unreachable `.tex` files, and PDFs of 47 and 46 pages.

## Law
The 260726 packaging test remains the last accepted rule: on a copy, removing `0-*`, `1-*`, and `2-*` must leave a paper that compiles and submits.
That copy-only test is not permission to erase the working repository.

The later `3-dist/` addition makes the old "three and only three" count stale.
Until JL rules the replacement in Items, neither the proposed submission-cut interpretation nor the proposed three-role projection model is Law, and no candidate may be promoted into `sections/` or `appendices/`.

`displays/` is the ONLY home of an asset, one folder per unit. There is no top-level `figures/` and no `Figure/` or `Table/` bucket: a display is a unit, and its render lives inside it.

Inside `0-lifecycle/`, one family one folder, and the folder holds S pages and its own index and nothing else.

A new paper is created Board-first and minimal, and every other page is absent until its unit is allocated. No request file, sidecar, section stub or empty stage tree is created in advance. Manuscript machinery is an upgrade performed at the Display or section frontier, never at creation.

Every stage declares exactly one of venue-free or venue-aligned, decided by whether a different journal could change its answer. The venue stage itself declares `venue_role`, because it is the stage that picks the venue and is therefore neither. Evidence is venue-free: a retarget may rewrite how a paper is told and may not reopen what it found.

## Discussion
> JL 260729: confirmed that this work is on the Paper skill Board and asked CC to continue the design.
> CC: treated that as authorization to design the manifest and gates, not as permission to promote files or as a final acceptance receipt for the proposed prefix and three-role model.

> CC 260729: `sections/` and `3-dist/tex/` should not compete for source authority.
> The S page is the only authored and gated source; `3-dist/tex/` is a candidate projection; the unnumbered LaTeX tree is the journal submission projection.
> The missing design is promotion: an explicit page-to-target manifest plus structural, evidence, compile, and human-diff gates.
> This also changes the prefix explanation from "safe to delete" to "excluded from the submission cut", because the numbered `0-lifecycle/` is authoritative and the unnumbered `sections/` is generated.

> JL 260726: things like 0, 1, 2 are the things we can delete when we want to submit.
> CC: adopted as the delete test, and it is checkable rather than a convention.

> CC 260726: one case does not fit and I have not resolved it. A display UNIT holds both halves, and the split is 2 of 8: `float.tex` and `assets/` ship; `README.md`, `preview.tex`, `preview.pdf`, `source/`, `candidates/` and `versions/` never do. Today they sit in one folder, so the delete test cannot be run on `displays/` without losing what a journal needs.
> Three ways out, none ruled: put the working six under `displays/<unit>/_work/`; or move them to `2-src/displays/<unit>/`; or accept the straddle and state that `displays/` is the one folder the test does not apply to. The first keeps a unit together and is what I would try first.

> JL 260726: we might not need STATUS.md and not need the status strip any more.
> CC: I agree on the file, and the case is stronger than a preference. Three arguments, in order of weight.
> ONE, the console already stopped reading it. `haipipe-paper-enter` describes itself as a derive-from-disk dashboard and says so explicitly at its own line 289: a strip glyph is "the strip's artifact-on-disk test, not a frontier claim". The stage strip was designed in the 260622 feedback around "single source of truth = STATUS.md `current_layer`" with the stated precondition that "a stale current_layer = a lying strip". That design has already been abandoned in place; the file is what is left of it.
> TWO, it is now the third answer to "where is this paper", after the S pages' `state:` and the disk. `QA7` forbids exactly that.
> THREE, the MISQ file is a live demonstration. It disagrees with itself in three directions at once: `current_layer: section-edit`, a Restart Note saying the frontier reset to `0-seed`, and a Gate Ledger showing five stages confirmed. It carries a 12-line CHECK note from 260720 asking a human to rule on its own self-contradiction. That note is not a bug in the file; it is what a stored frontier costs.
> The one thing genuinely NOT derivable is the Gate Ledger: who confirmed which gate, when, and why. History cannot be read off current disk state. It belongs in each S page's `## Log`, one row on the page whose gate it was, which is also where a reader is already standing when they want it.
> On the strip I would separate two things. Deleting the stored `current_layer` it was designed to read: yes, and it already does not read it. Deleting the strip itself: that is a different question about how a reply closes, not about this folder, and it belongs on `QA7` or `QA2` rather than here.

## Log
260729 2132 · Closed the final two cold-read precision gaps. Promotion now recomputes manifest, selected Content, every gate state, dependencies, pre-target bytes, and approved candidate bytes before writing, so a changed source or gate makes the check receipt stale rather than merely a changed target. QC5's introduction citation count was corrected from a raw-Content 29 to 16 prose calls; the larger count included apparatus and one unresolved marker.

260729 2124 · Fresh review refined the executable contract. Target ownership now stops at the recursive `sections/` and `appendices/` closure; Display and venue files remain external owners inside a hashed compile-dependency set. Projection units now separate source page from gate page, which corrected Appendix ownership: `S-Appendix-0` centralizes the prose while A through F are open unit gates. Added normalized-path and cycle refusal, ordered wrapper inputs, explicit orphan dispositions, isolated compile with no live-root fallback, separate check and promotion receipts with exact hash scopes, and proposed `haipipe-paper-project` as the callable runtime. QC5's restored citations and archived Display buckets were also synchronized. No runtime or paper artifact was created.

260729 2104 · Designed the first executable boundary without implementing it. Proposed `2-src/projection.yaml` as a pure wiring manifest, measured the target-root closure at 9 section entrypoints plus 11 appendix files, and identified 5 section plus 3 appendix orphans. Added G0 coverage, G1 source, G2 candidate, G3 evidence, G4 compile, and G5 human transactional promotion. Initially treated the six A through F scope pages as the missing prose sources; the 2124 entry corrects that premise against the substantive Content on `S-Appendix-0`. Recommended removing the unused direct-overwrite flag and keeping generation separate from promotion; no manifest, command, paper file, or submission target was created or changed.

260729 2020 · Reopened the fixed three-folder Law against the live `3-dist/` tree and designed the three-role projection model. The S page is source authority, `3-dist/tex/` is a candidate, and the unnumbered tree is the submission projection. Counted 10 Main pages against 14 section files on disk and 7 Appendix pages against 14 appendix files without yet resolving master reachability; the 2104 entry above refines that count. Measured a 47-page candidate against a 46-page submission PDF and filed the preliminary four-gate path; no file was promoted or moved.

260726 · The MISQ paper migrated, on JL's go, and this face's last blocking item closed. Three gates, all green: prose parity byte-identical, compile parity 42 pages to 42, and the delete test run for real on a copy rather than only asserted by block J. Two defects surfaced by doing the work rather than by reading anything. `haipipe-paper-scaffold`'s `compile.sh.tpl` was rewritten for `2-src/` but still discovered its master with `ls 0-*.tex`, so the one script a migrated paper installs could never find that paper's driver: it now takes the unnumbered top-level `.tex` carrying `\documentclass`. And the block that does it crashed on macOS, because bash 3.2 mis-parses a `case` pattern's `)` inside a process substitution; it is a plain loop now. Two decisions were deliberately NOT taken here: the flat buckets under `displays/` are a content promotion rather than a rename, and the board-purity findings are `QB2b`'s.

260726 · Rounds moved inside the lifecycle as an eighth family, one page per round. Folders renumbered to one-family-one-folder; 40 pages migrated with none lost. Numbered-versus-unnumbered adopted as the delete test on JL's ask. Page then rewritten clean: three Content divisions instead of seven, with the scaffold, the absent-until-allocated list and the upgrade point living in the Diagram rather than being restated beneath it.

260726 · The alignment ran, on JL's go, in the four phases the Diagram had set out. Twelve skills, plus the shared anatomy spec and 90 venue templates. Two rulings were settled on the way rather than deferred. The Gate Ledger landed in each S page's `## Log`, which unblocked retiring `STATUS.md` entirely; that in turn retired `DRIFT`, which had only ever named the gap between a stored frontier and the disk. And the venue pin moved into `S-Venue-0-venue.md` frontmatter, so one page owns the venue contract. The `0-seed` contract's four-line loopback warning was deleted rather than reworded: it existed to stop a re-run demoting a stored `current_layer`, and with nothing stored there is nothing to demote.

260726 · JL asked the Diagram to say which skills this rule changes and whether they are done. `WHO WRITES WHAT` gained an UPDATED column with per-skill counts, split into old-path debt and `STATUS.md` debt, and a second block saying what each of the four rewrites actually was. The measurement moved the priority: `haipipe-paper-stage` (22 old-path, 12 `STATUS.md`, across eight run-time stage contracts) is worse than `enter`, which the earlier `SKILL.md`-only count had put first.

260726 · The four `1-build/` skills rewritten against this face, on JL's go. `conform` 0.2.0 is the one that matters: the delete test stopped being a convention and became block J of `check_structure.sh`, which resolves every target a master reaches and asserts none sits behind a number. It fails the MISQ paper with 56 findings. `folder` 0.5.0, `scaffold` 0.2.0 (six templates rewritten, not just prose) and `restructure` 0.2.0 followed. `conform` first was deliberate: it is read-only, so it could not break anything, and once correct it is the pass/fail check the other three are written against.

260726 · JL asked what separates `displays/` from `figures/`. Nothing does, and that was an error in this diagram carried over from the pre-unit npjDM2025 layout: `figures/` on the MISQ paper holds 5 orphan PNGs no `\includegraphics` points at. `figures/` deleted from the layout, and the unit expanded to show its real 8 members and which 2 ship. Same turn, JL proposed retiring `STATUS.md` and the stage strip; the argument and the one blocker are in Discussion.

260726 · JL asked which skills this face is about, so the Diagram gained a WHO WRITES WHAT block: one author per line of the tree. Writing it exposed the real gap. The ruling was assumed to be one stale skill (`haipipe-paper-folder`); measuring found 15 `SKILL.md` carrying 63 old-layout mentions, all four `1-build/` skills among them, and the MISQ paper's own top level still failing the delete test. Items and Where we are rewritten against those counts.

260727 · Corrected a ruling reported as a fact. This face said eight families and eight folders; the board tooling knows seven. `Round` was ruled a family on 260726 and `FAMILIES` in `haipipe-board/stage.py:25` was never updated, so `resolve_filename("Round", …)` raises and the live `7-round/` holds only `_archive/`. Found while a subagent re-verified `QB2b`'s addressing claims against the code rather than against this page.
