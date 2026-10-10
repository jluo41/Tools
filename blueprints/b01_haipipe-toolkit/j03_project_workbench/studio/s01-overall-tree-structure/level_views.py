"""Screens per level: the proposed Job and Task tabs, one screen per Space, and today's screens beside them.

Used by the topic drawings s11 (Block), s12 (Job) and s13 (Task). For every variant:

    proposed   one screen per Space of its Level tab (Guide · Block · Job · Task), filled per family
    today      the same variant as the current workbench shows it: Spaces and views as the server
               code renders them (SERVER), run buttons from the family's workbench-table.md or the
               server's own list (SERVER_RUNS), and in red how today differs

Placeholders only: no project content. The proposed Block screens are build_ladder_v4.block_views.
"""
import build_ladder_v4 as L

INK, GRAY, RED, TEAL, BLUE = L.INK, L.GRAY, L.RED, L.TEAL, L.BLUE
text, path, base = L.text, L.path, L.base
GAP = 50                       # between two screens
ROW_GAP = 90                   # between the proposed row and today's row

JOB_FAMILY = {"work Job": "task", "discovery Job": "discovery", "Page Job": "task", "paper version": "paper",
              "cowork Job": "cowork", "DIKW level": "insight", "design method": "design", "labeling Job": "labeling"}
TASK_FAMILY = {"work Task": "task", "Page Task": "task", "paper Section": "paper", "discovery Task": "discovery",
               "insight question": "insight", "design folder": "design", "labeling Task": "labeling"}

