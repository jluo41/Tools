"""Read current handoff eligibility from exact owner receipts; never grant it."""
from __future__ import annotations

from pathlib import Path
import re


def _plain(value):
    """Ignore hash fields left in older records (JL 260928: no content hashes)."""
    if isinstance(value, dict):
        return {k: _plain(v) for k, v in value.items()
                if k not in {"sha256", "hash"} and not str(k).endswith(("_sha256", "_hash"))}
    if isinstance(value, list):
        return [_plain(v) for v in value]
    return value


def watch_paths(board: Path) -> list[Path]:
    """Expose recorded external dependencies to the read-only snapshot cache."""
    paths = []
    try:
        import yaml
    except ImportError:
        return paths
    for index in board.rglob("workflow/handoff.yaml"):
        paths.append(index)
        try:
            record = yaml.safe_load(index.read_text(encoding="utf-8"))
            if not isinstance(record, dict):
                continue
            gi6 = record.get("gi6", [])
            refs = [record.get("page"), record.get("gi5")]
            refs += gi6 if isinstance(gi6, list) else [gi6]
            refs += record.get("dependencies", []) if isinstance(record.get("dependencies"), list) else []
            for ref in refs:
                if isinstance(ref, dict) and isinstance(ref.get("path"), str):
                    paths.append(index.parent.parent / ref["path"].partition("#")[0])
        except (OSError, UnicodeError, yaml.YAMLError):
            continue
    return paths


def _source_path(folder: Path, reference: dict) -> tuple[Path, str]:
    if not isinstance(reference, dict) or not isinstance(reference.get("path"), str):
        raise ValueError("missing recorded source path")
    name, _, anchor = reference["path"].partition("#")
    path = Path(name)
    return (path if path.is_absolute() else folder / path), anchor


def recorded_bytes(folder: Path, reference: dict) -> bytes:
    """Read a whole file or one explicitly anchored Markdown log record."""
    path, anchor = _source_path(folder, reference)
    content = path.read_bytes()
    if anchor:
        text = content.decode("utf-8")
        matches = list(re.finditer(rf"(?m)^(#{{2,6}}) {re.escape(anchor)}[ \t]*$", text))
        if len(matches) != 1:
            raise ValueError(f"missing or ambiguous receipt anchor {reference['path']}")
        match = matches[0]
        tail = text[match.end():]
        end = re.search(rf"(?m)^#{{1,{len(match[1])}}} ", tail)
        content = tail[:end.start() if end else len(tail)].strip().encode("utf-8")
    return content


def changed_after(folder: Path, reference: dict, receipt: dict) -> bool:
    """Staleness by file time: a whole-file source modified after the receipt file.

    An anchored log record is not compared, because appending a later record
    to the same log moves the file time without changing this one.
    """
    path, anchor = _source_path(folder, reference)
    if anchor:
        return False
    signed, _ = _source_path(folder, receipt)
    return path.stat().st_mtime > signed.stat().st_mtime


def _control(folder: Path, reference: dict, key: str, page_pin: dict) -> dict:
    import yaml
    content = recorded_bytes(folder, reference).decode("utf-8")
    fenced = re.search(r"(?ms)^```yaml\s*\n(.*?)^```\s*$", content)
    record = yaml.safe_load(fenced[1] if fenced else content)
    if not isinstance(record, dict) or record.get("key") != key or record.get("status") != "passed":
        raise ValueError(f"{key} has no passed owner receipt")
    if not record.get("actor") or not record.get("workflow_runtime_id"):
        raise ValueError(f"{key} lacks its actor or Runtime binding")
    expected_owner = "haipipe-insight-wisdom" if key == "GI5" else "haipipe-insight-question"
    if record.get("authority") != expected_owner:
        raise ValueError(f"{key} has the wrong resource owner")
    # Page addresses in receipts are resolved relative to the Wisdom Folder,
    # just like the index. Receipts name an exact version, not `latest`.
    if _plain(record.get("page")) != _plain(page_pin):
        raise ValueError(f"{key} does not bind this exact Page version")
    return record


def eligibility(page: dict, signature: str, serves: str) -> dict:
    result = {"bindable": False, "signature_current": False,
              "eligibility": "unverified", "eligibility_reason": "no current handoff binding record"}
    if not signature:
        return {**result, "eligibility": "unsigned", "eligibility_reason": "awaiting person signature"}
    if page.get("identity_error"):
        return {**result, "eligibility_reason": page["identity_error"]}
    if not page.get("state", "").startswith("✅") or "🧊" in page["text"]:
        return {**result, "eligibility": "stale", "eligibility_reason": "Page is open, held, or marked stale"}
    folder = page["path"].parent
    index = folder / "workflow/handoff.yaml"
    if not index.is_file():
        return result
    try:
        import yaml
        record = yaml.safe_load(index.read_text(encoding="utf-8"))
        if not isinstance(record, dict) or record.get("schema") != "haipipe.insight-handoff/v1":
            raise ValueError("invalid handoff binding schema")
        pin = record.get("page", {})
        if not isinstance(pin, dict) or not pin.get("version") or pin["version"] == "latest":
            raise ValueError("handoff needs an exact Page version")
        if (folder / pin.get("path", "")).resolve() != page["path"].resolve():
            raise ValueError("handoff binding names another Page")
        recorded_bytes(folder, pin)
        dependencies = record.get("dependencies")
        if not isinstance(dependencies, list) or not dependencies:
            raise ValueError("handoff dependencies have not been recorded")
        for dependency in dependencies:
            recorded_bytes(folder, dependency)
        signed = _control(folder, record.get("gi5"), "GI5", pin)
        if signed.get("signature") != signature:
            raise ValueError("person signature differs from the GI5 record")
        if _plain(signed.get("dependencies")) != _plain(dependencies):
            raise ValueError("GI5 does not bind the recorded dependencies")
        for source in [pin, *dependencies]:
            if changed_after(folder, source, record.get("gi5")):
                return {**result, "eligibility": "stale",
                        "eligibility_reason": f"{source['path']} changed after the GI5 signature (file time)"}
        result["signature_current"] = True
        refs = record.get("gi6", [])
        refs = refs if isinstance(refs, list) else [refs]
        questions = set(re.findall(r"\bQW\d+\b", serves))
        settled_questions = set()
        for ref in refs:
            settled = _control(folder, ref, "GI6", pin)
            if _plain(settled.get("signature_receipt")) != _plain(record.get("gi5")):
                raise ValueError("GI6 does not reference this exact signature receipt")
            target = settled.get("target", {})
            if target.get("question") not in questions or target.get("partition") != (page.get("partition") or "F"):
                raise ValueError("GI6 settles a different question or partition")
            settled_questions.add(target["question"])
        if not questions or settled_questions != questions:
            raise ValueError("GI6 is missing for a served question")
        return {**result, "bindable": True, "eligibility": "current",
                "eligibility_reason": "exact signed payload, dependencies and GI6 receipt are current"}
    except (ImportError, OSError, UnicodeError, ValueError, TypeError, KeyError, AttributeError) as exc:
        return {**result, "eligibility_reason": str(exc)}
    except Exception as exc:
        # PyYAML is optional for the presenter; malformed YAML remains a
        # visible unverified binding, never a signature-presence fallback.
        if exc.__class__.__module__.startswith("yaml"):
            return {**result, "eligibility_reason": str(exc)}
        raise
