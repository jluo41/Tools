# Blind review brief: the design theme's page drawings (stage 1, drawings only)

You review drawn page designs for a research workbench. You did not build them. Never edit any file except the one
report file you are told to write. Look at each picture first (Read tool on the PNG), the code only if you must.

## What the pages are

The design theme makes N designs for one goal by one method, checks them and releases the kept ones.
- Block = one application, one channel (`Design-PreVisitChecklist`): goals, Jobs, rounds (one per inputs version), method scores.
- Job = one goal × one method version × one inputs version → N designs (`j01_prepare-before-visit_goal-only`).
- Task = one method step, three types: A 💡 t00 reason ideas (② ideas from the Job's inputs fence), B ✏️ one design
  (③ generate, ④ verified by another agent, revised until it passes), C 🏆 t99 review whole (⑤ rank, keep top n).
- Each page has sections: Report (check: results and progress), Work (do: the children, their next move), Studio
  (think: drawings and topics). Interactions, Delivery, Timeline, Files are right-rail sections, never views.
- A person signs only at the Block (goals, rules) and the Job (Review and approve = freeze predictions + release).
  No Task asks the person a question.

Each picture is one view (lettered A, B, C … or A1 … C3 for Task types × steps) drawn as a full screen: path,
title-&-section, view-button-list (open view orange in drawings only), goal-line, view-caption, then content.
Rails are drawn on purpose as pale short lines with no words (hidden until hovered). Words in angle brackets are
placeholders on purpose (the repository is public; the real designs are private). Folder names are real.

## Settled decisions you must not undo (say so instead of proposing it)

- JL 261012: the Block's Report opens on Summary, one row per Job, no design cards there; Next in plain words.
- JL 261011: a Job is always named by its full folder name, never a bare jNN; a goal and a method by their words.
- JL 261031: each section is a numbered boxed heading bar "N · emoji name" (no fold arrow); the main point first and
  large; helpers (the drawing, the mind map, Ask the agent) only at the bottom after a dashed rule; rails pale lines
  with no words, hidden until hovered (do not ask for rail words).
- JL 261101: a Report view is its numbered sections only: no ⚙️ Process or 📊 Results band, no "waits on you"
  section. A Work view is two bands, ⚙️ Process (🙋 Waits on you first, then the view's steps) then 📊 Results (the
  Report's own sections, read only), each numbered from 1. There is no "Runs" view: each step shows its own Runs.
- Report and Work of one page share view letters and names.
- JL 261101: a design is shown with b12 s32's design card: three columns, Design (as its reader sees it) ·
  Process ③ (each element's source) · Review ④ (tests, expected outcome, ⑤ rank).
- Earlier drafts live only in their Runs; dropped designs stay, folded.

## The rules

Five-second test: What is this? (name and goal) · Where am I? (path) · What is here? (open section, content
visible) · What can I do? (verbs next to what they act on).
1. Where am I, on top: path, title-&-section, view-button-list, goal-line (Purpose Block, Goal Job, Aim Task). No counts under the title.
2. One place, one job: left-rail pages, right-rail sections, view-button-list under the title, then goal-line, then caption, content centre.
3. Every section has a verb; the title shows only the section's name.
4. Content first: no instruction paragraphs; no fold arrows except section headings.
5. Every mark has a word; an action is a verb button on its row, at most three; real folder and file names.

Rubrics, each /10: Glance (four questions from the picture alone) · Place · Lean (no instructions, counts, ids,
one item a line) · Words (every mark a word; verbs on rows ≤3; real names) · One job (each view answers one
question; nothing shown twice across views; no rail section as a view) · Same look (white boxes, 1 px grey border,
rounded; reads like its sibling views) · Salience (main point first and largest; content shown as what it is:
tables, cards, chains, tiles; not only headings with a grey line). Phone is n/a. Pass = every rubric ≥7, mean ≥8.

## What to return

Write your report to the file you are given, and return the same text (under 600 words):

```text
cell <sNN-…>
  <L>  Glance N · Place N · Lean N · Words N · One job N · Same look N · Salience N · mean N · pass|not yet
       worst: <the one thing on screen that costs most>
  …one line pair per view…
across views
  1. <a problem that repeats across views or cells, with the views it hits>
  2. …
proposals (most valuable first, at most 5)
  1. <move/remove/rename/add> <thing> <where>: <why, one line>
  …
```

Also check consistency: between Report and Work of the same page (same letters, Report = results, Work = next
moves), between levels (Block row → Job page → Task page tell one story), and with the earlier design element
gallery (proposed look of one design: `b12_theme_design/s32-design-element-ui/shots/proposed__design.png`
and its review table proposed__review.png).
