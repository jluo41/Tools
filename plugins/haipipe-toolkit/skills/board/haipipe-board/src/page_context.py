"""Bounded cross-Page context declared under ``## Files``.

``Related Board Pages`` is a selective reading map, not dependency inference.
The current Page names which target Page fragment matters in which Page Phase;
the resolver follows those rows exactly once and never walks rows found in a
target Page.
"""
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
import re
from urllib.parse import unquote

from .common import ALIAS, PAGENAME
from .parse import parse_dir


# EVERY phase the lifecycle can dispatch, because haipipe-page-workflow SKILL.md
# §🔁 step 1 requires a context packet before EACH phase dispatch and this module
# could serve only four of the seven: `--phase OUTLINE` errored outright, and
# `--phase PROBE` silently returned EVIDENCE's scope (fixed 260821).
#
# PROBE had been an ALIAS of EVIDENCE since the 260816 rename. The 260817 split
# made them two phases with two different authorities, and the alias outlived it
# by four days. Retiring it renames nothing: every `· PROBE ·` row in the repo
# lives in template, snapshot or _archive text, and none in a live board page.
#
# PHASE_ALIASES stays as the mechanism, empty. The next rename adds one row here
# rather than a second hard-coded token list further down.
PHASE_ALIASES = {}
PHASES = ("OUTLINE", "DRAFT", "PROBE", "EVIDENCE", "REVISE", "COMPILE", "CHECK")
ROW_PHASES = PHASES + ("ALL",)
READABLE_ROW_PHASES = ROW_PHASES + tuple(PHASE_ALIASES)
RELATIONS = ("reads", "constrained by", "continues", "contrasts")

RELATED_HEADING_RE = re.compile(
    r"^###\s+🔗\s+Related Board Pages(?:\s+·\s+.+)?\s*$"
)
RELATED_ROW_RE = re.compile(
    r"^\s*[-*]\s+`(?P<relation>reads|constrained by|continues|contrasts)"
    r"\s+·\s+(?P<phase>" + "|".join(READABLE_ROW_PHASES) + r")`\s+·\s+"
    r"\[(?P<page_id>[A-Za-z][A-Za-z0-9-]*)\s+"
    r"(?P<scope>page|§\d+(?:\.\d+)*)\]"
    r"\((?P<path>[^)\s]+)\)\s*$"
)


@dataclass(frozen=True)
class RelatedPageRef:
    relation: str
    phase: str
    page_id: str
    scope: str
    path: str
    line: int


@dataclass(frozen=True)
class RelatedFinding:
    level: str
    code: str
    line: int
    message: str


class RelatedContextError(ValueError):
    """Raised when a context packet cannot be assembled without guessing."""


def _section_names(canon):
    return [canon] + ALIAS.get(canon, [])


def _section_source(text, canon):
    names = "|".join(re.escape(name) for name in _section_names(canon))
    found = re.search(
        rf"(?ms)^##\s+(?P<name>{names})\s*$\n?(?P<body>.*?)(?=^##\s+|\Z)",
        text,
    )
    if not found:
        return ""
    return f"## {found.group('name')}\n{found.group('body').rstrip()}".rstrip()


def _section_body(text, canon):
    source = _section_source(text, canon)
    return source.split("\n", 1)[1] if "\n" in source else ""


def _division_source(text, division_id):
    content = _section_body(text, "Content")
    if not content:
        return ""
    found = re.search(
        rf"(?ms)^###\s+(?:§\s*)?{re.escape(division_id)}"
        r"(?=\s+·|\s+[^.\d])[^\n]*\n?.*?(?=^###\s+|\Z)",
        content,
    )
    return found.group(0).rstrip() if found else ""


def _aim_group_source(text, canon, group_id):
    body = _section_body(text, canon)
    if not body:
        return ""
    found = re.search(
        rf"(?ms)^###\s+[AC]{re.escape(group_id)}(?:\s+·|\s*$)[^\n]*\n?.*?"
        r"(?=^###\s+|\Z)",
        body,
    )
    return found.group(0).rstrip() if found else ""


