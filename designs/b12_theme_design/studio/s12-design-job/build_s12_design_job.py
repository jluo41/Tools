"""b12 s12 · Design Job: s12-design-job.excalidraw, one design Job's tab on the shared frame, its Spaces as
full screens (JL 261007: "s11, s12, s13 … for the Block level, Job level and task level"; "check s11 s12 and
s13 [of b11] … borrow their ideas").

A Job pins one goal, one method version and one inputs version, and returns N designs, each a Task (s00),
drawn for j03_<goal>_<design-method> (G01 × design method M04 m2 × inputs i2, N = 10). Its Description is just what the Job
pins: Goal · Method · Inputs (JL 261007: no Map here; the Map is the Block's, s11). Placeholders
only; written through canvas.write, so every mark a person adds survives a rebuild.

    python build_s12_design_job.py [out.excalidraw]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_build"))
import design_ui as U  # noqa: E402
U.SH = 1180                       # s12's Description views hold more than one screen-height of cards (261007)

text, base, INK, GRAY, RED, MONO = U.text, U.base, U.INK, U.GRAY, U.RED, U.MONO

MOVES = [("a Design Folder (one goal, in a method folder)", "the Job tab j03_<goal>_<design-method>: one goal × method M04 m2 × inputs i2"),
         ("Design Task Space (venue, who, rules, N)", "Description › Goal (run-setup-goal-j03)"),
         ("method folder 2-Design-M<NN>/", "Description › Method: M04's choices at the five steps (run-setup-method-j03)"),
         ("B01: 1-IN-inputs/IN0N-…/packet.md (one per method)", "Description › Inputs: the Job's own inputs/, a fence (run-setup-inputs-j03)"),
         ("Commission", "set up = the three setup Runs closed"),
         ("Design Space: one card per design", "Work Details: t00 ideas · t01 – t15 one design each · t99 review whole"),
         ("(none)", "Audience Report: Reason ideas · Design display · Review whole · Performance"),
         ("Generate: one run record", "each design Task's own run-generate-dNN, from its idea"),
         ("Delivery Space", "Delivery: the kept designs, word for word; a person releases")]

DESC = lambda on: [(lab, on == k) for k, lab in enumerate(["Goal", "Method", "Inputs"])]
JOB = "j03_<goal>_<design-method>/"
DESIGNS = [("t01 · d01", "passed", "<opening> … <ask>", "✓", "✓", 0), ("t02 · d02", "passed", "<opening> … <reason>", "✓", "✓", 0),
           ("t03 · d03", "verify", "<opening> … <ask>", "…", "…", 0), ("t04 · d04", "passed", "<opening> … <sign-off>", "✓", "✓", 1),
           ("t05 · d05", "revise", "<opening> … <ask>", "✗ r2.3", "✓", 1), ("t06 … t10", "passed 4 · verify 1", "", "", "", 0), ("t11 … t15", "dropped by t99", "", "", "", 0)]


fold = U.fold          # the shared folding card (design_ui.py), the same on the Block (s11)


SETUP = [("run-setup-goal-j03", "Goal"), ("run-setup-method-j03", "Method"), ("run-setup-inputs-j03", "Inputs")]


def setup_strip(cx, cy, here):
    """The Job's three soft setup Runs (JL 261007: "run-setup-goal-j03, run-setup-method-j03, run-setup-inputs-j03 … when the
    three runs are ready, this job is setup"); the one behind this view in bold. Returns the y below it."""
    x = cx
    for k, (run, view) in enumerate(SETUP):
        on = view == here
        w = len(run) * 9.6 + 60
        base("rectangle", x, cy, w, 32, INK if on else GRAY, 2 if on else 1, rough=0)
        text(x + 12, cy + 7, "✓ " + run, 14, INK if on else GRAY, MONO)
        x += w + 10
        if k < 2:
            text(x - 6, cy + 6, "·", 16, GRAY)
    text(x + 10, cy + 7, "→ set up ✓ 3 of 3", 14, INK)
    return cy + 46


def job_goal(cx, cy, cw):
    """The goal as the design work sees it (inputs/goal.md), in the five cards of the old Design Goal Space
    (Aim · Venue · Rules · Resources · Leave out, haipipe-design-goal); Aim open."""
    cy = U.note(cx, cy, "261007  five cards (the old Design Goal), not a thin table")
    cy = U.note(cx, cy, "261007  set up by run-setup-goal-j03 (soft): pins G01 from the Block's goal list; signed once, at the Block")
    cy = setup_strip(cx, cy, "Goal")
    y = fold(cx, cy, cw, "Aim", "G01 <goal> · for <audience> · N = 10",
             [("goal", "G01 <goal>: <the behaviour to change>"), ("who", "<audience>"), ("N", "10 designs"),
              ("signed", "✅ <date> · a person, once, in the Block's goal list (not again here)")])
    y = fold(cx, y, cw, "Venue", "sms · <n> characters · venue-sms profile ↗")
    y = fold(cx, y, cw, "Rules", "4 · r2.1 · r2.3 shared (inputs i2) · 1 for this goal only · each with its source")
    y = fold(cx, y, cw, "Resources", "what it may draw on: the Inputs view (inputs/, the fence)")
    y = fold(cx, y, cw, "Leave out", "<what>, from the Block")
    text(cx, y + 6, "one card each; a card opens to its lines, each line with its source", 14, GRAY)


# the design unit, read from its one source: s03's design_unit_drawing.py (its STEPS and METHODS), so the Method
# view shows a registered method's real choices at each of the five steps (JL 261007: "see input, reasoning ideas,
# conduct process, review item, review whole … add it back")
UNIT = HERE.parent / "s03-design-methods" / "design_unit_drawing.py"


def unit():
    src = UNIT.read_text(encoding="utf-8")
    ns = {}
    exec(src[src.index("IN, ID, PR, CK, OV"):src.index("# layout")], ns)
    return ns["STEPS"], ns["METHODS"]


STEPS, METHODS = unit()
METHOD = next(m for m in METHODS if m[0].startswith("M04"))      # the method this Job pins
CHANGED = {1: "Δ m2: spread · distinct in principle", 4: "Δ m2: keeps the top N of N + 5"}