# ── proposed: the Job tab, one screen per Space ─────────────────────────────────────────────────
# Space -> (content lines, Runs buttons, picked line); the first line is the Space's heading
JOB_DEFAULT = {
    "Overview": (["jNN_<job>.md", "goal: the one line this Job delivers", "state: half · next: <step>",
                  "task_groups: t0N · t1N", "shared: src/ · sbatch/"], ["Update the Job", "Review the Job"]),
    "Studio": (["topics, one folder each (optional)", "s01-<topic>/   drawing · chat",
                "▢ the open topic's drawing, live"], ["+ Add topic", "Draw"]),
    "Reports": (["Q    question        status    report", "Q01  <question>      answered  q01_<topic>",
                 "(optional at Job level)"], ["Ask a Question"]),
    "Tasks": (["Task        Plan Build Run Report", "t01_<task>  done done  done half",
               "t02_<task>  done half  —    —", "t03_<task>  —    —     —    —",
               "pick a Task → the Task tab"], ["Add a Task", "Plan its Tasks"], 2),
    "Runs": (["this Job's soft Runs", "run-launch-all/      ok      starts its Tasks' Runs",
              "run-plan-tasks/      open", "☐ from below: its Tasks' Runs too"], ["Launch all", "Plan its Tasks"]),
    "Check": (["waiting in this Job", "t02   check a Task       2 days", "stale: t03   no Run for 30 days"],
              ["Check a Task", "Review the Job"]),
    "Delivery": (["its own (optional)", "the Job's output   released", "from below", "t01   report released"],
                 ["Release the Job's output"]),
}
JOB_FAMILY_VIEWS = {
    "discovery": {   # one inquiry (b14 Q01, 261007): the Block's six Spaces; its Tasks are its sub-questions
        "Description": (["jNN_<inquiry>.md: the inquiry", "asks: <the inquiry's one question>",
                         "sub-questions: t01 · t02 · t03", "boundary: <years · fields · source kinds>",
                         "state: half · 10 papers · 2 to verify"], ["Update the inquiry", "Plan its Tasks"]),
        "Idea Studio": ([("s01-<inquiry>-map", "", "drawing"), ("s02-<topic>", "", "1 chat")], ["Draw"]),
        "Audience Report": ([("Sub-question", "Papers read", "Answer"), ("t01 <sub-question>", "r01-r06 · 6", "verdict"),
                             ("t02 <sub-question>", "r01-r04 · 4", "draft"),
                             ("t03 <sub-question>", "—", "asked")], ["Synthesize a Task", "Check a Task"], 0),
        "Work Details": (["Task · paper            type       state", "▾ t01_<sub-question>    verdict    done",
                          "    r01_<author><year>   complete   cited", "    r02_<author><year>   complete   to verify",
                          "▸ t02_<sub-question>    landscape  half", "▸ t03_<sub-question>    map        new",
                          "pick a Task → the Task tab"], ["Add a Task", "Find papers", "Read a paper"], 1),
        "Runs": ([("Run", "type", "writes", "state"), ("run-plan-tasks", "Plan its Tasks", "face · tNN_", "closed · p01"),
                  ("run-delivery-bib", "Export BibTeX", "delivery/", "closed · p02"),
                  ("t01 › r02_<a><y>", "from below", "t01", "complete"),
                  ("t02 › run-section", "from below", "t02", "open")],
                 ["Plan its Tasks", "Add a Task", "Export BibTeX"], 0),
        "Delivery": (["its own (optional)", "jNN_<inquiry>.bib   merged · 10 entries", "from below",
                      "t01   verdict released · web", "t02   landscape: draft"], ["Export BibTeX"])},
    "cowork": {   # one line of work (b13 Q01, 261007): the Block's six Spaces; its items are rows, not Tasks
        "Description": (["jNN_<job>.md: the only place its state is", "state: 🟡 ACTIVE · waiting-on: <person>",
                         "since: <date> · next: <the next step>", "ticket: <office no.> · url",
                         "what we asked for, why, where it stands"], ["Update the Job", "Add a file"]),
        "Idea Studio": ([("s01-<topic>", "", "drawing"), ("s02-<topic>", "", "1 chat")], ["Draw"]),
        "Audience Report": ([("Question", "cites here", "status"), ("q01 <question>", "emails/<thread>", "answered"),
                             ("q02 <question>", "Timeline <date>", "open")], ["Ask a Question"]),
        "Work Details": (["date     item                  state", "<date>   email <thread>        waiting 3 days",
                          "<date>   step 4: <step>        done · decided <x>", "<date>   meeting <topic>       notes",
                          "<date>   email <thread>        draft ✎", "a row opens its file; no Task tab"],
                         ["Add an entry", "Draft an email", "Write meeting notes"], 1),
        "Runs": ([("Run", "type", "writes", "state"), ("run-email-<slug>", "Draft an email", "emails/", "draft · p02"),
                  ("run-meeting-<slug>", "Write meeting notes", "meetings/", "closed · p01"),
                  ("run-face-<jNN>", "Update the Job", "face · Timeline", "closed · p07"),
                  ("run-review-email-<slug>", "Review a draft", "none", "open")],
                 ["Update the Job", "Draft an email", "Write meeting notes", "Review a draft"], 0),
        "Delivery": (["what this Job sent and decided ?", "<date>   sent      <thread>",
                      "<date>   decided   <x>   (Timeline)", "✅ DONE → Block › Delivery ?"], ["Close the Job"])},
    "insight": {   # a DIKW level (JL 261006): the Block's six Spaces; today it is a View of Block › Prototype
        "Description": (["level.md: what this DIKW level asks", "DIKW level: D · what was observed", "opening question: <question>",
                         "questions: 5 live · 1 retired", "shared: src/ · the task configs it calls"],
                        ["Update the DIKW level"]),
        "Idea Studio": ([("s01-<level>-question-map", "", "generated"), ("s02-<topic>", "", "1 chat")],
                        ["Draw the question map", "Draw"]),
        "Audience Report": ([("Logic", "Work", "Report"), ("Question 1 <question>", "E1 → full · ok", "page <id>"),
                             ("Question 2 <question>", "E1 → full · ok", "page <id>"),
                             ("Question 3 <question>", "E2 → not bound", "No answer")],
                            ["Write the Data report", "Check alignment"], 0),
        "Work Details": (["Question · need      partitions   script", "▾ t01_<question>      full · <cut>  ok",
                          "    E1 compute: <spec>  bound", "    E2 cite: <source>   open",
                          "▸ t02_<question>      full          ok", "▸ t03_<question>      —             —",
                          "retired, folded: t04 → t07"],
                         ["Ask a Question", "Review the questions", "Plan the evidence", "Review the evidence plan",
                          "Write the script", "Review the script"], 1),
        "Runs": ([("Run", "type", "writes", "state"), ("run-review-questions", "Review the questions", "j01", "closed · p01"),
                  ("run-plan-evidence-t01", "Plan the evidence", "t01", "open · p02"),
                  ("run-review-plan-t01", "Review the plan", "t01", "waiting"),
                  ("t01 › <dataset>_full", "from below", "t01", "ok")],
                 ["Review the questions", "Plan the evidence", "Review the plan", "Write the script"], 1),
        "Delivery": (["its own (optional)", "the DIKW level's answers, signed", "W: the counsel · the handoff draft",
                      "→ Block › Delivery › Handoff"], ["Write the counsel", "Draft the handoff"])},
    "paper": {"Overview": (["jNN_v<N>.md", "venue: <venue> · deadline <date>", "state: drafting",
                            "task_groups: Main · Appendix"], ["Update the version"]),
              "Sections": (["Section            group     state", "S-<desk>-1-Intro   Main      done ▢",
                            "S-<desk>-2-Method  Main      half ▢", "S-<desk>-A1-<x>    Appendix  new ▢",
                            "pick a Section → the Task tab"], ["Add a Section", "Draft runs"], 2),
              "Delivery": (["its own", "paper.pdf · paper.docx   built", "cover letter · replies", "from below",
                            "S-<desk>-2   fragment built"], ["Build", "Cover letter"])},
    "design": {   # one goal × one method → N designs (JL 261007): the Block's six Spaces
        "Description": (["jNN_<goal>_by-<method>.md", "goal: <job> <venue> for <who>",
                         "keep: <rule> · <rule> · leave out: <x>", "N: 10 designs · close: all verified",
                         "method: M05 By insight · Internal · frozen", "reads: insight W-NN · P01 · P02"],
                        ["Set the goal", "Pick the method"]),
        "Idea Studio": ([("s01-<goal>-elements", "", "drawing"), ("s02-<topic>", "", "1 chat")], ["Draw"]),
        # Audience Report › Design display: the N designs as the reader sees them (JL 261008: "in the
        # Design-Job's Audience Report's Design display to show the Design Items")
        "Audience Report": ([("Design item", "as it shows", "verify", "rank"),
                             ("d01 <slug>", "▢ \"<the message, word for word>\"", "passed", "★ 1"),
                             ("d02 <slug>", "▢ <a screen, for a UI design>", "passed", "2"),
                             ("d03 <slug>", "▢ \"<the message>\"", "revise", "—")],
                            ["Generate N", "Verify", "Rank and keep"], 0),
        "Work Details": (["Design item        changed    state", "▾ t01_d01_<slug>   ask·reason passed",
                          "    \"<the message, word for word>\"", "▸ t02_d02_<slug>   reason     verify",
                          "▸ t03_d03_<slug>   ask        revise", "… t10_d10_<slug>",
                          "pick a design → the Task tab"],
                         ["Generate N", "Verify", "Revise one"], 1),
        "Runs": ([("Run", "type", "writes", "state"), ("run-commission-j01", "Commission", "release", "released"),
                  ("r01_generate_10", "Generate N", "t01-t10", "ok · p01"),
                  ("t02 › r01_verify", "from below", "t02", "open"),
                  ("t03 › run-revise-d03", "from below", "t03", "waiting")],
                 ["Commission", "Generate N", "Verify all", "Compare methods"], 2),
        "Delivery": (["passed Verify, word for word", "d01  \"<message>\"   t01 · released",
                      "d02  \"<message>\"   t04 · released", "designs.csv: goal · method · item · words",
                      "→ Block › Delivery"], ["Release"])},
    "labeling": {   # one dataset × one label (b15 Q01, 261007): the Block's six Spaces; Tasks = the four steps
        "Description": (["jNN_<dataset>_<label>.md", "dataset: <dataset> · items: <N>, fenced",
                         "label: <label> · schema S_<NN> (schema.yaml)", "human: <the person who decides>",
                         "side: Building · or scan only: reads j<NN>'s handoff"], ["Update the Job", "Edit the schema"]),
        "Idea Studio": ([("s01-<label>-boundaries", "", "1 chat")], ["+ Add topic", "Draw"]),
        "Audience Report": ([("Logic", "Work", "Report"), ("ours vs the experts' key", "t04 › r01 ok", "agree <x>%"),
                             ("ours in the raters' spread", "t04 › r02 ok", "inside"),
                             ("where we differ", "t04 › r03 open", "draft")],
                            ["Score against the keys", "Write the report"], 0),
        "Work Details": (["step · Task                  state", "prepare  t01_<dataset>_items   done · r03",
                          "keys     t02_<dataset>_keys    done · blind", "label    t03_<dataset>_labeling",
                          "         G0 ✓ · round 4 · guideline G_03", "score    t04_<dataset>_scoring   waits on D*",
                          "pick a Task → the Task tab"], ["Add a Task", "Plan its Tasks"], 3),
        "Runs": ([("Run", "type", "writes", "state"), ("run-setup-job", "Set up the Job", "face · schema", "closed · p01"),
                  ("run-plan-tasks", "Plan its Tasks", "t01-t04", "closed · p01"),
                  ("t03 › r07_human-calibration", "from below", "t03", "waiting")],
                 ["Set up the Job", "Plan its Tasks", "Edit the schema"], 2),
        "Delivery": (["from below", "t03   handoff  label-v1 · signed", "t03   final labels  D* · audited",
                      "t04   scored set  vs the keys", "→ Block › Delivery"], ["Publish final labels"])},
}

