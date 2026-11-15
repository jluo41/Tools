"""How one focus page is built, step by step on a PageContext: the frame it takes and which view an old link means,
its Report and Work views, the rail's sections, the open section's body, Around the Work, then the page itself."""
from __future__ import annotations

import re
import traceback
from pathlib import Path

from live import frame
from live.ui_parts import PB_JS
from live import interaction_section as IX
from live import focus_base, focus_interactions
from live.focus_context import PageContext
from live.focus_base import (GOAL_WORD, OTHER, UI_VIEWS, WORK_SHAPE, in_group, inside, kids, markdown, page_level,
    page_module, page_url, read_face, report_path, theme_parts)
from live.focus_styles_bands import BAND_CSS, numbered, side_css
from live.focus_ui import home_section, ui_view
from live.focus_interactions import card_interactions, interaction_where, known, standard_interactions
from live.focus_reports import (OLD_KEYS, OLD_VIEWS, THEME_ORDER, VIEW_WORDS, blocks_under, deliverables_html,
    overview_report_html, overview_summary, question_cards, reports_html, status_view, theme_title, themes_view)
from live.focus_tree import status_html
from live.project_branches import branches_html
from live.focus_studio import folder_html, related_html, studio_html, studio_none, timeline_events, timeline_html, topic_rows
from live.focus_delivery import delivery_html
from live.focus_themes import (_draft_css, design_views, draft_parts, insight_board_report, insight_job_work,
    insight_views_for, page_skills, paper_board_report, paper_board_work, paper_delivery, paper_delivery_views,
    paper_job_views, paper_look, paper_version_report, paper_version_work, view_items)
from live.focus_mindmap import parts_mindmap
from live.focus_findings import findings_board, job_findings, output_sections
from live.focus_plan_results import status_now_html, work_views
from live.focus_identity import page_identity_html
from live.focus_shell import page_shell, rail_kids, rail_link, rail_url


def page_route(theme, root: Path, folder: Path, section: str, group: str) -> PageContext:
    """Which frame the page takes and which section and view an old link means."""
    WF = context_frame = None                        # set only on a shared frame below
    data, level = read_face(folder, root), page_level(folder)
    project_report = level in ('Project', 'Theme')
    questions, question_errors = focus_base.owned_register(data, root, 'Questions', 'questions')
    deliverables, _ = focus_base.owned_register(data, root, 'Deliverables', 'deliverables')
    home = home_section(data, theme.name)
    draft = draft_parts(folder, root)                   # HOOK: a draft Task's own parts (focus_draft.py), else {}
    live_work = (theme.name in WORK_SHAPE and level in ('Block', 'Job', 'Task') and not draft
                 and page_module(theme.name, folder, root)[1] != 'prototype_')
    paper_board = theme.name == 'paper' and level == 'Block' and not draft
    design_block = False
    if theme.name == 'design' and level == 'Block' and not draft:
        from live import design_context
        design_block = design_context.applies(folder)
    insight_block = (level == 'Block' and not draft                # a Question Book and an insight Board take the work frame
                     and (page_module(theme.name, folder, root)[1] == 'prototype_'   # too: their own views, then 🧭
                          or theme.name == 'insight'))              # Around the Work (JL 261109: "check how did we do in the Work Theme")
    draft_frame = bool(draft)
    from live.board_read import is_version   # a version Job: 📋 Review Content, then 🧭 Around the Work, as a draft Task (JL 261113)
    version_frame = theme.name == 'paper' and level == 'Job' and not draft and is_version(folder)
    shared_frame = live_work or paper_board or design_block or insight_block or draft_frame or version_frame
    if shared_frame:
        from live import work_frame as WF
        context_frame = WF
    if paper_board:
        from live import paper_focus as context_frame
        if section in ('report', 'work', ''):
            section, group = 'report', group.removeprefix('work-').removeprefix('report-')
    if design_block:
        context_frame = design_context
        if section in ('report', 'work', ''):
            section, group = 'report', group.removeprefix('work-').removeprefix('report-')
            group = design_context.old_view(folder, group)   # Summary · Jobs · Methods open Designs · Rounds · Tests (261109)
    if draft_frame:
        from live import draft_context as context_frame
        if section in ('', 'work', 'report'):
            group = group.removeprefix('work-').removeprefix('report-')
            group = {'write': 'draft', 'revise': 'draft'}.get(group, group) or draft['open']   # old links (261113)
            section = 'report'
    if live_work:
        from live import work_frame as WF
        group = 'overview' if group == 'mindmap' else group  # old bookmarks remain usable
        if section == 'delivery':
            section, group = 'report', 'delivery'
    topics = topic_rows(folder, root, draft.get("studio") if draft else None)
    paper = theme.name == "paper"
    if paper and level in ("Job", "Task") and section == "work":   # Work is retired in the paper theme (JL 261111: "the
        section, group = "report", group.removeprefix("work-")    # Work is no longer used"): an old link, the same view
    retired = theme.name in ("design", "insight") and level in ("Job", "Task") and not draft   # the same rule (261111)
    if retired and section == "work":
        section, group = "report", group.removeprefix("work-")
    if section == "overview":
        section, group = "report", OLD_VIEWS.get(group, group)
    elif section == "report":
        group = OLD_VIEWS.get(group, group)
    if section in OLD_KEYS:
        reports_view = section == "reports" or (section == "overview-report" and group == "reports")
        section, group = OLD_KEYS[section]
        if reports_view and home == "overview-report":
            group = "answers"
    if project_report and section == 'work':
        section, group = 'report', {'progress': 'themes'}.get(group, group) or 'themes'
    if level in ('SPACE', 'Folder') and section == 'work':   # Work is retired (261111): an old link, the same Report view
        section, group = 'report', {'progress': 'projects'}.get(group.removeprefix('work-'), group.removeprefix('work-'))
    if draft_frame and section in ('work', 'report'):
        section, group = 'report', {'progress': 'status', 'standing': 'status'}.get(group, group)
    if live_work and section == 'work':                  # Work is retired (JL 261111): an old link, the same Report view
        section, group = 'report', group.removeprefix('work-') or 'standing'
    elif live_work and not section and level in ('Job', 'Task'):
        section, group = 'report', group or 'standing'
    return PageContext(theme=theme, root=root, folder=folder, section=section, group=group, data=data, level=level,
                       project_report=project_report, questions=questions, deliverables=deliverables, home=home,
                       draft=draft, topics=topics, paper=paper, retired=retired, live_work=live_work,
                       paper_board=paper_board, design_block=design_block, insight_block=insight_block,
                       draft_frame=draft_frame, version_frame=version_frame, shared_frame=shared_frame, WF=WF,
                       context_frame=context_frame)


