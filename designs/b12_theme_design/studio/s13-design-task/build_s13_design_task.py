"""b12 s13 · Design Task: s13-design-task.excalidraw, the Task tab on the shared frame, its Spaces as full screens
(JL 261007: "s11, s12, s13 … for the Block level, Job level and task level"; "check s11 s12 and s13 [of b11] …
borrow their ideas").

Each step of the method is a Task (s12, decided JL 261007), so a Job holds three kinds of Task: t00_reason-ideas
(② Reason ideas, one per Job), t01_d01_<name> … t15_d15_<name> (③ ④, one design each: generate and verify are
two Runs of one Task) and t99_review-whole (⑤ Review whole, one per Job: rank the 15, keep 10). The Task tab is one
frame with the same six Spaces for all three; what each Space shows follows the Task's run types, since a view
reads a run type's Result. Drawn side by side, a column per kind, in method order: t00, d04 (reason-then-ask), t99. The design band's Description › Design is the Job's design card
(s12's Design display), opened. Every source is a file in the Job's inputs/ fence (its manifest); step ④'s checks
come from the registered method linked at inputs/method.md; a prediction is frozen when a person releases the
design. Placeholders only; written through canvas.write, so every mark a person adds survives a rebuild.

    python build_s13_design_task.py [out.excalidraw]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_build"))
import design_ui as U  # noqa: E402

text, base, INK, GRAY, RED, MONO = U.text, U.base, U.INK, U.GRAY, U.RED, U.MONO

MOVES = [("a card in the Design Space (a design only)", "the Task tab by step: t00 reason ideas ② · tNN one design ③ ④ · t99 review whole ⑤"),
         ("Design · Rationale · Evaluation (on the card)", "design Task › Description: Design (the Job's card, opened) · Evaluation"),
         ("Design Item register, one row", "design Task › Work Details: Elements: words · from · source · because · step · changed (the Rationale)"),
         ("a Verify run record", "design Task › Audience Report: Tests (T0 – T3) · Drafts · Performance"),
         ("Generate: one run record", "design Task › Runs: run-generate (③) · run-verify v1 (④, another agent) · revise · run-verify v2"),
         ("(none)", "t00 › Audience Report: Topics (the reasoning chains) · Ideas (I01 – I15, each with its design)"),
         ("(none)", "t99 › Audience Report: Ranking (rank the 15, keep 10) · Coverage"),
         ("Delivery Space", "design Task › Delivery: released with the Job's Release (a person); the prediction freezes then"),
         ("(none)", "Idea Studio at every Task: optional drawings about that Task, studio/sNN-<topic>/ (as the Job's)")]

JOB = "j03_<goal>_<design-method>/"
B, J = "bNN_<app>/", JOB                              # each "on disk" is a tree from the Block folder (as s12)
TREE_NOTE = ("✎ 261007  a tree from the Block folder (was loose paths)", "")


# ── Idea Studio, at every kind of Task: optional drawings about that Task, as the Job's (s12) ─────────────
def studio_for(task, topics):
    """An Idea Studio screen body: the Task's drawings, each studio/sNN-<topic>/ with its builder; the first open."""
    def body(cx, cy, cw):
        cy = U.note(cx, cy, "261007  restored: an Idea Studio at every Task (it had been dropped); optional, as the Job's")
        text(cx, cy, f"optional: drawings about this Task ({task}), each a folder with its builder", 15, GRAY)
        y = cy + 34
        for k, (name, what) in enumerate(topics):
            if k == 0:                                # the first drawing open: its picture
                base("rectangle", cx, y, cw, 230, GRAY, 1, rough=0)
                text(cx + 14, y + 13, "▾", 16, GRAY)
                text(cx + 40, y + 12, name, 17, INK, MONO)
                text(cx + 40 + len(name) * 10.4 + 24, y + 15, what, 14, GRAY)
                base("rectangle", cx + 40, y + 56, cw - 80, 150, GRAY, 1, dashed=True, rough=0)
                text(cx + 60, y + 120, "[ the drawing, embedded; ↗ opens it full size ]", 16, GRAY)
                y += 240
            else:
                y = U.fold(cx, y, cw, name, what, mono_title=True)
        text(cx, y + 6, "a drawing is a scratch for thinking; nothing here changes the Task's Runs or Results", 14, GRAY)
    return body


def studio_disk(task):
    return [(B, ""), ("└── " + J, ""), ("    └── " + task, ""), ("        └── studio/s01-<topic>/", "optional"),
            ("            ├── build_s01_<topic>.py", "the builder; marks kept on rebuild"),
            ("            └── s01-<topic>.excalidraw", "the drawing")]


SK_STUDIO = [("skills/1_base/display/", ""), ("└── excalidraw-report/", "run-draw-s01: a drawing")]


# ── band A · ② t00 reason ideas: one per Job, the 15 ideas ───────────────────────────────────────────────
TA = "t00_reason-ideas/"
TOPICS = [("T1 · why click at all", "W-03 row 2", "<what the insight says>", "so: give the reason before the ask",
           ["I01 reason-first", "I02 reason-question"]),
          ("T2 · what to ask", "rule r2.1", "<the rule>", "so: one ask, at the end", ["I03 ask-alone", "I04 reason-then-ask"]),
          ("T3 · who it is from", "own knowledge", "<a known pattern>", "so: name the sender first", ["I05 sender-first", "I06 …"])]


