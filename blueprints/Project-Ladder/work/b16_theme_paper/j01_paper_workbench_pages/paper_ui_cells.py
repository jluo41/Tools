"""The nine sNN of j01 · The paper pages, level by level: one per level (Board, version, Section) and section (Report,
Work, Studio), each drawn in haipipe-studio's five parts (scripts/five_parts.py), as b17-s04. Each sNN's builder is
`build(Path(__file__).parent)`: its cell is found by its folder name (s32-board-ui-report → board, report).

A cell's Design is its page's views, lettered A, B, C …, each drawn as the same full screen (window, title and section
word, view buttons with that view in orange, its sections as heading bars with one line each), three a row, the open
question in red under them (JL 261031: "could you make each of them to be the same size and format"). A view is
settled one round at a time; a settled view's screen is written to delivery/ui/ (AGREED). Names are placeholders: the papers are unpublished and
Tools is public. The draft step names come from draft_steps.STEPS on every build (JL 261031: "I think it should be 3 x 3").
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = next(p for p in HERE.parents if (p / "plugins/haipipe-toolkit").is_dir())
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))
from five_parts import *  # noqa: E402,F401,F403  (the helpers and build())
from five_parts import _el  # noqa: E402
from canvas import change_note  # noqa: E402
import five_parts  # noqa: E402

_ds = (TOOLS / "plugins/haipipe-toolkit/servers/workbench/workbench-task-draft/draft_steps.py").read_text(encoding="utf-8")
STEPS = [s for s in re.search(r"^STEPS = \((.*?)\)$", _ds, re.M).group(1).replace('"', "").split(", ") if s[:1].isdigit()]
VERB = {"report": "Report", "work": "Work", "studio": "Studio"}          # no verb after the section word (b10-s33-D06)
LIST = ("Idea", "Story", "Data flow", "Paper flow", "Support blocks", "Evidence", "Displays", "Writing")   # the Board's views (s32-D12, D26)
PAGE = {"board": ("Paper-Example", "…/paper/Paper-Example"),
        "version": ("j11_writing_v1130_venue", "…/Paper-Example/j11_writing_v1130_venue"),
        "section": ("t00_summary", "…/j11_writing_v1130_venue/t00_summary")}


# ── the screen's parts, drawn plainly ───────────────────────────────────────────────────────────────────────────
def window(eid, x, y, w, h, url):
    els = [_el("rectangle", eid, x, y, w, h, INK, "#ffffff", roundness={"type": 3})]
    els += line(eid + "_bar", [(x, y + 28), (x + w, y + 28)], ROOM, 1)
    return els + [_el("ellipse", f"{eid}_d{k}", x + 10 + k * 14, y + 9, 9, 9, ROOM, ROOM) for k in range(3)] + \
        text(eid + "_url", x + 60, y + 7, url, 12, BODY)


def head(eid, x, y, name, section, views, on=0):
    """The title-&-section, then the view-button-list, the open view in orange."""
    els = text(eid + "_t", x, y, name, 20, INK) + text(eid + "_s", x + 12 * len(name) + 20, y + 4, VERB[section], 15, ROOM)
    cx = x
    for k, v in enumerate(views):
        w = 12 + 8 * len(v)
        els += [_el("rectangle", f"{eid}_v{k}", cx, y + 38, w, 24, OR if k == on else ROOM,
                    "#fff4e6" if k == on else "#ffffff", roundness={"type": 3})] + text(f"{eid}_v{k}_t", cx + 6, y + 42, v, 12, INK)
        cx += w + 8
    return els






def topic_row(eid, x, y, w, addr, words, stage):
    els = [_el("rectangle", eid, x, y, w, 64, ROOM, "#ffffff", roundness={"type": 3})]
    els += [_el("rectangle", eid + "_p", x + 10, y + 10, 70, 44, ROOM, "#f1f3f5")]
    els += text(eid + "_a", x + 92, y + 8, addr, 13, TITLE) + text(eid + "_w", x + 92, y + 28, words, 11, BODY)
    return els + text(eid + "_s", x + w - 110, y + 8, stage, 12, GR) + text(eid + "_v", x + 92, y + 44, "Slides · Draw · Mind map", 11, INK)










# ── the nine cells: Idea's words, the delivery piece, the two sketches and their open questions ───────────────────


def secbar(eid, x, y, w, title, words):
    """A section as the page draws it now: a boxed heading bar that folds, its content below it, unboxed."""
    return ([_el("rectangle", eid, x, y, w, 30, ROOM, "#ffffff", roundness={"type": 3})]
            + text(eid + "_t", x + 12, y + 7, "▾ " + title, 13, TITLE) + text(eid + "_w", x + 12, y + 38, words, 11, BODY))


LETTERS = "ABCDEFGH"                     # one letter per view, the same on Report and Work; the eight views use A to H (s32-D12, D26)


def slug(view):
    return view.lower().replace(" ", "-")


# Each view's sections, in page order, each with the one line under its bar (JL 261031: each view "the same size and
# format" as the big sketch). Titles are the bars the live page draws; words are placeholders, never paper text.
REPORT_SECTIONS = (
    ("Idea", (("sec", "1 · 🧭 Direction", ("big", "<the direction chosen, in one plain sentence>", "agreed")),  # s32-D14
              ("sec", "2 · 🔀 Directions considered", ("cardtabs", (("✅ selected", "<the chosen direction>"),  # tabs, as the RQs
                                                              ("○ second", "<direction 2>"), ("✕ lost", "<direction 3>")),
                                                             (("Direction", "<the direction, in full>"),
                                                              ("Verdict", "<selected, second, fallback, lost …>"),
                                                              ("Reason", "<why, in one line>"),
                                                              ("Decided", "<who and when>")))),
              ("sec", "3 · 🤝 Hand-off", ("chain", (("from", "s01-ideation"), ("hands", "<the direction, the venue>"),
                                                     ("to", "s02-story-<desk>-<idea>")))),
              ("rule",),                                                        # the helpers, at the bottom
              ("sec", "🙋 Interactions", ("ask", "r02_collect_idea_choices waits on you", "Answer")),
              ("sec", "🖼️ The drawing", ("picture", "<the topic, sNN-…>")),
              ("sec", "🧠 The mind map", ("line", "the topic's map, in its own frame")))),
    ("Story", (("sec", "1 · 💡 Pitch", ("big", "<what the paper finds, for whom, in one plain sentence>", "agreed")),
               ("sec", "2 · ❓ Questions", ("cardtabs", (("RQ1", "<the question, one line>"), ("RQ2", "<the question, one line>"),
                                                   ("RQ3", "<the question, one line>")),
                                          (("Hypothesis", "<what we expect, and why>"),        # the open RQ's detail
                                           ("Claim", "<what an answer lets the paper say>"),
                                           ("Tested by", "<its Runs and displays>"),
                                           ("Answer so far", "<the finding, or what it waits on>")))),
               ("sec", "3 · ⚖️ Stakes and evidence basis", ("tiles", (("Stakes", "why it matters,\nand to whom"),
                                                                     ("Evidence basis", "what it can claim,\nand what it cannot")))),
               ("sec", "4 · 🏛️ Venues", ("cardtabchain", (("target", "<journal>"), ("fallback 1", "<journal>"),  # Venue merged in;
                                                    ("fallback 2", "<journal>")),                    # each journal a tab,
                                         (("Desk rules", "<deadline · word limit · format>"),          # its related papers
                                          ("Review and scope", "<how it reviews, what it takes>"),      # inside (JL 261031)
                                          ("Related papers", "<its closest papers, on the related-work map>"),
                                          ("Fit", "<why this paper belongs here>")))),
               ("sec", "5 · 🗺️ Roadmaps", ("tiles", (("Discovery roadmap", "<the literature\nstill to read>"),
                                                   ("Task roadmap", "<the Runs\nstill to make>")))),
               ("sec", "6 · 🧠 Section narrative", ("narrative", "<paper>",                  # the narrative IS the
                                                     (("Introduction", "<what it says>"),     # mind map (JL 261031)
                                                      ("Methods", "<what it says>"), ("Results", "<what it says>"),
                                                      ("Discussion", "<what it says>")))),
               ("rule",),
               ("sec", "🙋 Interactions", ("ask", "r01_collect_story_choices waits on you", "Answer")),
               ("sec", "🖼️ The drawing", ("picture", "<the topic, sNN-…>")))),
    ("Data flow", (("sec", "1 · 🔗 Flow", ("flowmap", (("The data", ("<claims>", "<traits>", "<policy dates>")),   # the map of how
                                                    ("The linking", ("<visits>", "<physician>", "<state>")),   # the data come
                                                    ("The tables", ("<visit table>", "<other tables>")),        # together
                                                    ("The questions", ("Q01", "Q02", "Q03", "Q04", "Q05"))))),   # (JL 261101)
                   ("sec", "2 · 🧩 Questions to Runs", ("cardtabs", (("Q01", "<its name>"), ("Q02", "<its name>"), ("Q03", "<its name>")),
                                                       (("Question", "<the question, one line>"), ("Hypothesis", "<what we expect>"),
                                                        ("Claim if it holds", "<the claim>"), ("Now", "<its Runs, read or waiting>")))),
                   ("sec", "3 · 🚧 Waits on", ("line", "<what the flow still waits on>")),
                   ("rule",),
                   ("sec", "🖼️ The drawing", ("picture", "<the topic, sNN-…>")))),       # the Flow is the mind map
    ("Paper flow", (("sec", "1 · 📮 Send", ("big", "<the Sections, the displays, the dated steps to the send>", "send <date>")),
                    ("sec", "2 · 📑 Sections", ("cardtabs", (("Summary", "answers RQ1, RQ2"), ("Methods", "answers RQ1 … RQ5"),
                                                             ("Results", "answers RQ1 … RQ5")),
                                               (("Its job", "<what the Section must do>"), ("Displays", "<Figure 1, Table 1>"),
                                                ("Evidence", "<E1, E2>"), ("Words", "<its budget>")))),
                    ("sec", "3 · 🖼️ Displays", ("cardtabs", (("Figure 1", "✅ done"), ("Table 1", "⬜ not started"), ("Figure 2", "⬜ not started")),
                                               (("Title", "<its title>"), ("Kind", "<figure or table>"), ("Answers", "<RQ1>"),
                                                ("Made by", "<the Run that draws it>")))),
                    ("sec", "4 · 🗓️ Timeline", ("line", "<date · step · who · ✅ done, ⏳ running, ⬜ not started>")),
                    ("rule",),
                    ("sec", "🖼️ The drawing", ("picture", "<the topic, sNN-…>")))),
    ("Support blocks", (("sec", "1 · 🧪 Work", ("ftree", ((0, "Project-Example/", ""), (1, "work/", ""),          # one tree per
                                                         (2, "bNN_<block>/", "<what it builds>"),         # Project, only
                                                         (3, "jNN_<job>/", "<its goal>"),                     # what this paper
                                                         (4, "tNN_<task>/", "<its aim>"),                       # uses (JL 261101)
                                                         (0, "Project-Example-B/", ""), (1, "work/", ""),
                                                         (2, "bNN_<block>/", "<what it builds>")))),
                        ("sec", "2 · 🔎 Discovery", ("ftree", ((0, "Project-Example/", ""), (1, "discovery/", ""),
                                                              (2, "b01_<question>/", "<what it reads>"),
                                                              (3, "j01_<topic>/", "<its question>")))))),
    ("Evidence", (("sec", "1 · 🔢 Values", ("sidetabs", (("Sample", "<what it waits on>"), ("<policy>", "<…>"), ("Timing", "<…>")),   # side tabs:
                                                       (("1.", "<Section sentence · the number>"), ("", "source: <Run · file>"),   # list left,
                                                        ("2.", "<Section sentence · the number>"), ("", "source: <Run · file>")))),  # read right
                  ("sec", "2 · 📚 Citations", ("sidetabs", (("<topic A>", "<N checked>"), ("<topic B>", "<…>"), ("Methods", "<…>")),
                                                           (("<paper key>", "<its Sections> · ✅ checked"), ("<paper key>", "<its Sections> · ✅ checked")))),
                  )),
    # G · Displays, its own view after Evidence (JL 261101: "put the display outside of the Evidence, and put it after
    # the Evidence and before the Writing, to highlight it"): the plan against the venue, then each display
    ("Displays", (("sec", "1 · 📐 Plan", ("sidetabs", (("Figure 1 (Display A)", "📈 Figure · <what it shows>"),
                                                     ("Table 1 (Display B)", "📊 Table · <who is in it>"),
                                                     ("eFigure 1 (Display C)", "📈 Figure · <a check>")),
                                                    (("", "✅ 2 of at most 5 main displays · ❗ Display A: too narrow for 7 in at 300 dpi"),
                                                     ("Shows", "<its layout>"), ("Answers", "<RQ1> · Results · main"),
                                                     ("Made by", "<the Run>"), ("", "<its sketch>")))),
                  ("sec", "2 · 🖼️ Displays", ("sidetabs", (("Figure 1 (Display A)", "📈 Figure · <what it shows>"),
                                                          ("Table 1 (Display B)", "📊 Table · <who is in it>"),
                                                          ("eFigure 1 (Display C)", "📈 Figure · <a check>")),
                                                         (("", "Open all displays as one PDF"),
                                                          ("", "<preview.pdf: page 1 as the paper prints it, then how it was made>")))))),
    ("Writing", (("sec", "1 · ✍️ j11_writing_v1130_venue", ("sidetabs", (("Summary", "Plan: waits for your sign"),
                                                                       ("Methods", "Write: next"), ("Results", "Evidence: asked")),
                                                        (("BACKGROUND", "<the Section's text, to read>"), ("METHODS", "<its paragraph>"),
                                                         ("FINDINGS", "<its paragraph>"), ("", "Open the Section")))),
                 ("sec", "2 · 📄 The assembled paper", ("sidetabs", (("The paper", "draft · <when>"), ("The paper · Word", "draft · <when>"),
                                                                   ("Earlier round", "<when it was sent>")),          # each output
                                                      (("", "⤢ Pop out  (the whole paper over the page)"),            # read right;
                                                       ("", "<the PDF itself, page by page>"),                        # pops out
                                                       ("", "Open the PDF · Open the Word file")))))),                # (JL 261101)
)
# Every view in two bands, PROCESS and RESULTS, each numbered from 1 (JL 261101: "the index for each section should be
# 1, 2, ... 1, 2, 3"; "the results should be consistent to the report"). RESULTS is Report's own sections, the same on
# Report and Work; PROCESS is how the layer is being made: Interactions (Report: what was decided; Work: what waits on
# you), what is open (Evidence: where each stands; Writing: each Section's steps), and in Work the skills that do it
# (JL 261101: "show what is the skills related to each UI"). Report reads RESULTS first, Work PROCESS first.
SKILLS = {"Idea": (("/haipipe-paper-ideation", "picks the direction"), ("/haipipe-ideation", "finds and tests ideas")),
          "Story": (("/haipipe-paper-story", "questions, claims, narrative"), ("/haipipe-paper-venue", "each journal's desk rules"),
                    ("/haipipe-paper-related", "the closest papers")),
          "Data flow": (("/haipipe-paper-plan", "how the data becomes answers"), ("/haipipe-report", "each Board Question"),
                        ("/haipipe-task", "the Runs and their Results")),
          "Paper flow": (("/haipipe-paper-plan", "Sections, displays, dated steps"), ("/haipipe-paper", "routes the paper's work")),
          "Support blocks": (("/haipipe-work", "work Blocks, Jobs, Tasks"), ("/haipipe-discovery", "discovery Blocks, papers")),
          "Evidence": (("/haipipe-paper-evidence", "checks values and citations"), ("/haipipe-evidence", "lands each item")),
          "Displays": (("/haipipe-paper-plan", "plans each display against the venue"), ("/haipipe-display", "draws each table and figure"),
                       ("/haipipe-paper-evidence", "each version's preview.pdf")),
          "Writing": (("/haipipe-paper-draft", "one Section, step by step"), ("/haipipe-draft-writing", "writes the prose"),
                      ("/haipipe-paper-assemble", "builds the PDF and Word"))}
Q = (("Q1 · <a question>", "Needs your judgment", "Answer"), ("Q2 · <a question>", "Needs your judgment", "Answer"))
DONE = (("Q1 · <the pick>", "Answered", "See answers"), ("Q2 · <the pick>", "Answered", "See answers"))
TODO_STEPS = {          # each view's things to do, step by step, one row each: its words, its state, its verb (b15 s58 C2)
    "Data flow": ("2 · ⚙️ Runs to do", (("T0 · <return the Runs>", "waiting for you", "Open"),
                                                    ("T6 · <a Run>", "running", "Open"), ("T1 · <a Run>", "done", "Open"))),
    "Paper flow": ("2 · 🗓️ Next steps to the send", (("<date> · <step> · <who>", "waiting for you", ""),
                                                        ("<date> · <step> · <who>", "running", ""), ("<date> · <step> · <who>", "not started", ""))),
    "Evidence": ("2 · 📋 Where each stands", (("Values · Sample", "waiting", "Open"),
                                                             ("Citations · <topic A>", "done", "Open"))),
    "Displays": ("2 · 🖼️ Where each display stands", (("Figure 1 (Display A)", "done", "Open"),
                                                      ("Table 1 (Display B)", "not started", "Open"))),
    "Writing": ("2 · 🪜 Sections to finish", (("Summary · next: Plan", "waiting for you", "Open Plan"),
                                                       ("Methods · next: Evidence", "running", "Open Evidence"), ("Results · next: Write", "not started", "Open Write"))),
    "Support blocks": None}


def _bands(view, secs, work):
    cut = secs.index(("rule",)) if ("rule",) in secs else len(secs)
    results = tuple(x for x in secs[:cut] if not (x[0] == "sec" and "Waits on" in x[1]))     # Waits on is process
    helpers = tuple(x for x in secs[cut:] if not (x[0] == "sec" and "Interactions" in x[1]))  # Interactions is process
    process = [("sec", "1 · 🙋 Decisions waiting for you", ("todo", Q)) if work else
               ("sec", "1 · 🙋 Decisions made", ("todo", DONE))]
    if view == "Data flow":                  # the plan center: open it, use this skill, copy the prompt (JL 261101)
        process.append(("sec", "2 · 🧭 Plan", ("todo", (
            ("🗂️ Design the dataset", "use /haipipe-paper-plan", "Open · Copy prompt"),
            ("📈 Design the regressions", "use /haipipe-task", "Open · Copy prompt"),
            ("⚙️ Make them run", "use /haipipe-run", "Open · Copy prompt"),
            ("🖼️ Plan the displays", "use /haipipe-paper-plan", "Open · Copy prompt"),
            ("🔎 Plan the reading", "use /haipipe-discovery", "Open · Copy prompt")))))
    two = TODO_STEPS.get(view, ("2 · 🚧 Open", (("<an open point>", "open", ""),)))
    if two:
        process.append(("sec", two[0].replace("2 · ", f"{len(process) + 1} · ", 1), ("todo", two[1])))
    if work and view != "Data flow":
        process.append(("sec", f"{len(process) + 1} · 🧰 Skills that do it", ("rows", SKILLS[view])))
    P = (("band", "⚙️ Process", ""),) + tuple(process)
    R = (("band", "📊 Results", ""),) + results
    # the Report is its own sections only, 1, 2, 3; Process and Results are Work's (JL 261101; s32-D27)
    return (P + R if work else results) + (helpers if len(helpers) > 1 else ())


REPORT_ONLY = REPORT_SECTIONS
WORK_SECTIONS = tuple((v, _bands(v, secs, True)) for v, secs in REPORT_ONLY)
REPORT_SECTIONS = tuple((v, _bands(v, secs, False)) for v, secs in REPORT_ONLY)
LAYERS = "① plan: A to D   ·   ② explore: E   ·   ③ evidence: F, G   ·   ④ writing: H"


CAPTION = {"Idea": "the direction chosen, and the others", "Story": "what the paper says, and where it is sent",
           "Data flow": "how the data becomes each answer", "Paper flow": "Sections in reader order, to the send",
           "Support blocks": "the work and discovery Blocks behind it", "Evidence": "each value and citation",
           "Displays": "each display, against the venue's rules",
           "Writing": "each send, its Sections and their steps"}
CRUMB = {"board": "Physician-SPACE › Project-Example › paper › Paper-Example", "version": "… › Paper-Example › j11_writing_v1130_venue",
         "section": "… › j11_writing_v1130_venue › t00_summary"}
GOAL = {"board": "Purpose: one paper, from its idea to its send", "version": "Goal: this send, ready by its date",
        "section": "Aim: this Section, as the venue asks"}
RAIL = ("Report", "Work", "Studio", "Interactions", "Delivery", "Related", "Timeline", "Files")


BLUE = "#1864ab"                     # the workbench's colour for the current thing (frame.py :root)


def buttons(eid, x, y, verbs, color=INK):
    """Verb buttons, styled like Answer: a word in a small rounded box."""
    els, bx = [], x
    for k, v in enumerate(verbs):
        bw = 14 + 7.5 * len(v)
        els += [_el("rectangle", f"{eid}{k}", bx, y, bw, 24, ROOM, "#ffffff", roundness={"type": 3})] + \
            text(f"{eid}{k}_t", bx + 7, y + 5, v, 11, color)
        bx += bw + 6
    return els


def lead(eid, x, y, w, label, words, stage):
    """The view's main point, first and largest: a blue edge, its label, the sentence big, the picture beside it."""
    els = [_el("rectangle", eid, x, y, w, 124, ROOM, "#ffffff", roundness={"type": 3}),
           _el("rectangle", eid + "_e", x, y, 8, 124, BLUE, BLUE)]
    els += text(eid + "_l", x + 22, y + 12, label, 12, BLUE) + text(eid + "_s", x + w - 290, y + 12, stage, 12, GR)
    els += text(eid + "_w", x + 22, y + 34, words, 19, INK)
    els += [_el("rectangle", eid + "_p", x + w - 203, y + 12, 189, 74, ROOM, "#f1f3f5")]
    return els + buttons(eid + "_b", x + w - 203, y + 92, ("Slides", "Draw", "Mind map"))