def job_method(cx, cy, cw):
    """The pinned method: one card per step of the design unit, its choices; ② open, with each part."""
    name, sub, _, picks, explain = METHOD
    cy = U.note(cx, cy, "261007  M04's choices at the design unit's five steps (s03), as cards; was 5 made-up parts")
    cy = U.note(cx, cy, "261007  set up by run-setup-method-j03 (soft): links the registered method's card into inputs/method.md")
    cy = U.note(cx, cy, "261007  no methods Block (JL): a method is a card in the design skill's registry, generic, versioned there")
    cy = setup_strip(cx, cy, "Method")
    text(cx, cy, f"{name} · {sub} · m2 · inputs/method.md -> …/haipipe-design-unit/methods/M04-….md · <sha>", 15, INK)
    step = {p: si for si, st in enumerate(STEPS) for p, _ in st[4]}
    y = cy + 36
    for si, st in enumerate(STEPS):
        mine = [(p, o) for p, o in picks if step.get(p) == si]
        if si == 0:
            mine = [("Goal", "always: inputs/goal.md")] + mine
        line = " · ".join(o for _, o in mine) or "nothing chosen"
        line = line if len(line) < 70 else line[:68] + " …"
        delta = CHANGED.get(si, "")
        if si == 3:
            y = U.note(cx, y, "261007  ④ ⑤ renamed: Review item · Review whole (were Check output · Check overall)")
        y = fold(cx, y, cw, st[0], line + (f"   {delta}" if delta else ""),
                 None)
    y = U.note(cx, y, "261007  the method names who runs it: a skill and an agent per step")
    y = fold(cx, y, cw, "Runs it", "skill haipipe-design-unit reads inputs/method.md · ①②③ designer agent · ④⑤ another agent",
             [("① ② ③", "haipipe-designer-agent, loading haipipe-design-unit"),
              ("④ Review item", "? a reviewer agent, never the one that generated (haipipe-design-reviewer-agent, proposed)"),
              ("⑤ Review whole", "the same reviewer, on the N together"),
              ("extra skills", "only if a step's choice needs them: M05 calls haipipe-insight (it analyses raw data)")])
    y = U.note(cx, y, "261007  a method may loop (JL): its card says how many rounds, and step ① reads the last output")
    y = fold(cx, y, cw, "Loops", "M04: one pass · only the Revise loop, inside each design Task (verify → revise → verify)")
    text(cx, y + 6, "\n".join(U.wrap(explain, 120)), 14, GRAY)
    U.chip(cx, y + 50, "type: card By insight ↗", 230)
    U.chip(cx + 250, y + 50, "the unit: s03 design-unit-methods ↗", 300)


# what each part of step ① puts into the Job's inputs/: a file card (name, its line, red = left out) or a plain line
INPUT_FILES = {
    "Goal · how much is set": [("goal.md", "aim · N · leave out: written by run-setup-inputs-j03", False),
                               ("rules.md", "-> ../../inputs/i2/rules.md · <sha>", False)],
    "Goal · for whom": ["in goal.md: who = <audience>"],
    "Information · whose": ["ours: the insight Block's signed handoff (its file under form)"],
    "Information · form": [("handoff-W-03.md", "-> …/insights/…/W-03.md · cited by d01 d02 d04", False),
                           ("venue-sms.md", "-> …/venue-sms/ · the delivery setting", False),
                           ("theory/", "a theory or rule: not picked, left out", False)],
    "Examples": ["nothing: no past designs given"],
    "Tools": ["nothing: no code, no search"],
    "Reading": ["read whole, no summary first"],
    "From the last unit": ["nothing: j02's designs are not given (only the method moved)"],
}


def job_inputs(cx, cy, cw):
    """The Job's own inputs/: the only thing the design work may see (JL 261007: "for this design job, it will
    only see the content in this inputs/ … we can use the symlink"). One row per part of the design unit's
    step ① See input (JL 261007: "label each type of the input, like goal · how much is set, goal · for whom"):
    the part, M04's choice, and what it puts into inputs/."""
    cy = U.note(cx, cy, "261007  each input labelled by its step-① part (s03's design unit), M04's choice beside it")
    cy = U.note(cx, cy, "261007  set up by run-setup-inputs-j03 (soft), after goal + method: builds inputs/ and its manifest")
    cy = setup_strip(cx, cy, "Inputs")
    text(cx, cy, "j03_<goal>_<design-method>/inputs/  ·  the fence: Generate and Verify see these and nothing else",
         15, INK, MONO)
    picks = {}
    for part, opt in METHOD[3]:
        picks.setdefault(part, []).append(opt)
    y0 = y = cy + 40
    LX, CX, FX = cx + 10, cx + 230, cx + 480                # part · M04's choice · what lands in inputs/
    for h, x in [("① See input · part", LX), ("M04's choice", CX), ("in inputs/", FX)]:
        text(x, y, h, 13, GRAY)
    y += 24
    y = U.note(cx, y, "261007  the method itself is in inputs/ too: the design work reads how, and what")
    text(LX, y + 12, "the method (how)", 14, INK)
    U.chip(CX, y + 8, "M04 · m2", 90)
    y = fold(FX, y + 4, cw - (FX - cx), "method.md", "-> …/haipipe-design-unit/methods/M04-….md · <sha>", mono_title=True) + 2
    U.path([(cx, y), (cx + cw, y)], arrow=False, color=GRAY)
    for part, _options in STEPS[0][4]:
        top = y
        text(LX, y + 12, part, 14, INK)
        chosen = picks.get(part, [])
        if part == "Information · form" and "the delivery setting" not in chosen:
            chosen = chosen + ["shared: the delivery setting"]  # the venue: a pick every method makes (decided)
        if not chosen and part.startswith("Goal"):
            chosen = ["shared: aim + rules"]
        cyy = y + 8
        for c in chosen or ["—"]:
            U.chip(CX, cyy, c.lstrip("? "), max(80, len(c) * 7.6 + 18), red=c.startswith("?"))
            cyy += 32
        fy = y + 4
        for item in INPUT_FILES.get(part, []):
            if isinstance(item, str):
                text(FX, fy + 10, item, 14, GRAY)
                fy += 40
            else:
                name, line, red = item
                fy = fold(FX, fy, cw - (FX - cx), name, line, red=red, mono_title=True) - 4
        y = max(cyy, fy, top + 40) + 4
        U.path([(cx, y), (cx + cw, y)], arrow=False, color=GRAY)
    y = fold(cx, y + 8, cw, "manifest.yaml", "every file above, its source and sha256 · frozen when run-setup-inputs-j03 closes = i2",
             mono_title=True)
    base("rectangle", cx - 8, y0 - 8, cw + 16, y - y0 + 6, RED, 2, dashed=True, rough=0)


# Audience Report follows the design unit (JL 261007): ② Reason ideas → ③ ④ Design display → ⑤ Review whole
TOPICS = [  # reasoning topics: an input, the chain of thinking, the ideas it ends in
    ("T1 · why click at all", "W-03 row 2", ["<what the insight says>", "so: give the reason before the ask"],
     ["I01 reason-first", "I02 reason-question"]),
    ("T2 · what to ask", "rule r2.1", ["<the rule>", "so: one ask, at the end"], ["I03 ask-alone", "I04 reason-then-ask"]),
    ("T3 · who it is from", "own knowledge", ["<a known pattern>", "so: name the sender first"], ["I05 sender-first", "I06 …"])]


def chain(x, y, w, src, steps, ideas):
    """One reasoning chain, drawn left to right: the input → each step → the ideas. Returns its bottom."""
    boxes = [(src, GRAY)] + [(s, INK) for s in steps]
    bw, gap = 200, 34
    for k, (s, c) in enumerate(boxes):
        bx = x + k * (bw + gap)
        base("rectangle", bx, y, bw, 52, c, 1, rough=0)
        text(bx + 10, y + 8, "\n".join(U.wrap(s, 24)[:2]), 13, c)
        U.path([(bx + bw + 2, y + 26), (bx + bw + gap - 4, y + 26)], color=GRAY)
    ix = x + len(boxes) * (bw + gap)
    for k, idea in enumerate(ideas):
        U.chip(ix, y + k * 30, idea, min(w - (ix - x), 230))
    return y + max(60, len(ideas) * 30 + 6)


