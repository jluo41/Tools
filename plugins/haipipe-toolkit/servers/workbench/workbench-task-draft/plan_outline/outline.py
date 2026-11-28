"""📃 Page · the page re-read per division, live and storage-less (QPf12).

WHAT THIS ANSWERS (JL 260816): a page groups its material by section kind —
all Content, then all Aims, then all States — so nothing shows one division
with ITS aims, ITS ticks, and ITS state receipts together. This surface flips
the axis: one card per Content division, everything that belongs to it inside.

RULE-BASED, NEVER AUTHORED (JL 260816: "我不想每一次都靠一个 code 去做这件事"):
the aim-to-division tie is read from the material, two grammars deep —
  ① the template's own A-grammar: an Aims/States group `### A<n>` and an id
    `A<n>.<m>` both carry the division number already; nothing to add.
  ② the §N anchor (QPf12 §1): a loose checkbox aim, a state line, or a Files
    row may carry `§N` pointing at Content's `### N ·` division. Files rows
    may carry several. An unanchored line is legal and means 🌐 page-wide.
No claude call at render time. A bad anchor renders as a named ❌, and the
🌐 card doubles as the worklist for anchoring the page.

LIVE AND STORAGE-LESS for reads, the QPf1 folderstat precedent: rendered from
the .md on every open, so it can never be stale. The POST twin keeps the
shell's `tab: {url, write}` contract, but the four-space reader is deliberately
read-only; Markdown, Result, and delivery writers live in their owning workflows.

TWO LENSES, one parse (QPf12 §2): 🧭 By division and 🚦 By progress are the
same data sorted twice, both rendered server-side, toggled client-side by
chips with no second request. The 🚦 lens lists ⬜ before ✅ on purpose:
opening it is asking what the page still owes.
"""
from src.common import delivery_dir, delivery_read_lane_dir, delivery_relative  # noqa: F401  (kept importable)
import html
import re
import textwrap  # noqa: F401  (kept importable)
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

from src.outline_version import plan_dir, latest_outline, version_tag  # noqa: F401
from src.item_table import (  # noqa: F401  (kept importable)
    ITEM_TYPES,
    LADDER as ITEM_LADDER,
    bullets as typed_bullets,
    cycle_now as item_cycle,
    evidence_none_targets,
    item_status,
    read_items,
    repo_root,
    wall_label,
)
from src.plan_shape import canonical_plan, iter_plan_bullets, presentation_point  # noqa: F401
from src.plan_layout import is_sectioned, to_canonical  # noqa: F401
from live.outline_preview import (draft_path, read_drafts, bullet_token, record_token,  # noqa: F401  (kept importable)
                                  reader_prose, read_opening_draft)
from live.outline_scratch import (read_scratch, save_scratch,  # noqa: F401  (kept importable)
                                  scratch_assets_html, scratch_control_html,
                                  scratch_flag_html, scratch_heading_attr)
from src.evidence_labels import collect_result_labels, resolve_inline_labels  # noqa: F401
from live.space_views import (SPACE_CSS, SPACE_JS, delivery_space_html,
                              draft_reads_html, evidence_space_html, run_tabs)
from live.outline_structure import (structure_card_html, save_structure,
                                    STRUCTURE_CSS, STRUCTURE_JS)
from live.outline_revise import (save_revise, revise_rows_html, add_paragraph,  # noqa: F401  (kept importable)
                                 sentence_id as revise_sentence_id,
                                 assets_html as revise_assets_html)

from live.outline_parse import (  # noqa: F401  (moved; names kept importable here)
    DONE, STATE_EMOJI, _SEC_ALIAS, _DIV_RE, _GROUP_RE, _ID_RE, _ANCHOR_RE, _XREF_TAIL, _LEAD_STRIP,
    _TRAIL_ANCHORS, _CAPTION_RE, _is_job_line, _brief, _ID_LEAD, _strip_id, _strip_anchors, _anchors,
    _CHECK_RE, _sections, parse_outline)
from live.outline_plan_html import (  # noqa: F401  (moved; names kept importable here)
    _e, _scratch_run_meta, _opening_preview_card, _outline_cycle_strip, _typed_item_chip,
    _PREVIEW_EVIDENCE_RE, _resolved_evidence_html, _preview_token_html, _preview_reader_html,
    _bundle_row_html)
from live.outline_plan_read import (  # noqa: F401  (moved; names kept importable here)
    _MARK, _latest_plan, _PLAN_VERSION_RE, _next_shape_version, _typed_item_review,
    _paragraph_display, _source_realizations, _join_wrapped)
from live.outline_division_cards import _aim_row, _card, _tally  # noqa: F401  (moved)
from live.outline_page_parts import (  # noqa: F401  (moved; names kept importable here)
    _BOARD_LEVEL_ROUTES, _board_line, page_roadmap_html, _no_plan_html, _page_band,
    board_level_link)
