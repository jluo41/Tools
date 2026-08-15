# Sentence · the details lifecycle
state: 🟡 PARTIAL · rules recorded through the 260805 RUN; two Decision Now rulings and all implementation remain
owner: JL
method: give the sentence panel typed views, explicit record states, and a previewed archive-first cleanup path
session: 12fb5622-ff63-4e49-b5a3-9efbcb113613
## Opening
How should sentence details stay useful as comments, evidence, and changes accumulate over time?
Sentence details is the panel opened beneath one sentence to hold its attached records.
Old does not mean resolved here: a comment can stay open for months, and current evidence is not disposable history.
A panel with no lifecycle rules grows forever or deletes context that still matters.
This page decides typed views, record states, and a previewed archive-first cleanup with restore and a separate purge.

**Covered elsewhere**: `QB8` owns the sentence and everything written onto it: what may attach, how adjacency renders it, writing a remark, and editing with its change record.
`QD8` owns C/H/P/S addresses and Sentence Focus in Chat.

**What success looks like**: Active records stay protected, every cleanup is previewed, archives can be restored, and purge stays a separate explicit act.


## Diagram

**One sentence's records, end to end**: the click path from the closed badge to live, archived, and purged records.

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
**The surface at three depths**: what the reader sees closed, on Overview, and filtered to one family.

```
😴 CLOSED     sentence · ⚑ 12         one total badge only
     │ 🖱 click
     ▼
🪟 OVERVIEW   Comments 3 · Evidence 4 · Changes 5
              ➕ at most 1 latest record per family
     │ 🖱 pick one family
     ▼
🎛 FILTERED   one family only · 📌 sticky across sentences
              📏 max height · internal scroll
```
📌 This part fixes the surface: its name, its compact default, and the filter behavior that keeps it compact.

#### 1.1 · User-facing name
The thing opened beneath a sentence is called Sentence details.
Panel or drawer describes the UI mechanism, while apparatus remains the technical name for the attached records.
The Board vocabulary `queue` keeps its existing group meaning, so this lifecycle is an independent Q rather than a second kind of queue.

#### 1.2 · Compact default
The closed sentence shows only its total badge.
Opening Sentence details starts on Overview, which shows counts and at most the latest representative record from Comments, Evidence, and Changes.
Selecting one type shows only that type, and the selected type remains sticky while the reader moves between sentences.
The panel has a maximum height and scrolls internally rather than lengthening the whole page without limit.

### §2 Three record families
**Three families, three lifecycles**: who lives in each family and which records cleanup may ever touch.

```
💬 COMMENTS  JL · CC · Note · Check · Q-consumer
             🔓 open        🛡 never removed
             ✅ resolved    📦 archive-eligible
🧾 EVIDENCE  Citation · Source · Value · Display · Link
             🟢 current     🛡 no count limit
             🚫 superseded · rejected · broken    📦 eligible
✎ CHANGES    edit history + legacy revision Notes
             🕐 newest 5    🛡 stay live
             📜 older       📦 archive · actor + time intact
```
📌 This part separates the three families, because open, current, and recent mean different things in each.

#### 2.1 · Comments
Comments contains human discussion and requests: `JL`, `CC`, `Note`, `Check`, and `Q-consumer`.
Open comments are never removed by cleanup.
A comment must be explicitly marked resolved before it becomes eligible for retention or archive rules.

#### 2.2 · Evidence
Evidence contains material that supports or locates the sentence: `Citation`, `Source`, `Value`, `Display`, and `Link`.
Current evidence has no count limit.
Only evidence explicitly marked superseded, rejected, or broken becomes eligible for archive.

#### 2.3 · Changes
Changes contains `✎` editing history and legacy revision Notes that carry deletion and insertion markers.
The live sentence keeps the five most recent change records by default.
Older change records move to archive; their original actor and time stay intact.

### §3 Cleanup lifecycle
**Archive first, purge apart**: the only two moves a record can make out of the live panel.

```
🧹 CLEAN UP ──▶ 👁 PREVIEW ──▶ ✅ CONFIRM ──▶ 📦 ARCHIVE
   🛡 always kept   🔓 open comments · 🟢 current evidence
   🕐 also kept     the configured recent records
📦 ARCHIVE ──▶ ↩️ RESTORE    back into the live panel
📦 ARCHIVE ──▶ 🔥 PURGE      its own preview · its own confirm
🚫 never     silent delete · age as proof of resolved
```
📌 This part makes removal a two-step act: cleanup archives after a confirmed preview, and purge is a separate later act on the archive alone.

#### 3.1 · Archive first
Cleanup never performs permanent deletion.
It always preserves unresolved comments and current evidence, keeps the configured recent records, previews every proposed move, and archives only after confirmation.
The live panel reports older archived counts and can open or restore them.

#### 3.2 · Permanent deletion is separate
Purge acts only on already archived records and requires its own explicit preview and confirmation.
Automatic age alone never proves that a comment is resolved or evidence is obsolete.
The initial retention proposal keeps all open comments, all current evidence, the five newest resolved comments, and the five newest changes.

### §4 Identity
**Render address against durable key**: why `QB8e.C1.P1.S1` cannot anchor archive and restore.

```
🏷 C/H/P/S address   where the record sits in TODAY's render
        ↯ Content reorganized ──▶ the address moves
🔑 durable key       the open choice, JL's to make
   A · 🕶 hidden stable key on every attached sentence
   B · 📄 page-level archive · no per-sentence restore
```
📌 This part holds the one open identity decision that archive and restore depend on.