def reason_ideas(cx, cy, cw):
    """Step ② Reason ideas: from inputs/ to the ideas, as reasoning chains; one card per reasoning topic."""
    cy = U.note(cx, cy, "261007  decided: each step's from is a file in the manifest, or \"own knowledge\"; the reviewer checks it before t01 – t15 open")
    cy = U.note(cx, cy, "261007  step ② as reasoning chains, one card per topic; ends in the ideas (was the element matrix)")
    cy = U.note(cx, cy, "261007  drawn from t00 › run-reason-t00/result/chains.yaml: each step names its source in inputs/")
    text(cx, cy, "inputs/ → reasoning, topic by topic → 15 ideas (N + 5), frozen before any design is made", 15, INK)
    y = cy + 34
    for k, (topic, src, steps, ideas) in enumerate(TOPICS):
        if k == 0:                                      # the first topic open: its chain
            base("rectangle", cx, y, cw, 46 + 84, GRAY, 1, rough=0)
            text(cx + 14, y + 13, "▾", 16, GRAY)
            text(cx + 40, y + 12, topic, 17)
            text(cx + 40 + len(topic) * 9.6 + 24, y + 15, f"from {src} · 2 steps · → {len(ideas)} ideas", 14, GRAY)
            U.path([(cx, y + 46), (cx + cw, y + 46)], arrow=False, color=GRAY)
            chain(cx + 20, y + 60, cw - 40, src, steps, ideas)
            y += 46 + 84 + 10
        else:
            y = fold(cx, y, cw, topic, f"from {src} · {len(steps)} steps · → {', '.join(i.split()[0] for i in ideas)}")
    y = fold(cx, y, cw, "… T4 – T6", "3 more topics")
    y = U.note(cx, y + 4, "261007  each idea gets a short name when it is born; its design keeps it (t04_d04_reason-then-ask/)")
    text(cx, y + 2, "the ideas: I01 – I15, each with a short name, its topic and its source in inputs/; one design per idea (step ③)", 14, GRAY)


# Design display, as the earlier design workbench showed it (servers/workbench-design/design.py: _item_card): the
# design as the reader sees it (an SMS: a phone, "Text message", one bubble, {LINK} where the platform puts it; a UI:
# its rendered screen), then its process, then its review; cards in order, one open; dropped ones folded at the end
SMS = "<opening>. <the reason>. <the ask>: {LINK}"


phone = U.phone        # the shared phone and bubble (design_ui.py)


def design_display(cx, cy, cw):
    """Steps ③ ④: one card per design, in order: the design as it reads │ its process │ its review and outcome."""
    cy = U.note(cx, cy, "261007  decided: the 5 dropped designs keep their Tasks, marked dropped and folded")
    cy = U.note(cx, cy, "261007  the design as the reader sees it (a phone, one bubble), cards in order, as the old workbench")
    C1, C2 = 330, 690
    text(cx + cw - 150, cy - 2, "open all · close all", 13, U.TEAL)
    for h, x in [("Design", 0), ("Process (③): its idea, each element's source", C1),
                 ("Review (④) · expected outcome", C2)]:
        text(cx + x + 10, cy + 18, h, 13, GRAY)
    y = cy + 42
    # d01 open: the three columns
    h = 210
    base("rectangle", cx, y, cw, h, GRAY, 1, rough=0)
    for x in (C1, C2):
        U.path([(cx + x, y), (cx + x, y + h)], arrow=False, color=GRAY)
    text(cx + 12, y + 10, "▾ d01 · reason-first", 15, INK, MONO)
    phone(cx + 22, y + 38, SMS)
    for k, s in enumerate(["from idea I01 (T1 · why click at all)", "<opening> ← W-03 r2", "<the reason> ← W-03 r4",
                           "<the ask> ← rule r2.1", "③ run-generate-d01 · freestyle · one agent"]):
        text(cx + C1 + 12, y + 12 + k * 24, s, 13, GRAY if k == 0 else INK)
    for k, s in enumerate(["④ run-verify-d01-v1 · T0 ✓ · T1 ✓ · passed", "expected +x [lo, hi]", "⑤ rank #2 of 15 · kept"]):
        text(cx + C2 + 12, y + 12 + k * 24, s, 13, INK)
    y += h + 8
    # d02, d03 … closed: one line each, the message's start and where it stands
    for d, prev, where in [("d02 · reason-question", "<opening>. <the reason as a question> …", "passed · rank #5 · kept"),
                           ("d03 · ask-alone", "<opening>. <the ask> …", "verify · draft 1"),
                           ("d04 · reason-then-ask", "<opening>. <the reason>. <the ask> …", "passed (draft 2) · rank #1 · kept"),
                           ("d05 · sender-first", "<opening>. <the ask> …", "revise · ✗ T0 r2.3")]:
        base("rectangle", cx, y, cw, 38, GRAY, 1, rough=0)
        text(cx + 12, y + 10, "▸ " + d, 15, INK, MONO)
        text(cx + 300, y + 11, prev, 13, INK)
        text(cx + C2 + 12, y + 11, where, 13, RED if "✗" in where else GRAY)
        y += 44
    text(cx + 12, y + 2, "▸ d06 … d10 · 5 more, in order", 13, GRAY)
    y += 30
    base("rectangle", cx, y, cw, 38, GRAY, 1, dashed=True, rough=0)
    text(cx + 12, y + 10, "▸ Dropped by t99, kept for the record · 5   (d11 … d15)", 14, GRAY)
    text(cx, y + 52, "a UI design shows its rendered screen here (render_screen.py), its HTML one click away", 13, GRAY)


def review_whole(cx, cy, cw):
    """Step ⑤ Review whole: rank the 15, keep the top 10 (N of N + 5), each with its frozen prediction."""
    cy = U.note(cx, cy, "261007  decided: run-rank-t99 writes each predicted effect into ranking.csv; the workflow projects a draft prediction.yaml; frozen when a person releases")
    cy = U.note(cx, cy, "261007  step ⑤ ranks all 15 and keeps the top 10 (was three coverage checks)")
    y = U.table(cx, cy, cw, ["rank", "design", "predicted click-through", "why", "kept"], [0, 80, 300, 520, 900],
                [("1", "d04 reason-then-ask", "+x [lo, hi]", "the clearest reason, one ask", "✓"),
                 ("2", "d01 reason-first", "+x [lo, hi]", "<why>", "✓"),
                 ("…", "…", "…", "", "✓ 10"),
                 ("11", "d07", "+x [lo, hi]", "near-duplicate of d03", "✗"),
                 ("…", "…", "…", "", "✗ 5")], mono=(1,))
    U.pairs(cx, y + 20, [("ranked by", "predicted click-through, by a different agent (④ ⑤ reviewer)"),
                         ("keeps", "the top N of N + 5 = 10 of 15"),
                         ("also checks", "the 10 cover the goal · no two alike · every input row used")])


