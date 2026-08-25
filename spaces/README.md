# JJ-LUO Spaces

This directory is the space layer under the JJ-LUO house. The canonical brand
name is `JJ-LUO` (two Js), and the DNS root is `jjluo.com`.

The four SPACE repositories are sibling directories under the Desktop workspace.
`Tools-SPACE/spaces` stores their shared registry; it is not a replacement for
any of the four repositories.

## Space domains

| Space | Canonical slug | Domain | Local path | Status |
|---|---|---|---|---|
| Physician-SPACE | `physician` | `physician.jjluo.com` | `../Physician-SPACE` | active |
| WellDoc-SPACE | `welldoc` | `welldoc.jjluo.com` | `../WellDoc-SPACE` | active |
| REACH-SPACE | `reach` | `reach.jjluo.com` | `../REACH-SPACE` | active |
| DrFirst-SPACE | `drfirst` | `drfirst.jjluo.com` | `../DrFirst-SPACE` | active |

The machine-readable source of truth is [`registry.yaml`](registry.yaml).

## Board URLs

Boards stay under their owning space:

```text
https://physician.jjluo.com/b/{board-slug}
https://welldoc.jjluo.com/b/{board-slug}
https://reach.jjluo.com/b/{board-slug}
https://drfirst.jjluo.com/b/{board-slug}
```

This reuses the Board server's existing short route and keeps deployment and
authentication at the space boundary. A board gets its own subdomain only when
it needs an independent service, access policy, or release lifecycle.

## Deployment shape

The root `jjluo.com` remains the personal profile site. The SPACE layer uses one
Cloudflare Tunnel with four hostname-to-service routes:

```text
physician.jjluo.com  -> 127.0.0.1:5601  -> Physician-SPACE
welldoc.jjluo.com    -> 127.0.0.1:5602  -> WellDoc-SPACE
reach.jjluo.com      -> 127.0.0.1:5603  -> REACH-SPACE
drfirst.jjluo.com    -> 127.0.0.1:5604  -> DrFirst-SPACE
```

The first public deployment should be read-only and protected by Cloudflare
Access. Each service must mount only its own SPACE root. The interactive
`serve.py` runtime includes file writes, chat, and a terminal, so it must not be
published with the whole Desktop or the whole Tools repository as its root.

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

Allowed lifecycle statuses are `planned`, `active`, `review`, `paused`, and
`archived`. The registry describes ownership and routing; it does not claim a
domain is live until DNS and hosting are configured.