def report_view_map(ctx: PageContext) -> None:
    """The Report section's views, in order, each built only when opened."""
    from live import project_page as PP
    theme, root, folder, section, group = ctx.theme, ctx.root, ctx.folder, ctx.section, ctx.group
    data, level, questions, home, draft, paper, topics = (ctx.data, ctx.level, ctx.questions, ctx.home, ctx.draft,
                                                          ctx.paper, ctx.topics)
    standing = (lambda: status_now_html(folder, root, level, topics)) if level in ("Block", "Job", "Task") and not draft else ""   # built only when opened (each took 4.5 s on b01)

    # Overview: read. Its views: Report (what we know: the recorded answers first), Questions, Context, Pipeline,
    # Timeline; each piece of content in one view only.
    untabbed = lambda html: re.sub(r'<nav class="overview-tabs".*?</nav>', '', html, flags=re.S)
    has_reports = any(report_path(row, folder, root) for row in questions)
    report = ""
    if home == "overview-report":
        report = untabbed(overview_report_html(data, questions, folder, root, False))
    elif theme.name in WORK_SHAPE and level == "Block" and not draft:
        report = lambda: findings_board(questions, folder, root, markdown(data["takeaways"], folder, root) if data["takeaways"] else "",
                                        theme_parts(theme.name, folder, root, level))   # built only when opened
    elif theme.name in WORK_SHAPE and level == "Job" and not draft:   # the Block's Findings, one level down (round 2, 261106)
        report = lambda: job_findings(folder, root, theme_parts(theme.name, folder, root, level))
    elif has_reports:
        report = reports_html(questions, folder, root)
    elif questions:
        report = question_cards(questions, folder, root, detailed=theme.name in WORK_SHAPE)   # it is their only view there
    elif data["takeaways"]:
        report = markdown(data["takeaways"], folder, root)
    elif paper and not draft:
        report = '<p class="mut">No takeaways recorded in this page’s Markdown.</p>'
    events = timeline_events(folder, root)
    overview = {}
    if level == "Project":                                    # JL 261109: the Project's buttons are its Themes, the
        overview["mindmap"] = ("Project", lambda: PP.project_top(folder, root) + PP.mindmap_view(folder, root) + PP.face_sections(folder, root))   # whole Project's map first
        for th in sorted(kids(folder), key=lambda t: THEME_ORDER.index(t.name) if t.name in THEME_ORDER else 99):
            if page_level(th) == "Theme":
                overview["theme-" + th.name] = (theme_title(th.name), lambda th=th: PP.theme_report(th, root))
        if group in ("findings", "themes", "status"):        # an old Project link opens the Project button
            group = "mindmap"
    elif level in ("SPACE", "Folder"):                       # the front door (JL 261114): Home, then Chart; what each
        from live.space_home import space_home               # Project found is its own page's, never listed here
        overview["home"] = ("Home", lambda: space_home(folder, root))
        if group in ("mindmap", "findings", "themes", "status", "projects"):   # an old link opens Home
            group = "home"
    elif level == "Theme":                                   # JL 261029 sketch: MindMap · Summary · Blocks · Status
        under = blocks_under(folder)
        overview["mindmap"] = ("MindMap", lambda: PP.mindmap_view(folder, root))
        overview["findings"] = ("Findings", overview_summary(folder, root, level, events))
        overview["themes"] = ("Themes", lambda: themes_view(folder, root))
        overview["status"] = ("Plan + Results", lambda: status_view(under, root))
    if level in ("Block", "Job", "Task"):                       # its own parts as a map, as above the Block
        overview["mindmap"] = ("MindMap", lambda: parts_mindmap(folder, root))
    if standing:
        overview["standing"] = ("Plan + Results", standing)            # where its sNN, Jobs and Tasks stand
    if report:
        overview["findings"] = ("Findings", report)            # what it has found: answers, takeaways
    if draft:                                                  # HOOK: Text · Review · Status (focus_draft.report_views)
        overview.update(draft["report"])
    if home == "overview-report" and has_reports:
        overview["answers"] = ("Answers", untabbed(overview_report_html(data, questions, folder, root, True)))
    if questions and theme.name not in WORK_SHAPE:                     # a work page's Questions live in Findings (JL 261104: "we don't need the questions")
        overview["questions"] = ("Questions", question_cards(questions, folder, root, detailed=True))
    for key, name in UI_VIEWS:                                 # a theme Block's real pages, level by level
        if data["ui"][key]:
            overview["ui-" + key] = (name, ui_view(data["ui"][key], name, root, folder, folder / "walks" / f"{key}.html"))
    if theme.name == "design" and level in ("Block", "Job", "Task") and not draft:   # HOOK: the design letters (b12 j01),
        letters = design_views(folder, root, "report")                                # the shared MindMap last (R6), and
        if letters:                                                                    # Report opens on its first letter
            overview = {**letters, **{k: v for k, v in overview.items() if k == "mindmap"}}
            group = ("summary" if group == "findings" and "summary" in letters      # OLD_VIEWS read its Summary as Findings
                     else group or (next(iter(letters)) if section in ("", "report") else ""))
    if theme.name == "insight" and level == "Block" and not draft:   # HOOK: an insight Board's letters (b11 s51), MindMap last
        letters = insight_board_report(folder, root)
        overview = {**letters, **{k: v for k, v in overview.items() if k == "mindmap"}} if letters else overview
    own_first = False                                          # a page whose own views open on their first
    if level == "Block" and not draft and page_module(theme.name, folder, root)[1] == "prototype_":   # HOOK: a Question Book's
        try:                                                         # own buttons, Questions · Versions · Ideas · Method
            from live import insight_focus as _IF                    # (JL 261109), the shared MindMap last
            letters = _IF.prototype_views(folder, root, level)
        except Exception:
            traceback.print_exc()
            letters = {}
        if letters:
            overview = {**letters, **{k: v for k, v in overview.items() if k == "mindmap"}}
            own_first = True
    if theme.name == "insight" and level in ("Job", "Task") and not draft:   # HOOK: insight Job and Task letters (s54, s57),
        letters = insight_views_for(folder, root, "report")                     # MindMap last (a Job draws its own)
        overview = {**letters, **{k: v for k, v in overview.items() if k == "mindmap" and k not in letters}} if letters else overview
    if paper and level == "Job" and not draft:                 # HOOK: a version's Report, its Work's six views (261106),
        version_views = paper_version_report(folder, root)       # a version: Structure · Evidence · Display only
        own = version_views or paper_job_views(folder, root, "report")   # (JL 261113); an evidence or submission
        if own:                                                  # Job's views keep the MindMap first
            overview = own if version_views else {**{k: v for k, v in overview.items() if k == "mindmap"}, **own}
    if paper and level == "Task" and not draft:                # HOOK: a paper evidence Task, what it made first (paper_tasks)
        from live import paper_tasks; overview = paper_tasks.views(folder, root, "report", overview)
    if paper and level == "Block":                             # HOOK: a paper Board's own parts, then its MindMap; no
        overview = paper_board_report(folder, root) or {k: v for k, v in overview.items() if k == "mindmap"}  # no Status, Findings, Questions (JL 261031: "no need to use
                                                                 # them anymore"); the mind map is a section of each part
    ctx.untabbed, ctx.events, ctx.overview, ctx.group, ctx.own_first = untabbed, events, overview, group, own_first


