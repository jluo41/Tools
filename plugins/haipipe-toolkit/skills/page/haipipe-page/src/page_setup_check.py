"""Deterministic setup audit for a standalone Page Folder.

The audit distinguishes mechanical readiness from semantic or human gates.
Mechanical failures block ``setup``; unresolved editorial judgments remain
visible as deferred or untested checks instead of being reported as passes.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import re

from live.outline_preview import bullet_token, read_drafts
from src.page_workspace import dependency_files, load_page
from src.plan_shape import iter_plan_bullets, paragraph_order_findings


ALLOWED_STATUSES = {"pass", "missing", "deferred", "untested", "n/a"}
ALLOWED_ROLES = {
    "Condition", "Definition", "Evidence", "Example", "Implication",
    "Learning", "Mechanism", "Phenomenon", "Possibility", "Principle",
    "Problem", "Process", "Question", "Requirement", "Voice",
}


@dataclass(frozen=True)
class SetupCheck:
    id: str
    label: str
    status: str
    detail: str
    blocking: bool = False

    def __post_init__(self):
        if self.status not in ALLOWED_STATUSES:
            raise ValueError(f"Unsupported setup-check status: {self.status}")


@dataclass(frozen=True)
class SetupAudit:
    checks: tuple[SetupCheck, ...]
    artifacts: dict[str, dict[str, str]]

    @property
    def blocking_passed(self) -> bool:
        return all(item.status == "pass" for item in self.checks if item.blocking)

    def status_counts(self) -> dict[str, int]:
        return {
            status: sum(item.status == status for item in self.checks)
            for status in ("pass", "missing", "deferred", "untested", "n/a")
        }

    def as_dict(self) -> dict:
        return {
            "schema": "haipipe-page-setup-audit-v1",
            "blocking_gate": "pass" if self.blocking_passed else "fail",
            "summary": self.status_counts(),
            "artifacts": self.artifacts,
            "checks": [asdict(item) for item in self.checks],
        }

    def write_json(self, path: Path) -> None:
        path.write_text(json.dumps(self.as_dict(), indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")

    def markdown(self) -> str:
        rows = [
            "| Check | Status | Gate | Evidence or next action |",
            "|---|---|---|---|",
        ]
        for item in self.checks:
            detail = item.detail.replace("|", "\\|").replace("\n", " ")
            rows.append(
                f"| `{item.id}` · {item.label} | **{item.status}** | "
                f"{'blocking' if item.blocking else 'informational'} | {detail} |"
            )
        return "\n".join(rows)


def _section(text: str, name: str) -> str | None:
    match = re.search(rf"(?ms)^## (?:[^\w\n]+\s*)?{re.escape(name)}\s*\n(.*?)(?=^## |\Z)", text)
    return match.group(1).strip() if match else None


def _check(identifier: str, label: str, ok: bool, success: str, failure: str,
           *, blocking: bool = True) -> SetupCheck:
    return SetupCheck(identifier, label, "pass" if ok else "missing",
                      success if ok else failure, blocking)


def _configuration(page, face: str) -> SetupCheck:
    try:
        current = load_page(page.folder)
        explicit = (page.folder / "page.toml").is_file()
        ok = current.source == page.source and bool(re.search(r"(?m)^state:\s*\S+", face)) \
            and bool(re.search(r"(?m)^owner:\s*\S+", face))
        detail = (
            f"Page Face `{page.source.name}` resolves through "
            f"{'page.toml' if explicit else 'the same-stem convention'} with explicit state and owner."
        )
    except (OSError, ValueError) as error:
        ok, detail = False, str(error)
    return _check("source_configuration", "Source/configuration", ok, detail,
                  "No independently loadable Page Face with explicit state and owner was found.")


def _input_preservation(page, input_hash: str, input_file: Path | None,
                        strict: bool) -> SetupCheck:
    content = page.content or page.source
    imported_ok = content.is_file() and sha256(content.read_bytes()).hexdigest() == input_hash
    original_ok = True
    original_note = "External original was not available during this Folder resume."
    if input_file is not None:
        original_ok = input_file.is_file() and sha256(input_file.read_bytes()).hexdigest() == input_hash
        original_note = "The supplied original still matches the recorded intake hash."
    if imported_ok and original_ok:
        return SetupCheck(
            "input_preservation", "Input preservation", "pass",
            f"The imported editable copy matches `{input_hash}`. {original_note}", strict,
        )
    if strict:
        return SetupCheck(
            "input_preservation", "Input preservation", "missing",
            "The original or imported editable copy no longer matches the intake hash.", True,
        )
    return SetupCheck(
        "input_preservation", "Input preservation", "untested",
        "The editable source differs from the intake hash; this may be an intentional later edit, so resume does not certify original-byte preservation.",
    )


def _opening(face: str, title: str) -> SetupCheck:
    body = _section(face, "Opening")
    generic = body is None or "Working Page for " in body or len(re.sub(r"\s+", " ", body)) < 80
    named = body is not None and (title.lower() in body.lower() or "this page" in body.lower())
    return _check(
        "opening", "Opening", not generic and named,
        "Opening is Page-specific, non-placeholder prose that names the Page or its subject.",
        "Opening is missing, generic, or too thin to identify this Page's purpose and boundary.",
    )


def _plan_and_drafts(
    page, plan: Path | None, expect_shape: bool,
) -> tuple[SetupCheck, SetupCheck, SetupCheck, SetupCheck, SetupCheck]:
    if plan is None or not plan.is_file():
        status = "missing" if expect_shape else "deferred"
        detail = "No Shape exists for this Markdown setup." if expect_shape else "No plan exists on this Page yet."
        return (
            SetupCheck("outline_structure", "Outline", status, detail, expect_shape),
            SetupCheck("paragraph_global_order", "Page-global paragraph order", status, detail, expect_shape),
            SetupCheck("content_draft_mapping", "Bullet ↔ Content Draft", status, detail, expect_shape),
            SetupCheck("semantic_role_syntax", "Semantic role syntax", status, detail, expect_shape),
            SetupCheck("bullet_head_readability", "Bullet-head readability", status, detail, expect_shape),
        )
    text = plan.read_text(encoding="utf-8")
    blocks = list(iter_plan_bullets(text))
    divisions = re.findall(r"(?m)^## C(\d+)\s*·\s*(.+?)\s*$", text)
    paragraphs = re.findall(r"(?m)^### C\d+\.P\d+\s*·", text)
    evidence_rows = re.findall(r"(?m)^\s+Evidence:\s*\S.*$", text)
    outline_ok = bool(divisions and paragraphs and blocks) and len(evidence_rows) == len(blocks)
    outline = _check(
        "outline_structure", "Outline", outline_ok,
        f"Shape has {len(divisions)} divisions, {len(paragraphs)} paragraphs, {len(blocks)} Bullets, and one Evidence decision per Bullet.",
        "Shape is empty or lacks a division, paragraph, Bullet, or explicit Evidence decision.",
    )
    order_findings = paragraph_order_findings(text)
    paragraph_order = _check(
        "paragraph_global_order", "Page-global paragraph order", not order_findings,
        f"Paragraph identities form one uninterrupted P1–P{len(paragraphs)} Page sequence.",
        "; ".join(order_findings[:8]) or "Paragraph identities are not Page-global.",
    )
    drafts = read_drafts(page.source)
    mapping_ok = len(drafts) == len(blocks) and all(
        block["address"] in drafts
        and drafts[block["address"]].get("text", "").strip()
        and drafts[block["address"]].get("bullet-sha256") == bullet_token(block)
        for block in blocks
    )
    if not drafts and not expect_shape:
        mapping = SetupCheck(
            "content_draft_mapping", "Bullet ↔ Content Draft", "deferred",
            "This existing Page has no embedded Draft in its Outline; setup did not invent one.",
        )
    else:
        mapping = _check(
            "content_draft_mapping", "Bullet ↔ Content Draft", mapping_ok,
            f"All {len(blocks)} Bullets have nonempty, fingerprint-current Content Draft records.",
            "Content Draft coverage is missing, empty, extra, or stale against the current Shape.",
            blocking=expect_shape or bool(drafts),
        )
    roles = []
    for block in blocks:
        match = re.match(r"\[([^]]+)\]", block["head"].strip())
        roles.append(match.group(1) if match else "")
    role_ok = len(roles) == len(blocks) and all(role in ALLOWED_ROLES for role in roles)
    role_check = (
        _check(
            "semantic_role_syntax", "Semantic role syntax", role_ok,
            f"All {len(roles)} Bullets use a recognized semantic role label.",
            "One or more setup-generated Bullets lack a recognized semantic role label.",
        )
        if expect_shape else SetupCheck(
            "semantic_role_syntax", "Semantic role syntax", "n/a",
            "This existing Page was not created by semantic Markdown setup; its owner may use another Bullet grammar.",
        )
    )
    statements = [re.sub(r"^\[[^]]+\]\s*", "", block["head"].strip()) for block in blocks]
    banned = re.compile(
        r"^(?:open with|explain|introduce|name|connect|ask|keep|return|hand|state)\b",
        re.I,
    )
    dangling = re.compile(
        r"\b(?:a|an|and|because|for|of|or|that|the|to|when|which|while|with)$",
        re.I,
    )

    def clipped(block: dict[str, str], statement: str) -> bool:
        draft = re.sub(
            r"\s+", " ", drafts.get(block["address"], {}).get("text", "")
        ).strip()
        head = re.sub(r"\s+", " ", statement).strip()
        remainder = draft[len(head):] if head and draft.startswith(head) else ""
        return bool(remainder and (remainder[0].isspace() or remainder[0] in ",;:"))

    readable = all(
        4 <= len(re.findall(r"\b[\w’'-]+\b", statement)) <= 24
        and not statement.endswith(("…", "..."))
        and not dangling.search(statement)
        and not banned.match(statement)
        and not clipped(block, statement)
        for block, statement in zip(blocks, statements)
    )
    readability = (
        _check(
            "bullet_head_readability", "Bullet-head readability", readable,
            f"All {len(statements)} setup Bullet heads are complete 4–24 word provisional reader moves without clipping or planner imperatives.",
            "One or more setup Bullet heads are clipped, dangling, outside the 4–24 word provisional range, or written as planner instructions.",
        )
        if expect_shape else SetupCheck(
            "bullet_head_readability", "Bullet-head readability", "n/a",
            "This existing Page was not created by semantic Markdown setup; its owner may use another Bullet grammar.",
        )
    )
    return outline, paragraph_order, mapping, role_check, readability


def _content(page, face: str) -> SetupCheck:
    if page.content is not None:
        ok = page.content.is_file() and page.content.stat().st_size > 0
        detail = f"Bound editable Content `{page.content.relative_to(page.folder)}` is nonempty."
    else:
        body = _section(face, "Content")
        ok = bool(body and re.sub(r"\s+", " ", body).strip())
        detail = "Page-authored Content is present."
    return _check("content", "Content", ok, detail,
                  "No readable bound Content or authored Content body was found.")


def _aims(face: str, plan: Path | None, expect_shape: bool) -> SetupCheck:
    body = _section(face, "Aims")
    if body is None:
        return SetupCheck("aims_structure", "Aims structure", "missing",
                          "The Page has no Aims section.", True)
    records = list(re.finditer(
        r"(?ms)^-\s+[✅🔨🧠⬜❄️]\s+((?:A\d+\.\d+)|P\d+)\s*·.*?(?=^-\s+[✅🔨🧠⬜❄️]|^### |\Z)",
        body,
    ))
    complete = bool(records) and all("**Done when:**" in item.group(0) and "**Now:**" in item.group(0)
                                     for item in records)
    aligned = True
    alignment = "No initialized Shape requires division alignment."
    if plan is not None and plan.is_file():
        text = plan.read_text(encoding="utf-8")
        divisions = {int(n) for n in re.findall(r"(?m)^## C(\d+)\s*·", text)}
        groups = {int(n) for n in re.findall(r"(?m)^### A(\d+)\s*·", body)}
        aligned = groups == divisions if expect_shape else groups.issubset(divisions)
        alignment = f"Aim groups {sorted(groups)} align with Shape divisions {sorted(divisions)}."
    return _check(
        "aims_structure", "Aims structure", complete and aligned,
        f"{len(records)} Aim records have stable IDs, Done when, and Now. {alignment}",
        "Aims are missing stable records, Done when/Now fields, or division alignment.",
    )


def _delivery(page, delivery: Path) -> SetupCheck:
    marker = delivery.parent / ".haipipe-page-export"
    markup = delivery.read_text(encoding="utf-8") if delivery.is_file() else ""
    expected = dependency_files(page.content or page.source, page.folder)
    copied = all(
        (delivery.parent / item.relative_to(page.folder)).is_file()
        and sha256((delivery.parent / item.relative_to(page.folder)).read_bytes()).digest()
        == sha256(item.read_bytes()).digest()
        for item in expected
    )
    ok = bool(markup and marker.is_file() and "<main id=\"reading\"" in markup
              and f"<title>{escape(page.title)} · Page</title>" in markup and copied)
    return _check(
        "static_delivery", "Static website", ok,
        f"`{delivery.relative_to(page.folder)}` is a marked Page export and contains all {len(expected)} current source/assets.",
        "Static output is missing, malformed, unmarked, stale, or lacks a required source/asset.",
    )


def _artifacts(page, plan: Path | None, delivery: Path) -> dict[str, dict[str, str]]:
    candidates = {
        "page_face": page.source,
        "content": page.content or page.source,
        "shape": plan,
        "content_draft": plan if plan is not None and plan.is_file() else None,
        "static_delivery": delivery,
    }
    records = {}
    for name, path in candidates.items():
        if path is None or not path.is_file():
            continue
        records[name] = {
            "path": path.relative_to(page.folder).as_posix(),
            "sha256": sha256(path.read_bytes()).hexdigest(),
        }
    return records


def validate_setup(page, *, plan: Path | None, delivery: Path, mode: str,
                   input_hash: str, input_file: Path | None = None,
                   strict_input: bool = False) -> SetupAudit:
    """Evaluate every setup checklist category without claiming editorial approval."""
    face = page.source.read_text(encoding="utf-8")
    expect_shape = mode == "create-semantic-records" or "setup: semantic-markdown-v1" in face
    plan_text = plan.read_text(encoding="utf-8") if plan is not None and plan.is_file() else ""
    shape_approved = bool(re.search(r"(?m)^approved:\s*✅\s+\S", plan_text))
    outline, paragraph_order, drafts, roles, readability = _plan_and_drafts(
        page, plan, expect_shape
    )
    checks = [
        _configuration(page, face),
        _input_preservation(page, input_hash, input_file, strict=strict_input),
        _opening(face, page.title),
        outline,
        paragraph_order,
        drafts,
        roles,
        readability,
        _content(page, face),
        _aims(face, plan, expect_shape),
        _delivery(page, delivery),
        SetupCheck(
            "semantic_role_judgment", "Semantic-role judgment", "untested",
            "Role labels are mechanically valid, but an agent or person must review whether each role fits its reader move.",
        ),
        SetupCheck(
            "outline_logic_judgment", "Bullet-only argument review", "untested",
            "An agent or person must read the Bullet heads without the Content Draft and confirm that the argument remains intelligible, ordered, and complete.",
        ),
        SetupCheck(
            "aim_targets", "Aim targets", "deferred",
            "Targets are recorded, but setup cannot certify that the substantive targets are achieved.",
        ),
        SetupCheck(
            "human_shape_approval", "Human Shape approval",
            "pass" if shape_approved else "deferred",
            "The Shape records an explicit human approval."
            if shape_approved else "The generated Shape remains unapproved until a person accepts it.",
        ),
        SetupCheck(
            "human_content_acceptance", "Human Content acceptance", "deferred",
            "Candidate prose exists, but setup does not mark it accepted.",
        ),
        SetupCheck(
            "hosting", "Hosted Page", "n/a",
            "Setup requested a static build, not a live listener or deployment.",
        ),
    ]
    return SetupAudit(tuple(checks), _artifacts(page, plan, delivery))
