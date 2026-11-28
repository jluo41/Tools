# The face

Part of hai-studio's topic contract (`ref/topic-contract.md`).

**Title:** when the Block's face names its Studio bands (`bands: s0N 🧱 Block Structure · s1N 👀 Block Job UI Preview`),
a topic's title starts with its band's name, then which one it is: `s02 · Block Structure: Blueprint`. `new_topic.py`
writes it so; `scripts/topic_titles_check.py` finds a title that does not (A05).

**Placeholders:** a name that is not fixed (a slot an instance fills in, a thing not decided yet) is written in 〈 〉:
`〈Job type 1〉`, `bNN_〈block〉/`. A real, agreed name carries no brackets (A07; `scripts/placeholder_check.py`).


```text
sNN · <title>
=============
view: findings

**Tags:** `<tag>` · `<tag>`

**Stage:** explore

**Why:** <the one question this topic answers, in a sentence>

**Topic:** <one paragraph: what this topic thinks through, and why now>

**Feeds:** Q01 · Q02

Q01 · Answer
------------
**Answer:** <the answer today, in one or two sentences>
**Evidence:** [<frame name>](sNN-<topic>.excalidraw) · <a file in the Block>
**Limits:** <what the answer does not cover yet>

Files
-----
(a tree of the folder)

Decided
-------
sNN-D01 · <what was decided> (<who> <date>)

Open
----
1. <an open point>
```

**`view:`**: the focus page's view this topic shows in, on its own line right under
the title's underline: `overview`, `standing`, `findings` or `delivery` (a Work Block (Blueprint) also
`ui-block`, `ui-job`, `ui-task`, `ui-run`). Without it, or a `**Tags:**` tag of the same name,
the topic shows in no view's Around the Work at all (b12 on 261109: every topic hidden).
Pick by what the topic is for: background and maps `overview`, where a wait stands `standing`,
an answer to a Question `findings`, a page or email to hand over `delivery`.

**`**Why:**`**: the question the five-part drawing's Idea part asks. `studio_update.py` draws no
five parts for a face without it (261109: the 10-31 run drew "why do we need s02?" on 19 topics).

**A Question's answer lives in its topic.**
`**Feeds:**` names the Block's Questions (`Q01`) this topic answers, and each gets a
`Q01 · Answer` part in the face: the answer, its evidence (a frame of this topic's drawing,
linked by its exact name, and files in the Block), its limits. The board.md Question's `report:`
points at the face (`sNN-<topic>/sNN-<topic>.md`). There is no `reports/qNN_*/` page and no
report drawing; an older `reports/` folder moves to `_old/reports/` once its answers are in.

The stage (b10 s09-D03): how far along the topic is, one word on its **Stage:** line.

```text
🌱 explore   rough drawing, many red ?, no plan yet
🔶 shaping   decisions made, open points and red ? still left
✅ agreed    no red ? and no open point left; the person signs; a Job may be built from it
📦 closed    its Jobs closed, the Reports it feeds answered; frozen
```

1. **A person moves it**: change the line and add a decision row, `sNN-DNN · Stage → agreed (JL <date>)`.
2. **The gate only counts**: red marks left, Open items, dated decisions, frame checks; it never moves the stage.
3. **New topics** start at explore (`new_topic.py`); the shared Studio shows the stage as a badge on each card,
   and "no stage" when the line is missing.

The Idea Studio reads the face by these marks, so keep them:

1. **`**Topic:**`**: its paragraph is the row's one line.
2. **`**Feeds:**`**: every Question named there (`Q01`, or an older `qNN_<topic>`) becomes a
   chip on the row, and the topic is listed in that Question's row (`hai-report`).
3. **Decided**: each line starting `sNN-DNN` counts as one decision.
4. **Open**: each numbered line under the `Open` heading counts as one open point.
5. **ASCII headings** (`===`, `---`), as every doc here.