def t00_task(cx, cy, cw):
    cy = U.note(cx, cy, "261007  a Task that is not a design: its face says what step ② reads and must return")
    y = U.pairs(cx, cy, [("step", "② Reason ideas · method M04, version m2 (inputs/method.md)"),
                         ("reads", "inputs/: goal.md · handoff-W-03.md · rules.md · venue-sms.md"),
                         ("returns", "15 ideas (N + 5), each with a short name, in topics"),
                         ("by", "the designer agent · run-reason-t00 (hard)"),
                         ("state", "closed ✓ · its ideas opened t01 – t15")])
    text(cx, y + 20, "what it must return", 15, INK)
    U.table(cx, y + 50, cw, ["part", "the rule"], [0, 260],
            [("ideas", "15 = N + 5, one design each (step ③); t99 keeps 10"),
             ("each idea", "a short name (it becomes its design's name), its topic, the step it came from"),
             ("each step", "from: a file in inputs/ · says · so"),
             ("frozen", "before any design is made")])


def t00_topics(cx, cy, cw):
    cy = U.note(cx, cy, "261007  the reasoning as chains, one card per topic (the same cards as Job › Reason ideas, opened)")
    text(cx, cy, "inputs/ → reasoning, topic by topic → the ideas", 15, INK)
    y = cy + 34
    topic, src, says, so, ideas = TOPICS[0]           # the first topic open: its chain, box by box
    base("rectangle", cx, y, cw, 150, GRAY, 1, rough=0)
    text(cx + 14, y + 13, "▾", 16, GRAY)
    text(cx + 40, y + 12, topic, 17)
    text(cx + 280, y + 15, f"from {src} · 2 steps · → {len(ideas)} ideas", 14, GRAY)
    U.path([(cx, y + 46), (cx + cw, y + 46)], arrow=False, color=GRAY)
    x, by = cx + 20, y + 70
    for w, s, mono in [(150, src, True), (240, says, False), (290, so, False)]:
        base("rectangle", x, by, w, 44, INK, 1, rough=0)
        text(x + 12, by + 12, s, 14, INK, MONO if mono else U.SANS)
        U.path([(x + w + 6, by + 22), (x + w + 40, by + 22)], color=INK)
        x += w + 46
    for k, idea in enumerate(ideas):
        base("rectangle", x, by - 14 + k * 40, 220, 32, INK, 1.5, rough=0)
        text(x + 10, by - 8 + k * 40, idea, 14, INK, MONO)
    y += 160
    for topic, src, says, so, ideas in TOPICS[1:]:
        y = U.fold(cx, y, cw, topic, f"from {src} · 2 steps · → {', '.join(i.split()[0] for i in ideas)}")
    y = U.fold(cx, y, cw, "… T4 – T6", "3 more topics")
    text(cx, y + 6, "each step names its source in inputs/; each idea's box opens the design it became", 14, GRAY)


def t00_ideas(cx, cy, cw):
    cy = U.note(cx, cy, "261007  each idea with its short name, the design it became and what t99 did with it")
    y = U.table(cx, cy, cw, ["idea", "name", "topic", "rests on", "its design (Task)", "⑤ t99"],
                [0, 70, 260, 360, 520, 860],
                [("I01", "reason-first", "T1", "W-03 r2", "t01_d01_reason-first", "kept #2"),
                 ("I02", "reason-question", "T1", "W-03 r2", "t02_d02_reason-question", "kept #5"),
                 ("I03", "ask-alone", "T2", "rule r2.1", "t03_d03_ask-alone", "verify …"),
                 ("I04", "reason-then-ask", "T2", "rule r2.1", "t04_d04_reason-then-ask", "kept #1"),
                 ("I05", "sender-first", "T3", "own knowledge", "t05_d05_sender-first", "revise …"),
                 ("…", "", "", "", "t06 … t10", "kept"),
                 ("I11 – I15", "", "", "", "t11 … t15", "dropped")], mono=(4,))
    text(cx, y + 14, "ideas.yaml; a row opens its design's Task tab", 14, GRAY)


def t00_chains(cx, cy, cw):
    y = U.table(cx, cy, cw, ["topic", "step", "from (inputs/)", "says", "so"], [0, 90, 160, 380, 700],
                [("T1", "1", "handoff-W-03.md r2", "<what the insight says>", "give the reason before the ask"),
                 ("T1", "2", "goal.md", "<the aim>", "→ I01 · I02"),
                 ("T2", "1", "rules.md r2.1", "<the rule>", "one ask, at the end"),
                 ("T2", "2", "venue-sms.md", "<n> characters", "→ I03 · I04"),
                 ("T3", "1", "own knowledge", "<a known pattern>", "→ I05 · I06")], mono=(2,))
    text(cx, y + 14, "chains.yaml: one row per step; from is a file in inputs/, or says 'own knowledge' (the fence)", 14, GRAY)


def t00_runs(cx, cy, cw):
    U.table(cx, cy, cw, ["Run", "kind", "by", "state"], [0, 420, 560, 800],
            [("runs/run-reason-t00/", "hard", "designer agent", "closed ✓ · 15 ideas"),
             ("../runs/run-open-designs-j03/", "soft", "the Job", "opened t01 – t15 · read only here")], mono=(0,))


def t00_delivery(cx, cy, cw):
    U.pairs(cx, cy, [("hands", "ideas.yaml → t01 – t15: each design Task reads its one idea"),
                     ("to the Block", "nothing: an idea is never released; a design is"),
                     ("frozen", "when run-reason-t00 closes, before any design is made")])


