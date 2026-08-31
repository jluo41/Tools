haipipe-task — Changelog
========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## 0.11.0 · 2026-08-31

**Config and ticket: recoverability replaces "no params" (JL 260831).** The old
rule said a ticket carries no params. That was a means, not the end; the end is
that a person can open a results folder months later and know what produced it.

- `config/` now holds TWO kinds: SHARED (loaded by several runs of the task —
  `cohort.do`, `_defaults.yaml`, no `rNN` prefix) and PER-RUN (`rNN_{stem}`,
  1:1 with `runs/rNN_{stem}`).
- A ticket MAY carry settings that SELECT A SLICE (year, source, fold). It must
  never restate a setting its config already holds — two sources of truth drift,
  and the drift is silent. Settings that change WHAT is computed (cohort, trait,
  spec family, outcome) stay in a config, where they are reviewed and diffed.
- Wherever a setting lives, the RUN records it: `results/<task>/<run>/runtime.yaml`
  carries run, started, host, user, `git_sha`, `git_dirty`, ticket, `config_file`,
  `config_sha256`, and every varying setting. Written BEFORE the work starts, so a
  crashed run still has an identity.
- `config_sha256` is the load-bearing field: two runs of the same name, from a
  config edited in between, are otherwise indistinguishable on disk.
- **Naming law for block/job/task/run, and a checklist that enforces it.**
  `ref/naming-bjtr.md` states eight rules, each traced to a real break: a name must
  stand alone at EVERY level (it travels into queues, results paths and logs), carry
  its stage letter, use the project's own vocabulary, be ordered numerically not
  alphabetically, never be shape words alone, never collide with a sibling across
  jobs, share one stem between ticket and config, and never be re-spelled by a script
  that could look it up.
- N9: never restate the tree in a file. A `sbatch/all.ps1` listing every ticket
  duplicates `t*/runs/` and needs a drift guard to stay honest — and that guard is
  the proof the file should not exist. `run_slice.ps1` with no filter runs
  everything; `-WhatIf` prints the plan computed from disk, so it cannot go stale.
  Checker code S6 replaces S4.
- Step 4 of SKILL.md is now RUN THE CHECKLIST: any verb that created or renamed
  structure ends by running `_tools/check_task_tree.py <block>` (codes N1 N2 N4 N5
  N6 N7 N8 S1 S2 S3 S5 S6 S7 S8 S9) and fixing findings before it reports.
  `--expect-fail` proves the checker can still fail.
- Audit codes R01 unidentifiable run · R02 same name different config_sha256 ·
  R03 git_dirty · R04 incomplete record. Reference checker `_tools/check_runs.py`,
  proven against a known-broken fixture before use (GATE-1).

**A batch DECLARES whether it runs one by one or all at once (JL 260831).** An
sbatch that does not say is telling the reader nothing, and "sequential" is not a
safe guess: a job whose runs overwrite each other and a job whose runs are
independent look identical from outside.

- `sbatch/batch.psd1`, beside the engine, states `Mode` ('sequential' | 'parallel'),
  `Ceiling` (the most that may run at once), `CollisionKey` and a one-line `Why`.
  `run_slice.ps1` REFUSES TO START without it.
- `Ceiling` is CAPACITY, `CollisionKey` is CORRECTNESS, and they are different
  questions. The engine builds WAVES: two runs that agree on every CollisionKey
  field land in different waves however wide the job runs. Real case, not
  hypothetical — in Physician-SPACE stage B a `full` and a `synth` run of one
  task-year write the same `BENE-*` and `BFAF-*` files, because only `CASES-*`
  carries the source in its filename.
- The banner states the mode on EVERY invocation and names the source of it
  (the file, or the `-Sequential` / `-Parallel <N>` override). `-Parallel` above
  the ceiling is refused; raising the ceiling is an edit with a reason.
- A named entry point forwards `@PSBoundParameters` (a hashtable, binds by name),
  never `@Rest` / `@args` (an array, binds POSITIONALLY). The array form bound
  `-WhatIf` to the next axis parameter and made all 24 of Physician-SPACE's entry
  points fail on every call. Checker code S9.
- New checker codes: **S7** an sbatch that never declares its mode, or declares it
  inconsistently (sequential with a ceiling above 1, a CollisionKey naming a field
  that is not a ticket coordinate); **S8** a doc naming a folder, ticket or script
  that does not exist; **S9** the array-splat entry point. All three proven to fire
  on deliberately broken copies before use (GATE-1).
- S8's companion is generation: a page that LISTS what the tree already holds
  drifts on the next rename, so the listing half of every task page and sbatch
  README is generated from the tree, and only the hand-written head is preserved.
  Reference generator: `_tools/write_pages.py`.

## 0.10.0 · 2026-08-31

New task-type `page` → specialist `10_page/haipipe-task-for-page` (one collection
job per Board Page: answers its task-route probe cards with code, values.yaml +
QA digests, proposes missing upstream tasks). Type table row, keyword map row
(collect·values·page-serving·probe-batch), Step 2/3a type lists now 10.
ref/run-sh-template.sh §4: the exec line hardcoded the pre-260830 `scripts/`
path for nested jobs while §1's CONFIG branch already handled both shapes;
`PY_PREFIX` now mirrors that branch (found by the 260831 task-for-page field
test).

