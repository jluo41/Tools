haipipe-board — Changelog
=========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

**v0-series rule (JL, 2026-07-23):** this skill stays on `0.x.x` — **it never goes to 1.0.0 without JL's explicit say-so.** Everything here is provisional: the board form, the Q template, the generator's output. Ship `0.MINOR.PATCH` freely; `1.0.0` is a decision, not a milestone that arrives on its own.

## [0.29.0] — 2026-07-26 — warn when a board writes markers and declares no dialect

The `dialect: paper` seam had exactly one silent failure: a board that writes `\citep{}`, `{VAL:?}` or `[Q-…]` and forgets the two frontmatter lines renders them as plain text, produces an EMPTY marker report, and looks completely fine. Nothing said anything. On a paper board that is the loss of the family's only cross-check of prose against the `.bib` and the display units.

`build.py` now says so, on the `else` branch that previously did nothing.

**The trigger is the board's own CONTENT, never its folder name.** A dialect is deletable (QBc5) and `build.py` must not learn what a paper is, so it does not look for `0-lifecycle/`; it looks for marker syntax.

**Code spans are stripped first, and that is the whole precision of the check.** A board that MEANS a marker writes it in prose; a board that DISCUSSES the syntax quotes it. Measured across the four real boards on 2026-07-26: `01-boardform-260722` has 13 mentions and `01-probe-qa-260726` has 2, all inside code fences or backticks, none meant. A naive raw match warned on both; stripping code first gives zero false positives on all four, while a real paper board with the two lines removed reports 429.

Verified: `Paper-Personality2Opioid-MISQ2026/0-lifecycle` builds byte-identically (40 pages, 22 markers), and the same folder with `dialect:`/`paper-root:` deleted now warns loudly with the exact two lines to add.


## [0.28.1] — 2026-07-26

**Driven by a real browser at last, which found two things nothing else had.** JL asked "will it work?", and the honest answer was that nobody knew: 0.27 and 0.28 were verified against a server and a stub. Chrome is installed on this machine and Node 22 ships a WebSocket, so the DevTools protocol closed that gap.

- **The app never started.** `proxy_excalidraw()` injected the boot script at `<head>`,
  which put it BEFORE the `window.__haipipeApp` assignment it reads, so `start()`
  returned quietly and no module was ever appended. The page rendered a correct badge
  over a blank screen. The boot tag now goes immediately AFTER the assignment. This had
  been shipped, reviewed and reasoned about twice without being noticed, because every
  test up to that point stubbed the very thing that was broken.
- **Opening a page dirtied the repo.** Excalidraw renormalises everything it loads
  (`version`, `versionNonce`, `updated`, `boundElements` null → []), so the editor saved
  one second after opening with nothing drawn. Two halves to the fix: the tab compares
  element CONTENT rather than raw JSON, and `xcal.py` keeps an element the browser has
  enriched instead of writing its plainer version back. Without the second half the two
  would have dirtied the file in turn forever, each undoing the other.

End to end in headless Chrome: the app mounts, our seed is what it loads, pressing `r`
and dragging produces a rectangle, and that rectangle arrives in `fig/board.excalidraw`
inside `frame-QB3` with the other 88 elements untouched and no page errors. Opening the
editor twice leaves the file byte-identical the second time; two `xcal.py` runs do too.

## [0.28.0] — 2026-07-26

**A pasted image survives, as a real file in `fig/assets/` rather than as base64 inside the scene.**

JL: *"could we make it saved? we can have an assets folder for it."* Right on both counts, and the folder is the part that matters. Excalidraw keeps images as base64 dataURLs INSIDE the document, so one screenshot is megabytes that git then re-diffs every time anyone nudges a box.

- **Bytes out, pointer in.** `stash_files()` decodes each dataURL into
  `fig/assets/<fileId>.<ext>` and leaves `{id, mimeType, path}` in the scene.
  `hydrate_files()` does the reverse on the way out, for the elements being
  returned only. Fetched through `serve.py` the scene is self-contained and the
  editor never knows; the files map is MERGED on save, so an image saved by an
  earlier tick is never lost by a later one.
- **Every `.excalidraw` GET now goes through the scene handler**, not only
  `?frame=` ones, because a whole-scene fetch needs rehydrating too.
- **IndexedDB, not localStorage.** Images live in `files-db`/`files-store`, keyed
  by fileId, which localStorage seeding never touched. The boot script seeds and
  reads that store directly.
- **The app's own module script is now HELD.** `proxy_excalidraw()` turns it into
  `window.__haipipeApp` and the boot script appends it once seeding has actually
  finished. A classic script in `<head>` was enough to beat localStorage, which
  is synchronous; it is NOT enough for IndexedDB, and an app that boots mid-seed
  renders grey placeholders. A URL with no `board=` starts the app immediately,
  so a plain visit to the editor is unaffected.
- **An image is uploaded once.** The tab tracks which fileIds the server already
  has (seeded from the scene it loaded), so a 1.5s save tick does not re-send a
  megabyte screenshot every time a line moves.

Verified over HTTP end to end: a PNG saved, landed byte-identical on disk, left
no base64 in the scene, and came back byte-identical through both the frame URL
and the whole-scene URL; a frame with no images gets an empty files map. Plus 13
new browser-stub assertions (app held until the seed lands, a plain visit still
boots, an image sent once and not again) and the 25 existing ones still passing.

⚠️ The cost of the split, worth naming because "open it in any Excalidraw" was an
argument for owning the file: read straight off disk by the VS Code or Obsidian
plugin, images show as missing, since the bytes are beside the scene rather than
in it. Through the server they are there.

⚠️ Still open on `QA4a`: deleting an image element leaves its file in
`fig/assets/` (removing it automatically would leave undo with nothing to come
back to), and editing the seeded ASCII text is still reverted by the next
`xcal.py` run.

## [0.27.0] — 2026-07-26

**The excalidraw round-trips: what you draw lands in `fig/board.excalidraw`, and opening another page no longer offers to throw it away.**

JL, on the 0.26.0 build: *"When I edit the excalidraw, the changes won't save. And when I open another new Page, it asks me to reopen again and overwrite the current one. What I added will be gone."* Both symptoms had one cause: the open-source app loads from `#url=` and saves to the browser, so the file was in the loop at neither end.

- **`assets/xcal-boot.js`, injected by the proxy.** `proxy_excalidraw()` now rewrites the
  app's HTML to add one classic `<script>` in `<head>`, which is the only window in
  which `localStorage` can be replaced (a module script is deferred; a classic one in
  head is not). The script seeds the editor from the scene file and, in the editing
  tab, pushes changes back. `#url=` is gone, so the "Replace my content" dialog has
  nothing to confirm and never appears.
- **The URL changed**: `?board=<scene>&frame=<page>` replaces `#url=…`. `xcal.py --wire`
  writes the new form; `board.md`'s `excalidraw:` line is unchanged.
- **`POST /_board/excalidraw-save` MERGES.** With `frame=`, only that frame's slice is
  replaced and the other 27 are left byte-identical, which is what lets one file be
  edited from any page. The frame's id and name are forced back on save because the
  name IS the page's link; a deleted frame is restored; deleted elements are dropped;
  the write is atomic. Without `frame=`, the whole scene is replaced.
- **An embed reads, a tab writes.** A board page carries one iframe per page, all on one
  origin sharing one storage key, so an editable embed would be 28 editors overwriting
  each other and then reading the result back as their own. An embed gets an in-memory
  storage and persists nothing; "✏️ Edit this frame" opens the one tab that writes, and
  a lock in real storage keeps it to one tab (a second drops to read-only and says so).
  The app REFUSES to restore `viewModeEnabled` from storage, found by reading its own
  per-key policy table; `activeTool` and `zenModeEnabled` do restore, and a locked hand
  tool is better anyway because panning and zooming still work.

