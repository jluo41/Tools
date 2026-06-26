haipipe-paper — Feedback Digest
===============================

Generated: 2026-06-26
Source: all feedback/ inboxes under skills/paper/

Summary
-------

  58 total items across 12 skills
  24 open  ·  31 fixed  ·  3 other (resolved/unset)

Open Items by Skill (need attention)
-------------------------------------

  haipipe-paper-display (10 open) ............. heaviest inbox
    display-must-plan-then-route-to-task-probe-not-adhoc-plot
    display-ascii-contact-sheet-of-all-displays
    display-gallery-show-section-and-subsection-names
    display-must-follow-predefined-display-unit-content
    display-pdf-order-follow-minimap-narrative
    display-per-unit-venue-narrative-selfcheck-subagent
    display-plan-boilerplate-too-heavy
    display-review-loop-agent-and-ascii-preview
    gallery-owns-sizing-not-unit-floattex
    persist-user-display-comments-into-float-tex

  haipipe-paper-minimap (7 open)
    bake-advisor-feedback-into-minimap
    claim-tags-show-content-not-index
    drop-coverage-check-crosswalk
    minimap-should-be-sentence-level-spine-not-job-table
    minimap-title-short-fit-venue
    narrative-notes-lean-no-verb-role-prefix
    supplement-sync-with-real-supplement

  haipipe-paper [orchestrator fallback] (5 open)
    construction-is-first-class-beat-probe-via-subagent
    every-stage-must-compile-readable-pdf
    every-stage-must-illuminate-and-elicit-taste
    probe-dispatch-skipped-buffer
    probe-should-auto-buffer-during-lifecycle

  haipipe-paper-claims (2 open)
    claims-hunted-gaps-before-evidence-inventory-and-overrode-framing
    claims-needs-claim-zero-data-description

  haipipe-paper-display-figure (1 open)
    no-baked-text-caption-in-figure

  haipipe-paper-display-diagram (1 open)
    vector-render-elbow-connectors-and-icons

  components/compile (1 open)
    preview-build-not-in-compile-sh

Fixed Items (resolved, kept as history)
---------------------------------------

  haipipe-paper-pitch .............. 8 fixed
  haipipe-paper [orchestrator] ..... 8 fixed (incl 1 resolved)
  haipipe-paper-lifecycle .......... 4 fixed
  haipipe-paper-claims ............. 4 fixed
  haipipe-paper-narrative .......... 3 fixed
  haipipe-paper-display ............ 1 fixed
  haipipe-paper-enter .............. 1 fixed

Coverage: Skills with Feedback Folders
--------------------------------------

  ✅ has feedback/   12 skills (with items)
  ✅ has feedback/   37 skills (newly created, empty — ready for capture)
  ── total           49 paper sub-skills covered

Hotspots
--------

  🔥 haipipe-paper-display   10 open items — the display lifecycle (plan,
     route to task, review loop, gallery, sizing, comments) is the most
     complained-about area. Most items cluster around "display should plan
     then route to task/probe, not ad-hoc plot" and "persist user comments."

  🔥 haipipe-paper-minimap   7 open items — minimap format (sentence-level
     vs job-table), claim tags, and supplement sync are the main themes.

  ⚠️  haipipe-paper [orch]   5 open cross-cutting items — compile-every-stage,
     illuminate-every-stage, and probe-buffering during lifecycle are
     spine-wide rules that need wiring into every stage.

Next Actions
------------

  1. Triage display items — several may be addressed by the new display
     renderer family (diagram/figure/table/illustration). Close resolved ones.
  2. Minimap format — decide sentence-level spine vs job-table once.
  3. Cross-cutting wiring — the 5 orchestrator items need per-stage enforcement.
  4. Run `/haipipe-paper feedback list` periodically to track progress.
