---
name: haipipe-board-serve
description: >-
  Serve one Board or a selected project/SPACE root containing multiple Boards.
  Keep one repository server, distinguish generated Board HTML from live
  source, and route single-Page hosting to haipipe-page.
argument-hint: "<board-or-space-root>"
allowed-tools: Bash, Read, Grep, Glob
---

# Serve · Board or SPACE root

Use `/haipipe-board serve <root>` when the person wants a Board index, a
Board-hosted Page, or several Boards reachable through one server. This
function owns the Board hosting adapter and the root boundary. It does not
own the Page renderer or create a second Page server per Page.

## Choose the root

| Desired scope | `--root` | Server result |
|---|---|---|
| One Board | that Board folder | Its generated site and Board live routes |
| Several Boards in one project | the common project root | One server plus the project's Boards |
| Several projects or the whole SPACE | the configured repository/SPACE root | SPACE Home plus every discovered Board below it |
| One standalone Page with no Board | not this function | Use `haipipe-page/fn/serve.md` |

The server discovers `board.md` below `--root`, skips generated `board/`
trees and archives, and serves the SPACE Home at `/`. A common root is useful
when several Pages are being worked on together, but it also exposes every
Board beneath that root. Choose the narrowest root that contains the intended
work.

## Use the verified short routes

After the server is reachable, resolve links from the Home or the selected
Board's rendered index. The reader-facing routes are:

| Surface | Route |
|---|---|
| SPACE Home | `<origin>/` or `<origin>/boards` |
| Board index | `<origin>/b/<board-slug>` |
| One Page in that Board | `<origin>/b/<board-slug>/<page-id>` |

The short route redirects to the canonical generated file so relative assets,
live panes, and write-back paths keep the correct origin. Obtain
`<board-slug>` from the discovered Board and `<page-id>` from its resolved
rendered Page link or index; never invent either value from a folder name.
Verify the exact final Board or Page route before returning it. An unknown or
ambiguous slug is a 404, not permission to guess another Board.

## Read before serving

Read `../SKILL.md`, the selected Board's `board.md`, its parent Project or
SPACE identity, and `../ref/operations.md`. Do not infer Board membership from
generated HTML. `board.md` and the source tree are authoritative; `board/` is
derived.

Before returning a Board URL, build the selected Board when its generated index
is missing or stale:

```bash
<python> <board-engine>/cli/build.py <board-folder>
```

Do not rebuild unrelated Boards merely because they share the same server
root. A `serve` operation hosts what is present; `build` is the operation that
refreshes a generated Board projection.

## Start one server

Use the repository's configured server settings. The recommended interpreter
is the repository virtual environment because live Chat routes may require its
SDK:

```bash
<repo-root>/.venv/bin/python <board-engine>/cli/serve.py --root <root>
```

When settings are not available, the CLI accepts these relevant overrides:

```text
--host <address>       listener address
--port <port>          listener port
--space-name <name>    SPACE Home label
--public-url <origin>  reader-facing origin
--auth-file <path>     username:password file for a non-loopback host
--no-auth              explicit trusted-private-network exception
--daemon <logfile>     detach with output in a named log
```

Omitted host, port, SPACE name, public URL, and auth file are read from the
non-secret values in `<root>/.server_config/settings.env` when available. Do
not print that file, copy credentials into a Board, or put a real password in
the function reply.

For a non-loopback host, use an auth file by default. `--no-auth` is allowed
only when the person explicitly accepts the trusted private-network boundary.
The Board server includes a terminal endpoint; exposing it without the
intended authentication boundary is unsafe.

Use the workspace's supported background process manager for a user-facing
server. If the requested server is already running for the same root, reuse it
instead of starting a second listener.

## Markdown, build, and refresh

