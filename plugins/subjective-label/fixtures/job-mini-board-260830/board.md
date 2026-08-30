# Job-mini: the fixture run that proves the labeling pages work

spine: Run one mock labeling job (30 mock reviews × empathy) far enough that every division of a run page has something real to show, so the Page Type, the templates, and the family skills can be checked against a board a stranger can open. The corpus is fake; the artifacts, checksums, and gates are real.
close: The run page and the Dash render, the checker passes, and every number on the page traces to a file under fixtures/job-mini/.

## Topic

The `subjective-label` plugin's design board settled HOW the loop works. This board is a FIXTURE: it points the 0.4.0 family (Building and Scanning sides, round units, register, gates) at a 30-item mock corpus so the run pages can be exercised without spending a human's real labeling time.

One page holds one run: the mock corpus paired with the target `empathy`. Two calibration rounds are closed as full round units on disk under `fixtures/job-mini/rounds/`; the handoff is deliberately NOT written, so §4 and §5 demonstrate the empty-division-as-status rule.

Cast: JL is the semantic authority in the fixture's records, shown 🧠. CC built the fixture and the pages, shown 🔧. Every label in the fixture is mock data authored to exercise the contract, not a real human judgment; the page says so.

Words: a target is the one thing labeled on a page. A round is one unit folder closed by a checkpoint. A gate is one of the four stopping conditions read from the newest checkpoint. The seal is the reserved test never read during Building.

## Pipeline

**One run**: the chain the single page walks.

```text
🗄 30 mock reviews + 🎯 empathy
      │
      ▼
🔁 round units ──▶ 🧑 judgments ──▶ 📜 G_t ──▶ 📌 checkpoint ──▶ 🗺 register
      │                                                            │
      └───────────── another round, until the gates pass ──────────┘
                              │
                              ▼
        🔒 P2 Freeze → 🧪 sealed test → 📊 scorecards → 🏭 scan → 🎲 audit → 📦 D*
        (not reached in this fixture, on purpose)
```

## Pages

### SL · labeling runs

One page per corpus and label target. The contract these pages obey is `haipipe-page-for-labeling` 0.4.0, and the method they execute is the `subjective-label` family's six phases.

S-Label-Dash.md
S-Label-1-job-mini-empathy.md

## Links
haipipe-page-for-labeling   ../../skills/page-types/haipipe-page-for-labeling/SKILL.md
subjective-label            ../../skills/subjective-label/SKILL.md
label-building              ../../skills/label-building/SKILL.md
label-building-workflow     ../../skills/label-building-workflow/SKILL.md
subjective-label-workflow   ../../skills/subjective-label-workflow/SKILL.md
ref-assets                  ../../ref/ref-assets.md
QA1    ../../diagram/SubjectiveLabelBoard-260722/1-QA-semantic-contract/QA1-system-contract/QA1-system-contract.md
QLw00  ../../diagram/SubjectiveLabelBoard-260722/7-QLw-labeling-workflow/QLw00-the-workflow/QLw00-the-workflow.md
