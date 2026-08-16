# haipipe-application-probe · v0.3.2
state: 🔴 OPEN
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
haipipe-application-probe is a shipped unit: what does it still owe, and is it healthy?

Write here what this unit is for in one paragraph a stranger could follow, why it exists on its own rather than as part of its neighbour, and what would have to be true for it to be considered finished.
The generated sections answer what it IS; only this one can answer whether it is any good.
`Opening` is the lead section's ONE name on every page kind (JL 260731: "just one single Opening"); `Question` survives only as a legacy alias for pages written before the rename.

## Writing Style
English only. One sentence per source line. Describe the shipped unit factually and keep generated inventory separate from human health judgment.

## Diagram
<!-- haipipe:skill:tree:start 7403c62bfdd40ed1 application/2-phase/1-probe/haipipe-application-probe -->

```
haipipe-application-probe/
  ref/
    harvest-acceptance.md    26 ln  Harvest — no sidecar (haipipe-application-probe, ⑤ INTERPRET)
    per-stage-dispatch.md    99 ln  Per-stage dispatch reference (haipipe-application-probe)
  CHANGELOG.md               78 ln  haipipe-application-probe — Changelog
  check-probe-cards.sh      679 ln
  SKILL.md                  174 ln  Skill: haipipe-application-probe — the PROBE-phase worker for an application
```

<!-- haipipe:skill:tree:end -->

```
WORKFLOW  (authored: a folder can be read off disk, an intent cannot)
Draw how this skill is actually used: the entry point, what it reads,
what it writes, and where it hands off. Delete this fence if the tree
above is the whole story.
```

## Content
<!-- haipipe:skill:body:start 7403c62bfdd40ed1 application/2-phase/1-probe/haipipe-application-probe -->

**haipipe-application-probe** · `0.3.2` · last shipped 2026-07-19

- folder   `application/2-phase/1-probe/haipipe-application-probe/`
- tools    Bash, Read, Write, Edit, Grep, Glob, Skill, Agent
- summary  The intervention's PROBE-phase worker — runs ③DISPATCH→④POINT→⑤INTERPRET for an application (DRAFT authored ①ORGANIZE+②MATCH; the plan is executed, not re-matched). The model (anatomy, QA contract, cost ladder, LAWS, states, checker codes) belongs to probe: ../../../../probe/haipipe-probe/SKILL.md. This file is only the application-side deltas: intervention_root, the DIKW-ladder rungs, and no-sidecar harvest (folds into a-executor). History: ./CHANGELOG.md.

### SKILL.md



Skill: haipipe-application-probe — the PROBE-phase worker for an application
============================================================================

Called by application stage skills (seed, descriptions, themes, claims, venue, pitch, narrative, display, section-edit) after DRAFT.
DRAFT raised the Q-consumer questions in the stage doc and stopped there. THIS worker owns everything probe-shaped: ①ORGANIZE each Q-consumer into an ENTRY, ②MATCH it against the bank (read-only grep), ③DISPATCH only what the ceiling allows, ④POINT, ⑤INTERPRET.

⭐ THE MODEL IS NOT THIS FILE'S — it is `probe`'s: `../../../../probe/haipipe-probe/SKILL.md`.
Read it for the probe-file anatomy, the QA state-line contract, the cost ladder, the two LAWS, the derived states, and the checker's FAIL codes.
This file is ONLY how an application runs the loop, plus the application-side deltas `probe` does not cover.

Not user-facing: users invoke stage skills; a stage calls `Skill("haipipe-application-probe", args="from-buffer <intervention_root> [PPNN]")`.
Which rung runs which lanes, seed/claims specifics, and section-edit logic: `ref/per-stage-dispatch.md`.

The application-side deltas:
- `intervention_root` vocabulary, and the intervention's OWN registries (the T1 whitelist).
- the DIKW ladder rungs raise the questions (there is no resource stage; that is paper-only).
- harvest folds into the entry's `### a-executor` — no sidecar docs, no lanes (application delta).


