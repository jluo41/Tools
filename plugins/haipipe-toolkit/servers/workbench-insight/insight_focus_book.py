"""A Question Book's own parts on the shared focus page (the hooks focus_page.py asks for by name: parts,
delivery tabs, status, process, lead, map) and its views."""

from __future__ import annotations

from pathlib import Path

from live.ui_parts import _numbered
from live.insight_view_parts import _section
from live.insight_focus_parts import _page


# ── a Question Book's own parts (the shared page asks; round 1, 261106: "a Prototype is insight's") ────────────────────
def _marked(parts):
    """A Question Book's parts (title, word, html, …) with each state word as its mark; None stays None."""
    from live.insight_view_parts import mark
    return parts if parts is None else [(p[0], mark(p[1])) + tuple(p[2:]) for p in parts]


def prototype_parts(folder: Path, root: Path, level: str) -> list:
    """A Question Book's Findings parts before 📦 Delivery: the questions by release (Block) or by DIKW level (a release),
    each in words with its script; the proposals; the segments (insight_prototype.py)."""
    from live import insight_prototype as PR
    return _marked(PR.parts(folder, root, level))


def prototype_delivery_tabs(folder: Path, root: Path, level: str) -> list:
    """A Question Book's 📦 Delivery tabs, in place of the shared lanes: each release and the files a Board Job pins."""
    from live import insight_prototype as PR
    return _marked(PR.delivery_tabs(folder, root, level))


def prototype_status(folder: Path, root: Path, level: str) -> list:
    """A Question Book's Status bars in place of the shared ones: each release by its state and sign, each question by
    question.md and its Runs; a question its Runs (insight_prototype.py)."""
    from live import insight_prototype as PR
    return _marked(PR.status(folder, root, level))


def prototype_process(folder: Path, root: Path, level: str, view: str) -> list | None:
    """A Question Book's ⚙️ Process steps on a Work view, in place of the shared ones: on Findings triage its proposals
    and sign the question version, each a Copy prompt; on Status each question's next step, or "nothing to do"; None
    leaves the shared steps (insight_prototype.process)."""
    from live import insight_prototype as PR
    return _marked(PR.process(folder, root, level, view))


def prototype_lead(folder: Path, root: Path, level: str, view: str) -> str:
    """The main line a Question Book's Status or Findings opens with (insight_prototype.lead)."""
    from live import insight_prototype as PR
    return PR.lead(folder, root, level, view)


def prototype_map_branches(folder: Path, root: Path, level: str) -> list:
    """A release's MindMap: its questions by DIKW level, each leaf the question (insight_prototype.map_branches)."""
    from live import insight_prototype as PR
    return PR.map_branches(folder, root, level)


def prototype_map_top(folder: Path, root: Path, level: str) -> str:
    """Above a release's MindMap: its questions as a network (insight_prototype.map_top); a Question Book Block shows it
    in its Questions view instead."""
    from live import insight_prototype as PR
    return PR.map_top(folder, root, level) if level != "Block" else ""


PROTO_VIEWS = (("questions", "Questions"), ("ideas", "Ideas"), ("versions", "Versions"))


def prototype_views(folder: Path, root: Path, level: str) -> dict:
    """{key: (name, build)}: a Question Book's own buttons, Questions · Ideas · Versions (plain words, the
    list before the map, each thing shown once: the newest version's questions in Questions, a version's sign, what it
    added and its segments in Versions); {} for a release or any other page (the shared views draw it)."""
    from live import insight_prototype as PR
    if level != "Block":
        return {}
    folder, root = Path(folder), Path(root).resolve()
    proto = PR._proto(folder, level)
    if not proto["releases"]:
        return {}

    def sec(part):                                   # a Question Book part (title, word, html, waits[, share]) as a section
        return _section(part[0], part[2], part[1]) if part else ""

    def questions():
        return sec(PR._questions_newest(proto, root)) + _section("🕸 Question map", PR.map_top(folder, root, level), "version by version")

    def ideas():
        return sec(PR._proposals_part(PR._proposals(proto), root)) or "<p>No idea proposed yet.</p>"

    def versions():
        return "".join(sec(PR._version_part(proto, r, root)) for r in reversed(proto["releases"]))

    parts = {"questions": questions, "ideas": ideas, "versions": versions}
    return {key: (name, lambda key=key: _page(_numbered(parts[key]()))) for key, name in PROTO_VIEWS}


# a Question Book's own views carry no caption; the shared one is left off
prototype_CAPTIONS = {("Block", key): "" for key, _ in PROTO_VIEWS}
