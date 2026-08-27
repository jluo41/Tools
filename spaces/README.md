# JJ-LUO Spaces

This directory is the space layer under the JJ-LUO house. The canonical brand
name is `JJ-LUO` (two Js), and the DNS root is `jjluo.com`. The custom DNS
names are currently parked; the live SPACE services use the Mac's Tailscale
hostname and separate ports.

The four SPACE repositories are sibling directories under the Desktop workspace.
`Tools-SPACE/spaces` stores their shared registry; it is not a replacement for
any of the four repositories.

## Space endpoints

| Space | Canonical slug | Tailscale endpoint | Legacy custom domain | Local path | Config page | Status |
|---|---|---|---|---|---|---|
| Physician-SPACE | `physician` | `http://jluo41s-mac-studio.tail582a01.ts.net:5601` | `physician.jjluo.com` (disabled) | `../Physician-SPACE` | `Physician-SPACE/.server_config/README.md` | active |
| WellDoc-SPACE | `welldoc` | `http://jluo41s-mac-studio.tail582a01.ts.net:5602` | `welldoc.jjluo.com` (disabled) | `../WellDoc-SPACE` | `WellDoc-SPACE/.server_config/README.md` | active |
| REACH-SPACE | `reach` | `http://jluo41s-mac-studio.tail582a01.ts.net:5603` | `reach.jjluo.com` (disabled) | `../REACH-SPACE` | `REACH-SPACE/.server_config/README.md` | active |
| DrFirst-SPACE | `drfirst` | `http://jluo41s-mac-studio.tail582a01.ts.net:5604` | `drfirst.jjluo.com` (disabled) | `../DrFirst-SPACE` | `DrFirst-SPACE/.server_config/README.md` | active |

The machine-readable source of truth is [`registry.yaml`](registry.yaml).

CMSRegBoard is a second board service rooted at Physician-SPACE and keeps its
own port: `http://jluo41s-mac-studio.tail582a01.ts.net:5599/b/cmsregboard`.
It uses the Physician auth file and is recorded in the shared registry as a
service, not as a fifth SPACE.

## Board context and configuration

Resolving a Board has two layers. The nearest or explicitly attached
`board.md` identifies the Board and its `## Pages` registry. The repository
around that Board identifies its owning SPACE; match that repository against
`registry.yaml`, then read the entry's `config_page` before changing any public
host, port, route, mount, root, or discovery setting.

The four neighboring SPACE folders are part of this lookup even when the
current working directory is `Tools-SPACE`. Inspect the registry first, then
the one matched SPACE and its public configuration page. Do not recursively
inventory unrelated sibling projects.

This registry deliberately contains no per-Board list. Each SPACE Board Home
discovers Boards by walking its own root for `board.md`, so adding or moving a
Board cannot leave a second list stale. `board.md ## Pages` remains the Page
registry; this file remains the SPACE registry.

When a public configuration fact changes, update `registry.yaml` and the
matched `.server_config/README.md` in the same round. The adjacent
`settings.env` is machine-local and may contain local paths; do not print,
copy, or edit it unless the user explicitly requests a machine setting. Page
title and prose changes do not require a SPACE configuration write.

## Board URLs

Boards stay under their owning space:

```text
http://jluo41s-mac-studio.tail582a01.ts.net:5601/b/{board-slug}
http://jluo41s-mac-studio.tail582a01.ts.net:5602/b/{board-slug}
http://jluo41s-mac-studio.tail582a01.ts.net:5603/b/{board-slug}
http://jluo41s-mac-studio.tail582a01.ts.net:5604/b/{board-slug}
```

This reuses the Board server's existing short route and keeps deployment and
authentication at the space boundary. A board gets its own subdomain only when
it needs an independent service, access policy, or release lifecycle.

## Deployment shape

The root `jjluo.com` remains the personal profile site. The SPACE layer now
uses direct Tailscale bindings. Each service's network-facing listener uses the
Mac's Tailscale address (`100.121.165.84`) and has a separate port. The server
also keeps a loopback listener for local development and SSH/VS Code forwards:

```text
jluo41s-mac-studio.tail582a01.ts.net:5599 -> CMSRegBoard / Physician-SPACE
jluo41s-mac-studio.tail582a01.ts.net:5601 -> Physician-SPACE
jluo41s-mac-studio.tail582a01.ts.net:5602 -> WellDoc-SPACE
jluo41s-mac-studio.tail582a01.ts.net:5603 -> REACH-SPACE
jluo41s-mac-studio.tail582a01.ts.net:5604 -> DrFirst-SPACE
```

Tailscale's encrypted transport protects the HTTP connections; the board
server's Basic Auth remains a second boundary. A viewer must be connected to
the JJ-LUO tailnet, and tailnet ACLs still apply. Tailscale Serve is not enabled
for this tailnet, so these endpoints intentionally use the direct hostname and
port form instead of HTTPS on port 443. Each service must mount only its own
SPACE root. The interactive `serve.py` runtime includes file writes, chat, and
a terminal, so it must not be published with the whole Desktop or the whole
Tools repository as its root.

## Board metadata

Each board should expose the same small status record wherever it is stored:

```yaml
id: example-board
space: physician
title: Example Board
status: active
source: Physician-SPACE/<relative-board-path>
updated: 2026-08-24
visibility: private
```

Human-facing configuration names follow the Board family's Naming law in
`plugins/haipipe-toolkit/skills/board/haipipe-board/ref/writing-rules.md`:
prefer six reader-facing words or fewer, never exceed eight, and use one
concrete object, action, or outcome instead of generic model-like framing.
Keys and slugs stay shorter still. A name is an address; the `note` field carries
the explanation.

Allowed lifecycle statuses are `planned`, `active`, `review`, `paused`, and
`archived`. The registry describes ownership and routing; it does not claim a
domain is live until DNS and hosting are configured.
