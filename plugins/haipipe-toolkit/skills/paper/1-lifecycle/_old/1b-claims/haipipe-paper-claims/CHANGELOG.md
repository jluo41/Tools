haipipe-paper-claims — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## 5.5.1 — 2026-07-19 — vocabulary: a probe question is an ENTRY, not a SECTION

### Changed
The probe file's unit of one question was renamed `## Q-<Stage>-<n>` SECTION (flat `serves:` /
`target:` / `a-consumer:` fields) -> `## QX<n>` ENTRY (four `###` subsections) when the probe model
changed. This file still said SECTION, so an agent reading it wrote the OLD flat structure, which
`check-probe-cards.sh` FAILs as `stale-old-format` -- that stage's PROBE phase could then never go
green. Mechanical rename, no design change. (JL ruling 2026-07-19, board 260719-04-SEED-2PHASE D5:
"如果这样的话，那还是叫entry 吧". Swept 31 lines across 15 files; phrase-level, because "section"
also legitimately means a MANUSCRIPT section in these docs.)

## 5.5.0 — 2026-07-19 — questions this stage typically raises

From `_console/closed/260719-01-DRAFT-RAISE-QUESTIONS.md` (R1).

### Added (JL: "是不是我们给每个stage写上，我们这里要写什么东西，一般会问到什么类型的问题？")

- **`## Questions this stage typically raises`** — the kinds of question this stage is PRONE to, named so a drafter can hunt for them instead of only stumbling into them. Until now nothing anywhere said how to FIND a question worth raising: `probe`'s DRAFT rule 2 opened "For each open question", presupposing it already existed, and the DRAFT workers only had a trigger ("when the search reveals a gap"). The mechanical half was covered — placeholder sweeps find missing numbers and citations — but the JUDGMENT half, the questions a stage is structurally prone to, had no home.
- This stage OWNS its list; the DRAFT worker points here and never restates it. One home.
- Not invented: the four `PROBE:` lines that had been sitting in `haipipe-paper-draft`'s Stage-specific notes were exactly this content, filed under the wrong PHASE (they assigned question ELICITATION to PROBE, against `probe`'s PROBE rule 1). This is where they belong.

## 5.4.0 — 2026-07-19 — the two-stage `supported` test names the real probe fields

Two vocabulary rulings from JL, both dated 2026-07-19, applied across `paper/`.

**Ruling A — the `probe` nickname.** JL: "宪法 don't use this name, just use `probe`." Every "THE CONSTITUTION" / "the constitution" / "the probe constitution" naming `probe/haipipe-probe/SKILL.md` is replaced by `probe` or by the actual path, whichever reads better at the site. A nickname already in the repo is still a nickname.

**Ruling B — the `a-consumer:` probe-file field.** `- a-consumer:` as a FIELD IN A PROBE FILE was replaced by the entry's `### a-executor`; `check-probe-cards.sh` HARD FAILs it under the `stale-old-format` rule. The a-consumer CONCEPT is untouched and still named a-consumer: it is the per-consumer interpretation written in the STAGE DOC (station ②), anchored `[source: PP<NN>]`. Prose that said "the probe section carries its `a-consumer:`" was wrong twice over — probe files hold ENTRIES, not sections, and what an entry carries is `### a-executor`.

Current model, for reference:
```
QA file (bank)  ->  the ENTRY's `### a-executor`  (probe file: the copy, single source of truth)
                ->  each Q-consumer's a-consumer  (STAGE DOC: what it MEANS for this consumer)
                ->  stage content                 (REVISE weaves it in, discharges the bracket)
```

Written under JL's NO TOMBSTONES rule (2026-07-19): "不需要留退役告示,直接抹除任何痕迹" then "follow this rule to do all the following changes." The docs state only the current contract; this CHANGELOG carries the history.

### Changed — the frontmatter `summary:` (ruling B)
"The PROBE phase raises questions as SECTIONS in 1-probes/ and runs the five-step loop; a section's a-consumer FEEDS this ledger" -> "...raises questions as ENTRIES in 1-probes/ ...; the entry's `### a-executor` and each Q-consumer's a-consumer FEED this ledger." This one nearly escaped: a verification grep piped through `grep -v CHANGELOG` silently drops every frontmatter `summary:` line, because each ends with "History: ./CHANGELOG.md." Filter on the FILE (`grep -v '/CHANGELOG\\.md:'`), never on the word.

