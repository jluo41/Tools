# q03_block_questions · draft v0.1
draft-version: v0.1
supersedes: none
date: 261006
approved: ⬜
status: working · carried over from the studio topic s02-studio-and-report (deleted 261007, no drawing)
arc: Studio is for creation, Report for presentation; one Block shape for both, and agent sessions saved as summaries.

from: the studio topic s02-studio-and-report (261006); its session record is `records/261006-design-session.md`
feeds: Q03 (main), Q07, proposed Q09 and Q10
status: proposal, nothing changed in skills or servers
source: JL's red notes on `Tools/designs/b03_project/studio/s01-overall-tree-structure/ladder-v3.excalidraw`


Reading of JL's notes
---------------------

JL's four notes, verbatim, sit beside the `sNN` and `qNN` trees of the ladder drawing:

1. On `sNN_<topic>.excalidraw`: "How to handle the human changes here? Try to be the tree
   based, with the lines and box. Give human more room to modify and scratch. Keep human's
   scratch."
2. On `chat/`: "also the claude code session or the codex session can be saved here."
3. On `qNN_<topic>.excalidraw`: "Report, Try to make things clear. More figures, and
   displays to show the results. Human can also modify, but just the minor changes, or
   suggestions."
4. Beside them: "For the Claude Code session and Codex session. For each Section of
   response, try to link to these two Studio Topic or Question (Report) Topic. Studio for
   Creation. Report for Presentation."

The reading, sharpened:

```text
                 studio/sNN-<topic>/              reports/qNN_<topic>/
purpose          CREATION                         PRESENTATION
who leads        the person; agent seeds          the agent; person suggests
drawing shape    a tree of boxes and lines,       frames led by figures, tables,
                 wide empty gutters               real values, one answer frame first
person's marks   anything, anywhere, kept         small edits or suggestion notes
generator        seeds, never overwrites          redraws; folds suggestions into
                 the person's marks               its builder, then rebuilds
text beside it   sNN-<topic>.md (decided so far)  qNN_<topic>.md (Answer, Evidence,
                 chat/ (one file per session)     Limits, Next) + draft/ (free notes)
reply link       "Studio for Creation"            "Report for Presentation"
```

Three points the notes imply but do not say:

1. A studio topic feeds one or more Questions. Creation turns into presentation: when a
   studio topic settles something, the settled part moves into a report's Answer. So a
   topic names the Questions it feeds (`feeds: Q03`).
2. Both drawings are seeded by a script and edited by a person. What differs is the edit
   rule, not who may touch the file. Scratch: the person's marks win and stay. Report: the
   person's marks are suggestions that the agent folds into the builder.
