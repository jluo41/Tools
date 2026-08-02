# Hosting: local vs server

state: 🟡 PARTIAL · read-only half verified; no route ruled, nothing deployed
owner: JL
method: first sort out "who needs to see it", then decide local vs. server

## Question
How can someone outside the author's machine open this board without exposing more of the repository than they should?

The static pages are easy to share, but comments, chat, and terminal access require a live service beside the source files.
Those two halves carry very different risks, especially in a repository with private data and credentials.
The chosen route determines authentication, write permissions, and whether collaborators get a view or a workbench.
It succeeds when a second reader can use the promised tier through a protected, narrow path.


## Boundary
- ✅ Covered here
  **How the board is reached**: local / LAN / server, who can see it, login or not, static export vs. full function.
- ↪ Covered elsewhere
  The Board's **content and layout**: that is the `QA` group, and `QA2b` for the Board-Webpage-Index and the shared surface.
  Nor whether **work can be done on the board**: that is the `QD` group; this question only owns "where it opens from".

## Diagram

```
                     the static half         the live half (files must be local)
                  board.html               comment write-back · chat · terminal
                  ─────────────            ──────────────────────────────────
① today: local     ✅ 127.0.0.1:5599        ✅ everything works      only you can see it
② static export    ✅ opens anywhere         ❌ all gone             enough for a look
③ full on server   ✅                        ⚠️ needs auth + a write-permission audit   real collaboration
```

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QE1

## Items to Finish
### Rulings awaiting JL
- [ ] Sort out "who needs to see it, and which half"
      A read-only glance (②) or commenting and working together (③).
      Different answers, completely different builds.
- [ ] Settle the read-only route
      Static export: `board.html` is self-contained and should open anywhere, but `fig/` and `## Links` relative paths must travel with it; verify once.
      The verification itself ran on 260727 and split into two answers: the page BODY travels
      (zero absolute-origin references, no iframes, no `/_excalidraw` reference), while the
      outward `## Links` do NOT (1019 `../` hrefs into `sections/`, `tasks/`, `discoveries/`).
      So the route is technically available for reading and dead for drilling through.
      This line still closes on JL choosing it, not on the verification.
- [ ] 🪜 the shared deployment has an explicit tier, and JL has picked one
      Tier A is board editing only: every comment, discussion, resolve, structure and excalidraw
      write stays live, while `/_term/` and `/_board/chat` are off, so the board behaves exactly
      like localhost for everyone who is not the owner. Tier B adds the shell and the chat, which
      is a remote shell and the owner's Claude login behind a shared password.
      Closes when JL names the tier the shared URL runs at.
- [ ] Settle the bar for the full-function route
      A server deployment needs auth (who may write) and an audit of `serve.py`'s write endpoints under a public network.

### Hardening before the origin goes public
- [ ] Bound what the published origin can read
      The repo holds CMS PHI (`_WorkSpace/1-CMS-Store`, `2-Data-Store`) and secrets (`env.sh`),
      so a file server rooted at the repo is excluded no matter what auth sits in front of it.
      Measured on 260727: `GET /env.sh` against the running server returns 200 and the whole file.
      This line closes when the static handler serves only what may leave, by allowlist or by root.
- [ ] 🔐 the exposed service has an auth gate
      `boards_api.py` has none on any route, and `serve.py` has none at any of its four entry points
      (`do_GET`, `do_HEAD`, `do_POST`, the ttyd `Upgrade` branch).
      Since 260727 the exposed program is `haichat-board`, so this closes when a shared credential is
      required there, covering the write POSTs and `/_board/page/*` alike.
- [ ] 🎚 the chat privilege level is pinned server-side, if chat is ever exposed
      `/_board/chat` accepts `scope: "bypass"` from the POST body, which disables the permission
      callback entirely. Moot while `INLAB_BOARD_LIVE` is empty and the endpoint 501s; it becomes
      required the moment tier B is chosen. Closes when the ceiling is set by the server, or when
      tier A is ruled permanent and this line points at that ruling.

### The public name and the short path
- [ ] Name the public address, because the tailnet IP cannot be one
      A domain pointed at `<tailscale-ip>` resolves for the owner's tailnet devices only, so a
      DNS A record is not a deployment; a tunnel is. This line closes when the chosen route
      names the actual vehicle.