Verified server-side over HTTP (a rectangle drawn into QB3 lands in that frame, the
other 27 slices compare identical, an unknown frame name and a path outside `--root`
are both refused) and client-side against a stubbed browser, 22 assertions covering
both modes, the save payload, the idle tick, and lock contention. **Not yet exercised
in a real browser**: no browser was reachable from the session that wrote it.

⚠️ Two edges left, both on `QA4a`: a pasted IMAGE does not survive, because Excalidraw
keeps images in a `files` map and the endpoint writes `elements` only; and editing the
seeded ASCII text in Excalidraw is reverted by the next `xcal.py` run, since that text
is a generated element (drawings around it are kept).

## [0.26.0] — 2026-07-26

**A board owns one excalidraw, a page owns one frame in it, and the frame opens onto the figure that page already had.**

- `xcal.py <board-dir>`: builds `fig/board.excalidraw` from `board.md` and the pages.
  One scene, one frame per page, one row per `## Pages` group with the group's name
  above it, each frame sized to what it holds. `--wire` also puts every frame's URL
  into its page's `## Diagram`, replacing whatever was there. It is a separate script
  from `build.py` on purpose: `build.py` runs on every file save and a scene regen
  must not.
- **Frames are seeded** with each page's first `## Diagram` fenced block, as one
  monospace text element. JL opened `?frame=QB3` on 260726 and found a blank
  rectangle, which is exactly what had been built: 28 named frames with nothing in
  them. A scaffold and its content are two deliverables and only the second one is
  visible, so shipping the first reads as a broken feature. The seed is ONE-WAY;
  the markdown stays the source, and 25 of 28 pages had a figure to give.
- **Re-running is safe**, which is the only reason it is a script. Every minted id is
  prefixed (`frame-QA4a`, `t-QA4a-fig`) so a regen renames nothing and no page's link
  dies; an unprefixed id is a human's drawing and is carried through; a frame a human
  moved keeps its position; a prefixed frame whose page has been retired is DROPPED,
  which is `QA4a`'s dead-frame rule. Verified by injecting both cases. `--fresh` is the
  one destructive mode and is never the default. Overlapping frames are reported,
  since a kept position plus a recomputed width can collide.
- `check.py` gained `open-with-done-items` and `partial-with-nothing-open`. SKILL.md's
  `sync` action has always required writing a page back in the same round; nothing
  ever noticed when a session skipped it. `QA4a` said "nothing is built and nothing is
  decided" on the day its whole route was built and running (JL 260726: think about
  how to update the related Q along the session). The check only sees `state:` and the
  boxes, so it is a backstop under the rule, not a replacement for it.
- SKILL.md: an `excalidraw` action, and `sync` now says the trigger is **substantive
  work in the session**, not opening a page. Every piece of real work belongs to some
  page even when it started as a line of chat, and work that belongs to no page is a
  new page. "Done" means written back.

⚠️ **Not closed: the write-back.** `#url=` loads, the editor saves to the browser, so
nothing drawn returns to `fig/board.excalidraw`. The scene is a view of the markdown
and not yet a place to work.

🩹 One regex cost four pages. `^\s*<url>\s*$` looks line-anchored and is not, because
`\s` spans newlines: it ate the blank lines around the URL, and an off-by-one on
`hit.end()` took the `#` of the next heading with it, welding `## Diagram` to the URL
on three pages and giving a fourth two `## Diagram` sections. All four were repaired
and `--wire` now rebuilds the section instead of splicing into it.

## [0.25.0] — 2026-07-26

**A board can now be checked, and an author note finally behaves the way the template said it did.**

