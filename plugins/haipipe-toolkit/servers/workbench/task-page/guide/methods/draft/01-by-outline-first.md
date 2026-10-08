By outline first
================

One draft method card. The Page workbench shows it in the shared Guide › Method,
under Draft methods; its papers are the rows of `../../../related/papers.md` whose
`group` is `by outline first`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: Draft: What will the Page say, and why?
move: Settle the Page's parts, paragraphs and Bullets, each with one role, before any
  sentence is drafted; the prose is written from the plan, never the plan from the
  prose.
comes from: Flower & Hayes 1981, writing as goal-directed processes; Kellogg 1988,
  outline against rough draft
reads: the Context record · the Page's brief
returns: a versioned plan: parts, paragraphs, Bullets and their roles
test now: T0 covered
test in use: T4 independent


What the literature says
------------------------

rationale: Writing is a set of distinct thinking processes (planning, translating ideas
  into text, reviewing) that the writer's own goals organize, and the goals grow as the
  writer composes [Flower 1981]. An outline is one way to do the planning first, so that
  translating does not have to plan at the same time [Kellogg 1988].
context: Composition research on expert and novice writers [Flower 1981]; an experiment
  comparing an outline strategy with a rough-draft strategy as ways to ease attentional
  overload while writing [Kellogg 1988].
steps: 1. Freeze the brief: what the Page must do and for whom. 2. Name the parts and
  their paragraphs. 3. Write each paragraph's Bullets, one point each, with one role. 4.
  Have the plan approved before prose is written.
strengths: The plan can be read, reviewed and changed before any prose exists, and a
  change to the argument is a change to one Bullet (ours).
limitations: A writer's goals change while composing [Flower 1981], so a fixed plan can
  miss what the drafting finds; the plan is versioned, not frozen (ours).


Applied to AI
-------------

agent: A structure agent writes the plan from the Context record and the brief; it does
  not draft prose.
steps: 1. Read the Context record. 2. Write parts, paragraphs and Bullets with roles. 3.
  Name every Evidence Item a Bullet needs. 4. Stop for the person's approval.
returns: draft/<stem>-draft-v<G>.<S>.md, its Structure table, approved: ⬜.
verify: The person approves the plan; after adoption, Folder health checks that every
  Bullet is realized by one sentence (T0).
risk: A model asked for an outline may return headings rather than claims, so the plan
  reads as a table of contents (ours).
evidence on ai: No study tests an agent's outline-first Page against draft-first writing
  (ours).
skill: haipipe-page-structure
