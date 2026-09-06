# Board operations

Read only the section for the operation being performed. `SKILL.md` owns
routing and invariants; `board-form.md` owns source shape.

## Preview without writing

```bash
python3 <skill>/cli/preview.py <board-or-page-path>
```

A Board preview prints its orientation and Page roster. A Group preview prints
its Pages. A Page preview follows the `haipipe-page` contract. Preview is a
gist, not a substitute for reading the source before an edit.

## View an existing Board

“Open `<existing-board-folder>`” means VIEW, not create.

1. Resolve the repository root and Board folder.
2. Read `board.md`, its parent owner, and applicable SPACE configuration.
3. Rebuild the site.
4. Open the Board's HTTP URL, never a `file://` URL.
5. Report Page counts, unresolved work, and the current blocking Page.

```bash
python3 <skill>/cli/build.py <board-folder>
```

The reader-facing base URL resolves in this order:

1. explicit command value;
2. `JJLUO_PUBLIC_URL` or `JJLUO_TAILSCALE_URL` from the repository's
   `.server_config/settings.env`;
3. `HAIPIPE_BOARD_URL` from the current environment or repository `env.sh`;
4. `http://127.0.0.1:5599`.

Never print `.server_config/settings.env` or `env.sh` credentials.

## Create a Board

Before writing, obtain explicit agreement on:

- `spine`: the one problem the Board organizes;
- `close`: the observable closing condition;
- initial Page list and grouping.

Then:

1. choose the owning unit and Board location;
2. write `board.md` using `board-form.md`;
3. create Q/S Pages from `page-template.md`, or use the owning generator for a
   generated Page kind;
4. register presentation order in `## Pages`;
5. build, check, and inspect the rendered Board.

A Task Block is not synthesized from Q/S templates. Add `board-kind:
task-block` to the Block's `board.md`; its existing Job/Task tree supplies
membership.

## Add or archive structure

The live structure route and direct source edits must produce the same grammar.

- Add a Group by appending one `### Q<id> · <title>` block to `## Pages`.
- Add a Q Page inside its Group folder and list its filename under that Group.
- Archive a Page by moving it under `_archive/` and removing its Pages row.
- Archive a Group only after it contains no active Page rows.

Archive history is written to the Page's
`outline/<stem>-log.md`, never to a Page-level `## Log`.

## Build and check

```bash
python3 <skill>/cli/build.py <board-folder>
python3 <skill>/cli/check.py <board-folder> --summary
python3 <skill>/cli/check.py <board-folder> --strict
python3 <skill>/cli/check.py --rules
```

`build.py` writes only the derived `board/` tree. `watch.py` rebuilds after
Markdown changes:

```bash
python3 <skill>/cli/watch.py <board-folder>
```

Changes to Python, CSS, JavaScript, templates, or assets require an explicit
build and the appropriate regression tests.

## Serve the repository

One server serves the repository root and all Boards beneath it:

```bash
.venv/bin/python <skill>/cli/serve.py --root <repo-root>
```

`serve.py` requires the project environment when live Chat dependencies are
used. Build and check use system Python. A non-loopback listener requires
authentication unless the user explicitly chooses a trusted private-network
exception. The terminal endpoint is a real shell; never expose it casually.

The live layer may write comments, edits, structure, Chat sessions, drawings,
and supported plugin records back to source. A write is complete only after
the Markdown lands and the Board rebuilds.

## Move Group and Page folders

Run migrations as dry runs first:

```bash
python3 <skill>/cli/regroup.py <board-folder>
python3 <skill>/cli/regroup.py <board-folder> --apply
python3 <skill>/cli/refold.py <board-folder>
python3 <skill>/cli/refold.py <board-folder> --apply
```

`regroup` places root Pages into ordered Group folders. `refold` gives each
Page its own Folder and moves Page-owned plugin material with it. Do not apply
either operation to an already-canonical subject tree merely to make it look
like a design Board. Always run `check.py` after moving because real paths in
`## Links` may require rebasing.

## Operate one Page

Route Page creation, editing, checking, or lifecycle execution to
`haipipe-page`. The current lifecycle is:

```text
00 CONTEXT   PREPARE
01 OUTLINE   SHAPE · SURVEY
02 EVIDENCE  LAND · EMBED
03 CONTENT   WRITE
04 CHECK     CHECK
```

The lifecycle may repeat or route backward. It is not an automatic advance
through five steps. The deterministic runner lives in
`ref/page-lifecycle.workflow.js`; normative packet and receipt law lives in
`haipipe-page-workflow/ref/page-run-contract.md`.

## Write back and close

After substantive work:

1. update the owning source;
2. update affected Aim ticks and `Now:` facts;
3. append the reason to `outline/<stem>-log.md`;
4. rebuild and check;
5. inspect the rendered result.

Close only after every Page is ✅ or explicitly ⏸️ and the Board's `close:`
statement is true. A Task Block additionally requires each Task's executable
P-B-E-R path and current `READING` gate to be closed.

## Keep the session attached

For a direct Board session, generate the reply footer from disk:

```bash
python3 <skill>/status.py <board-folder> \
  --focus <board|group:ID|PAGE_ID> \
  --mode <discussion|sourcing|implementation|review|status> \
  --status <ready|working|blocked|done> \
  --next "<one concrete next action>"
```

Do not hand-compose or cache a shared status file.
