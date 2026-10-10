s00 · Design structure
======================

**Topic:** the thinking behind the design ladder (JL 261007: "for the design, the key thing is what is
the design method, right?"), drawn as the design side of `../../../b11_theme_insight/studio/s00-insight-structure/`:
what a design method is; the methods as their own work Block whose Jobs are method versions; the
design Board whose Jobs pin a goal, one method version and one inputs version; the clocks; where a
new method version comes from and what triggers it; and the Block's questions with our ideas and the
choices still open.

**Feeds:** `../../reports/` q01_design_ladder, q02_design_workbench, q03_insight_steers_design (and a
proposed Q04, what a design method is and how it evolves).


Files
-----

```text
s00-design-structure/
├── s00-design-structure.md            this notes file
├── build_s00_design_structure.py      the builder; marks are kept on rebuild
├── s00-design-structure.excalidraw    the drawing: a design scratch, placeholders only
└── s00-design-structure.png           its preview
```

Rebuild: `python build_s00_design_structure.py`. The Questions frame reads `../../board.md`.


What the drawing holds
----------------------

1. A Design Project: `work/bNN_<app>_methods/` (the methods, versioned) beside `designs/bNN_<app>/`
   (goals, inputs, Jobs, designs); insights and discoveries optional; the Exp outside the theme.
2. What a design method is: a recipe, frozen per version, that turns a goal and its inputs into N
   designs, in five parts: see input, reason ideas, conduct, check each (T0 to T3), check overall.
   T4, the Exp, is the Learning loop, not part of the method. Three layers: a generic card (the
   Guide's 13), a method version made concrete for one app (inputs named, prompt written, checks
   coded, a bench), and a Job that pins that version by path and hash.
3. The two Blocks, each a box, a definition and its tree. Methods Block: one Job per method version
   (`j01_by-insight_m1`), frozen when closed, with `proposals/` as the backlog and `bench/` (fixed
   goals and inputs) so two versions compare on the same ground. Design Board: one Job per goal ×
   method version × inputs version; its Tasks are the N designs. Arrows: the Board's Job uses a
   version, never a copy; the Board's answers send proposals back.
4. One goal, two clocks (method, inputs) and the chain of Jobs; one clock per Job, so a change in the
   designs has one cause. Comparing methods is a sibling Job on the same goal and inputs.
5. Where a new method version comes from: six triggers (checks fail often, the N are alike, critique
   or pretest finds a pattern, the Exp says it loses, a paper suggests a procedure, a new kind of
   input) feed `proposals/`; the next version Job is written, benched against the last, reviewed by
   another agent, signed by a person and closed; the Board then adds a Job. New inputs alone need no
   new version.
6. Questions: the register's Q01 to Q03 and a proposed Q04, each with our idea (middle column) and the
   choice it waits on (right column, outlined red: still open).


Open
----

1. Methods in their own work Block, or frozen inside each design Job (`method.md`, as today)?
2. One methods Block per design Board, or one per Project shared across apps?
3. Does the Guide's card grow from three parts to the unit's five?
4. When to cut a method version: on a bench gain, per batch of proposals, or on demand?
5. One clock per Job?
6. Does a newer handoff make a closed Job's designs stale?

(write here, or mark the drawing in red)