def work_view_map(ctx: PageContext) -> None:
    """The Work section's views, and the Report's where a frame or theme shares them. The Work views read the inbox
    only when built, after rail_sections has set it."""
    from live import project_page as PP
    theme, root, folder, data, level = ctx.theme, ctx.root, ctx.folder, ctx.data, ctx.level
    questions, deliverables, home, draft, paper, topics = (ctx.questions, ctx.deliverables, ctx.home, ctx.draft,
                                                           ctx.paper, ctx.topics)
    live_work, project_report, paper_board, design_block = ctx.live_work, ctx.project_report, ctx.paper_board, ctx.design_block
    draft_frame, retired, WF, context_frame = ctx.draft_frame, ctx.retired, ctx.WF, ctx.context_frame
    untabbed, overview = ctx.untabbed, ctx.overview
    inbox_fn = lambda: ctx.inbox
    if live_work:
        work_topics = WF.topics_for(folder, root, questions)
        def live_findings():
            from live import work_sections
            if own := work_sections.view_html(folder, root, data, 'findings', WF.section):   # the face names its own
                return side_css() + own + PB_JS
            if home == 'overview-report':
                return untabbed(overview_report_html(data, questions, folder, root, False))
            if theme.name not in ('discovery', 'cowork'):        # work: Values and Displays only (JL 261111)
                return PP.work_findings(folder, root)
            extra = theme_parts(theme.name, folder, root, level)
            if level == 'Block':
                return findings_board(questions, folder, root, markdown(data['takeaways'], folder, root), extra, include_delivery=False, questions=theme.name in ('discovery', 'cowork'))
            if level == 'Job':
                return job_findings(folder, root, extra, include_delivery=False)
            return side_css() + numbered(output_sections(folder, root) + list(extra)) + PB_JS
        overview = {
            'overview': ('Overview', lambda: WF.overview(folder, root, data, questions, work_topics)),
            'standing': ('Plan + Results', lambda: WF.status(folder, root, data, work_topics)),
            'findings': ('Findings', live_findings),
            'delivery': ('Delivery', lambda: WF.delivery(folder, root, data)),
            **{k: v for k, v in overview.items() if k.startswith('ui-') or (home == 'overview-report' and k == 'answers')},
        }

    # Work: do. Its views: Progress (the children, or a Task's Runs), Deliverables, Files.
    work = {"progress": ("Job-Versions" if paper and level == "Block" else "Progress",
                         lambda: status_html(folder, root, level, [] if overview else questions))}   # built when opened
    if draft:                                            # HOOK: the five steps, then the Task's Runs
        _runs = work["progress"][1]                      # the steps' button words need the draft's own CSS on Runs too
        work = {**{k: v for k, v in draft["work"].items() if k != "runs"},   # (261105: "1 · Plannext" ran together)
                "runs": ("Runs", lambda: _draft_css() + (_runs() if callable(_runs) else _runs))}
    if theme.name in WORK_SHAPE and level in ("Block", "Job", "Task") and not draft:   # the same views as Report (JL 261104)
        work = work_views(overview, folder, root, level, questions, inbox_fn, work["progress"][1], topics,
                          live_status=live_work, results_first=live_work)
        if live_work:
            overview = work
    if data["sections"].get("deliverables") and not live_work:
        work["deliverables"] = ("Deliverables", deliverables_html(deliverables, folder, root) if deliverables
                                else markdown(data["sections"]["deliverables"], folder, root))
        if project_report:
            overview['deliverables'] = work['deliverables']
    if level in ("SPACE", "Folder"):                     # its Projects and progress chart are Report views now (JL 261111:
        if level == "SPACE":                             # the SPACE's progress chart, one click away (the old Home)
            overview["chart"] = ("Chart", '<p><a class="row-verb" href="/?view=chart">Open the progress chart</a> '
                                          '<a class="row-verb" href="/?view=list">Open the list index</a></p>')
        work = overview
    if paper and level == "Job" and not draft:           # HOOK: a paper version's Work, by band (s36-D01, D02), or an
        work = paper_version_work(folder, root) or paper_job_views(folder, root, "work") or work   # evidence or submission Job's
    if paper and level == "Task" and not draft:          # HOOK: a paper evidence Task's Work, Report's views (paper_tasks)
        from live import paper_tasks; work = paper_tasks.views(folder, root, "work", work)
    if paper and level == "Block":                       # HOOK: a paper Board's Work shares its Report's list
        if paper_board:
            overview = context_frame.report_views(folder, root)
            work = overview  # legacy Work URLs resolve to the same Report view
        else:
            work = paper_board_work(folder, root, work["progress"][1]()) or work
    if theme.name == "design" and level in ("Block", "Job", "Task") and not draft:   # HOOK: the design letters (b12 j01)
        work = design_views(folder, root, "work") or work
        if design_block:
            overview = context_frame.report_views(folder, root)
            work = overview
    if theme.name == "insight" and level in ("Block", "Task") and not draft:   # HOOK: insight Board and Task Work (s52, s58)
        work = insight_views_for(folder, root, "work") or work
    if theme.name == "insight" and level == "Job" and not draft:   # HOOK: an insight Job's Work, by letter (b11 s55)
        work = insight_job_work(folder, root) or work
    if retired and work is not overview:                 # Work retired: each Report view draws what its Work view did,
        overview = {k: (name, (work.get("work-" + k) or work.get(k) or (name, body))[1])   # its steps then its results
                    for k, (name, body) in overview.items()}

    if draft_frame:
        # One content surface: only the steps (JL 261113: "we dont need these views either": Text, Runs, MindMap,
        # Plan + Results); old Report views and all working steps stay reachable.
        overview = {k: v for k, v in work.items() if k != 'runs'}
        work = overview
    ctx.overview, ctx.work = overview, work


