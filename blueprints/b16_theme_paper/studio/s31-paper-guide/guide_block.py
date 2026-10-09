"""s31 · the Block level of the paper Guide (owned by the Block session, design_b16_theme_paper-block).

What the Paper Board's Guide shows in its Block section, View by View: read live from the paper Guide's
files (paper_guide_live.py), then the Block-level proposals, each marked "?" so it draws red until JL
settles it. The proposals (261007):

1. A Board-level step 0, Set up the paper: scope, venues and related work. The Board has three
   Description groups and three run types for them (Add a venue, Add a related item, Read a paper),
   but no Method step says when they are done or who signs.
2. Skills by level: guide.yaml lists the paper's skills in one list; the Block section names the
   Board's own (haipipe-paper owns; -story, -ideation, -venue, haipipe-question work; workbench-paper shows).
3. Two words kept apart: Description › Related (what the paper sits beside) and Guide › Related Paper
   (the papers behind the method); RoadMap Draw (the theme's drawings) and the Story's RoadMap Draw
   (one paper's drawing, now in its Idea Studio).
4. After the Q01 migration the Audience Report reads j00_story/, not A1-Story/.

Settled 261007 (g03): 1 is live in method.md (step 0, signed by naming the target venue); 2 stays one skills
list; the venue lives in both places. 4 changed: j00_story/ is gone (JL: the Story is not a Job), and where the
Story Page lives is open again (b03 s04: studio/ holds topics, reports/ holds Question reports). They draw as
green CHANGES; what is still open draws red.
"""
import paper_guide_live as G

SKILLS = "skills   haipipe-paper owns · haipipe-paper-story · -ideation · -venue · haipipe-question work · workbench-paper shows"

LEVEL = {
    "Description": [("t", G.role("Block")), ("c", G.space_cards("Block")), ("m", SKILLS),
                    ("t", "? the Story Page: a Board-level Page beside board.md (its drawings as studio topics, its "
                          "questions as reports), or the face of studio/s02-story/ (b03 s04)")],
    "Method": [("c", G.steps("Block")), ("t", "method cards"), ("c", G.method_cards("Block")),
               ("t", "step 3's work runs in the Project's work and discovery Blocks; the Board shows its answers")],
    "RoadMap Draw": [("w", G.drawings("Block")),
                     ("t", "? these are the theme's drawings; one paper's own RoadMap Draw is in its Idea Studio")],
    "Related Paper": [("c", G.papers("Block")),
                      ("t", "? none yet behind step 0 (choosing a venue, reading the related work)"),
                      ("t", "? not Description › Related: that is what one paper sits beside")],
}

ON_DISK = {
    "Description": [("servers/workbench-paper/guide/guide.yaml", "levels: Block · the Space cards' words"),
                    ("servers/workbench-paper/paper_theme.py", "each card's sub · runs, read live"),
                    ("servers/workbench/guide/levels.yaml", "the base's words, where paper says nothing")],
    "Method": [("servers/workbench-paper/guide/method.md", "**Block · …**: steps 0 to 3"),
               ("servers/workbench-paper/guide/methods/framing/", "2 cards: problematization, one main idea"),
               ("servers/workbench-paper/guide/methods/story/", "3 cards: claim and warrant, evidence first, reproducible run")],
    "RoadMap Draw": [("servers/workbench-paper/guide/guide.yaml", "roadmap: Block, three drawings"),
                     ("Tools/blueprints/b16_theme_paper/studio/s01-paper-ladder/", "the paper ladder"),
                     ("Tools/blueprints/b16_theme_paper/studio/s11-paper-block/", "the Board's screens"),
                     ("Tools/blueprints/b16_theme_paper/studio/s02-paper-workbench/", "the old four-Space page")],
    "Related Paper": [("servers/workbench-paper/related/papers.md", "rows with level Block: 8 papers"),
                      ("? a level Block row for step 0", "? a paper on choosing a venue or reading related work")],
}

OPEN = ["? The Story Page: a Board-level Page beside board.md, or the face of studio/s02-story/ (b03 s04: studio/ "
        "holds topics, reports/ holds Question reports); its research questions become reports/qNN_ either way"]

CHANGES = ["✎ 261007 · step 0, Set up the paper, is in method.md's Block table, signed by naming the target venue (g03)",
           "✎ 261007 · skills stay one list in guide.yaml; the Block's line names its own skills (g03)",
           "✎ 261007 · the venue lives in both places: venues/ at the Board, the version's face for its one (g03)",
           "✎ 261007 · no Story Job: j00_story/ is gone (JL: the Story is not a Job)"]
