# Workflow

Four entry stacks, one phase map. Pick the stack that matches your target, then walk the phases.

Read `PRINCIPLES.md` first -- the phase map here is mechanical; the principles say *which mindset* to apply at each phase.

**Venue routing at a glance:**

| Target | Playbook | When |
|---|---|---|
| Nature flagship | `nature-portfolio-playbook` | Broad advance legible to non-specialists |
| Nature Methods | `nature-portfolio-playbook` | Method / platform / computational framework |
| Nature Biotechnology | `nature-portfolio-playbook` | Biotech / translational / engineering depth |
| PNAS | `pnas-playbook` | Cross-disciplinary rigor, spans two NAS classifications, full Research Article scope |
| Science (out of scope) | -- | Societal / policy implications, short-form punch |
| MISQ / ISR / Management Science | `misq-playbook` / `isr-playbook` / `ms-is-playbook` | IS research, UTD24 venues |
| NeurIPS / ICML / ICLR / ACL / AAAI / COLM | (ARIS `paper-writing`) | Conference-first workflows |
| Patents | `patent-pipeline` | IP / invention protection |

===========================================================================
Entry stacks (curated subsets, not the full 98 skills)
===========================================================================

### Stack A -- Broad-science journal manuscript (Nature portfolio / PNAS / Science)

Default when venue is unstated or life-sciences-adjacent.

- `_workflows/paper-workflow` -- router
- `05_prewrite/paper-bootstrap` -- initialize project + notes
- `13_venue/nature-portfolio-playbook` -- choose Nature / Methods / Biotech + preflight
- `13_venue/pnas-playbook` -- PNAS fit, Significance Statement, classification, preflight
- `06_write/scientific-writing` -- draft and section rewriting
- `07_revise/manuscript-optimizer` -- structural revision, evidence-chain repair
- `07_revise/results-section-revision` -- late-stage Results narrative repair
- `09_figures/figure-planner` -- figure claim design and legend sync
- `10_review/citation-verifier` -- bibliography hygiene
- `10_review/submission-audit` -- pre-submission QA
- `11_respond/rebuttal-response` -- reviewer response + aligned edits

### Stack B -- ML / AI conference (NeurIPS, ICML, ICLR, ACL, AAAI, COLM)

Use only when venue is explicitly a conference.

- `_workflows/research-pipeline` -- full pipeline router (idea -> paper)
- `_workflows/idea-discovery` or `01_discover/research-lit` -- Workflow 1
- `02_plan/research-refine` + `02_plan/experiment-plan` -- Workflow 1b
- `_workflows/experiment-bridge` + `03_execute/experiment-queue` -- Workflow 1.5
- `04_analyze/result-to-claim` + `02_plan/ablation-planner` -- result -> claims -> ablations
- `_workflows/paper-writing` (chains `paper-plan` -> `paper-write` -> `paper-compile` -> `auto-paper-improvement-loop`)
- `09_figures/figure-spec` + `09_figures/paper-illustration` + `09_figures/mermaid-diagram`
- `10_review/auto-review-loop` (or `-llm` / `-minimax`) -- Workflow 2
- `10_review/paper-claim-audit` + `10_review/submission-audit` -- gate at `effort: max | beast`
- `_workflows/rebuttal` -- Workflow 4

### Stack C -- IS-journal (MISQ, ISR, Management Science)

- `_workflows/is-paper-workflow` -- IS-specific router (UTD24 venues)
- `13_venue/misq-playbook` or `isr-playbook` or `ms-is-playbook` -- pick by venue fit
- `06_write/scientific-writing` -- drafting
- `07_revise/manuscript-optimizer` -- structural revision
- `09_figures/figure-planner`
- `10_review/citation-verifier` + `submission-audit`
- `11_respond/rebuttal-response`

### Stack D -- Patent / IP

- `_workflows/patent-pipeline` -- router
- `01_discover/prior-art-search` -- prior art
- `13_venue/patent-novelty-check` -- novelty assessment
- `06_write/writing-systems-papers` (if systems-focused) or `13_venue/specification-writing`
- `13_venue/patent-review` -- internal review
- `13_venue/jurisdiction-format` -- jurisdictional formatting

===========================================================================
Unified phase map (all stacks walk this, but branch inside the write band)
===========================================================================