def scan_related_rows(text):
    """Return canonical rows plus malformed bullet rows and near-miss headings."""
    refs, findings = [], []
    in_files = False
    in_related = False
    in_fence = False
    for line_no, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("## "):
            in_files = line.strip() in {
                f"## {name}" for name in _section_names("Files")
            }
            in_related = False
            continue
        if not in_files:
            continue
        if line.startswith("### "):
            in_related = bool(RELATED_HEADING_RE.match(line))
            if "Related Board Pages" in line:
                if not in_related:
                    findings.append(RelatedFinding(
                        "ERROR", "related-group-name", line_no,
                        "use `### 🔗 Related Board Pages`; the exact group name is the parser boundary",
                    ))
            continue
        if not in_related or not re.match(r"^\s*[-*]\s+", line):
            continue
        match = RELATED_ROW_RE.match(line)
        if not match:
            findings.append(RelatedFinding(
                "ERROR", "related-row-form", line_no,
                "use `- `reads · EVIDENCE` · [QB7 §3](group/QB7-page.md)` "
                "with a supported relation, Page Phase, Page id, scope, and Board-relative path",
            ))
            continue
        row = match.groupdict()
        # A row written `· PROBE ·` selects the same phase as `· EVIDENCE ·`,
        # so the retired token never silently stops matching its own rows.
        row["phase"] = PHASE_ALIASES.get(row["phase"], row["phase"])
        refs.append(RelatedPageRef(line=line_no, **row))
    return refs, findings


def find_board_root(page_path):
    page = Path(page_path).resolve()
    for folder in (page.parent, *page.parents):
        if (folder / "board.md").is_file():
            return folder
    return None


def _safe_target(board_root, raw_path):
    decoded = unquote(raw_path).replace("\\", "/")
    pure = PurePosixPath(decoded)
    if (not decoded or pure.is_absolute() or ".." in pure.parts
            or decoded.startswith(("http://", "https://"))
            or any(ch in decoded for ch in "?#")):
        return None
    candidate = (board_root / Path(*pure.parts)).resolve()
    try:
        candidate.relative_to(board_root.resolve())
    except ValueError:
        return None
    return candidate


def _page_registry(board_root):
    _board, pages, _warnings = parse_dir(board_root)
    return {q.get("file", ""): q.get("id", "") for q in pages if q.get("file")}


def scope_exists(target_text, scope):
    if scope == "page":
        return True
    return bool(_division_source(target_text, scope[1:]))


def audit_related_rows(source_path, text=None):
    """Mechanically validate every declared related-Page row."""
    source = Path(source_path).resolve()
    text = source.read_text(encoding="utf-8") if text is None else text
    refs, findings = scan_related_rows(text)
    if not refs:
        return findings

    board_root = find_board_root(source)
    if board_root is None:
        return findings + [RelatedFinding(
            "ERROR", "related-no-board", refs[0].line,
            "no ancestor `board.md` exists, so Board-relative Page paths cannot resolve",
        )]

    registry = _page_registry(board_root)
    seen = set()
    for ref in refs:
        key = (ref.relation, ref.phase, ref.page_id, ref.scope, ref.path)
        if key in seen:
            findings.append(RelatedFinding(
                "WARN", "duplicate-related-row", ref.line,
                "the same relation, phase, Page, and scope is declared twice",
            ))
        seen.add(key)

        target = _safe_target(board_root, ref.path)
        if target is None:
            findings.append(RelatedFinding(
                "ERROR", "unsafe-related-path", ref.line,
                f"`{ref.path}` must be a Board-root-relative path with no climb, URL, query, or fragment",
            ))
            continue
        if target == source:
            findings.append(RelatedFinding(
                "ERROR", "related-self", ref.line,
                "a Page cannot declare itself as a Related Board Page",
            ))
            continue
        try:
            rel = target.relative_to(board_root).as_posix()
        except ValueError:
            rel = ""
        if (not target.is_file() or target.suffix.lower() != ".md"
                or not PAGENAME.match(target.name)):
            findings.append(RelatedFinding(
                "ERROR", "dead-related-page", ref.line,
                f"`{ref.path}` is not an existing Board Page source",
            ))
            continue
        target_id = registry.get(rel)
        if not target_id:
            findings.append(RelatedFinding(
                "ERROR", "unregistered-related-page", ref.line,
                f"`{ref.path}` is not discoverable as a Page on this Board",
            ))
            continue
        if target_id != ref.page_id:
            findings.append(RelatedFinding(
                "ERROR", "related-page-id", ref.line,
                f"the link says `{ref.page_id}` but `{ref.path}` is Page `{target_id}`",
            ))
            continue
        target_text = target.read_text(encoding="utf-8")
        if not scope_exists(target_text, ref.scope):
            findings.append(RelatedFinding(
                "ERROR", "dead-related-scope", ref.line,
                f"Page `{target_id}` has no direct Content division `{ref.scope}`",
            ))
    return findings