# ── proposed: the Task tab: the Guide, then one screen per Space ───────────────────────────────
# The six Spaces mirror the Block's (JL 261006): Description | Idea Studio · Audience Report |
# Work Details | Runs · Delivery. Audience Report is what the reader gets (a Page: Table · Reading);
# Work Details is how it is made (a Page: Draft-… · Evidence-…). See REPORT_GROUPS, WORK_GROUPS.
# key -> (content lines, Run types, picked line); a tuple line is a Studio topic (name, type, state)
TASK_DEFAULT = {
    "Description": (["tNN_<task>.md", "goal: the one thing this Task finds", "plan: inputs → worker → Runs",
                     "state: built · 2 Runs ok · report half", "close: the report answers its goal"],
                    ["Plan a Task", "Review the plan"]),
    "Idea Studio": ([("s01-analysis-flow", "", "1 chat"), ("s02-question-map", "", "generated")],
                    ["+ Add topic", "Draw"]),
    "Audience Report": (["its Page, as the reader sees it", "usually its face: tNN_<task>.md"], ["Write a report"]),
    "Code": (["how the work is done", "scripts/<worker>.py    the worker", "tests/test_<worker>.py",
              "CODE_REVIEW.md         the review", "notebooks/<run>.ipynb  generated"],
             ["Build the Task", "Review the Task code"]),
    "Displays": (["displays/<fig>/: the Page's figures", "fig1   recipe/plot.py · assets/fig1.png",
                  "fig2   recipe/ · assets/   built", "each one made by run-display-<fig>"],
                 ["Build figure / table"]),
    "Report": ([("q01 <question>", "r01 · r02 ok", "answered"), ("q02 <question>", "r03 open", "draft"),
                ("q03 <question>", "—", "asked")], ["Report the Run", "Write the report"], 0),
    "Runs": (["Run                 type    state   pass", "r01_<slug>/         run     ok      p02",
              "r02_<slug>/         run     failed  p01", "run-build-<task>/   build   closed  p01",
              "run-report-<task>/  report  open    p02", "hard rNN_ · soft run- · runs/README.md"],
             ["Build the Task", "Review the Task code", "Run a Task", "Check a Task"], 1),
    "Delivery": ([], ["Build the report", "Release"]),     # drawn as cards (DELIVERY_CARDS)
}
TASK_GROUPS_BY_SPACE = {   # variant -> Space -> its third row, where it differs from the default
    "Page Task": {"Delivery": []},   # one card per kind of delivery (b16 s13; frame PAGE_TASK_SUBS)
    "paper Section": {"Delivery": ["LaTeX"]},
    "labeling Task": {"Delivery": ["All", "Handoff", "Final labels", "Audit"]},
}
TASK_VARIANT_VIEWS = {
    "Page Task": {
        "Description": (["tNN_<task>.md (the Page)", "its point: the one thing it argues", "page.toml registers it",
                         "owner · reviewer", "close: CHECK closes it", "a paper Section: S-<…>.md · group Main"],
                        ["Context"]),
        "Idea Studio": ([("s01-page-logic", "", "the argument"), ("s02-scratch", "", "rough thinking"),
                         ("S-<…>-roadmap", "", "a Section's logic, by hand")],
                        ["Draw the logic", "Scratch"]),
        # Audience Report = what the reader gets: the plan Table and its Reading (today: Draft › Table, Reading)
        "Table": ([("Section · paragraph", "Evidence items", "State"), ("C1 · P1 <claim>", "E01-value · E03-cite", "written"),
                   ("C1 · P2 <claim>", "E02-display", "written"), ("C2 · P1 <claim>", "—", "open")],
                  ["Structure revise", "Section revise", "Paragraph revise"], 0),
        "Reading": (["the Page as the reader sees it", "Opening", "C1 <section>   written", "C2 <section>   open"],
                    ["Auto write"]),
        # Work Details = how the Page is made: writing rounds and evidence (today: Draft › Scratch, Revise; Evidence)
        "Draft-Scratch": (["rough paragraphs before the Table takes them", "run-scratch-<target>/   p02",
                     "a kept paragraph moves into the Table"], ["Scratch"]),
        "Evidence-Citation": (["item      reads (discovery)   state", "E03-cite  r01_<author><year>  verified",
                       "E05-cite  r04_<author><year>  open", "a verified citation → <stem>.bib",
                       "also here: Evidence-Display · -Value · -Supporting Runs"],
                      ["Bind / update citation", "Build figure / table", "Bind / update value"]),
        "Runs": (["Run (all soft here)      type       state", "run-structure-<target>/  structure  closed",
                  "run-section-c2/          section    open", "run-display-fig2/        display    ok",
                  "run-delivery-latex/      delivery   ok"], ["Section revise", "Build"]),
        "Delivery": (["its own", "d01-web    web     run-delivery-webpage", "d02-latex  LaTeX   run-delivery-latex",
                      "d03-word   Word    run-delivery-word", "a Section: latex/S-<…>.tex, its fragment"],
                     ["Build", "Check"])},
    "paper Section": {
        "Description": (["S-<desk>-<N>-<Section>.md", "its job in the paper: claim C<n>", "group: Main · place 3 of 9",
                         "plan: S-<…>-draft-v<G>.<S>.md", "close: its Page check passes"], ["Context"]),
        "Idea Studio": ([("S-<…>-roadmap", "", "the logic, by hand"), ("S-<…>-sections", "drawing",
                                                                                "the Section map, generated")],
                        ["Draw the logic", "Redraw the Section map"]),
        "Report": (["the Section as the reader sees it", "P1 <topic sentence>", "P2 <topic sentence>",
                    "P3 <topic sentence>", "today: Draft › Reading"], ["Auto write"]),
        "Draft": (["paragraph    state", "P1-P3        written", "P4           open",
                   "plan: S-<…>-draft-v<G>.<S>.md"], ["Draft runs", "Section revise"]),
        "Evidence": (["item        kind      reads", "E01-value   value     a work Task's Result",
                      "E02-cite    citation  a discovery Result"], ["Evidence runs"]),
        "Runs": (["Run (all soft here)      type       state", "run-structure-<target>/  structure  closed",
                  "run-section-<target>/    section    open", "run-value-<E01>/         evidence   ok",
                  "run-delivery-latex/      delivery   ok"], ["Draft runs", "Delivery runs"]),
        "Delivery": (["its own", "latex/S-<…>.tex   the fragment", "the paper pulls it in when it builds"],
                     ["Delivery runs"])},
    "discovery Task": {   # a Page that makes facts: hard Paper Runs, and its Page's soft Runs (b14 Q01, 261007)
        "Description": (["tNN_<task>.md · discovery.yaml", "asks: <the sub-question>", "type: prior-art-verdict",
                         "boundary: <years · fields · source kinds>", "admission: candidate rule v1, frozen",
                         "close: CHECK passes · 6 of 6 read"], ["Scope the Task", "Freeze the rule"]),
        "Idea Studio": ([("s01-<task>-clusters", "", "drawing"), ("s02-<topic>", "", "1 chat")], ["Draw"]),
        # Audience Report: Question │ Work │ Report (JL 261007, s13 1f): its divisions, the papers each reads
        "Table": ([("Division · ask", "Papers read", "State"), ("C1 <closest prior work>", "r01 · r02", "written"),
                   ("C2 <where they differ>", "r03 · r04", "written"), ("C3 <the gap>", "—", "open")],
                  ["Synthesize a Task", "Section revise"], 0),
        "Reading": (["the article as the reader sees it", "Opening: the answer in one line", "C1 <division>   written",
                     "C2 <division>   open"], ["Synthesize a Task"]),
        # Work Details: how it is made: its papers (the Result Cards), the screened candidates, the Page's plan
        "Papers": (["paper                 depth     claim    cite", "r01_<author><year>    full      support  ok",
                    "r02_<author><year>    abstract  partial  verify", "r03_<author><year>    —         —        running",
                    "each opens its Result Card: facts · Bib", "grouped by role ? (Q02)"],
                   ["Read a paper", "Review a Run", "Verify a citation"], 1),
        "Intake": (["candidate            disposition  why", "doi:<…>              admitted     → r01",
                    "s2:<record>          excluded     off-topic", "doi:<…>              unresolved   no population",
                    "from discovery.yaml: candidate_decisions"], ["Find papers", "Admit a candidate"]),
        "Draft": (["the Page's plan: draft/<stem>-draft-v<G>.<S>.md", "evidence items: E01-cite → r01 · …",
                   "Evidence Bib: draft/evidence/bibex/<task>.bib"], ["Structure revise"]),
        "Runs": (["Run                         type   state", "r01_<author><year>_<subj>/  read   complete · p01",
                  "r02_<author><year>_<subj>/  read   complete · p02", "run-section-c2/             write  open",
                  "run-check-<task>/           check  waiting", "hard rNN_ (one paper) · soft run-"],
                 ["Find papers", "Read a paper", "Synthesize a Task", "Check a Task"], 1),
        "Delivery": ([], ["Build the article", "Export BibTeX"])},     # drawn as cards (DELIVERY_CARDS)
    "insight question": {
        "Description": (["tNN_<question>.md (answering Page)", "question.md · DIKW level D", "needs: E1 · E2"],
                        ["Plan the evidence"]),
        "Partitions": (["partition   result   page", "<p1>        ok       written", "<p2>        ok       open",
                        "<p3>        —        —"], ["Run a partition", "Write the Data report"]),
        "Runs": (["Run                        kind  state", "<dataset>_<p1>/            hard  ok",
                  "<dataset>_<p2>/            hard  ok", "run-check-<target>/        soft  open"],
                 ["Run a partition", "Check alignment"])},
    "design folder": {
        "Description": (["Design-NN-<slug>.md", "the design task: venue · who · rules"], ["Frame the aim"]),
        "Design Task": (["aim · requirements · resources", "leave out: <x>"], ["Set the rules"]),
        "Design Item": (["card            state", "D1  <design>    passed", "D2  <design>    verify"],
                        ["Generate", "Verify"]),
        "Runs": (["Run                          state", "run-commission-<target>/     released ?",
                  "rNN_generate_<slug>/         hard  ok", "rNN_verify_<slug>/           hard  ok"],
                 ["Commission", "Generate", "Verify"]),
        "Delivery": (["its own", "passed designs · designs.csv"], ["Passed review"])},
    "labeling Task": {   # the Job's label step: one engine job in labeling/ (b15 Q01, 261007)
        "Description": (["tNN_<dataset>_labeling.md (page-type: labeling)", "contract: labeling/config.yaml",
                         "items: the bound package from t01 · <N>", "test: <M> held back, sealed",
                         "human: <the person> · custodian: <x>", "today: Data › Contract"],
                        ["Create the job"]),
        "Idea Studio": ([("s01-<label>-edge-cases", "", "1 chat")], ["+ Add topic", "Draw"]),
        "Report": (["REPORT.md, as the reader sees it", "phase: Round · gate: G0 ✓", "guideline G_03: cheatsheet · gallery",
                    "gold: <N> confirmed · regions covered 5/7", "next: close round 4", "rendered, never authority"],
                   ["Render the report"]),
        "Rounds": (["round      items      state", "round_01   20 judged  closed · G_01",
                    "round_04   12 / 20    open · yours to label", "card · prospect · judgments · rules · result",
                    "Building: Embedding · Definition · Rounds · Guideline", "Scanning: Test · Evaluation · Scan · Audit"],
                   ["Start a round", "Label the round", "Learn the guideline", "Measure", "Close the round"], 2),
        "Runs": (["Run                              side      state", "r01_corpus-contract/             Building  ok",
                  "r05_definition-discussion/       Building  ok", "r07_human-calibration_round04/   Building  waiting",
                  "r14_test-gold-lock/              Scanning  —", "README.md: 26 types · the gates are no Runs"],
                 ["Prepare a round", "Label the round", "Freeze the handoff", "Score executors", "Scan", "Audit"], 3),
        "Delivery": (["handoff/label-v1.yaml   signed · the crossing", "corpus/final/D_star    audited",
                      "audit/final_01/report.md", "delivery/ ? a csv export for readers", "→ Job › Delivery"],
                     ["Freeze the handoff", "Publish final labels"])},
}
# JL 261006, on s13: the Task's Audience Report holds its writing ("this can be draft / report /
# etc."), one screen per group; its Work Details holds the Runs, grouped by run type (runtype1 · runtype2).
# A work Task's report is one screen, Question │ Work │ Report, as on the Block (JL 261006: "one is
# necessary for the task"; a task-level report is not used much).
# Audience Report and Work Details: one screen each, its subspaces as the third row (JL 261006). A Page's
# today's Draft and Evidence split: what the reader gets (Table · Reading) and how it is made (the rest).
# a Page's Questions: its own register rows, a third view beside the two (b16 s13 Decided 4, 261007)
REPORT_GROUPS = {"work Task": ["Report", "Draft"],   # Draft: its Page's view, as the frame adds it (261008) "Page Task": ["Table", "Reading", "Questions"],
                 "labeling Task": ["Report"],   # b15 Q01: REPORT.md only; the guideline's cheatsheet inside it
                 "discovery Task": ["Table", "Reading"],   # b14 Q01: a Page; its Table is Question │ Work │ Report
                 "paper Section": ["Table", "Reading", "Questions", "Reviews"]}   # Reviews: paper only (JL 261007)
