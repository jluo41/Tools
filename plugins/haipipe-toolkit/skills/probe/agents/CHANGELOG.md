probe agents — Changelog
========================

Agent-scoped changelog for the probe layer's two live agents (the evidence gateway + the thin Judge shell).
Never loaded at invocation; read on demand.
Versions match each agent's frontmatter `version:`. Newest first, grouped per agent.


haipipe-probe-orchestrator-agent — evidence gateway
---------------------------------------------------

## [2.0.5] — 2026-07-06
Opening quote and layer description recast from "claim-level" to "explore+gather verb" (aligns with haipipe-probe 7.0.0 identity recast).

## [2.0.4] — 2026-07-06
SWEEP insights wording de-biased from K-only: ALL FOUR card layers (D/I/K/W) can end the "need new work?" question — match the need's SHAPE to the layer (dataset question → D, claim question → K). JL exam-C review: "for insights, why we only have K card?" — the old "settled K-cards" phrasing could steer an agent past a D/I hit.

## [2.0.3] — 2026-07-06
Step 3 names the governed rulebook — the reviewer agent is a thin shell over Skill(haipipe-probe-review) (JL: process norms live in a skill).

## [2.0.2] — 2026-07-06
SWEEP is INDEX-FIRST — headlines, then a shortlist, then targeted reads; bulk-reading ledgers was named a cost defect.

## [2.0.1] — 2026-07-06
Legacy probes/ folders made INVISIBLE to SWEEP (JL: delete the read-only-prior lane); SWEEP covers all three warehouses (discoveries/ + tasks/ + insights/) every time.

## [2.0.0] — 2026-07-05 — FOLDERLESS REFACTOR
JL: probes/ duplicated the paper-side _PROBE card — not single source of truth. This agent no longer creates or updates probes/ folders; the caller's PPNN card is the one home for contract+receipt+verdict. haipipe-probe-creator-agent RETIRED (its probe.yaml/evidence.md/status.md outputs no longer exist; linking absorbed here, presentation absorbed into the return contract). Judge: reviewer returns judgment text; the verdict travels in MY return and the caller lands it. Write/Edit removed from tools — executes the long-recorded 4.3.0(7) decision (open {CC->JL} C1 thread resolved as option A; the refactor made it moot: nothing left for this agent to write). Legacy probes/ folders remain readable in SWEEP, never created/updated. All 1.5.x-1.6.0 discipline retained.

## [1.6.0] — 2026-07-05 — LEAN BOOT
1.5.2: SWEEP scope = the given project_root only; cross-project = USER decision. 1.5.1: TRUST THE LEDGER. 1.5.0: NO INLINE SEARCHING + FRESH EVIDENCE MUST LAND. 1.4.0: pick_list. 1.3.x: anchored return contract. 1.2.0: PLAN input form + shape decision. 1.1.0: SWEEP. 1.0.0: initial triad. (Full text in git history.)


haipipe-probe-reviewer-agent — thin Judge shell
-----------------------------------------------

## [3.0.0] — 2026-07-06 — PROCESS → SKILL
JL: the agent may be called, but a skill must govern the flow. The G1/G2/G3 rulebook moved to probe/haipipe-probe-review/SKILL.md; this agent is now a thin dispatch shell that invokes it headless and returns the output. Skill added to tools. Instruments (g2_integrity_check.py, probe-caveats-checklist.txt) moved with the skill.

## [2.1.0] — 2026-07-06
Body rewritten folderless-native; G3 vocabulary aligned to the PPNN card (supported | refuted | inconclusive).

## [2.0.0] — 2026-07-05 — FOLDERLESS REFACTOR
Judgment RETURNED as text, never written; Write/Edit removed.

## [1.x] — 2026-06-23
Merged 3 retired Judge agents (probe-structural-reviewer / probe-integrity-auditor / claim-verifier); deterministic G2 script. (Full text in git history.)
