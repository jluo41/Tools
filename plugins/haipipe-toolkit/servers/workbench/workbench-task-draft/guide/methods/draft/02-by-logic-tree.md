By logic tree
=============

One draft method card. The Page workbench shows it in the shared Guide › Method,
under Draft methods; its papers are the rows of `../../../related/papers.md` whose
`group` is `by logic tree`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: Draft: What will the Page say, and why?
move: Draw the Page's claim at the left, the reasons it rests on beside it, and the Bullets
  as leaves, each its own row; a Bullet that hangs from no reason is cut or moved.
comes from: Toulmin 2003, claim, grounds and warrant
reads: the approved plan · its Bullets and roles
returns: the Page's RoadMap drawing: claim, reasons, Bullets
test now: T1 logic
test in use: T4 independent


What the literature says
------------------------

rationale: An argument is a claim supported by grounds, with a warrant that says why the
  grounds support the claim, and a qualifier and rebuttal that bound it; the layout
  makes each part visible [Toulmin 2003].
context: Argumentation theory and the study of how a field's norms justify an assertion
  [Toulmin 2003].
steps: 1. Write the claim the Page establishes. 2. Under it, the one to three reasons it
  rests on. 3. Split each reason until each leaf is one Bullet. 4. Put the Bullets on
  one row and colour each by its evidence.
strengths: Reading the boxes alone tells what the Page argues, so a missing or misplaced
  Bullet shows before the prose is read (ours).
limitations: A tree shows support, not the order a reader meets the points; the plan
  keeps the order and the tree the logic (ours).


Applied to AI
-------------

agent: The draw-logic-tree skill writes the first drawing from the plan; after that the
  person edits the drawing, which is the source.
steps: 1. Write the logic as an indented outline. 2. Draw it on the Page's RoadMap
  canvas. 3. Run the scene check after every edit.
returns: studio/<stem>-roadmap.excalidraw.
verify: The scene check fails on a plan Bullet no box names and on Bullets that do not
  share a row (T1).
risk: An agent may invent a reason to fill a branch; a missing Bullet goes back to
  Structure, never into the drawing alone (ours).
evidence on ai: No study tests agent-drawn argument trees for Pages (ours).
skill: draw-logic-tree
