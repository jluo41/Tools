---
name: haipipe-paper-revise
description: "Polish an existing LaTeX paper paragraph-by-paragraph across all its sections. Discovers section files from a tex root, then runs haipipe-paper-edit-weaving on each (pilot first, parallel for the rest), respecting haipipe-paper-edit-weaving's three gates G1 (review plan) → Q (auto quality check) → G2 (cleanup). Cross-section audit and before/after diff at the end. Venue-agnostic. Called by /haipipe-paper orchestrator. Direct invocation works for whole-paper polish. Trigger: revise paper, polish tex, paragraph polish, whole-paper revision, walk sections, weave whole paper, 修改论文, 整篇润色, /haipipe-paper-revise."
argument-hint: [tex-root-or-main.tex] [--feedback <path>] [--section <name>] [--apply] [--cleanup]
allowed-tools: Bash, Read, Grep, Glob, Write, Edit, AskUserQuestion, Skill, Agent
---

Skill: haipipe-paper-revise (workflow specialist)
=================================================

Whole-paper polish orchestrator. The **engine for each section file is
`haipipe-paper-edit-weaving`** (in `3-write-edit/haipipe-paper-edit-weaving/`): this skill walks every
section `.tex` in a paper, dispatches each to `haipipe-paper-edit-weaving`, and
threads `haipipe-paper-edit-weaving`'s three-gate lifecycle (G1 → Q → G2) up to the
paper-wide level.

This skill does NOT re-implement haipipe-paper-edit-weaving's diagnose / propose /
apply / check / cleanup logic. It coordinates *across files*; the
per-file engine owns the marker convention, the `%%@` plan blocks, the
hard rules, and the gates.

Venue-agnostic. Works on any tex root that follows the paper paper-
folder contract — or any folder with `.tex` section files.

Usage
-----

```
/haipipe-paper-revise <tex-root>
/haipipe-paper-revise <tex-root> --feedback 1-rounds/v0506/REVIEWS.md
/haipipe-paper-revise <tex-root> --section method
/haipipe-paper-revise <tex-root> --apply                 (post-G1: cascade apply across done sections)
/haipipe-paper-revise <tex-root> --cleanup               (post-G2: cascade cleanup across done sections)
/haipipe-paper-revise <tex-root> --resume
```

Examples
```
/haipipe-paper-revise papers/lhm-a/                              (whole paper, discover → pilot → parallel)
/haipipe-paper-revise papers/lhm-a/0-lhm-a.tex                    (main.tex auto-discovers sections)
/haipipe-paper-revise papers/lhm-a/ --feedback 1-rounds/v0506/  (reviewer-feedback pass per section)
/haipipe-paper-revise papers/lhm-a/ --section intro               (single section, no parallel)
/haipipe-paper-revise papers/lhm-a/ --apply                       (apply all G1-approved plans)
/haipipe-paper-revise papers/lhm-a/ --cleanup confirm-delete      (Gate G2 cascade with auth)
```

Lifecycle Position
------------------

```
1-narrative → 2-plan → 3-write → ┌──────────────────┐  → 5-review → 5-respond → 6-present
                                 │ haipipe-paper-   │
                                 │  revise (HERE)   │
                                 │                  │
                                 │  per-section:    │
                                 │  haipipe-paper-edit-weaving   │
                                 │   G1 → Q → G2    │
                                 └──────────────────┘
```

The polish hop. Pairs naturally with `haipipe-paper-create` upstream
(which writes new tex in the marker convention haipipe-paper-edit-weaving expects)
and `haipipe-paper-rebuttal` downstream (which consumes the polished
draft).

Required Inputs
---------------

1. **tex root** — directory (e.g. `papers/lhm-a/`) or path to a main
   `.tex` file (e.g. `papers/lhm-a/0-lhm-a.tex`)
2. **marker convention** — every section file MUST have `%% ---- PN.SN ----`
   index headers per paragraph/sentence (haipipe-paper-edit-weaving Step 1 format
   check). If not, this skill stops at Phase 2 and reports which
   sections need marker insertion before polish can begin.
3. **(optional) reviewer feedback** — path passed through to each
   `haipipe-paper-edit-weaving` invocation as author-comment context

Constants
---------

- **REVISE_DIR** = `revise/`  (board + state + audit reports)
- **ENGINE** = `haipipe-paper-edit-weaving`  (per-section diagnose + plan + apply + gates)
- **DEFAULT_STRATEGY** = `pilot-then-parallel`  (see Phase 3)
- **CROSS_SECTION_AUDIT** = `true`  (Phase 5 after all sections done)
- **DIFF_REPORT** = `true`  (Phase 7 emits a colored PDF diff)

Workflow
--------

### Phase 0: Resume or Initialize

