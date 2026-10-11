---
name: response-format
description: >-
  Canonical spec for the assistant's chat reply format in this workspace: the
  answer on line 1, then sections driven by the user's input. Numbered one-line
  scan points state the takeaways, a short readable ASCII sketch draws the content
  when useful, and plain prose paragraphs carry the detail. Changed files follow
  the explanation, one short line each saying what changed. Each ordinary section
  closes with Related studio: the owning Block, its sNN topic and what the section
  adds. Related question is optional when a recorded Question is being addressed.
  The last section is always the summary and next steps, without either line; there is no
  file section. This is a reference spec and
  does not self-activate. Trigger: response format, reply format, outline format,
  bullet points, section headers, emoji headers, 回复格式.
argument-hint: "(reference spec — usually not invoked directly)"
allowed-tools: Bash, Read
metadata:
  version: "0.20.0"
  last_updated: "2026-10-10"
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
- Studio associations describe where the discussion belongs: the owning Block
  and its sNN topic. Saving a topic, Question or Report is separate work through
  its owning skill; an association line does not create or change those files.


The format
----------

**Line 1 is the answer.** A bare answer, before any heading, before any bullet.
A closed question gets its yes, its no, or its one name, and nothing else on
that line. Never build up to it.

**Everything after line 1 is sectioned.** Form the sections from the user's
current input and the relevant session context, in a natural discussion order.
Then associate each ordinary section with the Studio topic it advances. Its content
starts with a NUMBERED list of one-line points, followed by a concise ASCII sketch
when there is a useful relationship to draw, then plain prose for whatever needs
explaining. Changed files follow the explanation. The closing **Related studio**
line names the owning Block, its sNN topic and what this section adds. When the
section directly addresses a recorded Question, an optional **Related question**
line may precede it. Summary and Next has neither.
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

