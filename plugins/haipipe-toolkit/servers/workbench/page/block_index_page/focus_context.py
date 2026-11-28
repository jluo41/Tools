"""PageContext: what one focus page knows while it is built, filled step by step by focus_render."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


@dataclass
class PageContext:
    """One page being built. page_route fills the request and the frame; each later step reads what it needs and
    sets what it makes (focus_render)."""
    # the request: section and group are rewritten as an old link resolves to a current view
    theme: Any
    root: Path
    folder: Path
    section: str = ""
    group: str = ""
    # the face and the level (page_route)
    data: dict = field(default_factory=dict)
    level: str = ""
    project_report: bool = False
    questions: list = field(default_factory=list)
    deliverables: list = field(default_factory=list)
    home: str = ""
    draft: dict = field(default_factory=dict)
    topics: list = field(default_factory=list)
    paper: bool = False
    retired: bool = False
    # the frame the page takes (page_route)
    live_work: bool = False
    paper_board: bool = False
    design_block: bool = False
    insight_block: bool = False
    draft_frame: bool = False
    version_frame: bool = False
    shared_frame: bool = False
    WF: Any = None                                   # live.work_frame on a shared frame
    context_frame: Any = None                        # the frame's own module (work, paper, design or draft)
    # the Report and Work views (report_view_map, work_view_map)
    untabbed: Callable | None = None
    events: list = field(default_factory=list)
    overview: dict = field(default_factory=dict)
    work: dict = field(default_factory=dict)
    own_first: bool = False
    # the rail's sections (rail_sections); inbox is read lazily by the Work views, after this step sets it
    delivery: Any = ""
    dviews: dict = field(default_factory=dict)
    look: dict = field(default_factory=dict)
    related: str = ""
    every: list = field(default_factory=list)
    inbox: list = field(default_factory=list)
    knows: list = field(default_factory=list)
    asked: dict = field(default_factory=dict)
    rail: list = field(default_factory=list)
    # the open section (section_body, around_work)
    view: Any = None
    merged: bool = False                 # a work page's views drawn as bands on one page (JL 261124)
    views: dict = field(default_factory=dict)
    selected: tuple = ()
    body: str = ""
    head: str = ""
    bar: str = ""
