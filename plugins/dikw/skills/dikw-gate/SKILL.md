---
name: dikw-gate
description: "DIKW gate-review skill. Runs during step=gate of any phase. Produces the gate's proposed outcome: approve (next phase), revise <phase> [feedback] (redo / go back / rewrite plan), or done (jump to report). Use when the user asks to review DIKW results, run a gate, or says /dikw-gate. Trigger: review results, gate check, quality check, next step, should we proceed, go back, revise plan."
argument-hint: [snapshot_dir]
---

# DIKW Gate Review

Runs during **`step=gate`** of any phase. Produces the gate's **proposed
outcome** — one of `approve` / `revise <phase> [feedback]` / `done` — which
the orchestrator then accepts (via human or `--auto`).

Called by `/dikw-session` at each gate (`G-plan`, `G-D`, `G-I`, `G-K`,
`G-W`, `G-report`), or manually at any point.

## Context: $ARGUMENTS

Note: `snapshot_dir` is a `_agent_dikw_space/snapshot-<date>/` folder.

## Constants

- `AUTO_PROCEED = false` — *default.* When false, present the proposed
  outcome and wait for the human. When `true` (the session passed
  `--auto`), auto-accept the proposed outcome.

## Gate outcome vocabulary (the only three)

```
approve                      → current phase output is good; next forward phase
revise <phase> [feedback]    → re-enter <phase>
                                 <phase>=current → redo current phase
                                 <phase>=earlier → go back to that phase
                                 <phase>=plan    → rewrite the plan (bumps plan-version)
done                         → findings sufficient; jump to report
```

There is no other vocabulary. Any proposal must map to one of these three.

## Persona (reviewer voice — set once at session start, locked for the whole session)

The gate's tendency is controlled by `DIKW_STATE.gate_persona`, set once
at `/dikw` Stage 4 and never changed mid-session. Three layers compose:

```
preset (Tier 1)  +  axes (Tier 3)  +  notes (Tier 2)  →  persona block
```

**Tier 1 — preset (required).** One of:

| Preset      | strictness | ambition | Default route when in doubt |
|-------------|-----------:|---------:|-----------------------------|
| `strict`    |          8 |        4 | `revise plan`               |
| `balanced`  |          5 |        5 | `revise plan`               |
| `creative`  |          3 |        8 | `approve`                   |
| `lenient`   |          2 |        3 | `approve`                   |

The preset seeds the two axes and sets the default route.

**Tier 3 — axes (optional overrides).** Integers 0–10; if present,
override the preset's seeded value:
- `strictness` — evidence bar. Concrete thresholds below.
- `ambition`   — richness bar. Tone-only (the LLM interprets).

Concrete `strictness` thresholds (applied in Step 3 "Sufficiency"):

| strictness | Evidence bar for categorical claims |
|-----------:|-------------------------------------|
|        0–3 | Directional language is fine; narrative judgment allowed |
|        4–6 | Point estimates + n are required; CI encouraged |
|        7–8 | CI must exclude the target to make a categorical claim; otherwise mark as "directional / CI-limited" |
|       9–10 | CI must exclude the target AND n must meet a stated minimum; otherwise `revise plan` |

`ambition` is tone-only — higher values mean the gate pushes K/W
toward richer patient-level synthesis, named hypotheses, and
follow-up questions, and is less willing to approve minimal
"contract-met" reports.

**Tier 2 — notes (optional free text).** A short string prepended
verbatim to the persona block for domain flavor or reviewer voice
(e.g. `"Act as Reviewer 2 at a top clinical journal"`).

**How to build the persona block.** At Step 1, read
`DIKW_STATE.gate_persona` and compose:

```
You are reviewing as persona: {preset}
  strictness = {N}/10 — {threshold description from table above}
  ambition   = {N}/10 — {"push for richer claims" if >=7, "accept minimal contract" if <=3, "balanced" otherwise}
  default route when ambiguous: {revise plan | approve}
  additional voice: {notes or "(none)"}
```

Inject this block at the top of Step 4 reasoning and at the top of the
justification paragraph in Step 5. It does NOT change the A/B/C/D/E
options, the NN filename scheme, or the outcome vocabulary — it
changes the *tendency* of the proposal only.

**Missing or malformed persona.** If `DIKW_STATE.gate_persona` is
absent (older session) or unparseable, default to `balanced` with no
notes and log a one-line warning in the gate file.

## Steps

### Step 1: Gather context

Read fresh:

```
{snapshot_dir}/exploration/explore_notes.md            — snapshot-level data context
{snapshot_dir}/sessions/{aim}/plan/plan-raw.yaml       — current plan (symlink to latest v)
{snapshot_dir}/sessions/{aim}/DIKW_STATE.json          — phase, plan-version, gates[]
{snapshot_dir}/sessions/{aim}/gates/*.md               — all prior gate outcomes (files named {NN}-G-{phase}.md)
{snapshot_dir}/insights/data/*/report.md               — D reports
{snapshot_dir}/insights/information/*/report.md        — I reports
{snapshot_dir}/insights/knowledge/*/report.md          — K reports
{snapshot_dir}/insights/wisdom/*/report.md             — W reports
```

