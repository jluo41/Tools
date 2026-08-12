#!/usr/bin/env python3
"""Manifest-driven, gated Markdown-to-LaTeX projection runtime."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment problem
    raise SystemExit("PyYAML is required: install pyyaml before running projection.") from exc


SCHEMA = "haipipe.paper.projection/v1"
RENDERER_VERSION = "md2tex-v1.3"
GATED_PREFIX = "✅ GATED"
INPUT_RE = re.compile(r"\\(?:input|include)\s*\{([^}]+)\}")
GRAPHICS_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\s*\{([^}]+)\}")
BIB_RE = re.compile(r"\\bibliography\s*\{([^}]+)\}")
BIBSTYLE_RE = re.compile(r"\\bibliographystyle\s*\{([^}]+)\}")
CLASS_RE = re.compile(r"\\documentclass(?:\[[^\]]*\])?\s*\{([^}]+)\}")
PACKAGE_RE = re.compile(r"\\usepackage(?:\[[^\]]*\])?\s*\{([^}]+)\}")
CITE_RE = re.compile(r"\\cite[a-zA-Z*]*\s*(?:\[[^\]]*\]\s*){0,2}\{([^}]+)\}")
QUESTION_RE = re.compile(r"\[Q-[A-Za-z0-9_.:@/-]+\]")
# LaTeX rungs, shallowest first. A selection deeper than this collapses onto the
# last one rather than emitting a command that misqdoc.cls does not define.
TEX_LEVELS = ("section", "subsection", "subsubsection", "paragraph")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


class ProjectionError(RuntimeError):
    """A contract or gate failure."""


class ProjectionBlocked(ProjectionError):
    """A valid run that cannot advance because an external prerequisite is absent."""


@dataclass(frozen=True)
class Context:
    paper: Path
    manifest_path: Path
    manifest_bytes: bytes
    data: dict[str, Any]
    master: Path
    target_roots: tuple[Path, ...]
    dependency_roots: tuple[Path, ...]
    candidate_root: Path


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strip_tex_comments(text: str) -> str:
    """Remove TeX comments while preserving escaped percent signs and newlines."""
    output: list[str] = []
    for line in text.splitlines(keepends=True):
        newline = ""
        body = line
        if line.endswith("\r\n"):
            body, newline = line[:-2], "\r\n"
        elif line.endswith("\n"):
            body, newline = line[:-1], "\n"
        for index, char in enumerate(body):
            if char != "%":
                continue
            backslashes = 0
            cursor = index - 1
            while cursor >= 0 and body[cursor] == "\\":
                backslashes += 1
                cursor -= 1
            if backslashes % 2 == 0:
                body = body[:index]
                break
        output.append(body + newline)
    return "".join(output)


def file_hash(path: Path) -> str | None:
    return sha256_bytes(path.read_bytes()) if path.is_file() else None


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")


def safe_rel(value: Any, field: str) -> PurePosixPath:
    if not isinstance(value, str) or not value.strip():
        raise ProjectionError(f"{field}: expected a non-empty relative POSIX path")
    if "\\" in value:
        raise ProjectionError(f"{field}: backslashes are not allowed")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise ProjectionError(f"{field}: unsafe relative path {value!r}")
    return path


def resolve_inside(root: Path, value: Any, field: str) -> Path:
    rel = safe_rel(value, field)
    root_resolved = root.resolve()
    result = root.joinpath(*rel.parts).resolve(strict=False)
    if result != root_resolved and root_resolved not in result.parents:
        raise ProjectionError(f"{field}: path escapes paper root: {value!r}")
    return result


def relative_posix(path: Path, root: Path) -> str:
    return path.resolve(strict=False).relative_to(root.resolve()).as_posix()


def discover_paper(start: Path) -> Path:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / "0-lifecycle").is_dir():
            return candidate
    raise ProjectionError(f"no paper root containing 0-lifecycle/ above {start}")


def load_context(paper_arg: str, manifest_arg: str | None) -> Context:
    paper = discover_paper(Path(paper_arg))
    manifest_path = (
        resolve_inside(paper, manifest_arg, "--manifest")
        if manifest_arg
        else paper / "2-src" / "projection.yaml"
    )
    if not manifest_path.is_file():
        raise ProjectionError(f"manifest not found: {manifest_path}")
    manifest_bytes = manifest_path.read_bytes()
    raw = yaml.safe_load(manifest_bytes)
    if not isinstance(raw, dict):
        raise ProjectionError("manifest root must be a mapping")
    if raw.get("schema") != SCHEMA:
        raise ProjectionError(f"schema must be {SCHEMA!r}")

    master = resolve_inside(paper, raw.get("master"), "master")
    if not master.is_file():
        raise ProjectionError(f"master does not exist: {relative_posix(master, paper)}")

    target_values = raw.get("target_roots")
    if not isinstance(target_values, list) or not target_values:
        raise ProjectionError("target_roots must be a non-empty list")
    target_roots = tuple(
        resolve_inside(paper, value, f"target_roots[{index}]")
        for index, value in enumerate(target_values)
    )
    for target in target_roots:
        rel = relative_posix(target, paper)
        if re.match(r"^[0-9]-", rel):
            raise ProjectionError(f"target root must be unnumbered: {rel}")

    dependency_values = raw.get("dependency_roots", [])
    if not isinstance(dependency_values, list):
        raise ProjectionError("dependency_roots must be a list")
    dependency_roots = tuple(
        resolve_inside(paper, value, f"dependency_roots[{index}]")
        for index, value in enumerate(dependency_values)
    )

    candidate_root = resolve_inside(paper, raw.get("candidate_root"), "candidate_root")
    dist_root = (paper / "3-dist").resolve(strict=False)
    if candidate_root != dist_root and dist_root not in candidate_root.parents:
        raise ProjectionError("candidate_root must be 3-dist/ or a descendant")

    return Context(
        paper=paper,
        manifest_path=manifest_path,
        manifest_bytes=manifest_bytes,
        data=raw,
        master=master,
        target_roots=target_roots,
        dependency_roots=dependency_roots,
        candidate_root=candidate_root,
    )


def units_mapping(ctx: Context) -> dict[str, dict[str, Any]]:
    units = ctx.data.get("units")
    if not isinstance(units, dict) or not units:
        raise ProjectionError("units must be a non-empty mapping")
    for name, unit in units.items():
        if not isinstance(name, str) or not name or not isinstance(unit, dict):
            raise ProjectionError("each unit must have a string id and mapping value")
    return units


def under_any(path: Path, roots: Iterable[Path]) -> bool:
    resolved = path.resolve(strict=False)
    return any(resolved == root.resolve() or root.resolve() in resolved.parents for root in roots)


def output_specs(ctx: Context) -> dict[str, tuple[str, dict[str, Any]]]:
    found: dict[str, tuple[str, dict[str, Any]]] = {}
    for unit_name, unit in units_mapping(ctx).items():
        outputs = unit.get("outputs")
        if not isinstance(outputs, list) or not outputs:
            raise ProjectionError(f"units.{unit_name}.outputs must be a non-empty list")
        for index, output in enumerate(outputs):
            if not isinstance(output, dict):
                raise ProjectionError(f"units.{unit_name}.outputs[{index}] must be a mapping")
            path = resolve_inside(ctx.paper, output.get("path"), f"{unit_name}.outputs[{index}].path")
            rel = relative_posix(path, ctx.paper)
            if not under_any(path, ctx.target_roots):
                raise ProjectionError(f"{unit_name}: output outside target_roots: {rel}")
            if path.suffix != ".tex":
                raise ProjectionError(f"{unit_name}: output must end in .tex: {rel}")
            if rel in found:
                raise ProjectionError(f"duplicate output path: {rel}")
            role = output.get("role")
            if role not in {"prose", "wrapper"}:
                raise ProjectionError(f"{unit_name}: unsupported role {role!r} for {rel}")
            found[rel] = (unit_name, output)

        entry = resolve_inside(ctx.paper, unit.get("entry"), f"units.{unit_name}.entry")
        entry_rel = relative_posix(entry, ctx.paper)
        if entry_rel not in {
            relative_posix(
                resolve_inside(ctx.paper, item.get("path"), f"{unit_name}.outputs.path"),
                ctx.paper,
            )
            for item in outputs
        }:
            raise ProjectionError(f"{unit_name}: entry must name one of its outputs")
    return found


def unreachable_specs(ctx: Context) -> dict[str, dict[str, Any]]:
    values = ctx.data.get("unreachable", [])
    if not isinstance(values, list):
        raise ProjectionError("unreachable must be a list")
    found: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(values):
        if not isinstance(item, dict):
            raise ProjectionError(f"unreachable[{index}] must be a mapping")
        path = resolve_inside(ctx.paper, item.get("path"), f"unreachable[{index}].path")
        rel = relative_posix(path, ctx.paper)
        if not under_any(path, ctx.target_roots) or path.suffix != ".tex":
            raise ProjectionError(f"unreachable path outside target roots or not .tex: {rel}")
        if rel in found:
            raise ProjectionError(f"duplicate unreachable path: {rel}")
        if not str(item.get("disposition", "")).strip() or not str(item.get("reason", "")).strip():
            raise ProjectionError(f"unreachable entry needs disposition and reason: {rel}")
        found[rel] = item
    return found


def source_for_unit(ctx: Context, unit_name: str, unit: dict[str, Any]) -> tuple[Path, str]:
    source = unit.get("source")
    if not isinstance(source, dict):
        raise ProjectionError(f"{unit_name}: source must be a mapping")
    page = resolve_inside(ctx.paper, source.get("page"), f"{unit_name}.source.page")
    if not page.is_file():
        raise ProjectionError(f"{unit_name}: source page does not exist: {relative_posix(page, ctx.paper)}")
    if not under_any(page, (ctx.paper / "0-lifecycle",)):
        raise ProjectionError(f"{unit_name}: source page must be under 0-lifecycle/")
    gate = unit.get("gate")
    if not isinstance(gate, str) or not gate.strip():
        raise ProjectionError(f"{unit_name}: gate must be a non-empty string")
    selector = source.get("select", "content")
    if not isinstance(selector, str):
        raise ProjectionError(f"{unit_name}: source.select must be a string")
    return page, selector


def gate_page_for_unit(ctx: Context, unit_name: str, unit: dict[str, Any]) -> Path:
    gate = unit.get("gate")
    if not isinstance(gate, str) or not re.fullmatch(r"S-[A-Za-z0-9][A-Za-z0-9-]*", gate):
        raise ProjectionError(f"{unit_name}: gate must be a valid S-page id")
    matches = sorted(
        path
        for path in (ctx.paper / "0-lifecycle").rglob("*.md")
        if path.stem == gate or path.stem.startswith(f"{gate}-")
    )
    if len(matches) != 1:
        found = [relative_posix(path, ctx.paper) for path in matches]
        raise ProjectionError(
            f"{unit_name}: gate id {gate!r} must match exactly one S page; found {found}"
        )
    return matches[0]


def first_state(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("state:"):
            return line.split(":", 1)[1].strip()
    return ""


def gate_state(ctx: Context, unit_name: str, unit: dict[str, Any]) -> tuple[bool, str, Path]:
    source_for_unit(ctx, unit_name, unit)
    gate_page = gate_page_for_unit(ctx, unit_name, unit)
    state = first_state(gate_page.read_text(encoding="utf-8"))
    return state.startswith(GATED_PREFIX), state or "<missing>", gate_page


def inventory_targets(ctx: Context) -> set[str]:
    result: set[str] = set()
    for root in ctx.target_roots:
        if not root.exists():
            continue
        for path in root.rglob("*.tex"):
            if path.is_file():
                result.add(relative_posix(path, ctx.paper))
    return result


def validate_context(ctx: Context) -> dict[str, Any]:
    outputs = output_specs(ctx)
    unreachable = unreachable_specs(ctx)
    overlap = sorted(set(outputs) & set(unreachable))
    if overlap:
        raise ProjectionError(f"paths cannot be both output and unreachable: {overlap}")
    inventory = inventory_targets(ctx)
    declared = set(outputs) | set(unreachable)
    missing = sorted(inventory - declared)
    phantom = sorted(declared - inventory)
    if missing or phantom:
        details = []
        if missing:
            details.append(f"undeclared existing targets={missing}")
        if phantom:
            details.append(f"declared paths absent from submission tree={phantom}")
        raise ProjectionError("G0 coverage failed: " + "; ".join(details))

    states: dict[str, str] = {}
    for unit_name, unit in units_mapping(ctx).items():
        gated, state, _ = gate_state(ctx, unit_name, unit)
        states[unit_name] = state
        if not isinstance(gated, bool):  # keeps the contract visually explicit
            raise AssertionError

    return {
        "G0": "pass",
        "master": relative_posix(ctx.master, ctx.paper),
        "outputs": len(outputs),
        "unreachable": len(unreachable),
        "inventory": len(inventory),
        "unit_states": states,
        "manifest_sha256": sha256_bytes(ctx.manifest_bytes),
    }


def select_markdown(text: str, selector: str) -> str:
    lines = text.splitlines()
    if selector == "content":
        wanted = "Content"
        wanted_depth = 2
    elif selector.startswith("heading:"):
        wanted = selector.split(":", 1)[1].strip()
        if not wanted:
            raise ProjectionError("heading selector must name a heading")
        wanted_depth = 0
    else:
        raise ProjectionError(f"unsupported selector: {selector!r}")

    matches: list[tuple[int, int]] = []
    depth = wanted_depth
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if not match:
            continue
        heading_depth = len(match.group(1))
        heading_text = match.group(2).strip()
        if heading_text == wanted and (wanted_depth == 0 or heading_depth == wanted_depth):
            matches.append((index + 1, heading_depth))
    if not matches:
        raise ProjectionError(f"selector did not resolve: {selector!r}")
    if len(matches) > 1:
        raise ProjectionError(f"selector is not unique: {selector!r} ({len(matches)} matches)")
    start, depth = matches[0]

    end = len(lines)
    for index in range(start, len(lines)):
        match = HEADING_RE.match(lines[index])
        if match and len(match.group(1)) <= depth:
            end = index
            break
    selected = "\n".join(lines[start:end]).strip()
    if not selected:
        raise ProjectionError(f"selector resolved to an empty region: {selector!r}")
    return selected + "\n"


def clean_heading(text: str) -> str:
    value = re.sub(r"^§\s*\d+(?:\.\d+)*\s*", "", text).strip()
    value = re.sub(r"^[A-Z]\.\s*", "", value).strip()
    return value


def inline_markdown(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r"\\href{\2}{\1}", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"`([^`]+)`", r"\\texttt{\1}", text)
    return text.strip()


def manuscript_prose_markdown(markdown: str) -> str:
    """Return selected manuscript prose before rendering, without Board apparatus."""
    output: list[str] = []
    in_comment = False
    in_fence = False
    skip_parenthetical = False
    for raw in markdown.splitlines():
        stripped = raw.strip()
        if stripped.startswith("<!--"):
            in_comment = True
        if in_comment:
            if "-->" in stripped:
                in_comment = False
            continue
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not stripped or stripped.startswith(">"):
            continue

        heading = HEADING_RE.match(stripped)
        if heading:
            title = heading.group(2).strip()
            if title == "Stage Record":
                skip_parenthetical = False
                continue
            if len(heading.group(1)) >= 4 and re.match(r"^P\d+[.:]", title):
                skip_parenthetical = True
                continue
            output.append(raw)
            continue

        if stripped.startswith("Lifecycle:"):
            continue
        if skip_parenthetical and stripped.startswith("(") and stripped.endswith(")"):
            skip_parenthetical = False
            continue
        skip_parenthetical = False
        output.append(raw)
    return "\n".join(output).rstrip() + ("\n" if output else "")


def heading_depths(markdown: str) -> list[int]:
    """Depths of the headings this renderer will actually emit.

    Board apparatus is excluded, because a heading that never reaches the .tex
    must not decide what level the ones that do get rendered at.
    """
    depths: list[int] = []
    in_comment = False
    in_fence = False
    for raw in markdown.splitlines():
        stripped = raw.strip()
        if stripped.startswith("<!--"):
            in_comment = True
        if in_comment:
            if "-->" in stripped:
                in_comment = False
            continue
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(stripped)
        if not match:
            continue
        title = match.group(2).strip()
        if title == "Stage Record":
            continue
        if len(match.group(1)) >= 4 and re.match(r"^P\d+[.:]", title):
            continue
        if not clean_heading(title):
            continue
        depths.append(len(match.group(1)))
    return depths


def markdown_to_tex(
    markdown: str, source_rel: str, selector: str, top_title: str | None = None
) -> str:
    """Render one selected Markdown region as the body of ONE .tex file.

    HEADING LEVELS ARE RELATIVE, NOT ABSOLUTE. The old rule was `### -> section,
    #### -> subsection` by raw markdown depth, and it is wrong in both
    directions on a real paper. A main section page's `## Content` holds
    `### §3.1`, `### §3.2`, `### §3.3`, which are the section's SUBSECTIONS; the
    old rule emitted three `\\section{}` commands and silently renumbered the
    manuscript. An appendix division selected by `heading:` lost its heading
    line to the selector and emitted no `\\section{}` at all, so the appendix
    letters disappeared. Only `main-1` was ever projected, and §1 happens to
    have exactly one division, which is the single shape both bugs spare.

    The rule now: ONE FILE, ONE `\\section{}`. `top_title` names it. Everything
    the selection itself carries sits below that, at its own relative depth.
    """
    output: list[str] = [
        f"%% GENERATED from {source_rel} ({selector}) by the haipipe-paper project verb.",
        "%% Do not hand-edit; backport changes to the S page and regenerate.",
        "",
    ]
    depths = heading_depths(markdown)
    base_depth = min(depths) if depths else 0
    if top_title:
        output.append(rf"\section{{{inline_markdown(top_title)}}}")
        # The section title came from outside the selection, so the selection's
        # own top level is one rung down from it.
        offset = 1
    else:
        offset = 0
    paragraph: list[str] = []
    in_comment = False
    in_fence = False
    skip_parenthetical = False
    bullets: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            output.append(" ".join(paragraph).strip())
            paragraph = []

    def flush_bullets() -> None:
        nonlocal bullets
        if bullets:
            flush_paragraph()
            output.append(r"\begin{itemize}")
            output.extend(rf"\item {item}" for item in bullets)
            output.append(r"\end{itemize}")
            bullets = []

    for raw in markdown.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if stripped.startswith("<!--"):
            in_comment = True
        if in_comment:
            if "-->" in stripped:
                in_comment = False
            continue
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not stripped or stripped.startswith(">"):
            continue

        heading = HEADING_RE.match(stripped)
        if heading:
            flush_bullets()
            flush_paragraph()
            depth = len(heading.group(1))
            title = heading.group(2).strip()
            if title == "Stage Record":
                skip_parenthetical = False
                continue
            if depth >= 4 and re.match(r"^P\d+[.:]", title):
                skip_parenthetical = True
                continue
            title = clean_heading(title)
            if title:
                rung = min(depth - base_depth + offset, len(TEX_LEVELS) - 1)
                output.append(rf"\{TEX_LEVELS[rung]}{{{inline_markdown(title)}}}")
            continue

        if stripped.startswith("Lifecycle:"):
            continue
        if skip_parenthetical and stripped.startswith("(") and stripped.endswith(")"):
            skip_parenthetical = False
            continue
        skip_parenthetical = False

        bullet = re.match(r"^[-*]\s+(.+)$", stripped)
        if bullet:
            flush_paragraph()
            bullets.append(inline_markdown(bullet.group(1)))
            continue
        flush_bullets()
        paragraph.append(inline_markdown(stripped))

    flush_bullets()
    flush_paragraph()
    return "\n".join(output).rstrip() + "\n"


def top_title_for(unit: dict[str, Any], output: dict[str, Any], selector: str) -> str | None:
    """The name of the one `\\section{}` this output file opens with.

    Two sources, in order, and neither of them guesses. An explicit
    `section_title:` on the output or on the unit wins: a main section page's
    `## Content` holds only the section's subdivisions, so the section's own
    name exists nowhere in the selected region and has to be declared. Failing
    that, a `heading:` selector already names the region, and `select_markdown`
    drops that heading line from the body, so it is free to become the section
    title. `select: content` with nothing declared yields None, and the file
    opens with whatever the selection's own top level is.
    """
    declared = output.get("section_title") or unit.get("section_title")
    if declared:
        return str(declared)
    if selector.startswith("heading:"):
        return clean_heading(selector.split(":", 1)[1].strip()) or None
    return None


def render_unit(ctx: Context, unit_name: str, unit: dict[str, Any]) -> tuple[dict[str, bytes], dict[str, Any]]:
    gated, state, gate_page = gate_state(ctx, unit_name, unit)
    if not gated:
        raise ProjectionError(f"G1 failed for {unit_name}: gate state is {state!r}")
    page, _ = source_for_unit(ctx, unit_name, unit)
    source = unit["source"]
    default_selector = source.get("select", "content")
    page_text = page.read_text(encoding="utf-8")
    page_rel = relative_posix(page, ctx.paper)
    rendered: dict[str, bytes] = {}
    evidence: dict[str, Any] = {}
    selections: dict[str, str] = {}
    for output in unit["outputs"]:
        rel = safe_rel(output["path"], f"{unit_name}.output.path").as_posix()
        role = output["role"]
        if role == "wrapper":
            inputs = output.get("inputs")
            if not isinstance(inputs, list) or not inputs:
                raise ProjectionError(f"{unit_name}: wrapper {rel} requires non-empty inputs")
            lines = [
                f"%% GENERATED from {page_rel} by the haipipe-paper project verb.",
                "%% Wiring only; do not add prose here.",
                "",
            ]
            for index, input_value in enumerate(inputs):
                input_path = resolve_inside(ctx.paper, input_value, f"{unit_name}.{rel}.inputs[{index}]")
                input_rel = relative_posix(input_path, ctx.paper)
                if input_rel not in {
                    safe_rel(item["path"], f"{unit_name}.outputs.path").as_posix()
                    for item in unit["outputs"]
                }:
                    raise ProjectionError(f"{unit_name}: wrapper input is not a unit output: {input_rel}")
                lines.append(rf"\input{{{PurePosixPath(input_rel).with_suffix('').as_posix()}}}")
            rendered_text = "\n".join(lines) + "\n"
            selected = ""
        else:
            selector = output.get("select", default_selector)
            if not isinstance(selector, str):
                raise ProjectionError(f"{unit_name}: selector for {rel} must be a string")
            selected = select_markdown(page_text, selector)
            rendered_text = markdown_to_tex(
                selected, page_rel, selector, top_title_for(unit, output, selector)
            )
            selections[rel] = sha256_bytes(selected.encode("utf-8"))
        rendered[rel] = rendered_text.encode("utf-8")
        manuscript_prose = manuscript_prose_markdown(selected) if selected else ""
        evidence[rel] = {
            # Evidence lanes (`>`), notes, and other Board apparatus are not
            # manuscript prose. Extract bindings from the filtered Markdown
            # before rendering so G3 remains independent of G2/the renderer.
            "source_citations": sorted(citation_keys(manuscript_prose)),
            "source_questions": sorted(set(QUESTION_RE.findall(manuscript_prose))),
        }
    return rendered, {
        "page": page_rel,
        "selected_sha256": selections,
        "state": state,
        "gate": unit["gate"],
        "gate_page": relative_posix(gate_page, ctx.paper),
        "evidence": evidence,
    }


def citation_keys(text: str) -> set[str]:
    keys: set[str] = set()
    for match in CITE_RE.finditer(strip_tex_comments(text)):
        keys.update(key.strip() for key in match.group(1).split(",") if key.strip())
    return keys


def select_units(ctx: Context, requested: list[str]) -> list[str]:
    units = units_mapping(ctx)
    names = requested or [name for name, unit in units.items() if gate_state(ctx, name, unit)[0]]
    unknown = sorted(set(names) - set(units))
    if unknown:
        raise ProjectionError(f"unknown unit(s): {unknown}")
    if not names:
        raise ProjectionError("no gated units selected")
    return names


def build_expected(ctx: Context, names: list[str]) -> tuple[dict[str, bytes], dict[str, Any]]:
    files: dict[str, bytes] = {}
    sources: dict[str, Any] = {}
    for name in names:
        unit_files, source_info = render_unit(ctx, name, units_mapping(ctx)[name])
        overlap = set(files) & set(unit_files)
        if overlap:
            raise ProjectionError(f"selected units collide on outputs: {sorted(overlap)}")
        files.update(unit_files)
        sources[name] = source_info
    return files, sources


def submission_snapshot(ctx: Context, paths: Iterable[str]) -> dict[str, str | None]:
    return {rel: file_hash(resolve_inside(ctx.paper, rel, "submission target")) for rel in sorted(paths)}


def resolve_local_dependency(
    ctx: Context, value: str, suffixes: tuple[str, ...], *, required: bool
) -> tuple[str, str | None] | None:
    if any(token in value for token in ("\\", "#", "$")):
        return None
    raw = PurePosixPath(value)
    candidates = [raw] if raw.suffix else [PurePosixPath(f"{value}{suffix}") for suffix in suffixes]
    for candidate in candidates:
        try:
            path = resolve_inside(ctx.paper, candidate.as_posix(), "latex dependency")
        except ProjectionError:
            return (f"unsafe:{value}", None)
        if path.is_file():
            return (relative_posix(path, ctx.paper), file_hash(path))
    if required:
        return (candidates[0].as_posix(), None)
    return None


def dependency_snapshot(ctx: Context, overlay: dict[str, bytes]) -> dict[str, str | None]:
    """Hash the exact static compile closure outside projected output bytes."""
    master_rel = relative_posix(ctx.master, ctx.paper)
    pending = [master_rel]
    visited: set[str] = set()
    snapshot: dict[str, str | None] = {}
    while pending:
        rel = pending.pop()
        if rel in visited:
            continue
        visited.add(rel)
        path = resolve_inside(ctx.paper, rel, "compile closure")
        if rel in overlay:
            content = overlay[rel]
        elif path.is_file():
            content = path.read_bytes()
            snapshot[rel] = sha256_bytes(content)
        else:
            snapshot[rel] = None
            continue
        text = strip_tex_comments(content.decode("utf-8", errors="replace"))

        for raw in INPUT_RE.findall(text):
            resolved = resolve_local_dependency(ctx, raw, (".tex",), required=True)
            if resolved is None:
                continue
            dep_rel, dep_hash = resolved
            if dep_hash is None:
                snapshot[dep_rel] = None
            else:
                pending.append(dep_rel)

        for raw in GRAPHICS_RE.findall(text):
            resolved = resolve_local_dependency(
                ctx, raw, (".pdf", ".png", ".jpg", ".jpeg", ".eps"), required=True
            )
            if resolved is not None:
                snapshot[resolved[0]] = resolved[1]

        for group in BIB_RE.findall(text):
            for raw in (item.strip() for item in group.split(",")):
                resolved = resolve_local_dependency(ctx, raw, (".bib",), required=True)
                if resolved is not None:
                    snapshot[resolved[0]] = resolved[1]

        for raw in BIBSTYLE_RE.findall(text):
            resolved = resolve_local_dependency(ctx, raw.strip(), (".bst",), required=False)
            if resolved is not None:
                snapshot[resolved[0]] = resolved[1]

        for raw in CLASS_RE.findall(text):
            resolved = resolve_local_dependency(ctx, raw.strip(), (".cls",), required=False)
            if resolved is not None:
                snapshot[resolved[0]] = resolved[1]

        for group in PACKAGE_RE.findall(text):
            for raw in (item.strip() for item in group.split(",")):
                resolved = resolve_local_dependency(ctx, raw, (".sty",), required=False)
                if resolved is not None:
                    snapshot[resolved[0]] = resolved[1]
    return dict(sorted(snapshot.items()))


def dependency_digest(snapshot: dict[str, str | None]) -> str:
    return sha256_bytes(
        json.dumps(snapshot, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )


def run_id_for(
    ctx: Context,
    names: list[str],
    files: dict[str, bytes],
    dependencies: dict[str, str | None],
) -> str:
    digest = hashlib.sha256()
    digest.update(RENDERER_VERSION.encode())
    digest.update(b"\0")
    digest.update(ctx.manifest_bytes)
    for name in sorted(names):
        digest.update(b"\0unit\0" + name.encode())
    for rel, content in sorted(files.items()):
        digest.update(b"\0path\0" + rel.encode() + b"\0")
        digest.update(content)
    digest.update(b"\0dependencies\0")
    digest.update(
        json.dumps(dependencies, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )
    return digest.hexdigest()


def metadata_bytes(
    ctx: Context,
    names: list[str],
    files: dict[str, bytes],
    sources: dict[str, Any],
    run_id: str,
    dependencies: dict[str, str | None],
) -> bytes:
    metadata = {
        "schema": SCHEMA,
        "renderer": RENDERER_VERSION,
        "candidate_id": run_id,
        "manifest": relative_posix(ctx.manifest_path, ctx.paper),
        "manifest_sha256": sha256_bytes(ctx.manifest_bytes),
        "units": names,
        "sources": sources,
        "outputs": {rel: sha256_bytes(content) for rel, content in sorted(files.items())},
        "dependencies": dependencies,
        "dependency_digest": dependency_digest(dependencies),
        "submission_before": submission_snapshot(ctx, files),
    }
    return (json.dumps(metadata, indent=2, sort_keys=True) + "\n").encode("utf-8")


def assert_direct_candidate(ctx: Context, candidate_arg: str) -> Path:
    candidate = resolve_inside(ctx.paper, candidate_arg, "--candidate")
    if candidate.parent.resolve() != ctx.candidate_root.resolve():
        raise ProjectionError("candidate must be a direct child of candidate_root")
    if not candidate.is_dir() or candidate.name.startswith(".partial-"):
        raise ProjectionError(f"candidate directory not found or incomplete: {candidate}")
    return candidate


def write_exclusive(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(content)


def write_receipt(ctx: Context, kind: str, payload: dict[str, Any]) -> Path:
    receipt_root = ctx.paper / "2-src" / "projection-receipts"
    receipt_root.mkdir(parents=True, exist_ok=True)
    body = {
        "schema": SCHEMA,
        "kind": kind,
        "created_at": datetime.now(timezone.utc).isoformat(),
        **payload,
    }
    encoded = (json.dumps(body, indent=2, sort_keys=True) + "\n").encode("utf-8")
    name = f"{utc_stamp()}-{kind}-{sha256_bytes(encoded)[:12]}.json"
    path = receipt_root / name
    write_exclusive(path, encoded)
    return path


def generate(ctx: Context, names: list[str]) -> dict[str, Any]:
    validate = validate_context(ctx)
    files, sources = build_expected(ctx, names)
    dependencies = dependency_snapshot(ctx, files)
    run_id = run_id_for(ctx, names, files, dependencies)
    final = ctx.candidate_root / run_id
    metadata = metadata_bytes(ctx, names, files, sources, run_id, dependencies)
    expected_all = {**files, "_projection.json": metadata}
    ctx.candidate_root.mkdir(parents=True, exist_ok=True)

    if final.exists():
        actual = {
            relative_posix(path, final): path.read_bytes()
            for path in final.rglob("*")
            if path.is_file()
        }
        if actual != expected_all:
            raise ProjectionError(f"candidate id collision or drift at {final}")
        reused = True
    else:
        partial = ctx.candidate_root / f".partial-{run_id}-{os.getpid()}"
        if partial.exists():
            raise ProjectionError(f"incomplete candidate already exists: {partial}")
        partial.mkdir(parents=False, exist_ok=False)
        # Intentionally no recursive cleanup: on failure the partial remains as evidence.
        for rel, content in sorted(expected_all.items()):
            target = resolve_inside(partial, rel, "candidate output")
            write_exclusive(target, content)
        os.rename(partial, final)
        reused = False

    receipt = write_receipt(
        ctx,
        "generate",
        {
            "candidate_id": run_id,
            "candidate": relative_posix(final, ctx.paper),
            "units": names,
            "gates": {"G0": "pass", "G1": "pass", "G2": "pass"},
            "reused": reused,
            "manifest_sha256": validate["manifest_sha256"],
            "source_hashes": {
                name: sources[name]["selected_sha256"] for name in sorted(sources)
            },
            "dependency_digest": dependency_digest(dependencies),
        },
    )
    return {
        "status": "ok",
        "candidate": relative_posix(final, ctx.paper),
        "candidate_id": run_id,
        "units": names,
        "reused": reused,
        "gates": {"G0": "pass", "G1": "pass", "G2": "pass"},
        "receipt": relative_posix(receipt, ctx.paper),
    }


def candidate_files(candidate: Path) -> dict[str, bytes]:
    return {
        relative_posix(path, candidate): path.read_bytes()
        for path in candidate.rglob("*.tex")
        if path.is_file()
    }


def candidate_units(ctx: Context, candidate: Path, metadata: dict[str, Any] | None) -> list[str]:
    if metadata is not None:
        names = metadata.get("units")
        if not isinstance(names, list) or not all(isinstance(name, str) for name in names):
            raise ProjectionError("candidate metadata has invalid units")
        return names
    paths = set(candidate_files(candidate))
    outputs = output_specs(ctx)
    unknown = sorted(paths - set(outputs))
    if unknown:
        raise ProjectionError(f"candidate contains undeclared outputs: {unknown}")
    return sorted({outputs[path][0] for path in paths})


def load_candidate_metadata(candidate: Path) -> dict[str, Any] | None:
    path = candidate / "_projection.json"
    if not path.exists():
        return None
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ProjectionError("candidate metadata must be a JSON object")
    return raw


def copy_deliverable(ctx: Context, destination: Path) -> None:
    for path in ctx.paper.iterdir():
        if path.name.startswith(("0-", "1-", "2-", "3-")):
            continue
        target = destination / path.name
        if path.is_file() and path.suffix in {".tex", ".bib", ".cls", ".bst", ".sty", ".cfg"}:
            shutil.copy2(path, target)
    for root in (*ctx.target_roots, *ctx.dependency_roots):
        if root.is_dir():
            shutil.copytree(root, destination / relative_posix(root, ctx.paper), dirs_exist_ok=True)


def missing_input_closure(ctx: Context, overlay: dict[str, bytes]) -> set[str]:
    """Return static \\input/\\include targets missing from a virtual overlay."""
    master_rel = relative_posix(ctx.master, ctx.paper)
    pending = [master_rel]
    visited: set[str] = set()
    missing: set[str] = set()
    while pending:
        rel = pending.pop()
        if rel in visited:
            continue
        visited.add(rel)
        path = resolve_inside(ctx.paper, rel, "compile input")
        if rel in overlay:
            text = overlay[rel].decode("utf-8", errors="replace")
        elif path.is_file():
            text = path.read_text(encoding="utf-8", errors="replace")
        else:
            missing.add(rel)
            continue
        text = strip_tex_comments(text)
        for raw in INPUT_RE.findall(text):
            if any(token in raw for token in ("\\", "#", "$")):
                continue  # dynamic TeX input; compiler remains the authority
            value = raw if PurePosixPath(raw).suffix else f"{raw}.tex"
            try:
                target = resolve_inside(ctx.paper, value, "latex input")
            except ProjectionError:
                missing.add(f"unsafe:{raw}")
                continue
            target_rel = relative_posix(target, ctx.paper)
            if target_rel in overlay or target.is_file():
                pending.append(target_rel)
            else:
                missing.add(target_rel)
    return missing


def compile_isolated(ctx: Context, candidate: Path) -> dict[str, Any]:
    latexmk = shutil.which("latexmk")
    if not latexmk:
        raise ProjectionError("G4 blocked: latexmk is not installed")
    overlay = candidate_files(candidate)
    baseline_missing = missing_input_closure(ctx, {})
    candidate_missing = missing_input_closure(ctx, overlay)
    introduced = sorted(candidate_missing - baseline_missing)
    if introduced:
        raise ProjectionError(f"G4 failed: candidate introduces missing inputs: {introduced}")
    if baseline_missing:
        raise ProjectionError(
            "G4 blocked: baseline submission input closure is already incomplete; "
            f"candidate did not introduce these paths: {sorted(baseline_missing)}"
        )
    master_head = "\n".join(
        ctx.master.read_text(encoding="utf-8", errors="replace").splitlines()[:20]
    ).lower()
    if "ts-program = xelatex" in master_head or "compile with: xelatex" in master_head:
        engine_flag = "-xelatex"
        engine = "xelatex"
    elif "ts-program = lualatex" in master_head or "compile with: lualatex" in master_head:
        engine_flag = "-lualatex"
        engine = "lualatex"
    else:
        engine_flag = "-pdf"
        engine = "pdflatex"
    with tempfile.TemporaryDirectory(prefix="haipipe-projection-") as temp_name:
        temp = Path(temp_name)
        copy_deliverable(ctx, temp)
        for rel, content in candidate_files(candidate).items():
            target = resolve_inside(temp, rel, "candidate compile overlay")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        master_rel = relative_posix(ctx.master, ctx.paper)
        completed = subprocess.run(
            [
                latexmk,
                engine_flag,
                "-interaction=nonstopmode",
                "-halt-on-error",
                master_rel,
            ],
            cwd=temp,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        pdf = temp / PurePosixPath(master_rel).with_suffix(".pdf")
        if completed.returncode != 0 or not pdf.is_file() or pdf.stat().st_size == 0:
            tail = "\n".join(completed.stdout.splitlines()[-60:])
            raise ProjectionError(f"G4 compile failed (exit {completed.returncode}):\n{tail}")
        log = temp / PurePosixPath(master_rel).with_suffix(".log")
        log_text = log.read_text(encoding="utf-8", errors="replace") if log.is_file() else ""
        unresolved_patterns = (
            r"LaTeX Warning: Citation .* undefined",
            r"LaTeX Warning: Reference .* undefined",
            r"There were undefined references",
        )
        if any(re.search(pattern, log_text) for pattern in unresolved_patterns):
            raise ProjectionError("G4 compile produced undefined citations or references")
        return {
            "status": "pass",
            "engine": engine,
            "pdf_bytes": pdf.stat().st_size,
            "log_tail": "\n".join(completed.stdout.splitlines()[-20:]),
        }


def check_candidate(
    ctx: Context,
    candidate: Path,
    *,
    compile_requested: bool,
    write_check_receipt: bool = True,
) -> dict[str, Any]:
    validate_context(ctx)
    metadata = load_candidate_metadata(candidate)
    names = candidate_units(ctx, candidate, metadata)
    if not names:
        raise ProjectionError("candidate contains no projected .tex outputs")
    expected, sources = build_expected(ctx, names)
    actual = candidate_files(candidate)
    if set(actual) != set(expected):
        raise ProjectionError(
            f"G2 candidate file set differs: actual={sorted(actual)}, expected={sorted(expected)}"
        )
    drift = [rel for rel in sorted(expected) if actual[rel] != expected[rel]]
    if drift:
        raise ProjectionError(f"G2 deterministic content mismatch: {drift}")

    evidence_findings: list[str] = []
    for rel, expected_bytes in expected.items():
        unit_name = output_specs(ctx)[rel][0]
        source_evidence = sources[unit_name]["evidence"][rel]
        source_cites = set(source_evidence["source_citations"])
        actual_text = strip_tex_comments(actual[rel].decode("utf-8"))
        missing_cites = sorted(source_cites - citation_keys(actual_text))
        source_questions = set(source_evidence["source_questions"])
        missing_questions = sorted(source_questions - set(QUESTION_RE.findall(actual_text)))
        if missing_cites or missing_questions:
            evidence_findings.append(
                f"{rel}: missing citations={missing_cites}, questions={missing_questions}"
            )
    if evidence_findings:
        raise ProjectionError("G3 evidence non-regression failed: " + "; ".join(evidence_findings))

    dependencies = dependency_snapshot(ctx, expected)
    metadata_status = "verified"
    if metadata is not None:
        if metadata.get("manifest_sha256") != sha256_bytes(ctx.manifest_bytes):
            raise ProjectionError("candidate manifest hash differs from current manifest")
        if metadata.get("dependencies") != dependencies:
            raise ProjectionError("candidate dependency closure differs from current paper")
        expected_id = run_id_for(ctx, names, expected, dependencies)
        if metadata.get("candidate_id") != expected_id or candidate.name != expected_id:
            raise ProjectionError("candidate id is not the deterministic content hash")
    else:
        metadata_status = "legacy-unreceipted"

    compile_result: dict[str, Any] | None = None
    if compile_requested:
        try:
            compile_result = compile_isolated(ctx, candidate)
        except ProjectionError as exc:
            gate_status = "blocked" if str(exc).startswith("G4 blocked:") else "failed"
            blocked = {
                "status": gate_status,
                "candidate": relative_posix(candidate, ctx.paper),
                "candidate_id": candidate.name,
                "units": names,
                "metadata": metadata_status,
                "gates": {
                    "G0": "pass",
                    "G1": "pass",
                    "G2": "pass" if metadata else "pass (legacy candidate; content exact)",
                    "G3": "pass",
                    "G4": gate_status,
                },
                "compile": None,
                "error": str(exc),
                "manifest_sha256": sha256_bytes(ctx.manifest_bytes),
                "source_hashes": {
                    name: sources[name]["selected_sha256"] for name in sorted(sources)
                },
                "dependency_digest": dependency_digest(dependencies),
            }
            receipt_rel = None
            if write_check_receipt:
                receipt = write_receipt(ctx, "check", blocked)
                receipt_rel = relative_posix(receipt, ctx.paper)
            suffix = f"; receipt={receipt_rel}" if receipt_rel else ""
            error_type = ProjectionBlocked if gate_status == "blocked" else ProjectionError
            raise error_type(f"{exc}{suffix}") from exc
    gates = {
        "G0": "pass",
        "G1": "pass",
        "G2": "pass" if metadata else "pass (legacy candidate; content exact)",
        "G3": "pass",
        "G4": "pass" if compile_requested else "not-run",
    }
    result = {
        "status": "ok",
        "candidate": relative_posix(candidate, ctx.paper),
        "candidate_id": candidate.name,
        "units": names,
        "metadata": metadata_status,
        "gates": gates,
        "compile": compile_result,
        "manifest_sha256": sha256_bytes(ctx.manifest_bytes),
        "source_hashes": {
            name: sources[name]["selected_sha256"] for name in sorted(sources)
        },
        "dependency_digest": dependency_digest(dependencies),
    }
    if write_check_receipt:
        receipt = write_receipt(ctx, "check", result)
        result["receipt"] = relative_posix(receipt, ctx.paper)
    return result


def atomic_write(path: Path, content: bytes, token: str) -> None:
    temp = path.with_name(f".projection-promote-{token}-{path.name}")
    if temp.exists():
        raise ProjectionError(f"promotion staging file already exists: {temp}")
    write_exclusive(temp, content)
    os.replace(temp, path)


def promote(
    ctx: Context,
    candidate: Path,
    approve: str,
    actor: str,
    reason: str,
) -> dict[str, Any]:
    if approve != "PROMOTE":
        raise ProjectionError("G5 requires the literal approval token: --approve PROMOTE")
    if not actor.strip() or not reason.strip():
        raise ProjectionError("G5 requires non-empty --actor and --reason")
    metadata = load_candidate_metadata(candidate)
    if metadata is None:
        raise ProjectionError("G5 refuses a legacy candidate without _projection.json")
    # Re-run G4 at promotion time so a stale or never-compiled candidate cannot
    # satisfy G5 merely by having passed the cheaper content checks earlier.
    check = check_candidate(ctx, candidate, compile_requested=True, write_check_receipt=False)
    actual_snapshot = submission_snapshot(ctx, candidate_files(candidate))
    if actual_snapshot != metadata.get("submission_before"):
        raise ProjectionError("G5 failed: submission targets changed after candidate generation")

    token = candidate.name[:12]
    backup_root = ctx.paper / "2-src" / "projection-receipts" / "backups" / f"{utc_stamp()}-{token}"
    backup_root.mkdir(parents=True, exist_ok=False)
    originals: dict[str, bytes | None] = {}
    promoted: list[str] = []
    try:
        for rel, content in sorted(candidate_files(candidate).items()):
            target = resolve_inside(ctx.paper, rel, "promotion target")
            original = target.read_bytes() if target.is_file() else None
            originals[rel] = original
            if original is not None:
                backup = resolve_inside(backup_root, rel, "promotion backup")
                write_exclusive(backup, original)
            target.parent.mkdir(parents=True, exist_ok=True)
            atomic_write(target, content, token)
            promoted.append(rel)
    except Exception:
        for rel in reversed(promoted):
            target = resolve_inside(ctx.paper, rel, "rollback target")
            original = originals[rel]
            if original is None:
                if target.exists():
                    target.unlink()
            else:
                atomic_write(target, original, f"rollback-{token}")
        raise

    receipt = write_receipt(
        ctx,
        "promote",
        {
            "candidate": relative_posix(candidate, ctx.paper),
            "candidate_id": candidate.name,
            "actor": actor,
            "reason": reason,
            "promoted": promoted,
            "backup_root": relative_posix(backup_root, ctx.paper),
            "submission_before": actual_snapshot,
            "submission_after": submission_snapshot(ctx, promoted),
            "gates": {**check["gates"], "G5": "pass"},
        },
    )
    return {
        "status": "ok",
        "candidate": relative_posix(candidate, ctx.paper),
        "promoted": promoted,
        "gates": {**check["gates"], "G5": "pass"},
        "receipt": relative_posix(receipt, ctx.paper),
        "backup_root": relative_posix(backup_root, ctx.paper),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "generate", "check", "promote"))
    parser.add_argument("--paper", default=".", help="paper root or a path inside it")
    parser.add_argument("--manifest", help="paper-relative manifest path")
    parser.add_argument("--unit", action="append", default=[], help="unit id; repeatable")
    parser.add_argument("--candidate", help="paper-relative candidate directory")
    parser.add_argument("--compile", action="store_true", help="run G4 in a disposable copy")
    parser.add_argument("--approve", default="", help="promotion token; must be PROMOTE")
    parser.add_argument("--actor", default="", help="human approving promotion")
    parser.add_argument("--reason", default="", help="human promotion rationale")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        ctx = load_context(args.paper, args.manifest)
        if args.command == "validate":
            result = {"status": "ok", **validate_context(ctx)}
        elif args.command == "generate":
            result = generate(ctx, select_units(ctx, args.unit))
        else:
            if not args.candidate:
                raise ProjectionError(f"{args.command} requires --candidate")
            candidate = assert_direct_candidate(ctx, args.candidate)
            if args.command == "check":
                result = check_candidate(ctx, candidate, compile_requested=args.compile)
            else:
                result = promote(ctx, candidate, args.approve, args.actor, args.reason)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except ProjectionBlocked as exc:
        print(json.dumps({"status": "blocked", "error": str(exc)}, indent=2), file=sys.stderr)
        return 3
    except (ProjectionError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
