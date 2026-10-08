"""s31 · the Task level of the design Guide: what one design's tab shows in its Guide's Task section.

Read live from the design Guide's files (design_guide_live.py), then the Task-level proposals, each
marked "?" (261007, after s13): one design is one Task, its draft made by its own generate Run (③) and
checked by its verify Runs (④), T0 to T3, in the Revise loop (JL 261007: one Task, two Runs); every source an element cites is a file in the Job's inputs/, and T1 checks
it is in the manifest; its numbers (tokens, time, rounds, length) are recorded, and its prediction is a
draft until a person releases the design, frozen then; T4 comes back from the Exp through an insight
Block, as totals for an arm that names the design, and is matched against that prediction.
"""
import design_guide_live as G

SKILLS = "skills   haipipe-design-unit: generate · verify · revise one design · workbench-design shows"
SOURCES = ("? 4a · Check its sources", "T1: every source an element cites is in the Job's inputs/manifest.yaml",
           "where: Audience Report › Tests   runs: run-verify-<design>   file: <job>/inputs/manifest.yaml")
NUMBERS = ("? 4c · Record the numbers", "tokens · time · rounds · length; the prediction, a draft until release, frozen then",
           "where: Audience Report › Numbers   runs: run-freeze-prediction-<design>   file: prediction.yaml")
TESTS = G.papers(["tests"])

LEVEL = {
    "Description": [("t", "? one design: its words, its elements, how it was checked  (base: " + G.role("Task") + ")"),
                    ("c", G.space_cards("Task")), ("m", SKILLS),
                    ("t", "? Description: Design · Rationale · Evaluation; each source a file in the Job's inputs/ (s12)"),
                    ("t", "? Audience Report: Tests · Drafts · Numbers (s13); live today: no views")],
    "Method": [("c", G.steps({4}) + [SOURCES, NUMBERS]), ("t", "the five tests"), ("c", G.tests()),
               ("t", "one design is one Task: ③ generate and ④ verify are its Runs, a revise another Run; ② is t00, ⑤ is t99 (s12)"),
               ("t", "T0 to T3 run per design in the Revise loop"),
               ("t", "T4, the Exp, comes back per arm: totals only, never rows, for an arm that names its design"),
               ("t", "? T2 critique and T3 pretest: per design, or once per Job?")],
    "RoadMap Draw": [("w", G.drawings([("s13-design-task", "s13 · the Task", "one design's screens")]))],
    "Related Paper": [("c", TESTS), ("t", "? none yet on predicting a message's effect before the Exp, or scoring it after")],
}

ON_DISK = {
    "Description": [("servers/workbench-design/design_theme.py", "_task: Design · Rationale · Evaluation"),
                    ("? design_theme.py _task: Audience Report", "? Tests · Drafts · Numbers"),
                    ("? <task>/elements.yaml", "? each element's words, source and why")],
    "Method": [("servers/workbench-design/guide/method.md", "§ 1 step 4 · § 4.1 the five tests"),
               ("? <job>/inputs/manifest.yaml", "? T1: every cited source is listed"),
               ("? <task>/prediction.yaml", "? a draft until release, then frozen"),
               ("? run.yaml usage: tokens", "? not in the Run receipt yet")],
    "RoadMap Draw": [("Tools/designs/b12_theme_design/studio/s13-design-task/", "the Task's screens")],
    "Related Paper": [("servers/workbench-design/related/papers.md", f"group 'tests': {len(TESTS)} papers")],
}

OPEN = ["? Steps for the sources (T1 against the manifest) and the numbers, with a prediction frozen at release?",
        "? Who predicts: the agent that wrote the design, another agent, or a model fit on past Exps?",
        "? T2 critique and T3 pretest: per design, or once per Job?",
        "? Every Exp arm names its design, so the arm's totals come back to that Task?",
        "? Tokens in each Run's receipt (usage:), a change to the shared Run contract?"]
