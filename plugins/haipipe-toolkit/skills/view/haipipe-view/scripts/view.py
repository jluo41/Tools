#!/usr/bin/env python3
"""Create, validate, build, and summarize a canonical Haipipe View Page."""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from typing import Iterable


HERE = pathlib.Path(__file__).resolve().parent
MANIFEST_TEMPLATE = HERE.parent / "assets" / "view-template" / "manifest.json"
PAGE_TEMPLATE = (
    HERE.parents[1]
    / "page-types"
    / "haipipe-page-for-view"
    / "assets"
    / "view-page-template.md"
)
VIEW_STEM_RE = re.compile(
    r"^(?P<page_id>Q[A-Za-z]*[1-9][0-9]*[a-z]?|S-[A-Za-z0-9]+-[1-9][0-9]*[a-z]?)"
    r"-[a-z0-9]+(?:-[a-z0-9]+)*$"
)
CARD_RE = re.compile(r"(?m)^>\s*Card\s+(.+?)\s*[:：]\s*(.+)$")
CITE_RE = re.compile(r"\\cite[tp]?\{([^}]+)\}")
IMAGE_RE = re.compile(r"^!\[[^]]*\]\(([^)]+)\)\s*$")
REQUIRED_DIVISIONS = (
    "### 1 · QA inputs",
    "### 2 · View body",
    "### 3 · Displays",
    "### 4 · Consumers",
)
DISPLAY_KINDS = ("table", "figure", "diagram", "illustration", "text", "ledger")
DISPLAY_UNIT_CONTRACT = "display-unit-output-v1"
DISPLAY_REQUIRED_FILES = (
    "README.md",
    "output.md",
    "intake/manifest.yaml",
    "float.tex",
    "preview.tex",
)
DISPLAY_REQUIRED_DIRS = ("intake", "recipe", "candidates", "assets", "versions")


class ViewError(Exception):
    pass


