"""Smoke test for BiteDetector.

Runs the MediaPipe bite detector on every frame of a video (or single image)
and prints per-frame debug info. Use this to calibrate the thresholds against
real eating footage.

Usage:
    python test_bite_detector.py <video.mp4 | image.jpg | 0>     # 0 = webcam

On this server there's no webcam — feed a short phone-recorded eating clip:
    scp phone_recording.mp4 server:/tmp/eating.mp4
    python test_bite_detector.py /tmp/eating.mp4
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import cv2

# Make bite_detector importable regardless of cwd
sys.path.insert(0, str(Path(__file__).parent))
from bite_detector import BiteDetector


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: test_bite_detector.py <video.mp4 | image.jpg | 0>", file=sys.stderr)
        return 2

    raw = sys.argv[1]
    src = int(raw) if raw.isdigit() else raw
    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        print(f"cannot open source: {raw}", file=sys.stderr)
        return 2

    det = BiteDetector()
    n = 0
    bites = 0
    t0 = time.time()
    try:
        while True:
            ok, frame_bgr = cap.read()
            if not ok:
                break
            n += 1
            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            fired = det.is_bite_event(frame_rgb)
            info = det.debug_info()
            if fired:
                bites += 1
                print(f"[{n:5d}]  🍽  BITE!  {info}", flush=True)
            elif n % 30 == 0:
                print(f"[{n:5d}]  {info}", flush=True)
    finally:
        cap.release()
        det.close()

    dt = time.time() - t0
    fps = n / dt if dt > 0 else 0.0
    print(f"\nDone: {n} frames in {dt:.1f}s ({fps:.1f} fps), {bites} bite events")
    return 0


if __name__ == "__main__":
    sys.exit(main())
