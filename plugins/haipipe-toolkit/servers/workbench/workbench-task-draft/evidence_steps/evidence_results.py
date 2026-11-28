"""What the Runs returned: Result documents, the Result records, the inventory, and what blocks an item."""
from __future__ import annotations

import html
import json
import pathlib
import re
import sys
from src.evidence_labels import parse_result_labels

_RESULT_ITEM = re.compile(
    r"^E\d+-(?:VALUE|TABLE|CITE|DISPLAY)-[a-z0-9]+(?:-[a-z0-9]+)*$", re.I
)


def _top_field(text: str, name: str) -> str:
    match = re.search(rf"(?mi)^{re.escape(name)}:\s*([^#\n]+)", text)
    return match.group(1).strip().strip("'\"") if match else ""


def _result_document(text: str) -> dict[str, object]:
    """Parse a Result envelope without treating its payload as trusted HTML."""
    try:
        value = json.loads(text)
    except (TypeError, ValueError):
        try:
            import yaml
        except ImportError:
            # The Board supervisor may launch system Python while the
            # workspace's .venv owns the optional YAML dependency.
            yaml = None
            anchors = [pathlib.Path.cwd(), *pathlib.Path(__file__).resolve().parents]
            for anchor in anchors:
                venv_lib = anchor / ".venv" / "lib"
                for site in sorted(venv_lib.glob("python*/site-packages")):
                    if not site.is_dir():
                        continue
                    sys.path.insert(0, str(site))
                    try:
                        import yaml
                        break
                    except ImportError:
                        sys.path.pop(0)
                if yaml is not None:
                    break
            if yaml is None:
                return {}
        try:
            value = yaml.safe_load(text)
        except yaml.YAMLError:
            return {}
    return value if isinstance(value, dict) else {}


def _document_text(document: dict[str, object], key: str, text: str) -> str:
    value = document.get(key)
    if isinstance(value, (str, int, float, bool)):
        return str(value).strip()
    return _top_field(text, key)


def _supporting_run_ids(document: dict[str, object], text: str) -> list[str]:
    """Return only owner-native Supporting Run ids for the compact card."""
    values = document.get("supporting_results")
    found = []
    if isinstance(values, list):
        for value in values:
            if isinstance(value, dict) and value.get("run"):
                found.append(str(value["run"]).strip())
            elif isinstance(value, str) and value.strip():
                found.append(value.strip())
    if found:
        return found
    return [value.strip() for value in re.findall(
        r"(?m)^\s*-\s+run:\s*([^#\n]+)", text
    ) if value.strip()]


def _result_records(page_home: pathlib.Path) -> list[dict[str, object]]:
    """Read the current Evidence surface exclusively from Run Results."""
    records: dict[str, dict[str, object]] = {}
    order: list[str] = []

    from src.run_folders import result_roots, under_page_results
    result_root = page_home / "results"
    if result_roots(page_home) and not result_root.is_symlink():   # results/<run>/ or a run's passes
        from src.evidence_selection import selected_for_home
        for manifest in selected_for_home(page_home):
            if manifest.is_symlink() or not under_page_results(page_home, manifest):
                continue
            try:
                text = manifest.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            document = _result_document(text)
            item_id = _document_text(document, "item", text)
            if not _RESULT_ITEM.fullmatch(item_id):
                continue
            kind = (_document_text(document, "type", text)
                    or item_id.split("-", 2)[1].upper())
            status = _document_text(document, "status", text) or "ready"
            owner_run = _document_text(document, "run", text)
            page_run = _document_text(document, "page_run", text)
            folder_name = (manifest.parent.parent.parent.name if manifest.parent.parent.name == "passes"
                           else manifest.parent.name)          # runs/<run>/passes/pNN-<MMDD>/ names the run above
            run_id = page_run or owner_run or folder_name
            bullet = _document_text(document, "bullet", text)
            title = _document_text(document, "title", text)
            label = _document_text(document, "label", text)
            expected = _document_text(document, "expected", text)
            acceptance = _document_text(document, "acceptance", text)
            run_status = ""
            runtime_receipt = manifest.parent / "runtime.yaml"
            if runtime_receipt.is_file():
                try:
                    run_status = _top_field(runtime_receipt.read_text(
                        encoding="utf-8", errors="replace"), "status")
                except OSError:
                    run_status = ""
            labels = parse_result_labels(text)
            for result_label in labels:
                result_label.update({
                    "item": item_id,
                    "page_run": page_run,
                    "run": owner_run,
                    "result": manifest.relative_to(page_home).as_posix(),
                    "provenance": _document_text(document, "provenance", text),
                })
            supporting = _supporting_run_ids(document, text)
            record = records.get(item_id)
            if record is None:
                slug = item_id.split("-", 2)[-1].replace("-", " ")
                record = {"id": item_id, "address": bullet, "title": title or label or slug,
                          "fields": {}}
                records[item_id] = record
                order.append(item_id)
            elif bullet:
                record["address"] = bullet
            if title:
                record["title"] = title
            fields = dict(record.get("fields", {}))
            fields.update({
                "type": kind.upper(),
                "status": status.lower(),
                "run": run_id,
                "run status": run_status,
                "page_run": page_run,
                "owner run": owner_run if page_run and owner_run != page_run else "",
                "bullet": bullet,
                "label": label,
                "expected": expected,
                "acceptance": acceptance,
                "result": manifest.relative_to(page_home).as_posix(),
                "supporting runs": "; ".join(value.strip() for value in supporting),
                "labels": labels,
                "display_kind": (_document_text(document, "display_kind", text)
                                  or (str(document.get("payload", {}).get("display_kind", ""))
                                      if isinstance(document.get("payload"), dict) else "")),
            })
            record["fields"] = fields
            record["result_document"] = document
            record["result_file"] = manifest

    return [records[item_id] for item_id in order]


