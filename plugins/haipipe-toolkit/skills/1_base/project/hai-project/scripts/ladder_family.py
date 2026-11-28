"""Resolve a Block's ladder family; kept separate from audit/update mechanics."""

from pathlib import Path
import re


def field_of(text: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:[ \t]*([^\s#]+)", text)
    return match.group(1) if match else ""


def family_of(block: Path) -> str:
    face = block / "board.md"
    text = face.read_text(encoding="utf-8", errors="ignore") if face.is_file() else ""
    if (field_of(text, "board-kind") == "ideation-block" or block.name.startswith("Idea-")
            or block.parent.name in ("ideation", "ideations")):   # the old world still reads
        return "ideation"
    fam = field_of(text, "workbench")
    if fam:
        return fam
    if "discovery" in field_of(text, "board-kind") or block.parent.name in ("discovery", "discoveries"):
        return "discovery"
    if "cowork" in field_of(text, "board-kind") or block.parent.name == "cowork":
        return "cowork"
    if block.name.startswith("Labeling-") or block.parent.name in ("labeling", "labelings"):
        return "labeling"
    if block.name.startswith(("Paper-", "Grant-")) or block.parent.name in ("paper", "papers"):
        return "paper"
    # the special boards are named by their kind (hai-block, JL 261008)
    if block.name.startswith(("Insight-", "InsightQuestionBook-", "QuestionBook-", "Prototype-")) or block.parent.name in ("insight", "insights"):
        return "insight"
    if block.name.startswith("Design-") or block.parent.name in ("design", "designs"):
        return "design"
    return "task"