## [0.9.0] — 2026-08-30

- **THE TASK IS THE PAGE, and it is self-contained** (JL: "I think under the job,
  the task will be the page, so task is more like the page... the runs and configs
  should within the task folder as well"). A task folder now sits DIRECTLY under
  the job and holds its own code, `config/`, `runs/` and `tNN_<name>.md`; the
  `scripts/` level is gone. The three document levels of a Board line up with the
  three folder levels of a job: BOARD↔BLOCK, GROUP↔JOB, PAGE↔TASK, and RUN keeps
  no counterpart because an execution is not a document.
- **The dividing line inside a job is AUTHORED vs GENERATED.** The task folder
  holds what a person wrote; the job holds what a machine produced (`results/`,
  `notebooks/`, `QA/`, `workflow/`). This is the line mode ② already drew, which
  is why a consumer-serving job still moves whole folders to its store.
- **Shared job code is `src/`, one name for every engine** (JL: "you can change
  the 0-libs to whatever, like code or src"). Not `code/`, which the SPACE's own
  package owns. Deliberately NOT an engine rule: `0-libs/` survives only in
  `Project-Personality-OpioidRx` (12 folders, 868 references, behind the CMS
  remote loop), recorded in hierarchy.md as "The 0-libs exemption" — a migration
  cost with a number, not a Stata convention. Tooling reads it; nothing writes it.
- **`sbatch/` splits by the same question**: one that SPANS tasks stays at job
  level, one that serves a single task moves into `tNN_<task>/sbatch/`. Many `.sh`
  in one `sbatch/` are alternative ENTRY POINTS, so they are not numbered: every
  file is `env.sh` or `run_*.sh`, an engine variant is `<name>.<engine>.sh`, and a
  job-level `run_` script must reference at least two different `tNN_` folders.
- **The shape detector changed and was a live bug.** `ref/run-sh-template.sh`
  decided flat-vs-nested from the ticket's parent folder name being `runs`, which
  the new shape also produces — every new ticket would have been read as flat and
  written `results/<run>/` instead of `results/<task>/<run>/`. The grandparent now
  breaks the tie (`t[0-9][0-9]_*` = a task folder), proven against all three
  shapes before being trusted.
- Swept across the family: `hierarchy.md` (level table, board↔block mapping,
  Levels 2-4, both drift checks, RUNNAME projections, sbatch), `SKILL.md`,
  `block-job-task-run.md`, `task-structure.md`, `authoring-conventions.md`,
  `task-lifecycle.workflow.js`, `workflow-template.yaml`, `fn/audit.md`,
  `fn/run.md`, `fn/qa.md`, and both task agents. STILL OPEN and marked as such in
  `hierarchy.md`: the Databricks column, "prefer FEW blocks" against a block being
  board-independent, whether a job name should read as a question group, and the
  migration bill for the jobs still in the old shape.
- Type specialists under `3_end/`, `4_individual/`, `8_stata/` and `9_agent/` are
  NOT yet updated; they still scaffold the pre-260830 shape.

## [0.8.1] — 2026-08-30

- **No orchestration-only job** (JL, the j05 ruling: "I don't understand this
  job name" → "split them into each job, so the job folder is self-contained"
  → "no more j05"). A job audits its OWN outputs at the tail of its run ticket
  and writes a receipt that MIRRORS the run dir under `audits/`; order between
  jobs is a data dependency, `required_audits` naming the exact upstream run,
  never a scheduler job. ref/hierarchy.md (block paragraph, nested tree
  `sbatch/` line), ref/block-job-task-run.md R9.
- Pilot (LLMRec b02): `j05_audit_ladder` dissolved into
  `audit_{a1,a2,b,c2}_outputs.py`, per-job `sbatch/run_all_arms.sh`, per-job
  `derive_model_arm_configs.py`; shared checks in
  `code/haiutils/agent_sdk/audit.py`; 118 tickets audit themselves; the
  9_agent llm-engine skill commands re-pointed to the jobs' own tickets.

## [0.8.0] — 2026-08-29

- Hierarchy renamed onto Databricks: BLOCK (was task-group) > JOB (was
  task-folder, THE self-contained unit) > TASK (new level: scripts/{NN}_*/
  with config/ always a folder) > RUN (a config stem — an execution, never a
  folder). Authority absorbed from ref/block-job-task-run.md into
  ref/hierarchy.md + ref/task-structure.md; old verbs `task-folder` /
  `task-group` stay as aliases of `job` / `block`.
- Two job shapes: NESTED canonical (scripts/0-libs shared + tasks; runs/,
  results/, notebooks/ mirrored at <task>/<run>), FLAT legacy accepted —
  ref/run-sh-template.sh auto-detects from the ticket's own path (verified
  both shapes + RESULT_STORE override on a mock repo, 260829).
- `store:` is a JOB property declared once (0-libs/config-defaults.yaml
  nested, configs/_defaults.yaml flat); per-run keys still honored as legacy.
- Two drift checks (task↔ticket, config↔ticket) made possible by the
  mirrored naming; documented with verified commands.
- Prefer FEW blocks: the letter is the block's identity (LLMRec audit:
  15 blocks / 32 jobs → 5 says the same thing).
