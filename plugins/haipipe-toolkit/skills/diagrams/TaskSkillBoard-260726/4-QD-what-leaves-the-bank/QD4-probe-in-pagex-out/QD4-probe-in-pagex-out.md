# Probe in, PageX out: the Task Board knowledge boundary
state: 🟡 PARTIAL · direction ruled · fresh-context route passed · open: materialized cross-board fixture
owner: JL

## Opening
Which door reaches raw evidence, and which door lets a delivery Board reuse what was learned?

Probe points inward from an Insight Page to Task and Discovery sources. PageX points outward from Paper or Application to a settled Insight Page. Keeping those directions separate prevents every consumer from rebuilding the same evidence chain.

**Covered here**: ownership and direction of the two doors.

**Covered elsewhere**: QD3 owns the DIKW Page content; BoardSkillBoard owns the generic PageX and Probe plugin mechanics.

## Writing Style
State directions with an explicit source and destination. Never use “evidence access” when Probe or PageX is the actual operation.

## Diagram
**Two doors, one wall**: raw evidence enters Insight; settled knowledge leaves through PageX.

```text
Task/Discovery folder ── Probe ──▶ Insight Page ── PageX ──▶ Paper/Application
```

## Content

### 1 · Probe belongs at knowledge production
**Inward door**: the evidence owner asks and harvests.
```text
Insight question ── Probe ──▶ Task/Discovery source
```
Probe may inspect Task/Discovery folders because the Insight Page owns evidence interpretation and DIKW settlement. Its cards and displays remain inside the Task/Insights Board boundary.

### 2 · PageX belongs at knowledge reuse
**Outward door**: the consumer selects a settled packet.
```text
Paper/Application ── PageX ──▶ settled Insight Page
```
Paper and Application read the settled Page contract, handoff, and source pointers. They do not recursively rerun the target Page's Probe or copy its cards into their own folder.

### 3 · Missing knowledge returns to this Board
**Return route**: a gap becomes a neutral question before evidence work starts.
```text
delivery gap → /haipipe-task insight → settle → PageX refresh
```
A delivery Page keeps its stake locally, sends a consumer-neutral question here, and waits for or reuses an Insight Page. The answer returns as a PageX binding, not a copied QA paragraph.

## Aims

### A1 · Probe belongs at knowledge production
- A1.1 · New Application and Paper contracts create no local evidence investigation for an existing Insight need.
  **Done when:** their Page Types route missing knowledge to this Board.

### A2 · PageX belongs at knowledge reuse
- A2.1 · A cross-board fixture resolves a settled Insight handoff without Task-folder access.
  **Done when:** the PageX binding and bounded packet are inspectable.

## States

### A1 · Probe belongs at knowledge production
- ✅ A1.1 · Met in the new Paper and Application Page Type contracts written 260817.

### A2 · PageX belongs at knowledge reuse
- ⬜ A2.1 · Cross-board fixture not yet materialized.

## Files

### 📋 Contracts
- `../../../../task/page-types/haipipe-page-for-insight/SKILL.md`
  Owns Probe-to-DIKW settlement.
- `../../../../board/page-plugins/haipipe-plugin-pagex/SKILL.md`
  Owns bounded Page reuse.
- `../../../../board/page-plugins/haipipe-plugin-probe/SKILL.md`
  Owns the generic Probe plugin.

## Law
- 260817 JL · ⚖️ Task/Insights Board owns DIKW; Paper and Application gather settled Pages and re-express them. Probe therefore enters the knowledge Board, while PageX leaves it toward delivery.

## Log
260817 · Two fresh-context runs preserved the direction: Insight used Probe toward Task/Discovery, while Application used PageX toward the settled Insight and routed a missing safety question back to Task.
260817 · Opened from JL's ruling that Application message design follows the same gather-and-reexpress logic as Paper.