WORK_GROUPS = {"work Task": ["Code", "Review", "Notebooks"],
               "discovery Task": ["Papers", "Intake", "Draft"],   # b14 Q01: its Result Cards, its screening, its plan
               # b15 Q01: today's Data · Labeling · Quality views, by side (b15 Q02)
               "labeling Task": ["Embedding", "Definition", "Rounds", "Guideline", "|",
                                 "Test", "Evaluation", "Scan", "Audit"],
               "Page Task": ["Draft-Scratch", "Draft-Revise", "Evidence-Citation", "Evidence-Display",
                                 "Evidence-Value", "Evidence-Supporting"],   # as the frame (PAGE_TASK_SUBS)
               "paper Section": ["Draft-Scratch", "Draft-Revise", "Evidence-Citation", "Evidence-Display",
                                 "Evidence-Value", "Evidence-Supporting Runs"]}
OPEN_GROUP = {("labeling Task", "Work Details"): "Rounds", ("work Task", "Audience Report"): "Report", ("Page Task", "Work Details"): "Evidence-Citation",
              ("paper Section", "Work Details"): "Evidence-Citation"}   # the subspace each screen shows open; default the first
# a work Task's Page views (JL 261008, "merge them into the base"): the frame adds them after each
# Space's own views (frame.py PAGE_VIEWS: the old /_board/draft, /evidence, … routes, now ?view=)
PAGE_VIEW_SUBS = {"Description": ["Folder"], "Work Details": ["Evidence", "Value"], "Runs": ["Page Runs"],
                  "Delivery": ["Lanes"]}