def observed(cx, cy, cw):
    """Predicted vs observed at the Job (JL 261007: "one in the job level Report as well"): each released design's
    frozen prediction beside what the Exp observed. observed/ and its scoring are the Block's, once per Exp (s11): this
    view reads the Block's rows for j03."""
    cy = U.note(cx, cy, "261007  the Job's own Predicted vs observed, read from the Block: observed/eNN/arms.csv + scores.csv rows for j03")
    C1, C2 = 330, 690
    for h, x in [("Design", 0), ("Predicted · frozen at release", C1), ("Observed · the Exp, its arm", C2)]:
        text(cx + x + 10, cy, h, 13, GRAY)
    y = cy + 24
    h = 170
    base("rectangle", cx, y, cw, h, GRAY, 1, rough=0)
    for x in (C1, C2):
        U.path([(cx + x, y), (cx + x, y + h)], arrow=False, color=GRAY)
    text(cx + 12, y + 10, "▾ d04 · reason-then-ask", 15, INK, MONO)
    text(cx + 20, y + 44, "\n".join(U.wrap(SMS, 34)), 13, INK)
    for k, s in enumerate(["+x [lo, hi] against the control", "run-freeze-predictions-j03 · <date>", "rank 1 of 15 (t99)"]):
        text(cx + C1 + 12, y + 12 + k * 24, s, 13, INK if k == 0 else GRAY)
    for k, s in enumerate(["+y [lo, hi] · arm B", "Block › observed/e01_<exp>/arms.csv", "direction ✓ · in range ✓"]):
        text(cx + C2 + 12, y + 12 + k * 24, s, 13, INK if k != 1 else GRAY)
    y += h + 8
    for d, pr, ob, bad in [("d01 · reason-first", "+x [lo, hi]", "✓ direction · ✗ range", True),
                           ("d02 · reason-question", "+x [lo, hi]", "not tested", False)]:
        base("rectangle", cx, y, cw, 38, GRAY, 1, rough=0)
        text(cx + 12, y + 10, "▸ " + d, 14, INK, MONO)
        text(cx + C1 + 12, y + 11, pr, 13, GRAY)
        text(cx + C2 + 12, y + 11, ob, 13, RED if bad else GRAY)
        y += 44
    U.pairs(cx, y + 10, [("scored by", "the Block's run-score-e01 (soft, once per Exp): scores.csv, the rows for j03"),
                         ("the Block", "Block › Predicted vs observed and Method scorecard sum them")])


def numbers(cx, cy, cw):
    """Each design's numbers: what it cost, how long it is, and its frozen prediction."""
    cy = U.note(cx, cy, "261007  renamed Performance (was Numbers); predictions are drafts until release")
    y = U.table(cx, cy, cw, ["design", "tokens", "time", "rounds", "length", "predicted", "frozen"],
                [0, 160, 290, 410, 520, 640, 840],
                [("d01", "<n>k", "<m> min", "1", "<n> ch · 1 seg", "+x [lo, hi] draft", "at release ⬜"),
                 ("d04", "<n>k", "<m> min", "2", "<n> ch · 2 seg", "+x [lo, hi] draft", "at release ⬜"),
                 ("d05", "<n>k", "<m> min", "2 …", "<n> ch · 1 seg", "–", "not yet"),
                 ("all 10", "<n>k", "<m> min", "1.2", "", "8 predicted", "")], mono=(0,))
    text(cx, y + 14, "a prediction is frozen when the design is released; the Job's totals feed Block › Cost (s11)", 14, GRAY)
    text(cx, y + 40, "? tokens: usage: in each Run receipt (a to-do for the Run skill) · predicted by the ④ ⑤ reviewer agent", 14, RED)


# Work Details: one view per step of the method (JL 261007: "Reason Ideas, Conduct & Review, and Review Whole"),
# each its Task(s) as folding cards; the work (Tasks and their Runs), where the Audience Report shows the results
WD = lambda on: [(v, k == on) for k, v in enumerate(["Reason Ideas", "Conduct & Review", "Review Whole"])]


def wd_reason(cx, cy, cw):
    cy = U.note(cx, cy, "261007  Work Details by step: Reason Ideas · Conduct & Review · Review Whole (were state filters)")
    y = fold(cx, cy, cw, "t00 · reason ideas", "step ② · 6 topics → I01 – I15 · closed ✅",
             [("its Run", "run-reason-t00 · hard · ok · the designer agent"),
              ("result", "chains.yaml · ideas.yaml · topics.md"),
              ("then", "run-open-designs-j03 opened t01 – t15, one per idea"),
              ("shown in", "Audience Report › Reason ideas")], mono_title=True)
    y = U.note(cx, y + 4, "261007  settled in s13: one Task tab, three kinds: t00 (its chains, its ideas) · a design · t99 (its ranking)")


DCARDS = [("t01 · d01 · reason-first", "I01 · passed · T0 ✓ T1 ✓", [("idea", "I01 reason-first · lead with the reason (T1)"),
                                                    ("run-generate-d01", "③ ok · draft 1"),
                                                    ("run-verify-d01-v1", "④ T0 ✓ · T1 ✓ · passed · another agent"),
                                                    ("design", "<opening>. <the reason>. <the ask>: {LINK}")]),
          ("t02 · d02 · reason-question", "I02 · passed · T0 ✓ T1 ✓", None), ("t03 · d03 · ask-alone", "I03 · verify · draft 1", None),
          ("t04 · d04 · reason-then-ask", "I04 · passed on draft 2 · r02 ✗ → revise → r03 ✓", None),
          ("t05 · d05 · sender-first", "I05 · revise · ✗ T0 r2.3", None)]


def wd_conduct(cx, cy, cw):
    cy = U.note(cx, cy, "261007  decided: T2 critique per design, inside ④; T3 pretest once per Job, on the 10 kept")
    cy = U.note(cx, cy, "261007  each design Task a card, in order (was a table); one Task, two Runs: generate · verify")
    x = cx
    for s in ["All 15", "passed 9", "verify 2", "revise 1", "dropped 5"]:   # the old filters, now small chips
        U.chip(x, cy, s, len(s) * 8 + 24)
        x += len(s) * 8 + 34
    y = cy + 40
    for name, line, body in DCARDS:
        y = fold(cx, y, cw, name, line, body, mono_title=True)
    text(cx + 12, y + 2, "▸ t06 … t10 · 5 more, in order", 13, GRAY)
    y += 30
    y = fold(cx, y, cw, "t11 … t15", "dropped by t99, kept for the record · 5", mono_title=True)
    text(cx, y + 4, "a card opens its Task tab (s13)", 14, GRAY)


def wd_whole(cx, cy, cw):
    y = fold(cx, cy, cw, "t99 · review whole", "step ⑤ · ranked 15 · kept 10 · 5 dropped",
             [("its Run", "run-rank-t99 · hard · ok · a different agent"),
              ("result", "ranking.csv: rank · design · predicted +x [lo, hi] · why · kept"),
              ("shown in", "Audience Report › Review whole")], mono_title=True)
    y = U.note(cx, y, "261007  a looping method adds rounds: each round is one more Run on t00 and t99, and new design Tasks")
    fold(cx, y, cw, "round 2 (a looping method, once one exists)",
         "t00 › run-reason-t00-r2 reads t99 › run-rank-t99 (① From the last unit) → t16 – t30 → t99 › run-rank-t99-r2")


