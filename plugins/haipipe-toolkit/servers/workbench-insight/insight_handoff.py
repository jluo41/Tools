"""Read current handoff eligibility from exact owner receipts; never grant it."""
from __future__ import annotations

import hashlib
from pathlib import Path
import re


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


def pinned_bytes(folder: Path, reference: dict) -> bytes:
    """Read a whole file or one explicitly anchored Markdown log record."""
    if not isinstance(reference, dict) or not isinstance(reference.get("path"), str):
        raise ValueError("missing pinned source path")
    name, _, anchor = reference["path"].partition("#")
    path = Path(name)
    if not path.is_absolute():
        path = folder / path
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
    if hashlib.sha256(content).hexdigest() != reference.get("sha256"):
        raise ValueError(f"source or receipt changed: {reference['path']}")
    return content


def _control(folder: Path, reference: dict, key: str, page_pin: dict) -> dict:
    import yaml
    content = pinned_bytes(folder, reference).decode("utf-8")
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
    # just like the index. Receipts pin a version and bytes, not `latest`.
    if record.get("page") != page_pin:
        raise ValueError(f"{key} does not bind this exact Page version/hash")
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
        pinned_bytes(folder, pin)
        dependencies = record.get("dependencies")
        if not isinstance(dependencies, list) or not dependencies:
            raise ValueError("handoff dependencies have not been pinned")
        for dependency in dependencies:
            pinned_bytes(folder, dependency)
        signed = _control(folder, record.get("gi5"), "GI5", pin)
        if signed.get("signature") != signature:
            raise ValueError("person signature differs from the GI5 record")
        if signed.get("dependencies") != dependencies:
            raise ValueError("GI5 does not bind the recorded dependencies")
        result["signature_current"] = True
        refs = record.get("gi6", [])
        refs = refs if isinstance(refs, list) else [refs]
        questions = set(re.findall(r"\bQW\d+\b", serves))
        settled_questions = set()
        for ref in refs:
            settled = _control(folder, ref, "GI6", pin)
            if settled.get("signature_receipt") != record.get("gi5"):
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
