---
name: response-format
description: >-
  Canonical spec for the assistant's chat reply format in this workspace: the
  answer on line 1, then sections driven by the user's input. Numbered one-line
  scan points state the takeaways, a short readable ASCII sketch draws the content
  when useful, and plain prose paragraphs carry the detail. Changed files follow
  the explanation, one short line each saying what changed. Each ordinary section
  answers one question, closed by its Related question line saying why. The last
  section is always the summary and next steps, without a Question; there is no
  file section. This is a reference spec and
  does not self-activate. Trigger: response format, reply format, outline format,
  bullet points, section headers, emoji headers, 回复格式.
argument-hint: "(reference spec — usually not invoked directly)"
allowed-tools: Bash, Read
metadata:
  version: "0.18.1"
  last_updated: "2026-10-03"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: response-format (0_utils)
================================

Canonical reference for conversational replies in this workspace. Apply it when
the user invokes this skill or another active instruction loads it. A skill file
does not make itself always-on, and this checkout has no root `CLAUDE.md` that
activates it.

When a loaded skill defines a reply shape for a specific request, that scoped
shape takes precedence for that request. In particular, `/task-table`'s
table-only response and `/remote-error`'s required report sections are explicit
exceptions to the general answer-first scan format below. Do not combine both
shapes in one reply.

Scope
-----

- Applies to CHAT replies, meaning what the assistant writes back to the user.
- Does NOT apply to file or document contents. Follow the actual directory
  guidance and document template, including their heading syntax. This chat
  skill neither forbids Markdown `##` nor requires ASCII underline headings
  in authored files.
- Question associations describe the chat's relationship to questions. Saving
  a question or updating its Report is separate work through its owning skills.


The format
----------

**Line 1 is the answer.** A bare answer, before any heading, before any bullet.
A closed question gets its yes, its no, or its one name, and nothing else on
that line. Never build up to it.

**Everything after line 1 is sectioned.** Form the sections from the user's
current input and the relevant session context, in a natural discussion order.
Then associate each ordinary section with the question it advances. Its content
starts with a NUMBERED list of one-line points, followed by a concise ASCII sketch
when there is a useful relationship to draw, then plain prose for whatever needs
explaining. Changed files follow the explanation. Each section answers ONE question,
named in its last line, the **Related question**, with why this section serves it.
Summary and Next has none.
The list is what the reader scans, the sketch is what the reader sees, and the
prose is ordinary paragraphs, with no keys and no repeated titles. Never interleave
these content layers.

```
<the answer, one line>

## 1. [emoji] Short Headline

1. **Short title**: the takeaway, the so-what
2. **Next title**: another takeaway

  (a fenced text block, a few short lines, one step per line: the flow, the
   before and after, the comparison these points are about)

The paragraph that explains them, in plain prose, after the whole list. It
covers what the points could not hold, and it is often not needed at all.

(changed file lines, if any)

**Related question:** [<Board> QNN "<short question>"](<workbench question URL>): <why this section serves it>
```


Question associations
---------------------

Determine the reply's content and section order from the user's input first;
match those sections to questions afterwards. A Board register supplies possible
associations, not an outline for ordinary chat. Keep the normal numbered sections
at the same level; do not wrap them in additional Question headings or regroup
them by Board order. Display the association as the section's last element, the
Related question, with one line saying why the section serves it.

**One question per section** (2026-10-03). Each ordinary section answers exactly one
question. When a section's content serves two questions, it is really two sections:
split it. Several sections may answer the same question, so a question can span
sections, but a section never spans questions.

Every ordinary section ends with one Related question line, naming the board and
its question (2026-10-03). A board's `reports/` folder is its list of questions:
each `qNN_<topic>` is one question.

```
**Related question:** [<Board> QNN "<short question>"](<workbench question URL>): <why>
**Related question:** (proposed) <Board> "<short question>": <why>
```

1. **Board**: owner and block holding `reports/`: `Tools/blueprints b01_utils`, `Paper-<Name>`.
2. **QNN**: from the question's folder `reports/qNN_<topic>`.
3. **Short question**: the topic question itself, in quotes, a few words.
4. **Link**: the Question in its workbench, so one click opens it (see "The link" below).
5. **Why**: what this section gives it: answers, narrows, evidences, or raises it.

