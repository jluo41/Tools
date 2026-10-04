## 1.6.0 · 2026-10-03 · A Report per Story question, in reports/

- `ref/paper-structure.md`: the paper root gains `reports/qNN_<topic>/qNN_<topic>.md`, one Report Page per Story question, a board-level folder beside `studio/` and not a Page group (JL 261003: "should we have the reports folder in the paper board as well"; "just like the studio and reports, like other board level folder"). Same shape as a Task Block's reports (`answers: RQ<n>`, `answer-status: open | partial | answered`, Opening = the answer).
- A Report is the G2 record: Story › High-level logic + Low-level work gains a Report column (haipipe-workbench-paper 0.23.0), and a hypothesis shows ✅ only when its question's Report says answered, else 📝.
- First Report: Paper-MessageTradeOffEgm `reports/q01_each_message_average/` (partial: E01 reproduced exactly; 1b's clustered variance not yet checked).

## 1.5.1 · 2026-10-02 · Related Papers says why we keep a paper

- "What the person sees": the Related Papers card now shows why the paper is kept (P-board `keep`, `bears on`; haipipe-paper-story 0.18.0) and the paper's logic beside its work (`logic-work.yaml`; haipipe-discovery 0.21.0, haipipe-workbench-paper 0.21.0).

## 1.5.0 · 2026-09-30 · The door names what the Workbench shows

- New table "What the person sees": each Paper Workbench tab (Ideation; Story › Spine, RoadMap Draw, High-level logic + Low-level work, Related Papers; Sections; Delivery › LaTeX, Word, Cover letter, Rounds) and the skill that owns it, so a person naming a tab reaches its owner (JL 260930, "go ahead and update them accordingly", on aligning the paper skills with the Workbench).
- Story parts are §N or their name, never C1-C8 (haipipe-paper-story 0.17.0), here and in `ref/page-integration.md`, `ref/paper-structure.md`, `ref/section-sessions.md` and `ref/run-naming.md`; the Task review Spec is `paper.judgment.task`; "canonical" and "obligation" are gone (AGENTS rule 9).
- `ref/paper-structure.md` and the family README show `studio/`, the folder Story › RoadMap Draw reads.

## 1.4.4 · 2026-09-29 · outline/ to draft/ in current-layout prose (JL 260929)

- Paths that describe the current Page layout say `draft/`: the plan `draft/<stem>-draft-v<G>.<S>[.<E>].md`, records `draft/records/`, `draft/previous/`, `draft/skill/`, the Evidence Markdown `draft/<stem>-evidence-items.md`, `draft/evidence/bibex/` and `draft/evidence/materials/` (JL 260929: "it should be draft"). Mentions of legacy Pages, retired `outline/evidence/` lanes and the migration keep `outline/`, as do the OUTLINE stage, the Outline table and the `outline:` grammar key.
- `scripts/audit_page_compatibility.py`: a Page-root `evidence/` is told its records belong under `draft/evidence/`.

## 1.4.3 · 2026-09-29 · Per-page Appendix pairs

- `scripts/create_section_sessions.py`: an Appendix that keeps one older Codex thread per page now gets one call-peer pair per page, `<Short>-Appendix-<letter>`, with the new Appendix Claude session, as `ref/section-sessions.md` already said; before, it got no pair at all. `codex_name()` reads the thread's name from the Codex session index for the pair. Found on Paper-CGMtoHbA1c (three pairs registered by hand); checked on a stubbed two-appendix paper.

## 1.4.2 · 2026-09-28 · Keep existing Codex threads (JL 260928)

- `ref/page-integration.md`, `ref/run-naming.md`: a Page Delivery Run is one fixed Run per lane (`run_delivery_<lane>`), not `rdNN_<target>`; `RD<NN>` stays the Round Page id (JL 260928).
- `scripts/create_section_sessions.py`: an Appendix unit whose pages each name their own live `codex-session:` counts as having Codex (`one per page`); the plan no longer creates one new thread and writes it over all pages, nor binds the whole unit to the first page's pair. `ref/section-sessions.md`: look for a paper's existing Codex threads and bind them before creating. Found on Paper-TimeEventDM-ISR2026, whose 13 per-page Codex threads from 260917 were missed.

## 1.4.1 · 2026-09-28 · No content hashes (JL 260928)

- `ref/page-integration.md`, `ref/run-naming.md`: the Ideation sync and Page projection receipts carry the revision number only, and a reused Result is named by path and version; no `source_hash`, output hash or hash pin. `scripts/audit_page_compatibility.py` no longer accepts `sha256:` as a Story binding: `story-row:` needs `+ <Story version>`.

## 1.4.0 · 2026-09-28

- Add `/haipipe-paper sessions` (JL 260928): once the Story's §8 compile order fixes the
  Sections, `scripts/create_section_sessions.py` gives each unit (a Main Section Page, and the
  whole Appendix group as ONE unit by default, `--appendix each` to split) a named Claude session
  `<Short>-<unit>` and a named Codex thread `<Short>-<unit>-Codex`, pairs them (identity-only
  call-peer), writes `session:` and `codex-session:` into each page header, gives both a read-only
  first turn with five scope rules, and stops the Claude session after that turn so `/resume` can
  open it. Codex threads are made through `codex app-server` (`thread/start`, `thread/name/set`,
  `turn/start`) so the Codex app lists them by name; `codex exec` threads are unlisted and unnamed.
  An existing Claude↔Codex pair is bound, not duplicated. Plan-only by default; `--apply` creates.
  A Claude session is the unit's own only when its saved name is `<Short>-<unit>`, so a
  `session:` copied in from a predecessor paper is replaced, not reused (found by a fresh-agent
  plan-only run on the JAMA paper). The prefix is recorded in `board.md` as `session-prefix:` on
  the first `--apply` and read from there afterwards. Contract: `ref/section-sessions.md`.
- A Section Run has two bookends the author calls (JL 260928): only the Section's Draft file
  changes in between; records and one log entry are written at the close; Content adoption and
  the web → LaTeX → Word lanes follow on request; assembly sees a mid-Run Section's previous
  export. Contract lives in `haipipe-page-workflow` 0.65.0 (`interactive-writing-run.md` §🔖).

## 1.3.0 · 2026-09-21

- Add the sourced 21-point submission-readiness overlay to the G4 gate, with
  section-owned and whole-paper criterion rows that reuse the shared rubric.

## 1.2.0 · 2026-09-20

- Route Paper/Page requests through the current owner contracts and shared Ideation specialists. Publish the Run Spec inventory, conditional skill map and legacy path compatibility.

## 1.1.0 · 2026-09-13

- Add the Paper–Page integration boundary for Page 0.89: Paper owns the
  journey and composition while the shared Page owns the Page Face, lifecycle,
  Page Runs, Evidence Workspace, release, and CHECK.
- Replace the current Page-local writing identity with the Page-owned
  `rp00_mermaid-structure` / `rpNN_pNN[-pNN]` rule; delegated work remains in
  the owner-native Task lane and historical identities remain read-only.
- Add the Page integration reference for Page-global paragraph addresses,
  Page release, G3/G4 admission, and source/projection boundaries.

## 1.0.3 · 2026-09-08

- Follow Page's paragraph-writing Ticket interface for Content; Paper Evidence/Display pm/pa/pr naming is unchanged.

# CHANGELOG · haipipe-paper

## 1.0.2 · 2026-09-08

- Add the Paper Run naming authority: new Paper-local Evidence/Display Runs
  use semantic `pm-`/`pa-`/`pr-` ids tied to Main/Appendix/Round Page names;
  Page-local Division Writing keeps `rNN_page-division-writing_cNN`.
- Mark `pjNNtNNrNN` Paper Run files as read-only historical dialect; no
  ordinary Paper work renames or bulk-migrates them.

## 0.8.1 · 260907

- P1 is Story: phase figure, one-liner, routing row, `/haipipe-paper story`
  verb (`seed` alias kept), completion check. Routes to `haipipe-paper-story`.

## 0.8.0 · 260907

- Paper folder scaffold rewritten (JL 260907): page groups and `board.md` at
  the paper root (`paper-root: .`), no `0-paperboard/`; `A1-Story` holds the
  pool plus one `Story<NN>-<idea-slug>/` per idea with its roadmap and
  narrative children nested inside; `delivery/` (factory: paper-build.toml,
  latex/, word/) replaces the hand-edited desk room. The room law of 260824 is
  replaced by the delivery law: pages own the words, `delivery/` is regenerated
  whole from their `<page>.tex` fragments and never hand-edited.
- Round folders hold `sent/` · `feedback/` · `released/`.
- Phase figure, Seed/Roadmap/Narrative one-liners, routing row, assembly
  figure and completion checks follow. `Paper-AgreeablePrescription` is the
  first repo on this layout; every earlier layout is grandfathered.

## 0.7.1 · 260904

- Keep the shared Outline presenter at the Page surface and load only its exact
  material refs inside concrete Paper Page phases.

## 0.7.0 · 260904

- Separate family-entry routing from the concrete Page RUN order.
- Replace the active Probe/PageX/workbench-lane model with one shared Outline
  workbench and typed VALUE/CITE/DISPLAY local Results over Supporting/local Runs.
- Add CONTEXT to the Paper Page loop and update status/folder/desk-room
  language to current evidence identities.

## 0.6.0 · 260901
- Active Section Page IDs are full semantic names: `S-<desk>-Main-<section-name>` and `S-<desk>-Appendix-<section-name>`. Reading order belongs in the Board Map, not in an opaque ordinal. Legacy `S<D><NN>` and `SA<NN>` identifiers are archive-only compatibility forms.

## 0.5.0 · 260831
- One letter per B group (JL 260831 "Ba to be Main, Bb to be Appendix, Bc to be Round"): first desk Ba-<desk>-Main · Bb-<desk>-Appendix · Bc-<desk>-Round, a second desk continues at Bd; shared-letter (0.4.x) and combined-group layouts grandfathered. Live: Ba-MISQ-Main/Bb-MISQ-Appendix/Bc-MISQ-Round, Ba-JAMA-IM-Main/Bb-JAMA-IM-Appendix.

## 0.4.1 · 260831
- Desk name keeps its capitals in group folders (JL: "make MISQ capitalized"): Ba-MISQ-Main/-Appendix/-Round; only the arrival letter is lowercase. MISQ board also capitalized the desk in Story03-narrative-MISQ and RD01-MISQ-feedback-20260825; desk rooms (1-misq2026/) and venue bank ids (QBv1-misq) keep their own conventions.

## 0.4.0 · 260831
- Desk layer split three ways (JL 260831 "I want to make Ba-misq into three page groups"): B<x>-<desk>-Main (S<D> units) · B<x>-<desk>-Appendix (SA units) · B<x>-<desk>-Round (RD pages); page tokens unchanged; a combined B<x>-<desk> group is grandfathered.

## 0.3.0 · 260831
- Story ids replace SD/NA (JL 260831 "I don't like the SD... make sure to be self explained"): one A1-Story group holds P0-P3, the venue-free head (Story00-ideation, Story01-seed, Story02-roadmap) plus one Story<NN>-narrative-<desk> per desk (Story03 first); the A2-NA-narrative group and the SD/NA tokens are retired to the grandfathered list.

## 0.2.1 · 260831
- Group-name grammar caught up with the SA ruling (JL 260831): appendix token is `SA` (Section-Appendix), never `A<D>`; the collision rule now retires desk letter `A`; the grandfathered legacy list names `A<D>` instead of `SA`. haipipe-paper-workflow 0.6.1 and haipipe-page-for-section 0.5.5 already carried it; this door was the leftover.

## 0.2.0 — 2026-08-31

- **workflow-phases/ replaces page-types/** (JL 260831: "replace page-types to
  be workflow-phases"): the six journey-phase contracts are now
  `workflow-phases/haipipe-paper-{ideation,seed,roadmap,narrative,section,round}`,
  each carrying its P-number and gates in a `## 🧭 Journey phase` block while
  still owning its `page-type:` key. Venue is a library lane, not a phase, so
  `haipipe-paper-venue` moved to the family top level beside the `venue/`
  bank submodule. Routing table and family map updated; page keys unchanged,
  so no board page changes.

## 0.1.0 — 2026-08-28

- First versioned door (backfilled row): routing, journey figure, assembly
  contract pointer, G6 gate, folder scaffold.
