"""Meal-cam capture loop (episode-driven, one receipt per Run).

Captures frames at target fps, runs the local MediaPipe bite-event detector
(hand-to-mouth + mouth-open), groups consecutive bites into "eating
episodes" via `EpisodeTracker`, and calls Claude vision ONLY on the first
bite of each episode. Later bites of the same episode are just counted. This
is an episode heuristic, not a guarantee that each physical food item gets
its own call.

Output: a unique `{output_dir}/meal-{YYYY-MM-DD}-{HHMMSS}-{microseconds}.md`
receipt created at startup and finalized on graceful stop. Episodes are
grouped (start–end · bite count · food label).

Requires: `pip install opencv-python anthropic mediapipe`.
`ANTHROPIC_API_KEY` must be set in the environment.

Usage:
    python meal_cam_loop.py --source 0 --fps 10 \\
        --cooldown-sec 3 --max-gap-sec 45 \\
        --output-dir /path/to/_WorkSpace/6-EndpointStore/mealcam_logs
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import math
import os
import signal
import sys
import time
from pathlib import Path
from dataclasses import dataclass

FOOD_LABEL_RUBRIC = "visible-food-v1"


@dataclass(frozen=True)
class FoodIdentification:
    """An image-only classification; it does not establish food consumed."""
    status: str  # identified | no_food_visible | uncertain | service_error
    labels: list[str] | None = None
    error_type: str | None = None
    model: str | None = None
    rubric: str = FOOD_LABEL_RUBRIC
    input_sha256: str | None = None
    judged_at: str | None = None


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--source", default=os.environ.get("MEAL_CAM_SOURCE", "0"),
        help="Webcam index, RTSP URL, or video file path; defaults to MEAL_CAM_SOURCE or '0'",
    )
    p.add_argument("--fps", type=float, default=10.0,
                   help="Frame capture / bite-detection rate (Hz)")
    p.add_argument("--cooldown-sec", type=float, default=3.0,
                   help="Min seconds between bite events (BiteDetector dedupe)")
    p.add_argument("--max-gap-sec", type=float, default=45.0,
                   help="Max seconds between bites in the same episode; "
                        "longer gap starts a new episode")
    p.add_argument("--output-dir", required=True,
                   help="Directory for per-session meal-*.md files")
    p.add_argument("--model", default="claude-sonnet-4-6",
                   help="Claude vision model ID")
    args = p.parse_args()
    if not math.isfinite(args.fps) or args.fps <= 0:
        p.error("--fps must be a finite number greater than zero")
    if (not math.isfinite(args.cooldown_sec) or args.cooldown_sec < 0
            or not math.isfinite(args.max_gap_sec) or args.max_gap_sec < 0):
        p.error("--cooldown-sec and --max-gap-sec must be finite non-negative numbers")
    return args


def open_capture(source: str):
    import cv2
    src = int(source) if source.isdigit() else source
    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        # Do not echo an RTSP URL: it may contain a username and password.
        cap.release()
        raise RuntimeError("Could not open camera source; check its local configuration")
    return cap


def frame_to_b64_jpeg(frame) -> tuple[str, str]:
    import cv2
    ok, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    if not ok:
        raise RuntimeError("JPEG encode failed")
    image_bytes = buf.tobytes()
    return (base64.standard_b64encode(image_bytes).decode("ascii"),
            hashlib.sha256(image_bytes).hexdigest())


def identify_food(image_b64: str, model: str,
                  input_sha256: str | None = None) -> FoodIdentification:
    """Classify visible food candidates; never infer what was swallowed."""
    from anthropic import Anthropic, APIError
    judged_at = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")

    def result(status: str, labels: list[str] | None = None,
               error_type: str | None = None) -> FoodIdentification:
        return FoodIdentification(status, labels, error_type, model,
                                  FOOD_LABEL_RUBRIC, input_sha256, judged_at)

    try:
        client = Anthropic()
        resp = client.messages.create(
            model=model,
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image",
                     "source": {"type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_b64}},
                    {"type": "text",
                     "text": (
                         "Classify only what is visibly identifiable in this "
                         "frame; this does not establish that any food was eaten. "
                         "Return one JSON object with status and labels. Use "
                         "status='identified' and labels as a list of short "
                         "lowercase food names when one or more foods are visible; "
                         "status='no_food_visible' and labels=[] when no food is "
                         "visibly identifiable; or status='uncertain' and labels=[] "
                         "when the image is ambiguous or obstructed. Do not add "
                         "confidence numbers or text outside the JSON."
                     )},
                ],
            }],
        )
        if not resp.content or not getattr(resp.content[0], "text", None):
            return result("uncertain")
        try:
            payload = json.loads(resp.content[0].text.strip())
        except (TypeError, json.JSONDecodeError):
            return result("uncertain")
        status = payload.get("status") if isinstance(payload, dict) else None
        labels = payload.get("labels") if isinstance(payload, dict) else None
        if status == "identified" and isinstance(labels, list):
            clean_labels = [
                " ".join(str(label).lower().split())
                for label in labels
                if isinstance(label, str) and label.strip()
            ]
            if clean_labels:
                return result("identified", clean_labels)
        if status == "no_food_visible" and labels == []:
            return result("no_food_visible", [])
        if status == "uncertain" and labels == []:
            return result("uncertain", [])
        return result("uncertain")
    except APIError as exc:
        error_type = type(exc).__name__
        print(f"[meal-cam] vision service error: {error_type}", flush=True)
        return result("service_error", error_type=error_type)


def render_session_file(path: Path,
                        start: dt.datetime,
                        end: dt.datetime | None,
                        episodes,
                        status: str) -> None:
    """Rewrite the full session Markdown file (idempotent).

    `episodes` is an iterable of Episode objects (from episode_tracker).
    """
    end_text = end.strftime("%H:%M:%S") if end else "In progress"
    duration_text = "In progress"
    if end:
        elapsed_sec = max(0, int((end - start).total_seconds()))
        duration_text = f"{elapsed_sec // 60} min {elapsed_sec % 60} sec"
    lines = [
        f"# {start.date().isoformat()}",
        "",
        f"- **Run ID:** {path.stem}",
        f"- **Start:**    {start.strftime('%H:%M:%S')}",
        f"- **End:**      {end_text}",
        f"- **Duration:** {duration_text}",
        f"- **Status:**   {status}",
        "",
        "## Episodes",
        "",
    ]
    has_episodes = False
    for ep in episodes:
        has_episodes = True
        ep_start = ep.start.strftime("%H:%M:%S")
        ep_end = ep.end.strftime("%H:%M:%S")
        bites = ep.bites
        suffix = "bite" if bites == 1 else "bites"
        interval = ep_start if ep_start == ep_end else f"{ep_start}–{ep_end}"
        labels = json.dumps(ep.labels, ensure_ascii=False) if ep.labels is not None else "null"
        line = (
            f"- **Episode #{ep.id}:** {interval} · {bites} {suffix} · "
        )
        if ep.label_model:
            line += (f"model={ep.label_model} · rubric={ep.label_rubric} · "
                     f"input_sha256={ep.label_input_sha256} · "
                     f"judged_at={ep.label_judged_at} · ")
            source = ("service_failure" if ep.label_status == "service_error"
                      else "vision_model_inference")
            line += f"label_source={source} · "
        line += f"label_status={ep.label_status} · labels={labels}"
        if ep.label_error_type:
            line += f" · service_error={ep.label_error_type}"
        lines.append(line)
    if not has_episodes:
        lines.append("- No bite episodes detected.")

    # Replace atomically so a concurrent reader sees either the previous
    # complete receipt or the new one, never a partially written file.
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    temporary.replace(path)


class GracefulExit:
    def __init__(self):
        self.stop = False
        self.skip_requested = False
        signal.signal(signal.SIGINT, self._handle)
        signal.signal(signal.SIGTERM, self._handle)
        self.skip_signal = getattr(signal, "SIGUSR1", None)
        if self.skip_signal is not None:
            signal.signal(self.skip_signal, self._request_skip)

    def _handle(self, *_):
        self.stop = True

    def _request_skip(self, *_):
        self.skip_requested = True

    def consume_skip_request(self) -> bool:
        requested = self.skip_requested
        self.skip_requested = False
        return requested


def main() -> int:
    from episode_tracker import EpisodeTracker

    args = parse_args()
    out_dir = Path(args.output_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    session_start = dt.datetime.now()
    session_file = out_dir / f"meal-{session_start.strftime('%Y-%m-%d-%H%M%S-%f')}.md"
    guard = GracefulExit()
    tracker = EpisodeTracker(max_gap_sec=args.max_gap_sec)
    frame_dt = 1.0 / args.fps
    consecutive_fail = 0
    max_consecutive_fail = max(1, int(args.fps * 2))  # about 2 seconds -> stop
    cap = None
    detector = None
    status = "starting"
    exit_code = 0

    # Write the receipt immediately, including for sessions with no bites or
    # a camera/model initialization error.
    render_session_file(session_file, session_start, None, tracker.episodes, status)
    print(f"[meal-cam] receipt created. session_file={session_file}", flush=True)

    def apply_pending_skip() -> None:
        if not guard.consume_skip_request():
            return
        removed = tracker.remove_last()
        if removed is None:
            print("[meal-cam] skip requested; no episode to remove", flush=True)
        else:
            print(f"[meal-cam] removed episode #{removed.id}", flush=True)
        render_session_file(session_file, session_start, None,
                            tracker.episodes, status)

    try:
        import cv2
        from bite_detector import BiteDetector

        cap = open_capture(args.source)
        detector = BiteDetector(cooldown_sec=args.cooldown_sec)
        status = "running"
        render_session_file(session_file, session_start, None,
                            tracker.episodes, status)
        source_kind = ("webcam" if args.source.isdigit() else
                       "network stream" if "://" in args.source else "video file")
        print(f"[meal-cam] started. source_type={source_kind} fps={args.fps} "
              f"cooldown={args.cooldown_sec}s max_gap={args.max_gap_sec}s "
              f"session_file={session_file}", flush=True)

        while not guard.stop:
            apply_pending_skip()
            t_start = time.monotonic()

            ok, frame_bgr = cap.read()
            if not ok:
                consecutive_fail += 1
                if consecutive_fail >= max_consecutive_fail:
                    print("[meal-cam] source exhausted, stopping", flush=True)
                    status = "source-ended"
                    break
                time.sleep(frame_dt)
                continue
            consecutive_fail = 0

            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

            if detector.is_bite_event(frame_rgb):
                now = dt.datetime.now()
                is_new_ep, ep = tracker.on_bite(now)

                if is_new_ep:
                    # New food — call Claude vision
                    b64, frame_sha256 = frame_to_b64_jpeg(frame_bgr)
                    identification = identify_food(b64, args.model, frame_sha256)
                    del b64
                    ep.labels = identification.labels
                    ep.label_status = identification.status
                    ep.label_error_type = identification.error_type
                    ep.label_model = identification.model
                    ep.label_rubric = identification.rubric
                    ep.label_input_sha256 = identification.input_sha256
                    ep.label_judged_at = identification.judged_at

                    render_session_file(session_file, session_start, None,
                                        tracker.episodes, status)
                    print(f"[meal-cam] episode #{ep.id} START  "
                          f"label_status={identification.status} "
                          f"labels={identification.labels!r} "
                          f"file={session_file.name}",
                          flush=True)
                else:
                    # Same episode — just update counter + session file
                    render_session_file(session_file, session_start, None,
                                        tracker.episodes, status)
                    print(f"[meal-cam] episode #{ep.id} bite #{ep.bites}  "
                          f"(label_status={ep.label_status}, labels={ep.labels!r})",
                          flush=True)

            # Maintain target fps; stay responsive to Ctrl-C
            elapsed = time.monotonic() - t_start
            sleep_for = max(0.0, frame_dt - elapsed)
            if sleep_for > 0 and not guard.stop:
                time.sleep(sleep_for)
    except Exception as exc:
        status = "failed"
        # Avoid printing the original exception because some camera drivers
        # include the configured RTSP URL (and credentials) in it.
        print(f"[meal-cam] failed during startup or capture: {type(exc).__name__}",
              flush=True)
        exit_code = 1
    finally:
        try:
            apply_pending_skip()
        except Exception as exc:
            print(f"[meal-cam] could not apply queued skip: {type(exc).__name__}",
                  flush=True)
        cleanup_failed = False
        if cap is not None:
            try:
                cap.release()
            except Exception as exc:
                cleanup_failed = True
                print(f"[meal-cam] camera cleanup failed: {type(exc).__name__}",
                      flush=True)
        if detector is not None:
            try:
                detector.close()
            except Exception as exc:
                cleanup_failed = True
                print(f"[meal-cam] detector cleanup failed: {type(exc).__name__}",
                      flush=True)
        session_end = dt.datetime.now()
        if status == "running":
            status = "stopped"
        if cleanup_failed and status == "stopped":
            status = "cleanup-failed"
        render_session_file(session_file, session_start, session_end,
                            tracker.episodes, status)
        total_bites = sum(ep.bites for ep in tracker.episodes)
        msg = (f"[meal-cam] stopped. episodes={len(tracker.episodes)} "
               f"bites={total_bites}")
        print(f"{msg}  file={session_file}", flush=True)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
