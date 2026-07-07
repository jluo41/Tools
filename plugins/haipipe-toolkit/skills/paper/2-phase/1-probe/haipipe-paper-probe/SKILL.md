---
name: haipipe-paper-probe
description: "PROBE phase worker (internal). Called by stage skills after DRAFT to collect what the draft needs but does not have -- internal materials (values from task results, display units) and external ones (citations, discovery lit). Document workers (citation/values/display) plus dispatch through /haipipe-probe (the project-side evidence gateway) via Agent(haipipe-probe-orchestrator-agent). Fully automatic, human review in CHECK only. Users invoke stage skills (seed, claims, pitch...), not this skill directly."
argument-hint: "[from-buffer <paper_root> [PPNN] | stage-or-section [paper-path]]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "3.1.0"
  last_updated: "2026-07-07"
  summary: "PROBE phase worker rebuilt as a 4-step procedure (BOOKKEEP -> DISPATCH -> TRANSLATE -> VERIFY), each step ending in a mandatory PROOF shown in the reply, plus a deterministic checker (check-probe-cards.sh) run at VERIFY and re-run by the stage gate. Reference prose moved to ref/. v3.0: enforcement is mechanical, not prose -- a step without its proof did not happen. v3.0.1 (post test-12334535): checker brace-aware; fresh dispatch forces background; no-bibtex grep anchored. v3.0.2: hard boundary clarified -- no inline search in PROBE. v3.1: harvester model (JL Part-0 ruling) -- ONE pipeline, workers are the HARVEST step; TRANSLATE writes per-lane OWED obligations into the card before paying them; PROOF 3 covers harvest; checker FAILs owed lanes + planned cards."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-probe (PROBE phase worker, internal)
==========================================================

