# Sentence details lifecycle
state: 🟡 PARTIAL · independent Q opened; lifecycle rules and implementation remain
owner: JL
method: give the sentence panel typed views, explicit record states, and a previewed archive-first cleanup path

## Question
How should the information attached to one sentence be viewed, resolved, cleaned up, archived, and restored without letting the page grow forever?
Clicking a sentence can reveal comments, evidence, and editing history, but those records do not share one lifecycle.
The panel needs a human name, compact filters, explicit states, and cleanup rules that never mistake old for resolved or active evidence for disposable history.

## Boundary
- ✅ Covered here
  The Sentence details panel, its Overview and typed filters, record states, retention limits, archive, restore, and permanent deletion.
- ↪ Covered elsewhere
  `QAb1` owns what apparatus can attach and how adjacency renders it.
  `QA6` owns writing a sentence-local comment, `QAb2` owns editing and change records, and `QAb3` owns C/H/P/S addresses plus Sentence Focus in Chat.

## Diagram

```
sentence                                         ⚑ 12
  │ click
  ▼
Sentence details
  Overview · Comments 3 · Evidence 4 · Changes 5
       │            │            │
       │ resolve    │ supersede  │ keep recent 5
       └────────────┴────────────┘
                    │ Clean up + Preview
                    ▼
       live records │ archived records │ explicit purge
```

## Content
### §1 The surface
#### User-facing name
The thing opened beneath a sentence is called Sentence details.
Panel or drawer describes the UI mechanism, while apparatus remains the technical name for the attached records.
The Board vocabulary `queue` keeps its existing group meaning, so this lifecycle is an independent Q rather than a second kind of queue.

#### Compact default
The closed sentence shows only its total badge.
Opening Sentence details starts on Overview, which shows counts and at most the latest representative record from Comments, Evidence, and Changes.
Selecting one type shows only that type, and the selected type remains sticky while the reader moves between sentences.
The panel has a maximum height and scrolls internally rather than lengthening the whole page without limit.

### §2 Three record families
#### Comments
Comments contains human discussion and requests: `JL`, `CC`, `Note`, `Check`, and `Q-consumer`.
Open comments are never removed by cleanup.
A comment must be explicitly marked resolved before it becomes eligible for retention or archive rules.

#### Evidence
Evidence contains material that supports or locates the sentence: `Citation`, `Source`, `Value`, `Display`, and `Link`.
Current evidence has no count limit.
Only evidence explicitly marked superseded, rejected, or broken becomes eligible for archive.

#### Changes
Changes contains `✎` editing history and legacy revision Notes that carry deletion and insertion markers.
The live sentence keeps the five most recent change records by default.
Older change records move to archive; their original actor and time stay intact.

### §3 Cleanup lifecycle
#### Archive first
Cleanup never performs permanent deletion.
It always preserves unresolved comments and current evidence, keeps the configured recent records, previews every proposed move, and archives only after confirmation.
The live panel reports older archived counts and can open or restore them.

#### Permanent deletion is separate
Purge acts only on already archived records and requires its own explicit preview and confirmation.
Automatic age alone never proves that a comment is resolved or evidence is obsolete.
The initial retention proposal keeps all open comments, all current evidence, the five newest resolved comments, and the five newest changes.

### §4 Identity
#### Render address versus durable key
A C/H/P/S address says where the record appears in the current render and may change when Content is reorganized.
Archive and restore therefore cannot use `QAb4.C1.P1.S1` as durable identity.
The remaining identity decision is whether an attached sentence receives a hidden stable key or whether archive is intentionally page-level and cannot restore to a sentence after its wording changes.

## Items to Finish
- [x] 🧭 Open one independent lifecycle Q
      `QAb4` owns filtering, record state, cleanup, archive, restore, and purge.
- [x] 🏷 Name the surface
      The user-facing name is Sentence details; apparatus is the technical record layer.
- [x] 🧱 Separate the three lifecycle families
      Comments, Evidence, and Changes have distinct membership and cannot share one retention rule.
- [ ] 🧠 JL accepts the default Overview and sticky filter behavior
      Overview shows counts plus at most one representative row from each family.
- [ ] ✅ Define and render explicit record states
      Comments need open and resolved; Evidence needs current, superseded, rejected, and broken.
- [ ] 🎛 Implement filters, counts, and bounded panel height
      The reader can isolate one family without expanding every record beneath the sentence.
- [ ] 🧹 Implement previewed archive-first cleanup
      Keep active records, retain the configured recent history, preview every move, and support restore.
- [ ] 🔑 Decide durable sentence identity
      Choose a hidden stable sentence key or accept page-level archive with limited restoration.
- [ ] 🧪 Pass fresh-context lifecycle acceptance
      A new agent must discover the rules, preserve active records, archive only eligible records, and stop before purge.

## Where we are
`QAb4` now exists as the independent Sentence details lifecycle decision.
The name, three record families, and archive-first safety boundary are recorded, but no filter, state marker, archive store, restore path, stable key, or purge action has been implemented.

## Files
- `haipipe-board/assets/board.js`
  Future filter state, cleanup preview, archive and restore interactions.
- `haipipe-board/assets/board.css`
  Future Overview tabs, bounded details panel, state and archived-count styling.
- `haipipe-board/src/body.py`
  Current apparatus classification and Sentence details rendering.
- `haipipe-board/serve.py`
  Future resolve, supersede, archive, restore, and purge write paths.

## Glossary
Sentence details: the user-facing panel opened for one sentence.
apparatus: the technical set of comments, evidence, and change records attached beneath a sentence.
archive: recoverable Board-internal storage removed from the live sentence view.
purge: explicit permanent deletion of records that are already archived.

## Log
260729 · Opened by JL as an independent Q for the sentence panel's filters, statuses, cleanup, archive, restore, and retention lifecycle.
