s33 · UI issues
===============

**Topic:** every problem a review of 261008 found in the design workbench as served, ranked worst first,
each with where it is, what is wrong, what it should be, its evidence and who owns the fix (JL 261008:
"review the Design workbench as it is now and list every problem ... we can call it s33-ui-issue"). The
review opened the live design Block
(`examples-5-design/Project-Application-SMSDesign/designs/Design-SMSR2-Stage25-CarryOver-261008/`) at every
level, Space and view, shot each with headless Chrome, fetched every link, and checked the Disk box against
the files. It is the list the level owners work down; a fix is marked in `issues.yaml` and the drawing
rebuilt, so the topic shows what is still open.

**Feeds:** `reports/` q02_design_workbench


Files
-----

```text
s33-ui-issue/
├── s33-ui-issue.md            this face
├── issues.yaml                the one source: each problem (rank · owner · where · wrong · should · evidence),
│                              what works well, the change notes
├── build_s33_ui_issue.py      draws it: a title frame, one frame per owner, a "works well" frame
├── s33-ui-issue.excalidraw    the drawing; marks are kept on rebuild
└── s33-ui-issue.png           its preview
```

Rebuild: `python build_s33_ui_issue.py`, then
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s33-ui-issue.excalidraw s33-ui-issue.png 1`.


Owners
------

```text
s11   design_b12_theme_design_s11_blcok   the Block tab              9 problems
s12   design_b12_theme_design_s12_job     the Job tab               14 problems
s13   design_b12_theme_design_s13task     the Task tab              15 problems
b03   the shared frame                    links, Disk box, Runs      7 problems
```

The worst five: every plain `.md` link opens a 404 "Not a Page" (b03); Disk-box `.md` rows leave the frame
(b03); kept designs count as not passed, so the furthest-along Jobs read "0 of 10 passed" (s11); the Disk box
says "not yet" for Runs that exist, because it still uses the old Run names (s12, s13).


Decided
-------

s33-D01 · The list lives in `issues.yaml`, one row per problem; the drawing is built from it, never edited
    by hand (261008).
s33-D02 · Screenshots are not copied into Tools: they show the live Block's messages. Evidence names a view
    and a file and line, so anyone can reshoot it (261008).


Open
----

1. Who takes the four b03 problems first: the file reader (any `.md` read-only in the pop-out) unblocks
   every level.
2. Reshoot after the next round of fixes and mark what closed (`fixed: <YYMMDD>`).
3. The board was being changed while it was reviewed (Jobs renamed, j03 ranked): recheck the counts once it
   settles.

(write here, or mark the drawing in red)
