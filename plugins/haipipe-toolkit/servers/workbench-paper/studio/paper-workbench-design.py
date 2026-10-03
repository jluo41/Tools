"""Build paper-workbench-design.excalidraw, the Paper workbench design drawing.

The drawing is generated: change this file, then run it (AGENTS.md rule 6):

    .venv/bin/python Tools/plugins/haipipe-toolkit/servers/workbench-paper/studio/paper-workbench-design.py

Part 1 answers the main question (JL 260928): which Spaces and sub-spaces the
paper has, which runs each sub-space holds, in what order, and which skill each
run uses. Part 2 draws each Space as the workbench shows it (content on the
left, the Runs panel on the right, same grammar as the Page workbench drawing).
Part 3 lists what changed and what each Space reads. Part 0 (JL 261003) draws the shell
every workbench shares: title, band, the Space row with Guide first and plain names, one
box per Space, the Runs panel folded to a strip; Guide › RoadMap Draw shows this drawing
as the Paper family's "Workbench design".
"""
import json
import random
import sys
import time
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_suffix(".excalidraw")
random.seed(260928)
NOW = int(time.time() * 1000)
E = []

BLUE, GREEN, INK, MUTED, RULE, PANEL = "#1864ab", "#2b8a3e", "#1e1e1e", "#495057", "#ced4da", "#f8f9fa"


def base(id_, type_, x, y, w, h, stroke=INK, bg="transparent", dashed=False, rounded=True):
    return {"id": id_, "type": type_, "x": x, "y": y, "width": w, "height": h, "angle": 0,
            "strokeColor": stroke, "backgroundColor": bg, "fillStyle": "solid", "strokeWidth": 2,
            "strokeStyle": "dashed" if dashed else "solid", "roughness": 0, "opacity": 100,
            "groupIds": [], "frameId": None, "roundness": {"type": 3} if rounded else None,
            "seed": random.randint(1, 2**31 - 1), "version": 1,
            "versionNonce": random.randint(1, 2**31 - 1), "isDeleted": False,
            "boundElements": [], "updated": NOW, "link": None, "locked": False}


def text(id_, x, y, s, size=16, color=INK, mono=False):
    lines = s.split("\n")
    w = max(len(l) for l in lines) * size * (0.6 if mono else 0.56)
    e = base(id_, "text", x, y, w, len(lines) * size * 1.25, stroke=color, rounded=False)
    e.update(text=s, originalText=s, fontSize=size, fontFamily=3 if mono else 8,
             textAlign="left", verticalAlign="top", containerId=None, autoResize=True,
             lineHeight=1.25)
    E.append(e)


def rect(id_, x, y, w, h, stroke=INK, bg="transparent", dashed=False):
    E.append(base(id_, "rectangle", x, y, w, h, stroke, bg, dashed))
    return E[-1]


def button(id_, x, y, w, h, label, sel=False, size=17, dashed=False, green=False):
    stroke = GREEN if green else (BLUE if sel else INK)
    bg = "#ebfbee" if green else ("#e7f5ff" if sel else "transparent")
    r = rect(id_, x, y, w, h, stroke, bg, dashed)
    tw, th = len(label) * size * 0.56, size * 1.25
    t = base(id_ + "-text", "text", x + (w - tw) / 2, y + (h - th) / 2, tw, th,
             stroke=stroke, rounded=False)
    t.update(text=label, originalText=label, fontSize=size, fontFamily=8, textAlign="center",
             verticalAlign="middle", containerId=id_, autoResize=True, lineHeight=1.25)
    r["boundElements"] = [{"id": id_ + "-text", "type": "text"}]
    E.append(t)


def line(id_, x, y, w, color=RULE):
    e = base(id_, "line", x, y, w, 0, stroke=color, rounded=False)
    e.update(points=[[0, 0], [w, 0]], lastCommittedPoint=None, startBinding=None,
             endBinding=None, startArrowhead=None, endArrowhead=None)
    E.append(e)


def arrow(id_, x, y, points, color, both=False):
    e = base(id_, "arrow", x, y, max(p[0] for p in points), max(abs(p[1]) for p in points), stroke=color,
             rounded=False)
    e.update(points=points, lastCommittedPoint=None, startBinding=None, endBinding=None,
             startArrowhead="arrow" if both else None, endArrowhead="arrow", elbowed=False)
    E.append(e)


FW, FH, GAP = 1176, 820, 32
X = [48 + i * (FW + GAP) for i in range(4)]