def rail_sections(ctx: PageContext) -> None:
    """Delivery, Related, Interactions and Know, then the right rail's sections in order."""
    root, folder, draft, level, overview, topics, events = (ctx.root, ctx.folder, ctx.draft, ctx.level, ctx.overview,
                                                            ctx.topics, ctx.events)
    live_work, project_report, retired, paper, shared_frame = (ctx.live_work, ctx.project_report, ctx.retired,
                                                               ctx.paper, ctx.shared_frame)
    paper_board, design_block, draft_frame, version_frame, WF = (ctx.paper_board, ctx.design_block, ctx.draft_frame,
                                                                 ctx.version_frame, ctx.WF)
    paper_out = "" if draft else paper_delivery(folder, root)   # HOOK: a paper version's or Board's whole paper
    delivery = draft["delivery"] if draft else (paper_out if paper_out and level == "Block" else paper_out + delivery_html(folder, root))
    dviews = draft.get("delivery_views", {}) if draft else paper_delivery_views(folder, root)   # HOOK: previews by lane
    look = draft or (paper_look() if dviews or (paper_out and level == "Block") else {})   # HOOK: a draft's or paper's look
    if dviews and not delivery:
        delivery = "previews"
    related = related_html(folder, root)
    # Interactions: the person's inbox, every interaction at this page or below (JL 261031): one record each, the
    # same one its Work row, its map node and its Studio card open
    every = focus_interactions.interactions(folder, root) if page_level(folder) not in ("SPACE", "Folder") else []
    # what to know has its own section, Know, apart from what asks (JL 261108: "yes, we should do that"): Interactions
    # keeps the questions and decisions; Know the notes at this page, below it and above it up to its Project
    inbox = [r for r in every if r["state"] != "to know"]
    knows = known(folder, root, every) if page_level(folder) not in ("SPACE", "Folder") else []
    # the standard Interaction, left tabs and one question on the right (JL 261104: "make this to be the standard items for
    # any of them"; "the workbecnh UI code"), or what the filter found nothing of
    empty = {"waiting": "Nothing needs your input.", "answered": "Nothing answered yet."}
    asked = {key: (name, standard_interactions([r for r in inbox if key == "all" or r["state"] == key], folder, root)
                   or '<p class="mut">' + empty.get(key, "Nothing asked yet.") + '</p>')   # the views' own words
             for key, name in (("all", "All"), ("waiting", "Needs your input"), ("answered", "Answered"))}   # opens on All
    rail = []                                            # (key, label, group): the right rail, in this order
    if overview:
        rail.append(("report", "Report", ""))
    if not (live_work or project_report or retired or level in ("SPACE", "Folder") or (paper and level in ("Job", "Task"))):   # Work retired (261111)
        rail.append(("work", "Work", ""))
    if topics or draft or page_level(folder) in ("Block", "Job", "Task"):   # HOOK: a draft Task always has its Studio;
        rail.append(("studio", "Studio", ""))          # every level has its own, "none yet" with Add a topic when empty
        #                                                (b11 form, JL 261106: "Every level, each its own topics"); its
        #                                                groups are its views, under the title (JL 261029)
    if page_level(folder) not in ("SPACE", "Folder"):    # always on the rail, empty or not (JL 261031: "in the right rail,
        rail.append(("interactions", "Interactions", ""))  # we should have a section named the Interaction, to show all
                                                         # the interaction under this page")
    if knows:                                            # what to keep in mind here; a section with nothing does not show
        rail.append(("know", "Know", ""))
    if not live_work and (delivery or page_level(folder) not in ("SPACE", "Folder")):   # work Delivery is a view now
        rail.append(("delivery", "Delivery", ""))                     # also missed the delivery here")
    if related:
        rail.append(("related", "Related", ""))
    if events or live_work:                              # keep the page-wide history address available
        rail.append(("timeline", "Timeline", ""))
    if page_level(folder) not in ("SPACE", "Folder"):   # the skills that work on it, most relevant first (JL 261105: "a
        rail.append(("skills", "Skills", ""))           # new tab in the right rail, named 'SKILL'")
    rail.append(("files", "Files", ""))                 # the folder itself: a place to go, on the rail (JL 261029)

    if shared_frame:
        rail = [('report', 'Report', '')] + [(key, title, '') for key, title in WF.SHARED]
        if paper_board or design_block or draft_frame or version_frame:
            rail.append(('delivery', 'Delivery', ''))
        if related:
            rail.append(('related', 'Related', ''))
    (ctx.delivery, ctx.dviews, ctx.look, ctx.related, ctx.every, ctx.inbox, ctx.knows, ctx.asked,
     ctx.rail) = delivery, dviews, look, related, every, inbox, knows, asked, rail


