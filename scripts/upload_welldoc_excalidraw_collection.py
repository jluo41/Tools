#!/usr/bin/env python3
"""Upload selected WellDoc-SPACE Excalidraw boards to Excalidraw+.

Requires EXCALIDRAW_API_KEY in the environment.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


API_BASE = "https://api.excalidraw.com/api/v1"
APP_ORG = "1JWkKv8oMIX"
COLLECTION_NAME = "WellDoc-SPACE"

SELECTED = [
    (
        "ScalingLaw - Project Overview",
        "examples/ProjC-Model-1-ScalingLaw/diagram/project.excalidraw",
    ),
    (
        "ScalingLaw - Task Map",
        "examples/ProjC-Model-1-ScalingLaw/diagram/04-taskmap.excalidraw",
    ),
    (
        "ScalingLaw - Status Board",
        "examples/ProjC-Model-1-ScalingLaw/diagram/docs/scaling-law-status.excalidraw",
    ),
    (
        "ScalingLaw - MLM Pretraining",
        "examples/ProjC-Model-1-ScalingLaw/tasks/A02_pretraining_mlm/A_pretraining_mlm.excalidraw",
    ),
    (
        "ScalingLaw - MTP Pretraining",
        "examples/ProjC-Model-1-ScalingLaw/tasks/A03_pretraining_mtp/A_pretraining_mtp.excalidraw",
    ),
    (
        "EventGlucose - Portfolio",
        "examples/ProjB-Bench-2-EventGlucose/docs/diagrams/eventglucose-portfolio.excalidraw",
    ),
    (
        "EventFixLenVec - Main Canvas",
        "examples/ProjC-Model-EventFixLenVec/diagram/canvas-260507.excalidraw",
    ),
    (
        "EventFixLenVec - A22 LHM CLM Direct",
        "examples/ProjC-Model-EventFixLenVec/tasks/A22_lhm_clm_direct/diagram/canvas-260508-a22-plan.excalidraw",
    ),
    (
        "EventBodyDelta - Body Event Arc",
        "examples/ProjC-Model-EventBodyDelta/diagram/canvas-260522.excalidraw",
    ),
    (
        "UnderstandCGM - Agent Paper Canvas",
        "examples/ProjF-Agent-1-UnderstandCGM/paper/Paper-CGMAgent-IS/diagram/canvas-260506.excalidraw",
    ),
    (
        "MealCam - Pipeline Flow",
        "examples/ProjE-Sensor-1-MealCam/docs/pipeline-flow.excalidraw",
    ),
]


def list_items(value: object) -> list:
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        for key in ("items", "data", "collections", "scenes"):
            nested = value.get(key)
            if isinstance(nested, list):
                return nested
    return []


def request(method: str, path: str, token: str, body: dict | None = None) -> dict:
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        f"{API_BASE}{path}",
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        raise RuntimeError(f"{method} {path} failed: HTTP {exc.code}: {detail}") from exc


def normalize_element(element: dict, index: int, updated: int) -> dict:
    element = dict(element)
    element.setdefault("roundness", None)
    element.setdefault("index", f"a{index}")
    element.setdefault("frameId", None)
    # Older local boards often have stale reverse bindings. The visible arrows
    # and text remain intact without them, while Excalidraw+ rejects inconsistent
    # binding graphs during API writes.
    element["boundElements"] = None
    element.setdefault("updated", updated)
    element.setdefault("link", None)
    element.setdefault("locked", False)
    element.setdefault("groupIds", [])
    element.setdefault("isDeleted", False)

    if element.get("type") == "text":
        text = element.get("text", "")
        element.setdefault("originalText", text)
        element.setdefault("containerId", None)
        element.setdefault("autoResize", True)
        element.setdefault("lineHeight", 1.25)
        element.setdefault("textAlign", "left")
        element.setdefault("verticalAlign", "top")
    elif element.get("type") in {"line", "arrow"}:
        element.setdefault("startBinding", None)
        element.setdefault("endBinding", None)
        for binding_key in ("startBinding", "endBinding"):
            binding = element.get(binding_key)
            if isinstance(binding, dict):
                fixed_point = binding.get("fixedPoint")
                mode = binding.get("mode")
                if (
                    not isinstance(fixed_point, list)
                    or len(fixed_point) != 2
                    or mode not in {"inside", "orbit", "skip"}
                ):
                    element[binding_key] = None
        element.setdefault("startArrowhead", None)
        element.setdefault("endArrowhead", None)
        if element.get("type") == "line":
            element.setdefault("polygon", False)
        else:
            element.setdefault("elbowed", False)
    elif element.get("type") == "image":
        element.setdefault("status", "saved")
        element.setdefault("scale", [1, 1])
        element.setdefault("crop", None)
    elif element.get("type") == "freedraw":
        points = element.get("points") or []
        element.setdefault("pressures", [0.5 for _ in points])
        element.setdefault("simulatePressure", False)
    elif element.get("type") in {"frame", "magicframe"}:
        element.setdefault("name", None)

    return element


def load_scene(root: Path, rel_path: str) -> dict:
    path = root / rel_path
    scene = json.loads(path.read_text())
    if scene.get("type") != "excalidraw":
        raise ValueError(f"not an Excalidraw scene: {path}")

    updated = int(time.time() * 1000)
    elements = [
        normalize_element(element, index, updated)
        for index, element in enumerate(scene.get("elements", []))
        if element.get("type") != "selection"
    ]
    app_state = scene.get("appState") or {}
    app_state = {
        "viewBackgroundColor": app_state.get("viewBackgroundColor", "#ffffff"),
        "lockedMultiSelections": app_state.get("lockedMultiSelections", {}),
    }

    return {
        "type": "excalidraw",
        "version": scene.get("version", 2),
        "source": scene.get("source", "https://plus.excalidraw.com"),
        "elements": elements,
        "appState": app_state,
        "files": scene.get("files") or {},
    }


def main() -> int:
    token = os.environ.get("EXCALIDRAW_API_KEY", "").strip()
    if not token:
        print("EXCALIDRAW_API_KEY is not set", file=sys.stderr)
        return 2

    root = Path(__file__).resolve().parents[2]
    collections_response = request("GET", "/collections", token)
    collections = list_items(collections_response)
    collection = next((item for item in collections if item.get("name") == COLLECTION_NAME), None)
    if collection is None:
        collection = request("POST", "/collections", token, {"name": COLLECTION_NAME})
    collection_id = collection["id"]

    scenes_response = request("GET", f"/collections/{collection_id}/scenes", token)
    existing_scenes = {
        (item.get("metadata") or item).get("name"): (item.get("metadata") or item)
        for item in list_items(scenes_response)
    }

    uploaded = []
    for title, rel_path in SELECTED:
        scene = existing_scenes.get(title)
        if scene is None:
            scene_meta = request(
                "POST",
                f"/collections/{collection_id}/scenes",
                token,
                {"name": title, "pinned": True},
            )
            scene = scene_meta["metadata"]
        scene_id = scene["id"]
        content = load_scene(root, rel_path)
        updated = request("PUT", f"/scenes/{scene_id}/content", token, content)
        uploaded.append(
            {
                "title": title,
                "source": rel_path,
                "scene_id": scene_id,
                "elements": len(updated.get("elements") or content["elements"]),
                "url": f"https://app.excalidraw.com/o/{APP_ORG}/{scene_id}",
            }
        )

    print(json.dumps({"collection": collection, "uploaded": uploaded}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