# ---- title -------------------------------------------------------------------
text("title", 48, 24, "Paper Workbench · design", 34)
text("subtitle", 48, 74, "Question first: each Space answers one question; each sub-space holds its runs "
     "in order; each run names the skill that does the work.", 18, MUTED)

# ---- part 0 · the shell every workbench shares (JL 261003) --------------------
S0 = 128
text("p0-title", 48, S0, "0 · The shell every workbench shares", 28)
rect("p0-screen", 48, S0 + 52, 2400, 330, RULE)
text("p0-h1", 72, S0 + 72, "📄 <paper title>      /w/<paper-board-folder>", 24)
button("p0-band", 72, S0 + 116, 2352, 42, "band · desk · Story version · N questions · N Sections · "
       "built or not built yet      e.g.  ManSci · Story v0.5 · 5 questions · 19 Sections · not built yet", size=16)
for n, (lab, w) in enumerate((("Guide", 110), ("Ideation", 130), ("Story", 110), ("Sections", 130), ("Delivery", 130))):
    button(f"p0-space-{n}", 72 + sum((110, 130, 110, 130, 130)[:n]) + n * 12, S0 + 176, w, 44, lab, sel=n == 2)
rect("p0-box", 72, S0 + 236, 2190, 126, RULE)
text("p0-box-note", 96, S0 + 252,
     "one box per Space: its tabs and View row first (a rule under it, no \"View\" label), then its content\n"
     "Guide: Description · Method · RoadMap Draw (this drawing + the Workbench Table) · Related Paper\n"
     "No `all boards · board index` line; Spine shows Identity · Pitch · Stakes by name, never C-codes; "
     "a Section's state is its word (🟡 Partial)", 17, MUTED)
button("p0-runs", 2278, S0 + 236, 146, 126, "◂ Runs", size=17, dashed=True)
text("p0-runs-note", 2278, S0 + 368, "folded until opened", 14, MUTED)

# ---- part 1 · Space → sub-space → runs in order → skill ----------------------
P1 = S0 + 420
text("p1-title", 48, P1, "1 · Spaces, sub-spaces, runs in order, and the skill of each run", 28)

MAP = [
    ("Ideation", "What paper should we write?", [
        ("Ideas", [("1", "Generate ideas", "haipipe-ideation-generate", ""),
                   ("2", "Test idea", "haipipe-ideation-test", "novelty · pressure · journal fit"),
                   ("3", "Idea review", "haipipe-paper-ideation", ""),
                   ("4", "Select idea", "haipipe-ideation-select", "G0 · the person decides")]),
    ], "hands on: the chosen idea and its venue → the Story"),
    ("Story", "What does the paper ask, and what must it find out?", [
        ("Spine", [("1", "Story revise", "haipipe-paper-story · haipipe-writing", "Identity · Pitch · Stakes")]),
        ("RoadMap Draw", []),
        ("High-level logic + Low-level work", [("2", "Task review", "haipipe-paper-story", "T<n> and D<n> under a hypothesis: is each the right question?"),
                       ("3", "Task runs", "haipipe-task", "T<n> → its Task folder (BJTR); you press Run"),
                       ("4", "Discovery runs", "haipipe-discovery", "D<n> → its Discovery folder (BJTR)"),
                       ("5", "Claim review", "haipipe-paper-story", "RQ → its claims, after 3 and 4")]),
        ("Related Papers", [("4", "Discovery runs", "haipipe-discovery", "P<n> → its Paper Run; the card opens the PDF")]),
    ], "hands on: C8 rows → Sections · Task and Discovery Results → Evidence Items"),
    ("Sections", "Does each Section say it right, with evidence?", [
        ("Narrative view", [("1", "Narrative review", "haipipe-paper-story", "the Section's C8 row")]),
        ("Table view", [("2", "Draft runs", "haipipe-page-structure → haipipe-page-writing", "then haipipe-page-revise"),
                        ("4", "Delivery runs", "haipipe-page-delivery", "run-delivery-webpage · latex · word"),
                        ("5", "Page check", "haipipe-page-check", "one exact version")]),
        ("Evidence view", [("3", "Evidence runs", "haipipe-page-evidence", "binds Task and Discovery Results")]),
    ], "tabs Main · Appendix pick the Sections · hands on: each Section's current files → Delivery"),
    ("Delivery", "Is the manuscript ready to send?", [
        ("LaTeX · Word", [("1", "Build", "haipipe-paper-assemble", "compile order from the Story"),
                          ("3", "Check", "haipipe-paper-assemble", "the build and the letter's checks; then you send")]),
        ("Cover letter", [("2", "Cover letter", "haipipe-paper-assemble", "words on the RD02 Round page; built with the manuscript")]),
        ("Rounds", [("4", "Response", "haipipe-paper-round", "one Round Page per review batch")]),
    ], "views Preview · Artifacts · Checks · hands on: a review round → new T or D questions in the Story"),
]
def _height(subs):
    y = 120
    for _sub, runs in subs:
        ry = y + sum(62 if note else 44 for *_x, note in runs)
        y = max(y + 56, ry + 12)
    return y


