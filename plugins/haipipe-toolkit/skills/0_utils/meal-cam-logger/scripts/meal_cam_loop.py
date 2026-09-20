"""Meal-cam capture loop (v0.3 — episode-driven).

Captures frames at target fps, runs the local MediaPipe bite-event detector
(hand-to-mouth + mouth-open), groups consecutive bites into "eating
episodes" via `EpisodeTracker`, and calls Claude vision ONLY on the first
bite of each episode. Later bites of the same episode are just counted.
One physical food item = one API call.

Output: `{output_dir}/meal-{YYYY-MM-DD}-{HHMM}.md` — per-session, with
episodes grouped (start–end · bite count · food label).

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
import signal
import sys
import time
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--source", default="0",
                   help="Webcam index (e.g. '0'), RTSP URL, or video file path")
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
    return p.parse_args()


def open_capture(source: str):
    import cv2
    src = int(source) if source.isdigit() else source
    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera source: {source}")
    return cap


def frame_to_b64_jpeg(frame) -> str:
    import cv2
    ok, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    if not ok:
        raise RuntimeError("JPEG encode failed")
    return base64.standard_b64encode(buf.tobytes()).decode("ascii")


def identify_food(image_b64: str, model: str) -> str | None:
    """Ask Claude vision what food is visible. Return short lowercase label, or None."""
    from anthropic import Anthropic, APIError
    client = Anthropic()
    try:
        resp = client.messages.create(
            model=model,
            max_tokens=30,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image",
                     "source": {"type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_b64}},
                    {"type": "text",
                     "text": "What food is visible in this image? Answer with "
                             "ONE short lowercase label only (e.g. 'green salad', "
                             "'sourdough bread', 'black coffee'). If no food "
                             "is visible, answer 'none'. No other text."},
                ],
            }],
        )
        label = resp.content[0].text.strip().lower().strip('"\'.')
        return None if label in {"none", ""} else label
    except APIError as exc:
        print(f"[meal-cam] API error: {exc}", flush=True)
        return None


def render_session_file(path: Path,
                        start: dt.datetime,
                        end: dt.datetime,
                        episodes) -> None:
    """Rewrite the full session Markdown file (idempotent).

    `episodes` is an iterable of Episode objects (from episode_tracker).
    """
    duration_min = max(1, int(round((end - start).total_seconds() / 60)))
    lines = [
        f"# {start.date().isoformat()}",
        "",
        f"- **Start:**    {start.strftime('%H:%M')}",
        f"- **End:**      {end.strftime('%H:%M')}",
        f"- **Duration:** {duration_min} min",
        "",
        "## Episodes",
        "",
    ]
    for ep in episodes:
        label = ep.label or "(unidentified)"
        ep_start = ep.start.strftime("%H:%M")
        ep_end = ep.end.strftime("%H:%M")
        bites = ep.bites
        suffix = "bite" if bites == 1 else "bites"
        if ep_start == ep_end:
            lines.append(f"- {ep_start}         ({bites} {suffix})  {label}")
        else:
            lines.append(f"- {ep_start}–{ep_end}  ({bites} {suffix})  {label}")
    path.write_text("\n".join(lines) + "\n")


class GracefulExit:
    stop = False

    def __init__(self):
        signal.signal(signal.SIGINT, self._handle)
        signal.signal(signal.SIGTERM, self._handle)

    def _handle(self, *_):
        self.stop = True


def main() -> int:
    import cv2
    from bite_detector import BiteDetector
    from episode_tracker import EpisodeTracker

    args = parse_args()
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    cap = open_capture(args.source)
    guard = GracefulExit()
    detector = BiteDetector(cooldown_sec=args.cooldown_sec)
    tracker = EpisodeTracker(max_gap_sec=args.max_gap_sec)

    session_start: dt.datetime | None = None
    session_file: Path | None = None
    frame_dt = 1.0 / args.fps
    consecutive_fail = 0
    max_consecutive_fail = int(args.fps * 2)  # 2 seconds of failures -> stop

    print(f"[meal-cam] started. source={args.source} fps={args.fps} "
          f"cooldown={args.cooldown_sec}s max_gap={args.max_gap_sec}s "
          f"output_dir={out_dir}", flush=True)

    try:
        while not guard.stop:
            t_start = time.monotonic()

            ok, frame_bgr = cap.read()
            if not ok:
                consecutive_fail += 1
                if consecutive_fail >= max_consecutive_fail:
                    print("[meal-cam] source exhausted, stopping", flush=True)
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
                    b64 = frame_to_b64_jpeg(frame_bgr)
                    label = identify_food(b64, args.model)
                    ep.label = label
                    ep.first_frame_b64 = b64

                    if session_start is None:
                        session_start = now
                        session_file = out_dir / (
                            f"meal-{now.strftime('%Y-%m-%d-%H%M')}.md"
                        )
                    render_session_file(session_file, session_start, now,
                                        tracker.episodes)
                    print(f"[meal-cam] episode #{ep.id} START  "
                          f"label={label!r}  file={session_file.name}",
                          flush=True)
                else:
                    # Same episode — just update counter + session file
                    if session_file is not None:
                        render_session_file(session_file, session_start, now,
                                            tracker.episodes)
                    print(f"[meal-cam] episode #{ep.id} bite #{ep.bites}  "
                          f"({ep.label})", flush=True)

            # Maintain target fps; stay responsive to Ctrl-C
            elapsed = time.monotonic() - t_start
            sleep_for = max(0.0, frame_dt - elapsed)
            if sleep_for > 0 and not guard.stop:
                time.sleep(sleep_for)
    finally:
        cap.release()
        detector.close()
        total_bites = sum(ep.bites for ep in tracker.episodes)
        msg = (f"[meal-cam] stopped. episodes={len(tracker.episodes)} "
               f"bites={total_bites}")
        if session_file is not None:
            msg += f"  file={session_file.name}"
        print(msg, flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