- [ ] 🌐 the public name exists and carries WebSockets
      A `cloudflared` tunnel with a `paper` CNAME on `jjluo.com`, verified by loading a board AND
      opening a terminal or a comment write through it, not by the HTML alone.
- [ ] 🔗 a short per-paper path exists
      JL asked for `paper.jjluo.com/<paper>/`, while `serve.py` is rooted at the repo and so serves
      the full repo-relative path. Closes when an alias maps one short segment to one board folder.

### A real second reader
- [ ] Decide how comments attribute to people
      Today the signature is browser-side initials of your choosing (any 1–4 uppercase letters).
      Real multi-user needs more than that.
- [ ] A second person has actually opened it once
      That is the acceptance line: not "theoretically possible": someone really opened it from another machine and left a comment.

## Where we are
**One route only: local, tunneled out by Remote-SSH.**

- How it opens today
  `serve.py --root <repo root> --port 5599`, bound to `127.0.0.1` only; VS Code Remote-SSH forwards 5599 to the laptop; Simple Browser opens it.
- Why it binds local-only
  `serve.py` has write endpoints (comment write-back, chat, terminal).
  Binding 0.0.0.0 hands disk writes and terminal spawning to the network, with no auth at all today.
- The static half is already quite independent
  The invariant guarantees "strip every `<script>` and every question plus all body text remains".
  So the technical bar for read-only distribution is low; what is missing is verification and rules, not capability.
- Route ③ now has a concrete vehicle (260724)
  `haichat-inlab` gained `boards_api.py` (`QE2`/`QE3`): SPACE mounting, board discovery, page serving, comment write-backs.
  It still binds locally, so nothing about THIS question's decisions (who can reach it, auth, attribution) has changed; but when JL picks route ③, the thing to expose now exists, and it lives inside a service that docker-compose already deploys.
- Route ② was measured on a real board (260727)
  Asked against `Paper-Personality2Opioid-MISQ2026/0-lifecycle/board.html`, 1.6 MB, 60 pages.
  The body is genuinely portable: no reference to `127.0.0.1:5599`, none to the machine's tailnet
  address, no `<iframe>` at all, and no `/_excalidraw` reference, so it renders at any origin and
  under any path prefix. `fig/` is empty for this board, so nothing has to travel beside it.
  What does not survive is drill-through: 1019 hrefs begin `../` and leave the board folder for
  `sections/`, `appendices/`, `tasks/*/QA/`, and `discoveries/*/QA/`. Exporting the one file
  publishes every ruling and every stage page and 404s every citation of the evidence behind them.
- The named IP is a tailnet address, not a host (260727)
  `<tailscale-ip>` is this machine's Tailscale address; `tailscale status` lists another device at
  `<another-tailnet-ip>` and one node belonging to `<another-tailnet-account>`. Addresses in
  `100.64.0.0/10` are private to the tailnet, so pointing a public name at it produces a name that
  resolves nowhere for a reader who is not already on the tailnet, and Cloudflare cannot proxy to
  it either. A public name therefore needs a tunnel out of this machine, not a DNS record into it.
- The vehicle for a public name is already installed (260727)
  `jjluo.com` is served by Cloudflare nameservers (`evelyn`/`khalid.ns.cloudflare.com`) with its
  apex on GitHub Pages; `paper.jjluo.com` does not exist yet. `cloudflared` is present at
  `/opt/homebrew/bin/cloudflared`. Neither Caddy nor nginx is installed, so a reverse proxy with
  a password would be a new dependency.
- JL ruled for the LIVE half, so route ③ is the target and its bar is now measured (260727)
  JL's requirement: "I want it can be modified as the real ones, I mean they should just as the
  local host." A snapshot does not satisfy that, so the thing to expose is `serve.py` itself, and
  the three findings below are what stand between it and a public name. None is a reason not to do
  it; each is a thing that has to be built first.
