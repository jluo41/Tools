# The anatomy of one skill
state: 🟡 PARTIAL
owner: JL
method: use progressive disclosure and keep only execution-critical instructions in SKILL.md

## Question
What may live inside one callable paper skill folder?

A skill should give a fresh agent the minimum non-obvious procedure needed to do one job. Runtime context becomes expensive and contradictory when a skill folder also carries design history, migration notes, feedback archives, duplicated manuals, and every supported variant.

## Boundary
- ✅ Covered here
  The standard internal anatomy of one callable skill.
- ↪ Covered elsewhere
  Which callable skills should exist is `QA2`; the contract form for stage variants is `QE1`.

## Content
### Compact anatomy
```
<skill-name>/
├── SKILL.md       trigger and shortest complete execution procedure
├── references/    detailed contracts and variants, loaded only when needed
├── scripts/       deterministic operations that should not be rewritten
├── assets/        templates or files copied into outputs
└── agents/        optional discovery and UI metadata
```

### Loading rule
Metadata selects the skill.
`SKILL.md` explains the core loop and tells the agent exactly which conditional reference to read.
Scripts and assets do work without consuming routine reasoning context.

### Material that does not belong
Design Boards, changelogs, feedback archives, migration narratives, and status reports do not belong in the live invocation path.
If history must be retained, keep it outside the callable skill folder.

### First inventory
`haipipe-paper/SKILL.md` is 556 lines and currently owns routing, closing UI, comment history, evidence routing, and delivery needs.
`haipipe-display-poster/SKILL.md` is 854 lines.
Several live skill folders also contain `CHANGELOG.md` and `feedback/` trees.
These are compaction evidence, not a reason to move everything into the front door.

## Items to Finish
- [x] ✂️ Choose progressive disclosure
      One short SKILL.md points directly to conditional references, scripts, and assets.
- [ ] 📏 Set a compactness acceptance test
      A fresh agent should identify the entry, stop conditions, and next owner without reading family history.
- [ ] 🧹 Inventory the current paper skills
      The first large candidates are identified. Complete the classification of each extra file as runtime reference, deterministic script, reusable asset, or design history.
- [ ] 🧪 Forward-test the compact skill
      After the skill changes, give a fresh agent a real Board page and inspect whether it follows the intended path.

## Where we are
The compact anatomy follows the shared skill design standard.
No live paper skill has been reorganized in this Board pass.

## Files
- `haipipe-paper/SKILL.md`
  The largest immediate compaction candidate.
- `1-lifecycle/haipipe-paper-stage/SKILL.md`
  The runner that should retain only the page-first loop.
- `skill-creator/SKILL.md`
  The shared progressive-disclosure standard.
