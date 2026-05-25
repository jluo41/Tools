---
name: meal-cam-logger
description: "Log meals in real time from a webcam or IP camera. Opens a capture loop, asks Claude vision what food is visible in each frame, dedupes, and writes each eating session to a standalone Markdown file. Use when the user says start meal cam, log my meal, watch me eat, 记录我吃的, or /meal-cam-logger."
---

Skill: meal-cam-logger
======================

Live meal logging. The user turns on a camera, starts eating, and this skill
watches the video stream, identifies food as it appears, and writes each
detection to a per-session Markdown file under `_WorkSpace/6-EndpointStore/
mealcam_logs/`.

Trigger phrases:
  /meal-cam-logger
  "start meal cam"
  "log my meal"
  "watch me eat"
  "记录我吃的"

---

## Overview

Three phases:

1. **Start** — confirm camera source (built-in webcam / RTSP URL), capture
   interval (default 5s), and output directory. Launch the capture loop as
   a background process.
2. **Monitor** — loop grabs one frame per interval, asks Claude vision what
   food is visible, dedupes against the last detection, writes / rewrites
   the session's Markdown file on each new detection.
3. **Stop** — user says "stop meal cam" → kill the loop → read the session
   Markdown file and summarise.

---

## Phase 1 — Start

Ask the user once:

> "Which camera? **[1] built-in webcam**  [2] IP camera (paste RTSP URL)"
>
> "Capture interval? (default **5s** — lower = more accurate but more API
> calls)"

Defaults are fine if they just say "go" — use built-in webcam, 5s interval.

Then launch the loop in the background:

```bash
cd /home/jluo41/WellDoc-SPACE
source .venv/bin/activate && source env.sh
mkdir -p _WorkSpace/6-EndpointStore/mealcam_logs
nohup python3 Tools/plugins/health/skills/meal-cam-logger/scripts/meal_cam_loop.py \
    --source 0 \
    --interval 5 \
    --output-dir _WorkSpace/6-EndpointStore/mealcam_logs \
    > /tmp/meal_cam.log 2>&1 &
echo $! > /tmp/meal_cam.pid
```

Confirm it's running:

```bash
sleep 2 && cat /tmp/meal_cam.log | tail -5
```

Tell the user: "📷 Meal cam is on. Just eat — I'll write down what I see."

---

## Phase 2 — Monitor

While the loop runs, the user may ask mid-session:
- **"what have I eaten so far?"** → `tail -20 /tmp/meal_cam.log` or `cat`
  the current session file, then summarise.
- **"skip that last one"** → pop the last entry from the in-memory list
  and rewrite the session file. (Currently requires manual edit of the
  `.md` — noted as a TODO.)
- **"pause"** → `kill -STOP $(cat /tmp/meal_cam.pid)`; **"resume"** →
  `kill -CONT`.

The loop itself handles:
- Frame capture (OpenCV `VideoCapture`, supports int index or RTSP URL).
- Vision call to Claude (Anthropic SDK, `claude-sonnet-4-6` default).
- Dedupe: skip frame if detected food is the same as the previous detection
  (string match on normalized food label).
- Rewrite `mealcam_logs/meal-{YYYY-MM-DD}-{HHMM}.md` on each new detection
  (full-file rewrite keeps the logic simple and avoids partial-write bugs).

---

## Phase 3 — Stop

When user says "stop meal cam" / "end meal" / "done eating":

```bash
kill $(cat /tmp/meal_cam.pid) && rm /tmp/meal_cam.pid
```

Then find the current session file and summarise:

```bash
ls -t _WorkSpace/6-EndpointStore/mealcam_logs/*.md | head -1 | xargs cat
```

Present to the user:

> "Logged this session (saved to meal-2026-04-19-1204.md):
>  • 12:04 salad with grilled chicken
>  • 12:09 sourdough bread
>  • 12:18 black coffee
>  Duration: 24 min. 3 unique foods from 6 detections."

---

## Markdown output format

Written to `_WorkSpace/6-EndpointStore/mealcam_logs/meal-{YYYY-MM-DD}-{HHMM}.md`.
One file per eating session; `HHMM` is the session start time.

```
# 2026-04-19

- **Start:**    12:04
- **End:**      12:28
- **Duration:** 24 min

## Foods

- 12:04  salad with grilled chicken
- 12:09  sourdough bread
- 12:18  black coffee
- 12:22  apple
```

The file is rewritten in full on each new detection (start/end/duration
stay in sync without append-tracking).

---

## Error Handling

- **Camera not found** — OpenCV returns no frames. Tell the user to check
  that no other app is holding the webcam (e.g. Zoom, browser).
- **API rate limit** — back off: double the interval and warn the user.
- **No food in frame** — vision returns `none`; do not write a bullet,
  just continue.
- **Output dir missing** — script auto-creates with `mkdir -p`; no manual
  setup needed.

---

## Privacy note

Frames are sent to the Anthropic API. Tell the user this up front on first
run. If they want fully local inference, point them at DeepCamera + a local
VLM (Qwen-VL / LLaVA) — not in scope for this skeleton.
