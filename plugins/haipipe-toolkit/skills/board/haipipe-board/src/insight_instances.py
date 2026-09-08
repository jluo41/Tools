"""Project Insight item Results into the existing Supporting Run registry.

The skill owns the schema and validator. This module only discovers instance
manifests and presents their checked item executions; it creates no state.
"""
from functools import lru_cache
import importlib.util
from html import escape
from pathlib import Path


@lru_cache(maxsize=1)
def contract():
    path = (Path(__file__).resolve().parents[3] / "task/page-types/haipipe-page-insight/scripts/insight_items.py")
    spec = importlib.util.spec_from_file_location("haipipe_insight_items", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def instance_manifests(root):
    root = Path(root)
    candidates = set(root.glob("*/workflow/insight.yaml"))
    if (root / "workflow/insight.yaml").is_file():
        candidates.add(root / "workflow/insight.yaml")
    for name in ("examples", "examples-nlp", "diagram", "board", "insights"):
        if (root / name).is_dir():
            candidates.update((root / name).glob("**/workflow/insight.yaml"))
    return sorted(candidates)


def register_instances(root, records):
    api = contract()
    for path in instance_manifests(root):
        folder = path.parent.parent
        try:
            manifest = api.read_yaml(path)
            if manifest.get("schema") != "haipipe.insight-instance/v1":
                continue
            if not api.INSTANCE.fullmatch(str(manifest.get("instance", ""))):
                continue
            for item in manifest.get("items", []):
                run = item.get("run", "")
                if not api.RUN.fullmatch(run):
                    continue
                ticket = folder / "runs" / f"{run}.sh"
                if not ticket.is_file():
                    continue
                for directory in sorted((folder / "results" / run).glob("v*")):
                    if not directory.is_dir() or not api.VERSION.fullmatch(directory.name):
                        continue
                    info, _ = api.execution(folder, manifest, item, directory)
                    ident = info["execution"]
                    ready = info["valid"] and info["outcome"] == "accepted" and not info["stale"]
                    status = "complete" if ready else "rerun"
                    if info["valid"] and info["status"] in {"planned", "running"}:
                        status = "ticket"
                    record = {
                        "status": status,
                        "label": {"complete": "Done", "ticket": "Run only", "rerun": "Rerun"}[status],
                        "ticket": str(ticket), "runtime": str(directory / "runtime.yaml"),
                        "result": str(directory / "result.yaml") if ready else "",
                        "family": "Insight", "target": item.get("question", ""),
                        "task_root": str(folder),
                    }
                    if ident in records:
                        # Duplicate instance identities must not silently pick a patient.
                        record.update(status="rerun", label="Duplicate identity", result="")
                    records[ident] = record
        except (OSError, ValueError, TypeError, KeyError, AttributeError, api.yaml.YAMLError):
            continue  # malformed manifests are reported by the explicit item checker


def render_items(page_src):
    """Render the skill-owned item table in the Page's existing Outline."""
    if page_src is None or not Path(page_src).is_file():
        return ""
    folder = Path(page_src).parent
    if not (folder / "workflow/insight.yaml").is_file():
        return ""
    api = contract()
    try:
        _manifest, rows, errors = api.inspect(folder)
        heads = "".join(f"<th>{escape(value)}</th>" for value in api.TABLE_HEADERS)
        content = "".join("<tr>" + "".join(f"<td>{escape(str(v))}</td>" for v in values) + "</tr>"
                          for values in api.table_rows(rows))
        warning = (f'<p class="mut">{len(errors)} item validation finding(s); inspect receipts before reuse.</p>'
                   if errors else "")
        return (f'{warning}<div class="outline-grid-wrap"><table class="outline-grid insight-items">'
                f'<thead><tr>{heads}</tr></thead><tbody>{content}</tbody></table></div>')
    except (OSError, ValueError, TypeError, KeyError, AttributeError, api.yaml.YAMLError) as exc:
        return f'<p class="mut">Insight item table unavailable: {escape(str(exc))}</p>'
