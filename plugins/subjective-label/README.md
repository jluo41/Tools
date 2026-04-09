subjective-label plugin
=======================

A general-purpose skill for subjective text annotation.

Captures a human's personal annotation criteria through interactive
gallery generation, then applies that gallery using a weak model at scale.

Core idea: define the criteria ONCE (with a strong model + human interaction),
then annotate EVERYTHING cheaply (with a weak model).


Two Phases
----------

  Phase 1 — Gallery Generation
    Small sample + human interaction -> labeled examples + guideline
    Run once. Takes 20-40 minutes. Human does the thinking here.

  Phase 2 — Inference
    Full corpus + weak model + gallery -> annotations at scale
    Automated. Cheap. Human only spot-checks.


Skills
------

  /subjective-label           main entry point (this skill)


Use Cases
---------

  - ICU transcript nudge detection  (WCC project)
  - Customer review quality rating
  - Message tone classification
  - Any task where the annotation criterion is one person's judgment


Design
------

  See: cc-archive/design/subjective-label/
