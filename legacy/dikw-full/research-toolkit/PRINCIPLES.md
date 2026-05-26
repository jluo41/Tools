# Principles

The toolkit bundles two philosophies: **Nature-Paper-Skills** (journal-first, claim-driven, deliberate revision) and **ARIS** (automated loops, effort levels, auto-review). Both are useful. They apply in different situations.

These principles say which mindset governs a given task so you don't run an auto-loop on an unstable claim or hand-polish prose that hasn't been through a reviewer pass.

===========================================================================
Part 1 -- Always true (Nature's discipline, adopted verbatim)
===========================================================================

**1. Claim before polish.** Do not smooth prose that sits on top of an unstable claim or a weak evidence chain. Fix the claim first. Applies to every skill that writes or revises text.

**2. Figure-led results.** One main claim per figure. Figures drive the story; text annotates them. Use `09_figures/figure-planner` before `06_write/scientific-writing`.

**3. Legends are second-layer narration.** Main text stays compressed; legends preserve panel roles, quantitative anchors, and interpretation scope.

**4. Reverse outline before rewriting.** For any existing section: identify the section thesis, each paragraph's job, and what evidence it carries. Then rewrite. `manuscript-optimizer` and `results-section-revision` enforce this.

**5. Evidence-bounded language.** Abstract, introduction, and discussion never overstate what results directly show. `submission-audit` checks this before submission; `paper-claim-audit` checks it continuously.

**6. Venue fit is a structural decision.** Choose venue family and article type *early*. Do not optimize for the wrong target and try to fix it stylistically late. See `WORKFLOW.md` for venue routing.

===========================================================================
Part 2 -- Automation discipline (ARIS's contribution)
===========================================================================

ARIS's auto-loops (`10_review/auto-review-loop*`, `08_postwrite/auto-paper-improvement-loop`, `research-pipeline`) are powerful but dangerous when pointed at unstable work. Rules:

**7. Auto-loops operate on stable claims only.** Before running any auto-loop, the claim-evidence map (see `examples/`) must be current and the result-summary must mark the target claim `supported`, not `directional` or `partial`. Running a loop on unstable claims produces polished prose defending weak evidence -- the worst outcome.

**8. Effort levels are assurance dials, not quality dials.** `lite` / `balanced` / `max` / `beast` change *how many verification passes* run, not *how good* the output is. A `beast`-run on a bad plan is still a bad paper.

**9. External verifiers beat self-critique.** When a skill offers both an internal critique step and an external verifier (Codex MCP, GPT-5.4 Pro via Oracle, auto-review-loop-llm), prefer the external one before accepting the output. `auto-paper-improvement-loop` and `paper-writing` at `effort: max | beast` gate on `tools/verify_paper_audits.sh`.

**10. Refresh notes before heavy revision.** Before a multi-session rewrite, refresh the canonical notes (see `examples/project-layout.md`):
- `notes/project_truth.md` -- what the paper currently claims
- `notes/result_summary.md` -- which claims are locked, directional, or gapped
- `notes/paper_handoff.md` -- what's ready to draft, what's blocked
- `notes/claim_evidence_map.md` -- claim -> evidence -> status ledger

Skills assume these exist. Running `manuscript-optimizer` without refreshing them first produces revision based on stale memory.

===========================================================================
Part 3 -- When the two philosophies diverge
===========================================================================

**Deliberate revision vs auto-loop.** Nature skills assume the user makes every decision; ARIS skills delegate to the loop. Pick by phase:

| Phase | Philosophy | Why |
|---|---|---|
| 01_discover | ARIS (loops, multi-source) | Breadth matters; missed coverage is the failure mode |
| 02_plan     | Mixed -- ARIS for brainstorm, Nature for claim lock | Plan novelty benefits from volume; claim selection benefits from discipline |
| 03_execute  | ARIS (auto-queue, auto-monitor) | Infra; automation wins |
| 04_analyze  | Nature (claim-evidence mapping first) | Premature quantitative polish masks weak claims |
| 05_prewrite | Nature (bootstrap, plan, architecture) | Setup discipline determines downstream quality |
| 06_write    | Nature (deliberate) for journals; ARIS (pipeline) for conferences | Journals reject on unstable claims; conferences reject on missing comparisons |
| 07_revise   | Nature (reverse outline, evidence-chain repair) | Revision is claim work, not prose work |
| 08_postwrite | ARIS (auto-improvement loop, compile) | Mechanical polish and build |
| 09_figures  | Nature (figure-planner drives layout) | Figure logic is structural, not decorative |
| 10_review   | Both in sequence: ARIS auto-loop *then* Nature audit | Loop catches mechanical issues fast; audit catches the rest |
| 11_respond  | Nature (rebuttal-response + paper-rebuttal) | Deliberate, reviewer-facing |
| 12_present  | ARIS (auto-slides/poster) | Mechanical output from finished paper |
| 13_venue    | Nature-ideology (venue fit is structural) | See `WORKFLOW.md` venue routing |

**Conflict resolution rule.** If a skill from ARIS and a skill from Nature seem to cover the same job (e.g., `auto-review-loop` vs `paper-reviewer`, `paper-writing` vs `paper-workflow`), use both in sequence, not either-or: ARIS first for breadth and speed, Nature second for discipline and venue fit. Never substitute auto-review for submission-audit before journal submission.

===========================================================================
Part 4 -- The anti-principles (what this toolkit refuses to do)
===========================================================================

- No "make my paper better" one-shot button. Every improvement loop gates on claims being locked first.
- No polishing without a claim-evidence map.
- No venue-agnostic writing. Either you named the venue or the default is journal-first.
- No auto-generated citations without verification. `citation-verifier` + `citation-audit` + `reference-audit-guide` run before acceptance.
- No silent skill substitution. If the user asked for Nature flow and you reached for an ARIS skill (or vice versa), state the swap and why.