- Same-day follow-ons (originally excluded, then done): a 68-file vocabulary
  sweep across the whole skills/task family (specialists, agents, page-types,
  fn/*.md; 290 replacements), a `job` alias on the workflow js input key, and
  a 5-reviewer audit whose fixes made the agent triad, fn/run+audit, the
  workflow js prompts, the stata dialect, and page-for-task shape-aware
  (nested <task>/<run> vs flat legacy).
- ONE GRAMMAR at every level (JL 260829, evening): `bNN_ · jNN_ · tNN_ ·
  rNN_<stem>` — level letter + two digits + stranger-test words. Block letter
  schemes and letter families retired (a family shows in the name). The
  address is the four prefixes joined, read off the path (`b02j01t01r03`);
  run-sh-template.sh reads them, computes nothing. Proven on a mock repo.
- LIBRARIES AND PROMPTS (JL 260830): code that several jobs import lives in the
  SPACE package `code/haiutils/` (LLMRec's agent runtime → haiutils.agent_sdk),
  never at project/block level; prompts are config and sit in
  scripts/tNN_*/config/prompts/ beside the config that names them, resolved
  relative to the config file; a job may be pure orchestration (sbatch/ +
  layout helpers) for a DAG that spans sibling jobs.
- A BLOCK IS A FOLDER OF JOBS AND NOTHING ELSE (JL 260829): no sbatch/, no
  shared code, no results above a job; jobs that share a DAG or a library are
  one job. Under scripts/, `tNN_*` = task, anything else = shared code, named
  freely (0-libs/ for Stata, src/ or code/ for Python).
- Naming law (JL 260829): the STRANGER TEST — `<noun>_<qualifier>`, shape
  words never alone, coined terms only when the block overview defines them;
  scaffolds refuse failing names (SKILL.md Step 3b NAME GATE, hierarchy.md
  "Naming", spec R8).
- Still open: the PowerShell store-resolution gap (block-job-task-run.md
  § Code that must change) and the other skill families' vocabulary (~84
  non-diagram mentions, boundary-reviewed as alias-safe).

## [0.7.0] — 2026-08-17

- Added the `insight` knowledge door and `fn/insight.md`.
- Separated execution from interpretation: P-B-E-R and QA remain source-side;
  the Task/Insights Board owns consumer-neutral DIKW Pages.
- Paper and Application now consume settled Insight handoffs through PageX rather
  than entering Task folders or rebuilding DIKW inside their own lifecycles.

## [0.6.3] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 6.3.0; older entries below keep their original numbers).

## [6.3.0] — 2026-07-19

- Owner ruling, 2026-07-19 (JL): "宪法 don't use this name, just use `probe`." The nickname
  "THE CONSTITUTION" / "the constitution" for `probe/haipipe-probe/SKILL.md` is dropped everywhere;
  each site now names either `probe` or the actual path.
  Touched: `fn/qa.md` (the QA-file anatomy / field-name / state-value pointer).

## [6.2.0] — 2026-07-14 — R19 hardening: the state line is read FIRST

> JL: what is R19? Make it self contained. 
>> CC 23:17: [SOLVED] R19 is the "claim" ruling introduced in 6.1.0 below (constitution: `probe/haipipe-probe/SKILL.md` PART 3a). Glossed inline so this entry stands alone.

R19 (the claim), in one line: the QA-file `- state:` line is the one mutable field that turns a write-once record into a TICKET — claimed `working` at dispatch — that becomes a RECEIPT — `answered` at Report — so a QA file can announce "a run is in flight RIGHT NOW", not merely "answered". This 6.2.0 entry HARDENS it: gate ① now reads that state line FIRST, before the literally-answers test.

- **Gate ① reads the STATE LINE *before* the literally-answers test.** The order is load-bearing. A `working` file's `## Answer` is EMPTY BY CONSTRUCTION, so the answer test is a guaranteed miss on it — the caller falls through to ③, allocates a NEW `<n>`, `set -C` never fires (different path), and RUNS THE SAME EXPENSIVE JOB a second time next to the one already in flight. A `working` file is matched on its `# Q —` LINE: same question ⇒ return the path + "in progress since <started>", run nothing.
- **A QA file with NO `- state:` line is MALFORMED, not legacy** (checker: `qa-no-state`). It is THIS layer's own file, so this layer REPAIRS it: tag `answered` if `## Answer` has a body; RECLAIM it as a zombie if the Answer is empty. A consumer may never do either.
- **The same-`<n>`/different-slug claim race is NON-FATAL BY RULING and is NOT a reviewer REVISE.** `fn/qa.md` said non-fatal in one paragraph and "the reviewer REVISEs it" twelve lines later. The reviewer's FILENAME check now carries the exemption explicitly, and renaming a QA file to "fix" it is forbidden (the body is frozen; a rename orphans a live claim).
- Reviewer twin (`haipipe-task-reviewer-agent` 1.3.0) gains the FULL QA-file review block it had been advertising and never had — token-identical to the discovery reviewer's.
- Twin: `haipipe-discovery` 3.2.0, character-identical.

## [6.1.0] — 2026-07-14 — THE CLAIM: a QA file becomes a TICKET that becomes a RECEIPT