def studio(cx, cy, cw):
    text(cx, cy, "optional: a drawing about this Job", 15, GRAY)
    base("rectangle", cx, cy + 34, cw, 46, GRAY, 1, rough=0)
    text(cx + 14, cy + 46, "▸ s01-<element ideas>", 17, INK, MONO)


# Runs: the same steps as Work Details, plus Setup for the Job's own soft Runs (JL 261007); hard or soft is a column.
# The Job's own runs/ holds only soft Runs; every hard Run sits in a Task.
RV = lambda on: [(v, k == on) for k, v in enumerate(["Setup", "Reason Ideas", "Conduct & Review", "Review Whole"])]
RCOLS, RHEAD = [0, 470, 570, 760], ["Run", "kind", "by", "state"]


def runs_setup(cx, cy, cw):
    cy = U.note(cx, cy, "261007  Runs by step, as Work Details (were All · hard · soft); kind is a column")
    cy = U.note(cx, cy, "261007  decided: run-open-designs-j03 (the Job's) opens t01 – t15; t00 only writes ideas.yaml")
    cy = U.note(cx, cy, "261007  the Job's own runs/ are soft only: the three setup Runs replace Commission")
    U.table(cx, cy, cw, RHEAD, RCOLS,
            [("runs/run-setup-goal-j03/", "soft", "designer agent", "closed ✅ · pinned"),
             ("runs/run-setup-method-j03/", "soft", "designer agent", "closed ✅"),
             ("runs/run-setup-inputs-j03/", "soft", "designer agent", "closed ✅ → set up"),
             ("runs/run-open-designs-j03/", "soft", "designer agent", "opened t01 – t15")], mono=(0,))


def runs_reason(cx, cy, cw):
    U.table(cx, cy, cw, RHEAD, RCOLS,
            [("t00_reason-ideas/runs/run-reason-t00/", "hard", "designer agent", "ok · I01 – I15")], mono=(0,))


def runs_conduct(cx, cy, cw):
    U.table(cx, cy, cw, RHEAD, RCOLS,
            ["t01 · d01", ("t01_d01_<slug>/runs/run-generate-d01/", "hard", "designer agent", "ok · draft 1"),
             ("t01_d01_<slug>/runs/run-verify-d01-v1/", "hard", "another agent", "passed"),
             "t04 · d04", ("t04_d04_<slug>/runs/run-generate-d04/", "hard", "designer agent", "ok · draft 1"),
             ("t04_d04_<slug>/runs/run-verify-d04-v1/", "hard", "another agent", "✗ T0 r2.3"),
             ("t04_d04_<slug>/runs/run-revise-d04/", "soft", "designer agent", "closed · draft 2"),
             ("t04_d04_<slug>/runs/run-verify-d04-v2/", "hard", "another agent", "passed"),
             "… t02 – t15, the same two Runs each"], mono=(0,))


def runs_whole(cx, cy, cw):
    U.table(cx, cy, cw, RHEAD, RCOLS,
            [("t99_review-whole/runs/run-rank-t99/", "hard", "another agent", "ok · kept 10"),
             ("runs/run-freeze-predictions-j03/", "soft", "a person ✍", "at release ⬜"),
             ("runs/run-release-j03/", "soft", "a person ✍", "⬜")], mono=(0,))


# Delivery: two files from one source (JL 261007: "a json file and also a markdown file"), written by run-release-j03
# from the kept designs' Tasks; designs.md is written from designs.json, so the two never disagree. A UI design adds
# its screens (the HTML and its rendered picture), which both files point to.
DV = lambda on: [(v, k == on) for k, v in enumerate(["designs.md", "designs.json"])]
JSON = """{
  "job": "j03_<goal>_<design-method>",
  "pins": {"goal": "G01", "method": "M04 m2", "inputs": "i2", "sha": "<sha>"},
  "released": {"by": "<person>", "at": "<date>"},
  "designs": [
    {"id": "d04", "name": "reason-then-ask", "rank": 1, "venue": "sms",
     "text": "<opening>. <the reason>. <the ask>: {LINK}",
     "idea": "I04", "sources": ["W-03 r2", "rule r2.1"],
     "predicted": {"ctr": "+x", "lo": "<lo>", "hi": "<hi>"}},
    {"id": "d07", "name": "<short-name>", "rank": 3, "venue": "ui-card",
     "screen": {"html": "screens/d07.html", "png": "screens/d07.png"}, …},
    …
  ]
}"""


def delivery_md(cx, cy, cw):
    """designs.md, as a person reads it: a table, top to bottom, the kept designs in rank order, each as it reads."""
    cy = U.note(cx, cy, "261007  two files, one source: designs.json (machines) · designs.md (people), both from run-release-j03")
    cy = U.note(cx, cy, "261007  designs.md reads top to bottom: one row per design, in rank order (was side by side)")
    cy = U.note(cx, cy, "261007  an SMS is just its text: one plain row per design (was a phone per row)")
    text(cx, cy, "delivery/designs.md · 10 kept designs, rank order · released ⬜ (a person, in run-release-j03)", 15, INK, MONO)
    y = U.table(cx, cy + 30, cw, ["rank", "name", "the design: its text (a UI: its screen files)", "idea", "predicted"],
                [0, 60, 290, 820, 930],
                [("1", "d04 reason-then-ask", "<opening>. <the reason>. <the ask>: {LINK}", "I04 · T2", "+x [lo, hi]"),
                 ("2", "d01 reason-first", "<opening>. <the reason>. <the ask>: {LINK}", "I01 · T1", "+x [lo, hi]"),
                 ("3", "d07 <short-name>", "ui-card: screens/d07.html · d07.png", "I07 · T3", "+x [lo, hi]"),
                 ("…", "", "4 – 10, in rank order", "", "")], mono=(1,), h=38)
    text(cx, y + 12, "the sources of each element stay in the design's Task (elements.yaml); the file stays short", 13, GRAY)


def delivery_json(cx, cy, cw):
    """designs.json, as a machine reads it: the experiment platform, or a UI that renders the designs."""
    text(cx, cy, "delivery/designs.json · what the experiment platform reads", 15, INK, MONO)
    box_h = len(JSON.splitlines()) * 25 + 30
    base("rectangle", cx, cy + 30, cw, box_h, GRAY, 1, rough=0)
    text(cx + 14, cy + 42, JSON, 13, INK, MONO)
    U.pairs(cx, cy + 50 + box_h, [("an SMS", "its text, {LINK} where the platform puts the link"),
                                  ("a UI", "its screen: the HTML (the source) and the PNG (rendered by render_screen.py)"),
                                  ("one source", "designs.md is written from this file; neither is edited by hand")])


