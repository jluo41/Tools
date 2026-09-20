# haipipe-design · version history

Recovered from the SKILL.md frontmatter summary on 260827, when the family retired the `summary:` field: version history lives here and is never loaded at invocation.

- 0.4.0 current, 260918 (version unchanged at 0.4.0, JL's rule): the docs say what the code does.
  - The register example judges design quality: goal "Send the salience
    wording unchanged, so the reader sees whose office wrote and what to
    review", expected "a first-time reader can say who sent it and what to do
    after one read", falsified "a cold reader cannot name the next step from
    the text alone". No arm, allocation, winner, or re-fielding.
  - `evidence` paths are relative to the Design Folder; the example uses a
    board name that follows the board-name law (`A00_SMSR2Full-InsightBoard`).
  - Adding an item checks the stance/mode bindings the records check enforces.
  - A Commission pins its config (goal sentence, stance, basis, mode, bet,
    compiled criteria, rule text) and the item's evidence files; it does not
    pin the Brief version or venue packs. Generate and Verify copy the released
    config, so a later register edit reaches only a new Commission. One
    Commission per item; a held one can be released later.
  - States gain `commission open`, `adoption open`, `verify invalid`, and
    `queued run out of date`; a draft that fails the records check goes back
    to Generate, a review that fails it goes back to Verify; the agent side
    never routes to HOLD. Runs are counted per Design Item.
  - Folder shape: the Page title is `<job> <venue> for <who>`; each part is
    marked always or when used; `outline/feedback/<run>.md`,
    `outline/<stem>-draft-request.md` and `results/<run>/content/` are listed;
    `outline/decisions/` is gone (decisions live in `results/`).
  - The Adopt preview is a copy of the exact draft, one per draft.
  - Screen rules stated: plain words only, no roster, handoff, Ticket,
    candidate, DU, or `R1` on screen; insight pages by label and title.
  - `rp00_mermaid-structure` became `rp-struct-01`; the legacy list names
    `2-DS-design/DS*`.
  - A retired record parks under the board's `_archive/` and leaves
    `board.md` `## Pages`: the checker judges no `_` folder, so the bytes
    stay for the Log to cite, the old link heals to the `Design-NN` folder
    that replaced it, and nothing is migrated, reinterpreted or deleted.

- 0.4.0 (260915, user ruling): version remains exactly 0.4.0. Replace Design phases
  with a directed four-Run graph (`commission → generate → verify → adopt`),
  and count human decision Runs when they have bounded Tickets, Results,
  receipts, and independent closure. The current clean-break architecture
  and field-test repair remain pre-1.0. The later-looking labels recorded
  below were never user-approved releases and are retracted as version
  assignments; their notes remain only as development provenance. Future
  `1.0.0+` requires explicit user approval. No compatibility path was added.
  260916: add the Design Item register (`outline/<stem>-design-items.md`,
  goal and rules only) and `item:` on every Design Run record; the Design
  Plugin reads the Folder in five Spaces, Goal · Design · Insight · Run ·
  Delivery, in plain words, presented by `haipipe-plugin-design`; the Brief
  table carries a `designs` count; ids are `ITEM<NN>`; register field
  `goal:`; folder shape is `2-Design/Design-<NN>-…`, never `DS`.
  260917: folder names say the goal (the first three content words of each
  Brief cell, filler dropped); a renamed folder keeps its `Design-NN` number.
  Earlier use of the same label (JL 260828, "在 boundary 内部是没有实验的"):
  the BOUNDARY section — this board's purpose is design, the experiment
  belongs to another team outside it; no control cell, allocation, power
  arithmetic or measured comparison lives on any page here, and the
  deliverable is well-designed CANDIDATES. The word law: arm is the
  experiment's word and nothing on this board is called one — designer (the
  writer machine, renamed from arm-agent the same day), candidate (written,
  unallocated), variant, unit. A candidate becomes an arm at allocation,
  which never happens here.

- 4.0.1 (260913): field-test repair. Unsupported Design bytes are never called
  read-only/readable/migration history; stop content inspection at a decisive
  unsupported marker and distinguish audit non-mutation from compatibility.