BH = max(_height(subs) for _t, _a, subs, _h in MAP) + 76
for i, (title, asks, subs, hands) in enumerate(MAP):
    x0, y0 = X[i], P1 + 56
    rect(f"m{i}-box", x0, y0, FW, BH)
    text(f"m{i}-title", x0 + 24, y0 + 22, title, 28)
    text(f"m{i}-asks", x0 + 24, y0 + 64, asks, 19, BLUE)
    line(f"m{i}-rule", x0 + 24, y0 + 100, FW - 48)
    y = y0 + 120
    for n, (sub, runs) in enumerate(subs):
        button(f"m{i}-sub{n}", x0 + 24, y, 200, 40, sub, size=17)
        ry = y
        for k, (num, run, skill, note) in enumerate(runs):
            text(f"m{i}-sub{n}-run{k}", x0 + 248, ry + 4, "%s  %-15s" % (num, run), 19, INK, mono=True)
            text(f"m{i}-sub{n}-skill{k}", x0 + 520, ry + 4, skill, 17, GREEN, mono=True)
            if note:
                text(f"m{i}-sub{n}-note{k}", x0 + 520, ry + 30, note, 14, MUTED)
            ry += 62 if note else 44
        y = max(y + 56, ry + 12)
    text(f"m{i}-hands", x0 + 24, y0 + BH - 52, hands, 16, MUTED)

mid = P1 + 56 + 60
for i in range(3):
    arrow(f"m-link{i}", X[i] + FW + 2, mid, [[0, 0], [GAP - 4, 0]], BLUE)
# a review round sends new questions back to the Story
back_y = P1 + 56 + BH + 36
arrow("m-back", X[3] + FW // 2, P1 + 56 + BH + 2, [[0, 0], [0, 34], [-(X[3] - X[1]), 34], [-(X[3] - X[1]), 0]],
      MUTED)
text("m-back-label", X[2] - 520, back_y + 8, "Rounds route new questions back to the Story's Roadmap", 16, MUTED)
text("m-rules", 48, back_y + 56,
     "The number is the order inside a Space. A question is written first; its run then creates or continues the "
     "folder that answers it (BJTR = Block › Job › Task › Run).\n"
     "Each run type names its skill in run-cards.md (🧩 SKILL); a run's own `skills:` line wins. "
     "Creating a folder never starts a run: the person presses Run.", 17)

# ---- part 2 · each Space as the workbench shows it ----------------------------
P2 = back_y + 170
text("p2-title", 48, P2, "2 · Each Space: content on the left, its Runs panel on the right", 28)
Y0 = P2 + 56


