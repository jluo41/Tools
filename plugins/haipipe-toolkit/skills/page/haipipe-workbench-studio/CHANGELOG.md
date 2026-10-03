## 0.5.0 · 2026-10-02 · served from servers/workbench-shared

- The Studio runtime moved from `servers/workbench-studio/` to `servers/workbench-shared/`, beside the read-only Guide, because every workbench reuses it: Paper Story › RoadMap Draw, Task Roadmap Studio, a Page's 🎨 Studio tab and Guide's canvases all open drawings through `xcal.py` and `excalidraw_proxy.py`. Moved with `git mv`: `xcal.py`, `excalidraw_proxy.py`, `autodraw.py`, `chat.py`, `turnring.py`, `term.py`, `autodeck.py`, `assets/xcal-boot.js`, `assets/js/10-drawer/*`, `assets/css/86-*.css`, `assets/vendor/xterm/`. Module names, `/_board/*` routes and the assembled `board.js`/`board.css` are unchanged (byte-identical apart from two comment paths).
- `_host/host_registry.WORKBENCH_ROUTES`: the `studio` row is now `shared`, named after its folder; `--only shared` is what keeps the terminal and chat on an `--only` host (`--only studio` is now refused with the list of names).
- The skill keeps its name; `servers/README.md` notes it as the one contract served from a differently named folder.

## 0.4.1 · 2026-09-29 · outline/ to draft/ in current-layout prose (JL 260929)

- Paths that describe the current Page layout say `draft/`: the plan `draft/<stem>-draft-v<G>.<S>[.<E>].md`, records `draft/records/`, `draft/previous/`, `draft/skill/`, the Evidence Markdown `draft/<stem>-evidence-items.md`, `draft/evidence/bibex/` and `draft/evidence/materials/` (JL 260929: "it should be draft"). Mentions of legacy Pages, retired `outline/evidence/` lanes and the migration keep `outline/`, as do the OUTLINE stage, the Outline table and the `outline:` grammar key.
- Server `workbench-studio/chat.py`: the Page context names the real plan folder (`draft/: ...`, `draft/skill/: ...`) instead of a fixed `outline/`, and the board rules tell the agent to log in `draft/records/<stem>-log.md`.

## 0.4.0 · 2026-09-22

- Renamed with the vocabulary: `plugin` now means only a Claude Code plugin
  (`plugins/haipipe-toolkit`), a **lane** is a folder on disk, a **workbench** is
  a served tab and its contract. This skill was `haipipe-plugin-studio`; it pairs by name with
  `servers/workbench-studio`.
- Moved up one level to `skills/page/haipipe-workbench-studio`.

## 0.3.1 · 2026-09-20

- Route candidate feedback into its existing Run and apply shared release rules.

## 0.3.0 · 2026-09-11

- Route feedback-led drafting to the persistent Writing Run instead of full CONTENT drafting per chat; distinguish kept chat transcripts from durable feedback/output records.

# Changelog · haipipe-workbench-studio

## 0.2.2 — 2026-09-06

- Align live Chat plan-version examples with the shared
  `v<G>.<S>[.<E>]` contract.

## 0.2.1 — 2026-09-04
- Make `studio/chat/` and `studio/draw/` the direct destinations of every new
  folded-Page writer; retain flat lane paths as read-only migration inputs.
  First canonical Draw open copies legacy scene content without altering the
  old file; save and autodraw refuse the legacy address.
- Make Chat keep land the promised timestamp-first `digest.md` plus
  `transcript.md`, with a numeric suffix only for a same-minute collision.

## 0.2.0 — 2026-09-04
- Make Studio the only callable skill for the human room; Chat and Draw keep
  their full lane laws as `ref/chat.md` and `ref/draw.md`.
- Carry forward Chat 0.4.6's current five-phase controller, Context Workspace,
  and Evidence Item Supporting/Local Run bindings. Git preserves both retired
  lane changelogs.

## 0.1.1 — 2026-08-31
- The draw half FOLDS (JL: "make the draw collapsable"): ⌄/⌃ on the ✨ bar
  and 🖌 in the chat composer both press window.__studioToggleDraw; the
  choice is per reader, remembered (board-studio-draw).

## 0.1.0 — 2026-08-31
- Born (JL: "put both of them into the studio, as one page"): ONE 🎨 tab
  staging the drawing above the chat, both live; shell strip rows 💬 🖌 🎞
  folded (🎞's ✨ pen moved to the 📤 Delivery slides segment); stored tab
  sets migrate on load; chat/draw rules untouched.
## 0.2.2 — 2026-09-06

- Align the Chat lane's Shape and evidence/Run revision examples with
  `v<G>.<S>[.<E>]`, including the G>=1 CONTENT route after an evidence fold.