- 4.0.0 (260913): clean break. Design Run ids become independent `rdNN_*`
  identities beside Page `rpNN`; v1, `rNN_design_*`, D0-D5/GD0-GD6,
  `design/DU*/`, PageX, and old thread/plugin readers are rejected. Brief and
  Unit move out of `workflow-phases/`; obsolete Design phase skills are removed.

- 3.0.0 (260913): align native Design with Page 0.89 as one Folder with two
  orthogonal workflows. Page Runs explain; Design Runs generate/verify; human
  adoption supplies the Page domain gate. Add v2 `design_intent`, current
  `outline/evidence/`, candidate-vs-Page delivery boundaries, and keep v1/D0-D5
  read-only.

- 1.0.3 (260831): make the subject-first unprefixed DesignBoard canonical and
  distinguish D4 acceptance from the required D5/GD6 round seal.

- 1.0.2 (260831): align the door with the final seam repair: Page RULING
  reuses GD1/GD5, Unit acceptance lives only on the D4 row, and PageDown always
  reaches GD6 before a round stops.

- 1.0.1 (260831): Card → Unit → Verdict are explicit in-place identities of
  one DU Folder; PageDown owns a minimal round receipt. DS identity includes
  venue, render lives at `delivery/render/`, and the two Design gates are named
  as cross-phase transfers distinct from nested Page-local ticks.

- 1.0.0 (260831): D0-D5 now each own one Folder contract and both faces.
  Principle ceased to be a Page Type or phase; its rare promoted form is a
  subordinate D4 role reread at D5.

- 0.6.1 (260828, same-day sync riders): the workflow reference reads D0-D5 / GD0-GD6 with D5 PageDown; the Reads Law table's `DR card` / `DU unit` labels became `design card` / `design unit`, retiring the last DR word in the door.
- 0.6.0 (260828, page-type normalization): the door NAMES its three page types (brief, design, principle). Nine contracts share `application/page-types/` with the insight door's six, so the folder cannot say which door owns which; this door had named `for-brief` and `for-principle` and never `for-design`, the one the whole lane is built around. Names only — versions come from disk via `/haipipe-skillset-status`.

- 0.5.0 (JL 260828, the one-thread-one-folder merge + the reads: second entry-kind): the board tree shows one thread folder per bet, card.md first; `reads:` may list the discovery bank so a generate/brainstorm card's warrant-theory QA file sits lawfully inside its grant — found as a live checker conflict (law 4 vs law 3) during the B00 migration, fixed by whitelisting, not by exemption.
- 0.4.1 (JL 260828, "unify the names"): the trio reads as one line — design card → designer → design unit; "direction card"/"strategy card" retired from prose family-wide; DR ids and the direction/ folder stay as disk anchors (checker + live cards).
- 0.3.0 (260828, JL's creativity critique): the creative half built — ① DIVERGE, an ideation slate before any card (evidence-fed AND theory-fed modes: a move from named theory or declared intuition is legal, the card carries the honesty via stance + falsification), mirroring the paper family's Ideation the design family never had; ② BET unchanged; ③ VARY, the realization law — one thesis may land a VARIANT SET (same wager, different verbalization), because wording effects are real and the design space is mostly there; variant difference is itself a testable hypothesis, the EMIT edge's natural cargo. Verb `diverge | ideate` added. Root observation: a designer who may only cite cannot surprise; the family had insight discipline applied to the wrong lane.
  Earlier use of the same label (260827, cold-read BLOCKER fix): the door no longer denies the lane's phase machine — §The journey now names haipipe-design-workflow (D0-D4, GD0-GD5, the thread, rounds, the commission entry) and states the division of labor, exactly as haipipe-insight did for its machine; the Who-owns-what block gains the machine's row and the plugin row gains prospect + the judged: verdict line.
- 0.2.1 (260827, cold-read audit): the mandate-first birth no longer borrows the page-state glyph `🔴` for register cells — needs land as open, unanswered cells, in the register's own vocabulary (haipipe-page-for-question).
- 0.2.0 (JL 260824): the Reads Law now says a grant NAMES InsightBoard pages without breaching the principle layer's warrant monopoly, and covers a board that declares no reads: at all — `mode: record`, for pre-contract artifacts. 0.1.0: the door, two plugins, one agent, three declarations.
