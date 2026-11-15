"""The base readers of a Design Page-Folder: file and YAML reads, escaping, the contract
check, the Design Unit gate and the file-name patterns every other part reads.

Split out of design.py; design.py re-exports every name here."""
from __future__ import annotations

import html
import importlib.util
import re
import traceback
from pathlib import Path

from host_paths import skill_dir
from urllib.parse import quote

try:
    import yaml
except ImportError:  # the presenter must still explain itself without PyYAML
    yaml = None


_DESIGN_MARKER = re.compile(r"(?m)^\s*folder-kind:\s*design\s*$", re.I)
_LEGACY_RUN = re.compile(r"^r\d+_design(?:_|$)", re.I)
_RUN_FILE = re.compile(
    r"^(rd(\d+)_(commission|generate|verify|adopt)_[A-Za-z0-9][A-Za-z0-9_-]*)\.ya?ml$", re.I)
# the current name: run-design-<step>-<MMDD>-design-<N>[-2]; order is `sequence:`
_RUN_FILE_NEW = re.compile(
    r"^(run-design-(commission|generate|verify|adopt)-\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*)\.ya?ml$")
_TITLE = re.compile(r"(?m)^#\s+(.+?)\s*$")
_READS = re.compile(r"(?im)^\s*reads:\s*(.*?)\s*$")
_ITEM_HEAD = re.compile(r"^##\s+(ITEM\d+)\s*[·:-]\s*(.+?)\s*$")
_FIELD = re.compile(r"^([a-z][a-z-]*):\s*(.*?)\s*$")
_SIGNED = re.compile(r"(?im)^\s*signed:\s*(✅|⬜)\s*(.*?)\s*$")
_UNIT_CHECKER = skill_dir("haipipe-design-unit") / "scripts" / "check_unit.py"
_STEP = {"commission": "Commission", "generate": "Generate",
         "verify": "Verify", "adopt": "Adopt (historical)"}
_ITEM_FIELDS = ("type", "audience", "job", "goal", "stance", "basis", "mode",
                "expected", "falsified", "because")
_ITEM_LISTS = ("acceptance", "evidence")


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _escape(value) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def _yaml(path: Path) -> dict:
    if yaml is None or not path.is_file():
        return {}
    try:
        data = yaml.safe_load(_read(path))
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def _legacy_reason(page_src: Path, text: str = "") -> str:
    folder = page_src.parent
    if folder.parent.name == "2-DS-design":
        return "legacy 2-DS-design/DS* folder is not a current Design Folder"
    if (folder / "design").is_dir():
        return "legacy design/DU* storage is not a current Design Folder"
    runs = folder / "runs"
    if runs.is_dir() and any(_LEGACY_RUN.match(p.name) for p in runs.iterdir()):
        return "legacy rNN_design_* Run storage is not supported"
    if re.search(r"(?im)^\s*(?:schema|contract-version):\s*v?1(?:\.0)?\s*$", text):
        return "legacy v1 Page/Ticket/Result storage is not supported"
    return ""


def design_contract_status(page_src: Path) -> tuple[bool, str]:
    """Return whether ``page_src`` is a current Design Page-Folder."""
    text = _read(page_src)
    if not page_src.is_file():
        return False, "Design Page source is missing"
    reason = _legacy_reason(page_src, text)
    if reason:
        return False, reason
    if not _DESIGN_MARKER.search(text):
        return False, "the Page source has no folder-kind: design marker"
    return True, ""


def is_current_design_page(page_src: Path) -> bool:
    return design_contract_status(page_src)[0]


def _relative_href(root: Path, path: Path) -> str:
    """A safe static path for a file inside the server root."""
    try:
        rel = path.resolve().relative_to(root.resolve())
    except (OSError, ValueError, RuntimeError):
        return ""
    return "/" + "/".join(quote(part) for part in rel.parts)


def _nearest_board(page_src: Path) -> Path | None:
    for candidate in (page_src.parent, *page_src.parents):
        if (candidate / "board.md").is_file():
            return candidate
    return None


def _unit_gate():
    spec = importlib.util.spec_from_file_location("design_unit_gate", _UNIT_CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _audit(folder: Path) -> list[str]:
    """Run the Design Unit gate read-only; a missing checker is reported, not hidden."""
    if not _UNIT_CHECKER.is_file():
        return ["check_unit.py not found beside haipipe-design-unit"]
    try:
        module = _unit_gate()
        return [str(issue).replace(str(folder) + "/", "") for issue in module.audit_folder(folder)]
    except Exception as exc:  # noqa: BLE001 - a presenter never crashes on the checker
        traceback.print_exc()
        return [f"checker unavailable: {exc}"]
