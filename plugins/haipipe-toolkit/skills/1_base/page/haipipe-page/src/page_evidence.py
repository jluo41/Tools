"""Check the Page's selected DISPLAY Results and their Delivery projections.

The Evidence Item ledger points at each current typed Result. This module
resolves a DISPLAY Result's payload.unit, checks the unit's intake/render/
acceptance state, and compares cited labels with generated LaTeX. The retired
display folder is read only for Pages using the no-ledger migration profile.
It never renders, edits a unit, or records a human acceptance decision.
"""
from __future__ import annotations

import json
import re
from pathlib import Path


# The winning render, by the display family's unit contract. A unit is RENDERED
# when one of these exists AND `preview.pdf` was compiled from it: the asset
# alone is what a half-run renderer leaves behind.
WINNING_ASSETS = ("table-body.tex", "figure.pdf", "figure.png", "figure.svg")

# Legacy `<stem>-Display<N>-<slug>` unit folders are read only during migration.
UNIT_DIR_RE = re.compile(r"^(?P<stem>.+)-Display(?P<n>\d+)-(?P<slug>.+)$")
# Bare Display<N> tokens are accepted only by the no-ledger migration checker.
CITE_RE = re.compile(r"(?<!\w)Display(\d+)(?![\w-])")
DISPLAY_TOKEN_RE = re.compile(
    r"\\(?:figure|table|algorithm)\s*\{\s*(D_[A-Za-z][A-Za-z0-9_-]*)\s*\}"
)
DISPLAY_KEY_RE = re.compile(r"^D_[A-Za-z][A-Za-z0-9_-]*$")
LATEX_REF_RE = re.compile(r"\\(?:auto|C|c)?ref\{([^}]+)\}")
CODE_SPAN_RE = re.compile(r"`[^`\n]*`")

# BOTH row forms are in the wild and both are the unit contract's rows: QV2's
# units write `- claim: ...` and every CMSStoreBoard unit writes a bare
# `claim: ...`. Requiring the bullet read ZERO rows off 25 real units, which
# means no claim, no kind, and no `accepted:` tick was visible on any of them.
# The leading `-` is optional for that reason, and the key is length-capped so a
# prose sentence containing a colon cannot pose as a row.
#
# Four dialects on disk, and the bold marker lands on either side of the colon:
#   `- claim: x`  ·  `claim: x`  ·  `**Claim**: x`  ·  `- **Kind:** x`
README_ROW_RE = re.compile(
    r"^\s*(?:[-*]\s*)?\*{0,2}([A-Za-z][\w -]{0,24}?)\*{0,2}\s*:\s*\*{0,2}\s*(.*?)\s*$",
    re.M)

# The unit contract fixes five rows: claim / kind / caption-job / fragility /
# status (`display/ref/display-unit-output-contract.md`). Three dialects exist
# on disk and all three MEAN those rows, so all three are read and the drift is
# reported separately. Reading only one dialect and calling the others litter is
# how a checker teaches people to ignore it.
ROW_ALIASES = {
    "reader job": "caption-job",
    "caption job": "caption-job",
    "job": "caption-job",
    "evidence": "intake",
    "source": "intake",
    "what it shows": "claim",
    "shows": "claim",
}


def _rows(unit: Path) -> dict[str, str]:
    readme = unit / "README.md"
    if not readme.is_file():
        return {}
    text = readme.read_text(encoding="utf-8", errors="replace")
    rows = {}
    for key, value in README_ROW_RE.findall(text):
        key = key.strip().lower()
        rows.setdefault(ROW_ALIASES.get(key, key), value)
    return rows


def _newest(root: Path) -> float:
    """The newest mtime under a folder, 0.0 when it holds no file."""
    times = [p.stat().st_mtime for p in root.rglob("*") if p.is_file()]
    return max(times) if times else 0.0


def _page_home(page_source: Path) -> Path:
    """Current Page output home: the directory that contains its source."""
    return page_source.parent


def _legacy_display_root(page_source: Path) -> Path:
    """Read the old sibling folder only while a Page migrates to Results."""
    candidate = page_source.parent / page_source.stem
    return candidate / "display" if candidate.is_dir() else page_source.parent / "display"