def ask(eid, x, y, w, words, verb):
    els = [_el("rectangle", eid, x, y, w, 38, OR, "#fff4e6", roundness={"type": 3})]
    els += text(eid + "_t", x + 14, y + 10, words, 13, INK)
    return els + [_el("rectangle", eid + "_b", x + w - 96, y + 6, 82, 26, OR, "#ffffff", roundness={"type": 3})] + \
        text(eid + "_bt", x + w - 84, y + 11, verb, 12, OR)


def tiles(eid, x, y, w, items):
    tw = (w - 16 * (len(items) - 1)) / len(items)
    els = []
    for k, (t, words) in enumerate(items):
        tx = x + k * (tw + 16)
        els += [_el("rectangle", f"{eid}{k}", tx, y, tw, 84, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_t", tx + 12, y + 10, t, 13, TITLE) + text(f"{eid}{k}_w", tx + 12, y + 34, words, 12, INK)
    return els


def chain(eid, x, y, w, title, steps, verb):
    """A sequence as boxes and arrows, each box with its role word above its name; the verb button on the right."""
    els = text(eid + "_t", x, y, title, 14, TITLE) + buttons(eid + "_v", x + w - 104, y - 4, (verb,))
    bw = 150
    for k, (role, name) in enumerate(steps):
        bx = x + k * (bw + 46)
        els += text(f"{eid}{k}_r", bx + 2, y + 30, role, 10, BLUE if k == 0 else BODY)
        els += [_el("rectangle", f"{eid}{k}", bx, y + 46, bw, 40, BLUE if k == 0 else ROOM, "#e7f5ff" if k == 0 else "#ffffff",
                    roundness={"type": 3})] + text(f"{eid}{k}_w", bx + 12, y + 58, name, 12, INK)
        if k:
            els += arrow(f"{eid}{k}_a", [(bx - 40, y + 66), (bx - 6, y + 66)], ROOM)
    return els


def more(eid, x, y, w, items):
    """Everything else, open, small, one line each: its name, then its line."""
    els = []
    for k, (n, words) in enumerate(items):
        els += line(f"{eid}{k}_l", [(x, y + k * 28), (x + w, y + k * 28)], "#e9ecef", 1) + \
            text(f"{eid}{k}", x + 8, y + k * 28 + 7, n, 12, INK) + text(f"{eid}{k}_w", x + 150, y + k * 28 + 7, words, 11, BODY)
    return els


def big(eid, x, y, w, words, stage):
    """The view's main point, under section 1's bar: one large sentence and its state word (no edge, JL 261031)."""
    return text(eid + "_w", x + 4, y + 2, words, 19, INK) + text(eid + "_s", x + 4, y + 36, stage, 12, GR)


def picture(eid, x, y, w, name):
    """The topic's picture, its name under it, and its verbs; the mind map has its own place (A: its own helper,
    B: section 6), so it is not a button here (b16 s32 A r01, B r04)."""
    return [_el("rectangle", eid + "_p", x, y, 189, 74, ROOM, "#f1f3f5")] + text(eid + "_n", x, y + 78, name, 11, BODY) + \
        buttons(eid + "_b", x + 204, y + 50, ("Slides", "Draw"))


def chain_only(eid, x, y, w, steps, verb=None):
    els = chain(eid, x, y - 37, w, "", steps, verb or "")[1:]
    return els if verb else [e for e in els if not e["id"].startswith(eid + "_v")]


def one_line(eid, x, y, w, words):
    return text(eid, x + 4, y, words, 12, BODY)


def cardtabs(eid, x, y, w, items, detail):
    """Tiles that act as a view-button-list (JL 261031: "for each RQ, when we click it, will it show the results
    below? ... treat them as the view button list"): one open at a time, the first open (orange in the drawing),
    the open one's detail in a panel under the tiles."""
    tw = (w - 16 * (len(items) - 1)) / len(items)
    els = []
    for k, (t, words) in enumerate(items):
        tx = x + k * (tw + 16)
        els += [_el("rectangle", f"{eid}{k}", tx, y, tw, 64, OR if k == 0 else ROOM, "#fff4e6" if k == 0 else "#ffffff",
                    roundness={"type": 3})]
        els += text(f"{eid}{k}_t", tx + 12, y + 8, t, 13, TITLE) + text(f"{eid}{k}_w", tx + 12, y + 32, words, 12, INK)
    py = y + 76
    els += [_el("rectangle", eid + "_d", x, py, w, 18 + 26 * len(detail), OR, "#ffffff", roundness={"type": 3})]
    for k, (name, words) in enumerate(detail):
        els += text(f"{eid}_d{k}", x + 14, py + 10 + k * 26, name, 12, TITLE) + \
            text(f"{eid}_d{k}_w", x + 140, py + 10 + k * 26, words, 12, INK)
    return els


def cardtabchain(eid, x, y, w, steps, detail):
    """A sequence whose boxes act as a view-button-list (JL 261031: "the journal can serve the same, like each
    journal you can describe the information about that journal"): role word above each box, arrows between, the
    first open, the open box's detail in a panel under the chain."""
    bw, els = 150, []
    for k, (role, name) in enumerate(steps):
        bx = x + k * (bw + 46)
        els += text(f"{eid}{k}_r", bx + 2, y, role, 10, OR if k == 0 else BODY)
        els += [_el("rectangle", f"{eid}{k}", bx, y + 16, bw, 40, OR if k == 0 else ROOM, "#fff4e6" if k == 0 else "#ffffff",
                    roundness={"type": 3})] + text(f"{eid}{k}_w", bx + 12, y + 28, name, 12, INK)
        if k:
            els += arrow(f"{eid}{k}_a", [(bx - 40, y + 36), (bx - 6, y + 36)], ROOM)
    py = y + 68
    els += [_el("rectangle", eid + "_d", x, py, w, 18 + 26 * len(detail), OR, "#ffffff", roundness={"type": 3})]
    for k, (name, words) in enumerate(detail):
        els += text(f"{eid}_d{k}", x + 14, py + 10 + k * 26, name, 12, TITLE) + \
            text(f"{eid}_d{k}_w", x + 160, py + 10 + k * 26, words, 12, INK)
    return els


def narrative(eid, x, y, w, root, branches):
    """The Section narrative drawn as its mind map (JL 261031: "the mindmap is actually the narrative"): the paper
    in the middle-left, a branch per Section in reader order, each with what it says; the full map opens by button."""
    n = len(branches)
    ry = y + (n * 32 - 32) / 2
    els = [_el("rectangle", eid + "_r", x, ry, 110, 32, TITLE, "#e7f5ff", roundness={"type": 3})] + \
        text(eid + "_rt", x + 14, ry + 8, root, 12, INK)
    for k, (name, words) in enumerate(branches):
        by = y + k * 32
        els += line(f"{eid}{k}_l", [(x + 110, ry + 16), (x + 170, by + 14)], ROOM, 1)
        els += [_el("rectangle", f"{eid}{k}", x + 170, by, 130, 28, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_n", x + 180, by + 6, name, 12, TITLE) + text(f"{eid}{k}_w", x + 316, by + 6, words, 12, INK)
    return els + buttons(eid + "_b", x + w - 82, y + n * 32 - 26, ("Mind map",))


def flowmap(eid, x, y, w, cols):
    """How the data come together (JL 261101: "show the mind map of how these data are collected together"): a column
    each for the data, the linking, the tables and the questions, a line from each box to the next column."""
    cw, bh, gap = (w - 3 * 24) / 4, 22, 6
    els = []
    for c, (head, boxes) in enumerate(cols):
        cx = x + c * (cw + 24)
        els += text(f"{eid}{c}_h", cx, y, head, 11, TITLE)
        for k, name in enumerate(boxes):
            by = y + 18 + k * (bh + gap)
            els += [_el("rectangle", f"{eid}{c}_{k}", cx, by, cw, bh, TITLE if c == 3 else ROOM, "#ffffff", roundness={"type": 3})]
            els += text(f"{eid}{c}_{k}_t", cx + 6, by + 4, name, 10, INK)
            if c:
                pk = min(k, len(cols[c - 1][1]) - 1)
                py = y + 18 + pk * (bh + gap) + bh / 2
                els += line(f"{eid}{c}_{k}_l", [(cx - 24, py), (cx, by + bh / 2)], ROOM, 1)
    return els


def ftree(eid, x, y, w, rows):
    """A folder tree, one line per folder: its name, then its line, an elbow from its parent."""
    els = []
    for k, (depth, name, words) in enumerate(rows):
        ry, rx = y + k * 22, x + depth * 22
        if depth:
            els += line(f"{eid}{k}_l", [(rx - 14, ry - 12), (rx - 14, ry + 8), (rx - 3, ry + 8)], ROOM, 1)
        els += text(f"{eid}{k}", rx, ry, name, 11, TITLE if depth > 1 else BODY)
        if words:
            els += text(f"{eid}{k}_w", rx + 9 * len(name) + 10, ry, words, 10, BODY)
    return els


def sidetabs(eid, x, y, w, items, detail):
    """Side tabs (JL 261101: "in the left there is a panel, and we can read the content quickly"): the items as a list on
    the left, the first open; the open one's content to read on the right."""
    lw = 110                                     # narrow, so the reading panel gets the room (JL 261101)
    els = []
    for k, (head, words) in enumerate(items):
        iy = y + k * 40
        els += [_el("rectangle", f"{eid}{k}", x, iy, lw, 34, OR if k == 0 else "#ffffff", "#fff4e6" if k == 0 else "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_t", x + 8, iy + 3, head, 11, TITLE) + text(f"{eid}{k}_w", x + 8, iy + 18, words, 9, BODY)
    ph = 18 + 24 * len(detail)
    els += [_el("rectangle", eid + "_d", x + lw + 14, y, w - lw - 14, max(ph, 40 * len(items)), OR, "#ffffff", roundness={"type": 3})]
    for k, (name, words) in enumerate(detail):
        els += text(f"{eid}_d{k}", x + lw + 26, y + 10 + k * 24, name, 10, TITLE) + text(f"{eid}_d{k}_w", x + lw + 110, y + 10 + k * 24, words, 10, INK)
    return els


def rows(eid, x, y, w, items):
    """Short rows, a name then its words (skills, steps, where each stands)."""
    els = []
    for k, (name, words) in enumerate(items):
        els += text(f"{eid}_{k}n", x + 4, y + k * 24, name, 12, TITLE) + text(f"{eid}_{k}w", x + 220, y + k * 24, words, 12, BODY)
    return els


TODO_PILL = {"Needs your judgment": (OR, "#fff4e6"), "waiting for you": (OR, "#fff4e6"), "running": (BLUE, "#e7f5ff"),
             "done": (GR, "#ebfbee"), "Answered": (GR, "#ebfbee")}


def todo(eid, x, y, w, items):
    """One full-width row per thing to do: its words, its state a coloured pill, its verb (b15 s58 C2)."""
    els = []
    for k, (words, state, verb) in enumerate(items):
        ry = y + 40 * k
        els += [_el("rectangle", f"{eid}{k}", x, ry, w, 34, ROOM, "#ffffff", roundness={"type": 3})]
        els += text(f"{eid}{k}_w", x + 12, ry + 9, words, 13, INK)
        stroke, fill = TODO_PILL.get(state, (ROOM, "#f8f9fa"))
        pw = 16 + 6.5 * len(state)
        verbs = tuple(verb.split(" · ")) if verb else ()
        bw = sum(20 + 7.5 * len(v) for v in verbs)
        px = x + w - 12 - (bw + 8 if verb else 0) - pw
        els += [_el("rectangle", f"{eid}{k}_p", px, ry + 7, pw, 20, stroke, fill, roundness={"type": 3})]
        els += text(f"{eid}{k}_pt", px + 8, ry + 10, state, 10, INK)
        if verb:
            els += buttons(f"{eid}{k}_b", x + w - 12 - bw, ry + 5, verbs)
    return els


def paras(eid, x, y, w, items):
    """A draft's text as the page lays it out: each paragraph its id and name, then its sentences as grey lines with
    their S numbers (JL 261101: "show the scratch of the layout here")."""
    els, yy, s_no = [], y, 0
    for k, (head, n) in enumerate(items):
        els += text(f"{eid}{k}_h", x + 4, yy, head, 12, TITLE)
        for j in range(n):
            lw = w - 60 - (j * 37) % 120
            s_no += 1                              # sentences count straight through the Section: S1, S2, S3 …
            els += text(f"{eid}{k}_s{j}", x + 4, yy + 22 + j * 18, f"S{s_no}", 9, BODY)
            els += [_el("rectangle", f"{eid}{k}_l{j}", x + 30, yy + 26 + j * 18, lw, 6, ROOM, "#e9ecef")]
        yy += 30 + 18 * n
    return els


def split(eid, x, y, w, items, right, by_s):
    """The text in two panels, as the draft page lays it out (rv-split: JL 261101, "it is the left part, and the right
    part"): the paragraphs and their sentences on the left; on the right, under its title, what belongs to each
    sentence, level with it: your editor row (Write), its evidence card (Evidence), its note (Revise)."""
    lw = (w - 16) * 0.55
    els = paras(eid + "_l", x, y + 22, lw, items)
    rx, rw = x + lw + 16, w - lw - 16
    els += [_el("rectangle", eid + "_rb", rx, y, rw, SIZE["paras"](("paras", items)) + 22, ROOM, "#ffffff", roundness={"type": 3})]
    els += text(eid + "_rt", rx + 10, y + 4, right, 11, TITLE)
    yy, s_no = y + 22, 0
    for k, (head, n) in enumerate(items):
        for j in range(n):
            s_no += 1
            sy = yy + 22 + j * 18
            what = by_s.get(s_no) if isinstance(by_s, dict) else (f"S{s_no} · <your words>" if by_s == "editor" else None)
            if what:
                label, state = (what, "") if isinstance(what, str) else what
                els += [_el("rectangle", f"{eid}_r{s_no}", rx + 8, sy - 3, rw - 16, 15, OR if state else ROOM,
                            "#fff4e6" if state else "#ffffff", roundness={"type": 3})]
                els += text(f"{eid}_r{s_no}_t", rx + 14, sy - 2, label + (f"  · {state}" if state else ""), 9, INK)
        yy += 30 + 18 * n
    return els


def chips(eid, x, y, w, items):
    """A Section a row, its five step words as chips, each opening that step (paper_version.section_row, s36-D01)."""
    els = []
    for k, (name, words) in enumerate(items):
        ry = y + 34 * k
        els += text(f"{eid}{k}_n", x + 4, ry + 6, name, 11, TITLE)
        cx = x + 150
        for j, wd in enumerate(words):
            cw = 14 + 6.2 * len(wd)
            you = wd.endswith(("sign", "asked"))
            els += [_el("rectangle", f"{eid}{k}_c{j}", cx, ry, cw, 24, OR if you else ROOM, "#fff4e6" if you else "#ffffff",
                        roundness={"type": 3})] + text(f"{eid}{k}_c{j}_t", cx + 7, ry + 5, wd, 10, INK)
            cx += cw + 5
    return els


def editor(eid, x, y, w, label):
    """An editor the person types in: a framed box, faint lines, its label."""
    els = [_el("rectangle", eid, x, y, w, 70, ROOM, "#ffffff", roundness={"type": 3})] + text(eid + "_t", x + 10, y + 6, label, 11, BODY)
    for j in range(3):
        els += [_el("rectangle", f"{eid}_l{j}", x + 10, y + 28 + j * 13, w - 60 - j * 70, 4, ROOM, "#f1f3f5")]
    return els


def band(eid, x, y, w, name, why=""):
    """A view's part, ⚙️ Process or 📊 Results: its name and a thin rule after it, as b15 s58 and the live page draw it
    (servers/workbench/ui_parts.py PROCESS, RESULTS; JL 261101: one look in every theme)."""
    return text(eid + "_n", x, y + 6, name, 16, INK) + line(eid + "_r", [(x + 120, y + 16), (x + w, y + 16)], ROOM, 1)


UNDER = {"chips": (chips, 0), "split": (split, 0), "paras": (paras, 0), "editor": (editor, 76), "todo": (todo, 4 * 40 + 2), "rows": (rows, 3 * 24 + 4), "big": (big, 64), "sidetabs": (sidetabs, 18 + 24 * 4 + 6), "ftree": (ftree, 9 * 22 + 6), "flowmap": (flowmap, 18 + 5 * 28 + 6), "narrative": (narrative, 4 * 32 + 6), "cardtabchain": (cardtabchain, 68 + 18 + 26 * 4 + 6), "cardtabs": (cardtabs, 76 + 18 + 26 * 4 + 6), "tiles": (tiles, 96), "chain": (chain_only, 70), "ask": (ask, 50), "picture": (picture, 100),
         "line": (one_line, 26)}


def sec_block(eid, x, y, w, title, inner):
    """A section as the page draws it: a boxed heading bar that folds, numbered in reading order, its content
    under it, unboxed and shown as what it is (JL 261031: "each section to be the [heading bar] ... seems to be
    ordered")."""
    els = [_el("rectangle", eid, x, y, w, 30, ROOM, "#ffffff", roundness={"type": 3})] + \
        text(eid + "_t", x + 12, y + 7, "▾ " + title, 13, TITLE)
    return els + UNDER[inner[0]][0](eid + "_c", x, y + 42, w, *inner[1:])


BLOCK = {"band": (band, 40), "lead": (lead, 140), "ask": (ask, 52), "tiles": (tiles, 100), "chain": (chain, 106)}


SIZE = {"todo": lambda inner: 40 * len(inner[1]) + 2, "rows": lambda inner: 24 * len(inner[1]) + 4,
        "paras": lambda inner: sum(30 + 18 * n for _, n in inner[1]),
        "split": lambda inner: sum(30 + 18 * n for _, n in inner[1]) + 26,
        "chips": lambda inner: 34 * len(inner[1]), "line": lambda inner: 26 if inner[1] else 0}


def block_h(sec):
    if sec[0] == "sec":
        kind = sec[2][0]
        return 42 + (SIZE[kind](sec[2]) if kind in SIZE else UNDER[kind][1]) + 14
    if sec[0] == "rule":
        return 24
    if sec[0] == "more":
        return 28 * len(sec[1]) + 16
    if sec[0] in BLOCK:
        return BLOCK[sec[0]][1]
    return 76 if len(sec) == 3 else 58


def screen(eid, x, y, h, level, section, views, on, secs):
    """One view as the full screen of the big sketch: the window, the title and section word, the view buttons with
    this one in orange, then its content: a section is a heading bar with its line under it (title, words); a topic
    or a row is a box with its picture, name, line and stage (name, words, stage)."""
    name, path = PAGE[level]
    els = window(eid + "w", x, y, 700, h, f"…&path={path}&section={section}")
    els += text(eid + "_cr", x + 40, y + 38, CRUMB[level], 10, ROOM)
    els += head(eid + "h", x + 40, y + 56, name, section, views, on)
    els += text(eid + "_go", x + 40, y + 126, GOAL[level], 11, BODY)
    els += text(eid + "_ca", x + 40, y + 146, CAPTION.get(views[on], ""), 11, INK)
    for k in range(4):                                            # left-rail: pale page lines
        els += line(f"{eid}_lr{k}", [(x + 10, y + 180 + k * 22), (x + 28, y + 180 + k * 22)], ROOM, 1)
    for k, r in enumerate(RAIL):                                  # right-rail: the sections, this one marked
        els += text(f"{eid}_rr{k}", x + 622, y + 180 + k * 22, r, 9, OR if r.lower() == section else ROOM)
    yy = y + 172
    for k, sec in enumerate(secs):
        if sec[0] == "sec":
            els += sec_block(f"{eid}r{k}", x + 40, yy, 570, sec[1], sec[2])
        elif sec[0] == "rule":
            els += line(f"{eid}r{k}", [(x + 40, yy + 8), (x + 610, yy + 8)], ROOM, 1, dashed=True)
        elif sec[0] == "more":
            els += more(f"{eid}r{k}", x + 40, yy, 570, sec[1])
        elif sec[0] in BLOCK:
            els += BLOCK[sec[0]][0](f"{eid}r{k}", x + 40, yy, 570, *sec[1:])
        elif len(sec) == 3:
            els += topic_row(f"{eid}r{k}", x + 40, yy, 570, *sec)
        else:
            els += secbar(f"{eid}r{k}", x + 40, yy, 570, *sec)
        yy += block_h(sec)
    return els


def tall(secs):
    return sum(block_h(sec) for sec in secs)


def screens(eid, x, y, items, level, section, changed=None, gap=40):
    """Every view lettered A, B, C …, every screen the same size (the tallest view's), three a row (JL 261031: each
    view "the same size and format" as the big sketch)."""
    cols = min(3, len(items))
    h = 192 + max(tall(secs) for _, secs in items)
    views = tuple(v for v, _ in items)
    els = []
    for k, (view, secs) in enumerate(items):
        sx, sy = x + (k % cols) * (700 + gap), y + (k // cols) * (h + 40 + gap)
        els += text(f"{eid}{k}_L", sx, sy, f"{LETTERS[k]} · {view}", 22, TITLE)
        if changed and LETTERS[k] in changed:
            els += [change_note(sx + 260, sy + 4, changed[LETTERS[k]], "261031", None)]
        els += screen(f"{eid}{k}", sx, sy + 40, h, level, section, views, k, secs)
    return els, y + ((len(items) + cols - 1) // cols) * (h + 40 + gap)


# ── the nine cells' views, each view its content in page order; names are placeholders (Tools is public) ─────────────
STUDIO_GROUPS = (                    # the Board Studio's views are its groups, a paper Board's _studio_groups.txt (r03, pick B)
    ("Ideation", (("s01-ideation", "the direction chosen, and the others", "shaping"),)),
    ("Story", (("s02-story-<desk>-<idea>", "the paper's questions and claims", "agreed"),)),
    ("Plan", (("s03-paper-dataflow", "how the data becomes each answer", "shaping"),
              ("s04-paper-workflow", "Sections in reader order, to the send", "shaping"))),
    ("Related work", (("s10-related-work-<venue>", "the closest papers, mapped", "shaping"),
                      ("s11-related-<type>", "one type of related paper, read closely", "explore"),
                      ("s12-related-<type>", "another type, read closely", "explore"))),
)
SECTIONS = (("t00_summary", "Summary"), ("t01_introduction", "Introduction"), ("t02_methods", "Methods"), ("t03_results", "Results"))
# A version (a writing Job) and a Section (a draft Task) keep what their pages show today, regrouped into the two parts
# every view has (JL 261101: "keep the previous draft workbench, keep the content as much as possible but use the new
# subsections layout"; "add the Interaction things as well, so we can track our changes along the way"): ⚙️ Process
# (the interactions, then the work rows) and 📊 Results (what the step or view made), each numbered from 1. The rows
# are the pages' own (focus_draft.step_html, paper_version.version_work_views); nothing is invented. Placeholders only.
def _lvl(results, process, work):
    P = (("band", "⚙️ Process", ""),) + tuple(process)
    R = (("band", "📊 Results", ""),) + tuple(results) if results else ()
    return P + R if work else R + P


IX = ("sec", "1 · 🙋 Interactions", ("todo", (("<a form on this page>", "waiting for you", "Answer"),
                                             ("<a decision recorded here>", "done", "See answers"))))
IX_NONE = ("sec", "1 · 🙋 Nothing waits on you", ("line", ""))
STEPW = lambda *w: tuple(f"{n} {x}" for n, x in zip(("Plan", "Write", "Evidence", "Display", "Revise"), w))
V_WORK = {   # what paper_version.version_work_views draws today, regrouped (JL 261101: "keep the content")
    "Draft-Main": ((IX, ("sec", "2 · 🪜 Sections", ("chips", (("t00_summary", STEPW("sign", "done", "next", "optional", "later")),
                                                             ("t01_introduction", STEPW("done", "done", "asked", "optional", "next")),
                                                             ("t02_methods", STEPW("done", "next", "later", "next", "later")))))), ()),
    "Draft-Appendix": ((IX_NONE, ("sec", "2 · 🪜 Sections", ("chips", (("t21_appendix", STEPW("done", "next", "later", "next", "later")),)))), ()),
    "Display-Main": ((IX_NONE,), (("sec", "1 · 🖼️ Displays", ("todo", (("Figure 1 · <its label>", "done", "Open"),
                                                                       ("Table 1 · <its label>", "not started", "Open")))),)),
    "Display-Appendix": ((IX_NONE,), (("sec", "1 · 🖼️ Displays", ("todo", (("eTable 1 · <its label>", "done", "Open"),))),)),
    "Values": ((IX_NONE,), (("sec", "1 · 🔢 Values", ("todo", (("<a value set>", "waiting for you", "Open"),
                                                             ("<another>", "done", "Open")))),)),
    "Citations": ((IX_NONE,), (("sec", "1 · 📚 Citations", ("todo", (("<a citation set>", "done", "Open"),))),)),
}
VERSION_WORK = tuple((v, _lvl(r, p_, True)) for v, (p_, r) in V_WORK.items())
VERSION_REPORT = (   # the frame's own Job views, as they show today (focus_page.py: MindMap · Status · Findings), regrouped
    ("MindMap", _lvl((("sec", "1 · 🧠 The map", ("narrative", "j11_writing_v1130_venue",
                                                 tuple((t, n) for t, n in SECTIONS))),), (IX,), False)),
    ("Status", _lvl((("sec", "1 · 📋 Tasks", ("todo", tuple((f"{t} · {n}", "not started", "") for t, n in SECTIONS[:3]))),), (IX,), False)),
    ("Findings", _lvl((("sec", "1 · 💡 Findings", ("rows", (("<a takeaway>", "in the answer's own words"),
                                                         ("<what waits for you>", "")))),), (IX,), False)),
)
VERSION_STUDIO = (                   # its own topics, then the Board's (s37 r03, pick A)
    ("This version", (("Ask the agent", "Copy prompt: talk and sketch about this send"),
                      ("s20-j01-telling", "how this version tells the story", "explore"),
                      ("s21-j01-round1", "round 1 comments, grouped", "shaping"))),
    ("Board", (("s02-story-<desk>-<idea>", "the paper's questions and claims", "agreed"),
               ("s04-paper-workflow", "Sections in reader order, to the send", "shaping"))),
)
SECTION_REPORT = (                   # MindMap · Text · Status stay (s38 r01 Q2, pick B); cards read only (Q1, pick A)
    ("MindMap", _lvl((("sec", "1 · 🧠 The map", ("rows", (("The map", "paragraphs, then points, then sentences"),
                                                           ("Open a node", "its sentences and their cards")))),), (IX,), False)),
    ("Text", _lvl((("sec", "1 · 📖 The text", ("rows", (("C1.P1 Background", "S1 to S2, each sentence beside its cards"),
                                                         ("C1.P2 Methods", "S3 to S6, read only"), ("C1.P3 Findings", "S7 to S11, read only")))),),
                  (IX,), False)),
    ("Status", _lvl((("sec", "1 · 📋 Where it stands", ("rows", (("Each step", "its word: done, next, waits"),
                                                               ("Waits on you", "the sign or card that holds it")))),), (IX,), False)),
)
# Each step as the draft workbench shows it today (focus_draft.step_html): ⚙️ Process 1 Interactions (the step's sign,
# the Task's forms and records), 2 Ask the agent (Plan, Write, Revise), 3 Input, 4 Runs of this step; 📊 Results, the
# step's own cards, by the names the page gives them.
ASK = ("sec", "2 · 🤖 Ask the agent", ("rows", (("Copy prompt", "the step's prompt, with your notes"),)))
STRUCT = ("narrative", "<Section>", (("C1.P1", "<point 1> · <point 2>"), ("C1.P2", "<point 3> · <point 4>"),
                                    ("C1.P3", "<point 5>"), ("C1.P4", "<point 6> · <point 7>")))
PARAS = (("C1.P1 · Background", 2), ("C1.P2 · Methods", 3), ("C1.P3 · Findings", 2))
TEXT = ("paras", PARAS)
TEXT_WRITE = ("split", PARAS, "✍️ Write it yourself", "editor")                     # draft_steps._text_and_editor
TEXT_EVIDENCE = ("split", PARAS, "🔎 Its evidence", {3: ("VALUE <the number>", "checked"), 5: ("CITE <the source>", "owed"),
                                                     6: ("DISPLAY Figure 1", "drawn")})  # draft_steps ev-split
# Revise as the page lays it out (draft_steps._revise, _text_and_cards): the text on the left, a + beside each sentence
# for your comment; on the right the pass's cards in reading order, filtered by chips (Comments · Logic · Edits ·
# Evidence): an Edit card with ✓ Accept ✗ Reject ✎ Edit, your Comment and its reply, a Logic score per sentence
TEXT_REVISE = ("split", PARAS, "🃏 Revise cards · Pass 2\n[Comments] [Logic] [Edits] [Evidence]",
               {2: ("Edit · <Why · Original → Expected>", "✓ Accept ✗ Reject ✎ Edit"), 4: ("Comment · <your note>", "AI replied"),
                6: ("Logic · S6 · logic 7/10 · read 8/10", "")})
STEP_CARDS = {   # each card by the name draft_steps gives it, drawn as a scratch of its layout (JL 261101)
    "Plan": (("📐 §1 Structure · v0.1", STRUCT), ("Scratch · your notes, a paragraph each", ("editor", "<your note on C1.P1>")),
             ("📚 Examples", ("rows", (("<an example paper>", "what to copy from it"), ("<another>", "its opening move")))),
             ("🧭 The Section's contract, from its Story", ("rows", (("Answers", "RQ1, RQ2"), ("Claims", "C1, C2"), ("Words", "<its budget>")))),
             ("📏 Requirement and Rubric", ("rows", (("<a venue rule>", "must"), ("<a rubric point>", "scored /10")))),
             ("🗂 Records", ("rows", (("<context record>", "<date>"), ("<plan record>", "<date>"))))),
    "Write": (("✍️ The text · v0.1", TEXT_WRITE), ("📚 Examples", ("rows", (("<an example paper>", "its paragraph shape"),)))),
    "Evidence": (("🔎 The text and its evidence · v0.1", TEXT_EVIDENCE), ("✍ Asks, for you to tick", ("todo", (("S3 · VALUE · <the number it quotes>", "waiting for you", "Tick"),
                                                      ("S5 · CITE · <the source>", "done", "Open")))),
                 ("❗ What does not resolve", ("todo", (("S7 · <a value with no Run>", "not started", "Open"),)))),
    "Display": (("🖼 The text and its displays · v0.1", ("picture", "<Figure 1, beside the sentence that calls it>")),),
    "Revise": (("📋 Revise Review Report · Pass 2", ("rows", (("Mechanics", "MEETS · 8/10 · Fix: <the smallest fix>"),
                                                               ("Function", "NEEDS WORK · 6/10 · Fix: <the smallest fix>"),
                                                               ("Evidence", "MEETS · 8/10"), ("Readability", "MEETS · 9/10"),
                                                               ("Coherence · Anti-AI · Venue", "<each, the same way>")))),
               ("✍️ The text and its Revise cards · v0.2", TEXT_REVISE),
               ("💬 Your marks from the canvas", ("rows", (("<a red mark on the drawing>", "its words"),))),
               ("📜 Revise rules · how a pass runs, and the author's rulings", ("rows", (("R1", "<a rule>"), ("R2", "<your ruling>")))),
               ("🕘 Older versions", ("rows", (("draft-v0.1", "previous/"),)))),
    "Runs": (("Every Run of this Section", ("todo", (("<a Run>", "done", "Open"), ("<a Run>", "running", "Open")))),),
}


def _step(name):
    proc = [("sec", "1 · 🙋 Interactions", ("todo", ((f"{name}: waits for your sign", "waiting for you", "Open the draft"),
                                                     ("<a decision recorded here>", "done", "See answers"))))]
    if name in ("Plan", "Write", "Revise"):
        proc.append(ASK)
    if name != "Runs":
        proc.append(("sec", f"{len(proc) + 1} · 📥 Input", ("line", "the table of what the step reads")))
        proc.append(("sec", f"{len(proc) + 1} · 🏃 Runs of this step", ("rows", (("<a Run>", "its type · its status"),))))
    res = tuple(("sec", f"{k} · {t}", inner) for k, (t, inner) in enumerate(STEP_CARDS[name], 1))
    return _lvl(res, proc, True)


SECTION_WORK = tuple((v, _step(v)) for v in STEP_CARDS)
assert [v for v, _ in SECTION_WORK][:-1] == [x.split(" · ")[1] for x in STEPS], "draft_steps.STEPS changed"
SECTION_STUDIO = (                   # always on the right-rail; Copy prompt only, no new-topic button (s40 r03, pick B)
    ("This Section", (("Ask the agent", "Copy prompt: talk and sketch"), ("No topic yet", "no Studio topic names t00_summary"))),
    ("Board", (("s02-story-<desk>-<idea>", "the paper's questions and claims", "agreed"),
               ("s04-paper-workflow", "Sections in reader order, to the send", "shaping"))),
)
VIEWS = {   # (level, section): (the line above the screens, the views, the open question, green notes)
    ("board", "report"): ("① plan: A to D   ·   ② explore: E   ·   ③ evidence: F   ·   ④ writing: G   ·   each: RESULTS, then PROCESS",
                          REPORT_SECTIONS, "(none: agreed, s32-D24)", {"A": "A: RESULTS · PROCESS bands"}),
    ("board", "work"): ("the same views and letters as Report; each: PROCESS (with its skills), then RESULTS, the same as Report",
                        WORK_SECTIONS, "? Work: PROCESS first;\nRESULTS = Report (261101)", {"A": "A: PROCESS · RESULTS bands (proposed)"}),
    ("board", "studio"): ("the groups of _studio_groups.txt, in button order; a topic's groups are its Tags", STUDIO_GROUPS,
                          "? these groups, or\nthe Block's own (r03)", None),
    ("version", "report"): ("the frame's own Job views (MindMap · Status · Findings), each 📊 Results then ⚙️ Process", VERSION_REPORT,
                            "? the same views, regrouped\n(261101)", {"A": "A: both parts, content as today (proposed)"}),
    ("version", "work"): ("each view: ⚙️ Process (its interactions, then the Sections' step words), then 📊 Results (the items)", VERSION_WORK,
                          "? the same rows, regrouped\n(261101, t02 r04)", {"A": "A: content as today (proposed)"}),
    ("version", "studio"): ("this version's own topics, then the Board's", VERSION_STUDIO,
                            "? a version's own topics,\nor only the Board's (r03)", None),
    ("section", "report"): ("each view: 📊 Results (as today), then ⚙️ Process (its interactions)", SECTION_REPORT,
                            "? the same views, regrouped\n(261101)", {"B": "B: content as today (proposed)"}),
    ("section", "work"): ("each step as the draft workbench shows it: ⚙️ Process (interactions, Ask the agent, Input, Runs), then 📊 Results (its cards)", SECTION_WORK,
                          "? the same sections, regrouped\n(261101, t03 r04)", {"A": "A: content as today (proposed)"}),
    ("section", "studio"): ("always on the right-rail, even before a topic names the Section", SECTION_STUDIO,
                            "? start a topic from here\nwith one click (r03)", None),
}
PIECE = {
    ("board", "report"): ("the Board's Report: the paper's four layers as views",
                          ["a Board opened on steps,\nnot on what it found", "answers sat in report\nfolders, unread", "no one line said\nhow far it has got"]),
    ("board", "work"): ("the Board's Work: the same views, each layer's work",
                        ["versions sat as a\ndropdown, not rows", "no row said which\nversion waits", "the old frame drew\nthree rows of tabs"]),
    ("board", "studio"): ("the Board's Studio: the paper's topics, by group",
                          ["Story and Ideation hid\nin old Spaces", "topics were one long\nlist, no groups", "a row said too much"]),
    ("version", "report"): ("a version's Report: the paper as the reader gets it",
                            ["a version hid which\nSection waits on me", "no whole manuscript\nto read", "status lived in chips"]),
    ("version", "work"): ("a version's Work: its Sections and their steps",
                          ["seven tabs per Section\nin a card", "no word said which\nstep waits", "a click went to\nthe old page"]),
    ("version", "studio"): ("a version's Studio: the topics that name it",
                            ["a send's telling had\nno place of its own", "review rounds sat\nin the Board", "no talk-and-sketch\nprompt here"]),
    ("section", "report"): ("a Section's Report: sentences beside their cards",
                            ["Findings said No\ntakeaways recorded", "the text read as\none block", "no evidence beside\nthe sentence"]),
    ("section", "work"): ("a Section's Work: the draft Task page",
                          ["the steps were old\npages in iframes", "cards inside cards,\nfold arrows", "no verb said what\nto do next"]),
    ("section", "studio"): ("a Section's Studio: always on the right-rail",
                            ["Studio sat as a\nWork button", "no topic named the\nSection: it vanished", "the prompt was\na long box"]),
}


# the letters settled so far: Report A (s32-D14), then all seven (JL 261101: "s32 is very good now"; "for the blocks I
# think they are good to go", s32-D24)
AGREED = {("board", "report"): {LETTERS[k]: secs for k, (_, secs) in enumerate(REPORT_SECTIONS)}}
MOCK = """<!doctype html><meta charset=utf-8><title>{letter} · {view}</title>
<!-- GENERATED by paper_ui_cells.py from AGREED; the agreed screen of {nn} view {letter} -->
<style>body{{font:14px system-ui;margin:24px;max-width:820px;color:#1e1e1e;background:#fff}}h1{{font-size:22px;margin:0}}
h1 small{{color:#868e96;font-weight:400;margin-left:8px}}nav{{margin:12px 0 18px}}nav span{{display:inline-block;border:1px solid
#ced4da;border-radius:6px;padding:3px 9px;margin-right:6px;font-size:12px}}nav span.on{{border-color:#e8590c;background:#fff4e6}}
section{{border:1px solid #dee2e6;border-radius:8px;padding:9px 14px;margin:8px 0}}section b{{font-size:13px}}</style>
<h1>Paper-Example<small>{section}</small></h1><nav>{nav}</nav>{secs}"""


def write_agreed(topic, nn, level, section):
    """delivery/ui/<level>-<section>/<L>-<view>.html for each settled letter; the screen, placeholder words only."""
    names = [v for v, _ in VIEWS[(level, section)][1]]
    for letter, secs in AGREED.get((level, section), {}).items():
        view = names[LETTERS.index(letter)]
        out = topic / "delivery" / "ui" / f"{level}-{section}" / f"{letter}-{slug(view)}.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        nav = "".join(f'<span class={"on" if v == view else "off"}>{v}</span>' for v in names)
        out.write_text(MOCK.format(letter=letter, view=view, nn=f"s{nn}", section=VERB[section], nav=nav,
                                   secs="".join(f"<section><b>▾ {t}</b><br><small>{w}</small></section>"
                                                for t, w in map(flat, secs) if t)) + "\n", encoding="utf-8")


def flat(sec):
    """(title, one line) of a section in either form, for the agreed screen file."""
    if sec[0] == "rule":
        return "", ""
    if sec[0] == "band":
        return sec[1], sec[2]
    if sec[0] != "sec":
        return sec[0], sec[1]
    inner = sec[2]
    words = {"tiles": lambda: " · ".join(t for t, _ in inner[1]), "cardtabs": lambda: " · ".join(t for t, _ in inner[1]),
             "cardtabchain": lambda: " → ".join(n for _, n in inner[1]),
             "narrative": lambda: " · ".join(n for n, _ in inner[2]),
             "flowmap": lambda: " → ".join(h for h, _ in inner[1]),
             "ftree": lambda: " · ".join(n for d, n, _ in inner[1] if d == 2),
             "sidetabs": lambda: " · ".join(h for h, _ in inner[1]), "chain": lambda: " → ".join(n for _, n in inner[1]),
             "picture": lambda: "Slides · Draw · Mind map",
             "todo": lambda: " · ".join(f"{w} ({st})" for w, st, _ in inner[1]),
             "rows": lambda: " · ".join(n for n, _ in inner[1])}.get(inner[0], lambda: inner[1])()
    return sec[1], words.replace("\n", " ")


def build(topic: Path):
    topic = Path(topic).resolve()
    m = re.match(r"s(\d+)-(board|version|section)-ui-(report|work|studio)$", topic.name)
    nn, level, section = m.group(1), m.group(2), m.group(3)
    piece, why = PIECE[(level, section)]
    lay, items, ask, changed = VIEWS[(level, section)]
    names = [v for v, _ in items]
    last = LETTERS[len(names) - 1]
    write_agreed(topic, nn, level, section)
    ui = topic / "delivery" / "ui"
    part = f"ui/{level}-{section}"
    lettered = True                                  # every cell: one lettered screen per view (JL 261031)
    pieces = [("page", f"{part}/{L}-{slug(v)}.html", f"{L} · the {v} view", (ui / f"{level}-{section}" / f"{L}-{slug(v)}.html").exists())
              for L, v in zip(LETTERS, names)]
    sk = topic / "delivery" / "skill" / f"{level}-{section}-views.md"
    pieces.append(("book", f"skill/{sk.name}", "the views' manual, for workbench-paper", sk.exists()))
    spec = {"title": f"{level.capitalize()} UI · {VERB[section]}: {piece.split(': ', 1)[1]}",
            "why": {"question": f"why do we need s{nn}?", "notes": why,
                    "quote": "JL 261031: 3 x 3, Board, version, Section × Report, Work, Studio"},
            "what": {"head": f"② what s{nn} hands over: one screen", "icon": "page", "name": "delivery/ui/", "type": "ui",
                     "deck_why": f"stays in s{nn}'s delivery/deck/, so anyone gets it in a minute",
                     "parts": pieces},
            "job": topic.parent.parent,
            "target": {"board": "servers/workbench-paper/ (the Board page)", "version": "servers/workbench-paper/ (a version page)",
                       "section": "workbench-task-draft/focus_draft.py (b32 s42)"}[level],
            "missing": [(name, "not settled yet") for _, name, _, done in pieces if not done and lettered]
                       or ([] if (ui / f"{level}-{section}").exists() else [(part, "the agreed screen, not drawn yet")])}
    if lettered:
        spec["have"] = [(name, "agreed") for icon, name, _, done in pieces if done and icon == "page"]
        spec["what"]["head"] = f"② what s{nn} hands over: one screen, A to {last}"
        spec["target"] = "servers/workbench-paper/ · workbench-paper/SKILL.md"

    def design():                                    # A, B, C … every view the same screen; no separate main sketch
        els = text("skA", 690, 280, f"A to {last} · {piece}, every view the same screen", 18, TITLE)
        els += text("lay", 690, 340, lay, 16, BODY)
        e, bottom = screens("sc", 690, 380, items, level, section, changed)
        return els + e + sticky("askD", 1180, bottom + 20, 320, 76, ask, 15, -0.03, RED, RE)

    return five_parts.build(topic, spec, design, shift=2300 - 925 * (3 - min(3, len(items))))