DA = {
    "Task": [(B, ""), ("└── " + J, ""), ("    ├── inputs/", "what step ② reads"),
             ("    └── " + TA, "the Task of step ②"), ("        └── t00_reason-ideas.md", "state · ## Topics")],
    "Topics": [(B, ""), ("└── " + J, ""), ("    └── " + TA + "runs/run-reason-t00/result/", "hard"),
               ("        ├── chains.yaml", "each topic: its steps (from · says · so) → its ideas"),
               ("        └── topics.md", "the readable report, written from chains.yaml")],
    "Ideas": [(B, ""), ("└── " + J, ""), ("    ├── " + TA + "runs/run-reason-t00/result/ideas.yaml", "I01 – I15"),
              ("    └── t01_d01_reason-first/ … t15_d15_<name>/", "one design per idea")],
    "Chains": [(B, ""), ("└── " + J, ""), ("    └── " + TA + "runs/run-reason-t00/result/chains.yaml", "a row per step")],
    "Runs": [(B, ""), ("└── " + J, ""), ("    ├── runs/run-open-designs-j03/", "soft: opens t01 – t15"),
             ("    └── " + TA + "runs/run-reason-t00/", "hard: the ideas")],
    "Delivery": [(B, ""), ("└── " + J, ""), ("    └── " + TA + "runs/run-reason-t00/result/ideas.yaml", "read by t01 – t15")],
}
DA = {k: v + [TREE_NOTE] for k, v in DA.items()}
AR_A = lambda on: [(v, k == on) for k, v in enumerate(["Topics", "Ideas"])]
BAND_A = [
    ("Description", [("Task", 1)], ["run-reason-t00"], "", t00_task, DA["Task"]),
    ("Audience Report", AR_A(0), ["run-reason-t00"], "", t00_topics, DA["Topics"]),
    ("Audience Report", AR_A(1), ["run-open-designs-j03"], "", t00_ideas, DA["Ideas"]),
    ("Work Details", [("Chains", 1)], ["run-reason-t00"], "", t00_chains, DA["Chains"]),
    ("Idea Studio", None, ["run-draw-s01"], "",
     studio_for("t00", [("s01-<topic map>", "the topics and their chains, as one picture"),
                        ("s02-<idea spread>", "the 15 ideas side by side: are they really different?")]),
     studio_disk(TA) + [TREE_NOTE]),
    ("Runs", [("All", 1), ("hard", 0), ("soft", 0)], ["run-reason-t00"], "", t00_runs, DA["Runs"]),
    ("Delivery", None, [], "", t00_delivery, DA["Delivery"]),
]


# ── band B · ③ ④ one design: d04 reason-then-ask (one of t01 – t15) ─────────────────────────────────────
T = "t04_d04_reason-then-ask/"
D = "    └── " + T
DESC = lambda on: [(lab, on == k) for k, lab in enumerate(["Design", "Evaluation"])]
AR_B = lambda on: [(v, k == on) for k, v in enumerate(["Tests", "Drafts", "Performance"])]
SMS = "<opening>. <the reason>. <the ask>: {LINK}"


def design(cx, cy, cw):
    """The Job's design card (s12's Design display), opened: the design │ its process │ its review."""
    cy = U.note(cx, cy, "261007  the Job's design card, opened: the design │ its process │ its review (was word boxes)")
    C1, C2 = 330, 690
    for h, x in [("Design", 0), ("Process (③): its idea, each element's source", C1), ("Review (④ ⑤) · expected outcome", C2)]:
        text(cx + x + 10, cy, h, 13, GRAY)
    y, h = cy + 24, 230
    base("rectangle", cx, y, cw, h, GRAY, 1, rough=0)
    for x in (C1, C2):
        U.path([(cx + x, y), (cx + x, y + h)], arrow=False, color=GRAY)
    U.phone(cx + 20, y + 20, SMS)
    for k, s in enumerate(["from idea I04 reason-then-ask (T2)", "<opening> ← W-03 r2", "<the reason> ← W-03 r4",
                           "<the ask> ← rule r2.1", "③ run-generate-d04 · designer agent"]):
        text(cx + C1 + 12, y + 14 + k * 26, s, 13, GRAY if k == 0 else INK)
    for k, s in enumerate(["④ r02 ✗ T0 r2.3 → revise → r03 ✓ passed", "expected +x [lo, hi] · a draft", "⑤ rank #1 of 15 · kept"]):
        text(cx + C2 + 12, y + 14 + k * 26, s, 13, INK)
    y = U.pairs(cx, y + h + 24, [("state", "passed · draft 2 · kept (rank #1 of 15) · not released yet"),
                                 ("name", "reason-then-ask · born with its idea I04 in t00"),
                                 ("Job", "j03 · G01 × design method M04, version m2 × inputs i2")])
    y = U.note(cx, y + 10, "261007  its short name comes from its idea (t04_d04_reason-then-ask) · kept by ⑤; dropped shows 'dropped'")
    text(cx, y + 4, "each element opens its row in Work Details; a UI design shows its rendered screen in the first column", 14, GRAY)


def evaluation(cx, cy, cw):
    y = U.pairs(cx, cy, [("verdict", "passed · run-verify-d04-v2 · another agent"), ("T0 rules", "all kept"),
                         ("T1 fidelity", "each element's row says it · every source in the manifest"),
                         ("T2 critique", "an expert reviewer agent read it: ✓ (per design, in ④)"),
                         ("T3 pretest", "not here: once per Job, on the 10 kept (s12)"),
                         ("⑤ Review whole", "kept · rank #1 of 15, top 10 kept (t99_review-whole)"),
                         ("T4 the Exp", "not the method's: comes back per arm (Audience Report › Performance)")])
    text(cx, y + 20, "the summary; the checks themselves are in Audience Report › Tests", 14, GRAY)
    U.note(cx, y + 50, "261007  T1 also checks the manifest · ⑤ kept it (rank #1 of 15) · T4 is the Exp's, not the method's")