# "on disk" under each screen: a tree from the design Block's folder down to what that screen reads (JL 261007:
# "it should start from the block folder level")
B, J = "bNN_<app>/", "j03_<goal>_<design-method>/"
DISK = {
    "Goal": [(B, "the design Block"), ("└── " + J, "this Job"),
             ("    ├── j03_<goal>_<design-method>.md", "## Goal · N · pins: G01 (signed at the Block) · M04 m2 · i2"),
             ("    ├── runs/run-setup-goal-j03/run.yaml", "soft: pins G01, already signed"),
             ("    └── inputs/", "the fence"),
             ("        ├── goal.md", "the goal as the design work sees it"),
             ("        └── venue-sms.md -> …/venue-sms/", "the venue profile (skills/…/venue/), inside the fence")],
    "Method": [(B, "the design Block"), ("└── " + J, ""),
               ("    ├── j03_<goal>_<design-method>.md", "pins: M04 m2 · <sha>"),
               ("    ├── runs/run-setup-method-j03/run.yaml", "soft: picks M04, links its card"),
               ("    └── inputs/method.md -> …/methods/M04-….md", "the method, inside the fence"),
               ("haipipe-design-unit/methods/", "? the registry, in the design skill (generic)"),
               ("├── M04-actionable-insights.md", "its five steps' choices · its runner"),
               ("└── M01 … M05 …", "the registered methods, each with its type")],
    "Inputs": [(B, "the design Block"), ("├── inputs/i2/", "the Block's inputs version"),
               ("│   ├── rules.md", ""), ("│   └── theory/", ""),
               ("└── " + J, ""), ("    ├── runs/run-setup-inputs-j03/run.yaml", "soft: builds inputs/, freezes the manifest"),
               ("    └── inputs/", "the fence: the only folder the design work sees"),
               ("        ├── method.md -> …/methods/M04-….md", "linked by run-setup-method-j03"),
               ("        ├── goal.md · venue-sms.md", "written / linked by run-setup-inputs-j03"),
               ("        ├── rules.md -> ../../inputs/i2/rules.md", "relative symlink"),
               ("        ├── handoff-W-03.md -> …/W-03.md", "-> ../../../../insights/bNN_<topic>/delivery/W-03.md"),
               ("        └── manifest.yaml", "each file, its source, its sha256; frozen")],
    "Reason ideas": [(B, ""), ("└── " + J, ""), ("    └── t00_reason-ideas/", "the Task of step ②"),
                     ("        └── runs/run-reason-t00/result/", "hard"),
                     ("            ├── chains.yaml", "each topic: its steps (from · says · so) → its ideas"),
                     ("            ├── ideas.yaml", "I01 – I15: the idea, its topic, the step it came from"),
                     ("            ├── topics.md", "the readable report, written from chains.yaml"),
                     ("            └── transcript.yaml", "a pointer + size; the text in ProjectResult"),
                     ("✎ 261007  the reasoning is recorded step by step (chains.yaml), so the UI can draw it", "")],
    "Design display": [(B, ""), ("└── " + J, ""), ("    └── tNN_d<NN>_<slug>/", "one card: the Task of one design"),
                       ("        ├── tNN_d<NN>_<slug>.md · elements.yaml", "the design · its process"),
                       ("        ├── runs/run-generate-d<NN>/ (③)", "one design from its idea"),
                       ("        ├── runs/run-verify-d<NN>-v1/ (④)", "its review"),
                       ("        └── prediction.yaml", "its expected outcome")],
    "Review whole": [(B, ""), ("└── " + J, ""), ("    └── t99_review-whole/", "the Task of step ⑤"),
                     ("        └── runs/run-rank-t99/result/ranking.csv", "hard: rank the 15, keep 10")],
    "Observed": [(B, "the design Block"),
                 ("├── observed/e01_<exp>/", "once per Exp, the Block's (s11)"),
                 ("│   ├── arms.csv", "arm · jNN · dNN · n · totals: the rows for j03"),
                 ("│   └── source.md · manifest.yaml", "the signed insight handoff, frozen"),
                 ("├── runs/run-score-e01/scores.csv", "soft, the Block's: the rows for j03"),
                 ("└── " + J + "delivery/designs.json", "predicted: frozen at release")],
    "Performance": [(B, ""), ("└── " + J, ""), ("    ├── runs/*/run.yaml", "started_at · finished_at · ? usage"),
                ("    └── tNN_d<NN>_<slug>/", ""), ("        ├── prediction.yaml", "frozen at release: +x [lo, hi], by whom"),
                ("        └── runs/*/run.yaml", "each verify and revise")],
    "WD Reason": [(B, ""), ("└── " + J, ""), ("    └── t00_reason-ideas/", "step ②: the ideas"),
                  ("        ├── t00_reason-ideas.md", "state · ## Topics"),
                  ("        └── runs/run-reason-t00/result/", "chains.yaml · ideas.yaml · topics.md")],
    "WD Conduct": [(B, ""), ("└── " + J, ""), ("    └── t01_d01_<slug>/ … t15_d15_<slug>/", "steps ③ ④: one design each; <slug> = its short name"),
                   ("        ├── tNN_d<NN>_<slug>.md · elements.yaml", "state · ## Design · its elements"),
                   ("        └── runs/run-generate-d<NN>/ · run-verify-d<NN>-v1/", "③ · ④ (+ run-revise, run-verify v2)")],
    "WD Whole": [(B, ""), ("└── " + J, ""), ("    └── t99_review-whole/", "step ⑤: the ranking, the kept 10"),
                 ("        ├── t99_review-whole.md", "state · ## Ranking"),
                 ("        └── runs/run-rank-t99/result/ranking.csv", "")],
    "Idea Studio": [(B, ""), ("└── " + J, ""), ("    └── studio/sNN-<topic>/", "optional: a drawing and its builder")],
    "Runs Setup": [(B, ""), ("└── " + J, ""), ("    └── runs/", "the Job's own: soft only"),
                   ("        ├── run-setup-goal-j03/ · run-setup-method-j03/", "the two pins"),
                   ("        ├── run-setup-inputs-j03/", "inputs/ + manifest; then set up"),
                   ("        └── run-open-designs-j03/", "opens t01 – t15 from the ideas")],
    "Runs Reason": [(B, ""), ("└── " + J, ""), ("    └── t00_reason-ideas/runs/run-reason-t00/", "hard: step ②")],
    "Runs Conduct": [(B, ""), ("└── " + J, ""), ("    └── tNN_d<NN>_<slug>/runs/", "steps ③ ④"),
                     ("        ├── run-generate-d<NN>/ · run-verify-d<NN>-v1/", "hard"),
                     ("        └── run-revise-d<NN>/ → run-verify-d<NN>-v2/", "soft, then hard")],
    "Runs Whole": [(B, ""), ("└── " + J, ""), ("    ├── t99_review-whole/runs/run-rank-t99/", "hard: step ⑤"),
                   ("    └── runs/run-freeze-predictions-j03/ · run-release-j03/", "soft: a person signs")],
    "Delivery": [(B, ""), ("├── delivery/", "the Block's: released designs, every Job"),
                 ("└── " + J, ""), ("    ├── runs/run-release-j03/", "soft: a person releases; writes delivery/"),
                 ("    └── delivery/", "the kept designs, from t99's ranking"),
                 ("        ├── designs.json", "for machines: one entry per design, its pins"),
                 ("        ├── designs.md", "for people: written from designs.json"),
                 ("        └── screens/dNN.html · dNN.png", "UI designs only: the source and its picture")],
}
TREE_NOTE = ("✎ 261007  a tree from the Block folder (was loose paths)", "")
DISK = {k: v + [TREE_NOTE] for k, v in DISK.items()}
AR = lambda on: [(v, k == on) for k, v in enumerate(["Reason ideas", "Design display", "Review whole",
                                                     "Predicted vs observed", "Performance"])]

