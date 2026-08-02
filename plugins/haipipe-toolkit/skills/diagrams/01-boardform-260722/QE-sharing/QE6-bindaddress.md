# Which address the board binds to

state: 🟡 PARTIAL
owner: JL
method: separate the shared-source default from the per-machine override and keep every personal address out of shared source

## Opening
Which address should the live board bind to when its reader may be on another machine?

The listener has no built-in authentication, and it fronts both file writes and a real shell.
Loopback is safe but fragile for remote readers, while a wider bind turns a convenience setting into an access decision.
The chosen address and its machine-specific override must agree without leaking personal network details into shared source.
It succeeds when the intended reader reaches the board and everyone else does not.

**Covered elsewhere**: Whether the board goes on a real server, with login and remote writes: that is `QE1`, and this question only owns the local machine's socket. Which process and repo the code runs in: that is `QE3`. What two people editing at once does: that is `QE4`.


## Diagram

```
serve.py has no auth, so the address IS the permission
──────────────────────────────────────────────────────
                        who can reach /_term/ (a real shell)     cost to the reader
① 127.0.0.1  (default)  only this machine                        must forward the port, by hand, every restart
② VS Code forwarded     only that one editor window              two clicks now, two clicks after every restart
③ ssh -L tunnel         only that ssh session                    one flag, but only for whoever opened it
④ tailnet 100.x (live)  every device on the owner's tailnet      nothing; the URL just works
⑤ 0.0.0.0              everything on the local network           nothing, and that is the problem

  ①②③ keep the loopback security model.  ④⑤ trade it for reach.
```

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QE6

## Content
### §1 The bind address is the only access control there is
`serve.py` has no token, no password, and no origin check.
Its own docstring names the loopback bind as the first line of the "deliberately narrow" write endpoint, alongside the `--root` containment and the two allowed kinds of edit.
`/_board/chat` uses the owner's existing Claude login, and `/_term/` opens a real terminal, so any address the server answers on is an address from which someone can run commands as the owner.
This is why the question cannot be settled as a convenience preference: changing the address changes who has a shell.

### §2 Where the setting could live, and what each costs
#### P1. A flag at launch
(explicit, unshared, and forgotten by the next person who starts the server)
`--host` is now implemented and defaults to `127.0.0.1`, so behaviour is unchanged unless someone asks for something else.
Nothing personal is baked into the shared source, which is the property that matters most for a repo other people clone.
The cost is that it must be retyped on every start, and the skill's documented start command does not carry it.

#### P2. An export in `env.sh`
(per-machine and gitignored, but `env.sh` is also the file people copy from each other)
`env.sh` is where this repo already keeps machine-specific values, and it is gitignored, so the reader-facing `HAIPIPE_BOARD_URL` stored there never ships.
`serve.py` does not read that value today, so its bind still arrives through a separate `--host` flag.
The risk is social rather than technical: `env.sh` is the file a new person is told to copy from a colleague, and a copied non-loopback address is a silently widened door.

#### P3. A default in the shared source
(the one option that must not be taken)
A personal tailnet or LAN address committed into `serve.py` would reach every clone of `Tools`.
It is listed here only so the ruling can say plainly that it is excluded.

### §3 What a second person on the same board actually needs
The question in the title is not only about the owner's own reading.
A colleague opening the same board needs a URL that resolves for them, and today every option except a wide bind requires them to have an account on the machine or an editor already attached to it.
That is the same wall `QE1` describes from the hosting side, and this question is the local half of it: what the single machine's socket does, before any decision about a real server.

## Aims
### The committed --host flag
- [x] 🔧 `serve.py` takes an explicit host and still defaults to loopback
      A `--host` flag exists, defaults to `127.0.0.1`, and the startup banner prints a warning line whenever the bind is not loopback.
      Verified on 260726 by starting the server on a tailnet address, confirming the warning and the listening socket, then restarting on the default and confirming loopback again.
      The flag is committed in `Tools`; the personal tailnet address is supplied only at launch and is not part of the shared source.
- [x] 📌 the `--host` flag is committed in `Tools`
      The flag was committed in revision `9eb8ea8e`, so a submodule update cannot remove it.
      Current unrelated working-tree edits to `serve.py` do not own or gate the committed flag.

### The shipped default and the /_term/ gate
- [ ] 🧠 JL rules what the shipped default is, and whether a non-loopback bind is offered at all
      The ruling has to name the default that other people get when they clone `Tools`, and say whether widening it is supported or merely possible.
      JL's leaning on 260726 was to stay local; this line closes when that is a decision rather than a leaning.
- [ ] 🔐 the unauthenticated terminal endpoint is either gated or named as the reason the default stays local
      Right now `/_term/` is the strongest argument against ever widening the bind, and nothing in the skill says so.
      This line closes when either a gate exists or the reasoning is written where someone about to widen the bind will read it.

