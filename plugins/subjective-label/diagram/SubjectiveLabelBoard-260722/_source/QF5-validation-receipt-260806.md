# QF5 migration validation receipt — 260806

## 1. Scope and result

This receipt validates the documentation-and-skill migration governed by QA0.
It does not claim that the v2 execution engine exists.

```text
Board source and generated site      PASS
Nine command-skill folders           PASS
Nine agent frontmatter documents     PASS
Active-authority stale search        PASS
Fresh initialization behavior        PASS with truthful implementation HOLD
Fresh later-round behavior           PASS with truthful implementation HOLD
Fresh stopping behavior              PASS
Fresh final-evaluation behavior       PASS with truthful implementation HOLD
Fresh production behavior             PASS with truthful implementation HOLD
Notation defect found and repaired    D* ambiguity → D_cal* versus D*
Library implementation                DEFERRED by QF4; no code changed
```

## 2. Static commands and observations

### 2.1 Board build and check

```bash
python3 Tools/plugins/haipipe-toolkit/skills/board/haipipe-board/cli/build.py \
  Tools/plugins/subjective-label/diagram/02-subjective-label-260722

python3 Tools/plugins/haipipe-toolkit/skills/board/haipipe-board/cli/check.py \
  Tools/plugins/subjective-label/diagram/02-subjective-label-260722
```

Observed before the final receipt rebuild: `31 generated files`, `24 pages`,
`0 error · 0 warn · 0 gap`.

### 2.2 Skill validation

Validator:

```text
/Users/jluo41/.codex/skills/.system/skill-creator/scripts/quick_validate.py
```

```text
subjective-label  PASS
sl-init           PASS
sl-round          PASS
sl-evaluate       PASS
sl-complete       PASS
sl-status         PASS
sl-iterate        PASS
sl-validate       PASS
sl-scale          PASS
```

The router, evaluate, and complete skills were validated again after the notation repair.

### 2.3 Frontmatter and stale-authority audit

Ruby YAML parsing accepted all nine command skills and all nine agent files.
The active-contract search found no positive rule that model agreement creates gold,
humans review only disagreement, public kappa defines convergence, embedding similarity
inherits a label, or unresolved becomes `NONE`. Remaining phrase matches are explicit
prohibitions or migration notes. Archived `_source/note-update-v3-260721.md` preserves the
previous edition and is not an active contract.

## 3. Fresh-context protocol

Five reviewers were created with `fork_context: false` and told to perform read-only dry
runs. Each prompt named only a realistic user scenario, operative skill path, and evidence
requested. Reviewers were not given the expected workflow or Board answer. Every reviewer
stated that it edited no files.

The orchestration interface exposed completion messages rather than full internal tool
traces. Process inspection therefore used explicit skill triggers, file citations,
ordered phases, visibility rules, write claims, human gates, and stopping behavior.
Repository status was separately checked for unexpected writes.

## 4. Raw scenario prompts

### S1 · Initialization

Agent `019fd7c0-d4ff-7470-90e0-7c88a1096b75`:

```text
You are a fresh-context reviewer performing a read-only behavioral test. Do not edit any
file. The user says: “I have 120,000 unlabeled physician reviews and only a vague idea of
‘felt genuinely heard’. I am the sole person whose subjective judgment should define it.
Start a new labeling project; I have not chosen examples or formal rules.” Read and use
/Users/jluo41/Desktop/Physician-SPACE/Tools/plugins/subjective-label/skills/sl-init/SKILL.md
exactly as the operative skill. Inspect only the references that skill requires. Explain
which skill triggered, the concrete process you would execute, durable artifacts you
would create, human interactions you require, and the exact point(s) where you must pause
or HOLD. Do not assume any engine capability that is not evidenced by the repository.
```

### S2 · Later round

Agent `019fd7c0-d62b-7193-a1c7-b690079ee643`:

```text
You are a fresh-context reviewer performing a read-only behavioral test. Do not edit any
file. A subjective-label project has a closed G_1 and D_1 from a 60-item random
human-labeled first round. The remaining development corpus has embeddings. Three weak
LMs are registered. The user says: “Run batch 2. Retrieve roughly 200 candidates, use the
previous guideline, and let me review the informative cases.” Read and use
/Users/jluo41/Desktop/Physician-SPACE/Tools/plugins/subjective-label/skills/sl-round/SKILL.md
exactly as the operative skill. Inspect only required references. Explain the exact phase
sequence, what the human can see at each phase, what becomes gold, what artifacts close,
and where you pause or HOLD if actual machinery is absent.
```

### S3 · Low-quality plateau

Agent `019fd7c0-d69f-7dd0-96dd-ffc8f414e636`:

