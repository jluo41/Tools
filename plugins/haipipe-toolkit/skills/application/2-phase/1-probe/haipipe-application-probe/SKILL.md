---
name: haipipe-application-probe
description: "PROBE phase worker (internal). Called by application stage skills after DRAFT to collect what the draft needs but does not have -- evidence for claims, context for the seed, materialized outputs for displays. ONE pipeline: ACQUIRE through Agent(haipipe-probe-orchestrator-agent) (the project-side evidence gateway) is the only door; HARVEST transcribes the return's pointers through venue-scaled lane hooks (values always; citation for sectioned venues; display for display-unit venues -- hooks, not sub-skills). Fully automatic, human review in CHECK only. Users invoke stage skills (seed, claims, ...), not this skill directly."
argument-hint: "[from-buffer <intervention-root> [PPNN] | stage <stage-name>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Agent
metadata:
  version: "2.4.0"
  last_updated: "2026-07-09"
  summary: "2.4.0: task_landing adds the config-variant rule (segment/dataset-agnostic task names; slice + input path = config keys; new subgroup = new config, not a new folder). 2.3.0: dispatch prompt carries task_landing (granularity ladder: config > task > group; one need = one task/config). 2.2.0 (GROW loop): values lane redirects to _DESCRIPTIONS/DS<n> profile sheets for rung 1a (same debt bookkeeping). 2.1.0 (bench rulings 2026-07-09): STEP 1.5 RELEASE GATE -- planned cards dispatch only on the user's explicit release (roster presented + stop otherwise); PHI-adjacent task dispatches pin the minimal aggregate-safe column allow-list by default (no operator ask). 2.0.0 Round-2 paper-alignment (SOP R1+R5; port of paper probe 3.1.0): 4-step procedure (BOOKKEEP -> DISPATCH -> TRANSLATE -> VERIFY), each step ending in a mandatory PROOF shown in the reply; deterministic checker (check-probe-cards.sh, family-local fork) run at VERIFY and re-run by the stage gate; lane debts `harvest: OWED` written before transcription; harvester vocabulary (ACQUIRE via gateway is the only door -> HARVEST follows pointers). Application deltas kept: no sub-worker skills -- venue-scaled lane hooks (_VALUES_ always; _CITATION_ sectioned venues; _DISPLAY_ display-unit venues) bound to paper's 2.0.0 sub-worker contract; claims C-line + Evidence Campaign flip at TRANSLATE."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-probe (PROBE phase worker, internal)
================================================================

Called by stage skills (seed, claims, venue, pitch, narrative, display, section-edit) after DRAFT to collect what the draft needs but does not have.
The stage defines WHAT needs collecting; this skill defines HOW.
ONE pipeline (JL 2026-07-07 harvester ruling, ported from paper: the workers "are the harvester agents... they don't restart the whole probe process, they are just one step within the whole probe"):

```
ACQUIRE (project-side, the ONLY door)   Agent(haipipe-probe-orchestrator-agent)
                                        -> gateway SWEEP (reuse|enrich|fresh)
                                        -> discovery/task orchestrators
                                        -> evidence LANDS in discoveries/ tasks/ insights/
HARVEST (intervention-side, pointer-following; venue-scaled HOOKS, not sub-skills)
  values    value refs -> _VALUES_{stage}.md                     (always)
  citation  pick_list  -> _CITATION_{stage}.md                   (sectioned venues only)
  display   unit refs  -> _DISPLAY_{stage}.md + artifact links   (display-unit venues only)
```

Intervention-side may FOLLOW pointers the return names; only the gateway may FIND things.
A hook that notices a gap reports it as a probe-plan suggestion, never fills it itself.

Not user-facing: users invoke stage skills; stages call this. `/haipipe-application probe run [PPNN]` reaches it via the router's `from-buffer` dispatch.
Which stage runs which mode, seed/claims/venue specifics, venue-scaled lane rules, phase-status strip forms: `ref/per-stage-dispatch.md`.

The Procedure (from-buffer entry)
----------------------------------

