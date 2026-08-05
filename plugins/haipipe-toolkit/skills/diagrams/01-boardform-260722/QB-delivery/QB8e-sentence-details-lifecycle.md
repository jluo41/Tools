# Sentence · the details lifecycle
state: 🟡 PARTIAL · independent Q opened; lifecycle rules and implementation remain
owner: JL
method: give the sentence panel typed views, explicit record states, and a previewed archive-first cleanup path
session: 12fb5622-ff63-4e49-b5a3-9efbcb113613
## Opening
How should sentence details stay useful as comments, evidence, and changes accumulate over time?

This page defines typed views, record states, retention, and recoverable cleanup for everything attached to one sentence.
The hard part is that comments, evidence, and edits do not share one lifecycle, so old does not mean resolved and current evidence is not disposable history.
Without explicit distinctions, the panel either grows forever or deletes context that still matters.
The lifecycle succeeds when active records stay protected, every cleanup is previewed, archives can be restored, and purge remains separate.

**Covered elsewhere**: `QB8` owns the sentence and everything written onto it: what may attach and how adjacency renders it, writing a remark, and editing with its change record. `QD8` owns C/H/P/S addresses and Sentence Focus in Chat.


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
Archive and restore therefore cannot use `QB8e.C1.P1.S1` as durable identity.
The remaining identity decision is whether an attached sentence receives a hidden stable key or whether archive is intentionally page-level and cannot restore to a sentence after its wording changes.

## Aims
### The panel's name and three families
- [x] 🧭 Open one independent lifecycle Q
      `QB8e` owns filtering, record state, cleanup, archive, restore, and purge.
- [x] 🏷 Name the surface
      The user-facing name is Sentence details; apparatus is the technical record layer.
- [x] 🧱 Separate the three lifecycle families
      Comments, Evidence, and Changes have distinct membership and cannot share one retention rule.

### Rulings awaiting JL
- [ ] 🧠 JL accepts the default Overview and sticky filter behavior
      Overview shows counts plus at most one representative row from each family.
- [ ] 🔑 Decide durable sentence identity
      Choose a hidden stable sentence key or accept page-level archive with limited restoration.

### The states, filters, and cleanup machinery
- [ ] ✅ Define and render explicit record states
      Comments need open and resolved; Evidence needs current, superseded, rejected, and broken.
- [ ] 🎛 Implement filters, counts, and bounded panel height
      The reader can isolate one family without expanding every record beneath the sentence.
- [ ] 🧹 Implement previewed archive-first cleanup
      Keep active records, retain the configured recent history, preview every move, and support restore.
- [ ] 🧪 Pass fresh-context lifecycle acceptance
      A new agent must discover the rules, preserve active records, archive only eligible records, and stop before purge.

## States
`QB8e` now exists as the independent Sentence details lifecycle decision.
The name, three record families, and archive-first safety boundary are recorded, but no filter, state marker, archive store, restore path, stable key, or purge action has been implemented.

### Decision Now
- [ ] 🧠 JL accepts the default Overview and sticky filter behavior
      Overview shows counts plus at most one representative row from each family; a tick here also closes the same row in Items to Finish.
- [ ] 🔑 Decide durable sentence identity
      The options this page records: a hidden stable sentence key, or page-level archive that cannot restore to a sentence after its wording changes; a tick here also closes the same row in Items to Finish.

## Files
### What renders Sentence details today
- `haipipe-board/src/body.py`
  Current apparatus classification and Sentence details rendering.

### The future lifecycle write and view paths
- `haipipe-board/assets/js/40-sentence/00-apparatus.js`
  Future filter state, cleanup preview, archive and restore interactions.
- `haipipe-board/assets/css/`
  Future Overview tabs, bounded details panel, state and archived-count styling.
- `haipipe-board/cli/serve.py`
  Future resolve, supersede, archive, restore, and purge write paths.

## Glossary
Sentence details: the user-facing panel opened for one sentence.
apparatus: the technical set of comments, evidence, and change records attached beneath a sentence.
archive: recoverable Board-internal storage removed from the live sentence view.
purge: explicit permanent deletion of records that are already archived.

## Log
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260729 · Opened by JL as an independent Q for the sentence panel's filters, statuses, cleanup, archive, restore, and retention lifecycle.