from live.outline_plan_card import plan_card  # noqa: F401  (moved; names kept importable here)


from live.outline_page import (  # noqa: F401  (moved; names kept importable here)
    _PAGE)

from live.outline_plan_edit import (  # noqa: F401  (moved; names kept importable here)
    _replace_header, _working_plan_text, _plan_region, _bullet_line, _normalise_head,
    _edit_plan_bullet)

from live.outline_state import (  # noqa: F401  (moved; names kept importable here)
    _disk_state, LEGACY_STATE, LANDED, READ, STUCK, _pstate, _short_authors, _tex_dash,
    _asset_url, _aim_rows, _live, _count_landed, _count_accepted, _bundle_state)


def _structure_map(page_src, root=None, path_q="", file_q="", read_only=False):
    """The Structure card at the top of Draft Space: the Outline headings as text.

    JL 260922: "we don't use the mermaid, just use the text to show the
    structure" and "我可以点进去 edit，有点像 Scratch 一样". One `run-structure`
    copy button sits above it; the card is plain text read from the selected
    Outline on every open, and (unless the host is read-only) clicking it opens
    a box whose Save rewrites the headings through `action: structure`.
    """
    if page_src is None:
        return ""
    # No copy-prompt chip above the card: the Runs panel holds every prompt (JL 260927).
    card = structure_card_html(page_src, read_only=read_only, path_q=path_q, file_q=file_q)
    return card + ("" if read_only or not card else STRUCTURE_JS)




def render(title, o, page_src=None, root=None, path_q="", file_q="", read_only=False,
           draft_mode="table", asset_base=None):
    """-> the full html page: both lenses rendered, chips toggle."""
    if draft_mode not in {"table", "reading", "scratch", "roadmap", "revise"}:
        draft_mode = "table"
    table_on = " on" if draft_mode == "table" else ""
    reading_on = " on" if draft_mode == "reading" else ""
    scratch_on = " on" if draft_mode == "scratch" else ""
    revise_on = " on" if draft_mode == "revise" else ""
    roadmap_on = " on" if draft_mode == "roadmap" else ""
    # Say it in words a tired reader can take in the first time (JL 260816).
    # "3 loose lines" and "aligned" are this workbench's own shorthand, and a
    # reader meeting the tab for the first time has no reason to know either.
    if o["bad"]:
        chip = '<span class=warn>❌ %s</span>' % " · ".join(
            _e(b.replace(": no such division", " points at a part that "
                         "does not exist")) for b in sorted(set(o["bad"])))
    elif o["loose"]:
        chip = ('<span class=warn>⚠️ %d line%s not placed in any part</span>'
                % (o["loose"], "s"[:o["loose"] != 1]))
    else:
        chip = '<span class=ok>✅ every line is placed</span>'

    # The pending asks used to get a card of their own here, above everything.
    # It was cut (JL 260816: "我们大概不需要吧"): the header line already says
    # `🗣 1 waiting on you`, so the card repeated a number the reader had just
    # read and spent four lines explaining what "waiting" means.
    cards = []
    for d in o["divs"]:
        n = d["n"]
        name = _e(d["title"]) if d["title"] else (
            '<span class=mut>not declared in Content</span>'
            if d.get("undeclared") else '<span class=mut>&mdash;</span>')
        cards.append(_card(
            n, "%d · %s" % (n, name),
            [a for a in o["aims"] if a["div"] == n],
            [s for s in o["states"] if s["div"] == n],
            [f for f in o["files"] if n in f["divs"]],
            brief=d.get("brief")))
    cards.append(_card(
        "P", "🌐 the whole page",
        [a for a in o["aims"] if a["div"] is None],
        [s for s in o["states"] if s["div"] is None],
        [f for f in o["files"] if not f["divs"]]))
    # TWO HALVES, and they are not the same thing (JL 260817 asked what the
    # second one was for). The PLAN is what we said we would write; the PAGE
    # is what is written now. Reading them unlabelled beside each other, with
    # two different section lists, is what made the tab confusing.
    plan = (plan_card(page_src, root, path_q, file_q, read_only=read_only,
                      minimal=True)
            if page_src is not None else "")
    structure = _structure_map(page_src, root, path_q, file_q, read_only=read_only)
    by_div = plan or (_no_plan_html(page_src) if page_src is not None else "")

    todo = [a for a in o["aims"] if not a["done"]]
    done = [a for a in o["aims"] if a["done"]]
    prog = ['<div class=card><h2>⬜ still to do · %d</h2>' % len(todo)]
    prog += [_aim_row(a, badge=True) for a in todo] or [
        '<div class=mut>nothing left to do</div>']
    prog.append('</div><div class=card><h2>✅ already done · %d</h2>' % len(done))
    prog += [_aim_row(a, badge=True) for a in done] or [
        '<div class=mut>nothing done yet</div>']
    prog.append("</div>")

    lead = ('<div class=lead>%s</div>' % _e(o.get("lead", ""))
            if o.get("lead") else "")
    evidence_url = ""
    run_url = ""
    delivery_url = ""
    if page_src is not None:
        encoded = (quote(path_q or ""), quote(file_q or page_src.name))
        evidence_url = "/_board/evidence?path=%s&file=%s&embed=1" % encoded
        run_url = "/_board/runs?path=%s&file=%s&embed=1" % encoded
        delivery_url = "/_board/delivery?path=%s&file=%s&workspace=1" % encoded
    document = _PAGE.format(title=_e(title), lead=lead, tally=_tally(o),
                        page_stem=_e(page_src.stem if page_src is not None else "standalone"),
                        board_link=_board_line(board_level_link(page_src, root), page_src, root),
                        band=_page_band(page_src),
                        chip=chip, by_div=by_div, by_prog="".join(prog),
                        structure=structure,
                        draft_mode=draft_mode,
                        table_on=table_on,
                        reading_on=reading_on,
                        scratch_on=scratch_on,
                        revise_on=revise_on,
                        roadmap_on=roadmap_on,
                        roadmap=page_roadmap_html(page_src, root),
                        structure_css=STRUCTURE_CSS,
                        evidence_url=html.escape(evidence_url, quote=True),
                        run_url=html.escape(run_url, quote=True),
                        delivery_url=html.escape(delivery_url, quote=True),
                        **_runs_parts(page_src, evidence_url=evidence_url,
                                      delivery_url=delivery_url, path_q=path_q,
                                      file_q=file_q, asset_base=asset_base))
    if page_src is None or not path_q:
        return document
    from live.workbench_guide import mount_guide
    return mount_guide(document, "page", {"path": path_q, "file": file_q}, ".spaces", ".lens")


