# SOP — Probe Folderless Refactor (2026-07-05)

Status: DRAFT for JL review. Execution paused at step 2.3; steps marked ✅ were applied before this SOP existed and sit UNCOMMITTED pending your sign-off.
Owner: JL. Executor: CC.
Decision record: JL 2026-07-05 — "probes/ 文件夹删掉,不是 single source of truth;probe 保留,可以 call task/discovery/insight;probe 的内容移到 lifecycle 各 stage 上。"

## 1. Target mental model

One sentence: probe becomes a PHASE (each stage's PROBE step) plus a GATEWAY (clean-context dispatch agent), and stops being a PLACE (`probes/` folder).

```text
BEFORE                                        AFTER
paper _PROBE/PPNN card   ┐ duplicated        paper/application _PROBE/PPNN card
project probes/<slug>/   ┘ contract          = the ONLY contract + receipt + verdict ✅
probe.yaml/evidence.md/verdict.md            (full mode adds a ## Verdict section)
        │                                            │
        ▼                                            ▼ PROBE phase (worker → gateway agent)
discoveries/ + tasks/  (execution)           discoveries/ + tasks/  (execution, unchanged)
insights/              (deposit)             insights/              (deposit, unchanged)
```

## 2. Invariants (must survive the refactor)

- The four principles hold: land-at-home (execution evidence lands in discovery/task ledgers; the verdict lands in the consumer's PPNN card), review-on-write (discovery reviewer for ledger writes; probe-reviewer G1/G2/G3 for full-mode verdicts), layered orders (stage → worker → gateway → discovery/task; no inline searching anywhere), trim-ceremony-never-principle.
- Execution artifacts NEVER move consumer-side: `discoveries/` and `tasks/` stay project-side, multi-paper reusable.
- All discipline earned from the four replication runs is retained verbatim in the gateway: SWEEP project-local, TRUST THE LEDGER, shape honesty (reused = pure read), FRESH EVIDENCE MUST LAND, background dispatch, batch, lean boot.
- Legacy `probes/` folders (ProjB etc.): read-only history. SWEEP may read them for reuse; nothing creates or updates them again.

## 3. Change list — load-bearing files (phase 1)

| # | File | Change | Status |
|---|------|--------|--------|
| 1 | probe/agents/haipipe-probe-orchestrator-agent.md | Rewrite → 2.0.0 "evidence gateway": no folder creation; SWEEP = discoveries+tasks+insights (+legacy probes read-only); shape reuse\|enrich\|fresh; full-mode verdict travels in the RETURN; Write/Edit removed from tools (executes the recorded 4.3.0(7) decision; resolves the open C1 thread as option A) | ✅ applied, uncommitted |
| 2 | probe/agents/haipipe-probe-creator-agent.md | RETIRE → `_old/` (its three outputs probe.yaml/evidence.md/status.md no longer exist; linking absorbed by gateway, presentation absorbed by return contract); `.claude/agents/` symlink removed | ✅ applied, uncommitted |
| 3 | probe/agents/haipipe-probe-reviewer-agent.md | → 2.0.0: input = claim + evidence refs; judgment RETURNED as text (G1/G2/G3 + verdict + reasoning ¶), never written to probe files; Write/Edit removed; G-gate definitions + g2 script unchanged | ✅ applied, uncommitted |
| 4 | probe/haipipe-probe/SKILL.md | Rewrite thin → gateway-layer doc: console RETIRED (dashboard folds into /haipipe-paper enter); documents the PPNN-card contract (order/receipt/## Verdict anatomy) and points to the gateway agent; fn/ + ref/ folder-era files marked LEGACY (kept for G-gate/reference value, not loaded) | ⬜ |
| 5 | paper/2-phase/1-probe/haipipe-paper-probe/SKILL.md | → 2.5.0: (a) refs always point directly at discovery/task artifacts; (b) TRANSLATE lands full-mode verdicts into the PPNN card `## Verdict` section + flips the claims ledger; (c) NEW RULE: every stage's PROBE phase re-invokes this Skill (no running from a stale in-context copy — test-123333333 PP02 ran from a 3-hour-old load) | ⬜ |
| 6 | project/haipipe-project (SKILL.md, ref/project-structure.md, fn/project.md, fn/repo-project.md, README.md) | Container layout: remove `probes/` from MANDATORY dirs; update the one-way dependency map (insights READS tasks/discoveries/stage cards; delete probes rows) | ⬜ |
| 7 | paper/wiki/08-stage-gate.md rule 4 | Reword: worker → gateway agent → discovery/task (drop "probe lifecycle" folder language); stage-read ban list says "discoveries/, tasks/, legacy probes/" | ⬜ |
| 8 | paper/wiki/00-evidence-principles.md | Land-at-home wording: evidence → discovery/task ledgers, verdict → consumer PPNN card | ⬜ |
| 9 | probe/DESIGN.md | Status → v5.0.0 folderless; Core Position rewritten (phase + gateway, not place); authority list updated (fn/ marked legacy) | ⬜ |
| 10 | probe/CHANGELOG.md | One rollup entry recording this refactor + the retirements | ⬜ |
| 11 | Memory: project_probe_aware_entrypoint.md (+ MEMORY.md line) | "probe = evidence hub (folder)" → "probe = PROBE phase + gateway agent; PPNN card = single source of truth; probes/ retired 2026-07-05" | ⬜ |

## 4. Phase 2 — peripheral reference sweep (separate pass, after phase 1 lands)

~30 files mention `probes/` in passing. Fix only lines that STATE routes or layouts; leave history (feedback/, _archive/, _old/, CHANGELOGs) untouched.

- application: haipipe-application-claims, haipipe-application-ask, ref/delivery-need.md (both copies)
- insight: haipipe-insight SKILL.md + review/data/information/knowledge/explore SKILL.md + ref/review-contract.md + DESIGN.md (deposit sources: task/discovery artifacts + stage _PROBE cards + claims ledgers)
- discovery: SKILL.md local_first sweep mention + DESIGN.md
- paper: claims/pitch/narrative SKILL.md mentions; wiki/11-delivery-need.md; README.md; ARIS_COMPARISON.md
- probe bucket internals: MENTAL_MODEL.md, PHILOSOPHY.md, SKILLSET_REVIEW.md (mark folder-era sections historical)
- task/DESIGN.md, haipipe-workflow/ref/plan-schema.md
- STRUCTURE.md (top-level tree)

## 5. What deliberately does NOT change

- PPNN numbering, `_PROBE/` folder name, 1-probe-plans/ index — consumer-side registry as-is.
- discovery + task + insight layers: zero contract changes.
- haipipe-probe-reviewer-agent survives (full-mode G gates need an independent judge).
- The 4-layer dispatch chain shape: stage → worker → gateway → discovery/task.

## 6. Rollback

Every phase-1 step = one scoped commit on Tools main. Rollback = `git revert` the refactor commits; legacy probes/ folders were never touched, so no data migration to undo. The three ✅ steps commit FIRST (one commit) so the rollback boundary is clean.

## 7. Exam (bench validation, after phase 1)

1. In test-123333333: next claims-stage evidence need (e.g. C1 experiment or prompt-design norms) runs under the new contract.
2. Watch: no probes/ folder appears; PPNN card carries receipt (+ verdict if full); refs resolve to discoveries/tasks; gateway lane shows zero Write/Edit calls; discipline rules still hold (bg dispatch, ledger landing, shape honesty).
3. Full-mode exam (G gates → ## Verdict in card) waits for the first real claims verdict; light path is exercised immediately.

## 8. Done criteria

- [ ] Phase-1 files 1-11 landed + committed (scoped commits)
- [ ] JL reviewed this SOP (this file), decisions confirmed
- [ ] Bench light-path exam passed (7.2)
- [ ] Phase-2 sweep landed
- [ ] Full-mode exam passed (first real verdict)
- [ ] This SOP archived into probe/CHANGELOG.md + deleted (no parallel bookkeeping files long-term)
