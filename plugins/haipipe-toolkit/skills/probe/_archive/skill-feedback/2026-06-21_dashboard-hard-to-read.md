---
status: fixed
created: 2026-06-21
context: general (project-level dashboard render for examples/ProjB-PhyTrait-OpioidRx; no active .probe-console.yaml)
fixed_in: "4.3.0"
---

Reporter (JL): 我感觉这个结果很难读。

Trigger: ran `/haipipe-probe` (no-args / project dashboard) on ProjB-PhyTrait-OpioidRx.
The render had 5 stacked sections plus a 5-row drift table plus a 5-row arm
table. The dashboard output reads as too dense / too many tables for a "what is
the status" glance.

Fix: trim the no-args dashboard to a short glance (one summary line + one
status line per probe + a single drift flag), and push the full per-arm drift
table behind an explicit `/haipipe-probe status P.0605` or `gather` call rather
than emitting it on the bare dashboard. Decide the cut in a feedback/console.md
revision pass.
