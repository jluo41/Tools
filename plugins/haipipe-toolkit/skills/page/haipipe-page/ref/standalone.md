# Standalone Page workspace

## Choose the entry

| User supplies | Action |
|---|---|
| Markdown that should become a working Page | `setup INPUT [--dest FOLDER]` |
| Technical-only Markdown, text, HTML, code or binary intake | `init --file INPUT --dest FOLDER` |
| Existing Page Face with Opening/Content | `inspect`, `build` or `serve` it in place |
| Page Folder with `page.toml` or same-stem Page Face | Open the Folder; do not create a nested Folder |
| Board membership request | Use Board to register this same source, after Page creation |

Resolve the skill location first. Commands below use `<page-engine>` for
`<toolkit>/skills/page/haipipe-page`; Python 3.11+ is required. Runtime creation,
rendering and serving need only the standard library, not a Board checkout.
Check the interpreter with `python3 --version` before invoking the CLI;
macOS's system Python may be older. Choose an installed Python 3.11+ (this
workspace's `.venv/bin/python` qualifies), rather than installing dependencies
or changing the project environment unnecessarily.

```bash
python3 <page-engine>/cli/page.py init --file /absolute/input.html --dest /absolute/my-page
python3 <page-engine>/cli/page.py setup /absolute/input.md [--dest /absolute/my-page]
python3 <page-engine>/cli/page.py setup /absolute/existing-page
python3 <page-engine>/cli/page.py inspect /absolute/my-page
python3 <page-engine>/cli/page.py build /absolute/my-page
python3 <page-engine>/cli/page.py serve /absolute/my-page --host <configured-host> --port <available-port> --public-url <configured-origin>
```

Use `PAGE_SERVER_TOKEN` for a remotely reachable server with plugin writes enabled. Do not put a
real token into command history, logs, or the reply. The server supports a
login URL/session cookie. Add `--read-only` to disable plugin writes too; this does
not make private content appropriate for public publishing. Respect repository
hosting policy; in Physician-SPACE use the configured Tailscale origin, not a
reader-facing loopback link. Verify the exact public URL before sharing it.
Do not occupy an existing server port or replace an unrelated listener.

## One Folder and one content authority

```text
my-page/
  page.toml                          portable registration, no absolute paths
  my-page.md                         Page Face / Opening / Content
  outline/evidence/materials/
    input.html                       editable imported copy, original bytes
    assets/...                       copied static local dependencies
  delivery/web/                      generated static reading export
```

`page.toml` version 1 declares `source`, optional `content`, `title`, and the
original input hash. Its `content` must match the Face's `source-content:`.
The Page renderer inserts that content directly: no duplicated editable prose.
For an imported HTML file, edit HTML/CSS/JS under materials; edit the Face for
Opening/Content. Requirements and targets stay in backstage records. HTML is
displayed in an opaque-origin sandboxed iframe.
The HTML `<title>`, its visible `<h1>`, and the outer Page title are distinct:
change only the field the user requested. `--title` names the outer Page.
No arbitrary uploaded code is executed by the server. Binary files remain
downloadable assets; they are not silently OCRed or converted.

`init` refuses an existing destination, validates dependencies before creating
anything, and copies rather than moves the original. It recognizes static
Markdown links/images, HTML src/href/srcset, and CSS url/import references
contained beneath the input file's directory. Missing, root-relative, hidden,
or escaping dependencies stop the import. Network resources are not fetched;
they remain network-dependent. JavaScript-discovered imports, runtime fetches,
servers, bundlers and SPA routing are not packaged automatically. Say so when
the input relies on those. This is a static-file Page workspace, not a general
application deployment system.