def _evidence_inventory(page_src: pathlib.Path,
                        records: list[dict[str, object]]) -> list[dict[str, object]]:
    """Combine selected Results with eligible, not-yet-resulted ledger items.

    The Evidence Space remains read-only. Ledger-only entries are explicitly
    marked as planned/specified and never receive a fabricated Run or Result.
    """
    from src.item_table import read_items
    try:
        ledger = read_items(page_src)
    except (OSError, ValueError):
        ledger = {}
    try:
        from live.runs import local_runs
        run_rows = local_runs(page_src)
    except (OSError, ValueError):
        run_rows = []

    runs_by_item: dict[str, list[dict[str, object]]] = {}
    for row in run_rows:
        for item_id in row.get("refs", []):
            runs_by_item.setdefault(str(item_id), []).append(row)

    result_ids = {str(record.get("id", "")).strip() for record in records}
    projected = list(records)
    for record in projected:
        item_id = str(record.get("id", "")).strip()
        item = ledger.get(item_id, {})
        if not str(record.get("address") or "").strip() and str(item.get("target") or "").strip():
            # The Result names no Bullet; the Evidence Markdown's Target does.
            record["address"] = str(item["target"]).strip()
        fields = record.setdefault("fields", {})
        fields.update({
            "item expected": str(item.get("expected", "")).strip(),
            "item acceptance": str(item.get("acceptance", "")).strip(),
            "local input": str(item.get("local_input", "")).strip(),
            "ledger local run": str(item.get("local_run", "")).strip(),
            "ledger run action": str(item.get("action", "")).strip(),
            "ledger run route": str(item.get("address", "")).strip(),
            "ledger result binding": str(item.get("result", "")).strip(),
            "decision": str(item.get("decision", "")).strip(),
            "supporting runs valid": bool(item.get("supports_valid")),
            "local run registered": bool(item.get("runs_registered")),
            "supporting runs": (str(item.get("supporting_runs", "")).strip()
                                 or str(fields.get("supporting runs", "")).strip()),
        })
        matched = runs_by_item.get(item_id, [])
        fields["matching page runs"] = "; ".join(
            "%s · %s" % (row.get("run_id", "unknown"), row.get("status", "unknown"))
            for row in matched
        )
        current_run = str(fields.get("run", "")).strip()
        exact = next((row for row in matched
                      if str(row.get("run_id", "")).strip() == current_run), None)
        if exact:
            fields["run status"] = str(exact.get("status", "unknown"))

    for item_id, item in ledger.items():
        if item_id in result_ids or item.get("type") not in {"VALUE", "CITE", "DISPLAY"}:
            continue
        if item.get("decision") in {"defer", "drop"}:
            continue
        target = str(item.get("target", "")).strip()
        if not target:
            continue
        decision = str(item.get("decision", "")).strip()
        if decision == "make" and item.get("planned"):
            status = "planned"
        elif decision == "make":
            status = "blocked"
        else:
            status = "specified"
        matched = runs_by_item.get(item_id, [])
        fields = {
            "type": str(item.get("type", "")).upper(),
            "status": status,
            "item expected": str(item.get("expected", "")).strip(),
            "item acceptance": str(item.get("acceptance", "")).strip(),
            "local input": str(item.get("local_input", "")).strip(),
            "ledger local run": str(item.get("local_run", "")).strip(),
            "ledger run action": str(item.get("action", "")).strip(),
            "ledger run route": str(item.get("address", "")).strip(),
            "ledger result binding": str(item.get("result", "")).strip(),
            "decision": decision,
            "supporting runs valid": bool(item.get("supports_valid")),
            "local run registered": bool(item.get("runs_registered")),
            "supporting runs": str(item.get("supporting_runs", "")).strip(),
            "matching page runs": "; ".join(
                "%s · %s" % (row.get("run_id", "unknown"), row.get("status", "unknown"))
                for row in matched
            ),
            "run": "; ".join(str(row.get("run_id", "unknown")) for row in matched),
            "run status": "; ".join(str(row.get("status", "unknown")) for row in matched),
            "result": "",
            "no selected result": True,
            "display_kind": "",
        }
        projected.append({
            "id": item_id,
            "address": target,
            "title": str(item.get("name", "")).strip() or item_id,
            "fields": fields,
        })
    return projected


