"""s39's screen: a Section page's Draft view, as the live page draws it (JL 261113). Work is retired on paper pages
(focus_render: an old Work, Write or Revise link opens Draft), so the Section × Work cell records the Report's Draft
view: the view buttons, Draft first; 📋 Review Content with its five numbered sections, no state word on a bar; then 🧭
Around the Work, whose empty sections are hidden. paper_ui_cells imports SECTION_WORK, BUTTON_DRAFT, RAIL_DRAFT and the
two helpers (lab, bandw) from here.

The drawing stays honest against the live code: the view order is read from focus_draft_words.WORK (Draft sorted first,
as focus_draft_steps.work_views does), and every section title drawn must stand in focus_draft_steps.py, else the build
stops. Words are placeholders: the papers are unpublished and Tools is public.
"""
import re
from pathlib import Path

from five_parts import BODY, INK, OR, ROOM, TITLE, _el, line, text  # noqa: F401
from quick_draw import WIDE

HERE = Path(__file__).resolve().parent
TOOLS = next(p for p in HERE.parents if (p / "plugins/haipipe-toolkit").is_dir())
LIVE = TOOLS / "plugins/haipipe-toolkit/servers/workbench/workbench-task-draft"

# the view buttons: focus_draft_words.WORK, Draft first (focus_draft_steps.work_views), numbered in that order
_work = re.search(r"^WORK = \((.*)\)$", (LIVE / "focus_draft_words.py").read_text(encoding="utf-8"), re.M).group(1)
_keys = re.findall(r'\("(\w+)", "\d+ · ([^"]+)"\)', _work)
VIEWS = tuple(name for key, name in sorted(_keys, key=lambda kv: kv[0] != "draft"))
assert VIEWS[0] == "Draft", "focus_draft_words.WORK has no draft step"

# the five sections of Draft, in page order (focus_draft_steps.step_html: plain() names the first three, then
# _section adds the rubric and the decisions); a title missing from the live file stops the build
TITLES = ("✍️ Draft Lab", "📋 Review Report", "📚 Examples", "📏 Writing Rubric", "⚖️ Decisions")
_steps = (LIVE / "focus_draft_steps.py").read_text(encoding="utf-8")
assert all(f'"{t}"' in _steps for t in TITLES), "focus_draft_steps.step_html's Draft section titles changed"


def bandw(eid, x, y, w, name, why=""):
    """A band as the Section page draws it (focus_render.around_work: 📋 Review Content, 🧭 Around the Work): its name,
    then a thin rule that starts after the name, however long."""
    end = x + len(name) * 16 * WIDE + 24
    return text(eid + "_n", x, y + 6, name, 16, INK) + line(eid + "_r", [(end, y + 16), (x + w, y + 16)], ROOM, 1)


def lab(eid, x, y, w, rows_):
    """✍️ Draft Lab (draft_step_revise._text_and_cards): one row per sentence, its reading-position number and its fixed
    id small, the text justified (flush both edges), its marks after the last word; a Section or paragraph heading is a
    row too, with its own card. Cards stand on the right, level with their row; a decided card is faded and collapsed.
    `rows_`: ("h", heading, card) or ("s", position, id, marks, card); a card is (words, live) or None."""
    lw = w * 0.6
    rx, rw = x + lw + 12, w - lw - 12
    els = []
    for k, row in enumerate(rows_):
        ry = y + 24 * k
        if row[0] == "h":
            _, head, card = row
            els += text(f"{eid}{k}_h", x + 4, ry + 4, head, 12, TITLE)
        else:
            _, pos, sid, marks, card = row
            els += text(f"{eid}{k}_n", x + 4, ry + 4, pos, 11, INK) + text(f"{eid}{k}_i", x + 18, ry + 7, sid, 8, BODY)
            els += [_el("rectangle", f"{eid}{k}_l", x + 46, ry + 9, lw - 140, 6, ROOM, "#e9ecef")]
            els += text(f"{eid}{k}_m", x + lw - 88, ry + 4, marks, 10, INK)
        if card:
            words, live = card
            els += [_el("rectangle", f"{eid}{k}_c", rx, ry + 2, rw, 20, OR if live else ROOM, "#fff4e6" if live else "#f8f9fa",
                        roundness={"type": 3})] + text(f"{eid}{k}_ct", rx + 6, ry + 6, words, 9, INK if live else BODY)
    ly = y + 24 * len(rows_) + 6
    return els + text(eid + "_k1", x + 4, ly, "after the last word: 📊 values · 📚 citations · 🖼️ displays · 🕘 earlier wordings", 10, BODY) + \
        text(eid + "_k2", x + 4, ly + 16, "📝 edits · ★ lowest review score · 💬 comments · ✓ checked (a pass never changes it)", 10, BODY)