def _yaml_scalar(value: str) -> str:
    """Decode the scalar fields needed from a Result envelope."""
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            decoded = json.loads(value)
            return decoded if isinstance(decoded, str) else str(decoded)
        except (TypeError, ValueError):
            return value[1:-1].replace("\\\\", "\\").replace('\\"', '"')
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value.split("#", 1)[0].strip()


def _minimal_result_document(text: str) -> dict:
    """Read the small, stable Result subset if PyYAML is unavailable."""
    result = {}
    for key in ("item", "type", "status", "display_kind"):
        match = re.search(rf"(?m)^{re.escape(key)}:[ \t]*(.*?)\s*$", text)
        if match:
            result[key] = _yaml_scalar(match.group(1))

    payload_match = re.search(
        r"(?ms)^payload:[ \t]*\n((?:^[ \t]+[^\n]*(?:\n|$))*)", text
    )
    payload = {}
    if payload_match:
        match = re.search(r"(?m)^[ \t]+unit:[ \t]*(.*?)\s*$", payload_match.group(1))
        if match:
            payload["unit"] = _yaml_scalar(match.group(1))
    result["payload"] = payload

    labels = []
    inline_labels = re.search(r"(?m)^labels:[ \t]*(\[.*\])[ \t]*$", text)
    if inline_labels:
        raw = inline_labels.group(1)
        try:
            value = json.loads(raw)
        except (TypeError, ValueError):
            try:
                import ast
                value = ast.literal_eval(raw)
            except (SyntaxError, ValueError):
                value = []
        if isinstance(value, list):
            labels.extend(str(item) for item in value)
    else:
        labels_match = re.search(
            r"(?ms)^labels:[ \t]*\n((?:^[ \t]+[^\n]*(?:\n|$))*)", text
        )
        if labels_match:
            entries = re.split(r"(?m)^[ \t]*-[ \t]+", labels_match.group(1))
            for entry in entries:
                fields = {}
                for line in entry.splitlines():
                    match = re.match(
                        r"^[ \t]*([A-Za-z_][A-Za-z0-9_-]*):[ \t]*(.*?)\s*$", line
                    )
                    if match:
                        fields[match.group(1)] = _yaml_scalar(match.group(2))
                if fields:
                    labels.append(fields)
                else:
                    token = _yaml_scalar(entry)
                    if token:
                        labels.append(token)
    result["labels"] = labels
    return result


def _result_document(manifest: Path) -> dict:
    try:
        text = manifest.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    try:
        value = json.loads(text)
    except (TypeError, ValueError):
        try:
            import yaml
        except ImportError:
            return _minimal_result_document(text)
        try:
            value = yaml.safe_load(text)
        except yaml.YAMLError:
            return _minimal_result_document(text)
    return value if isinstance(value, dict) else _minimal_result_document(text)


def _resolve_payload_unit(page_home: Path, manifest: Path, raw: object) -> Path | None:
    """Resolve payload.unit only inside the selected Result's payload tree."""
    if not isinstance(raw, str) or not raw.strip():
        return None
    value = raw.strip()
    root = manifest.parent / "payload"
    candidates = []
    placeholder = "<resolved-result>/"
    if value.startswith(placeholder):
        candidates.append(manifest.parent / value[len(placeholder):])
    path = Path(value)
    if path.is_absolute():
        candidates.append(path)
    else:
        candidates.extend((page_home / path, manifest.parent / path))
        if path.parts and path.parts[0] not in {"results", "payload"}:
            candidates.append(manifest.parent / "payload" / path)
    try:
        resolved_root = root.resolve()
    except OSError:
        return None
    for candidate in candidates:
        if candidate.is_symlink():
            continue
        try:
            resolved = candidate.resolve(strict=True)
            resolved.relative_to(resolved_root)
        except (OSError, ValueError):
            continue
        if resolved.is_dir():
            return resolved
    return None


def _display_label_key(label: object) -> str:
    if isinstance(label, str):
        token, kind = label.strip(), ""
        status = ""
    elif isinstance(label, dict):
        token = str(label.get("token") or label.get("label") or
                    label.get("placeholder") or label.get("key") or
                    label.get("reference") or "").strip()
        kind = str(label.get("kind") or "").strip().upper()
        status = str(label.get("status") or "").strip().lower()
    else:
        return ""
    if status in {"unresolved", "pending", "missing"}:
        return ""
    match = DISPLAY_TOKEN_RE.fullmatch(token)
    key = match.group(1) if match else token
    kind = kind or ("DISPLAY" if DISPLAY_KEY_RE.fullmatch(key) else "")
    return key if kind in {"DISPLAY", "TABLE"} and DISPLAY_KEY_RE.fullmatch(key) else ""


