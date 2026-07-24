# Hosting: local vs server

state: 🔴 OPEN
owner: JL
method: first sort out "who needs to see it", then decide local vs. server

## Question
This board lives only on one machine's `127.0.0.1:5599`. To show it to anyone else — an RA, a collaborator, a meeting projector — how does it get out?

- Why it is hard
  The board is two halves: the static half (`board.html`) can be hosted by anything; the **live half** (comment write-back, chat, terminal) must run on **the machine the files are on**. Putting it out means deciding which half the other person gets.
- What breaks if we leave it
  Today the options are screenshots or crowding around one machine. The board claims to be "for discussing with people, for handing to an RA" — yet the second person literally cannot open it.
- What it affects downstream
  Whether auth is needed, how comments attribute to people, whether outsiders may write to disk — the moment remote writes are allowed, `serve.py`'s narrow interface ("only under `--root`, only two kinds of edits") must be re-audited.

## Boundary
- ✅ This question owns
  **How the board is reached**: local / LAN / server, who can see it, login or not, static export vs. full function.
- ❌ This question does not own
  The board's **content and layout** — that is the `QA` group and `QC2`. Nor whether **work can be done on the board** — that is the `QD` group; this question only owns "where it opens from".

## Diagram
```
                     the static half         the live half (files must be local)
                  board.html               comment write-back · chat · terminal
                  ─────────────            ──────────────────────────────────
① today: local     ✅ 127.0.0.1:5599        ✅ everything works      only you can see it
② static export    ✅ opens anywhere         ❌ all gone             enough for a look
③ full on server   ✅                        ⚠️ needs auth + a write-permission audit   real collaboration
```

## Items to Finish
- [ ] Sort out "who needs to see it, and which half"
      A read-only glance (②) or commenting and working together (③). Different answers, completely different builds.
- [ ] Settle the read-only route
      Static export: `board.html` is self-contained and should open anywhere — but `fig/` and `## Links` relative paths must travel with it; verify once.
- [ ] Settle the bar for the full-function route
      A server deployment needs auth (who may write) and an audit of `serve.py`'s write endpoints under a public network.
- [ ] Decide how comments attribute to people
      Today the signature is browser-side initials of your choosing (any 1–4 uppercase letters). Real multi-user needs more than that.
- [ ] A second person has actually opened it once
      That is the acceptance line: not "theoretically possible" — someone really opened it from another machine and left a comment.

## Where we are
**One route only: local, tunneled out by Remote-SSH.**

- How it opens today
  `serve.py --root <repo root> --port 5599`, bound to `127.0.0.1` only; VS Code Remote-SSH forwards 5599 to the laptop; Simple Browser opens it.
- Why it binds local-only
  `serve.py` has write endpoints (comment write-back, chat, terminal). Binding 0.0.0.0 hands disk writes and terminal spawning to the network — with no auth at all today.
- The static half is already quite independent
  The invariant guarantees "strip every `<script>` and every question plus all body text remains". So the technical bar for read-only distribution is low — what is missing is verification and rules, not capability.
- Route ③ now has a concrete vehicle (260724)
  `haichat-inlab` gained `boards_api.py` (`QE2`/`QE3`): SPACE mounting, board discovery, page serving, comment write-backs. It still binds locally — so nothing about THIS question's decisions (who can reach it, auth, attribution) has changed; but when JL picks route ③, the thing to expose now exists, and it lives inside a service that docker-compose already deploys.

## Files
- `serve.py`
  Bind address, port, write endpoints, and (future) auth all live here.
- `board.html`
  The static-export deliverable itself; `fig/` and `## Links` relative paths must be verified together.

## Log
260724 1324 · Noted: route ③'s vehicle now exists (`boards_api.py` in haichat-inlab, see QE2/QE3) — exposure, auth, and attribution stay exactly as open as before
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Opened: the new QE group "putting the board out". The board has always claimed to be for a second reader, yet it lives only on 127.0.0.1
