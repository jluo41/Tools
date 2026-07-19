haipipe-paper-resource — Changelog
==================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## 2.3.0 — 2026-07-18 — description-first: Demand → Resource Description

JL reframe (2026-07-18): resource is a DESCRIPTION of the resources we HAVE, not a list of what we NEED. The `Demand` section (one `N<n>` need per hypothesis) is REPLACED by `Resource Description` — one `## Resource <n> · <name>` subsection per resource, `### <topic>` sub-subsections for its aspects, closed by a `### Serves & carries` topic naming the `H<n>` it serves and whether it carries them.

Changed (`ref/resource-template.md`)
- `Demand` (need-first, `**N<n> (H<n>)**`) → `Resource Description` (asset-first, `## Resource <n> · <name>` + `### topics` + `### Serves & carries`). Named `Resource <n>`, not `R<n>` (spelled out; avoids collision with H/N/C/Q ids).
- The feasibility gate is PRESERVED, relocated: "exists but cannot carry the claim / what it KILLS" now lives in `### Serves & carries` + the Q-consumer Answer; per-hypothesis coverage reads off each resource's `Serves & carries`.
- Q-consumer unchanged (uniform `## Q-Resource-<n>` Description/Reason/Answer); questions now cite into the `Serves & carries` line, e.g. `[Q-Resource-1]`.
- The CGM `REFERENCE` worked-example block was CUT (a real filled example teaches the discipline better; the template stays a lean skeleton).

SKILL.md
- description, summary, DRAFT step, artifact section list, and the "cannot carry" line: `Demand` / `N<n>` → `Resource Description` / `## Resource <n>` / `Serves & carries`. Exits reworded ("every hypothesis has a fit resource, or a cut").

Note: supersedes the `Demand` half of 2.2.0; 2.2.0's uniform-Q-consumer + KILLS-in-RULE still stand.


## 2.2.0 — 2026-07-18 — uniform Q-consumer (cross-stage charter)

Adopted the stage-template charter (`../../TEMPLATES.md`, JL 2026-07-18). Resource's `Questions` section → `Q-consumer` with the UNIFORM shape shared by every stage — `## Q-Resource-<n> · <title>` + `Description` / `Reason` / `Answer` — because the PROBE stage collects every stage's Q-consumer through one pipeline, so the shape is the interface.

Changed (`ref/resource-template.md`)
- `Questions` → `Q-consumer`; each `**Q<n> (N<n>)**` → `## Q-Resource-<n> · <title>` with Description / Reason / Answer.
- STAGE-PREFIXED ids `Q-Resource-<n>`; each question cited inline in the `N<n>` demand line it tests, e.g. `[Q-Resource-1]` (forward link); `Reason` names the `N<n>` served (back link).
- Fill rules moved INTO the template as `<!-- RULE -->` comments (follow then delete); top TEMPLATE marker added.
- Resource DISCIPLINE preserved as RULE guidance, NOT as different fields: the `Answer` states existence AND fitness AND what it KILLS (a woolly Answer is a defect); a BUILD question's Answer keeps COMMISSIONED / owner / eta / blocks / cross-project; the `-> PP<NN>` binding stays the probe worker's, surfacing as the Answer's `[source: PP<NN>]`.
- Worked REFERENCE example converted to the uniform shape (kept the KILLS lesson — "Read Q-Resource-1's Answer again").

SKILL.md
- description, summary, the DRAFT step, and the artifact section list: `Questions` → `Q-consumer`; DRAFT now cites `[Q-Resource-<n>]` inline; the artifact note points to the template's `<!-- RULE -->` comments + the `../../TEMPLATES.md` charter.


## 2.1.0 — 2026-07-14

