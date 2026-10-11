"""s31 · the Block level of the insight Guide: what the insight Board's Guide shows in its Block section.

Read live (insight_guide_live.py): the six Space cards from s11's screens, today's six steps from method.md,
the method cards and papers from the Guide's files, the drawings from b11's studio. Typed here, as the
proposal (red, "?"): the Board's own steps under plan C (add a version, add a Job, read across Jobs), and
where the Prototype's steps (ask, plan, sign a release) live, since the Prototype is its own work Block.
"""
import insight_guide_live as G

WORDS = {"Description": ("one dataset, its versions, and the Prototype it runs: the Map of Jobs", "board.md · meta/ · the release"),
         "Idea Studio": ("the Board's drawings, one topic after another", "studio/sNN-<topic>/"),
         "Audience Report": ("the Block's own questions over the Jobs: Coverage · Tracks · Consistency · Findings",
                             "reports/qNN_<topic>/"),
         "Work Details": ("the Jobs, each opening to its Tasks' quick results", "j0N_pN_<d>vM/"),
         "Runs": ("the Board's own soft Runs, and its Jobs' from below", "runs/run-<type>-<target>/"),
         "Delivery": ("the signed Wisdom counsel, naming the Job it came from", "delivery/")}
SKILLS = "skills   haipipe-insight owns · haipipe-insight-workflow runs · haipipe-insight-check checks · workbench-insight shows"
PROTOTYPE = ("? 0 · Make the Prototype (in its work Block)", "ask and plan each question, cut the partitions, sign a release",
             "today's steps 1 and 2; where: the Prototype Block (work theme)   signs: a person signs the release")
STEPS = [PROTOTYPE,
         ("? 1 · Add a data version", "register a new extract: frozen, its rows counted per cut",
          "where: Description › Dataset (Add a data version)   signs: —"),
         ("? 2 · Add a Job", "pair a release with a data version: one clock moved from its neighbour",
          "where: Description › Map · Work Details (Add a Job)   signs: —"),
         ("? 3 · Read across Jobs", "what each Job answered, how answers moved, what replicates (T8)",
          "where: Audience Report › Coverage · Tracks · Consistency · Findings   signs: a person signs W"),
         G.step_card(6, "Block")]

LEVEL = {
    "Description": [("t", G.role("Block", "one insight topic over one growing dataset: a Job per pair (release × data version)")),
                    ("c", G.space_cards("Block", WORDS)), ("m", SKILLS),
                    ("t", "? until insight_theme.py exists, these cards follow s11's design, not the live frame")],
    "Method": [("c", STEPS), ("t", "method cards"), ("c", G.method_cards(["By protocol reuse"])),
               ("t", "? no card yet for reading across Jobs (replication, test T8)")],
    "RoadMap Draw": [("w", G.drawings(["s00-insight-structure", "s01-insight-ladder", "s11-block-level", "s02-insight-workbench"])),
                     ("t", "? guide.yaml roadmap: names these per level; today the Guide shows only s02")],
    "Related Paper": [("c", G.papers(["by protocol reuse"])[0]),
                      ("t", "? none yet behind reading across Jobs (replication across data versions)")],
}

ON_DISK = {
    "Description": [("servers/workbench-insight/guide/guide.yaml", "the Guide's words; ? no levels: yet"),
                    ("Tools/blueprints/b11_theme_insight/studio/s11-block-level/", "the Board's six Spaces, as designed"),
                    ("servers/workbench/guide/levels.yaml", "the base's words, where insight says nothing"),
                    ("? servers/workbench-insight/insight_theme.py", "? then the cards read the live frame")],
    "Method": [("servers/workbench-insight/guide/method.md", "today: one six-step table (Prototype · Instance)"),
               ("? method.md **Block · …** table", "? add a version · add a Job · read across Jobs · hand off"),
               ("skills/1_base/question/haipipe-question-asking/methods/", "the asking cards, used in the Prototype")],
    "RoadMap Draw": [("guide.yaml explain: roadmap-draw", "today: the one design drawing (s02)"),
                     ("? guide.yaml roadmap: Block", "? s00 · s01 · s11 · s02")],
    "Related Paper": [("servers/workbench-insight/related/papers.md", "rows by group; ? no level column yet"),
                      ("? a level Block row", "? a paper on replication across data versions")],
}

OPEN = ["? The Prototype's steps (ask, plan, sign a release) live in its work Block: show them here as step 0, or link to the work Guide?",
        "? method.md by level (**Block · …** · **Job · …** · **Task · …**) in place of today's one six-step table?",
        "? papers.md gets a level column, as the paper Guide's has?",
        "? insight_theme.py on the frame: then every Space card reads the live frame, not s11–s13"]