def space(key, i, title, tabs, sel_tab, reads, views, sel_view, draw_content, types, sel_type, run, notes):
    x0 = X[i]
    rect(f"{key}-space", x0, Y0, FW, FH)
    text(f"{key}-title", x0 + 24, Y0 + 26, title, 30)
    line(f"{key}-rule", x0 + 24, Y0 + 62, FW - 48)
    tx = x0 + 24
    for n, tab in enumerate(tabs):                  # a tab is as wide as its label
        tw = max(176, 11 * len(tab) + 28)
        button(f"{key}-tab-{n}", tx, Y0 + 76, tw, 50, tab, sel=n == sel_tab, size=19)
        tx += tw + 12
    text(f"{key}-reads", x0 + 24, Y0 + 148, reads, 16, MUTED)
    if views:                                       # the View row needs no label (JL 261003)
        for n, v in enumerate(views):
            button(f"{key}-view-{n}", x0 + 24 + n * 122, Y0 + 176, 112, 42, v, sel=n == sel_view)
    cx, cy = x0 + 24, Y0 + 272
    rect(f"{key}-content", cx, cy, 552, 410)
    draw_content(key, cx, cy)
    rx, ry = x0 + 600, Y0 + 272
    rect(f"{key}-runs", rx, ry, 552, 410, bg=PANEL)
    text(f"{key}-runs-title", rx + 18, ry + 22, "Runs", 22)
    text(f"{key}-runs-fold", rx + 90, ry + 28, "shown open here; on the page it starts folded", 13, MUTED)
    for n, label in enumerate(types):
        button(f"{key}-type-{n}", rx + 18, ry + 70 + n * 50, 180, 40, label, sel=n == sel_type,
               size=14, dashed=label.startswith("+"))
    dx, dy = rx + 210, ry + 70
    rect(f"{key}-detail", dx, dy, 324, 316, bg="#ffffff")
    text(f"{key}-run-name", dx + 14, dy + 12, run["name"], 15)
    text(f"{key}-skill", dx + 14, dy + 38, "Skill " + run["skill"], 11, GREEN, mono=True)
    button(f"{key}-rerun", dx + 232, dy + 8, 80, 28, "Rerun", size=13)
    button(f"{key}-copy", dx + 232, dy + 58, 80, 28, "Copy", size=13)
    text(f"{key}-prompt-label", dx + 14, dy + 62, "Prompt", 15)
    text(f"{key}-prompt", dx + 14, dy + 84, run["prompt"], 12, MUTED)
    text(f"{key}-process-label", dx + 14, dy + 156, "Running process", 15)
    text(f"{key}-process", dx + 14, dy + 178, run["process"], 12)
    text(f"{key}-results-label", dx + 14, dy + 228, "Results", 15)
    text(f"{key}-results", dx + 14, dy + 250, run["results"], 12, BLUE)
    text(f"{key}-notes", x0 + 24, Y0 + 706, notes, 16)


def card(key, x, y, w, head, body, sel=False, h=None):
    color = BLUE if sel else INK
    if sel:
        rect(f"{key}-sel", x - 8, y - 8, w + 16, h or 40, BLUE, "#e7f5ff")
    text(f"{key}-head", x, y, head, 14, color)
    if body:
        text(f"{key}-body", x + 14, y + 22, body, 12, color)


def ideation_content(key, cx, cy):
    x = cx + 18
    card(f"{key}-i1", x, cy + 40, 510,
         "▾ i1 · Review-inferred physician agreeableness and\n   prescribing behavior beyond the public rating",
         "\n\nResearch question: does perceived agreeableness predict\n"
         "opioid prescribing beyond the public star rating?\n"
         "Verdict: PROCEED WITH CAUTION\n"
         "Went to: StoryA-misq-phytrait-discretion\n"
         "▸ Pitch · Stakes · Evidence · Risks",
         sel=True, h=196)
    text(f"{key}-more", x, cy + 262, "▸ i2 · …\n▸ i3 · …", 14, MUTED)


space("ideation", 0, "Ideation", ["Ideas"], 0,
      "Reads Story00-ideation.md · Ideas (ranked) · Idea divisions", [], None,
      ideation_content,
      ["1 Generate ideas", "2 Test idea", "3 Idea review · 1", "4 Select idea", "+ New Run"], 2,
      {"name": "run-idea-01", "skill": "haipipe-paper-ideation",
       "prompt": "Review i1 against its evidence. Record\nits rationale, limits and next question\n"
                 "in a new version; do not select again.",
       "process": "✓ read Story00 ✓ wrote v001\n▸ waiting for your feedback",
       "results": "results/run-idea-01/v001.md\nBefore / After · Accept"},
      "Ideas → 1 Generate · 2 Test · 3 Review · 4 Select (G0)\n"
      "The card says its verdict and the Story it went to.")


def story_content(key, cx, cy):
    """The question is the block (JL 260929): logic left, its work right, in run order."""
    x = cx + 18
    card(f"{key}-q1", x, cy + 30, 510,
         "▾ Question 1 · Is there an association beyond the rating?",
         "  Hypothesis 1a               🔨 │  › Data  › Training  › Evaluation\n"
         "  Holds: it adds to the rating   │\n"
         "                                 │  Results  What do all the models say?\n"
         "  Claim 1a                       │   for Hypothesis 1a · b03 j02 t01  ▸ 4 runs\n"
         "  Beyond the rating: …           │  Discovery  Has anyone shown this?\n"
         "  Contribution 1a                │   b01 j01 t01 prior_work  supports\n"
         "  A new signal: …                │", sel=True, h=132)
    text(f"{key}-rest", x, cy + 182,
         "▸ Question 2 · Is the link stronger at high doses?\n"
         "▸ Not under a question", 12, mono=True)