def elements(cx, cy, cw):
    """The design's elements, each with its source and why: the Rationale view folded in here (decided 261007)."""
    text(cx, cy, "idea I04 reason-then-ask (topic T2): <the idea, one line>  ·  from t00_reason-ideas (②)", 15, INK)
    y = U.table(cx, cy + 34, cw, ["element", "words", "from", "source", "because", "method step", "changed"],
                [0, 100, 230, 330, 450, 700, 960],
                [("opening", "<opening>", "insight", "W-03 r2", "<what the insight says>", "① See · ② Reason", "★"),
                 ("reason", "<reason>", "insight", "W-03 r4", "<what the insight says>", "② Reason", "★"),
                 ("ask", "<ask>", "rule", "r2.1", "<the rule>", "① See (rules)", ""),
                 ("sign-off", "<sign-off>", "theory", "<paper>", "<the theory>", "② Reason", "★")], h=40)
    text(cx, y + 14, "elements.yaml, one entry per element; from = insight · rule · venue · theory · precedent · hunch", 14, GRAY)
    text(cx, y + 40, "source = a file in the Job's inputs/ manifest (a cited row outside it fails T1) · ★ = changed from the idea's plain form", 14, GRAY)
    y = U.note(cx, y + 70, "261007  venue is a source (venue-sms.md in inputs/) · sources come from the manifest")
    U.note(cx, y, "261007  decided: the Rationale view is folded in here: one table, the words and the why (both read elements.yaml)")


def tests(cx, cy, cw):
    y = U.table(cx, cy, cw, ["test (step ④ Review item)", "check", "draft 1", "draft 2"], [0, 220, 640, 820],
                ["T0 · rules", ("", "r2.1 <rule>", "✓", "✓"), ("", "r2.3 <rule>", "✗", "✓"), ("", "<n> characters · venue-sms.md", "✓", "✓"),
                 "T1 · fidelity", ("", "opening ← W-03 r2", "✓", "✓"), ("", "reason ← W-03 r4", "✓", "✓"),
                 ("", "every source in inputs/manifest.yaml", "✓", "✓"),
                 "T2 · critique", ("", "an expert reviewer agent reads it", "", "✓")])
    text(cx, y + 14, "step ④ Review item: one row per check, from inputs/method.md (M04 m2); a ✗ sends it to revise", 14, GRAY)
    y = U.note(cx, y + 44, "261007  step ④ Review item (was part 4) · T1 row: every source in the manifest · T0 reads venue-sms.md")
    U.note(cx, y, "261007  the checks come from the registered method at inputs/method.md (no methods Block)")


def drafts(cx, cy, cw):
    x, y = cx, cy + 10
    text(cx, y, "draft 1 is this Task's run-generate-d04 (③), from idea I04 in t00; t99 (⑤) ranks all 15, keeps 10", 14, GRAY, MONO)
    y += 34
    for k, (name, note) in enumerate([("draft 1", "run-verify-d04-v1: ✗ T0 r2.3"), ("revise", "run-revise-d04: the feedback"),
                                      ("draft 2", "run-verify-d04-v2: passed")]):
        base("rectangle", x, y, 300, 64, RED if "✗" in note else INK, 1.5, rough=0)   # three fit in the content
        text(x + 16, y + 10, name, 18)
        text(x + 16, y + 38, note, 13, GRAY, MONO)
        if k < 2:
            U.path([(x + 306, y + 32), (x + 360, y + 32)], color=INK)
        x += 370
    text(cx, y + 100, "a revision is another Run in this Task (another step, the same design); a new design is a new Task", 14, GRAY)
    yy = U.note(cx, y + 136, "261007  decided (JL): a design and its review are one Task, two Runs · a revision is a Run")
    U.note(cx, yy, "261007  draft 1 is this Task's own run-generate-d04 (③): each method step is a Task (was the Job's generate)")


def performance(cx, cy, cw):
    """This design's numbers: cost, length, the frozen prediction, and the Exp's result when it is back."""
    cy = U.note(cx, cy, "261007  renamed Performance (was Numbers), as the Job's (s12)")
    y = U.pairs(cx, cy, [("tokens", "<n>k · its generate + 2 verify + 1 revise"),
                         ("time", "<m> min · from the Runs' started_at → finished_at"), ("rounds", "2 drafts"),
                         ("length", "<n> characters · 2 segments"), ("elements changed", "3 of 4"),
                         ("predicted", "+x [lo, hi] against the control · by t99's rank (another agent) · draft, frozen at release"),
                         ("Exp arm", "? <arm> · it must name j03 · d04"),
                         ("observed (Exp)", "waits: d04's row of the Block's observed/e01_<exp>/arms.csv (arm totals, never rows)"),
                         ("matched", "– until scored: d04's row of the Block's run-score-e01 scores.csv (direction · in range)")])
    text(cx, y + 20, "the prediction freezes when a person releases the design, and is never edited after the Exp", 14, GRAY)
    text(cx, y + 46, "? tokens: not in the Run receipt yet (haipipe-run's to add: usage:)", 14, RED)
    y = U.note(cx, y + 80, "261007  prediction is a draft until release (was frozen on a date) · Exp arm · arm totals only")
    U.note(cx, y, "261007  observed and matched read from the Block (s11): observed/e01_<exp>/arms.csv · run-score-e01 (was the handoff)")