```
00_meta       cross-cutting, always available
  |
  v
01_discover   lit search, paper reading, idea generation, novelty check
  |
  v
02_plan       refine method, plan experiments, draft claims, derive formulas
  |
  v
03_execute    run experiments (local / modal / vast.ai), queue, monitor
  |
  v
04_analyze    experiment outputs -> claims + evidence map
  |
  v
05_prewrite   bootstrap, outline, architecture, incubation + routers
  |
  v  (write band: 06-08 branch by target)
  +-------------------+-------------------+------------------+
  v (journal)         v (conference)      v (IS journal)     v (patent)
06_write [Nature]    06_write [ARIS]     06_write [hybrid]   13_venue [patent]
  |                    |                   |                   |
  v                    v                   v                   v
07_revise            07_revise           07_revise           (inventions)
  |                    |                   |                   |
  v                    v                   v                   v
08_postwrite         08_postwrite        08_postwrite        13_venue [patent-review]
  |                    |                   |                   |
  v                    v                   v                   v
09_figures           09_figures          09_figures          (interleaved w/ 05-06)
  |                    |                   |
  v                    v                   v
10_review            10_review           10_review
  (audit-first)        (loop-first)        (both)
  |                    |                   |
  +---------+----------+-------------------+
            v
        11_respond   rebuttal (if reviews received)
            |
            v
        12_present   slides / poster / talk
```

Note: `09_figures` is placed after writing for linear reading, but in practice `figure-planner` runs in parallel with `05_prewrite` (figure-led results, PRINCIPLES.md #2). Render-oriented figure skills (`paper-figure`, `paper-illustration`, `mermaid-diagram`) run during `06_write`-`08_postwrite`.

**Branch rule at phase 06 (writing):**
- Journal manuscript (Stack A): use Nature skills -- deliberate, claim-driven, single-pass-with-revision.
- Conference paper (Stack B): use ARIS `paper-writing` -- auto-plan + auto-draft + auto-improve loop. Effort ramps: `lite` for rough draft, `max | beast` for submission.
- IS journal (Stack C): start with Nature's `scientific-writing` discipline, then feed through ARIS's `auto-paper-improvement-loop` for mechanical polish.

**Branch rule at phase 10 (review):**
- Journal manuscripts run `submission-audit` **before** any loop -- the loop may polish over unstable claims. Principle 7.
- Conference papers can run `auto-review-loop` iteratively during drafting; gate with `submission-audit` + `paper-claim-audit` at `effort: max | beast` (ARIS assurance gate).
- Run `citation-verifier` + `citation-audit` before every submission regardless of stack.

===========================================================================
Refresh-notes discipline (required before phases 05-08)
===========================================================================

Before any heavy writing, figure, review, or rebuttal work, refresh these files in `notes/`:

- `notes/project_truth.md` -- what the paper currently claims (single source of truth)
- `notes/result_summary.md` -- locked vs directional vs gapped findings
- `notes/paper_handoff.md` -- ready-to-draft vs blocked, with artifact pointers
- `notes/claim_evidence_map.md` -- claim -> evidence -> status (supported / partial / directional)
- `notes/decision_log.md` -- decisions made across sessions so skills don't re-litigate them

Templates in `examples/`. `paper-bootstrap` creates them on project init.

Principle 10: Skills that revise prose assume these files are current. A `manuscript-optimizer` run against stale notes produces confident revisions of yesterday's claims.

===========================================================================
Default sequence (journal path, for reference)
===========================================================================

1. `paper-bootstrap` -- init project, create notes/ templates
2. `nature-portfolio-playbook` -- venue fit, article type decision
3. Refresh `notes/project_truth.md`, `notes/result_summary.md`, `notes/paper_handoff.md`, `notes/claim_evidence_map.md`
4. `scientific-writing` (drafting) or `manuscript-optimizer` (revising)
5. `figure-planner`
6. `results-section-revision` -- when Results is scientifically stable but narratively abrupt
7. `citation-verifier`
8. `submission-audit`
9. (submit)
10. `rebuttal-response` when reviews return

===========================================================================
Routing rules between overlapping skills
===========================================================================

- `scientific-writing` -- draft or rewrite section prose
- `manuscript-optimizer` -- fix claim structure, evidence chain, terminology
- `results-section-revision` -- fix only local Results flow when claims are stable
- `paper-write` (ARIS) -- LaTeX-first drafting for conference papers
- `paper-writing` (ARIS) -- the full conference-paper meta-workflow
- `paper-workflow` (Nature) -- top-level journal router
- `auto-review-loop*` (ARIS) -- iterative LLM-reviewer loop; useful during drafting
- `paper-reviewer` (Nature) -- single-pass reviewer-side evaluation
- `submission-audit` (Nature) -- pre-submission gate; never skipped for journals
- `paper-claim-audit` (ARIS) -- claim grounding check; complements submission-audit

When in doubt, run the Nature discipline skill *after* the ARIS automation skill. Automation gives speed; Nature discipline gives the audit that submission deserves.
