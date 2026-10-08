"""Select current Evidence Results from the authored Item ledger, never file order."""
from pathlib import Path

from .outline_version import plan_dir


class EvidenceSelectionError(ValueError):
    pass


def legacy_profile(page_src):
    """Only Pages without an authored Item ledger use the migration reader."""
    from .item_table import items_path
    return not items_path(Path(page_src)).is_file()


def page_head(page_src, key):
    """A `key: value` line from the Page Face head (above its first `## `), or ''."""
    import re
    try:
        head = Path(page_src).read_text(encoding="utf-8", errors="replace").split("\n## ", 1)[0]
    except OSError:
        return ""
    m = re.search(r"(?m)^%s:[ \t]*(.*?)\s*$" % re.escape(key), head)
    return m.group(1) if m else ""


def draft_delivery(page_src):
    """`delivery: draft` in the Page head: a Page still at SHAPE may export.

    Its items that are only specified (no Local Run, no Result, Decide not
    signed) are not bindings yet, so they do not block the export; the export
    lists them as pending in evidence-selection.json. A signed or planned
    item with a missing Result still blocks, exactly as without the key."""
    return page_head(page_src, "delivery").lower() == "draft"


def _only_specified(row):
    return (not row.get("decision") and not str(row.get("local_run") or "").strip()
            and not str(row.get("result") or "").strip())


def pending_items(page_src):
    """The specified-only items a `delivery: draft` export leaves out, in ledger order."""
    from .item_table import read_items
    if not draft_delivery(page_src) or legacy_profile(page_src):
        return []
    return [item for item, row in read_items(Path(page_src)).items() if _only_specified(row)]


def _unbound_manifests(home, *, strict=False):
    """Compatibility inspection for pre-ledger Pages; ambiguous items stay unresolved."""
    from .page_evidence import _result_document
    root = home / "results"
    if root.is_symlink() or not root.is_dir():
        return []
    by_item = {}
    for manifest in sorted(root.rglob("result.yaml")):
        if manifest.is_symlink():
            continue
        try:
            manifest.resolve().relative_to(root.resolve())
        except (OSError, ValueError):
            continue
        item = str(_result_document(manifest).get("item") or manifest)
        by_item.setdefault(item, []).append(manifest)
    duplicates = [item for item, paths in by_item.items() if len(paths) > 1]
    if strict and duplicates:
        raise EvidenceSelectionError("Ambiguous historical Results; bind one Result in the Evidence Item ledger: " + ", ".join(duplicates))
    return [paths[0] for paths in by_item.values() if len(paths) == 1]


RECEIPT_OK = {"ok", "ready", "complete", "completed", "accepted", "resolved"}


def run_receipt(path):
    """The ticket receipt that vouches for a run's output file, or None.

    A run ticket writes `results/<run>/` and its `runtime.yaml` (status, spec and script
    hashes, outputs). A VALUE or CITE item that binds one of those output files directly is
    bound to that receipt: an Insight answering Page binds `results/<partition>/<table>.csv`,
    and a cite binds another Page's run file the same way (JL 261004: Insight pages export
    to LaTeX and Word). Returns (receipt path, status)."""
    path = Path(path)
    for folder in path.parents:
        if folder.parent.name == "results":
            receipt = folder / "runtime.yaml"
            if not receipt.is_file():
                return None
            import re
            m = re.search(r"(?m)^status:\s*['\"]?([\w-]+)", receipt.read_text(encoding="utf-8", errors="replace"))
            return receipt, (m.group(1).lower() if m else "")
        if folder.name == "results":
            return None
    return None


