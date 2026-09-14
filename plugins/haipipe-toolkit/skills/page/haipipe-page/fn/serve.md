---
name: haipipe-page-serve
description: >-
  Serve one self-contained Page Folder for live reading or editing. Distinguish
  live standalone Page hosting from a static build and route Board or SPACE
  hosting to haipipe-board.
argument-hint: "<page-folder> [--read-only]"
allowed-tools: Bash, Read, Grep, Glob
---

# Serve · one Page Folder

Use `/haipipe-page serve <page-folder>` when the person wants a live URL for
one existing Page Folder. This function owns the standalone Page server; it
does not create a Page, register Board membership, or replace the Page's
Markdown with generated HTML.

## Route by target

| Target supplied | Route | Result |
|---|---|---|
| One existing Page Folder | this function | Live standalone Page server |
| One Board, a project root, or a SPACE/repository root | `haipipe-board/fn/serve.md` | One Board server over the selected tree |
| A plain Markdown file that is not a Page Face | `setup` first | A Page Folder is created or resumed before serving |
| A portable reading artifact only | `build` | `delivery/web/`; no listener |

Do not pass a Board or repository root to `page.py serve`. If more than one
Page should be reachable from one server, route to the Board function even if
the person initially names only one Page inside that tree.

## Read before serving

Read the Page Face and `../ref/standalone.md`. Confirm that the target is an
existing Page Folder with a loadable `page.toml` or same-stem Page Face. Read
the source and its registration; do not silently wrap a plain file or create a
nested Page Folder. Python 3.11 or newer is required.

## Live versus static

| Operation | Source of truth | What a refresh sees |
|---|---|---|
| `serve` | Current Page source on disk | The current Markdown/Page Face and live plugin projections |
| `build` | Page source at build time | The last generated `delivery/web/` export |

The standalone `GET /` path reloads the current Page source before rendering.
After an authorized editor saves Markdown, a browser refresh is enough to see
the live Page. This does not rewrite `delivery/web/`; run `build` when a
portable static artifact or a downstream Board projection must be refreshed.
Generated HTML is never an edit target.

`--read-only` removes the Source editor and rejects supported write requests.
Without it, the Source workspace still protects against stale hashes and
keeps imported content bound to its registered source file.

## Start the server

Use an installed Python 3.11+ interpreter and the Page engine's CLI:

```bash
<python-3.11+> <page-engine>/cli/page.py serve <page-folder> \
  --host <host> --port <port> [--read-only] \
  [--public-url <configured-origin>]
```

The CLI also accepts `--token`; obtain it from the protected environment or
`PAGE_SERVER_TOKEN`, never from Page Markdown, a log, or the reply. The
defaults are `127.0.0.1:8765`, with no token needed for a loopback-only
server. A non-loopback binding requires `--token` or `--read-only`.

For a user-facing request, use the workspace's supported background process
manager so the agent turn returns after startup. Do not start a second listener
when the requested Page server is already running; reuse the existing URL or
choose an available port after identifying the conflict.

## Verify and return

1. Confirm the Page server starts and prints its startup URL.
2. Request the exact configured public origin when one is configured. For a
   local-only server, verify the loopback URL from the same machine.
3. Require a successful response for `/`; a successful process start alone is
   not a hosted Page.
4. Return the Page Folder, mode (`live` or `read-only`), source path, verified
   URL, and whether static `delivery/web/` is current or not required.

In Physician-SPACE, a reader-facing reply uses `JJLUO_PUBLIC_URL` from
`.server_config/settings.env`. Never substitute `localhost`, `127.0.0.1`, or
`file://` for that configured origin. Do not publish private inputs without
the person's authority.

## Stop conditions

- A static-site request ends with `build`; it does not start an indefinite
  server.
- Board index, aggregate navigation, Board-only terminal, and multi-Page
  hosting belong to `haipipe-board/fn/serve.md`.
- A successful build is reported separately from server reachability and
  source-edit capability.
- Never claim that `serve` refreshed a static export. For a Board source edited
  outside the browser, use the Board watcher or run its build explicitly.

## Return packet

```text
PAGE · SERVE
target:       <Page Folder>
mode:         live | read-only
source:       <relative source path>
url:          <verified configured URL>
static:       current | stale | not required
editing:      available | disabled
next:         <one concrete next action, if any>
```