def _result_display_labels(document: dict) -> set[str]:
    labels = document.get("labels")
    if not isinstance(labels, list):
        return set()
    return {key for key in (_display_label_key(label) for label in labels) if key}


def current_display_results(page_source: Path) -> tuple[list[dict], bool]:
    """Ledger-selected DISPLAY envelopes, with confined payload paths.

    The boolean says a current typed DISPLAY Result exists even when its payload
    has not been produced yet. That prevents legacy folders from taking over a
    Page that has moved to Results.
    """
    page_home = _page_home(page_source)
    result_root = page_home / "results"
    records = {}
    from .evidence_selection import legacy_profile, selected_results
    saw_display = not legacy_profile(page_source)
    try:
        selection_errors = []
        manifests = selected_results(page_source, strict=False, errors=selection_errors)
    except OSError:
        return [], False
    for issue in selection_errors:
        if str(issue.get("type", "")).upper() not in {"DISPLAY", "TABLE"}:
            continue
        item = str(issue.get("item") or issue.get("reference") or "unresolved DISPLAY Result")
        records[item] = {
            "item": item,
            "manifest": None,
            "unit": None,
            "unit_ref": issue.get("reference"),
            "labels": set(),
            "status": "unresolved",
            "selection_error": issue.get("error", "invalid selected Result"),
        }
        saw_display = True
    for manifest in manifests:
        if manifest.is_symlink():
            continue
        try:
            manifest.resolve().relative_to(result_root.resolve())
        except (OSError, ValueError):
            continue
        document = _result_document(manifest)
        item = str(document.get("item", "")).strip()
        kind = str(document.get("type", "")).strip().upper()
        if kind not in {"DISPLAY", "TABLE"} and not re.search(r"-(?:DISPLAY|TABLE)-", item, re.I):
            continue
        saw_display = True
        payload = document.get("payload")
        raw_unit = payload.get("unit") if isinstance(payload, dict) else None
        unit = _resolve_payload_unit(page_home, manifest, raw_unit)
        key = item or manifest.relative_to(page_home).as_posix()
        records[key] = {
            "item": item or key,
            "manifest": manifest,
            "unit": unit,
            "unit_ref": raw_unit,
            "labels": _result_display_labels(document),
            "status": str(document.get("status", "")).strip().lower(),
        }
    return list(records.values()), saw_display


def display_result_requires_unit(status: str) -> bool:
    """Ready/complete Result states must point to a concrete payload unit."""
    token = re.sub(r"^[^a-z]+", "", str(status).replace("_", " ").lower())
    return token.startswith(("complete", "ready", "rendered", "accepted", "resolved"))


