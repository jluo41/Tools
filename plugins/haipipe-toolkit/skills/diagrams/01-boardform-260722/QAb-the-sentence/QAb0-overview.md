# The sentence, as the board's atomic unit
state: 🟡 PARTIAL · the unit is settled; the family map is new (260729)
owner: JL
method: one sentence per source line; everything that attaches to a sentence gets its own face

## Question
What is a sentence on a board page, and what can attach to it?
One sentence per source line (0.19.0) made the sentence the board's atomic row: the thing you click, comment on, attach evidence to, and hand to an agent.
This face is the sentence family's front door; the machinery lives on its sibling faces.

## Boundary
- ✅ Covered here
  The sentence as a unit, and the map of what attaches to it.
- ↪ Covered elsewhere
  The evidence card and typed `>` lanes: `QAb1`. Editing the sentence's own text: `QAb2`.
  Whether an agent sees what is attached: `QAb3`. A comment pinned to a selection: `QA6`.
  Filtering, resolving, cleaning up, archiving, and restoring Sentence details: `QAb4`.
  What a marker MEANS in a paper (citation, value, display): `QC0@paper` through `QC4@paper`.
  Whether this family ships as its own skill: `QB7`.

## Diagram

```
   "The coefficient is 0.42 in the pooled model."     ← one source line
        │
        ├── ⚑ typed > lanes beneath it          QAb1  (evidence card)
        ├── 💬 a comment directly under it        QA6
        ├── ✏️ editing + one diff record           QAb2
        ├── 🤖 does the acting agent see these?  QAb3
        └── 🧹 filter, resolve, archive, restore   QAb4
```

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QAb0

## Content
### §1 Demonstration
#### Try the sentence
(One row should reveal the sentence family's interaction without requiring the rest of this page.)
This sentence is the Board's atomic unit, and its evidence, comments, edits, address, and Chat stay attached to this one row.
> Citation: `QAb1` defines the adjacent evidence-card mechanism.
> Value: Five sentence features meet on this demonstration row.
> Display: The family map in the Diagram above shows the same five branches.

#### Read the controls
(Each gesture answers one concrete question about the sentence.)
Click the sentence to reveal its three attached evidence records.
Hover or keyboard-focus it to reveal its generated address, `＋` Comment action, and `💬` Chat action.
Double-click it to edit the source sentence and create one adjacent whole-sentence change record.
On touch, open `⋯` to reach the same Comment, Chat, and Edit actions.
The future `QAb4` Sentence details view will filter attached records into Comments, Evidence, and Changes; that lifecycle is designed but not implemented yet.

### §2 Why adjacency, and not new syntax
The paper unit docs already write review threads and `> CHECK:` blocks under the sentence they discuss, so existing files gain the behavior with zero edits once their board rebuilds.
A `>` line directly under a sentence attaches to it by adjacency and by nothing else: no marker, no id, no sidecar file.
That is the property the whole family rests on, and `QAb3` measured it: every attachment is one line an author could have typed.

### §3 The family, one face each
The card (`QAb1`) renders the sentence clean and its apparatus on click.
The comment (`QA6`) writes a remark immediately under its selected sentence.
Editing (`QAb2`) replaces one plain sentence and writes one adjacent whole-sentence diff record.
Visibility (`QAb3`) rules what an agent acting on the sentence is handed.
Lifecycle (`QAb4`) rules how Sentence details are filtered, resolved, cleaned up, archived, restored, and purged.

## Items to Finish
- [x] 🧪 Put a live sentence-family demonstration first
      One row demonstrates evidence, generated controls, Comment, Chat, Edit, and the boundary around the future Sentence details lifecycle.
- [ ] 🧠 JL confirms the family map
      Opened 260729 when the QAb group was carved; the unit itself was settled in 0.19.0.

## Where we are
The unit is settled and live on every board; QAb0 now opens with one self-demonstrating sentence before it explains the family assembled from the former QA8 family plus QA6.

## Files
- `src/body.py`
  One sentence per source line, and the adjacency walk.
- `QAb1-evidence-card.md` · `QAb2-editing.md` · `QAb3-agent-visibility.md` · `QAb4-sentence-details-lifecycle.md` · `QA6-comments.md`
  The family.

## Log
260729 · Added §1 Demonstration so one sentence exposes Evidence, Comment, Chat, Edit, address, and the QAb4 lifecycle boundary before the reader enters the detailed family map
260729 · Added QAb4 as the independent Sentence details lifecycle face for filters, statuses, cleanup, archive, restore, and purge
260729 · Opened as the sentence family's front door when QAb was carved (JL: QAb0 overview, QAb1 evidence card, QAb2 editing)
