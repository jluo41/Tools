haipipe-discovery — Changelog
=============================

Skill-scoped changelog (lives INSIDE the skill folder so it is never loaded at
invocation; read on demand). Versions match SKILL.md frontmatter `version:`.
Layer-wide structural events (bucket renames, folder moves) also land here,
since this orchestrator owns the layer contract. Newest first. Rollup lives in
the plugin-level `CHANGELOG.md`. The type specialists keep their own
`CHANGELOG.md` in their own folders.


## [0.3.5] — 2026-08-27

- Known-dead claim exit added to gate ①: a `working` ticket whose executor is KNOWN to have died before Report (the run ended without completing the file) is reclaimed immediately — fresh `started:`/`by:` on the SAME file, or superseded — with no TTL wait, and a ticket is NEVER deleted. Found in the 260827 paper field test: three executors died mid-lap and the actor's only lawful options were "wait out the TTL" or improvise; it improvised delete-and-remint, which erased claim history.

## [0.3.4] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 3.4.0; older entries below keep their original numbers).

## [3.4.0] — 2026-07-19

- ⑨ TOMBSTONES erased. Owner ruling (JL): "不需要留退役告示,直接抹除任何痕迹" — a doc states the CURRENT contract and never names the dead thing.
  `SKILL.md:78` and `ref/discovery-yaml-schema.md`'s `## 💀 DELETED:` section head both restated positively
  ("The bank is probe-unaware").
- ⑩ probe files hold `## QX<n>` ENTRIES, not "sections" — wording corrected; the schema's `q-executor:` field notation corrected to `### q-executor`.


## [3.3.0] — 2026-07-19

- Owner ruling, 2026-07-19 (JL): "宪法 don't use this name, just use `probe`." The nickname
  "THE CONSTITUTION" / "the constitution" for `probe/haipipe-probe/SKILL.md` is dropped everywhere;
  each site now names either `probe` or the actual path.
  Touched: `fn/qa.md` (the QA-file anatomy pointer), `ref/discovery-yaml-schema.md`, and `../DESIGN.md`.

## [3.2.0] — 2026-07-14 — R19 hardening: the state line is read FIRST

- **Gate ① reads the STATE LINE *before* the literally-answers test.** The order is load-bearing. A `working` file's `## Answer` is EMPTY BY CONSTRUCTION, so the answer test is a guaranteed miss on it — the caller falls through to ③, allocates a NEW `<n>`, `set -C` never fires (different path), and RUNS THE SAME EXPENSIVE JOB a second time next to the one already in flight. A `working` file is matched on its `# Q —` LINE: same question ⇒ return the path + "in progress since <started>", run nothing.
- **A QA file with NO `- state:` line is MALFORMED, not legacy** (checker: `qa-no-state`). It is THIS layer's own file, so this layer REPAIRS it: tag `answered` if `## Answer` has a body; RECLAIM it as a zombie if the Answer is empty. A consumer may never do either.
- **The same-`<n>`/different-slug claim race is NON-FATAL BY RULING and is NOT a reviewer REVISE.** `fn/qa.md` said non-fatal in one paragraph and "the reviewer REVISEs it" twelve lines later. The reviewer's FILENAME check now carries the exemption explicitly, and renaming a QA file to "fix" it is forbidden (the body is frozen; a rename orphans a live claim).
- Reviewer twin (`haipipe-discovery-reviewer-agent` 1.4.0): WRITE-ONCE → BODY FROZEN (it would have REVISEd every gate-③ completion), plus the STATE LINE check; creator (`haipipe-discovery-creator-agent` 1.8.1) return contract gains `qa_file:` / `qa_state:` / `superseded:`.
- Twin: `haipipe-task` 6.2.0, character-identical.

## [3.1.0] — 2026-07-14 — THE CLAIM: a QA file becomes a TICKET that becomes a RECEIPT

Ruling of record: JL, 2026-07-14 (`Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/` PART 3b, the `>> CC0714` block).
Constitution: `probe/haipipe-probe/SKILL.md` v8.2.0, PART 3a — R19 (the claim) · R20 (supersession) · R21 (the three readers).

**THE HOLE IT CLOSES.** A QA file used to be written ONCE, at Report, complete. Its EXISTENCE meant "answered", and there was NO way to say *"someone is working on this right now."* So: two consumers ask the same question a week apart. The first dispatches an expensive lifecycle run. The second, **while that run is still going**, sees no QA file — and dispatches THE SAME RUN AGAIN. Nothing prevented it.