def section_body(ctx: PageContext) -> None:
    """The open section: its view, its body, its heading and its views bar."""
    theme, root, folder, section, group, level = ctx.theme, ctx.root, ctx.folder, ctx.section, ctx.group, ctx.level
    draft, paper, own_first, look, shared_frame = ctx.draft, ctx.paper, ctx.own_first, ctx.look, ctx.shared_frame
    project_report, overview, work, asked, knows = ctx.project_report, ctx.overview, ctx.work, ctx.asked, ctx.knows
    dviews, rail, topics, every, inbox, events = ctx.dviews, ctx.rail, ctx.topics, ctx.every, ctx.inbox, ctx.events
    delivery, related, WF, context_frame = ctx.delivery, ctx.related, ctx.WF, ctx.context_frame
    live_work, paper_board, retired = ctx.live_work, ctx.paper_board, ctx.retired
    view = None                                      # a shared section has no view of its own
    opens = "report" if shared_frame or project_report or level in ("SPACE", "Folder") or (overview and level == "Block") else "work"
    keys = [k for k, _, _ in rail]
    if opens not in keys:          # a paper Job or Task has no Work since 261111: open on Report, else the first section
        opens = "report" if "report" in keys else keys[0]   # (it crashed every version page, JL 261112)
    section = section if section in keys else opens
    groups = list(dict.fromkeys(t_ for _, _, f in topics for t_ in f["tags"]))   # no "All": one button per group
    if groups and any(not f["tags"] for _, _, f in topics):                     # (JL 261029); the ungrouped go last
        groups.append(OTHER)
    studio_views = {tag: (tag, None) for tag in groups}
    told = {"know": ("Know", lambda: standard_interactions(knows, folder, root, title="📌 What you should know"))}   # one view, its name the section's
    views = {"report": overview, "work": work, "interactions": asked, "know": told, "delivery": dviews}.get(section, {})
    if shared_frame and section in dict(WF.SHARED):
        selected = next(r for r in rail if r[0] == section)
        label = dict(WF.SHARED)[section]
        rail_items = [r for r in every if r['state'] == group] if section == 'interactions' and group in ('waiting', 'answered') else every
        body, _ = context_frame.shared_bodies(folder, root, theme.name, level, None, topics, inbox, knows, events, rail_items, only=section)[section]
        if section == 'studio' and group:
            filtered = [row for row in topics if in_group(row[2], group)]
            body = studio_html(filtered, root, '', card_interactions(folder, root), tabs=True) if filtered else studio_none(folder, root)
        body = WF.STYLE + side_css() + body + PB_JS
        head = label
        bar = (f'<nav class="section-views" aria-label="Views"><a href="{frame.esc(page_url(folder, root, section))}"'
               + ('' if section == 'studio' and group else ' aria-current="page"') + '>All</a>'
               + (f'<a href="{frame.esc(page_url(folder, root, section, group))}" aria-current="page">{frame.esc(group)}</a>' if section == 'studio' and group else '') + '</nav>')
        if section == 'interactions':
            bar = '<nav class="section-views" aria-label="Views">' + ''.join(
                f'<a href="{frame.esc(page_url(folder, root, section, key))}"'
                + (' aria-current="page"' if key == (group or 'all') else '') + f'>{name}</a>'
                for key, name in (('all', 'All'), ('waiting', 'Needs your input'), ('answered', 'Answered'))) + '</nav>'
    elif section in views or section in ("report", "work", "interactions", "know") or (section == "delivery" and dviews):
        view = group if group in views else draft["open"] if section == "work" and draft \
            else draft["open"] if section == "report" and draft \
            else next(iter(views)) if (paper and level in ("Block", "Job")) or (theme.name == "insight" and level in ("Block", "Job", "Task")) or own_first \
            else next((k for k in (("standing", "findings", "overview", "mindmap") if section == "work" else ("overview", "mindmap", "findings", "standing"))
                       if k in views), next(iter(views)))   # HOOK: a paper Board opens on its first part
        selected = next(r for r in rail if r[0] == section)
        label, body = views[view]
        body = body() if callable(body) else body           # MindMap, Blocks, Status: built only when opened
        caption = (look.get("captions") or {}).get(view) or ("" if theme.name == "insight" and level in ("Block", "Job", "Task")
                                                             and view != "mindmap" else VIEW_WORDS.get(view, ""))   # its letters carry their own
        if theme.name in WORK_SHAPE and level in ("Block", "Job") and view == "findings":
            caption = "What it has found so far, and what it hands over."
        if view == "standing" and caption and level in ("Job", "Task"):   # its own level's words (261105)
            caption = {"Job": "Where its Tasks stand, each with its newest result.",
                       "Task": "What its newest Run returned, and where its Runs stand."}[level]
        if level in ("Block", "Job", "Task"):            # a theme's own words for a view at a level (CAPTIONS, 261108)
            _mod, _prefix = page_module(theme.name, folder, root)
            caption = (getattr(_mod, _prefix + "CAPTIONS", {}) if _mod is not None else {}).get((level, view.removeprefix("work-")), caption)
            _cap = getattr(_mod, _prefix + "caption", None) if _mod is not None else None   # a page's own words (j00 people)
            try:
                caption = (_cap(folder, level, view.removeprefix("work-")) if _cap else None) or caption
            except Exception:
                pass
        if (paper and level in ("Job", "Task") and not draft) or retired or level in ("SPACE", "Folder", "Project", "Theme"):   # the view's name says it (JL 261111; AGENTS: no secondary
            caption = ""                                         # labels): no grey line under the paper views' buttons
        body = (f'<p class="view-caption">{frame.esc(caption)}</p>' if caption else "") + body
        if shared_frame:
            if paper_board or live_work or view != 'standing':   # no grey caption under the views (JL 261111)
                body = re.sub(r'^<p class="view-caption">.*?</p>', '', body, flags=re.S)
            body = WF.STYLE + side_css() + body + PB_JS
        words = draft.get("words", {}) if draft and section in ('work', 'report') else {}
        bar = ('<nav class="section-views" aria-label="Views">' + "".join(
            f'<a href="{frame.esc(page_url(folder, root, section, key))}"' + (' aria-current="page"' if key == view else '')
            + f'>{frame.esc(name)}' + (f'<span class="vw {words[key][1]}">{frame.esc(words[key][0])}</span>' if key in words else '')
            + '</a>' for key, (name, _) in views.items()) + '</nav>')   # one view too: the bar is always there
        head = section.title()
    else:
        selected = next(r for r in rail if r[0] == section)
        selected = (selected[0], selected[1], (group if group in studio_views else next(iter(studio_views), ""))
                    if section == "studio" else "")
        # the Studio's topic groups are its views: the bar above the Purpose, as every section's (JL 261031, b10 r01
        # Q1: "if it is the view based, we will put it above the Purpose"; it was under the Purpose before)
        groups_nav = ('<nav class="section-views studio-groups" aria-label="Views">' + "".join(
            f'<a href="{frame.esc(page_url(folder, root, "studio", key))}"' + (' aria-current="page"' if key == selected[2] else '')
            + f'>{frame.esc(name)}</a>' for key, (name, _) in studio_views.items()) + '</nav>') \
            if section == "studio" and studio_views else ""
        # a section with one view keeps its bar too, one button naming it, so the Purpose never moves (JL 261031)
        one = {"studio": "Topics", "delivery": "Deliveries", "related": "Related", "files": "Folder",
               "timeline": "Timeline", "skills": "Skills"}[section]
        bar = groups_nav or (f'<nav class="section-views" aria-label="Views"><a href="{frame.esc(page_url(folder, root, section))}"'
                             f' aria-current="page">{one}</a></nav>')
        body = {"studio": lambda: (draft["studio_top"]() if draft else "") + (studio_html(topics, root, selected[2], card_interactions(folder, root))
                                                                            if topics else studio_none(folder, root)), "delivery": lambda: (delivery() if callable(delivery) else delivery) or '<p class="mut">Nothing handed over yet: a delivery lands in this folder\'s <code>delivery/</code> once it is agreed.</p>',
                "related": lambda: related, "files": lambda: folder_html(folder, root),
                "skills": lambda: page_skills(folder, root, theme.name, level, bool(draft), bool(topics), bool(inbox), paper),
                "timeline": lambda: (branches_html(folder, root) if level == "Project"   # a Project: one line per Block
                                     else timeline_html(events, folder, root))}[section]()
        head = section.title()
    ctx.section, ctx.view, ctx.views, ctx.selected, ctx.body, ctx.head, ctx.bar = section, view, views, selected, body, head, bar


