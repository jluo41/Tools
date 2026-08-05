haipipe-probe — Changelog
=========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## [0.11.2] — 2026-08-04 — Probe is the concept

- Canonicalizes the user-facing vocabulary as PROBE phase, lowercase probe exchange, and persisted Probe record or Probe Page.
- Keeps `entry` only as a legacy label in checker names, paths, and executable schemas, not as another Page Type or lifecycle concept.
- Leaves the Q-consumer, Q-executor, A-executor, and A-consumer model unchanged.

## [0.11.1] — 2026-08-01 — Board section labels are paired plurals

- Emits Q-consumer status rows under canonical `## States`; one row is still
  the singular State record paired with one Aim.

## [0.11.0] — 2026-08-01 — Board Q-consumers are Aims with State

- Replaced Board-first checklist records in `## Items to Finish` with
  Content-linked records in `## Aims`.
- Gave every such Aim one separate factual `## State` row while preserving the
  consumer-local Q id used by PROBE.

## [0.10.4] — 2026-07-26 — Q-consumer is a logical role

- Defined the consumer-family adapter: Board-first paper S pages store
  Q-consumers as checklist records in `## Items to Finish`; non-Board
  consumers may retain a literal section.
- Kept Description, Reason, Probe, and Answer together while ensuring Content
  contains only the stage's substantive product.

## [0.10.3] — 2026-07-26 — audit copy is not a dispatch leak

- Resolved the stake contradiction: the authoritative stake remains in the
  stage doc, while its original wording may appear only in the review-only
  `### q-consumer` copy. It is forbidden in q-executor, a-executor, collector
  payloads, bindings, and the bank.
- Canonicalized paper's terminal `concern` state to match the executable
  checker: `route: none`, no bank/target, and final `discussed:` receipt.
- Kept one universal file anatomy: even `concern` requires all four
  subsections and a real stake-free q-executor; it is recorded but never
  dispatched.

## [0.10.2] — 2026-07-26 — bank and target agree

- Made MATCH deterministic: `reuse` always targets an existing QA answer;
  `run` / `code` / `new` carry `NEW path` until the executor returns one.
- This removes the last canonical wording that permitted an impossible
  `reuse` binding without a readable QA file.

## [0.10.1] — 2026-07-26 — one topic folder, one file per q-executor

- Corrected the opening definition to match the operative anatomy.
- Repointed the rationale to the live first-class Probe design Board under
  `skills/diagrams/01-probe-qa-260726/`.
- Removed historical topology wording from the current operational contract
  and synchronized the fillable template: DRAFT raises Q-consumers only,
  PROBE authors entries and dispatches through the collector.

## [0.10.0] — 2026-07-26 — one phase owner, one dispatch wall

- Made the current phase model executable in one way only: DRAFT writes stage
  content and Q-consumers; PROBE owns ORGANIZE through INTERPRET; CHECK is the
  current human gate.
- Removed the retired DRAFT│PROBE approval gate and the conflicting rule that
  made DRAFT author/match probe entries.
- Standardized dispatch through `haipipe-probe-q-executor-agent`; the collector
  alone calls the task/discovery executor orchestrators in its isolated context.
- Removed the unsupported `argument-hint` frontmatter key.

## [0.9.9] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 9.9.0; older entries below keep their original numbers).

## 9.9.0 — 2026-07-20 — probe files are a FOLDER of one-q-executor files (flat RETIRED)

