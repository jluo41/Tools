# Page folds: the drawer below the read
state: 🟡 PARTIAL · rules settled on QB4, carved 260729; face awaits JL
owner: CC
method: Law, Lesson, Glossary, Discussion, Comments, Log sit folded below the reading path

## Question
What lives below the main reading path, and why does it start folded?
Law · Lesson · Glossary · Discussion · Comments · Log preserve rules, failures, vocabulary, deliberation, pinned remarks, and history for readers who need them, while Opening through Files stays a clean first pass.
The renderer assembles this drawer from a fixed list (`page_question.py`), so a section name it does not know renders nowhere, which is why a new section is a template decision (`QB4`, which owns the template), never a page-local invention.


## Boundary
- ✅ Covered here
  Which sections fold below the read, their order, and the rule that they never fold a sentence's apparatus.
- ↪ Covered elsewhere
  What a Comment IS and its lifecycle: `QB5b`. The Log line format: `SKILL.md`'s sync table.
  Retired section names (`Why here`) and aliases: `src/common.py`'s `ALIAS`.

## Diagram

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/BoardSkillBoard-260722/board.excalidraw&frame=QAa6

## Content
### 1 · What the folds convey
```
🗃 the folds · answers: what was ruled, learned, and changed, if I need it?
──────────────────────────────────────────────────────────────
conveys   durable memory that must not tax the first read
holds     Law, the binding rules · Lesson, what failure taught · Glossary,
          the words · Discussion, the deliberation · Comments, pinned
          remarks · Log, the reverse-chronological history
source    each an optional ## section in the .md; the renderer assembles
          the drawer from its own fixed list, in its own fixed order
rules     always below the read, always starting folded · Log newest
          first · a new fold section is a template decision on QB4, never
          a page-local invention · a sentence's ⚑ apparatus folds under
          its sentence, never down here
omit      any may be absent · an empty fold never renders
```
Law, Lesson, Glossary, Discussion, Comments, and Log sit below the main reading path and begin folded.
They preserve rules, failures, vocabulary, deliberation, pinned remarks, and change history for readers who need them, while Opening through Files remains a clean first pass.
Retired Why here content is still parsed here for compatibility, but new rationale belongs in Question.
Under the base/variant model on `QB4`, the folds are frame: identical for every page kind.



The folds never swallow apparatus: a `>` run bound to a sentence folds under that sentence (`QB5a`), and the supporting folds render their own `>` threads as plain discussion, exactly as before the sentence apparatus existed.

### 2 · Fold prose takes comments like any other sentence
Since 260731 the drawer is not read-only: select or double-click a prose sentence in Law, Lesson, Glossary, or Discussion and it takes a `> WHO:` comment exactly like main prose, because `serve.py`'s anchor rule lands on any plain source line regardless of its section.
What still refuses is what cannot anchor: rendered comment rows, a sentence's own apparatus, and Log rows, which are records rather than sentences.



## Items to Finish
- [ ] 🧠 JL confirms this face owns the folds
      Carved 260729 from QB4 §7 with the text verbatim; the history stays on `QB4`.

## Where we are
Settled and shipped; the fixed fold list in `page_question.py` is the enforcement, and its lack of a catch-all is deliberate.

- 260731 JL · 💬 Fold prose now takes sentence comments
  JL asked on this page's own Discussion, "can I add comments?", and the answer was no: three blanket `.folds` guards in `board.js` (the highlight scanner, the select-to-comment path, and the double-click editor) refused every sentence in the drawer.
  The refusal was frontend-only, since `serve.py`'s anchor rule already lands a `> WHO:` row under any plain source line, wherever its section sits.
  The guards now exclude only what cannot anchor: rendered comment rows (`.cmt`), a sentence's apparatus (`.sapp`), and Log rows, which never were `<p>` sentences.
  Shipped in haipipe-board 0.59.0.
- 260731 JL · 📸 The discussion box takes pasted screenshots
  JL followed up: "when I take the screenshot, can it be paste there?", so pasting a clipboard image into the discussion box (and the comment box, `QB5b`) uploads it to this board's `fig/` through the new `/_board/image` and drops `![image](fig/…)` at the cursor.
  The upload stores the file only; the visible row still lands through the normal discuss or comment write, so no new writer touches a page.
  Shipped in haipipe-board 0.60.0.

### Decision Now
- [ ] 🧠 Confirm this face owns the folds
      Carved 260729 from QB4 §7 with the text verbatim, and the fixed fold list in `page_question.py` has enforced it since.
      A tick here also closes the same row in Items to Finish.

## Files
- `src/page_question.py`
  The fold assembly: Why here · Law · Lesson · Glossary · Log, plus the Comments drawer.
- `src/common.py`
  `ALIAS`, the section registry the folds resolve names through.

## Discussion
> JL: can I add comments?
> CC: Yes, since 260731: select or double-click any fold prose sentence and it takes a comment like main prose; only rendered comment rows, apparatus, and Log rows still refuse, because `serve.py` will not anchor on them.

## Log
260801 · §1 renamed "What the folds convey" and opened with the five-row protocol face diagram (conveys · holds · source · rules · omit) on JL's ask; master view on QB4 §0
260731 · The discussion and comment boxes take pasted screenshots: fig/ upload via /_board/image (haipipe-board 0.60.0)
260731 · Fold prose became commentable: the three `.folds` guards in board.js narrowed to what cannot anchor (haipipe-board 0.59.0)
260729 · Marked frame under the base/variant model on QAa0: identical for every page kind
260729 · Opened by carving QA4 §7 out to its own face, text verbatim