**The link** (2026-10-06). The link opens the board's workbench UI on its Questions
view, scrolled to that Question's row, so the reader clicks once and sees it with its
work and report beside it (JL: "I can just click and open them"; "what I want is the
workbench UI, not the webpage of the page"). Not `&report=QNN`: that opens the
report's own Page.

```
<host>/_board/<kind>-board?path=<board>/board.md&view=questions#question-QNN
```

1. **Kind**: the board's workbench: `task` (a Task Block, also `Tools/blueprints/bNN_*`),
   `cowork` (a CoWork Block), `discovery` (a Discovery Block). A wrong kind returns 404.
2. **Path**: the board's `board.md`, relative to the SPACE root, with plain slashes.
3. **Host**: the shared host serving that SPACE, its `--public-url`: find it with
   `ps aux | grep _host/serve.py` (for WellDoc-SPACE, `http://100.121.165.84:5622`).
   Never start a host just to make a link.
4. **Fallback**: no host serves that SPACE, or the board has no workbench (a Paper
   board): link the question's file, `<board>/reports/qNN_<topic>/qNN_<topic>.md`.

Example: `[b01_irb Q01 "How to write an IRB submission"](http://100.121.165.84:5622/_board/cowork-board?path=examples-4-agent/Project-Samsung/cowork/b01_irb/board.md&view=questions#question-Q01)`.

**Granularity: a topic, not a decision** (2026-10-03). A board question is a topic
that many sections feed and that grows into its report; the narrow decision goes in
the section's points and its Why. Reuse the board's existing question first. What a
question is, how big it is and how it is created: [haipipe-question](../../1_base/question/haipipe-question/SKILL.md).

The board is the one that owns the section's work. No question fits: write
`(proposed) <Board> "<short question>"` unlinked; never invent a QNN or a link.
There is no Session form. One question per section; several sections may share one.

**Propose its folder** (2026-10-03). A proposed question comes with a proposal to
make it real: the closing Summary and Next offers to create its folder,
`<board>/reports/qNN_<topic>/`, with the board's next free NN, and names the question
that folder will hold. Create it only when the user agrees, through `haipipe-question`;
the reply itself creates nothing. Several sections proposing the same question make
one offer.

Keep the question at topic level and let the Why say what this section adds; preserve
the user's latest clarifications. Ordinary follow-ups feed the same question.
For matching evolving session questions, identifying candidates, or deciding
whether clarification is needed, use [ask-questions](../../1_base/question/ask-questions/SKILL.md).
Simple attribution from an explicit user question can be done directly.

The final **Summary and Next** has no Related question line. It summarizes
the whole reply and may mention Q ids naturally in its points or prose. A trivial
answer consisting only of line 1 needs no Question association.


Inside one section: scan, see, then explain
-------------------------------------------

Each section's content has three layers in THIS order. First a numbered scan
layer of one-line points. Then a sketch when useful: a very concise ASCII drawing
of what the points are about (see "The sketch"). Then plain prose for whatever
needs more context. A
reader who stops after the numbers already has the point; a reader who stops after
the sketch has seen it. A section whose work changed files adds a fourth layer:
its file lines (see "Files live in their section"). Last comes the Related question
line: the question this section serves, and why.

```
scan point   N. **Short title**: one takeaway. ONE line, <= 14 words
sketch       a ```text block: draws the thing, one step per line, emoji on its
             nodes, <= 10 lines, <= 72 columns; a blank line around it
prose        plain paragraphs after the whole list. no keys, no titles.
             as detailed as the point deserves. skip it when it adds nothing
file lines   - `name` (where): change in <= 8 words. only if the section changed files
related q    **Related question:** [<Board> QNN "<short question>"](<workbench question URL>): <why>. always, last
```

1. **Numbers, not dashes**: the scan layer is `1.` `2.` `3.`, never `-`.
2. **One authored line**: keep each point short; avoid manual line breaks.
3. **The title names, it does not tell**: `**Push landed**`, not a sentence.
4. **The takeaway is the consequence**: the verdict, the number, the decision.
5. **The prose carries the detail**: plain paragraphs, as long as they need.

Numbering makes the section countable at a glance. The reader sees three points
rather than an unbounded list, and can say "point 2" out loud without quoting it.

The one-line cap keeps the scan layer concise. It means one short authored line;
the reader's viewport may wrap it naturally. When a point needs several clauses,
its detail belongs in the paragraph below, or it was really two points. The word
limits count whitespace-separated words; in Chinese and similar writing systems,
use a comparably short phrase rather than treating every character as a word.

Below the list, write normally, and write as much as the material deserves. The
scan layer is deliberately starved: 14 words cannot hold a mechanism, an
argument, or a caveat with its conditions attached. Those go in the prose, at
whatever length they need, because a hard cap here would only push the detail
back into the points and undo the split. The one thing to avoid is padding a
section that had nothing more to say, in which case the list simply ends.

Earlier drafts keyed each paragraph to its number and repeated its bold title,
which put the same words on the page twice and made the section look like a
form. Plain paragraphs read better, and the reader can already see which points
they answer.

Dashes now mean something: a dash list is a list of files or names, a numbered
list is an argument. File lines keep their dashes, but a bare path is not
information: every file line says what changed. Never nest anything under a point,
either. Multiple takeaways are multiple numbers.

Rules, all countable
--------------------

```
heading -> scan -> sketch -> explain -> files -> related q   ordinary section ORDER
summary: heading -> scan -> sketch -> explain               no related question
question match follows drafting  user's input drives content and section order
one question per section        one Related question line, last: board, QNN, name, why
link = the workbench question   <host>/_board/<kind>-board?path=<board>/board.md&view=questions#question-QNN
question = a topic               it grows a report; the decision goes in the Why
proposed -> propose its folder   Summary and Next offers reports/qNN_<topic>/
1. 2. 3. not -                   numbered scan layer; dashes mean inventory
1 authored line per scan point   short phrase; viewport wrapping is outside the writer's control
<= 14 words per scan point       title included. count them
1 to 5 scan points               a 6th means the section is really two
title = 1 to 3 words             it NAMES the point, it does not state it
plain prose after the list       no keys, no titles repeated from above
prose runs as long as it needs   this layer is where detail belongs
0 nested children                multiple takeaways are multiple numbers
0 or 1 useful sketch per section <= 10 lines, <= 72 columns, real names inside
one step per line                readable first; several short lines beat one long
emoji nodes, no separators       a blank line around it; no rules, no borders
## N. sections                   numbered 1, 2, 3 ...; the summary is the last
heading = number, emoji, words  no question in it, no dot padding, no trailing marks
why <= 20 words, one line        the section's contribution, not the question again
a sketch draws, never restates   the list redrawn in boxes is not a sketch
body prose follows scan          the Related question closes the section
a file line says what changed    `name` (where): change, <= 8 words, one line
```

One count does the work: 14 words caps the scan point. The prose below it has no
cap, because the cap is what forces detail out of the list and into the prose,
which is the only place it reads well.

Sections
--------

- **Header shape** — `## N. [emoji] Short Headline`: the section's
  number (1, 2, 3 ... in reading order; 2026-10-02), one emoji, a 2 to 5 word
  headline in title case, and nothing after it (the trailing dot padding was dropped
  2026-10-03 as clutter; the question moved to the section's last line, 2026-10-03). Not kebab-case; write it like a headline a human scans.
  With numbered sections, "2.3" names section 2, point 3.
- **Emoji palette**, suggestive and not fixed — 🧩 short answer · 🎯 recommendation ·
  ⚠️ caveat or risk · 🛠️ how-to · 📋 summary and next (the last section) ·
  🔍 findings · ✅ done · 🙋 question for you ·
  👀 (a mark on a file line: read this one) · 🧪 experiment ·
  💡 idea · 📊 results · 🚧 in progress.
- **How many** — 2 to 5 for a typical reply, following the user's discussion,
  with the immediate answer first. One
  section is fine for a small reply. A trivial reply can be the answer line alone.
- **The last section is the summary and next steps** (2026-09-27) — every
  substantive reply ends with `## N. 📋 Summary and Next` (the last number): its scan points say where
  things stand now and what comes next, most important first; its prose holds the
  detail. It is the section a reader who skipped everything else reads, so it
  carries the real state and the real next step, never a list of files. A question
  for the user belongs here too, as the next step it blocks. It has no Related
  question line.
- **Honest headlines** — the headline names what is under it. Never pad to hit a count.

The sketch (2026-10-02)
----------------------

A reader takes in the first line and the pictures first. Keep a sketch between
the scan list and the prose whenever it helps draw the section's content. It is
an ASCII drawing, in the shapes of `/diagram-ascii`, laid out to be read: one step
per line, a short note beside each, several lines when that reads better than one
long line. The Related question line supplements this diagram; it does not replace it.

```text
📥 raw row          FoodName, ExternalSourceID, FoodID
   ↓
🔤 dialect API      vendor code ─▶ the vendor's own word
   ↓
🔎 describe-food    split, search USDA, add up
   ↓
📤 answer           6 values, Conf, Source
```

```text
              today          planned
📤 values     6              14 (FatSecret's list)
🆔 match      hidden         FoodIDResolved, named
🧮 basis      per_100g       per_100g + one serving
```

A flow down the page and a comparison are the two common shapes; a share bar
(`🎯 first pick right  ███████████████░░░░  76.4%`), a state line (`✅ ─▶ 🔶 ─▶ ⬜`)
and a small folder tree, before and after, are the others.

1. **Draws, never restates**: the list redrawn in boxes is not a sketch.
2. **Readable over short**: one step per line, up to 10 lines, 72 columns, never wraps.
3. **Real names and numbers inside**: the same file, field and figure as the text.
4. **No boxes, no rules**: no borders, no separator lines; a blank line is enough.
5. **None when nothing draws**: a section that only states one fact skips it.

Emoji (2026-10-02):

1. **Emoji mark the nodes**: one in front of a name, the same one for the same thing.
2. **Status emoji**: ✅ done · 🔶 partly · ⬜ not yet · 🙋 your call · ❗ risk.
3. **Thing emoji**: 📥 input · 📤 output · 🔎 search · 📄 file · 🧮 numbers · 🎯 score.
4. **Keep columns straight**: an emoji is two columns wide; rows that line up carry
   the same number of emoji before each column. Avoid emoji that need a variation
   selector (⚠️, ✔️): terminals disagree on their width.

No separator lines: the fenced block already stands apart from the numbers above
and the prose below, so a blank line on each side is enough (rules of dots and dashes
were tried on 261002 and dropped as clutter). A flow reads best down the page: a
step, then `↓`, then the next step, each with its note in one aligned column.

The sketch sits after the scan list because the numbers still carry the takeaway:
the sketch shows how the points fit together (what flows into what, what changed
into what, how big one part is next to another). If the only drawing a section can
make is its own list again, the section has no sketch; that was the lesson of
260910, when three box drawings were shown and none belonged. The closing
`## N. 📋 Summary and Next` usually takes a short state sketch: one line per step,
✅ done, 🙋 waiting on the reader, ⬜ next.

Bigger blocks
-------------

Numbered scan points are the default scan layer and prose paragraphs are the default
explanation layer. A fenced block bigger than a sketch earns its place only when the
content is genuinely two-dimensional or must be shown verbatim:

```
a folder TREE, before and after, side by side
a table whose columns are compared across rows
verbatim output: a log, an error, a return block, a command
a file:line report
```

Such a block may stand in for the section's sketch. Everything else that used to
be a large ASCII diagram becomes numbered scan points, a sketch, and explanation
paragraphs. If a block is only a list drawn with box characters, it was never a
diagram.

Carried over, unchanged
-----------------------

- **Define every term at first use**, inline, even when it looks obvious.
  Write `AAMC = Association of American Medical Colleges`, not `AAMC`.
- **Say the real name** — real file paths, real field names, real function names.
  No nicknames, no invented vocabulary, and never pass a subagent's coined word
  through without translating it first.
- **No em-dashes.** Use a colon, a semicolon, a comma, parentheses, or a new sentence.

Files live in their section (2026-09-26)
---------------------------------------

A list of bare paths at the end of a reply answers "which files" and nothing else.
So a changed file is written down next to the work that changed it, as short as it
can be while still saying what changed.

1. **In the section**: changed files follow the explanation and end the section.
2. **Name, where, change**: ``- `name` (where): change``, the change in 8 words or fewer.
3. **👀 means read it**: add `Check:` and what to confirm, 8 words or fewer.
4. **Outputs too**: a notebook or result goes under the section that made it.
5. **No file section**: a leftover is one sentence in the closing section, never a section.

A file line is ONE line; if it wraps, cut it. `name` is the file name, or the
shortest path that is unique in the reply; never an absolute path. When the reader
needs the folder, say it once in the section's prose, not on every line. "Where" is
a line range, a function, or `new`. The change is a verb and an object (`added
hourly reader`), never what the file is for. Files that share one change share one
line.

```
- 👀 `serialize_windows.py` (~141-180): added hourly format and reader. Check: NA rule
- `r05_hourly_start_delta.yaml`, `.sh` (new): b02's fifth Run
- `r09_pt_hourly_start_delta.ipynb` (generated, git-ignored): format on real windows
```

Mark 👀 only on what really deserves a human read: hand-written logic, prose and
docs, the largest diff, the highest transcription risk. Derived and generated files
get no mark.

When this task changed files in a Git checkout, check its current status before
reporting those changes; compare with the initial status to distinguish existing
work from this task's edits:

```
git status --short
git -C <submodule> status --short      # if a submodule such as Tools/ was touched
```

Every file this task actually changed belongs in its section's file lines.
Mention a material unclaimed side effect of this task in one sentence in the
closing `## 📋 Summary and Next`. Pre-existing unrelated changes are outside this
reply's file inventory. Discussion-only replies require no Git check or checkout
inventory. There is no `📁 File Changes` section (2026-09-27): a reply ends on where
things stand and what comes next.

Example
-------

Inside this example each sketch is indented, because fences cannot nest; in a real
reply each sketch is its own ```text block.

```
Yes, and one cheap test settles it.

## 1. 🧩 Short Answer

1. **Claim holds**: the back-test resolves direction before any build
2. **The catch**: a skill alone cannot make a behavior always-on

  📄 an instruction loads it
     ↓
  ✅ the skill runs        ─▶ the format applies

  📄 no instruction
     ↓
  ⬜ the skill stays idle  ─▶ the format is ignored

A skill runs only when it is invoked or explicitly loaded by another active
instruction. To make this format always-on, an active global instruction must
load it; this checkout currently has no root `CLAUDE.md` pointer.

**Related question:** [Tools/blueprints b01_utils Q01 "Point to a skill or restate it?"](<host>/_board/work-board?path=Tools/blueprints/b01_utils/board.md&view=questions#question-Q01): gives the verdict and the one condition under which it fails.

## 2. 🛠️ What I Changed

1. **Builder fixed**: the trigger now skips days with no readings
2. **Rebuilt**: the generated function matches the builder again

  ❗ before   empty day ─▶ window ─▶ a case with no readings
  ✅ after    empty day ─▶ skipped

The builder counted empty days as windows, so every empty day produced a case with
no readings. It now skips them, and the rebuild picked that up.

- 👀 `builder_x.py` (`build_cases`): skip days with zero readings. Check: skip before window cut
- `fn_case/x.py`: regenerated from the builder

**Related question:** (proposed) <Project> b02_record "How are records cut into cases?": empty days made empty cases; the builder now skips them.

## 3. 📋 Summary and Next
1. **Now**: empty days no longer make cases; the CaseSet is rebuilt
2. **Next**: pick the model, Bedrock (BAA-covered) or a local in-VPC model
3. **New question**: create `b02_record/reports/q03_records_to_cases/`?

  ✅ builder fixed
  ✅ CaseSet rebuilt
  🙋 model pick        Bedrock or a local in-VPC model
  🙋 q03 folder        "How are records cut into cases?"
  ⬜ training Run      starts from this CaseSet

The rebuild wrote `_WorkSpace/3-CaseStore/x/@v0002/`, which git ignores. Once the
model is picked, the training Run can start from this CaseSet. If you agree, I will
record "How are records cut into cases?" as b02_record's Q03, so today's fix becomes
the first entry of its report.
```

## 📎 "Show me" means in the reply (2026-09-04)

"Show me", "preview", "so we can understand it": paste the content INTO the
reply, as bullets or a real table. The requested preview belongs in chat so the
reader can inspect it immediately. Create a separate Artifact when the user
requests an artifact or page.