def selected_results(page_src, *, strict=True, errors=None):
    from .item_table import items_path, read_items, repo_root, resolve
    from .page_evidence import _result_document
    page_src = Path(page_src)
    ledger = items_path(page_src)
    results = page_src.parent / "results"
    if not ledger.is_file():
        return _unbound_manifests(page_src.parent, strict=strict)
    if results.is_symlink():
        if strict:
            raise EvidenceSelectionError("The Page Results root must be local, not a symlink")
        if errors is not None:
            for item, row in read_items(page_src).items():
                if row.get("decision") in {"drop", "defer"}:
                    continue
                ref = str(row.get("result") or "").strip().strip(chr(96))
                errors.append({
                    "item": item,
                    "type": row.get("type", ""),
                    "reference": ref,
                    "error": "The Page Results root must be local, not a symlink",
                })
        return []
    selected = []
    draft = draft_delivery(page_src)
    for item, row in read_items(page_src).items():
        if row.get("decision") in {"drop", "defer"}:
            continue
        if draft and _only_specified(row):
            continue  # pending: listed by pending_items(), never a binding yet
        ref = str(row.get("result") or "").strip().strip(chr(96))
        try:
            path = resolve(ref, repo_root(page_src.parent), page_src.parent)
            if path is None:
                raise EvidenceSelectionError(f"{item}: selected Result is missing ({ref or 'no Result binding'})")
            path = Path(path).resolve()
            if path.is_file() and path.name != "result.yaml" and row["type"] in {"VALUE", "CITE"}:
                bound = run_receipt(path)
                if bound is None:
                    raise EvidenceSelectionError(f"{item}: a bound run file needs its run's runtime.yaml receipt")
                if row["type"] == "VALUE":
                    path.relative_to(results.resolve())          # a value comes from this Page's own runs
                if strict and bound[1] not in RECEIPT_OK:
                    raise EvidenceSelectionError(f"{item}: the bound run is not ok ({bound[1] or 'missing status'})")
                continue                                         # receipt-bound: no manifest to select
            if path.is_dir():
                path /= "result.yaml"
            path = path.resolve()
            path.relative_to(results.resolve())
            if path.name != "result.yaml" or not path.is_file():
                raise EvidenceSelectionError(f"{item}: bind an exact local result.yaml")
            document = _result_document(path)
            kind = str(document.get("type", "")).upper()
            if kind == "TABLE":
                kind = "DISPLAY"
            if document.get("item") != item or kind != row["type"]:
                raise EvidenceSelectionError(f"{item}: selected Result identity/type does not match the ledger")
            owner = row.get("address", "").strip("`")
            if owner and owner not in {str(document.get("page_run", "")), str(document.get("run", ""))}:
                raise EvidenceSelectionError(f"{item}: selected Result does not belong to the ledger's Local Run ({owner})")
            status = str(document.get("status", "")).lower()
            if strict and status not in {"ready", "complete", "completed", "accepted", "resolved"}:
                raise EvidenceSelectionError(f"{item}: selected Result is not ready ({status or 'missing status'})")
            acceptance = document.get("acceptance")
            if strict and isinstance(acceptance, dict) and acceptance.get("passed") is False:
                raise EvidenceSelectionError(f"{item}: selected Result failed acceptance")
            if strict and row["type"] == "CITE" and not row.get("verification_signed"):
                raise EvidenceSelectionError(f"{item}: CITE verification is missing")
            selected.append(path)
        except (OSError, ValueError) as exc:
            if strict:
                if isinstance(exc, EvidenceSelectionError):
                    raise
                raise EvidenceSelectionError(f"{item}: invalid selected Result: {exc}") from exc
            if errors is not None:
                errors.append({
                    "item": item,
                    "type": row.get("type", ""),
                    "reference": ref,
                    "error": str(exc),
                })
    if strict:
        from .evidence_labels import parse_result_labels, label_aliases
        labels = {}
        for manifest in selected:
            for label in parse_result_labels(manifest.read_text(encoding="utf-8")):
                for alias in label_aliases(label):
                    if alias in labels and labels[alias] != manifest:
                        raise EvidenceSelectionError(f"Ambiguous current Evidence Label: {alias}")
                    labels[alias] = manifest
    return selected


def selected_for_home(page_home):
    """Read-only projections tolerate missing Results but never bind an older one."""
    home = Path(page_home)
    ledgers = list((plan_dir(home)).glob("*-evidence-items.md"))
    if not ledgers:
        return _unbound_manifests(home)
    if len(ledgers) != 1:
        return []
    stem = ledgers[0].name.removesuffix("-evidence-items.md")
    return selected_results(home / (stem + ".md"), strict=False)
