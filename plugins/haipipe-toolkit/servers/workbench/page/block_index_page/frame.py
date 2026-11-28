"""The base frame every theme draws in, and the vanilla workbench when no theme is laid over it.

    Guide · Studio | Block · Job ▾ · Task ▾ | Delivery                top navigation
    Description | Report | Work | Runs                             work mode only
    <subspaces>                                                           the third row
    content                                                  │ Runs panel

Studio and Delivery are the Block's shared views (b10 s09-D05): one Studio and one delivery/ per
Block, opened from every level; Delivery at a Job or Task shows that level's part. Related, the
Block's related/ (what came in), folds inside the Studio, under its topic cards (b10 s04 Open 1,
JL 261011: "put the related as the second collapse part in the box of the studio items"); the Block's
delivery/ (what went out) folds under Related, every result previewed (JL 261014).
The frame owns the levels, shared Guide, Studio (with Related) and Delivery, the work Spaces, their order and
dividers, the third row, the Runs panel and the look (b10_project_workbench (removed 261126), Q08 and s02-studio-workbench-skill). A theme
gives only what each Space holds at each level: `servers/workbench-<theme>/<theme>_theme.py`
exports `THEME`, a `Theme`. A Space a theme leaves out shows the vanilla default, read from the
standard folders (the face `.md`, `studio/`, `reports/`, the child `jNN_` / `tNN_` folders,
`runs/`, `delivery/`), so a theme with nothing special works as is.

A theme may name its levels, pick which levels it has, name the subspaces of each Space, fill a
Space's content and list its run types. It may not change the levels, the six Spaces or their
order, draw its own tab rows, or carry its own look.

Read-only: nothing here writes. Every link is origin-relative (`/_board/workbench?path=…`).
"""

from __future__ import annotations

import json
import re
from dataclasses import replace
from pathlib import Path

# the frame's parts, by responsibility; every name stays readable as frame.X (`x as x`: re-exported)
from live.frame_base import (IN_STUDIO as IN_STUDIO, LEVELS as LEVELS, LEVEL_SKILL as LEVEL_SKILL, ROUTE as ROUTE,
                             RUN_ANY as RUN_ANY, SPACES as SPACES, SPACE_LABELS as SPACE_LABELS,
                             SPACE_NAMES as SPACE_NAMES, Space as Space, THEME_FOLDERS as THEME_FOLDERS,
                             TOP_ROW as TOP_ROW, Theme as Theme, VANILLA as VANILLA, _CLAIMS as _CLAIMS,
                             _LEVEL_OF as _LEVEL_OF, _PATTERNS as _PATTERNS, _PREFIXED as _PREFIXED,
                             _block_above as _block_above, _claimed as _claimed, _e as _e,
                             _empty_view as _empty_view, _fields as _fields, _file_url as _file_url, _link as _link,
                             _patterns_for as _patterns_for, _reader as _reader, _rel as _rel, _table as _table,
                             _theme_patterns as _theme_patterns, _title as _title, _yaml_scalar as _yaml_scalar,
                             chain as chain, children as children, esc as esc, face as face, fields as fields,
                             fill_tag as fill_tag, href as href, is_project as is_project, level_of as level_of,
                             link as link, named as named, pop as pop, reader as reader, rel as rel,
                             run_type as run_type, runs_of as runs_of, short_name as short_name, table as table,
                             theme_folder as theme_folder, theme_of as theme_of, title as title)
from live.frame_runs import (RUN_CSS as RUN_CSS, RUN_LEGEND as RUN_LEGEND, RUN_MARK as RUN_MARK,
                             _HARD_RUN as _HARD_RUN, _RUN_SKIP as _RUN_SKIP, _receipt as _receipt,
                             _run_status as _run_status, _tally as _tally, hard_runs as hard_runs,
                             run_cells as run_cells, runs_list as runs_list, runs_tally as runs_tally,
                             studio_runs as studio_runs)
from live.frame_css import CSS as CSS
from live.frame_js import (EMBED_JS as EMBED_JS, GUIDE_TITLE_JS as GUIDE_TITLE_JS, POP_HTML as POP_HTML,
                           POP_JS as POP_JS, STUDIO_JS as STUDIO_JS)
from live.frame_tasks import (_TASK_TYPE as _TASK_TYPE, _task_modules as _task_modules, task_card as task_card,
                              task_layouts as task_layouts, task_type as task_type)