`Skill("haipipe-application-probe", args="from-buffer <intervention_root> [PPNN]")` -- the ONLY path that dispatches probe plans.
Stage skills and the umbrella NEVER call /haipipe-probe or evidence agents directly.

Four steps. **Each ends with a PROOF the worker MUST show in its reply. A step whose proof is absent did not happen, no matter what the prose claims.**
This worker does NO evidence work of its own: never searches, never sweeps discoveries/tasks/insights inline, never writes findings into a PP card from its own context. Findings enter cards ONLY from the orchestrator's return.

**STEP 0 -- RE-INVOKE PER RUN.**
Every PROBE phase invokes this skill fresh via the Skill tool, even when its text is already in context from an earlier stage of the same session (paper-side stale-copy incident: a PP card ran a 3-hour-old contract).

**STEP 1 -- BOOKKEEP.**
- Read the index `<intervention_root>/1-probe-plans/README.md`; resolve each planned item to its `0-lifecycle/<stage>/_PROBE/PPNN_*.md` card (or the named PPNN).
- Resolve `project_root`: walk UP from intervention_root to the FIRST ancestor containing `discoveries/`. Do NOT use `git rev-parse --show-toplevel` -- repo-backed projects make it return the wrong root. (`check-probe-cards.sh` resolves the same way; when in doubt run it.)
- Ensure each PP card exists with the anatomy from `../../../../probe/haipipe-probe/SKILL.md` ("PPNN card anatomy") -- READ that section, never re-derive from memory. At BOOKKEEP a card carries stage/mode/status/claim + Need/Why/Route, an EMPTY `refs:`, and NO tables. A card with findings already in it at BOOKKEEP is a shortcut -- reset it.

PROOF 1: print `project_root=<path>` + the output of `ls <project_root>/discoveries/`.

**STEP 1.5 -- RELEASE GATE (JL bench ruling 2026-07-09: "stop after the draft... I would like to review the probes to be released").**
Planned cards are RELEASED by the user, never auto-dispatched. A user-issued `probe run PPNN` (or "release PP02" / "release all") IS the approval for the named card(s). A stage's DRAFT->PROBE handoff, or a bare `from-buffer` sweep with no user-named card, must STOP here: present the planned roster (PP id -- question -- mode -- route), end the turn, and await the user's pick. Record each release in the stage `_LOG` (`[RELEASE] PPNN approved <date>`). No exception for "cheap" probes -- discovery scans are releases too. Normally the user already picked from the RELEASE MENU the DRAFT worker presented at its close (draft step 5); this gate is the backstop for paths that skip DRAFT (--refresh, backfill, direct probe run).

PROOF 1.5: either the user's release words quoted (which card, where they said it) or the presented roster + stop.

**STEP 2 -- DISPATCH.**
One call per PP card (batch independent cards in one turn):

```
Agent(haipipe-probe-orchestrator-agent, run_in_background=<true for fresh>, prompt="
  project_root: <from STEP 1 -- the dir with discoveries/>
  mode: light            # 'full' only for claims committed verdicts
  task_landing: config variant on an existing task > new task in the existing
                group > new group (last resort). One need = ONE task/config --
                never a fan of sibling scaffolds for related queries. Task
                names are SEGMENT/DATASET-AGNOSTIC (arm_engagement, never
                young_male_arm_engagement): the slice + input dataset are
                config keys -- configs/<variant>.yaml + runs/run_<variant>.sh
                (one config = one run, results name-paired); a new subgroup
                or same-shape dataset = a new config, not a new folder.
  plan: |
    <the PP card's Need + Why + Route, verbatim>
")
```