### Changed — "It is the ONLY home of a claim's status" (ruling B)
"A probe section carries the evidence's MEANING for this paper (its `a-consumer:`)" -> "A probe entry carries the evidence itself (its `### a-executor`) and each Q-consumer's a-consumer, here in this stage doc, says what that evidence MEANS for this paper". The old sentence collapsed two stations into one and put the surviving one in the wrong file.

### Changed — the status-settling line (ruling B)
"written at INTERPRET when a probe section's `a-consumer:` lands" -> "written at INTERPRET when a probe entry's `### a-executor` lands and its Q-consumer's a-consumer reads it".

### Changed — the two-stage `supported` test (ruling B, the contract clarification behind the minor bump)
Stage 2 read: "a probe section whose `target:` QA file RESOLVES on disk and whose `a-consumer:` says that number carries the claim." It now reads: "a probe entry whose `**target**:` QA file RESOLVES on disk, whose `### a-executor` carries the answer, and whose Q-consumer's a-consumer here says that number carries the claim." This is the gate an author actually runs before flipping a claim to `supported`, and it was pointing at a field that fails the checker — so the test could never be satisfied as written.

## 5.3.0 — 2026-07-19 — `_VALUES_1b-claims.md` / `_CITATION_1b-claims.md` sidecars RETIRED

The claims stage still told its reader to keep two stage-local registries. The sidecar working docs (`_CITATION_*`, `_VALUES_*`, `_DISPLAY_{stage}*`, `_DISCOVERY_*`, `_EVIDENCE_*`) are all retired across the paper layer: `1-probes/` is the only consumer-side source of truth and `_LOG_<stage>.md` the only sidecar. Two lines survived the earlier sweeps — the artifact section's "Verified numbers live in ... citation candidates in ..." and the PROBE phase line's `numbers -> _VALUES_`.

JL ruling on the removal style, 2026-07-19: "不需要留退役告示，直接抹除任何痕迹" / "follow this rule to do all the following changes." SKILL.md states only the current contract; the retirement is recorded here.

Changed
- The artifact section's sidecar line is replaced by the placeholder contract: an owed number is `{VAL:? <what>} [Q-Claim-<n>]`, an owed citation `\cite{TOADD} [Q-Claim-<n>]` — the marker and the anchor bracket sit side by side, NEVER fused, and the bracket names the question that will produce it. A placeholder with no bracket is a defect (a hole no question will ever fill). The number lands in that question's `Answer`, sourced from the QA file its entry's `target:` names.
- PROBE phase line — `the claim's status FLIPS here, numbers -> _VALUES_` → `... and each verified number lands in the Answer of the Q-Claim-<n> that owed it`. The COLLECT step no longer writes to a registry that does not exist.

## 5.2.0 — 2026-07-18 — Q-consumer under the charter; M:N claims↔questions; Evidence Campaign cut

Adopted the stage-template charter (`../../TEMPLATES.md`, JL 2026-07-18). The claims ledger keeps Hypotheses + Claims; the question section is standardized and made many-to-many; the Evidence Campaign scoreboard was deleted.

Changed (`ref/claims-template.md`)
- `Probes` → `Q-consumer`, uniform shape: `## Q-Claim-<n> · <title>` + `Description` / `Reason` / `Answer` (was `## Q<n>` + free-text). STAGE-PREFIXED ids `Q-Claim-<n>`.
- ANSWERABLE + SPECIFIC rule (JL): each question is a concrete check a task/discovery can answer with a definite result; decompose a big claim into several small questions, each a different ANGLE (fit/eval/robustness/placebo/IV/external), named in the title; never a broad "is the effect real?".
- M:N (was implicitly 1:1): a claim is settled by SEVERAL questions, and a question may settle SEVERAL claims. Each claim's `Evidence:` line LISTS its questions — `Evidence: [Q-Claim-1] [Q-Claim-2] …` (was `-> PP<nn>`, one); `Reason` names the `C<n>`(s) it settles. AGGREGATION rule: `supported` only when the claim's required angles CONVERGE; a shared question feeds every claim it settles; the PP source lives in the Q's `Answer` as `[source: PP<nn>]`.
- DELETED the `Evidence Campaign` section (dispatch order + PP ledger table): its status/claims columns duplicated the Claims section + the citations, its dispatch/PP tracking is the probe layer's. Nothing lost (JL 2026-07-18).
- Fill rules moved INTO the template as `<!-- RULE -->` comments (follow then delete); top TEMPLATE marker added.
- The loop closes at REVISE: each Answer feeds the status of every claim it settles.

