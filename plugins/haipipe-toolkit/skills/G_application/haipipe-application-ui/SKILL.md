---
name: haipipe-application-ui
description: "UI specialist of the haipipe-application family. STUB. Will be an outer-loop session producing UI sketches / specs from the project's K/W knowledge base. Reads K_knowledge + W_wisdom from E_insight, can trigger /haipipe-insight ask, writes to examples/<project>/applications/ui/. NEVER writes back to insights/. Trigger: ui, sketch, mockup, screen, layout, wireframe, /haipipe-application ui."
argument-hint: '[--audience designer|dev] [--project <path>] [--slug <slug>] "<intent>"'
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-05-31"
---

Skill: haipipe-application-ui   (STUB)
=======================================

**Status: STUB.** This specialist mirrors the structure of
`haipipe-application-message` but is not yet filled out for the UI case.

Defer to the sibling SKILL files for the architecture:
  - `../haipipe-application/SKILL.md`               (umbrella + Phase 0-8)
  - `../haipipe-application/ref/audience-requirements.md`
  - `../haipipe-application/ref/application-input-contract.md`
  - `../haipipe-application-message/SKILL.md`       (full reference impl)

When a real UI-creation request arrives, expand this stub by following
the message-specialist's structure with these UI-specific changes:

```
Audiences:        designer (visual, concrete, with ASCII sketch)
                  dev      (precise interface + behavior spec)

Output dir:       applications/ui/<slug>/
                   ├── sketch.md          (ASCII layout + annotations)
                   └── spec.md            (component contract for dev)

Schema additions: include `screens: [<name1>, <name2>]` in frontmatter
                  include `interactions: [<event → effect>]`

Length budget:    designer ≤ 300 words + ASCII sketch
                  dev      ≤ 500 words + interface block (typed)
```


Risk profile
-------------

WRITES new files under `applications/ui/<slug>/`. May trigger
`/haipipe-application ask`. NEVER writes to insights/.


Specialist tail
----------------

```
status:    stub_invoked | (post-expansion: ok | blocked | failed | gap_unresolved)
summary:   "UI specialist is a stub; expand following message specialist pattern"
next:      Implement following haipipe-application-message/SKILL.md
```