- `check.py <board-dir>`: the structural half of `QA9`, read-only, four families.
  BOARD (`board.md` against disk, declared Links resolve, ids unique), FACE (required
  sections, the four state values, references resolve, one sentence per line, no
  em-dash, English-only), PAGE (the built html: local hrefs resolve, tags balance,
  ids unique, the zero-script invariant), and TEMPLATE (render `ref/q-template.md`
  as a Q AND an S, then assert each of QA9's 15 constructs). It reuses `src/parse.py`
  rather than carrying its own grammar. Report-only, exit 0; `--strict` exits 1 on
  ERROR and waits on JL's ruling about whether a red result blocks a change.
- A construct the template never demonstrates is reported as a GAP rather than
  skipped, which found three on the first run: code block, group title, excalidraw
  canvas are documented and untested.
- `parse.strip_notes`: `<!-- ... -->` author notes are dropped BEFORE the text is cut
  into sections. `ref/q-template.md` has always told authors a note "is dropped at
  generation either way" and it was not: the only strip lived in the Stage Contract
  path, so a note written anywhere else came out as escaped `&lt;!--` prose. Order
  matters and cost two attempts to learn, because `split_sections` reads a `## ` line
  INSIDE a comment as a heading, so a note listing sections was torn in half and left
  a phantom section behind. Fenced blocks are protected and `<!-- haipipe:… -->` is kept.
- The index page's ＋ button writes Boundary and Files, which `QA2` rules "strongly
  advised", and offers the optional sections as an author note. Its stub was a second
  definition of a new face carrying 4 of the template's 14 sections; a face generated
  from it arrived with no Diagram and nothing said one was available.
- `prime_context` counts unresolved comments and unticked items separately and names
  each. One number announced as "unresolved comments" made a cold agent notice the
  mismatch, fail to resolve it, and invent an explanation for it.
- `CHAT_RULES` lists the current section names, with the retired ones named as
  accepted aliases, and explains what a `>` lane is and that it is addressed to the
  turn reading it. It had described a face layout retired days earlier.
- Index rows lost their coloured left stripe (`QA10`). Every row already opens with
  the state emoji, so the bar restated it in a second language.

## [0.24.0] — 2026-07-26

**Diagram was the last body section you could only read. Now you can draw into it.**

- `🖼 Diagram` gets a `🖌 Add an Excalidraw canvas` control (`QD7`). Paste a share URL, hit
  Save, and `serve.py` writes it on a line of its own inside `## Diagram`: the same line an
  author types by hand, so the md stays the single source and an older copy of the skill
  still renders the result. Endpoint `/_board/diagram`, control `wireXcal` in `board.js`,
  styles `.xadd`. The generator was not touched.
- One canvas per face: a second paste replaces the first instead of stacking iframes. The
  response says `replaced: true` when it did.
- A face with no `## Diagram` gets one created immediately before `## Content`, which is where
  the fixed on-stage order puts it, and the response warns that a canvas without an ASCII
  figure is the half that disappears when it cannot load (`QA4 §2`).
- A URL that is not `excalidraw.com` is refused with nothing written, and the section scan
  skips fenced code blocks so example markdown inside `QA4` is never written into.
- `serve.py` takes `--host`, still defaulting to `127.0.0.1` (`QE6`). The bind address is this
  server's only access control, since there is no auth and `/_term/` is a real shell, so any
  non-loopback bind now prints a warning line at startup. Nothing changes for anyone who does
  not pass the flag.
- `QA4 §2` documents the Excalidraw half as a mechanism rather than a mention: one URL alone
  on its line, what it renders, and why the fallback link and the ASCII figure both stay.

## [0.23.0] — 2026-07-26

**The first Board UI taste pilot is live, bounded by QA10.**

- All native links, buttons, disclosures, fields, and explicit tab stops now share one
  high-contrast `:focus-visible` ring; pointer interaction keeps its existing appearance.
- Four semantic radius tokens replace unrelated one-off values: inline highlight, control,
  surface, and pill. Focused faces keep their existing zero-radius, unframed reading mode.
- `prefers-reduced-motion: reduce` now suppresses current and future transitions and animations.
- The pilot is CSS-only and reversible: it changes no Markdown grammar, generated structure,
  interaction contract, or dependency.

## [0.22.0] — 2026-07-25

**The page directory is now called Pages.**

- New and migrated boards use `## Pages` for the filenames, groups, group introductions, and display order.
- Parser and structure writers treat `Pages` as the canonical section while continuing to read old `Roster` headings.
- Board prompts, warnings, examples, Paper page creation, and the seven active boards now use the same plain term.

## [0.21.0] — 2026-07-25

**Content gets a second heading level, and 🔹 gets its meaning back.**

- `####` is now a first-class paragraph heading (`.ph`): no icon, one size below a group
  title, its own spacing. It used to be flattened to `**bold**` before rendering, and a
  full-line bold IS the group-title construct, so every paragraph arrived wearing 🔹 and
  claiming to lead a run of items. Deleting the icon would have hidden the mistake; the
  page was not over-decorating a paragraph, it was calling it something it is not.
  On the MISQ board the split came out 113 paragraph headings · 82 job lines · 31 group
  titles, with 🔹 left only on the 31 that really lead items.
- A full-line `(…)` directly under a `####` heading is that paragraph's **job line**
  (`.pj`): grey italic, on stage, one line only. It is the scan hook that lets a reader
  see what each paragraph does without reading the prose, so it is not hidden behind a
  click. Only the line immediately after the heading is read this way.
- Focus-mode spacing fix: `.q:target .ph` (0,3,0) outranked `.ph:first-child` (0,2,0), so
  the first paragraph after a section heading opened 22px low instead of 2px, and only in
  sections that begin with a heading, which is why it read as inconsistency rather than as
  a gap. `.gt` had already been patched for this once; both now share one selector.
- **The rule these render:** Content carries exactly two levels and the depth lives in the
  numbering, not the heading level. `###` is a division that folds on its own, `####` is one
  paragraph inside it, and there is no third level because the page folds exactly one. A
  division is written only when it holds something, so a flat section carries one
  `### §1 Introduction` over its paragraphs while a subsectioned one starts at `### §6.1`.
  The shape is then checkable without reading: the subsection count is the number of `###`
  headings whose number contains a dot.
- An S page title may carry the artifact's own number when it is offset from the board
  index (`S Main 7 · §6 Results`), so the derived Content heading reads
  `📚 Content · Main 7 §6 Results` and the two numbers stop competing on one screen.
- New writing rule: **an ASCII figure must survive being copied.** Never draw two trees side
  by side; the column boundary is whitespace, it disappears on paste, and the right column's
  rows read as branches of the left one. Real case: a two-column comparison of two heading
  trees came back pasted as one tree with the wrong nesting.
- Docs caught up with code that had already shipped: the levels and the job line existed only
  in `src/body.py` and `assets/board.css` and were documented in none of SKILL.md,
  `ref/board-form.md` §4/§5, `ref/writing-rules.md`, or `ref/q-template.md`. All four now
  carry them, and QA4 records the ruling, the Law, the Glossary terms, and the Lesson.

## [0.20.0] — 2026-07-25

**Sentence apparatus v1 (QA8): click a sentence, see its evidence.**

- A plain sentence followed by `>` lines now renders as a native `<details>`: the sentence
  stays on stage with a ⚑N badge; the `>` lines fold into a drawer beneath it. Typed lanes
  name the attachments (`> Citation:` 📚 · `> Value:` 🔢 · `> Display:` 🖼 · `> Check:` ⚠️ ·
  `> Q-consumer:` 🔎 · `> Link:` 🔗 · `> Source:` 📄 · `> Note:` 📝); `> WHO:` review threads
  join the same drawer with their comment styling. Implemented in `src/body.py`
  (`render_apparatus` + the `last_p` attachment walk) and `assets/board.css`.
- Attachment is by adjacency: a `>` run under a sentence (blank lines tolerated) belongs to
  that sentence; a run with no sentence above it renders as before, and the supporting folds
  (Discussion, Why here, Law, Lesson, Glossary, Log) never fold apparatus.
- Zero-script invariant holds (native details). Pages change only where `>` lines already
  follow a sentence. Piloted on the boardform lab board (QA8 ruling + QA4 self-demonstrating
  subsection); the MISQ paper board is untouched pending JL's acceptance.
- Click-to-add: `POST /_board/sentence` inserts `> Lane: text` directly under the exact
  sentence in the md (markdown-stripped anchor match, visible failure on a miss) and rebuilds.
  On the page: click a bare sentence for the lane + text form, or the "➕ add to this
  sentence" row inside any open drawer. Script-only enhancement over the no-JS reading path.
- Sentence hover tint (accent at 8%) shows which sentence a click or selection will target.
  The form opens on DOUBLE-click, leaving single click free for reading and selection.
- Copy is section-level: every section heading carries a ⧉ button that copies that whole
  section as clean plain text, folded drawers and item explanations included, with no badges,
  buttons, or highlight formatting. A per-sentence copy button was tried and removed.
- Every section folds from its own heading (Content, Items to Finish, Where we are, Files), the
  native-details mechanism Diagram already used. All open by default except Diagram, since the
  reading path must survive a reader who never clicks; folding is display-only, so Ctrl-F, the
  section ⧉ copy, and the no-JS fallback are unaffected. Expand-all and ⧉ no longer toggle the
  section they sit in, and ⧉ force-opens a folded section in its clone before copying.
- `ref/q-template.md` brought up to these rulings, then hardened by a fresh-context cold read:
  the apparatus example was itself hard-wrapped and taught the failure it warns about (a wrapped
  lane becomes its own sentence row and steals the lanes below it); the S title convention that
  feeds the Content heading was undocumented; the contract markers must not be hand-copied
  (a hand-written sha reports the page unsynchronized, and sync replaces anything between them);
  `requires:` resolves S ids bare but needs a real filename with extension for anything else.
- Opening starts fully collapsed on S pages (JL 260725: "all the things here should be hidden").
  Why this matters, the optional Stage Record, the Stage Contract, and the contract's own parts
  all begin shut, so the lead question is the only thing on stage. Q pages are unchanged.
- S Content holds the stage's real product only (QA4 Law, JL 260725). Inherited contract
  material belongs to `## Stage Contract`, settled flags and corrections to `## Where we are`,
  open work to `## Items to Finish`. The Content heading now NAMES the stage on S pages
  (`📚 Content · Main 7 Results`) instead of counting subsections; Q pages keep the count.
  Authored subsections under `## Stage Contract` are sync-safe: `replace_managed` rewrites
  only the span between the `haipipe:contract` markers (verified on the MISQ Results page).
- Comment highlights are painted with inset box-shadow instead of background-color, so text
  copied into Word no longer carries the pale yellow fill; `code_or_link` stopped
  double-escaping code spans (backticked `>` rendered as `&gt;`).

## [0.19.0] — 2026-07-25

**The reading pass: sentence lines, serif prose, Stage Contract inside Opening (JL 260725).**

- Stage Contract now renders INSIDE Opening as one collapsed disclosure after Why this matters
  and Stage Record (JL: "within the Opening. Not a separate section."). The standalone section
  between Opening and Diagram is gone; comment anchors scan it as part of Opening. Source
  anatomy is unchanged: S files keep their `## Stage Contract` section and managed markers.
- One sentence per source line is a writing hard rule (ref/writing-rules.md). The renderer has
  always given each plain prose line its own row, so a mid-sentence hard wrap became a broken
  line on the page. Both live boards were re-flowed to sentence lines (boardform 25 faces,
  MISQ lifecycle 42 faces); prose content untouched, only line boundaries.
- Face prose (Opening lead, paragraphs, item titles, group titles) switched to a serif reading
  stack: Charter / Georgia / Cambria with Times New Roman as the print-classic fallback. UI
  chrome (ids, pills, bars, code) keeps its sans/mono faces.

## [0.18.0] — 2026-07-25

**Display is independent, and S pages inherit explicit requirements and writing style.**

- Canonical paper families are now Seed, Work, Venue, Display, Main, Appendix, Submission.
  Display owns the claim-to-display map, approved assets, captions, statistical labels, and
  placement consumed by Main and Appendix.
- S metadata accepts `requires`, `style-from`, `provides`, and `contract-source-hash`. Pages
  adjacency never implies a dependency.
- `stage.py new|sync|check` creates S pages, refreshes only the managed Stage Contract block,
  and detects upstream source changes. `build.py` remains render-only and reports stale contracts.
- `stage.py sync --all` follows the explicit dependency graph in topological order; Pages order
  remains a navigation concern and never controls inheritance.
- S pages render `Stage Contract` between Opening and Diagram. Required Inputs and Writing Style
  stay separate from authored Content; upstream prose is linked and summarized, never copied whole.

## [0.17.1] — 2026-07-25

**S families are stable homes, while Pipeline owns execution and revision loops.**

- The six-family index order no longer claims every paper runs as a simple family-by-family line.
  A Pipeline may revisit Work/Displays after Narrative while keeping one stable Work group.
- Submission pages are reused per initial submission and revision round. An external decision
  reopens affected Work, Main, or Appendix pages, then returns through reconcile, compile, review,
  and submit; it does not duplicate a new S page set for every round.

## [0.17.0] — 2026-07-25

**Paper lifecycle S pages now use readable, full-name families.**

- Canonical filenames use `S-<Family>-<unit>-<slug>.md`, with six families in lifecycle order:
  Seed, Work, Venue, Main, Appendix, Submission.
- Seed can carry both `S Seed` and `S Literature`; Main exposes one page per manuscript section;
  Appendix uses `0` for control and `A-F` for units; Submission makes reconcile, compile, review,
  and submit explicit gates.
- HTML ids are readable (`#S-Main-3`, `#S-Appendix-D`), badges name the family, JSON emits
  `family`, and the index reports a separate progress fraction for each family.
- Legacy `S0`, `SM0`, and `SA0` filenames remain parse-compatible for existing boards, but the
  authoring docs and template no longer recommend those abbreviations.
- The MISQ paper board was migrated end to end, including a new literature-seed page and three
  terminal submission pages.

## [0.16.1] — 2026-07-25

**Paper lifecycle boards now expose the lifecycle as their primary index structure.**

- One Pages group represents one paper stage, ordered S0 through S5.
- The canonical S face is the first row; every Q row after it is a ruling owned by that stage.
- Stage-only groups remain visible instead of being merged into broad QA/QB/QC buckets.
- Group headings retain a unique Q family writer key, such as `QD · S4 · Display`, so index-side
  add/archive controls keep working.
- The MISQ paper lifecycle board was reorganized into one paper-level frontier group plus eight
  stage groups, with S4→QD2-QD8 and S5→QE2-QE7 ownership explicit.

## [0.16.0] — 2026-07-25

**Creating an S lifecycle stage is documented, not only rendering one (QB pass).**

The QB2 fresh-agent acceptance was re-run against the shared Q/S skill (4 Q faces + 1 S stage
on a lab data-retention topic; SKILL.md + `ref/` only, existing boards out of bounds). Verdict
YES, first-try build, gate respected, Stage Record lifted. Everything it had to invent was on
the S **authoring** side, and all of it is now written down:

- `SKILL.md` `open` steps 1 and 4 ask for Q **and** S faces, give both filename shapes
  (`Q<letter><n>-<slug>.md` / `S<order>-<slug>.md`), state S's required `## Content`, and say how
  an S is listed in `## Pages`.
- `close` and the Face section: both kinds share the same four `state:` values, and a new face of
  either kind starts 🔴 OPEN. ✅ means "every checkbox closed" on Q and "this stage's human gate
  passed" on S (what the index counts as `stages gated`). `human-gated` is not a state value.
- `ref/board-form.md` §2 gained the S state mapping plus the Pages rule (bare filename, free-text
  group heading, own group or mixed in); §3's example gained an S line.
- `ref/q-template.md`: the Q-consumer `**Probe:**` line no longer assumes a paper's `1-probes/`
  tree; on a standalone board name the real route or write `not opened yet`. Its state legend now
  carries the Q-versus-S ✅ distinction.
- The build section names the interpreter split: `build.py` / `watch.py` run on any system
  `python3`; only `serve.py` needs the repo `.venv` (the SDK requires 3.10+).

Board-side records refreshed in the same pass: QB1's stale figures (128 lines / five actions /
CHANGELOG 0.2.0) replaced with the 0.15.x reality, QB2's second run and a new `## Law`, QB4 noting
that QB5's `src/` split superseded its 850-line build.py, and the `ALIAS` / `sec()` pointers in
QB3 and QA2 repointed from `build.py` to `src/common.py`.