def around_work(ctx: PageContext) -> None:
    """Report and Work on a shared frame end with 🧭 Around the Work; other themes add their own items."""
    from live import project_page as PP
    theme, root, folder, section, level, body = ctx.theme, ctx.root, ctx.folder, ctx.section, ctx.level, ctx.body
    view, views, questions, topics, inbox, knows = ctx.view, ctx.views, ctx.questions, ctx.topics, ctx.inbox, ctx.knows
    events, every, shared_frame, insight_block = ctx.events, ctx.every, ctx.shared_frame, ctx.insight_block
    live_work, draft_frame, version_frame, context_frame = (ctx.live_work, ctx.draft_frame, ctx.version_frame,
                                                            ctx.context_frame)
    if section in ("report", "work") and shared_frame:
        # Existing view ownership remains the fallback; explicit view metadata can target Delivery.
        own = view_items(theme.name, folder, root, level, 'mindmap' if view == 'overview' else view,
                         ['mindmap' if k == 'overview' else k for k in views], inbox, questions)
        shared = context_frame.shared(folder, root, theme.name, level, view, topics, own, knows, events, every)
        if (draft_frame or version_frame) and '<h2>📋 Review Content</h2>' not in body:
            body = '<h2>📋 Review Content</h2>' + body
        if insight_block:                                       # its views' own sections under the Work band (JL 261109)
            body = BAND_CSS + '<h3 class=wk-band>📋 Review Content</h3>' + body
        if live_work and theme.name == "work" and level in ("Block", "Job") and view == "standing":
            body += PP.findings_band(folder, root)                 # 🔎 Findings under Review Content, as the Project's
        body = ('<section class="work-section-group" aria-label="Report content">'
                + body + '</section>' + ('<section class="work-section-group" aria-labelledby="work-shared"><h2 id="work-shared">'
                                         '🧭 Around the Work</h2>' + shared + '</section>' if shared else ''))   # no heading over nothing
    elif section in ("report", "work") and page_level(folder) in IX.LEVELS:   # other themes retain their own layout
        own = view_items(theme.name, folder, root, level, view, list(views), inbox, questions)   # its own items (261106)
        body += IX.view_section(own, root, IX.next_number(body), lambda r: interaction_where(r, folder, root))
    ctx.body = body


