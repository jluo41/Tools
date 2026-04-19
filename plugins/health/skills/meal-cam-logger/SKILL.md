---
name: meal-cam-logger
description: "Log meals in real time from a webcam or IP camera. Opens a capture loop, asks Claude vision what food is visible in each frame, dedupes, and appends bullets to today's LogSeq journal. Use when the user says start meal cam, log my meal, watch me eat, 记录我吃的, or /meal-cam-logger."
---

Skill: meal-cam-logger
======================

Live meal logging. The user turns on a camera, starts eating, and this skill
watches the video stream, identifies food as it appears, and writes each
detection as a time-stamped bullet in today's LogSeq journal.

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
   interval (default 5s), and journal target. Launch the capture loop as a
   background process.
2. **Monitor** — loop grabs one frame per interval, asks Claude vision what
   food is visible, dedupes against the last detection, appends a bullet to
   today's LogSeq journal under a `Meal-Cam-Records` block.
3. **Stop** — user says "stop meal cam" → kill the loop → summarize what got
   logged this session.

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
nohup python3 Tools/plugins/health/skills/meal-cam-logger/scripts/meal_cam_loop.py \
    --source 0 \
    --interval 5 \
    --journal /home/jluo41/LogSeq-Me/journals \
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
- **"what have I eaten so far?"** → `tail -20 /tmp/meal_cam.log` and summarize.
- **"skip that last one"** → remove the last bullet from today's journal file.
- **"pause"** → `kill -STOP $(cat /tmp/meal_cam.pid)`; **"resume"** →
  `kill -CONT`.

The loop itself handles:
- Frame capture (OpenCV `VideoCapture`, supports int index or RTSP URL).
- Vision call to Claude (Anthropic SDK, `claude-opus-4-7` or `claude-sonnet-4-6`).
- Dedupe: skip frame if detected food is the same as the previous detection
  (string match on normalized food label).
- Append bullet to `journals/YYYY_MM_DD.md` under `[[Meal-Cam-Records]]`,
  creating the heading on first write of the day.

---

## Phase 3 — Stop

When user says "stop meal cam" / "end meal" / "done eating":

```bash
kill $(cat /tmp/meal_cam.pid) && rm /tmp/meal_cam.pid
```

Then read today's journal and summarize **only the Meal-Cam-Records block**:

> "Logged this session:
>  • 12:04 salad with grilled chicken
>  • 12:09 sourdough bread
>  • 12:18 black coffee
>  Total detections: 6 (3 unique foods). Full log in today's journal."

---

## LogSeq output format

Appended to `/home/jluo41/LogSeq-Me/journals/YYYY_MM_DD.md`:

```
- [[Meal-Cam-Records]]
	- HH:MM <food label> #meal-cam
	- HH:MM <food label> #meal-cam
```

If the heading already exists for today, append children under it; otherwise
create the heading at the bottom of the file.

---

## Error Handling

- **Camera not found** — OpenCV returns no frames. Tell the user to check
  that no other app is holding the webcam (e.g. Zoom, browser).
- **API rate limit** — back off: double the interval and warn the user.
- **No food in frame** — vision returns `none`; do not write a bullet,
  just continue.
- **LogSeq journal missing** — create `journals/YYYY_MM_DD.md` with an empty
  first line before appending.

---

## Privacy note

Frames are sent to the Anthropic API. Tell the user this up front on first
run. If they want fully local inference, point them at DeepCamera + a local
VLM (Qwen-VL / LLaVA) — not in scope for this skeleton.
