"""MediaPipe-based bite-event detector (tasks API).

Returns True when a new bite event is detected — hand fingertip close to the
mouth AND mouth open — with a cooldown so one bite ≠ many events.

Runs **locally on CPU** (no API, no cost). Uses the modern
`mediapipe.tasks.vision.{HandLandmarker, FaceLandmarker}` API. The two
`.task` model bundles are cached under `~/.cache/mediapipe/` (or
`$MEDIAPIPE_CACHE_DIR`) and downloaded on first use from Google's public
model storage.

Benchmark reference: RABiD (skeletal-feature bite detector) reports F1=0.948
on real meal video. This detector is a simpler proxy — expect lower precision
until thresholds are calibrated on real footage.
"""

from __future__ import annotations

import os
import time
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


_MODEL_URLS = {
    "hand_landmarker.task": (
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
        "hand_landmarker/float16/latest/hand_landmarker.task"
    ),
    "face_landmarker.task": (
        "https://storage.googleapis.com/mediapipe-models/face_landmarker/"
        "face_landmarker/float16/latest/face_landmarker.task"
    ),
}

_DEFAULT_CACHE = Path(
    os.environ.get("MEDIAPIPE_CACHE_DIR", Path.home() / ".cache" / "mediapipe")
)


def _ensure_model(name: str, cache_dir: Path) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / name
    if path.is_file() and path.stat().st_size > 10_000:
        return path
    url = _MODEL_URLS[name]
    print(f"[bite_detector] downloading {name}  <-  {url}", flush=True)
    urllib.request.urlretrieve(url, path)
    size_mb = path.stat().st_size / (1024 * 1024)
    print(f"[bite_detector]   saved {size_mb:.1f} MB to {path}", flush=True)
    return path


# MediaPipe FaceLandmarker indices (478 points, same layout as the legacy mesh).
_LIP_TOP_INNER = 13
_LIP_BOTTOM_INNER = 14
_CHEEK_LEFT = 234
_CHEEK_RIGHT = 454

# MediaPipe HandLandmarker indices (21 per hand).
_INDEX_TIP = 8
_THUMB_TIP = 4
_MIDDLE_TIP = 12


@dataclass
class BiteDetector:
    """Detects bite events from RGB video frames.

    Usage:
        det = BiteDetector()
        if det.is_bite_event(frame_rgb):
            ...  # trigger food ID
        det.close()
    """

    distance_threshold: float = 0.40   # hand-to-mouth dist / face width
    mouth_open_threshold: float = 0.025  # inner-lip gap / face width
    cooldown_sec: float = 3.0
    cache_dir: Path = field(default_factory=lambda: _DEFAULT_CACHE)

    _hand_lm: Any = field(init=False, default=None, repr=False)
    _face_lm: Any = field(init=False, default=None, repr=False)
    _last_bite_ts: float = field(init=False, default=0.0, repr=False)
    _last_debug: dict = field(init=False, default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        from mediapipe.tasks.python import BaseOptions, vision

        hand_model = _ensure_model("hand_landmarker.task", self.cache_dir)
        face_model = _ensure_model("face_landmarker.task", self.cache_dir)

        self._hand_lm = vision.HandLandmarker.create_from_options(
            vision.HandLandmarkerOptions(
                base_options=BaseOptions(model_asset_path=str(hand_model)),
                num_hands=2,
                min_hand_detection_confidence=0.5,
                min_hand_presence_confidence=0.5,
                min_tracking_confidence=0.5,
                running_mode=vision.RunningMode.IMAGE,
            )
        )
        self._face_lm = vision.FaceLandmarker.create_from_options(
            vision.FaceLandmarkerOptions(
                base_options=BaseOptions(model_asset_path=str(face_model)),
                num_faces=1,
                min_face_detection_confidence=0.5,
                min_face_presence_confidence=0.5,
                min_tracking_confidence=0.5,
                running_mode=vision.RunningMode.IMAGE,
            )
        )

    def is_bite_event(self, frame_rgb) -> bool:
        """frame_rgb : HxWx3 uint8 numpy array, **RGB** (not BGR)."""
        import mediapipe as mp

        now = time.monotonic()
        if now - self._last_bite_ts < self.cooldown_sec:
            self._last_debug = {"reason": "cooldown"}
            return False

        mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        hand_res = self._hand_lm.detect(mp_img)
        face_res = self._face_lm.detect(mp_img)

        if not face_res.face_landmarks:
            self._last_debug = {"reason": "no_face"}
            return False
        if not hand_res.hand_landmarks:
            self._last_debug = {"reason": "no_hand"}
            return False

        lm = face_res.face_landmarks[0]

        mx = (lm[_LIP_TOP_INNER].x + lm[_LIP_BOTTOM_INNER].x) / 2
        my = (lm[_LIP_TOP_INNER].y + lm[_LIP_BOTTOM_INNER].y) / 2

        dx = lm[_CHEEK_LEFT].x - lm[_CHEEK_RIGHT].x
        dy = lm[_CHEEK_LEFT].y - lm[_CHEEK_RIGHT].y
        face_w = (dx * dx + dy * dy) ** 0.5
        if face_w <= 0:
            self._last_debug = {"reason": "face_width_zero"}
            return False

        mouth_gap = abs(lm[_LIP_TOP_INNER].y - lm[_LIP_BOTTOM_INNER].y) / face_w
        if mouth_gap < self.mouth_open_threshold:
            self._last_debug = {"reason": "mouth_closed",
                                "mouth_gap": round(mouth_gap, 3)}
            return False

        min_rel_dist = float("inf")
        for hand in hand_res.hand_landmarks:
            for tip_idx in (_INDEX_TIP, _THUMB_TIP, _MIDDLE_TIP):
                hx = hand[tip_idx].x
                hy = hand[tip_idx].y
                d = ((hx - mx) ** 2 + (hy - my) ** 2) ** 0.5
                rel = d / face_w
                if rel < min_rel_dist:
                    min_rel_dist = rel

        self._last_debug = {
            "rel_dist": round(min_rel_dist, 3),
            "mouth_gap": round(mouth_gap, 3),
        }
        if min_rel_dist < self.distance_threshold:
            self._last_bite_ts = now
            self._last_debug["reason"] = "bite!"
            return True

        self._last_debug["reason"] = "hand_far"
        return False

    def debug_info(self) -> dict:
        """Last frame's detector state (for logging / overlays)."""
        return dict(self._last_debug)

    def close(self) -> None:
        if self._hand_lm is not None:
            self._hand_lm.close()
        if self._face_lm is not None:
            self._face_lm.close()