### Step 2: Identify the current gate

Determine which gate is firing from `DIKW_STATE.json.current_phase`:

```
current_phase == "plan"   → gate is G-plan (after initial plan write or revision)
current_phase == "D"      → gate is G-D   (after D tasks complete)
current_phase == "I"      → gate is G-I
current_phase == "K"      → gate is G-K
current_phase == "W"      → gate is G-W
current_phase == "report" → gate is G-report (final check)
```

### Step 3: Assess quality

**Completeness** — every task in `pending_tasks[phase]` satisfies the
artifact contract from `dikw-session/SKILL.md § "Task is complete iff…"`:
report.md exists and is >100 bytes, AND for D/I also `analysis.py` exists.
For `plan`, `plan-raw-v{N}.yaml` exists and has goal + a per-level task
list within the plan's configured cap.

**Sufficiency for next phase:**
- `G-plan`    → Does the plan cover the question? Are task descriptions self-contained (specific inputs, method, artifact)?
- `G-D`       → Do D reports profile what I needs? Key columns, quality issues, temporal structure?
- `G-I`       → Do I findings include specific numbers / effects / segments that K can synthesize?
- `G-K`       → Are causal claims evidenced; knowledge gaps named?
- `G-W`       → Are recommendations concrete (not vague)?
- `G-report`  → Does the final report answer the question? All phases summarized?

**Surprises** — any finding that invalidates a prior assumption (data quality
issue, wrong data grain, key column missing) routes to `revise plan`.

### Step 4: Produce the gate outcome

Pick **exactly one** outcome:

| Situation | Decision |
|---|---|
| Everything looks good, move forward | `approve` |
| Current phase had an **execution problem** (buggy code, misleading narrative, mislabeled section, wrong number in a report) — same spec on retry should fix it | `revise <current_phase> "<fix description>"` |
| An **earlier phase** is missing evidence this phase needs — same-spec retry of the earlier task | `revise <earlier_phase> "<what's needed and why current phase can't do it>"` |
| A task's **spec itself must change** — its description, output contract, method, or inputs — because the plan's v1 assumption is wrong or incomplete | `revise plan "<what changed and why>"` |
| Enough is done; skip remaining phases | `done` |

**Default rule — when in doubt, route per persona's "default route".**

The persona preset sets the default route for ambiguous cases
(`strict`/`balanced` → `revise plan`; `creative`/`lenient` → `approve`).
When the current phase's output has substantive feedback but no clear
execution bug, apply the persona default. The plan phase is still
where spec-level discussion happens; the gate's job is to surface the
issue and hand it off per the persona's tendency.

Use `revise <current_phase>` only for clear retry-with-same-spec cases
(e.g. a task skill crashed, an artifact is missing, nothing about the
output itself is under discussion).

Write to `{snapshot_dir}/sessions/{aim}/gates/{NN}-G-{phase}.md`:

`{NN}` is a **sequential gate counter** across the entire session
(two digits, zero-padded, starts at `00`). Every gate firing — whether
it's the first G-plan or the fifth G-D after a revise-plan loop — takes
the next NN. This gives every gate file a unique, time-ordered name
with no `-v{...}` suffix needed.

Example flow where `G-I` returns `revise plan`:

| # | Gate fires | Filename                |
|---|------------|-------------------------|
| 0 | G-plan     | `00-G-plan.md`          |
| 1 | G-D        | `01-G-D.md`             |
| 2 | G-I        | `02-G-I.md` (→ revise plan) |
| 3 | G-plan     | `03-G-plan.md`  (plan v2) |
| 4 | G-D        | `04-G-D.md`             |
| 5 | G-I        | `05-G-I.md`             |
| 6 | G-K        | `06-G-K.md`             |
| … | …          | …                       |

To compute NN: `NN = count(sessions/{aim}/gates/*.md)` at the moment
the gate is about to be written, formatted as `%02d`.

File contents:

```markdown
# Gate G-{phase} (plan-v{N})

Fired: 2026-04-22T15:00:00
Plan version: {N}
Current phase output summary:
  - D01-cgm_normalize_profile ✓ (2.1 KB)
  - D02-cgm_quality_sampling  ✓ (1.8 KB)
  - D03-context_streams_align ✓ (3.4 KB)

Assessment:
  Completeness: all 3 D tasks produced reports
  Sufficiency:  D reports cover distribution, sampling, context
  Surprises:    none

Decision: approve
Routes to: I
```

Or for a revise example:

```markdown
# Gate G-D (plan-v1)

Decision: revise plan "D01 showed only 61 readings over 75 days with huge
  gaps — not a continuous CGM feed as plan assumed. Plan's I-level
  'temporal_patterns' and 'bg_distribution_and_range' assume dense sampling;
  need to reframe as case-level observations with explicit sparsity caveats."
Routes to: plan (plan-version will bump 1 → 2)
```

