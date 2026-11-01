# Studio follow-ups · answers

received: 2026-10-31 16:41

for: b35-s01:studio @ studio_skill

Three choices left from the sNN move and the retired sNN page.

## Q1 · Who draws parts

Every sNN drawing has five parts (Idea, Now, Design, Process, Delivery). Only five_parts.py knows this; the excalidraw skills do not.

```text
today   five_parts.py draws all 5; excalidraw-job, -task draw a whole drawing
A       excalidraw-studio owns the 5; job, task, story draw Design only
```

**Who owns the five-part drawing?**

- [x] A · excalidraw-studio owns it; the kind skills draw only the Design part.
- [ ] B · Each kind skill keeps its whole drawing; excalidraw-studio only links five_parts.py.
- [ ] C · Leave the skills as they are for now.

Why A: One owner for the shape; each kind adds only what differs.

Answer: A, my pick.

## Q2 · Loose studio folders

Every sNN is out, but 305 studio/ folders still hold loose things. s01-D12 says no studio/ folder.

```text
131 drawings · 77 .py · 47 _build/ · 48 _groups.txt
22 chat/ · 20 draw/ · 26 legacy/ · 12 question-map
```

**What happens to the loose studio/ folders?**

- [ ] A · Helpers to scripts/, maps beside board.md, the rest to _old/studio/.
- [ ] B · Keep studio/ for loose things only; an sNN never goes in.
- [x] C · Make each loose drawing an sNN, then delete studio/.

Why A: No studio/ left, nothing lost, and no new topics past the limit of 9.

Answer: C, changed from my pick A. Where the note below says otherwise, the note wins.

> note: We will not have the studio anymore, we will just use the sNN under the block, or job or task folder.

## Q3 · Runs in Process

The drawing's Process part ticks each Task. Each Run's run.yaml also says its status, agent and skill.

```text
today   ✅ t01_build_table   ⬜ t02_check_rows
A       ✅ t01_build_table · r01 done · JL · haipipe-task
```

**Does Process show each Run?**

- [x] A · Yes: each Run's status, agent and skill under its Task.
- [ ] B · Only each Run's status.
- [ ] C · No: Process keeps one tick per Task.

Why A: Who runs what is the question a reader asks first.

Answer: A, my pick. Where the note below says otherwise, the note wins.

> note: Yes, we should do it,

## The pasted text

```text
haipipe-interaction answers · r01_collect_studio_followups · Studio follow-ups · 2026-10-31 16:40
form: /blueprints/Project-PageParts/work/b35_studio/runs/r01_collect_studio_followups/r01_collect_studio_followups.html
built: 2026-10-31 16:26:42.701521
Q1 · Who draws parts: A · excalidraw-studio owns it; the kind skills draw only the Design part.
Q2 · Loose studio folders: C · Make each loose drawing an sNN, then delete studio/. (changed from A)
   note: We will not have the studio anymore, we will just use the sNN under the block, or job or task folder.
Q3 · Runs in Process: A · Yes: each Run's status, agent and skill under its Task.
   note: Yes, we should do it,
```
