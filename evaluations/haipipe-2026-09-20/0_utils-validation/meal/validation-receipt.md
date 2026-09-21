# Meal-cam fresh-context validation

Executed production meal_cam_loop.py and EpisodeTracker with deterministic dependency substitutes. No repository source changes.

## Result

27 / 27 assertions passed.

## Scope

Real: bash launch/identity/pause/stop commands copied verbatim from current SKILL; OS signals; production capture loop, grouping, render, finalization, cleanup dispatch. Start paths restored in separate shell invocations.

Substituted: cv2 capture/color/JPEG (no actual image), BiteDetector event outputs (frames 1 and 31, or none), Anthropic client label response. Socket connections disabled; clean child environment omitted credentials. No camera, model downloads, network, API, or package installation.

Unverified: real camera opening/permissions/backend behavior; MediaPipe initialization/model downloads/detection accuracy/cooldown; genuine JPEG encoding; actual Anthropic authentication, network, responses, error behavior, latency and billing. Linux/Windows were not run.

## Checks

- PASS meal started
- PASS meal progress
- PASS one identification for repeated bites
- PASS pause suspends capture and receipt
- PASS meal final receipt
- PASS meal resources closed
- PASS meal stale PID rejected
- PASS duration includes pause
- PASS empty started
- PASS empty startup receipt
- PASS empty final receipt
- PASS empty resources closed
- PASS empty stale PID rejected
- PASS empty finalized without identification
- PASS independent-a started
- PASS independent-b started
- PASS independent controls and receipts
- PASS skip affects only selected session
- PASS independent-a final receipt
- PASS independent-a resources closed
- PASS independent-a stale PID rejected
- PASS other session remains running
- PASS independent-b final receipt
- PASS independent-b resources closed
- PASS independent-b stale PID rejected
- PASS final outputs remain independent
- PASS sources unchanged

## Commands and artifacts

Run: `python3 /tmp/mealcam-fresh-20260920/validate.py` (requires process inspection allowed by sandbox).

All exact shell commands, stdout/stderr, audit events and JSON results are alongside this receipt. Skill bash blocks saved as start.sh, identity.sh, stop.sh.

## Friction

Environment: sandbox denied ps before execution. Documented process identity checks at SKILL.md:153-160 and start timestamp capture at SKILL.md:84 need process inspection; run used an auto-reviewed escalation. This is an environment limit, not a demonstrated script defect.

No functional friction in the exercised lifecycle paths.

## Session files

- meal: /private/tmp/mealcam-fresh-20260920/receipts/meal-2026-09-20-173745-606276.md; log /tmp/meal-cam.JQYvEi/run.log
- empty: /private/tmp/mealcam-fresh-20260920/receipts/meal-2026-09-20-173750-725825.md; log /tmp/meal-cam.P7fmLz/run.log
- independent-a: /private/tmp/mealcam-fresh-20260920/receipts/meal-2026-09-20-173753-974683.md; log /tmp/meal-cam.GbBZyo/run.log
- independent-b: /private/tmp/mealcam-fresh-20260920/receipts/meal-2026-09-20-173756-048094.md; log /tmp/meal-cam.tE6Azx/run.log
