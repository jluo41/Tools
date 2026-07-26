# Which address the board binds to

state: 🔴 OPEN
owner: JL
method: keep the shipped default local, then decide separately where a per-machine override is allowed to live

## Question
When the person reading a board is not sitting at the machine that generates it, which address should `serve.py` bind to, and where should that setting live once the code is shared with other people?

`serve.py` binds `127.0.0.1` and has no authentication of any kind, so the bind address is not a convenience setting: it is the entire access control, and `/_term/` behind it is a real shell.
That makes the question awkward in both directions.
Keep it on loopback and anyone working over SSH sees nothing at all until they hand-forward the port, which they must redo every time the server restarts, and which fails silently in a way that looks exactly like a broken board.
Open it wider and every device that can reach the new address can run commands as the owner, on a codebase that ships to other people who will not read the flag before using it.
The setting also has no obvious home: a flag is explicit but has to be retyped, `env.sh` is per-machine and gitignored but is the file everyone copies from a colleague, and a default baked into the shared source is the one place a personal address must never go.

## Boundary
- ✅ Covered here
  **Which address `serve.py` listens on**, what the shipped default is for someone who clones `Tools`, and where a per-machine override lives.
  Who can consequently reach the unauthenticated write and terminal endpoints, since that follows directly from the address.
- ↪ Covered elsewhere
  Whether the board goes on a real server, with login and remote writes: that is `QE1`, and this question only owns the local machine's socket.
  Which process and repo the code runs in: that is `QE3`.
  What two people editing at once does: that is `QE4`.

## Diagram
```
serve.py has no auth, so the address IS the permission
──────────────────────────────────────────────────────
                        who can reach /_term/ (a real shell)     cost to the reader
① 127.0.0.1  (today)    only this machine                        must forward the port, by hand, every restart
② VS Code forwarded     only that one editor window              two clicks now, two clicks after every restart
③ ssh -L tunnel         only that ssh session                    one flag, but only for whoever opened it
④ tailnet 100.x         every device on the owner's tailnet      nothing; the URL just works
⑤ 0.0.0.0              everything on the local network           nothing, and that is the problem

  ①②③ keep the loopback security model.  ④⑤ trade it for reach.
```

## Content
### §1 The bind address is the only access control there is
`serve.py` has no token, no password, and no origin check.
Its own docstring names the loopback bind as the first line of the "deliberately narrow" write endpoint, alongside the `--root` containment and the two allowed kinds of edit.
`/_board/chat` spends the owner's ambient OAuth login, and `/_term/` opens a real terminal, so any address the server answers on is an address from which someone can run commands as the owner.
This is why the question cannot be settled as a convenience preference: changing the address changes who has a shell.

### §2 Where the setting could live, and what each costs
#### P1. A flag at launch
(explicit, unshared, and forgotten by the next person who starts the server)
`--host` is now implemented and defaults to `127.0.0.1`, so behaviour is unchanged unless someone asks for something else.
Nothing personal is baked into the shared source, which is the property that matters most for a repo other people clone.
The cost is that it must be retyped on every start, and the skill's documented start command does not carry it.

#### P2. An export in `env.sh`
(per-machine and gitignored, but `env.sh` is also the file people copy from each other)
`env.sh` is where this repo already keeps machine-specific values, and it is gitignored, so a personal address there never ships.
`serve.py` does not read it today, so this would mean the server growing an environment-variable fallback under the flag.
The risk is social rather than technical: `env.sh` is the file a new person is told to copy from a colleague, and a copied non-loopback address is a silently widened door.

#### P3. A default in the shared source
(the one option that must not be taken)
A personal tailnet or LAN address committed into `serve.py` would reach every clone of `Tools`.
It is listed here only so the ruling can say plainly that it is excluded.

### §3 What a second person on the same board actually needs
The question in the title is not only about the owner's own reading.
A colleague opening the same board needs a URL that resolves for them, and today every option except a wide bind requires them to have an account on the machine or an editor already attached to it.
That is the same wall `QE1` describes from the hosting side, and this question is the local half of it: what the single machine's socket does, before any decision about a real server.

## Items to Finish
- [x] 🔧 `serve.py` takes an explicit host and still defaults to loopback
      A `--host` flag exists, defaults to `127.0.0.1`, and the startup banner prints a warning line whenever the bind is not loopback.
      Verified on 260726 by starting the server on a tailnet address, confirming the warning and the listening socket, then restarting on the default and confirming loopback again.
      The change is uncommitted in the `Tools` submodule, so it is real on this machine and nowhere else.