def unit_state(unit: Path) -> dict:
    """One display unit's position on the five-step walk.

    The step names and their order are the unified Evidence display lane's, adopted
    verbatim: ① INTAKE 🧑 → ② RENDER ⚙️ → ③ PICK 🧑 → ④ BUILD ⚙️ → ⑤ ACCEPT 🧑.
    """
    rows = _rows(unit)
    inputs = unit / "intake" / "inputs"
    has_intake = ((unit / "intake" / "manifest.yaml").is_file()
                  and inputs.is_dir()
                  and any(p.is_file() for p in inputs.rglob("*")))
    recipe = unit / "recipe"
    has_recipe = recipe.is_dir() and any(p.is_file() for p in recipe.rglob("*"))
    assets = unit / "assets"
    has_asset = assets.is_dir() and any(
        p.is_file() and p.name in WINNING_ASSETS for p in assets.rglob("*"))
    has_preview = (unit / "preview.pdf").is_file()
    accepted_text = rows.get("accepted", "").strip().lower()
    accepted = accepted_text.startswith(("✅", "yes", "true", "accepted"))

    rendered = has_asset and has_preview

    # TWO INDEPENDENT AXES, and conflating them mislabels real units. The tab's
    # "first missing step" walk is a to-do list; a CHECKER must say which of two
    # different things is wrong, because they have different consequences and
    # different fixes. Seven units on CMSStoreBoard are rendered and cited and
    # print correctly while carrying an `intake/manifest.yaml` whose
    # `intake/inputs/` was never frozen: calling those "not rendered" would send
    # someone to re-run a renderer that already worked.
    if not rendered:
        if not has_intake:
            missing = "① INTAKE · no frozen intake/manifest.yaml + inputs"
        elif not has_recipe:
            missing = "② RENDER · no renderer-owned recipe/"
        elif not has_asset:
            missing = "② RENDER · recipe/ produced no winning asset in assets/"
        else:
            missing = "④ BUILD · no preview.pdf"
    else:
        missing = ""            # a rendered candidate awaiting ⑤ is not a defect

    # Visible but untraceable: the render exists, the snapshot it was drawn from
    # does not, so no reader can get from a printed number back to its source.
    unfrozen = rendered and not has_intake

    # A tick binds a render to the inputs it was accepted WITH, so an intake
    # touched afterwards silently un-accepts the unit.
    stale_accept = bool(accepted and has_intake
                        and _newest(unit / "intake") > _newest(assets)
                        and _newest(assets) > 0)

    # DRAFT may PROPOSE a unit in owed state, and a proposal SAYS WHAT IT WILL
    # HOLD: `claim:` is what separates a promise from an empty folder someone
    # left behind. Without it nobody downstream can render the unit, and nobody
    # can tell whether it was ever meant to exist.
    proposed = bool(rows.get("claim", "").strip())

    return {
        "name": unit.name,
        "kind": rows.get("kind", ""),
        "proposed": proposed,
        "declared": True,
        "rendered": rendered,
        "accepted": accepted,
        "stale_accept": stale_accept,
        "unfrozen": unfrozen,
        "missing": missing,
    }


def display_units(page_source: Path) -> list[Path]:
    """Every current Result unit, falling back to the retired folder lane.

    Typed Results own current units. Legacy folder discovery remains readable
    only for Pages that have not yet written a typed DISPLAY Result.
    """
    results, saw_display = current_display_results(page_source)
    if saw_display:
        return sorted({record["unit"] for record in results if record["unit"]},
                      key=lambda path: path.as_posix())

    root = _legacy_display_root(page_source)
    if not root.is_dir():
        return []

    def key(path: Path) -> tuple:
        m = UNIT_DIR_RE.match(path.name)
        return (int(m.group("n")), path.name) if m else (10**6, path.name)

    return sorted((d for d in root.iterdir()
                   if d.is_dir() and not d.name.startswith((".", "_"))),
                  key=key)


def cited_ids(text: str) -> set[str]:
    """Every display unit id the page's prose cites, in either legal form."""
    prose, fence = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if not fence and not line.lstrip().startswith(">"):
            prose.append(CODE_SPAN_RE.sub(" ", line))
    return {n.lstrip("0") or "0" for n in CITE_RE.findall("\n".join(prose))}


def cited_display_labels(text: str) -> set[str]:
    """Page-facing D_ labels cited in prose, excluding quoted examples."""
    prose, fence = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if not fence and not line.lstrip().startswith(">"):
            prose.append(CODE_SPAN_RE.sub(" ", line))
    return set(DISPLAY_TOKEN_RE.findall("\n".join(prose)))


def cited_latex_refs(text: str) -> set[str]:
    """Manuscript labels cited directly with ref/autoref, excluding examples."""
    prose, fence = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith(chr(96) * 3):
            fence = not fence
            continue
        if not fence and not line.lstrip().startswith(">"):
            prose.append(CODE_SPAN_RE.sub(" ", line))
    return set(LATEX_REF_RE.findall("\n".join(prose)))


def _projection(page_source: Path, kind: str) -> Path | None:
    folder = _page_home(page_source)
    suffix = ".tex" if kind == "latex" else ".docx"
    current = folder / "delivery" / kind / f"{page_source.stem}{suffix}"
    if current.is_file():
        return current
    candidate = page_source.parent / page_source.stem
    legacy_home = candidate if candidate.is_dir() else folder
    legacy = legacy_home / kind / f"{page_source.stem}{suffix}"
    return legacy if legacy.is_file() else None