- 🔓 A plain GET reads every secret in the repo, no shell required
  `serve.py` subclasses `SimpleHTTPRequestHandler` rooted at `--root`, so the static handler serves
  any file under the repo. Measured against the running server on 260727:
  `GET /env.sh` returns `200` and all 1537 bytes, `GET /pyproject.toml` returns `200`, and `GET /`
  returns a directory listing. `env.sh` holds the AWS, HuggingFace, OAuth and Render credentials.
  So the first thing a public origin leaks is not the terminal; it is the secrets file, to anyone
  who guesses one filename. A read allowlist or a narrowed root is therefore not a hardening
  extra, it is a precondition.
- 🎚 The browser chooses its own privilege level
  `/_board/chat` reads `scope` from the POST body and accepts `bypass`, which sets the SDK's
  `permission_mode` to `bypassPermissions` and installs no `can_use_tool` callback: the documented
  equivalent of `--dangerously-skip-permissions`. The client, not the server, decides this. Any
  remote caller can therefore request an unsupervised full-tool Claude run spending the owner's
  ambient OAuth login. Remote exposure requires the server to pin `scope` instead of trusting it,
  and that is true even for the owner's own use over a tunnel.
- 🖥 The terminal is ttyd over a WebSocket, and it does tunnel
  `board.js` connects to `/_term/<key>/ws` with the `tty` subprotocol, and `serve.py` handles the
  `Upgrade` by raw-pumping both directions. Cloudflare Tunnel passes WebSockets, so the shell
  would work remotely rather than fail closed. Convenient, and the reason the shell has to be an
  explicit tier rather than something inherited by accident.
- 🐳 JL redirected the vehicle to the container, and it changes which program gets exposed (260727)
  JL: "could we keep things in a docker, and it will mount only the board folder, and will only change
  the things within that board folder", pointing at `platforms/HAIChat-SPACE/haichat-board`.
  That is a better answer than gating `serve.py`, because it moves the exposed program from the one
  with a shell to the one without. `haichat-board` implements comment, discuss, resolve and structure
  itself by importing the skill's md-writers, and RELAYS only `/_board/chat` and `/_term/` upstream to
  a workstation `serve.py` named by `INLAB_BOARD_LIVE`. The shipped compose sets
  `INLAB_BOARD_LIVE: "{}"`, so with no upstream configured those two endpoints answer an honest 501
  while pages stay readable and commentable. Tier A is therefore the ALREADY-SHIPPED posture rather
  than something to build, and the three preconditions above land as follows:
  the `env.sh` read disappears because the file is not in the mount, the client-chosen `bypass` scope
  disappears because `/_board/chat` has no upstream to relay to, and the ttyd WebSocket disappears with
  it. What does NOT improve is tier B: if `INLAB_BOARD_LIVE` is ever pointed at a host `serve.py`, the
  shell and the chat run ON THE HOST, outside the container, so Docker contains none of it. The
  container is an argument for tier A, not a way to make tier B safe.
  Still missing there, and the reason this question stays open: `boards_api.py` contains no
  authentication of any kind, on any route.
- 🔨 If the gate goes in `serve.py` instead, it is small
  There are exactly four request entry points to cover: `do_GET`, `do_HEAD`, `do_POST`, and the
  `Upgrade` branch that fronts ttyd. `serve.py` takes only four flags today
  (`--root --port --host --daemon`), so auth has no home yet; adding it here also closes `QE6`'s
  open item asking for the terminal endpoint to be gated or the reason written down. Neither Caddy
  nor nginx is installed, so putting the gate in a proxy would add a dependency to do the same job
  in a second place.
- What may be exposed is narrower than what auth protects
  A password decides WHO reaches the origin; it does not decide WHAT the origin can read. This
  repo holds CMS PHI under `_WorkSpace/` and every secret in `env.sh`, so containment has to come
  from the served root, and a repo-rooted file server is excluded regardless of the login in front
  of it. The same argument applies to exposing `serve.py` itself: `/_term/` is a real shell,
  `/_board/chat` spends the owner's OAuth login with write tools, and `/_board/structure` creates
  and archives files, so one shared password in front of it is one shared password in front of
  remote code execution.

### Decision Now
- [ ] 🪜 Name the tier the shared URL runs at
      Tier A is board editing only, with `/_term/` and `/_board/chat` answering 501, and it is the posture the shipped container already runs; tier B adds the shell and the chat, which run on the host and which Docker does not contain.
      The container reading above argues for tier A; a tick here also closes the 🪜 row in Items to Finish.