BELOW_NAMES = {"SPACE": "Projects", "Folder": "Projects", "Project": "Blocks", "Theme": "Blocks", "Block": "Jobs",
               "Job": "Tasks", "Task": "Runs"}


def rail_words(ctx: PageContext, key: str, tag: str = "") -> str:
    """What is in a section, in a few words, under its name on the rail; never a count (JL 261031: "Don't add N
    topics, N jobs, they are useless, they will change along the way")."""
    if key == "work":                            # Work holds the Report's own views, with how each is made, when it
        mirror = {k.removeprefix("work-") for k in ctx.work} & set(ctx.overview)   # does (round 3: the rail still said "its Jobs")
        if ctx.overview and len(mirror) * 2 >= len(ctx.overview):
            return "the same views, and what to do on each"
        return f"its {BELOW_NAMES.get(ctx.level, 'items')}"
    if key == "studio":
        return "" if tag else "drawings, mind maps, slides"
    if key == "interactions":
        return ("🙋 waits on you" if any(r["state"] == "waiting" for r in ctx.inbox)
                else "nothing waits on you" if ctx.inbox else "nothing asked yet")
    if key == "delivery" and not ctx.delivery:
        return "nothing handed over yet"
    if key == "know":
        return "what to keep in mind"
    return {"report": "read the results and check the progress", "delivery": "what it has handed over",
            "related": "what came in: meetings, papers, emails", "timeline": "what happened when",
            "files": "the folder itself", "skills": "the skills that work on it"}.get(key, "")


