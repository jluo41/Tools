"""Read selected Insight work from frozen definitions; never allocate a Run."""
from __future__ import annotations

import json
from pathlib import Path


# Reader labels and surface placement for the Insight controller's own Spec
# templates. Canonical Run Types and workers always come from owner records.
_TEMPLATES = {
    "support": ("Produce the missing source result", "evidence"),
    "evidence": ("Prepare one evidence item", "evidence"),
    "structure": ("Plan the selected Page", "insight"),
    "write": ("Write the selected section or paragraphs", "insight"),
    "deliver": ("Build the selected deliverable", "delivery"),
}
def describe(value) -> str:
    if value in (None, "", [], {}):
        return "not recorded"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
    return str(value)


def people(record: dict) -> tuple[str, str]:
    worker = next((record[key] for key in ("worker_skills", "workers", "worker_skill", "worker")
                   if record.get(key)), None)
    return describe(worker), describe(record.get("actor"))


def reader_name(spec: dict) -> str:
    family = str(spec.get("id", spec.get("run_spec_id", ""))).split(".", 1)[0]
    return str(spec.get("name") or spec.get("label") or _TEMPLATES.get(family, ("Native Run", ""))[0])


def definition(board: Path, runtime: dict) -> dict:
    """Read only the frozen definition this Runtime names (its version is in the file name)."""
    import yaml
    directory = (board / runtime["path"]).parent.resolve()
    ref = runtime.get("definition")
    if not isinstance(ref, str) or not ref or ref == "not recorded":
        raise ValueError("frozen definition path is not recorded")
    path = (directory / ref).resolve()
    if not path.is_relative_to(directory):
        raise ValueError("frozen definition must remain inside its Runtime directory")
    data = yaml.safe_load(path.read_bytes())
    if not isinstance(data, dict) or data.get("schema") != "haipipe.insight-definition/v1" \
            or data.get("workflow_id") != "hai-insight-workflow":
        raise ValueError("unsupported Insight definition")
    specs, targets = data.get("run_specs"), data.get("requested_answer_targets")
    if not isinstance(specs, list) or not isinstance(targets, list):
        raise ValueError("definition must list run_specs and requested_answer_targets")
    if any(not isinstance(target, dict) for target in targets):
        raise ValueError("definition answer targets must be records")
    ids = [s.get("id") for s in specs if isinstance(s, dict)]
    if len(ids) != len(specs) or any(not isinstance(i, str) or not i for i in ids) or len(set(ids)) != len(ids):
        raise ValueError("definition has missing or duplicate Spec identities")
    return data
