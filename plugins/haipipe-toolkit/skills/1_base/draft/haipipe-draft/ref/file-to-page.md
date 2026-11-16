This file holds the rest of § File → Page Folder → work (after `setup`: hosting, the standalone server, Scratch, the Draft authority, the two response modes), moved from `SKILL.md`.

Markdown `setup` already performs `build`; do not run a redundant second build.
Use `migrate-addresses` explicitly for a pre-0.81 Shape whose paragraph number
resets inside each division; it preserves prose and rewrites active Page-owned
references before `setup` revalidates and rebuilds the Page.
`outline-tidy` rewrites the current Outline Draft-first, moves every older
version (and any retired `-logic.mmd`) into `draft/previous/`, moves the six
process records into `draft/records/`, and repoints `draft/<file>`
citations in the Page's own files (records, Run scripts). It refuses when a Bullet would
change, and works on Board Pages too, not only standalone folders.
After it returns, inspect the generated Page Face, Shape/Draft coverage, setup
Result checklist (`checks.json` and `report.md`), and `delivery/web/index.html`.
Setup fails when a blocking mechanical check is missing; semantic judgment and
human acceptance stay visibly deferred/untested. If role or Draft inspection
changes a checked artifact, rerun `setup <existing-page-folder>` so a new Task
Run validates the current records; `build` alone does not
refresh the audit. Start `serve` only when the user
explicitly asks for a hosted/live URL; a request for a built website is
satisfied by the static delivery and does not authorize an indefinite foreground
server. When hosting is requested, use the workspace's supported background
process manager, verify the configured public URL, and return instead of
blocking on the listener. One skill invocation performs all requested mechanical
substeps; do not make the user request them separately.

The built `delivery/web/` is a portable static reading site. The server always
renders Page source read-only and adds the same category-workbench pane used by
Board Pages. Standalone advertises only real top-level presenters: Outline,
Delivery, Folder, plus an optional domain-owned Labeling presenter when a
direct `labeling/` lane is present. The
standalone Labeling surface uses the current Codex task as its Chat transport;
Studio remains Board-hosted until its chat/draw backend is extracted. Evidence
and Run stay internal Outline workspaces, never duplicate top-level Workbenches.
Choose the configured
reader-facing origin for links; exposing workbench writes beyond loopback requires
a token. The standalone Page Face has no Chat launcher, comment composer, or
Page-source save control. Edit Markdown and imported material on disk. Bounded
workbench read views remain available in either server mode. `--read-only`
disables workbench writes; without it, Scratch notes autosave and Finish is a
separate manual action. Do not publish private inputs without the user's
authority. Static files do not provide save-back.
Report build, server reachability, and workbench interaction mode separately; do
not claim hosting from a successful build alone.

Board registration is optional and separate: register the same Page Face,
then let Board supply navigation. Moving/removing Board membership must not
move or replace the Page's source. Board Page group descriptions remain
Board-owned and are outside this file-intake operation.

Scratch is available as a small human-thinking capture once the selected
Outline exists. Notes autosave to `run-scratch-<target>`; the person manually
clicks Finish Scratch, which asks the AI to generate a concise Summary from
the raw notes and closes the Run only after a non-empty Summary is returned.
Scratch writes only the selected Outline's `## Scratch` registry plus its
paired `runs/` and `results/` receipt; it never edits Draft prose. In
Scratch Mode, saved raw Scratch remains visible by default even when the
underlying body is hidden; `+` reopens its editor. The Board-hosted Page Chat
and terminal read the current Scratch registry at connect time, and a saved
Scratch refreshes a held Page Chat's context. When the person asks to use
Scratch, treat the notes as user-authored planning context and route any
resulting wording through the normal Page workflow.

The reader-facing completion packet is defined in
`ref/user-check-packet.md`. The Draft Space includes a read-only Draft
projection beside each Bullet during SHAPE. The selected
`draft/<stem>-draft-v<G>.<S>[.<E>].md` (legacy `outline/<stem>-outline-...`) is the sole Draft authority: each
Bullet stores its planning fields and Draft candidate in that same file.
The candidate may exist before Shape approval and becomes exact adoption input
for CONTENT when explicitly accepted. The Page/Run Workflow is the writer of
the plan, the Page, and every Result; the reader-facing Table and Reading
views write none of them through the browser. Human feedback and acceptance
enter through the owning Page Writing Run's interaction and its recorded
Steps/Versions; Scratch is the explicitly bounded exception for rough human
notes. Draft Space has no legacy note thread or feedback composer. Delivery Workspace
is the read-only source-to-artifact consistency projection; it does not replace
the human Page CHECK gate.
See `workbench-task-draft/ref/content-preview.md` for the write boundary.

Use `ref/user-check-packet.md` for the two response modes: a routine Writing
Step returns its exact Run/Version/Step heading, complete selected paragraphs,
a frozen Structure description beside each paragraph address, a numbered
blockquote review passage, a brief change explanation, and the three
final Draft Space, Evidence Space, and Run Space links;
a formal delivery also returns the Delivery Workspace consistency receipt and
the evidence/PDF surfaces that are current.
The Current Run derives granular Track Changes from clean Step-level Before and
After text and shows each material wording change's local type, rationale, and
analysis status. Legacy records may retain historical preference fields, but
interactive Page Steps defer new preference inference to post-run analysis.
Diff markup never becomes Page prose, and analysis never becomes shared policy
without confirmation.
Classification lives in the change-card heading, not a second table. Status,
navigation, acceptance-only, and presenter-only Steps create no Track Changes;
the Runs surface expands only the current Step and keeps older Steps collapsed.
