"""Meal-cam capture loop. SKELETON — vision call and dedupe are TODO.

Grabs one frame per interval from a webcam (index 0) or RTSP URL, asks Claude
vision what food is visible, and appends a time-stamped bullet to today's
LogSeq journal.

Usage:
    python meal_cam_loop.py --source 0 --interval 5 \\
        --journal /home/jluo41/LogSeq-Me/journals
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import os
import signal
import sys
import time
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--source", default="0",
                   help="Webcam index (e.g. '0') or RTSP URL")
    p.add_argument("--interval", type=float, default=5.0,
                   help="Seconds between frames")
    p.add_argument("--journal", required=True,
                   help="Path to LogSeq journals/ directory")
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
    """Ask Claude vision what food is visible. Return short label or None.

    TODO: wire to anthropic SDK. Expected contract:
      - input: base64 JPEG
      - output: lowercase short food label (e.g. "green salad"),
                or None if no food detected
      - prompt should say: "One short label only, or 'none'. No prose."
    """
    # from anthropic import Anthropic
    # client = Anthropic()
    # resp = client.messages.create(
    #     model=model,
    #     max_tokens=40,
    #     messages=[{
    #         "role": "user",
    #         "content": [
    #             {"type": "image",
    #              "source": {"type": "base64",
    #                         "media_type": "image/jpeg",
    #                         "data": image_b64}},
    #             {"type": "text",
    #              "text": "What food is visible? One short lowercase label, "
    #                      "or 'none'. No prose."}
    #         ],
    #     }),
    # label = resp.content[0].text.strip().lower()
    # return None if label in {"none", ""} else label
    return None  # stub


def append_to_journal(journal_dir: Path, label: str) -> None:
    """Append a bullet under the Meal-Cam-Records heading in today's journal."""
    now = dt.datetime.now()
    fname = now.strftime("%Y_%m_%d") + ".md"
    path = journal_dir / fname
    heading = "- [[Meal-Cam-Records]]"
    bullet = f"\t- {now.strftime('%H:%M')} {label} #meal-cam"

    path.touch(exist_ok=True)
    text = path.read_text()
    if heading in text:
        # append child under the existing heading (TODO: handle nested blocks
        # properly — current version just appends at end-of-file under heading)
        path.write_text(text.rstrip() + "\n" + bullet + "\n")
    else:
        path.write_text(text.rstrip() + "\n" + heading + "\n" + bullet + "\n")


class GracefulExit:
    stop = False

    def __init__(self):
        signal.signal(signal.SIGINT, self._handle)
        signal.signal(signal.SIGTERM, self._handle)

    def _handle(self, *_):
        self.stop = True


def main() -> int:
    args = parse_args()
    journal_dir = Path(args.journal)
    if not journal_dir.is_dir():
        print(f"ERROR: journal dir not found: {journal_dir}", file=sys.stderr)
        return 2

    cap = open_capture(args.source)
    guard = GracefulExit()
    last_label: str | None = None
    detections = 0

    print(f"[meal-cam] started. source={args.source} interval={args.interval}s "
          f"journal={journal_dir}", flush=True)

    try:
        while not guard.stop:
            ok, frame = cap.read()
            if not ok:
                print("[meal-cam] frame read failed, retrying...", flush=True)
                time.sleep(args.interval)
                continue

            b64 = frame_to_b64_jpeg(frame)
            label = identify_food(b64, args.model)

            if label and label != last_label:
                append_to_journal(journal_dir, label)
                detections += 1
                last_label = label
                print(f"[meal-cam] logged: {label}", flush=True)
            else:
                # silent skip — either no food or same as last
                pass

            # sleep in small chunks so Ctrl-C is responsive
            slept = 0.0
            while slept < args.interval and not guard.stop:
                time.sleep(min(0.5, args.interval - slept))
                slept += 0.5
    finally:
        cap.release()
        print(f"[meal-cam] stopped. total detections={detections}", flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