- This dispatch is the ONLY door -- audit-shaped scopes ("re-verify the set", "double-check the refs") included; the agent's SWEEP answers those from the ledger. Never invent a side-channel worker (generic web-search agents etc.).
- The agent decides reused|enriched|fresh in its own SWEEP, clean context -- never pre-chew the shape, never paste discoveries into the prompt.
- PHI-adjacent task plans (row-level health data input): the dispatch prompt pins the MINIMAL aggregate-safe column allow-list the Need requires and states that outputs must be aggregates only. Restricted-by-default is NOT a question for the operator (bench ruling 2026-07-09: the restricted-vs-full ask was noise mid-flow); org PHI gates apply on top and are never overridden from here.
- Likely-fresh plans (new searches / landscape / task run) dispatch `run_in_background=true`; sync on a fresh run froze a paper session 25 minutes. When unsure, go background; TRANSLATE runs when it returns. RULE OF THUMB: if `<project_root>/discoveries/` is empty (or holds only `.gitkeep`), EVERY plan is fresh -- set `run_in_background=true` on all of them, and do not report a dispatch as "background" unless the call actually carried the flag (the label must match the call).
- Card `status: dispatched`; update the index row.

PROOF 2: the literal Agent(...) call(s) visible in the transcript -- one per PP card.

**STEP 3 -- TRANSLATE** (probe is application-unaware; this worker is the bilingual layer).
- Light return: <=5 anchored takeaway lines into the card; `status: read`.
- `refs:` = EXACTLY the paths the return names (discoveries/.../sources.md, tasks/...); verify each with `ls <project_root>/<ref>`. A return with NO refs means the evidence never landed project-side: the card goes `status: failed (no project-side evidence)` and the phase is NOT green. Takeaways with empty `refs:` are the exact shortcut this contract prevents.
- **LANE OBLIGATIONS -- write the debt into the card FIRST, then pay it.** When the return carries harvestable content for a lane the venue fires (see "Venue-hook contract" below), IMMEDIATELY record it on the card as a lane line (this is what makes a skipped harvest checkable):
  ```
  - value_refs: tasks/X03_cohort_summary/results/summary.csv · harvest: OWED    (values lane, always)
  - pick_list:  S01,S02,S03 · harvest: OWED                      (citation lane, sectioned venues)
  - unit_refs:  0-artifacts/fig-overview · harvest: OWED         (display lane, display-unit venues)
  ```
  Then dispatch the lane's harvester hook as a subagent (cheap tier, pointer-following only -- see the venue-hook contract) and accept MECHANICALLY per `ref/harvest-acceptance.md` (run the greps, never eyeball). On acceptance flip the line: `harvest: accepted (<n> entries, <doc>)`. A lane line still saying `OWED` at VERIFY is a checker FAIL -- the phase cannot go green over a skipped harvest (paper seed-incident rule, JL 2026-07-07).
- Full return: verdict block (G1/G2/G3 + verdict + reasoning + judged-by + date) lands in the card's `## Verdict`; `status: verdicted`; the claims ledger's C-line AND its Evidence Campaign row flip in the same pass (enum: `supported | refuted | inconclusive`).
- This worker reads no project files; `ls` for existence only, never content. Sections / round logs backfill from the card, never from memory. Buffer + index convention: `../../../haipipe-application/fn/probe-plans.md`.

PROOF 3: per-card `refs:` line + the `ls` results, PLUS -- for every lane line written -- the harvester Agent(...) call and its acceptance-grep output. A card with a lane line and no harvest proof means STEP 3 did not finish.

**STEP 4 -- VERIFY** (deterministic; the stage CHECK gate re-runs the same script).

```
sh <this-skill-dir>/check-probe-cards.sh <intervention_root> [<project_root>]
```

Checks: read/verdicted cards have resolving refs; planned/dispatched cards FAIL (probe-not-run); `harvest: OWED` lane lines FAIL (harvest skipped); no markdown tables in any card; no card over 80 lines; `status: failed` surfaced; working docs (_CITATION_/_VALUES_/_DISPLAY_) carry no bibtex, _CITATION_ no tables.
Any FAIL -> fix or surface it; NEVER report a green PROBE over a FAIL.
The stage CHECK gate re-runs this same script (wired in haipipe-application-check).

PROOF 4: the checker output pasted in the reply.

Venue-hook contract (application delta: hooks, not sub-worker skills)
----------------------------------------------------------------------

