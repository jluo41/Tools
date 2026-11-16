This file holds how to open the rendered Page and the user check packet surfaces, moved from `SKILL.md` § 🚪 Preview · create · work on · run.

### 🔗 Open the rendered Page

For standalone technical intake/edit/build, use `ref/standalone.md` and its
handoff; a source/Folder link is appropriate and a Board URL is not required.
For a hosted standalone Page, verify its configured Page-server origin. The
following server instructions apply only when this Page is hosted by a Board.

A source `.md` path is not the Board reader-facing link. Build the Board, then open
the generated Page through the repository's configured Board server:

```bash
ROOT="$(git rev-parse --show-toplevel)"
set -a
source "$ROOT/.server_config/settings.env"
set +a
python3 plugins/haipipe-toolkit/servers/_host/serve.py --root "$ROOT"
# host, port, SPACE name, DOMAIN and auth file come from
# $ROOT/.server_config/settings.env (BIND_HOST, PORT, SPACE_NAME, DOMAIN, AUTH_FILE)
```

Open `<DOMAIN>/b/<board-slug>/<page-id>` in a browser. The short
route redirects to the live reader (`/_board/page`); `<page-id>` is the resolved
Page id (for example, `b01j03t04` for a Task Page). The Board index is
`<DOMAIN>/b/<board-slug>`; its workbench is `<DOMAIN>/w/<board-slug>/<page-id>`. If the server is already running, reuse
it; do not start a second listener. Use the configured public URL for a
reader-facing reply and never substitute `localhost`, `127.0.0.1`, or
`file://`. The short-route and server details are owned by
`fn/serve-host.md`; this section is the Page entry point.

Before returning a reader-facing Page link, make a lightweight request to the
exact configured public URL and require a successful response. Every Board-hosted
delivery reply ends with that verified Board URL when the request
succeeds. If verification fails, the user-check packet ends with an explicit
Board-unavailable blocker and no clickable substitute. It may not end with a
source-file path, `localhost`, `127.0.0.1`, or `file://`.

### 👀 User check packet · the only primary return surfaces

For substantive writing or research delivery, return the compact packet in
`ref/user-check-packet.md`. For a routine interactive turn, return the full
selected paragraphs and concise feedback dispositions, followed by direct
Draft Space, Evidence Space, and Current Run links at the very end.
Only the live
Draft Space must be refreshed for a routine Step; the Evidence Space
changes only when that Step changes an evidence requirement. Do not update
adopted Content or build web, LaTeX, Word, or PDF at Page Run close. The
following surfaces are the formal Page-release packet, produced once after all
Page Runs and required evidence Task Results are complete:

1. the verified Board route in two direct views: **Draft Space**
   (`lens=div`) and **Outline table** (the compact Page projection);
2. **Evidence you can open now**: the direct Evidence Space link
   (`lens=evidence`) plus, per ready
   typed Evidence Item, the DISPLAY unit's `preview.pdf`, the Page's citation
   register, or the VALUE item card deep link;
3. **Content state**: the Page version and whether Revise ran (owner-selected workers and
   the fresh-context style verdict against the resolved owner's policy); a first draft is labelled as such;
4. the current one-Page compiled PDF, labelled **Latest Page-level PDF**, the
   delivery surface shown after Revise;
5. the read-only **Delivery Workspace** (`lens=delivery`), whose lane receipt
   confirms that the current Page source and saved delivery artifacts agree.

“Page-level” means this Page or Section Page only. It is not the paper master,
the desk-room build, a Display preview, or a configuration file. Keep raw
receipts, logs, TeX sources, manifests, and unrelated outputs out of the
primary completion block. If any requested surface is missing or stale, say so
explicitly and name the blocker instead of presenting an older file as current.
The user-check packet is new-layout-only: it accepts only Result payload
previews and bibliography artifacts at their resolved producer paths, the Evidence Space one-URL
route, and `delivery/latex/<stem>.pdf`; legacy locations do not qualify.