def runs(cx, cy, cw):
    U.table(cx, cy, cw, ["Run", "kind", "by", "state"], [0, 420, 560, 800],
            [("runs/run-generate-d04/", "hard", "designer agent", "③ draft 1, from idea I04"),
             ("runs/run-verify-d04-v1/", "hard", "another agent", "✗ T0 r2.3"),
             ("runs/run-revise-d04/", "soft", "designer agent", "closed"),
             ("runs/run-verify-d04-v2/", "hard", "another agent", "passed"),
             ("../t99_review-whole/runs/run-rank-t99/", "hard", "t99 (⑤)", "rank #1 · kept · read only here")], mono=(0,))
    U.note(cx, cy + 26 + 5 * 34 + 20, "261007  generate is this Task's own Run (③); t99's rank shown, read only")


def delivery(cx, cy, cw):
    y = U.pairs(cx, cy, [("released", "⬜ waits for the Job's Release (a person, s12)"),
                         ("on release", "prediction.yaml frozen · the words are final"),
                         ("goes to", "j03 › Delivery (designs.md · designs.json, as reason-then-ask) → Block › Delivery → the Exp"),
                         ("Exp arm", "? <arm>, naming j03 · d04, so its result comes back here")])
    text(cx, y + 20, "<opening> <reason> <ask> <sign-off>", 16, INK, MONO)
    U.note(cx, y + 60, "261007  on release: the words are final, the prediction freezes · the Exp arm names d04")


DB = {
    "Design": [(B, "the design Block"), ("└── " + J, "the Job (s12)"),
               ("    ├── inputs/", "the fence: the only folder the design work sees"),
               ("    ├── " + TA + "runs/run-reason-t00/result/", "② ideas.yaml: I04 reason-then-ask, topic T2"),
               (D, "one design (③ ④)"), ("        ├── t04_d04_reason-then-ask.md", "state · ## Design"),
               ("        └── runs/run-generate-d04/", "③ draft 1, from idea I04")],
    "Evaluation": [(B, ""), ("└── " + J, ""), ("    ├── " + T, ""), ("    │   ├── t04_d04_reason-then-ask.md", "## Evaluation"),
                   ("    │   └── runs/run-verify-d04-v<k>/result/", "the verdict (④)"),
                   ("    └── t99_review-whole/runs/run-rank-t99/result/", "⑤ ranking.csv: kept, rank #1")],
    "Tests": [(B, ""), ("└── " + J, ""),
              ("    ├── inputs/method.md -> …/methods/M04-….md", "step ④'s checks, from the registered method"),
              ("    ├── inputs/manifest.yaml · venue-sms.md", "T1: every cited source listed · T0: the venue's limits"),
              (D, ""), ("        └── runs/run-verify-d04-v<k>/result/", "one row per check")],
    "Drafts": [(B, ""), ("└── " + J, ""), (D, ""), ("        ├── runs/run-generate-d04/result/", "③ draft 1, from idea I04"),
               ("        └── runs/", "each draft is its Run's result: generate, revise; no drafts/ folder")],
    "Performance": [(B, ""), ("├── observed/e01_<exp>/", "what the Exp returned, once, for the Block (s11)"),
                    ("│   ├── arms.csv", "per-arm totals, each arm naming jNN · dNN: d04's row"),
                    ("│   └── source.md", "from an insight Block's handoff"),
                    ("├── runs/run-score-e01/scores.csv", "soft, the Block's: d04's row, matched or not"),
                    ("└── " + J, ""), (D, ""),
                    ("        ├── prediction.yaml", "a draft until release, then frozen: +x [lo, hi], by whom, date"),
                    ("        └── runs/*/run.yaml", "started_at · finished_at · ? usage")],
    "Elements": [(B, ""), ("└── " + J, ""), ("    ├── inputs/manifest.yaml", "each source an element cites is listed"),
                 (D, ""), ("        └── elements.yaml", "a row per element: words · source · because")],
    "Runs": [(B, ""), ("└── " + J, ""), ("    ├── " + TA + " · t99_review-whole/", "② the ideas · ⑤ the rank, read only"),
             (D, ""), ("        └── runs/", ""), ("            ├── run-generate-d04/", "hard ③: draft 1"),
             ("            ├── run-verify-d04-v1/ · run-verify-d04-v2/", "hard ④: result/"),
             ("            └── run-revise-d04/", "soft")],
    "Delivery": [(B, ""), ("└── " + J, ""), ("    ├── delivery/designs.md · designs.json", "the Job's, when released"),
                 (D, ""), ("        └── prediction.yaml", "frozen then")],
}
DB = {k: v + [TREE_NOTE] for k, v in DB.items()}

BAND_B = [
    ("Description", DESC(0), [], "", design, DB["Design"]),
    ("Description", DESC(1), [], "", evaluation, DB["Evaluation"]),
    ("Audience Report", AR_B(0), ["run-verify-d04"], "", tests, DB["Tests"]),
    ("Audience Report", AR_B(1), ["run-generate-d04", "run-revise-d04"], "", drafts, DB["Drafts"]),
    ("Audience Report", AR_B(2), ["run-freeze-predictions-j03"], "", performance, DB["Performance"]),
    ("Work Details", [("Elements", 1)], ["run-revise-d04"], "", elements, DB["Elements"]),
    ("Idea Studio", None, ["run-draw-s01"], "",
     studio_for("d04", [("s01-<element options>", "each element's options, before a revise"),
                        ("s02-<draft 1 vs 2>", "what the revise changed, and why")]),
     studio_disk(T) + [TREE_NOTE]),
    ("Runs", [("All", 1), ("hard", 0), ("soft", 0)], ["run-generate-d04", "run-verify-d04", "run-revise-d04"], "", runs, DB["Runs"]),
    ("Delivery", None, [], "", delivery, DB["Delivery"]),
]


