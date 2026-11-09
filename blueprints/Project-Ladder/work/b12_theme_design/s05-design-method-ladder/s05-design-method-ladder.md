s05 · Design method ladder
==========================

**Tags:** `Structure`

**Stage:** explore

**For:** a deck, and the method Block's folder contract and its pages (a design method's versions as Jobs you try), for the people who write the design skills and the workbench

**Delivery type:** skill

**Covers:** where a design method's versions are made and tested on the ladder: the method Block, a version Job and its five Tasks (write the recipe, build its checks, bench it, compare it, release it), how a design Board's Job pins a released version, and how the Board's results come back as proposals for the next version. M05's m1 → m2 → m3 is the worked example.

**Excluded:** making designs with a pinned method (the design Board, s01 and j01's pages); what a method card is in general (the Guide's 13 cards, s03-design-methods); the insight Prototype it copies (b11 s04-insight-structure).

**Topic:** A design Job pins one method version, but the methods themselves (M01 to M05, versions m1 to m3) live only as files in the Tools skill registry (`haipipe-design-method/methods/`), written by hand; no Job, Task or Run shows a method being written, tested or compared, so the Block's Methods view can only name the method a Job pinned (JL 261101: "how could we highlight more about the methods? … where is the task or jobs for designing the design methods? … the designer itself should be some tasks to try"). s04 drew the answer on 261007 and it was never built: a methods Block beside the design Board, one Job per method version, a bench of fixed goals and inputs, proposals as its backlog. The insight theme built the same shape as its Prototype (`insight/Prototype-<topic>/`, one Job per release, a Board Job pins a release), live on the SMS project. This topic draws it for design, so a method version is work you try: written, benched, compared by another agent, signed, then pinned.

**Feeds:** `reports/` q06_design_method_ladder


Files
-----

```text
s05-design-method-ladder/
├── s05-design-method-ladder.md            this face
├── s05-design-method-ladder.mindmap.md    its mind map, built from this face
├── build_s05_design_method_ladder.py      the builder (excalidraw-studio draw.py); marks are kept on rebuild
└── s05-design-method-ladder.excalidraw    the drawing: the gap · the method Block · the loop, M05 as the example
```

Rebuild: `python build_s05_design_method_ladder.py`.


Proposed (261101)
-----------------

```text
work/Method-bNN-<app>/                one Block: the methods this app's designs use
├── board.md                          its methods, the bench, the proposals backlog
├── bench/                            fixed goals + inputs, so two versions compare on the same ground
├── proposals/                        from Board Jobs and Exp scores: what the next version should change
└── jNN_<method>_m<k>/                one version of one method (a designer)
    ├── t01_write-recipe/             the five steps' prompts, the agent, what ① may read (and its tools)
    ├── t02_build-checks/             T0 rules · T1 sources · T2 critique · T3 pretest
    ├── t03_bench/                    run it on the bench: fixed goals + inputs → N designs
    ├── t04_compare/                  another agent: against m<k-1> and the sibling methods, same bench
    └── t05_release/                  🙋 a person signs; frozen; a Board Job pins it by path + hash
```

- The generic method stays in the Tools skill (the Guide's 13 cards, each method's definition); a version written for one
  app's inputs (its prompts, checks, and scripts such as `aggregate_query.py`) moves into the Project's method Block.
- The design Block's Methods view becomes the method ladder: each method × its versions, bench score, Exp score, the Jobs
  that pinned it.


Decided
-------

(none yet: a decision is one line, s05-D01 · <what was decided> (<who> <date>))


Open
----

1. ? One method Block per app (`work/Method-bNN-<app>/`), or one per Project shared by its design Boards.
2. ? Move the app-specific versions (M05 m3's `aggregate_query.py`) out of the Tools skill into the Project, or keep the
   registry in Tools and link the Project's version Jobs to it.
3. ? What the bench is: a fixed goal and inputs version from a design Board (`inputs/i1`), or its own small set.
4. ? Does a version Job need its own 3 × 3 pages, or does it reuse the design Job page with the five Tasks above.

(write here, or mark the drawing in red)
