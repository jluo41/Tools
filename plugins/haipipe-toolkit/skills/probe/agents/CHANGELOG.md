probe agents — Changelog
========================

Agent-scoped changelog for the probe layer's agents. As of 2026-07-14 there is exactly ONE
live agent (the thin Judge shell); the evidence gateway is RETIRED.
Never loaded at invocation; read on demand.
Versions match each agent's frontmatter `version:`. Newest first, grouped per agent.


## [RETIREMENT] — 2026-07-14 — haipipe-probe-orchestrator-agent (the EVIDENCE GATEWAY) is DEAD

Ruling: `Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/` v3 (APPROVED by JL 2026-07-14), CC-6 + JL-13. Companion to
haipipe-probe 8.0.0.

Moved `haipipe-probe-orchestrator-agent.md` -> `./_archive/` (git mv, history preserved) and
DE-REGISTERED: the symlinks were removed from BOTH `~/.claude/agents/` and
`<repo>/.claude/agents/`, where they would otherwise have resolved to nothing. `./_archive/README.md`
is the tombstone. **Do not re-symlink it.**

Why — the gateway was a THIRD clean context in front of two that already had one:

```text
   v7:  📄 paper ──▶ 🤖 probe-orchestrator (clean ctx) ──▶ 🤖 task-orchestrator (clean ctx) ──▶ bank
                     └─ SWEEP · shape · write _ASK/ stub · dispatch ─┘
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        one extra hop that bought nothing and cost a stake leak

   v8:  📄 paper ──▶ 🤖 task-orchestrator / discovery-orchestrator (clean ctx) ──▶ bank
                     the commission goes VERBATIM (LAW 1); THEIR clean context IS the wall
```

Where each of its four jobs went:
- **SWEEP** (grep discoveries/ + tasks/) -> the PAPER-SIDE **MATCH** (haipipe-probe PART 4, step 2), run in the consumer's own session. A grep never needed an agent.
- **shape: reused | enriched | fresh** -> split in two, and both halves moved: the **COST LADDER** (R13: T0 JOIN · T1 LOCAL · T2 REUSE · T3 ENRICH · T4 FRESH) is the probe's; the **qa gate** (R11: 1 scan, 2 digest, 3 P-B-E-R) is the executor's, and the ENRICH DEPTH (R15) is the executor's PRIVATE business — the probe never learns which depth ran.
- **write the `_ASK/PPNN_<slug>.md` stub** -> **DELETED**. The bank is PROBE-UNAWARE (R2): no `_ASK/`, no `_ANS/`, no `answers:`, no PP ids. The `commission` block inside the probe file's question SECTION replaces the stub entirely, and it survives a dead paper session because the PAPER is the memory (R6).
- **dispatch execution** -> a DIRECT `Agent()` call on the EXISTING orchestrators (JL-13 confirmed them as the doors): `haipipe-task-orchestrator-agent` / `haipipe-discovery-orchestrator-agent`.

Not retired, do not confuse: **`haipipe-probe-reviewer-agent` and the `haipipe-probe-review`
SKILL SURVIVE.** They do consumer-side claim judging (G1/G2/G3), and were never part of the
gateway — the JUDGMENT ITSELF is unchanged (three gates, five fraud patterns, the thresholds,
the confidence scale, the `associational | causal` guard).

Two things about them DID change, and both had to be written down (see their entries below —
reviewer 4.0.0/4.1.0, skill 2.0.0/2.1.0 — because until then they still described the dead world):

- their **CALLER**: the gateway was their only declared dispatcher, so with it archived they had
  none. They are now dispatched DIRECTLY by the paper/application PROBE-phase worker at its
  INTERPRET step, for a `mode: full` section.
- their **LANDING SITE**: the judgment lands in the consumer's `0-lifecycle/1-claims/1-claims.md`
  (per-claim, per-consumer, private). The PPNN card's `## Verdict` block is gone and `verdicted`
  is no longer a state (R7).

Note this does NOT touch a discovery's own `verdict.md` terminal file, which is executor-native
and survives.

**Why 产审分离 still holds without the gateway.** The old rationale was "the gateway assembled the
evidence, so the gateway does not grade it." With no gateway, the principle is unchanged and the
mechanism is cleaner: the EXECUTOR assembles the evidence, in its own probe-unaware session; a
SEPARATE fresh-context reviewer grades it. Producer and judge were never the same context, and
still are not.

