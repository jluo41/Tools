# Paper Skill Wiki

Single source of truth for all paper skill conventions, architecture, and protocols. Numbered for reading order. Update topics in place when conventions evolve.

## Index

**Foundations**
0. [Evidence Principles (总纲)](00-evidence-principles.md) -- the root goal (trustworthy shared memory) + the four principles (land-at-home, review-on-write, layered orders, trim-ceremony-not-principle) every evidence rule derives from

**Design conventions**
1. Focus Strip Markers -- ABSORBED into haipipe-paper/SKILL.md Closing Block (2026-07-03); numbering gap kept on purpose
2. [Comment Convention and Lifecycle](02-comment-lifecycle.md) -- actor ids (never hardcode), two formats (blockquote + tex), anchoring, lifecycle (move to _LOG on resolve), round invariants

**System architecture**
3. [Paper Lifecycle](03-paper-lifecycle.md) -- lifecycle stages, maturity ladder, stage ordering
4. [Lifecycle Map](04-lifecycle-map.md) -- stage routing, command map, skill dispatch
5. [Paper Dashboard](05-paper-dashboard.md) -- how to derive the dashboard from disk
6. [Paper Skill Structure](06-paper-skill-structure.md) -- skill folder layout and naming conventions
7. [Paper Rounds](07-paper-rounds.md) -- dated work rounds, discussion/decisions/todo/applied

**Operational protocols**
8. [Stage Gate](08-stage-gate.md) -- exit criteria + confirm-before-advance gate
9. [Stage Illuminate](09-stage-illuminate.md) -- illuminate + elicit taste before drafting
10. Stage Strip renderer -- MOVED to haipipe-paper/stage-strip.sh (2026-07-03, co-located with the Closing Block spec); numbering gap kept on purpose
11. [Delivery Need](11-delivery-need.md) -- need record schema + backfill protocol
12. [Evidence Routing](12-evidence-routing.md) -- \needprobe macro + paper/evidence boundary
13. [TeX Quality](13-tex-quality.md) -- self-contained compilable tex with Pn.Sm tags