- [ ] ✍️ Decide how comments attribute to people
      Today the signature is browser-side initials of the writer's choosing, and the page records no candidate scheme yet, so a tick here also closes the same row in Items to Finish.

## Files
- `serve.py`
  Bind address, port, write endpoints, and (future) auth all live here.
- `board.html`
  The static-export deliverable itself; `fig/` and `## Links` relative paths must be verified together.

## Discussion
> JL: How do you think I can host on <tailscale-ip> with the domain of paper.jjluo.com/paperxxx/ should I can share it with ours with a password. How do you think?
>> CC0727: measured the three things the question turns on before answering. The named IP is a
>> tailnet address, so it cannot be the target of a public name; the static half of a real board
>> was verified portable in the body and dead in its outward links; and the repo holds PHI and
>> secrets, so the served root matters more than the password. Recommended a narrow publish
>> directory behind a Cloudflare tunnel, read-only first, with commenting added later through a
>> default-deny proxy rather than by exposing `serve.py`. The ruling is JL's and is still open.
> JL: I want it can be modified as the real ones, I mean they should just as the local host.
>> CC0727: read-only is rejected, so route ③ is the target and the static-snapshot plan is dropped.
>> Measured what route ③ actually costs and found three preconditions, all now items above: a plain
>> `GET /env.sh` returns the secrets file, `/_board/chat` lets the CLIENT ask for
>> `bypassPermissions`, and the ttyd shell tunnels fine over WebSockets rather than failing closed.
>> The gate belongs in `serve.py`, which has four entry points and no auth flag today. What is
>> still JL's to name is the TIER: board editing live with the shell off, or the shell included.
> JL: could we keep things in a docker, and it will mount onf the board folder only, and will only change the things within that board folder, how do you think? we have platforms/HAIChat-SPACE/haichat-board
>> CC0727: better than gating `serve.py`, because it exposes the program that has no shell. Read the
>> shipped service: the container, the mount and the narrow writes already exist, and the empty
>> `INLAB_BOARD_LIVE` already makes tier A the default by 501-ing chat and terminal. So the plan
>> shrinks to three things: teach discovery to see boards outside `diagram/` (it cannot see the
>> paper board today), mount a skeleton rather than one folder so the 260724 `## Files` widening
>> survives, and add the auth that neither program has. Mount shape and discovery are `QE2`'s;
>> auth and the tunnel stay here.

## Log
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260729 · Redacted machine and account-specific tailnet identifiers from tracked Board history; only generic placeholders remain in source
260727 · JL redirected the vehicle to Docker + `haichat-board`. Read the service: the container, the
       mounted-not-baked SPACE, the `BOARD_SKILL_DIR` escape hatch, and `_target()`'s board-folder
       write vetting all already exist, and `INLAB_BOARD_LIVE: "{}"` already ships tier A by making
       chat and terminal 501. Recorded that the container does nothing for tier B, whose shell would
       run on the host. Remaining gap here is auth, which `boards_api.py` has none of. Mount shape
       and the `diagram/`-only discovery gap were written to `QE2`.
260727 · JL ruled for the live half: the shared board must be editable exactly as on localhost, so
       route ③ is the target and the read-only snapshot plan is dropped. Measured the three
       preconditions (`GET /env.sh` returns 200 and the whole secrets file; `/_board/chat` accepts a
       client-chosen `bypass` scope; ttyd's WebSocket tunnels rather than failing closed) and added
       six items covering the gate, the pinned scope, the tier, the tunnel, and the short path.
260727 · JL asked how to host a board at `paper.jjluo.com/<paper>/` behind a shared password.
       Verified: `<tailscale-ip>` is a tailnet address and cannot back a public name; `board.html`
       is portable in body but has 1019 dead outward links once exported; `jjluo.com` is on
       Cloudflare and `cloudflared` is installed; PHI and secrets make the served root the real
       control. Three items added, state moved to 🟡. Route still unruled.
260724 1324 · Noted: route ③'s vehicle now exists (`boards_api.py` in haichat-inlab, see QE2/QE3); exposure, auth, and attribution stay exactly as open as before
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Opened: the new QE group "putting the board out". The board has always claimed to be for a second reader, yet it lives only on 127.0.0.1