Everything below this line is the gateway's history, kept for the record. It describes `_ASK/`
stubs, `answers:` returns, and PP ids crossing to the bank — all three are now spec violations
(haipipe-probe/SKILL.md PART 9). Read it as archaeology, never as instruction.


haipipe-probe-orchestrator-agent — evidence gateway  💀 RETIRED 2026-07-14
--------------------------------------------------------------------------

## [2.4.0] — 2026-07-12  (haipipe-probe-orchestrator-agent) — INSIGHT RETIRED

- **The SWEEP reads TWO warehouses, not three**: `discoveries/` (outside evidence, incl. Review-type verdict.md / landscape.md) + `tasks/` (inside evidence). `insights/`, `insights/INDEX.md` and D/I/K/W shape-matching are GONE from Step 1; shape-matching is now WAREHOUSE-matching. Supersedes the 2026-07-05 "all three warehouses, every time" rule recorded below.
- **NEW Step-1 item 1b — cross-consumer QUERY-ONCE (READ-ONLY)**: grep already-landed PPNN cards in `papers/*/1-probe-plans/` + `applications/*/1-probe-plans/` (status read|verdicted|answered-local). A card that already answers the need is a REUSE hit — cite the card AND the refs it anchors. This is what makes a settled judgment reusable across consumers now that insight is retired. Hard limits: never write another consumer's card; never re-dispatch an answered question; never carry a card's `## Why` into a stub or plan (PAPER-AGNOSTIC still binds).
- `insights/` added to the do-not-touch list: legacy folders are dead history — never read, never written, never deleted.

## [2.3.1] — 2026-07-12  (haipipe-probe-orchestrator-agent)

Audit repair (pairs with haipipe-probe 7.8.1):
- Discovery target/creation paths corrected to TWO-level (`discoveries/{S|L|P}{NN}_{group}/{NN}_{topic}/_ASK/`) — the agent was told to create group-level stubs, which no Plan stage would ever read.
- DIRECT-ASK EXEMPTION added to HANDOFF FIRST: a card-less plan (no correlation_id/PPNN) writes NO stub and is dispatched in-session; never invent a PP number.
- The task-GROUP guard is now stated as task-only (discovery groups are created by the discovery layer by design).

## [2.3.0] — 2026-07-12  (haipipe-probe-orchestrator-agent)

JL routing ruling 2026-07-12 (haipipe-probe 7.8.0 companion):
- Input spec gains `target:` — the caller's proposed receiving folder (existing path / `NEW <path>` / `?`). The gateway HONORS it unless its SWEEP finds better coverage; a `?` or a `NEW` target that duplicates an existing folder is the gateway's to resolve. The actual landing site returns in `handoff:` so the caller can correct its card.
- Step 2 gains the folder-creation law: create folder + `_ASK/` + stub and **NOTHING ELSE** — no `.py`/`configs/`/`runs/`/`workflow/`. Code scaffolding needs task-TYPE knowledge (specialist + template) the gateway does not have; that is the task layer's BUILD stage. Naming by reference to each layer's own law (task folders TWO-level per ref/hierarchy.md; discoveries `{S|L|P}{NN}_{topic}`), never an invented scheme. A new task-GROUP is NEVER created silently — return `blocked` and let a human name it.
- Stub path corrected to TASK-FOLDER level (`tasks/{G}{NN}_{group}/{NN}_{task}/_ASK/`); the old line pointed at the task-GROUP.

## [2.2.0] — 2026-07-12  (haipipe-probe-orchestrator-agent)