PAGE_VIEW_TASKS = {"work Task"}
RUN_GROUPS = {"work Task": ["All", "run", "build", "report"], "labeling Task": ["All", "Building", "Scanning"],
              "discovery Task": ["All", "read", "write", "check", "delivery"],   # b14 Q01
              "Page Task": [],   # no third row: the Page's own Runs view, by lane (b16 s13; frame PAGE_TASK_SUBS)
              "paper Section": ["All", "structure", "section", "evidence", "delivery"]}
# A work Task's Delivery: no third row; today's style, its items as cards under group headings (JL 261006)
DELIVERY_CARDS = {"work Task": [("Reports", [("d01-report", "web · LaTeX · released"), ("d02-report", "draft")]),
                                ("Exports", [("d03-<table>", "csv → j11 › Delivery")])],
                  "discovery Task": [("Article", [("d01-web", "the synthesis, built · released")]),   # b14 Q01
                                     ("Export", [("tNN_<task>.bib", "derived → Job · Block")])]}
# a DIKW level's third rows and its notes, one per Space
DIKW_ROWS = {"Description": ["Level", "Shared code"], "Idea Studio": [], "Audience Report": ["Full", "<cut>", "<cut>", "Cross"],
             "Work Details": ["All", "live", "retired"], "Runs": ["All", "review", "plan", "script", "from below"],
             "Delivery": []}
# a design Job's third rows and notes (JL 261007): one goal, one method, N designs
DESIGN_ROWS = {"Description": ["Goal", "Method", "Resources"], "Idea Studio": [],
               "Audience Report": ["Reason ideas", "Design display", "Review whole", "Predicted vs observed",
                                   "Performance"],   # the design theme's five views (JL 261008)
               "Work Details": ["All", "passed", "verify", "revise"],
               "Runs": ["All", "commission", "generate", "verify", "revise"], "Delivery": []}
FAMILY_OPEN = {("design", "Audience Report"): "Design display"}   # the view a Job screen shows open
DESIGN_NOTES = {"Description": "the Brief's row for this goal + method.md: ① see ② do ③ check",
                "Idea Studio": "drawings while designing: element ideas, sketches",
                "Audience Report": "✎ 261008 Design display: each design item as it shows, word for word",
                "Work Details": "one Task per design: Design · Rationale · Evaluation",
                "Runs": "Generate is the Job's: one Run makes N drafts, opens N Tasks ?",
                "Delivery": "step 5 Release, by a person; step 6, the Exp, is outside"}
DIKW_NOTES = {"Description": "level.md, and Meta's counts for this DIKW level only",
              "Idea Studio": "this DIKW level's part of the question map ?",
              "Audience Report": "the Block's Insight table, this DIKW level's rows only",
              "Work Details": "was Block › Prototype › Data: its questions = Tasks",
              "Runs": "the design runs; its questions' hard Runs from below",
              "Delivery": "only j04_wisdom delivers; D · I · K hand answers up ?"}
# a cowork Job's third rows and notes (b13 Q01, 261007): one line of work; emails and meetings are rows
COWORK_ROWS = {"Description": ["Job", "Files"], "Idea Studio": [], "Audience Report": [],
               "Work Details": ["Timeline", "Checklist", "Emails", "Meetings"],
               "Runs": ["All", "email", "notes", "update", "check"], "Delivery": []}
COWORK_NOTES = {"Description": "the job page: its header is the Job's only state",
                "Idea Studio": "optional: drawings; today's design/ drawings move here ?",
                "Audience Report": "optional: the Block's Questions that cite this Job, from above",
                "Work Details": "rows, not Tasks: Timeline (all, by date) · Checklist · Emails · Meetings",
                "Runs": "soft only: a draft is a Run until the person sends it (Q02)",
                "Delivery": "what it sent and decided; done Jobs roll up (Q03) ?"}
# a labeling Job's third rows and notes (b15 Q01, 261007): one dataset × one label, four step Tasks
LABELING_ROWS = {"Description": ["Dataset", "Label", "Resources"], "Idea Studio": [],
                 "Audience Report": ["Scored", "Building"],
                 "Work Details": ["All", "prepare", "keys", "label", "score"],
                 "Runs": ["All", "setup", "from below"], "Delivery": []}
LABELING_NOTES = {"Description": "the face + schema.yaml: one label, by version (Q03 ?)",
                  "Idea Studio": "optional: drawings of the label's edges",
                  "Audience Report": "was Quality › External gold: our labels vs the dataset's keys",
                  "Work Details": "was Data › Preparation (the data Tasks) + the labeling page",
                  "Runs": "soft only; the operations are the label Task's",
                  "Delivery": "rolls up t03's handoff + D*, t04's scored set"}
# a discovery Job's third rows and notes (b14 Q01, 261007): one inquiry, its sub-question Tasks
DISCOVERY_ROWS = {"Description": ["Inquiry", "Resources"], "Idea Studio": [], "Audience Report": [],
                  "Work Details": ["All", "Search", "Review", "Synthesize"],
                  "Runs": ["All", "plan", "delivery", "from below"], "Delivery": []}
DISCOVERY_NOTES = {"Description": "jNN_<inquiry>.md: today a job: block in each Task's discovery.yaml ?",
                   "Idea Studio": "optional drawings; no Job has one on disk today",
                   "Audience Report": "its Tasks' answers, one row each: a view, no reports/",
                   "Work Details": "was Work › Tasks; grouped by discovery_type's specialist",
                   "Runs": "soft only; its Tasks' Paper Runs from below",
                   "Delivery": "the merged Bib; a synthesis across Tasks = a Task ?"}
COLUMNS = {}   # variant -> the keys of its proposed screens, left to right: today lines up under them
SPACES = {}    # variant -> the Space of each of those screens: the blockers go between their groups


def cards(x, y, groups):
    """Today's style for a Delivery: a heading per group, one card per item beneath it."""
    for name, items in groups:
        text(x, y, name, 12, INK)
        y += 20
        for title, note in items:
            base("rectangle", x, y, L.UI_W - 190 - 36, 30, GRAY, 1)   # inside the content, left of Disk · Runs
            text(x + 10, y + 7, title, 12, INK, L.MONO)
            text(x + 130, y + 8, note, 11, GRAY)
            y += 38
        y += 6