## [0.15.2] — 2026-07-25

**The QD2 chat drawer header is quieter, clearer, and consistent.**

- The saturated accent banner became a neutral 56px utility bar separated by one hairline.
- Face id is compact mono metadata; the full title uses the remaining width and ellipsizes in CSS,
  preserving the complete title in a tooltip.
- Terminal and close are matching 32px square controls with hover and keyboard-focus states,
  accessible labels, and a stable `>_` terminal mark instead of a platform-dependent keyboard emoji.

## [0.15.1] — 2026-07-25

**QA2's source-template contract now explicitly mirrors QA4's rendered Q/S face contract.**

- `ref/q-template.md` states the fixed visible sequence, Q-versus-S Content requiredness,
  rationale placement, Q-consumer closure rule, and optional S-only `### Stage Record` behavior.
- The board's QA2 face now specifies the source-to-render mapping for Opening, Diagram, Content,
  Items to Finish, Where we are, Files, and supporting folds; stale Q-only wording was retired.
- Two fresh-context acceptance rounds rendered realistic temporary boards. The first exposed that
  Stage Record optionality was only implied; after revision, the second rendered one Q and two S
  variants and passed with Stage Record both present and absent.

## [0.15.0] — 2026-07-25

**A chatbot on the index page (JL 260725 on QC2: "just add a chatbot in the index page").**

- It is the existing QD2 drawer and QD3 terminal, opened on `board.md` instead of one question.
  No new agent, no second engine; details recorded on QD2, entry point on QC2.
- `serve.py` accepts `file: "board.md"` as one more face: the orientation block carries the
  index's own view (spine, close, every face's state + open-comment count); board-flavored
  rules; the restricted tier's "own files" widens to any `.md` inside the board folder
  (verified: in-board Write auto-allowed, /tmp Write denied).
- The session id lands in `board.md`'s header (`session:` under `close:`), is parsed into meta
  (`src/parse.py`) and rendered as `data-bsession` on `div.wrap` (`src/page_board.py`), inside
  the live-swap region so it stays fresh without a reload. The drawer's ⌨ opens the same
  session in a real terminal (verified: same session id, proxy 200, clean release).
- `assets/board.js`: `chatOpen('board')`; the bottom-right fab now also shows on the index,
  labeled "🤖 Board chat"; index flavor of the action buttons (🧭 which question should I act
  on · 🔧 handle open comments board-wide); `follow()` returns to the board session when you
  navigate back to the index. `assets/board.css`: the fab shows whenever the drawer is closed.

## [0.14.0] — 2026-07-25

**Stage orientation moved into Opening, and Opening now uses a compass.**

- The visible heading is `🧭 Opening`, replacing the question mark with an orientation icon that
  works for both Q rulings and S lifecycle stages.
- On S faces, the automatic "Why this matters" disclosure now lives in Opening and starts open.
- An exact direct `### Stage Record` inside S Content is lifted into Opening and starts collapsed;
  the remaining stage subsections stay under Content.