Called by stage skills (seed, claims, pitch, narrative, display, section-edit)
after DRAFT to collect what the draft needs but does not have.
The stage defines WHAT needs collecting; this skill defines HOW.
ONE pipeline (JL 2026-07-07 harvester ruling: the workers "are the harvester
agents... they don't restart the whole probe process, they are just one step
within the whole probe"):

```
ACQUIRE (project-side, the ONLY door)   Agent(haipipe-probe-orchestrator-agent)
                                        -> gateway SWEEP (reuse|enrich|fresh)
                                        -> discovery/task orchestrators
                                        -> evidence LANDS in discoveries/ tasks/ insights/
HARVEST (paper-side, pointer-following) citation  pick_list  -> _CITATION_{stage}.md
                                        values    value refs -> _VALUES_{stage}.md
                                        display   unit refs  -> _DISPLAY_{stage}.md + tex links
```

Paper-side may FOLLOW pointers the return names; only the gateway may FIND
things. A harvester that notices a gap reports it as a probe-plan suggestion,
never fills it itself.

Not user-facing: users invoke stage skills; stages call this.
Which stage runs which workers/mode, seed/claims specifics, section-edit
worker logic, phase-status strip forms: `ref/per-stage-dispatch.md`.

The Procedure (from-buffer entry)
----------------------------------

`Skill("haipipe-paper-probe", args="from-buffer <paper_root> [PPNN]")` --
the ONLY path that dispatches probe plans.
Stage skills and the umbrella NEVER call /haipipe-probe or evidence agents directly.

Four steps. **Each ends with a PROOF the worker MUST show in its reply.
A step whose proof is absent did not happen, no matter what the prose claims.**
This worker does NO evidence work of its own: never searches, never sweeps
discoveries/tasks/insights inline, never writes findings into a PP card from
its own context. Findings enter cards ONLY from the orchestrator's return.

**STEP 0 -- RE-INVOKE PER RUN.**
Every PROBE phase invokes this skill fresh via the Skill tool, even when its
text is already in context from an earlier stage of the same session
(stale-copy incident: test-123333333 PP02 ran a 3-hour-old contract).

**STEP 1 -- BOOKKEEP.**
- Read the index `<paper_root>/1-probe-plans/README.md`; resolve each planned
  item to its `0-lifecycle/<stage>/_PROBE/PPNN_*.md` card (or the named PPNN).
- Resolve `project_root`: walk UP from paper_root to the FIRST ancestor
  containing `discoveries/`. Do NOT use `git rev-parse --show-toplevel` --
  repo-backed papers are their own git repos, so it returns paper_root itself.
  (`check-probe-cards.sh` resolves the same way; when in doubt run it.)
- Ensure each PP card exists with the anatomy from
  `../../../../probe/haipipe-probe/SKILL.md` ("PPNN card anatomy") -- READ that
  section, never re-derive from memory. At BOOKKEEP a card carries
  stage/mode/status/claim + Need/Why/Route, an EMPTY `refs:`, and NO tables.
  A card with findings already in it at BOOKKEEP is a shortcut -- reset it.

PROOF 1: print `project_root=<path>` + the output of `ls <project_root>/discoveries/`.

**STEP 2 -- DISPATCH.**
One call per PP card (batch independent cards in one turn):

```
Agent(haipipe-probe-orchestrator-agent, run_in_background=<true for fresh>, prompt="
  project_root: <from STEP 1 -- the dir with discoveries/>
  mode: light            # 'full' only for claims committed verdicts
  plan: |
    <the PP card's Need + Why + Route, verbatim>
")
```

- This dispatch is the ONLY door -- audit-shaped scopes ("re-verify the set",
  "double-check the refs") included; the agent's SWEEP answers those from the
  ledger. Never invent a side-channel worker (generic web-search agents etc.).
- The agent decides reused|enriched|fresh in its own SWEEP, clean context --
  never pre-chew the shape, never paste discoveries into the prompt.
- Likely-fresh plans (new searches / landscape / task run) dispatch
  `run_in_background=true`; sync on a fresh run froze a session 25 minutes
  (test-2-2222). When unsure, go background; TRANSLATE runs when it returns.
  RULE OF THUMB: if `<project_root>/discoveries/` is empty (or holds only
  `.gitkeep`), EVERY plan is fresh -- set `run_in_background=true` on all of
  them, and do not report a dispatch as "background" unless the call actually
  carried the flag (test-12334535 ran three sync dispatches while PROOF 2
  claimed "all background" -- the label must match the call).
- Card `status: dispatched`; update the index row.

PROOF 2: the literal Agent(...) call(s) visible in the transcript -- one per PP card.

**STEP 3 -- TRANSLATE** (probe is paper-unaware; this worker is the bilingual layer).
- Light return: <=5 anchored takeaway lines into the card; `status: read`.
- `refs:` = EXACTLY the paths the return names (discoveries/.../sources.md,
  tasks/...); verify each with `ls <project_root>/<ref>`. A return with NO refs
  means the evidence never landed project-side: the card goes
  `status: failed (no project-side evidence)` and the phase is NOT green.
  Takeaways with empty `refs:` are the exact shortcut this contract prevents.
- **LANE OBLIGATIONS -- write the debt into the card FIRST, then pay it.**
  When the return carries harvestable content, IMMEDIATELY record it on the
  card as a lane line (this is what makes a skipped harvest checkable):
  ```
  - pick_list:  S01,S02,S03 · harvest: OWED        (citation lane)
  - value_refs: tasks/T03/results/summary.csv · harvest: OWED   (values lane)
  - unit_refs:  0-displays/fig-overview · harvest: OWED         (display lane)
  ```
  Then dispatch the matching harvester subagent (cheap tier, reads its worker
  SKILL.md headless -- same pattern for all three lanes) and accept
  MECHANICALLY per `ref/harvest-acceptance.md` (run the greps, never eyeball).
  On acceptance flip the line: `harvest: accepted (<n> entries, <doc>)`.
  A lane line still saying `OWED` at VERIFY is a checker FAIL -- the phase
  cannot go green over a skipped harvest (seed-incident rule, JL 2026-07-07).
- Full return: verdict block (G1/G2/G3 + verdict + reasoning + judged-by +
  date) lands in the card's `## Verdict`; `status: verdicted`; the claims
  ledger's C-section flips in the same pass.
- This worker reads no project files; `ls` for existence only, never content.

PROOF 3: per-card `refs:` line + the `ls` results, PLUS -- for every lane line
written -- the harvester Agent(...) call and its acceptance-grep output. A card
with a lane line and no harvest proof means STEP 3 did not finish.

**STEP 4 -- VERIFY** (deterministic; the stage CHECK gate re-runs the same script).

```
sh <this-skill-dir>/check-probe-cards.sh <paper_root> [<project_root>]
```

Checks: read/verdicted cards have resolving refs; planned/dispatched cards FAIL
(probe-not-run); `harvest: OWED` lane lines FAIL (harvest skipped); no markdown
tables in any card; no card over 80 lines; `status: failed` surfaced; working
docs (_CITATION_/_VALUES_/_DISPLAY_) carry no bibtex, _CITATION_ no tables.
Any FAIL -> fix or surface it; NEVER report a green PROBE over a FAIL.
The stage CHECK gate re-runs this same script (wired in haipipe-paper-check).

PROOF 4: the checker output pasted in the reply.

Hard boundaries (inherited by all workers)
-------------------------------------------
- NEVER generate bibtex or touch .bib; _CITATION_ is plain text only
- NEVER fabricate numbers; NEVER create ad-hoc plots inline
- NO markdown tables in PP cards, _CITATION_, or any probe/discovery document
  (JL standing rule) -- bullet lines only, one per source
- NO inline search in the PROBE phase -- durability is the whole point here;
  the orchestrator dispatch is the only door. (DRAFT may WebSearch to orient;
  the difference is card durability, not the search verb. DRAFT search feeds
  prose + `status: planned` skeletons; PROBE lands `read` cards with refs.)
- All flags (🔍 unverified citations, ⚠️ uncertain values) resolve in CHECK, not here

Return contract
---------------

```
status:    ok | blocked
section:   <stage-or-section>
workers:   cite <status> │ val <status> │ disp <status>
cards:     PPNN <status> · refs <n>/<n> resolved
next:      <suggested command>
```

Reference
---------

```
ref/per-stage-dispatch.md   stage->worker/mode map · seed/claims specifics ·
                            section-edit logic · phase-status strip forms
ref/harvest-acceptance.md   citation harvest dispatch + the LITERAL acceptance greps
check-probe-cards.sh        the STEP 4 / stage-gate verifier
../../../../probe/haipipe-probe/SKILL.md   PPNN card anatomy (single source of truth)
```

Siblings: DRAFT (haipipe-paper-draft) -> PROBE (this) -> REVISE (haipipe-paper-revise) -> CHECK (haipipe-paper-check).
PROBE reads the DRAFT outline; REVISE weaves PROBE outputs into prose; CHECK verifies all PROBE flags.
