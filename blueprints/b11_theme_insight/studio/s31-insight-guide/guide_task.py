"""s31 · the Task level of the insight Guide: one question on one Job's pair.

Read live: the Space cards from s13's screens, today's steps 3 to 5 from method.md (they are the Task's
work), the answering and reading cards and their papers from the Guide's files. Typed here, as the
proposal (red): the question is asked in the Prototype, so the Task's Description reads it, never edits it.
"""
import insight_guide_live as G

ANSWER = ["By exploring", "By automated insight search", "By pattern mining", "By model comparison", "By hypothesis test"]
READ = ["By multiverse", "By heterogeneity", "By sensemaking"]
WORDS = {"Description": ("its question, read only from the release, and its records", "…/j0N_pN/tNN_<L><NN>_<q>/question.md"),
         "Idea Studio": ("optional: a drawing about this question", "studio/"),
         "Audience Report": ("its page: the answer, a part per partition", "tNN_<L><NN>_<q>.md"),
         "Work Details": ("one Run per partition, and Cross", "runs/rNN_<partition>/"),
         "Runs": ("hard: one per partition · soft: write, check", "runs/"),
         "Delivery": ("none of its own: its answer goes up as a cite need", "—")}
STEPS = [G.step_card(3, "Task"), G.step_card(4, "Task"), G.step_card(5, "Task"),
         ("? 6 · Sign (Wisdom only)", "a person signs the counsel before it leaves", "where: Audience Report › its page   signs: a person")]

LEVEL = {
    "Description": [("t", G.role("Task", "one question on one Job's pair: its runs per partition and its page")),
                    ("c", G.space_cards("Task", WORDS)),
                    ("t", "? Description › Question is read only: a change is a proposal to the Prototype")],
    "Method": [("c", STEPS), ("t", "answering cards"), ("c", G.method_cards(ANSWER)),
               ("t", "reading cards"), ("c", G.method_cards(READ))],
    "RoadMap Draw": [("w", G.drawings(["s13-task-level", "s03-insight-methods"])),
                     ("t", "? guide.yaml roadmap: Task")],
    "Related Paper": [("c", G.papers([a.lower() for a in ANSWER + READ] + ["all methods (question-answering)"], 6)[0]),
                      ("t", "the tests' papers (T4 to T7) are under 'tests (after the run)'")],
}

ON_DISK = {
    "Description": [("Tools/blueprints/b11_theme_insight/studio/s13-task-level/", "the question's six Spaces, as designed"),
                    ("work/…_prototype/j0N_pN/tNN_<L><NN>_<q>/question.md", "the question, read only")],
    "Method": [("servers/workbench-insight/guide/method.md", "today's steps 3 · 4 · 5, the answering and reading cards"),
               ("servers/workbench-insight/guide/methods/answer/ · read/", "the cards' files")],
    "RoadMap Draw": [("? guide.yaml roadmap: Task", "? s13 · s03")],
    "Related Paper": [("servers/workbench-insight/related/papers.md", "groups: the answering and reading methods")],
}

OPEN = ["? today's step words (Run each partition · Check the run · Write the page) stay, with 'where' in the six Spaces?",
        "? a question's change goes to the Prototype's proposals/, never edited in the Task"]