| Change | What updates immediately | What is required |
|---|---|---|
| Browser/live-pane write | Markdown plus the affected Board projection | The server's write route performs its scoped rebuild |
| External editor saves `.md` | Source Markdown only | Run `watch.py <board-folder>` or `build.py` |
| Python/CSS/JS/template change | Source code only | Run the appropriate build; restart the server if its loaded code changed |
| Static-only reading request | Nothing hosted | Run `build.py`; no listener is needed |

One Board server can host many Boards, while the current watcher is scoped to
one Board folder. Therefore the normal multi-Board authoring setup is:

```text
one Board/SPACE server
  ├── watcher for Board A, only while its Markdown is being edited
  ├── watcher for Board B, only while its Markdown is being edited
  └── no watcher for an unchanged Board
```

`serve` and `watch` are different functions: the first provides HTTP routes;
the second turns external Markdown saves into generated `board/` updates.
Refreshing a Board URL without a rebuild can still show the old generated
Page, even though the source Markdown is already current.

## Verify and return

1. Confirm the selected Board's `board/index.html` exists after the scoped
   build, when a Board URL is requested.
2. Start or reuse the one server for the chosen root.
3. Request the exact configured public origin and require a successful HTTP
   response for the Home or selected Board route.
4. Return the root scope, selected Board(s), server URL, authentication mode,
   build freshness, and watcher state.

In Physician-SPACE, resolve the reader-facing origin from `JJLUO_PUBLIC_URL`
in `.server_config/settings.env`. Use the verified configured URL in the
reply; never substitute `localhost`, `127.0.0.1`, or `file://`.

## Stop conditions

- Do not start one server per Page when one common root is in scope.
- Do not widen `--root` simply to make a Board discoverable; a wider root
  changes the set of files and terminal routes exposed by the server.
- Do not hand-edit generated `board/` files or report them as source.
- Do not say that `serve` alone rebuilt a Board after an external Markdown
  edit; name the watcher or explicit build that made the projection current.
- Do not return a Board URL until its exact configured route has been checked.

## Two URLs, always both

A served Board answers at two different addresses and a reply that gives only
one is incomplete. The reader wants the Board; the person doing the work wants
the plugin surface that shows the Board's own journey.

| URL | What it is | Shape |
|---|---|---|
| board | the generated static site, wrapped in the reader shell | `<origin>/<board-path>/board/index.html` |
| plugin | the live, storage-less plugin surface for this Board kind | `<origin>/_board/<route>?path=<board-path>/board.md&file=board.md` |

`<board-path>` is the Board folder relative to the server's `--root`, with no
leading slash. `file=board.md` is mandatory on every plugin route: the handler
returns 400 without it, and 400 again when `board.md` does not declare the
dialect or kind that route serves.

Pick the plugin route from what `board.md` declares:

| board.md declares | Plugin route |
|---|---|
| `dialect: paper` | `/_board/paper` |
| `board-kind: design-board` | `/_board/design-board` |
| `board-kind: insight-board` | `/_board/insight-board` |
| `board-kind: labeling-board` | `/_board/labeling-board` |
| none of the above | no board-level plugin; return `plugin-url: none` |

A page-level surface is a different thing and is not this field. 🧭 Outline
answers at
`/_board/outline?path=<board-path>/<page-rel>&file=<page-rel>`, where
`<page-rel>` is the Page Face relative to the BOARD root, not a bare basename;
it belongs to one Page, not to the Board. `haipipe-page/fn/serve.md` owns it.

Verify both by request, not by construction. A plugin URL that was assembled
from a template and never fetched is not a verified URL: the common failure is
a 200 that renders every count as zero because `board.md` does not bind, which
no amount of string-building can detect. Fetch it, and read one number off the
response before reporting it.

## Return packet

```text
BOARD · SERVE
root:         <selected root>
boards:       <Board scope or list>
board-url:    <verified configured URL of board/index.html>
plugin-url:   <verified /_board/<route> URL, or none for this board kind>
auth:         loopback | auth-file | trusted-private exception
build:        current | rebuilt | stale | blocked
watchers:     <active Board watchers, or none>
next:         <one concrete next action, if any>
```
