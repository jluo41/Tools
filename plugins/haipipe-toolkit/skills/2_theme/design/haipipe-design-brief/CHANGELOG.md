# haipipe-design-brief · version history

- 261007 · review fixes (version unchanged): Domain examples replaced by placeholders (no partition name); the agent card says older boards only; method-folders.md path fixed.

## 0.4.0 current · 2026-10-07 · Legacy: older boards only (JL 261007) (version unchanged)

- On the design ladder the Block's goal list (`haipipe-design-goal`, `board.md ## Goals`) replaced the
  Brief's list of designs; this skill now serves only an older board until it is carried over. Not
  deleted: the older board's page and its run cards still name it.

## 0.4.0 · 2026-10-05 · Rows are tasks on a method-folder board (JL 261005) (version unchanged)

- On a board with `2-Design-M<NN>-<slug>/` method folders a row is a task and its folder cell
  names the task's `Design-NN-…` folder, the same under every method; the `method` column is
  read only on boards with just `2-Design/` (`haipipe-design/ref/method-folders.md`).

## 0.4.0 · 2026-09-28 · No content hashes (JL 260928) (version unchanged at 0.4.0; the Design family version is frozen)

- A signed Wisdom handoff is named by path, Page version, signature and GI6
  receipt; no content hash.

## 0.4.0 · 2026-09-20 (version unchanged at 0.4.0)

- List all eight supplied venue guides so the four earlier examples cannot be
  mistaken for a restricted venue enum. Fresh-context portfolio validation
  confirmed all eight parse into distinct Brief tasks without allocating Runs.

## 0.4.0 · 2026-09-18 (version unchanged at 0.4.0)

- The design-task table grammar now lives here: the list sits under the
  `What to design` heading and is the only Brief table whose header holds
  `audience`, `job` and `venue` together; columns `line`, `audience`, `job`,
  `venue`, `designs`, `insight`, `folder` by header word; a Brief with no
  `line` column numbers its rows R1, R2 …; a line id is a key in the file,
  never a name on screen; the audience is written in plain words.
- The Board-level Design workbench is named as the second writer: it adds lines
  (`add-tasks`) and writes a line's `folder` cell (`new-folder`), nothing
  else.
- The eighth division is `What to design` (was "What to design and handoff").
- Handoff says what the code does: a Commission pins its item's config and
  evidence files, not the Brief version, `reads:`, or venue packs.
- One version-governance paragraph instead of two.

## 0.4.0 · 2026-09-13 (user ruling) and 2026-08-24

- 2026-09-13: Keep the current Brief pre-1.0. Later-looking labels below are
  retracted as release assignments and retained only as development
  provenance.
- 2026-09-13: Any future `1.0.0+` requires explicit user approval.
- 2026-08-24, the earlier use of the same label: `born-of:` required — a
  Brief is born mandate-first (a person names the program, needs raised
  open) or evidence-first (signed W handoffs propose it; opportunity/
  audience/outcome/kill drafted from the handoff fields, settled needs born
  answered).

## 2.0.0 — 2026-09-13

- Move Brief out of `workflow-phases/` and make it a canonical Folder owner.
- Remove D0/GD0, `page-type: brief`, PageX, and D1 compatibility routes.
- Release the Brief through its Page workflow; current Commissions pin it.

## 1.1.0 — 2026-09-13

- Replace active PageX inputs with exact frozen signed-W inputs and carry each
  unmet need's derived `partition × DIKW target` Question Group.

## 1.0.1 — 2026-08-31

- Name the outgoing authority `GD0-closed Brief`; D0 has no undefined
  `accepted Brief` token and declares no Page-local owner ruling.

## 1.0.0 — 2026-08-31

- Migrated from `haipipe-page-for-brief` to Design workflow phase D0.
- The Brief skill now owns both faces, workbench profile, GD0, and its Card handoff.

## 0.3.0 — 2026-08-20

- Now heads the DesignBoard rather than the whole Application.
- Divisions 6-7 lost the data inventory to `haipipe-page-for-meta`. Division 6 is
  now `Insight Needs Raised`: the Brief raises a need and the Meta Page's Insight
  Roster records which Insight Page took it, so each row has one writer.
- Division 8 became `Design Roster and Handoff`; it no longer releases the Insight
  roster.
- Moved the runtime home to `<DesignTopic>-DesignBoard/0-A-brief/`.

## 0.2.0 — 2026-08-20

- Recast Brief as the single Application identity and intent Page.
- Added an Insight Need Map and Design roster without embedding evidence work.
- Established PageX-only consumption and explicit audience/outcome/venue scope.
