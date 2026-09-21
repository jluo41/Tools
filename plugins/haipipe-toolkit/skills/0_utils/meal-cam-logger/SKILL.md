---
name: meal-cam-logger
description: "Log a meal session from a webcam or IP camera using local bite detection and Anthropic food identification. Use when the user says start meal cam, log my meal, watch me eat, 记录我吃的, or /meal-cam-logger."
metadata:
  version: "0.3.0"
  last_updated: "2026-09-20"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: meal-cam-logger
======================

Each meal session is one **Run**. Start, Monitor, and Stop are Steps within
that Run. The process writes one uniquely named Markdown receipt for the Run
under `_WorkSpace/6-EndpointStore/mealcam_logs/` (or the output directory
the user chooses).

Trigger phrases:
  /meal-cam-logger
  "start meal cam"
  "log my meal"
  "watch me eat"
  "记录我吃的"

---

## Before starting

- Explain the data flow before starting: MediaPipe examines sampled frames
  locally. Only the JPEG from the first detected bite in each episode is sent
  to the Anthropic API for food identification. Images may include the user
  and their surroundings. Frames are not written as image files by this
  script; the selected JPEG is handled in process memory for the vision call.
- `ANTHROPIC_API_KEY` must already be available in the local process
  environment. Do not ask the user to paste an API key into chat or put it in
  the command, script, or log.
- MediaPipe may download its public hand and face landmark model files on
  first use and cache them locally. No frames are sent to MediaPipe's model
  download host.
- The runtime needs Python packages `opencv-python`, `anthropic`, and
  `mediapipe`, plus access to the selected camera. Do not claim it started
  until the process is still running and its log shows the session file.

---

## Start Step

Ask whether to use the built-in webcam (default source `0`) or a source the
user has configured locally, such as an IP camera or video file. Do not ask
the user to paste a credential-bearing RTSP URL into chat. The script reads
`MEAL_CAM_SOURCE` from the local environment when set; otherwise it uses
`0`. Ask whether the user wants to change the capture rate or output
directory. Defaults are 10 frames per second, a 3-second bite cooldown, a
45-second maximum gap within one episode, and the repository's
`_WorkSpace/6-EndpointStore/mealcam_logs/` directory. The CLI option is
`--fps`; there is no `--interval` option.

Resolve `MEAL_CAM_SKILL_DIR` from the absolute location of this loaded
SKILL.md, following installation symlinks. Choose an absolute
`MEAL_CAM_OUTPUT_DIR` in the target project or the user's chosen location.
Verify that the selected Python (`MEAL_CAM_PYTHON`, default `python3`) has the
packages above. Keep tool location, target output, and private camera source
separate; the target need not contain a toolkit checkout.

Launch the bundled script after setting those paths:

```bash
: "${MEAL_CAM_SKILL_DIR:?Set the absolute directory of the loaded meal-cam skill}"
: "${MEAL_CAM_OUTPUT_DIR:?Set the confirmed absolute output directory}"
MEAL_CAM_SCRIPT="$MEAL_CAM_SKILL_DIR/scripts/meal_cam_loop.py"
MEAL_CAM_OUTPUT="$MEAL_CAM_OUTPUT_DIR"
MEAL_CAM_CONTROL_DIR="$(mktemp -d /tmp/meal-cam.XXXXXX)"
MEAL_CAM_LOG="$MEAL_CAM_CONTROL_DIR/run.log"
MEAL_CAM_PID_FILE="$MEAL_CAM_CONTROL_DIR/run.pid"

nohup "${MEAL_CAM_PYTHON:-python3}" "$MEAL_CAM_SCRIPT" \
    --fps 10 \
    --cooldown-sec 3 \
    --max-gap-sec 45 \
    --output-dir "$MEAL_CAM_OUTPUT" \
    > "$MEAL_CAM_LOG" 2>&1 &
MEAL_CAM_PID=$!
printf '%s\n' "$MEAL_CAM_PID" > "$MEAL_CAM_PID_FILE"
ps -p "$MEAL_CAM_PID" -o lstart= > "$MEAL_CAM_CONTROL_DIR/process-start.txt"
printf '%s\n' "$MEAL_CAM_SCRIPT" > "$MEAL_CAM_CONTROL_DIR/script-path.txt"
sleep 2
printf 'PID_FILE=%s\nLOG_FILE=%s\nPID=%s\n' \
    "$MEAL_CAM_PID_FILE" "$MEAL_CAM_LOG" "$MEAL_CAM_PID"
if kill -0 "$MEAL_CAM_PID" 2>/dev/null; then
    tail -n 8 "$MEAL_CAM_LOG"
else
    cat "$MEAL_CAM_LOG"
fi
```