SKILL.md
- `Probes` → `Q-consumer` (description, summary, DRAFT, artifact list); `-> PP` claim ref → `Evidence: [Q-Claim-<n> …]`; DRAFT gained the answerable / decompose / M:N note; artifact list dropped Evidence Campaign ("three sections + a campaign summary" → "three sections"); v5.1.1 → 5.2.0.


## 5.1.0 — 2026-07-14

Probe redesign (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14). Mirrors haipipe-application-claims 5.2.0.

- **THE CLAIM LEDGER IS NOW THE ONLY HOME OF A CLAIM'S STATUS.** R7 killed the probe `## Verdict` block and the `verdicted` state. `supported | refuted | inconclusive` + confidence + claim_type + G1/G2/G3 are written HERE, per-claim, per-paper, private. A probe section's `reading:` FEEDS this ledger; it no longer carries a judgment of its own. New "judgment fields" block in the Artifact Spec.
- Two papers reading the SAME bank fact may judge their own claims differently — the fact is shared, the judgment is not (new Principle 6).
- PROBE phase described as the five-step loop (ORGANIZE -> MATCH -> DISPATCH -> POINT -> INTERPRET); "backfill confirmed verdicts, spawn probe plans" is gone.
- The evidence pointer is the section's `target:` — a QA file path that must RESOLVE on disk. The two-stage evidence gate restated on that basis (Principle 11).
- Ledger PP entries carry a DERIVED `State:` (`planned | commissioned | answered | read`); the `dispatched` state is DELETED (ref/claims-template.md updated to match).
- `1-probes/PPNN_<topic>.md` named as the probe FILES; the per-stage `_PROBE/` folder and the `1-probe-plans/` index are RETIRED.
- New Principle 15: this stage never executes bank work inline (LAW 1).

## [5.1.1] — 2026-07-14 — the required-reads were off by one `../`

Fixed
- **The first instruction in this skill pointed at nothing.** `Read first: ../../PHILOSOPHY.md, ../../<shared-refs>/04-lifecycle-map.md` — but this skill lives at `skills/paper/1-lifecycle/<N>-<stage>/<skill>/`, so `../../` is `1-lifecycle/`, which holds neither `PHILOSOPHY.md` nor the shared-reference folder. Both live one level further up, at `skills/paper/`. Every in-body citation (stage-gate, comment-lifecycle, stage-illuminate, delivery-need, `../../_venue/playbook-<venue>`) failed the same way, silently — an agent loading the philosophy and the stage-gate rules got file-not-found and proceeded without them. All repointed to `../../../`; every target verified to resolve on disk.

## [4.5.0] — 2026-07-14
## 5.0.0 — 2026-07-14

- PROBE REDESIGN (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14 — R1-R18). 1-probe-plans/ -> 1-probes/ (PPNN_<topic>.md, one file per TOPIC, one SECTION per question: serves/target/state/commission/reading + ONE `## Why` per file holding the stake). Binding is by PATH: a section's `target:` points at the answering `<leaf>/QA/<n>-<slug>.md` in the bank. DELETED: `## Verdict`, the `verdicted` and `dispatched` states, `_ASK/`/`_ANS/` stubs, `answers:`, and Agent(haipipe-probe-orchestrator-agent) (the GATEWAY — archived + de-registered). A claim's STATUS now lives ONLY in 0-lifecycle/1b-claims/1b-claims.md. Dispatch is now DIRECT: the section's `commission:` block, VERBATIM, to Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent).
- `--backfill` no longer reads a probe VERDICT (there is none — R7 deleted it). It reads the probe SECTION's `reading:` (+ the Agent(haipipe-probe-reviewer-agent) judgment for a `mode: full` section) and writes supported|refuted|inconclusive + confidence + claim_type + G1/G2/G3 HERE. The evidence pointer is the section's `target:` QA-file path, which must RESOLVE on disk.