SCREENS = [
    ("Description", DESC(0), ["run-setup-goal-j03", "run-close-j03"], "set up: 3 of 3 ✓", job_goal, DISK["Goal"]),
    ("Description", DESC(1), ["run-setup-method-j03"], "set up: 3 of 3 ✓", job_method, DISK["Method"]),
    ("Description", DESC(2), ["run-setup-inputs-j03"], "set up: 3 of 3 ✓", job_inputs, DISK["Inputs"]),
    ("Audience Report", AR(0), ["run-reason-t00"], "", reason_ideas, DISK["Reason ideas"]),
    ("Audience Report", AR(1), ["run-generate-dNN", "run-verify-dNN-v1"], "", design_display, DISK["Design display"]),
    ("Audience Report", AR(2), ["run-rank-t99"], "", review_whole, DISK["Review whole"]),
    ("Audience Report", AR(3), ["run-freeze-predictions-j03"], "", observed, DISK["Observed"]),
    ("Audience Report", AR(4), ["run-freeze-predictions-j03"], "", numbers, DISK["Performance"]),
    ("Work Details", WD(0), ["run-reason-t00", "run-open-designs-j03"], "", wd_reason, DISK["WD Reason"]),
    ("Work Details", WD(1), ["run-generate-dNN", "run-verify-dNN-v1", "run-revise-dNN"], "", wd_conduct, DISK["WD Conduct"]),
    ("Work Details", WD(2), ["run-rank-t99"], "", wd_whole, DISK["WD Whole"]),
    ("Idea Studio", None, ["run-draw-s01"], "", studio, DISK["Idea Studio"]),
    ("Runs", RV(0), ["run-setup-goal-j03", "run-setup-method-j03", "run-setup-inputs-j03", "run-open-designs-j03"], "",
     runs_setup, DISK["Runs Setup"]),
    ("Runs", RV(1), ["run-reason-t00"], "", runs_reason, DISK["Runs Reason"]),
    ("Runs", RV(2), ["run-generate-dNN", "run-verify-dNN-v1", "run-revise-dNN"], "", runs_conduct, DISK["Runs Conduct"]),
    ("Runs", RV(3), ["run-rank-t99", "run-freeze-predictions-j03", "run-release-j03"], "", runs_whole, DISK["Runs Whole"]),
    ("Delivery", DV(0), ["run-release-j03"], "", delivery_md, DISK["Delivery"]),
    ("Delivery", DV(1), ["run-release-j03"], "", delivery_json, DISK["Delivery"]),
]

# "skills" to the right of each on-disk tree (JL 261007: "in the right we will have skills … from the block level
# of the skill folder"): the skills that screen's Runs load, from skills/; "?" = proposed, not there yet
D = "skills/2_theme/design/"
UNIT = [(D, "the design theme's skills"), ("├── haipipe-design-unit/", "one unit: steps ② – ⑤"),
        ("│   ├── SKILL.md", "reads inputs/method.md"), ("│   └── ? methods/M04-….md", "? the registry")]
UNIT2 = UNIT[:2]


def agents(designer=True, reviewer=False, last="└──"):
    """The agents, inside the tree: haipipe-design/agents/ (the reviewer is proposed)."""
    rows = [(last + " haipipe-design/agents/", "")]
    pre = "    " if last == "└──" else "│   "
    kids = ([("haipipe-designer-agent.md", "runs the step")] if designer else []) + \
           ([("? …-reviewer-agent.md", "? ④ ⑤: check · rank · predict")] if reviewer else [])
    for k, (name, what) in enumerate(kids):
        rows.append((pre + ("└── " if k == len(kids) - 1 else "├── ") + name, what))
    return rows


SK = {
    ("Description", "Goal"): [(D, ""), ("├── haipipe-design-goal/", "the goal, signed at the Block"),
                              ("├── haipipe-design/", "run-setup-goal-j03: pins it"),
                              ("└── venue/venue-sms/", "the venue profile, linked in")],
    ("Description", "Method"): [(D, ""), ("├── haipipe-design/", "run-setup-method-j03: pins M04"),
                                ("└── haipipe-design-unit/", "the method it runs"),
                                ("    └── ? methods/M04-….md", "? linked into inputs/method.md")],
    ("Description", "Inputs"): [(D, ""), ("├── haipipe-design/", "run-setup-inputs-j03: inputs/"),
                                ("├── haipipe-design-unit/", "step ① says what goes in"),
                                ("└── venue/venue-sms/", "linked in as venue-sms.md")],
    ("Audience Report", "Reason ideas"): UNIT + agents(),
    ("Audience Report", "Design display"): [(D, ""), ("├── haipipe-design-unit/", "③ generate · ④ verify"),
                                            ("│   └── scripts/check_unit.py", "T0: the rules"),
                                            ("│       render_screen.py", "a UI design's picture")]
                                           + agents(reviewer=True),
    ("Audience Report", "Review whole"): UNIT2 + agents(designer=False, reviewer=True),
    ("Audience Report", "Predicted vs observed"): [(D, ""), ("└── ? haipipe-design-delivery/", "? run-freeze-predictions-j03"),
                                                   ("    (the Block's run-score-e01)", "scores.csv, rows for j03")],
    ("Audience Report", "Performance"): [("skills/1_base/project/", ""), ("└── haipipe-run/", "the Run receipt"),
                                         ("    └── ? usage:", "? tokens per Run: a to-do")],
    ("Work Details", "Reason Ideas"): UNIT2 + [("├── haipipe-design/", "run-open-designs-j03")] + agents(),
    ("Work Details", "Conduct & Review"): UNIT2 + agents(reviewer=True),
    ("Work Details", "Review Whole"): UNIT2 + agents(designer=False, reviewer=True),
    ("Idea Studio", ""): [("skills/1_base/display/", ""), ("└── excalidraw-report/", "run-draw-s01: a drawing")],
    ("Runs", "Setup"): [(D, ""), ("├── haipipe-design/", "setup method · inputs · open"),
                        ("└── haipipe-design-goal/", "setup goal (pins it)"),
                        ("skills/1_base/project/haipipe-run/", "every Run's folder + receipt")],
    ("Runs", "Reason Ideas"): UNIT2 + agents(),
    ("Runs", "Conduct & Review"): UNIT2 + agents(reviewer=True),
    ("Runs", "Review Whole"): UNIT2 + [("├── ? haipipe-design-delivery/", "? freeze · release")] + agents(designer=False, reviewer=True),
    ("Delivery", "designs.md"): [(D, ""), ("├── ? haipipe-design-delivery/", "? run-release-j03: writes both"),
                                 ("│   └── ? ref/designs-schema.md", "? designs.json's shape"),
                                 ("└── haipipe-design-unit/scripts/", "render_screen.py: screens/"),
                                 ("✎ 261007  its own delivery skill (JL)", "")],
    ("Delivery", "designs.json"): [(D, ""), ("└── ? haipipe-design-delivery/", "? owns the schema"),
                                   ("    └── ? ref/designs-schema.md", "? one entry per design")],
}
SK = {k: v + [("✎ 261007  skills: what this screen's Runs load, from skills/", "")] for k, v in SK.items()}