For a different source, configure `MEAL_CAM_SOURCE` through a local mechanism
that is not committed or shared, or pass a non-secret source with `--source`.
Keep camera credentials out of chat, command history, and logs. For a different output
directory, replace `MEAL_CAM_OUTPUT` or set `MEAL_CAM_OUTPUT_DIR`. Keep the
printed PID, PID file, log path, and the `session_file` path from the log
attached to this Run; do not use a shared fixed PID file or infer the session
by listing the newest file, since multiple sessions can run at once.

The script creates the receipt at startup, before bite detection. Confirm the
log says `started` and includes `session_file=...`, and that the process is
still alive. If startup fails, report the failure and do not say the camera
is on. The script's own messages omit the complete camera source. Camera
backend diagnostics may still contain sensitive source details: inspect them
locally and never paste an unfiltered camera log into chat.

---

## Monitor Step

- To check progress, read the exact `session_file` printed by this Run, or
  inspect its log. The Markdown receipt is refreshed atomically when an
  episode or bite count changes.
- Before each control command, restore `MEAL_CAM_CONTROL_DIR` to the exact
  directory printed at startup, then run the identity check below. Shell
  variables do not persist between separate commands. If the process has
  exited or its identity differs, do not signal the stored PID.
- **"What have I eaten so far?"** — read that receipt and summarize the
  episodes. Do not substitute the newest Markdown file from the directory.
- **"Skip that last one"** — on macOS/Linux, send `SIGUSR1` to this Run's PID:
  `kill -USR1 "$MEAL_CAM_PID"` after the identity check. This removes the most recent
  whole episode (including its bite count), not just one bite. Confirm from
  the log that the episode was removed. If there is no episode yet, the
  process reports that nothing was removed. Do not hand-edit the live receipt:
  the process rewrites it from memory. If `SIGUSR1` is unavailable, note the
  correction and apply it to the finalized receipt after stopping.
- **Pause/resume** — on macOS/Linux, use `kill -STOP PID` and `kill -CONT PID`
  with the checked `MEAL_CAM_PID`. These suspend and resume the whole process.
  Elapsed Duration includes paused time. Stop must also send CONT, as below,
  so a suspended process can handle its pending termination.
- Local MediaPipe bite detection runs on sampled frames. The 3-second
  cooldown filters repeated detections, and bites no more than 45 seconds
  apart are grouped into one episode. This heuristic can miss a food change
  within an episode or detect a bite incorrectly; do not present episodes as
  verified foods or exact nutrition data.
- Claude vision is called only on the first detected bite of an episode. Its
  receipt records an **inferred visible-food label**, with multiple candidate
  labels or an abstention. `no_food_visible`, `uncertain`, and `service_error`
  are separate states; none means “nothing was eaten.” A visible-food label
  does not prove consumption, exact ingredients, or nutrition. API failures
  record the error class without storing the frame; there is no automatic
  rate-limit backoff.

### Restore and check this process before a control command

```bash
: "${MEAL_CAM_CONTROL_DIR:?Restore the exact control directory printed at startup}"
MEAL_CAM_PID_FILE="$MEAL_CAM_CONTROL_DIR/run.pid"
MEAL_CAM_LOG="$MEAL_CAM_CONTROL_DIR/run.log"
MEAL_CAM_PID="$(cat "$MEAL_CAM_PID_FILE")"
MEAL_CAM_SCRIPT="$(cat "$MEAL_CAM_CONTROL_DIR/script-path.txt")"
check_meal_cam_process() {
    case "$MEAL_CAM_PID" in ''|*[!0-9]*) return 1 ;; esac
    [ "$MEAL_CAM_PID" -gt 1 ] || return 1
    [ -s "$MEAL_CAM_CONTROL_DIR/process-start.txt" ] || return 1
    [ "$(ps -p "$MEAL_CAM_PID" -o lstart=)" = "$(cat "$MEAL_CAM_CONTROL_DIR/process-start.txt")" ] || return 1
    case "$(ps -p "$MEAL_CAM_PID" -o args=)" in
        *"$MEAL_CAM_SCRIPT"*) return 0 ;;
        *) return 1 ;;
    esac
}
# Execute the requested signal only in this success branch.
if check_meal_cam_process; then
    printf 'Verified meal-cam PID %s; log: %s\n' "$MEAL_CAM_PID" "$MEAL_CAM_LOG"
else
    printf '%s\n' 'No matching live meal-cam process; do not send a signal.'
fi
```