def _projection_embeds_unit(tex_text: str, tex_path: Path, unit: Path) -> bool:
    """Return whether generated TeX references a real asset inside this unit."""
    asset_root = (unit / "assets").resolve()
    refs = re.findall(
        r"\\(?:input|includegraphics)\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}",
        tex_text,
    )
    for raw in refs:
        ref = Path(raw.strip())
        candidate = ref if ref.is_absolute() else tex_path.parent / ref
        try:
            resolved = candidate.resolve()
            resolved.relative_to(asset_root)
        except (OSError, ValueError):
            continue
        if resolved.is_file() or any(
                resolved.with_suffix(suffix).is_file()
                for suffix in (".tex", ".pdf", ".png", ".jpg", ".jpeg", ".svg")):
            return True
    return False


def check_page_evidence(page_source: Path, text: str, name: str, rep,
                        error="ERROR", warn="WARN") -> None:
    """Report every gap between what the page promised and what it built.

    ``rep`` is `cli/check.py`'s report object; ``error``/``warn`` are its level
    constants, passed in so this module stays importable without the CLI.
    """
    result_records, has_typed_results = current_display_results(page_source)
    unresolved = []
    if has_typed_results:
        unit_records = [record for record in result_records if record["unit"]]
        for record in result_records:
            if record["unit"]:
                continue
            status = record["status"].replace("_", " ")
            raw_unit = record["unit_ref"]
            requires_unit = display_result_requires_unit(status)
            if record.get("selection_error") or raw_unit or requires_unit:
                unresolved.append(record)
                if record.get("selection_error"):
                    detail = (f"selected Result {raw_unit!r} is invalid: "
                              f"{record['selection_error']}" if raw_unit else
                              f"no selected Result is bound: {record['selection_error']}")
                else:
                    detail = (f"payload.unit {raw_unit!r} does not resolve inside this Result's payload/"
                              if raw_unit else
                              f"status is {status!r}, but payload.unit is missing")
                rep.add(error, "display-result-unit-unresolved",
                        f"{name} -> {record['item']}",
                        f"the current DISPLAY Result cannot supply its Page unit: {detail}.")
        units = [record["unit"] for record in unit_records]
    else:
        units = display_units(page_source)
        unit_records = [{"unit": unit, "item": unit.name, "labels": set()}
                        for unit in units]
    if not units and not unresolved:
        return

    states = [unit_state(u) for u in units]
    rendered = sum(1 for s in states if s["rendered"])

    for state in states:
        if not state["proposed"]:
            rep.add(error, "display-declared-no-claim",
                    f"{name} -> {state['name']}",
                    "the README states no claim under any of the contract's row "
                    "names or their known aliases, so nothing says what this unit "
                    "would show: no renderer can draw it and no reader can miss "
                    "it. A folder without a claim is not a proposal.")
        if state["missing"]:
            rep.add(error, "display-declared-not-rendered",
                    f"{name} -> {state['name']}",
                    f"declared but not rendered; first missing step is "
                    f"{state['missing']}. A unit folder is not a display, and "
                    f"the projections embed only rendered units, so this one "
                    f"is invisible to every reader of the PDF or docx.")
        if state["unfrozen"]:
            rep.add(error, "display-intake-unfrozen",
                    f"{name} -> {state['name']}",
                    "rendered, but `intake/inputs/` holds no frozen snapshot, so "
                    "nothing carries a printed number back to the run that "
                    "produced it. The render is fine; the provenance is missing.")
        if state["stale_accept"]:
            rep.add(error, "display-accept-stale",
                    f"{name} -> {state['name']}",
                    "`accepted: ✅` but intake/ is newer than assets/; the tick "
                    "binds a render that no longer matches its inputs. Re-render, "
                    "then have a person accept it again.")

    # The QV2 defect itself: the prose names a unit and the PDF never carries it.
    if has_typed_results:
        declared_labels = {
            label for record in result_records for label in record["labels"]
        }
        for token in sorted(cited_display_labels(text) - declared_labels):
            rep.add(warn, "display-label-unbound",
                    f"{name} -> {token}",
                    "no selected current DISPLAY Result declares this Page label; "
                    "Delivery leaves it visibly pending until the token is bound.")

    tex = _projection(page_source, "latex")
    if tex is not None:
        tex_text = tex.read_text(encoding="utf-8", errors="replace")
        if has_typed_results:
            cited = cited_display_labels(text)
            cited_refs = cited_latex_refs(text)
            by_label = {}
            by_ref = {}
            for record in unit_records:
                for label in record["labels"]:
                    by_label.setdefault(label, record)
                float_tex = record["unit"] / "float.tex"
                if float_tex.is_file():
                    body = float_tex.read_text(encoding="utf-8", errors="replace")
                    match = re.search(r"\\label\{([^}]+)\}", body)
                    if match:
                        by_ref.setdefault(match.group(1), record)
            cited_records = set()
            mentions = ([(label, by_label.get(label)) for label in cited]
                        + [(label, by_ref.get(label)) for label in cited_refs])
            for token, record in mentions:
                if record is None:
                    # Unbound Page tokens remain visible in draft mode.
                    continue
                cited_records.add(record["item"])
                unit = record["unit"]
                if not _projection_embeds_unit(tex_text, tex, unit):
                    state = unit_state(unit)
                    detail = ("it has no winning render, so the exporter skipped it"
                              if not state["rendered"]
                              else "it IS rendered, so this is an export fault")
                    rep.add(error, "display-cited-not-embedded",
                            f"{name} -> {token}",
                            f"cited in the prose but absent from "
                            f"{tex.parent.name}/{tex.name}; {detail}.")
            for record, state in zip(unit_records, states):
                if (state["rendered"] and record["labels"]
                        and record["item"] not in cited_records):
                    rep.add(warn, "display-rendered-not-cited",
                            f"{name} -> {record['item']}",
                            "rendered, but no sentence cites one of this Result's "
                            "D_ labels, so the projection has no placement point.")
        else:
            by_n = {}
            for unit, state in zip(units, states):
                m = UNIT_DIR_RE.match(unit.name)
                if m:
                    by_n[m.group("n").lstrip("0") or "0"] = (unit, state)
            for n in sorted(cited_ids(text), key=lambda v: int(v)):
                pair = by_n.get(n.lstrip("0") or "0")
                if pair is None:
                    rep.add(warn, "display-cited-unit-missing", f"{name} -> Display{n}",
                            "the prose cites this unit and no such folder exists "
                            "under the retired display/ lane")
                    continue
                unit, state = pair
                if not _projection_embeds_unit(tex_text, tex, unit):
                    detail = ("it has no winning render, so the exporter skipped it"
                              if not state["rendered"]
                              else "it IS rendered, so this is an export fault")
                    rep.add(error, "display-cited-not-embedded",
                            f"{name} -> Display{n}",
                            f"cited in the prose but absent from "
                            f"{tex.parent.name}/{tex.name}; {detail}.")

            cited = {n.lstrip("0") or "0" for n in cited_ids(text)}
            for n, (unit, state) in sorted(by_n.items(), key=lambda kv: int(kv[0])):
                if n not in cited and state["rendered"]:
                    rep.add(warn, "display-rendered-not-cited",
                            f"{name} -> {unit.name}",
                            "rendered but no sentence cites `Display" + n + "`, and "
                            "the projections embed only cited units, so this render "
                            "reaches no reader.")

        # The Page's own H1 must reach the document as a title block.
        if not re.search(r"\\(title|section\*?)\{", tex_text):
            rep.add(error, "latex-untitled", f"{name} -> {tex.name}",
                    "the exported .tex carries no title block, so the PDF opens "
                    "on its first body question with nothing naming it.")

        if tex.stat().st_mtime < page_source.stat().st_mtime:
            rep.add(warn, "projection-stale", f"{name} -> {tex.name}",
                    "the .tex is older than the Page source it projects; REVISE "
                    "changed the page and did not rebuild.")

    docx = _projection(page_source, "word")
    if docx is not None and docx.stat().st_mtime < page_source.stat().st_mtime:
        rep.add(warn, "projection-stale", f"{name} -> {docx.name}",
                "the .docx is older than the Page source it projects; REVISE "
                "changed the page and did not rebuild.")

    if units and rendered < len(units):
        rep.add(warn, "display-counts-split", name,
                f"{len(units)} declared · {rendered} rendered · "
                f"{sum(1 for s in states if s['accepted'])} accepted. The three "
                f"counts are independent and folder count is never completed work.")
