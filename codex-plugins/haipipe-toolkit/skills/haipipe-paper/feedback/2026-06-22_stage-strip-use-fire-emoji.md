---
date: 2026-06-22
status: resolved
source: user
scope: orchestrator / stage strip
---

# Stage strip: use fire emoji for current stage, not play button

The stage strip currently marks the active stage with ▶️ (play button).
User prefers 🔥 (fire) instead — it is more visually distinct and conveys
active work energy better than ▶️.

Change: replace ▶️ with 🔥 in the stage strip for the current-stage marker.

Applies to:
- The strip line itself (e.g. `seed ✅  pitch 🔥  claims ⬜  ...`)
- The titled top rule label (e.g. `── 📄 paper · claims 🔥 ───`)
- The stage-strip.sh helper (if it exists)
- All stage/enter skills that render the closing block