`setup` accepts imported Markdown. In one step it runs the safe import and then
populates the Page's real working records: source-specific Opening,
backstage requirements/targets,
`outline/<stem>-outline-v0.1.md`, matching reader-move
`outline/<stem>-outline-v<G>.<S>[.<E>].md` with embedded `Draft:` fields,
Context/Files projections, and a completed
`rNN_page-setup` Task Run with a Result report. The Shape is intentionally
`approved: ⬜`; automatic setup cannot impersonate human review. Its semantic
role labels and Bullet heads are a first pass that the invoking agent must
inspect and refine before presenting the Page. Setup begins with one primary
reader move per authored paragraph; its Content Draft may contain one or more
source sentences. It never creates one Bullet merely because it found one full
stop. Split a paragraph only when it contains independently removable,
contradictable, or reorderable moves. Re-running setup refuses authored records unless
`--force` is explicitly supplied after reviewing the replacement scope.
Every setup Result includes `checks.json` plus the same checklist in
`report.md`. Configuration, input preservation on intake, the reader-facing
Opening/Content, backstage Outline/Aim records, Bullet/Draft freshness, role
syntax, Bullet-head readability, static delivery, and copied assets are
blocking checks. A blocking
failure records a failed Run and makes the command fail. Semantic-role and
Bullet-only argument judgment, Aim achievement, human Shape/Content acceptance,
and unrequested hosting remain visibly
`deferred`, `untested`, or `n/a`; setup never converts them into automatic
passes. The machine audit fingerprints the checked Face, Content, Shape,
Content Draft, and static delivery. After correcting a generated role or Draft,
run `setup <existing-page-folder>` again—not only `build`—so a new setup Task
Run validates the changed records and refreshes both the delivery and audit.
The setup command already builds `delivery/web/index.html`. Do not invoke a
second build merely to make setup complete. Do not start a listener for a
static-site request; `serve` is a separate requested capability and, when used,
must run under an authorized background process manager rather than holding the
agent's foreground session open.

The Page website has no Source editor and refuses Page-source save requests.
Edit the registered Markdown and imported material on disk. The browser still
renders the current source and exposes read-only plugin projections. Draft
Scratch note autosave and Finish remain available unless the server is started with
`--read-only`; that flag disables plugin writes as well.
The Page Face has no chat launcher or comment composer; authored comments stay
readable as Notes, and copy-prompt controls remain inside the Draft/plugin
surfaces.

## Read site versus working site

| Surface | Capability |
|---|---|
| `build` → `delivery/web/index.html` | Static reading export and imported assets; no write-back |
| `serve` → Page | Read-only Page source; category-plugin pane for Outline, Runs, Delivery and Folder, plus optional domain-owned Labeling when direct `labeling/` exists; Scratch note autosave/Finish unless `--read-only` |
| Board | Groups, membership, navigation and aggregate build over the same Face |

No Board is required for these Page operations. The independent server keeps
the existing `/_board/*` plugin route names as compatibility endpoint names
only; it resolves its single Page directly. Evidence remains inside Outline
rather than becoming a second picker row. Those names do not imply
that `board.md`, a Board registry or a Board Python package is needed.
Board-only agent/terminal and external evidence-producer actions are not
standalone server capabilities. Do not report an unavailable action as done.
The optional Labeling presenter is loaded from the separate subjective-label
plugin and reads only safe receipts and `rlNN` envelopes. Its lower transport
points back to the current Codex task; it does not invent a standalone semantic
writer or expose protected corpus text through Source/static routes.

## Check and hand off

Use `page-checklist.md` to distinguish configuration readiness from the
reader-facing Opening/Content and the backstage Outline/Aims records. An
imported scaffold or successful build must not be reported as content
acceptance or a hosted site.

1. Read the supplied file and identify its dependencies and any sensitive data.
2. Create or reuse the Page Folder; use `setup` rather than `init` when the user
   expects a content-ready Markdown Page. Compare imported bytes with the original.
3. Inspect the rendered Opening/Content, then inspect generated backstage
   semantic roles, Bullet/Draft coverage, Aims, Context/Files, and setup
   Result; correct obvious semantic errors without marking Shape or Content
   accepted. Read the Bullet heads with the right-hand
   prose hidden: they must reconstruct the argument in reader order. A Bullet
   may map to several sentences when they jointly perform one move. If anything
   changed, rerun `setup <existing-page-folder>` to refresh the audit and build.
4. Inspect the actual rendered Page, not only exit status. For HTML,
   inspect its embedded source and asset requests too.
5. If editing was requested, save a scoped change and re-read the exact source;
   verify that the original is unchanged and the rendered Page reflects it.
6. If hosting was requested, start/reuse an authorized listener and verify the
   actual configured reader URL. Report live serving versus static export
   explicitly. A build without a listener is not a hosted site.
7. Return the Page Folder/source link and the verified working/reading URL when
   available. A technical import/build does not require the scholarly delivery
   packet, a PDF, a writing Run, or human acceptance; those gates apply when
   substantive Page writing or formal research delivery is requested.

For Board integration, a `page.toml` registers an arbitrary filename with
Board discovery. Add its Page Face's Board-relative path to the intended
`board.md` group and rebuild the Board. Do not copy/import it a second time.
Current Board discovery covers Pages beneath that Board's source root. It
does not register arbitrary external/sibling folders. If the Page is outside
that tree, keep it standalone and ask before any relocation or expansion of
the Board root; never silently move it or create another editable copy.