### Step 5: Present to the human (when `AUTO_PROCEED=false`)

Present in this order:
  1. Banner.
  2. One-line proposed outcome (`approve` / `revise <phase>` / `done`).
  3. **Justification paragraph** (2–4 sentences, required): explain *why*
     you're proposing this outcome — what the reports collectively say,
     what the key judgment call was, and why the alternative outcomes
     were rejected. Do NOT jump straight to the findings table; the
     human needs a short narrative before the bullets.
  4. Findings / evidence table (with short verbatim quotes so the human
     doesn't have to open reports).
  5. Change table (if the outcome proposes task changes).
  6. (A)–(E) response options.

Keep the paragraph short — it's a rationale, not a re-statement of the
table. If you can't write a rationale in 2–4 sentences, reconsider
whether the proposed outcome is actually right.

Mapping from reply letter to gate outcome:

| Reply | Resulting outcome |
|-------|-------------------|
| `A` | apply the gate's proposed outcome verbatim (whatever it was: approve / revise / done) |
| `B: <feedback>` | override — treat as `revise <phase>` where `<phase>` is the current gate's phase, using the user's feedback text |
| `C` | force `approve`, ignoring the gate's revise proposal; next forward phase |
| `D` | force `done`, jump to `report` |
| `E` | cancel the session (no state change) |

```
[{subject} · snap-YYYY-MM-DD · NN_{slug} · plan-v1 · D-Gate · G-D · awaiting]

🔍 Gate G-D review
  ✅ Completed: D01-cgm_normalize_profile, D02-cgm_quality_sampling, D03-context_streams_align
  ⚠️  Finding: Sampling is sparse (61 readings / 75 days); plan assumed dense feed.

Proposed outcome: revise plan
  feedback: "D revealed sparse sampling; reframe I-level tasks as case-level
  observations with explicit sparsity caveats."

Tasks to re-run (with applied feedback):
  | #   | Task                    | Change                                                              |
  |-----|-------------------------|---------------------------------------------------------------------|
  | I01 | bg_distribution_sparsity_aware | Compute TIR/TAR/TBR with explicit N-caveat; no claims of stability. |
  | I02 | dense_window_zoom       | Zoom on 2021-02-15..17 (dense window) for within-window variability. |

(When the outcome is `revise plan`, this becomes "New plan tasks"
instead — same table shape, the column reads "Description" because the
tasks are brand new rather than re-runs of existing ones.)

Header convention:
  - `revise <current_phase>`  →  "Tasks to re-run"
  - `revise <earlier_phase>`  →  "Tasks to re-run"   (in the earlier phase)
  - `revise plan`             →  "New plan tasks"    (full plan-v{N+1})

How to respond? (reply with the letter)
  (A) accept the gate's recommendation above
  (B) provide your own feedback  — reply `B: <your feedback>` to override
  (C) go ahead to the next phase — approve as-is, skip the gate's recommended revise
  (D) done — jump straight to the final report, skip remaining phases
  (E) cancel
```

If `AUTO_PROCEED=true`, skip the wait and accept the proposed outcome,
but still print the above so the outcome is auditable.

## State update

After the gate outcome, `/dikw-session` updates `DIKW_STATE.json`:

```json
{
  "current_phase": "plan",                     // routed to by this outcome
  "current_step": "task",                       // next phase starts at step=task
  "current_gate": null,                         // gate closed after outcome applied
  "plan_version": 2,                            // bumped when outcome was revise plan
  "gates": [
    {
      "gate": "G-D",
      "plan_version": 1,
      "outcome": "revise plan",
      "feedback": "D revealed sparse sampling; reframe I-level ...",
      "routes_to": "plan",
      "timestamp": "2026-04-22T15:00:00"
    }
  ],
  "revisions_count": 1                          // incremented iff outcome=revise plan
}
```

## Rules

- Read ALL reports before deciding the outcome — outcomes must be grounded in full state.
- Be specific in `feedback` — name the column, the missing analysis, the
  exact issue. No vague feedback like "needs more analysis".
- If the outcome re-enters a phase, the `feedback` must describe the new
  task(s) with enough detail that `/dikw-plan` (for `revise plan`) or the
  phase skill can execute from it.
- `revise <earlier_phase>` must explain why the current phase can't fix it.
- Gate file path: `sessions/{aim}/gates/{NN}-G-{phase}.md` where NN is
  the sequential gate counter (see Step 4). Never reuse an NN — even
  if the same phase gate fires again after a revise-plan loop, it
  gets the next NN.
- `MAX_REVISIONS` is enforced by `/dikw-session` (the orchestrator), NOT
  by this skill. Propose freely; the orchestrator will downgrade a
  `revise plan` to `approve` with a warning when the cap is reached.
  This keeps cap logic in one place and avoids a write-order race on
  `revisions_count`.
