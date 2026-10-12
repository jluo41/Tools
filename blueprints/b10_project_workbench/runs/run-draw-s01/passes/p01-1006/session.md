261006 · Claude Code · the ladder drawings
=========================================

Agent: Claude Code. Summary of the session, not the raw log (the log stays in the agent's own
store). No project or patient data was used: the drawings are placeholders only.


What JL asked, in order
-----------------------

1. Put Run under Project as one hierarchy: Space → Project → Theme → Block → Job → Task → Run,
   with a checker in haipipe-project.
2. Draw it in b03's studio as dense, plain scratches (Nunito font, no colour, no project
   content, room to scratch anywhere), marked up in red by JL, answered in blue.
3. Ladder v3: a node per level, specials to the right, green "holds" arrow to the next level,
   definition + variants box under each node, Tools/ skills on the far right pointing left;
   strict column alignment.
4. Frames 2-4: Block, Job and Task variants with their full folder trees.
5. Frame 5: Task → Run → skill · agent, read from each workbench's ref/workbench-table.md;
   then the Workbench Space › subspace columns; then a UI scratch per row.
6. UI scratch for Block, Job and Task too; subspaces as tabs under the Space, not a left panel.
7. Frames 2-4 laid out like frame 5 (one row per variant, top to bottom); frames 2 → 5 left
   to right.
8. Skills per variant: owns · works · shows.
9. v3 frozen as JL's copy; the builder writes ladder-v4; both moved into this topic.


What came out of it
-------------------

- `build_ladder_v4.py` and `ladder-v4.excalidraw` (this folder).
- `../_build/canvas.py`: the writer that keeps a person's marks across rebuilds (seed ids from
  content, a snapshot of the last 8 builds, stale-tab detection).
- excalidraw-report skill 0.5.0: scratch rules, the plain concept table, the comment loop,
  the shared canvas.
- A Space workbench view (servers/space-home), built by a separate agent session.
- `../s02-studio-and-report/`: a separate agent session on Studio vs Report.


Links
-----

- Studio topic: `s01-overall-tree-structure` (this folder).
- Questions: `reports/q01_bjtr_boundary`, `q02_bjtr_across_themes`, `q06_skill_per_level`,
  `q07_workbench_mapping`.
