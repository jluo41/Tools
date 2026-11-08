"""The items Task's one worker: every Run (describe, items, embed) goes to haipipe-labeling-preparation's
engine, items_task.py, by its config's `operation`. Written by `items_task.py plan`; edit the engine, not this."""
import sys
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "env.sh").is_file())
sys.path.insert(0, str(ROOT / "Tools/plugins/haipipe-toolkit/skills/2_theme/labeling/engine"))
import items_task  # noqa: E402

items_task.worker_main()