3. A session is saved where its work was creation (a studio topic's `chat/`). A report has
   `draft/`, not `chat/`: presentation is not where the discussion lives.

Two places where the drawing on the canvas and the skills disagree today:

1. The canvas calls `studio/` and `reports/` "two special Jobs". Every contract
   (`haipipe-task`, `haipipe-question`, `haipipe-project`) treats them as Block-level
   folders beside the `jNN_` Jobs, with no `jNN` number. This proposal keeps them as
   folders (open question 2).
2. The canvas sketch writes `sNN_<topic>` (underscore); JL's first real folder is
   `s01-overall-tree-structure/` (hyphen). This proposal uses JL's hyphen form
   `sNN-<topic>/`, while `qNN_<topic>/`, `bNN_`, `jNN_`, `tNN_` keep underscores (open
   question 1).


Topics
------

Where this belongs in `Tools/designs/b03_project/` (register in `board.md`, Q01 to Q08):

| Question | What this topic gives it |
|---|---|
| Q03 "How do Questions live at the Block level?" | Main home. The Block shape becomes `board.md` + `studio/sNN-<topic>/` + `reports/qNN_<topic>/`; this proposal fills in what each folder holds. |
| Q07 "How does the workbench map onto the ladder?" | Where a studio topic and a report drawing show (Scope › RoadMap Draw, the Report column, the Studio tab). |
| Q06 "Which skill owns each level?" | Who owns a Block's `studio/` topics: today nobody (open question 6). |
| Q08 "How do we host the SPACE?" | Small: a viewer may leave suggestions on a report drawing, never a scratch edit. |

Two new Questions, proposed (created only if JL agrees, through `haipipe-question`, with the
next free ids):

- proposed Q09 `q09_shared_drawings`: "How do a person and a generator share one drawing?"
  The two modes, the edit rule of each, the seed snapshot, the stale-tab conflict, the
  suggestion loop on a report drawing.
- proposed Q10 `q10_agent_sessions`: "How are agent sessions kept and linked to the Block?"
  Where Claude Code and Codex sessions are saved, what a saved session holds, the PHI gate,
  and how each reply section links a studio topic or a report question.

First studio topics (`studio/sNN-<topic>/`):

| Topic | Feeds | What it is for |
|---|---|---|
| `s01-overall-tree-structure` | Q01, Q02, Q03 (a guess; JL's to set) | JL's, exists: the ladder drawings (v3 with these notes, v4). |
| `s02-studio-and-report` | Q03, Q07, Q09, Q10 | This proposal; moved into this draft 261007. |
| `s03-drawing-modes` | Q09 | Prototype the scratch tree and the report suggestion loop on a canvas. |
| `s04-session-keeping` | Q10 | The saved-session file, its template, the PHI gate, the helper. |
| `s05-reply-links` | Q10 | The reply's Related line for sNN and qNN, and the workbench anchors it links to. |

s03 to s05 are suggestions; s04 and s05 can stay inside s02 if JL prefers fewer topics.


Skills to change
----------------

Paths are under `Tools/plugins/haipipe-toolkit/skills/`.

| Skill | Change | Why |
|---|---|---|
| `0_utils/response-format` | Widen "Related question" to "Related": a section links ONE studio topic (creation) or ONE report question (presentation). Forms below. A studio link opens `view=studio#studio-sNN`; until that anchor exists, link the topic's `.md` or folder. `(proposed) <Board> sNN-<topic>` allowed, offered in Summary and Next as today. | JL note 4. Today the line only knows `qNN`, so design and drafting sections are forced onto a Question they do not answer yet. |
| `question/ask-questions` | Match each section to a studio topic or a Question; rule: making, exploring, drafting a drawing or contract = studio; a result, answer, evidence = report. | It is the skill that does the association `response-format` points to. |
| `question/haipipe-question` | (a) Report folder = `qNN_<topic>.md` + `qNN_<topic>.excalidraw` (same stem, beside the Page) + `draft/` + `page.toml`; `reports/qNN_<topic>/studio/` becomes a readable old form. (b) `--drawing` writes the same-stem drawing. (c) The Block's `studio/` is described as topic folders, not "drawings the whole Block shares". (d) If JL agrees it owns them: `block_questions.py add-topic <block> --slug <topic>` makes `studio/sNN-<topic>/` with the next free NN and a frame `sNN-<topic>.md` (`feeds:`). | JL's tree. Today the skill says a report's drawing lives in `reports/qNN/studio/`, which the new layout drops. |
| `display/excalidraw-report` | Scratch mode: (a) default shape is a tree of boxes and lines (the `build_ladder_trees.py` shape), with wide gutters and new content placed in new columns, so the person's marks keep lining up; this softens the 261005 "loose clusters" wording rather than reversing "not too structured". (b) The builder lives at `studio/sNN-<topic>/sNN-<topic>.py`, its snapshot at `studio/sNN-<topic>/.sNN-<topic>.seed.json`. (c) Move the merge writer `canvas.py` from `Tools/designs/b03_project/studio/_build/` into the skill (`ref/canvas.py`) so every Block imports one copy. (d) Write a `mode` into the scene (`scratch`, `report`, `generated`) so the workbench knows whether to give the pen. Report mode: add a "Suggestions" section: the person may edit or leave notes; the agent reads them (non-`s-` ids and edited `s-` elements), answers in blue, folds each into the builder, rebuilds; once the builder draws the edited content the element is absorbed as seed. | JL notes 1 and 3. The skill already has the seed-snapshot writer and the comment loop, but only for scratches; the report mode has no edit rule at all. |
| `page/haipipe-workbench-studio` (`ref/chat.md`) | Add a Block-topic keep: one file per session in `studio/sNN-<topic>/chat/`, a summary with section links, no raw transcript. Fix the Page keep: `transcript_markdown` and the keep head write `source:` as the absolute jsonl path (breaks AGENTS.md rule 7); write the session id and agent instead. Name Codex as a second source. | JL note 2; privacy; rule 7. |
| `page/haipipe-page` | One paragraph: a Page's `studio/{chat,draw}/` (lanes of one Page) is not a Block's `studio/sNN-<topic>/` (topics of a Block). Same word, two shapes; say which is which. | Two contracts share the name `studio/`. |
| `task/haipipe-task` | SKILL tree, `ref/hierarchy.md`, `ref/block-board-template.md`: Block `studio/` = `sNN-<topic>/` + `_build/` (shared helpers only). `ref/check_task_tree.py`: Block rows (topic names, one drawing per topic named after it, `chat/` file names, no transcript dumps, report folder holds only `.md`, `.excalidraw`, `.png`, `draft/`, `page.toml`). Task-level S4 unchanged. | The checker reads only Task-level `studio/` today. |
| `project/haipipe-project` | `ref/project-structure.md`: "Drawings are rebuilt by their scripts, never edited by hand" (cowork Block) and "question-map ... never edited" stay true only for `mode: generated`. A seeded scratch or report drawing is merged, never overwritten, and the person may draw on it. | Today's wording contradicts "keep human's scratch". |
| later: `haipipe-insight`, `haipipe-paper`, `haipipe-cowork` | They use flat `studio/*.excalidraw` (question map, Story drawings). Align after the task Block works. | Keep the first wave small. |

The Related line, both forms:

```text
**Related:** [<Board> s02 "studio and report"](<host>/_board/task-board?path=<board>/board.md&view=studio#studio-s02) (studio): <why>
**Related:** [<Board> Q03 "Questions at Block level"](<host>/_board/task-board?path=<board>/board.md&view=questions#question-Q03) (report): <why>
```


Workbench to change
-------------------

This part is carried to Q12 (`../../q12_studio_report_on_screen/`; it was b02's Q04 before b02 merged into b03).

Servers under `Tools/plugins/haipipe-toolkit/servers/`.

1. **Plain drawings get a revision check** (`workbench-shared/xcal.py`, `assets/xcal-boot.js`).
   Today only linked Page or Group scenes check `base_revision` (`save_linked_page`,
   `save_linked_group`); `save_excalidraw`'s plain path replaces the elements with no check,
   and `serve_frame` sends a plain scene with no revision. A stale editor tab therefore saves
   over a newer build every 1.5 s. Fix: `serve_frame` adds `revision` (sha256 of the file)
   to a plain scene; the client takes `baseRevision = runtime.revision || scene.revision`;
   the plain save, under `draw_lock`, refuses a mismatch with the existing `conflict()`
   reply and returns the new revision. The client already stops saving and says "reload"
   on `conflict`. A save without `base_revision` (an old tab) is refused for paths under
   `studio/` and `reports/`, accepted elsewhere during migration. This also makes the
   "stale copy" guess in `canvas.py` a fallback rather than the main defence.
2. **RoadMap Draw reads topics** (`workbench-task/task_questions.py` `extend_snapshot`,
   `task_views.py`; the same flat `studio.glob("*.excalidraw")` sits in `workbench-cowork`,
   `workbench-insight`, `workbench-paper`). One row per `studio/sNN-<topic>/`: its drawing,
   its `.md` status line, `feeds:`, and the number of saved sessions in `chat/`; anchor
   `id="studio-sNN"`. Flat drawings stay listed as before.
3. **Pen by mode, not by script.** Today a drawing whose `source` ends in `.py` opens
   "view only, never edited". New rule: `mode: generated` stays view only (the question map);
   `mode: scratch` gets the pen; `mode: report` opens view first with a "Suggest" button that
   gives the pen.
4. **"+ Add drawing" becomes "+ Add topic"**: it makes `studio/sNN-<topic>/sNN-<topic>.excalidraw`
   with the next free NN (and the frame `.md`), instead of a flat `studio/<name>.excalidraw`.
5. **Report column and pop-out** (`task_questions.py` report drawings): pick up the same-stem
   `reports/qNN_<topic>/qNN_<topic>.excalidraw` even before `### Evidence` links it (today only
   `reports/qNN/studio/*.excalidraw` is found unlinked). Show the drawing first; `draft/` stays
   off the presentation face, reachable from the folder list.
6. **Studio tab and keep** (`workbench-shared/chat.py` `keep_sessions`, `_host/serve.py`
   `/_board/chat-keep`): today it accepts only a folded Page and writes
   `studio/chat/<YYMMDD-HHMM>/{digest,transcript}.md`. Add a Block-topic target that writes one
   summary file into `studio/sNN-<topic>/chat/`, runs the PHI gate first, and writes no absolute
   path.


Saving agent sessions
---------------------

Where the raw logs live (outside the repo, never copied in):

```text
Claude Code   $HOME/.claude/projects/<slug>/<session-id>.jsonl
              <slug> = the session's working folder with "/" -> "-"; a session started in a
              subfolder (e.g. a studio/_build) lands under a different slug
Codex         $HOME/.codex/sessions/<YYYY>/<MM>/<DD>/rollout-<stamp>-<id>.jsonl
              (+ $HOME/.codex/session_index.jsonl)
```

What a saved session is: ONE Markdown file, a summary with links, written by the agent at the
end of the session (or by the keep button through the same helper). Not the raw log.

```text
studio/sNN-<topic>/chat/<YYMMDD>-<HHMM>-<agent>-<slug>.md     agent = cc | codex

header   session: <id> · agent: cc|codex · date · topic: sNN-<topic>
Ask      what the person asked, paraphrased, no pasted data
Read     the files and skills read (relative paths)
Sections each reply section: its heading, one-line takeaway, its Related link (sNN or qNN)
Changed  files changed, one line each (relative paths)
Decided  what was settled -> also copied into sNN-<topic>.md (the chat file is not the record)
Open     what is still open, and for whom
```

1. **One file per session.** A re-save overwrites the same file (match on `session:`). This
   differs from the Page lane's two-file folder (`digest.md` + `transcript.md`, checker row
   S4); a Block topic keeps only the digest.
2. **One home.** The file sits in the topic most of its sections link to; the other topics and
   Questions are reached through its links, never copied.
3. **No PHI, ever** (DrFirst is a HIPAA-covered entity). The summary paraphrases; it holds no
   data values, no row-level records, no names with health or Rx data, no identifiers, no
   screenshots. Before writing, the helper scans the draft for the org's red-flag patterns
   (SSN, DEA, MRN or DOB fields, HL7 `PID|`, FHIR `Patient`) and refuses on a hit. A session
   that handled real patient data is not saved at all; its summary says only "work on
   restricted data, not kept". Encoded ids are not PHI (AGENTS.md rule 9) but are still left
   out: a summary does not need them.
4. **No absolute paths** (AGENTS.md rule 7): the jsonl is named by session id and agent, not by
   `$HOME/...` path.
5. **Authored, not generated.** The file is written by the agent, so a person may edit it. A
   later helper (`keep_session.py --agent cc|codex --session <id> --topic <block>/studio/sNN-<topic>`)
   only pre-fills the header and the section list from the assistant's own headings and Related
   lines (never the user's text); the agent writes the rest.

The first example is `records/261006-design-session.md` beside this draft (named by the brief, before
the `-<HHMM>-<agent>-` form was proposed).


Plan
----

```text
1  xcal.py plain revision check          bug fix, one file + one client line, no contract change
2  response-format Related: sNN or qNN   text only; file-link fallback until anchors exist
3  contracts: haipipe-question,          studio/sNN-<topic>/, report draft/ + same-stem drawing,
   haipipe-task, haipipe-project, -page  the "never edited by hand" wording narrowed to generated
4  excalidraw-report                     tree scratch, report Suggestions, canvas.py into ref/, mode
5  workbench RoadMap Draw + Report       topic rows + anchors, pen by mode, + Add topic, same-stem
6  session keeping                       template now (by hand, as this session did); helper and
                                         keep button next; fix the absolute source path
7  checker rows                          check_task_tree.py Block studio/ and reports/ rows
```

Step 1 stands alone and stops a real loss today. Steps 2 and 3 are text and can land in one
Tools commit once JL answers questions 1, 2 and 6.


Open questions for JL
---------------------

1. **Hyphen or underscore?** `s01-overall-tree-structure/` uses hyphens; the canvas sketch and
   every other level (`bNN_`, `jNN_`, `tNN_`, `qNN_`) use underscores. Keep `sNN-` only for
   studio topics, or move all to one form?
2. **Jobs or folders?** The canvas calls `studio/` and `reports/` "special Jobs". Keep them as
   Block-level folders beside the `jNN_` Jobs (as every contract says today)?
3. **One drawing per topic?** `s01-overall-tree-structure/` holds `ladder-v3` and `ladder-v4`
   and `build_ladder_v4.py`. Is a topic one `sNN-<topic>.excalidraw` (versions become frames),
   or may it hold several?
4. **Flat drawings.** The Block's flat `studio/ladder-grid`, `ladder-trees`, `project-scratch`:
   move each into a topic, or keep flat as Block-wide drawings?
5. **A folded suggestion.** On a report drawing, after the agent folds a suggestion into the
   builder, does the person's note stay where it is, move into a "Suggestions" frame, or does
   the person clear it?
6. **Owner of studio topics.** `haipipe-question` (beside reports, with `add-topic`), a new
   small skill, or `haipipe-workbench-studio`?
7. **Raw transcripts.** Summary only for Block topics (proposed). Should the Page lane also stop
   committing `transcript.md` by default, given the HIPAA rule?
8. **Every section linked?** May a purely mechanical section (a push, a rename) skip the link, and
   may one section name both a topic and the Question it feeds, or strictly one?
9. **Register.** Is the folder list the register of studio topics (as `reports/` is of
   Questions), with `feeds:` in each `sNN-<topic>.md`, or should `board.md` gain a `## Studio`
   register?
10. **New Questions.** Create proposed Q09 (shared drawings) and Q10 (agent sessions), or fold
    both into Q03?