Owner co-design (JL): "a q-executor a file, and several q-executor a folder in 1-probes … break down the current PP markdown" + "don't 向后兼容 … 全面推 folder 为默认". A probe TOPIC is now a FOLDER `1-probes/PPNN_<topic>/` holding one `## QX<n>` entry per `QXn_<slug>.md` file — each q-executor path-addressable and single-purpose. The flat single-file `1-probes/PPNN_<topic>.md` is RETIRED, not deprecated: the checker no longer globs it. (No backward-compatibility window — the owner ruled it out; the only flat files on disk were this paper's and the test fixture, both migrated in this change.)

### Changed — check-probe-cards.sh is folder-only (paper + application, kept in step)

PASS 1's loop glob changed from `1-probes/PP*.md` to `1-probes/PP*/*.md` (flat dropped, not added-alongside). Each file still carries its `## QX<n>` heading, so the section-splitter awk is UNCHANGED — only the glob. The resource-stage backlink resolver (paper-only) now resolves `1-probes/<q_pp>*/*.md`; the legacy `1-probe-plans/` + `0-lifecycle/*/_PROBE/` globs are a SEPARATE loop and untouched (pre-v8 history still surfaces as MIGRATE). The `no probe files` WARN text updated. Verified on the fixture regression harness (`test/run-checker-tests.sh`, folder fixture → same FAIL/PASS/CONCERN code per entry) AND on this paper (`--stage seed` exit 0).

### Migrated — this paper + the checker's own test fixture

`papers/Paper-Personality2Opioid-MISQ2026/1-probes/`: `PP01_seed-feasibility.md` (QX1, QX2) and `PP02_discretion-mechanism.md` (QX1) → `PP01_seed-feasibility/{QX1_novelty,QX2_obtainability}.md` and `PP02_discretion-mechanism/QX1_precedent.md`. The checker's `test/fixture/.../PP01_states.md` (5 state cases) → `PP01_states/QX{1..5}_<slug>.md`. Both extractions verified byte-faithful (concat(new) == flat-from-first-`## QX`, empty diff); only the redundant `# PP<NN> —` H1 header dropped (the folder name carries the topic).

### Anchors re-pointed to paths (the `PP·QX` double-id is gone)

In `0-seed.md`: the stage-doc `**Probe:**` pointers, the `> CHECK:` refs, AND the `[source: …]` a-consumer tags all path-ified from `PP·QX` to `PPNN_<topic>/QXn_<slug>.md`.

### Documented + propagated folder-only across the whole skill tree

This layer's `ref/probe-template.md` (What-this-is + filled-section shape) and `SKILL.md` (The probe file, flow diagram, pointer convention, frontmatter description) were rewritten to folder-only by hand. Then the flat placeholder `1-probes/PPNN_<topic>.md` was replaced by the folder form `1-probes/PPNN_<topic>/` in ~140 more files (`grep -rl` → `sed`), covering the WRITE side and every doc: the paper + application PROBE and DRAFT workers, all 8 paper `stage.md` contracts' `probes:` field, the ~90 venue section templates' probe references, the application lifecycle + stage skills, the probe collector agent + `probe/agents/README.md`, `project/`, `discovery/`, and the lifecycle/anatomy refs. The two PROBE workers' write instruction additionally NAMES the entry file — `.../PPNN_<topic>/QXn_<slug>.md`, one q-executor per file — so an authoring agent knows the filename, not just the folder. Only `_console/` history and the deliberate `RETIRED`-context mentions (this CHANGELOG + `SKILL.md`/`probe-template.md`) keep the flat form. Checker green throughout (`--stage seed` exit 0; the fixture regression harness exercises all five entry states in the folder layout).

## 9.8.0 — 2026-07-20 — free-text bodies are one sentence per line (readability)

Owner ruling (JL; this file is shared by paper + application, so the change is owner-gated): "we want the one sentence one line version". Motivated by a real instance — a harvested `### a-executor` (papers/Paper-Personality2Opioid-MISQ2026, PP01 QX1, the novelty prior-art digest) had grown into a wall of prose JL found hard to read, and asked for the fix at the template, not the instance.

### Changed — a formatting rule for the free-text BODIES, in ref/probe-template.md

The probe file's prose bodies — the `### q-executor` question, the `### q-consumer` originals, and the `### a-executor` answer — are now written ONE SENTENCE PER LINE (semantic line breaks), no dense paragraphs; when a body lists sources, one source per bullet. The `### q-executor` already carried "one sentence per line" (SKILL.md:76); this generalizes it to every body and names the `### a-executor` — the longest body, and the one a human actually reads — explicitly, in both the filled-section note and the a-executor field guide.

### Changed — the `### q-consumer` id is bold

Owner request (JL: "why not make it to be `**Q-<Stage>-<n>**`"). The q-consumer bullet's stage-doc id is now written bold — `**Q-<Stage>-<n>**` — so it stands out at a glance in a long entry. Checker-safe: the `--stage` gate greps the q-consumer text for the stage word as a substring (e.g. `q-seed`), and the `**…**` decoration around the unchanged id text does not affect the match. Applied to the template shape + the q-consumer field-guide entry.

### Changed — navigation emojis in the template GUIDANCE

Owner request (JL: "add the emojis to the probe template ... so we are easier to follow"). The guidance now carries emojis: the top-level section headers (🧭 what-this-is · 🔀 executor/consumer · 🪜 three-homes · 📋 filled-section · 📖 field-guide · ✍️ for-the-creator · ➕ optional), plus a four-emoji mnemonic for the subsections — 📤 q-executor · 🙋 q-consumer · 🔗 bank binding · 📥 a-executor — repeated on the Field-guide entry headers, which use an emoji-plus-name LABEL form (`📤 q-executor  (the question OUT)`, `----`-underlined) rather than the `### ` token — so the guide never shows a `### `-name that a reader might copy with an emoji still attached. SCOPED TO GUIDANCE ONLY: the copied "filled section" skeleton (`## QX<n>`, the four bare `### ` names, the `**field**:` lines) stays emoji-free, so real probe files parse identically. The emojis live where a human reads to follow the format, never where the machine reads to check it.

### Validated — fresh-context subagent (CLAUDE.md skill-validation protocol)

A fresh-context agent, given only the template path and a realistic "author one entry" task, produced the format correctly: one-sentence-per-line bodies, a bold `**Q-Claim-4**` q-consumer id, and the four bare `### ` skeleton names + `**field**:` lines left clean. It flagged ONE ambiguity — the first cut put the emoji ON the Field-guide `### ` names (`### q-executor 📤`), the same token the filled section shows bare, a possible copy-the-emoji trap. Fixed by the LABEL form above (Field-guide headers carry no `### `). Checker unaffected throughout: `check-probe-cards.sh --stage seed` = exit 0 before and after, including on the two instances reflowed to the new format (PP01, PP02).

### Why it does NOT touch the checker

The rule is scoped to BODIES only, never the skeleton. The machine tokens `check-probe-cards.sh` parses — `## QX<n>`, the four `###` subsection names, and the `**field**:` lines (`**state**:`, `**bank**:`, `**target**:`, `**eta**:`, …) — are never wrapped or split, so every awk/grep match is unchanged. The `### a-executor` is only checked non-empty and is never leak-scanned; the `### q-executor` leak scan is per-line, so extra line breaks only make it finer-grained. No `check-probe-cards.sh` logic changed.

### Not done here

Existing probe-file instances were NOT reflowed by this change (the template governs new/edited entries). Reflowing a live a-executor is a separate, per-instance edit. The global marketplace copy (`~/.claude/plugins/marketplaces/jluo41-tools/…`) is a separate copy from this Tools source; re-run `install.sh --global` to propagate beyond the symlinked project.

## 9.7.0 — 2026-07-19 — DRAFT rule 2 no longer presupposes the question

From `_console/closed/260719-01-DRAFT-RAISE-QUESTIONS.md` findings B3 and D5 (JL: "可以直接去改" — this file is shared by paper and application, so the change was gated on the owner).

### Changed — B3, the missing half of DRAFT rule 2

Rule 2 opened "For each open question: raise a `## Q-<Stage>-<n>` …", which presupposes the question already exists. Nothing in this file, or in either DRAFT worker, said how to FIND one. The mechanical half was covered (a placeholder sweep finds missing numbers and citations); the JUDGMENT half — the questions a stage is structurally prone to — had no home at all. Rule 2 now opens with FIND, and points at each stage skill's own `## Questions this stage typically raises` (new, in all 16 stage skills), naming the shape per family so a reader sees what kind of thing is meant.

### Changed — D5, ENTRY is the only word for an entry

The file used "section" and "entry" interchangeably for the same object — "An entry's parts" (:162) against "Per SECTION:" (:96) and "MOST sections should land on T2" (:219) — and `haipipe-paper-draft` had inherited the drift. 11 sites normalized to ENTRY: the build-lane clause, the cost ladder's T2/T3/T4 rungs, the dispatch payload, the supersession clause, the derived-state table, and the self-review checklist header. "Section" now means only what it means in a stage doc.

## [9.6.0] — 2026-07-19

- ⑨ TOMBSTONES erased. Owner ruling (JL): "不需要留退役告示,直接抹除任何痕迹" — a doc states the CURRENT contract and never names the dead thing.
  "There is no `## Why` in a probe file" and the DRAFT self-review's "no `## Why` and no stake anywhere"
  both restated as where the stake DOES live (the stage-doc Q-consumer).


## [9.5.0] — 2026-07-19 — PROBE FILE REDESIGN: Q-executor-oriented, many-to-one, a-executor copy (matches ref/probe-template.md)

JL co-design 2026-07-19 (branch "C-P-E-Skill-Update-Probe-Template"). The probe file is redesigned to be Q-EXECUTOR-oriented, and the constitution anatomy is synced to `ref/probe-template.md`. Full record: `HANDOFF.md`.

- ENTRY = one Q-executor, id `QX<n>` (topic-local). Three id layers, none crosses the wall: `Q-<Stage>-<n>` (stage doc) · `QX<n>` (probe) · `QA/<n>-<slug>.md` (bank); they bind by PATH, never a shared id.
- MANY-TO-ONE: one q-executor may serve SEVERAL Q-consumers (reuse, structurally). `### q-consumer` lists them and COPIES IN each consumer's original question (review-only, never dispatched).
- `## Why` DROPPED. The stake lives in each Q-consumer, in the stage doc — never in a probe file.
- ANSWER: `### a-executor` = a COPY of the QA answer, the consumer-side single source of truth; the a-consumer (per-consumer interpretation) moves to each stage doc (station ②). The three-station chain is copy-then-anchor at each hop (QA → a-executor → a-consumer `[source: PP<NN>]` → content) — self-contained AND traceable.
- `serves:` → `### q-consumer`; `match:` → `bank` (a four-value verdict `reuse | run | code | new`, richer than EXISTS/NONE); `a-consumer:` (in the probe file) → `### a-executor`.
- FORMAT: entry `## QX<n>` + four `###` subsections (q-executor / q-consumer / bank binding / a-executor); short scalars are `**field**: value` under `### bank binding`; no `- field:` lines, no `|` block scalars, no indentation.

PENDING (see HANDOFF.md): `check-probe-cards.sh` ×2 not yet rewritten to this format — do NOT run the old checker on a new-format file. The DRAFT self-review checklist (9.3.0) is already updated for the new fields; stage skills + the application family still need the field-name sweep.

## [9.4.0] — 2026-07-19 — PHASE RULES: two followable checklists (DRAFT / PROBE) distilled from the loop

JL 2026-07-19: give each phase a CLEAN, followable rules checklist so a worker can act without wading through the whole model. New **Phase rules** section — a terse DO-THIS list per phase (DRAFT: author the plan → self-review → stop; PROBE: read the plan → dispatch NEW → point → harvest → verify), distilled from the five-step loop + the two LAWS + the self-review checklist. The family workers (`haipipe-paper-draft`, `haipipe-paper-probe`) POINT here for the shared rules and add only their family-specific rules; on conflict the model sections above win. No new files/skills — `ref/*.md` was considered and rejected as a redundant middle layer that would split the cohesive loop.

## [9.3.0] — 2026-07-19 — DRAFT SELF-REVIEW: a fresh-context reviewer checks draft + probe plan before the gate

JL addition 2026-07-19. Before the DRAFT human gate, a review sub-agent (fresh context — a creator/reviewer split) checks the phase's output: the draft against the stage's artifact spec, and the probe plan against the new **DRAFT self-review checklist** (q-executor LAW-2-clean · answerable+specific · route set · match ROOTED to a specific folder, read + judged on the answer · target agrees with match · heading id = Q-consumer id · one ## Why, stake never leaked). It reports; the drafter fixes and re-reviews (bounded); the verdict rides to the human gate. It PRECEDES the gate, never replaces it, and complements `check-probe-cards.sh` (which still runs at CHECK as the mechanical backstop — the reviewer judges what a regex cannot). The paper DRAFT worker (`haipipe-paper-draft` v4.2.0) implements it and adds the draft-prose checks; the application twin should mirror it.

## [9.2.0] — 2026-07-19 — PROBE PLAN MOVES INTO DRAFT: ①② at DRAFT, ③④⑤ at PROBE; two gates → one

JL ruling 2026-07-19 (paper co-design). The probe PLAN is authored during DRAFT, beside the stage draft, so ONE human gate reviews draft + probe plan together — the plan-review gate is MERGED into the DRAFT gate, not added as a second gate. The five-step loop is re-assigned to phases: ① ORGANIZE + ② MATCH run at DRAFT (the consumer organizes each Q-consumer into a probe section and ROOTS it to a SPECIFIC bank folder — a read-only bank grep, LAW 1), and ③ DISPATCH + ④ POINT + ⑤ INTERPRET run at PROBE, which RUNS FORWARD with no second gate (PROBE stays a milestone). Reverses the old "DRAFT writes only title+intent, does NOT pick route/answerer — unknown yet" and moves ORGANIZE from APPROVE to DRAFT.

Two new section fields, part of the DRAFT-authored plan: `route:` (the dispatch door `task | discovery`, AUTHORITATIVE — the executor executes it, not re-decides) and `match:` (the ② MATCH result rooted to a SPECIFIC folder: `EXISTS · <folder>` → link, or `NONE → propose NEW <folder>`). The consumer's route + folder are authoritative because at plan time it already knows which bank/partition holds the answer.

Heading id = the stage-doc Q-consumer id, CONSUMER-LOCAL (`Q-Seed-1`, `Q-Claim-6`; each family owns its scheme, ids never collide because a Q-consumer id never crosses the wall — only `q-executor` is shared). Dissolves the cross-family token question.

Mechanical change: the old "empty `target:` = not yet probed" DRAFT/PROBE discriminator retires (DRAFT now writes `target:`); `state:` is the sole marker of planned-but-unrun. Ripples: `ref/probe-template.md` already carries route/match + the `Q-<Stage>-<n>` heading; each stage skill's DRAFT/PROBE description and any "DRAFT never writes target:/a-consumer:" invariant must be re-swept.

## [9.1.0] — 2026-07-18 — the answer's THREE STATIONS (station ② restored, anchored)

JL ruling (cross-family, paper co-design): the harvested answer is SELF-CONTAINED in the stage doc, not probe-file-only. New section **"The answer's three stations"**: ① probe file `a-consumer:` (evidence) → ② Q-consumer `Answer:` in the stage doc, anchored `[source: PPnn]` (self-contained Q&A + review checkpoint) → ③ stage content (woven at REVISE). Replaces the old "the stage doc keeps only the human question + the pointer / never copied back": station ② IS a copy-back, but ANCHORED (the anchor points at ①, which points at the QA file — traceable, not fabricable). Applies to paper AND application; the concurrent application `qconsumer-nosidecar` session had dropped station ② and must re-add it (see `diagram/260718-qconsumer-nosidecar/PAPER-3STATION-AMENDMENT.md`). No-sidecar (application D6) is compatible — ② is one anchored `Answer:` line, not a `_VALUES_`/`_CITATION_` doc.

## [8.3.0] — 2026-07-14 — R19 HARDENING: four holes the v8.2 rollout left open

Follow-up to 8.2.0 (the state line). Each item below was a live runtime failure, not a style nit.

**(a) R14 is SCOPED to `state: answered`.** R14 said "a hit counts ONLY if the QA file LITERALLY ANSWERS THIS question; if it does not, it is a T3 ENRICH — dispatch it". A `working` file's `## Answer` is EMPTY BY CONSTRUCTION — that is what `working` MEANS, and the CLAIM idiom writes it empty on purpose. So a `working` file can NEVER pass R14's test, and R14's own remedy sends the reader to DISPATCH: consumer #2 re-runs the SAME expensive job consumer #1 is three hours into, with a different slug, so `set -C` never fires. **The exact failure R19 exists to kill, executed by obeying R19's own text.** Now: THE STATE LINE IS READ FIRST, BEFORE the literally-answers test, on EVERY reader — the consumer's ② MATCH and BOTH executor ① SCANs. A `working` file is matched on its `# Q —` LINE: if that restated question IS my question it is a HIT-IN-FLIGHT (commission + point, NO dispatch / return "in progress since <started>").

**(b) The IN-FLIGHT LOOP is CLOSED.** The MATCH→`working` path issues NO DISPATCH by design, so those sections have NO live return, EVER — and nothing tested a `commissioned` section's target. A section whose answer LANDED sat GREEN until its eta expired (weeks), with the claim it serves unsupported by evidence already on disk. New checker teeth: `commissioned-target-answered` (harvest it) and `commissioned-target-superseded` (re-point). `working` still PASSES — that is the honest in-flight case, TTL-guarded by `qa-working-expired`.

**(b′) `owner:` / `eta:` on the in-flight path are DERIVED, never invented.** Nothing in the bank supplied them, so the agent had to FABRICATE a date at the gate whose whole purpose is to prevent laundering. Now: `owner:` := the target's `by:` (or `bank`); `eta:` := the target's `started:` + QA_CLAIM_TTL_HOURS. The checker's commissioned-liveness clock and the claim's TTL clock become ONE clock.

**(c) `state:` is MANDATORY, ALWAYS — a stateless QA file is MALFORMED, not "legacy".** The grandfather clause mapped a QA file with no state line to a kind that was EXEMPT from every claim check — so a lying receipt shipped BY OMISSION: drop one line, leave `## Answer` empty, gate green, and a consumer publishes a `reading:` derived from nothing. It had zero beneficiaries (no QA file predates the field on disk). New codes: `qa-no-state` · `read-target-no-state` · `commissioned-target-no-state`. The file's OWNER — the executor, never a consumer — adds the line.

**(d) WRITE-ONCE is retired in the REVIEWERS too.** The discovery reviewer's QA checklist still forbade editing a previously-existing QA file — which is EXACTLY what the completion (`working` → `answered`) and the supersession append ARE. It would have REVISEd every gate-③ Report on day 1. Replaced by BODY FROZEN (the `# Q —` / `## Answer` / `## Caveats` / `## Not-done` body is frozen; the `state:` line is the one mutable field, edited twice, by its owner). The task reviewer had NO QA checklist at all despite advertising one — it now carries the block token-identical.

Also: the FILENAME check in both reviewers carries the CLAIM-RACE exemption (a duplicate `<n>` from a same-instant/different-slug race is NON-FATAL by ruling — `ls QA/` indexes both — and must NOT be REVISEd), which the qa verb asserted and the reviewer contradicted. And the paper-side rebuttal `fn-task` no longer AUTHORS task folders under `tasks/` (a LAW-1 violation that planted rebuttal ids C10/B7 into the bank); it DISPATCHES.

## [8.2.0] — 2026-07-14 — THE QA FILE GAINS ONE MUTABLE FIELD: a TICKET that becomes a RECEIPT

JL ruling 2026-07-14 (`Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/` PART 3b, the `>> CC0714` block answering *"how about haipipe-task qa create the QA-task.md when it decide to generate it, and then give the status, saying we are working on it, so other probes will not ask the same questions"*). ADOPTED. This is the layer's ONE SOURCE for the new vocabulary; the task/discovery twins, the `qa` verbs, the probe workers and the checker copy the canonical strings from here.

**The hole it closes.** Until now a QA file was written ONCE, at REPORT, complete, and its EXISTENCE was the entire signal — `ls QA/` said *answered* or *not answered*, with no third state and no way to say **"someone is working on this right now."** So: two consumers ask the same question a week apart. The first dispatches an expensive P-B-E-R run. The second, **while that run is still going**, sees no QA file and dispatches **THE SAME RUN AGAIN**. Nothing prevented it. The same missing field also left the day-1/day-40 staleness hole open (v8.0 flagged it as ⛔ NOT SOLVED, two candidate fixes, neither ruled on).

Added — **R19, THE CLAIM.** A QA file now carries exactly ONE MUTABLE FIELD, the **state line**:
- `state:` — `working` | `answered` | `superseded-by: QA/<m>-<slug>.md`. The ONLY mutable field in the file.
- `started:` — `YYYY-MM-DDTHH:MM` (`date +%Y-%m-%dT%H:%M`). **MANDATORY on a `working` file.** A claim with no `started:` can never expire, so it is not a claim — it is a zombie by construction, and the checker FAILs it.
- `by:` — optional provenance (run id | agent | human).
- `## Answer` is **EMPTY while `working`**, filled at REPORT.

**⚠️ THE LOAD-BEARING INVARIANT IS *ONE WRITER*, NOT *WRITE-ONCE*.** The EXECUTOR writes the file TWICE — the **CLAIM** at the qa gate's (3) decision, the **COMPLETION** at REPORT — in its OWN folder, on its OWN file. Two writes by the same owner is fine; nothing is shared, nothing is planted, no lock is needed. **A CONSUMER (probe/paper/application) must NEVER create, claim, edit, complete, or supersede a QA file.** A consumer-authored `working` file is the retired `_ASK/` stub wearing a `QA/` costume — the sin was always the WRITER (a consumer planting a half-file in the bank), never the half-ness. It is FORBIDDEN, and it is the A03 C6/C7 leak by another name. LAW 1 now says so explicitly.

Added — **the CLAIM LIFECYCLE (which gate path writes what, and when).** Only path (3) ever produces a `working` file, and only transiently:
- **(1) QA SCAN** — writes NOTHING (already answered); returns the path. On a `working` file: **DO NOT RE-RUN** — return the path + "in progress since `<started>`". Cost ~0, an expensive run SAVED.
- **(2) DIGEST** — writes ONCE, COMPLETE, `state: answered`. The facts are already in `results/`; zero code runs, so the write is instant and there is nothing to claim.
- **(3) P-B-E-R** — writes the CLAIM at the moment it decides to run, then COMPLETES the same file at REPORT.

Added — **the TTL / zombie rule.** `QA_CLAIM_TTL_HOURS = 24`, stated as a **NAMED CONSTANT** so it can be tuned in one place (never hard-code `24`). Past the TTL a `working` file is STALE: the next `qa` call MAY **RECLAIM** it — rewrite the claim with a fresh `started:`, and record the abandoned attempt in `## Not-done`. The checker FAILs a `working` file older than the TTL. Without expiry, one crashed run makes every future reader defer to a dead one, forever.

Added — **the RACE GUARD, and its deliberate limit.** Two `qa` calls may reach the (3) decision at the same instant and both pick `QA/3-`. The claim file is created under **`set -C` (noclobber)**: the loser sees it already exists, re-runs (1) SCAN, and DEFERS. This shrinks the race window from THE WHOLE RUN to microseconds. The residual same-instant/**different-slug** collision is possible and **NON-FATAL** — (1) SCAN finds both files. **DO NOT over-engineer past this: no lock dirs, no lease servers, no ledgers** (a claim ledger here is `probes.ledger` reborn, and that is already on the do-not-resurrect list). The canonical bash idiom is pinned in PART 3a, verbatim, for the twins to copy.

Added — **R20, SUPERSESSION** (subsumes the staleness hole v8.0 left open). A later run whose answer CHANGES writes a NEW `QA/<n+1>-<slug>.md` and **APPENDS** `superseded-by: QA/<n+1>-<slug>.md` to the OLD file's state line — written by the EXECUTOR, the file's own owner, never by a consumer. **Reconciled with R15 ("ENRICH never mutates"):** R15 holds EXACTLY as written, *for the BODY*. `# Q —` / `## Answer` / `## Caveats` / `## Not-done` are FROZEN forever once written. Only the `state:` line is ever mutable, and only by the file's own owner — two edits are legal in a file's whole life (`working → answered`, then `answered → + superseded-by:`).

Added — **R21, THE THREE READERS.** (1) a 2nd `qa` call: `working` → do not re-run, defer. (2) a probe MATCH: `working` → the question is LIVE, so the consumer sets its own SECTION to `state: commissioned`, points `target:` at that QA file, and does **NOT** dispatch a second time (and does not touch the file). (3) a human: `ls QA/` + the state line now reads as BOTH *what this leaf has established* AND *what it is establishing right now*.

Changed — **PART 6, STATUS DERIVATION now reads the STATE LINE, not mere existence.** An `ls` is no longer enough; the reader must OPEN the file. Bank-side: no QA file → NOT ANSWERED · `working` → IN PROGRESS (since `<started>`; STALE + reclaimable past the TTL) · `answered` → ANSWERED · `superseded-by: X` → ANSWERED BUT STALE, the live answer is X. Section-side: `commissioned` now has TWO disk facts (leaf exists with no QA file yet, **OR** the target QA file exists and is `working`), and `answered` requires the target to be `state: answered` — a `working` target is NOT `answered`. The BUILD-lane fields (`owner:`/`eta:`/`blocks:`/`cross-project:`) bind at `commissioned` **both ways in**; no new exemption, and `check-probe-cards.sh` still has no lane test.

Added — **THE CHECKER'S TEETH, stated HERE as LAW** (PART 6; `check-probe-cards.sh` implements them). The entire point of the state line is that these become MACHINE-DETECTABLE. Five FAIL conditions, with their failure codes:
- `read-target-working` — a section at `state: read` whose `target:` resolves to a `working` QA file ⇒ **the paper claims it read an UNFINISHED answer.**
- `read-target-superseded` — a section at `state: read` whose `target:` carries `superseded-by:` ⇒ **the paper's reading is built on a STALE answer.** ⚠️ **THIS IS THE DAY-1/DAY-40 SILENT-FALSE-CLAIM BUG**: every file is internally consistent, the claim is FALSE, and before R20 nothing on disk was wrong so no checker could ever fire.
- `qa-working-no-started` — a `working` QA file with no `started:` ⇒ an UNEXPIRABLE claim.
- `qa-working-expired` — a `working` QA file older than `QA_CLAIM_TTL_HOURS` (`date -d "$started"`, a machine test) ⇒ a ZOMBIE claim.
- `qa-answered-empty` — `state: answered` with an EMPTY `## Answer` ⇒ a LYING RECEIPT.

Retired (PART 9) — **"write-once" as the QA invariant** (it was never the real rule; ONE WRITER was) · **lock dirs / lease servers / claim ledgers / any coordination service** (noclobber is the whole race guard).

Unchanged: everything else. Path binding (R1), the probe-unaware bank (R2), the two translations (R3/R4), the section anatomy (R5-R8), the three reasons a QA file may exist (R10), the `qa` verb (R11), the writer table (R12 — now noting that the ONE owner writes the file twice), the cost ladder (R13), match-on-the-answer (R14), the ENRICH depth ladder (R15), the two LAWS, the two session modes (R17) and the two explorers (R18).

Companions (must carry the IDENTICAL vocabulary — they drifted before): `task/haipipe-task/fn/qa.md` + the task Report stage · `discovery/haipipe-discovery/fn/qa.md` + the discovery Report stage · `haipipe-task-orchestrator-agent` / `haipipe-discovery-orchestrator-agent` · `haipipe-paper-probe` + `haipipe-application-probe` (the MATCH-on-`working` branch) · `check-probe-cards.sh` (the five new FAIL conditions) · `ARCHITECTURE.md`.

⚠️ NOTE ON THE VERSION: the ruling was handed to this pass as "bump to 8.1.0", but 8.1.0 was already on disk (the two-ambiguities pass, below). This change is strictly newer and lands as **8.2.0**.


## [8.1.0] — 2026-07-14 — two ambiguities the v8.0 rewrite inherited from the spec

Fixed
- **"Is the MATCH grep the thing the wall forbids?"** PART 4 ② tells the agent to `grep {tasks,discoveries}/**/QA/*.md`; PART 5's wall diagram then said "❌ paper session **greps**/edits the bank itself, stake in context → WALL NEVER EXISTED". A cautious agent could not tell whether the read-only grep it was just ordered to run was itself the violation, and both ways out are bad: skip MATCH (every section becomes a T3/T4 commission — the unbudgeted-spend smell) or treat the wall as advisory. **LAW 1 now names the ACT, not the tool:** it is broken by RUNNING bank work or WRITING a bank file (including a QA digest authored "helpfully"). A read-only grep of the QA corpus IS step ② and is called out as LEGAL and REQUIRED — "the wall bans the PEN and the RUN, not the EYE". Same repair in `ARCHITECTURE.md`. (The spec's own PART 5 carries the loose phrasing; the fix narrows the docs to LAW 1's actual text, which was always about executing/writing.)
- **"Does a fast commission need an eta?"** PART 2 scoped `owner:` / `eta:` / `blocks:` / `cross-project:` to a **BUILD-lane** section, but `check-probe-cards.sh:330-341` fires four hard failures on ANY `state: commissioned` section missing them and has no lane test (`grep 'build lane'` → 0 hits). An author who followed the SKILL literally wrote an ordinary commissioned section and was failed by the gate with no explanation. **Stated the rule the checker implements:** a section still `commissioned` WHEN THE GATE RUNS is BY DEFINITION build-lane — a dispatch that actually returned is `answered` or `read`. So the four fields are unconditional at that state. Mirrored in `ARCHITECTURE.md`'s BUILD LANE paragraph.

Unchanged: the model. Anatomy, path binding, the QA/ contract, the qa verb, the five-step loop, the cost ladder, status derivation and the writer table are all exactly as approved.


## [8.0.0] -- 2026-07-14 -- THE PROBE IS A PAPER-LEVEL Q/A MAP (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, APPROVED)
## 8.0.1 — 2026-07-14

- PART 4 ③ now states the DISPATCH PAYLOAD BLOCK VERBATIM, in the executor orchestrators' own input spelling (`action: qa` / `project:` / `question:` / `leaf:`). The constitution previously described the dispatch without pinning the keys, and the two consumer buckets each invented their own — the application worker sent `project_root`/`qa`/`target`/`deliverable`, which matches NONE of the orchestrators' four declared input forms. Both buckets now copy this block instead of inventing keys.

Spec of record: `Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/` v3, approved by JL 2026-07-14. All rulings R1-R18 adopted. This SKILL is rewritten as that spec's operative form — the layer's CONSTITUTION. Everything else in the toolkit cites it for vocabulary.

**The one-sentence change: a probe is a PAPER-LEVEL DOCUMENT, and the bank never learns it exists.**

The redefinition
- **A probe is `papers/<P>/1-probes/PPNN_<topic>.md` and nothing else** (`applications/<A>/1-probes/` identical). ONE FILE PER TOPIC. It is GENERATED in the PROBE phase from the Q-papers the DRAFT stage raised (JL-12). The v7 "bridge with two feet" is gone: the probe has ONE foot, on the paper.
- **Each Q-paper is ONE SECTION** (JL-8), carrying `serves:` / `target:` / `state:` / `commission:` / `reading:`, plus ONE `## Why` per file holding the STAKE, which never leaves the file. The words **"row" and "table" are BANNED** (JL-14) — it is a Q-paper, in its own SECTION.
- **R1 BINDING BY PATH, NOT BY ID.** `target:` is a PATH to the answering file. PP numbers are PAPER-LOCAL footnote numbers: two papers may both carry a PP04, the way two books both carry a footnote 4. The v1 collision bug (CGM2LabVital, 2 papers x PP01-PP06) DISSOLVES — no shared namespace, no ledger, nothing to renumber, nothing to grep. **No PP id ever crosses to the bank.**
- **R2 THE BANK IS PROBE-UNAWARE.** No `_ASK/`, no `_ANS/`, no `answers:`, no PP ids under `tasks/` or `discoveries/`. Probe-unaware is not question-DEAF: the executor answers plain questions through its own `qa` verb.
- **R7 "Verdict" IS DEAD** (JL-7) and `verdicted` as a state is DELETED. The section's `reading` carries the A-paper; the CLAIM's status (supported|refuted|inconclusive + confidence + claim_type + G1/G2/G3) lives in `1-claims.md` — per-claim, per-paper, PRIVATE. Two consumers judging the same evidence run two reviews: correct spend, not duplication. A DISCOVERY's own `verdict.md` (Review-type terminal file) is a DIFFERENT thing and SURVIVES.

The executor side (new — and it is THEIRS, not ours)
- **R9 the `QA/` folder** — optional, on EVERY executor leaf, task AND discovery (JL-10: both are executors, same shape). `QA/<n>-<slug>.md`, where **the numbering IS the index** (JL-9): `ls QA/` reads as a menu of what the leaf has established. Slug only — a PP id in a bank filename is R2 broken. Anatomy: `# Q —` / `## Answer` (+ `[-> results/...]` anchors) / `## Caveats` / `## Not-done`. Write-once; a later question ADDS `QA/<n+1>-...`, never edits.
- Precedent, not invention: `tasks/A03_welldoc_cycle_check/result.md` already grew organically as exactly this file — ungoverned, and contaminated with C6/C7.
- **R10 the three reasons a QA file may exist**: commissioned · digest-only · executor's own (incl. proactive answerability work). No fourth. Abuse guard: a QA/ mirroring every result file is noise, and the lint flags orphans.
- **R11 the `qa` VERB** — `/haipipe-task qa "<question>" [<leaf>]` and `/haipipe-discovery qa`, symmetrically. Gate: (1) QA SCAN (return the path, ~0) -> (2) DIGEST (write the QA file from EXISTING artifacts, no code runs) -> (3) P-B-E-R, or REFUSE. It takes ONE question in GENERAL language and never learns who asks or why. **It replaces the DELETED probe-aware `asks` verb — reborn probe-UNAWARE**, which is the whole point.
- **R15 the ENRICH DEPTH LADDER** (answering JL's "what does a new question mean to a task folder?"): depth 0 READ · 1 NEW RUN (config) · 2 NEW SCRIPT · 3 NEW LEAF. The EXECUTOR picks the SHALLOWEST depth that answers it; the scope test (2 vs 3) is "does it fit THIS leaf's plan.yaml IPO?". **The probe NEVER learns which depth was used** — it hands a question and gets back a path. ACCRETES (QA files, configs, runs, scripts, leaves); FROZEN (past results/, existing QA files, the commission).

The loop and its cost
- **The five-step loop**: DRAFT raises Q-papers -> (1) ORGANIZE -> (2) MATCH -> (3) DISPATCH -> (4) POINT -> (5) INTERPRET.
- **R13 the COST LADDER**: T0 JOIN (~0) · T1 LOCAL (~0) · T2 REUSE (1 grep + 1 read) · T3 ENRICH (agent) · T4 FRESH (agent). Only T3/T4 summon an agent.
- **R14 MATCH ON THE ANSWER, NEVER ON THE TOPIC.** The trap is live on disk: CGMtoAge/PP03 ("profile WellDoc cohorts" -> A04) and CyclePhase/PP03 ("scan WellDoc cycle columns" -> A03) look like the same topic, but A04 holds ZERO cycle evidence while A03's answer IS claim C6's entire base. READ the QA file, or it is a T3 ENRICH.
- **CC-7 / R17 — most probes should hit T2 REUSE.** A commission is the EXCEPTION, not the norm; a probe file whose every section is T3/T4 is a smell (a lazy MATCH, or a starving bank).

The wall — restated as a DISPATCH rule, because that is what it always was
- **LAW 1 — a consumer session NEVER executes task/discovery work inline.** Dispatch = hand the `commission` block, VERBATIM, nothing else. Never `## Why`, never the probe file, never the paper.
- **LAW 2 — backstop lint, two surfaces**: probe files' commission blocks carry no `C\d` / `H\d` / stake words; the bank's `QA/*.md` carry no consumer vocabulary.
- **CC-4, the evidence**: `tasks/A03_welldoc_cycle_check/result.md` contains "C6" / "C7" / "claims-stage" — written with NO probe file, NO stub, NO id involved anywhere. The stake traveled through a paper session's own CONTEXT when it did bank work inline. A FILE rule could never have caught that; LAW 2 would have. (v1's `_ASK` bridge pass provably could not: A03 had no `_ASK`.)
- **CC-8 — the PROBE CAUSES a QA file; the EXECUTOR AUTHORS it.** JL-17 asked whether the probe should write `QA/` in tasks, since human/orchestrator only produce `results/`. NO — and the reason is A03: a probe-authored bank file IS a consumer session with the stake in context writing a bank file. When a probe meets a bare `results/` with no digest, it DISPATCHES a digest-only run (qa path 2). The probe's action creates the file, through the executor's hand. That one hop is the entire wall.
- **T1 is never deleted** in favor of the lint: T1 is semantic, LAW 2 is a backstop, and a regex provably misses real leaks.

Two session modes, two explorers (JL-15 "very important", JL-16)
- **R17 TWO SESSION MODES.** LEFT/executor: just runs P-B-E-R, for its own sake — no questions, no asks. The bank grows AUTONOMOUSLY. It may also do **ANSWERABILITY WORK**: write QA digests, build/refactor code so future questions are cheap — without knowing which questions will come. RIGHT/consumer: asks. This is why the match-first loop works at all.
- **R18 TWO EXPLORERS**, both probe-unaware, both writing the same artifact through the same gate: a HUMAN via `/haipipe-task qa` (the everyday "go explore this direction" verb), and the ORCHESTRATOR agent (commissioned OR self-directed). QA/ = the leaf's growing map of explored directions. **The probe is one caller of a door it neither invented nor owns.**

Retirements (PART 9 — the do-not-resurrect list)
- **haipipe-probe-orchestrator-agent (the GATEWAY) RETIRED** (CC-6 / JL-13) -> `../agents/_archive/`, de-registered from `~/.claude/agents/` and `<repo>/.claude/agents/`. Its SWEEP became the paper-side MATCH; its dispatch is now a direct `Agent()` call on the EXISTING `haipipe-task-orchestrator-agent` / `haipipe-discovery-orchestrator-agent` — their clean context IS the wall, and the gateway was a third clean context standing in front of two that already had one. The `haipipe-probe-review` SKILL and `haipipe-probe-reviewer-agent` SURVIVE (paper-side claim judging).
- **DIRECT ASK no longer executes.** `/haipipe-probe "<question>"` now ROUTES to the executor's own door (`/haipipe-task qa` · `/haipipe-discovery qa`) and writes no probe file; the QA file is the receipt. [DECISION — the spec is silent here, but it retires the gateway that direct-ask depended on, and R18 makes `qa` the everyday human explore verb; routing is the only reading consistent with both.]
- Also dead: `_ASK/` + `_ANS/` mailboxes · the `answers:` field · the `asks` verb · probes.ledger + project-unique PP ids · `1-probe-plans/` (-> `1-probes/`) · "Takeaways" (-> `reading`) · "card" as the name of a probe file (-> probe; **allowlist rename only** — ~90 of 941 uses in this repo mean poster card-styles, venue-ui-card, KPI cards, _CITATION_ cards, "model card"; NEVER a blind sed).
- Carried forward unchanged: the retired `probes/` folder store, the INSIGHT layer, the Probe Console, `haipipe-probe-creator-agent`.

PRESERVED, not overturned
- **The BUILD-lane `commissioned` state** (7.10.0 below, JL resource-stage rulings C4 + C6 — landed concurrently with this rewrite) survives INTACT, re-expressed in section vocabulary: at `state: commissioned` a BUILD-lane section carries `owner:` · `eta: YYYY-MM-DD` · `blocks:` · `cross-project:`. It PASSES the gate (a 3-week build must not red every downstream gate for 3 weeks) and is a HARD FAIL the moment its eta passes with no QA file — without the date test it becomes a laundering token. `cross-project:` stays MANDATORY on every BUILD-lane section (the MATCH may NAME a sibling-project source but never CONSUME it; that line is how the candidate reaches the only human gate whose job is authorizing SPEND). Only the CARRIER changed (card + `_ASK/` stub -> question section + leaf), never the rule.
- The harvest lanes (`values:` / `sources:` / `displays:`) and the harvester model.
- `check-probe-cards.sh` **KEEPS ITS FILENAME** (65 refs across 33 files) — internals rewritten for question sections, commission lint, target resolution, and the bank-side QA lint.

Companions: probe agents (gateway archived, roster rewritten; reviewer untouched) · haipipe-paper-probe · haipipe-paper · task `fn/qa.md` (new) · discovery `fn/qa.md` (new) · the task/discovery Report stages (QA/ authoring) · the application/ family.


## [7.10.0] -- 2026-07-14 -- `commissioned`: the BUILD lane gets a status a producer can WRITE

The RESOURCE stage (haipipe-paper-resource 1.0.0) shipped a two-lane model — SCAN (minutes, gate-blocking) and BUILD (days-to-weeks, NON-BLOCKING ALWAYS) — and `check-probe-cards.sh` shipped the enforcement for it (owner + eta + blocks + cross-project, plus the C6 future-eta test). But `commissioned` was never added to the LAYER'S STATUS VOCABULARY, and no step in `haipipe-paper-probe` ever wrote it.

The defect that made the whole two-lane design dead on arrival:
- The vocabulary here (and in `haipipe-paper/fn/probe-plans.md`) listed only `planned | dispatched | read | verdicted | answered-local | failed`.
- TRANSLATE writes `dispatched` / `read` / `verdicted` / `answered-local` — never `commissioned`.
- So a REAL in-flight resource BUILD sat at `dispatched`, which the checker FAILs as `status-dispatched(probe-not-run)` — reddening the resource CHECK gate on EXACTLY the BUILD that JL ruled non-blocking. The C6 anti-laundering guard could never fire, because nothing could ever ENTER the state it guards. A status only the checker could READ and no producer could WRITE.

Added
- **`commissioned` in the status vocabulary** ("Statuses are derived from disk, never asserted"): a BUILD-lane ask in flight — the `_ASK/PPNN_*.md` stub exists on the execution bank AND the card carries `owner:` + `eta:` (still in the FUTURE) + `blocks:` + `cross-project:`, with no answering report yet. This is `dispatched` for work that legitimately takes DAYS TO WEEKS (`task-for-data` / `task-for-algo` / `task-for-fit`, or a long acquisition whose ETA is calendar months). It PASSES the gate; it goes FAIL the moment its eta passes with no receipt.
- **DERIVED, not asserted** — the layer's core law holds: the stub is on disk, the four fields are on the card, and `date -d "$eta"` is a machine test. It is the one status that survives an OPEN gate, so it carries the most enforcement. WITHOUT the date test, `commissioned` becomes the status every un-run probe wears and the mechanism ships as a laundering token (JL ruling C6).
- **Card anatomy gains `owner:` / `eta:` / `blocks:` / `cross-project:`** — REQUIRED at `status: commissioned`, absent otherwise. `cross-project:` is MANDATORY on every BUILD card (JL ruling C4): the gateway may NAME a sibling-project reuse candidate but may not CONSUME it, and this field is how that candidate reaches the only human gate whose job is authorizing SPEND. (Live case: a masked-LM CGM backbone about to be costed at GPU-weeks while its pipeline sat scaffolded one repo over.)

Companions: `haipipe-paper/fn/probe-plans.md` (status list mirrored) · `haipipe-paper-probe` 3.9.0 (TRANSLATE now LANDS a BUILD-lane card as `commissioned` instead of `dispatched`; SCAN-lane cards keep the `dispatched -> read` path) · `check-probe-cards.sh` (enforcement already present, unchanged by this pass).


## [7.9.0] -- 2026-07-12 -- INSIGHT LAYER RETIRED (JL ruling)

JL 2026-07-12: "we might want to retire insight." Fully retired.

The fact that decided it (verified on disk at retirement):
- ZERO K cards and ZERO W cards had ever been written, in any project.
- ZERO `insights/INDEX.md` files existed — the SWEEP's mandated index-first first stop had NEVER resolved.
- Five projects held an `insights/` dir: all empty, `.gitkeep`-only, or holding hand-written notes (not cards).
The DIKW ladder was a design promise, never a practice. Retiring it cost **zero reuse at runtime**; keeping it cost a third warehouse swept on every probe that never contained anything.

Changed
- **TWO warehouses, not three.** The evidence base is `discoveries/` (OUTSIDE evidence) + `tasks/` (INSIDE evidence). The gateway's SWEEP no longer reads `insights/` or `insights/INDEX.md`; D/I/K/W SHAPE-matching is replaced by WAREHOUSE-matching (an outside question ends in discoveries/, an inside question in tasks/).
- **A probe deposits NOTHING.** The PPNN card's `## Takeaways` / `## Verdict` IS the settled record.
- **Card anatomy gains `confidence:` and `claim_type:`** in the Verdict block — the K card's two load-bearing fields, which had no home outside the retired layer.
- **`insights/` removed from the project container** (`/haipipe-project` 3.1.0 no longer mints it).
- Skills + agents archived to `skills/insight/_archive/` and DE-REGISTERED (7 skill symlinks + 9 agent symlinks removed from ~/.claude/). `skills/insight/` is now a tombstone: README + CHANGELOG + _archive/.

Added (the two patches that keep the retirement from being a regression)
- **SWEEP item 1b — CROSS-CONSUMER QUERY-ONCE (read-only).** The gateway now greps already-LANDED PPNN cards (`papers/*/1-probe-plans/`, `applications/*/1-probe-plans/`, status read|verdicted|answered-local) so a verdict ONE paper settled is visible to the NEXT. This is the one thing K cards were supposed to provide and never did. HARD LIMITS: never writes another consumer's card; never re-dispatches an answered question; and NEVER carries a card's `## Why` into a stub or plan — the PAPER-AGNOSTIC rule binds here as everywhere.
- **`claim_type: associational | causal`** ported into the probe-review return contract (1.1.0) — the correlation→causation guard whose ONLY home was `insight/ref/dikw-boundaries.md`. It is a separate axis from `confidence` (sample→population); `causal` requires a named identification strategy (RCT / valid IV / RDD / DiD with checked parallel trends), and is NEVER upgraded just because confidence is high.

Dropped, deliberately
- The D→I→K→W provenance graph + `index-integrity-auditor` (it never had an edge — zero cards).
- The OKF interchange export (`export_okf.py`) — zero consumers anywhere in the toolkit.
- The standalone, cited, reusable W-card form. W's real flavors survive: "next experiment" IS the claims-ledger GAP → PPNN card → `_ASK/` stub chain (executable, not advisory), and "what a stakeholder should do" IS `applications/`.

Legacy `insights/` folders on disk: DEAD HISTORY — never read, never written, **never deleted** (same treatment as the retired `probes/` folders).

Companions: gateway agent 2.4.0 · haipipe-probe-review 1.1.0 · probe-reviewer-agent 3.0.1 · haipipe-project 3.1.0 · ARCHITECTURE.md + STRUCTURE.md + README.md.


## [7.8.1] -- 2026-07-12 -- Audit repair (multi-agent skill audit, 59 confirmed findings)

Fixed (all found by the 2026-07-12 adversarially-verified skill audit; the first was introduced by 7.8.0 itself):
- **Discovery paths were ONE level too shallow** — 7.8.0 corrected the task stub depth but left every discovery path at the GROUP level (`discoveries/{S|L|P}{NN}_{topic}/`). Discovery folders are TWO-level (`discoveries/{S|L|P}{NN}_{group}/{NN}_{topic}/`, per discovery/haipipe-discovery/SKILL.md); a stub dropped in a real GROUP container has no `discovery.yaml`, so no Plan stage would read it and the card would sit `dispatched` forever. (Honesty about the one live case: `ProjC-Model-PersonalizedModel/discoveries/L01_personalization-landscape/` is a LEGACY one-level folder — group and leaf at once, holding discovery.yaml AND _ASK/ — so its stubs were read and answered. The spec was still wrong, and the next fresh discovery handoff written to a true group container would have died silently.) Fixed in the stub-path block, the target vocabulary, and the gateway's folder-creation law. The "never create a group silently" guard is now explicitly TASK-ONLY (discovery S/L/P letters are fixed purpose hints; the discovery layer creates its own groups by design).
- **`answers:` had no schema** — writers said scalar (`answers: PPNN`), the creator agent said "one entry per stub" (a list), and readers grepped the literal scalar string, so a two-stub report would never be harvested. PINNED here (this doc owns the bridge): ALWAYS a flow list of bare PP ids (`answers: [PP04, PP07]`), and every consumer greps shape-agnostically (`answers:.*\bPP04\b`), which still matches legacy scalars.
- **DIRECT ASK vs HANDOFF-FIRST** — the gateway's stub rule was unconditional, but a direct ask has no card to mirror and no `from:` to point at. Direct asks now explicitly write NO stub (inventing a PP number would leave a dangling bridge foot in `grep -r PPNN` and `/haipipe-task asks`); the gateway dispatches them in-session instead.
- **Card status enum omitted `failed`** — the header template listed 5 statuses while the same file defined `failed` twice as real and disk-derivable.
- Task-folder target examples now obey the task layer's `{NN}_` law.
- The bridge pass's consumer-vocab check was rebuilt CONTEXT-AWARE after a first attempt false-positived on legitimate work: a bare `H2`/`C3` is not a leak in this domain (forecast horizons H1-H9, cohort arms, and real task paths like `tasks/.../C3-Visual-ForecastScaling/` — which cannot be reworded). It now flags an H/C id only where it is USED as a claim id: a `serves:` line in a stub (the exact field that licensed the 2026-07-11 leak), or an H/C id on a line that also carries claim vocabulary (claim/hypothes/support/refut). Path-looking tokens are stripped before matching. Verified against both a clean stub (paths + H1/H6 horizons + arm C2 → PASS) and a leaked one (`serves: C1,C2,C3` + "rescue H2" → FAIL).

KNOWN GAP (not fixed, stated honestly): nothing MECHANICALLY enforces the two-level leaf rule — the checker's stub glob deliberately accepts depth-1 so it keeps scanning legacy one-level discovery folders. It therefore cannot distinguish a legacy leaf (fine) from a stub dropped in a true group container (dead on arrival). The rule is spec-enforced only.

Companions: gateway agent 2.3.1, discovery agents (orchestrator 1.7.0 / creator 1.6.0 — they were entirely blind to the bridge), haipipe-paper-probe 3.8.1 (+ Agent tool, which its allowed-tools had omitted despite Agent dispatch being its only permitted door), haipipe-task 5.10.1.


## [7.8.0] -- 2026-07-12 -- Routing: the card names WHERE the ask is sent

JL ruling 2026-07-12: "this should also be in the PP plan — which task folder or discovery folder to send the ask." Routing was previously implicit (the gateway picked a folder ad-hoc at dispatch, and the paper never recorded where its answer would come from).

Added
- **`target:` card field** — the receiving folder. Vocabulary: an existing `tasks/<group>/<folder>` or `discoveries/<folder>` path · `NEW tasks/<existing-group>/<slug>` · `NEW discoveries/L##_<topic>` · `?` (undecided). The paper PROPOSES (campaign pass authors it; `?` is honest at DRAFT, when the paper does not yet know what the project holds), the gateway's SWEEP DISPOSES (may re-route toward reuse), and the actual landing site returns in `handoff:` for TRANSLATE to write back.
- **Campaign rule "EVERY CARD GETS A TARGET"** — routing is resolved at the consolidation pass, the only moment the whole campaign is visible: two cards aimed at one task-folder hint they should merge; a card with no plausible home hints the need is under-specified. A card left `?` there must say why.
- **"Routing the ask" section** — target vocabulary + the folder-creation rules for the gateway.

Fixed
- **Stub path was one level too shallow.** The spec said `tasks/<G><NN>_<slug>/_ASK/...` — that is the task-GROUP level. Task folders are TWO-level (`tasks/{G}{NN}_{group}/{NN}_{task}/`, per task/haipipe-task/ref/hierarchy.md), and the ask belongs to the task-FOLDER (the unit of work). The live 2026-07-11 ScalingLaw stub was already at the correct depth; only the spec was wrong.

Boundary (answering "should probe scaffold a task folder?")
- The gateway creates the receiving folder + `_ASK/` + the stub and **NOTHING ELSE** — no `.py`, no `configs/`, no `runs/`, no `workflow/`. Code scaffolding requires task-TYPE knowledge (which specialist, which template); that is the task layer's BUILD stage. A folder holding only `_ASK/` is a complete, valid handoff (the zeroth state). Naming follows the execution layer's own law by reference, never an invented scheme; a new task-GROUP is never created silently (group letters encode a project's scheme — a human names it).

Companions: gateway agent 2.3.0, haipipe-paper-probe 3.8.0 (BOOKKEEP requires target), haipipe-paper 2.10.0 (campaign pass authors routes), haipipe-task 5.10.0 (`asks run` — screen an unfinished ask and answer it through the lifecycle).


## [7.7.0] -- 2026-07-12 -- Both-banks layout: cards pool in 1-probe-plans/, stubs pool in _ASK/

JL ruling 2026-07-12 (two decisions, same session): (a) consumer bank — under the per-stage `_PROBE/` layout a merged cross-stage card had to pick an ARBITRARY home stage, and PPNN numbering was already paper-global; ALL cards now live FLAT in `1-probe-plans/PPNN_<slug>.md`, beside the campaign README that orders them — the whole campaign is one `ls`. (b) execution bank — stubs move from flat `_ASK_PPNN.md` at the task/discovery root into an `_ASK/` container: `_ASK/PPNN_<slug>.md`, keeping the root clean when several consumers ask ("加一个 ask folder，把它们放到一块儿").

SUPERSEDES the JL 2026-06-29 stage-self-containment ruling FOR PROBE CARDS ONLY (that ruling had moved cards from flat `1-probe-plans/` into per-stage `_PROBE/`; the 07-11 campaign ruling then made cards cross-stage in logic — one card, many `serves:` — so the physical layout now follows the logic back). Stage-owned working docs (`_CITATION_`, `_VALUES_`, `_EVIDENCE_`, `_DISPLAY_`) are NOT affected: they stay with their stage.

Changed
- **Card anatomy** — cards live at `1-probe-plans/PPNN_<slug>.md` (flat, cross-stage pool). Header field `stage:` → `serves:` (comma-separated stages and/or claim ids — the affinity field a stage gate greps in place of "ls my folder").
- **Stub anatomy** — path `<receiving folder>/_ASK/PPNN_<slug>.md`; heading `# PPNN — <need title>` (was `# _ASK_PPNN — ...`). The stub filename MIRRORS the card filename: same PPNN, same slug on both banks; folder name tells the role, filename tells the question, one `grep -r PPNN` finds both feet. Zeroth state re-phrased: a task/discovery whose only content is `_ASK/`.
- **Status derivation globs** — cards `papers/*/1-probe-plans/PP*.md`; stubs `tasks/**/_ASK/PP*.md` + `discoveries/**/_ASK/PP*.md`.
- **Legacy** — per-stage `_PROBE/` cards and flat `_ASK_*.md` stubs are read-only history, migrated on first touch (the fn/probe-plans.md migration direction is REVERSED).

Companions: gateway agent 2.2.0 (new stub path + inline PAPER-AGNOSTIC rule), haipipe-task 5.8.0, haipipe-discovery 2.8.0, haipipe-paper-probe 3.7.0 + checker globs, haipipe-paper 2.9.0 + fn/probe-plans.md rewrite, haipipe-paper-folder scaffold note. NOT mirrored (parked by JL): application/ family — now 3 rulings behind (7.4/7.5, 7.6, 7.7).


## [7.6.0] -- 2026-07-12 -- PAPER-AGNOSTIC bridge: consumer vocabulary does not cross

JL ruling 2026-07-12: "when probe leaves the ask to the discovery folder, you should not mention H1, H2 — they are from the paper or application. Discovery and task should not be aware of it; they just do the task and the discovery as they are."

Root cause (live failure, 2026-07-11 seed incident, `Paper-PersonalizedGlucoseModel`): the spec ITSELF licensed the leak. The stub anatomy prescribed `serves: <claim ids>` and `## Need (from the card, verbatim where possible)`, and the paper worker's STEP 2 said to paste `<the PP card's Need + Why + Route, verbatim>` into the dispatch plan. The card's `Why` is, by construction, the paper's stake. Two probes dispatched that way produced a discovery whose own `verdict.md`, `sources.md`, `landscape.md` and `discovery.yaml` were STRUCTURED around one paper's H1/H2 (27 and 25 mentions in verdict.md alone; `report.h2.pp02` as a YAML key).

Two distinct harms, and the second is the serious one:
- CONTAMINATION — a discovery exists to be swept and REUSED by future papers. One organized around this paper's H1/H2 is paper-shaped and effectively single-use. Contaminating the ledger costs more than the probe did.
- BIAS — a stub saying "this is the one probe that could rescue H2" tells the executor which answer is wanted. (The PP02 stub literally read "The consumer WANTS a positive." It was compensated with an adversarial "default to NEGATIVE" brief and did return a negative — but a patch for a leaked stake is not a substitute for not leaking it.)

Changed
- **PPNN card anatomy** — `## Need` / `## Why` / `## Route` now carry an explicit bridge boundary: Need + Route are PAPER-AGNOSTIC and CROSS; `Why` is PAPER VOCABULARY (H1/H2, the stake) and STAYS. The card is named as the ONE bilingual document — the only artifact allowed to hold both vocabularies, mapping Q1/Q2 (evidence) ↔ H1/H2 (paper) on return.
- **Handoff stub anatomy** — `serves: <claim ids>` REMOVED from the header (it was the licensed leak). `## Need` now reads "the evidence question(s), SELF-CONTAINED — name them Q1/Q2/..., never the consumer's claim ids". `from:` survives as a human-facing provenance pointer the executor never acts on; `PPNN` is an opaque correlation token.
- **NEW rule: PAPER-AGNOSTIC**, stated ahead of VERDICT-BLIND. The stub must be executable by a stranger with no access to the paper.
- **VERDICT-BLIND strengthened** — naming what the consumer would DO with each outcome is itself a stake disclosure, not just naming the hoped-for answer.

Enforcement (in the paper worker's `check-probe-cards.sh`, v3.6.0): a new BRIDGE PASS greps every `_ASK_*.md` on the execution bank for consumer vocabulary (`H[1-9]`, "the seed", "the pitch", "the narrative") and for stake disclosure ("rescue", "we want", "hoped-for", ...) and FAILs. The `- from:` line is exempt; "the paper" is deliberately NOT a pattern (a discovery legitimately says "the paper reports X" about a SOURCE paper). Verified against the real 2026-07-11 stub: FAIL consumer-vocab(13-lines); stake-disclosed(1-lines).


## [7.5.0] -- 2026-07-11 -- Campaign planning: probes consolidate cross-stage

JL ruling 2026-07-11 (same session as 7.4.0): stage drafts should be done cross-stage together, then the probes thought about HOLISTICALLY, consolidated, handed off, and each answer queried exactly once.

Added
- NEW section "Campaign planning — probes are consolidated cross-stage, not stage-by-stage": the 5-step global pass (DRAFT SWEEP → PROBE-PLAN → HANDOFF → RUN → HARVEST) and four campaign rules — ONE CARD PER QUESTION (many serves:, duplicates retired at consolidation), DISPATCH DAG not a flat list (gating cards first, refutation-capable early, dependents wait on answers), QUERY-ONCE (landed answers are consumed from cards/registries via answered-local, never re-dispatched; re-querying is a campaign defect), and the two-part README.
- The v7.4 index demotion refined: `1-probe-plans/README.md` = `Campaign` section (AUTHORED — merge rationale + DAG; genuine planning content not derivable from cards) + `Status board` section (GENERATED). Status queries updated to match. Motivating instance: Paper-ScalingGlucose-NatSeries2026's consolidated campaign (16 cards → 5 claims, PP04 gates all).
- Siblings in the same pass: haipipe-paper 2.8.0 (`probe plan` verb), haipipe-paper-lifecycle 2.3.0 (Global-pass mode), haipipe-paper-probe 3.5.0 (worker obeys the Campaign DAG).

## [7.4.0] -- 2026-07-11 -- The two-footed bridge: _ASK_PPNN.md handoff stubs

JL ruling 2026-07-11 (GlucoScaling design session): "probes are the bridges" — a probe must leave its handoff ON DISK in the receiving task/discovery folder so /haipipe-task and /haipipe-discovery know what to do and what not to do, and so two concurrent sessions (one on tasks, one on the paper) communicate through files, not through a live agent.

Added
- NEW section "The handoff stub (`_ASK_PPNN.md`) — the bridge's second foot": written at DISPATCH into the receiving `tasks/<G><NN>_<slug>/` or `discoveries/<GROUP>/<NN>_<topic>/` folder; anatomy = from/serves/mode header + Need / Deliverable / Do-not / Pre-accepted. Three rules: VERDICT-BLIND (pre-registration — the answer SPACE, never the hoped-for side; PP05-class refutation probes must not be poisoned from the paper bank), WRITE-ONCE consumer-side (execution reads, never edits; the answer lands in report.yaml `answers: PPNN` / the discovery report block), LOCK-FREE two-session workflow (paper session writes cards+stubs, execution session writes reports; no shared writes).
- Zeroth-state rule: a fresh need with no folder yet = create folder + stub and NOTHING else — a stub IS a task/discovery in its zeroth state; the receiving Plan stage reads it into plan.yaml / discovery.yaml. No _INBOX/, no new registry.
- NEW section "Statuses are derived from disk, never asserted": planned / dispatched / read / verdicted / answered-local / failed each get a disk-checkable definition — `dispatched` = stub exists with no answering report (previously an unverifiable assertion about a launched agent, the exact class of lie the refs-required invariant kills; the stub is that invariant's missing twin).
- Values-mirror-citations note on the value lane: `task → results/ → canonical value table → _VALUES_ slot map → prose` mirrors `discovery → sources.md → .bib → _CITATION_ slot map → prose`; with a gating values probe, every value_refs resolves against the ONE canonical table artifact, never scattered result files.

Changed
- Flow diagram: enrich|fresh dispatch shows HANDOFF (write stub FIRST, then execute — or STOP after the stub for deferred pickup by another session; the card is still honestly `dispatched`).
- Layer-boundaries block: probe "owns no files" → "owns no FOLDER; its only files are the consumer's PPNN card and the _ASK handoff stub, the bridge's two feet".
- Status queries: scans now include `tasks/**/_ASK_*.md` + `discoveries/**/_ASK_*.md` + answering reports; `1-probe-plans/README.md` demoted to a GENERATED dashboard (regenerate when stale, never hand-maintain, cards win).
- Siblings updated in the same pass: gateway agent 2.1.0 (writes the stub), haipipe-paper-probe 3.4.0 (deferred handoff + async harvest), haipipe-task 5.7.0 + haipipe-discovery 2.7.0 (consume the stub, answer in report), haipipe-paper 2.7.1 (index demotion).

## [7.3.0-note] -- 2026-07-10

Fixed (fresh-agent audit, M15)
- Frontmatter summary now mentions v7.3 answered-local.

## [7.3.0] -- 2026-07-10

Changed (paper-side paper-local sweep, JL 2026-07-10)
- PPNN card status vocabulary gains `answered-local`: the need was closed from the paper's own registries at the paper-side LOCAL SWEEP (no gateway dispatch); refs may be paper-root-relative. See haipipe-paper-probe 3.2.0 STEP 2.

## [7.2.0] — 2026-07-07

Added (paper 2-phase skillset-diagnose, Part-0 harvester ruling — JL: "they are the harveste agents... just one step within the whole probe")
- PPNN card anatomy: three optional LANE LINES (`pick_list:` / `value_refs:` / `unit_refs:`, each `· harvest: OWED | accepted (...)`) written by the paper worker's TRANSLATE when a return carries harvestable content. The debt exists on disk before the harvest runs; check-probe-cards.sh FAILs an OWED line at VERIFY/the CHECK gate. Flow diagram updated: TRANSLATE dispatches the citation/values/display HARVESTERS (transcription-only, pointer-following) and mechanically accepts.

## [7.0.0] — 2026-07-06

Changed (JL: "probe is just exploring, can be general; it will be used by paper/application for explore and gather the evidence")
- Identity recast: probe = general-purpose EXPLORE+GATHER verb, not "claim-level evidence contract". Any evidence question (dataset profile, field norms, run result, claim verdict) enters here; judgment is an optional add-on (full mode only, via haipipe-probe-review). The opening definition, description, layer-boundary block, and all "claim-level" language rewritten.

## [6.2.0] — 2026-07-06

Changed (JL: reviewer flow must be governed by a SKILL — "haipipe-probe就只保留 reviewer之外的内容")
- Judgment process split out to the sibling skill `../haipipe-probe-review/` (G1/G2/G3 gates, thresholds, verdict vocabulary); this skill keeps everything else — layer contract, PPNN card anatomy (incl. where the verdict LANDS), DIRECT ASK.
- `g2_integrity_check.py` + `probe-caveats-checklist.txt` moved `../agents/` → `../haipipe-probe-review/` (the judgment skill owns its instruments).

## [6.1.1] — 2026-07-05

Changed
- Legacy probes/ folders INVISIBLE to SWEEP; Agent added to allowed-tools; archive-pass ref repoints. (Rollup of 6.1.x fixes; details in git history.)

## [6.1.0] — 2026-07-05

Added (JL: "We might still need a haipipe-probe, but we don't need a standalone probes folder")
- DIRECT ASK front door restored: `/haipipe-probe "<question|claim>" [light|full]` runs ad-hoc evidence work outside any stage — gateway dispatch (bg), evidence lands in discoveries/tasks, anchored takeaways return in chat (user = consumer, reply = receipt). No folder, no card, no console state. Later paper use = PPNN card with refs to the already-landed artifacts (pure REUSE).

## [6.0.0] — 2026-07-05

Changed (FOLDERLESS REFACTOR — see ../CHANGELOG.md 5.0.0 for the layer rollup)
- SKILL.md rewritten thin: layer contract + PPNN card anatomy; Probe Console, probes/ folders, probe.yaml/evidence.md/verdict.md retired; fn/ + ref/ marked LEGACY.

## [5.2.0] — 2026-07-05

- SKILL.md slimmed 481 → 286 lines (JL: "这个怎么这么长，是不是有很多重复的地方"): feedback/digest rules were stated 4 times (Commands, Skill Procedures, Routing 1b/1c, Feedback section) and are now one-liners pointing at fn/feedback.md + fn/digest.md, the single source of truth; Gather detail (Call/Link/Extract/DONE, fan-out, naming) deferred to fn/gather.md; Boundaries merged into the header; full/light chains stated once; Copilot policy and stage-strip prose compressed. No rule was deleted, only duplicates; every cut has its canonical body in fn/ or ref/.
- Formatting: one sentence per line, no manual line wrapping (JL: "一句话一行 不要break lines").

## [5.1.0] — 2026-07-05

- Legacy verbs removed entirely (owner decision, JL: "我们就用一个gather得了，把legacy去掉好了。"): the legacy-alias table is deleted from SKILL.md and ref/lifecycle-map.md; design/bridge/dispatch/harvest/post/resume/review/file/return no longer route; scattered-work filing goes through `gather` (link path applies ref/probe-attach.md); probe-attach front door and the dashboard nag line reworded from `/haipipe-probe file` to gather. Old probe.yaml DATA stays compatible (status: returned etc. still accepted by the stage strip).
- Skill-set review round (SKILLSET_REVIEW.md): fn/judge.md rewritten off the 3 retired reviewer agents onto haipipe-probe-reviewer-agent G1/G2/G3 with deterministic fn/g2_integrity_check.py for G2 and the caveats-checklist pointer (A1); allowed-tools Task → Agent in SKILL.md, fn/judge.md, fn/gather.md (A8); letter convention P.<LETTER><MMDD> added to fn/plan.md (id: field + write paths), fn/gather.md, ref/probe-attach.md scaffold, SKILL.md layout (A7); lifecycle-map Judge external calls updated off Codex (A4); dashboard shallow-check `return` → `deposit` and schema "called by Return" → Deposit (A6); fn/deposit.md target path corrected to source.deposit_target (C3); false "auto-invoked by haipipe-data/haipipe-discovery" claims removed from ref/probe-attach.md, lower layers are probe-UNAWARE by design (D1); argument-hint extended with utility verbs (B2).

## [5.0.1] — 2026-07-03

- paper phase renamed GATHER->PROBE; paper-side worker names updated (haipipe-paper-probe-{citation,values,display}).

## [5.0.0] — 2026-07-02

- added mode: full|light. Light probes stop at Read (no Judge, no Deposit, no insight cards). Escalation from light to full supported. Section-edit gather workers (citation, values, display) route evidence needs through light probes. Added Connection to Section-Edit section. Unwrapped hard-wrapped lines.

## [4.3.0] — 2026-06-23

- feedback-driven revision pass (14 items). (1) Plan: kind: field (atomic|comparison); comparison arms must be atom: links. (2) Gather: link+extract lightweight variant; fan-out model (1 probe : N discoveries : N tasks); naming rule (topic not verb); done-predicate strengthened (actual items, not evidence_plan); participant roster at Gather->Read boundary. (3) Read: elevated to stop-and-internalize gate (most participatory step); verdict-language ban in evidence.md. (4) Deposit: output readability template. (5) stage-strip.sh: fixed Gather false-positive (evidence_plan was Plan artifact, not Gather). (6) Dashboard: no-args view trimmed to compact glance. (7) Orchestrator agent: Write/Edit removed from tools (structural anti-monolith enforcement); dispatch prompts use coordinator language. (8) probe-yaml-schema: kind field, deposited status, deposit block heading.

## [4.2.0] — 2026-06-22

- completed the Return->Deposit rename (artifact deposit.md, fn/deposit.md, probe.yaml deposit:/status: deposited/deposited_at/deposit_target; stage-strip predicate + accepts deposited|returned|closed). LEAN-ATOM MODE: a leaf probe declaring parent: logs Read/Judge/Deposit as yaml blocks (result:/verdict:/deposit:) and the strip reads them (yaml is disk). Deposit step now ALWAYS proposes the /haipipe-insight review handoff in next: (loop no longer implicit).

## [4.1.0] — 2026-06-22

- source-type letter in the probe ref. P.D<MMDD> discovery-sourced, P.T<MMDD> task-sourced (other source.type derives the letter from the primary evidence_plan kind). Folder becomes probes/<LETTER><MMDD>_<slug>/. Resolver accepts lettered + legacy letterless refs; existing letterless probes migrate lazily. See ref/probe-yaml-schema.md.

## [4.0.1] — 2026-06-22

- rename lifecycle step Return -> Deposit (settle the judged verdict into durable memory); legacy command alias return kept; Read reframed as a present-and-internalize stop; Gather-done = participating tasks/discoveries have run, closed by a participant manifest.

## [4.0.0] — 2026-06-22

- reframe probe around Probe Console and the concise lifecycle Plan/Gather/Read/Judge/Deposit; flat probe folders; group folders removed.

## [3.3.0] — 2026-06-21

- delivery-need inputs from paper/application and verdict backfill.

## [3.1.0] — 2026-06-19

- sandwich lifecycle around discoveries/tasks.