space("story", 1, "Story", ["Spine", "RoadMap Draw", "High-level logic + Low-level work", "Related Papers"], 2,
      "Reads StoryA-….md · Spine ### 1, 2, 4 · RoadMap Draw studio/ · logic + work ### 3, 5, 6 (D, Q), 7 (T)", [], None,
      story_content,
      ["2 Task review · 0", "3 Task runs · 22", "4 Discovery runs · 53", "5 Claim review · 1", "+ New Run"], 1,
      {"name": "b03.j02.t01.r04", "skill": "haipipe-task",
       "prompt": "/haipipe-task T5: continue the Task\nfolder that answers this question;\nJL presses Run.",
       "process": "Done · used by S-MISQ-Main-0-Abstract\nand S-MISQ-Main-5-Results",
       "results": "task/b03_…/t01_…/results/r04_…/"},
      "Spine → 1 Story revise\n"
      "High-level logic + Low-level work → 2 Task review · 3 Task runs · 4 Discovery runs · 5 Claim review\n"
      "Question block: Hypotheses · Claims · Contributions │ its work, named as questions, in run order (JL 260929).")


def sections_content(key, cx, cy):
    x = cx + 18
    text(f"{key}-row0", x, cy + 30, "▸ 0 · Abstract              v2.2   🟡 Partial", 13, mono=True)
    rect(f"{key}-row1-sel", x - 8, cy + 58, 526, 30, BLUE, "#e7f5ff")
    text(f"{key}-row1-head", x, cy + 64, "▸ 1 · Introduction          v2.6   🔨 Draft   Open ↗", 13, BLUE, mono=True)
    text(f"{key}-rows", x, cy + 98,
         "▸ 2 · Literature Review     v1.3   🟡 Partial\n"
         "▸ 3 · Theory                v2.4   🔨 Draft\n"
         "▸ 4 · Empirical Strategy    v1.5   🟡 Partial\n"
         "▸ 5 · Results               v1.5   ✅ Check\n"
         "▸ 6 · Discussion            v1.3   🟡 Partial\n"
         "▸ 7 · Conclusion            v1.2   🟡 Partial", 13, mono=True)


space("sections", 2, "Sections", ["Main", "Appendix"], 0,
      "Reads StoryA-….md ### 8 (order, narrative) · each Section Page", ["Table", "Narrative", "Evidence"], 0,
      sections_content,
      ["1 Narrative review", "2 Draft runs · 23", "3 Evidence runs · 72", "4 Delivery runs · 3",
       "5 Page check", "+ New Run"], 1,
      {"name": "run-section-0927-readability", "skill": "haipipe-page-writing · haipipe-writing",
       "prompt": "/haipipe-page run S-MISQ-Main-1-\nIntroduction: continue this Section's\nDraft in its Page workbench.",
       "process": "Waiting · your feedback on P2",
       "results": "results/run-section-0927-readability/\nv003.md · working.md"},
      "Narrative → 1 Narrative review · Evidence → 3 Evidence runs\n"
      "Table → 2 Draft runs · 4 Delivery runs · 5 Page check\n"
      "Open ↗ goes to that Page's workbench; its runs are the same runs.")


def delivery_content(key, cx, cy):
    x = cx + 18
    text(f"{key}-head", x, cy + 24, "RD02 · not ready · Open ↗   …-cover-letter.pdf", 15)
    rect(f"{key}-page", x + 60, cy + 60, 390, 320, RULE, "#ffffff")
    text(f"{key}-page-text", x + 84, cy + 84,
         "September 29, 2026\nEditor-in-Chief, MIS Quarterly\n\nDear Editor-in-Chief,\n\n"
         "We submit “…” for consideration\nin MIS Quarterly. ……………………\n……………………………………………\n\n"
         "Why MISQ ………………………………………\n……………………………………………\n\n"
         "Related work and disclosures ……\n……………………………………………", 14, MUTED)


space("delivery", 3, "Delivery", ["LaTeX", "Word", "Cover letter", "Rounds"], 2,
      "Reads delivery/paper-build.toml · build-manifest.json (cover_letter) · read only",
      ["Preview", "Artifacts", "Checks"], 0,
      delivery_content,
      ["1 Build · 1", "2 Cover letter", "3 Check", "4 Response", "+ New Run"], 1,
      {"name": "run-delivery-coverletter", "skill": "haipipe-paper-assemble",
       "prompt": "Draft or revise the Cover letter\ndivision on the RD02 Round page; the\nbuild fills the facts and runs checks.",
       "process": "Held · draft not adopted · author\nblock needs affiliation and email",
       "results": "delivery/cover-letter/\n…-cover-letter.pdf · .docx"},
      "LaTeX, Word → 1 Build · 3 Check · Cover letter → 2 Cover letter · Rounds → 4 Response\n"
      "The words live on the submission Round page (RD02); the build writes the letter; Delivery only reads it.")

