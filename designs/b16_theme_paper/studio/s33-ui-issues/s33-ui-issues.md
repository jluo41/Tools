s33 · Paper workbench UI issues
===============================

**Topic:** what is wrong with the paper theme as the shared frame serves it today, found by a read-only review
of every level (the Board tab, a version tab, a Section tab), every Space and view, and every link on them.
Each issue says where it shows, what is wrong, what it should be, the code behind it and who owns it: the shared
frame (b03), the Board tab (s11), the version tab (s12) or the Section tab (s13). It is judged against what JL
asked for: clean and easy to read, no nested boxes, no filler repeated on every row, the old paper page's cards,
b03's question row, content written out where it matters, every link inside the frame, and a Disk box that
names the real files. Written in placeholders; the review's screenshots stay with the session, not here.

**Feeds:** `reports/` q01_paper_ladder (each level's screens)


Files
-----

```text
s33-ui-issues/
├── s33-ui-issues.md            this face
├── build_s33_ui_issues.py      the builder: the issues as lists, drawn as one frame per owner
├── s33-ui-issues.excalidraw    the drawing: title · shared frame · Board tab · version tab · Section tab · keep · open
└── s33-ui-issues.png           its preview
```

Rebuild: `python build_s33_ui_issues.py`, then
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py
s33-ui-issues.excalidraw s33-ui-issues.png 0.4`. An issue fixed is removed from the builder's list with a
green note where it was; a new one is added to its owner's list.

How the review was done (261008): every view of the three tabs fetched and shot with headless Chrome (it needs
`--timeout`, issue F5), every fold opened for a full-height shot, every link printed by those views checked
for its status, and each view compared with the files on disk and with the s11 · s12 · s13 drawings and b03's
studio-and-report design.


Decided
-------

(none yet: a decision is one line, s33-D01 · <what was decided> (<who> <date>))


Open
----

1. The Board's Main · Appendix · Delivery: the newest version only, or each version side by side?
2. Section › Comments: read the comments report's concern table as it is, or give a comments report a
   `## Review Items` table?
3. A sent version: do its sent files and its decision live in it, or in the next version's comments report?
4. The Board's Evidence list: drop it (each version has its own), or keep it with a version column?
5. What keeps the page loading after it has drawn (F5), and does it matter beyond headless screenshots?

(write here, or mark the drawing in red)