#### 4.1 · Render address versus durable key
A C/H/P/S address says where the record appears in the current render and may change when Content is reorganized.
Archive and restore therefore cannot use `QB8e.C1.P1.S1` as durable identity.
The remaining identity decision is whether an attached sentence receives a hidden stable key or whether archive is intentionally page-level and cannot restore to a sentence after its wording changes.

## Aims
### A1 · 🪟 The surface
- A1.1 · The surface is named: Sentence details for the reader, apparatus for the technical record layer.
  **Done when:** The page and the rendered panel use Sentence details as the user-facing name and apparatus only for the attached records.
- A1.2 · JL accepts the default Overview and sticky filter behavior.
  **Done when:** JL has answered the matching Decision Now row on Overview counts, the one representative record per family, and the sticky selected type.
- A1.3 · Filters, counts, and bounded panel height are implemented.
  **Done when:** The reader can isolate one family without expanding every record beneath the sentence, and the panel scrolls internally at its maximum height.

### A2 · 🧱 Three record families
- A2.1 · The three lifecycle families stay separate.
  **Done when:** §2 records distinct membership for Comments, Evidence, and Changes, and no retention rule treats the three families as one.
- A2.2 · Explicit record states are defined and rendered.
  **Done when:** Comments render open and resolved; Evidence renders current, superseded, rejected, and broken.

### A3 · 🧹 Cleanup lifecycle
- A3.1 · Previewed archive-first cleanup is implemented.
  **Done when:** Cleanup keeps active records, retains the configured recent history, previews every move, and supports restore.

### A4 · 🔑 Identity
- A4.1 · Durable sentence identity is decided.
  **Done when:** JL has chosen a hidden stable sentence key or page-level archive with limited restoration, and the ruling is recorded on this page.

### P · 🏁 Page-level
- P1 · QB8e stands as the one independent lifecycle Q.
  **Done when:** `QB8e` owns filtering, record state, cleanup, archive, restore, and purge, and no other page claims that lifecycle.
- P2 · Fresh-context lifecycle acceptance passes.
  **Done when:** A new agent discovers the rules, preserves active records, archives only eligible records, and stops before purge.

## States
### Decision Now
- [ ] 🧠 JL accepts the default Overview and sticky filter behavior
      Overview shows counts plus at most one representative record from each family, and the selected type stays sticky while the reader moves between sentences.
      A · accept the default, which commits the panel to opening on Overview and keeping the reader's chosen family selected across sentences.
      B · reject it, which sends §1's compact default back for a different opening view before any filter code is written.
      → CC recommends A, because a count-first Overview keeps a closed sentence compact while one click still reaches any family.
- [ ] 🔑 Decide durable sentence identity
      A C/H/P/S address moves when Content is reorganized, so archive and restore cannot use it as a durable key.
      A · give every attached sentence a hidden stable key, which commits the Board to writing that key and carrying it through every edit, archive, and restore.
      B · keep archive page-level, which commits the reader to losing per-sentence restore after a sentence's wording changes.
      → CC recommends A, because restore that finds its sentence again is what makes the archive recoverable rather than a dump.

### A1 · 🪟 The surface
- 🔨 A1.1 · Partly met; §1 and the Glossary record Sentence details as the user-facing name and apparatus as the technical record layer, but the rendered panel in `haipipe-board/src/body.py` does not yet carry the Sentence details name, so the render half of Done when still waits on implementation.
- 🧠 A1.2 · Waiting on JL; the Overview and sticky filter default is the first Decision Now row above.
- ⬜ A1.3 · Not started; no filter, count, or bounded-height code exists.

### A2 · 🧱 Three record families
- ✅ A2.1 · Met: §2 records distinct membership and a separate retention rule for Comments, Evidence, and Changes.
- ⬜ A2.2 · Not started; no record state is rendered anywhere.

### A3 · 🧹 Cleanup lifecycle
- ⬜ A3.1 · Not started; §3 records the archive-first rule, but no preview, archive store, restore, or purge path exists.

### A4 · 🔑 Identity
- 🧠 A4.1 · Waiting on JL; the identity choice is the second Decision Now row above.

### P · 🏁 Page-level
- ✅ P1 · Met: this page exists as the independent lifecycle Q and owns filtering, record state, cleanup, archive, restore, and purge.
- ⬜ P2 · Not started; acceptance can only run after A1.3, A2.2, and A3.1 land.

`QB8e` now exists as the independent Sentence details lifecycle decision.
The name, three record families, and archive-first safety boundary are recorded, but no filter, state marker, archive store, restore path, stable key, or purge action has been implemented.

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
- 🪟 **Sentence details**: the user-facing panel opened for one sentence.
- ⚙️ **apparatus**: the technical set of comments, evidence, and change records attached beneath a sentence.
- 📦 **archive**: recoverable Board-internal storage removed from the live sentence view.
- 🔥 **purge**: explicit permanent deletion of records that are already archived.

## Log
- 260806 2105 · [REVISE-CC] swept to the 260806 architecture; state line refreshed from the stale 260729 opening claim to reflect that the 260805 RUN recorded the rules and only two Decision Now rulings plus implementation remain
260805 · REVISE r1s4 (run 260805-0216-QB8e): the eight Content paragraph headings numbered 1.1 through 4.1 in the division.n form, and the A1.1 State row corrected from ✅ Met to 🔨 partly met because the rendered panel does not yet carry the Sentence details name.
260805 · REVISE r1s2 (run 260805-0216-QB8e): face figures with captions added to §1-§4 and the Diagram, the Opening restaged as question plus rationale with labelled drawer parts, Aims converted to A/P ids with Done when, States mirrored per Aim, Decision Now options split one per line, and Glossary rows bulleted.
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260729 · Opened by JL as an independent Q for the sentence panel's filters, statuses, cleanup, archive, restore, and retention lifecycle.