def lab_h(inner):
    return 24 * len(inner[1]) + 44


LAB = ("lab", (("h", "C1 · Title", ("§ <its heading card>", True)),
               ("s", "1", "S1a", "📊 📚", None),
               ("h", "C2 · Abstract", None),
               ("h", "C2.P1 · <a paragraph>", ("¶ <its paragraph card>", True)),
               ("s", "2", "S2a", "📊 ★6 💬", ("📝 Edit · A │ B · 72% same", True)),
               ("s", "3", "S3b", "📚 🕘 📝", ("📝 Edit · decided ▸", False)),
               ("s", "4", "S4a", "🖼️ ✓", ("💬 <your comment> · its reply", True))))
REVIEW = ("rows", (("<the score>", "/10"), ("Mechanics", "<its score> · <the smallest fix>"),
                   ("Function", "<its score> · <the smallest fix>"), ("Coherence · Anti-AI · Venue", "<each, the same way>")))
EXAMPLES = ("rows", (("<a published example>", "<what to copy from it>"), ("<another, same venue>", "<its opening move>")))
RUBRIC = ("sidetabs", (("This Section", "W rules · R rulings"), ("Coauthors", "writing-patterns.md"), ("Venue", "V blocks"),
                       ("Plain English", "read only"), ("Anti-AI", "read only")),
          (("W1", "<a writing rule>"), ("W2", "<a writing rule>"), ("R1", "<the author's ruling>"),
           ("✚", "<a new rule> · Add (POST /_board/draft-rule)")))
DECISIONS = ("sidetabs", (("This Section", "D-threads, then decisions"), ("Contract", "must-establish · refuse"),
                          ("Paper", "the Board's decisions.md"), ("Venue", "venues/<venue>/")),
             (("D1", "<an open thread, discussion.md>"), ("<date>", "<a decision, <stem>-decisions.md>"),
              ("✚", "<a new decision> · Add")))
INNER = (LAB, REVIEW, EXAMPLES, RUBRIC, DECISIONS)
DRAFT_SECS = ((("bandw", "📋 Review Content", ""),)
              + tuple(("sec", f"{k} · {t}", inner) for k, (t, inner) in enumerate(zip(TITLES, INNER), 1))
              + (("bandw", "🧭 Around the Work", ""),
                 ("sec", "🧰 Skills", ("rows", (("/haipipe-draft-writing", "this view · ✍️ Prompt · Copy prompt"),))),
                 ("sec", "Files", ("line", "<the Task's folder: draft/, records/, runs/>"))))
SECTION_WORK = (("Draft", DRAFT_SECS, VIEWS),)       # one screen, Draft; its buttons are all four views
# a button: its number and name alone, no state word (AGENTS.md § Page words)
BUTTON_DRAFT = {v: (f"{n} · {v}", "") for n, v in enumerate(VIEWS, 1)}
# the Section page's right rail as it reads live (focus_page.render, 261113)
RAIL_DRAFT = ("Report", "Studio", "Interactions", "Decisions", "Things to Know", "Checklist", "Timeline", "Skills", "Files",
              "Delivery")