- The gateway is REMOVED from the ownership chain everywhere: DRAFT asks (Q) -> GATE 1 -> the PROBE WORKER opens the SECTION + writes the `-> PP<NN>` backlink -> MATCH resolves it or DISPATCH commissions it to `Agent(haipipe-task-orchestrator-agent)` / `Agent(haipipe-discovery-orchestrator-agent)` -> the QA file lands -> INTERPRET writes the `A:`.
- "card" -> "SECTION" throughout (BUILD-lane fields, the spend-gate rule, the CHECK FAIL lines, the done-criteria). `status: commissioned` -> `state: commissioned`.
- "the gateway's SWEEP names cross-project:" -> "② MATCH names it" (the fact GATE 1b depends on, so the gate's justification still holds).
- ref/resource-template.md: the `-> PP<NN>` backlink is written when the PROBE WORKER opens the section, not when a gateway mints a card.

## [2.1.1] — 2026-07-14 — the required-reads were off by one `../`

Fixed
- **The first instruction in this skill pointed at nothing.** `Read first: ../../PHILOSOPHY.md, ../../<shared-refs>/04-lifecycle-map.md` — but this skill lives at `skills/paper/1-lifecycle/<N>-<stage>/<skill>/`, so `../../` is `1-lifecycle/`, which holds neither `PHILOSOPHY.md` nor the shared-reference folder. Both live one level further up, at `skills/paper/`. Every in-body citation (stage-gate, comment-lifecycle, stage-illuminate, delivery-need, `../../_venue/playbook-<venue>`) failed the same way, silently — an agent loading the philosophy and the stage-gate rules got file-not-found and proceeded without them. All repointed to `../../../`; every target verified to resolve on disk.

## [1.2.0] — 2026-07-14
## 2.0.0 — 2026-07-14

- PROBE REDESIGN (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14 — R1-R18). 1-probe-plans/ -> 1-probes/ (PPNN_<topic>.md, one file per TOPIC, one SECTION per question: serves/target/state/commission/reading + ONE `## Why` per file holding the stake). Binding is by PATH: a section's `target:` points at the answering `<leaf>/QA/<n>-<slug>.md` in the bank. DELETED: `## Verdict`, the `verdicted` and `dispatched` states, `_ASK/`/`_ANS/` stubs, `answers:`, and Agent(haipipe-probe-orchestrator-agent) (the GATEWAY — archived + de-registered). A claim's STATUS now lives ONLY in 0-lifecycle/1b-claims/1b-claims.md. Dispatch is now DIRECT: the section's `commission:` block, VERBATIM, to Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent).
- The Q -> PP handoff now OPENS a question SECTION under 1-probes/ (state: planned, commission: the Q re-posed as a self-contained evidence question) instead of MINTING a card in 1-probe-plans/. The `-> PP<NN>` backlink into 1a-resource.md — the mechanical proof the question was ASKED — is unchanged, and the checker's paper-only RESOURCE PASS still tests it.

Fixed (adversarial review, BLOCKER 1 — THE ROOT ONE: **the Q -> PP mint had no owner**)

The stage shipped able to ASK and unable to be ANSWERED. Three parties, and none of them minted the card:

- this stage writes `Q<n>` and is FORBIDDEN to mint a PP id (JL's Q-not-PP ruling — correct, and unchanged);
- the PROBE worker's STEP 1 (BOOKKEEP) resolved cards from `1-probe-plans/README.md` planned items to EXISTING PPNN cards, and never read `1a-resource.md` — the word "resource" did not appear in that file at all;
- the gateway takes `correlation_id: PPNN` as an **INPUT**, so a PP id cannot be its OUTPUT.

So the PROBE phase dispatched an EMPTY BUFFER and the CHECK gate greened over it, vacuously. Empirically confirmed before the fix: `check-probe-cards.sh <Paper-CGMtoAge> --stage resource` printed `OK no cards serve stage 'resource'` and exited **0**. Same class of bug the toolkit already fixed once — a gate going green over an un-run probe.

- **The mint now sits with the PROBE WORKER**, which is the only place left that can hold it, and is exactly what JL described ("the probe stage will pick them up"). `haipipe-paper-probe/SKILL.md` STEP 1 gains a **STAGE INTAKE — RESOURCE**: read `1a-resource.md`, and for every `Q<n>` that GATE 1 approved (present, not DECLINED in `_LOG`) carrying neither an `A:` nor a `-> PP<NN>` backlink, MINT one card (`serves: resource · blocks: N<n> · target: ? · status: planned · ## Need` = the Q verbatim — a resource question is already paper-agnostic, it asks what EXISTS and never which answer is wanted). Then WRITE THE BACKLINK `**Q<n> (N<n>) -> PP<NN>**` into 1a-resource.md.
- **The stage still never mints a PP id and never picks a probe type or topic.** JL's ruling is preserved intact. The worker mints; the GATEWAY picks the type and the topic in its SWEEP. The ownership chain, now stated explicitly in the skill: `DRAFT asks (Q) -> GATE 1 approves -> PROBE WORKER mints -> GATEWAY picks type+topic -> answer lands -> TRANSLATE writes the A back into the Q`.
- **The answer comes home.** `haipipe-paper-probe` STEP 3 (TRANSLATE) gains a **RESOURCE WRITE-BACK**: a card that `serves: resource` writes its landed takeaway into 1a-resource.md as the Q's `A:`. A BUILD card writes its A the moment the build is BOOKED (`COMMISSIONED · owner · eta · blocks · cross-project`), not weeks later. Two receipts, always — the card is the probe-layer one, the Q's `A:` is the consumer-facing one; 1a-resource.md is what the human reads at GATE 2 and what claims reads downstream, so a stage whose answers live only in cards never sees its own answers.
- **The vacuous green is closed.** `check-probe-cards.sh` gains a RESOURCE-STAGE PASS (fires only on `--stage resource`, and only when `1a-resource.md` exists): every Q must carry an `A:`, or a `-> PP<NN>` backlink **to a card that exists on disk**, or a DECLINED line in `_LOG`. A Q with none of the three FAILs by name — `unasked-question(Q3)`. A backlink to a card that is not there FAILs as `dangling-backlink`. And "no cards serve stage resource" while questions are still open no longer prints the reassuring OK: it FAILs as the vacuous green.
- Documented in the artifact template: the `-> PP<NN>` backlink is the mechanical proof the question was ASKED, and the Done-criteria now test A-or-backlink-or-DECLINED rather than only "every Q that has landed carries its A" (which was silent on the ones that never landed — the exact hole).

Verification: a fixture with (a) an unasked Q, (b) an asked Q with a resolving backlink, (c) an answered Q FAILs (a) by name and PASSes (b) and (c); adding the backlink to (a) turns the run green (exit 0); pointing it at a card that does not exist FAILs as `dangling-backlink`; a DECLINED-in-`_LOG` Q is exempt; and papers with no `1a-resource.md` are byte-for-byte unaffected.


## [1.1.1] — 2026-07-14

Fixed (adversarial review, BLOCKER 10 — the card-checker locator could resolve to the WRONG SKILL FAMILY)

- **Checker locator disambiguated, in BOTH places this skill locates it** (GATE 2 code block; Done-criteria now points at GATE 2 rather than repeating a second, divergent copy). TWO files named `check-probe-cards.sh` exist on disk — the paper family's under `haipipe-paper-probe/`, and the application family's under `haipipe-application-probe/`. The shipped locator was `find ... -name check-probe-cards.sh | head -1`, whose result depends on `find`'s traversal order: it could hand GATE 2 the APPLICATION checker and silently assert this paper against application invariants. Now filtered on the path: `-path "*haipipe-paper-probe*"`.
- **A missing checker now FAILS LOUDLY**, never silently: `[ -n "$CHK" ] || { echo "FAIL: paper checker not found"; exit 1; }`. A gate that cannot run its checker has not checked anything, and a silent skip is exactly how a green gate ships over an un-run probe.

Companion repair, same blocker, in `2-phase/3-check/haipipe-paper-check` (v1.9.0): the worker that actually RUNS GATE 2 now KNOWS this stage — it gained a `resource` row in its per-stage gate table carrying the load-bearing sentence verbatim, the resource pass/fail rulings, the `--stage resource` card pass, and the THREE-exit amendment (proceed / reseed / park) that made `reseed` and `park` reachable in practice.


## [1.1.0] — 2026-07-14

Fixed (adversarial review, MAJOR 12 — GATE 1 was ordered so it had to authorize spend BLIND)

The defect was real and structural, not cosmetic. `cross-project:` exists to carry a sibling-project reuse candidate to the human gate that authorizes SPEND — but that candidate is NAMED by the gateway's SWEEP, and the gateway does not run until PROBE, which is AFTER GATE 1. So as shipped in 1.0.0, GATE 1 asked the human to authorize GPU-weeks of BUILD spend BEFORE anything had told them whether the thing already existed. The mechanism could not see its own motivating case: the masked-LM backbone sitting scaffolded one repo over at `ProjC-Model-1-ScalingLaw/tasks/A02_pretraining_mlm`.

The two lanes already implied the fix. SCAN is blocking and cheap; BUILD is not. So the SPEND decision belongs BETWEEN them, and PROBE runs in TWO passes.

- **New phase order.** `DRAFT -> GATE 1 (questions) -> PROBE/SCAN (blocking) -> GATE 1b (SPEND) -> PROBE/BUILD (non-blocking) -> REVISE -> GATE 2 (CHECK)`.
- **GATE 1 CORRECTED: it approves the QUESTIONS, not the SPEND.** Asking is cheap — every SCAN is minutes, and nothing expensive is reachable from GATE 1 without passing GATE 1b first. The human now approves THREE things (the DEMAND, the QUESTIONS, the SCOPE CUTS), not four. This restores JL's Q-not-PP ruling to its literal words: *"In the draft, I will determine whether we want to ask these questions."* A declined Q is still LOGGED in `_LOG`, never deleted. Logged as before: `[GATE] draft-review: approved`, quoting the user. Its scope is now "no Q is ROUTED before this line exists" (was: "nothing expensive is DISPATCHED").
- **NEW — GATE 1b / SPEND.** A SECOND, NARROW human stop. Fires ONLY if there is at least one BUILD question; with none there is nothing to authorize (`[GATE] spend-authorized: n/a -- no BUILD questions`). It sits AFTER the SCAN pass, which is the first moment the `cross-project:` candidates exist. The human decides, INFORMED, PER BUILD ROW: **build it · cut it · AUTHORIZE cross-project reuse** (JL ruling C4; JL 2026-07-05 — the orchestrator may NAME a sibling source, only the USER may CONSUME it). Each row is presented with what it BLOCKS (`N<n>`), its COST (pipeline-days, GPU-weeks, or a DUA whose cost is CALENDAR-MONTHS not compute), and its `cross-project:` candidate or `none-found`. Logged as `[GATE] spend-authorized: ...` in `_LOG`, QUOTING THE USER.
- **THE SPEND-GATE RULE (stated plainly, in three places — Phase Orchestration, Principle 9, GATE 2).** *NO BUILD-LANE CARD MAY BE DISPATCHED BEFORE `[GATE] spend-authorized` EXISTS IN `_LOG_1a-resource.md`.* A scope cut at GATE 1b is FREE; the same cut after claims costs a CLAIM; after display it costs a FIGURE.
- **PROBE is now two passes, still one worker call each.** SCAN pass: the gateway assigns type/topic/lane, mints the PPs, and dispatches the SCAN lane only; it BLOCKS, and the A's land — including every BUILD row's swept `cross-project:` candidate. The BUILD cards exist as PROPOSALS at this point; nothing in the BUILD lane has dispatched. BUILD pass (after spend-auth): the authorized cards dispatch, NON-BLOCKING as always, landing as `status: commissioned` with owner + eta + blocks + cross-project. Rows the human CUT are logged as scope cuts, not commissioned; rows sent to REUSE carry the authorized sibling path.
- **New GATE 2 ruling.** A `commissioned` BUILD card with no `[GATE] spend-authorized` line in `_LOG` -> **FAIL**. A gate that can be walked around is not a gate.
- **New done-criterion.** If any BUILD-lane question exists, `[GATE] spend-authorized` must exist in `_LOG`, quoting the user, timestamped AFTER the SCAN answers landed.
- **Verb surface updated.** `probe` now runs the SCAN pass and stops at GATE 1b on first invocation; re-invoked after spend-authorization it runs the BUILD pass.

Unchanged (explicitly): the artifact is still EXACTLY TWO SECTIONS (Demand + Questions). Nothing JL cut on 2026-07-14 — Kill Conditions, Setup Contract, Resource Ledger, Binding table, all sidecars — is restored. The stage still ASKS and never mints a PP id, never picks a probe type or topic; the gateway still owns that. `cross-project:` mandatory on every BUILD card and the C6 eta test remain as enforced in `check-probe-cards.sh`.


## [1.0.0] — 2026-07-14

Added (JL ruling 2026-07-14, Paper-CGMtoAge postmortem — new lifecycle stage)

New venue-FREE stage between seed and claims: `seed(0) -> RESOURCE -> claims(1) -> [venue] -> pitch -> narrative -> display -> section-edit`. Answers one question: what must EXIST for this paper to be testable, does it exist, and can it CARRY the claim?

- **Placement.** `<paper>/0-lifecycle/1a-resource/1a-resource.md` + `_LOG_1a-resource.md`. SHARES the number 1 with `1b-claims/` — deliberate, and already precedented on disk by `2a-venue/` + `2b-pitch/`. No other stage renumbers: `stage-strip.sh` strips the leading digit before matching and the spine key is the bare name `resource`.
- **Scope (JL ruling C1): DATA + MODELS + PRODUCING-CODE.** Any prerequisite. Datasets, checkpoints/backbones, and producing-code ("does code that emits metric X exist?") are the same kind of question; data is the bulk but not the boundary. Live proof for models: Paper-CGMtoAge needs an MLM CGM backbone, no checkpoint exists, but the pipeline is scaffolded one repo over (`ProjC-Model-1-ScalingLaw/tasks/A02_pretraining_mlm`) — the difference between GPU-WEEKS and a RUN. Live proof for producing-code: Paper-ScalingGlucose shipped an AUROC claim to its ABSTRACT with no producing code.
- **Artifact: EXACTLY TWO SECTIONS.** Demand (one `N<n>` per hypothesis, derived from the seed) and Questions (one `Q<n>`, and its `A` when the answer lands). JL explicitly CUT Kill Conditions, Setup Contract, Resource Ledger, Resource Binding table, and ALL sidecars (no `_VALUES_`, no `_CITATION_`, no `_RESOURCE_` satellite, no new lane worker). Two sections suffice because "do we have it?" and "does it WORK?" are BOTH the A — no existence axis, no fitness axis, no binding table.
- **Keyed on `H<n>`, not `C<n>`.** C-ids do not exist at resource time (seed emits H1/H2/H3 as prose; C-ids are minted downstream in claims). Writing the stage in C-space would require retro-fitting a claims ledger that was already written.
- **THE STAGE ASKS; THE PROBE LAYER ROUTES (JL Q-not-PP correction).** The stage writes Q ids and NEVER mints a PP id, NEVER picks a probe type or topic. At GATE 1 the human picks which Q's are worth asking (a declined Q is LOGGED, not deleted); the probe gateway then assigns each approved Q its type/topic/lane, mints the PP, routes and dispatches it, and the answer lands back as the Q's A. Side effect: minting no PP ids, this stage cannot collide with a sibling paper's ids.
- **The cleavage rule (the stage's constitution).** A question that CHANGES what exists on disk -> RESOURCE. A question that READS what exists and MOVES A CLAIM'S STATUS -> CLAIMS. The pipeline-stage/task-type rows the toolkit had already written but filed under claims MOVE here: `task-for-data` (input), `task-for-algo` (method), `task-for-fit` (fit). `task-for-eval` (evaluate) STAYS IN CLAIMS.
- **Two hard boundaries.** (1) Resource may NOT commission `task-for-eval` — the one rule that stops the stage swallowing the paper; the live anti-pattern is PP04 in Paper-CGMtoAge, self-labelled "bundled fit+eval", whose bundling is exactly why its null was uninterpretable (MODEL or CORPUS?). (2) Resource NEVER EXECUTES — never `/haipipe-data`, `/haipipe-nn` or `/haipipe-task`, never scaffolds a task folder, never scans a store inline. It writes questions; the gateway dispatches.
- **Two lanes.** SCAN (minutes, GATE-BLOCKING — store scan / capability grep / access-rung PUBLIC|REGISTER|DUA|APPLICATION; a SCAN whose route exceeds ~1 HOUR is MISFILED, re-route to BUILD or shrink it) and BUILD (days to weeks, NON-BLOCKING ALWAYS — task-for-data/algo/fit plus long acquisitions like a DUA/IRB application whose ETA is in MONTHS of CALENDAR, not compute). BUILD cards carry `status: commissioned · owner: · eta: · blocks: N<n> · cross-project:`.
- **`cross-project:` is MANDATORY on every BUILD question (JL ruling C4).** A sibling-project path the gateway NAMED, or `none-found`. Empty -> FAIL. This wires JL's 2026-07-05 ruling (cross-project reuse is a USER decision; the orchestrator may NAME a sibling source but may NOT consume it) to the only human gate in the lifecycle whose job is authorizing SPEND. Without it, the gate authorizes spend BLIND.
- **GATE 1 (after DRAFT, hard STOP).** The human approves FOUR things: the DEMAND, the SCOPE CUTS, CROSS-PROJECT REUSE ("build it · cut it · or authorize reuse"), and the COST of every BUILD about to be commissioned (pipeline-days, GPU-weeks, DUA calendar-months). NOTHING EXPENSIVE DISPATCHES before `[GATE] draft-review: approved` exists in `_LOG`, quoting the user. A scope cut here is free; the same cut after claims costs a CLAIM, after display a FIGURE.
- **GATE 2 (CHECK) — the load-bearing sentence.** "Does every hypothesis have a resource that is HAVE+FIT, or a COMMISSIONED build with an owner and a DATE, or a SCOPE CUT the human said out loud?" NOT "are the resources BUILT?" — unanswerable in a turn when a build takes three weeks, and a stage that waits on one never closes. Answerable in MINUTES even when the work takes WEEKS. `commissioned` + owner + future eta -> PASS; no owner -> FAIL; a fitness ruling that does not say what it KILLS -> FAIL; a demand with NO resource is a SCOPE CUT, not a failure. CHECK RUNS `check-probe-cards.sh <paper_root> --stage resource` and SHOWS its output (checker located by glob, never a hard-coded relative path; `--stage` keeps other stages' un-run cards from redding this gate and this stage's in-flight builds from redding theirs).
- **C6 enforcement.** A `commissioned` card whose `eta:` has PASSED with no receipt is a HARD FAIL at the next gate. Without the date test, `commissioned` becomes the status every un-run probe wears and the whole mechanism ships as a LAUNDERING TOKEN. Already implemented in `check-probe-cards.sh`.
- **DRAFT forward-pointer consume-grep is GLYPH- and LEGACY-TOLERANT.** There are 7 live pointers on disk; ALL say "CLAIMS" (the stage did not exist when they were written) and at least one uses a UNICODE arrow (→). A strict ASCII/RESOURCE-only grep silently orphans all seven. The skill mandates `grep -E "\[FORWARD (->|→) (RESOURCE|CLAIMS)\]"`; each pointer becomes an N row, a Q, or an explicit DECLINE in `_LOG` (cleavage rule decides which pointers are ours).
- **REVISE default: skipped** (`[REVISE] skipped -- ledger doc, no venue-quality prose`), same as seed and claims. NOT skipped when a fitness ruling is woolly — "probably fine" is a DEFECT, not an answer. Either way the `[REVISE]` `_LOG` entry carries its `workers:` proof line.
- **Three exits (JL ruling C7) — AMENDS the Stage Exit Invariant in `08-stage-gate.md`.** `proceed -> claims` (normal forward gate); `reseed -> [LOOPBACK -> SEED]` when EVERY demand row is unobtainable and the paper cannot be written as seeded (🔥 moves back to seed); `park -> maturity: resource-blocked`. A stage whose PURPOSE is discovering the paper CANNOT BE WRITTEN must be able to SAY SO — without these it could only `promote -> claims`, mechanically handing a DEAD PAPER FORWARD.
- **Worked example in the Template section:** Paper-CGMtoAge as of the morning of 2026-07-07 (PP02/PP03 landed, PP04 not yet dispatched) — N1-N4 + Q1-Q5, verified against disk.

Rationale (the receipt)
- PP02, a SEED probe, landed 2026-07-07 already carrying the ruling in prose ("trainable now, but a mid-to-late-life clock, not a lifespan clock"). It HAD NOWHERE TO GO — no stage owned "this corpus cannot carry this claim", and nothing in the lifecycle could BLOCK A DISPATCH. PP04 trained on that corpus anyway and returned INCONCLUSIVE (FM MAE 9.313 vs baseline 9.387, p=0.071, negative R² on all 5 candidates), re-deriving at the cost of a full training pass exactly what PP02 already knew. This stage is where that ruling goes, and the gate that stops the dispatch.

Notes
- **Ships the standard stage folder, like every sibling:** `ref/resource-template.md` (the canonical two-section template the SKILL's Template section points at, with the Paper-CGMtoAge worked example) and `feedback/README.md` (the skill's feedback inbox). Without the template file, `haipipe-paper-draft` resolved no format source for a `resource` draft; the DRAFT-worker registry row that reaches it landed in `haipipe-paper-draft` 3.10.0.
- **C5: NO PILOT.** Built for real use; migration of live papers runs in parallel.
- Supporting wiring landed outside this skill: `haipipe-paper/stage-strip.sh` carries `resource` in the canonical spine (`seed resource claims venue pitch narrative display section-edit review`), and `2-phase/1-probe/haipipe-paper-probe/check-probe-cards.sh` implements the C6 eta test and the C8-i `--stage` filter.