JL rulings 2026-07-12 (haipipe-probe 7.6.0 + 7.7.0 companions):
- Stub path → `<receiving folder>/_ASK/PPNN_<slug>.md` (the `_ASK/` container; filename mirrors the caller's `1-probe-plans/PPNN_<slug>.md` card — same PPNN, same slug on both banks). Zeroth-state phrasing updated (folder whose only content is `_ASK/`).
- Step 2's inline stub rule list now LEADS with PAPER-AGNOSTIC ahead of VERDICT-BLIND — the 7.6.0 rule existed here only by pointer; this agent WRITES the stubs, and the incident review showed inline rule lists beat by-pointer anatomy when an agent is in a hurry. The list states: self-contained Q1/Q2, no consumer claim ids (H1/H2/C3), no seed/pitch/narrative words, no stake, no re-injection of consumer vocabulary into an already-translated plan.
- Consumer-side card references updated: "per-stage `_PROBE/PPNN` card" → "`1-probe-plans/PPNN` card"; return-contract `handoff:` line carries the new stub path shape.

## [2.1.0] — 2026-07-11  (haipipe-probe-orchestrator-agent)

Changed (two-footed-bridge ruling, JL 2026-07-11; pairs with haipipe-probe 7.4.0)
- The zero-writes rule gains its one deliberate exception: at enrich/fresh dispatch, Step 2 now writes the `_ASK_PPNN.md` handoff stub into the RECEIVING tasks//discoveries/ folder BEFORE dispatching the execution agent — the durable dispatch record that makes the caller's `status: dispatched` disk-derivable and lets a later /haipipe-task or /haipipe-discovery session pick the work up if this agent dies. Fresh need with no folder: create folder + stub and nothing else (zeroth state). REUSE writes no stub. Stub anatomy + verdict-blind/write-once rules live in haipipe-probe/SKILL.md.
- `Write` added to tools. Return contract gains a `handoff:` line (stub paths written, or none).

## [2.0.6] — 2026-07-07  (haipipe-probe-orchestrator-agent)

Changed (Part-0 harvester ruling)
- Return contract: the pick_list pointer discipline generalized to all three harvest lanes — value-shaped/display-shaped needs must name the value-bearing files / display units explicitly in refs, which the caller records as value_refs/unit_refs lane lines (harvest: OWED) and pays via the matching harvester.

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

## [4.1.0] — 2026-07-14 — the last retired vocabulary out of the body

Fixed
- The do-not list still forbade writing "no verdict.md, no probe.yaml, no **card**" — two of those three artifacts are retired, so the rule was phrased in a dead vocabulary. It now names what actually exists and must never be written by this agent: the claim ledger, a probe file, a bank file.
- Return key `verdict:` → `status:`, matching `haipipe-probe-review` 2.1.0 and the `1-claims.md` field the caller transcribes it into.

Changed
- 产审分离 is EXPLAINED rather than asserted. The old justification ("the gateway assembled the evidence, so the gateway does not grade it") died with the gateway. The principle did not: the EXECUTOR assembles the evidence in its own probe-unaware session, and this reviewer grades it in a SEPARATE fresh context. Producer and judge were never the same context, and still are not.
- Points at `./README.md` for the live dispatch map, so the agent and its roster cannot drift apart again.

## [4.0.0] — 2026-07-14 — dispatched DIRECT; judgment lands in 1-claims.md

Ruling: `Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/` v3 (APPROVED by JL 2026-07-14), CC-6 + JL-13.

Fixed
- 3.0.0 survived the redesign but declared its ONLY dispatcher to be `haipipe-probe-orchestrator-agent` (retired + de-registered) and told the caller to land the verdict in a `1-probe-plans/PPNN` card (retired folder, retired block). So it had **no live caller AND no live landing site**: a full-mode section's judgment was returned and then dropped on the floor.
- Now dispatched DIRECTLY by the paper/application PROBE-phase worker at INTERPRET for a `mode: full` section; the caller lands the return in the consumer's `0-lifecycle/1-claims/1-claims.md`. Every 'gateway' and '1-probe-plans/PPNN card' mention removed.

## [3.0.0] — 2026-07-06 — PROCESS → SKILL
JL: the agent may be called, but a skill must govern the flow. The G1/G2/G3 rulebook moved to probe/haipipe-probe-review/SKILL.md; this agent is now a thin dispatch shell that invokes it headless and returns the output. Skill added to tools. Instruments (g2_integrity_check.py, probe-caveats-checklist.txt) moved with the skill.

## [2.1.0] — 2026-07-06
Body rewritten folderless-native; G3 vocabulary aligned to the PPNN card (supported | refuted | inconclusive).

## [2.0.0] — 2026-07-05 — FOLDERLESS REFACTOR
Judgment RETURNED as text, never written; Write/Edit removed.

## [1.x] — 2026-06-23
Merged 3 retired Judge agents (probe-structural-reviewer / probe-integrity-auditor / claim-verifier); deterministic G2 script. (Full text in git history.)