def task_screens(variant):
    """(Space, open group, content key, its third row) for each proposed screen of the Task tab."""
    parts = L.TASK_PARTS.get(variant, [])
    own = TASK_GROUPS_BY_SPACE.get(variant, {})
    desc = L.TASK_DESCRIPTION.get(variant, ["Scope", "Plan", "Records"])
    pv = PAGE_VIEW_SUBS if variant in PAGE_VIEW_TASKS else {}
    desc = list(desc) + pv.get("Description", [])
    out = [("Description", desc[0], "Description", desc),
           ("Idea Studio", None, "Idea Studio", [])]   # no third row: one drawing after another (JL 261006)
    if variant in REPORT_GROUPS:                         # the writing: draft / evidence / report
        for space, gs in (("Audience Report", REPORT_GROUPS[variant]), ("Work Details", WORK_GROUPS[variant])):
            g = OPEN_GROUP.get((variant, space), gs[0])
            out.append((space, g, g, gs + pv.get(space, [])))
        rg = RUN_GROUPS[variant] + pv.get("Runs", [])
        out.append(("Runs", "All" if rg else None, "Runs", rg))
        deliv = [] if variant in DELIVERY_CARDS else own.get("Delivery", L.GROUP_ROWS["Delivery"])
        out.append(("Delivery", None, "Delivery", (["Files"] if pv and not deliv else deliv) + pv.get("Delivery", [])))
        return out
    out.append(("Audience Report", None, "Audience Report", own.get("Audience Report", [])))
    out += [("Work Details", g, g, parts) for g in parts]   # other variants: their parts, then the Runs
    out.append(("Runs", None, "Runs", []))
    out.append(("Delivery", None, "Delivery", own.get("Delivery", L.GROUP_ROWS["Delivery"])))
    return out


def task_proposed(x, y, variant):
    """The Guide, then one screen per Space of the Task tab (one per group of Work Details)."""
    family = TASK_FAMILY[variant]
    own = TASK_VARIANT_VIEWS.get(variant, {})
    text(x, y, "proposed · the Guide, then the Task tab: one screen per Space (and per group of Audience Report)",
         16, TEAL)
    g = L.VIEW_DEFAULT["Guide"]
    bottom = L.wireframe(x, y + 30, (family, "Guide", variant, "Description", None, "lines", "", ""), lines=g[0],
                         runs=g[1], header=f"{variant} · Guide › Description", groups=[])
    keys, spaces = ["Guide"], ["Guide"]
    for i, (space, group, key, row) in enumerate(task_screens(variant), start=1):
        if not space:                                    # an empty slot where a dropped screen was
            text(x + i * (L.UI_W + GAP), y + 30, "(Draft dropped: one report screen is enough)", 13, GRAY)
            keys.append("")
            spaces.append("")
            continue
        spec = own.get(key) or TASK_DEFAULT.get(key) or ([key, "(to fill)"], ["—"])
        lines, runs = spec[0], spec[1]
        pick = spec[2] if len(spec) > 2 else None
        tup = bool(lines) and isinstance(lines[0], tuple)
        body = "studio" if key == "Idea Studio" else "table" if key == "Table" else "qwr" if tup else "lines"
        if key == "Delivery" and variant in DELIVERY_CARDS and variant not in PAGE_VIEW_TASKS:
            row = []                                     # no third row: groups are headings over cards
        sp_ = (family, "Task", variant, space, group, body, "", "")
        head = f"{variant} · Task › {space}" + (f" › {group}" if group else "")
        sx = x + i * (L.UI_W + GAP)
        bottom = max(bottom, L.wireframe(sx, y + 30, sp_, lines=lines, runs=runs, pick=pick, header=head, groups=row, wrap=True))
        if key == "Delivery" and variant in DELIVERY_CARDS:
            cards(sx + 12, y + 30 + 24 + 80 + (28 if row else 0), DELIVERY_CARDS[variant])
        keys.append(key)
        spaces.append(space)
    COLUMNS[variant] = keys
    SPACES[variant] = spaces
    return bottom


def task_dividers(x0, top, bottom, variant):
    """The blockers, as on the Block rows (JL 261006): a line down the row before each group of Spaces,
    the groups of the bars in the Spaces row: Guide | Description | Idea Studio · Audience Report |
    Work Details | Runs · Delivery."""
    groups, cur = [["Guide"]], []
    for s in L.level_subs(TASK_FAMILY[variant], "Task", variant) + ["|"]:
        if s == "|":
            groups.append(cur)
            cur = []
        else:
            cur.append(s.lstrip("~"))
    group_of = {s: k for k, g in enumerate(groups) for s in g}
    last = None
    for i, space in enumerate(SPACES.get(variant, [])):
        if space and group_of.get(space, last) != last:
            gx = x0 + i * (L.UI_W + GAP) - GAP / 2
            path([(gx, top), (gx, bottom)], arrow=False, color=INK)
            last = group_of[space]


def job_dividers(x0, top, bottom, variant):
    """The blockers on the Job rows, as on the Block and Task rows: a line down the row before each
    group of the Job tab's Spaces, Overview · Studio · Reports | its children | Runs · Delivery
    (no Guide screen on this row)."""
    groups, cur = [], []
    for s in L.level_subs(JOB_FAMILY[variant], "Job", variant) + ["|"]:
        if s == "|":
            groups.append(cur)
            cur = []
        else:
            cur.append(s.lstrip("~"))
    group_of = {s: k for k, g in enumerate(groups) for s in g}
    last = None
    for i, space in enumerate(SPACES.get(variant, [])):
        if group_of.get(space, last) != last:
            gx = x0 + i * (L.UI_W + GAP) - GAP / 2
            path([(gx, top), (gx, bottom)], arrow=False, color=INK)
            last = group_of[space]


def proposed(x, y, variant, level):
    """One proposed screen per Space of the Job or Task tab; returns the bottom."""
    family = (JOB_FAMILY if level == "Job" else TASK_FAMILY)[variant]
    spaces = [s.lstrip("~") for s in L.level_subs(family, level, variant) if s != "|"]
    own = (JOB_FAMILY_VIEWS.get(family, {}) if level == "Job" else TASK_VARIANT_VIEWS.get(variant, {}))
    default = JOB_DEFAULT if level == "Job" else TASK_DEFAULT
    text(x, y, f"proposed · the {level} tab, one screen per Space", 16, TEAL)
    bottom = y
    fam_rows, fam_notes = ({"insight": (DIKW_ROWS, DIKW_NOTES), "design": (DESIGN_ROWS, DESIGN_NOTES),
                            "cowork": (COWORK_ROWS, COWORK_NOTES),
                            "labeling": (LABELING_ROWS, LABELING_NOTES),   # b15 Q01
                            "discovery": (DISCOVERY_ROWS, DISCOVERY_NOTES)}   # b14 Q01
                           .get(family, (None, None)) if level == "Job" else (None, None))
    for i, space in enumerate(spaces):
        spec = own.get(space) or default.get(space) or ([f"{space}", "(to fill)"], ["—"])
        lines, runs = spec[0], spec[1]
        pick = spec[2] if len(spec) > 2 else None
        tup = bool(lines) and isinstance(lines[0], tuple)
        body = "studio" if space == "Idea Studio" and tup else "table" if tup else "lines"
        row = fam_rows.get(space) if fam_rows else None
        opened = FAMILY_OPEN.get((family, space)) or (row[0] if row else None)
        sp_ = (family, level, variant, space, opened, body, "", fam_notes.get(space, "") if fam_notes else "")
        head = f"{variant} · {level} › {space}" + (f" › {opened}" if row else "")
        bottom = max(bottom, L.wireframe(x + i * (L.UI_W + GAP), y + 30, sp_, lines=lines, runs=runs, pick=pick,
                                         header=head, groups=row))
    COLUMNS[variant] = spaces
    SPACES[variant] = spaces
    return bottom