Repeat `check_meal_cam_process` immediately before sending a signal. Keep the
exact session receipt address from startup; the PID check does not replace it.

---

## Stop Step

When the user says "stop meal cam", "end meal", or "done eating", send a
graceful termination signal to the PID from this Run:

```bash
# Use the restored paths and function above in this same shell.
if ! check_meal_cam_process; then
    printf '%s\n' 'No matching live meal-cam process; stop is unconfirmed.'
    exit 1
fi
kill -TERM "$MEAL_CAM_PID"
# SIGTERM remains pending while SIGSTOP has suspended the process.
kill -CONT "$MEAL_CAM_PID" 2>/dev/null || true
MEAL_CAM_WAITED=0
while check_meal_cam_process && [ "$MEAL_CAM_WAITED" -lt 10 ]; do
    sleep 1
    MEAL_CAM_WAITED=$((MEAL_CAM_WAITED + 1))
done
if check_meal_cam_process; then
    echo "Graceful stop has not been confirmed; keep the PID and check the log."
else
    tail -n 12 "$MEAL_CAM_LOG"
fi
```

On SIGTERM, SIGINT, or normal camera end, the script writes a final local end
time, duration, status, and episode list. Read the exact session file from
this Run's log and summarize its contents, including when there were no bite
episodes. Do not claim a final end time until the log shows the process
stopped and the receipt has a final status. A camera read or API request can delay Python signal handling; if the
wait expires, retain the process identity and report stop as pending. A forced
kill, power loss, or crash can leave the last receipt marked `running`; explain that it was not
finalized rather than inventing an end time.

---

## Markdown receipt

Each Run creates a distinct file such as
`meal-2026-09-20-120401-123456.md`. Timestamps are local to the host running
the process. The receipt is written at startup and atomically refreshed; a
graceful stop fills in End, Duration, and final Status. An empty meal still
has a receipt.

```markdown
# 2026-09-20

- **Run ID:** meal-2026-09-20-120401-123456
- **Start:**    12:04:01
- **End:**      12:28:15
- **Duration:** 24 min 14 sec
- **Status:**   stopped

## Episodes

- **Episode #1:** 12:04:32–12:05:17 · 4 bites · model=claude-sonnet-4-6 · rubric=visible-food-v1 · input_sha256=<frame hash> · judged_at=<UTC timestamp> · label_source=vision_model_inference · label_status=identified · labels=["salad"]
- **Episode #2:** 12:09:20 · 1 bite · label_status=uncertain · labels=[]
```

If no bite episodes were detected, the Episodes section says so. The output
is an episode log, not a unique-food list: the same food can appear in
multiple episodes. Episode numbers are stable correction targets. `identified`
means the model inferred visible candidates from the first-bite frame; it does
not mean a person verified the label.

### Record a human correction

After the Run is finalized, append a correction event to its sibling
`<receipt>.corrections.jsonl` file. This keeps the model's original label and
the human correction, actor, timestamp, and optional reason together without
changing or retaining the camera image:

```bash
python "$MEAL_CAM_SKILL_DIR/scripts/record_correction.py" \
  --receipt "$MEAL_CAM_OUTPUT_DIR/meal-YYYY-MM-DD-HHMMSS-ffffff.md" \
  --episode 1 \
  --label "spinach salad" \
  --actor "<person making the correction>" \
  --reason "The visible dish was spinach salad"
```

Repeat `--label` for multiple foods. Read the original receipt together with
the correction sidecar; later corrections append new events and never replace
earlier judgments. Do not overwrite the inferred label in the Markdown file.

---

## Error handling

- **Camera cannot open:** the Run receipt is finalized as `failed`, and the
  process log reports a startup error without echoing the camera URL. Ask the
  user to check the device, URL, credentials, or camera permissions locally.
- **Camera stops returning frames:** after about two seconds of consecutive
  read failures, the script ends the Run and finalizes the receipt with
  `source-ended` status.
- **Anthropic API error:** the episode records `label_status=service_error`
  and the error class, distinct from `no_food_visible` and `uncertain`; it does
  not retry or increase the capture interval automatically.
- **Output directory:** created automatically. If it is not writable, report
  the file error; do not claim a receipt exists.
