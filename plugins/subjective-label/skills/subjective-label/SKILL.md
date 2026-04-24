---
name: subjective-label
description: "Multi-agent panel for subjective text annotation. One researcher + an AI panel (3-5 persona labelers + moderator + analyzer + validator) converge on a labeling guideline through iterative disagreement analysis, validated against public-dataset human consensus (κ). Use when the user wants to label texts on a subjective dimension (humanity, empathy, moral framing, emotion, stance, etc.), run a labeling panel, validate a gallery against public datasets, or says /subjective-label."
---

Skill: subjective-label (router)
================================

Entry point for the subjective-label plugin. Routes the user to the correct sub-skill.

Invocation:  /subjective-label <command> [args]


Sub-commands
------------

  init      Create project, define topic + boundaries via dialogue
  iterate   Run one iteration: probe → panel labels → analyze → surface
  validate  Benchmark current gallery against public dataset (κ vs human)
  scale     Batch-label full dataset using the converged gallery
  status    Show project state, κ trajectory, gallery stats, next step

  (no sub-command) Show this menu and ask what the researcher wants.


Routing
-------

Parse $ARGUMENTS for the sub-command token. Then invoke the matching sub-skill:

  init      ->  /sl-init
  iterate   ->  /sl-iterate
  validate  ->  /sl-validate
  scale     ->  /sl-scale
  status    ->  /sl-status


Core Model
----------

The researcher talks only to the **Moderator** agent. All other work happens
behind Moderator:

  Researcher <---> Moderator --+--> Boundary Prober
                               |--> Labeler Panel (3-5 personas)
                               |--> Disagreement Analyzer
                               |--> Gallery Keeper
                               +--> Validator

See ref/ref-architecture.md for the full protocol.


Key Principle
-------------

Disagreement is signal, not noise. When the panel disagrees, the Analyzer
decides whether it's (a) boundary case → refine guideline,
(b) rule ambiguity → add tie-breaker, (c) novel pattern → extend label
schema, or (d) pure noise → ignore. Only (a)/(b)/(c) are surfaced to the
researcher.

Convergence = agent-panel κ matches human-panel κ ceiling on a public dataset.