- Q faces retain "Why this matters" as Content's first open subsection.

## [0.13.3] — 2026-07-25

**Colleagues replaces the generic assistant role.**

- User-facing prose now says colleague or colleagues instead of assigning everyone one generic role.
- Each colleague signs and owns work with their own initials; examples use `ZW` rather than a
  shared role identity.
- The comment picker defaults to `JL` and `CC`, while any colleague can add their own initials.

## [0.13.2] — 2026-07-25

**Diagram is now a real section and starts closed.**

- The fixed visible order is `Opening → Diagram → Content → Items to Finish → Where we are`;
  Files follows.
- Opening now contains the question lead and optional Boundary. Optional Diagram renders as a
  peer-level native `<details>` section whose heading stays visible while its figure is hidden
  until clicked.
- The figure remains in the HTML and works without JavaScript; ASCII and embedded Excalidraw
  content retain their existing rendering once opened.

## [0.13.1] — 2026-07-25

**The visible first layer is Opening, not a peer list of Question, Boundary, and Diagram.**

- The rendered hierarchy is `Opening → Content → Items to Finish → Where we are`; Files follows.
- Opening contains the actual question lead plus optional Boundary and Diagram. The rest of the
  Question becomes Content's first "Why this matters" subsection, so Q faces follow the same
  visible rhythm even without an explicit `## Content`.
- The source keeps `## Question` for precision, while `## Opening` is accepted as an alias.
- Opening uses the same section-heading hierarchy as Content, Items, and Where.

## [0.13.0] — 2026-07-25

**One face grammar now serves rulings and lifecycle stages.**

- `Q*.md` remains a board ruling; `S*.md` is a lifecycle stage. Both are recursively discovered,
  rostered, commentable, and rendered by the same face renderer.
- `## Content` lands between Diagram and Items. It is optional for Q and required for S; each
  direct `###` heading renders as a native collapsible subsection.
- Former stage `Q-consumer` blocks become recognizable checklist records under
  `## Items to Finish`. The answer must land, be interpreted, and be woven into Content before
  its box closes.
- Question settlement and stage gates have separate index summaries. A stage carries a STAGE
  badge and never inflates the question settled count.
- Focus mode now has a real narrow-viewport layout: smaller wrapping titles, zero-width-safe
  flex/detail children, and measured `clientWidth == scrollWidth` at a 390px device viewport.
- The first complete consumer is the MISQ paper lifecycle board: 14 Q rulings + 8 S stages, with
  the previous stage files archived and all lifecycle `_LOG_*.md` sidecars removed at the user's
  request.


## [0.12.1] — 2026-07-24

**The drawer terminal stops smearing on emoji + CJK (QD3, JL's fig/image.png).** The cause left standing after 0.9.2's cell-metrics fix: claude's TUI counts 🟡✅💬 as 2 cells (modern wcwidth) while the vendored xterm.min.js only ships Unicode 6 width tables that say 1 — every emoji shifts the row, full-screen repaints land off-cell, and the frames interleave into the smear. Vendored `@xterm/addon-unicode11@0.8.0` (new `vendor/xterm/addon-unicode11.js`, whitelisted in serve.py's `serve_asset`, loaded right after xterm.min.js, `unicode.activeVersion = '11'`); verified offline that the v11 provider returns width 2 for 🟡✅💬汉 where V6 said 1. The stacked second cause fixed with it: Menlo has no CJK, fallback glyphs overflow the measured row — the drawer terminal's fontFamily now carries PingFang SC / Hiragino Sans GB / Microsoft YaHei and `lineHeight: 1.2` adds the headroom. Addon load is soft-fail (console warning, terminal still opens), so an older running serve.py cannot brick the drawer.

Also in 0.12.1: **`scrub_cjk_comments` scoped to `<style>`/`<script>` blocks.** Run page-wide it treated body prose as code: QD3's `GET /_board/asset/*` glob read as a `/*` comment-opener, and the span to the next `*/` (inside QE3) was silently dropped the moment CJK landed in between — five slides (QD4–QE2) gone. build.py's no-JS invariant caught it; body prose is now never scrubbed.

## [0.12.0] — 2026-07-24

**ascii inside an item's fold (JL: "for each item's hidden text, add the ascii").** An INDENTED ` ``` ` fence in an item's explanation lines is collected into that item's hidden text (dedented, rendered as `<pre class="ip">`), instead of flushing the item and landing as a sibling block. Column-0 fences keep the old sibling behaviour, so the face stays title-only and the diagram lives behind the click — the QA4 item shape (heading + summary + prose) is unchanged, the ascii just joins it. This deliberately revisits the 1705 ascii-in-item experiment that 0.11-era reverted: that revert traded ascii away to get the QA4 shape; now both hold at once. First user: the CMS board's QC10 (AMI → CABG), all 6 items. CSS: `.bd pre.ip` one size down, horizontal scroll of its own. Regression: boardform board (28 questions) rebuilds unchanged.

## [0.11.0] — 2026-07-24

**A board can sit on an existing tree (QC3), show other files' content live (QF1), and the Python got its src/ split (QB5).** All three driven by the first board laid directly over a paper's `0-lifecycle/`.

- **folder questions (QC3, JL ruling).** A question is a `Q*.md` at ANY depth under the board folder: `q_files()` discovery (rglob, skipping path segments starting `_`/`.` and `fig/`), Pages keeps bare filenames, duplicate basenames warn and keep the first, the page's data-file carries the board-relative posix path, serve.py vets it (`vet_qpath`: no absolute, no `..`, basename must look like a Q file), archiving flattens into the board's `_archive/`, watch.py watches the whole tree. Flat boards untouched (regression: unchanged question set).
- **embeds (QF1, JL: "can a markdown file incorporate another file?").** `![[path]]` / `![[path#Section]]` on its own line pulls another file's content into the slide at build time, by reference — zero copy, zero drift, zero dialect knowledge. `src/page_stage.py` renders generically (atx AND setext headings, fences, lists, quotes, `|` record lines) under a "live from source" header; every failure mode (missing file, non-md/txt, heading not found) is a visible warning box, never a silent gap; no recursive expansion. Comments on embedded text keep living in the FACE's `## Comments` and re-anchor against the re-rendered embed at rebuild. Still open on the board: the paper-side anchors handshake (haipipe-paper-stage contracts).
- **src/ split (QB5, JL named the page modules).** build.py 995 → 70 lines, code moved VERBATIM to `src/{common,parse,body,page_board,page_question,page_stage}.py`; serve.py imports `QNAME`/`vet_qpath`/`q_files` from `src/common.py` instead of duplicating. Byte-identical proven on board.html AND `--json` BEFORE any feature landed.
- **bugfix, found by the byte-identical gate:** the old single-function `render()` reused `lab`, so any question WITH comments wore the comments count in its state pill (`✅ 💬 Comments (0 open / 7) …`) instead of its state label. Reproduced first to prove the move pure, then fixed (`cm_lab` in `src/page_question.py`).
- **doc slides (QF2, JL: "no need to generate QB3-claims.md").** A Pages line `doc: <path> <path>…` renders the listed source files DIRECTLY as one slide (id = first file's stem, title = its own `#`/setext title) — no Q wrapper at all. Doc slides are views, not questions: no state pill, no Items counting, no comment target, excluded from the settled count and the bar. Files are explicit, so `_LOG_*.md` can be shown even though `_` paths are excluded from Q discovery.
- First consumer: `examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle/` — 14 ruling Q slides + 8 doc slides after JL's scope ruling ("I think 14 ruling faces"): every stage renders straight from its own docs (0-seed, 1a-resource, 1b-claims, 2a-venue, 2b-pitch, 3-narrative, 4-display + _DISPLAY_REQUEST, z-structure), while QA1 + QD2..QD8 + QE2..QE7 keep Q files, live embeds, and comment write-back (verified over HTTP on 5599). The settled bar counts the 14 rulings only.

## [0.10.0] — 2026-07-24

**The index becomes editable (QC2, JL): groups introduce themselves, and the board's structure is writable from the page.**

- New Pages grammar: plain lines between a `### ` group heading and its first `.md` entry are the GROUP INTRO. Line 1 renders as an always-visible sentence under the group header; further lines become the click-to-expand "what this group is for, why it is here" body. Rendered as a native `<details>`, so strip-scripts still leaves the whole board readable; `parse_dir` collects intros into `meta["groups"]` and the `--json` path carries them for free.
- One structure writer: `structure_op()` in serve.py behind `POST /_board/structure`, imported by the console's boards_api (QE3: one writer set, never reimplemented). Ops: `add_group` (letter auto-picked, optional hook/body intro), `add_question` (seeds a stub Q file in the house shape, numbers past the group's max, lists it at the group's tail), `archive_question` (logs the move in the Q's `## Log`, moves the file to `_archive/` inside the board, drops the pages line; NEVER deletes), `archive_group` (refuses while the group lists any question).
- Page controls (board.js/css): ＋Q on each group header, ＋Group at the index tail, hover 🗄 on rows and headers with a two-click "sure?" confirm and an inline mini form (no native dialogs). Wired into `__boardRewire`, so they survive QD6's in-place swaps; after each op the server rebuilds and the watcher refreshes the page under you.
- Index rows carry `data-f` (their file name) and group headers carry `data-g`, so the page controls address md reality instead of guessing from display text.
- Verified: a full add→archive round trip leaves board.md byte-identical; refusal paths (non-empty group, unknown op, taken letter) exercised over HTTP on 5599 and through the console relay on 8093; the boardform board's five groups now carry real intros (moved out of `## Pipeline`, which keeps only the overall narrative, so nothing is said twice).