# ── band C · ⑤ t99 review whole: one per Job, ranks the 15, keeps 10 ────────────────────────────────────
TC = "t99_review-whole/"


def t99_task(cx, cy, cw):
    cy = U.note(cx, cy, "261007  a Task that is not a design: its face says what step ⑤ reads, its rule and who ranks")
    U.pairs(cx, cy, [("step", "⑤ Review whole · method M04, version m2 (inputs/method.md)"),
                     ("reads", "the 15 design Tasks: words, idea, ④ verdict, expected outcome"),
                     ("rule", "rank by predicted click-through; keep the top N of N + 5 = 10"),
                     ("also checks", "the 10 cover the goal · no two alike · every input row used"),
                     ("by", "another agent (the ④ ⑤ reviewer), never the designer · run-rank-t99 (hard)"),
                     ("state", "closed ✓ · kept 10 · dropped 5")])


def t99_ranking(cx, cy, cw):
    y = U.table(cx, cy, cw, ["rank", "design (Task)", "idea", "predicted click-through", "why", "kept"],
                [0, 70, 380, 470, 680, 980],
                [("1", "t04_d04_reason-then-ask", "I04", "+x [lo, hi]", "the clearest reason, one ask", "✓"),
                 ("2", "t01_d01_reason-first", "I01", "+x [lo, hi]", "<why>", "✓"),
                 ("…", "…", "", "…", "", "✓ 10"),
                 ("11", "t07_d07_<name>", "I07", "+x [lo, hi]", "near-duplicate of d03", "✗"),
                 ("…", "…", "", "…", "", "✗ 5")], mono=(1,))
    text(cx, y + 14, "ranking.csv; a row opens its design's Task tab", 14, GRAY)


def t99_coverage(cx, cy, cw):
    y = U.table(cx, cy, cw, ["check (on the 10 kept)", "result", "verdict"], [0, 420, 820],
                [("the 10 cover the goal", "<n> of <n> sub-aims reached", "ok"),
                 ("no two alike", "d07 dropped: near-duplicate of d03", "ok"),
                 ("every input row used", "W-03 rows 1-5 used; row 6 never", "note")])
    text(cx, y + 14, "the checks step ⑤ adds after the rank; part of run-rank-t99's result", 14, GRAY)


def t99_list(cx, cy, cw):
    y = U.table(cx, cy, cw, ["design (Task)", "④", "rank", "kept"], [0, 520, 700, 860],
                [("t04_d04_reason-then-ask", "passed (draft 2)", "#1", "✓"), ("t01_d01_reason-first", "passed", "#2", "✓"),
                 ("t02_d02_reason-question", "passed", "#5", "✓"), ("… 7 more", "", "", "✓"),
                 ("t07_d07_<name> … 5", "passed", "#11 – #15", "dropped")], mono=(0,))
    text(cx, y + 14, "kept first, dropped folded at the end, as the Job's Design display", 14, GRAY)


def t99_runs(cx, cy, cw):
    U.table(cx, cy, cw, ["Run", "kind", "by", "state"], [0, 420, 560, 800],
            [("runs/run-rank-t99/", "hard", "another agent", "closed ✓ · kept 10"),
             ("../t01 … t15/runs/run-verify-*/", "hard", "each design Task", "read: each ④ verdict")], mono=(0,))


def t99_delivery(cx, cy, cw):
    U.pairs(cx, cy, [("kept 10", "→ Job › Delivery, where a person releases them"),
                     ("dropped 5", "their Tasks kept, marked dropped, folded at the end"),
                     ("predictions", "written by this rank, a draft until a person releases; frozen then")])


DC = {
    "Task": [(B, ""), ("└── " + J, ""), ("    ├── t01_d01_reason-first/ … t15_d15_<name>/", "what step ⑤ reads"),
             ("    └── " + TC, "the Task of step ⑤"), ("        └── t99_review-whole.md", "state · ## Ranking")],
    "Ranking": [(B, ""), ("└── " + J, ""), ("    └── " + TC + "runs/run-rank-t99/result/", "hard"),
                ("        └── ranking.csv", "rank · design · predicted · why · kept")],
    "Coverage": [(B, ""), ("└── " + J, ""), ("    └── " + TC + "runs/run-rank-t99/result/", ""),
                 ("        └── coverage.yaml", "the three checks, beside ranking.csv")],
    "List": [(B, ""), ("└── " + J, ""), ("    └── " + TC + "runs/run-rank-t99/result/ranking.csv", "a row per design")],
    "Runs": [(B, ""), ("└── " + J, ""), ("    └── " + TC + "runs/run-rank-t99/", "hard: rank, keep 10")],
    "Delivery": [(B, ""), ("└── " + J, ""), ("    └── delivery/", "the kept 10, after a person releases")],
}
DC = {k: v + [TREE_NOTE] for k, v in DC.items()}
AR_C = lambda on: [(v, k == on) for k, v in enumerate(["Ranking", "Coverage"])]
BAND_C = [
    ("Description", [("Task", 1)], ["run-rank-t99"], "", t99_task, DC["Task"]),
    ("Audience Report", AR_C(0), ["run-rank-t99"], "", t99_ranking, DC["Ranking"]),
    ("Audience Report", AR_C(1), ["run-rank-t99"], "", t99_coverage, DC["Coverage"]),
    ("Work Details", [("Kept · Dropped", 1)], ["run-rank-t99"], "", t99_list, DC["List"]),
    ("Idea Studio", None, ["run-draw-s01"], "",
     studio_for("t99", [("s01-<the 15 on a grid>", "predicted outcome × how different: where each design sits"),
                        ("s02-<near pairs>", "two designs too alike: which one to keep")]),
     studio_disk(TC) + [TREE_NOTE]),
    ("Runs", [("All", 1), ("hard", 0), ("soft", 0)], ["run-rank-t99"], "", t99_runs, DC["Runs"]),
    ("Delivery", None, [], "", t99_delivery, DC["Delivery"]),
]