Ruling of record: JL, 2026-07-14 (`Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/` PART 3b, the `>> CC0714` block).
Constitution: `probe/haipipe-probe/SKILL.md` v8.2.0, PART 3a — R19 (the claim) · R20 (supersession) · R21 (the three readers).

**THE HOLE IT CLOSES.** A QA file used to be written ONCE, at Report, complete. Its EXISTENCE meant "answered", and there was NO way to say *"someone is working on this right now."* So: two consumers ask the same question a week apart. The first dispatches an expensive P-B-E-R run. The second, **while that run is still going**, sees no QA file — and dispatches THE SAME RUN AGAIN. Nothing prevented it.

Added
- **ONE MUTABLE FIELD — the `state:` line.** A QA file now carries `- state: working | answered | superseded-by: QA/<m>-<slug>.md`, `- started: YYYY-MM-DDTHH:MM` (MANDATORY when `working`), and an optional `- by:`. Everything below the state line — `# Q —` / `## Answer` / `## Caveats` / `## Not-done` — is written once and never touched again.
- **Gate ③ P-B-E-R now CLAIMS FIRST.** At the moment it decides to run — before Plan, before any code — it writes the QA file with `state: working` + `started:` + an EMPTY `## Answer`, and COMPLETES it at Report (`state: answered` + the body). Gate ② DIGEST still writes ONCE, complete, `answered` (the facts are already in `results/`; zero code runs, so there is nothing to claim and nothing to race). Gate ① writes NOTHING. **Only gate ③ ever produces a `working` file, and only transiently.**
- **Gate ① SCAN now branches on the STATE LINE, not on existence.** `answered` → return the path · `working` → **DO NOT RE-RUN**, return the path + "in progress since `<started>`" (this is the duplicate-work fix; an expensive run is SAVED at ~0 cost) · `working` past the TTL → 🧟 ZOMBIE, RECLAIM it · `superseded-by: X` → follow the chain (possibly multi-hop) and return the LIVE answer's path.
- **`QA_CLAIM_TTL_HOURS = 24`** — the named constant. A `working` file whose `started:` is older is STALE: RECLAIMABLE by the next qa call (rewrite the claim with a fresh `started:`, record the abandoned attempt in `## Not-done`) and a HARD FAIL for the checker. **A `working` file with no `started:` can never expire — it is a zombie by construction, and it is INVALID.** Never hard-code the literal `24` anywhere; reference the name.
- **RACE GUARD: `set -C` (noclobber), and nothing more.** Two qa calls can decide ③ at the same instant and both pick `QA/3-`. The loser sees the file already exists, re-runs gate ① **ONCE**, and DEFERS — it never loops back into ③. This shrinks the race window from THE WHOLE RUN to microseconds. The residual same-instant/different-slug collision is NON-FATAL (gate ① finds both files). **No lock dirs, no lease servers, no ledgers, no flock** — all retired machinery in a new hat.
- **R20 SUPERSESSION.** A later run whose answer CHANGES writes `QA/<n+1>-<slug>.md` and APPENDS `superseded-by:` to the OLD file's state line (`- state: answered · superseded-by: QA/2-cycle.md`) — the only edit ever permitted to a frozen file, and only by its own owner. Supersede ONLY when the answer changed; a deeper cut or a different subset is just `QA/<n+1>`, and the old file stays live.
- **A REFUSE RELEASES its claim.** Never leave a `working` file behind a refusal — it tells every future reader that work is underway when nothing is.

Changed
- **⚠️ THE LOAD-BEARING INVARIANT IS *ONE WRITER*, NOT *WRITE-ONCE*.** The executor writes the file TWICE — the CLAIM at the ③ decision, the COMPLETION at Report. Two writes by the SAME owner, in its OWN folder, is fine. **A CONSUMER (probe/paper/application) must NEVER create, claim, edit, complete, or supersede a QA file.** A consumer-planted `working` file is the retired `_ASK/` stub wearing a `QA/` costume, and it is FORBIDDEN — the same violation as the A03 C6/C7 leak. "Write-once" was never the real rule.
- **R15 (ENRICH never mutates) still holds — FOR THE BODY.** Only the state line is ever mutable. Two edits in a file's whole life: `working → answered`, and `answered → + superseded-by:`.
- **STATUS is derived from the state line, not from mere existence.** `ls QA/` is no longer enough — the reader must OPEN THE FILE. No file = not answered · `working` = IN PROGRESS since `<started>` · `answered` = answered · `superseded-by: X` = answered but STALE, the live answer is X.
- **Stage 4 REPORT's file-ownership line gains its one exception:** on gate ③ the QA file is CLAIMED before Plan runs and COMPLETED at Report. That is two writes by the same owner — it does not break file ownership, it is what file ownership MEANS.
- `--check-only` now explicitly writes **NO CLAIM** (it already wrote nothing else). A qa call that fell through to ③ during the probe's MATCH step — a FREE detection pass — would otherwise spawn an unbudgeted run AND plant a claim.

