# Probe · legacy compatibility family

The active Page workflow no longer has Probe or PageX plugins. It uses one
typed Evidence Item graph:

```text
SHAPE    name E<NN>-VALUE|CITE|DISPLAY-<slug> and its acceptance contract
SURVEY   map Supporting Runs + one Local Input + one Local Page Run
LAND     validate supports, freeze input, execute/reuse the local Run
EMBED    fold the ready Result back into the Bullet Workspace
```

Current authorities:

| Concern | Contract | Storage |
|---|---|---|
| Evidence Item plan and Run graph | `../board/page-plugins/haipipe-plugin-outline/ref/item-table.md` | `<page>/outline/<stem>-evidence-items.md` |
| Evidence landing and embedding | `../board/page-workflows/haipipe-page-evidence/SKILL.md` | `<page>/runs/` + `<page>/results/` |
| Supporting execution/discovery | `../board/page-plugins/haipipe-plugin-runs/SKILL.md` | owning Folder's real Run/Result paths |

`_old/haipipe-probe/` and `agents/haipipe-probe-q-executor-agent.md` exist only
for un-migrated QA-bank records. They must not create a new `<page>/probe/`,
`<page>/evidence/pagex/`, or standalone Evidence surface. New cross-Folder
evidence is a Supporting Run Result; Related Page links belong to Context
Workspace.