# ── today: the variant as the current workbench shows it, read from the server code ─────────────
# (workbench, level) -> [(Space, [Views])], as the server renders them (checked 261006 in
# Tools/plugins/haipipe-toolkit/servers and subjective-label/servers). Run buttons per View come from
# the family's workbench-table.md where the server reads it; SERVER_RUNS overrides where it does not.
GUIDE = ("Guide", ["Description", "Method", "RoadMap Draw", "Related Paper"])
SERVER = {
    ("task", "board"): [GUIDE, ("Scope", ["Block", "Questions", "Resources", "RoadMap Draw"]),
                        ("Task", ["<group A>", "<group B>", "Not under a Question"]),
                        ("Check", ["Runs", "Tasks", "Reports"]), ("Delivery", ["Reports"])],
    ("discovery", "board"): [GUIDE, ("Scope", ["Block", "Questions", "Resources", "RoadMap Draw"]),
                             ("Work", ["Papers", "Tasks", "Questions"]), ("Check", ["Runs", "Citations", "Reports"]),
                             ("Delivery", ["Reports", "BibTeX"])],
    ("cowork", "board"): [GUIDE, ("Scope", ["Block", "People", "Resources", "RoadMap Draw"]),
                          ("Work", ["Jobs", "Questions", "Emails", "Meetings"]),
                          ("Check", ["Waiting on", "Drafts", "Reports"]), ("Delivery", ["Reports", "Done jobs"])],
    ("page", "page"): [GUIDE, ("Draft", ["Table", "Reading", "Scratch", "RoadMap Draw", "Revise"]),
                       ("Evidence", ["Citations", "Displays", "Values", "Supporting Runs"]),
                       ("Delivery", ["Web", "LaTeX", "Word", "Slides"])],
    ("paper", "board"): [GUIDE, ("Ideation", []),
                         ("Story", ["Spine", "RoadMap Draw", "High-level logic + Low-level work", "Related Papers"]),
                         ("Sections", ["Main", "Appendix"]), ("Delivery", ["LaTeX", "Word", "Cover letter", "Rounds"])],
    ("insight", "board"): [GUIDE, ("Scope", ["Dataset", "Partitions", "Questions"]),
                           ("Prototype", ["Meta", "Data", "Information", "Knowledge", "Wisdom", "RoadMap Draw"]),
                           ("Insight", ["Full", "<partition>", "Cross"]), ("Check", ["Gates", "Checks", "Runtime"]),
                           ("Delivery", ["Handoff"])],
    ("design", "board"): [GUIDE, ("Design Tasks", ["<method family>", "<method family>"])],
    ("design", "page"): [GUIDE, ("Design Task", ["Aim", "Requirements", "Resources", "Leave out"]),
                         ("Design Item", []), ("Delivery", [])],
    ("labeling", "board"): [GUIDE, ("Jobs", [])],
    ("labeling", "page"): [GUIDE, ("Data", ["Preparation", "Contract", "Embedding"]),
                           ("Labeling", ["Definition", "Rounds", "Guideline"]),
                           ("Quality", ["Test", "Evaluation", "Audit", "External gold"]),
                           ("Delivery", ["Handoff", "Scan", "Final labels"])],
}
SERVER_RUNS = {  # hard-coded in insightboard.py, not read from any table
    ("insight", "Scope"): ["Prepare extract", "Ask"],
    ("insight", "Insight"): ["Data runs", "Information runs", "Report", "Pool or split"],
    ("insight", "Check"): ["Mechanical check", "Answer review"],
    ("insight", "Delivery"): ["Handoff draft"],
}
# variant -> (workbench, level, the Spaces to show (None = all), what today looks like, the gap in red)
TODAY = {
    "work Block": ("task", "board", None, "the Task workbench, board level",
                   "matches its table; Task's Views are the Question groups"),
    "discovery Block": ("discovery", "board", None, "the Discovery workbench, board level", "matches its table"),
    "cowork Block": ("cowork", "board", None, "the CoWork workbench, board level",
                     "no Task anywhere; the Runs panel never lists run instances; no Runs list"),
    "paper Board": ("paper", "board", None, "the Paper workbench, board level",
                    "Ideation has no Views; Runs panel reads run-cards.md, not the table; no Runs list"),
    "insight Block (DIKW)": ("insight", "board", None, "the Insight workbench, board level",
                             "Runs panel hard-coded in Python: differs from the table in every Space"),
    "insight register board": ("insight", "board", None, "the Insight workbench, board level",
                               "a register board shows only a note in Prototype"),
    "design Board": ("design", "board", None, "the Design workbench, board level",
                     "Views are method families, not the table's Task list · Shared rules"),
    "labeling Block": ("labeling", "board", None, "the Labeling workbench, board level",
                       "one Space, Jobs: each labeling Job is a row"),
    "work Job": ("task", "board", ["Scope", "Task", "Check"], "no Job screen: a Job is spread over 3 places",
                 "Scope › Block lists it · a line in each Task Work tree · a column in Check › Tasks"),
    "Page Job": ("task", "board", ["Scope", "Task", "Check"], "no Job screen: a Job is spread over 3 places",
                 "Scope › Block lists it · a line in each Task Work tree · a column in Check › Tasks"),
    "discovery Job": ("discovery", "board", ["Scope", "Work"], "no Job screen: a Job is spread over 2 places",
                      "Scope › Block lists it · headings in Work › Papers · a column in Work › Tasks"),
    "cowork Job": ("cowork", "board", ["Work", "Check", "Delivery"], "the Job is CoWork's main unit",
                   "a row in Work › Jobs · Check › Waiting on and Drafts · Delivery › Done jobs"),
    "paper version": ("paper", "board", ["Story"], "no version today",
                      "a Job is only a line in Story's Block → Job → Task → Run tree"),
    "DIKW level": ("insight", "board", ["Prototype", "Insight"], "a DIKW level is a View of Prototype, rows in Insight",
                  "j01_data … j04_wisdom = Prototype's Views; its answers mixed into each partition's table"),
    "design method": ("design", "board", None, "a method folder 2-Design-M<NN>/ is the nearest Job",
                      "it holds every goal; one goal is a Design folder; no Job tab, a board View"),
    "labeling Job": ("labeling", "page", ["Data", "Quality"], "no Job screen: the labeling page reaches up",
                     "Data › Preparation lists the Job's data Tasks; Quality › External gold reads t04"),
    "work Task": ("task", "board", ["Task", "Check"], "no Task screen: a line in the Task Work tree",
                  "its 'Task Page' link opens the Page workbench as a pop-out; a row in Check › Tasks"),
    "Page Task": ("page", "page", None, "the Page workbench (a paper Section opens here too)",
                  "a hidden Run lens (?lens=run) has no button; Runs panel reads run-cards.md"),
    "paper Section": ("page", "page", None, "the Page workbench: a Section opens here",
                      "the paper workbench lists it as a row of Sections; Story's tree has no link to it"),
    "discovery Task": ("discovery", "board", ["Work"], "a row in Work › Tasks; opens the Page workbench",
                       "also a heading in Work › Papers"),
    "insight question": ("insight", "board", ["Prototype", "Insight"], "a row in its DIKW level View and in each partition",
                         "its page and Runs open as pop-outs; no Task screen"),
    "design folder": ("design", "page", None, "the design page level: the folder's own screen",
                      "Design Item and Delivery render no View tabs (the table lists some)"),
    "labeling Task": ("labeling", "page", None, "the page-level workbench = the labeling Task's screen",
                      "four Spaces, not six; Scan sits in Delivery; Runs dated run-labeling-<op>-<MMDD>-…"),
}


