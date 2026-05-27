---
name: haipipe-paper-create
description: "Create a fresh LaTeX paper paragraph-by-paragraph from an existing narrative + plan. Scaffolds the tex root from a venue template, walks the planned sections, and drafts each paragraph through interactive author discussion. Every paragraph is written with paper-weaving's marker convention (PN.SN headers) so the resulting draft is immediately polishable by /haipipe-paper-revise without a marker-insertion pass. Called by /haipipe-paper orchestrator. Direct invocation works for whole-paper drafting. Trigger: create paper, write tex from plan, draft paper paragraph by paragraph, scaffold paper, new paper from narrative, 写论文初稿, /haipipe-paper-create."
argument-hint: [plan-or-narrative-path] [--venue <v>] [--out <dir>]
allowed-tools: Bash, Read, Grep, Glob, Write, Edit, AskUserQuestion, Skill
---

Skill: haipipe-paper-create (workflow specialist)
=================================================

Drive the **first draft** of a paper from an existing narrative + plan,
section-by-section and paragraph-by-paragraph. Venue-agnostic at the
workflow level — venue only picks the LaTeX template and section budget.

Hand-off contract: every paragraph this skill writes carries the
`%% ---- PN.SN ----` markers that `paper-weaving` (the per-file revision
engine) expects. So once a section is drafted, `/haipipe-paper-revise`
can polish it without any marker-insertion pass.

This skill does NOT generate the narrative or the plan. It assumes both
exist (or routes back to the upstream skills if not).

Usage
-----

```
/haipipe-paper-create <plan-dir-or-NARRATIVE_REPORT.md>
/haipipe-paper-create <plan-dir> --venue iclr --out paper/
/haipipe-paper-create <plan-dir> --section intro      (single section only)
/haipipe-paper-create <plan-dir> --resume             (continue prior session)
```

Examples
```
/haipipe-paper-create 1-narrative/NARRATIVE_REPORT.md --venue neurips
/haipipe-paper-create papers/lhm-a/  --venue iclr  --out papers/lhm-a/draft/
/haipipe-paper-create papers/lhm-a/  --section method
```

Lifecycle Position
------------------

```
1-narrative  →  2-plan  →  ┌──────────────────┐  →  haipipe-paper-revise → 5-review → ...
                          │ haipipe-paper-    │       (paper-weaving runs
                          │   create (HERE)   │        per-section: G1 → Q → G2)
                          └──────────────────┘
```

The drafting hop. Reads the contracts produced upstream, emits a
compileable tex tree, every paragraph written in paper-weaving's
marker convention.

Required Inputs
---------------

1. **narrative-report**  — `NARRATIVE_REPORT.md` (from `1-narrative/narrative-report`)
2. **paper plan**         — `PAPER_PLAN.md` / `PAPER_ARCHITECTURE.md` (from `2-plan/`)
3. **venue**              — `iclr | neurips | icml | nature | pnas | misq | isr | …`

If any are missing, **pause and route back**:
- no narrative → `Skill("narrative-report")`
- no plan      → `Skill("paper-plan")` or `Skill("paper-architecture")`
- no venue     → `AskUserQuestion`

Constants
---------

- **CREATE_DIR** = `create/`  (state + per-section drafting log)
- **OUT_DIR**    = `--out` if given, else `draft/`
- **PARAGRAPH_GATE** = `true`  — every paragraph confirmed via `AskUserQuestion` before write
- **MAX_PARAGRAPH_RETRIES** = 3
- **AUTO_COMPILE** = `false`  — skip Phase 5 compile unless requested
- **MARKER_CONVENTION** = `paper-weaving`  — every paragraph carries `%% ---- PN.SN ----`

Workflow
--------

### Phase 0: Resume or Initialize

1. If `CREATE_DIR/CREATE_STATE.md` exists and `--resume` (or fresh state
   shows incomplete sections) → load state, skip to next pending phase.
2. Otherwise → create `CREATE_DIR/`, initialize `CREATE_STATE.md`
   (paper title, venue, plan path, narrative path, section list).

### Phase 1: Load Contracts

1. Read narrative-report → extract: claim, story arc, evidence chain
2. Read plan → extract: section list, per-section budget, figure anchors
3. Read venue template → identify the canonical section order and limits
4. Emit `CREATE_DIR/PAPER_CONTRACT.md` — single-page summary the
   per-paragraph drafting will keep referencing

If contracts disagree (plan says 5 sections but narrative implies 6),
**stop and ask**.

