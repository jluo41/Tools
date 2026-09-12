# Standalone Page workspace

## Choose the entry

| User supplies | Action |
|---|---|
| Ordinary Markdown, text, HTML, code or binary file | `init --file INPUT --dest FOLDER` |
| Existing Page Face with Opening/Content/Aims | `inspect`, `build` or `serve` it in place |
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
python3 <page-engine>/cli/page.py inspect /absolute/my-page
python3 <page-engine>/cli/page.py build /absolute/my-page
python3 <page-engine>/cli/page.py serve /absolute/my-page --host <configured-host> --port <available-port> --public-url <configured-origin>
```

Use `PAGE_SERVER_TOKEN` for a remotely reachable writable server. Do not put a
real token into command history, logs, or the reply. The server supports a
login URL/session cookie. A read-only site can use `--read-only`; this does not
make private content appropriate for public publishing. Respect repository
hosting policy; in Physician-SPACE use the configured Tailscale origin, not a
reader-facing loopback link. Verify the exact public URL before sharing it.
Do not occupy an existing server port or replace an unrelated listener.

## One Folder and one content authority

```text
my-page/
  page.toml                          portable registration, no absolute paths
  my-page.md                         Page Face / Opening / Content / Aims
  outline/evidence/materials/
    input.html                       editable imported copy, original bytes
    assets/...                       copied static local dependencies
  delivery/web/                      generated static reading export
```

`page.toml` version 1 declares `source`, optional `content`, `title`, and the
original input hash. Its `content` must match the Face's `source-content:`.
The Page renderer inserts that content directly: no duplicated editable prose.
For an imported HTML file, edit HTML/CSS/JS under materials; edit the Face for
Opening/Aims. HTML is displayed in an opaque-origin sandboxed iframe.
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

The Source workspace edits UTF-8 files up to 2 MiB. Save includes the loaded
SHA-256 hash; stale writes fail without replacing either version. The browser
keeps unsaved text on conflict. Reopen/reconcile the source before retrying;
never force-overwrite to make a test pass. Hidden files, external symlinks and
runtime/private lanes are not web-editable. Registration is edited on disk.

## Read site versus working site

| Surface | Capability |
|---|---|
| `build` → `delivery/web/index.html` | Static reading export and imported assets; no write-back |
| `serve` → Page | Live source; category-plugin pane for Outline, Runs, Delivery and Folder; Source editor only on writable hosts |
| Board | Groups, membership, navigation and aggregate build over the same Face |

No Board is required for these Page operations. The independent server keeps
the existing `/_board/*` plugin route names as compatibility endpoint names
only; it resolves its single Page directly. Evidence remains inside Outline
rather than becoming a second picker row. Those names do not imply
that `board.md`, a Board registry or a Board Python package is needed.
Board-only agent/terminal and external evidence-producer actions are not
standalone server capabilities. Do not report an unavailable action as done.

## Check and hand off

Use `page-checklist.md` to distinguish configuration readiness from substantive
Opening/Outline/Content/Aims completion. An imported scaffold or successful
build must not be reported as content acceptance or a hosted site.

1. Read the supplied file and identify its dependencies and any sensitive data.
2. Create or reuse the Page Folder; compare imported bytes with the original.
3. Build; inspect the actual rendered Page, not only exit status. For HTML,
   inspect its embedded source and asset requests too.
4. If editing was requested, save a scoped change and re-read the exact source;
   verify that the original is unchanged and the rendered Page reflects it.
5. If hosting was requested, start/reuse an authorized listener and verify the
   actual configured reader URL. Report static export versus live editing
   explicitly. A build without a listener is not a hosted site.
6. Return the Page Folder/source link and the verified working/reading URL when
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