from live.frame_studio import (DELIVERY_TYPES as DELIVERY_TYPES, READ_ONLY_MAPS as READ_ONLY_MAPS, STAGES as STAGES,
                               STRUCTURED as STRUCTURED, STUDIO_ITEM as STUDIO_ITEM, _FACTS as _FACTS,
                               _draw_url as _draw_url, _feed_chip as _feed_chip, _group_parts as _group_parts,
                               _hung_here as _hung_here, _note_facts as _note_facts, _notes as _notes,
                               _read_note_facts as _read_note_facts, _report_page as _report_page, _rungs as _rungs,
                               _sessions as _sessions, _short as _short, _split_tags as _split_tags,
                               _studio_parts as _studio_parts, _studio_topics as _studio_topics,
                               _studio_transcripts as _studio_transcripts, _topic_row as _topic_row,
                               _topic_rows as _topic_rows, is_structured as is_structured,
                               mindmap_module as mindmap_module, render_module as render_module,
                               structured_of as structured_of, studio_anchor as studio_anchor,
                               studio_inventory as studio_inventory, studio_parts as studio_parts,
                               topic_address as topic_address, topic_drawings as topic_drawings,
                               topic_label as topic_label, topic_owner as topic_owner)
from live.frame_groups import (GROUP_EMOJI as GROUP_EMOJI, GROUP_FILE as GROUP_FILE, GROUP_PALETTE as GROUP_PALETTE,
                               GROUP_SHELVES as GROUP_SHELVES, _GROUP_BAD as _GROUP_BAD,
                               _GROUP_RESERVED as _GROUP_RESERVED, _set_tags as _set_tags,
                               _write_group_order as _write_group_order, group_emoji as group_emoji,
                               group_file as group_file, group_list as group_list, studio_cards as studio_cards,
                               studio_group_order as studio_group_order, studio_sessions as studio_sessions)
from live.frame_pptx import (_DASH as _DASH, _Deck as _Deck, _EMU as _EMU, _MIME as _MIME,
                             _PPTX_CACHE as _PPTX_CACHE, _PRESET_COLOURS as _PRESET_COLOURS, _PX as _PX,
                             _pptx_geometry as _pptx_geometry, _pptx_one as _pptx_one,
                             _pptx_placeholder as _pptx_placeholder, _pptx_ppr as _pptx_ppr, _pptx_rpr as _pptx_rpr,
                             _pptx_shapes as _pptx_shapes, _pptx_text as _pptx_text, _pptx_xfrm as _pptx_xfrm,
                             _q as _q, pptx_media as pptx_media, pptx_preview as pptx_preview)
from live.frame_report import (AUDIENCE_VIEWS as AUDIENCE_VIEWS, Q_HEAD as Q_HEAD,
                               REPORT_SUGGESTED as REPORT_SUGGESTED, WHO_ASKS as WHO_ASKS,
                               _answer_ids as _answer_ids, _answering as _answering,
                               _first_sentence as _first_sentence, _opening as _opening,
                               _question_records as _question_records, _register as _register,
                               _register_set_groups as _register_set_groups, _report_cell as _report_cell,
                               _studio_links as _studio_links, _theme_fixed as _theme_fixed,
                               question_cell as question_cell, question_rows as question_rows,
                               report_view as report_view)
from live.frame_delivery import (DELIVERY_LANES as DELIVERY_LANES, DELIVERY_OPENS as DELIVERY_OPENS,
                                 DELIVERY_PIECES as DELIVERY_PIECES, LIVE_PAGE as LIVE_PAGE,
                                 RESULT_GROUPS as RESULT_GROUPS, _VERSION as _VERSION,
                                 _delivery_card as _delivery_card, _delivery_links as _delivery_links,
                                 _delivery_preview as _delivery_preview,
                                 _delivery_set_groups as _delivery_set_groups, _live_pages as _live_pages,
                                 _result_groups as _result_groups, _size as _size, _version_of as _version_of,
                                 delivery_items as delivery_items, delivery_view as delivery_view,
                                 live_url as live_url, version_label as version_label,
                                 version_panes as version_panes, version_roots as version_roots)