def _with_skills(sc):
    view = next((lab.lstrip("? ") for lab, on in sc[1] or [] if on), "")
    return sc + (SK.get((sc[0], view), []),)


SCREENS = [_with_skills(sc) for sc in SCREENS]

POPOUTS = [U.card_window("By insight"),
           ("d04 · one design  ·  its Task (s13)", [("Design", INK), ("  <opening> <reason> <ask> <sign-off>", GRAY),
                                                   ("Rationale", INK), ("  each element → its row in W-03, its rule", GRAY),
                                                   ("Evaluation", INK), ("  T0 ✓ · T1 ✓ · passed", GRAY)])]

QUESTIONS = [  # under the screen each is about: "✎" = decided (green, with its reason), "?" = still open or to create
    ("Delivery", "designs.json", "✎ decided: haipipe-design-delivery owns the schema: one owner for the one file another system reads; "
                                 "a platform with its own shape gets an adapter"),
    ("Delivery", "designs.md", "✎ decided (s11): the Block's delivery/ is one designs.json · designs.md across every Job, "
                               "written by each run-release-jNN, plus screens/"),
    ("Delivery", "designs.md", "? to create in the code pass: haipipe-design-delivery (the release, the schema, the screens)"),
    ("Runs", "Conduct & Review", "✎ 261007 decided: every Run is run-<type>-<target>, hard ones too (JL: unify the name to be "
                                 "run-xxx-xxx); was rNN_<type>_<target>"),
    ("Runs", "Setup", "✎ decided: re-running run-setup-goal or run-setup-method reopens run-setup-inputs, since step ① reads both; "
                      "its manifest is rebuilt"),
    ("Description", "Method", "✎ decided: the registry is haipipe-design-unit/methods/, generic and versioned with the skill; "
                              "the Guide reads it (to create in the code pass)"),
    ("Description", "Method", "? to create: haipipe-design-reviewer-agent; decided (s13) that ④ ⑤ are always a separate reviewer agent"),
    ("Work Details", "Review Whole", "✎ decided: a looping method's rounds stay inside the Job: one goal, method and inputs, so one clock; "
                                     "each round adds a Run on t00 and t99"),
    ("Work Details", "Review Whole", "✎ decided: in round 2 the earlier results are linked into inputs/round-2/ and added to the manifest, "
                                     "so the design work still sees only inputs/"),
    ("Audience Report", "Reason ideas", "✎ decided: chains.yaml is the record; the raw transcript goes to ProjectResult and result/ keeps "
                                        "its pointer and size (a Result stays light)"),
    ("Work Details", "Conduct & Review", "✎ decided (s13): a design keeps its short name through a revise; the name is the idea's, "
                                         "and a new idea is a new Task"),
    ("Description", "Inputs", "✎ decided: relative symlinks + sha256 in the manifest: light, and the hash catches any drift"),
    ("Description", "Inputs", "✎ decided: a changed target blocks Generate; before any design, rerun run-setup-inputs; after, "
                              "the inputs moved, so it is a new Job (one clock)"),
    ("Description", "Inputs", "✎ decided: data outside the SPACE is named by its variable ($RESULT_STORE/…) with its sha256, "
                              "never linked (AGENTS rule 10)"),
    ("Description", "Inputs", "✎ decided: the goal (aim + rules) and the venue are picks every method makes, shared, not M04's own"),
    ("Description", "Inputs", "✎ decided: Generate's ticket may read inputs/ only; Verify (T1) checks every cited source is in the manifest"),
]

ASIDES = {"Idea Studio": ("typical topics, jNN_…/studio/sNN-<topic>/", [
    ("s01-<element ideas>", "the options for each element before Generate"),
    ("s02-<what moved>", "this Job against the last: what changed, and why"),
    ("s03-<a near pair>", "two designs too alike: which to keep")])}


CHANGES = ["261007  every Run named run-<type>-<target>, hard ones too: run-reason-t00 · run-generate-dNN · run-verify-dNN-v1/-v2 · run-rank-t99; a looping round adds -r2 (JL: unify the name; was rNN_<type>_<target>)",
           "261007  own judgement (JL): the open questions are decided in green, each with its reason; red only for what is still to create",
           "261007  a delivery skill of its own (proposed): haipipe-design-delivery writes designs.json · .md · screens/ and freezes predictions",
           "261007  the Job gets Predicted vs observed, read from the Block's observed/eNN and run-score-eNN (one Exp spans Jobs)",
           "261007  a goal is signed once, in the Block's goal list; run-setup-goal-j03 only pins it (agreed with s11)",
           "261007  every design has a short name, born with its idea (I04 reason-then-ask) and used everywhere: folder, cards, delivery",
           "261007  Delivery: designs.json (machines) + designs.md (people) from one source; UI designs add screens/",
           "261007  Runs by step: Setup · Reason Ideas · Conduct & Review · Review Whole; hard or soft is a column",
           "261007  Work Details by step: Reason Ideas · Conduct & Review · Review Whole; every Task a card",
           "261007  Audience Report: no vs last Job (Jobs compare on the Block: Method scorecard, or two Jobs in a Map cell); Numbers renamed Performance",
           "261007  a method may loop (JL): rounds are more Runs on t00 and t99, plus new design Tasks (red, proposed)",
           "261007  decided (JL): a design and its review are one Task, two Runs; a new object is a new Task, another step a new Run",
           "261007  Work Details: t00 reason ideas · t01 – t15 one design each · t99 review whole; no Job-level generate",
           "261007  Audience Report follows the unit: Reason ideas (②) · Design display (③ ④) · Review whole (⑤)",
           "261007  no methods Block: a method is a registered card in the design skill, linked into inputs/method.md",
           "261007  setup lives in runs/ (run-setup-goal-j03 · -method · -inputs), no setup/ folder",
           "261007  soft Runs carry their target (run-setup-goal-j03 …); hard Runs showed as rNN_ (superseded: run-<type>-<target>); predictions frozen by the Job only",
           "261007  every Runs panel entry is a folding card named run-<type>-<target>",
           "261007  three soft setup Runs: run-setup-goal-j03 · run-setup-method-j03 · run-setup-inputs-j03; set up = all three closed",
           "261007  the Job folder is jNN_<goal>_<design-method> (was jNN_<goal>_by-<method>)",
           "261007  Description is Goal · Method · Inputs: no Map (the Block's, s11)",
           "261007  each open question sits under the screen it is about"]


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s12-design-job.excalidraw"
    U.level_drawing(out, Path(__file__).name, "Job",
                    "Job level: one goal × one method version × one inputs version → N designs (j03_<goal>_<design-method>)",
                    "A Job pins goal G01, method M04 (type by-insight, a card in the design skill) and inputs i2; its Tasks are the 10 designs.",
                    MOVES, SCREENS, POPOUTS, QUESTIONS, ASIDES, CHANGES)


if __name__ == "__main__":
    main()
