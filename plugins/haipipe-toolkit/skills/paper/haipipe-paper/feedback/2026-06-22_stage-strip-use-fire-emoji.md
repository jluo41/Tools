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

## Refinement 2026-06-24 (REOPENED then resolved): split frontier vs session

User refined the meaning. The strip is OVERALL PROGRESS (where the paper sits in
its lifecycle), but 🔥 reads as "actively burning / being worked now", which is a
SESSION semantic. The two can differ (frontier = `write/edit`, but this session
looped back to tune `minimap`). So 🔥 was the wrong glyph for the progress marker.

New two-marker scheme, TWO markers in TWO places (chosen via options; user picked
🚀 for the strip, kept 🔥 for the session). Clarified same day: 🔥 lives in the
closing-block TOP-RULE LABEL, not in the strip.
- 🚀 = current OVERALL frontier IN THE STRIP (replaces 🔥). Calm "you-are-here";
  user picked 🚀 over ▶️/📍/🔵. The strip never shows 🔥.
- 🔥 = the stage this session is actively working, shown in the closing-block
  TOP-RULE LABEL (`📄 paper · <current_layer> 🔥`). So a closing block = a 🔥 label
  above a 🚀 strip. When the session loops back to a done stage, the label reads
  `· minimap 🔥` while the strip shows the real frontier `write/edit 🚀`.
- The helper also accepts an optional 2nd arg to mark a stage 🔥 inside a BARE
  strip (no label), e.g. the enter dashboard.
- ✅ done/confirmed, ⬜ not reached (unchanged).

Applied 2026-06-24:
- `paper/ref/stage-strip.sh`: current marker 🔥 -> 🚀; added optional 2nd arg
  `session-stage` that marks that stage 🔥 when it differs from current_layer;
  header comments updated.
- `paper/haipipe-paper/SKILL.md` (orchestrator): Stage Strip section + closing-block
  label `📄 paper · <layer> 🚀` + examples updated; documents the 🔥 session marker.
- `paper/0-enter/haipipe-paper-enter/SKILL.md`: example strips 🔥 -> 🚀.
- Probe skill (`probe/haipipe-probe/ref/stage-strip.sh`): NO change needed; it
  already uses ▶️ (calm, disk-derived), not 🔥.

STILL OPEN (minor doc sweep): other paper sub-skill SKILL.md files that hardcode
an example strip with 🔥 in their closing-block illustration should be swept to 🚀
for doc consistency (functionally they already render via the helper, so live
output is correct). Status set back to resolved once that sweep lands.