Fixed (forward-pointer DOUBLE CONSUMPTION -> permanent claims deadlock)
- **RESOURCE is now the SOLE consumer of seed's FORWARD pointers.** 4.4.0 landed the resource stage with its own DRAFT consume-grep (`\[FORWARD (->|→) (RESOURCE|CLAIMS)\]`, glyph- and legacy-tolerant) but left claims' 4.1.0 reader clause standing. Both stages then owned the same 7 live pointers on disk (4 in Paper-ScalingGlucose, 2 in Paper-PersonalizedGlucoseModel, 1 unicode-arrow in Paper-CGMtoCyclePhase — every one says `CLAIMS`, because they were written before the resource stage existed). Resource consumes them at its DRAFT; claims' done-criterion demanded no unconsumed `[FORWARD -> CLAIMS]` pointer remain — a bar claims could never clear, since the pointer LINE stays in `_LOG_0-seed.md` after resource takes it. Result: a PERMANENT DEADLOCK at the claims CHECK gate, or a double-dispatch of the same build if the agent "consumed" it again as a PP entry.
- **DRAFT consume clause DELETED.** Claims DRAFT no longer greps `_LOG_0-seed.md`. It opens on `1a-resource.md` (the N demand rows and their Q/A) and reads `_LOG_1a-resource.md` for the pointers resource explicitly DECLINED to claims — those, and only those, become PP entries in Probes.
- **Done-criterion REWRITTEN**, from "no unconsumed `[FORWARD -> CLAIMS]` pointer in seed's `_LOG_0-seed.md`" to "no pointer that RESOURCE explicitly DECLINED to claims (per `_LOG_1a-resource.md`) is left unconsumed here". A pointer resource re-routes to claims is still caught; a pointer resource consumed is DONE and is not double-counted. The 4.1.0 writer-without-reader gap (A5/B9) stays closed — the reader simply moved one stage upstream.
- Companion edit: `2-phase/1-probe/haipipe-paper-probe/ref/per-stage-dispatch.md` claims row no longer says it consumes seed's pointers; `2-phase/0-draft/haipipe-paper-draft/SKILL.md` seed + claims stage-notes now name RESOURCE as the consumer.

## [4.4.0] — 2026-07-14

Changed (JL ruling 2026-07-14: the RESOURCE stage lands between seed and claims)
- **Boundary moved.** The probe-type table now leaves claims with exactly ONE row — `evaluate` / `task-for-eval`, the probe that produces the VERDICT. `input` / `task-for-data`, `method` / `task-for-algo` and `fit` / `task-for-fit` MOVE OUT to the new venue-free RESOURCE stage (`0-lifecycle/1a-resource/1a-resource.md`, skill `haipipe-paper-resource`). Cleavage rule stated in place: a question that CHANGES what exists on disk -> RESOURCE; a question that READS what exists and MOVES A CLAIM'S STATUS -> CLAIMS. A claim CITES the resource answer (its `N<n>` row and that row's Q/A) instead of re-planning the build inside the argument document. Claims' own two rules ("the evaluation probe settles the claim"; "task settles claims, discovery is reserved for method-investigation + external data/context") are UNCHANGED, verbatim.
- Ledger Maintenance route block follows the same cut: dataset / model / new-method routes are no longer claims probes — they are DEMANDS owned by resource, and the claim waits as `BLOCKED-ON-RESOURCE`.

Added
- **Claim status `BLOCKED-ON-RESOURCE`** (status vocabulary, Evidence Gate, done-criteria, Artifact Spec). A claim whose resource is UNOBTAINABLE or not yet built is NOT a "GAP with a plan" — it is UNFALSIFIABLE, it carries no probe entry here, and it names the `N<n>` demand row it waits on. Live case: Paper-CGMtoAge's H2 and H3 both depend on a dataset whose access application has not been filed.
- **Inputs (binding) clause** after Read-first, and a read step in the DRAFT phase block: claims READS `0-lifecycle/1a-resource/1a-resource.md` before writing, and may not assert a claim whose demand row has no resource. Retires the "Feasibility & constraints (preconditions, not claims)" material that used to squat in live claim ledgers (`1b-claims.md:48`) — preconditions are resource's business now.

## [4.3.0] — 2026-07-10

Added (JL, Paper-CGMtoAge session)
- Probe Plans now organize by **pipeline stage / task type**, not only urgency: one probe = one unit of work = one haipipe task type (`task-for-data` / `task-for-algo` / `task-for-fit` / `task-for-eval`). Explicit anti-monolith rule — do NOT bundle build+fit+evaluate into one probe; decompose so each stage is independently runnable/resumable (real incident: a bundled build+fit+eval probe had to be stopped and split mid-run).
- Two rules codified: (a) **the evaluation probe settles the claim** — a claim's evidence pointer names the eval probe, which chains back fit <- data (a bundled fit+eval entangles the verdict); (b) **task settles claims, discovery is reserved for method-investigation + external data/context** (discovery alone never settles an internal experimental claim; it feeds `task-for-algo` or supplies an external cohort/citation).
- Ledger Maintenance route table expanded to name task types (dataset->for-data, model->for-fit, verdict->for-eval, new method->discovery+for-algo).
- Layered on top of 4.2.0 (verbs/gates); the two changesets touch disjoint SKILL.md regions, no content overlap.