Rules (follow these — the model is `probe`'s)
==============================================

The PROBE-phase rules live in `../../../../probe/haipipe-probe/SKILL.md` → **Phase rules · PROBE phase** (+ **The QA file**, **The two LAWS**). Follow those; on conflict, that file wins. Application-specific additions:
- Dispatch goes through the collector agent (`haipipe-probe-q-executor-agent`), NEVER an orchestrator called inline by this worker — results would die with the reply.
- Harvest folds into the entry's `### a-executor` — the answer's numbers/citations land INLINE there, anchored to `target:`; no sidecar docs, no `values:`/`sources:`/`displays:` lanes (application delta). See `ref/harvest-acceptance.md`.
- A claim's STATUS goes in `0-lifecycle/1c-claims/1c-claims.md`, written by the AUTHOR, NEVER in the probe file.
- No bibtex; no ad-hoc plots; no markdown tables in any probe document.

The loop below is the HOW-TO for these rules.


The loop, application-side — DRAFT authored ①②; this worker runs ③④⑤
====================================================================

Each step ends with a PROOF this worker MUST show in its reply; an absent proof means the step did not happen.
STEP 0 — re-invoke this skill fresh every run, even when its text is already in context (a probe once ran a 3-hour-old contract).

THE PHASE SPLIT (`probe`).
①ORGANIZE + ②MATCH happen HERE. Read the stage doc's Q-consumer and author each ENTRY: `### q-executor` (stake stripped, then FROZEN, + Deliverable/Accepted), `### q-consumer` bullets, `### bank binding` (`route`, `bank`, `target` — an existing path or `NEW <path>`). DRAFT authors none of it and never opens `1-probes/`.
This worker runs ③DISPATCH + ④POINT (COLLECT the answer from the bank, per `probe`) + ⑤INTERPRET (HARVEST it — write `### a-executor` and the stage-doc a-consumer). Collection is `probe`'s model; harvest is this worker's, and `probe` says nothing about it.


① + ② — DONE AT DRAFT (this worker's PRECONDITION)
-------------------------------------------------

The entries already exist under `<intervention_root>/1-probes/PPNN_<topic>/`, each carrying the DRAFT-authored plan. This worker READS them; it does not author or re-match them.
- Resolve `project_root`: walk UP from `intervention_root` to the first ancestor containing `discoveries/`.
  Do NOT use `git rev-parse` — a repo-backed project is its own git repo. (The checker resolves the same way.)
- Read each entry's `### bank binding` (`bank` + `target`) to route it: an existing `target:` path (bank `reuse`) → the answer may already be banked, go to ④/⑤ (verify then harvest); `target: NEW …` (bank `run`/`code`/`new`) → ③ DISPATCH.
- T1 LOCAL still runs inline (application-specific): a CLOSED whitelist of the intervention's OWN registries — entries already `read` (their `### a-executor`) · `0-artifacts/` display units · `1c-claims.md` campaign rows.
  Fully answered there → write `### a-executor`, set `answered-local`, do NOT dispatch. Adopt the POINTER, never the verdict (a reused value re-verifies against its ORIGINAL source at harvest).
- DISPLAY-shaped needs are REROUTED, not collected: a question asking for a display unit that does not exist becomes a request row for the display stage; close the entry `answered-local` with `### a-executor` "rerouted to display stage".

PROOF 1: `project_root=<path>` + `ls <project_root>/discoveries/` + `ls <intervention_root>/1-probes/`, and per entry its `bank` verdict + `target:` (existing→④/⑤ or NEW→③).


③ DISPATCH — hand the NEW entries to the collector agent
--------------------------------------------------------

For each STILL-COLLECTING entry (`target: NEW`, bank `run`/`code`/`new`, not resolved by T1 LOCAL), hand the SET to the collector agent, tagging each with the DRAFT-authored `route:` (task|discovery — AUTHORITATIVE, not a hint):

  ```text
  Agent(haipipe-probe-q-executor-agent, prompt="
    project_root: <from ①>
    probe_files:  <the PPNN files touched this run>
    dispatch:     <entry ids with target: NEW>, each with its route: task|discovery
  ")
  ```

The agent runs the stake-free middle in ITS OWN clean context: it sends each `### q-executor` VERBATIM to `Agent(haipipe-task-orchestrator-agent)` / `Agent(haipipe-discovery-orchestrator-agent)` (`run_in_background` for fresh work; omit the leaf for fresh — the orchestrator picks the folder and returns the path), and returns `{ entry → target: QA-path | in-flight | failed }`, having written each `target:`.
The agent does NOT re-run ②MATCH — the DRAFT `bank`/`target` already rooted each question; the agent DISPATCHES (the executor orchestrator's OWN QA-gate still dedups against an existing answer). It NEVER reads the intervention's registries, the stake, or the stage-doc Q-consumers — its clean context IS the wall; and it never authors a fresh folder (LAW 1).
The stage NEVER calls `haipipe-task-orchestrator-agent` / `haipipe-discovery-orchestrator-agent` ITSELF — the collector owns dispatch; a stage that dispatches inline lands results nowhere reviewable.

DEFERRED / ASYNC is the agent's too: an entry it cannot land synchronously comes back `in-flight` and stays `commissioned`; the NEXT PROBE run re-hands it. This worker writes NOTHING under `tasks/` or `discoveries/`, ever — no stub, no mailbox.

PROOF 3: the agent's per-entry dispatch / in-flight lines (from its return); NO orchestrator call appears in THIS worker's own transcript.


④ POINT — the agent wrote `target:`; the stage VERIFIES it on disk
------------------------------------------------------------------

The agent already wrote each resolved entry's `target:` (the FILE, never the folder). Before harvesting, VERIFY — do not trust the return blind (the state is the TARGET's state line, not the target's existence — open the file):
- `ls <project_root>/<target>` resolves, and `grep '^- state:' <target>` reads `answered` → ⑤.
- `working` → stays `commissioned`, report IN PROGRESS since `<started>` (dead past `QA_WORKING_TTL_HOURS` → re-hand to the agent next run).
- no QA-file path returned → `state: failed`, phase not green.
- a `commissioned` target that has since gone `answered` is a HARD FAIL (`commissioned-target-answered`) — harvest it now.

PROOF 4: per entry the `target:` line, the `ls` that resolves it, and `grep '^- state:' <target>`.

════════ COLLECTION (①–④) ends here — the answer is banked.
HARVEST (⑤) begins. ════════

⑤ INTERPRET — the a-executor, the stage-doc a-consumer, and the claim status
----------------------------------------------------------------------------

- Write `### a-executor` — a COPY of the answering QA file's answer, ONLY against an `answered`, non-superseded target (`probe`).
  HARVEST folds in here: write the answer's numbers / citations INLINE, each with its anchor `<value>  [→ <the entry's target QA file>]`.
  `target:` is already verified `answered` + non-superseded — that IS the fabrication anchor. No second transcription, no `values:`/`sources:`/`displays:` lane, no sidecar doc.
- Each Q-consumer this entry serves then writes its OWN a-consumer in its stage doc (station ②), anchored `[source: PP<NN>]` back to the `### a-executor` copy — the per-consumer interpretation UP into the intervention's words.
- The AUTHOR writes the claim status (`supported | refuted | inconclusive` + confidence) into `0-lifecycle/1c-claims/1c-claims.md`, flipping the C-line AND its Evidence Campaign row in the same pass — never in the probe file.
  A probe is communication, not judgment — there is no review gate; keep the overclaim check (never causal from associational evidence).
  The venue gate later reads THIS campaign against its settlement bar (light | medium | full).
- A display unit a question needs but that does not exist REROUTES to the display stage (a request row); do not invent an artifact here.
  Details: `ref/harvest-acceptance.md`.

PROOF 5: per entry the `### a-executor` line (with its inline `[→ target]` anchor), the stage-doc a-consumer it feeds, and the claim-ledger diff (if it serves a claim).


VERIFY — the checker (the stage CHECK gate re-runs the same script)
------------------------------------------------------------------

```
sh <this-skill-dir>/check-probe-cards.sh <intervention_root> [<project_root>]
```

Checks: `read` entries have resolving, non-`working`, non-superseded targets; `planned` entries FAIL (probe-not-run); `commissioned` entries carry owner/eta/blocks/cross-project with a future eta; dead vocabulary FAILs; no markdown tables in any probe file; the bank carries no consumer vocabulary (LAW 2).
The FAIL codes are `probe`'s.
Never report a green PROBE over a FAIL.

PROOF 6: the checker output, pasted.


Harvest — no sidecar (application delta)
========================================

Application keeps NO probe sub-worker skills and NO harvest sidecar docs.
Every answer's numbers / citations land INLINE in the entry's `### a-executor`, anchored to `target:`
(the answering QA file, already verified). No `values:`/`sources:`/`displays:` lanes, and no sidecar docs.
Finding stays the bank's monopoly; this worker transcribes only what the entry's `target:` already points at. Details: `ref/harvest-acceptance.md`.


Hard boundaries (application-specific; the wall + ONE-WRITER belong to `probe`)
====================================================================================

- Citations land inline in `### a-executor` — plain text, no bibtex, anchored to the source.
- Numbers trace to a source; plots come from the display/task side, never inline.
- Probe files hold `## QX<n>` entries with `###` subsections, no markdown tables.
- The dispatch is the only door — a stage that calls an evidence agent itself lands results nowhere reviewable and dies with the reply.


Return contract
===============

```
status:    ok | blocked
stage:     <stage-name>
probes:    PPNN <n> entries · T0/T1 <n> · T2 <n> · T3/T4 <n> dispatched
next:      <suggested command>
```


Reference
=========

```
../../../../probe/haipipe-probe/SKILL.md   probe — the model. Read it.
ref/per-stage-dispatch.md                  rung→lane map · seed/claims specifics · venue-scaled lanes
ref/harvest-acceptance.md                  no-sidecar harvest: write into a-executor, anchored to target
check-probe-cards.sh                       the VERIFY / stage-gate verifier (family-local fork)
../../../haipipe-application/fn/probes.md   buffer + release convention
```

Siblings: DRAFT (haipipe-application-draft) → PROBE (this) → REVISE (haipipe-application-revise) → CHECK (haipipe-application-check).

### The other files

3 files besides `SKILL.md` and `CHANGELOG.md`, each with the purpose it states about itself. They are described here, not reproduced: the folder is the copy.

```
check-probe-cards.sh          679 ln
ref/harvest-acceptance.md      26 ln  Harvest — no sidecar (haipipe-application-probe, ⑤ INTERPRET)
ref/per-stage-dispatch.md      99 ln  Per-stage dispatch reference (haipipe-application-probe)
```

<!-- haipipe:skill:body:end -->

## Aims
### P · Page-level health ruling
- P1 · Rule this skill's health.
  **Done when:** `state:` records a human judgment: stable, in flux, needs work, or parked.

## States
### P · Page-level health ruling
- ⬜ P1 · Page generated 260802 1200; nothing ruled yet.

## Log
260802 1200 · page generated from `application/2-phase/1-probe/haipipe-application-probe/` by `skillpage.py new`

<!-- haipipe:skill:log:start 7403c62bfdd40ed1 application/2-phase/1-probe/haipipe-application-probe -->

Converted from the skill's own `CHANGELOG.md`: 10 releases.

260724 · `0.3.2`
      Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 3.2.0; older entries below keep their original numbers).
260719 · `3.2.0`
      - Owner ruling, 2026-07-19 (JL): "宪法 don't use this name, just use `probe`." The nickname
        "THE CONSTITUTION" / "the constitution" for `probe/haipipe-probe/SKILL.md` is dropped everywhere;
        each site now names either `probe` or the actual path.
        Touched: SKILL.md (frontmatter summary, model pointer, Rules header, PHASE SPLIT header, ⑤ INTERPRET,
        the checker note, Hard-boundaries header, Reference block), `ref/per-stage-dispatch.md`,
        `ref/harvest-acceptance.md`, and two `check-probe-cards.sh` comments.
      - `ref/per-stage-dispatch.md` seed section: dropped the retired FIELD notation `a-consumer:` while keeping the
        live concept — the a-consumer (in 0-seed.md) feeds the opportunity, mechanism hypothesis, and kill criteria.
        Matches the paper twin (`paper/2-phase/1-probe/haipipe-paper-probe/ref/per-stage-dispatch.md`). Vocabulary: `a-consumer:` as a PROBE-FILE FIELD is gone — the probe entry's answer subsection is
        `### a-executor` (the copy of the answering QA file's answer, the consumer-side single source of truth).
        The a-consumer CONCEPT is untouched: it remains the per-consumer interpretation written in the STAGE DOC
        (station 2, anchored `[source: PP<NN>]`).
260719 · `3.1.1`
      - Probe constitution v9.5.0 sync (Q-executor-entry probe-file format), mirroring the paper family. A question is now a `## QX<n>` ENTRY (topic-local) with four `###` subsections: `### q-executor` (was `q-executor:`; carries Deliverable/Accepted), `### q-consumer` (was `serves:`; one bullet per stage-doc Q-consumer id + that consumer's ORIGINAL question), `### bank binding` (`route` · `bank` — was `match: EXISTS/NONE` — · `target` · `state`), and `### a-executor` (was the probe-file `a-consumer:`; a COPY of the answering QA file's answer). `## Why` DROPPED: the stake lives in the stage-doc Q-consumer. `a-consumer` SURVIVES as the stage-doc concept (station ②), anchored `[source: PP<NN>]` back to the `### a-executor` copy.
      - Model A phase split adopted: DRAFT authors ①ORGANIZE + ②MATCH; this worker runs ③DISPATCH → ④POINT → ⑤INTERPRET and does NOT re-match (`route`/`bank` are AUTHORITATIVE). ①+② became a documented PRECONDITION section; the collector agent runs ③④ (was ②③④). Added a "Rules" pointer block to the constitution's PROBE-phase rules, mirroring haipipe-paper-probe.
      - Harvest (the application no-sidecar delta, unchanged in substance) folds into `### a-executor` rather than the probe-file `a-consumer:`; numbers/citations stay inline with their `[→ target QA]` anchor.
      - Archaeology strip: `PASS 1 R19/R20`, the `2026-07-18` date tags, and the retired `_VALUES_`/`_CITATION_`/`_DISPLAY_`/`_DESCRIPTIONS/` sidecar enumerations removed — reason kept, citation cut. `1-probes/` is the only consumer-side source of truth; `_LOG` is the only kept sidecar.
      - `ref/per-stage-dispatch.md` and `ref/harvest-acceptance.md` synced to the same anatomy and stripped (both are unversioned refs in this skill dir).
260718 · `3.1.0`
      - No-sidecar harvest (JL, application-only; paper handled separately). Retired the `values:`/`sources:`/`displays:` harvest LANES and the `_VALUES_`/`_CITATION_`/`_DISPLAY_`/`_DESCRIPTIONS/` sidecar docs. ⑤ INTERPRET now writes the answer's numbers/citations INLINE in the section's `a-consumer:`, each anchored `[→ target QA]`; the already-verified `target:` (PASS 1 R19/R20) is the fabrication anchor. Updated: ⑤, the venue-hook section → "Harvest — no sidecar", T1 whitelist, VERIFY, return contract, frontmatter. Checker PASS 2 removed; `harvest-acceptance.md` rewritten.
260715 · `3.0.0`
      Changed (probe-redesign port; application catches up to paper probe 5.0.0 + the constitution haipipe-probe 9.0.0)
      - Rebuilt as THIN DELTAS over the probe constitution (`../../../../probe/haipipe-probe/SKILL.md`): the model — probe-file anatomy, QA state-line contract, cost ladder T0–T4, the two LAWS, derived states, checker FAIL codes — is the constitution's; this file is only the application-side deltas.
      - Loop: the 4-step BOOKKEEP→DISPATCH→TRANSLATE→VERIFY becomes the constitution's five-step ORGANIZE → MATCH → DISPATCH → POINT → INTERPRET (⑤ = HARVEST, the worker's own).
      - Probe files: per-stage `0-lifecycle/<stage>/_PROBE/PPNN_*.md` cards + the `1-probe-plans/README.md` index RETIRED → flat `1-probes/PPNN_<topic>.md`, one file per TOPIC, each question a SECTION (serves/target/state/q-executor/a-consumer + `## Why`). ORGANIZE migrates a legacy card on first touch.
      - Dispatch: the `haipipe-probe-orchestrator-agent` "gateway" framing → the shared `haipipe-probe-q-executor-agent` collector, which runs ②③④ (MATCH/DISPATCH/POINT) in stake-free clean context and writes each `target:`.
      - Claim settling: `## Verdict` block, the `verdicted` state, and the G1/G2/G3 review gate DELETED — a probe is communication, not judgment; a full-mode answer's status is written by the author into `0-lifecycle/1c-claims/1c-claims.md` (C-line + Evidence Campaign row), never in the probe file. States drop `dispatched` for the constitution's set.
      - Harvest lanes renamed to the constitution's field names — `values:` / `sources:` / `displays:` (were value_refs / pick_list / unit_refs); still venue-scaled HOOKS (application delta), not sub-worker skills.
      - `check-probe-cards.sh` replaced by a faithful fork of paper's redesigned 784-line checker (intervention_root vocab, LAW-2 leak lint retuned to intervention vocab, dead-vocab FAIL for `verdicted`/`## Verdict`), minus the paper-only resource-stage pass.
      - `ref/per-stage-dispatch.md` and `ref/harvest-acceptance.md` rewritten to the new vocabulary and the collector-dispatch model.
260707 · `2.0.0`
      Changed (round-2 paper-alignment SOP §4 rows 1-3, resolutions R1 + R5; port of paper probe 3.1.0 enforcement)
      - Rebuilt as the 4-step procedure: BOOKKEEP -> DISPATCH -> TRANSLATE -> VERIFY, each step ending in a mandatory PROOF shown in the reply (project_root + ls, the literal Agent call(s), per-card refs + ls + harvest proofs, checker output). A step without its proof did not happen.
      - NEW `check-probe-cards.sh` (family-local fork of paper's, stage-strip.sh precedent): read/verdicted ⇒ refs resolve under project_root (brace-aware expand_ref); planned/dispatched cards FAIL (probe-not-run); `harvest: OWED` lane lines FAIL (harvest skipped); no tables, ≤80 lines, status:failed surfaced; working docs scanned for bibtex/tables. Presence-driven exactly like paper's — venue-scaling happens at lane CREATION, so the fork needs no venue lookup. Run at STEP 4 and re-run by the stage CHECK gate.
      - Lane obligations: TRANSLATE writes `harvest: OWED` on the lane line FIRST, then dispatches the harvester hook and accepts mechanically; acceptance flips the line to `harvest: accepted (...)`. A skipped harvest now leaves disk residue the checker FAILs.
      - Harvester vocabulary: ONE pipeline — ACQUIRE (gateway, the only door) -> HARVEST (venue-scaled lane hooks, pointer-following transcribers). Intervention-side may follow pointers; only the gateway may find things.
      - Venue-hook contract (R5, application delta): still NO sub-worker skills — the lanes are hooks that fire venue-scaled (_VALUES_ always; _CITATION_ sectioned venues only; _DISPLAY_ only if the artifact has display units; simple venues have no document lanes) and, when they fire, MUST follow paper's 2.0.0 sub-worker contract: pointer-following + gateway dispatch only, mechanical acceptance greps, no inline search.
      - NEW `ref/per-stage-dispatch.md` (re-derived for the application spine: 0-seed, 1-claims, 2-venue, 2-pitch, 3-narrative, 4-display, 5-section-edit; modes light default / full for claims verdicts / background for fresh runs; venue-scaled lane rules; strip forms + OWED gate rule) and `ref/harvest-acceptance.md` (paper's literal greps adapted per lane; citation card format spec stays paper-side, single source of truth).
      - Application deltas preserved: claims C-line + Evidence Campaign row flip at TRANSLATE (enum supported | refuted | inconclusive); `_VALUES_` landing; venue scaling; `fn/probe-plans.md` buffer convention.
      - Housekeeping: frontmatter still said 1.0.0 while this CHANGELOG already had 1.1.0 (the 765696f port bumped the log only) — resolved by this 2.0.0 bump; entry order corrected to newest-first.
260706 · `1.1.0`
      - 765696f port: TRANSLATE lands verified numbers in _VALUES_ and flips the Evidence Campaign row alongside the C-line.
260706 · `1.0.0`
      - NEW phase worker (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0; full-DPRC ruling R4).
260709 · `2.1.0`
      - BENCH RULINGS (Test-Haipipe-Application): STEP 1.5 RELEASE GATE — planned cards dispatch only on the user's explicit release (`probe run PPNN` / "release PP02" / "release all"); stage handoffs and bare from-buffer sweeps present the planned roster and STOP (PROOF 1.5). No exception for cheap probes.
      - PHI-adjacent task dispatches pin the MINIMAL aggregate-safe column allow-list in the prompt by default (aggregates-only outputs); restricted-vs-full is never asked mid-flow; org PHI gates apply on top.
      - (Earlier same day, logged under family 6.1.1: two-level _PROBE glob fix in check-probe-cards.sh.)
260709 · `2.2.0`
      - GROW-loop support: the values lane REDIRECTS for rung 1a — descriptions-stage probes land their harvest in `_DESCRIPTIONS/DS<n>_<name>.md` (per-dataset profile sheet: field inventory + Field Disposition + readable landed profile; quoted-only, anchored + dated). Same OWED/accepted debt bookkeeping; the 1a doc keeps one-line D entries.

<!-- haipipe:skill:log:end -->