Added
- **ONE MUTABLE FIELD — the `state:` line.** A QA file now carries `- state: working | answered | superseded-by: QA/<m>-<slug>.md`, `- started: YYYY-MM-DDTHH:MM` (MANDATORY when `working`), and an optional `- by:`. Everything below the state line — `# Q —` / `## Answer` / `## Caveats` / `## Not-done` — is written once and never touched again.
- **Gate ③ LIFECYCLE now CLAIMS FIRST.** At the moment it decides to run — before Plan, before any search — it writes the QA file with `state: working` + `started:` + an EMPTY `## Answer`, and COMPLETES it at Report (`state: answered` + the body). Gate ② DIGEST still writes ONCE, complete, `answered` (the artifacts already answered; zero searching happens, so there is nothing to claim and nothing to race). Gate ① writes NOTHING. **Only gate ③ ever produces a `working` file, and only transiently.**
- **Gate ① SCAN now branches on the STATE LINE, not on existence.** `answered` → return the path · `working` → **DO NOT RE-RUN**, return the path + "in progress since `<started>`" (this is the duplicate-work fix; an expensive run is SAVED at ~0 cost) · `working` past the TTL → 🧟 ZOMBIE, RECLAIM it · `superseded-by: X` → follow the chain (possibly multi-hop) and return the LIVE answer's path.
- **`QA_CLAIM_TTL_HOURS = 24`** — the named constant. A `working` file whose `started:` is older is STALE: RECLAIMABLE by the next qa call (rewrite the claim with a fresh `started:`, record the abandoned attempt in `## Not-done`) and a HARD FAIL for the checker. **A `working` file with no `started:` can never expire — it is a zombie by construction, and it is INVALID.** Never hard-code the literal `24` anywhere; reference the name.
- **RACE GUARD: `set -C` (noclobber), and nothing more.** Two qa calls can decide ③ at the same instant and both pick `QA/3-`. The loser sees the file already exists, re-runs gate ① **ONCE**, and DEFERS — it never loops back into ③. This shrinks the race window from THE WHOLE RUN to microseconds. The residual same-instant/different-slug collision is NON-FATAL (gate ① finds both files). **No lock dirs, no lease servers, no ledgers, no flock** — all retired machinery in a new hat.
- **R20 SUPERSESSION.** A later run whose answer CHANGES writes `QA/<n+1>-<slug>.md` and APPENDS `superseded-by:` to the OLD file's state line (`- state: answered · superseded-by: QA/2-cycle.md`) — the only edit ever permitted to a frozen file, and only by its own owner. Supersede ONLY when the answer changed; a deeper cut or a different source base is just `QA/<n+1>`, and the old file stays live.
- **A REFUSE RELEASES its claim.** Never leave a `working` file behind a refusal — it tells every future reader that work is underway when nothing is.

Changed
- **⚠️ THE LOAD-BEARING INVARIANT IS *ONE WRITER*, NOT *WRITE-ONCE*.** The executor writes the file TWICE — the CLAIM at the ③ decision, the COMPLETION at Report. Two writes by the SAME owner, in its OWN folder, is fine. **A CONSUMER (probe/paper/application) must NEVER create, claim, edit, complete, or supersede a QA file.** A consumer-planted `working` file is the retired `_ASK/` stub wearing a `QA/` costume, and it is FORBIDDEN — the same violation as the A03 C6/C7 leak. "Write-once" was never the real rule.
- **R15 (ENRICH never mutates) still holds — FOR THE BODY.** Only the state line is ever mutable. Two edits in a file's whole life: `working → answered`, and `answered → + superseded-by:`.
- **STATUS is derived from the state line, not from mere existence.** `ls QA/` is no longer enough — the reader must OPEN THE FILE. No file = not answered · `working` = IN PROGRESS since `<started>` · `answered` = answered · `superseded-by: X` = answered but STALE, the live answer is X.
- **Protocol Step 4 Report** now spells both entrances: via gate ③ the claim is already on disk and the creator COMPLETES it; via gate ② the creator CREATES it once, complete.
- `--check-only` now explicitly writes **NO CLAIM** (it already wrote nothing else). A qa call that fell through to ③ during the probe's MATCH step — a FREE detection pass — would otherwise spawn an unbudgeted run AND plant a claim.

