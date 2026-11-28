---
title: checks know live items
date: 2026-11-27 20:50
work: [s72, s11, s12, s13, s14, s15]
aim: "plugins/haipipe-toolkit/checks/run.py passes on what the server already shows: a studio-views.json item may be a live workbench page (`url`), and a type topic that carries its own generator (s72's build_type_pages.py) is compared with that generator instead of type_requirements.py."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2050_checks_know_live_items.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/checks/skills/studio/manifest.py
    what: "a fourth binding, url: it starts with /_board/workbench? and its path= is a real file or folder inside the SPACE"
  - do: edit
    path: plugins/haipipe-toolkit/checks/skills/studio/freshness.py
    what: "a type topic with its own build_type_pages.py is compared with its built(True), in memory"
  - do: edit
    path: plugins/haipipe-toolkit/checks/ (tests/test_studio_checks.py, README.md)
    what: a test for each; the two Coverage rows say so
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2050_checks_know_live_items.md
  - plugins/haipipe-toolkit/checks/skills/studio/manifest.py
  - plugins/haipipe-toolkit/checks/skills/studio/freshness.py
  - plugins/haipipe-toolkit/checks/tests/test_studio_checks.py
  - plugins/haipipe-toolkit/checks/README.md
---

# checks know live items

## Prompts

- **20:40** (a peer session reported after the hai-studio to hai-studio rename: checks/run.py fails on s11-s14 bindings and on s72's generated pages)
- **20:45** go

## Check

- checks/run.py --target on s72, s11, s13, s15 and s71: every line PASS, exit 0 (before: s11-s14 "expected one path, folder or block binding", s72 "out of date; regenerate with type_requirements.py").
- A url outside the route, to a missing page or leaving the SPACE fails (test); a hand-edited page of a type with its own generator fails (test). checks tests: 31 pass.
- checks/run.py --target on the whole b17 Block: every line PASS, exit 0.
- No server code changed; no restart.

## Summary

The checks accept a live-page item and use a type topic's own generator; s72 and its five instances pass.