from live.frame_related import (PREVIEW_FRAME as PREVIEW_FRAME, PREVIEW_IMAGE as PREVIEW_IMAGE,
                                _DOCX_CACHE as _DOCX_CACHE, _related_folder as _related_folder,
                                _related_link as _related_link, _related_preview as _related_preview,
                                _related_set_groups as _related_set_groups, _related_target as _related_target,
                                _related_versions as _related_versions, docx_preview as docx_preview,
                                eml_preview as eml_preview, related_items as related_items,
                                related_rows as related_rows, related_view as related_view,
                                studio_delivery as studio_delivery, studio_related as studio_related)
from live.frame_nav import (OLD_VIEW_SPACE as OLD_VIEW_SPACE, _delivery_row as _delivery_row, _label as _label,
                            _level_row as _level_row, _options as _options, _spaces_row as _spaces_row,
                            delivery_by_source as delivery_by_source, delivery_parts as delivery_parts,
                            frame_redirect as frame_redirect)
from live.frame_timeline import (TIMELINE_KINDS as TIMELINE_KINDS, TIMELINE_LEVELS as TIMELINE_LEVELS,
                                 _NOTES_SEEN as _NOTES_SEEN, _YYMMDD as _YYMMDD, _decisions as _decisions,
                                 _drawing_notes as _drawing_notes, _session_day as _session_day, _yymmdd as _yymmdd,
                                 studio_timeline as studio_timeline, timeline_events as timeline_events)
from live.frame_sessions import sessions_part as sessions_part
from live.frame_folders import (FILE_ICONS as FILE_ICONS, FOLDER_SKIP as FOLDER_SKIP, FOLDER_WORDS as FOLDER_WORDS,
                                _run_word as _run_word, _shown as _shown, _when as _when, folder_rows as folder_rows,
                                folder_word as folder_word, studio_folder as studio_folder)
from live.frame_work import (WORK_CSS as WORK_CSS, _run_line as _run_line, _run_passes as _run_passes,
                             _short_title as _short_title, _theme_meta as _theme_meta, _work_job as _work_job,
                             _work_runs as _work_runs, _work_task as _work_task, task_action as task_action,
                             work_tree as work_tree)
from live.frame_spaces import (DISK_CSS as DISK_CSS, disk_markup as disk_markup, lays_out_page as lays_out_page,
                               spaces_for as spaces_for, vanilla as vanilla, vanilla_disk as vanilla_disk)
from live.frame_group_op import _group_members as _group_members, studio_group_op as studio_group_op


def _subs_row(theme, root, folder, space, view: Space) -> str:
    if not view.subspaces:
        return ""
    return ('<nav class="row subs">' + "".join(
        f'<a class="tab{" on" if s == view.open else ""}" href="{_e(href(folder, root, theme, space, s))}">{_e(s)}</a>'
        for s in view.subspaces) + "</nav>")