Enforced (the checker's new teeth — the whole point is that these become MACHINE-DETECTABLE)
- `qa-working-no-started` — a `working` QA file with no `started:` → an UNEXPIRABLE claim.
- `qa-working-expired` — a `working` QA file older than `QA_CLAIM_TTL_HOURS` → a ZOMBIE.
- `qa-answered-empty` — `state: answered` with an EMPTY `## Answer` → a LYING RECEIPT.
- (consumer-side, in `check-probe-cards.sh`) `read-target-working` and `read-target-superseded` — a probe section at `state: read` whose `target:` resolves to an UNFINISHED or STALE QA file. **The latter is the day-1/day-40 silent-false-claim bug: every file internally consistent, the claim FALSE, and nothing caught it before.**

Files
- `fn/qa.md` — rewritten: the state line, the gate-path write contract, the CLAIM (Step 3a, with the `set -C` idiom and what the loser does), the RECLAIM path (Step 3b), SUPERSESSION, the three readers, status derivation, the five checker codes. `qa_state:` added to the return. The depth ladder (0 READ / 1 ENRICH / 2 NEW FOLDER / 3 NEW GROUP) and the artifacts it reads (sources.md / notes.md / verdict.md / landscape.md / ideas.md) are the ONLY things adapted from the task twin.
- `SKILL.md` — the qa-verb block, the QA/ folder contract, Protocol Step 4 (Report), description + summary.
- `agents/haipipe-discovery-orchestrator-agent.md` → 2.1.0 (I own the CLAIM; gate ① reads the state line; the loser defers without looping).
- `agents/haipipe-discovery-creator-agent.md` → 1.8.0 (at Report I COMPLETE the claim on gate ③, CREATE once on gate ②; never a lying receipt; never touch someone else's `working` file).

Twin parity: the task twin (`task/haipipe-task/fn/qa.md`, v6.1.0) states every field name, state value, TTL constant, flag spelling and bash idiom **character-identically**. Verified: all three bash blocks (grep/parse form, the `set -C` claim idiom, the staleness test) diff clean between the twins. They drifted before; they must not again.

## [3.0.0] — 2026-07-14 — PROBE-UNAWARE: the bridge comes out, the `qa` verb goes in
## 3.0.1 — 2026-07-14

- **`allowed-tools` FIXED: added `Write, Edit`.** The frontmatter allowed only `Bash, Read, Grep, Glob, Skill`, but the new `qa` verb's gate ② DIGEST instructs THIS SKILL to author the file itself ("write the digest, stop" — no Skill() or Agent() delegation is named on that path). DIGEST is the cheap, common outcome of a probe's MATCH (the spec's "most probes should hit T2 REUSE"), so the Write would be denied by the allowlist, the QA file would never be created, the verb would return no path, and the probe's `target:` would stay empty with the section stuck at `commissioned`. Now matches the task twin.
- `<n>` allocation rule added to fn/qa.md (fail-closed, computed immediately before the write; never clobber). Identical to the task twin — the two banks must not drift.

Spec of record: `Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/` (v3, APPROVED JL 2026-07-14, rulings R1-R18). Constitution: `probe/haipipe-probe/SKILL.md` v8.0.0 — where this layer and that file disagree, that file wins.

**The one-line version.** v2.7 → v2.8.1 spent three releases building a probe handoff bridge INTO this layer. R2 rules that the bank is **probe-unaware**. So the bridge comes out — both feet — and a door goes in its place: `qa`, which takes a plain question and hands back a file. The layer no longer knows what a probe is, and that is the point: an answer nobody shaped around one paper's story is an answer the next paper can reuse.

### Removed (the whole bridge — do not resurrect)
- `_ASK/PPNN_<slug>.md` stub folders, the legacy flat `_ASK_*.md`, and the "stub-seeded zeroth state". A discovery folder's zeroth state is an EMPTY folder, not an inbox.
- The top-level `answers: [PPNN]` field in `discovery.yaml`. It is DELETED, not optional — a missing one is now CORRECT. There is nothing to grep for, because the answer IS a file.
- Every PP id under `discoveries/`. No consumer id, claim id, or paper reference in any discovery filename or file, ever.
- The reviewer's "Bridge check — the `answers:` field" gate (its two live concerns moved to the QA-file gate + the new bank-purity check).

### Added — the `qa` verb (R11 · `fn/qa.md` · the task twin is `task/haipipe-task/fn/qa.md`)
`/haipipe-discovery qa "<question>" [<leaf>] [--check-only]` — ONE question, GENERAL language, no PP id, no paper ref, no stake. The gate, cheapest door first:

```
① QA SCAN    grep <leaf>/QA/*.md (or all leaves) — already answered? -> return the PATH   ~0
             MATCH ON THE ANSWER, NEVER THE TOPIC (R14): open it and READ it.
② DIGEST     sources.md / notes.md / verdict.md / landscape.md / ideas.md already answer it,
             but no readable digest exists -> write QA/<n>-<slug>.md from EXISTING
             artifacts. No searching. No new sources. No new conclusions.              cheap
③ LIFECYCLE  neither -> Plan → Build(opt) → Execute → Report at the SHALLOWEST depth:
               depth 0 READ · 1 ENRICH (on-topic, same leaf) · 2 NEW FOLDER · 3 NEW GROUP
             scope test (1 vs 2): does it fit THIS leaf's discovery.yaml question:?
🚫 REFUSE    task-shaped (code / runs / metrics on our own data) -> /haipipe-task qa
             claim-shaped ("is C6 supported?") -> not an evidence question; not ours
```

THREE CALLERS, none special: a consumer's probe DISPATCH (via the orchestrator agent), a HUMAN exploring a direction (R18), and the ORCHESTRATOR itself doing answerability work with nothing pending (R17). The depth is the executor's private business — the caller hands over a question and gets back a path.

### Added — the optional `QA/` folder (R9/R10, on BOTH banks)
`discoveries/<leaf>/QA/<n>-<slug>.md`. `<n>` = creation order, and **the numbering IS the index** (`ls QA/` is the index; no INDEX file). SLUG ONLY. WRITE-ONCE — a later question ADDS `QA/<n+1>-…`. Anatomy: `# Q —` (self-contained, general) / `## Answer` (plain words + `[→ sources.md#S02]` anchors) / `## Caveats` / `## Not-done`. Three legal reasons to exist, no fourth: **commissioned · digest-only · executor's own**. A `QA/` mirroring every source is noise, not an index.

### THE EXECUTOR HOLDS THE PEN (CC-8 — the rule this release exists for)
A consumer may CAUSE a QA file. **This layer AUTHORS it.** When a probe meets a bare terminal with no digest, it does not write the digest — it dispatches a digest-only run, and a clean-context agent writes it. The failure that proves the rule is on disk: `tasks/A03_welldoc_cycle_check/result.md` carries "C6" and "C7" because a consumer session, with the stake in its own context, did bank work INLINE. No stub, no mailbox, no id was involved — which is why the wall cannot be a file rule. It is the orchestrator's clean context, and nothing else.

### Session modes (R17 — "very important", JL-15)
This layer's PRIMARY mode is its own autonomous Plan → Build → Execute → Report: no question, no ask, nobody asking. `qa` is a SIDE door. **Answerability work** — writing digests, building reusable source bases so future questions are cheap — is native executor work, done without knowing which questions will come. Consequence: in a healthy project most questions are ALREADY ANSWERED before anyone asks, so a commission should be the EXCEPTION, not the norm.

### Survives, untouched
A Review-type discovery's own **`verdict.md`** is this layer's terminal file and it is ALIVE. It is a different thing from the retired probe "Verdict" (R7, dead). Also unchanged: the two axes, the 3 types, the 3 buckets, the type specialists, ENRICH mode, the Haiku search-worker fan-out, `source-format.md`, and self-contained folders (no parent, no consumed_by).

### Files
`haipipe-discovery/SKILL.md` 2.8.1 → **3.0.0** · `fn/qa.md` 🆕 · `ref/discovery-yaml-schema.md` (v2.6 → v3.0: `answers:` deleted, `QA/` added to the leaf contract + a terminal template) · `agents/haipipe-discovery-orchestrator-agent.md` 1.7.0 → **2.0.0** (the direct dispatch target; QA mode; the wall) · `agents/haipipe-discovery-creator-agent.md` 1.6.0 → **1.7.0** (authors the QA file at Report) · `agents/haipipe-discovery-reviewer-agent.md` 1.2.0 → **1.3.0** (QA-file gate + bank-purity check) · `agents/README.md` (direct-dispatch diagram; gateway retirement) · `DESIGN.md` (boundary rules + decision log) · `3_idea/idea-creator/SKILL.md` 1.0.1 (composes into `qa`, not the retired gateway).


## [2.8.1] — 2026-07-12 — Audit repair: the AGENTS were blind to the bridge

The 2.7/2.8 stub semantics lived only in the interactive SKILL. The discovery AGENTS — which are the gateway's ONLY dispatch path — never mentioned `_ASK/` stubs or `answers:`, so every agent-run discovery silently dropped the ask: Plan ignored the stub, Report emitted no `answers:` field, and the consumer's card sat `dispatched` forever with the work already done. Fixed: orchestrator 1.7.0 (stub-seeded input form; Plan step 0 reads the stub; Step 5 Report requires `answers:`), creator 1.6.0 (new "Probe handoff stubs" section: Plan seeds discovery.yaml from the stub, Report writes `answers: [PPNN]`, never edits the stub, and structures its OWN artifacts around the questions — never around a consumer's framing, which is what contaminated the 2026-07-11 discovery).

Also: `answers:` is a flow list of bare PP ids (schema owned by probe/haipipe-probe/SKILL.md).


## [2.8.0] — 2026-07-12 — Ask stubs move into an _ASK/ container

JL ruling 2026-07-12 ("加一个 ask folder，把它们放到一块儿"; pairs with haipipe-probe 7.7.0): stubs live at `<discovery-folder>/_ASK/PPNN_<slug>.md` — one file per ask, the container keeps the folder root clean when several consumers ask. The stub filename mirrors the consumer's `1-probe-plans/PPNN_<slug>.md` card, so `grep -r PPNN` finds both feet of the bridge. Zeroth state re-phrased: a folder whose only content is `_ASK/`. Legacy flat `_ASK_PPNN.md` is read the same way and moved into `_ASK/` on first touch. All v2.7 semantics unchanged: read-only, Plan seeds from it, Report answers with `answers: PPNN`, this layer still references nothing upward.


## [2.7.0] — 2026-07-11 — Probe handoff stubs (_ASK_PPNN.md)

### Added (two-footed-bridge ruling, JL 2026-07-11; pairs with haipipe-probe 7.4.0)
- Plan stage reads an `_ASK_PPNN.md` probe handoff stub when present (READ-ONLY; possibly the folder's only content — its zeroth state): Need → question, Deliverable → expected_outputs, Do-not → scope guards; the stub is never edited by this layer.
- Report stage: when a stub exists, the report block carries `answers: PPNN` — the disk signal the consumer greps to harvest.
- Handoff step clarified: an _ASK stub is not an upward reference — the CONSUMER wrote it; this layer only reads it and answers in its own report block, preserving "references nothing upward". Stub anatomy: probe layer (haipipe-probe/SKILL.md "The handoff stub").

## [2.6.0] — 2026-07-03

### Verified (same day)
- Agents triad synced to v2.6 (1.2.0 each: Execute via type specialists, report appended,
  self-contained folders, source-format checks in the reviewer gates); CODE_REVIEW.md
  regenerated as a fresh v2.6 review (old 06-23 review retired). Small fixes: dead
  .discovery-console.yaml routing signal removed from fn/feedback.md; types x roles table
  now lives ONLY in the schema doc (lifecycle-map points); S-id scope defined
  (folder-local default, group-global by declaration).
- LIVE END-TO-END VALIDATION PASSED: a fresh-context agent ran a real prior-art discovery
  (ProjB P02.01, review-text traits -> opioid Rx novelty) through the full lifecycle —
  correct scaffold (new P02 group), Plan, Execute via Skill(haipipe-discovery-review) ->
  research-lit with real S2/web search, reviewer-agent gate fired and caught one
  unverified citation (REVISE loop worked), report appended, v2 log events, zero contract
  violations (no parent/status.yaml/site.md/tables; 11/11 sources with summary + finding).


### Changed (JL: "I think this should be Search -> Review -> Idea")
- Type ordering everywhere is Search -> Review -> Idea — the type names ARE the IPO order
  (input: gather sources; process: judge/synthesize; output: create). Applied to
  lifecycle-map Axis-2 heading, SKILL.md, DESIGN.md. In-file comment thread resolved and
  archived here.

### Added
- `ref/source-format.md` — THE one home for paper/source presentation (one source = one
  subsection, never a table; sources.md + notes.md + inline-chat templates + filled
  example pointer). Schema doc and the search/review specialists now point here instead
  of restating. Also retro-converted the 6 remaining table-style sources.md on disk
  (8 tables, cell text preserved verbatim) and deleted the SKILL.md Legacy section
  (nothing legacy remains on disk to document).


### Changed (JL: "内容有点重复" — dedup rewrite)
- SKILL.md rewritten to say each thing ONCE: Invocation + Dashboard merged into one Verbs
  block; Two Axes + Three Types collapsed into one Model section (the tables they restated
  live in ref/lifecycle-map.md and ref/discovery-yaml-schema.md, the declared canonical
  homes); the feedback contract — previously written THREE times (Routing inline block,
  Feedback section, tail ## Feedback section) — is now one compact section pointing at
  fn/feedback.md; Disambiguation merged into routing rule 5/7/9; the Review Output
  Contract pointer folded into the Buckets line. No rules or verbs were removed, only
  restatements. ~6,300 -> ~3,300 tokens per invocation.
- ON-DISK LEGACY FULLY MIGRATED (JL: "不要留旧的符号了"): renamed C01_p0622-threats ->
  P01_p0622-threats (ids + cross-refs updated); stripped parent:/consumed_by: from all 17
  remaining discovery.yaml; deleted all 16 status.yaml/site.md; converted the last flat
  single-file discovery (ProjC L01.01 rank-divergence) into a v2.6 folder (discovery.yaml
  + sources.md per-source sections + notes.md + verdict.md — group-level references stay
  valid). The docs' Legacy sections shrank to one line; only the append-only project log
  keeps old field names. Also fixed a pre-broken unquoted-colon YAML in the PhyPat
  submodule. 19/19 discovery.yaml parse clean.
- Group letters collapsed 5 -> 3 (JL approved): `S` source base / `L` landscape (absorbs B
  benchmark) / `P` proof-prior-art (absorbs C counterevidence). Letters tag the GROUP's
  purpose, not folder types (a group mixes types), so S/R/I was rejected; letters kept for
  the task mirror + ls clustering + compact ids. Existing B/C folders keep their names
  (renaming would break caller-side links); legacy note (f) added.
- Changelog convention applied toolkit-wide the same day (89 skills): frontmatter carries
  version + pointer only; history lives in each skill's own ./CHANGELOG.md (this file was
  git-mv'd here from the layer level, where its entries had always been keyed by this
  skill's versions).

## [2.5.0] — 2026-07-03

### Added (JL: "I think we should have them")
- **Type specialist skills**, one per bucket, mirroring the sibling-layer pattern
  (haipipe-data-source etc.):
  - `1_search/haipipe-discovery-search/` — owns the Search Execute (find + read ->
    sources.md + notes.md), dispatches the six 1_search workers.
  - `2_review/haipipe-discovery-review/` — owns the Review Execute (judge -> verdict.md,
    synthesize -> landscape.md) and is the new canonical home of the Review Output
    Contract (moved from the orchestrator, pointer left behind).
  - `3_idea/haipipe-discovery-idea/` — owns the Idea Execute (generate -> ideas.md,
    novelty_check -> verdict.md), the ideation loop.
- Orchestrator Execute now dispatches the type skill instead of raw workers; dashboard
  and bucket listing updated; three `.claude/skills/` symlinks added.
- This REVERSES the v2.0.0 "no per-type skill family" decision — its rationale
  (workers != types) dissolved once buckets became 1:1 with the types.

## [2.4.0] — 2026-07-03

### Changed (JL simplification pass: "we have plan/build/execute/report — why so many other things")
- **novelty_check re-typed Review -> Idea.** It is the evaluation half of the ideation loop
  (generate -> check novelty), so `Idea` now branches by role like Review does:
  `idea_generation -> ideas.md`, `novelty_check -> verdict.md`. Buckets and types are now
  exactly 1:1; the v2.3.0 exception footnote is deleted everywhere.
- **`parent:` and `consumed_by:` fields REMOVED — discovery is probe-UNAWARE.** JL
  principle: task and discovery never know about probes; they run freely against their
  own question, and ORGANIZING happens at the probe level. References point one way,
  downward: the probe records which discoveries/tasks it uses in its own files
  (probe.yaml evidence links); a discovery never tracks who commissioned or consumed it.
  Group letters are purpose hints (L landscape, P prior-art, B benchmark, C
  counterevidence, S source base), no longer parent hints. Legacy folders carrying
  `parent:`/`consumed_by:` are ignored, cleaned on next edit.
- **Folder contract slimmed to discovery.yaml + evidence files.** `status.yaml` and
  `site.md` dropped from the contract (progress = discovery.yaml `status:`, human summary
  = `report.summary`); the `report:` block is APPENDED at Report and absent before
  (replaces round-2's empty-block convention, resolving JL's open comment on it).
  `ref/discovery-yaml-schema.md` rewritten lean (~40% shorter); SKILL.md protocol,
  lifecycle-map, DESIGN.md, and the creator agent updated to match.
- Feedback keyword map: "novelty"/"查新" now routes to 3_idea (was 2_review).
- **NEVER tables for papers/sources (JL, third time).** Every paper/source listing in the
  layer is now one-item-one-subsection with the full title in the heading (+ Scholar link
  in sources.md): schema sources.md template, arxiv / semantic-scholar / exa-search /
  deepxiv result presentation, comm-lit-review literature output, novelty-check Closest
  Prior Work. Feedback items 2026-06-22 (1_search) and 2026-06-29 (fallback) marked fixed;
  the 06-22 item records the 07-03 recurrence (the v2.4 schema rewrite had reintroduced
  the table).
- **Docs are self-contained at the layer level (JL).** SKILL.md / lifecycle-map / schema no
  longer mention probe or paper as consumers: dropped the "consumer" column, the
  "-> probe/paper" role glosses, and the cross-layer flow diagram; handoff = "return the
  terminal to the caller; the caller records the link on its own side". DESIGN.md keeps
  only the sibling-layer positioning table.
- **Concrete example slugs (JL).** Doc examples renamed from generic placeholders
  (L01_initial-landscape) to topical names (L01_personality-prescribing-landscape); rule:
  the slug names the TOPIC.
- **SKILL.md frontmatter description shortened ~60% (JL: too long).**

## [2.3.0] — 2026-07-03

### Changed (buckets 4 -> 3, one folder per type; English-only pass)
- **Merged `2_read/` into `1_search/`** (alphaxiv, deepxiv, paper-analyzer moved). Reading
  is the second half of the `Search` type and the two buckets were only ever used together.
- **Renumbered `3_review/` -> `2_review/` and `4_idea/` -> `3_idea/`.** Each type now maps
  1:1 to its Execute bucket (Search -> 1_search, Review -> 2_review, Idea -> 3_idea).
  `novelty-check` stays in `3_idea/` by choice (pairs with ideation) while serving
  Review-judge — the one documented exception. Workspace `.claude/skills/` symlinks repointed.
- **English-only pass.** Purged residual 搜/析/创 from DESIGN.md (was stale at v2.0.0),
  the agents/ triad + README, fn/feedback.md, and feedback READMEs. Historical
  changelog/decision-log entries keep their original wording.

### Fixed
- **Dangling references removed.** SKILL.md: `0_venue/`, `D_patent/`, `/idea-discovery`,
  `/research-pipeline`, `/patent-pipeline` (none exist). Orchestrator agent Step 0 no
  longer points at `fn/plan|build|execute|report.md` (never existed); the per-stage
  procedure is SKILL.md's Step-by-Step Protocol. Creator/reviewer citation verification
  now goes through the `/arxiv` + `/semantic-scholar` skills instead of the missing
  `research-toolkit/*.py` paths.
- **Deleted the stray dangling self-symlink** `haipipe-discovery/haipipe-discovery`.
- **Backfilled the missing 2.1.0 / 2.2.0 entries below** (they existed only in SKILL.md
  frontmatter).

### Round 2 (same day)
- **Sibling contracts specified** in `ref/discovery-yaml-schema.md` — status.yaml schema,
  site.md card format, project.log.jsonl event shapes, `id` format, and the
  empty-report-block-at-Plan convention were all previously unwritten (every author
  invented a shape; a fresh-context dry-run surfaced this). Live pre-2026-07-03 files
  migrate-on-next-edit.
- **Light-Review wording disambiguated** in `ref/lifecycle-map.md` ("dropping sources.md +
  notes.md as work products" read as either depositing or omitting; now says WRITING them).
- **Cross-layer glyph stragglers fixed**: `blueprints/end-to-end-sandwich-run.md` and
  `skills/paper/2-phase/1-probe/haipipe-paper-probe/SKILL.md` still taught 搜/析/创 types.
- **ProjC discovery folders migrated** (7 folders under
  `examples/ProjC-LLMRecPhysicain/discoveries/` — the v2.1.0 "migrated all existing
  folders" claim had only covered ProjB): `type:` glyph -> English, transitional
  `type_en:` field dropped, glyph comments in site.md/ideas.md/status.yaml de-CJK'd.
- **`{CC->JL}` review markers** left at the judgment points (schema conventions,
  novelty-check exception, bucket defaults, stale CODE_REVIEW handling) for JL's
  eyeball pass; delete each marker after confirming.

## [2.2.0] — 2026-06-24

### Added
- **Capture-time feedback ROUTING (mirrors haipipe-paper).** `feedback "<text>"` infers the
  bucket unit and files into THAT unit's `feedback/`; cross-cutting -> orchestrator
  fallback. Added `fn/feedback.md` (cross-cutting guard -> keyword -> context -> fallback;
  merge-or-create; `list` aggregates across inboxes; `move` re-routes). Recast
  `feedback/README.md` as the fallback inbox.

## [2.1.0] — 2026-06-24

### Changed
- **Type values renamed from the glyphs 搜/析/创 to the English words Search/Review/Idea.**
  The type axis is no longer CJK; orthogonality vs the stage axis now comes from
  non-overlapping word lists (process verbs vs folder kinds). Updated SKILL.md +
  ref/lifecycle-map.md + ref/discovery-yaml-schema.md and migrated all existing discovery
  folders. Chinese trigger phrases (查新/找idea) unchanged.

## [2.0.1] — 2026-06-23

### Fixed
- **4-bucket directory structure created on disk.** Moved alphaxiv/deepxiv/paper-analyzer
  from `1_search/` to `2_read/`, renamed `2_review/` to `3_review/`, renamed `3_idea/` to
  `4_idea/`. Now matches DESIGN.md, SKILL.md, and `.claude/skills/` symlinks (which had been
  broken — 8 of 12 symlinks were dangling).
- **Cross-layer rename completed.** `haipipe-discover` -> `haipipe-discovery` applied to 12
  files across paper/probe/application/task/toolkit layers. TODO.md deleted.
- **Orchestrator Chinese character normalized.** 創 (traditional, U+5275) -> 创 (simplified,
  U+521B) on line 42, matching all other files.
- **CODE_REVIEW.md updated.** All 4 WARNs resolved; verdict now PASS.
- **DESIGN.md `play/` reference removed.** Directory does not exist.

## [2.0.0] — 2026-06-22

### Changed (TWO-AXIS redesign, mirrors task)
- **Lifecycle is now the uniform `Plan -> Build(opt) -> Execute -> Report`.** Retires the
  old `open -> search -> read -> review -> post` verb-lifecycle. Build is optional (only
  for a systematic query string / extraction schema). One execution per folder (no `runs/`
  multiplicity, unlike task).
- **`search/read/review/idea` are no longer stage verbs — they are the capability buckets
  (Execute-stage workers).** The folder TYPE is one of 3 Chinese-char types:
  - `搜` source = search + read merged -> `sources.md` + `notes.md` (a reusable, accumulating source base).
  - `析` analyze = judge + synthesize merged -> `verdict.md` (判, role prior_art/counter/novelty -> probe)
    or `landscape.md` (综, role landscape/benchmark -> paper); `role:` picks the branch.
  - `创` idea -> `ideas.md` (-> probe-open / paper-seed).
- **`verdict:` block renamed to `report:`** (report-to-human; generalized across types).
- **New terminal files** `landscape.md` + `ideas.md` alongside `verdict.md`.
- Workers (4 buckets) and types (3) are different axes; per-type specialist skills are NOT created.
- Old folders (`role:` + `verdict:`, no `type:`) remain readable; treat missing `type:` as `析`.
- Updated: `SKILL.md` (2.0.0), `DESIGN.md` (2.0.0), `ref/lifecycle-map.md`,
  `ref/discovery-yaml-schema.md`, and the minimal-dry-run fixture.


## [Unreleased] — 2026-06-21

### Changed
- **Skill renamed `haipipe-discover` -> `haipipe-discovery` (1.8.0).** Matches the
  haipipe-<noun> sibling convention (probe/paper/task/insight/project/application);
  the verb-named skill was the lone exception. Inner folder `haipipe-discovery/`,
  the `.claude` symlink, the command `/haipipe-discovery`, and all in-repo refs
  updated.
- **Discovery is a FOLDER, not a single file (reverted v1.5).** A discovery is
  one research topic = its own folder (`discovery.yaml` + `sources.md` /
  `notes.md` / `verdict.md` + `status.yaml` / `site.md`), mirroring a
  task-folder; sources/notes/verdict are its `results/`. The dry-run fixture and
  blueprint already used folders; v1.5's single-file default never landed.
  `ref/lifecycle-map.md` recast as `open -> search -> read -> review/idea -> post`,
  each stage filling one IO file (no separate `verdict` verb; review writes
  `verdict.md`). SKILL.md / DESIGN.md / discovery-yaml-schema.md flipped to
  match. Version 1.7.0.
- **Folder renamed `discover/` to `discovery/`.** The layer concept now reads as
  a noun, matching the `discoveries/` artifact dir and the task/probe/insight
  sibling layers. (The skill itself was renamed too, see above.) Cross-reference
  path fixups in `STRUCTURE.md`, the blueprint, and the plugin CHANGELOG are a
  follow-up.
- **Narrative layer retired across discovery docs.** A discovery now has exactly
  two parents: a delivery lifecycle (`paper` / `application`) for L* landscape /
  novelty work, and a `probe` for claim-level evidence. The story-side dispatch
  that used to come from `Narrative-open` now comes from `Delivery-open`. Updated
  DESIGN.md (layer table, project tree, combine-with-probe section, boundary
  rules), SKILL.md, and `ref/discovery-yaml-schema.md`.

### Added
- **`feedback/` inbox + `feedback` utility verb (1.9.0, mirrors probe).**
  `/haipipe-discovery feedback "<text>"` captures a complaint/confusion/wish about
  the skill into `feedback/<date>_<slug>.md` (capture-only); `feedback list`
  reviews open items. Fixing is a separate revision pass, so users can improve the
  skill as they use it.
- **`ref/lifecycle-map.md`** — the canonical verb-based lifecycle table
  (Status / Open / Search / Read / Review / Verdict / Post), isomorphic to the
  probe lifecycle map: per verb, the question, action, reads, writes, external
  calls, human output, machine state, and stop gate. SKILL.md and DESIGN.md now
  point here instead of restating the per-verb columns (the lifecycle had been
  written in two places; it now has one home).
- This `CHANGELOG.md`, for parity with the task / probe / insight / project
  layers (discovery previously tracked history only in SKILL.md frontmatter and
  the DESIGN.md Decision Log).