1. If `REVISE_DIR/REVISE_STATE.md` exists and `--resume` (or board
   shows incomplete) → load state, jump to next pending phase.
2. Otherwise → create `REVISE_DIR/`, initialize state with tex root,
   feedback path (if any), strategy, and a snapshot of the section list.

### Phase 1: Discover Sections (hybrid)

Try in order, stop at first success:

1. **Parse main.tex.** If input is a `.tex` file, or a directory has
   exactly one top-level `.tex`, scan it for `\input{…}` / `\include{…}`
   / `\subfile{…}`. Each resolved path is a section file.
2. **Glob `0-sections/*.tex`.** Standard paper paper-folder layout.
3. **Glob `*.tex` in the root** (excluding the main shell). Last resort.

If discovery returns 0 files → stop and ask. If it returns 1 file →
dispatch straight to `haipipe-paper-edit-weaving` (no orchestration overhead).

### Phase 2: Format Check (gate before any section is walked)

For each discovered section file, verify haipipe-paper-edit-weaving's format
contract (Step 1 of haipipe-paper-edit-weaving):

- every paragraph has a `%% ---- PN.SN ----` header
- PN numbering is file-local, monotone from 1
- at least one `%% Comments: {INITIALS} v<tag>:` line exists (if
  reviewer feedback drove this invocation, this should be auto-true
  after Phase 0 injects the feedback)

Emit `REVISE_DIR/SECTION_BOARD.md`:

```markdown
# Section Board — <tex-root>   (strategy: pilot-then-parallel)

| # | Section file                | Role          | Markers? | Status   | Notes |
|---|-----------------------------|---------------|----------|----------|-------|
| 1 | 0-sections/01_intro.tex     | intro         | ✅ ok    | pilot    |       |
| 2 | 0-sections/02_related.tex   | related-work  | ✅ ok    | pending  |       |
| 3 | 0-sections/03_method.tex    | method        | ✅ ok    | pending  |       |
| 4 | 0-sections/04_results.tex   | results       | 🟡 P3 missing S markers | blocked | fix before walk |
| 5 | 0-sections/05_discussion.tex| discussion    | ✅ ok    | pending  |       |
```

A `blocked` row stops the whole walk. The author can either fix the
markers manually or invoke `Skill("haipipe-paper-edit-weaving", args="<file>")`
directly so haipipe-paper-edit-weaving's own format-check error guides them.

Role detection by filename pattern. Pick the **pilot** as the most
structurally representative section (default: intro if present, else
the first section the author knows best — ask if ambiguous).

### Phase 3: Pilot + Parallel Walk

Adapted from haipipe-paper-edit-weaving's "Multi-subsection workflow (pilot +
parallel)" pattern, applied at the section level.

#### Phase 3a: Pilot (main agent, one section)

1. Mark pilot row `in_progress`
2. Dispatch:
   ```
   Skill("haipipe-paper-edit-weaving", args="<pilot.tex> [feedback-slice]")
   ```
3. haipipe-paper-edit-weaving runs its inline diagnose + plan embed (Step 1 through
   Step 4) and ends the turn at its own **Gate G1** (review the plan
   before any prose edits)
4. The author iterates with haipipe-paper-edit-weaving directly until Gate G1 is
   resolved (typically: approve / rework P<n> / rethink the story)
5. Mark pilot row `g1-approved`
6. **Lock the cross-section vocabulary** observed in the pilot
   (role-label phrasing, icon style, ARC-verb conventions). Record
   under `REVISE_DIR/PILOT_VOCAB.md` — this becomes the structural
   reference for the parallel sub-agents.

#### Phase 3b: Parallel (N sub-agents, remaining N-1 sections)

For every remaining `pending` section, spawn ONE sub-agent **in a
single message** (so they run concurrently):

```
Agent(
  description: "haipipe-paper-edit-weaving on <section>",
  subagent_type: "general-purpose",
  prompt: """
    Run /haipipe-paper-edit-weaving on <abs-path-to-section.tex>.

    Structural reference (read FIRST):
      <abs-path-to-pilot.tex>   — pilot section with embedded plan
      <abs-path-to-PILOT_VOCAB.md>

    Paper-level context:
      - shared ARC framing: <one line from pilot>
      - RQ: <from narrative or plan>
      - lexical preferences: <from PILOT_VOCAB.md>
      - reviewer feedback (if any): <slice of feedback for this section>

    Constraints:
      - STOP at Gate G1 (do NOT apply prose edits)
      - Do NOT run Gate Q (apply hasn't happened yet)
      - Report back under 300 words: severity counts, top issues,
        blocks inserted (4a + 4b × N ± 4c)
  """
)
```

After all sub-agents return:

1. Update each row to `g1-pending` (plan embedded, waiting for author)
2. Print a triage table to chat:
   ```
   Section          🔴   🟡   🟢   Notes
   02_related        0    2    1   compress P2
   03_method         1    3    2   P4 logic break (R2-C1)
   05_discussion     0    1    4   light pass
   ```
3. Sections marked all-🟢 are flagged "late-polish, ready for one-shot
   approve". Sections with 🔴 / 🟡 return to the main conversation for
   sequential G1 resolution.

#### Phase 3c: G1 resolution loop (main agent)

For each `g1-pending` section, the author reviews the embedded plan in
that `.tex` and chooses haipipe-paper-edit-weaving's G1 options (approve / rework /
rethink / abort) directly in the main conversation. haipipe-paper-edit-weaving handles
the iteration; this skill only updates the board row to `g1-approved`
when the author signals approval.

### Phase 4: Apply Pass (`--apply`)

Once enough sections are `g1-approved`, the author invokes:

```
/haipipe-paper-revise <tex-root> --apply
```

For each `g1-approved` section:

1. Mark row `applying`
2. Dispatch the apply phase through haipipe-paper-edit-weaving or its sibling
   `paper-revise`. Two routes:
   - **Default**: hand off to `Skill("paper-revise", args="<section.tex> apply")`
     for sentence-level apply (broader workflow, comments → edits)
   - **Fast**: when the author wants haipipe-paper-edit-weaving's own collapse-block
     apply path, dispatch `Skill("haipipe-paper-edit-weaving", args="<section.tex>")`
     and let haipipe-paper-edit-weaving's lifecycle handle apply + auto-trigger Gate Q
3. Mark row `q-pending` (apply done, Gate Q will fire next)

### Phase 5: Cross-Section Audits + per-section Gate Q

haipipe-paper-edit-weaving's **Gate Q** fires per file automatically after apply.
This skill adds a paper-wide audit on top:

1. Collect each section's Gate Q summary (PASS / 🟡 ATTENTION / FAIL)
   into `REVISE_DIR/REVISE_AUDIT.md`
2. Run cross-section sweeps (these complement the per-file checks):
   ```
   Skill("haipipe-paper-edit-optimizer")  # review mode — claim ↔ evidence ↔ figures ↔ terminology
   Skill("haipipe-paper-edit-claim-audit")     # does the polished draft still support the headline claim?
   Skill("haipipe-paper-edit-submission-audit")      # only if --pre-submission flag set
   ```
3. Aggregate into a paper-wide PASS/🟡/FAIL table; present to the
   author with offers to loop back to specific sections

### Phase 6: Gate G2 Cleanup Cascade (`--cleanup`)

Once Gate Q passes paper-wide (or the author acknowledges the 🟡
items), the author invokes:

```
/haipipe-paper-revise <tex-root> --cleanup
```

This **does not auto-delete anything**. For each section row marked
`q-pending` (post-Q) or `q-resolved`:

1. Print the haipipe-paper-edit-weaving Gate G2 prompt for that file (verbatim,
   path substituted) so the author can decide per-section:
   - delete in place themselves (recommended sed regex shown)
   - ask the skill to delete (requires `confirm-delete` token)
   - keep plan blocks (for next round's audit trail)
2. If the author types `--cleanup confirm-delete-all`, cascade the
   sed deletion across every section in scope and report the diff.

This is the only destructive operation; it always requires explicit
`confirm-delete-*` authorization.

### Phase 7: Diff Report

If the tex root was version-controlled (or has a pre-revise snapshot):

1. `Skill("haipipe-paper-edit-diffpdf")` to produce a colored before/after PDF
2. Save under `REVISE_DIR/DIFF.pdf`
3. Mention path in final report

### Phase 8: Final Report

Update `REVISE_STATE.md`. Present to user:
- Sections walked (with per-file paragraph-edit counts pulled from
  haipipe-paper-edit-weaving's block-collapse markers `[APPLIED v<tag>]`)
- Paper-wide Gate Q summary (Phase 5)
- Cleanup status (Phase 6)
- Diff location (Phase 7)
- Suggested next: `/paper-compile <tex-root>` or
  `/haipipe-paper-rebuttal` if revision was driven by reviews

---

Discovery Examples
------------------

Standard paper layout (Phase 1.2 hit):
```
papers/lhm-a/
├── 0-lhm-a.tex                ← main shell
├── 0-sections/                ← discovery hits here
│   ├── 01_intro.tex
│   ├── 02_related.tex
│   ├── 03_method.tex
│   ├── 04_results.tex
│   └── 05_discussion.tex
└── ...
```

Ad-hoc layout (Phase 1.1 — \input parsing):
```
paper/
├── main.tex                   ← parse \input{…}
│   \input{intro}
│   \input{method}
│   \input{results}
├── intro.tex
├── method.tex
└── results.tex
```

Flat layout (Phase 1.3 fallback):
```
paper/
├── intro.tex · method.tex · results.tex
```

---

Inherited Hard Rules (from haipipe-paper-edit-weaving)
-----------------------------------------

These are haipipe-paper-edit-weaving's hard rules, propagated to the workflow level.
The workflow MUST NOT violate them when writing its own files
(`REVISE_DIR/*`) or when phrasing chat output:

1. **Preserve author inline comments verbatim.** `%% Comments: {INITIALS} v<tag>:`
   lines stay exactly as written. Never paraphrase or translate them in
   the workflow's chat output either.
2. **PN.SN markers are file-local.** Workflow never uses cross-file
   continuous numbering in the board or audit reports.
3. **No em-dashes anywhere.** Workflow output (board, audit, chat) uses
   commas, colons, or sentence breaks.
4. **No AI-flavored prose.** Workflow's chat updates follow haipipe-paper-edit-weaving's
   anti-pattern list (no comma-fenced adverbs, no apposition padding,
   no callback constructions, no noun stacks).
5. **No sidecar `.txt` files for plan content.** Plan lives in each
   `.tex` as `%%@` blocks (owned by haipipe-paper-edit-weaving). Workflow may write
   `.md` files for *state* (board, audit, vocab) — those are coordination
   artifacts, not plan content.
6. **`%%@` sentinel is haipipe-paper-edit-weaving's namespace.** This workflow never
   writes `%%@` lines into any `.tex` file. All `.tex` edits flow
   through haipipe-paper-edit-weaving.
7. **Never auto-delete `%%@` blocks.** Phase 6 always requires explicit
   `confirm-delete-*` authorization from the author.
8. **Never apply prose edits without Gate G1 approval per section.**
   Phase 4 only walks sections marked `g1-approved` in the board.
9. **Gate Q always runs after apply per file.** Workflow does not
   suppress it; haipipe-paper-edit-weaving owns the suppression rules (micro-round,
   author override).
10. **Immerse before acting.** Even at the workflow level, read each
    section's embedded plan before drafting the triage table — don't
    summarize from sub-agent reports alone.

Workflow-specific additional rules:

11. **Board is the source of truth.** `REVISE_DIR/SECTION_BOARD.md` is
    updated before every `Skill()` or `Agent()` dispatch so a mid-
    section interrupt is resumable.
12. **Feedback passes through unchanged.** When `--feedback` is given,
    read the file once at Phase 0; forward the relevant slice (or the
    whole file if section-specific slicing isn't obvious) into the
    `haipipe-paper-edit-weaving` invocation as the author-comment argument.
13. **No silent skipping.** A section the user asks to skip is marked
    `skipped` with a one-line reason in the board, not removed.
14. **One paper at a time.** Don't walk two tex roots in one invocation
    — split into separate sessions.

---

Engine Map (haipipe-paper-edit-weaving and its siblings)
-------------------------------------------

| Per-section need | Engine | Notes |
|---|---|---|
| diagnose + plan embed in `.tex` (default) | `haipipe-paper-edit-weaving` | inline section-route |
| rework one paragraph | `Skill("paper-revise-paragraph")` via haipipe-paper-edit-weaving | haipipe-paper-edit-weaving routes |
| rewrite one sentence | `Skill("paper-revise-sentence")` via haipipe-paper-edit-weaving | haipipe-paper-edit-weaving routes |
| verify quantitative claims | `Skill("paper-check-numeric")` via Gate Q | Q substep Q2 |
| verify citations | `Skill("haipipe-paper-edit-check-reference")` via Gate Q | Q substep Q2 |
| broader multi-pass revision with sentence-annotation lifecycle | `paper-revise` | sibling of haipipe-paper-edit-weaving; this workflow can also dispatch directly to it |

This workflow does not call the leaf engines (paper-revise-paragraph,
paper-revise-sentence, paper-check-numeric, haipipe-paper-edit-check-reference,
citation-verifier) directly — haipipe-paper-edit-weaving routes to them as needed.

---

Specialist Return Contract
--------------------------

```
status:    ok | blocked | failed
summary:   2-3 sentences on what got walked, what passed Gate G1/Q,
           what's pending cleanup
artifacts: [REVISE_DIR/REVISE_STATE.md, REVISE_DIR/SECTION_BOARD.md,
            REVISE_DIR/PILOT_VOCAB.md, REVISE_DIR/REVISE_AUDIT.md,
            REVISE_DIR/DIFF.pdf (if Phase 7)]
next:      typically /haipipe-paper-revise <tex-root> --apply
           or       /haipipe-paper-revise <tex-root> --cleanup
           or       /paper-compile <tex-root>
           or       /haipipe-paper-rebuttal (if review-cycle)
```