for i in range(3):
    arrow(f"link{i}", X[i] + FW + 2, Y0 + 346, [[0, 0], [GAP - 4, 0]], BLUE if i == 1 else MUTED, both=i == 1)

# ---- part 3 · what changed, what each Space reads ------------------------------
SY = Y0 + FH + 90
text("change-title", 48, SY, "3 · What changes (JL 260928, 260929, 261003)", 28)
rect("change-box", 48, SY + 56, 1320, 470)
text("change-table", 72, SY + 82,
     "Before                                       Now\n"
     "\n"
     "Story › Questions and Story › Roadmap,       one tab, one tree split down the middle: Question →\n"
     "  two tabs; Task home, Discovery home           Hypothesis │ B → J → T → R\n"
     "B1–B4 (the old Block Board ids)              T1–T4: short plain questions, a folder column\n"
     "Supporting runs, one button                  Task runs (haipipe-task) · Discovery runs\n"
     "                                             (haipipe-discovery)\n"
     "Runs named no skill                          every run type and run names its skill\n"
     "rd01_web, rd02_web …, typed receipts         one fixed run per lane: run-delivery-webpage,\n"
     "                                             run-delivery-latex, run-delivery-word\n"
     "rp-sec-07, re-cite-03 …                      run-<kind>-<MMDD>-<slug>, e.g. run-section-0927-…\n"
     "Evidence cards said contract only            state from the item's Result; names like Evalue03\n"
     "No cover letter                              Delivery › Cover letter: the RD02 Round page's words,\n"
     "                                             built with the manuscript (run-delivery-coverletter)\n"
     "New: Select idea (Ideation 4) · Page check (Sections 5) · T5 (main association)\n"
     "261003: the shared shell (Part 0); Guide › Description · Method · RoadMap Draw ·\n"
     "        Related Paper; Workbench Table and papers table; /w/ link", 17, INK, mono=True)

FX = 48 + 1320 + 64
text("files-title", FX, SY, "What each Space reads", 28)
rect("files-box", FX, SY + 56, 1120, 470)
text("files-map", FX + 24, SY + 82,
     "UI tab                 reads                                   runs live in\n"
     "\n"
     "Ideation › Ideas       Story00-ideation.md · Ideas (ranked)    Story00-ideation/runs/\n"
     "Story › Spine          StoryA-….md · ### 1, 2, 4               StoryA-…/runs/\n"
     "Story › RoadMap Draw   studio/<Story stem>.excalidraw           (the canvas saves to it)\n"
     "Story › logic + work   StoryA-….md · ### 3, 5, 6, 7            StoryA-…/runs/\n"
     "Story › Related Papers StoryA-….md · #### 5.3 P rows           discoveries/…/results/<run>/paper.pdf\n"
     "                       task/ · discoveries/                    task/, discoveries/<BJTR>/runs/\n"
     "Sections › Table       StoryA-….md · ### 8.2 + each Page       each Page's runs/\n"
     "Sections › Narrative   StoryA-….md · ### 8.1                   StoryA-…/runs/\n"
     "Sections › Evidence    each Page's draft/…-evidence-items.md   each Page's runs/\n"
     "Delivery › LaTeX, Word delivery/paper-build.toml, manifest     delivery/\n"
     "Delivery › Cover letter Bc-MISQ-Round/RD02-… (Cover letter)   delivery/cover-letter/\n"
     "Delivery › Rounds      Bc-MISQ-Round/RD01-…/RD01-….md          RD01-…/runs/",
     15, BLUE, mono=True)

text("footer", 48, SY + 560, "Design drawing: illustrative states, not live data. Generated by "
     "studio/paper-workbench-design.py; edit that file, then run it.", 16, MUTED)

OUT.write_text(json.dumps({"type": "excalidraw", "version": 2, "source": "haipipe-paper-workbench-design",
                           "elements": E, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
                           "files": {}}, ensure_ascii=False, indent=2), encoding="utf-8")
print(len(E), "elements →", OUT)
