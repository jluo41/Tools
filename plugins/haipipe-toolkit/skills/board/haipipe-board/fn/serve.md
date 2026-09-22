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
| SPACE Home | `<DOMAIN>/` or `<DOMAIN>/boards` |
| Board index | `<DOMAIN>/b/<board-slug>` |
| One Page in that Board | `<DOMAIN>/b/<board-slug>/<page-id>` |
| The Board's workbench | `<DOMAIN>/w/<board-slug>` |
| One Page's workbench | `<DOMAIN>/w/<board-slug>/<page-id>[/<tab>]` |

`b` is the reader's address, `w` the worker's, and they take the same two
words. Both redirect to the canonical long route, so relative assets, live
panes, and write-back paths keep the correct origin, and the server fills in
the long route's query itself. Obtain `<board-slug>` from the discovered Board
(the folder name without its `NN-` ordinal and `-YYMMDD` date) and `<page-id>`
from the Board's page id (`QA1`, `S-Label-1`); never invent either value.
`<tab>` is one of `runs`, `delivery`, `folder`, `evidence`, `value`, `design`,
`insight`, `labeling`; omitted, the Page's workbench opens on 📃 Page. An
unknown slug, page, or tab is a 404 that says why, not permission to guess.

`<DOMAIN>` is a variable, not a value to type: the origin the person will use.
The server prints every DOMAIN it answers at when it starts (loopback, the
Tailscale IP when the bind reaches it, and the configured origin from
`--public-url`, the `HAIPIPE_DOMAIN` environment variable, or the `DOMAIN` line
of `<root>/.server_config/settings.env`). The link body after `<DOMAIN>` is the
same for all of them.

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
<repo-root>/.venv/bin/python <servers>/_host/serve.py --root <root>
```

`<servers>` is the plugin-level servers tree, `plugins/haipipe-toolkit/servers`,
a sibling of `skills/`; the Board skill folder itself holds no server code.

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

Omitted host, port, SPACE name, DOMAIN, and auth file are read from the
non-secret keys of `<root>/.server_config/settings.env` when available:
`BIND_HOST`, `PORT`, `SPACE_NAME`, `DOMAIN`, `AUTH_FILE`, `NO_AUTH` (a
deployment may prefix them, `<PREFIX>_DOMAIN`). Do not print that file, copy
credentials into a Board, or put a real password in the function reply.
`--only <workbench>` serves one workbench's routes and nothing else; the
labeling host under `plugins/subjective-label/servers/_host/serve.py` is that
flag with `labeling` filled in.

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

Resolve `<DOMAIN>` from the server's startup print or, before it starts, from
`--public-url`, `HAIPIPE_DOMAIN`, or the `DOMAIN` line of
`.server_config/settings.env`. A reader-facing reply uses the DOMAIN the reader
will actually use (the configured origin or the Tailscale IP), never a bare
`localhost` or `file://` substitute; a loopback DOMAIN is right only for the
person sitting at this machine.

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
the workbench surface that shows the Board's own journey.

| URL | What it is | Shape |
|---|---|---|
| board | the generated static site, wrapped in the reader shell | `<DOMAIN>/b/<board-slug>` |
| workbench | the live, storage-less workbench for this Board kind | `<DOMAIN>/w/<board-slug>` |

Both are short routes that redirect to the canonical long form. The workbench
redirect picks the route from what `board.md` declares and fills in
`path=<board-path>/board.md&file=board.md` itself:

| board.md declares | Long route behind `/w/<board-slug>` |
|---|---|
| `dialect: paper` | `/_board/paper` |
| `board-kind: design-board`, or a Design Board by layout | `/_board/design-board` |
| `board-kind: insight-board`, or an InsightBoard by layout | `/_board/insight-board` |
| `board-kind: labeling-board`, or Pages that own labeling jobs | `/_board/labeling-board` |
| none of the above | 404 with the reason; return `workbench-url: none` |

The long form stays valid, and `file=` may now be omitted on every route: the
server derives it from `path=` (a Board folder or anything under its generated
`board/` is `board.md`; a Page folder is its registered or same-stem Face).

A page-level workbench is a different thing and is not this field. One Page's
workbench answers at `<DOMAIN>/w/<board-slug>/<page-id>[/<tab>]` and belongs
to that Page, not to the Board; `haipipe-page/fn/serve.md` owns it.

Verify both by request, not by construction. A URL that was assembled and never
fetched is not a verified URL: the common failure is a 200 that renders every
count as zero because `board.md` does not bind, which no amount of
string-building can detect. Fetch it, follow the redirect, and read one number
off the response before reporting it.

## Return packet

```text
BOARD · SERVE
root:         <selected root>
boards:       <Board scope or list>
domain:        <DOMAIN the reader will use; the others the server printed>
board-url:     <DOMAIN>/b/<board-slug>           verified by request
workbench-url: <DOMAIN>/w/<board-slug>           verified, or none for this board kind
auth:         loopback | auth-file | trusted-private exception
build:        current | rebuilt | stale | blocked
watchers:     <active Board watchers, or none>
next:         <one concrete next action, if any>
```