### One home for the address setting
- [ ] 🗂 the override has exactly one home
      Either the flag alone, or the flag plus an `env.sh` variable that `serve.py` reads, but not two half-implemented paths.
      JL chose `env.sh` on 260729 as this machine's home for the reader-facing URL, represented here as `HAIPIPE_BOARD_URL=http://<tailscale-ip>:5599`.
      The line remains open because `serve.py` still receives its bind through `--host`, so one setting does not yet control both the listener and the emitted URL.
      This line closes when the chosen home is implemented and the other is documented as not supported.
- [x] 📖 the skill stops claiming `127.0.0.1` unconditionally
      `SKILL.md` now distinguishes the reader-facing domain from the listener bind.
      Its view command reads `HAIPIPE_BOARD_URL` and retains loopback only as the safe shared-source fallback.
- [x] 🔀 the two places that emit a URL read the same setting
      `status.py` and `SKILL.md`'s view step now both prefer `HAIPIPE_BOARD_URL`, then the machine-local assignment in the repository's gitignored `env.sh`, then loopback.
      The personal Tailscale IP is therefore handed to this machine's reader without becoming every clone's default.

### Proving a second reader is reached
- [ ] 🧭 the skill's view step stops guessing local against remote from the presence of a socket
      The current test is whether a VS Code IPC socket and a `browser.sh` exist, and on this machine both do while the reader is still on another machine.
      The check that actually decides it is whether a request lands in the server log, and this line closes when the view step verifies reach that way instead of guessing.
      It is written here rather than in `SKILL.md` because this question is open, and an open question's rules do not graduate.
- [ ] 🤝 a second person can open a board without editing anyone's configuration
      This is the acceptance test for the whole question, and it is currently failed by every option that preserves the loopback model.
      It may well be answered by `QE1` instead, in which case this line closes by pointing there.

## States
The committed flag exists and works, its shared-source default is unchanged, and this machine keeps its reader-facing tailnet URL in the gitignored `env.sh`.
JL has chosen the per-machine reader URL, and both link emitters now consume it without requiring the calling shell to source `env.sh`.
The shared-source listener default and whether one setting should also control the bind remain open.
**The running server is on option ④, not option ②.** As of 260727 the live process uses `serve.py --root <repo> --port 5599 --host <tailscale-ip> --daemon`, and both its tailnet and internal loopback listeners return HTTP 200.
This page said until 260727 that the arrangement was loopback-only; that was true when JL said "maybe just use the local version" on 260726 and stopped being true when the server was next started with the flag.
Option ④'s cost is the one written in the diagram: every device admitted to the tailnet can reach `/_term/`.
`--host` still defaults to loopback, so nothing about a clone of `Tools` changed; only this machine's launch and reader-facing URL changed, while one setting still does not control both.
**Before JL chose the tailnet URL, the bind was widened and the emitted URL was not.** JL asked earlier on 260729 whether `<tailscale-ip>` was being used as the host, and it was not: every link handed over that session, both the browser pushes and the closing strips, said `127.0.0.1:5599`.
Three things were verified at that time: the live process listened on both addresses and both returned 200 from the machine itself, `HAIPIPE_BOARD_URL` was unset in the agent's shell, and `SKILL.md`'s push command carried the loopback address literally rather than reading any variable.
At that time a reader off this machine saw a dead link unless the VS Code forward happened to be alive, which is the failure already written in the Lesson below, arriving by a second route.
**JL has now chosen the tailnet URL for this machine.** On 260729 JL said that Board links should bind to the Tailscale IP and should not be handed over as localhost.
The gitignored `env.sh` holds the real `HAIPIPE_BOARD_URL`; tracked files show only `http://<tailscale-ip>:5599`.
Loopback remains an internal fallback listener in the current `serve.py`; it is no longer the address handed to JL.
The shared-source default and the single-setting implementation remain open because a personal Tailscale address must not be committed into the plugin.

- 260726 CC · 🕳 A board that looked broken was never reached at all
      A push of the board URL produced an endlessly loading tab, and the cause was not the board.
      The server log showed zero requests for that board from JL's browser across two pushes, while a leftover tab on the machine's own display polled happily every four seconds.
      At that time `serve.py` bound loopback, JL reached the machine over SSH, and the VS Code forward for 5599 had died when the server was restarted, so the tab was retrying against a port with nothing behind it.
- 260726 CC · 🔧 serve.py grew a --host flag, default unchanged
      Four edits: the flag, the bind using it, a warning line in the banner, and the docstring's "binds 127.0.0.1 only" replaced with what is now true.
      It was exercised on a tailnet address and then put back on loopback at JL's word.
- 260726 JL · ✅ The board opened from JL's laptop, on loopback, after re-forwarding
      JL removed the stale PORTS rows, added 5599 again while the server was listening, and the board loaded.
      The sequence that works is: server listening first, then Add Port, then open or reload the tab.
      Nothing about the bind changed to make this work, which is the point: option ② costs two clicks per restart and gives exactly one person access.