# "skills" to the right of each on-disk tree (as s12): the skills that screen's Runs load, from skills/; "?" = proposed
SKD = "skills/2_theme/design/"
UNIT = lambda what, more=False: [(SKD, ""), ("└── haipipe-design-unit/", what),
                                 (("    ├── " if more else "    └── ") + "SKILL.md", "reads inputs/method.md")]
AGENT = ("haipipe-design/agents/", "the designer agent runs it")        # short lines: the meaning sits 225 px right
REVIEWER = ("? …/reviewer-agent.md", "? ④ ⑤: checks, ranks, predicts")
RUN = ("1_base/project/haipipe-run/", "every Run's receipt")
SK_A = {"Task": UNIT("② reason ideas") + [AGENT], "Topics": UNIT("② reason ideas") + [AGENT],
        "Ideas": UNIT("② reason ideas") + [("haipipe-design/", "run-open-designs-j03"), AGENT],
        "Chains": UNIT("② reason ideas") + [AGENT, REVIEWER], "All": UNIT("② reason ideas") + [AGENT, RUN],
        "": UNIT("② its ideas.yaml")}
SK_B = {"Design": UNIT("③ generate", True) + [("    └── scripts/render_screen.py", "a UI design's picture"), AGENT],
        "Evaluation": UNIT("④ verify") + [REVIEWER],
        "Tests": UNIT("④ verify", True) + [("    └── scripts/check_unit.py", "T0: the rules, by script"), REVIEWER],
        "Drafts": UNIT("③ generate · revise") + [AGENT], "Elements": UNIT("③ generate") + [AGENT],
        "Performance": [("skills/1_base/project/", ""), ("└── haipipe-run/", "the Run receipt"),
                        ("    └── ? usage:", "? tokens per Run: haipipe-run's to-do")],
        "All": UNIT("③ ④ and revise") + [AGENT, REVIEWER, RUN],
        "": [(SKD, ""), ("└── haipipe-design/", "run-release-j03 (the Job's)")]}
SK_C = {k: UNIT("⑤ review whole") + [REVIEWER] for k in ("Task", "Ranking", "Coverage", "Kept · Dropped")}
SK_C.update({"All": UNIT("⑤ review whole") + [REVIEWER, RUN], "": [(SKD, ""), ("└── haipipe-design/", "run-release-j03 (the Job's)")]})
SK_NOTE = ("✎ 261007  skills: what this screen's Runs load, from skills/", "")


def _skills(band, table):
    """Each screen gets its skills tree (the 7th element), by its open view."""
    out = []
    for sc in band:                                   # AGENT etc. are under skills/2_theme/design/ unless they say 1_base
        view = next((lab.lstrip("? ") for lab, on in sc[1] or [] if on), "")
        sk = SK_STUDIO if sc[0] == "Idea Studio" else table.get(view, [])
        out.append(sc + (sk + [SK_NOTE],))
    return out


BAND_A, BAND_B, BAND_C = _skills(BAND_A, SK_A), _skills(BAND_B, SK_B), _skills(BAND_C, SK_C)

BANDS = [("t00", "② t00 · reason ideas  ·  runs: reason (hard)", "Task · t00 · reason ideas ▾", BAND_A),
         (None, "③ ④ d04 · reason-then-ask  ·  runs: generate · verify · revise", "Task · d04 · reason-then-ask ▾", BAND_B),
         ("t99", "⑤ t99 · review whole  ·  runs: rank (hard)", "Task · t99 · review whole ▾", BAND_C)]

# One UI for every Task: the same tab, the same six Spaces; a Task's run types decide what its Spaces show,
# since each run type's Result is what a view reads (JL 261007: "different type of runs … the same UI, but
# different content?")
RUN_VIEWS = ("run type → the views its Result fills", [
    ("the same tab and six Spaces for every Task; its run types decide the content", GRAY),
    ("reason ②  (hard · t00)          → Topics · Ideas · Chains", INK),
    ("generate ③  (hard · a design)   → Design · Drafts · Elements", INK),
    ("verify ④  (hard, another agent) → Tests · Evaluation", INK),
    ("revise  (soft · a design)       → Drafts", INK),
    ("rank ⑤  (hard, another agent · t99) → Ranking · Coverage · Kept · Dropped", INK),
    ("freeze-prediction  (soft)       → Performance", INK),
    ("every Task: its Runs → Runs · its Result handed on → Delivery", GRAY)])

