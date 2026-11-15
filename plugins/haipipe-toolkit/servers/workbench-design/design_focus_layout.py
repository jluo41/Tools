"""The design focus page's views at each level: their keys and names, the Task steps, each view's caption, what
comes after each Task step, and the skills each view's work calls on (split out of design_focus.py)."""
from __future__ import annotations

# a Design Board's buttons, in plain words, paired with the insight Board's (Findings · Questions · Data · Rounds ·
# Advice): Designs what was made · Goals what was asked · Inputs what it read · Rounds each Job, one method
# on one inputs version · Tests what came back. The method's own views are the Design Method Book's (design_book.py).
BLOCK_VIEWS = (("designs", "Designs"), ("goals", "Goals"), ("inputs", "Inputs"), ("rounds", "Rounds"), ("tests", "Tests"))
OLD_BLOCK_VIEWS = {"summary": "designs", "jobs": "rounds", "methods": "tests"}     # an older link opens its new view
JOB_VIEWS = (("setup", "Setup"), ("ideas", "Ideas"), ("designs", "Designs"), ("ranking", "Ranking"), ("release", "Release"))
TASK_STEPS = {"t00": ("💡", "reason ideas", ("Inputs", "Chains", "Ideas", "Fence check")),
              "design": ("✏️", "design", ("Draft", "Verify", "Revise", "State")),
              "t99": ("🏆", "review whole", ("Rank", "Coverage", "Kept"))}
CAPTIONS = {"goals": "the signed goals, the shared rules and the Block's questions",
            "inputs": "each frozen inputs version, one round each",
            "rounds": "each goal × method × inputs version, and how far each Job has got",
            "tests": "how the predictions held up in the experiment, and what each Job cost",
            "setup": "the three pins: goal, method, inputs", "ideas": "what was reasoned, from the fence only",
            "designs": "each design as it reads, and its verdict", "ranking": "t99's ranking and coverage",
            "release": "what was released, and its frozen predictions"}
# what comes after each Task step (task_views.NEXT, b12 j01): the "next: …" pointer under a Task's Work
NEXT = {"inputs": ("🔗 Chains", "chains"), "chains": ("💡 Ideas", "ideas"), "ideas": ("✅ Fence check", "fence-check"),
        "fence-check": ("✏️ the design Tasks · Draft", "design"), "draft": ("🧪 Verify", "verify"),
        "verify": ("🔁 Revise if it failed, 🪜 State if it passed", "revise"), "revise": ("🧪 Verify the new draft", "verify"),
        "state": ("🏆 review whole · Rank", "t99"), "rank": ("🧩 Coverage", "coverage"), "coverage": ("✅ Kept", "kept"),
        "kept": ("the Job · Review and approve", "release")}

# the skills each view's work calls on (the rail's Skills: focus_page.page_skills reads it, 261106)
VIEW_SKILLS = {
    "goals": (("haipipe-design-goal", "adds a goal and sets the shared rules; a person signs each"),),
    "rounds": (("haipipe-design", "launches a Job: a signed goal × a signed method version × an inputs version"),
               ("haipipe-design-workflow", "says each Job's next Run and checks its gates")),
    "tests": (("haipipe-design-method", "adds an experiment's per-arm totals, scores the predictions and proposes "
               "the next method version"),),
    "setup": (("haipipe-design-goal", "pins the goal and builds the Job's fence"),
              ("haipipe-design-method", "pins the method version")),
    "ideas": (("haipipe-design-unit", "reasons the ideas, step by step, from the fence only"),
              ("haipipe-design", "checks the fence and opens the design Tasks")),
    "designs": (("haipipe-design-unit", "generates, verifies and revises each design"),
                ("haipipe-design-workflow", "projects a draft and its verdict into the Task")),
    "ranking": (("haipipe-design-unit", "ranks the designs and keeps the top N"),
                ("haipipe-design-workflow", "projects the ranking into each prediction")),
    "release": (("haipipe-design-delivery", "freezes the predictions and releases the kept designs"),
                ("haipipe-design-workflow", "closes the Job once a person signs")),
    "inputs": (("haipipe-design-goal", "builds the fence: inputs/ and its manifest"),),
    "chains": (("haipipe-design-unit", "reasons the chains, each step with its source"),),
    "fence-check": (("haipipe-design", "opens the design Tasks after another agent's fence check"),),
    "draft": (("haipipe-design-unit", "generates the design from its idea"),),
    "verify": (("haipipe-design-unit", "verifies the draft in a fresh context"),),
    "revise": (("haipipe-design-unit", "revises what the verify named, nothing else"),),
    "state": (("haipipe-design-workflow", "projects the verdict and the rank into the Task"),),
    "rank": (("haipipe-design-unit", "ranks the passed designs, a predicted effect each"),),
    "coverage": (("haipipe-design-unit", "checks which parts of the goal the kept cover"),),
    "kept": (("haipipe-design-workflow", "projects kept or dropped onto each design's face"),),
}
