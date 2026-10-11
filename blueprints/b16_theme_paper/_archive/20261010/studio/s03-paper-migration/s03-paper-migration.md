s03 · paper migration
=====================

**Topic:** how the old paper folders (`A1-Story/`, the `Ba-`/`Bb-`/`Bc-<desk>-` groups, a root `delivery/`)
and the old paper page (`/_board/paper-board`) move to the new ladder (Block · Job · Task) and the shared
frame. Rewritten 261007 as a plain prototype (JL: the first version "is very badly written"): lines-only
boxes, few words, red only for the open points.

**Source:** the shell, `build_s03_paper_migration.py`, draws the picture, the steps and the open list; each
level is its own session's file, as in s31: `migration_block.py`, `migration_job.py` (-job session) and
`migration_task.py` (-task session), each exporting LEVEL, OLD, NEW, SCREEN, COUNTS and OPEN. Counts are read
from the Project paper Boards on every build, never a name.

**Feeds:** a proposed Q04, "How do the old paper folders and page move to the new ladder?"; Q01 (the ladder),
Q02 (where delivery lives), Q03 (where rounds go).


Files
-----

```text
s03-paper-migration/
├── s03-paper-migration.md            this notes file
├── build_s03_paper_migration.py      the shell (shared)
├── migration_block.py                the Block part (-job session)
├── migration_job.py                  the Job part (-job session)
├── migration_task.py                 the Task part (-task session)
├── s03-paper-migration.excalidraw    the drawing; marks are kept on rebuild
├── s03-paper-migration.png           preview
└── history/                          the earlier versions (v1 tables, v2 expanded), builder · notes · png
```

Rebuild: `python build_s03_paper_migration.py`, then
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s03-paper-migration.excalidraw s03-paper-migration.png`.


What the drawing holds
----------------------

```text
00 · the move in one picture   old tree → new tree, a level beside each new line
Block · Job · Task             old on disk │ new on disk (kept · new · moved · rebuilt · regenerated · open,
                               and why); on screen: old page view → new tab › Space › view; counts on disk
the steps                      settle → readers read both → dry run → one Board → the rest → retire the old page
open                           every level's open points, in red
```


Proposed (261007)
-----------------

1. Folders move, names stay: no Page is renamed (Story00, Story<L>, S-<desk>-…, RD<NN>), so every Run,
   receipt and Story row still finds it. A move edits `board.md`'s `## Pages` headings, the build config's
   paths and any `../` link.
2. `A1-Story/` → `j00_story/`; `Ba-`/`Bb-`/`Bc-<desk>-` → one version `j01_v1_<desk>/` with its Sections,
   its rounds and its `delivery/`.
3. Generated files are rebuilt, never moved by hand; frozen sent builds move as records, unchanged.
4. Readers first, then one Board at a time by a dry-run script, only when no session works in it; the old
   page stays linked until the last step.


Open
----

See the drawing's open frame (each level's file lists its own).

(write here, or mark the drawing in red)