def _runs_parts(page_src, *, evidence_url="", delivery_url="", path_q="", file_q="",
                asset_base=None):
    """The three Spaces' own parts and one Runs panel per Space (Page 0.118)."""
    blank = {"runs_draft": "", "runs_evidence": "", "runs_delivery": "",
             "runs_css": "", "runs_js": "", "space_css": "", "space_js": "",
             "draft_reads": "", "evidence_space": "", "delivery_space": ""}
    if page_src is None:
        return blank
    from live.runs import local_runs
    from live.runs_panel import PANEL_CSS, PANEL_JS, panel_html, run_types
    try:
        rows = local_runs(page_src)
    except Exception:  # a broken ticket must not blank the Draft Space
        rows = []
    types = run_types()
    try:
        from live.runs import supporting_task_runs
        supporting = supporting_task_runs(page_src)
    except Exception:  # an unreadable registry must not blank the Evidence Space
        supporting = []
    plan = latest_outline(plan_dir(page_src.parent), page_src.stem)
    plan_name = ("%s/%s" % (plan.parent.name, plan.name)) if plan else "no plan yet"
    return {
        # each Runs panel starts as the folded strip, as on every workbench (JL 261003)
        "runs_draft": panel_html(page_src, "draft", rows, types, plan_name=plan_name, folded=True),
        "runs_evidence": panel_html(page_src, "evidence", rows, types, plan_name=plan_name,
                                    run_tabs=run_tabs(page_src), supporting=supporting, folded=True),
        "runs_delivery": panel_html(page_src, "delivery", rows, types, plan_name=plan_name, folded=True),
        "runs_css": PANEL_CSS,
        "runs_js": PANEL_JS,
        "space_css": SPACE_CSS,
        "space_js": SPACE_JS,
        # which file and `##` section each view reads: the View row's tooltip, not a line
        # on screen (JL 261003: the Draft Space laid out as Guide's View row)
        "draft_reads": html.escape(re.sub(r"<[^>]+>", "", draft_reads_html(page_src)), quote=True),
        "evidence_space": evidence_space_html(page_src, card_url=evidence_url, supporting=supporting),
        "delivery_space": delivery_space_html(page_src, checks_url=delivery_url, path_q=path_q,
                                              file_q=file_q, asset_base=asset_base),
    }