**Related studio:** [<Block> sNN-<topic>](<workbench Studio topic URL>): <what this section adds>
```


Studio associations
-------------------

Determine the reply's content and section order from the user's input first;
match the sections to Studio topics afterwards. The topic list helps locate the
work; it does not replace the user's discussion with a board outline.

**Related studio is the default** (2026-10-10). Close an ordinary section with one
Studio association: the owning Block, an existing sNN topic and one short line
saying what the section contributes. Several sections may share the same topic.
Use the topic being worked on, even when the section changes a skill or code
rather than a drawing. A topic owns the discussion; its drawing is one of its files.

```
**Related studio:** [<Block> sNN-<topic>](<workbench Studio topic URL>): <why>
**Related studio:** (proposed) <Block> "<topic title>": <why>
```

1. **Block**: the Block owning this work, named explicitly, such as `b01_haipipe-toolkit`.
2. **Topic**: the existing `sNN-<topic>` folder, with its real name and number.
3. **Why**: what this section settles, changes, checks or leaves open for that topic.
4. **One topic**: choose the closest one; do not attach a list of loosely related topics.
5. **Existing first**: reuse the topic already being discussed before proposing another.

A Job or Task may select the work context, but the Studio association names its
owning Block. Existing topics still stored under a Job or Task can appear in the
Block's shared Studio. Link that actual topic, retaining its source-qualified
anchor; do not claim the files have already moved to the Block's `studio/`.

**The link** opens the shared Workbench's Studio with the topic expanded in place:

```
<host>/_board/workbench?path=<block folder>&studio=1&studio_group=all#topic-sNN-<topic>
```

1. **Path**: the Block folder relative to the served SPACE root; URL-encode the query value.
2. **Anchor**: use the topic row's actual id, as `frame.studio_anchor` produces it.
   A Block topic uses `topic-sNN-<topic>`; an existing Job topic may use
   `topic-jNN_<job>--sNN-<topic>`. This keeps repeated sNN numbers distinct.
3. **All**: `studio_group=all` makes the link work even when the topic is outside Current.
4. **Host**: use the host already serving that SPACE and its configured public origin.
   Never start a host just to make an association link.
5. **Fallback**: when no host is available, link the topic's existing notes or drawing
   file. Do not guess a URL, a path or an anchor.

Example for the existing shared-Studio design topic, still stored in its Job:

```
**Related studio:** [b01_haipipe-toolkit s04-studio-and-report](<host>/_board/workbench?path=blueprints%2Fb01_haipipe-toolkit&studio=1&studio_group=all#topic-j03_project_workbench--s04-studio-and-report): settles how Studio is shared across levels.
```

**No matching topic**: if the owning Block is known, write an unlinked `(proposed)`
Studio title. Never invent an sNN, a folder or a link. The reply itself creates
nothing; creating a topic requires the user's authorization and `haipipe-studio`.
When the section has no known Block or Studio work, omit the association instead
of inventing one. A trivial answer line needs no association.

**Related question is optional**. Include it only when the section directly
answers, reviews or updates a recorded Question. It supplements Related studio
and appears before it; ordinary design discussion does not need a QNN.

```
**Related question:** [<owner> QNN "<short question>"](<workbench Question URL>): <why>
**Related studio:** [<Block> sNN-<topic>](<workbench Studio topic URL>): <why>
```

Use the real Question owner and its existing QNN. A Block, Job or Task Question
can open in that owner's shared Workbench Report view:

```
<host>/_board/workbench?path=<question owner folder>&space=Audience+Report#question-QNN
```

Verify the row exists; without a serving host, link its existing report file.
`haipipe-question` owns creating Questions and `haipipe-report` owns their Reports.
A missing QNN never forces a proposed Question or a new report folder just to
satisfy the reply format.

The final **Summary and Next** has no Related studio or Related question line.
It summarizes the whole reply and may mention topic or Q ids naturally in its
points or prose.


Inside one section: scan, see, then explain
-------------------------------------------

Each section's content has three layers in THIS order. First a numbered scan
layer of one-line points. Then a sketch when useful: a very concise ASCII drawing
of what the points are about (see "The sketch"). Then plain prose for whatever
needs more context. A
reader who stops after the numbers already has the point; a reader who stops after
the sketch has seen it. A section whose work changed files adds a fourth layer:
its file lines (see "Files live in their section"). Last comes the Related studio
line: the Block and sNN this section advances, and why. An optional Related question
line comes before it when a recorded Question is directly addressed.

```
scan point   N. **Short title**: one takeaway. ONE line, <= 14 words
sketch       a ```text block: draws the thing, one step per line, emoji on its
             nodes, <= 10 lines, <= 72 columns; a blank line around it
prose        plain paragraphs after the whole list. no keys, no titles.
             as detailed as the point deserves. skip it when it adds nothing
file lines   - `name` (where): change in <= 8 words. only if the section changed files
related q    **Related question:** [<owner> QNN "<short question>"](<Question URL>): <why>. optional
related st   **Related studio:** [<Block> sNN-<topic>](<Studio topic URL>): <why>. default, last
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
heading -> scan -> sketch -> explain -> files -> related q -> related st   ordinary ORDER
summary: heading -> scan -> sketch -> explain               no related question or studio
studio match follows drafting   user's input drives content and section order
one Studio topic per section    default Related studio line: Block, sNN, contribution
Studio link opens the topic     /_board/workbench?path=<Block>&studio=1&studio_group=all#<actual topic id>
Question link is optional       /_board/workbench?path=<owner>&space=Audience+Report#question-QNN
Studio = the discussion topic   its drawing is a file; Job and Task reuse the Block Studio
proposed topic has no sNN        no invented folder or link; creation needs user authorization
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
body prose follows scan          Related studio closes; optional Related question precedes it
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
  studio or Related question line.
- **Honest headlines** — the headline names what is under it. Never pad to hit a count.

The sketch (2026-10-02)
----------------------

A reader takes in the first line and the pictures first. Keep a sketch between
the scan list and the prose whenever it helps draw the section's content. It is
an ASCII drawing, in the shapes of `/diagram-ascii`, laid out to be read: one step
per line, a short note beside each, several lines when that reads better than one
long line. The Related studio line supplements this diagram; it does not replace it.

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

1. **In the section**: changed files follow the explanation, before the association lines.
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

**Related studio:** (proposed) b01_haipipe-toolkit "Skill instructions and reply format": gives the verdict and when the format applies.

## 2. 🛠️ What I Changed

1. **Builder fixed**: the trigger now skips days with no readings
2. **Rebuilt**: the generated function matches the builder again

  ❗ before   empty day ─▶ window ─▶ a case with no readings
  ✅ after    empty day ─▶ skipped

The builder counted empty days as windows, so every empty day produced a case with
no readings. It now skips them, and the rebuild picked that up.

- 👀 `builder_x.py` (`build_cases`): skip days with zero readings. Check: skip before window cut
- `fn_case/x.py`: regenerated from the builder

**Related studio:** (proposed) <Project> b02_record "Record-to-case rules": settles how empty days are handled.

## 3. 📋 Summary and Next
1. **Now**: empty days no longer make cases; the CaseSet is rebuilt
2. **Next**: pick the model, Bedrock (BAA-covered) or a local in-VPC model
3. **Topic**: the proposed Studio topic remains unnumbered until creation is approved

  ✅ builder fixed
  ✅ CaseSet rebuilt
  🙋 model pick        Bedrock or a local in-VPC model
  ⬜ proposed topic    "Record-to-case rules", no folder created
  ⬜ training Run      starts from this CaseSet

The rebuild wrote `_WorkSpace/3-CaseStore/x/@v0002/`, which git ignores. Once the
model is picked, the training Run can start from this CaseSet. The proposed Studio
topic names where this discussion belongs; it has no sNN or folder yet.
```

## 📎 "Show me" means in the reply (2026-09-04)

"Show me", "preview", "so we can understand it": paste the content INTO the
reply, as bullets or a real table. The requested preview belongs in chat so the
reader can inspect it immediately. Create a separate Artifact when the user
requests an artifact or page.