POPOUTS = [RUN_VIEWS, ("Task ▾  ·  the Job's Tasks, by step", [("the same list as Job › Work Details (s12)", GRAY),
                                                    ("② t00 · reason ideas", INK),
                                                    ("③ ④ t01 d01 reason-first", INK), ("     t02 d02 reason-question", INK),
                                                    ("     t04 d04 reason-then-ask  ←", INK), ("     … t10", INK),
                                                    ("     ▸ t11 … t15 · dropped, folded", GRAY),
                                                    ("⑤ t99 · review whole", INK)]),
           U.card_window("By insight"),
           ("W-03 row 4  ·  the insight it cites", [("../inputs/handoff-W-03.md -> insights/bNN_<topic>/delivery/W-03.md · signed ✅", GRAY),
                                                   ("  <the counsel, one line>", INK),
                                                   ("the design's <reason> element names this row (T1)", GRAY)])]

DEC = "✎ 261007 decided: "
QUESTIONS = [  # each under the screen it is about: (space, view, "…") or (band, space, view, "…"); green ✎ = decided
    # (JL 261007: "have your own judgements"), red ? = for another owner
    ("t00", "Description", "", DEC + "the Job's run-open-designs-j03 opens t01 – t15: opening Tasks writes the Job's "
                                     "folder, so the Job owns it; t00 only writes ideas.yaml"),
    ("t00", "Audience Report", "Topics", DEC + "every step's from is a file in the manifest or says 'own knowledge', "
                                               "the same fence as T1; the ④ ⑤ reviewer checks it before t01 – t15 open"),
    ("Description", "Design", DEC + "the short name stays when a revise changes the words: the name is the idea's, "
                                    "and a revise is a Run on the same design; a new idea would be a new Task"),
    ("Description", "Evaluation", DEC + "verify is always a separate reviewer agent, never the one that generated"),
    ("Audience Report", "Tests", DEC + "T2 critique per design, inside ④ (an expert reviewer agent reads each); T3 "
                                       "pretest once per Job on the 10 kept, since it needs real readers"),
    ("Audience Report", "Drafts", DEC + "earlier drafts live only in the Runs: each generate or revise Run's result "
                                        "is its draft; one copy, no drafts/ folder"),
    ("Audience Report", "Performance", DEC + "t99's run-rank-t99 writes each predicted effect into its ranking.csv; "
                                             "the workflow projects it into this design's prediction.yaml as a draft, "
                                             "frozen when a person releases the design"),
    ("Runs", "", DEC + "every Run is run-<type>-<target>, hard ones too (JL: unify the name to be run-xxx-xxx); a "
                       "repeat names what it reads: run-verify-d04-v2 checks draft 2 (was rNN_<type>_<target>)"),
    ("Delivery", "", DEC + "a newer handoff never makes a released design stale: it keeps its pinned inputs; "
                           "the new handoff is a new inputs version and a new Job (one clock per Job)"),
    ("Delivery", "", "? the Exp arm names j03 · d04 in the Block's observed/e01_<exp>/arms.csv (the Exp's owner)"),
    ("t99", "Audience Report", "Ranking", DEC + "the prediction is written here and frozen at release, so the "
                                              "ranking and the released design agree"),
    ("t99", "Work Details", "", DEC + "the 5 dropped keep their Tasks, marked dropped and folded: the ranking cites "
                                      "them, and a record of what lost is evidence for the next method version"),
]

CHANGES = ["261007  Performance's Run is the Job's run-freeze-predictions-j03 (was a per-design run-freeze-prediction-d04): one freeze, signed with the release",
           "261007  every Run named run-<type>-<target>, hard ones too: run-reason-t00 · run-generate-d04 · run-verify-d04-v1/-v2 · run-rank-t99 (JL: unify the name; was rNN_<type>_<target>)",
           "261007  three kinds of Task, one per method step: t00 ② · tNN ③ ④ · t99 ⑤, side by side, a column each (was the design Task only)",
           "261007  one UI for every Task: the same tab and six Spaces; its run types decide the content (pop-out: run type → views)",
           "261007  Description › Design is the Job's design card, opened · every design has a short name from its idea",
           "261007  the Job folder is jNN_<goal>_<design-method> (was jNN_<goal>_by-<method>)",
           "261007  after s11 · s12: the inputs/ fence, a prediction frozen at release; a design and its review: one Task, two Runs",
           "261007  steps ④ Review item · ⑤ Review whole (s03's design unit); the checks from inputs/method.md (no methods Block)",
           "261007  each open question sits under the screen it is about",
           "261007  Runs panel: one card per run type, run-<type>-<target> (was Verify · Revise · Freeze)",
           "261007  Numbers renamed Performance (as s12)",
           "261007  decided here, not left open (JL: \"have your own judgements\"): green notes under their screens; red only for another owner",
           "261007  decided: the Rationale view folded into Work Details › Elements",
           "261007  Idea Studio restored at every Task (JL): optional drawings about that Task, as the Job's",
           "261007  skills: each screen's skills, as a tree from skills/, right of its on-disk tree (as s12)",
           "261007  a vertical line between the three kinds (JL)"]


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s13-design-task.excalidraw"
    U.level_drawing(out, Path(__file__).name, "Task",
                    "Task level: a Task per method step (t00 ② · d04 ③ ④ · t99 ⑤ in j03_<goal>_<design-method>)",
                    "One UI for every Task: the same tab and six Spaces; the Task's run types decide what each shows. Left to right: t00 · a design · t99.",
                    MOVES, [], POPOUTS, QUESTIONS, changes=CHANGES, bands=BANDS, side_by_side=True)


if __name__ == "__main__":
    main()