# `embed=1`: one view of the Page inside a frame Space (task_draft.py draft_task_spaces,
# b03 261007). The Page draws as always; this hides its own header, Space row, Draft mode row, tab row
# and Runs panels (the frame has its own), then opens the asked Space (`space`: bullet · evidence ·
# delivery) and tab (`tab`: citations · displays · values · supporting · latex · word …) through the
# Page's own controls, so every script of the Page works as it does there.
EMBED_HTML = """<style>
html.wb-embed body>header,html.wb-embed .spaces,html.wb-embed .wb-band,html.wb-embed body>h1,
html.wb-embed .wb-links,html.wb-embed .draft-mode-switcher,html.wb-embed .space-split>.runs-panel,
html.wb-embed .space-tabs{display:none!important}
html.wb-embed body{padding:0 4px}html.wb-embed .space-split>.space-main{border:0;padding:0}
</style><script>(function(){document.documentElement.classList.add('wb-embed');
function go(){var q=new URLSearchParams(location.search),sp=q.get('space'),tab=q.get('tab');
 if(sp){var b=document.querySelector('.spaces .space[data-space="'+sp+'"]');if(b&&!b.classList.contains('on'))b.click();}
 if(tab){var t=document.querySelector('.lens.show .space-tab[data-tab="'+tab+'"]');if(t)t.click();}}
if(document.readyState==='loading')addEventListener('DOMContentLoaded',go);else go();})();</script>"""


class OutlineMixin:

    # ---- GET/HEAD /_board/draft?path=…&file=… ------------------------
    def outline_view(self, head_only=False):
        q = parse_qs(urlparse(self.path).query)
        p = {"path": (q.get("path") or [""])[0],
             "file": (q.get("file") or [""])[0]}
        got = self.target(p)
        if got[0] is None:
            body = ("<h1>🧭 outline</h1><p>%s</p>" % html.escape(got[1])
                    ).encode()
            return self._outline_send(body, 404, head_only)
        f, board = got
        page_src = Path(board) / f
        o = parse_outline(page_src.read_text(encoding="utf-8"))
        # workbench-task-draft 0.16.0: the Aims live in the PLAN and the page
        # keeps no copy, so a migrated page parsed alone reads "lists no aims
        # yet" while its plan holds them (JL 260830, SM08). Page first, plan
        # second, the same order check.py's page_aims_text uses.
        if not o.get("aims"):
            plan, _v = _latest_plan(page_src)
            if plan is not None:
                po = parse_outline(plan.read_text(encoding="utf-8", errors="replace"))
                if po.get("aims"):
                    o["aims"] = po["aims"]
        draft_mode = (q.get("view") or ["table"])[0]
        if draft_mode not in {"table", "reading", "scratch", "roadmap", "revise"}:
            draft_mode = "table"
        page = render(page_src.stem, o, page_src, self.root, p["path"], p["file"],
                      read_only=getattr(self.server, "read_only", False),
                      draft_mode=draft_mode,
                      asset_base=getattr(self, "delivery_asset_base", None))
        if (q.get("embed") or [""])[0] == "1":
            page = page.replace("</body>", EMBED_HTML + "</body>", 1)
        return self._outline_send(page.encode("utf-8"), 200, head_only)

    def _outline_send(self, body, code, head_only):
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    # ---- POST /_board/draft — the shell's write() twin ---------------
    def plug_outline(self, p):
        """Register the live tab; Scratch, Revise and Structure are its Draft writes.

        The normal workbench write remains a no-op URL registration for the shell.
        `action: scratch` writes the human Scratch registry into the selected
        Outline Markdown and creates its paired Page Run. `action: revise` saves
        the person's direct edits to one paragraph's Draft sentences and extends
        that paragraph's Revise Run with a change ledger Step. Feedback remains
        a historical Run-space record; Draft has no comment composer.
        """
        got = self.target(p)
        if got[0] is None:
            return None, got[1]
        action = p.get("action")
        if action == "scratch":
            f, board = got
            read_only = getattr(getattr(self, "server", None), "read_only", False)
            return save_scratch(Path(board) / f, p, read_only=read_only)
        if action == "structure":
            f, board = got
            read_only = getattr(getattr(self, "server", None), "read_only", False)
            return save_structure(Path(board) / f, p, read_only=read_only)
        if action == "revise":
            f, board = got
            read_only = getattr(getattr(self, "server", None), "read_only", False)
            return save_revise(Path(board) / f, p, read_only=read_only)
        if action == "add-paragraph":
            f, board = got
            read_only = getattr(getattr(self, "server", None), "read_only", False)
            return add_paragraph(Path(board) / f, p, read_only=read_only)
        if action == "feedback":
            return None, "Draft comments are removed; use Scratch Mode"
        if action in {"edit-preview", "edit-bullet", "append-bullet"}:
            return None, ("Draft Space is read-only for Bullets; sentences are edited in the "
                          "Revise view, structure through run-structure")
        paragraph = p.get("paragraph")
        url = ("/_board/draft?path=%s&file=%s"
               % (quote(p.get("path") or ""), quote(p.get("file") or "")))
        return {"url": url}, None