Enforced (the checker's new teeth — the whole point is that these become MACHINE-DETECTABLE)
- `qa-working-no-started` — a `working` QA file with no `started:` → an UNEXPIRABLE claim.
- `qa-working-expired` — a `working` QA file older than `QA_CLAIM_TTL_HOURS` → a ZOMBIE.
- `qa-answered-empty` — `state: answered` with an EMPTY `## Answer` → a LYING RECEIPT.
- (consumer-side, in `check-probe-cards.sh`) `read-target-working` and `read-target-superseded` — a probe section at `state: read` whose `target:` resolves to an UNFINISHED or STALE QA file. **The latter is the day-1/day-40 silent-false-claim bug: every file internally consistent, the claim FALSE, and nothing caught it before.**

Files
- `fn/qa.md` — rewritten: the state line, the gate-path write contract, the CLAIM (Step 3a, with the `set -C` idiom and what the loser does), the RECLAIM path (Step 3b), SUPERSESSION, the three readers, status derivation, the five checker codes. `qa_state:` added to the return.
- `SKILL.md` — the qa-verb block, the QA/ folder contract, Stage 4 REPORT, the Step-2 `qa` routing note, description + summary.
- `agents/haipipe-task-orchestrator-agent.md` → 2.1.0 (I own the CLAIM; gate ① reads the state line; the loser defers without looping).
- `agents/haipipe-task-creator-agent.md` → 3.1.0 (at Report I COMPLETE the claim on gate ③, CREATE once on gate ②; never a lying receipt; never touch someone else's `working` file).

Twin parity: the discovery twin (`discovery/haipipe-discovery/fn/qa.md`, v3.1.0) states every field name, state value, TTL constant, flag spelling and bash idiom **character-identically**. Verified: all three bash blocks (grep/parse form, the `set -C` claim idiom, the staleness test) diff clean between the twins. They drifted before; they must not again.

## [6.0.2] — 2026-07-14 — probe-redesign residue sweep

Fixed
- **The task layer's own orientation diagram taught the exact behavior the redesign banned.** `diagram/01-architecture.txt:84-85` read: "the consumer (a paper/application stage, **via its PPNN card**) **reads the artifacts** and judges them." Two dead things in one sentence: (a) cards are retired — a consumer's question is a SECTION in `1-probes/PPNN_<topic>.md`; (b) under LAW 1 a consumer session NEVER reads bank artifacts inline (`paper/wiki/08-stage-gate.md` rule 4: "opening results/, reading a plan.yaml, grepping the code is bank work and breaks LAW 1"). The consumer reads the **QA file the EXECUTOR authored**. Rewritten to say exactly that, with the LAW-1 line stated inline so the diagram carries the rule and not just the shape. (The migration passes checked `SKILL.md` and `fn/`; `diagram/` was never swept.)

## [6.0.0] — 2026-07-14 — The `qa` verb: the task layer becomes consumer-unaware
## 6.0.1 — 2026-07-14

- **`--check-only` ADDED to the `qa` verb.** The constitution (probe/haipipe-probe/SKILL.md) and both PROBE workers instruct the MATCH step to "call qa in CHECK-ONLY mode: detect ①/②, execute nothing". The discovery twin implemented the flag; the task twin did NOT — its qa verb had exactly one optional positional (`<leaf>`), so `--check-only` was consumed AS a leaf path. That path never resolves, gate ① has no leaf to grep, gate ② finds no results/ there, and the verb falls through to ③ P-B-E-R: the MATCH step — defined as a FREE detection pass (T2: 1 grep + 1 read) — would silently SPAWN a full Plan->Build->Execute->Report run and WRITE into the bank. Now spelled identically to discovery's.
- **`<n>` ALLOCATION RULE ADDED.** Nothing allocated `<n>`, while parallel backgrounded orchestrators are the DESIGNED dispatch mode and two can be T3 ENRICH on the same leaf at once: both `ls QA/`, both see 2 files, both compute n=3, both write. The index invariant dies, the reviewer REVISEs a file that is correct in content, and on a slug collision the second Write silently CLOBBERS an answer that was never supposed to be editable. Rule: n = (highest existing n) + 1, computed IMMEDIATELY BEFORE the write; if the filename is taken, re-scan and take the next free n — never overwrite.

Spec of record: `Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/` v3 (APPROVED by JL 2026-07-14, rulings R1-R18). Constitution: `probe/haipipe-probe/SKILL.md` v8.0.0.

**BREAKING — the mailbox is gone.** `_ASK/` stubs, `_ANS/`, the `answers:` report field, external ids anywhere under `tasks/`, and the probe-aware `asks` verb are all DELETED. Nothing in this layer references a consumer, and nothing needs to. The task layer can now run with no idea that consumers exist — which is the point: evidence shaped by one consumer's frame is evidence the next one cannot reuse.

- **DELETED `fn/asks.md`** — the SCREEN/ANSWER verb. It read consumer-authored stubs and resolved consumer ids: probe-AWARE by construction, and unfixable as such.
- **NEW `fn/qa.md`** — the question door, and the layer's only one. `/haipipe-task qa "<question>" [<leaf>]` takes ONE question in general language (no id, no reference to whoever asked, no stake) and returns a PATH.
  - Gate, in order: **① QA SCAN** (grep `<leaf>/QA/*.md` — already answered? return the path, cost ~0; a hit counts only if the file LITERALLY answers the question — topic similarity is not an answer) · **② DIGEST** (`results/` already answer it but no readable digest exists → write `QA/<n>-<slug>.md` from the existing artifacts, run no code) · **③ P-B-E-R** (neither → run the lifecycle) · **🚫 REFUSE** (out of scope — e.g. a literature question — say so and stop; the caller re-routes).
  - **ENRICH depth ladder** on ③, shallowest first: depth 0 READ (enter at Report) · depth 1 NEW RUN (enter at Execute: `+configs/<new>.yaml` `+runs/<new>/`, never edit an old run) · depth 2 NEW SCRIPT (enter at Build: `+<new>.py` `+plan-script-<new>.yaml`) · depth 3 NEW LEAF (full P-B-E-R in a sibling). Scope test 2-vs-3: does it fit THIS leaf's `plan.yaml` IPO — same inputs, same process family?
  - **THREE CALLERS, one identical door:** a human steering an exploration · the orchestrator agent self-directed · a question relayed from elsewhere. None gets a special path, and the verb cannot tell them apart.
  - ACCRETES: QA files, configs, runs, scripts, leaves. FROZEN: past `results/`, existing QA files. LIVING: `plan.yaml`.
- **NEW `QA/` folder (OPTIONAL, per task-folder)** — `QA/<n>-<slug>.md`, `<n>` = creation order. **The numbering IS the index**; `ls QA/` is the index; there is no INDEX file. Slug only. Write-once — a later question ADDS `QA/<n+1>-…`. Sections, exactly: `# Q —` / `## Answer` (plain words + `[→ results/…]` anchors) / `## Caveats` / `## Not-done`. **The task layer authors it**, at Report.
  - **THREE REASONS, no fourth:** a question arrived · a digest was missing though `results/` already answered one · a task session judged a finding worth digesting. A `QA/` mirroring every result is noise, not an index.
  - **NO CONSUMER VOCABULARY** — no claim ids, no hypothesis ids, no "claims-stage", no "the paper". This layer never saw one and cannot honestly write one. (A task result file on disk today asserts a consumer's claim ids. That file is why this rule exists.)
- **TWO SESSION MODES stated plainly.** The task session's PRIMARY mode is AUTONOMOUS P-B-E-R — no question pending, no ask; this IS the project's research, and the bank grows here. ANSWERABILITY WORK (writing digests, building code so future questions are cheap) is legitimate task-native work with no question pending. `qa` is the SIDE door, never the engine. Consequence: most questions should land on gate ① or ②; a gate-③ run is the exception.
- Agents: orchestrator 2.0.0 (clean-context dispatch target; COMMISSION input form; runs the qa gate; returns `qa_file:` instead of `answers:`; may be self-directed), creator 3.0.0 (authors the QA digest at Report — the pen never leaves this layer), reviewer 1.2.0 (report gate lints the digest: anchored numbers, no vocabulary this layer could not have produced).
- Schema: `haipipe-workflow/ref/plan-schema.md` drops `answers:` entirely (haipipe-workflow 2.4.0).
- Swept: `fn/workflow-plan.md` (`probe_ref:` arg), `ref/metrics-json-schema.md` (an upper layer's aggregation contract), `DESIGN.md` (the "sandwich model" + "Downstream Consumer Contract" sections), `README.md`, `agents/README.md`.

## [5.10.1] — 2026-07-12 — Audit repair

- fn/asks.md Boundary said "this verb writes nothing" while its own ANSWER mode runs the full write-heavy lifecycle. Now scoped: SCREEN is read-only; ANSWER writes only inside the receiving task-folder (plan/report/script/configs/results) and still never edits the stub or the consumer's cards.
- `answers:` harvest greps made shape-agnostic; the field's schema (flow list of bare PP ids) is owned by probe/haipipe-probe/SKILL.md and pointed at, not restated.
- Frontmatter summary carried an impossible glob (`tasks/**/discoveries/**`) — the scan has two roots.
- Agents: creator 2.1.0 writes `answers: [PP04]` (list, not the ambiguous scalar); orchestrator's do-not list no longer names the retired `probe.yaml`.

## [5.10.0] — 2026-07-12 — `asks run <PPNN>`: screen an ask, then answer it

JL 2026-07-12: "could haipipe-task screen the _ASK, find an ask that is not finished, and then answer it by updating the code and run scripts." The SCREEN half shipped in 5.9.0; this is the ANSWER half. `asks run <PPNN>` resolves the stub → its task-folder and runs the normal 4-stage lifecycle with the stub as the contract — no new machinery:
- Stage selection by folder state: zeroth (only `_ASK/`) → Plan→Build→Execute→Report; existing code needing new analysis → Plan→Build (extend script + new `configs/<run>.yaml`)→Execute→Report; answerable by a new run alone → Plan→Execute→Report.
- The stub's `Do-not` lines are BUILD scope guards: if answering honestly requires crossing one (a retrain, a new sweep), STOP and report the conflict — never silently exceed the ask.
- `Pre-accepted` names the answer SPACE: a negative result is a COMPLETED ask, not a failure.
- Report writes `answers: PPNN`. The verb never notifies or touches the consumer's card — they harvest on their own schedule (the point of the file bridge).

## [5.9.0] — 2026-07-12 — `asks` verb: the task-side ask inbox

JL 2026-07-12 ("make haipipe-task aware of the PROBE _ASK", second half): the two-session workflow's task session needs an opening move — "which asks are waiting for me?". New `fn/asks.md`: scan `tasks/**` + `discoveries/**` for `_ASK/PP*.md` stubs (+ legacy flat), cross-check each PPNN against answering reports (`answers: PPNN` in report.yaml / discovery.yaml), print a pending-first bullet inbox with pickup commands. Read-only, consumer-blind — never opens the consumer's 1-probe-plans/ cards; PPNN stays an opaque token.

Same session, agent conformance fix (the awareness existed only in this SKILL): haipipe-task-creator-agent 2.1.0 (Stage 1 seeds plan.yaml from stubs; Stage 4 writes `answers: PPNN`), haipipe-task-orchestrator-agent 1.2.0 (stub-seeded zeroth-state input form; PLAN dispatch names the stubs; return carries `answers:`).

## [5.8.0] — 2026-07-12 — Ask stubs move into an _ASK/ container

JL ruling 2026-07-12 ("加一个 ask folder，把它们放到一块儿"; pairs with haipipe-probe 7.7.0): stubs live at `<task-folder>/_ASK/PPNN_<slug>.md` — one file per ask, the container keeps the task root clean when several consumers ask. The stub filename mirrors the consumer's `1-probe-plans/PPNN_<slug>.md` card, so `grep -r PPNN` finds both feet of the bridge. Zeroth state re-phrased: a folder whose only content is `_ASK/`. Legacy flat `_ASK_PPNN.md` at the root is read the same way and moved into `_ASK/` on first touch. All v5.7 semantics unchanged: read-only, Plan seeds from it, Report answers with `answers: PPNN`, this layer still tracks no consumers.

## [5.7.0] — 2026-07-11 — Probe handoff stubs (_ASK_PPNN.md)

Added (two-footed-bridge ruling, JL 2026-07-11; pairs with haipipe-probe 7.4.0)
- Stage 1 PLAN reads: `_ASK_*.md` (if present) — a READ-ONLY probe handoff stub dropped by an upstream consumer; Need seeds the intent, Deliverable the outputs, Do-not the out-of-scope list. A folder holding only a stub is a task in its zeroth state.
- Stage 4 REPORT: when a stub exists, report.yaml carries a top-level `answers: PPNN` — the disk signal the consumer greps to harvest.
- New "Probe handoff" paragraph after the ends-at-Report rule: the task never edits the stub, never writes the consumer's card, never reaches upward — "tracks no consumers" stays intact because the one consumer link on disk was written BY the consumer. Stub anatomy lives in the probe layer (haipipe-probe/SKILL.md "The handoff stub").

## [5.6.0] — 2026-07-08

- skill-diagnose fixes (3_end+core round): dead `fn/project.md` refs -> Skill("haipipe-project"); task-group letter table aligned to the SKILL top-NOTE defaults (+R raw, A=fit; "enforced consistency" claim removed); retired `/haipipe-project log task` dropped from fn/run.md; workflow-audit example no longer infers type from the group letter (and its cascade now mirrors Step 3a incl. raw/endpoint); `run`+`audit` added to Commands (were dispatchable but undiscoverable); ProjA-* examples -> Project-REACH-ADHD; run-row reads-list corrected.
- ref/: CONFIG NAMING UNIFIED — config filename == run filename everywhere (task-structure example rewritten, "freestyle" line removed; hierarchy type-table relabeled "config skeleton"; workflow-template <CONFIG>-><RUN>) — matches run-sh-template.sh and every real task on disk (JL: "yes, please go ahead and fix them"). hierarchy blesses the A00 stage-0 group index; runtime-yaml headline doc trimmed to shipped behavior; metrics-json-schema gains the `summary` object; config-meta-template gains notebook:/skip_review:; AIData token, footer 0-RawDataStore glob, D_demo note, databricks-execution illustrative values synced.

## [5.5.0] — 2026-07-04

### Changed (JL: "task其实不aware of discovery insight probe, 对吗")

- CONFIRMED by JL 2026-07-05: 5.3.0-5.5.0 read-through ("OK，没问题。") and ref/hierarchy.md letter defaults A fit/B eval/C display/D data/E individual/F agent/R raw/X_algo ("okay 好"); both review threads removed. README Boundary: JL picked option B, his five-layer mental-model table restored (reader-facing only, no upward routing).

- task layer made upper-layer-UNAWARE, same principle as discovery: description + body no longer route users to /haipipe-insight (replaced with "a task ends at Report; whoever consumes results records the link on THEIR side"); ref/metrics-json-schema.md no longer names the probe extractor (retired haipipe-probe-result ref removed); ref/task-structure.md skill-runner example made layer-neutral. Agents' caller-mentions (dispatch target for probe-orchestrator) stay — discovery precedent: advertising to callers is not layer-awareness. haipipe-workflow keeps naming all layers (toolkit-wide infra, not task-layer doc).

## [5.4.0] — 2026-07-04

### Changed (JL: "你看看这个skill有没有重复的地方" + "One sentence one line")

- dedup pass on SKILL.md, each thing now said ONCE:
  - feedback/digest was explained 3x (Commands + a ~25-line Step 2(0) restating fn/feedback.md + fn/digest.md + a ~30-line tail section) — Step 2(0) reduced to pure routing, tail section reduced to a 5-sentence pointer; the fn/ files are the single source.
  - the 9 specialists were listed 2x — Dispatch Table now references the type table instead of re-listing.
  - plan/report artifacts + plan-schema pointer appeared 2-3x — "Per-task observability" section deleted; its one non-duplicated line (Plan = intent, Report = evidence, same IPO shape) folded into Four Stages.
  - "/haipipe-project for project scaffolding" said 2x (Commands footer dropped); "/haipipe-insight separately" said 3x (intro copy dropped); Stata delegation prose halved (the code block already carries it); group-letter NOTE in Step 3a now references the top NOTE.
- ## Feedback + ## Behavioral Preferences rewritten one sentence per line (JL's in-file note, applied and archived here).

## [5.3.0] — 2026-07-04

Skill-set review fixes (see task/SKILLSET_REVIEW.md for the full diagnosis):

- routing repaired: dispatch calls now use the real skill names `haipipe-task-for-<type>` (were `haipipe-task-<type>`, which resolves to nothing); `endpoint` added to the known-type list, dispatch table, keyword table, and script-inference cascade ("7 options" was stale — 8 types + Stata engine).
- Step 3b scaffolds route to their real owners: project → `/haipipe-project`, group → the new `task-group` verb.
- fn/task-group.md + fn/scan-status.md (received from the project layer 2026-07-03) are now WIRED: new Commands verbs `task-group` and `scan-status`, dispatch-table rows, Step 2 cascade entries.
- Agents section: says three agents (orchestrator/creator/reviewer triad — orchestrator row was missing); stale "Codex two-stage" review claim replaced with fresh-agent independence (reviewer v1.1.0 removed Codex 2026-06-23).
- deleted legacy `fn/task-folder.md` (DESIGN.md Phase 4 recorded its removal 2026-06-08 but the file survived on disk); repointed fn/task-group.md's reference to the Step 3a specialist dispatch.
- Risk Profile: dropped stale "scope=project" sentence.
- ref/task-lifecycle.workflow.js + ref/workflow-template.yaml: `project/haipipe-workflow/` → `task/haipipe-workflow/` (dead since the 2026-07-03 move).
- PREFERENCES.md sync note reworded layer-neutrally (no paper-layer skill named from task).
- `raw` wired as a first-class task-type (JL decision): type table, known-type list, keyword row, script-inference, dispatch table — /haipipe-task-for-raw was an orphan nothing routed to.
- ref/hierarchy.md group-letter table rewritten: letters are PROJECT-SPECIFIC with specialist defaults A fit / B eval / C display / D data / E individual / F agent / R raw / X_algo (old table had a third, conflicting scheme: A=model-run B=eval C=display D=demo).
- CHANGELOG itself repaired: the two 2026-07-03 entries were numbered 4.2.0/4.3.0 (below the then-current 5.0.0) and appended at the bottom of a newest-first file; renumbered to 5.1.0/5.2.0 and moved into order.

## [5.2.0] — 2026-07-03

- (renumbered from 4.3.0) received ref/task-structure.md from project/haipipe-project/ref/project-structure.md (ownership refactor: project owns only the top-level container). Carries group folders, task naming, task-folder contents, skill-runner exemption, group/task diagram contracts, run script templates, runs/results/notebooks/sbatch relationship, auto-example rule; rules already in ref/authoring-conventions.md stay there and are only pointed to.

## [5.1.0] — 2026-07-03

- (renumbered from 4.2.0) received fn/task-group.md + fn/scan-status.md (+ ref/scan_status scripts) from haipipe-project (project skill reduced to setup-only). haipipe-workflow also moved into task/.

## [5.0.0] — 2026-06-11

- remove Stage 5 (Insight) from task lifecycle — insight is /haipipe-insight's responsibility, not task's. This skill is now a pure 4-stage code lifecycle (Plan/Build/Execute/Report). Task-group iteration updated accordingly.

## [4.1.0] — 2026-06-11

- task-group iteration — when given a task-group path, enumerate child task-folders and run lifecycle on each one sequentially (Step 3d). Removed project/task-group redirects to /haipipe-project; this skill now owns both task-folder and task-group scope.

## [4.0.0] — 2026-06-11

- 5-stage lifecycle — add Stage 5 (Insight), optional, files D_data observation card via /haipipe-insight-data for insight-worthy types. Code lifecycle (1-4) + data lifecycle (5).

## [3.0.0] — 2026-06-09

- 4-stage lifecycle (Plan/Build/Execute/Report) via task-lifecycle.workflow.js; creator-reviewer agent loop at each stage; all plans follow haipipe-workflow IPO schema; type-specific workflow-plan-sample.yaml in every specialist; project/task-group scope moved to haipipe-project.

## [2.1.0] — 2026-06-08

- three-layer plans; per-script IPO; Stata four-sister; wire reviewer+auditor agents.

## [2.0.0] — 2026-06-08

- add workflow lifecycle — audit, plan, report. New fn/ procedures. New ref: workflow-template.yaml.

## [1.0.0] — 2026-05-31

- baseline metadata added.