- 260726 JL · 🧭 Leaning is to stay local
      JL raised two objections that shaped this question: other people use this board, and the code is shared, so a personal address must not become part of either.

### Decision Now
- [ ] 🧠 Confirm the shipped default for the bind address
      When someone clones `Tools`, should `serve.py` listen on `127.0.0.1` (loopback only), or offer a wider address?
      JL's leaning on 260726 was loopback; a tick here closes the same row in Items to Finish.
- [ ] 🗂 Decide the single home for the address setting
      Either `--host` flag alone, or the flag plus an `env.sh` variable that `serve.py` reads; not both half-implemented.
      JL chose `env.sh` on 260729 for the reader-facing URL; a tick closes the same row in Items to Finish.

## Files
### The running server and documentation
- `cli/serve.py`
  Holds the bind, the `--host` flag, and the docstring that states the security model. Start here when this question changes.
- `SKILL.md`
  Uses the same machine-local reader URL for browser pushes and documents loopback only as the safe fallback.

### Machine-local settings
- `status.py`
  Resolves an explicit URL, the live environment, or the one `HAIPIPE_BOARD_URL` assignment in root `env.sh`, in that order.
- `env.sh`
  Gitignored and per-machine. It now holds this machine's reader-facing `HAIPIPE_BOARD_URL`; the listener still receives its address separately through `--host`.

## Lesson
A row in the VS Code PORTS panel is not a live tunnel: a User Forwarded entry survives the death of the process it pointed at, so the panel kept showing 5599 as forwarded while nothing was behind it.
Restarting a server silently breaks every hand-made forward that pointed at it, and on a macOS remote nothing re-creates them, because VS Code's process-based port detection does not run there.
The forward binds to whatever is listening at the moment it is added, so the order is fixed: start the server, then Add Port, then open or reload the tab; adding the port first produces a row that looks correct and relays nothing.
Zero requests in the server log is the fastest way to tell "the page is broken" apart from "the page was never fetched"; everything else about the two looks the same.
Opening the URL on the serving machine proves the page renders and proves nothing about whether the reader can see it, so `open` succeeding is not evidence the job is done.
The skill's own view step decides local against Remote-SSH by looking for a VS Code IPC socket and a `browser.sh`, and on this machine both exist while the reader is still remote, so the heuristic picks the wrong branch and the agent reports success into an empty room.

## Glossary
loopback: the `127.0.0.1` address, reachable only from processes on the same machine.
forwarded port: an editor or ssh relay that makes a remote machine's loopback port appear on yours; it dies with the process it was pointed at.
tailnet: the private mesh network Tailscale gives one owner's devices, addressed in the `100.x` range and reachable by those devices only.
`/_term/`: `serve.py`'s terminal endpoint, which opens a real shell on the machine serving the board, with no authentication.

## Discussion
> JL: what if other are using this board as well?
> JL: should we put this into the env.sh? you need to know that the code will be shared with others as well.
> JL: maybe just use the local version, that should be ok.
>> CC0726: put the server back on loopback the same turn. The flag stays in place and defaults to loopback, so nothing changes for anyone who clones Tools, and this question now owns the ruling rather than the running server.

## Log
260802 · The short route `/b/<slug>/<page-id>` is now live on the same 5599 listener as the long `/Tools/...` paths, so the address ruled on here serves both shapes from one bind and one port; checked at 302 on the tailnet address and on loopback, and the route's own design stays `QE2`'s
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260729 · Redacted the machine-specific Tailscale IP from tracked Board history; the real reader URL remains only in gitignored env.sh
260729 · Reader-facing domain now resolves to this machine's Tailscale IP without requiring `source env.sh`: status.py reads only HAIPIPE_BOARD_URL from root env.sh, and the skill's browser-push command consumes the same setting; loopback remains the shared fallback
260729 · JL chose the tailnet URL for this machine. Added `HAIPIPE_BOARD_URL=http://<tailscale-ip>:5599` to the gitignored `env.sh`; the live server was already listening there, so user-facing Board links can stop using localhost without putting a personal address in shared source.
260729 · JL asked whether the tailnet address was being used; it was not. Recorded that the emitted URL is a third setting, separate from the bind: `status.py` reads `HAIPIPE_BOARD_URL` (unset here) and `SKILL.md`'s push hardcodes loopback, so widening the bind on 260727 changed nothing about what a reader is handed. Nothing was set or defaulted, because that home is JL's to rule.
260727 · Corrected a stale claim: this page described the running arrangement as loopback-only,
       while the live process has been started with `--host <tailscale-ip>`, so the machine is on
       option ④. Found while answering `QE1`'s public-hosting question. Default and code unchanged.
260726 1150 · JL re-forwarded 5599 against the live listener and the board opened; recorded as option ② working, plus three lessons on why it had not
260726 1130 · opened after the loopback bind and a dead VS Code forward made a working board look broken; `--host` implemented and the default unchanged; this was the historical pre-commit state, and the flag is committed now
