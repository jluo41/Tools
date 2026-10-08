s03 · paper migration
=====================

**Topic:** how the old paper folders (`A1-Story/`, `Ba-`/`Bb-`/`Bc-<desk>-` groups, a root `delivery/`)
and the old paper workbench (`paper.py`'s page, `/_board/paper-board`) move to the new ladder (Block · Job ·
Task, s01) and the shared frame (s11–s13), one Board at a time, without losing a Page identity or hand-editing
a generated file (JL 261007: "a new s03 about how to do the immigration from the old paper folder and
workbench to the new one").

**Source:** read from disk on every build: the Project paper Boards (`examples-*/*/paper*/Paper-*`), counted
and named Board 1..N only (no Board, Section or venue name is drawn); the old workbench's Spaces and Views
from `workbench-paper/ref/workbench-table.md`; the sizes of `paper.py` and `paper_theme.py`. Typed: where each
part goes, the readers' assumptions, the phases, the checks and the open points. Facts about the readers
and the build came from the Block session (paper_theme.py's author), 261007.

**Feeds:** a proposed Q04, "How do the old paper folders and workbench move to the new ladder?"; Q01 (the
ladder), Q02 (where delivery lives), Q03 (where rounds go).


Files
-----

```text
s03-paper-migration/
├── s03-paper-migration.md            this notes file
├── build_s03_paper_migration.py      the builder (b04's sketch helpers, b03's canvas writer)
├── s03-paper-migration.excalidraw    the drawing; marks are kept on rebuild
└── s03-paper-migration.png           preview
```

Rebuild: `python build_s03_paper_migration.py`, then
`python ../../../b03_project_workbench/studio/_build/render_png.py s03-paper-migration.excalidraw s03-paper-migration.png`.


What the drawing holds
----------------------

```text
1 · what there is to move   each Board: kind, Stories, Main/Appendix/Round Pages, frozen builds, desks,
                            delivery, _venue, root code, ../ links, receipts naming old folders
2 · the folder map          old path → new path, with why; Page stems never change
3 · the workbench map       the old page's Spaces → the frame's tabs; paper.py vs paper_theme.py; the
                            readers' layout assumptions and what each needs
4 · the phases              settle → readers → dry-run script → one Board → the rest → retire the old page
0 · why migrate             the workbench already reads today's layout (261007): the move is for the ladder's
                            names, one send = one version, homes for new parts, and retiring the old page
1b · each Board             its own repo or the SPACE's, its uncommitted paths, the phase it fits, its first step
5 · readers × layouts       every tool that finds a paper's folders: today's layout, the ladder's, the change
6 · the script              migrate_paper.py: preflight · plan (--dry-run) · apply · moves map · verify · roll back
7 · one Board worked        the Board with Sections, an Appendix and Rounds, counts only: before → after, and
                            what the script edits and what it leaves
Questions                   the proposed Q04
```


Proposed (261007)
-----------------

1. Page stems never change (`Story00-…`, `Story<L>-…`, `S-<desk>-Main-…`, `RD<NN>`): run names, the
   Story's compile order and receipts cite them. A move is a folder move plus a rewrite of `board.md`'s
   `## Pages` heading, the build config's paths and any `../` link.
2. `A1-Story/` → `j00_story/`; `Ba-`/`Bb-`/`Bc-<desk>-` → one version `j01_v1_<desk>/` holding the
   Sections, its `RD<NN>` rounds and its `delivery/` (JL's three open calls).
3. Generated files are rebuilt, never moved by hand; frozen `sent/`/`released/` builds move as records.
4. Readers first: the skills and `paper_theme.py` read both layouts before any folder moves; the old page
   stays linked from the band until the last phase.
5. One Board at a time, by a dry-run script, only when no session works in it; a Board with its own git
   repository is committed by its owner first.
6. (261007, the Block session) The workbench no longer waits on the move: the frame reads today's layout at
   every level (the paper theme's Block tab; level_patterns make each B<x>- group a Job and each S- a Task).
   So the move is for the ladder's names, one send = one version, the new Board homes (venues/, related/,
   reports/) and retiring the old page, and it can go Board by Board with no hurry.
7. The script is one Board per run: a preflight (a clean repo, no session at work, the readers pass), a
   printed plan, git mv with history, a moves map (`<board>/.paper-moves.yaml`) the tools read for old
   receipt paths, a verify (every Page opens at its level, assemble finds every fragment, no broken
   link), and a roll back from the moves map. Every paper Board is its own git repository today.


Open
----

- `A1-Story/` → `j00_story/`; rounds kept with their send; delivery in the version Job (JL to decide).
- The Board from before the layout: archive as it is.
- Code at a Board's root: move to a work Task by hand, or flag only.
- Old Run receipts with old paths: a moves map the tools read, or history only.
- One Job per send: today Ba-, Bb- and Bc- are three Jobs on the frame; the ladder merges them into one
  version (JL to decide; it changes the readers × layouts row for level_patterns).

(write here, or mark the drawing in red)