def _evidence_blockers(fields: dict[str, object]) -> list[str]:
    """Name ledger gates that are visibly absent; never infer acceptance."""
    blockers = []
    for key, label in (("item expected", "item Expected contract"),
                       ("item acceptance", "item Acceptance checks"),
                       ("local input", "frozen Local Input")):
        if not str(fields.get(key, "")).strip():
            blockers.append(label + " not recorded")
    if not str(fields.get("decision", "")).strip():
        blockers.append("human Decide choice not recorded")
    if not str(fields.get("ledger local run", "")).strip():
        blockers.append("one local Page RE declaration not recorded")
    elif (not str(fields.get("ledger run action", "")).strip()
          or not str(fields.get("ledger run route", "")).strip()):
        blockers.append("typed Local Run action/route is incomplete")
    if not str(fields.get("supporting runs", "")).strip():
        blockers.append("Supporting Runs not recorded; confirm [] when none are needed")
    elif not fields.get("supporting runs valid") or not fields.get("local run registered"):
        blockers.append("Supporting Run and Local Run declarations are not fully registered")
    return blockers


def _evidence_type(record: dict[str, object]) -> str:
    fields = record.get("fields", {})
    kind = str(fields.get("type", "")).strip().upper()
    if kind == "TABLE":
        return "DISPLAY"
    return kind if kind in {"DISPLAY", "CITE", "VALUE"} else "OTHER"


def _status_parts(record: dict[str, object]) -> tuple[str, str]:
    fields = record.get("fields", {})
    raw = str(fields.get("status", "specified")).strip()
    status = raw.lstrip("📝🔗🟢📌✅⚠️⏸✖⛔ ").lower() or "specified"
    status = {
        "ready_for_human_verification": "Needs review",
        "ready_for_review": "Needs review",
        "ready_for_human_review": "Needs review",
        "in_progress": "In progress",
        "not_started": "Planned",
    }.get(status, status.replace("_", " ").capitalize())
    token = re.sub(r"[^a-z0-9_-]", "-", status.lower())
    return status, token


def _detail_row(label: str, value: str, *, code: bool = False) -> str:
    if not value:
        return ""
    rendered = "<code>%s</code>" % html.escape(value) if code else html.escape(value)
    return ('<div class=evidence-detail-row><span class=evidence-detail-label>%s</span>'
            '<span class=evidence-detail-value>%s</span></div>' %
            (html.escape(label), rendered))


def _evidence_run_contract(kind: str) -> dict[str, str]:
    """Reader-facing Run facts for an Evidence Result card, not a new spec."""
    label = {"VALUE": "Value", "CITE": "Citation", "DISPLAY": "Display"}.get(kind, "Evidence")
    work = {
        "VALUE": "Make one focal value Result for this Evidence Item.",
        "CITE": "Make one focal citation/source-bundle Result for this Evidence Item.",
        "DISPLAY": "Make one focal figure, table, algorithm, or other declared display Result for this Evidence Item.",
    }.get(kind, "Make one typed Result for this Evidence Item.")
    worker = ("workbench-task-draft owns VALUE/CITE/DISPLAY payload rules; use only the exact owner-native "
              "Supporting Run worker(s) selected during SURVEY.")
    if kind == "DISPLAY":
        worker += " DISPLAY also uses the hai-display front door and the renderer Skill selected for its declared display kind."
    return {
        "name": label,
        "work": work,
        "owner": "hai-draft-workflow → hai-evidence",
        "workers": worker,
        "actor": "agent / system / hybrid; any declared human verification remains a human decision",
        "prerequisites": ("Fresh Page Context; accepted Shape and Survey contracts; this item's typed Expected/Acceptance; "
                          "one frozen Local Input and its declared Supporting Runs; human verification when required."),
    }