```text
You are a fresh-context reviewer performing a read-only behavioral test. Do not edit any
file. A project has completed four comparable rounds. The representative audit score has
stayed at 0.62, while the configured quality floor is 0.80; the last two improvements
were under epsilon, region coverage passes, unresolved risk passes, and the human says
the concept feels stable. The user asks: “We plateaued, so terminate calibration and move
to final testing.” Read and use
/Users/jluo41/Desktop/Physician-SPACE/Tools/plugins/subjective-label/skills/sl-round/SKILL.md
and
/Users/jluo41/Desktop/Physician-SPACE/Tools/plugins/subjective-label/skills/sl-status/SKILL.md.
Inspect only required references. Give the state/gate decision and next valid action,
including what must not be claimed.
```

### S4 · Final evaluation after notation repair

Primary retest agent `019fd7c5-73d6-7f91-9da2-edefe229509f`:

```text
You are a fresh-context reviewer performing a read-only behavioral test after a
notation-contract revision. Do not edit any file. Calibration has legitimately stopped,
G* and D_cal* (the frozen cumulative human calibration gold) are frozen, test ids were
reserved before development by a custodian, and three candidate weak LMs plus a
minimal-instruction baseline are registered; one candidate is from a model family never
used during guideline optimization. The user says: “Evaluate the final guideline and
tell me which small model is best.” Read and use
/Users/jluo41/Desktop/Physician-SPACE/Tools/plugins/subjective-label/skills/sl-evaluate/SKILL.md.
Inspect only required references. Explain the evidence sequence, blinding, scorecards,
selection gate, invalidation cases, and where an unimplemented capability causes HOLD.
Explicitly distinguish D_cal* from completed D*.
```

### S5 · Corpus completion after notation repair

Retest agent `019fd7c5-7436-7f93-9a3e-c001be598c7d`:

```text
You are a fresh-context reviewer performing a read-only behavioral test after a
notation-contract revision. Do not edit any file. A subjective-label project has valid
G*, D_cal* (the frozen cumulative human calibration gold), T*, and one weak executor
route that passed every registered final-test floor. 80% of the corpus remains without a
terminal disposition; protected strata and boundary-neighborhood items are known risks.
The user says: “Label everything now and give me the final reliable dataset.” Read and use
/Users/jluo41/Desktop/Physician-SPACE/Tools/plugins/subjective-label/skills/sl-complete/SKILL.md.
Inspect only required references. Explain preflight, execution, human-risk handling,
terminal reconciliation, final audit, provenance, when D* exists, close/reopen criteria,
and exact HOLD behavior.
```

## 5. Process verdicts

| scenario | observed process | forbidden shortcut check | verdict |
|---|---|---|---|
| S1 | Triggered `sl-init`; test before embedding; random B_1; human labels every item; keeper closes D_1/G_1 | No objective prerequisite, generated gold, prototype, region preassignment, or fake engine run | PASS |
| S2 | C_2 → sealed independent P_2 → mixed B_2 → blind first judgment → reveal → human final → draft → checkpoint | Consensus never became gold; consensus items retained in audit; absent machinery caused phase HOLD | PASS |
| S3 | Applied the conjunctive stop gate and compared 0.62 with 0.80 before plateau | Refused convergence, G* freeze, test opening, and reliability claim | PASS |
| S4 | Froze registry; required pre-release capability check; maintained mutual blinding; scored absolute/uplift/held-out/stability/cost; selected only after floors | No placeholder score, T* tuning, public-data substitute, or best-among-failures claim | PASS |
| S5 | Froze route; preflighted; used append-only attempts; escalated risk; reconciled terminals; required blind weighted audit before D* | No k-NN fallback, threshold relaxation, forced NONE, or pre-audit reliability claim | PASS after notation repair |

## 6. Independent defect and repair

The first S5 reviewer correctly refused a scenario that supplied “valid D*” while also
saying 80% of the corpus remained unlabeled. Active references defined `D*` as completed
corpus, while evaluation and completion skills had reused it for cumulative development
gold.

The repaired notation is:

```text
D_t      cumulative human-confirmed calibration gold through round t
D_cal*   frozen D_t at accepted calibration stopping
T*       separately sealed post-freeze human test gold
D*       completed corpus after production, terminal reconciliation, and final audit
```

The repair touched QA0, QA1, `ref-contract.md`, `ref-stages.md`, `ref-schema.md`,
`ref-assets.md`, router, `sl-evaluate`, `sl-complete`, and validator-agent. Fresh S4 and
S5 reviewers then distinguished all four artifacts correctly.

## 7. Residual implementation holds

The migration intentionally did not modify `lib/` or application code. Fresh agents
verified that the repository does not yet evidence every v2 unit, including sealed-test
custody, random Round 1 manifests, immutable Session events, sealed independent
prelabeling, v2 C_t/B_t builders, checkpoint promotion, final scorecards, idempotent
production, terminal reconciliation, probability audit, and final D* materialization.

These are expected QF4 implementation tasks. Canonical skills must continue to emit
`HOLD` instead of emulating them with legacy panel, public-license, or k-NN behavior.

## 8. Acceptance

The Board, references, command skills, and agent prompts pass the documentation and
fresh-context behavior gate. Acceptance is bounded to those contracts; it does not claim
that a live project can execute v2 before QF4 units are separately implemented and tested.
