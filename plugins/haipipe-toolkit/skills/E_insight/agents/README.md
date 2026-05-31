E_insight — Agent Roster
========================

Two families, separated by folder — applied THOUGHTFULLY (the way D_probe
departed from C_task; see ../DESIGN.md). E goes per-DIKW on BOTH families:

```
creators/   🔨 BUILDER family  — one per DIKW layer (files the card)
reviewers/  🔍 REVIEWER family — one per DIKW layer (gates the card) + 1 cross-layer
```

Folder = family. Knowledge lives in `../ref/insight-md-schema.md` (card format),
`../ref/dikw-boundaries.md` (each layer's boundary + worked examples), and
`../ref/invocation-modes.md` (the dual-mode contract) — NOT in the agents.
Agents are thin pointers.


The asymmetry note (E vs C vs D)
--------------------------------

C_task keeps reviewers TYPE-AGNOSTIC ("fixed at 2; adding a task type costs 0
reviewers") because run trustworthiness is the same check for any task type.
**E departs**: each DIKW card has a genuinely DIFFERENT boundary —

```
🟦 D  numbers must trace · no interpretation
🟩 I  a regularity across ≥ 2 D
🟨 K  claim ⊆ evidence · ALL counter-evidence · + the ★ probe gate
🟧 W  actionable ("could I write the command?")
```

— so E uses a SPECIFIC reviewer per type, each enforcing that layer's accuracy
+ style/boundary against `../ref/dikw-boundaries.md`. The ONE shared reviewer is
`index-integrity`: the cross-layer graph (D→I→K→W edges, `ref_by` symmetry,
INDEX↔files) CANNOT be per-type, so it stays single.


The E_insight lifecycle
-----------------------

```
   source: probes/<...>/probe.yaml (confirmed)  OR  prior D/I/K cards
                          │
   ▼ FILE                │ creators/ call the layer skill headless (full spec → SILENT)
   card-creator-<layer>-agent       → insights/<LAYER>/<ID>_<slug>.md
                          │
   ▼ 🚦 GATE 1 (per-type) │ reviewers/ — one per DIKW type, filer ≠ judge
   card-reviewer-<layer>-agent      accurate + in-boundary + in-style?  → <LAYER>_CARD_REVIEW.md
                          │
   ▼ 🚦 GATE 2 (integrity)
   index-integrity-auditor-agent    cross-layer graph consistency       → INDEX_AUDIT.md
                          │
                          ▼  (card is now a trustworthy KB entry)
```


creators/ (4 — one per DIKW layer)
----------------------------------

| Agent | Calls skill | Sole deliverable |
|-------|-------------|------------------|
| `card-creator-data-agent`        | `haipipe-insight-data`        | one 🟦 D card |
| `card-creator-information-agent` | `haipipe-insight-information` | one 🟩 I card |
| `card-creator-knowledge-agent`   | `haipipe-insight-knowledge`   | one 🟨 K card |
| `card-creator-wisdom-agent`      | `haipipe-insight-wisdom`      | one 🟧 W card |

Each is THIN: call the layer skill (headless) → verify the card → return.
The card schema + filing logic stay in the SKILL; the creator never re-implements them.


reviewers/ (4 per-type + 1 cross-layer)
---------------------------------------

| Agent | Gate | Reviewer | Sole deliverable |
|-------|------|----------|------------------|
| `card-reviewer-data-agent`        | 🟦 D card | Codex (accuracy) + self (style) | `D_CARD_REVIEW.md` |
| `card-reviewer-information-agent` | 🟩 I card | Codex + self | `I_CARD_REVIEW.md` |
| `card-reviewer-knowledge-agent`   | 🟨 K card | Codex + self | `K_CARD_REVIEW.md` |
| `card-reviewer-wisdom-agent`      | 🟧 W card | Codex + self | `W_CARD_REVIEW.md` |
| `index-integrity-auditor-agent`   | cross-layer graph | self (checklist) | `INDEX_AUDIT.md` |

Each per-type reviewer checks **accuracy** (card ≤ cited evidence — Codex
re-reads the sources) + **boundary/style** (conforms to its layer in
`../ref/dikw-boundaries.md` + `../ref/insight-md-schema.md`). None judges
VALIDITY ("is the claim true?") — that was D_probe's `review` upstream.


filer ≠ judge
-------------

A creator files and stops; a different agent (Codex-backed for accuracy) judges
it. The filer rationalizes its own overclaim; an independent context does not.
Never let a creator review its own card.


Registration & invocation
--------------------------

Real files live here (`creators/`, `reviewers/`). The plugin top-level `agents/`
holds **flat symlinks** so each is callable as a `subagent_type` (for fan-out:
`agent_type:"card-reviewer-knowledge-agent"`). Nested subfolders are for humans;
the flat symlinks are for the harness. Same convention as C_task and D_probe.