def read_json(path: pathlib.Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ViewError(f"missing manifest: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ViewError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ViewError(f"manifest must be one JSON object: {path}")
    return value


def view_paths(page: pathlib.Path) -> tuple[pathlib.Path, pathlib.Path]:
    page = page.resolve()
    return page, page.parent / "views" / page.stem


def resolve_from(unit: pathlib.Path, value: str) -> pathlib.Path:
    candidate = pathlib.Path(value)
    if candidate.is_absolute():
        return candidate.resolve()
    direct = (unit / candidate).resolve()
    if direct.exists():
        return direct
    for ancestor in unit.parents:
        trial = (ancestor / candidate).resolve()
        if trial.exists():
            return trial
    return direct


def content_block(page_text: str) -> str:
    match = re.search(r"(?ms)^## Content\s*$\n(.*?)(?=^##\s|\Z)", page_text)
    if not match:
        raise ViewError("canonical Page is missing ## Content")
    return match.group(1).strip() + "\n"


def manifest_lists(manifest: dict) -> tuple[dict, list, list]:
    inputs = manifest.get("inputs", {})
    displays = manifest.get("displays", [])
    consumers = manifest.get("consumers", [])
    if not isinstance(inputs, dict):
        raise ViewError("manifest inputs must be an object")
    if not isinstance(displays, list) or not isinstance(consumers, list):
        raise ViewError("manifest displays and consumers must be arrays")
    for key in ("qa_probes", "sources"):
        if not isinstance(inputs.get(key, []), list):
            raise ViewError(f"manifest inputs.{key} must be an array")
    return inputs, displays, consumers


def build_config(manifest: dict) -> dict:
    value = manifest.get("build", {})
    if not isinstance(value, dict):
        raise ViewError("manifest build must be an object")
    fixture_root = value.get("fixture_root")
    formats = value.get("formats", [])
    if not isinstance(fixture_root, str) or not fixture_root.strip():
        raise ViewError("manifest build.fixture_root must be a non-empty path")
    if formats != ["tex", "pdf", "docx"]:
        raise ViewError("manifest build.formats must be [tex, pdf, docx]")
    return value


def fixture_root(unit: pathlib.Path, manifest: dict, override: pathlib.Path | None = None) -> pathlib.Path:
    if override is not None:
        target = override.resolve()
    else:
        target = (unit / build_config(manifest)["fixture_root"]).resolve()
    if target == unit or unit in target.parents:
        raise ViewError("fixture root must be outside the authored View resource folder")
    return target


def yaml_scalar(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*[\"']?([^\n\"']+?)[\"']?\s*$", text)
    return match.group(1).strip() if match else None


def directory_digest(root: pathlib.Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        label = path.relative_to(root).as_posix()
        value = hashlib.sha256(path.read_bytes()).hexdigest()
        digest.update(label.encode("utf-8") + b"\0" + value.encode("ascii") + b"\n")
    return digest.hexdigest()


def validate_display_unit(output: pathlib.Path, row: dict, errors: list[str]) -> None:
    display_id = row.get("id", "")
    if row.get("unit_contract") != DISPLAY_UNIT_CONTRACT:
        errors.append(f"{display_id} unit_contract must be {DISPLAY_UNIT_CONTRACT}")
    for name in DISPLAY_REQUIRED_FILES:
        if not (output / name).is_file():
            errors.append(f"Display lacks {name}: output/{output.name}")
    for name in DISPLAY_REQUIRED_DIRS:
        if not (output / name).is_dir():
            errors.append(f"Display lacks {name}/: output/{output.name}")

    intake = output / "intake" / "manifest.yaml"
    if intake.is_file():
        text = intake.read_text(encoding="utf-8")
        if yaml_scalar(text, "display_id") != display_id:
            errors.append(f"Display intake display_id must be {display_id}: output/{output.name}")
        if yaml_scalar(text, "kind") != row.get("kind"):
            errors.append(f"Display intake kind must match the View manifest: output/{output.name}")
        if row.get("status") in ("rendered", "current") and re.search(r"\bTODO\b", text):
            errors.append(f"rendered Display intake contains TODO: output/{output.name}")

    if row.get("status") in ("rendered", "current"):
        assets = output / "assets"
        if assets.is_dir() and not any(
            path.is_file() and path.name != ".gitkeep" for path in assets.rglob("*")
        ):
            errors.append(f"rendered Display has no winning asset: output/{output.name}/assets")
        float_path = output / "float.tex"
        if float_path.is_file() and re.search(
            r"\b(?:TODO|pending)\b", float_path.read_text(encoding="utf-8"), re.IGNORECASE
        ):
            errors.append(f"rendered Display float is still pending: output/{output.name}/float.tex")


def validate(page: pathlib.Path) -> tuple[dict, list[str], list[str]]:
    page, unit = view_paths(page)
    errors: list[str] = []
    warnings: list[str] = []
    if not page.is_file():
        return {}, [f"missing canonical View Page: {page}"], warnings
    match = VIEW_STEM_RE.fullmatch(page.stem)
    if not match:
        errors.append(f"invalid View Page stem {page.stem!r}")
        page_id = ""
    else:
        page_id = match.group("page_id")
    try:
        manifest = read_json(unit / "manifest.json")
        inputs, displays, consumers = manifest_lists(manifest)
        build_config(manifest)
    except ViewError as exc:
        return {}, errors + [str(exc)], warnings

    if manifest.get("schema_version") != 2:
        errors.append("schema_version must be 2")
    if manifest.get("id") != page.stem:
        errors.append("manifest id must equal the canonical Page stem")
    if manifest.get("page_id") != page_id:
        errors.append(f"manifest page_id must be {page_id!r}")
    if unit.name != page.stem:
        errors.append("View resource folder must equal the canonical Page stem")
    page_source = manifest.get("page_source", "")
    if not isinstance(page_source, str) or resolve_from(unit, page_source) != page:
        errors.append("page_source must resolve to the canonical View Page")
    if manifest.get("acceptance") not in ("waiting", "accepted", "reopened"):
        errors.append("acceptance must be waiting, accepted, or reopened")
    if not isinstance(manifest.get("title"), str) or not manifest.get("title", "").strip():
        errors.append("title must be a non-empty string")

    page_text = page.read_text(encoding="utf-8")
    try:
        body = content_block(page_text)
    except ViewError as exc:
        errors.append(str(exc))
        body = ""
    for heading in REQUIRED_DIVISIONS:
        if heading not in body:
            errors.append(f"canonical Page Content is missing {heading}")

    qa_probes = inputs.get("qa_probes", [])
    if not qa_probes:
        errors.append("declare at least one answered Probe in inputs.qa_probes")
    for group in ("qa_probes", "sources"):
        seen: set[str] = set()
        for value in inputs.get(group, []):
            if not isinstance(value, str):
                errors.append(f"inputs.{group} entries must be strings")
                continue
            if value in seen:
                errors.append(f"duplicate inputs.{group} path: {value}")
            seen.add(value)
            path = resolve_from(unit, value)
            try:
                path.relative_to(unit)
            except ValueError:
                errors.append(f"inputs.{group} must stay inside the View resource folder: {value}")
            if not path.is_file():
                errors.append(f"missing inputs.{group} file: {value}")
    if any("input/probes/" in value for value in qa_probes if isinstance(value, str)):
        errors.append("use input/QA-probes/, not input/probes/")

    display_ids: set[str] = set()
    numbers: set[int] = set()
    for row in displays:
        if not isinstance(row, dict):
            errors.append("each Display must be an object")
            continue
        display_id = row.get("id", "")
        id_match = re.fullmatch(rf"{re.escape(page_id)}-Display([1-9][0-9]*)", display_id) \
            if page_id and isinstance(display_id, str) else None
        if not id_match:
            errors.append(f"invalid Display id {display_id!r}; expected {page_id}-Display<n>")
        elif display_id in display_ids:
            errors.append(f"duplicate Display id: {display_id}")
        else:
            display_ids.add(display_id)
            numbers.add(int(id_match.group(1)))
        folder = row.get("folder", "")
        output = unit / "output" / folder if isinstance(folder, str) else unit / "output"
        if not isinstance(folder, str) or not re.fullmatch(
            rf"{re.escape(display_id)}-[a-z0-9]+(?:-[a-z0-9]+)*", folder
        ):
            errors.append(f"Display folder must be {display_id}-<lowercase-slug>")
        if not output.is_dir():
            errors.append(f"missing Display folder: output/{folder}")
            continue
        validate_display_unit(output, row, errors)
        if row.get("status") in ("rendered", "current"):
            for required in (row.get("preview_image", "preview.png"), row.get("preview_pdf", "preview.pdf")):
                if not isinstance(required, str) or not (output / required).is_file():
                    errors.append(f"rendered Display lacks {required}: output/{folder}")
            page_reference = f"views/{page.stem}/output/{folder}/{row.get('preview_image', 'preview.png')}"
            if page_reference not in page_text:
                errors.append(f"Display preview is not embedded in the canonical Page: {page_reference}")
        if row.get("kind") not in DISPLAY_KINDS:
            errors.append(f"{display_id} kind must name a supported Display kind")
        if not isinstance(row.get("reader_job"), str) or not row.get("reader_job", "").strip():
            errors.append(f"{display_id} reader_job must be non-empty")
        if row.get("status") not in ("planned", "sourced", "rendered", "current", "stale"):
            errors.append(f"{display_id} has an invalid status")
        if row.get("acceptance") not in ("waiting", "accepted", "reopened"):
            errors.append(f"{display_id} acceptance must be waiting, accepted, or reopened")
        if not isinstance(row.get("body_bindings", []), list):
            errors.append(f"{display_id} body_bindings must be an array")
    if numbers and numbers != set(range(1, max(numbers) + 1)):
        warnings.append("Display ids have gaps; legal, but intentional only")

    for row in consumers:
        if not isinstance(row, dict):
            errors.append("each Consumer must be an object")
            continue
        cid = row.get("id", "")
        if not re.fullmatch(r"C[1-9][0-9]*", cid) if isinstance(cid, str) else True:
            errors.append(f"invalid Consumer id {cid!r}; expected C<n>")
        target = row.get("target", "")
        if not isinstance(target, str) or not (unit / target).resolve().is_file():
            errors.append(f"missing Consumer target for {cid}: {target}")
        uses = row.get("uses", [])
        if not isinstance(uses, list) or not uses:
            errors.append(f"{cid} uses must be a non-empty array")
        elif any(value != page.stem and value not in display_ids for value in uses):
            errors.append(f"{cid} uses an unknown View or Display")
        if row.get("status") not in ("planned", "linked", "handed-off", "stale"):
            errors.append(f"{cid} has an invalid status")
        if not isinstance(row.get("placement"), str) or not row.get("placement", "").strip():
            errors.append(f"{cid} placement must be non-empty")

    cards = CARD_RE.findall(body)
    if not cards:
        warnings.append("canonical Page Content contains no exact-span Card annotations")
    for anchor, payload in cards:
        clause = re.search(
            r"\bBindings?:\s*((?:`[^`]+`(?:\s*,\s*)?)+)", payload
        )
        bindings = re.findall(r"`([^`]+)`", clause.group(1)) if clause else []
        if re.search(r"\bBindings?:", payload) and not bindings:
            errors.append(f"Card {anchor!r} names Binding but has no path")
        for binding in bindings:
            if not resolve_from(unit, binding).exists():
                errors.append(f"Card {anchor!r} has missing binding: {binding}")

    cited = {key.strip() for group in CITE_RE.findall(body) for key in group.split(",")}
    bibs = [resolve_from(unit, value) for value in inputs.get("sources", [])
            if isinstance(value, str) and value.endswith(".bib")]
    if cited and not bibs:
        errors.append("the Page cites references but no .bib source is declared")
    else:
        keys = set().union(*(bib_keys(path) for path in bibs)) if bibs else set()
        for key in sorted(cited - keys):
            errors.append(f"citation key is absent from references.bib: {key}")
    return manifest, errors, warnings


def bib_keys(path: pathlib.Path) -> set[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    return set(re.findall(r"@[A-Za-z]+\s*\{\s*([^,\s]+)\s*,", text))


def raw_bib_entries(paths: Iterable[pathlib.Path]) -> dict[str, str]:
    """Return complete BibTeX entries while preserving human-authored formatting."""
    entries: dict[str, str] = {}
    start = re.compile(r"@[A-Za-z]+\s*\{\s*([^,\s]+)\s*,")
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        cursor = 0
        while match := start.search(text, cursor):
            opening = text.find("{", match.start())
            depth = 0
            closing = -1
            for index in range(opening, len(text)):
                if text[index] == "{":
                    depth += 1
                elif text[index] == "}":
                    depth -= 1
                    if depth == 0:
                        closing = index + 1
                        break
            if closing < 0:
                raise ViewError(f"unclosed BibTeX entry {match.group(1)!r} in {path}")
            raw = text[match.start():closing].strip() + "\n"
            key = match.group(1)
            if key in entries and entries[key] != raw:
                raise ViewError(f"conflicting BibTeX key {key!r} in one View")
            entries[key] = raw
            cursor = closing
    return entries


def bib_entries(paths: Iterable[pathlib.Path]) -> dict[str, dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}
    start = re.compile(r"@[A-Za-z]+\s*\{\s*([^,\s]+)\s*,")
    field = re.compile(r"(?ms)^\s*([A-Za-z]+)\s*=\s*[\{\"](.*?)[\}\"]\s*,?\s*$")
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        matches = list(start.finditer(text))
        for index, match in enumerate(matches):
            block = text[match.end(): matches[index + 1].start() if index + 1 < len(matches) else len(text)]
            values: dict[str, str] = {}
            for name, value in field.findall(block):
                values[name.lower()] = re.sub(r"[{}]", "", " ".join(value.split()))
            entries.setdefault(match.group(1), values)
    return entries


def cite_label(key: str, entries: dict[str, dict[str, str]]) -> str:
    entry = entries.get(key, {})
    author = entry.get("author", key).split(" and ")[0]
    surname = author.split(",")[0].strip() if "," in author else author.split()[-1]
    if " and " in entry.get("author", ""):
        surname += " et al."
    return f"{surname}, {entry.get('year', 'n.d.')}"


def replace_citations(text: str, entries: dict[str, dict[str, str]]) -> str:
    return CITE_RE.sub(
        lambda match: "(" + "; ".join(cite_label(key.strip(), entries)
                                         for key in match.group(1).split(",")) + ")",
        text,
    )


def tex_escape(text: str) -> str:
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text)
    text = text.replace("**", "").replace("`", "")
    for source, target in (
        ("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
        ("$", r"\$"), ("#", r"\#"), ("_", r"\_"), ("{", r"\{"),
        ("}", r"\}"), ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}"),
    ):
        text = text.replace(source, target)
    return text


def review_sources(page: pathlib.Path, unit: pathlib.Path, manifest: dict) -> list[pathlib.Path]:
    inputs, displays, _ = manifest_lists(manifest)
    paths = [page, unit / "manifest.json"]
    paths += [resolve_from(unit, value) for group in ("qa_probes", "sources")
              for value in inputs.get(group, [])]
    for display in displays:
        paths += sorted(path for path in (unit / "output" / display["folder"]).rglob("*") if path.is_file())
    return sorted(set(path.resolve() for path in paths))


def source_receipt(page: pathlib.Path, unit: pathlib.Path, manifest: dict) -> tuple[str, list[dict]]:
    rows = []
    digest = hashlib.sha256()
    for path in review_sources(page, unit, manifest):
        data = path.read_bytes()
        try:
            label = path.relative_to(page.parent).as_posix()
        except ValueError:
            label = str(path)
        value = hashlib.sha256(data).hexdigest()
        rows.append({"path": label, "sha256": value})
        digest.update(label.encode("utf-8") + b"\0" + value.encode("ascii") + b"\n")
    return digest.hexdigest(), rows


REGISTRY_NAME = ".haipipe-view-build.json"


def load_registry(root: pathlib.Path) -> dict:
    path = root / REGISTRY_NAME
    if not path.exists():
        return {"generated_by": "haipipe-view", "schema_version": 1, "views": {}}
    value = read_json(path)
    if value.get("generated_by") != "haipipe-view" or value.get("schema_version") != 1:
        raise ViewError(f"refusing foreign or unsupported fixture registry: {path}")
    if not isinstance(value.get("views"), dict):
        raise ViewError(f"fixture registry views must be an object: {path}")
    return value


def registry_bibliography(registry: dict) -> str:
    merged: dict[str, str] = {}
    owners: dict[str, str] = {}
    for view_id, record in sorted(registry.get("views", {}).items()):
        bibliography = record.get("bibliography", {})
        if not isinstance(bibliography, dict):
            raise ViewError(f"fixture registry bibliography must be an object for {view_id}")
        for key, raw in bibliography.items():
            if not isinstance(raw, str):
                raise ViewError(f"fixture registry BibTeX entry must be text: {view_id}/{key}")
            if key in merged and merged[key] != raw:
                raise ViewError(
                    f"BibTeX key collision for {key!r}: {owners[key]} and {view_id} differ"
                )
            merged[key] = raw
            owners[key] = view_id
    return "\n".join(merged[key].rstrip() for key in sorted(merged)) + ("\n" if merged else "")


def fixture_float(text: str, folder: str) -> str:
    return text.replace(f"output/{folder}/", f"displays/{folder}/")


def display_handoff(manifest: dict, row: dict) -> dict:
    blockers = []
    if manifest.get("acceptance") != "accepted":
        blockers.append(f"View acceptance is {manifest.get('acceptance')}")
    if row.get("acceptance") != "accepted":
        blockers.append(f"Display acceptance is {row.get('acceptance')}")
    if row.get("status") not in ("rendered", "current"):
        blockers.append(f"Display artifact status is {row.get('status')}")
    return {"eligible": not blockers, "blockers": blockers}


def distributable_displays(manifest: dict) -> list[dict]:
    return [
        row for row in manifest.get("displays", [])
        if isinstance(row, dict) and row.get("status") in ("rendered", "current")
    ]


def public_display_manifest(manifest: dict, row: dict, source_digest: str, unit: pathlib.Path) -> dict:
    folder = row["folder"]
    source = unit / "output" / folder
    image = row.get("preview_image", "preview.png")
    pdf = row.get("preview_pdf", "preview.pdf")
    return {
        "schema_version": 1,
        "generated_by": "haipipe-view",
        "owner_view": manifest["id"],
        "id": row["id"],
        "folder": folder,
        "kind": row["kind"],
        "reader_job": row["reader_job"],
        "body_bindings": row.get("body_bindings", []),
        "artifact_status": row["status"],
        "acceptance": row["acceptance"],
        "source_digest": source_digest,
        "display_digest": directory_digest(source),
        "artifacts": {
            "float": "float.tex",
            "assets": "assets/",
            "preview_image": image,
            "preview_pdf": pdf,
            "bibliography": "../../references.bib",
        },
        "handoff": display_handoff(manifest, row),
    }


def public_view_manifest(manifest: dict, source_digest: str) -> dict:
    displays = []
    for row in manifest.get("displays", []):
        displays.append({
            "id": row["id"],
            "folder": row["folder"],
            "kind": row["kind"],
            "reader_job": row["reader_job"],
            "body_bindings": row.get("body_bindings", []),
            "artifact_status": row["status"],
            "acceptance": row["acceptance"],
            "distribution": (
                f"../../displays/{row['folder']}/manifest.json"
                if row.get("status") in ("rendered", "current") else None
            ),
            "handoff": display_handoff(manifest, row),
        })
    consumers = [
        {key: row[key] for key in ("id", "uses", "placement", "status")}
        for row in manifest.get("consumers", [])
    ]
    blockers = [] if manifest.get("acceptance") == "accepted" else [
        f"View acceptance is {manifest.get('acceptance')}"
    ]
    return {
        "schema_version": 1,
        "generated_by": "haipipe-view",
        "id": manifest["id"],
        "page_id": manifest["page_id"],
        "title": manifest["title"],
        "acceptance": manifest["acceptance"],
        "source_digest": source_digest,
        "displays": displays,
        "consumers": consumers,
        "bibliography": "../../references.bib",
        "handoff": {"eligible": not blockers, "blockers": blockers},
    }


def json_bytes(value: dict) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def stage_display(unit: pathlib.Path, manifest: dict, row: dict, source_digest: str, stage: pathlib.Path) -> None:
    folder = row["folder"]
    source = unit / "output" / folder
    stage.mkdir(parents=True)
    (stage / "float.tex").write_text(
        fixture_float((source / "float.tex").read_text(encoding="utf-8"), folder),
        encoding="utf-8",
    )
    for field in ("preview_image", "preview_pdf"):
        name = row.get(field, "preview.png" if field == "preview_image" else "preview.pdf")
        shutil.copy2(source / name, stage / name)
    if (source / "assets").is_dir():
        shutil.copytree(source / "assets", stage / "assets")
    (stage / "manifest.json").write_bytes(
        json_bytes(public_display_manifest(manifest, row, source_digest, unit))
    )


def expected_display_files(unit: pathlib.Path, manifest: dict, row: dict, source_digest: str) -> dict[str, bytes]:
    folder = row["folder"]
    source = unit / "output" / folder
    expected = {
        "float.tex": fixture_float(
            (source / "float.tex").read_text(encoding="utf-8"), folder
        ).encode("utf-8"),
        "manifest.json": json_bytes(public_display_manifest(manifest, row, source_digest, unit)),
    }
    for field in ("preview_image", "preview_pdf"):
        name = row.get(field, "preview.png" if field == "preview_image" else "preview.pdf")
        expected[name] = (source / name).read_bytes()
    assets = source / "assets"
    if assets.is_dir():
        for path in sorted(item for item in assets.rglob("*") if item.is_file()):
            expected[(pathlib.Path("assets") / path.relative_to(assets)).as_posix()] = path.read_bytes()
    return expected


def replace_owned_directory(stage: pathlib.Path, target: pathlib.Path, owned: bool) -> None:
    if target.exists() and not owned:
        raise ViewError(f"refusing unowned generated target: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(stage, target)


def copy_review_images(body: str, page: pathlib.Path, stage: pathlib.Path) -> tuple[dict[str, str], dict[str, str]]:
    tex_paths: dict[str, str] = {}
    data_urls: dict[str, str] = {}
    assets = stage / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    image_sources = [match.group(1) for line in body.splitlines()
                     if (match := IMAGE_RE.match(line.rstrip()))]
    for index, source_text in enumerate(image_sources, 1):
        source = (page.parent / source_text).resolve()
        if not source.is_file():
            for ancestor in page.parents:
                candidate = (ancestor / source_text).resolve()
                if candidate.is_file():
                    source = candidate
                    break
        if not source.is_file():
            raise ViewError(f"embedded review image is missing: {source_text}")
        suffix = source.suffix.lower() or ".png"
        name = f"display-{index}{suffix}"
        shutil.copy2(source, assets / name)
        tex_paths[source_text] = name
        mime = "image/png" if suffix == ".png" else "image/jpeg"
        data_urls[source_text] = f"data:{mime};base64," + base64.b64encode(source.read_bytes()).decode("ascii")
    return tex_paths, data_urls


def markdown_to_tex(body: str, entries: dict[str, dict[str, str]], image_paths: dict[str, str]) -> str:
    out: list[str] = []
    in_code = False
    in_items = False
    for raw in body.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            if in_items:
                out.append(r"\end{itemize}")
                in_items = False
            out.append(r"\end{Verbatim}" if in_code else r"\begin{Verbatim}[fontsize=\small]")
            in_code = not in_code
            continue
        if in_code:
            out.append(line)
            continue
        image = IMAGE_RE.match(line)
        if image:
            if in_items:
                out.append(r"\end{itemize}")
                in_items = False
            out.append(r"\begin{center}\includegraphics[width=0.94\linewidth]{assets/" + image_paths[image.group(1)] + r"}\end{center}")
            continue
        heading = re.match(r"^(###|####)\s+(.+)$", line)
        if heading:
            if in_items:
                out.append(r"\end{itemize}")
                in_items = False
            command = "section" if heading.group(1) == "###" else "subsection"
            out.append(rf"\{command}*{{{tex_escape(heading.group(2))}}}")
            continue
        if line.startswith("- "):
            if not in_items:
                out.append(r"\begin{itemize}")
                in_items = True
            out.append(r"\item " + tex_escape(replace_citations(line[2:], entries)))
            continue
        if in_items:
            out.append(r"\end{itemize}")
            in_items = False
        if line.startswith("> Card "):
            out.append(r"\begin{quote}\footnotesize\textbf{Evidence card.} " + tex_escape(replace_citations(line[2:], entries)) + r"\end{quote}")
        elif line:
            out.append(tex_escape(replace_citations(line, entries)) + "\n")
    if in_items:
        out.append(r"\end{itemize}")
    return "\n".join(out)


def markdown_to_html(body: str, entries: dict[str, dict[str, str]], images: dict[str, str]) -> str:
    out: list[str] = []
    in_code = False
    in_items = False
    for raw in body.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            if in_items:
                out.append("</ul>")
                in_items = False
            out.append("</code></pre>" if in_code else "<pre><code>")
            in_code = not in_code
            continue
        if in_code:
            out.append(html.escape(line) + "\n")
            continue
        image = IMAGE_RE.match(line)
        if image:
            if in_items:
                out.append("</ul>")
                in_items = False
            out.append(f'<figure><img src="{images[image.group(1)]}" /></figure>')
            continue
        heading = re.match(r"^(###|####)\s+(.+)$", line)
        if heading:
            if in_items:
                out.append("</ul>")
                in_items = False
            level = 2 if heading.group(1) == "###" else 3
            out.append(f"<h{level}>{html.escape(heading.group(2))}</h{level}>")
            continue
        if line.startswith("- "):
            if not in_items:
                out.append("<ul>")
                in_items = True
            out.append(f"<li>{html.escape(replace_citations(line[2:], entries))}</li>")
            continue
        if in_items:
            out.append("</ul>")
            in_items = False
        clean = replace_citations(line, entries).replace("**", "").replace("`", "")
        if line.startswith("> Card "):
            out.append(f'<aside><strong>Evidence card.</strong> {html.escape(clean[2:])}</aside>')
        elif line:
            out.append(f"<p>{html.escape(clean)}</p>")
    if in_items:
        out.append("</ul>")
    return "\n".join(out)


def reference_text(key: str, entry: dict[str, str]) -> str:
    author = entry.get("author", key).replace(" and ", "; ")
    title = entry.get("title", "Untitled")
    container = entry.get("booktitle") or entry.get("journal", "")
    return f"{author} ({entry.get('year', 'n.d.')}). {title}. {container}".strip()


def write_docx(
    destination: pathlib.Path,
    title: str,
    body: str,
    entries: dict[str, dict[str, str]],
    image_paths: dict[str, str],
    stage: pathlib.Path,
    cited: list[str],
) -> None:
    """Write a small, dependency-free DOCX with embedded Display previews."""
    ns = (
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"'
    )

    def x(value: str) -> str:
        return html.escape(value, quote=True)

    def paragraph(text: str, style: str | None = None) -> str:
        properties = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
        return f'<w:p>{properties}<w:r><w:t xml:space="preserve">{x(text)}</w:t></w:r></w:p>'

    media: list[tuple[str, pathlib.Path, str]] = []
    relationships: list[str] = []
    document: list[str] = [paragraph(title, "Title")]
    drawing_id = 1
    in_code = False
    for raw in body.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            in_code = not in_code
            continue
        image = IMAGE_RE.match(line)
        if image:
            name = image_paths[image.group(1)]
            source = stage / "assets" / name
            rid = f"rId{len(media) + 1}"
            width, height = 1200, 700
            data = source.read_bytes()
            if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
                width = int.from_bytes(data[16:20], "big")
                height = int.from_bytes(data[20:24], "big")
            cx = int(5.9 * 914400)
            cy = min(int(cx * height / max(width, 1)), int(4.5 * 914400))
            media.append((name, source, rid))
            relationships.append(
                f'<Relationship Id="{rid}" '
                'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                f'Target="media/{x(name)}"/>'
            )
            drawing = f'''<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing>
<wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>
<wp:docPr id="{drawing_id}" name="Display {drawing_id}"/><a:graphic>
<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic>
<pic:nvPicPr><pic:cNvPr id="{drawing_id}" name="{x(name)}"/><pic:cNvPicPr/></pic:nvPicPr>
<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData>
</a:graphic></wp:inline></w:drawing></w:r></w:p>'''
            document.append(drawing)
            drawing_id += 1
            continue
        heading = re.match(r"^(###|####)\s+(.+)$", line)
        if heading:
            document.append(paragraph(heading.group(2), "Heading1" if heading.group(1) == "###" else "Heading2"))
            continue
        clean = replace_citations(line, entries).replace("**", "").replace("`", "")
        if in_code:
            document.append(paragraph(clean, "Code"))
        elif line.startswith("> Card "):
            document.append(paragraph("Evidence card. " + clean[2:], "Quote"))
        elif line.startswith("- "):
            document.append(paragraph("• " + clean[2:], "ListParagraph"))
        elif line:
            document.append(paragraph(clean))
    if cited:
        document.append(paragraph("References", "Heading1"))
        for key in cited:
            document.append(paragraph(reference_text(key, entries.get(key, {})), "ListParagraph"))
    document.append(
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar '
        'w:top="1080" w:right="1080" w:bottom="1080" w:left="1080"/></w:sectPr>'
    )

    document_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<w:document {ns}><w:body>{"".join(document)}</w:body></w:document>'
    )
    styles_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="22"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:spacing w:after="320"/></w:pPr><w:rPr><w:b/><w:sz w:val="34"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="280" w:after="120"/></w:pPr><w:rPr><w:b/><w:sz w:val="28"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="220" w:after="100"/></w:pPr><w:rPr><w:b/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Quote"><w:name w:val="Evidence card"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="360"/><w:shd w:fill="F1F5F9"/><w:spacing w:before="80" w:after="120"/></w:pPr><w:rPr><w:sz w:val="18"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Code"><w:name w:val="Code"/><w:basedOn w:val="Normal"/><w:rPr><w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/><w:sz w:val="18"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="360"/></w:pPr></w:style>
</w:styles>'''
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="png" ContentType="image/png"/>
<Default Extension="jpg" ContentType="image/jpeg"/>
<Default Extension="jpeg" ContentType="image/jpeg"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''
    root_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''
    doc_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">''' + \
        "".join(relationships) + \
        '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>'

    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", root_rels)
        archive.writestr("word/document.xml", document_xml)
        archive.writestr("word/styles.xml", styles_xml)
        archive.writestr("word/_rels/document.xml.rels", doc_rels)
        for name, source, _ in media:
            archive.write(source, f"word/media/{name}")


def generated_review(page: pathlib.Path, unit: pathlib.Path, manifest: dict, stage: pathlib.Path) -> None:
    body = content_block(page.read_text(encoding="utf-8"))
    inputs, _, _ = manifest_lists(manifest)
    bib_paths = [resolve_from(unit, value) for value in inputs.get("sources", []) if value.endswith(".bib")]
    entries = bib_entries(bib_paths)
    cited = [key.strip() for group in CITE_RE.findall(body) for key in group.split(",")]
    cited = list(dict.fromkeys(cited))
    image_paths, _ = copy_review_images(body, page, stage)
    title = manifest["title"]

    refs_tex = "\n".join(r"\item " + tex_escape(reference_text(key, entries.get(key, {}))) for key in cited)
    tex = r"""\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{fontspec}
\setmainfont{Arial}
\usepackage{graphicx}
\usepackage{fvextra}
\usepackage{enumitem}
\setlist{nosep}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.55em}
\begin{document}
""" + "\n" + r"\begin{center}\LARGE\textbf{" + tex_escape(title) + r"}\end{center}" + "\n" + \
        markdown_to_tex(body, entries, image_paths) + "\n"
    if cited:
        tex += r"\section{References}\begin{itemize}" + "\n" + refs_tex + "\n" + r"\end{itemize}" + "\n"
    tex += r"\end{document}" + "\n"
    tex_path = stage / f"{page.stem}.tex"
    tex_path.write_text(tex, encoding="utf-8")

    xelatex = shutil.which("xelatex")
    if not xelatex:
        raise ViewError("xelatex is required to build the View review PDF")
    for _ in range(2):
        run = subprocess.run(
            [xelatex, "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
            cwd=stage, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        if run.returncode:
            raise ViewError("xelatex failed:\n" + "\n".join(run.stdout.splitlines()[-30:]))
    write_docx(stage / f"{page.stem}.docx", title, body, entries, image_paths, stage, cited)
    for suffix in ("aux", "log", "out"):
        auxiliary = stage / f"{page.stem}.{suffix}"
        if auxiliary.exists():
            auxiliary.unlink()


def check_fixture(
    page: pathlib.Path,
    unit: pathlib.Path,
    manifest: dict,
    root_override: pathlib.Path | None = None,
) -> list[str]:
    page = page.resolve()
    unit = unit.resolve()
    root = fixture_root(unit, manifest, root_override)
    target = root / "views" / page.stem
    receipt = target / "build-manifest.json"
    errors: list[str] = []
    if not receipt.is_file():
        return [f"missing View fixture build: {target}"]
    try:
        built = read_json(receipt)
        registry = load_registry(root)
    except ViewError as exc:
        return [str(exc)]
    digest, _ = source_receipt(page, unit, manifest)
    if built.get("source_digest") != digest:
        errors.append("review build is stale against the canonical Page or resources")
    for suffix in ("tex", "pdf", "docx"):
        path = target / f"{page.stem}.{suffix}"
        if not path.is_file():
            errors.append(f"missing review format: {path.name}")
    pdf = target / f"{page.stem}.pdf"
    if pdf.is_file() and not pdf.read_bytes().startswith(b"%PDF"):
        errors.append("review PDF is invalid")
    docx = target / f"{page.stem}.docx"
    if docx.is_file():
        try:
            with zipfile.ZipFile(docx) as archive:
                if "word/document.xml" not in archive.namelist():
                    errors.append("review DOCX lacks word/document.xml")
        except zipfile.BadZipFile:
            errors.append("review DOCX is invalid")
    public_manifest = target / "manifest.json"
    expected_public = json_bytes(public_view_manifest(manifest, digest))
    if not public_manifest.is_file() or public_manifest.read_bytes() != expected_public:
        errors.append("View consumer manifest is missing or stale")
    record = registry.get("views", {}).get(page.stem)
    if not isinstance(record, dict):
        errors.append(f"fixture registry does not own {page.stem}")
        return errors
    if record.get("source_digest") != digest:
        errors.append("fixture registry is stale against the canonical Page or resources")
    displays = distributable_displays(manifest)
    expected_folders = [row["folder"] for row in displays]
    if record.get("displays") != expected_folders:
        errors.append("fixture registry Display list is stale")
    for row in displays:
        destination = root / "displays" / row["folder"]
        if not destination.is_dir():
            errors.append(f"missing paper-ready Display: {destination}")
            continue
        expected = expected_display_files(unit, manifest, row, digest)
        actual_names = sorted(
            path.relative_to(destination).as_posix()
            for path in destination.rglob("*") if path.is_file()
        )
        if actual_names != sorted(expected):
            errors.append(f"paper-ready Display file set is stale: {row['folder']}")
            continue
        for name, data in expected.items():
            if (destination / name).read_bytes() != data:
                errors.append(f"paper-ready Display file is stale: {row['folder']}/{name}")
    bibliography = root / "references.bib"
    expected_bib = registry_bibliography(registry).encode("utf-8")
    if not bibliography.is_file() or bibliography.read_bytes() != expected_bib:
        errors.append("fixture references.bib is missing or stale")
    return errors


def build(
    page: pathlib.Path,
    check_only: bool,
    root_override: pathlib.Path | None = None,
) -> int:
    page, unit = view_paths(page)
    manifest, errors, warnings = validate(page)
    for warning in warnings:
        print(f"WARN {warning}")
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1
    if check_only:
        failures = check_fixture(page, unit, manifest, root_override)
        for failure in failures:
            print(f"ERROR {failure}")
        if failures:
            return 1
        root = fixture_root(unit, manifest, root_override)
        print(f"current {root / 'views' / page.stem} · review + Displays + references")
        return 0

    root = fixture_root(unit, manifest, root_override)
    review_target = root / "views" / page.stem
    digest, sources = source_receipt(page, unit, manifest)
    try:
        root.mkdir(parents=True, exist_ok=True)
        registry = load_registry(root)
        previous = registry["views"].get(page.stem, {})
        previous_displays = previous.get("displays", []) if isinstance(previous, dict) else []
        if review_target.exists() and not previous:
            raise ViewError(f"refusing unowned generated target: {review_target}")
        displays = distributable_displays(manifest)
        for row in displays:
            destination = root / "displays" / row["folder"]
            if destination.exists() and row["folder"] not in previous_displays:
                raise ViewError(f"refusing unowned generated target: {destination}")
        inputs, _, _ = manifest_lists(manifest)
        bib_paths = [
            resolve_from(unit, value)
            for value in inputs.get("sources", [])
            if isinstance(value, str) and value.endswith(".bib")
        ]
        bibliography = raw_bib_entries(bib_paths)
        new_record = {
            "source_digest": digest,
            "review": f"views/{page.stem}",
            "displays": [row["folder"] for row in displays],
            "bibliography": bibliography,
        }
        next_registry = json.loads(json.dumps(registry))
        next_registry["views"][page.stem] = new_record
        root_bib = registry_bibliography(next_registry)
        with tempfile.TemporaryDirectory(prefix=f".{page.stem}-fixture-", dir=root) as temporary:
            stage_root = pathlib.Path(temporary)
            review_stage = stage_root / "view"
            review_stage.mkdir()
            generated_review(page, unit, manifest, review_stage)
            receipt = {
                "generated_by": "haipipe-view",
                "schema_version": 1,
                "view": page.stem,
                "canonical_page": manifest["page_source"],
                "source_digest": digest,
                "sources": sources,
                "outputs": [
                    f"{page.stem}.tex",
                    f"{page.stem}.pdf",
                    f"{page.stem}.docx",
                    "manifest.json",
                ],
            }
            (review_stage / "build-manifest.json").write_text(
                json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
            (review_stage / "manifest.json").write_bytes(
                json_bytes(public_view_manifest(manifest, digest))
            )
            display_stages: dict[str, pathlib.Path] = {}
            for row in displays:
                display_stage = stage_root / "displays" / row["folder"]
                stage_display(unit, manifest, row, digest, display_stage)
                display_stages[row["folder"]] = display_stage
            replace_owned_directory(review_stage, review_target, bool(previous))
            for row in displays:
                replace_owned_directory(
                    display_stages[row["folder"]],
                    root / "displays" / row["folder"],
                    row["folder"] in previous_displays,
                )
            for folder in previous_displays:
                if folder not in new_record["displays"]:
                    retired = root / "displays" / folder
                    if retired.is_dir():
                        shutil.rmtree(retired)
            (root / "references.bib").write_text(root_bib, encoding="utf-8")
            (root / REGISTRY_NAME).write_text(
                json.dumps(next_registry, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
    except (OSError, ViewError) as exc:
        print(f"ERROR {exc}")
        return 1
    print(
        f"built {root} · review + {len(displays)} paper-ready Displays + references · "
        "canonical Page unchanged"
    )
    return 0


def create(parent: pathlib.Path, view_id: str, title: str) -> int:
    match = VIEW_STEM_RE.fullmatch(view_id)
    if not match:
        print(f"ERROR invalid View Page stem {view_id!r}")
        return 1
    page = (parent / f"{view_id}.md").resolve()
    unit = (parent / "views" / view_id).resolve()
    if page.exists() or unit.exists():
        print(f"ERROR refusing to overwrite existing View: {page} or {unit}")
        return 1
    page_text = PAGE_TEMPLATE.read_text(encoding="utf-8")
    page_text = page_text.replace("<View title>", title).replace("<ViewPageStem>", view_id)
    page_text = page_text.replace("<PageID>", match.group("page_id"))
    manifest_text = MANIFEST_TEMPLATE.read_text(encoding="utf-8")
    for marker, value in (("{{ID}}", view_id), ("{{PAGE_ID}}", match.group("page_id")), ("{{TITLE}}", title)):
        manifest_text = manifest_text.replace(marker, value)
    unit.mkdir(parents=True)
    for folder in ("input/QA-probes", "input/sources", "source", "output"):
        (unit / folder).mkdir(parents=True)
    page.write_text(page_text, encoding="utf-8")
    (unit / "manifest.json").write_text(manifest_text, encoding="utf-8")
    print(f"created canonical Page {page}")
    print(f"created resource folder {unit} · no duplicate view.md")
    return 0


def add_display(
    page: pathlib.Path,
    kind: str,
    slug: str,
    reader_job: str,
    body_bindings: list[str],
) -> int:
    page, unit = view_paths(page)
    if not page.is_file() or not (unit / "manifest.json").is_file():
        print(f"ERROR missing canonical View pair for {page}")
        return 1
    if kind not in DISPLAY_KINDS:
        print(f"ERROR unsupported Display kind {kind!r}")
        return 1
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        print("ERROR Display slug must be lowercase hyphen-case")
        return 1
    manifest = read_json(unit / "manifest.json")
    _, displays, _ = manifest_lists(manifest)
    numbers = []
    for row in displays:
        match = re.fullmatch(rf"{re.escape(manifest['page_id'])}-Display([1-9][0-9]*)", row.get("id", ""))
        if match:
            numbers.append(int(match.group(1)))
    number = max(numbers, default=0) + 1
    display_id = f"{manifest['page_id']}-Display{number}"
    folder = f"{display_id}-{slug}"
    target = unit / "output" / folder
    if target.exists():
        print(f"ERROR refusing to overwrite Display unit: {target}")
        return 1
    target.mkdir(parents=True)
    for directory in DISPLAY_REQUIRED_DIRS:
        (target / directory).mkdir(parents=True, exist_ok=True)
    for directory in ("recipe", "candidates", "assets", "versions"):
        (target / directory / ".gitkeep").write_text("", encoding="utf-8")
    (target / "README.md").write_text(
        f"# {display_id}\n\nstatus: planned\nkind: {kind}\nreader-job: {reader_job}\n",
        encoding="utf-8",
    )
    (target / "output.md").write_text(
        f"# {display_id}: {slug.replace('-', ' ')}\n\n"
        "state: PLANNED · waiting for intake and rendering\n"
        f"parent: {manifest['id']}\ntype: {kind}\n\n"
        f"## Reader job\n\n{reader_job}\n\n"
        "## View bindings\n\n" + ("\n".join(f"- {value}" for value in body_bindings) or "- pending") +
        "\n\n## Acceptance checks\n\n- Define before rendering.\n",
        encoding="utf-8",
    )
    (target / "intake" / "manifest.yaml").write_text(
        "schema_version: 1\n"
        f"display_id: {display_id}\nkind: {kind}\nmode: pending-intake\n"
        f"purpose: \"{reader_job.replace(chr(34), chr(39))}\"\nsources: []\n",
        encoding="utf-8",
    )
    (target / "float.tex").write_text(
        "% Caller-owned caption, label, placement, and asset reference remain pending.\n",
        encoding="utf-8",
    )
    (target / "preview.tex").write_text(
        "\\documentclass{article}\n\\usepackage{graphicx}\n\\begin{document}\n"
        "\\input{float.tex}\n\\end{document}\n",
        encoding="utf-8",
    )
    displays.append({
        "id": display_id,
        "folder": folder,
        "unit_contract": DISPLAY_UNIT_CONTRACT,
        "kind": kind,
        "reader_job": reader_job,
        "body_bindings": body_bindings,
        "status": "planned",
        "acceptance": "waiting",
        "preview_image": "preview.png",
        "preview_pdf": "preview.pdf",
    })
    (unit / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"created Display unit {target}")
    print("update the canonical Page Content 3 before marking the Display rendered")
    return 0


def check(page: pathlib.Path) -> int:
    manifest, errors, warnings = validate(page)
    for warning in warnings:
        print(f"WARN {warning}")
    for error in errors:
        print(f"ERROR {error}")
    if errors:
        return 1
    inputs, displays, consumers = manifest_lists(manifest)
    print(
        f"valid {page.resolve()} · {len(inputs['qa_probes'])} QA probes · "
        f"{len(displays)} displays · {len(consumers)} consumers · acceptance {manifest['acceptance']}"
    )
    return 0


def status(page: pathlib.Path) -> int:
    page = page.resolve()
    unit = page.parent / "views" / page.stem
    manifest, errors, warnings = validate(page)
    if not manifest:
        for error in errors:
            print(f"ERROR {error}")
        return 1
    inputs, displays, consumers = manifest_lists(manifest)
    print(f"View       {manifest.get('id')} · canonical Page")
    print(f"Inputs     {len(inputs.get('qa_probes', []))} QA probes · {len(inputs.get('sources', []))} sources")
    print("Displays   " + (", ".join(f"{row['id']}:{row['status']}/{row['acceptance']}" for row in displays) or "none"))
    print("Consumers  " + (", ".join(f"{row['id']}:{row['status']}" for row in consumers) or "none"))
    try:
        root = fixture_root(unit, manifest)
        fixture_state = "current" if not check_fixture(page, unit, manifest) else "missing/stale"
        print(f"Fixture    {root} · {fixture_state}")
    except ViewError as exc:
        print(f"Fixture    ERROR {exc}")
        errors.append(str(exc))
    print(f"Acceptance {manifest.get('acceptance')}")
    for warning in warnings:
        print(f"WARN       {warning}")
    for error in errors:
        print(f"ERROR      {error}")
    return 1 if errors else 0


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    commands = value.add_subparsers(dest="command", required=True)
    create_cmd = commands.add_parser("create")
    create_cmd.add_argument("parent", type=pathlib.Path)
    create_cmd.add_argument("view_id")
    create_cmd.add_argument("--title", required=True)
    display_cmd = commands.add_parser("add-display")
    display_cmd.add_argument("page", type=pathlib.Path)
    display_cmd.add_argument("kind", choices=DISPLAY_KINDS)
    display_cmd.add_argument("slug")
    display_cmd.add_argument("--reader-job", required=True)
    display_cmd.add_argument("--body-binding", action="append", default=[])
    for name in ("check", "status"):
        command = commands.add_parser(name)
        command.add_argument("page", type=pathlib.Path)
    build_cmd = commands.add_parser("build")
    build_cmd.add_argument("page", type=pathlib.Path)
    build_cmd.add_argument("--check", action="store_true")
    build_cmd.add_argument(
        "--target",
        type=pathlib.Path,
        help="override manifest build.fixture_root for this build or freshness check",
    )
    return value


def main() -> int:
    args = parser().parse_args()
    if args.command == "create":
        return create(args.parent, args.view_id, args.title)
    if args.command == "add-display":
        return add_display(args.page, args.kind, args.slug, args.reader_job, args.body_binding)
    if args.command == "check":
        return check(args.page)
    if args.command == "status":
        return status(args.page)
    return build(args.page, args.check, args.target)


if __name__ == "__main__":
    sys.exit(main())