def render(theme: Theme, root: Path, folder: Path, space: str = "", sub: str = "", *, studio: bool = False) -> str:
    """One work level, or its shared Block Studio; Guide can replace either body."""
    from live.runs_panel import PANEL_CSS, PANEL_JS, SPLIT_CSS, panel_markup
    from live.space_views import SPACE_VIEW_CSS
    from live.work_items import WORK_ITEM_CSS
    from live.workbench_guide import mount_guide

    root, folder = root.resolve(), folder.resolve()
    level = level_of(folder) or "Block"
    # a Related link (space=Related, or the older Description › Related) opens the Studio with its
    # Related part unfolded (b10 s04, JL 261011)
    unfold = space in IN_STUDIO or (space == "Description" and sub in IN_STUDIO)
    studio = studio or space in ("Idea Studio", "Studio") or unfold   # saved Space links still open Studio
    space = space if space in SPACE_NAMES and space not in ("Idea Studio",) + IN_STUDIO else "Description"
    if unfold:
        sub = ""
    block = chain(folder, root).get("Block")
    owner = block if studio and block else folder      # the Block's, at every level
    owner_level = "Block" if studio and block else level
    views = spaces_for(theme, owner_level, owner, root, "" if studio else sub)
    view = views["Idea Studio" if studio else space]
    if studio:                                  # Related, the second folding part under the topic cards
        part = studio_related(views.get("Related") or Space(), owner, root, unfold)
        # then Delivery, the third: what went out (JL 261014); Runs, the fourth: each Task's hard Runs and their
        # status (JL 261019); Timeline, the fifth: what moved when (JL 261011); Folder, the sixth: what the folder holds
        view = replace(view, html=view.html + part.html + studio_delivery(owner, root, theme)
                       + studio_runs(owner, root, theme) + studio_timeline(owner, root) + studio_folder(owner, root)
                       + sessions_part(owner, root),
                       run_types=tuple(view.run_types) + tuple(part.run_types),
                       disk=tuple(view.disk) + tuple(part.disk))
    rel = _rel(owner, root)
    kinds = [dict(k, prompt=k.get("prompt", "").replace("{folder}", rel)) for k in view.run_types]
    panel = panel_markup("Idea Studio" if studio else space, kinds, [list(k.get("rows") or []) for k in kinds], base=root, fill=lambda row: {"page": rel, "folder": rel},
                         whole=f"this {theme.level_name(owner_level)}",
                         extra=f'<p class=mut style="margin:6px 0">{_e(view.note)}</p>' if view.note else "",
                         top=disk_markup(view.disk, owner, root),   # Disk folds with the Runs (JL 261007)
                         title="Disk · Runs" if view.disk else "Runs", compact=True, folded=True)
    md = face(folder)
    title = f"{theme.icon} {theme.label} · {folder.name}"     # the browser tab: the full folder name
    # the page's own title, under the level row (b03 s32-D13, JL 261008: "make the first line like the
    # page index and the second line to be the title of the webpage"): the theme, the level and its tag,
    # then the folder's own title (its face's heading)
    m = _PREFIXED.match(folder.name)
    tag = folder.name.split("_", 1)[0] if m else ""
    named = _title(md) if md else folder.name
    if tag and named != folder.name:            # a heading that starts with its own tag: said once
        named = re.sub(rf"^{re.escape(tag)}\b\s*[·:\-–]?\s*", "", named, flags=re.I) or named
    block_tag = block.name.split("_", 1)[0] if block and _PREFIXED.match(block.name) else ""
    block_context = f"{theme.level_name('Block')} {block_tag or short_name(block.name)}" if block else ""
    lead = f"{theme.level_name(level)} {tag}".strip()
    if level != "Block" and block_context:
        lead = f"{block_context} · {lead}"
    guide_title = f"{theme.icon} {theme.label} · Guide" + (f" · {block_context}" if block_context else "")
    heading = (f'{_e(theme.icon)} {_e(theme.label)} · <span class=lv>{_e(lead)} ·</span> {_e(named)}'
               if named != folder.name or tag else f'{_e(theme.icon)} {_e(theme.label)} · {_e(named)}')
    delivery = not studio and space == "Delivery"
    if studio or (delivery and block):          # a Block-owned view: the Block's name, from any level
        studio_context = block_tag or (short_name(block.name) if block else "No Block")
        block_md = face(block) if block else None
        block_name = _title(block_md) if block_md else (block.name if block else "")
        if block_tag:
            block_name = re.sub(rf"^{re.escape(block_tag)}\b\s*[·:\-–]?\s*", "", block_name, flags=re.I) or block_name
        elif block_name.startswith(studio_context):          # an untagged Board's title starts with its name: once
            block_name = block_name[len(studio_context):].lstrip(" ·:-–") or block_name
        heading = (f'{_e(theme.icon)} {_e(theme.label)} · {"Studio" if studio else "Delivery"} · '
                   f'<span class=lv>{_e(studio_context)}</span>')
        if block_name and block_name != studio_context:
            heading += f' · {_e(block_name)}'
    if delivery and block and folder == block:  # the Block's own Delivery lists every part, by source
        view = replace(view, html=view.html + delivery_by_source(theme, block, root))
    if studio:
        work_rows = ""
    elif delivery:                              # no Spaces row: the source row (Block · jNN · tNN), then a
        work_rows = ((_delivery_row(theme, root, block, folder) if block else "")   # lanes row if there is a choice
                     + (_subs_row(theme, root, folder, space, view) if len(view.subspaces or ()) > 1 else ""))
    else:
        work_rows = _spaces_row(theme, root, folder, space, view.open, views) + _subs_row(theme, root, folder, space, view)
    body_class = ("frame-body studio-body" if studio else "frame-body delivery-body" if delivery
                  else "frame-body")
    # No band line: the title keeps the Block context when the top button just says Block
    # (b03 s02-D08, JL 261010); the folder's path stays one hover away, on the title.
    where = f"{theme.level_name(level)} · {_rel(folder, root)} · " + (f"{theme.label} theme" if theme.name != "vanilla" else "vanilla")
    document = ('<!doctype html><html lang=en><head><meta charset=utf-8>'
                '<meta name=viewport content="width=device-width,initial-scale=1">'
                f'<title>{_e(title)}</title><link rel="icon" href="data:,">'
                # the base's shared view styles, which a theme's Spaces may use; never a theme's own
                # (b03, JL 261007: "base styles only": a theme carries no look of its own)
                f'<style>{CSS}{PANEL_CSS}{SPLIT_CSS}{SPACE_VIEW_CSS}{WORK_ITEM_CSS}{DISK_CSS}{WORK_CSS}</style></head><body><main>'
                + _level_row(theme, root, folder, level, space, sub, studio=studio)
                + f'<header class=page-title><h1 title="{_e(where)} · {_e(folder.name)}" '
                  f'data-guide="{_e(guide_title)}">{heading}</h1></header>'
                + f'<section class="{body_class}" data-owner="{_e(rel)}">'  # Guide replaces either body
                + work_rows
                + f'<div class=split><div class=space-main>{view.html}</div>'
                  f'{panel}</div></section>'
                f'{POP_HTML}</main><script>{PANEL_JS}{STUDIO_JS}{POP_JS}{EMBED_JS}{GUIDE_TITLE_JS}</script></body></html>')
    # as every workbench mounts it: the face's SPACE-relative path, and its file name
    # `level`: the Guide opens this level's section and folds the other two (b03 s31-D07)
    context = {"path": _rel(md, root) if md else rel, "file": md.name if md else "", "level": level}
    return mount_guide(document, theme.guide, context, "nav.levels", ".frame-body")