def rail_view(ctx: PageContext, key: str, tag: str = "") -> str:
    """Report and Work share one view list: moving between them stays in the view (JL 261104: "When I switch from
    Report to Work, could I still stay in the same view"), on every page whose Work has the Report's views (a paper
    Board's `work-<view>`, a work, insight or design page's `<view>`; 261106)."""
    if ctx.level in ("Block", "Job", "Task") and key in ("report", "work") and ctx.section in ("report", "work") and ctx.group:
        base = ctx.group.removeprefix("work-").removeprefix("report-")
        there = ctx.work if key == "work" else ctx.overview
        return next((t for t in (("work-" + base, base) if key == "work" else (base, "report-" + base)) if t in there), tag)
    return tag


def left_rail(root: Path, folder: Path):
    """The left rail: the page's siblings, with its children (and a Theme's or a folder's grandchildren) under it."""
    if page_level(folder) in ("Job", "Task"):          # a Job's or a Task's siblings include its level's sNN
        siblings = rail_kids(folder.parent, root)
    else:
        siblings = sorted(q for q in folder.parent.iterdir() if q.is_dir() and not q.name.startswith((".", "_"))
                          and inside(q, root) and page_level(q) == page_level(folder)) if folder != root else [folder]
    left = []
    for sibling in siblings:                             # siblings, with the open page's children under it
        left.append(rail_link(rail_url(sibling, root), sibling.name, sibling == folder))
        if sibling == folder:                            # its children, and under a Theme or a folder of Projects
            for child in rail_kids(folder, root):        # their own children too (JL 261029: "show the blocks")
                if not inside(child, root):
                    continue
                left.append(rail_link(rail_url(child, root), child.name, False, "child"))
                if page_level(child) in ("Theme", "Folder"):
                    left += [rail_link(page_url(g, root), g.name, False, "child grand") for g in kids(child) if inside(g, root)]
    return left


def crumbs_goal_source(root: Path, folder: Path, data: dict, draft: dict):
    """The path on top, the goal line and the source Markdown link."""
    crumbs, cur = ([frame._link("/", root.name)] if folder != root else []), root   # the path starts at the SPACE (rule 1)
    for part in folder.relative_to(root).parts[:-1]:
        cur /= part
        crumbs.append(frame._link(page_url(cur, root), part))
    if folder != root:                                   # the path ends where you are (JL 261029)
        crumbs.append(f'<span aria-current="page">{frame.esc(folder.name)}</span>')
    goal = data["goal"].split("\n")[0] if data["goal"] else draft.get("aim", "")
    try:                                    # a theme may spell a goal id in words (design: G01 → its aim; look rule 5)
        from live import design_focus as _DF
        goal = _DF.goal_line(folder, goal) or goal
    except Exception:  # noqa: BLE001 -- a theme's words never break the base page
        pass
    source = frame.pop(frame.reader(data["face"], root), "Source Markdown", "Open this page's Markdown") if data["face"] and inside(data["face"], root) else ""
    goal_html = (f'<div class="focus-goal"><span class="goal-word">{GOAL_WORD.get(page_level(folder), "Goal")}</span>'
                 f'{markdown(goal, folder, root)}</div>' if goal else '')
    return crumbs, goal_html, source


def page_document(ctx: PageContext) -> str:
    """The finished page: the open section's body in the shared shell, with both rails, the path and the goal."""
    root, folder, body = ctx.root, ctx.folder, ctx.body
    sub_line = "" if ctx.shared_frame else rail_words(ctx, ctx.section, ctx.selected[2])
    if ctx.look:                                         # HOOK: a draft or paper page's own look (width, sections), every
        body = ctx.look["css"] + body                    # section; no verb beside its name (JL 261031, b10 r01 Q2)
    left = left_rail(root, folder)
    right = "".join(rail_link(page_url(folder, root, key, rail_view(ctx, key, tag)), name, (key, name, tag) == ctx.selected,
                              "", "" if ctx.shared_frame else rail_words(ctx, key, tag)) for key, name, tag in ctx.rail)
    crumbs, goal_html, source = crumbs_goal_source(root, folder, ctx.data, ctx.draft)
    return page_shell(folder, root, crumbs, frame.esc(folder.name), ctx.head, sub_line, ctx.bar, goal_html, body, source,
                      left, right, [(key, name, rail_view(ctx, key)) for key, name, tag in ctx.rail if not tag], ctx.section,
                      identity=page_identity_html(ctx.theme.name, folder, root, ctx.data))
