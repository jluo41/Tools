"""The rendered screens of a Design Folder: each Generate Result's render manifest, the
picture of exactly the shown draft, and its <img>.

Split out of design.py; design.py re-exports every name here."""
from __future__ import annotations

import traceback
from pathlib import Path

from src.common import delivery_read_lane_dir

from live.design_core_base import _escape, _read, _relative_href, _unit_gate, _yaml


_PICTURE = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg")


def _renders(folder: Path, runs: list[dict]) -> dict[str, list[dict]]:
    """Read Result-local evidence first; retain old Delivery manifests as history."""
    try:
        import json
        rows = json.loads(_read(delivery_read_lane_dir(folder, "render") / "manifest.json") or "[]")
    except ValueError:
        rows = []
    out: dict[str, list[dict]] = {}
    for row in rows if isinstance(rows, list) else []:
        if isinstance(row, dict) and row.get("item") and row.get("render"):
            path = delivery_read_lane_dir(folder, "render") / str(row["render"])
            out.setdefault(str(row["item"]), []).append(
                {**row, "path": path, "picture": path.suffix.lower() in _PICTURE and path.is_file()})
    gate = None
    for run in runs:
        if run["kind"] != "generate" or run["status"] != "complete":
            continue
        result_path = run["result_dir"] / "result.yaml"
        manifest = _yaml(result_path)
        if "render_manifest" not in manifest:
            continue
        # An invalid current manifest must not silently fall back to an old picture.
        for item_rows in out.values():
            item_rows[:] = [row for row in item_rows if row.get("candidate") != run["id"]]
        try:
            gate = gate or _unit_gate()
            # Same rule as the records check: a file newer than result.yaml is stale (file time, no hash).
            subjects = {path: run["id"] for _, path in
                        gate.artifact_records(run["result_dir"], manifest.get("artifacts"), record=result_path)}
            for row in gate.render_records(run["result_dir"], manifest, subjects, run["item"],
                                           record=result_path):
                out.setdefault(run["item"], []).append(
                    {**row, "picture": row["path"].suffix.lower() in _PICTURE})
        except (OSError, ValueError, TypeError, KeyError, ImportError, AttributeError):
            # The folder audit reports the error; the presenter shows no false preview.
            traceback.print_exc()
            continue
    return out


def _render_for(rows: list[dict], run: str) -> dict | None:
    """The picture of exactly this draft; a picture of an older draft is never shown for a newer one."""
    def version(row):
        # Historical Delivery manifests also used numeric strings or no version.
        # New Result manifests already enforce a positive integer in the gate.
        try:
            return int(row.get("version") or 0)
        except (TypeError, ValueError, OverflowError):
            return -1
    hits = [r for r in rows if r.get("candidate") == run and r["picture"]
            and version(r) >= 0]
    return max(hits, key=version) if hits else None


def design_picture(root: Path, item: dict, alt: str = "") -> str:
    """An <img> of the item's rendered screen, or '' when its design is text only."""
    render = item.get("render")
    if not render:
        return ""
    src = _relative_href(Path(root), render["path"])
    if not src:
        import base64
        kind = "svg+xml" if render["path"].suffix.lower() == ".svg" else render["path"].suffix.lower().lstrip(".").replace("jpg", "jpeg")
        src = f"data:image/{kind};base64," + base64.b64encode(render["path"].read_bytes()).decode("ascii")
    return (f'<img class=shot src="{_escape(src)}" alt="{_escape(alt or item.get("title", ""))}" loading=lazy>')
