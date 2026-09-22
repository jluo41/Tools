# Discovery Board synchronization contract

This contract makes the Discovery BJTR tree readable as a Board while work is
still in progress. It does not create another hierarchy. The mapping is fixed:

```text
Block  bNN  = Board
Job    jNN  = Board Group
Task   tNN  = Page Folder + Page Face
Run    rNN  = execution record (never a Board Page)
```

## Ownership

- Discovery owns the Block, Job, Task, Run, Result, and Task/Page semantics.
- `haipipe-board` owns the Board parser, generated `board/` site, navigation,
  aggregate status, and Board close check.
- The direct `jNN_/tNN_` filesystem is the membership and default-order
  authority for a `board-kind: discovery-block` Board.
- `board.md` owns only Board identity, spine, close condition, Topic, Pipeline,
  map, and the presentation-level Job roster. It does not copy Task titles,
  Page state, Result prose, or Run inventories.

## The source that is formed along the way

Every canonical Block gets this source head at `open-block`:

~~~~markdown
# <Block title> Discovery Board
board-kind: discovery-block
spine: <the evidence program this Block organizes>
close: <the observable condition for closing the Board>

## Topic
<why these Jobs belong together>

## Pipeline
SCOPE -> PREPARE? -> ACQUIRE -> SYNTHESIZE -> Page CHECK -> CLOSE

## Board Map
```text
Block / Board
└── Job / Group
    └── Task Page
        └── Paper or Source Runs
```

## Pages
<!-- haipipe:discovery-board-jobs:start -->
### j01 · j01_<job-slug>
<one-line Job description>
<!-- haipipe:discovery-board-jobs:end -->
~~~~

The helper `scripts/board_sync.py` writes or repairs this head without
overwriting authored prose. Its managed span contains one exact-folder-bound
`### jNN · jNN_<job-slug>` heading per Job. It may say “No Jobs opened yet”
while the Block is new. It never lists `tNN` rows: the Board engine discovers
Task Pages from the direct tree and renders their current state.

## Checkpoint protocol

| Discovery event | Source change | Board action | What the user can read |
|---|---|---|---|
| `open-block` | create `board.md` with the Board head | `board_sync.py <block> --build --check --strict` | an empty Board with its spine, pipeline, and close rule |
| `open-job` | create `jNN_<job>/` and refresh the managed Job span | sync, build, check | a new Group appears; its Task roster is still filesystem-derived |
| `open` | create the `tNN_<task>/` Page Folder and root Page | sync, build, check | the Page appears under its Job with its current state |
| `scope` / `prepare` | update manifest, Page context, or instrument | build, check | the Board stays structural; Page and Task facts remain on their owners |
| `add` / `run` | add or update one `rNN` Run/Result pair | build, check at the Task or batch checkpoint | Page rows and derived status reflect the new evidence state |
| `synthesize` | update the root Page and derived Evidence Bib | build, check after Page CHECK | the Board shows the checked Page and current aggregate status |
| `close` | reconcile `discovery.yaml` report/status | build, check with `--strict` | the Board closes only when its `close:` condition is true |

Run internal steps may batch their checkpoint. A Board refresh is required
after a structural change, after a Run batch, after Page CHECK, and before any
user-facing completion claim. It is not a new Run and it must not mutate the
generated `board/` files by hand.

## Commands

From the Discovery skill directory:

```bash
python3 scripts/board_sync.py <path/to/discoveries/bNN_<block>>
python3 scripts/board_sync.py <path/to/discoveries/bNN_<block>> --build --check --strict
```

At `open-block`, pass `--title`, `--spine`, and `--close` when the defaults do
not express the agreed evidence program. Those values seed a new or repaired
head; an already authored non-empty value is preserved.

The helper is the narrow Discovery seam. For a Board-only edit, use the Board
skill directly:

```bash
python3 <path/to/haipipe-board>/cli/build.py <block>
python3 <path/to/haipipe-board>/cli/check.py <block> --strict
```

If the checker fails, report the exact Page or Board finding and route back to
the owner. Do not mark a Task or Board closed because the generated HTML exists.
