s07 · Report groups across the themes
=====================================

New on 261011 (JL: "I asked you to have the report groups across the themes ... Please add it as the
s07"). s07 was Job variants until 261007, when it became s12; no file cites an old s07 decision, so
the ids start at s07-D01. s05 is the Report's workbench and skill; this topic is only how the Report
groups its Questions, in every theme.

**Tags:** `Report` · `UI`

**Stage:** shaping

**Topic:** how a Report groups its Questions, theme by theme. Today every Block of every theme shows
the paper Board's four buttons, Ideation · Narrative · High-level logic + Low-level work · Related
Questions (`AUDIENCE_VIEWS`, servers/workbench/frame.py, since 261009), and two of them list studio
topics, not Questions. JL 261011, on a screenshot of b10's Report: "for the Report, definitely, the
groups should not be design in this way ... these group names should be predefined and also can be
added if we want? ... I think for the groups in the report, this will be an very important question
to think about." Proposed here: the Report gets the group bar the Studio and Related already have;
each theme brings its starting groups, the kinds of question it keeps asking; a Block adds its own;
a Question's group is its register `group:` line.

**Feeds:** `reports/` q03_block_questions · q09_studio_report_on_screen


Files
-----

```text
s07-report-groups-across-themes/
├── s07-report-groups-across-themes.md        this face
├── s07-report-groups-across-themes.excalidraw   three frames: Background, the map, the screens (below)
├── s07-report-groups-across-themes.png       its preview
├── .s07-report-groups-across-themes.seed.json   generated snapshot for preserving marks
├── build_s07_report_groups_across_themes.py  the builder; reads each theme's Report live on every build
└── history/                                  the 261011 builder, face and preview (four frames); -261012b,
                                              the three tree frames
```


The drawing
-----------

Three frames (s07-D14, haipipe-studio 0.13.0; JL 261012: "so we can have both tree and box, and -->"). ① and ② are
the yaml under Frames below; ③ the builder draws. An emoji leads every line; ❓ is still open, in red.

```text
① 🧭 Background    for a newcomer: what the topic is about, the Report in one minute, the words it uses
                   (group, the bar, fixed, suggested, own, lens, standing Question, theme), where it sits
② 🗺️ the map       8 boxes, each with why it is there and its own tree, joined by named arrows:
                   Questions -tagged with-> Group names -become buttons-> The group bar -shows at->
                   Every level; Each theme -suggests, fixes-> Group names; Insight topics -insight's own->
                   Each theme; Lenses stay rows -stay above-> the bar; In Tools -draws-> Every level
③ the screens      the base and the 7 themes, one row each: the Report today, read live through
                   frame.render, beside the proposal, in the workbench's own colours (blue open, gray
                   fixed, amber suggested, white own); a red box and a red → note around what is not
                   built or guessed (s07-D12)
```

The Blocks read for ③, in the SPACEs beside Tools: b10 (base), b02_pretrain_corpus (work), Samsung
b12_epic_streaming (cowork), Paper-ScalingGlucose-NatSeries2026 (paper), Insight-SMSR2v1's Job j01
(insight, the screen JL showed 261012), Design-PreVisitChecklist (design, an older Design Folder board),
b01_scaling_law_literature (discovery), b01_aci_bench (labeling, in Physician-SPACE). Every level (②) reads
b02's Block, its Job j01_trace_to_text and Task t02_sampled_windows, and Samsung b12's Job j01_pace_request.


Frames
------

What `build_s07_report_groups_across_themes.py` draws as ① and ② (haipipe-studio `topic_map.draw_frames`); ③, the
screens, the builder draws itself. A leaf `‹name›` is filled from disk on every build: `‹b10›` b10's register,
`‹levels›` one Block, Job and Task read live, `‹themes›` each theme's Report today, `‹topics›` the insight topics
off Insight-SMSR2v1's Task names, `‹folds›` insight's level folds, `‹hooks›` each theme file's Report settings.

```yaml
frames:
- title: 🧭 Background, for a newcomer
  intro: The words this topic uses and where it sits. The map is the next frame; the screens are the third.
  cols: 2
  tree:
  - 🎯 What this topic is about:
    - 🏷️ how a Report groups its Questions, in every theme, with the row of group buttons above its list
    - 📝 s05 is the Report itself; this topic is only its groups
    - "💬 JL 261011: \"these group names should be predefined and also can be added if we want?\""
  - 📝 The Report, in one minute:
    - 📂 a report answers one Question of its level, in reports/qNN_<topic>/
    - "🗂️ the Report Space sits in the Spaces row: Description · Report · Work · Runs"
    - 🃏 it lists one card per Question, opened as Logic │ Work │ Report
    - 🧱 every level keeps its own Report (s09-D02), Block, Job and Task
  - 📖 Words it uses:
    - 🏷️ group, a name that gathers Questions into one list; a Question's register group line
    - "🎛️ the bar: Current · the groups · Untagged · + Group, as the Studio shows its topics"
    - 🔒 fixed group, gray, from the Question itself or the theme's own files; no ×
    - 💡 suggested group, amber, the theme's kinds of question, shown even when empty
    - ✋ own group, white, one the Block added with + Group
    - 🔭 lens, the same Questions shown another way (a cut, a period, a manuscript part); a row above the bar
    - 📌 standing Question, asked on every Board with no register line
    - "🎨 theme, the kind of Block: work, cowork, paper, insight, design, discovery, labeling; base: none"
  - 📍 Where it sits:
    - 🧱 b10 keeps the rule and the table; each theme Block, b11 to b17, its own list
    - 🖥️ the code is servers/workbench/frame.py, one look for Studio, Related and Report
    - "🔗 it feeds q03_block_questions and q09_studio_report_on_screen"
- title: 🗺️ Report groups, from a Question's name to every screen
  intro: Each box says why it is there; the arrows say how one part leads to the next. ❓ is still open.
  boxes:
  - id: questions
    at: [0, 0]
    title: 📌 Questions
    why: each is one card on its Report
    tree:
    - ✅ asked in the face's register
    - ‹b10›
    - ✅ a drag writes its group line
    - ❓ Q11, Guide or UI? (Open 2)
  - id: names
    at: [1, 0]
    title: 🏷️ Group names
    why: a name comes from one of three places
    tree:
    - 🔒 fixed, gray, the theme's own
    - 💡 suggested, amber, the theme's kinds
    - 💡 Random thoughts, on every theme
    - ✋ own, white, + Group on the Block
    - ❓ one word everywhere? (Open 4)
  - id: bar
    at: [2, 0]
    title: 🎛️ The group bar
    why: the Studio's bar, one way everywhere
    tree:
    - ✅ one card per Question (s07-D09)
    - ✅ coloured by kind (s07-D12)
    - ✅ order, _groups.txt, theme, Studio
    - 🤝 names shared with the Studio
    - ❓ share names, or one list? (Open 1)
  - id: levels
    at: [3, 0]
    title: 🧱 Every level
    why: Block, Job and Task each report
    tree:
    - ‹levels›
    - ✅ a Job with none shows the Block's
    - ✅ a Task with none lists its Page
  - id: themes
    at: [0, 1]
    title: 🎨 Each theme
    why: the kinds of question it keeps asking
    tree:
    - ‹themes›
    - ❓ guessed names; theme Blocks answer (Open 3, 5)
  - id: insight
    at: [1, 1]
    title: 🔎 Insight topics
    why: topics cut across the level folds
    tree:
    - ‹topics›
    - ✅ the folds stay, ‹folds›
    - ❓ guessed names; agree them (D10, Open 7)
  - id: lenses
    at: [2, 1]
    title: 🔭 Lenses stay rows
    why: the same Questions shown another way
    tree:
    - 🔭 insight, partitions and Period
    - "📋 work Task, Draft · Report"
    - 📄 paper version, its manuscript parts
    - 📚 paper, Related Papers
    - 📌 standing Questions in their group
  - id: tools
    at: [3, 1]
    title: 🧰 In Tools
    why: where the rule and its code live
    tree:
    - 🖥️ frame.py, report_view, group_list
    - ‹hooks›
    - 🧠 haipipe-question, the group line
    - 📝 haipipe-report, the Report (s05)
    - 🎨 canvas.UI_KIND, drawing colours
  arrows:
  - {from: questions, to: names, label: tagged with}
  - {from: names, to: bar, label: become buttons}
  - {from: bar, to: levels, label: shows at}
  - {from: themes, to: names, label: "suggests, fixes"}
  - {from: insight, to: themes, label: insight's own}
  - {from: lenses, to: bar, label: stay above}
  - {from: tools, to: levels, label: draws}
```


In Tools
--------

Where the code and skills sit, under `Tools/plugins/haipipe-toolkit/`; the drawing's "In Tools" frame
reads the same off the disk on every build.

```text
skills/1_base/question/haipipe-question/   the register: a Question's group: line
skills/1_base/project/haipipe-report/      the Report (s05)
servers/workbench/frame.py                 question_rows · group_list · studio_group_op
                                           AUDIENCE_VIEWS · WHO_ASKS, the four buttons today
servers/workbench-<theme>/<theme>_theme.py each theme's Report row today; its starting groups
```


Read on disk (261011)
---------------------

1. Of the Blocks with a Question register, 2 use `group:` at all: a work Block (Corpus · Pilot ·
   Evaluation · Learning strategy) and one paper (a single group, `nmi-cgm-scaling-axes`). The 12
   blueprint Blocks (50 Questions) and the 5 cowork Blocks (32 Questions) use none.
2. Where groups exist they name subjects (Corpus, Pilot) or the event kind a Question is about
   (Food, Insulin, Medication, Exercise); a theme's kind and a Block's subject mix in one list.
3. The Report's second row differs by theme today: vanilla and b10 show the paper's four; paper adds
   Related Papers, and its version Job shows Questions · Draft-Main · Draft-Appendix · Comments ·
   Cover letter; cowork shows All plus its groups; design Elements · Evaluation; discovery Questions ·
   Reports; insight one view per partition (D · I · K · W); work's Task Draft · Report.


Paper and insight today (read 261011)
--------------------------------------

JL 261011, on the first table's paper and insight rows: "for this two, you need to think about this very
carefully ... think about what is the current things looks like". Read from the code
(servers/workbench-paper/paper_theme.py, servers/workbench-insight/insight_theme.py, insight_views.py)
and the real Boards:

1. The paper Board's buttons each read their own rows (Paper-ScalingGlucose-NatSeries2026):
   **Ideation**, 5 ideas with their verdicts (studio/s01-ideation), then register Questions with
   `group: ideation` (0 here); **Narrative**, 3 standing rows "Will it attract the editor / reviewer /
   public?", then `group: narrative` (0); **High-level logic + Low-level work**, the current Story's 7
   research questions RQ0 to RQ6, which are the register's Q00 to Q06 under a second name, logic beside
   work; **Related Questions**, the register groups the Story does not feed (0 here: all 7 Questions sit
   in one group named after the Story, `nmi-cgm-scaling-axes`); **Related Papers**, the Story's paper
   table (no related/ yet). So four of the five are kinds of question, not the vanilla filter.
2. The paper version Job (j01_v1009_nmi): Questions (the standing J1 to J4, its own register empty) ·
   Draft-Main · Draft-Appendix · Comments · Cover letter, the parts of the manuscript. A Section Task:
   Table · Reading · Questions · Comments.
3. The two older paper Boards (AnchorPK, FairGlucose) have no register, no reports/, no studio/: only
   ideas (4 and 6), claims C1 to C8 and comment rounds.
4. Insight-S1023 (plan C) shows no buttons of questions at all: row 2 is the partitions, full · awake ·
   asleep · cross, one cut at a time; row 3 the readings, Coverage · Tracks · Consistency · Findings; the
   body folds by Data · Information · Knowledge · Wisdom, read off each Question's id (release p2: 20
   Questions, D 6 · I 6 · K 6 · W 2). A Job: the partitions, then Current · vs previous; a Task: Table ·
   Reading. Its board.md register is empty: the Questions live in the Prototype's release (release.yaml,
   one question.md each). No `group:` anywhere.
