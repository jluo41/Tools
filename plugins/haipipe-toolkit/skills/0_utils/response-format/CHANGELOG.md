response-format — Changelog
===========================

## [0.18.2] — 2026-10-09

- A Job's question links the shared workbench on the Job's Audience Report
  (`/_board/workbench?path=<job folder>&space=Audience+Report#question-QNN`): the toolkit's
  blueprint Blocks became Jobs of `Tools/blueprints/b01_haipipe-toolkit/` (one Block per
  package, JL 261009), and a Job has no `board.md`.

## [0.18.1] — 2026-10-06

- The link opens the workbench UI, not the report's Page (JL: "what I want is the
  workbench UI, not the webpage of the page"): `…/board.md&view=questions#question-QNN`
  opens the Questions view scrolled to that row, in the Task, CoWork and Discovery
  workbenches alike. `&report=QNN` opened the report Page and is no longer used.

## [0.18.0] — 2026-10-06

- A Related question's link opens the Question in its board's workbench:
  `<host>/_board/<kind>-board?path=<board>/board.md&report=QNN` (kind task, cowork or
  discovery; host = the shared host's `--public-url`). JL: "I can just click and open
  them". The question's file stays the fallback when no host serves the SPACE or the
  board has no workbench.

## [0.17.0] — 2026-10-03

- Questions get their own skillset, `skills/question/` (JL 261003: "should I put all the
  question related skills into here"). The granularity tests and the topic/decision table
  move to `haipipe-question`; this skill keeps one paragraph and points to it, and creating
  a proposed question's folder goes through `haipipe-question`. `ask-questions` moved to
  `skills/question/ask-questions/`; its link here follows.

## [0.16.0] — 2026-10-03

- Granularity made checkable (JL 261003: "pay attention to the question granularity"):
  a topic/decision pair table, a sketch of sections feeding one topic, and five tests
  (report test, reuse test, too narrow, too broad, reuse first). "Keep the Related
  question specific" is replaced by "keep it at topic level; the Why says what this
  section adds".
- A proposed question proposes its folder (JL 261003: "propose to generate the
  questions folder under the report as well"): Summary and Next offers to create
  `<board>/reports/qNN_<topic>/`, with the next free NN; created only when the user
  agrees, through the board's own skill.
- Board is owner and block (`Tools/designs b01_utils`, `<Project> b02_record`); project
  names in the examples replaced by placeholders. The example's proposed question is
  lifted to a topic: "How are records cut into cases?".

## [0.15.0] — 2026-10-03

- The Related question names the board and the question so its report can be found
  (JL 261003: "the question to find the board name and the question name, as concise
  as possible"): `**Related question:** [<Board> · QNN <question name>](<report
  path>): <why>`. The Session form is removed (JL 261003: "why you have the session
  question? … link the questions in certain boards' reports folder"); with no fitting
  report, `Proposed · <Board> · <question>`, unlinked.
- Then simplified (JL 261003: "(proposed) Tools/designs b01_utils \"short and brief description
  of the question\""): `[<Board> QNN "<short question>"](<report>): <why>`, and
  `(proposed) <Board> "<short question>": <why>`.
- Wording (JL 261003: "the reports/ is the questions, reports is a list of questions"):
  the line links a board's question (`reports/qNN_<topic>`), and the skill says question, not report.
- Granularity (JL 261003: "the question is not like the specific question, it is a topic
  question … eventually it can develop the report"): a Related question names the board's
  topic the section adds to, reused first; a narrow decision stays in the points and the Why.

## [0.14.0] — 2026-10-03

- The question leaves the heading and becomes the section's last element, the
  Related question line: `**Related question:** <address>. **Why:** <what this
  section gives it>` (JL 261003: "add the 6, to remove the questions to the section
  element as the related questions, and explain why this section is related to a
  question"). The heading is a plain `## N. [emoji] Short Headline` again.
- A section's elements are now six: heading, scan points, sketch (optional), prose,
  file lines (only when files changed), Related question. The Why is one line of 20
  words or fewer and names the section's contribution (answers, narrows, evidences,
  raises), never the question restated. Address forms are unchanged: recorded,
  `Session · …`, `Proposed · …`. Summary and Next has no Related question.

## [0.13.0] — 2026-10-03

- The question moves into the section heading:
  `## N. [emoji] Short Headline (Q: <address>)`, for example
  `## 2. ✅ Shown as Steps Now (Q: Session · <question>)`. The reader sees the
  question before the content. The bold `Question:` footer line is dropped.
- Address forms are unchanged inside the parentheses: recorded
  `<owner>/<block>/QNN-<slug>` (linked when its report exists), `Session · ...`,
  `Proposed · ...`. Summary and Next still has none.
- ask-questions follows.

## [0.12.0] — 2026-10-03

- One question per section: each ordinary section answers exactly one question;
  content serving two questions is split into two sections. Several sections may
  still share one question.
- The footer line starts with `Question:`, the whole line bold:
  `Question: Tools/designs/b01_utils/Q01-point_or_restate`,
  `Question: Session · <question>`, `Question: Proposed · <question>`.
- ask-questions follows both rules.

## [0.11.0] — 2026-10-03

- Drop the `·` dot padding after section headings: a heading ends at its headline.
- Shorten the Question footer to one bold address line. Recorded:
  `<owner>/<block>/QNN-<slug>` (e.g. `Tools/designs/b01_utils/Q01-point_or_restate`),
  linked when its report exists; no `Related question:` label, no `Belongs to:`
  line, no repeated question wording. Session and Proposed keep their wording:
  `Session · <question>`, `Proposed · <question>`.
- ask-questions points to the new footer form.

## [0.10.1] — 2026-10-02

- Move the related Question to the bottom of each ordinary section, after its
  content and changed file lines. Bold the full label, id, wording and link text.
- Keep meaningful ASCII diagrams between scan points and explanation when
  useful; the Question footer supplements them. Summary and Next remains independent.
- Update the section template, recorded / Session / Proposed forms and examples.
- Fresh-context validation confirmed fully bold linked footers, useful diagrams,
  input-driven section order and a Summary and Next without attribution.

## [0.10.0] — 2026-10-02

- Form normal chat sections from the user's input first, then associate them
  with questions. Preserve section order and use no additional Question wrapper.
- Put the Question association immediately after each ordinary section title,
  before its scan points. Support verified recorded links, Session questions,
  Proposed questions and optional Block / Project context.
- Keep Summary and Next independent, without Question or ownership lines.
- Link to ask-questions for evolving question matching and clarification;
  distinguish the agreed report/Q01 placement from actual existing link targets.
- Fresh-context use confirmed ordering, recorded links, equal ids in different
  Blocks, proposed candidates and Session fallback across three discussion cases.
  Follow-up review clarified multilingual brevity and limited Git reporting to
  actual task edits; active instructions now use neutral reader wording.

## [0.9.3] — 2026-10-02

- The heading line is dots (`·`), not `─`: `## 1. ✅ What's in Place ······`. JL: "could you make it to be the
  dots?"

## [0.9.2] — 2026-10-02

- Each section heading ends in a light `─` line padded to 56 columns, so headings end in one column and the
  line separates the sections: `## 1. ✅ What's in Place ──────`. JL: "for the heading, could we add the light
  separation".

## [0.9.1] — 2026-10-02

- No separator lines around the sketch: the fenced block already stands apart, so a blank line above and below
  is enough. JL: "or we don't need the separation, just leave the space?"

## [0.9.0] — 2026-10-02

- Sections are numbered: `## N. [emoji] Short Headline`, 1, 2, 3 in reading order, the summary last; "2.3" names
  section 2, point 3. JL: "for the index, could we have index, like 1, 2, 3, 4 as well."
- The sketch sits between two dotted `·` rules (was `┈`) and is laid out to be read: one step per line with a
  short note beside it, up to 10 lines and 72 columns (was 6 lines, 90 columns). JL: "could we make it with
  dots? and make it readable, it could be several lines."

## [0.8.1] — 2026-10-02

- The sketch gets emoji and a light rule: a line of `┈` as wide as the sketch above and below it, no side
  borders; one emoji in front of each node (✅ 🔶 ⬜ 🙋 ❗ for state, 📥 📤 🔎 📄 🧮 🎯 for things); rows that line up
  carry the same number of emoji. JL: "how could I have the diagram with the emoji and have the light separator?"

## [0.8.0] — 2026-10-02

- Every section carries one sketch between its scan list and its prose: a very concise ASCII drawing (at most 6
  lines, 90 columns) of the thing the points are about: a flow, a before and after, a mini comparison, a share
  bar, a state line or a small tree. JL: "in each section, could we add the very concise diagram-ascii to explain
  the content of it?"
- A sketch draws, never restates the list; a section with nothing to draw has none. The four bigger-block cases
  (folder tree, compared table, verbatim output, file:line report) stay and may stand in for the sketch.
- Section order is now scan -> sketch -> explain -> files; the example shows a sketch in each section.

## [0.7.0] — 2026-09-27

- The last section of every substantive reply is `## 📋 Summary and Next`: where things stand and what comes next (JL 260927).
- No `📁 File Changes` section any more: a leftover (a side effect, another session's file that could slip into a commit) is one sentence in the closing section's prose.

## [0.6.1] - 2026-09-26

As concise as possible. JL: "I want the file changes to be in each sections, and
make the files changes to be as concise as possible."

- A file line is one line: file name (or the shortest unique path, never absolute),
  where, and the change in 8 words or fewer; `Check:` also 8 words or fewer.
- Files with one shared change share one line; the folder is said once in prose.
- Generated outputs go under the section that made them.
- The closing `📁 File Changes` appears only when git shows unclaimed files or a
  dangerous one; otherwise it is left out. Other sessions' changes are mentioned
  only when they could slip into a commit.

## [0.6.0] - 2026-09-26

Files live in their section. JL, reading a reply whose last two sections were bare
path lists: "could we [attach] this to each section? ... because changes and file
to review these two are just without information."

- A section whose work changed files ends with those files, after its prose.
- Every file line says what changed and where: ``- `path` (where): the change``.
- 👀 is now a mark on a file line with `Check:` and what to look for; the separate
  "Files To Review" section is gone.
- `## 📁 File Changes` stays, still derived from git, but holds only what no section
  claimed (generated outputs, side effects, other sessions' changes, dangerous
  files), each with what it is; one line when nothing is left over.
- Worked example updated to show both.

## [0.5.1] - 2026-09-20

- Limit the reply format to chat; artifact headings follow their own template or directory rules.
- Align the default scan format with numbered scan points and keep explicit response exceptions.
- Place the final file inventory consistently in the worked reply example.

## [0.5.0] - 2026-09-20

- Clarify that this reference does not self-activate and has no root
  `CLAUDE.md` pointer in the current checkout.
- Define the scoped table-only and remote-error response exceptions.


## [0.4.0] - 2026-09-09

SCAN -> EXPLAIN inside each section. JL: "No this is too scatter, what I want is
`## 🛡️ Two Escapes I Built In` / `- Compact Form xxxxxxxx` /
`- Inventory Sections Exempt` / `Paragraphs to explain`."

The first draft of this version put the takeaways and the explanation INSIDE
every bullet, as nested children under a bold title. That is what scattered the
reply: one point was broken across three indent levels, and the scan layer was
buried under the detail meant to support it. The revised rule pulls the two
apart into two layers of the SECTION, not of the bullet:

- Each ordinary section begins with 1 to 6 flat `**Title**: takeaway` bullets.
- Optional explanation paragraphs follow the complete bullet list, in the same
  order, and repeat the bold title so each paragraph maps to its bullet.
- A short point with no needed context stays a single bullet and gets no
  paragraph. No nested takeaway bullets are needed.
- 📁 File Changes and 👀 Files To Review remain flat inventory lists, with no
  explanation layer.
- The worked example demonstrates the point-first, paragraph-second shape.
- NUMBERED, not dashed. JL: "mabe change - to be 1. 2. 3? amd make the as short
  and concise and readable as possible." The scan layer is `1.` `2.` `3.`; a
  dash list now means an INVENTORY of paths or names, so the two are visually
  distinct on sight.
- PLAIN PROSE below the list. JL: "a few bullet points of 1, 2, 3, and then we
  just have the paragraphas as before for details." Two intermediate drafts tried
  to key each paragraph to its point, first by repeating the bold title and then
  by opening `**1.**`. Both put the same words on the page twice and made a
  section read like a form. Paragraphs are now ordinary paragraphs: no keys and
  no repeated titles.
- ONE HARD CAP, on the scan point only: <= 14 words including the title, on one
  line. JL: "the paragraphs can be detailed." The prose layer is deliberately
  UNCAPPED, because the point cap is what pushes mechanism, argument and caveat
  out of the list and into the prose, and a second cap there would only push
  them back. Titles drop to 1 to 3 words, since the number now does the pointing.
  The only thing to avoid is padding a section that had nothing more to say.
- REVERSES the `0 prose paragraphs` rule that 0.2.0 set. Prose is legal again,
  but in one position only: under a completed scan list, never as the reply
  itself and never above the bullets. 0.2.0 banned prose because it drifted into
  unstructured replies; the ban then pushed every explanation into nested
  bullets, which is the scatter this version removes. The rules block states the
  new limit as `prose is allowed HERE ONLY`.


## [0.3.0] - 2026-09-09

RENAMED `claude-response-format` -> `response-format`, reversing the 1.0.1 rename
of 2026-06-02. JL: "update this Tools/plugins/haipipe-toolkit/skills/0_utils/
claude-response-format to be response-format." The `claude-` prefix said nothing
the folder did not already say: every skill here is a Claude skill, and the
prefix only made the invocation longer. It now sits with the other unprefixed
methods in `0_utils` (`diagram-ascii`, `field-test`, `notebook-cell-python`,
`remote-error`), which carry no vendor prefix either.

- `name:` in SKILL.md frontmatter and the `Skill:` header line follow the folder.
- Repo `CLAUDE.md` Rule 5 now cites `.../0_utils/response-format/`.
- The live cross-reference in `remote-error/SKILL.md` points at `/response-format`.
- Body text corrected: the pointer lives in the repo `CLAUDE.md`, not
  `~/.claude/CLAUDE.md`. The spec itself is unchanged, this is a rename only.


## [0.2.0] - 2026-08-29

OUTLINE REPLACES DIAGRAM. JL: "for this one, I want you to update it so it will
just reply all the things in the bullet point format."

The 0.1.x spec set the SECTION shape (`## [emoji] Short Headline`) and then said
of the content: "prose, bullets, tables, code — all fine." That permission is
what the reply format kept drifting through. `~/.claude/CLAUDE.md` had been
patching around it from the other side with a diagram-first rule and a prose
budget ("a paragraph longer than 2 lines = a diagram you have not drawn yet"),
which produced replies built out of ASCII boxes that were, most of the time,
lists drawn with box-drawing characters.

- Content is now an OUTLINE: nested bullets, and zero prose paragraphs. A
  paragraph is a bullet that has not been split yet.
- Countable rules, so it can be checked rather than felt: one bullet = one fact ·
  <= 2 lines per bullet · <= 3 levels · <= 6 top-level bullets per section ·
  a bold lead-in label on every top-level bullet · numbers live in the bullet.
- "Line 1 is the answer" was promoted from CLAUDE.md into this spec, so the
  answer-first rule and the outline rule live in the same file.
- A fenced block is now EARNED, not default. Four cases keep it: a before/after
  tree, a real compared table, verbatim output (log, error, return block,
  command), and a file:line report. A block that is only a list drawn with box
  characters was never a diagram, and becomes bullets.
- Carried over unchanged from CLAUDE.md so this file is self-sufficient: define
  every term at first use, say the real name, no em-dashes.
- The 📁 file-changes and 👀 files-to-review sections survive, restated as bullets.

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [0.1.2] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.2.0; older entries below keep their original numbers).

## [1.2.0] — 2026-06-26

- changed section headers from kebab-case slugs to natural readable headlines in title case.

## [1.1.0] — 2026-06-09

- merged claude-chat-format; added end-of-run file-change report (📁) and conditional review-list (👀) sections; enabled Bash for git status.

## [1.0.1] — 2026-06-02

- renamed skill dir response-format -> claude-response-format.

## [1.0.0] — 2026-06-02

- initial spec; referenced by repo CLAUDE.md Rule 5.