def themes() -> dict:
    """{name: Theme} from every workbench folder that has a `<name>_theme.py` exporting THEME."""
    import importlib
    from host_registry import workbench_folders, workbench_name
    found = {"vanilla": VANILLA}
    for folder in workbench_folders():
        name = workbench_name(folder)
        if (folder / f"{name}_theme.py").is_file():
            try:
                found[name] = importlib.import_module(f"live.{name}_theme").THEME
            except Exception:                    # a broken theme falls back to vanilla, never the page
                continue
    return found


# ── what the Guide's Space cards read live (b03 s31-D06): each level's sub · runs, from here ─────
def theme_for_guide(family: str) -> Theme:
    """The theme whose Guide family this is (its `guide`, or its own name), else vanilla."""
    for theme in themes().values():
        if family in (theme.guide, theme.name):
            return theme
    return VANILLA


def level_folders(folder: Path, root: Path) -> dict:
    """{level: folder} for the open folder's ladder: its own chain upward, then the first child of
    each level below it (a Block's first Job and that Job's first Task). A level with no folder is
    left out."""
    folder = folder.resolve()
    found = dict(chain(folder, root.resolve()))
    for parent, below in (("Block", "Job"), ("Job", "Task")):
        if below not in found and parent in found:
            kids = children(found[parent], parent)
            if kids:
                found[below] = kids[0]
    return found


def space_cards(theme: Theme, level: str, folder: Path | None, root: Path) -> list:
    """[(Space, subspaces, run type labels)] of one level, as its tabs show them: the base, then the
    theme (spaces_for). With no folder at that level, the theme's defaults: the same call over a
    folder that does not exist, so nothing on disk is read."""
    root = root.resolve()
    at = folder.resolve() if folder else root / f".no-{level.lower()}"
    views = spaces_for(theme, level, at, root)
    return [(name, tuple(views[name].subspaces), [k["label"] for k in views[name].run_types])
            for name in SPACE_NAMES]


def frame_json(theme: Theme, root: Path, folder: Path, sub: str = "") -> str:
    """The same frame as data: levels, Spaces and each Space's subspaces and run types (for tests
    and for a theme checking what it fills)."""
    level = level_of(folder.resolve()) or "Block"
    views = spaces_for(theme, level, folder.resolve(), root.resolve(), sub)
    return json.dumps({"theme": theme.name, "level": level, "levels": list(theme.levels),
                       "spaces": [{"name": n, "group": g, "optional": o, "subspaces": list(views[n].subspaces),
                                   "open": views[n].open, "run_types": [k["label"] for k in views[n].run_types],
                                   "run_doing": [k.get("doing") or k["label"] for k in views[n].run_types]}
                                  for n, g, o in SPACES]}, ensure_ascii=False)