### Phase 2: Scaffold Tex Root

1. Resolve venue template (see Venue Map below)
2. Copy the template into `OUT_DIR/`:
   - `0-<paper>.tex`     master shell
   - `0-<paper>.bib`     empty bib (or carry over if found)
   - `0-sections/`       one stub `.tex` per planned section
   - `0-display/{Figure,Table,AppendixFigure,AppendixTable}/`
3. Emit `OUT_DIR/1-config.yaml` and `OUT_DIR/1-compile.sh` if the venue
   template defines them
4. Record scaffold paths in `CREATE_STATE.md`

If `OUT_DIR/` already has tex files, **stop** — do not overwrite. Ask
the user whether to (a) point `haipipe-paper-revise` at them instead,
(b) write to a sibling dir, or (c) explicitly `--force`.

### Phase 3: Section Loop — paragraph-by-paragraph drafting

For each section in plan order (or only `--section <name>` if given):

1. Mark `CREATE_DIR/SECTION_BOARD.md` row as `in_progress`
2. Load the per-section playbook:
   ```
   Skill("section-<name>")   # e.g. section-intro, section-method
   ```
   (Read-only: pulls in the structural template for this section type.)
3. Read the section's slot in the plan → extract the paragraph budget
   (often: "intro: P1 hook, P2 gap, P3 contribution, P4 roadmap")
4. For each planned paragraph `Pn`:
   a. Draft `Pn` referencing the narrative + plan + section playbook
   b. Present the draft to the author via `AskUserQuestion`:
      - **Accept** → write `Pn` into `OUT_DIR/0-sections/<file>.tex` in
        **the marker convention** (see Marker Format below)
      - **Revise** → take user comment, redraft (up to MAX_PARAGRAPH_RETRIES)
      - **Skip**   → emit placeholder header only with `[TODO]` tag and move on
   c. Update `SECTION_BOARD.md` paragraph counter
5. Mark section as `done` once all planned paragraphs are accepted/skipped
6. After every 2 sections, summarize progress inline and offer to pause

