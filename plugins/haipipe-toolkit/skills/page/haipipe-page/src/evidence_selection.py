"""Select current Evidence Results from the authored Item ledger, never file order."""
from pathlib import Path


class EvidenceSelectionError(ValueError):
    pass


def legacy_profile(page_src):
    """Only Pages without an authored Item ledger use the migration reader."""
    from .item_table import items_path
    return not items_path(Path(page_src)).is_file()


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
    for item, row in read_items(page_src).items():
        if row.get("decision") in {"drop", "defer"}:
            continue
        ref = str(row.get("result") or "").strip().strip(chr(96))
        try:
            path = resolve(ref, repo_root(page_src.parent), page_src.parent)
            if path is None:
                raise EvidenceSelectionError(f"{item}: selected Result is missing ({ref or 'no Result binding'})")
            path = Path(path).resolve()
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
    ledgers = list((home / "outline").glob("*-evidence-items.md"))
    if not ledgers:
        return _unbound_manifests(home)
    if len(ledgers) != 1:
        return []
    stem = ledgers[0].name.removesuffix("-evidence-items.md")
    return selected_results(home / (stem + ".md"), strict=False)