## [0.9.2] — 2026-07-24

**The terminal self-heals, and its columns stop lying.** JL's screenshot (QD3's Lesson) showed reconnect banners knocking six times on a terminal that had been RELEASED — reconnecting cannot revive a dead ttyd — over a TUI mangled by drifting column math.

- after 2 failed reconnects the drawer now respawns the terminal through `/_board/term` (`--resume` restores the session) instead of knocking to 6 and giving up.
- `fitTerm` reads xterm's real rendered cell size (fallback to the old constants) and refits 350ms after connect — the pty and the pane agree on width, claude repaints clean.

## [0.9.1] — 2026-07-24

**No button closes the chatbot anymore.** JL clicked the drawer's "↻ Reload to see the result" and lost the drawer — that button predated live refresh and did a hard `location.reload()`, which tears down everything the scripts built. All four reload sites (the drawer's post-write button, the drawer's ↻, the dock panel's ↻, the discussion-add success) now call `window.__boardRefresh` — the QD6 in-place swap, run immediately — so content updates under you and the drawer stays open mid-conversation. Labels renamed to "↻ Refresh in place" / "↻ Refresh". First edit made directly in `assets/board.js` since the QB4 split — checked with `node --check` on the real file.

## [0.9.0] — 2026-07-24

**Live refresh, an honest wait line, and the QB4 split.** Three JL asks in one afternoon of drawer-testing.

