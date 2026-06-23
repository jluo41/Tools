"""
Progress tracking for food-to-description pipeline.
Inspired by haipipe-probe-loop LOOP_LOG pattern and scan_status.py JSON pattern.

Tracks per-stage: status, count, metric, timestamp, error.
File-based (JSON): ~/.food-description/status.json (persistent across invocations).
"""
import json
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional
from .constants import STATUS_DIR, STATUS_FILE


class Statusline:
    """Track and report progress per pipeline stage."""

    def __init__(self, pipeline_name: str = "food-to-description"):
        self.pipeline_name = pipeline_name
        self.STATUS_DIR.mkdir(parents=True, exist_ok=True)

    def _read_status(self) -> dict:
        """Load status from JSON file."""
        if STATUS_FILE.exists():
            with open(STATUS_FILE) as f:
                return json.load(f)
        return {
            "pipeline": self.pipeline_name,
            "created": datetime.now().isoformat(),
            "stages": {}
        }

    def _write_status(self, data: dict):
        """Atomically write status to JSON file (temp → rename)."""
        tmp = tempfile.NamedTemporaryFile(
            mode="w",
            dir=STATUS_DIR,
            delete=False,
            suffix=".json"
        )
        try:
            json.dump(data, tmp, indent=2)
            tmp.close()
            # Atomic rename
            Path(tmp.name).replace(STATUS_FILE)
        except Exception:
            tmp.close()
            Path(tmp.name).unlink()
            raise

    def update(
        self,
        stage: int,
        status: str,  # "running" | "done" | "failed" | "pending"
        count: Optional[int] = None,
        metric: Optional[str] = None,
        error: Optional[str] = None
    ):
        """Update status for a stage.

        Args:
            stage: Stage number (1, 2, 3, 4)
            status: One of "pending", "running", "done", "failed"
            count: Number of rows/items processed
            metric: Success metric (e.g., "62.8%" for rank-1 hit rate)
            error: Error message if failed
        """
        data = self._read_status()
        if "stages" not in data:
            data["stages"] = {}

        stage_key = f"stage_{stage}"
        data["stages"][stage_key] = {
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "count": count,
            "metric": metric,
            "error": error
        }
        data["last_updated"] = datetime.now().isoformat()
        self._write_status(data)

    def get_status(self, stage: Optional[int] = None) -> dict:
        """Get status for a specific stage or all stages.

        Args:
            stage: Stage number (1-4) or None for all.

        Returns:
            Dict with stage status info.
        """
        data = self._read_status()
        if stage is None:
            return data
        stage_key = f"stage_{stage}"
        return data.get("stages", {}).get(stage_key, {})

    def get_dashboard(self) -> str:
        """Return human-readable emoji dashboard of current progress.

        Example output:
            📥 Stage 1 Decompose: ✅ done — 2,018 components
            📊 Stage 2 Retrieve: ✅ done — 62.8% rank-1
            🧠 Stage 3 LLM Rerank: ⏳ running — 150/1,676 calls
            📤 Stage 4 Aggregate: ⬜ pending
        """
        data = self._read_status()
        stages_info = [
            ("Stage 1", "Decompose", "📥"),
            ("Stage 2", "Retrieve", "📊"),
            ("Stage 3", "LLM Rerank", "🧠"),
            ("Stage 4", "Aggregate", "📤"),
        ]

        lines = [f"🔄 Pipeline: {self.pipeline_name}\n"]
        for i, (stage_num, stage_name, emoji) in enumerate(stages_info, 1):
            status_data = data.get("stages", {}).get(f"stage_{i}", {})
            status = status_data.get("status", "pending")
            metric = status_data.get("metric", "")
            count = status_data.get("count", "")

            # Status emoji
            if status == "done":
                status_emoji = "✅"
            elif status == "running":
                status_emoji = "⏳"
            elif status == "failed":
                status_emoji = "❌"
            else:
                status_emoji = "⬜"

            # Build line
            metric_str = f" — {metric}" if metric else ""
            count_str = f" ({count} items)" if count else ""
            line = f"{emoji} {stage_num} {stage_name}: {status_emoji} {status}{metric_str}{count_str}"
            lines.append(line)

        return "\n".join(lines)

    def can_resume_from(self, stage: int) -> bool:
        """Check if a stage is complete, so we can skip it."""
        status_data = self.get_status(stage)
        return status_data.get("status") == "done"

    def reset(self):
        """Clear all status (for fresh run)."""
        if STATUS_FILE.exists():
            STATUS_FILE.unlink()