# today's Space -> the proposed column it sits under (Block: build_ladder_v4.BLOCK_COLUMNS; Job: its Spaces)
BLOCK_UNDER = {"Guide": "Guide", "Scope": "Scope", "Prototype": "Jobs", "Insight": "Reports", "Check": "Runs",
               "Delivery": "Delivery", "Task": "Reports", "Work": "Jobs", "Ideation": "Studio", "Story": "Reports",
               "Sections": "Jobs", "Design Tasks": "Jobs", "Jobs": "Jobs"}
JOB_UNDER = {"Scope": ["Description", "Overview"], "Prototype": ["Work Details"], "Insight": ["Audience Report"],
             "Task": ["Tasks"], "Work": ["Tasks", "Work Details", "Overview"], "Check": ["Runs"], "Story": ["Overview"],
             "Design Tasks": ["Work Details", "Design folders"],
             "Data": ["Work Details"], "Quality": ["Audience Report"]}   # labeling (b15 Q01)


def under(variant, space, cols):
    """The proposed column today's Space sits under, or None (then the next free one)."""
    if variant in TASK_FAMILY:
        key = {"Task": "Runs"}.get(space, space)
        if key in cols:
            return key
        sps = SPACES.get(variant, [])                # a Page's today Draft and Evidence: split (JL 261006)
        sp_ = {"Draft": "Audience Report", "Evidence": "Work Details",   # an insight question (JL 261007):
               "Prototype": "Description", "Insight": "Work Details",   # its ask · its partitions
               "Data": "Description", "Labeling": "Work Details",       # a labeling Task (b15 Q01)
               "Quality": "Audience Report",
               "Work": "Work Details"}.get(space)                       # a discovery Task (b14 Q01)
        return cols[sps.index(sp_)] if sp_ in sps else None
    if variant in JOB_FAMILY:
        return next((k for k in JOB_UNDER.get(space, [space]) if k in cols), None)
    key = BLOCK_UNDER.get(space)
    return key if key in cols else None


def today_screen(x, y, header, tabs, open_tab, views, runs):
    """A plain screen in today's layout: Space tabs, the open Space's views, its run buttons."""
    W, H, RUNS = L.UI_W, L.UI_H, 160
    text(x, y, header, 13, GRAY)
    y += 24
    base("rectangle", x, y, W, H, GRAY, 1, dashed=True)          # dashed: today, not the proposal

    def row(names, open_name, ty, h, size, gap, x0):
        tx = x0
        for n in names:
            w = len(n) * size * 0.58 + 14
            if tx + w > x + W - 10:
                text(tx, ty + 3, "…", size, GRAY)
                break
            on = n == open_name
            base("rectangle", tx, ty, w, h, INK if on else GRAY, 1.5 if on else 1)
            text(tx + 7, ty + (h - size * 1.25) / 2, n, size, INK if on else GRAY)
            tx += w + gap

    row(tabs, open_tab, y + 8, 24, 12, 6, x + 10)
    path([(x, y + 38), (x + W, y + 38)], arrow=False, color=GRAY)
    row([v for v, _ in views], views[0][0] if views else None, y + 44, 20, 11, 4, x + 10)
    path([(x, y + 70), (x + W, y + 70)], arrow=False, color=GRAY)
    path([(x + W - RUNS, y + 70), (x + W - RUNS, y + H)], arrow=False, color=GRAY)
    for k, (v, rs) in enumerate(views[:7]):
        text(x + 16, y + 84 + k * 24, f"{v}", 12, INK if k == 0 else GRAY)
        text(x + 16 + 190, y + 84 + k * 24, f"{len(rs)} run button{'s' if len(rs) != 1 else ''}", 11, GRAY)
    text(x + W - RUNS + 10, y + 80, "Runs", 12, INK)
    for k, r in enumerate(runs[:6]):
        text(x + W - RUNS + 10, y + 102 + k * 20, "▸ " + L.short(r, 19), 12, GRAY)
    if len(runs) > 6:
        text(x + W - RUNS + 10, y + 102 + 6 * 20, f"+{len(runs) - 6} more", 12, GRAY)
    return y + H + 34


def today(x, y, variant):
    """Today's screens for one variant, as the server renders them; returns the bottom."""
    bench, level, only, what, gap = TODAY[variant]
    table = {(sp, v): rs for lvl, sp, vs in L.ui_tree(L.UI_TABLES[bench]) if lvl == level for v, rs in vs}
    layout = SERVER[(bench, level)]
    tabs = [sp for sp, _ in layout]
    text(x, y, f"today · {what}   (read from the server code; dashed)", 16, GRAY)
    text(x, y + 22, "differs: " + gap, 13, RED)
    bottom = y + 40
    shown = [(sp, vs) for sp, vs in layout if only is None or sp in only]
    cols = COLUMNS.get(variant)                      # each of today's screens under its proposed one
    nxt = len(cols) if cols else 0
    used = set()
    for i, (space, view_names) in enumerate(shown):
        col = i
        if cols:
            key = under(variant, space, cols)
            if key is not None and cols.index(key) not in used:
                col = cols.index(key)
            else:
                col, nxt = nxt, nxt + 1
            used.add(col)
        views = [(v, table.get((space, v)) or (table.get((space, "each group")) or table.get((space, "each partition"))
                                                 if v.startswith("<") or v == "Full" else []) or [])
                 for v in view_names]                # a View made per group or partition: the table's "each …" row
        runs = SERVER_RUNS.get((bench, space)) or [r["Run"] for (sp, _), rs in table.items() if sp == space
                                                    for r in rs]
        bottom = max(bottom, today_screen(x + col * (L.UI_W + GAP), y + 56, f"{bench} › {level} › {space}", tabs,
                                          space, views, list(dict.fromkeys(runs))))
    return bottom


def rows(level):
    """The screens column for draw_trees(views=…): the proposal on top, today underneath."""
    def draw(x, y, variant):
        top = (L.block_views(x, y, variant) if level == "Block" else task_proposed(x, y, variant) if level == "Task"
               else proposed(x, y, variant, level))
        if level == "Block":                         # the Block's columns: today lines up under them
            COLUMNS[variant] = L.BLOCK_VIEW_NAMES
        bottom = today(x, top + ROW_GAP, variant)
        if level == "Task":                          # the blockers, down the proposed and today's rows
            task_dividers(x, y - 60, bottom + 10, variant)
        elif level == "Job":
            job_dividers(x, y - 60, bottom + 10, variant)
        return bottom
    return draw