- **live in-place refresh (QD6).** "When the chat changed something, refresh automatically — and my chat interface is still there." The page HEAD-polls its own URL every 4s (both servers send Last-Modified; the console's page route gained HEAD) and, on change, swaps ONLY `div.wrap`: content updates under you, scroll restored, "↻ board updated" toast, held while text is selected. The chat drawer (mid-stream included), terminal, and comment dock hang off `<body>` and never notice. No Node, no reload, drawer survives — that requirement decided the design.
- **the wait line tells the truth (QD2).** serve.py emits `stage` events ("booting claude — the full tier loads the whole skill registry…", "session up — sending your message") so the drawer shows real progress instead of a static "…thinking"; the collapsed thinking block is labeled `💭 Thinking (N chars — click to reopen)`. Verified along the way: resumed sessions DO stream thinking now (the explicit `thinking={enabled}` option cured yesterday's loose end ②).
- **build.py split into assets (QB4).** 2,488 → 850 lines: the page's JS and CSS now live as REAL files — `assets/board.js` (1,173 lines, `node --check`s in place) and `assets/board.css` (465 lines) — read and inlined at build, output still ONE self-contained board.html. Byte-identical proven on a frozen board (split vs. mechanically re-joined build), a proof that caught two wrapper-newline slips before they shipped. The grammar's home stays the skill; `haichat-board/` keeps importing it.

## [0.8.0] — 2026-07-24

**The gate shows the change (duplicating the VS Code extension, step 1).** JL: "what is the backend of the vscode claude plugin? I want to duplicate it." The backend is the `claude` binary over the stream-JSON agent protocol — exactly what the drawer already drives through `claude_agent_sdk`; the visible delta was the gate.

- serve.py's permission ask events now carry `detail`: Edit → old/new strings; Write → the file's current content vs. the proposed; MultiEdit → per-edit pairs (capped at 6); Bash → the command. Truncated (4k/edit) — a gate preview, not a diff viewer.
- the drawer renders it: − red blocks, + green blocks, commands verbatim, above Allow once / Always / Deny. Strip-scripts invariant unaffected (the gate only exists in the live layer).
- honest status: emitted JS node-checked; a live gate-pop E2E is still owed (full-tier boots load the ~150-skill registry and outran the test window).
- next duplication step (QD2 ④): one persistent claude process per session, like the extension — also the cure for those slow boots.

## [0.7.1] — 2026-07-24

**`## Files` links actually open.** JL clicked `cms_production.do` on the CMS board and nothing usable happened — the link machinery (`resolve()`'s walk-up + `## Links`) was fine; the serving side wasn't.

- `EXT` widened: `.do .R .sql .tex .bib .toml .csv .tsv .ps1 .log` now count as path-like, so backticked references to them resolve (existence-checked, as always).
- `serve.py` serves source-ish suffixes as `text/plain` — they display in the browser instead of downloading (default mimetypes made `.do` an octet-stream).
- The first consumer moved: `boards_api.py` now lives in HAIChat-SPACE's **`haichat-board/`** sibling project (own service on 8094; `haichat-inlab` imports the same router). Its page serving widened to any existing file under the space root, read-only, matching serve.py — that is what makes a `## Files` click work in the console.

## [0.7.0] — 2026-07-24

**English output + the parser as a service.** JL: "put all the things in English, no Chinese anymore — in the board html or markdown."

- **the emitted page is fully English.** All user-visible chrome strings in `build.py` translated (index labels, tooltips, comment badges, the CLI summary line); `<html lang="en">`; comment quotes render as `“…”`. New `scrub_cjk_comments()` drops CJK-bearing CSS/JS comments from the **emitted** page only — the source keeps its comments for developers; the build asserts the page still reads with scripts stripped, as before.
- **comment grammar widened to curly quotes.** `CM_HEAD` (build.py) and `resolve` (serve.py) accept `“…”` alongside `「…」`/`"…"`, and `serve.py`'s writer now writes `“…”`. Found the hard way: an English board written with curly quotes parsed to zero comments — they silently vanished from the page (~19k chars of body reappeared after the fix).
- **`build.py <dir> --json`** — the parser half exposed as a service (the boardform board's QE3: one grammar, two render paths). Emits meta + per-question `{state, owner, done/total, comments_open/total, sections}` from the same code the HTML is built from, so JSON and HTML cannot disagree (asserted in the consumer's tests).
- **first external consumer: `haichat-inlab`'s `boards_api.py`** (HAIChat-SPACE, branch `feat/haichat-board`) imports `build.py`/`serve.py` from this skill dir — SPACE mounting, board discovery, page serving, and the comment/discuss/resolve write-backs, none of it re-implemented. Design record: the boardform board's QE2/QE3.
- **terminal smoothness (QD3 ①–④):** the drawer terminal now auto-reconnects with backoff (the xterm survives, scrollback intact; the post-auth resize makes claude repaint), sends a same-size resize op every 30s as keepalive, refits via ResizeObserver when the pane resizes, and pre-warms the xterm assets on ⌨ hover (assets only — never `POST /_board/term`, which takes HOLD).
- the skill's own board (`diagram/01-boardform-260722/`, 23 questions) fully translated to English — body, JL quotes, comments, logs.

## [0.6.0] — 2026-07-23

**The question page was reordered so a stranger can read it.** JL: "currently it is very very hard for a fresh eye to understand." The diagnosis was ordering, not wording — the page gave you *what we did* before *what we're deciding and why*.

- **on-stage order is now fixed: intent first, state second.** `Question → Boundary → Diagram → Items to Finish → Where we are → Files`. Previously `Now` sat above `Done when`, so a reader hit a wall of implementation detail before learning the goal, and `Why here` — the single most orienting paragraph — was buried fifth.
- **`## Question` became a lede plus bullets.** It renders through `body()` now: the first paragraph is the 21px lede, and 2–4 bullets carry *why it's hard / what breaks if we don't decide / what it affects downstream*. The acceptance bar is stated in QA4's `## Law`: **read this one section and a zero-context reader knows what the question is.**
- **new `## Boundary` section** (`.bnd`, grey rule) — what the question covers and, more importantly, what it does **not**, naming the question that owns the excluded part. Without it readers bring another question's expectations to this one. Optional but strongly recommended.
- **new `## Files` section** (`.fls`, blue rule, last on stage) — which files this question touches, and what each one's role is. Read the question, then know where to go; change a file, then know which question to write back to. Paths in backticks become clickable through `board.md`'s `## Links`. Optional but strongly recommended.
- **`## Done when` → `## Items to Finish`, `## Now` → `## Where we are`.** Plainer names for a fresh reader.
- **`## Why here` retired** — its job moved into `## Question`'s bullets. Boards that still carry the section parse fine; it renders in the bottom folds, so no content is lost.
- **no board breaks.** `ALIAS` now maps one slot to many names, so `Done when`/`Items to Finish`, `Now`/`Where we are` and the old Chinese names all resolve. Every existing question file rebuilt untouched.
- **QA2 and QA4 reopened (`✅ → 🟡`).** The layout and the template were both settled under the old structure — this change invalidates them. QA4 carries the new `## Law` and a `## Lesson` worth keeping: *it was closed ✅ that same morning and reopened by one sentence from JL, because the finish line never included "a stranger can read it."* Every one of the board's questions was then converted to the new shape — Question as lede-plus-bullets, plus `## Boundary` and `## Files`, with `## Why here` folded in and removed (18/18, verified against the *rendered* page rather than the markdown, because a substring check gets fooled by headings that appear inside ascii fences — QA2 lost a whole section to exactly that). Still owed: the fresh-agent cold read.

## [0.5.0] — 2026-07-23

- 新增 **view** 动作：「打开 <板文件夹>」= 看已有的板，不是开新板。
  之前只有 open（开新板），第 5 步还只写「打开 board.html 给用户看」而没给命令，
  新 agent 会去跑 `open board.html` —— 那是在**服务器**桌面上开，用户（Remote-SSH，
  浏览器在自己笔记本上）什么都看不到。现在写明唯一有效的方式：
  通过 VS Code IPC socket + `browser.sh` 把 `http://127.0.0.1:5599/<板>/board.html` 推过去。
- frontmatter 的 description 补上「打开这块板」触发词，并写明 view ≠ open、禁用 `open`/`file://`。
- open 第 6 步改成「按 view 那节推到用户的 VS Code 浏览器」。
- 清掉写死的「14 题」（板的题数会变，写死必过期）。

## [0.4.3] — 2026-07-23

A compose box in every question's Discussion — write a thought in bulk, it lands in `## Discussion`.

- **`## Discussion` gets a textarea.** Inside each question's Discussion fold there is now a box + signer dropdown + "➕ Add to discussion". Type a thought — a whole block, *not* pinned to a sentence the way a comment is — pick a signer, press Add: serve.py appends it as `> WHO: …` to that question's `## Discussion` and rebuilds; a reload shows it. Reuses the existing write path (new `/_board/discuss`, sibling of `/_board/comment`) and is fence-aware like the comment fix, so it never lands in a `## Discussion` line shown inside a code example. With serve.py not running the button says to hand-write it instead. The box is inert static HTML without the script, so the invariant (strip every `<script>`, the prose survives) still holds. Decided the simple way (JL): into `## Discussion`, not a new section — reuses the free-form thread that already exists.

## [0.4.2] — 2026-07-23

A third level of hierarchy inside a section — the **group topic** — plus the comment-writer bug that surfaced it.

- **a whole-line-bold `**…**` becomes a group topic.** A line that is entirely bold is no longer just a bold paragraph; it renders as a 🔹-marked, slightly-larger heading that leads a cluster of items — sitting between the section heading (`.ch`, underlined, 📍/🎯/💡) and the item names (`.bt`, `▸`). Three visible levels now: 📍 section ＞ 🔹 group ＞ ▸ item. The 🔹 is the default marker; write an emoji at the start of the bold line (`**🎨 …**`) and it becomes the marker instead — the icon is *authored*, never guessed by the generator (build.py has no LLM, and guessing an emoji from keywords is exactly the kind of machine-guess the writing rules forbid). Mixed-bold lines (`**a** b`) are untouched — only fully-bold lines convert. Documented across `ref/q-template.md` (the `## Now` example), `ref/board-form.md` §5 (syntax table) and §8 (on-stage hierarchy). QA4 asked for it — recorded through the board's own comment layer.
- **the Question block shows its name.** Every other section renders a label (📍 Now, 🎯 Done when, 💡 Why here); the question line carried only a bare `❓`. It now has a small `❓ Question` eyebrow (`.ql`, accent, above the question text), matching the rest. QA4's remaining open comment asked for exactly this — resolved and re-anchored on close (the `❓` moved into the label, so the quote moved to the question text).
- **serve.py no longer writes comments into fenced examples.** `add_comment` matched the *first* `## Comments` heading in the file — including the one inside QA4's `md 段落→页面位置` code fence — so a comment on that slide landed in the example, not the real section. It now skips ``` fences when locating `## Comments` / `## Log`. The stray comment was moved back to QA4's real `## Comments`. (A running serve.py must be restarted to pick this up.)

## [0.4.1] — 2026-07-23

Doc-consistency pass out of the first fresh-agent acceptance read (the QB2 known-gap): a new agent, given only `SKILL.md` + `ref/`, opened a real board, built it, and the build.py-invocation drift it hit got fixed across the ref spec. `SKILL.md`'s open/build sections had already been corrected; `ref/board-form.md` had been left stale — exactly the cross-file drift this skill warns about.

- **`ref/board-form.md` synced to the `<skill>/build.py` call.** §7 still showed the bare `python3 build.py <folder>`, which fails if you `cd` into the board folder (the script lives in the skill dir, not the board). It now reads `python3 <skill>/build.py <board 文件夹>` with the same "don't cd in" note the SKILL.md open/build sections carry. The last bare shorthand in SKILL.md's `sync` section was corrected too.
- **`ref/board-form.md` §2 gains the slug + default-state rules.** `-<slug>` is short lowercase English, parser-ignored; a freshly-opened Q is always `state: 🔴 OPEN`. Both were in SKILL.md's open steps but missing from the "full spec".
- **`ref/board-form.md` §3 marks board.md's required vs optional sections.** The Q-file spec (§4) already listed 必填/选填; board.md did not — `## Topic` / `## Pipeline` / `## Pages` required, `source:` / `## Links` optional, now stated.
- **known-gap surfaced, not folded in.** The acceptance read hit a question the current model has no home for — where a note that is off the board's `spine` but worth keeping should go (not ⏸️ ON HOLD, which is on-topic-deferred; not a forced Q). Drafted as a question for the skill's own board; left off SKILL.md per the graduation rule (undecided stays out of the manual). Distinct from the existing `QB3` (migrate the two older boards).

## [0.4.0] — 2026-07-23

The single-Q slide layout (QA4) is settled and closed. The focus-mode slide got the polish that finally answered its last open fork — *what belongs on stage vs. folded* — and the rule graduated into the spec.

- **section headings gain a line + an `expand all`.** Each of 📍 Now / 🎯 Done when / 💡 Why here now has an underline and, when it holds collapsible items, a right-aligned `expand all` that opens/collapses every item and code block in that section at once. Pure enhancement (`.secall` + a delegated click handler): strip the script and each item is still individually openable, all text stays in the DOM.
- **code blocks fold by default.** A ```` ``` ```` block in the prose renders as a one-line `</> code · N 行` disclosure, revealed on click or via `expand all`; `## Diagram` (the headline picture) is the one that stays open (`body(txt, fold_code=False)`). So a slide's first glance is a clean column of item names + the diagram, not walls of code.
- **the big title copies with a space.** `<span class="hid">QA4 </span>…` — the id and title were glued on copy (`QA4Single…`) because the gap was CSS `margin`, not a character; a real space now sits inside the badge so the heading copies as `QA4 Single-Q slide layout`.
- **QA4's `## Law` graduated into `ref/board-form.md §8`**, not SKILL.md — display spec stays in the spec doc, keeping SKILL.md lean (QB1's rule). The on-stage/folded rule, up-down `Now`/`Done when` stacking, long-Q scrolling (no truncate/split), no-16:9-lock, and the copyable-title note all live there now. Graduated list: `QA2 · QA4 · QA6 · QC1`.

## [0.3.0] — 2026-07-23

The graduation mechanism — SKILL.md is now defined as the board's settled questions, distilled. Plus the live layer (serve.py) gets a foothold in the manual.

- **板 ↔ SKILL.md, written down.** New SKILL.md section: this file is the crystallisation of the skill's own board (`diagram/01-boardform-260722/`). A question that reaches `✅ SETTLED` graduates its `## Law` into SKILL.md; questions still `🟡/🔴` do NOT enter the manual — so a "just-decided" rule never gets written as iron law (QD1's permission rule was written hard, then overturned — the cautionary case). SKILL.md is therefore always *the sum of settled rulings, no more*. The rule lives in QB1's `## Law`.
- **serve.py enters the manual.** New `serve` action: one server serves the whole repo root (`serve.py --root <root>`), giving every board live commenting-to-disk plus chat/terminal per question. The old `comment` text ("stage in localStorage → Sync to md") was stale — QA6 shipped Save-immediately-writes-to-disk; the section now says so, with the browser Sync/Copy path demoted to the serve.py-not-running fallback.
- **chat / terminal held as provisional.** The QD group (drawer via claude_agent_sdk, terminal via ttyd) is real and running but still `🟡` — SKILL.md carries only a pointer to it, not rules, per the graduation mechanism.
- **actions regrouped** — offline (`open · add · build · sync · link · close`, needs only build.py) vs live (`serve · comment`, needs serve.py).

## [0.2.0] — 2026-07-23

`SKILL.md` written. Comments become first-class. The zero-script promise is restated as what it actually protects.

- **`SKILL.md` + three `ref/` files** — the skill is now readable by someone who was not in the room: `ref/q-template.md` (copy this to add a question), `ref/board-form.md` (full spec: folder, numbering, section↔page map, syntax table), `ref/writing-rules.md` (how to write it so people understand, plus the cold-read prompt and its convergence test). `ref/board-example.md` was replaced — it still held the pre-0.1 single-file `[BOARD]`/`[Qn]` form.
- **`## Comments`** — inline comments pinned to a sentence, each with its own state: `- [ ] JL 「quoted sentence」 · 260723 1100` plus an indented body; `[x]` marks it solved. Open comments highlight their sentence in the prose and force the fold open; solved ones grey out and strike through. A quote that no longer matches the prose is flagged **⚠ anchor lost** on the item and in the fold label — a comment can never silently detach. `## Discussion` stays as the free-form thread.
- **in-page commenting** — select a sentence, press 💬, write, Save. Comments stage in `localStorage` and go to the md in one shot via "Sync to md" (File System Access API) or "Copy". Any 1–4 letter initials work, not just the original defaults; new names are added from the dropdown and remembered, and each gets a stable colour.
- **`watch.py`** — rebuilds on any `.md` change, so "Sync to md" → refresh is a closed loop with no Claude Code in it.
- **topic/explanation bullets** — `- heading` plus indented lines renders as a bolded lead with its explanation underneath; `## Done when` items take the same shape. Long passages stop being walls of sentences.
- **`## Log` takes a time** — `260723 1030 · what changed`; the time is optional.
- **titles are phrases, ≤14 chars** — the full question belongs in `## Question`. The board's own ten titles went from 43 chars at worst down to 8–15.
- **the invariant replaced the rule.** 0.1.0 asserted "zero `<script>` in the output". That became false the moment commenting shipped, and it was never the real guarantee anyway. What is asserted now: **strip every `<script>` and each question plus the full prose is still there** (checked on every build). Scripts may only enhance.

Known gaps (tracked on the board at `0_utils/diagram/01-boardform-260722/`): "Sync to md" has never been run end to end (QA6), no fresh-agent acceptance run (QB2), the two older boards are not migrated (QB3), and comments already written into md have no check for a broken anchor after the prose is edited.

## [0.1.0] — 2026-07-22

First working version. Board = a folder; `build.py` turns it into one static page.

- **board form** — `<unit>/diagram/<NN>-<topic>-<YYMMDD>/` holds `board.md` (title · `spine:` · `close:` · `## Topic` · `## Pipeline` · `## Pages`) plus one `Q<A><n>-<slug>.md` per question, plus generated `board.html` and `fig/`.
- **binding is by PATH** — every `Q*.md` in the folder is on the board; `## Pages` only sets order and grouping. An unlisted file still renders (under ⚠️) and warns on stderr — a missed pages entry can never drop a question.
- **Q file sections in English** — `## Question / Diagram / Done when / Now / Why here / Glossary / Discussion / Log`. Chinese section names still parse, so older boards build unchanged.
- **`## Done when` is a checklist** — `- [ ]` / `- [x]`, with an auto count (`3/5`) in the panel header.
- **`## Diagram`** — a fenced ASCII diagram per question, readable in the md and rendered as-is in the page.
- **`## Log`** — dated one-line history per question (`260722 · what changed`).
- **state labels** — `✅ SETTLED / 🟡 PARTIAL / 🔴 OPEN / ⏸️ ON HOLD`.
- **zero `<script>` in the output, asserted at build time.** Every question is a real `<section>`; collapsibles are native `<details>`; navigation is plain anchors. The page cannot render blank.
- **focus mode is pure CSS** — `:target` + `:has()` show one question full-screen, unbounded (no card border/radius/fill), 38px title, prev/next/index links. Same file serves both reading and projecting; there is no separate `deck.html`.

Known gaps (tracked on the board at `0_utils/diagram/01-boardform-260722/`): `SKILL.md` is not written (QB1), no fresh-agent acceptance run (QB2), the two older boards are not migrated (QB3), inline comments are half-built (QA6 — the md syntax parses, the CSS does not exist yet).
