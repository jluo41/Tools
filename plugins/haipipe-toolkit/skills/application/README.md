# Application skill family

An Application is a pair of Boards whose Folders are owned by workflow phases:

```text
🔎 InsightBoard                                  🎨 DesignBoard
I0 Meta → I1 Question → I2 D → I3 I → I4 K → I5 W
                              └── signed W handoff ── PageX ──▶
                                                  D0 Brief → D1 Card → D2 Unit
                                                  → D3 Verdict → D4 Division
                                                  → D5 PageDown → accepted
```

It ends at accepted. Building, fielding, allocation, execution, and measurement
are Task work outside the Application.

## Folder model

`haipipe-folder` is the shared base. Every Folder has:

- a **Page Face** for reading, expression, and judgment;
- a **Task Face** for intent, work, progress, and closure;
- a phase-selected plugin profile;
- one gate and one handoff owned by the same phase.

`primary_face` identifies the normal entry, not the only face. Page Types no
longer own Application semantics. Existing runtime `page-type:` keys remain
readable through each phase skill's `legacy_page_type` metadata.

## Ownership

| Layer | Owns | Does not own |
|---|---|---|
| `haipipe-application` | two-board umbrella, routing verbs, PageX crossing, accepted boundary | interior I/D phases |
| `haipipe-application-workflow` | cross-board frontier, X0-X3 assertions, delegation and crossing receipts | a third P0-P4 machine |
| `haipipe-insight` | one-dataset, climb, register, partition, handoff laws | Folder-specific two-face content |
| `haipipe-insight-workflow` | I0-I5 order, GI0-GI6, cell frontier, dispatch and receipts | Design phases |
| `haipipe-design` | reads/born-of/grant/stance laws, bets, no-experiment boundary | Folder-specific two-face content |
| `haipipe-design-workflow` | D0-D5 order, GD0-GD6, thread/round frontier, dispatch and receipts | Insight phases |
| each phase skill | one Folder kind's Page Face, Task Face, plugins, gate, closure, handoff | family-wide routing |
| each plugin skill | reusable storage/surface/writer/boundary capability | deciding which phase uses it |

## Phase skill set

```text
application/workflow-phases/
├── haipipe-insight-meta/          I0 · meta
├── haipipe-insight-question/      I1 · question register
├── haipipe-insight-data/          I2 · run-bound observations
├── haipipe-insight-information/   I3 · reproducible pattern
├── haipipe-insight-knowledge/     I4 · bounded claim
├── haipipe-insight-wisdom/        I5 · counsel + signed handoff
├── haipipe-design-brief/          D0 · frame
├── haipipe-design-card/           D1 · bet + release/kill
├── haipipe-design-unit/           D2 · realization
├── haipipe-design-verdict/        D3 · independent judgment
├── haipipe-design-division/       D4 · render + accept/emit
└── haipipe-design-pagedown/       D5 · prose truth pass + round seal
```

Each file follows the mechanically checked contract:

```text
Position → Folder Kind → Input → Page Face → Task Face → Plugins
→ Gate and Closure → Handoff → Files
```

Run:

```bash
python3 ../board/haipipe-board/cli/foldercontracts.py --check
```

## Principle

Principle is not a Page Type or independent phase. The default warrant stays on
the D1 Card's `stance:`. D4 may promote one subordinate Principle Folder only
when a warrant serves two or more Design Pages or when two InsightBoards
conflict. D5 rereads it for staleness. Its rule is:

```text
because <signed W handoff>, do <move>, within <rail>
```

## Plugins

The phase selects plugins. Important boundaries:

- PageX is the one cross-Folder binding surface, across Boards and into Task
  Folders. A Folder card reads live plan/report/QA status when present.
- There is no `haipipe-plugin-task` or `task/` lane after migration.
- Code stays named **Code**. Task Face is universal; execution is behavior;
  Code is the optional presenter over `scripts/config/`, `runs/`, and
  `results/`.
- Principle is not a plugin.

## Runtime

Runtime paths and human decisions remain stable during this semantic migration:

```text
<application-root>/
├── <Subject>-InsightBoard/
│   ├── board.md
│   ├── 0-MT-meta/MT00-meta/ + MT01-MT04/
│   ├── 1-D-data/
│   ├── 2-I-information/
│   ├── 3-K-knowledge/
│   └── 4-W-wisdom/
└── <Topic>-DesignBoard/
    ├── board.md
    ├── 0-BR-brief/BR00-brief/
    ├── 1-P-principle/          optional promoted D4 role
    ├── workflow/rounds/R<NN>-pagedown/   minimal D5 audit receipt
    └── 2-DS-design/DS<NN>-<audience>-<job>-<venue>/
        ├── <stem>.md
        ├── design/             one evolving Card → Unit → Verdict thread Folder
        ├── delivery/render/
        ├── evidence/pagex/
        └── outline/
```

Insight may also use the partition-major layout defined by
`haipipe-application/ref/partition.md`. Layout changes paths, not phase
ownership.

## Cross-board workflow

`haipipe-application-workflow` reports the native frontiers unchanged:

```text
insight: <cell> · I<n> · GI<n>
design:  <thread> · D<n> · GD<n>
crossing: X0 need-out | X1 signed-handoff | X2 outbound | X3 read-back
```

It delegates to the owning workflow and adds no human gate. The four human
gates remain Probe release, Wisdom signing, Card release/kill, and Division
acceptance.

## Compatibility

- Read legacy `page-type: meta|question|data|information|knowledge|wisdom|
  brief|design` through phase metadata.
- Do not create new `haipipe-page-for-*` Application skills.
- Retired `intervention` and `artifact` are read-and-fold inputs only.
- Retired `principle` has no live compatibility key because no live page used
  it; D4 owns any future promoted role.
- Historical boards and receipts are not bulk-rewritten.
- Unmigrated families may retain legacy compatibility contracts until their
  own workflow phases absorb those Page faces.

## Validation

The migration is complete only when:

1. Folder-contract validation is clean and proven to fail on a broken fixture.
2. Page-Face outline resolution works for both `folder-kind:` and legacy
   `page-type:`.
3. the Page-Type compatibility inventory has no Application registry drift.
4. Board checks and Application family tests pass.
5. a fresh-context agent discovers the phase skill, follows both faces, selects
   plugins correctly, and stops at the owning gate.