- [ ] 🧠 JL rules what the shipped default is, and whether a non-loopback bind is offered at all
      The ruling has to name the default that other people get when they clone `Tools`, and say whether widening it is supported or merely possible.
      JL's leaning on 260726 was to stay local; this line closes when that is a decision rather than a leaning.
- [ ] 🗂 the override has exactly one home
      Either the flag alone, or the flag plus an `env.sh` variable that `serve.py` reads, but not two half-implemented paths.
      This line closes when the chosen home is implemented and the other is documented as not supported.
- [ ] 🔐 the unauthenticated terminal endpoint is either gated or named as the reason the default stays local
      Right now `/_term/` is the strongest argument against ever widening the bind, and nothing in the skill says so.
      This line closes when either a gate exists or the reasoning is written where someone about to widen the bind will read it.
- [ ] 📖 the skill stops claiming `127.0.0.1` unconditionally
      `SKILL.md` and the serve section describe the URL as `127.0.0.1:5599` with no mention that a reader off the machine has to do anything at all.
      This line closes when the documented start command and the documented URL agree with whatever this question settles.
- [ ] 🧭 the skill's view step stops guessing local against remote from the presence of a socket
      The current test is whether a VS Code IPC socket and a `browser.sh` exist, and on this machine both do while the reader is still on another machine.
      The check that actually decides it is whether a request lands in the server log, and this line closes when the view step verifies reach that way instead of guessing.
      It is written here rather than in `SKILL.md` because this question is open, and an open question's rules do not graduate.
- [ ] 🤝 a second person can open a board without editing anyone's configuration
      This is the acceptance test for the whole question, and it is currently failed by every option that preserves the loopback model.
      It may well be answered by `QE1` instead, in which case this line closes by pointing there.
- [ ] 📌 the `Tools` change is committed or reverted
      Uncommitted edits to `serve.py` disappear the next time anyone runs `git submodule update`, which would take the flag with them.
      This line closes when JL authorizes a commit in `Tools` or asks for the flag to be dropped.

## Where we are
The flag exists and works, the default is unchanged, and nothing is committed.
The ruling itself is untouched: what the shipped default should be, and where a per-machine override belongs, are both still open, and JL owns them.
The working arrangement today is option ② from the diagram: the server stays on `127.0.0.1:5599` and JL re-forwards port 5599 in VS Code, which was confirmed working on 260726.
That is a per-restart manual step for one person, so it answers the practical need without answering the question.

- 260726 CC · 🕳 A board that looked broken was never reached at all
      A push of the board URL produced an endlessly loading tab, and the cause was not the board.
      The server log showed zero requests for that board from JL's browser across two pushes, while a leftover tab on the machine's own display polled happily every four seconds.
      `serve.py` binds loopback, JL reaches the machine over SSH, and the VS Code forward for 5599 had died when the server was restarted, so the tab was retrying against a port with nothing behind it.
- 260726 CC · 🔧 serve.py grew a --host flag, default unchanged
      Four edits: the flag, the bind using it, a warning line in the banner, and the docstring's "binds 127.0.0.1 only" replaced with what is now true.
      It was exercised on a tailnet address and then put back on loopback at JL's word.
- 260726 JL · ✅ The board opened from JL's laptop, on loopback, after re-forwarding
      JL removed the stale PORTS rows, added 5599 again while the server was listening, and the board loaded.
      The sequence that works is: server listening first, then Add Port, then open or reload the tab.
      Nothing about the bind changed to make this work, which is the point: option ② costs two clicks per restart and gives exactly one person access.
- 260726 JL · 🧭 Leaning is to stay local
      JL raised two objections that shaped this question: other people use this board, and the code is shared, so a personal address must not become part of either.

## Files
- `serve.py`
  Holds the bind, the `--host` flag, and the docstring that states the security model. Start here when this question changes.
- `SKILL.md`
  Documents the start command and the `127.0.0.1:5599` URL, so it goes stale the moment the default moves.
- `env.sh`
  Gitignored, per-machine, and the candidate home for an override in P2. It holds no board setting today.

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
260726 1150 · JL re-forwarded 5599 against the live listener and the board opened; recorded as option ② working, plus three lessons on why it had not
260726 1130 · opened after the loopback bind and a dead VS Code forward made a working board look broken; `--host` implemented, default unchanged, nothing committed
