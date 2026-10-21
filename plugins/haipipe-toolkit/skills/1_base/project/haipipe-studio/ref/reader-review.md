# Reader review: does the drawing answer a reader's questions?

Asked 261012, on a Job topic that showed a few nearly empty boxes: "for things like this, this is very thin, I think
for the /haipipe-studio, after you create such a draw, you should ask it yourself, If I am a reader, will this answer
my questions for this job etc. Maybe you need to call a reviewer for it as well."

A drawing that passes `check.py` can still say nothing. `check.py` measures size, words and layout; it cannot tell
whether a reader who opens the topic learns what they came for. So every new or redrawn topic gets two readings
before it is called done: the maker's own, then a reviewer's in a fresh context. The reader assumed is someone who
knows nothing about this kind of work yet.

```text
draw ─▶ check.py ✅ ─▶ 1 read it as a reader ─▶ 2 reviewer, fresh context ─▶ fix the face or the builder ─▶ again
                          the questions below      haipipe-studio-reviewer-agent        until every question is answered
```


## The questions, by kind of topic

Answer each from the rendered picture alone (the preview png, or each frame rendered on its own), never from what
you know about the work. An answer that needs the face, a page or a receipt opened is a gap.

**A Job topic** (excalidraw-job; a results topic)

1. What is this Job for, in one sentence, and why does the Block need it?
2. What went in (data, models, sources), and what came out (checkpoints, pages, numbers)?
3. What did each Task do, and what did it find, with its real number?
4. What is the one thing the Job concluded, and how sure is it?
5. What is still open or broken, and what would close it?
6. Where do I go for the detail of a Task (its topic, its page)?

**A Task topic** (excalidraw-task)

1. What question does this Task answer, and why does it matter?
2. What words must I know first, defined so I can follow?
3. What is the method, and its formula, with every symbol explained and a worked example?
4. For each source or Run: what did it show or do, step by step, and what did it find?
5. What should I be able to say about it afterwards (an interview line, the takeaway)?
6. What is not checked yet, and where is the source itself (the video, the result folder)?

**A video or Run frame**

1. What is this one about, in a sentence I could repeat?
2. What did the screen show (a screenshot), or what did the Run use (its config)?
3. What numbers came out, before and after?
4. Do I understand each step, and why it holds?
5. What is red (unchecked), and why?

**s00, a Block's background and index**: what the Block is for; which topics and Jobs it holds and how far each has
come; where a newcomer starts; what is proposed next.

**A concept or design topic**: what is decided, what the options were and why this one, what is open, who answers.

**A paper's plan, s03-paper-dataflow and s04-paper-workflow** (haipipe-paper-plan): its four reader questions, in its
Steps. A gap the face cannot close because the drawer does not show it (excalidraw-workflow's `workflow_drawing.py`
or `paperflow_drawing.py`), or that the story owns, is written once in the topic's Open for its owner ("for
excalidraw-workflow: …", "for the story: …") and not reviewed again; the topic is done when every gap left is so
listed.


## 1. Read it as a reader (the maker)

Render each frame on its own and look at it at the size a person sees it (half zoom: a frame's 30 px words read as
15 px). Write one line per question: the answer as the drawing gives it, or "gap: …". Thin is a gap too: a box with
one line where the page holds a paragraph, a Run listed with no number, a frame that names a thing without saying
what it is.


## 2. The reviewer (a fresh context)

Call `haipipe-studio-reviewer-agent` with the topic folder (and the frames, if they are rendered). It reads only the
pictures first and answers the questions above as a newcomer would; then it opens the face and the sources to say,
for each gap, what is on disk that the drawing should show. It returns `answers` or `gaps`, one line per question,
each gap with where its answer lives. It never edits.

The maker fixes the face's words or the builder, redraws, runs `check.py`, and calls the reviewer again until it
returns `answers`. A gap that cannot be closed from disk (the work is not done) is drawn red in place and listed in
the face's Open.


## What done means

`check.py` passes, the maker's reading has no gap, and the reviewer returns `answers`. Save the session with the
reviewer's verdict in its summary (`new_topic.py session … --summary '… reviewer: answers'`).
