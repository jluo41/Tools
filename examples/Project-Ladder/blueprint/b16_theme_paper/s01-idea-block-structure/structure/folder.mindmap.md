---
mindmap: 1
title: Idea-〈name〉/
---

# Idea-〈name〉/

- jNN_〈job〉/ <!-- jobs -->
  One candidate Idea per Job.
  - tNN_〈task〉/ <!-- tasks -->
    A bounded assessment or deliverable.
    - assessments/ <!-- assessments -->
      Authored assessment receipts for the bounded question.
    - runs/ <!-- runs -->
      Commissioned Runs and their Results.
    - tNN_〈task〉.md <!-- task-face -->
      Task type, question and workflow.
  - cards/ <!-- cards -->
    Canonical records for this one candidate Idea.
    - venue-fit/ <!-- venue-fit -->
      Candidate target readings.
    - direction.yaml <!-- direction -->
      The candidate's bounded question and context.
    - iNN_〈idea〉.yaml <!-- idea-card -->
      Exactly one canonical Idea Card, with stable identity.
    - test-matrix.yaml <!-- test-matrix -->
      Assessments and decision criteria for this Idea.
  - bundle/ <!-- bundle -->
    - evidence-bundle.yaml <!-- evidence-bundle -->
      Pointers to original evidence owned by Work or Discovery.
  - workflow/ <!-- workflow -->
    Semantic receipts and immutable human decisions.
  - projection/ <!-- projection -->
    - paper-ideation-sync.yaml <!-- sync -->
      Revision-pinned projection of the Idea's records.
  - handoff/ <!-- handoff -->
    - paper-ideation.yaml <!-- handoff-card -->
      Destination pointers after explicit selection; it does not create a Paper.
  - jNN_〈job〉.md <!-- job-face -->
    Job purpose, requirements, Tasks and source links.
  - ideation.yaml <!-- job-index -->
    kind: ideation-unit; layout: idea-job; this candidate's identity and source paths.
- sNN-〈topic〉/ <!-- studio -->
  A design question at the level that uses its output.
  - sNN-〈topic〉.md <!-- topic-face -->
    Its question, decisions and source links.
- related/ <!-- related -->
  External material and references, linked without duplicating authority.
- delivery/ <!-- delivery -->
  Block-owned outputs, retaining Job and Task identity.
- trace/ <!-- trace -->
  Plans, prompts, changes and verification.
- board.md <!-- board -->
  The Block face; its own topic groups and navigation.
- ideation.yaml <!-- index -->
  Pointer-only index; each Job owns its canonical Idea Card.
