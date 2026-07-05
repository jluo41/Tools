haipipe-discovery — Changelog
=============================

Skill-scoped changelog (lives INSIDE the skill folder so it is never loaded at
invocation; read on demand). Versions match SKILL.md frontmatter `version:`.
Layer-wide structural events (bucket renames, folder moves) also land here,
since this orchestrator owns the layer contract. Newest first. Rollup lives in
the plugin-level `CHANGELOG.md`. The type specialists keep their own
`CHANGELOG.md` in their own folders.


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
