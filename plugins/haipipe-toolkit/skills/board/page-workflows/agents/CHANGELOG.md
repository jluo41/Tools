## 2026-09-04 · canonical Page dependency order

- Align all five phase agents with Page → router → phase → owning workflow →
  exact Page Face owner → policy/worker → presenter ordering, loading one
  canonical family owner only once when it also owns the Folder.
- Require phase routes and target cycles to remain separate in their shared
  producer receipt.

## haipipe-page-outline-agent 0.3.1 · haipipe-page-evidence-agent 0.3.1 — 2026-09-02

- Outline SURVEY now plans exact PageX bindings beside Supporting Runs, while
  Evidence LAND validates and freezes them before the one local item Run.
- Both producers keep PageX outside Run and Result cardinality and route its
  lane law through the unified Evidence Plugin.

## haipipe-page-outline-agent 0.3.0 · haipipe-page-evidence-agent 0.3.0 — 2026-09-01

- Outline agent specifies typed Evidence Items at SHAPE and plans their
  Supporting/Local Run graphs at SURVEY without allocating Runs.
- Evidence agent executes support → frozen input → one local Result at LAND
  and limits EMBED to interpreting ready local Results.

## haipipe-page-outline-agent 0.2.0 · haipipe-page-evidence-agent 0.2.0 — 2026-09-01

- Each phase agent owns its phase's two cycles (outline: SHAPE, SURVEY;
  evidence: LAND, EMBED) and returns `cycle:` beside `phase:`.
  haipipe-page-probe-agent retired to `_old/` (its installed link removed).

## haipipe-page-outline-agent · haipipe-page-draft-agent — 2026-08-31

- Descriptions aligned with the rewritten phase contracts: the outline agent
  runs FIVE checks and writes the plan, the open `D<nn>` threads and one log
  record (not "ONE file"); the draft agent turns a Section slot into one
  sentence ending `<!-- realizes: … -->` with a `> Value:` lane per number, no
  hole token, and folds the diff under one log record.

## haipipe-page-probe-agent 0.3.0 — 2026-08-20

- **REVERSES 0.2.0's no-Agent-tool design, hours later, on JL's refinement**
  ("一般来说应该是由 Page Probe Agent 去做这件事，不会有其他的 skill 或 agent
  call 这个 haipipe-probe"): the producer now HOLDS the Agent tool, scoped to
  ONE callee — haipipe-probe-q-executor-agent — and is the ONLY page-family
  hand that loads haipipe-probe or hands the collector a batch. The crossing
  is layered: producer → collector → orchestrators, one door at each level.

## haipipe-page-probe-agent 0.2.0 — 2026-08-20

- **Prepares the crossing, never performs it** (JL ruling A, 260820): the
  producer returns a dispatch batch for haipipe-probe-q-executor-agent, the
  probe layer's one door; holding no Agent tool is now BY DESIGN, not a gap.
  0.1.0 promised "dispatches the stripped question" while lacking the tool to
  do it — the defect that surfaced this whole seam audit.

## 0.14.0 — 2026-08-19

- **The producer's shared law moved out of the creator agent** into
  `ref/producer-contract.md`: packet, procedure, house rules, return shape.
  Every phase agent (and the fallback) now loads only CONTRACTS — no agent
  reads another agent's file any more, which was the one roster relationship
  JL could not hold ("is this for the board or for the page?").
  `haipipe-page-creator-agent` 0.10.0 keeps only its two verbs.
- **`haipipe-page-orchestrator-agent` → `haipipe-page-auditor-agent`**: it
  validates the packet, stores receipts, and runs the lifecycle auditor; it
  cannot dispatch the loop (subagents get no Workflow tool), so "orchestrator"
  named a power it lacks. The check agent's base stays the reviewer file until
  the judge side earns the same carve-out.
- Same-night: README gains the "Stand-in rule" section — an agent type not registered in the running session is executed by a general-purpose stand-in that first reads the agent file as identity plus ref/producer-contract.md, with the receipt's actor naming the ROLE; the 260819 run used exactly this pattern.

## 0.13.0 — 2026-08-19

- **Two agents renamed to say what they are** (JL: "is this for the board or
  for the page? I am confused"): `haipipe-board-creator-agent` →
  `haipipe-page-creator-agent` (0.9.0) and `haipipe-board-approver-agent` →
  `haipipe-page-approver-agent`. Both are 100%% page-scoped — the creator never
  touches board.md, and every tick the approver checks lives on one page's
  artifacts. `haipipe-board-reviewer-agent` alone keeps `board`, because its
  board-wide jobs (mechanical checker, opening cold reads) are real. Old
  receipts naming the old actor strings stay auditable; CHANGELOG history is
  untouched. The broken root symlink `agents/haipipe-board-page-orchestrator-
  agent.md` (target renamed long ago) was deleted.

# page-workflows/agents

## 0.1.0 — 2026-08-19

- 0.1.0 add-on, same day: `haipipe-page-check-agent` joins as the sixth, the
  page-scoped half of `haipipe-board-reviewer-agent` (split, not rename: the
  reviewer keeps whole-board jobs and stays the judge's base).
- Born, all five: JL ruled the producer breaks down per phase ("for the
  creator-agent, it should have the outline-agent, etc."). Each file is a THIN
  wrapper — identity, skill chain, role walls, receipt duty — and restates no
  contract content, because a restated table is a mirror and every mirror on
  this board drifted within a day. `haipipe-board-creator-agent` stays as the
  shared base (packet, procedure, house rules, return contract) and keeps the
  non-phase verbs: `create-page` and `revise-opening`.
## 2026-09-04 · five-phase Page workflow

- Add `haipipe-page-context-agent` for 00 CONTEXT/PREPARE.
- Add `haipipe-page-content-agent` for 03 CONTENT/WRITE.
- Remove PageX from OUTLINE/SURVEY and EVIDENCE/LAND agent contracts.
- Keep DRAFT and REVISE agent names only for historical receipt compatibility;
  new dispatch uses CONTENT.