Application keeps NO probe sub-worker skills; the three HARVEST lanes are venue-scaled hooks inside this worker. Which lanes fire is decided at lane CREATION (TRANSLATE), from the pinned venue -- the checker stays presence-driven and needs no venue lookup:

- `_VALUES_` lane -- ALWAYS eligible: any venue's artifact quotes numbers, and claims-rung verified values land in `_VALUES_1c-claims.md` regardless of venue. RUNG 1a REDIRECT (GROW loop, 2026-07-09): descriptions-stage probes land this lane in `_DESCRIPTIONS/DS<n>_<name>.md` (per-dataset profile sheet: field inventory + Field Disposition + readable landed profile; quoted-only, every line anchored + dated) -- same OWED/accepted debt bookkeeping, different home; the 1a doc itself stays one-line D entries.
- `_CITATION_` lane -- SECTIONED venues only (report/dashboard-like, per the venue profile). Pre-pin stages (seed and the 1a-1d ladder are venue-FREE) keep source anchors in the card takeaways; no _CITATION_ doc exists before a sectioned venue is pinned.
- `_DISPLAY_` lane -- only if the venue's artifact has display units (panels, charts, figures). Simple venues (sms/push/reminder) have no document lanes at all: their PROBE phase is claims-evidence only.

When a hook fires it MUST follow paper's 2.0.0 sub-worker contract (haipipe-paper-probe-citation/-values/-display): pointer-following + gateway dispatch only, mechanical acceptance greps, no inline search -- the hook NEVER searches (no WebSearch, no Semantic Scholar; finding is the gateway's monopoly), transcribes only what the gateway's return points at, and is accepted by the LITERAL greps in `ref/harvest-acceptance.md`. Card format specs are read from their single source of truth, never paraphrased into the dispatch prompt.

Hard boundaries (inherited by all stages)
-------------------------------------------
- NEVER generate bibtex; _CITATION_ is plain text only
- NEVER fabricate numbers; NEVER create ad-hoc plots inline; NEVER write insight cards (deposits belong to the probe/insight side)
- NO markdown tables in PP cards, _CITATION_, or any probe/discovery document (JL standing rule) -- bullet lines only, one per source
- NO inline search in the PROBE phase -- durability is the whole point here; the orchestrator dispatch is the only door. (DRAFT may WebSearch to orient; the difference is card durability, not the search verb. DRAFT search feeds prose + `status: planned` skeletons; PROBE lands `read` cards with refs.)
- Never dispatch discovery/task orchestrator agents directly from a stage skill -- this worker is the ONLY door: stage -> this worker -> gateway -> discovery/task during probe's own Gather. A stage that calls `Agent(haipipe-discovery-orchestrator-agent)` or `/haipipe-probe` itself is bypassing the evidence contract (results land nowhere reviewable and die with the reply).
- All flags (uncertain values, unverified sources) resolve in CHECK, not here

Return contract
---------------

```
status:    ok | blocked
stage:     <stage-name>
lanes:     val <status> [· cite <status> · disp <status> -- only lanes the venue fires]
cards:     PPNN <status> · refs <n>/<n> resolved
next:      <suggested command>
```

Reference
---------

```
ref/per-stage-dispatch.md   stage->mode map · seed/claims/venue specifics ·
                            venue-scaled lane rules · phase-status strip forms
ref/harvest-acceptance.md   lane-hook dispatch + the LITERAL acceptance greps
check-probe-cards.sh        the STEP 4 / stage-gate verifier (family-local fork)
../../../../probe/haipipe-probe/SKILL.md         PPNN card anatomy (single source of truth)
../../../haipipe-application/fn/probe-plans.md   buffer + index convention
```

Siblings: DRAFT (haipipe-application-draft) -> PROBE (this) -> REVISE (haipipe-application-revise) -> CHECK (haipipe-application-check).
PROBE reads the DRAFT outline; REVISE weaves PROBE outputs into the artifact; CHECK verifies all PROBE flags.