def extract_scope(target_text, scope, include_frame=True):
    """Return a whole Page or a compact closure around one Content division."""
    if scope == "page":
        return target_text.strip()
    division_id = scope[1:]
    division = _division_source(target_text, division_id)
    if not division:
        raise RelatedContextError(f"target Page has no Content division {scope}")
    group_id = division_id.split(".", 1)[0]
    identity = target_text.split("\n## ", 1)[0].rstrip()
    pieces = []
    if include_frame:
        pieces.append(identity)
        opening = _section_source(target_text, "Opening")
        if opening:
            pieces.append(opening)
    pieces.append(f"## Content\n{division}")
    aims = _aim_group_source(target_text, "Done when", group_id)
    if aims:
        pieces.append(f"## Aims\n{aims}")
    states = _aim_group_source(target_text, "Now", group_id)
    if states:
        pieces.append(f"## States\n{states}")
    return "\n\n".join(pieces).strip()


def related_context_packet(source_path, phase):
    """Build a one-hop Markdown packet for rows matching ``phase`` or ``ALL``."""
    phase = (phase or "").upper()
    phase = PHASE_ALIASES.get(phase, phase)
    if phase not in PHASES:
        raise RelatedContextError(
            f"phase must be one of {', '.join(PHASES)}; got {phase or '<empty>'}"
        )
    source = Path(source_path).resolve()
    text = source.read_text(encoding="utf-8")
    findings = audit_related_rows(source, text)
    errors = [f for f in findings if f.level == "ERROR"]
    if errors:
        raise RelatedContextError("; ".join(
            f"line {finding.line} {finding.code}: {finding.message}"
            for finding in errors
        ))

    refs, _ = scan_related_rows(text)
    selected = [ref for ref in refs if ref.phase in (phase, "ALL")]
    board_root = find_board_root(source)
    out = [
        f"# Related Board Pages · {source.name} · {phase}",
        "Traversal: one hop only; rows declared by a target Page are not followed.",
    ]
    if not selected:
        out.append("No Related Board Pages rows match this phase.")
        return "\n\n".join(out) + "\n"

    emitted = set()
    framed_targets = set()
    for ref in selected:
        key = (ref.relation, ref.page_id, ref.scope, ref.path)
        if key in emitted:
            continue
        emitted.add(key)
        target = _safe_target(board_root, ref.path)
        target_text = target.read_text(encoding="utf-8")
        include_frame = ref.path not in framed_targets
        framed_targets.add(ref.path)
        out.extend([
            f"## {ref.page_id} {ref.scope} · {ref.relation}",
            f"Source: `{ref.path}` · declared for `{ref.phase}`",
            extract_scope(target_text, ref.scope, include_frame=include_frame),
        ])
    return "\n\n".join(out) + "\n"