## [4.2.0] -- 2026-07-09

Changed (JL ruling 2026-07-09 (LLMTrait-Section session postmortem): normalize the writing process)
- Phase VERBS on the stage (`claims <paper-dir> [draft|probe|revise|check]`); bare invocation = status, user's verb advances.
- Hard gates + binding comment rules inlined (STOP after DRAFT with [GATE] log; Skill() dispatch proof; [REVISE] workers line; never delete `> USER:` comments; surgical edits only).

## [4.1.0] — 2026-07-07

Added (skillset-diagnose T3, JL: "同意。")
- FORWARD reader clause: the `[FORWARD -> CLAIMS]` pointers that seed/draft register in `_LOG_0-seed.md` (internal-data probes deferred out of seed) now have a consumer — claims DRAFT opens by grepping seed's `_LOG` for them; each becomes a PP entry in Probes or is explicitly declined; a new done-criterion fails CHECK on any unconsumed pointer. Closes the writer-without-reader gap (A5/B9): the deferred probe used to die silently at the seed→claims handoff.

## [4.0.0] — 2026-07-06

Changed (major restructure: claims as evidence campaign brain)
- Claims is now the evidence campaign brain: plans evidence needs, commissions work (tasks/discoveries), tracks results. Three jobs: plan, outsource, collect.
- Content structure changed from (Hypotheses, Claims with inline design, Pending Evidence, H-C Alignment) to three sections + summary: Hypotheses, Claims (short: statement + status + probe ref), Probes (full evidence plan per PP number), Evidence Campaign (dispatch order + summary).
- Removed Hypothesis-Claim Alignment section (alignment visible in tags: `C1 (H1)`, `PP03 (C1/C3/C7)`).
- Removed Discussion-Only Interpretations, Robustness, and Pending Evidence sections (probes absorb these roles).
- Added _VALUES_ satellite file for verified numbers backing each supported claim.
- Heading style changed from `#`/`##`/`###` to `=====`/`-----` underlines + `**bold**` sub-items for paper artifacts.
- One-sentence-per-line convention added as a formatting principle.
- Updated ref/claims-template.md to match.

## [3.2.0] - 2026-07-05

Changed
- Ledger is now PROSE ONLY, no tables. Dropped both markdown tables from ref/claims-template.md: the Claim-Evidence Matrix (`| ID | Claim | Status |`) is replaced by a `## Claims` section of one `### C<n> - <title> (<H>, <role>) - <status>` prose subsection per claim, and the Hypothesis-Claim Alignment table is replaced by a paragraph. Scrubbed all "matrix"/"row" language from SKILL.md (Artifact Spec, done-criteria, DRAFT step, template reading order, gates, Ledger Maintenance) and rewrote principle 6 as "Prose subsections, no tables". Codifies JL's standing rule (papers/ledgers never group claims/evidence in tables) so the template stops regenerating them.

## [3.1.3] — 2026-07-03

Changed
- Added the Phase Transition Contract pointer (08-stage-gate.md): announce every phase boundary, no silent phase skips (explicit logged verdict only), CHECK never implicit.

## [3.1.2] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE; workers haipipe-paper-probe*, haipipe-paper-revise*).

## [3.1.1] — 2026-07-03

- converted canonical template to ref/claims-template.md (plain markdown, no LaTeX, no compile); deleted ref/claims-template.tex.

## [3.1.0] — 2026-07-03

- claims becomes stage orchestrator that drives its own phases. Phase skills (draft/gather/polish/check) are internal workers called by this skill, not user-facing. Removed inline workflow steps and shared-protocol references. Comment lifecycle wired in.

## [3.0.0] — 2026-07-01

- claims is now venue-FREE. Editor's Chair Test, [primary] designation, and venue-shaped RQs migrated to pitch (the cover letter). Claims keeps venue-neutral hypotheses (H1, H2, H3) and a pure evidence inventory reusable across venues.

## [2.0.0] — 2026-06-29

- switched from .tex to .md + _LOG. Argument documents are markdown; only display compiles to PDF. Claims create PP probe plans in 1-probe-plans/ for evidence gaps.

## [unversioned]

- v1.3.0: added editor's chair test, RQs in claims (not pitch), RQ→Claim→Answer alignment table, probe plans buffer convention, extracted template to ref/claims-template.tex

## [unversioned]

- v1.2.0: added illuminate protocol + cross-refs to stage-gate, tex-quality