5. Insight's subjects cut across its levels: sleep (I03 · K04 · K05), walking (I04 · K02), stress and
   heart (I05 · K03), events (D05 · I06 · K06), glucose control (I01 · I02 · K01).


Decided
-------

s07-D01 · Decided and built (JL 261011: "if the report card to show, it will be the same as the sNN, we can
    create and add the tags"): the Report gets the group bar, Current · the groups · Untagged · + Group, the same
    code as the Studio's and Related's (`frame.group_list`, a third kind beside `studio` and
    `related`), one row per Question under it. A Question's groups are its register `group:` line,
    comma-separated like a topic's **Tags:** line; dragging a row onto a group writes that line;
    `reports/_groups.txt` keeps the buttons' order (JL 261011: "these group names should be
    predefined and also can be added").
s07-D02 · Decided (JL 261011: "for someother report, the groups are of the special forms, and that ones are
    fixed, depending on different theme"); the hook is built, each theme fills it: the names
    come from three places. **Fixed** by the Question's own structure, always shown, never removed:
    insight's Data · Information · Knowledge · Wisdom, read off the id's letter (D01, I03), as a Related
    item's subfolder is its group (s04-D08). **Starting**, the theme's kinds of question, shown even when
    empty (`Theme.report_groups` in `servers/workbench-<theme>/<theme>_theme.py`). **Added**, "+ Group",
    the Block's subjects (Corpus, Pilot; Food, Insulin; insight's Sleep, Walking, Events, which cut
    across its four levels). Every theme also starts with **Random thoughts**, the Questions a
    reviewer, coauthor, editor, reader or partner asked; it replaces `WHO_ASKS` and the Related
    Questions button.
s07-D03 · Proposed (JL 261011; paper and insight revised the same day from their real Reports): each theme's
    groups, and what stays a row above the list (a lens or another part, s07-D05):

    ```text
    theme      groups on the bar                          stays a row above the list
    work       Data · Pilot · Evaluation                  Task: Draft · Report
    discovery  Known · Closest · Gap (guessed)            Questions · Reports
    cowork     Needs · Works · Blockers                   (none)
    paper      Ideation · Narrative · Research questions  Related Papers; version: Questions · Draft-Main ·
               · Random thoughts (today's four, renamed)  Draft-Appendix · Comments · Cover letter
    insight    Data · Information · Knowledge · Wisdom,   partitions (full · awake · asleep · cross);
               fixed by the id; + Group: Sleep, Walking   Coverage · Tracks · Consistency · Findings
    design     Goal · Rules · Ranking (guessed)           Elements · Evaluation
    labeling   Guideline · Agreement · Models (guessed)   (none)
    every one  Random thoughts                            -
    ```
    The paper keeps what it has: Ideation (its ideas and their verdicts), Narrative (will it attract),
    Research questions (today's "High-level logic + Low-level work": the Questions the current telling's
    **Feeds:** line names, read by id, still drawn logic beside work; b16 s05-D01) and Random thoughts
    (today's Related Questions). Its first draft here,
    "Claims · Evidence", was written without reading the paper Report and is dropped.
s07-D04 · Proposed (JL 261011): Studio and Report share group names, not one list. A name on both shelves filters
    both: pick UI in the Studio, open the Report, and UI stays picked (the link's `studio_tag`). The
    Report's button order is `reports/_groups.txt`, then the Studio's order for the same names. A
    shared name links the two: the paper's Ideation names its s01-ideation topic in the Studio and its 5
    ideas in the Report. Related keeps its own groups, its subfolders (s04-D08). Why not one list (the
    watcher's first proposal): the Report's fixed and starting groups (insight's four levels, Asked by
    others) would sit as empty buttons on the Studio bar, and the Studio's subjects as empty buttons on
    the Report's. The watcher session agreed the same day and withdrew the one-list option.
s07-D05 · Proposed (JL 261011; revised the same day): a Report's second and third rows hold three different
    things today, and only one goes on the bar. A **group** gathers rows into one list: Related Questions,
    cowork's All plus its groups, the paper's Ideation and Narrative. It goes on the bar, and a theme may
    put rows of its own in it, in the same Question │ Work │ Report shape (the paper's ideas, its "will it
    attract" rows). A **fixed section** comes from the Question itself (insight's level letter): it becomes
    a fixed group (s07-D02). A **lens** shows the same Questions another way, or another part of the work:
    insight's partitions, readings and periods; a Task's Table · Reading or Draft · Report; the paper
    version's manuscript parts; Related Papers, which reads related/. It stays a row above the list. The
    vanilla filter "High-level logic + Low-level work" becomes the plain list.
s07-D06 · Proposed (JL 261011): by level. A Block's Report groups its own register. A Job's shows the Block's
    Questions it answers (`answers: Q05`), with their groups, so picking a group at the Block and
    opening a Job keeps it. A Task's Report is its own result: no Questions, no bar (s09-D02).
s07-D07 · Proposed (JL 261011): b10's own 12 Questions in its existing Studio groups, so b10 needs no new name
    (from the watcher's mapping, with Q03 moved to Report, a group b10's Studio gained on 261011):
    Levels Q01 Q02 · Report Q03 · Structure Q04 · Run and Skill Q05 Q06 · UI Q07 Q08 Q09 · Guide Q10
    Q11 · Server Q12.
s07-D08 · Proposed (JL 261011): a theme may also predefine **standing Questions**, asked on every Board or version
    with no register line, each in its group. The paper already does: Narrative's three "Will it attract
    the editor / reviewer / public?" on the Board, and J1 to J5 on every version (What is the one-minute
    story? · Why this venue? · Which writing principles does it follow? · Is it ready to send? · What
    changed since the last send?, J5 a revision only; `STANDING` in paper_theme.py). This is where "what
    are the typical questions to ask" (JL 261011, to the sNN session) gets each theme's answer.

s07-D09 · Built 261011 in servers/workbench/frame.py (workbench 1.19.0). `report_view` draws each Question as
    a folding card, as a Studio topic is (⋮⋮ · its id and title · its chips · state and work · Add to
    Current), opened on its Logic │ Work │ Report row, under `group_list(kind="reports")`; the vanilla
    Report has no second row any more. `_question_records` reads the register once for the cards and for
    `question_rows`, which the paper and cowork themes still call. `_register_set_groups` writes the
    `group:` line in the face's `## Questions` yaml (replaced, added after `title:`, or removed), touching
    no other line. `Theme.report_fixed(row)` gives a theme's fixed groups (no ×; a remove is refused,
    "fixed by the theme"), `Theme.report_groups` its starting ones. Order: `reports/_groups.txt`, then the
    theme's starting groups, then the Studio's order for the same names. b10's 12 Questions got their
    `group:` lines through the same op (s07-D07, Q11 under Guide until Open 2). Checked live on 5623: the
    bar reads Structure 1 · Levels 2 · Guide 2 · Run and Skill 2 · Server 1 · UI 3 · Report 1, picking UI
    leaves Q07 · Q08 · Q09, and a save over HTTP writes and removes a group line. The paper and insight
    themes draw their own Report and do not use the hook yet (b16 for the paper; b11 for insight).
    For the paper, b16 asked for two more, added the same day (workbench 1.19.1): `report_fixed(row, owner)`
    (its fixed group comes from the telling's **Feeds:**; a one-argument rule still works), and
    `Theme.report_cards(level, folder, root)`, the theme's own cards that are no register row (its ideas,
    its standing Questions), drawn under the same bar, not draggable, their groups fixed.

s07-D10 · Proposed (JL 261012, on Insight-SMSR2v1's Job Report: "besides the period, we can also have the topics:
    with different topics across D I K W"): an insight Report gets a **Topic** row under Period, and it is the
    group bar (Current · the topics · + Group). The level folds stay as they are today (Executive, added
    261012 by the insight session, then Data · Information · Knowledge · Wisdom), each counting only the
    topic picked, instead of becoming fixed buttons (this revises s07-D02's insight example). Why: a topic
    gathers Questions (a group); the partitions and Period show the same Questions on another cut or time
    (lenses, s07-D05), and the levels are already the folds. Read 261012 off the Task names of release p1
    (49 Questions), 12 topics, each across levels: Variants 9 (D02 · I02 I12 I18 I24 · K05 K11 · W01 W02),
    Timing 5 (I04 I09 · K03 K07 K17), Demographics 4 (I03 I07 I20 · K02), Data quality 4 (D01 D04 D05 · I19),
    Place and income 5, Medical context 4, Behaviour 4, Wording 3, Partitions 3, Sender 3, Prior messages 3,
    Funnel 2. The names are guessed from the Task names until agreed; a Question's topic is a `group:` line
    in its question.md in the Prototype (Open 7).
s07-D11 · Decided (JL 261012, through the b10 watcher: "go ahead and do all"): the drawing is three frames,
    each a folder tree: ① Background, ② the Tree, ③ the screens, today beside proposed for the base and
    every theme. The 261011 four frames (the screens, Across the themes, Paper and insight today, In Tools)
    are folded into ② and ③; the old builder, face and preview are in `history/`.
s07-D12 · Decided and built (JL 261012: "for each group, I think we might have the things like the fixed groups
    (or the suggested default group labels), do we have that? if so, we might give them to different
    colors"): a Report group's button takes the colour of where its name comes from: **gray**, fixed by the
    theme (`Theme.report_fixed`, `report_cards`; no ×); **amber**, suggested by the theme and shown even when
    empty (`Theme.report_groups`, and "Random thoughts" in every theme, s07-D02); **white**, the Block's own
    (+ Group). The bar's help line names the colours. Built in `servers/workbench/frame.py` (`group_list`
    takes `fixed`; `--grp-fixed-*`, `--grp-sug-*`, light and dark; `REPORT_SUGGESTED`). The suggested groups of
    s07-D03 are set for work (Data · Pilot · Evaluation, `work_theme.py`) and cowork (Needs · Works ·
    Blockers, `cowork_theme.py`); the guessed ones (design, discovery, labeling) are not. A drawing shows the
    same colours through `canvas.UI_KIND` (a box's `customData.ui_kind`), and marks what is proposed or
    guessed with a red box and a red → note, never with a colour the screen does not have (JL 261012: "if we
    want to show the indicator, we can use the red box to circle them and give --> text to explain them, I
    don't want it to be mislead the UI design").
s07-D13 · Decided and built (JL 261012: "for the report, we might have the report group tags for both the block
    level, job level and task level"): every level's Report shows its group bar, Block, Job and Task, even
    before its first Question (then "No Questions at this level yet", or a Task's own Page row, under it).
    A Job with no Questions of its own shows the Block's it answers: `answers:` on its face, or, new, the
    Block's Questions whose register `work:` names a file of the Job (a cowork register); cowork's Job Report
    is now the base's cards. A work Task keeps Draft · Report as a lens and shows its bar under Report. This
    revises s07-D06 ("Task: no bar"). `report_view` always returns the bar (`empty` is the list under it).
    Tests: `_host/tests/test_frame.py` (`test_report_bar_at_every_level_and_its_kinds_coloured`) and
    `workbench-cowork/tests/test_cowork_theme.py`; 221 workbench tests pass.
s07-D14 · Decided (JL 261012, through the b10 watcher: "it is not that vivid ... add the things like the emoji";
    "so we can have both tree and box, and -->"): the drawing is ① Background, a tree, and ② a map of boxes,
    each with why it is there and its own tree, joined by named arrows, both from the face's `frames:` yaml
    (haipipe-studio 0.13.0, `topic_map.draw_frames`, a `‹name›` leaf filled from disk); ③ stays the
    screens. An emoji leads every line. The 3-tree version is in `history/` (-261012b).


Read on the screens (261012)
----------------------------

1. On the bar today: the base (b10, 12 cards); the work Block (b02_pretrain_corpus, 5 cards: Corpus 2 ·
   Evaluation 1 · Learning strategy 1 · Pilot 1), because work's Block and Job read as the base; and,
   since 261012, the cowork Block (Samsung b12, 2 cards, Untagged 2): `cowork_theme.py` leaves its Report
   to the base's `report_view`, and a report with an event table adds a Questions · Timeline row above
   the list, a lens (built by the b10-report session). Cowork's Job still lists the Questions that cite
   it, in a table.
2. Not on the bar: the paper its five buttons; insight its partitions, Period and level folds
   (Executive · Data · Information · Knowledge · Wisdom); the older design board its own six; discovery
   Questions · Reports; labeling has no Questions on its one Block.
3. Since s07-D12, work and cowork set `report_groups`: Data · Pilot · Evaluation and Needs · Works · Blockers
   show in amber on every Report of those themes, with Random thoughts on every theme's bar. No theme sets
   `report_fixed` or `report_cards` yet (the paper's will, b16).


Open
----

1. Share the names (s07-D04, the recommendation; the watcher session agreed 261011) or, as the
   alternative, keep one list for Studio and Report?
2. Q11, how a Page's logic is drawn: Guide or UI?
3. The starting groups of discovery, design and labeling are guesses: learn them on one real Block
   each (s09 Open 2 says the same).
4. Is "Random thoughts" one name in every theme, or the theme's own word (paper: Reviewers)?
5. Each theme Block (b11 to b17) owns its theme's list? For the paper, yes (b16 s05-D02, proposed
   261011): b10 keeps the rule and this table, b16 the paper's four groups and its standing Questions.
   The other six theme Blocks have not answered.
6. Answered for the paper by b16 s05-D01 (proposed 261011): a Question's `group:` is its kind
   (Ideation, Narrative, or an asker: reviewer, coauthor, editor, reader). The telling is said once, in
   its **Feeds:** line (q00_ to q06_), so Research questions are the Questions it feeds, read by id; a
   research question needs no group line, and `nmi-cgm-scaling-axes` keeps working unedited. b16 s05
   Open 5 asks which name the screen keeps, RQ0 or Q00 (JL's choice).
7. An insight topic (Sleep; Variants, Timing): a `group:` line in each question.md's front matter in the
   Prototype, so every Board of that Prototype shares it? And agree the 12 SMS topic names (s07-D10).
8. A paper's research questions have two names, RQ0 to RQ6 in the Story and Q00 to Q06 in the
   register: which one does the screen keep (b16 s05 Open 5, JL's choice)?

(write here, or mark the drawing in red)