If the author makes structural changes ("merge P2 and P3", "add a P5
for ablation summary"), update the plan slot **before** continuing the
paragraph loop — never silently diverge from the plan.

### Phase 4: Cross-Section Sanity (optional, default ON)

Once the section loop completes:

1. `Skill("manuscript-optimizer")` in **review mode** on `OUT_DIR/`
2. `Skill("paper-claim-audit")` — does the draft support the narrative claim?
3. Emit `CREATE_DIR/CREATE_AUDIT.md` summarizing flagged issues
4. If issues found → present to user; they can either invoke
   `/haipipe-paper-revise` to address them or accept and proceed

### Phase 5: Compile (optional, off by default)

If `--compile` or `AUTO_COMPILE=true`:

```
Skill("paper-compile", args=OUT_DIR)
```

Otherwise emit a one-line hint:
`Next: cd <OUT_DIR> && bash 1-compile.sh   # or  /paper-compile <OUT_DIR>`

### Phase 6: Final Report

Update `CREATE_STATE.md`. Present to user:
- Sections drafted (with paragraph counts)
- TODO paragraphs (skipped, need follow-up)
- Audit findings (if Phase 4 ran)
- Suggested next:
  `/haipipe-paper-revise <OUT_DIR>` — polish via paper-weaving
  (markers are already in place, no insertion pass needed)

---

Marker Format (paper-weaving handoff contract)
----------------------------------------------

Every paragraph this skill writes into a section file follows this
shape so `paper-weaving` accepts the file as-is at its Step 1 format
check:

```latex
%% ---- P1.S1 ----
First sentence of paragraph 1.
%% ---- P1.S2 ----
Second sentence of paragraph 1.
%% ---- P1.S3 ----
Third sentence of paragraph 1.

%% ---- P2.S1 ----
First sentence of paragraph 2.
%% ---- P2.S2 ----
Second sentence of paragraph 2.
```

Rules:

- **PN numbering is file-local.** P1 always restarts at the top of a
  section file. Never use cross-file continuous numbering.
- **SN numbering is paragraph-local.** S1 restarts inside every P.
- **One marker per sentence.** Even short transitional sentences get
  their own `%% ---- PN.SN ----` header.
- **Paragraph ceiling: ≤6 sentences per paragraph.** This matches
  paper-weaving Hard Rule 5. If the plan slot calls for more, split
  the paragraph or rethink the slot with the author.
- **No `%%@` lines.** The `%%@` sentinel is paper-weaving's namespace
  (for plan/diagnose/propose blocks). This skill never writes them.
- **Empty paragraph slot**: when the author skips, write only the
  paragraph's lead marker with a TODO tag, no body:
  ```latex
  %% ---- P3.S1 [TODO: motivate ablation summary] ----
  ```
- **Provenance bracket allowed** in the header: `%% ---- P2.S1 [NEW per v0517] ----`
  is fine; the bracket note is the only optional element.

---

Venue Map
---------

Which template `3-write/conference-paper-writing/templates/<X>/` to copy
into the scaffold:

```
iclr, iclr2026                   → templates/iclr2026/
neurips, neurips2025             → templates/neurips2025/
icml, icml2026                   → templates/icml2026/
acl                              → templates/acl/
aaai, aaai2026                   → templates/aaai2026/
colm, colm2025                   → templates/colm2025/

ieee_conf                        → 3-write/paper-write/templates/ieee_conference.tex
ieee_journal                     → 3-write/paper-write/templates/ieee_journal.tex

nature, pnas, misq, isr          → fall back to plain article + a note
                                    that journal venues usually use the
                                    publisher's own submission system;
                                    offer to use the closest IEEE/ACM-
                                    style template as a stub.
```

If the requested venue has no template in the tree, **ask** before
defaulting — page limit and column count differ enough that the wrong
template wastes drafting work.

---

Inherited Hard Rules (from paper-weaving)
-----------------------------------------

Because this skill's output is the input contract for `paper-weaving`,
it adopts paper-weaving's hard rules at draft time so the polish round
doesn't have to undo them:

1. **PN.SN markers file-local** (already described above)
2. **No em-dashes anywhere.** Use comma, colon, or sentence break.
   Applies in drafted prose AND in this skill's chat output.
3. **No AI-flavored prose.** Anti-pattern shortlist (paper-weaving Hard Rule 4):
   - parenthetical adverbs comma-fenced mid-sentence ("primarily,", "specifically,")
   - apposition padding ("we use LLMs *as the measurement instrument* …")
   - callback constructions ("the same X *that drives* Y *also* enables Z")
   - anthropomorphic comparison verbs ("agree with", "claim that", "suggest that")
   - comma-tacked disclaimer appendages
   - double-marked adverbs ("recently, … increasingly …")
   - noun stacks (4+ chained nouns)
   - buzzword stacks ("two-agent large language model pipeline")
   - inline (i)/(ii)/(iii) packing
   - italics-on-key-nouns (`\emph{Score}`)
   - parenthetical name-explosions
   Read-aloud test applies.
4. **Compress, don't split.** 20-25 words per academic sentence;
   30 trigger compression review; 35+ split into two complete sentences
   (each gets its own PN.SN marker).
5. **Paragraph ceiling ≤6 sentences.**
6. **No sidecar `.txt` files for content.** State files in `CREATE_DIR/`
   are coordination only (board, contract, audit), not paper content.
7. **No fabricated citations.** Placeholder `\cite{TODO-author-year}` only;
   real citation work happens later via `components/citation/`.

Workflow-specific additional rules:

8. **Never skip the plan.** If the plan slot for a section is empty,
   pause and route to `Skill("paper-plan")` for that section only.
9. **Paragraph gate is hard.** Even in `--resume`, every paragraph
   re-prompts unless `--auto-accept` is explicitly passed.
10. **No silent overwrite.** Existing files in `OUT_DIR/` halt the run.
11. **One section at a time.** Don't parallelize sections — the author's
    voice drifts when they context-switch.
12. **Reuse, don't rewrite.** Section structure comes from
    `sections/section-<name>/`, prose style from
    `3-write/scientific-writing/`, templates from
    `3-write/conference-paper-writing/templates/`. This skill is glue.
13. **State first, write second.** `CREATE_STATE.md` updated before
    every `.tex` write so a crash mid-paragraph is resumable.

---

Specialist Return Contract
--------------------------

```
status:    ok | blocked | failed
summary:   2-3 sentences on what got drafted (sections + paragraph counts)
artifacts: [OUT_DIR/, CREATE_DIR/CREATE_STATE.md, CREATE_DIR/PAPER_CONTRACT.md,
            CREATE_DIR/SECTION_BOARD.md, CREATE_DIR/CREATE_AUDIT.md (if Phase 4)]
next:      typically /haipipe-paper-revise <OUT_DIR>
           or       /paper-compile <OUT_DIR>
```
